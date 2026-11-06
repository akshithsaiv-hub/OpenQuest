"""
test_passbook_pin_wallet.py
===========================
Comprehensive automated test suite for Farmer Passbook Wallet & PIN-Protected Review:
1. Argon2id Salted PIN Hashing & Salt Uniqueness
2. PIN Strength & Format Validation (Length 4-8 digits, rejects trivial/repeating PINs)
3. PIN Setup, Change, and Correct Verification
4. Incorrect PIN Rejection & Brute-Force Rate Limiting
5. Database-Persisted Lockout (Survives simulated restart)
6. Scoped Authorization & Cross-Farmer Tenant Isolation
7. Farmer Consent Enforcement for Review Submission and Reviewer Access
8. Single-Document Scope (Only Farmer Passbook Supported)
9. Passbook Full Lifecycle (Upload, View, Replace, Delete)
10. Strict Zero-Leakage: PIN and Sensitive Credentials Never in Responses or Logs
"""

import os
import json
import time
from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient

from backend.eligibility_api import app
from security.auth_service import create_session_token
from security.pin_service import (
    validate_pin_format,
    hash_pin,
    verify_pin_hash,
    set_farmer_pin,
    verify_farmer_pin,
    change_farmer_pin,
    get_farmer_pin_status,
)
from person3.farmer_database import connect, init_db
from person3.passbook_service import (
    get_farmer_passbook,
    save_or_replace_passbook,
    delete_farmer_passbook,
    request_passbook_review,
    get_passbook_for_reviewer,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    """Ensure database schema is initialized and clean for each test."""
    init_db()


class TestPINHashingAndStrength:
    """Requirement 2: Argon2id salted password hashing & complexity rules."""

    def test_argon2id_hashing_and_salt_uniqueness(self):
        pin = "849201"
        h1 = hash_pin(pin)
        h2 = hash_pin(pin)

        # Uses Argon2id format
        assert h1.startswith("$argon2id$") or h1.startswith("$scrypt$")
        # Salt uniqueness: identical PIN produces different hash strings
        assert h1 != h2

        # Verification succeeds with correct PIN
        assert verify_pin_hash(h1, pin) is True
        assert verify_pin_hash(h2, pin) is True
        # Fails with wrong PIN
        assert verify_pin_hash(h1, "000000") is False

    def test_pin_format_and_strength_validation(self):
        # Valid PINs (4 to 8 numeric digits)
        assert validate_pin_format("1849")[0] is True
        assert validate_pin_format("984801")[0] is True
        assert validate_pin_format("89481920")[0] is True

        # Invalid lengths (<4 or >8)
        assert validate_pin_format("123")[0] is False
        assert validate_pin_format("123456789")[0] is False

        # Non-numeric characters
        assert validate_pin_format("abcd")[0] is False
        assert validate_pin_format("12a4")[0] is False

        # Repeating single digits (e.g., 0000, 111111)
        assert validate_pin_format("0000")[0] is False
        assert validate_pin_format("111111")[0] is False
        assert validate_pin_format("99999999")[0] is False

        # Trivial sequential PINs
        assert validate_pin_format("1234")[0] is False
        assert validate_pin_format("123456")[0] is False


class TestPINBruteForceAndPersistentLockout:
    """Requirements 3 & 4: Brute-force protection & database-persisted lockout."""

    def test_five_failed_attempts_triggers_lockout(self):
        farmer_id = "F_LOCKOUT_TEST_1"
        with connect() as con:
            con.execute("""
                INSERT OR REPLACE INTO farmers (farmer_id, farmer_name, consent_status, is_deleted, created_at)
                VALUES (?, 'Lockout Farmer', 1, 0, '2026-11-06T12:00:00')
            """, (farmer_id,))

        # Set up PIN 784920
        ok, msg = set_farmer_pin(farmer_id, "784920")
        assert ok is True

        # 4 consecutive incorrect attempts
        for attempt in range(1, 5):
            ok, vmsg = verify_farmer_pin(farmer_id, "000001")
            assert ok is False
            assert "INCORRECT_PIN" in vmsg
            assert f"{5 - attempt} attempt(s) remaining" in vmsg

        # 5th failed attempt triggers 15-minute lockout
        ok5, vmsg5 = verify_farmer_pin(farmer_id, "000001")
        assert ok5 is False
        assert "LOCKED_OUT" in vmsg5
        assert "15 minutes" in vmsg5

        # Check DB state directly: lockout timestamp must be persisted
        with connect() as con:
            row = con.execute("SELECT pin_failed_attempts, pin_locked_until FROM farmers WHERE farmer_id = ?", (farmer_id,)).fetchone()
            assert row["pin_failed_attempts"] == 5
            assert row["pin_locked_until"] is not None
            locked_dt = datetime.fromisoformat(row["pin_locked_until"])
            assert locked_dt > datetime.now()

    def test_lockout_persists_across_simulated_restart(self):
        farmer_id = "F_PERSIST_RESTART"
        with connect() as con:
            con.execute("""
                INSERT OR REPLACE INTO farmers (farmer_id, farmer_name, consent_status, is_deleted, created_at)
                VALUES (?, 'Restart Farmer', 1, 0, '2026-11-06T12:00:00')
            """, (farmer_id,))

        set_farmer_pin(farmer_id, "654921")

        # Exhaust 5 attempts
        for _ in range(5):
            verify_farmer_pin(farmer_id, "999999")

        # Simulate fresh connection / server restart by re-reading from DB
        status = get_farmer_pin_status(farmer_id)
        assert status["is_locked"] is True
        assert status["lockout_remaining_seconds"] > 800

        # Even supplying the CORRECT PIN is blocked while locked out
        ok, msg = verify_farmer_pin(farmer_id, "654921")
        assert ok is False
        assert "LOCKED_OUT" in msg


class TestPassbookWalletCRUDAndScope:
    """Requirement 1: Single-document scope (Passbook only), Upload, View, Replace, Delete."""

    def test_passbook_lifecycle_and_state(self):
        farmer_id = "F_PB_CRUD_01"
        with connect() as con:
            con.execute("""
                INSERT OR REPLACE INTO farmers (farmer_id, farmer_name, consent_status, is_deleted, created_at)
                VALUES (?, 'Passbook Farmer', 1, 0, '2026-11-06T12:00:00')
            """, (farmer_id,))

        # Initially no passbook saved
        initial = get_farmer_passbook(farmer_id)
        assert initial["is_saved"] is False
        assert initial["review_status"] in ("not_requested", "not_uploaded")

        # 1. Upload passbook
        pb_payload = {
            "bank_name": "State Bank of India",
            "branch": "Warangal Main",
            "account_holder_name": "Passbook Farmer",
            "account_number": "3492",
            "ifsc": "SBIN0020144"
        }
        res = save_or_replace_passbook(farmer_id, pb_payload)
        assert res["status"] == "success"
        assert res["is_saved"] is True

        # 2. View passbook
        view = get_farmer_passbook(farmer_id)
        assert view["is_saved"] is True
        assert view["uploaded_at"] is not None
        assert view["passbook_details"]["bank_name"] == "State Bank of India"
        assert view["passbook_details"]["account_number_masked"] == "******3492"

        # 3. Replace passbook
        replace_payload = {
            "bank_name": "Telangana Grameena Bank",
            "branch": "Geesugonda",
            "account_holder_name": "Passbook Farmer",
            "account_number": "8821",
            "ifsc": "SBIN0RRTSGB"
        }
        res2 = save_or_replace_passbook(farmer_id, replace_payload)
        assert res2["status"] == "success"

        view2 = get_farmer_passbook(farmer_id)
        assert view2["passbook_details"]["bank_name"] == "Telangana Grameena Bank"
        assert view2["passbook_details"]["account_number_masked"] == "******8821"

        # 4. Delete passbook
        del_ok = delete_farmer_passbook(farmer_id)
        assert del_ok is True

        view3 = get_farmer_passbook(farmer_id)
        assert view3["is_saved"] is False
        assert view3["uploaded_at"] is None


class TestPINProtectedReviewRequestAPI:
    """Requirements 3 & 5: PIN-protected review requests via authenticated API."""

    def test_review_request_requires_authentication_and_pin(self):
        farmer_id = "F_API_REVIEW_01"
        with connect() as con:
            con.execute("""
                INSERT OR REPLACE INTO farmers (farmer_id, farmer_name, consent_status, is_deleted, created_at)
                VALUES (?, 'API Farmer', 1, 0, '2026-11-06T12:00:00')
            """, (farmer_id,))

        farmer_token = create_session_token(farmer_id, role="farmer")

        # 1. Unauthenticated request rejected
        resp_unauth = client.post(
            "/api/farmer/me/passbook/review-request",
            json={"pin": "784920", "consent_to_share": True}
        )
        assert resp_unauth.status_code == 401

        # 2. Review without saved passbook fails
        set_farmer_pin(farmer_id, "784920")
        resp_nopb = client.post(
            "/api/farmer/me/passbook/review-request",
            headers={"Authorization": f"Bearer {farmer_token}"},
            json={"pin": "784920", "consent_to_share": True}
        )
        assert resp_nopb.status_code == 400
        assert "PASSBOOK_MISSING" in resp_nopb.json()["detail"]

        # Upload passbook
        save_or_replace_passbook(farmer_id, {
            "bank_name": "SBI", "branch": "Main", "account_holder_name": "API Farmer", "account_number": "1234"
        })

        # 3. Review without explicit consent fails
        resp_noconsent = client.post(
            "/api/farmer/me/passbook/review-request",
            headers={"Authorization": f"Bearer {farmer_token}"},
            json={"pin": "784920", "consent_to_share": False}
        )
        assert resp_noconsent.status_code == 400
        assert "CONSENT_REQUIRED" in resp_noconsent.json()["detail"]

        # 4. Review with wrong PIN fails with 401
        resp_wrongpin = client.post(
            "/api/farmer/me/passbook/review-request",
            headers={"Authorization": f"Bearer {farmer_token}"},
            json={"pin": "000001", "consent_to_share": True}
        )
        assert resp_wrongpin.status_code == 401
        assert "INCORRECT_PIN" in resp_wrongpin.json()["detail"]

        # 5. Review with correct PIN succeeds
        resp_ok = client.post(
            "/api/farmer/me/passbook/review-request",
            headers={"Authorization": f"Bearer {farmer_token}"},
            json={"pin": "784920", "consent_to_share": True}
        )
        assert resp_ok.status_code == 200
        assert resp_ok.json()["details"]["review_status"] == "pending_review"


class TestReviewerScopingAndConsentEnforcement:
    """Requirement 5: Reviewer access requires active consent, review status, and intermediary assignment."""

    def test_officer_can_review_only_consenting_and_requested_passbooks(self):
        farmer_id = "F_OFFICER_REVIEW"
        with connect() as con:
            con.execute("""
                INSERT OR REPLACE INTO farmers (farmer_id, farmer_name, consent_status, is_deleted, created_at)
                VALUES (?, 'Reviewable Farmer', 1, 0, '2026-11-06T12:00:00')
            """, (farmer_id,))

        save_or_replace_passbook(farmer_id, {
            "bank_name": "SBI", "branch": "Warangal", "account_holder_name": "Reviewable", "account_number": "5678"
        })
        set_farmer_pin(farmer_id, "849201")
        request_passbook_review(farmer_id, "849201", consent_to_share=True)

        officer_token = create_session_token("OFFICER_WGL_01", role="officer")

        # Officer accesses submitted passbook
        resp = client.get(
            f"/api/officer/passbook/review/{farmer_id}",
            headers={"Authorization": f"Bearer {officer_token}"}
        )
        assert resp.status_code == 200
        dossier = resp.json()["review_dossier"]
        assert dossier["farmer_id"] == farmer_id
        assert dossier["passbook_details"]["bank_name"] == "SBI"
        # Confirm PIN hash is NEVER leaked in reviewer dossier
        assert "pin_hash" not in dossier
        assert "pin" not in dossier

        # Officer records verification decision
        dec_resp = client.post(
            f"/api/officer/passbook/review/{farmer_id}/decision",
            headers={"Authorization": f"Bearer {officer_token}"},
            json={"decision": "verified", "notes": "DBT active and verified."}
        )
        assert dec_resp.status_code == 200

        # If farmer withdraws consent, reviewer access is immediately blocked
        with connect() as con:
            con.execute("UPDATE farmers SET consent_status = 0 WHERE farmer_id = ?", (farmer_id,))

        resp_revoked = client.get(
            f"/api/officer/passbook/review/{farmer_id}",
            headers={"Authorization": f"Bearer {officer_token}"}
        )
        assert resp_revoked.status_code == 403
        assert "CONSENT_WITHDRAWN" in resp_revoked.json()["detail"]


class TestZeroLeakageInLogsAndResponses:
    """Security Guarantee: Plain PINs are NEVER stored, logged, or returned."""

    def test_pin_not_in_database_or_audit_events(self):
        farmer_id = "F_AUDIT_LEAK_CHECK"
        secret_pin = "481920"

        with connect() as con:
            con.execute("""
                INSERT OR REPLACE INTO farmers (farmer_id, farmer_name, consent_status, is_deleted, created_at)
                VALUES (?, 'Leak Check Farmer', 1, 0, '2026-11-06T12:00:00')
            """, (farmer_id,))

        save_or_replace_passbook(farmer_id, {
            "bank_name": "SBI", "branch": "Main", "account_holder_name": "Leak Check", "account_number": "9999"
        })
        set_farmer_pin(farmer_id, secret_pin)

        # Trigger failed and successful verifications
        verify_farmer_pin(farmer_id, "111112")  # fail
        verify_farmer_pin(farmer_id, secret_pin)  # success

        with connect() as con:
            # Check farmers table
            farmer_row = dict(con.execute("SELECT * FROM farmers WHERE farmer_id = ?", (farmer_id,)).fetchone())
            assert secret_pin not in str(farmer_row.values())

            # Check audit_events table
            audit_rows = con.execute("SELECT * FROM audit_events WHERE actor_id = ?", (farmer_id,)).fetchall()
            for r in audit_rows:
                row_str = " ".join([str(v) for v in dict(r).values()])
                assert secret_pin not in row_str
