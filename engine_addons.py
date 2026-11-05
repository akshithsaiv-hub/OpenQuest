"""
Additional intelligence modules for Person 1:
- MSP vs Mandi price comparison
- Farm input budget planning with direct PACS/FPO dealer contacts
"""

import os
import json
from typing import Dict, Any, Optional, List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MSP_MANDI_FILE = os.path.join(BASE_DIR, "msp_mandi.json")
FARM_INPUTS_FILE = os.path.join(BASE_DIR, "farm_inputs.json")

def load_json(filepath: str) -> Any:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def compare_msp_mandi(crop_name: str, preferred_mandi: Optional[str] = None) -> Dict[str, Any]:
    records: List[Dict[str, Any]] = load_json(MSP_MANDI_FILE)
    crop_clean = crop_name.lower().strip()
    matched_record = None

    for record in records:
        if crop_clean in record["crop"].lower() or record["crop"].lower() in crop_clean:
            matched_record = record
            break

    if not matched_record:
        return {
            "error": f"Crop '{crop_name}' not found.",
            "available_crops": [r["crop"] for r in records]
        }

    msp = matched_record["msp_per_quintal"]
    reports = matched_record.get("mandi_reports", [])
    selected_mandi = reports[0] if reports else {}

    if preferred_mandi and reports:
        for rep in reports:
            if preferred_mandi.lower() in rep["mandi_name"].lower() or preferred_mandi.lower() in rep["district"].lower():
                selected_mandi = rep
                break

    modal_price = selected_mandi.get("modal_price", msp)
    diff = modal_price - msp

    if diff < 0:
        verdict = "SELL AT GOVT MSP CENTER"
        advice = f"Mandi rate is ₹{abs(diff)} BELOW MSP! Sell at MSP center to avoid ₹{abs(diff) * 100:,} loss per 100 quintals."
    elif diff == 0:
        verdict = "EQUAL VALUE"
        advice = f"Mandi rate equals MSP (₹{msp}/quintal)."
    else:
        verdict = "SELL IN OPEN MANDI"
        advice = f"Mandi rate is ₹{diff} HIGHER than MSP! Sell in {selected_mandi.get('mandi_name')} for better profit."

    return {
        "crop": matched_record["crop"],
        "msp_per_quintal": msp,
        "mandi_name": selected_mandi.get("mandi_name", "Local Mandi"),
        "mandi_modal_price": modal_price,
        "difference": diff,
        "verdict": verdict,
        "advice": advice,
        "procurement_centers": matched_record.get("procurement_centers", []),
        "quality_rules": matched_record.get("quality_faq", "")
    }

def get_input_budget_and_dealers(crop: str, acres: float, district: str = "Warangal") -> Dict[str, Any]:
    data = load_json(FARM_INPUTS_FILE)
    crops_dict = data.get("crops", {})
    crop_clean = crop.lower().strip()
    matched_key = None

    for k in crops_dict:
        if crop_clean in k.lower() or k.lower() in crop_clean:
            matched_key = k
            break

    if not matched_key:
        return {"error": f"Crop '{crop}' not found.", "supported_crops": list(crops_dict.keys())}

    info = crops_dict[matched_key]
    dealers = data.get("verified_dealers_and_pacs", [])
    matched_dealers = [d for d in dealers if district.lower() in d["district"].lower()] or dealers[:2]

    return {
        "crop": matched_key,
        "acres": acres,
        "seed_cost_total": info["estimated_seed_cost_per_acre"] * acres,
        "fertilizer_schedule": info["recommended_fertilizer_schedule"],
        "fertilizer_cost_total": info["estimated_total_fertilizer_cost_per_acre"] * acres,
        "total_budget": info["estimated_total_input_budget_per_acre"] * acres,
        "budget_advisory": info["budget_advisory"],
        "verified_dealers": matched_dealers
    }
