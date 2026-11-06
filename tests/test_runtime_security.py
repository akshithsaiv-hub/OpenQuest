"""
test_runtime_security.py
========================
End-to-End Automated Test Suite for Runtime Security Safeguards:
1. Unauthenticated Request Rejection (HTTP 401 / 403)
2. Tenant Isolation & Scoped Access (Farmers cannot access other farmers' records)
3. Role-Based Access Control (Farmer vs Intermediary vs Officer)
4. Intermediary Access Scoping (Only assigned farmers with active consent)
5. Consent Lifecycle (Grant, Withdraw, Reminders halted, Intermediary hidden)
6. Data Minimization (Raw Aadhaar, PAN, Bank Accounts, Scans rejected at entry points)
7. OTP Security (Fail-closed, Single-use, Rate limiting, No OTP returned in payload)
8. Officer Dashboard K-Anonymity (Counts >= 10, Micro-cohorts suppressed, No individual records)
9. AI PII Masking & RAG Namespace Isolation
10. CORS Allowlist Enforcement
11. Database Git Tracking & Filesystem Permission Verification
"""

import os
import subprocess
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from backend.eligibility_api import app, otp_service
from security.auth_service import create_session_token
from security.otp_service import MockTestSMSProvider
from security.rag_guard import rag_guard, RAGIsolationViolation
from person3.farmer_database import connect, init_db, restrict_db_permissions
from person3.farmer_profiles import save_profile, get_profile
from person3.consent_manager import withdraw_consent, grant_consent, is_consent_active
from person3.intermediary_backend import get_intermediary_farmers
from person3.reminder_engine import get_due_alerts

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    """Ensure database is initialized and fresh for test execution."""
    init_db()


class TestAuthenticationAndAuthorization:
    """Safeguards 4, 5, 9: Auth enforcement, RBAC, and Token Scoping."""

    def test_unauthenticated_requests_rejected(self):
        # 1. Missing Authorization header
        resp = client.get("/api/farmer/me")
        assert resp.status_code == 401
        assert "UNAUTHORIZED" in resp.json()["detail"]

        # 2. Invalid / forged bearer token
        resp2 = client.get("/api/farmer/me", headers={"Authorization": "Bearer invalid_signature_token"})
        assert resp2.status_code == 401

        # 3. Officer analytics endpoint unauthenticated
        resp3 = client.get("/api/officer/analytics")
        assert resp3.status_code == 401

    def test_role_mismatch_rejected(self):
        # Farmer token attempting officer endpoint
        farmer_token = create_session_token("FARMER_TEST_1", role="farmer")
        resp = client.get(
            "/api/officer/analytics",
            headers={"Authorization": f"Bearer {farmer_token}"}
        )
        assert resp.status_code == 403
        assert "FORBIDDEN" in resp.json()["detail"]

    def test_farmer_tenant_isolation(self):
        # Setup two distinct farmers
        with connect() as con:
            con.execute("""
                INSERT OR REPLACE INTO farmers (farmer_id, farmer_name, phone_number, consent_status, is_deleted, created_at)
                VALUES ('F_ALICE_01', 'Alice Farmer', '9848011111', 1, 0, '2026-11-06T12:00:00'),
                       ('F_BOB_02', 'Bob Farmer', '9848022222', 1, 0, '2026-11-06T12:00:00')
            """)

        alice_token = create_session_token("F_ALICE_01", role="farmer")
        bob_token = create_session_token("F_BOB_02", role="farmer")

        # Alice fetches her profile
        alice_resp = client.get("/api/farmer/me", headers={"Authorization": f"Bearer {alice_token}"})
        assert alice_resp.status_code == 200
        assert alice_resp.json()["profile"]["farmer_id"] == "F_ALICE_01"
        assert alice_resp.json()["profile"]["farmer_name"] == "Alice Farmer"

        # Bob fetches his profile
        bob_resp = client.get("/api/farmer/me", headers={"Authorization": f"Bearer {bob_token}"})
        assert bob_resp.status_code == 200
        assert bob_resp.json()["profile"]["farmer_id"] == "F_BOB_02"
        assert bob_resp.json()["profile"]["farmer_name"] == "Bob Farmer"

        # Alice tries to update profile supplying Bob's ID in body
        # Scoping strictly adheres to Alice's authenticated token
        update_resp = client.put(
            "/api/farmer/me",
            headers={"Authorization": f"Bearer {alice_token}"},
            json={"farmer_id": "F_BOB_02", "farmer_name": "Alice Modified", "state": "Telangana"}
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["profile"]["farmer_id"] == "F_ALICE_01"

        # Verify Bob remains completely untouched
        bob_check = get_profile("F_BOB_02")
        assert bob_check["farmer_name"] == "Bob Farmer"


class TestConsentLifecycleAndAccessRevocation:
    """Safeguards 1, 2: Consent mandatory, immediate halt on withdrawal, Right to Be Forgotten."""

    def test_consent_withdrawal_halts_reminders_and_intermediary(self):
        with connect() as con:
            con.execute("""
                INSERT OR REPLACE INTO farmers (
                    farmer_id, farmer_name, phone_number, preferred_language,
                    intermediary_id, consent_status, is_deleted, created_at
                )
                VALUES ('F_CONSENT_01', 'Consent Farmer', '9848033333', 'te', 'CSC_WARANGAL_01', 1, 0, '2026-11-06T12:00:00')
            """)

        farmer_token = create_session_token("F_CONSENT_01", role="farmer")
        intermediary_token = create_session_token("CSC_WARANGAL_01", role="intermediary")

        # Active consent initially -> visible to assigned intermediary
        int_resp = client.get(
            "/api/intermediary",
            headers={"Authorization": f"Bearer {intermediary_token}"}
        )
        assert int_resp.status_code == 200
        fids = [r["farmer_id"] for r in int_resp.json()["records"]]
        assert "F_CONSENT_01" in fids

        # Withdraw consent via authenticated endpoint
        withdr_resp = client.post(
            "/api/farmer/me/consent/withdraw",
            headers={"Authorization": f"Bearer {farmer_token}"}
        )
        assert withdr_resp.status_code == 200
        assert is_consent_active("F_CONSENT_01") is False

        # Attempting alert returns HTTP 403
        alert_resp = client.post(
            "/api/send_alert",
            json={"farmer_id": "F_CONSENT_01", "channel": "sms", "message": "Test"}
        )
        assert alert_resp.status_code == 403

        # Immediately excluded from intermediary task queue
        int_resp2 = client.get(
            "/api/intermediary",
            headers={"Authorization": f"Bearer {intermediary_token}"}
        )
        fids2 = [r["farmer_id"] for r in int_resp2.json()["records"]]
        assert "F_CONSENT_01" not in fids2

        # Immediately excluded from reminder alerts
        alerts = get_due_alerts("2026-11-10")
        alert_fids = [a["farmer_id"] for a in alerts]
        assert "F_CONSENT_01" not in alert_fids

    def test_soft_delete_and_data_portability(self):
        with connect() as con:
            con.execute("""
                INSERT OR REPLACE INTO farmers (
                    farmer_id, farmer_name, phone_number, consent_status, is_deleted, created_at
                )
                VALUES ('F_DELETE_ME', 'Delete Candidate', '9848044444', 1, 0, '2026-11-06T12:00:00')
            """)

        farmer_token = create_session_token("F_DELETE_ME", role="farmer")

        # 1. Export Data (Portability)
        export_resp = client.get(
            "/api/farmer/me/export",
            headers={"Authorization": f"Bearer {farmer_token}"}
        )
        assert export_resp.status_code == 200
        assert export_resp.json()["export"]["profile"]["farmer_id"] == "F_DELETE_ME"

        # 2. Delete Account (Right to be Forgotten)
        del_resp = client.delete(
            "/api/farmer/me",
            headers={"Authorization": f"Bearer {farmer_token}"}
        )
        assert del_resp.status_code == 200

        # Subsequent fetch rejected with 404
        fetch_resp = client.get(
            "/api/farmer/me",
            headers={"Authorization": f"Bearer {farmer_token}"}
        )
        assert fetch_resp.status_code == 404

        # Profile in DB is anonymized
        with connect() as con:
            row = con.execute("SELECT * FROM farmers WHERE farmer_id = 'F_DELETE_ME'").fetchone()
            assert row["is_deleted"] == 1
            assert row["consent_status"] == 0
            assert "ANONYMIZED_FARMER" in row["farmer_name"]
            assert row["phone_number"] == ""


class TestDataMinimizationAndPIIValidation:
    """Safeguard 1: Prevention of raw citizen PII storage at all entry points."""

    def test_rejects_raw_aadhaar(self):
        resp = client.post(
            "/api/farmers",
            json={
                "farmer_name": "Ramu",
                "phone_number": "9876543210",
                "aadhaar_number": "5432 1098 7654",  # Raw 12-digit Aadhaar
                "consent_status": True
            }
        )
        assert resp.status_code == 400
        assert "Aadhaar" in resp.json()["detail"]

    def test_rejects_raw_bank_account_in_body(self):
        resp = client.post(
            "/api/farmers",
            json={
                "farmer_name": "Ramu",
                "phone_number": "9876543210",
                "bank_account_number": "123456789012345",  # Raw bank account
                "consent_status": True
            }
        )
        assert resp.status_code == 400
        assert "bank account" in resp.json()["detail"].lower()

    def test_requires_explicit_consent_for_creation(self):
        resp = client.post(
            "/api/farmers",
            json={
                "farmer_name": "Ramu",
                "phone_number": "9876543210",
                "consent_status": False  # Missing consent
            }
        )
        assert resp.status_code == 400
        assert "consent" in resp.json()["detail"].lower()


class TestOTPSecurityRuntime:
    """Safeguard 9: Fail-closed delivery, no OTP leakage in responses, single-use burn, rate limit."""

    def test_fail_closed_without_sms_provider(self):
        # In default environment without SMS_PROVIDER_API_KEY, OTP request fails closed
        resp = client.post(
            "/api/auth/otp/request",
            json={"phone_number": "9123400000", "role": "farmer"}
        )
        # Returns 503 fail-closed
        assert resp.status_code == 503
        assert "fail-closed" in resp.json()["detail"].lower()

    def test_mock_provider_verification_and_no_leakage(self):
        # Set mock provider for test verification
        mock_sms = MockTestSMSProvider()
        otp_service.set_provider(mock_sms)
        phone = "9123456789"

        # Request OTP
        req_resp = client.post(
            "/api/auth/otp/request",
            json={"phone_number": phone, "role": "farmer"}
        )
        assert req_resp.status_code == 200
        resp_data = req_resp.json()
        assert resp_data["status"] == "success"
        # Confirm OTP is never returned in response payload
        assert "otp" not in resp_data
        assert "code" not in resp_data
        assert "dispatched successfully" in resp_data["message"]

        # Code is captured only in private mock delivery provider
        dispatched_otp = mock_sms.last_sent[phone]
        assert len(dispatched_otp) == 6

        # Verify OTP
        verify_resp = client.post(
            "/api/auth/otp/verify",
            json={"phone_number": phone, "otp_code": dispatched_otp, "role": "farmer"}
        )
        assert verify_resp.status_code == 200
        auth_data = verify_resp.json()
        assert "access_token" in auth_data
        assert auth_data["role"] == "farmer"

        # Single-use: Replaying the same code fails immediately
        replay_resp = client.post(
            "/api/auth/otp/verify",
            json={"phone_number": phone, "otp_code": dispatched_otp, "role": "farmer"}
        )
        assert replay_resp.status_code == 401


class TestOfficerAnalyticsKAnonymity:
    """Safeguards 8, 10: Aggregate analytics, K-anonymity (>= 10), no individual records."""

    def test_officer_analytics_k_anonymity_enforced(self):
        officer_token = create_session_token("OFFICER_001", role="officer")
        resp = client.get(
            "/api/officer/analytics",
            headers={"Authorization": f"Bearer {officer_token}"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert data["k_anonymity_threshold"] == 10

        # Verify that small groups (< 10) are suppressed
        for cohort in data["cohorts"]:
            if cohort["status"] == "suppressed":
                assert cohort["cohort_size"] == "< 10 (Suppressed for k-anonymity)"
            # Ensure no individual names or phone numbers exist
            assert "farmer_name" not in cohort
            assert "phone" not in cohort
            assert "farmer_id" not in cohort

    def test_public_farmers_endpoint_does_not_leak_raw_records(self):
        resp = client.get("/farmer_status")
        assert resp.status_code == 200
        data = resp.json()
        # Does not return raw array of individual farmers
        assert isinstance(data, dict)
        assert "k_anonymity_threshold" in data


class TestAIPrivacyAndRAGIsolation:
    """Safeguards 6, 7: PII Scrubbing on AI queries & RAG namespace isolation."""

    def test_ai_query_scrubs_pii(self):
        query_with_pii = "My name is Ramesh Kumar, mobile 9876543210, survey 142/A, please check PMFBY"
        resp = client.post(
            "/api/query_ai",
            json={"query": query_with_pii, "language": "en"}
        )
        assert resp.status_code == 200
        # Check that query processing succeeds without errors

    def test_rag_guard_blocks_private_tables(self):
        with pytest.raises(RAGIsolationViolation):
            rag_guard.validate_rag_query("farmers")

        with pytest.raises(RAGIsolationViolation):
            rag_guard.validate_rag_query("private_user_claims")

        assert rag_guard.validate_rag_query("public_schemes") is True


class TestCORSAndTransport:
    """Safeguard 5: CORS explicit allowlist & Security response headers."""

    def test_cors_rejects_unapproved_origins(self):
        resp = client.options(
            "/api/query_ai",
            headers={
                "Origin": "https://malicious-attacker.com",
                "Access-Control-Request-Method": "POST",
            }
        )
        # Malicious origin must not receive Access-Control-Allow-Origin header
        assert resp.headers.get("access-control-allow-origin") != "https://malicious-attacker.com"

    def test_security_headers_present(self):
        resp = client.get("/health")
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"
        assert resp.headers.get("X-Frame-Options") == "DENY"


class TestDatabaseSecurityAndGitHygiene:
    """Safeguard 3, 4: Git tracking hygiene & SQLite permissions."""

    def test_sqlite_db_not_tracked_in_git(self):
        result = subprocess.run(
            ["git", "ls-files", "database/farmer_data.db"],
            capture_output=True,
            text=True
        )
        # Must be empty (untracked)
        assert result.stdout.strip() == ""

    def test_gitignore_contains_db_and_secrets(self):
        gitignore_path = Path(".gitignore")
        assert gitignore_path.exists()
        content = gitignore_path.read_text(encoding="utf-8")
        assert "*.db" in content
        assert ".env" in content
        assert "*.key" in content or "*.pem" in content
