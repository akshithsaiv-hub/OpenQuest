"""
farmer_schemes_engine: Core Rule Engine (Person 1 Component)
Strictly deterministic if/else eligibility matching.
LLM NEVER decides eligibility; it only explains the outputs returned here.
"""

import json
import os
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMES_FILE = os.path.join(BASE_DIR, "schemes.json")
MSP_MANDI_FILE = os.path.join(BASE_DIR, "msp_mandi.json")
FARM_INPUTS_FILE = os.path.join(BASE_DIR, "farm_inputs.json")


def load_json(filepath: str) -> Any:
    """Helper to load JSON data files safely."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


class EligibilityEngine:
    def __init__(self, schemes_file: str = SCHEMES_FILE):
        self.schemes: List[Dict[str, Any]] = load_json(schemes_file)
        self.schemes_by_id = {s["scheme_id"]: s for s in self.schemes}

    def check_eligibility(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Primary interface function agreed across Person 1, Person 2, and Person 3.
        Evaluates a farmer profile against all schemes using deterministic rules.
        
        Input profile shape:
        {
            "farmer_id": Optional[str],
            "farmer_name": str,
            "state": str,                  # e.g. "Telangana"
            "district": str,               # e.g. "Warangal"
            "land_acres": float,           # e.g. 2.5
            "is_tenant": bool,             # e.g. False
            "has_rofr_patta": bool,        # e.g. False
            "crops": List[str],            # e.g. ["Paddy", "Cotton"]
            "age": int,                    # e.g. 42
            "is_tax_payer": bool           # e.g. False
        }

        Returns list of results:
        [
          {
            "scheme": str,
            "scheme_id": str,
            "eligible": bool,
            "reasons": List[str],
            "docs": List[str],
            "source_url": str,
            "last_verified": str,
            "deadlines": str,
            "claim_window": str,
            "benefit_summary": str,
            "kisan_e_mitra_redirect": bool
          },
          ...
        ]
        """
        state = profile.get("state", "Telangana").strip()
        land_acres = float(profile.get("land_acres", 0.0))
        is_tenant = bool(profile.get("is_tenant", False))
        has_rofr_patta = bool(profile.get("has_rofr_patta", False))
        crops = [c.lower() for c in profile.get("crops", [])]
        age = int(profile.get("age", 35))
        is_tax_payer = bool(profile.get("is_tax_payer", False))

        results = []

        for scheme in self.schemes:
            scheme_id = scheme["scheme_id"]
            name = scheme["scheme_name"]
            rules = scheme.get("rules", {})
            eligible = True
            reasons = []

            # 1. State restriction check
            state_req = rules.get("state_restriction")
            scheme_state = scheme.get("state", "All")
            target_state = state_req if state_req else scheme_state
            if target_state != "All" and target_state.lower() != state.lower():
                eligible = False
                reasons.append(f"Applicable only for residents of {target_state}, not {state}.")

            # 2. Income Tax Payer check (PM-KISAN exclusion)
            if is_tax_payer and "income_tax_payer" in rules.get("excluded_categories", []):
                eligible = False
                reasons.append("Income-tax payers and institutional holders are excluded by official central guidelines.")

            # 3. Land ownership & Tenant check
            requires_land = rules.get("requires_land_ownership", False)
            tenant_allowed = rules.get("tenant_allowed", True)
            rofr_allowed = rules.get("rofr_patta_allowed", False)

            if is_tenant:
                if not tenant_allowed:
                    eligible = False
                    reasons.append("Requires registered land ownership (Pattadar passbook); oral tenant farmers not eligible.")
                elif land_acres <= 0.0:
                    eligible = False
                    reasons.append("Tenant cultivation requires positive leased land acreage.")
            else:
                if requires_land and land_acres <= 0.0 and not (rofr_allowed and has_rofr_patta):
                    eligible = False
                    reasons.append("Requires positive cultivable landholding or valid RoFR title deed.")

            # Specific check for crop insurance (PMFBY): requires active crop and positive cultivated acreage
            if scheme_id == "pmfby":
                if land_acres <= 0.0 or not crops:
                    eligible = False
                    reasons.append("Crop insurance requires positive cultivated land and at least one sown notified crop.")

            # 4. Maximum land ceiling check (e.g. Rythu Bharosa 10 acres)
            max_land = rules.get("max_land_acres")
            if max_land is not None and land_acres > max_land:
                eligible = False
                reasons.append(f"Landholding ({land_acres} acres) exceeds scheme maximum cap of {max_land} acres.")

            # 5. Age restrictions check (e.g., Rythu Bima: 18 to 59 years)
            min_age = rules.get("min_age")
            max_age = rules.get("max_age")
            if min_age is not None and age < min_age:
                eligible = False
                reasons.append(f"Farmer age ({age}) is below minimum requirement of {min_age} years.")
            if max_age is not None and age > max_age:
                eligible = False
                reasons.append(f"Farmer age ({age}) exceeds maximum ceiling of {max_age} years.")

            # 6. Supported Crops check (e.g., PMFBY)
            supported_crops = rules.get("supported_crops")
            if supported_crops and crops:
                supported_lower = [sc.lower() for sc in supported_crops]
                crop_matched = any(c in supported_lower or any(sc in c for sc in supported_lower) for c in crops)
                if not crop_matched:
                    eligible = False
                    reasons.append(f"Crops cultivated {profile.get('crops')} are not notified under current season coverage.")

            if eligible:
                reasons.append("All eligibility criteria met based on profile parameters.")

            results.append({
                "scheme": name,
                "scheme_id": scheme_id,
                "eligible": eligible,
                "reasons": reasons,
                "docs": scheme.get("documents_required", []),
                "source_url": scheme.get("source_url", ""),
                "last_verified": scheme.get("last_verified", ""),
                "deadlines": scheme.get("deadlines", ""),
                "claim_window": scheme.get("claim_window", ""),
                "benefit_summary": scheme.get("benefit_summary", ""),
                "kisan_e_mitra_redirect": scheme.get("kisan_e_mitra_redirect", False)
            })

        return results

    def get_scheme_docs(self, scheme_id: str) -> List[str]:
        """Helper for Person 3's check_documents module."""
        scheme = self.schemes_by_id.get(scheme_id)
        return scheme.get("documents_required", []) if scheme else []


# Standalone instances
_engine = EligibilityEngine()

def check_eligibility(profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Official function signature for Person 1."""
    return _engine.check_eligibility(profile)

def get_scheme_documents(scheme_id: str) -> List[str]:
    """Helper for Person 3."""
    return _engine.get_scheme_docs(scheme_id)

def get_msp_vs_mandi(crop_name: str, preferred_mandi: Optional[str] = None) -> Dict[str, Any]:
    """MSP vs Mandi comparison engine."""
    from engine_addons import compare_msp_mandi
    return compare_msp_mandi(crop_name, preferred_mandi)


# Compatibility aliases for demo.py and team interfaces

def evaluate_farmer_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    raw_results = check_eligibility(profile)
    eligible = [s for s in raw_results if s['eligible']]
    ineligible = [s for s in raw_results if not s['eligible']]

    total_cash = 0.0
    formatted_eligible = []
    for s in eligible:
        formatted_eligible.append({
            'name': s['scheme'],
            'level': 'State / Central',
            'benefit_summary': s['benefit_summary'],
            'deadlines': s['deadlines'],
            'required_documents': s['docs'],
            'official_portal': s['source_url']
        })
        if s['scheme_id'] == 'rythu_bharosa':
            total_cash += 15000.0 * min(float(profile.get('land_acres', 0.0)), 10.0)
        elif s['scheme_id'] == 'pm_kisan':
            total_cash += 6000.0

    formatted_ineligible = []
    for s in ineligible:
        formatted_ineligible.append({
            'name': s['scheme'],
            'reasons': s['reasons']
        })

    return {
        'eligible_schemes_count': len(eligible),
        'total_direct_cash_benefit_annual': total_cash,
        'eligible_schemes': formatted_eligible,
        'ineligible_schemes': formatted_ineligible
    }


def compare_msp_mandi(crop_name: str, preferred_mandi: str = None):
    from engine_addons import compare_msp_mandi as _cmp
    return _cmp(crop_name, preferred_mandi)

def get_input_planning(crop: str, acres: float, district: str = 'Warangal'):
    from engine_addons import get_input_planning as _gip
    return _gip(crop, acres, district)
