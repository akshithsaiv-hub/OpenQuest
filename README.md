# 🌾 Unified AI Assistant for Farmers: Core Engine & Data (Person 1)

**Role:** Person 1 (The "Brain" & Data Engine)  
**Target Focus:** Telangana State (Small & Marginal Farmers, Tenant Farmers)  
**Location:** `C:\Users\tomka\.gemini\antigravity\scratch\farmer_schemes_engine`

---

## 🎯 What Person 1 Delivers

As **Person 1**, you own the **deterministic intelligence and ground truth data** of the system:
1. **Curated Scheme Knowledge Base (`schemes.json`)**: Central & State schemes with verified eligibility criteria, benefits, documents, and official links.
2. **Deterministic Eligibility Rule Engine (`engine.py`)**: Clear, rule-based Python logic (`evaluate_farmer_profile`) without hallucination.
3. **MSP vs Mandi Price Intelligence (`msp_mandi.json` & `compare_msp_mandi`)**: Compares official Minimum Support Prices with live Mandi rates to give clear "Sell at MSP" vs "Sell at Mandi" recommendations.
4. **Farm Input Planning & Anti-Broker Directory (`farm_inputs.json` & `get_input_planning`)**:
   - Recommended seed and fertilizer schedules (Urea, DAP, MOP) based on ICAR/Professor Jayashankar Telangana State Agricultural University (PJTSAU) recommendations.
   - Statutory Government capped MRPs (e.g. Urea @ ₹266.50/bag) to prevent overcharging.
   - Verified local directory of **Primary Agricultural Credit Societies (PACS)** and **Farmer Producer Organizations (FPOs)** with direct contact persons, phones, and addresses to bypass commission brokers.

---

## 📁 File Structure

```text
farmer_schemes_engine/
│
├── schemes.json        # Central & State scheme database (PM-KISAN, PMFBY, Rythu Bharosa, Rythu Bima, KCC, PM-KMY)
├── msp_mandi.json      # MSP 2024-25/2026 rates & live Mandi market data across Telangana
├── farm_inputs.json    # Standard per-acre input budgets & verified PACS/FPO direct contacts
├── engine.py           # Core rule engine & clean API functions for Person 2 & 3
├── demo.py             # Test script running 4 distinct farmer profiles & scenarios
└── README.md           # Interface contract & documentation
```

---

## 🤝 Team Interface Contract (How Person 2 & 3 Connect to Person 1)

### 1. Farmer Profile Schema (Shared with Person 3)
Person 3 saves or loads this dictionary, and Person 2 passes it to Person 1:

```python
farmer_profile = {
    "farmer_name": "Ramesh",
    "state": "Telangana",
    "district": "Warangal",
    "land_acres": 2.5,
    "is_tenant": False,            # Set True for oral lease / tenant farmers
    "has_rofr_patta": False,       # True if tribal RoFR title holder
    "crops": ["Paddy", "Cotton"],
    "age": 42,
    "category": "small",           # "marginal", "small", "medium", "large"
    "is_tax_payer": False
}
```

### 2. Scheme Eligibility Call
```python
from engine import evaluate_farmer_profile

result = evaluate_farmer_profile(farmer_profile)

# Output contains:
# - result["eligible_schemes"]: List of schemes with benefits, documents, deadlines, links
# - result["ineligible_schemes"]: Filtered schemes with exact reasons why (e.g. tenant restrictions)
# - result["total_direct_cash_benefit_annual"]: Total annual direct benefit amount in ₹
```

### 3. MSP vs Mandi Price Comparison Call
```python
from engine import compare_msp_mandi

analysis = compare_msp_mandi(crop_name="Paddy (Common)", preferred_mandi="Warangal")

# Output:
# - analysis["verdict"]: "SELL AT GOVT MSP CENTER" or "SELL IN OPEN MANDI"
# - analysis["price_difference_per_quintal"]: -₹120
# - analysis["action_advice"]: "Mandi price is ₹120 below MSP! Sell at PACS procurement center."
# - analysis["quality_standard_advisory"]: Moisture must be <17%
# - analysis["procurement_centers"]: List of local collection yards
```

### 4. Farm Input Planning & Direct Dealer Connection
```python
from engine import get_input_planning

budget_plan = get_input_planning(crop="Paddy", acres=2.5, district="Warangal")

# Output:
# - budget_plan["total_estimated_budget"]: Estimated seed + fertilizer cost
# - budget_plan["fertilizer_schedule"]: Exact bags of Urea, DAP, MOP required
# - budget_plan["budget_advisory"]: Statutory MRP reminder (Urea ₹266.50/bag)
# - budget_plan["verified_cooperative_dealers"]: List of genuine PACS/FPOs with phone numbers
```

---

## 🚀 Key Value Adds for Pitch & Demo

1. **Why not pure LLM for eligibility?**
   - *Pitch point:* Government scheme eligibility must be 100% deterministic and auditable. An LLM might hallucinate rules; our rule engine uses strict state legislation and circular parameters. The LLM (Person 2) acts as the multilingual explainer over Person 1's trusted decision engine.
2. **Tenant Farmer Transparency:**
   - Clearly tells tenant farmers where they qualify (PMFBY crop insurance, KCC loans with declaration) and where current state policy restricts them (Rythu Bharosa requires patta), preventing wasted trips to government offices.
3. **Zero-Broker Input Buying:**
   - Instead of giving vague fertilizer advice or pushing private commission dealers, the engine directs the farmer directly to their mandal's **PACS or FPO** with exact statutory MRPs and contact numbers.
