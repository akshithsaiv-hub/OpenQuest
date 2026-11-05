import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.eligibility_api import app
from utils.credit_kcc import calculate_kcc_eligibility, generate_kcc_application_form
from utils.status_tracker import get_all_claims, add_claim_entry, delete_claim_entry

class TestKccClean(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_kcc_calculation_clean(self):
        res = calculate_kcc_eligibility("Paddy", 3.0, 0.0)
        self.assertEqual(res["crop"], "Paddy")
        self.assertEqual(res["first_year_limit"], 151200)
        self.assertTrue(res["is_collateral_free"])
        self.assertEqual(res["interest_subvention"]["effective_net_rate"], "4.0% p.a. (Only 40 paise per ₹100 per month!)")

    def test_generate_kcc_application_form(self):
        form_text = generate_kcc_application_form(
            farmer_name="Komirelli Ramulu",
            phone="9848022338",
            crop="Paddy",
            land_acres=3.0,
            village="Geesugonda",
            district="Warangal",
            survey_no="284/B"
        )
        self.assertIn("SIMPLIFIED 1-PAGE KISAN CREDIT CARD", form_text)
        self.assertIn("Komirelli Ramulu", form_text)
        self.assertIn("284/B", form_text)
        self.assertIn("4.0% p.a.", form_text)

    def test_api_kcc_application_form(self):
        resp = self.client.post("/api/kcc/application_form", json={
            "farmer_name": "Banoth Padma",
            "phone": "9848099887",
            "crop": "Cotton",
            "land_acres": 2.5,
            "village": "Narsampet",
            "district": "Warangal",
            "survey_no": "104/A",
            "existing_debt": 0.0
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("Banoth Padma", data["form_text"])

    def test_delete_claim_entry(self):
        # Add a temporary test claim
        add_claim_entry(
            farmer_name="Temp Test",
            phone="9000011111",
            scheme_name="Test Scheme",
            reference_number="DELETE_ME_123",
            status="Under Review"
        )
        resp = self.client.delete("/claims/DELETE_ME_123")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")

if __name__ == "__main__":
    unittest.main()
