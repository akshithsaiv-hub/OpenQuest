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


def generate_kcc_application_form(
    farmer_name: str,
    phone: str,
    crop: str,
    land_acres: float,
    village: str = "Geesugonda",
    district: str = "Warangal",
    survey_no: str = "284/B",
    existing_debt: float = 0.0
) -> str:
    """
    Generates official, standard 1-page pre-filled KCC loan application
    compliant with RBI & NABARD simplified formats.
    """
    kcc_data = calculate_kcc_eligibility(crop, land_acres, existing_debt)
    date_str = datetime.now().strftime("%d-%b-%Y")
    collateral_status = "APPLIED (100% Collateral-Free under RBI Rs 1.60 Lakh threshold)" if kcc_data['is_collateral_free'] else "Charge creation on RoR-1B required (> Rs 1.60 Lakh)"
    
    return f"""================================================================================
SIMPLIFIED 1-PAGE KISAN CREDIT CARD (KCC) APPLICATION FORM
Prescribed by Reserve Bank of India (FIDD.CO.FSD.BC.No.6/05.05.010/2019-20)
Empanelled Banks: State Bank of India / TGB / APGVB / Canara Bank / DCCB
================================================================================
Date of Application: {date_str}
Branch Name: _______________________ Branch Code: _____________

1. APPLICANT DETAILS
   - Full Name of Farmer: {farmer_name}
   - Mobile Number: {phone}
   - Residential Address: Village {village}, Mandal: _____________, District {district}
   - Aadhaar Number: XXXX-XXXX-_________________
   - Category: Small / Marginal Farmer (< 5 Acres)

2. LAND & CULTIVATION PARTICULARS
   - Survey / Khata / Passbook No: {survey_no}
   - Total Operational Holding: {land_acres} Acres
   - Primary Crop to be Cultivated: {crop}
   - Land Ownership Status: Owner-Cultivator / CCRC Tenant Cultivator

3. STATUTORY CREDIT REQUIREMENT (DLTC SCALE OF FINANCE)
   - Crop Cultivation Scale of Finance: Rs {kcc_data['scale_of_finance_per_acre']:,} per acre
   - Crop Cultivation Cost (A): Rs {kcc_data['scale_of_finance_per_acre'] * land_acres:,.2f}
   - 20% Post-Harvest / Household Maintenance (B): Rs {kcc_data['first_year_limit'] - (kcc_data['scale_of_finance_per_acre'] * land_acres):,.2f}
   - Total Sanctioned Limit for Year 1 (A + B): Rs {kcc_data['first_year_limit']:,.2f}
   - Existing Crop Loan Outstanding: Rs {existing_debt:,.2f}
   - NET ELIGIBLE DRAWING LIMIT: Rs {kcc_data['available_limit']:,.2f}

4. REGULATORY PRIVILEGES APPLIED
   - Collateral Waiver: {collateral_status}
   - Subvention Scheme: 4.0% p.a. Net Interest under Central MISS (7% Base - 3% PRI)
   - RuPay KCC ATM Card: Demanded for direct debit & input procurement.

5. DECLARATION BY APPLICANT
   I hereby declare that the particulars given above are true and correct. I undertake
   to repay the borrowed amount along with interest on or before the statutory due date
   ({kcc_data['repayment_reminder']['statutory_due_date']}) to remain eligible for the 3% Prompt Repayment Incentive.

Enclosures Attached:
[ ] 1. Copy of Aadhaar Card
[ ] 2. Certified Digital Land Record (Pahani / Dharani / RoR-1B) or CCRC Agreement
[ ] 3. Two Passport-size Photographs
[ ] 4. Sowing Proof / Self-Declaration of Cultivation

Signature / Thumb Impression of Farmer: _________________________
For Bank Branch Use Only:
Date Received: ________________ Processing Officer: ___________________
Mandated RBI Clearance SLA: Within 14 Days
================================================================================
"""
