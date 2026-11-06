import os
import sys
import unittest
from datetime import datetime, timedelta
from rapidfuzz import fuzz

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.eligibility_api import evaluate_farmer, load_schemes, FarmerProfile, verify_name_match
from utils.llm import (
    process_farmer_query,
    generate_plain_explanation,
    detect_pmkisan_intent,
    detect_uncertainty,
    FALLBACK_PMKISAN,
    FALLBACK_UNCERTAIN
)
from utils.claim_assistant import calculate_72hr_window, generate_intimation_sms, PMFBY_HELPLINE
from utils.document_wallet import get_farmer_documents, add_farmer_document, check_scheme_document_readiness
from utils.credit_kcc import calculate_kcc_eligibility
from utils.status_tracker import get_all_claims, add_claim_entry, compute_claim_urgency
from utils.escalation_feedback import record_feedback, get_all_feedbacks, generate_formal_escalation_petition

class TestPerson2FrontEndAndEngine(unittest.TestCase):

    def setUp(self):
        self.schemes = load_schemes()
        self.assertGreater(len(self.schemes), 0, "Schemes database must not be empty.")

    def test_01_deterministic_eligibility(self):
        """Test that eligibility engine is strictly deterministic and rule-based."""
        profile1 = FarmerProfile(
            state="Telangana",
            land_holding_acres=1.5,
            crop="Paddy",
            category="marginal",
            is_tenant=False,
            has_irrigation_well=True
        )
        matches1 = [evaluate_farmer(profile1, s) for s in self.schemes if evaluate_farmer(profile1, s).eligible]
        scheme_names = [m.name for m in matches1]
        self.assertIn("Rythu Bharosa (Telangana)", scheme_names)
        self.assertIn("PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)", scheme_names)
        self.assertIn("Pradhan Mantri Fasal Bima Yojana (PMFBY) - Rabi Insurance", scheme_names)
        self.assertIn("MSP Procurement Operations (Paddy & Cotton 2026)", scheme_names)

        profile_out_of_state = FarmerProfile(
            state="Punjab",
            land_holding_acres=3.0,
            crop="Wheat",
            category="small"
        )
        matches_state = [evaluate_farmer(profile_out_of_state, s) for s in self.schemes if evaluate_farmer(profile_out_of_state, s).eligible]
        for m in matches_state:
            self.assertNotEqual(m.scheme_id, "TS-RB-01")

    def test_02_tenant_farmer_ccrc_rule(self):
        """Test tenant farmer without CCRC vs with CCRC for Rythu Bharosa."""
        tenant_no_ccrc = FarmerProfile(
            state="Telangana",
            land_holding_acres=2.0,
            crop="Paddy",
            category="tenant",
            is_tenant=True,
            has_ccrc=False
        )
        rb_scheme = next(s for s in self.schemes if s["scheme_id"] == "TS-RB-01")
        res_no_ccrc = evaluate_farmer(tenant_no_ccrc, rb_scheme)
        self.assertTrue(any("CCRC" in r for r in res_no_ccrc.reasons))

    def test_03_llm_source_link_and_date_traceability(self):
        """Every explanation MUST include source link and last-verified date."""
        rb_scheme = self.schemes[0]
        for lang in ["en", "te", "hi"]:
            explanation = generate_plain_explanation(rb_scheme, language=lang)
            self.assertIn(rb_scheme["source_url"], explanation, f"Missing source URL in {lang}")
            self.assertIn(rb_scheme["last_verified"], explanation, f"Missing last verified date in {lang}")

    def test_04_fallback_pmkisan_redirect(self):
        """Inquiries regarding PM-KISAN payments or grievances redirect to Kisan e-Mitra."""
        queries = [
            "When will I get my 2000 rupees PM-KISAN installment?",
            "PM-KISAN payment status",
            "పీఎం కిసాన్ డబ్బులు ఎప్పుడు వస్తాయి?"
        ]
        for q in queries:
            self.assertTrue(detect_pmkisan_intent(q), f"Failed to detect PM-KISAN query: {q}")
            res = process_farmer_query(q, [self.schemes[0]], language="en")
            self.assertEqual(res["type"], "redirect_kisan_emitra")
            self.assertIn("pmkisan.gov.in", res["message"])

    def test_05_fallback_uncertain_query(self):
        """Out of scope or uncertain inquiries redirect to local Agriculture Officer."""
        uncertain_queries = [
            "How to buy bitcoin crypto subsidy?",
            "Can I get loan for luxury car subsidy?"
        ]
        for q in uncertain_queries:
            self.assertTrue(detect_uncertainty(q), f"Failed to detect uncertain query: {q}")
            res = process_farmer_query(q, [self.schemes[0]], language="en")
            self.assertEqual(res["type"], "uncertainty_fallback")
            self.assertIn("Agriculture Extension Officer", res["message"])

    def test_06_aadhaar_bank_fuzzy_name_matching(self):
        """Document readiness check: Fuzzy match between Aadhaar name and Bank passbook name."""
        res1 = verify_name_match("Komirelli Ramulu", "K. Ramulu")
        self.assertGreaterEqual(res1["similarity_score"], 80)

        res2 = verify_name_match("Boda Venkanna", "Boda Venkanna")
        self.assertEqual(res2["similarity_score"], 100)
        self.assertEqual(res2["status"], "Exact Match")

        res3 = verify_name_match("Banoth Padma", "Guguloth Saroja")
        self.assertLess(res3["similarity_score"], 50)
        self.assertEqual(res3["status"], "Severe Mismatch")

    def test_07_live_weather_api(self):
        """Test live climate/weather API integration (Open-Meteo)."""
        from utils.weather_api import get_live_weather
        weather = get_live_weather("Warangal")
        self.assertIn(weather["status"], ["online", "cached_offline"])
        self.assertIn("current_temperature", weather)
        self.assertIn("forecast_7day_total_rain_mm", weather)
        self.assertIn("consecutive_dry_days", weather)

    def test_08_water_stress_and_advisory(self):
        """Test water stress calculation and PMFBY agronomic advisory generation."""
        from utils.weather_api import get_live_weather, evaluate_water_stress, generate_multilingual_water_advisory
        weather = get_live_weather("Warangal")
        assessment = evaluate_water_stress(weather, crop="Paddy", water_source="Borewell")
        
        self.assertIn(assessment["stress_level"], ["CRITICAL", "MODERATE", "NORMAL"])
        self.assertTrue(len(assessment["preventive_measures"]) >= 3)
        self.assertIn("PMFBY", assessment["insurance_shield"]["scheme"])

        adv_te = generate_multilingual_water_advisory(assessment, lang="te")
        adv_en = generate_multilingual_water_advisory(assessment, lang="en")
        self.assertIn("AWD", adv_en)
        self.assertIn("PMFBY", adv_en)
        self.assertIn("వరి పంట", adv_te)
        self.assertIn("1800-180-1551", adv_te)

    def test_09_pan_india_geocoding_and_weather(self):
        """Test Pan-India meteorological lookups across different states."""
        from utils.weather_api import get_live_weather, resolve_pan_india_coordinates
        punjab_coords = resolve_pan_india_coordinates("Ludhiana", state="Punjab")
        self.assertEqual(punjab_coords["name"], "Ludhiana")
        punjab_weather = get_live_weather("Ludhiana", state="Punjab")
        self.assertIn("Ludhiana", punjab_weather["location"])

        tn_weather = get_live_weather("Thanjavur", state="Tamil Nadu")
        self.assertIn("Thanjavur", tn_weather["location"])

        wb_weather = get_live_weather("Bardhaman", state="West Bengal")
        self.assertIn("Bardhaman", wb_weather["location"])

    def test_10_72hr_claim_assistant(self):
        """Test 72-hour countdown computation and multi-lingual intimation draft generation."""
        now = datetime.now()
        recent_incident = now - timedelta(hours=10)
        window = calculate_72hr_window(recent_incident)
        self.assertEqual(window["status"], "ACTIVE")
        self.assertGreaterEqual(window["hours_remaining"], 60)
        self.assertEqual(window["urgency"], "LOW")

        older_incident = now - timedelta(hours=60)
        window_crit = calculate_72hr_window(older_incident)
        self.assertEqual(window_crit["status"], "ACTIVE")
        self.assertLessEqual(window_crit["hours_remaining"], 12)
        self.assertEqual(window_crit["urgency"], "CRITICAL")

        lapsed_incident = now - timedelta(hours=75)
        window_exp = calculate_72hr_window(lapsed_incident)
        self.assertEqual(window_exp["status"], "EXPIRED")

        sms = generate_intimation_sms(
            farmer_name="Komirelli Ramulu",
            phone="9848022338",
            crop="Paddy",
            district="Warangal",
            village="Geesugonda",
            survey_no="142/A",
            loss_percent=70,
            hazard_type="Hailstorm",
            acreage=2.2,
            language="te"
        )
        self.assertIn("Komirelli Ramulu", sms["text"])
        self.assertIn("142/A", sms["text"])
        self.assertIn("72 గంటల", sms["text"])
        self.assertEqual(sms["target_helpline"], "1800-180-1551")

    def test_11_water_saving_subsidy_matcher(self):
        """Test loading and content of diversified water saving subsidy schemes (18+ schemes across India)."""
        import json
        water_schemes_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "water_saving_schemes.json")
        self.assertTrue(os.path.exists(water_schemes_path))
        with open(water_schemes_path, "r", encoding="utf-8") as f:
            schemes = json.load(f)
        
        self.assertGreaterEqual(len(schemes), 15, "Must contain diversified Pan-India water-saving subsidy schemes.")
        ids = [s["scheme_id"] for s in schemes]
        self.assertIn("PMKSY_PDMC", ids)
        self.assertIn("PMKSY_HKKP", ids)
        self.assertIn("PMKSY_WDC", ids)
        self.assertIn("PM_KUSUM_A", ids)
        self.assertIn("PM_KUSUM_B", ids)
        self.assertIn("PM_KUSUM_C", ids)
        self.assertIn("TSMIP_TELANGANA", ids)
        self.assertIn("APMIP_ANDHRA_PRADESH", ids)
        self.assertIn("MAHA_SHET_TALE", ids)
        self.assertIn("KARNATAKA_KRISHI_BHAGYA", ids)
        self.assertIn("HARYANA_MERA_PANI", ids)
        self.assertIn("PUNJAB_UGPL_PIPELINE", ids)

        tsmip = next(s for s in schemes if s["scheme_id"] == "TSMIP_TELANGANA")
        self.assertIn("100% subsidy", tsmip["subsidy_rules"]["sc_st_farmers"])

    def test_12_low_water_crops_and_msp(self):
        """Test diversified low-water crop alternatives across pulses, oilseeds and millets (26+ crops)."""
        import json
        crops_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "low_water_crops.json")
        self.assertTrue(os.path.exists(crops_path))
        with open(crops_path, "r", encoding="utf-8") as f:
            crops = json.load(f)

        self.assertGreaterEqual(len(crops), 25, "Must contain at least 25 diversified alternative crops.")
        crop_ids = [c["crop_id"] for c in crops]
        
        # Pulses
        self.assertIn("bengal_gram", crop_ids)
        self.assertIn("green_gram", crop_ids)
        self.assertIn("black_gram", crop_ids)
        self.assertIn("red_gram", crop_ids)
        self.assertIn("horse_gram", crop_ids)
        self.assertIn("cowpea", crop_ids)
        
        # Oilseeds
        self.assertIn("sesame", crop_ids)
        self.assertIn("groundnut", crop_ids)
        self.assertIn("mustard_rapeseed", crop_ids)
        self.assertIn("safflower", crop_ids)
        self.assertIn("sunflower", crop_ids)
        self.assertIn("castor", crop_ids)
        
        # Millets / Shree Anna
        self.assertIn("sorghum_jowar", crop_ids)
        self.assertIn("pearl_millet_bajra", crop_ids)
        self.assertIn("finger_millet_ragi", crop_ids)
        self.assertIn("foxtail_millet_korra", crop_ids)
        self.assertIn("little_millet_samalu", crop_ids)

        sesame = next(c for c in crops if c["crop_id"] == "sesame")
        self.assertGreaterEqual(sesame["msp_rate_per_quintal"], 9000)
        self.assertIn("85%", sesame["water_savings_percentage"])

    def test_13_kcc_credit_and_subvention(self):
        """Test KCC limit calculation and 4% effective interest subvention."""
        kcc = calculate_kcc_eligibility(crop="Paddy", land_acres=2.5)
        self.assertGreaterEqual(kcc["first_year_limit"], 100000)
        self.assertTrue(kcc["is_collateral_free"])
        
        kcc_large = calculate_kcc_eligibility(crop="Paddy", land_acres=4.0)
        self.assertFalse(kcc_large["is_collateral_free"])

        sub = kcc["interest_subvention"]
        self.assertEqual(sub["commercial_bank_rate"], "9.0% p.a.")
        self.assertEqual(sub["govt_interest_subvention"], "2.0% p.a.")
        self.assertEqual(sub["prompt_repayment_incentive"], "3.0% p.a.")
        self.assertIn("4.0%", sub["effective_net_rate"])

    def test_14_document_wallet_and_readiness(self):
        """Test document wallet consent, masking, and scheme readiness evaluator."""
        vault = get_farmer_documents("DEMO_FARMER_1")
        self.assertTrue(vault["consent_granted"])
        self.assertGreaterEqual(len(vault["documents"]), 1)

        passbook_doc = next((d for d in vault["documents"] if d["doc_type"] == "bank_passbook"), None)
        self.assertIsNotNone(passbook_doc)
        self.assertIn("8821", passbook_doc["identifier_masked"])

        reqs = ["Bank Account Passbook with active IFSC & A/c"]
        readiness = check_scheme_document_readiness(reqs, farmer_id="DEMO_FARMER_1")
        self.assertTrue(readiness["is_ready"])
        self.assertEqual(readiness["readiness_percent"], 100.0)

    def test_15_claim_and_application_status_tracker(self):
        """Test application status tracker, claim logging, and SLA monitoring."""
        new_entry = add_claim_entry(
            farmer_name="Test Farmer",
            phone="9999988888",
            scheme_name="TSMIP Subsidy",
            reference_number="TEST/REF/01",
            status="Under Review",
            notes="Testing status tracker"
        )
        self.assertEqual(new_entry["status"], "Under Review")

        urgency = compute_claim_urgency(new_entry)
        self.assertIn(urgency["urgency"], ["NORMAL", "MEDIUM", "HIGH"])

    def test_16_feedback_loop(self):
        """Test logging and retrieving community feedback on scheme data."""
        fb = record_feedback(
            scheme_id="PMKSY_PDMC",
            scheme_name="PMKSY Per Drop More Crop",
            feedback_type="OUTDATED_DEADLINE",
            reporter_role="CSC Operator",
            description="Portal registration extended till Dec 31."
        )
        self.assertEqual(fb["scheme_id"], "PMKSY_PDMC")
        all_fbs = get_all_feedbacks()
        self.assertTrue(any(f["feedback_id"] == fb["feedback_id"] for f in all_fbs))

    def test_17_higher_official_grievance_escalation(self):
        """Test generation of formal, legally grounded grievance petition."""
        petition = generate_formal_escalation_petition(
            farmer_name="Komirelli Ramulu",
            father_husband_name="K. Venkaiah",
            aadhaar_masked="XXXX-XXXX-4921",
            phone="9848022338",
            village="Geesugonda",
            mandal="Geesugonda",
            district="Warangal",
            survey_no="142/A",
            problem_category="72-Hour PMFBY Loss Survey Not Conducted",
            scheme_name="PMFBY Crop Insurance",
            description="Severe hailstorm damaged standing paddy. Intimated on day 1, no survey conducted after 5 days.",
            escalation_level="Level 3: District Agriculture Officer (DAO) & District Collector (Prajavani)"
        )
        self.assertIn("GRV/WAR", petition["petition_ref"])
        self.assertIn("District Agriculture Officer", petition["petition_text"])
        self.assertIn("Komirelli Ramulu", petition["petition_text"])
        self.assertIn("142/A", petition["petition_text"])
        self.assertIn("72-Hour PMFBY Loss Survey Not Conducted", petition["petition_text"])

if __name__ == "__main__":
    unittest.main()
