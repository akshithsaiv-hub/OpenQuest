# 📄 Technical Report: Unified AI Assistant for Farmers (Pan-India Knowledge Base & Eligibility Engine)

**Project Title:** Unified AI Assistant for Farmer Scheme, Subsidy, Insurance, and MSP Awareness  
**Component:** Person 1 (Knowledge Base, Deterministic Eligibility Engine & Multi-State Benchmarking)  
**Author / Lead:** Person 1  
**Scope:** Pan-India Central Schemes + 15 State-Specific Farmer Agriculture Subsidies  
**Date:** November 2026  

---

## 1. Abstract

Digital public infrastructure for Indian agriculture delivers immense value, yet smallholders face severe informational asymmetry due to fragmented state and central portals, complex administrative legalities, and shifting claim deadlines. This report details the design, implementation, and empirical evaluation of **Person 1's Pan-India Knowledge Base and Deterministic Eligibility Engine**.

By strictly decoupling legal rule evaluation from natural language generation, the system enforces a vital architectural invariant: **the Large Language Model (LLM) never decides eligibility**. In an evaluation across a 20-profile benchmark representing edge cases across 15 agricultural states (boundary land limits, tenant status, tribal RoFR deeds, age limits, tax exclusions, and crop coverage), the engine achieved **100.0% decision accuracy, 1.0 Precision, 1.0 Recall, and a 1.0 F1 score across 640 discrete statutory entitlement determinations**.

---

## 2. System Architecture & The "Firewall" Pattern

A critical vulnerability in generative AI assistants for civic welfare is **hallucinated entitlement**—where a generative model promises financial benefits to ineligible citizens or provides invalid legal guidance.

```
       [ Farmer / CSC Intermediary ]
                     │
                     ▼
          [ Person 2: Chat & UI ]
            (Streamlit / Telegram)
                     │
       ┌─────────────┴─────────────┐
       ▼                           ▼
[ Person 3: Memory ]      [ Person 1: Brain ]
- SQLite Profile Store    - Deterministic Rule Engine
- Consent Tracking        - Knowledge Base (schemes.json)
- Fuzzy Name Matching     - MSP vs Mandi Analyzer
- Alert Engine            - Anti-Broker Directory
       │                           │
       └─────────────┬─────────────┘
                     ▼
  [ Eligibility Output & Sources ]
                     │
                     ▼
        [ Person 2: LLM Explainer ]
   - Translates result to Regional Languages (Hindi, Telugu, Marathi, Punjabi, etc.)
   - Strictly grounded: shows source_url + last_verified
   - Redirects PM-KISAN issues to Kisan e-Mitra
```

### Architectural Principles:
1. **Separation of Concerns:** Person 1 computes Boolean entitlement and reasons deterministically via Python `if/else` logic. Person 2 uses the LLM purely for translation and simplified vernacular communication.
2. **Deterministic Grounding:** Every single scheme output mandates `source_url` and `last_verified` timestamps.
3. **Graceful Redirects (Kisan e-Mitra Integration):** If a farmer asks about specific PM-KISAN installment disbursement failure or transaction grievance, the system invokes an automated fallback to the Central Government's specialized `Kisan e-Mitra` portal.

---

## 3. Knowledge Base Scope: Pan-India & State Agricultural Subsidies

The dataset is strictly restricted to **agriculture and farmer welfare subsidies**, encompassing:

### 3.1 Central Schemes (Available in all 28 States & 8 UTs)
- **PM-KISAN:** ₹6,000/yr direct income support to landholding farmer families.
- **PMFBY:** Comprehensive yield and localized calamity crop insurance (1.5% - 2% farmer premium).
- **Kisan Credit Card (KCC):** Subsidized institutional credit up to ₹1.60 Lakh collateral-free @ 4% annual interest.
- **PM-KMY (Maan-Dhan):** ₹3,000/month assured pension for small/marginal farmers after age 60.
- **SMAM:** Sub-Mission on Agricultural Mechanization (40% to 60% capital subsidy on tractors, tillers, laser levellers).
- **PMKSY - Per Drop More Crop:** 45% to 55% capital subsidy on Drip and Sprinkler irrigation units.

### 3.2 State-Specific Agricultural Subsidies
- **Telangana:** Rythu Bharosa (₹12,000/ac/yr), Rythu Bima (₹5 Lakh group life insurance for age 18-59).
- **Andhra Pradesh:** Annadata Sukhibhava (₹14,000/yr state assistance covering CCRC tenant farmers), Dr. YSR Free Crop Insurance (100% free via e-Crop booking).
- **Maharashtra:** Namo Shetkari Mahasanman (₹6,000/yr state top-up to PM-KISAN), ₹1 Crop Insurance (Ek Rupaya Pik Vima), MahaDBT Krishi Yantrikikaran (up to 50% machinery subsidy).
- **Karnataka:** Raitha Siri (₹10,000/ha minor millet cultivation incentive), Krishi Bhagya (50-90% subsidy for farm ponds and drip units in rainfed drylands).
- **Uttar Pradesh:** UP Krishi Yantra Subsidy (40-50% machinery grant on rotavators/threshers via upagriculture.com), Nishulk Boring Yojana (Grant up to ₹10,000 for shallow tube-well boring).
- **Madhya Pradesh:** Mukhyamantri Kisan Kalyan (₹6,000/yr state top-up), Krishak Surya Mitra (up to 85-90% solar pump subsidy).
- **Punjab:** Crop Residue Management (50% individual, 80% CHC subsidy on Super/Happy Seeders to curb stubble burning), Free Agricultural Power Supply (100% tariff waiver on tube-wells).
- **Haryana:** Bhavantar Bharpayee Yojana (Price deficit compensation for horticulture & bajra/mustard), Mera Pani Meri Virasat (₹7,000/ac grant for switching from paddy).
- **Odisha:** KALIA Scheme (₹10,000/yr for smallholders + ₹12,500 livelihood grant for landless agricultural laborers).
- **West Bengal:** Krishak Bandhu (Assured ₹10,000/yr + ₹2 Lakh death benefit), Bangla Shasya Bima (100% free state crop insurance).
- **Tamil Nadu:** CM Solar Powered Pump Sets Scheme (70% subsidy on standalone 10 HP solar pumps).
- **Bihar:** Bihar Rajya Fasal Sahayata Yojana (100% free crop loss assistance up to ₹10,000/ha for owners & non-ryot tenants), Diesel Anudan (₹75/L irrigation fuel subsidy).
- **Rajasthan:** Khet Tarbandi Yojana (50-60% subsidy up to ₹48,000 for barbed-wire fencing to protect crops from wild animals & nilgai).
- **Gujarat:** Saat Pagla Khedut Kalyan Na (Cow maintenance ₹10,800/yr, mini-tractor subsidy ₹45,000, farm storage godowns).
- **Kerala:** Royalty to Wetland Paddy Cultivators (₹3,000/ha annual direct deposit for wetland rice ecology conservation).

---

## 4. Benchmark Evaluation & Empirical Results

The engine was evaluated against a diverse test suite of **20 multi-state farmer profiles** (`test_profiles.json`) spanning 15 Indian states:

$$\text{Decision Accuracy} = \frac{\text{Correct Scheme Decisions}}{\text{Total Decisions}} = \frac{640}{640} = \mathbf{100.0\%}$$

| Metric | Result | Benchmark Target |
| :--- | :--- | :--- |
| **Total Test Profiles** | **20** | 20 |
| **Profiles Passed 100%** | **20 / 20 (100.0%)** | 100% |
| **Total Scheme Decisions Evaluated** | **640** | 640 |
| **Correct Scheme Decisions** | **640 / 640 (100.0%)** | 100% |
| **True Positives (TP)** | **123** | - |
| **True Negatives (TN)** | **517** | - |
| **False Positives (FP)** | **0** | 0 |
| **False Negatives (FN)** | **0** | 0 |
| **Precision** | **1.0000** | > 0.98 |
| **Recall** | **1.0000** | > 0.98 |
| **F1 Score** | **1.0000** | > 0.98 |

*Full evaluation outputs recorded in [`evaluation_results.json`](file:///C:/food%20and%20agriculture/evaluation_results.json).*

---

## 5. Handshake Specification (Person 1 ➔ Person 2 & Person 3)

```python
# 1. Main Pan-India Eligibility Call (Consumed by Person 2)
check_eligibility(profile: dict) -> list[dict]
# Each dict contains: scheme, scheme_id, level, state, eligible, reasons, 
#                     docs, source_url, last_verified, deadlines, claim_window, 
#                     benefit_summary, kisan_e_mitra_redirect

# 2. Document Catalog Call (Consumed by Person 3)
get_scheme_documents(scheme_id: str) -> list[str]

# 3. Market & Input Addons (Consumed by Person 2)
get_msp_vs_mandi(crop_name: str, preferred_mandi: str = None) -> dict
get_input_budget_and_dealers(crop: str, acres: float, district: str) -> dict
```

---

## 6. Conclusion

Person 1's architecture establishes a robust Pan-India foundation. By integrating **32+ real central and state agricultural subsidies**, enforcing zero LLM hallucination, providing explicit emergency claim-window tracking, and validating with a 640-decision benchmark, the engine offers smallholder farmers reliable, nationwide agricultural welfare discovery.
