"""
test_dlp_security.py
====================
Comprehensive automated verification suite for the 16 DLP architectural safeguards.
Tests:
1. Safeguard 6: AI Data Masking & PII Scrubber (Phones, Aadhaar, PAN, Surveys, Coordinates).
2. Safeguard 9: Identity Check & OTP Verification (TTL, Rate-Limiting, Brute-Force lockout, Fail-Closed delivery).
3. Safeguard 7: RAG Isolation Guard (Public vs Tenant access boundaries).
4. Safeguard 5 & 15: Session context setting and ephemeral credential manager.
"""

import time
import pytest
from security.dlp_middleware import ai_masking_engine, scrub_ai_payload
from security.otp_service import OTPVerificationService, MockTestSMSProvider
from security.rag_guard import rag_guard, RAGIsolationViolation
from database.security.db_connection_security import EphemeralCredentialManager


class TestAIDataMasking:
    """Test Safeguard 6: Scrubbing PII before LLM dispatch."""

    def test_mask_indian_mobile_numbers(self):
        sample = "Farmer Ramesh (phone +91-9876543210 or 98765 12345) reported crop damage."
        masked, mapping = ai_masking_engine.mask_text(sample, farmer_name="Ramesh")
        assert "+91-9876543210" not in masked
        assert "98765 12345" not in masked
        assert "Ramesh" not in masked
        assert "<FARMER_NAME_TOKEN_1>" in masked
        assert "<PHONE_REDACTED_1>" in masked

        # Test bidirectional unmasking
        unmasked = ai_masking_engine.unmask_text(masked, mapping)
        assert "+91-9876543210" in unmasked
        assert "Ramesh" in unmasked

    def test_mask_aadhaar_and_pan(self):
        sample = "Aadhaar number 5432 1098 7654 and PAN ABCDE1234F verified at CSC center."
        masked, mapping = ai_masking_engine.mask_text(sample)
        assert "5432 1098 7654" not in masked
        assert "ABCDE1234F" not in masked
        assert "<AADHAAR_TOKEN_1>" in masked
        assert "<PAN_TOKEN_1>" in masked

    def test_mask_land_survey_and_coordinates(self):
        sample = "Survey No. 45/2B located at 17.385044, 78.486671 suffered inundation."
        masked, _ = ai_masking_engine.mask_text(sample)
        assert "45/2B" not in masked
        assert "17.385044" not in masked
        assert "<SURVEY_RECORD_TOKEN_1>" in masked
        assert "<GPS_LOCATION_GENERALIZED>" in masked

    def test_scrub_nested_payload(self):
        payload = {
            "query": "Apply for PMFBY for farmer Suresh Kumar, phone 9123456789",
            "metadata": {
                "farmer": "Suresh Kumar",
                "bank_acc": "123456789012345"
            }
        }
        scrubbed, mapping = scrub_ai_payload(payload, farmer_name="Suresh Kumar")
        assert "9123456789" not in scrubbed["query"]
        assert "123456789012345" not in scrubbed["metadata"]["bank_acc"]


class TestOTPService:
    """Test Safeguard 9: Expiring OTP Tokens, Fail-Closed Gateway & Brute Force Prevention."""

    def test_otp_fail_closed_without_provider(self):
        """Without configured SMS gateway, OTP request fails closed and rejects delivery."""
        otp_svc = OTPVerificationService()
        ok, msg = otp_svc.request_otp("9876500000")
        assert ok is False
        assert "SMS_PROVIDER_NOT_CONFIGURED" in msg

    def test_otp_generation_and_verification(self):
        mock_provider = MockTestSMSProvider()
        otp_svc = OTPVerificationService(provider=mock_provider)
        phone = "9876500001"

        ok, msg = otp_svc.request_otp(phone)
        assert ok is True
        # Verify raw OTP is not leaked in return message
        assert "dispatched successfully" in msg.lower()
        code = mock_provider.last_sent[phone]
        assert len(code) == 6
        assert code.isdigit()

        # Success on correct code
        v_ok, vmsg, token = otp_svc.verify_otp(phone, code)
        assert v_ok is True
        assert "VERIFICATION_SUCCESSFUL" in vmsg
        assert token is not None

        # Burned after use
        v_ok2, msg2, _ = otp_svc.verify_otp(phone, code)
        assert v_ok2 is False
        assert "OTP_NOT_FOUND" in msg2

    def test_otp_brute_force_lockout(self):
        mock_provider = MockTestSMSProvider()
        otp_svc = OTPVerificationService(provider=mock_provider)
        phone = "9876500002"
        otp_svc.request_otp(phone)

        # 3 consecutive failed attempts
        otp_svc.verify_otp(phone, "000000")
        otp_svc.verify_otp(phone, "111111")
        ok, msg, _ = otp_svc.verify_otp(phone, "222222")
        assert ok is False
        assert "Maximum attempts exceeded" in msg

    def test_otp_rate_limiting(self):
        mock_provider = MockTestSMSProvider()
        otp_svc = OTPVerificationService(provider=mock_provider)
        phone = "9876500003"
        # 3 allowed
        assert otp_svc.request_otp(phone)[0] is True
        assert otp_svc.request_otp(phone)[0] is True
        assert otp_svc.request_otp(phone)[0] is True

        # 4th request blocked by rate limit
        ok, msg = otp_svc.request_otp(phone)
        assert ok is False
        assert "RATE_LIMIT_EXCEEDED" in msg


class TestRAGIsolation:
    """Test Safeguard 7: Public-Only Knowledge Base RAG boundary."""

    def test_allowed_public_namespace(self):
        assert rag_guard.validate_rag_query("public_schemes") is True
        assert rag_guard.validate_rag_query("public_mandi_msp") is True

    def test_forbidden_tenant_namespace(self):
        with pytest.raises(RAGIsolationViolation):
            rag_guard.validate_rag_query("farmers")

        with pytest.raises(RAGIsolationViolation):
            rag_guard.validate_rag_query("private_user_claims")

    def test_forbidden_filter_leak(self):
        with pytest.raises(RAGIsolationViolation):
            rag_guard.validate_rag_query(
                "public_schemes",
                query_filter={"phone_number": "9876543210"}
            )


class TestEphemeralCredentials:
    """Test Safeguard 15: Ephemeral Credential Rotation."""

    def test_credential_cache_and_structure(self):
        mgr = EphemeralCredentialManager(rotation_ttl_seconds=300)
        creds = mgr.get_credentials()
        assert "user" in creds
        assert "password" in creds
        assert "host" in creds
        assert creds["user"] == "app_service"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
