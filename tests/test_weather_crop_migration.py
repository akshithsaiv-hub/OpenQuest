import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.eligibility_api import app
from utils.agro_climate_advisory import (
    get_district_weather,
    compute_agro_climate_ecosystem,
    DISTRICT_WEATHER_PROFILES,
    ROUTINE_CROPS_CATALOG,
    CROP_MIGRATIONS,
    STATE_MICRO_IRRIGATION_BODIES
)

class TestAgroClimateAndCropMigration(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_01_weather_deficit_detection(self):
        """Verifies near-future weather deficit and dry spell assessment."""
        w = get_district_weather("Telangana", "Warangal")
        self.assertLess(w["rainfall_deficit_pct"], -20, "Should detect rainfall deficit in dry profile.")
        self.assertGreater(w["dry_spell_days"], 10, "Dry spell continuous days should be tracked.")
        self.assertIn(w["drought_alert_level"], ["CRITICAL", "SEVERE", "MODERATE"])
        self.assertTrue(len(w["forecast_daily"]) >= 3, "Should include daily micro-forecast.")

    def test_02_drip_subsidy_matching_sc_st(self):
        """Tests that SC/ST farmers get 100% micro-irrigation subsidy in Telangana."""
        res = compute_agro_climate_ecosystem(
            state="Telangana",
            district="Warangal",
            routine_crop="Paddy",
            irrigation_type="flood",
            acres=2.0,
            farmer_category="sc_st"
        )
        adv = res["micro_irrigation_advisory"]
        self.assertEqual(adv["subsidy_percentage"], 100)
        self.assertEqual(adv["farmer_payable_share"], 0.0)
        self.assertIn("TSMIP", adv["agency_name"])
        self.assertTrue(adv["is_drip_urgently_needed"])

    def test_03_drip_subsidy_matching_small_marginal(self):
        """Tests that Small & Marginal farmers get 90% subsidy in Telangana."""
        res = compute_agro_climate_ecosystem(
            state="Telangana",
            district="Karimnagar",
            routine_crop="Paddy",
            irrigation_type="borewell",
            acres=3.0,
            farmer_category="small_marginal"
        )
        adv = res["micro_irrigation_advisory"]
        self.assertEqual(adv["subsidy_percentage"], 90)
        # Total cost = 3 * 32,000 = 96,000; Subsidy = 86,400; Farmer share = 9,600
        self.assertEqual(adv["total_market_cost"], 96000.0)
        self.assertEqual(adv["government_subsidy_amount"], 86400.0)
        self.assertEqual(adv["farmer_payable_share"], 9600.0)

    def test_04_chc_rental_option(self):
        """Verifies that equipment rental from Custom Hiring Centers (CHCs) is available."""
        res = compute_agro_climate_ecosystem(
            state="Telangana",
            district="Nalgonda",
            routine_crop="Sugarcane",
            irrigation_type="flood",
            acres=2.0
        )
        rent = res["micro_irrigation_advisory"]["rent_option"]
        self.assertIn("Custom Hiring", rent["title"])
        self.assertTrue("day" in rent["rental_rate_per_day"])

    def test_05_crop_migrations_water_savings(self):
        """Verifies that all alternative crops save significant water over routine Paddy."""
        res = compute_agro_climate_ecosystem(
            state="Telangana",
            district="Warangal",
            routine_crop="Paddy",
            irrigation_type="flood",
            acres=2.5
        )
        migrations = res["crop_migrations"]
        self.assertGreaterEqual(len(migrations), 4, "Must offer at least 4 viable crop migrations.")
        
        for m in migrations:
            self.assertGreater(m["water_saved_pct"], 50.0, f"Crop {m['name']} should save > 50% water vs Paddy.")
            self.assertGreater(m["liters_saved_total"], 0)
            self.assertGreater(m["msp_per_quintal"], 2000)
            self.assertIn("recommended_varieties", m)
            self.assertIn("buyer_body", m)

    def test_06_already_equipped_drip(self):
        """Tests that if a farmer already has Drip, advisory recognizes it."""
        res = compute_agro_climate_ecosystem(
            state="Telangana",
            district="Warangal",
            routine_crop="Paddy",
            irrigation_type="drip_irrigation",
            acres=2.0
        )
        adv = res["micro_irrigation_advisory"]
        self.assertTrue(adv["has_drip"])
        self.assertFalse(adv["is_drip_urgently_needed"])

    def test_07_api_endpoints(self):
        """Tests GET and POST /api/weather_advisory endpoints via TestClient."""
        # Test POST
        resp_post = self.client.post("/api/weather_advisory", json={
            "state": "Telangana",
            "district": "Warangal",
            "routine_crop": "Paddy",
            "irrigation_type": "flood",
            "acres": 2.0,
            "farmer_category": "small_marginal"
        })
        self.assertEqual(resp_post.status_code, 200)
        data_post = resp_post.json()
        self.assertEqual(data_post["status"], "success")
        self.assertIn("weather", data_post)
        self.assertIn("crop_migrations", data_post)

        # Test GET
        resp_get = self.client.get("/api/weather_advisory?state=Telangana&district=Warangal&routine_crop=Paddy")
        self.assertEqual(resp_get.status_code, 200)
        data_get = resp_get.json()
        self.assertEqual(data_get["status"], "success")

        # Test districts list
        resp_dist = self.client.get("/api/weather_districts/Telangana")
        self.assertEqual(resp_dist.status_code, 200)
        self.assertIn("Warangal", resp_dist.json()["districts"])

if __name__ == "__main__":
    unittest.main()
