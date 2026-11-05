"""
Interactive CLI Demo for Farmer Schemes Engine (Person 1's Brain)
Run this script to verify the rule engine, MSP advisor, and input planner.
"""

import json
from engine import evaluate_farmer_profile, compare_msp_mandi, get_input_planning


def run_demo():
    print("=" * 70)
    print("🌾 UNIFIED FARMER ASSISTANT - ENGINE & DATA TEST (PERSON 1) 🌾")
    print("=" * 70)

    # Test Profile 1: Small landholder farmer in Telangana (Paddy & Cotton, 3 acres, age 38)
    profile_1 = {
        "farmer_name": "Mallesh Reddy",
        "state": "Telangana",
        "district": "Warangal",
        "land_acres": 3.0,
        "is_tenant": False,
        "has_rofr_patta": False,
        "crops": ["Paddy", "Cotton"],
        "age": 38,
        "category": "small",
        "is_tax_payer": False
    }

    print("\n--- TEST CASE 1: Landowning Small Farmer (3.0 acres, Age 38, Warangal) ---")
    result_1 = evaluate_farmer_profile(profile_1)
    print(f"Eligible Schemes Found: {result_1['eligible_schemes_count']}")
    print(f"Total Direct Annual Cash Assistance: ₹{int(result_1['total_direct_cash_benefit_annual']):,}")
    print("\n[Eligible Schemes Details]:")
    for s in result_1["eligible_schemes"]:
        print(f"  ✅ {s['name']} ({s['level']})")
        print(f"     Benefit: {s['benefit_summary']}")
        print(f"     Deadlines: {s['deadlines']}")
        print(f"     Key Documents: {', '.join(s['required_documents'][:2])}...")
        print(f"     Portal: {s['official_portal']}")

    print("\n[Ineligible Schemes / Filtered Out]:")
    for ins in result_1["ineligible_schemes"]:
        print(f"  ❌ {ins['name']}: {', '.join(ins['reasons'])}")

    # Test Profile 2: Tenant Farmer (1.5 acres, Age 45, Khammam)
    profile_2 = {
        "farmer_name": "Laxman Rao",
        "state": "Telangana",
        "district": "Khammam",
        "land_acres": 1.5,
        "is_tenant": True,
        "has_rofr_patta": False,
        "crops": ["Paddy"],
        "age": 45,
        "category": "marginal",
        "is_tax_payer": False
    }

    print("\n" + "=" * 70)
    print("--- TEST CASE 2: Tenant Farmer (1.5 acres, Khammam) ---")
    result_2 = evaluate_farmer_profile(profile_2)
    print(f"Eligible Schemes Found: {result_2['eligible_schemes_count']}")
    for s in result_2["eligible_schemes"]:
        print(f"  ✅ {s['name']}: {s['benefit_summary']}")
    print("\nIneligible Due to Land Ownership Restrictions:")
    for ins in result_2["ineligible_schemes"]:
        print(f"  ❌ {ins['name']}: {', '.join(ins['reasons'])}")

    # Test MSP vs Mandi Price Comparison
    print("\n" + "=" * 70)
    print("--- TEST CASE 3: MSP vs Mandi Price Advisor (Paddy vs Cotton) ---")
    paddy_check = compare_msp_mandi("Paddy (Common)", "Warangal")
    print(f"\n🌾 Crop: {paddy_check['crop']}")
    print(f"   MSP Rate: ₹{paddy_check['msp_per_quintal']}/quintal")
    print(f"   {paddy_check['mandi_analyzed']} Price: ₹{paddy_check['mandi_modal_price']}/quintal")
    print(f"   Verdict: {paddy_check['verdict']}")
    print(f"   Advice: {paddy_check['action_advice']}")
    print(f"   Quality Rule: {paddy_check['quality_standard_advisory']}")

    tur_check = compare_msp_mandi("Red Gram (Tur / Arhar)", "Tandur")
    print(f"\n🌾 Crop: {tur_check['crop']}")
    print(f"   MSP Rate: ₹{tur_check['msp_per_quintal']}/quintal")
    print(f"   {tur_check['mandi_analyzed']} Price: ₹{tur_check['mandi_modal_price']}/quintal")
    print(f"   Verdict: {tur_check['verdict']}")
    print(f"   Advice: {tur_check['action_advice']}")

    # Test Farm Input Planning & Local Dealer Bypass
    print("\n" + "=" * 70)
    print("--- TEST CASE 4: Farm Input Planning & Verified Local PACS (Warangal, 3 acres Paddy) ---")
    input_plan = get_input_planning("Paddy", acres=3.0, district="Warangal")
    print(f"Crop: {input_plan['crop']} | Land: {input_plan['land_acres']} acres")
    print(f"Estimated Seed Cost: ₹{int(input_plan['seed_cost_total']):,}")
    print(f"Estimated Fertilizer Cost: ₹{int(input_plan['fertilizer_cost_total']):,}")
    print(f"Estimated Total Input Budget: ₹{int(input_plan['total_estimated_budget']):,}")
    print(f"Government Advisory: {input_plan['budget_advisory']}")
    print("\nVerified Local Dealers & PACS (Direct Contact - No Middlemen):")
    for dealer in input_plan["verified_cooperative_dealers"]:
        print(f"  🏢 {dealer['facility_name']} ({dealer['entity_type']})")
        print(f"     Contact: {dealer['contact_person']} | Phone: {dealer['phone']}")
        print(f"     Address: {dealer['address']}")
        print(f"     Available Stocks: {', '.join(dealer['stocks_available'])}")

    print("\n" + "=" * 70)
    print("✅ All Person 1 tests completed successfully! Ready for Person 2 integration.")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
