"""
test_person3.py
================
Comprehensive automated test suite for Person 3 Backend Services.
Farmer Assistance System - Hackathon Edition.

Tests all 12 key scenarios using fictional farmer test data:
1. Successful farmer registration.
2. Registration without consent (rejection).
3. Duplicate farmer ID prevention.
4. Farmer profile retrieval and alias compatibility.
5. Farmer profile update.
6. Missing document detection.
7. Complete document readiness.
8. Bank-name similarity detection (RapidFuzz / fallback).
9. Insurance claim-window reminder prioritisation.
10. Expired deadline handling.
11. Consent withdrawal and reminder exclusion.
12. CSC/FPO Intermediary filtering and prioritisation.
"""

import os
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from person3.farmer_database import init_db, connect
from person3.farmer_profiles import (
    save_profile,
    get_profile,
    update_profile,
    search_farmer,
)
from person3.consent_manager import (
    withdraw_consent,
    grant_consent,
    is_consent_active,
)
from person3.document_checker import (
    normalize_name,
    check_name_match,
    check_documents,
)
from person3.reminder_engine import (
    parse_date,
    is_deadline_expired,
    get_due_alerts,
    get_expired_deadlines,
)
from person3.intermediary_backend import (
    get_intermediary_farmers,
)

# Test SQLite file in a test directory
TEST_DB_PATH = PROJECT_ROOT / "database" / "test_farmer_data.db"


class Person3BackendTestSuite(unittest.TestCase):
    """Unit and Integration Test cases for Person 3 modules."""

    @classmethod
    def setUpClass(cls):
        """Prepare clean test database environment."""
        if TEST_DB_PATH.exists():
            try:
                TEST_DB_PATH.unlink()
            except Exception:
                pass
        init_db(TEST_DB_PATH)

    @classmethod
    def tearDownClass(cls):
        """Clean up test database."""
        if TEST_DB_PATH.exists():
            try:
                TEST_DB_PATH.unlink()
            except Exception:
                pass

    def setUp(self):
        """Reset farmers table before each test."""
        with connect(TEST_DB_PATH) as con:
            con.execute("DELETE FROM farmers;")
            con.commit()

    # -------------------------------------------------------------------------
    # SCENARIO 1: Successful farmer registration
    # -------------------------------------------------------------------------
    def test_01_successful_farmer_registration(self):
        """Test registration of a valid farmer profile with explicit consent."""
        fictional_farmer = {
            "farmer_id": "TEST_F101",
            "farmer_name": "Suresh Reddy",
            "phone_number": "9123456780",
            "preferred_language": "Telugu",
            "intermediary_id": "CSC_TEL_01",
            "consent_status": True,
            "uploaded_documents": {"Aadhaar": True, "Land Records": True},
            "bank_account_name": "Suresh Reddy",
        }
        profile = save_profile(fictional_farmer, db_path=TEST_DB_PATH)

        self.assertIsNotNone(profile)
        self.assertEqual(profile["farmer_id"], "TEST_F101")
        self.assertEqual(profile["farmer_name"], "Suresh Reddy")
        self.assertTrue(profile["consent_status"])
        self.assertIn("Aadhaar", profile["uploaded_documents"])
        self.assertTrue(profile["uploaded_documents"]["Aadhaar"])

    # -------------------------------------------------------------------------
    # SCENARIO 2: Registration without consent
    # -------------------------------------------------------------------------
    def test_02_registration_without_consent(self):
        """Test that profile creation is rejected when consent is missing or False."""
        no_consent_farmer = {
            "farmer_id": "TEST_F102",
            "farmer_name": "Lakshmi Devi",
            "phone_number": "9123456781",
            "consent_status": False,  # No consent
        }
        with self.assertRaises(ValueError) as ctx:
            save_profile(no_consent_farmer, db_path=TEST_DB_PATH)
        self.assertIn("Consent is required", str(ctx.exception))

        # Verify not in DB
        self.assertIsNone(get_profile("TEST_F102", db_path=TEST_DB_PATH))

    # -------------------------------------------------------------------------
    # SCENARIO 3: Duplicate farmer ID prevention
    # -------------------------------------------------------------------------
    def test_03_duplicate_farmer_id(self):
        """Test that registering a duplicate farmer ID is strictly prevented."""
        farmer = {
            "farmer_id": "TEST_DUP01",
            "farmer_name": "Anil Rao",
            "phone_number": "9888877770",
            "consent_status": True,
        }
        # First registration must succeed
        save_profile(farmer, db_path=TEST_DB_PATH)

        # Second registration with the same farmer_id must raise ValueError
        with self.assertRaises(ValueError) as ctx:
            save_profile(farmer, db_path=TEST_DB_PATH)
        self.assertIn("already exists", str(ctx.exception))

    # -------------------------------------------------------------------------
    # SCENARIO 4: Farmer profile retrieval
    # -------------------------------------------------------------------------
    def test_04_farmer_profile_retrieval(self):
        """Test retrieving and searching profile by farmer_id."""
        farmer = {
            "farmer_id": "TEST_F104",
            "farmer_name": "Venkatesh Rao",
            "phone_number": "9777766660",
            "preferred_language": "Telugu",
            "intermediary_id": "FPO_AP_02",
            "consent_status": True,
            "uploaded_documents": {"Aadhaar": True},
            "bank_account_name": "Venkatesh Rao",
        }
        save_profile(farmer, db_path=TEST_DB_PATH)

        retrieved = get_profile("TEST_F104", db_path=TEST_DB_PATH)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["farmer_id"], "TEST_F104")
        self.assertEqual(retrieved["name"], "Venkatesh Rao")  # Check alias
        self.assertEqual(retrieved["phone"], "9777766660")    # Check alias

        # Test search function
        searched = search_farmer("TEST_F104", db_path=TEST_DB_PATH)
        self.assertEqual(searched["farmer_id"], "TEST_F104")

        # Test non-existent ID
        self.assertIsNone(search_farmer("NON_EXISTENT_ID", db_path=TEST_DB_PATH))

    # -------------------------------------------------------------------------
    # SCENARIO 5: Farmer profile update
    # -------------------------------------------------------------------------
    def test_05_farmer_profile_update(self):
        """Test updating existing farmer details (e.g. adding documents & updating phone)."""
        farmer = {
            "farmer_id": "TEST_F105",
            "farmer_name": "Kavitha Sharma",
            "phone_number": "9000011111",
            "consent_status": True,
            "uploaded_documents": {"Aadhaar": True},
        }
        save_profile(farmer, db_path=TEST_DB_PATH)

        # Update phone number and add Bank Passbook
        updated = update_profile(
            "TEST_F105",
            {
                "phone_number": "9000099999",
                "uploaded_documents": {"Aadhaar": True, "Bank Passbook": True},
                "bank_account_name": "Kavitha Sharma",
            },
            db_path=TEST_DB_PATH
        )

        self.assertEqual(updated["phone_number"], "9000099999")
        self.assertTrue(updated["uploaded_documents"].get("Bank Passbook"))
        self.assertEqual(updated["bank_account_name"], "Kavitha Sharma")

    # -------------------------------------------------------------------------
    # SCENARIO 6: Missing document detection
    # -------------------------------------------------------------------------
    def test_06_missing_document_detection(self):
        """Test that missing required documents are properly identified."""
        profile = {
            "farmer_name": "Ramesh Kumar",
            "bank_account_name": "Ramesh Kumar",
            "uploaded_documents": {
                "Aadhaar": True,
                "Land Records": True
            }
        }
        scheme = {
            "name": "PM-KISAN Samman Nidhi",
            "documents_required": [
                "Aadhaar",
                "Bank Passbook",
                "Land Records"
            ],
            "name_match_required": True
        }

        result = check_documents(profile, scheme)
        self.assertFalse(result["ready"])
        self.assertIn("Bank Passbook", result["missing"])
        self.assertEqual(len(result["missing"]), 1)
        self.assertEqual(len(result["mismatches"]), 0)

    # -------------------------------------------------------------------------
    # SCENARIO 7: Complete document readiness
    # -------------------------------------------------------------------------
    def test_07_complete_document_readiness(self):
        """Test document readiness when all required documents are present."""
        profile = {
            "farmer_name": "Ramesh Kumar",
            "bank_account_name": "Ramesh Kumar",
            "uploaded_documents": {
                "Aadhaar": True,
                "Bank Passbook": True,
                "Land Records": True
            }
        }
        scheme = {
            "name": "PM-KISAN Samman Nidhi",
            "documents_required": [
                "Aadhaar",
                "Bank Passbook",
                "Land Records"
            ],
            "name_match_required": True
        }

        result = check_documents(profile, scheme)
        self.assertTrue(result["ready"])
        self.assertEqual(len(result["missing"]), 0)
        self.assertEqual(len(result["mismatches"]), 0)

    # -------------------------------------------------------------------------
    # SCENARIO 8: Bank-name similarity detection
    # -------------------------------------------------------------------------
    def test_08_bank_name_similarity_detection(self):
        """Test RapidFuzz and fallback name comparison: exact match, spelling typo, and severe mismatch."""
        # 1. Exact match (case and space normalized)
        res_exact = check_name_match("  Ravi Kumar ", "RAVI KUMAR")
        self.assertEqual(res_exact["match_status"], "matched")
        self.assertEqual(res_exact["similarity_score"], 100.0)
        self.assertFalse(res_exact["requires_manual_verification"])

        # 2. Minor spelling variation ("Ravi Kumar" vs "Ravi Kumer")
        res_typo = check_name_match("Ravi Kumar", "Ravi Kumer")
        self.assertEqual(res_typo["match_status"], "possible_mismatch")
        self.assertGreaterEqual(res_typo["similarity_score"], 85.0)
        self.assertTrue(res_typo["requires_manual_verification"])

        # 3. Severe mismatch ("Ravi Kumar" vs "Sita Devi")
        res_mismatch = check_name_match("Ravi Kumar", "Sita Devi")
        self.assertEqual(res_mismatch["match_status"], "mismatch")
        self.assertLess(res_mismatch["similarity_score"], 60.0)
        self.assertTrue(res_mismatch["requires_manual_verification"])

        # 4. Fallback branch test (simulating RapidFuzz unavailable)
        import person3.document_checker as dc
        orig_val = dc.RAPIDFUZZ_AVAILABLE
        try:
            dc.RAPIDFUZZ_AVAILABLE = False
            fallback_res = dc.check_name_match("Ravi Kumar", "Ravi Kumer")
            self.assertEqual(fallback_res["match_status"], "possible_mismatch")
            self.assertEqual(fallback_res["method_used"], "fallback_difflib")
            self.assertEqual(fallback_res["similarity_score"], 90.0)
        finally:
            dc.RAPIDFUZZ_AVAILABLE = orig_val

    # -------------------------------------------------------------------------
    # SCENARIO 9: Insurance claim-window reminder
    # -------------------------------------------------------------------------
    def test_09_insurance_claim_window_reminder(self):
        """Test that upcoming insurance claim-windows generate alerts and are prioritised."""
        eval_today = date(2026, 11, 5)

        farmer = {
            "farmer_id": "TEST_INS01",
            "farmer_name": "Mahesh Babu",
            "consent_status": True,
        }
        save_profile(farmer, db_path=TEST_DB_PATH)

        # Scheme with claim window ending on Nov 8 (3 days left) and deadline on Nov 25 (20 days left)
        schemes = [{
            "name": "Pradhan Mantri Fasal Bima Yojana",
            "claim_window": {
                "start": "2026-10-15",
                "end": "2026-11-08"
            },
            "deadline": "2026-11-25"
        }]

        alerts = get_due_alerts(eval_today, schemes, days_before=7, db_path=TEST_DB_PATH)
        self.assertEqual(len(alerts), 1)
        alert = alerts[0]
        self.assertEqual(alert["farmer_id"], "TEST_INS01")
        self.assertEqual(alert["days_left"], 3)
        self.assertEqual(alert["message_key"], "claim_window_closing")
        self.assertEqual(alert["priority"], 1)

    # -------------------------------------------------------------------------
    # SCENARIO 10: Expired deadline handling
    # -------------------------------------------------------------------------
    def test_10_expired_deadline_handling(self):
        """Test that expired deadlines do not emit false upcoming alerts and are correctly detected."""
        eval_today = date(2026, 11, 5)

        farmer = {
            "farmer_id": "TEST_EXP01",
            "farmer_name": "Prakash Verma",
            "consent_status": True,
        }
        save_profile(farmer, db_path=TEST_DB_PATH)

        # Scheme that ended on Oct 31, 2026 (5 days ago)
        expired_schemes = [{
            "name": "Old Kharif Subsidy",
            "deadline": "2026-10-31",
            "claim_window": None
        }]

        # Standard upcoming alerts must NOT include expired schemes
        alerts = get_due_alerts(eval_today, expired_schemes, days_before=7, db_path=TEST_DB_PATH)
        self.assertEqual(len(alerts), 0)

        # Check expired deadlines inspection utility
        expired = get_expired_deadlines(eval_today, expired_schemes)
        self.assertEqual(len(expired), 1)
        self.assertEqual(expired[0]["scheme"], "Old Kharif Subsidy")
        self.assertEqual(expired[0]["days_expired"], 5)
        self.assertTrue(is_deadline_expired("2026-10-31", eval_today))

    # -------------------------------------------------------------------------
    # SCENARIO 11: Consent withdrawal and reminder exclusion
    # -------------------------------------------------------------------------
    def test_11_consent_withdrawal_and_reminder_exclusion(self):
        """Test withdrawing consent immediately ceases reminders and removes profile from active views."""
        eval_today = date(2026, 11, 5)

        farmer = {
            "farmer_id": "TEST_WDR01",
            "farmer_name": "Gita Rani",
            "consent_status": True,
            "intermediary_id": "CSC_01"
        }
        save_profile(farmer, db_path=TEST_DB_PATH)

        schemes = [{
            "name": "PM-KISAN",
            "deadline": "2026-11-09"  # 4 days away
        }]

        # 1. Alert should be generated while consent is active
        alerts_before = get_due_alerts(eval_today, schemes, days_before=7, db_path=TEST_DB_PATH)
        self.assertEqual(len(alerts_before), 1)

        # 2. Withdraw consent
        success = withdraw_consent("TEST_WDR01", db_path=TEST_DB_PATH)
        self.assertTrue(success)
        self.assertFalse(is_consent_active("TEST_WDR01", db_path=TEST_DB_PATH))

        # 3. Alert engine must now return 0 alerts for this farmer
        alerts_after = get_due_alerts(eval_today, schemes, days_before=7, db_path=TEST_DB_PATH)
        self.assertEqual(len(alerts_after), 0)

        # 4. Intermediary view must exclude this farmer
        inter_farmers = get_intermediary_farmers(
            schemes, today=eval_today, intermediary_id="CSC_01", db_path=TEST_DB_PATH
        )
        self.assertEqual(len(inter_farmers), 0)

    # -------------------------------------------------------------------------
    # SCENARIO 12: Intermediary filtering by CSC/FPO ID
    # -------------------------------------------------------------------------
    def test_12_intermediary_filtering_by_csc_fpo_id(self):
        """Test CSC/FPO staff can filter farmers by their intermediary_id and see prioritized tasks."""
        eval_today = date(2026, 11, 5)

        # Farmer 1 assigned to CSC_01 with missing Bank Passbook
        f1 = {
            "farmer_id": "F_CSC01",
            "farmer_name": "Farmer Alpha",
            "intermediary_id": "CSC_WARANGAL",
            "consent_status": True,
            "uploaded_documents": {"Aadhaar": True},  # Missing passbook
            "bank_account_name": "Farmer Alpha",
        }
        # Farmer 2 assigned to CSC_02
        f2 = {
            "farmer_id": "F_CSC02",
            "farmer_name": "Farmer Beta",
            "intermediary_id": "CSC_KHAMMAM",
            "consent_status": True,
            "uploaded_documents": {"Aadhaar": True, "Bank Passbook": True},
            "bank_account_name": "Farmer Beta",
        }
        save_profile(f1, db_path=TEST_DB_PATH)
        save_profile(f2, db_path=TEST_DB_PATH)

        schemes = [{
            "name": "PM-KISAN",
            "deadline": "2026-11-20",
            "documents_required": ["Aadhaar", "Bank Passbook"]
        }]

        # Query only CSC_WARANGAL
        warangal_list = get_intermediary_farmers(
            schemes, today=eval_today, intermediary_id="CSC_WARANGAL", db_path=TEST_DB_PATH
        )
        self.assertEqual(len(warangal_list), 1)
        self.assertEqual(warangal_list[0]["farmer_id"], "F_CSC01")
        self.assertIn("Bank Passbook", warangal_list[0]["missing_documents"])

        # Query only CSC_KHAMMAM - farmer Beta has all documents and deadline is > 14 days away
        khammam_list = get_intermediary_farmers(
            schemes, today=eval_today, intermediary_id="CSC_KHAMMAM", db_path=TEST_DB_PATH
        )
        # Beta has no missing docs and no mismatches; deadline is within 30 days ahead
        self.assertTrue(all(item["farmer_id"] == "F_CSC02" for item in khammam_list))


if __name__ == "__main__":
    unittest.main(verbosity=2)
