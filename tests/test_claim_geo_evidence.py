import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.eligibility_api import app
from utils.claim_assistant import calculate_claim_compensation, generate_claim_dossier, GEO_PHOTO_CHECKLIST

class TestClaimGeoEvidence(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_calculate_claim_compensation(self):
        res = calculate_claim_compensation(crop="Paddy", acreage=2.5, loss_percent=80, is_irrigated=True, state="Telangana")
        self.assertEqual(res["crop"], "Paddy")
        self.assertEqual(res["acreage"], 2.5)
        self.assertEqual(res["loss_percent"], 80)
        self.assertEqual(res["total_sum_insured"], 105000.0)
        self.assertEqual(res["pmfby_expected_payout"], 84000.0)
        self.assertTrue(res["sdrf_eligible"])
        self.assertGreater(res["sdrf_payout"], 0)
        self.assertGreater(res["total_estimated_recovery"], 84000.0)

    def test_generate_claim_dossier(self):
        dossier = generate_claim_dossier(
            farmer_name="Komirelli Ramulu",
            phone="9848022338",
            crop="Paddy",
            district="Warangal",
            village="Geesugonda",
            survey_no="284/B",
            hazard_type="Hailstorm",
            loss_percent=80,
            acreage=2.5,
            geo_photos_count=2
        )
        self.assertIn("Komirelli Ramulu", dossier)
        self.assertIn("284/B", dossier)
        self.assertIn("PMFBY", dossier)
        self.assertIn("TOTAL PROJECTED STATUTORY RECOVERY", dossier)

    def test_api_claim_payout_calc(self):
        resp = self.client.post("/api/claim/payout_calc", json={
            "crop": "Cotton",
            "acreage": 3.0,
            "loss_percent": 75,
            "is_irrigated": True,
            "state": "Telangana"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["crop"], "Cotton")
        self.assertIn("pmfby_expected_payout", data)
        self.assertIn("total_estimated_recovery", data)

    def test_api_claim_dossier(self):
        resp = self.client.post("/api/claim/dossier", json={
            "farmer_name": "Banoth Padma",
            "phone": "9848099887",
            "crop": "Chilli",
            "district": "Warangal",
            "village": "Narsampet",
            "survey_no": "104/A",
            "hazard_type": "Excess Rain / Inundation",
            "loss_percent": 90,
            "acreage": 1.5,
            "geo_photos_count": 3
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("Banoth Padma", data["dossier_text"])

    def test_api_claim_checklist(self):
        resp = self.client.get("/api/claim/checklist")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("geo_photo_checklist", data)
        self.assertIn("document_checklist", data)
        self.assertEqual(data["pmfby_helpline"], "1800-180-1551")

    def test_api_claim_evidence_upload(self):
        resp = self.client.post("/api/claim/evidence/upload", json={
            "farmer_name": "Komirelli Ramulu",
            "survey_no": "284/B",
            "latitude": 17.9784,
            "longitude": 79.5941,
            "accuracy": 3.2,
            "timestamp": "2026-11-05 23:55:00 IST",
            "image_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            "photo_type": "Wide Field View"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertTrue(data["evidence_id"].startswith("GEO-"))

if __name__ == "__main__":
    unittest.main()
