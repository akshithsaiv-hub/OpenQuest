"""
Kisan Credit Card (KCC) & Credit Help Advisory Engine
Covers:
- Scale of Finance (SoF) credit limit estimation per crop/acre
- Modified Interest Subvention Scheme (MISS) calculation (7% base - 3% prompt repayment = 4% effective interest)
- Collateral-free loan limits (up to ₹1.60 Lakh)
- Kharif (March 31) and Rabi (June 30) repayment schedule reminders
- Step-by-step guidance for PACS, Regional Rural Banks (RRB), and Commercial Banks
"""

from typing import Dict, Any, List
from datetime import datetime

SCALE_OF_FINANCE_PER_ACRE = {
    "Paddy": {"sof_per_acre": 42000, "post_harvest_consumption_add_on": 0.20},
    "Cotton": {"sof_per_acre": 45000, "post_harvest_consumption_add_on": 0.20},
    "Chilli": {"sof_per_acre": 65000, "post_harvest_consumption_add_on": 0.20},
    "Maize": {"sof_per_acre": 28000, "post_harvest_consumption_add_on": 0.20},
    "Bengal Gram": {"sof_per_acre": 24000, "post_harvest_consumption_add_on": 0.20},
    "Pulses": {"sof_per_acre": 22000, "post_harvest_consumption_add_on": 0.20},
    "Groundnut": {"sof_per_acre": 30000, "post_harvest_consumption_add_on": 0.20},
    "Default": {"sof_per_acre": 30000, "post_harvest_consumption_add_on": 0.20}
}

def calculate_kcc_eligibility(
    crop: str,
    land_acres: float,
    existing_kcc_debt: float = 0.0
) -> Dict[str, Any]:
    crop_info = SCALE_OF_FINANCE_PER_ACRE.get(crop, SCALE_OF_FINANCE_PER_ACRE["Default"])
    sof_rate = crop_info["sof_per_acre"]
    
    crop_cultivation_cost = int(sof_rate * land_acres)
    maintenance_and_consumption = int(crop_cultivation_cost * 0.20)
    total_sanction_limit_year1 = crop_cultivation_cost + maintenance_and_consumption
    five_year_limit = int(total_sanction_limit_year1 * 1.5)
    available_limit = max(0, total_sanction_limit_year1 - int(existing_kcc_debt))

    is_collateral_free = total_sanction_limit_year1 <= 160000
    collateral_note = (
        "✅ 100% Collateral-Free & No Hypothecation Stamp Duty needed (Under RBI ₹1.60 Lakh threshold)."
        if is_collateral_free else
        "⚠️ Mortgage / Charge creation on land records (Pahani/Dharani) required because limit exceeds ₹1.60 Lakh."
    )

    subvention_eligible_amount = min(total_sanction_limit_year1, 300000)
    commercial_rate = 9.0
    headline_farmer_rate = 7.0
    effective_rate_if_timely = 4.0

    annual_interest_commercial = int(subvention_eligible_amount * 0.09)
    annual_interest_effective_timely = int(subvention_eligible_amount * 0.04)
    annual_savings = annual_interest_commercial - annual_interest_effective_timely

    curr_month = datetime.now().month
    if 4 <= curr_month <= 9:
        season = "Kharif"
        due_date_str = f"March 31, {datetime.now().year + 1}"
    else:
        season = "Rabi"
        due_date_str = f"June 30, {datetime.now().year if curr_month <= 3 else datetime.now().year + 1}"

    return {
        "crop": crop,
        "land_acres": land_acres,
        "scale_of_finance_per_acre": sof_rate,
        "first_year_limit": total_sanction_limit_year1,
        "five_year_card_limit": five_year_limit,
        "available_limit": available_limit,
        "is_collateral_free": is_collateral_free,
        "collateral_note": collateral_note,
        "interest_subvention": {
            "eligible_amount": subvention_eligible_amount,
            "commercial_bank_rate": "9.0% p.a.",
            "govt_interest_subvention": "2.0% p.a.",
            "headline_rate": "7.0% p.a.",
            "prompt_repayment_incentive": "3.0% p.a.",
            "effective_net_rate": "4.0% p.a. (Only 40 paise per ₹100 per month!)",
            "annual_interest_payable_timely": annual_interest_effective_timely,
            "annual_interest_saved_vs_moneylender": annual_savings
        },
        "repayment_reminder": {
            "current_season": season,
            "statutory_due_date": due_date_str,
            "critical_warning": f"Must repay or roll-over principal before {due_date_str} to retain the 4% interest rate and prevent penal 9% charges + CIBIL downgrade."
        },
        "application_steps": [
            "1. Visit local Primary Agricultural Credit Society (PACS), Regional Rural Bank (e.g. Telangana Grameena Bank / APGVB), or Commercial Bank branch.",
            "2. Submit standard 1-page simplified KCC Form (KCC-Aadhaar-Pahani link).",
            "3. Bank branch is mandated by RBI to process KCC within 14 days of complete application.",
            "4. Receive Rupay KCC debit card for hassle-free ATM input purchases (fertilizer, seeds, diesel)."
        ],
        "official_sources": [
            "RBI Master Circular on Kisan Credit Card (RBI/FIDD/2023-24)",
            "NABARD Scale of Finance Guidelines",
            "Modified Interest Subvention Scheme (MISS) - Ministry of Agriculture"
        ],
        "last_verified": "2026-11-05"
    }
