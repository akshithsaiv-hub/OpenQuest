import os
import sys
import unittest
from rapidfuzz import fuzz

# Ensure project root is in path
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

class TestPerson2FrontEndAndEngine(unittest.TestCase):

    def setUp(self):
        self.schemes = load_schemes()
        self.assertGreater(len(self.schemes), 0, "Schemes database must not be empty.")

    def test_01_deterministic_eligibility(self):
        """Test that eligibility engine is strictly deterministic and rule-based."""
        # 1. Marginal farmer in Telangana growing Paddy
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

        # 2. Out of state farmer (e.g. Punjab)
        profile_out_of_state = FarmerProfile(
            state="Punjab",
            land_holding_acres=3.0,
            crop="Wheat",
            category="small"
        )
        matches_state = [evaluate_farmer(profile_out_of_state, s) for s in self.schemes if evaluate_farmer(profile_out_of_state, s).eligible]
        # State schemes should NOT match
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
        # Should explain that CCRC is required
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
        # 1. Close match (Initial vs Full Name)
        res1 = verify_name_match("Komirelli Ramulu", "K. Ramulu")
        self.assertGreaterEqual(res1["similarity_score"], 80)

        # 2. Exact match
        res2 = verify_name_match("Boda Venkanna", "Boda Venkanna")
        self.assertEqual(res2["similarity_score"], 100)
        self.assertEqual(res2["status"], "Exact Match")

        # 3. Severe Mismatch
        res3 = verify_name_match("Banoth Padma", "Guguloth Saroja")
        self.assertLess(res3["similarity_score"], 50)
        self.assertEqual(res3["status"], "Severe Mismatch")

if __name__ == "__main__":
    unittest.main()
