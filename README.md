# 🌾 OpenQuest: Unified AI Assistant for Farmer Scheme, Subsidy, Insurance and MSP Awareness

**Theme:** Agriculture and Food Systems  
**Scope:** Pan-India Central Government Schemes + State-Specific Agriculture Subsidies (Telangana, Andhra Pradesh, Maharashtra, Karnataka, Uttar Pradesh, Madhya Pradesh, Punjab, Haryana, Odisha, West Bengal, Tamil Nadu, Bihar, Rajasthan, Gujarat, Kerala)  
**Target Beneficiaries:** Small & Marginal Farmers, Oral Tenant Cultivators, Tribal RoFR Patta Holders, and Village Intermediaries (CSC Operators, AEOs, FPOs)  
**Repository:** [https://github.com/akshithsaiv-hub/OpenQuest](https://github.com/akshithsaiv-hub/OpenQuest)

---

## 🏛️ System Architecture & Team Roles

This repository unites the core intelligence and interactive interfaces across roles:

```text
OpenQuest/
│
├── 🧠 PERSON 1 (The "Brain" & Knowledge Base)
│   ├── schemes.json             # 32+ Pan-India Central & State-Specific Farmer Agriculture Subsidies
│   ├── msp_mandi.json           # MSP vs Mandi benchmark market data across Indian APMCs
│   ├── farm_inputs.json         # PJTSAU/ICAR input budgets & direct PACS/FPO dealer contacts
│   ├── engine.py                # Deterministic rule engine (check_eligibility, evaluate_farmer_profile)
│   ├── engine_addons.py         # MSP comparison & input budgeting modules
│   ├── test_profiles.json       # 20 diverse farmer benchmark profiles across Indian states
│   ├── test_runner.js           # Automated benchmark runner (100% decision accuracy across 640 decisions)
│   ├── evaluate_engine.py       # Python benchmark evaluation script
│   ├── evaluation_results.json  # Full benchmark metrics report
│   ├── research_gap_analysis.md # Detailed gap research vs Kisan e-Mitra & Farmer.CHAT
│   └── technical_report.md      # Comprehensive technical evaluation report
│
├── 🗣️ PERSON 2 (The "Face" & Multilingual Interface)
│   ├── ui/
│   │   ├── streamlit_app/app.py # Interactive web app (Farmer Chat + Intermediary Desk + MSP Tracker + Climate Shield)
│   │   └── telegram_bot/bot.py  # Telegram bot with multilingual commands (/water_alert) & CLI test mode
│   ├── utils/
│   │   ├── llm.py               # Multilingual LLM explainer, strict rules & fallback routing
│   │   ├── translation.py       # Localized Telugu (తెలుగు), Hindi (हिंदी), and English strings
│   │   └── weather_api.py       # Live Open-Meteo Climate API, 7-day forecast & rice water stress calculator
│   ├── backend/
│   │   └── eligibility_api.py   # FastAPI backend with fuzzy document verification, climate & alert dispatch
│   ├── data/
│   │   └── schemes_telangana.json # Person 2 complementary scheme catalog
│   ├── tests/
│   │   └── test_assistant.py    # Automated unit tests validating engine, fallbacks, climate API & fuzzy checks
│   └── DEMO_SCRIPT.md           # 3-minute hackathon presentation script with scene-by-scene narration
│
└── ⚙️ RUNNERS & SCRIPTS
    ├── demo.py                  # End-to-end multi-scenario CLI test runner
    ├── requirements.txt         # All Python dependencies
    └── README.md                # Project architecture & user guide
```

---

## 🎯 Pan-India Agricultural Subsidies Supported by Person 1

Every scheme is **strictly an agricultural / farmer subsidy** with verified criteria, documents, deadlines, emergency claim windows, and official links:

| Level / State | Flagship Agricultural Subsidies in Knowledge Base |
| :--- | :--- |
| **All States (Central)** | **PM-KISAN** (₹6,000/yr), **PMFBY** (Crop Insurance with 72-hr rule), **Kisan Credit Card** (4% loan), **PM-KMY** (Pension), **SMAM** (40-60% Farm Machinery Grant), **PMKSY-PDMC** (45-55% Drip/Sprinkler Subsidy) |
| **Telangana** | **Rythu Bharosa** (₹12,000/ac/yr), **Rythu Bima** (₹5 Lakh Life Insurance, 10-day nominee claim) |
| **Andhra Pradesh** | **Annadata Sukhibhava** (₹14,000/yr state assistance covering CCRC Tenants), **Dr. YSR Free Crop Insurance** (100% Free via e-Crop) |
| **Maharashtra** | **Namo Shetkari Yojana** (₹6,000/yr state top-up), **₹1 Crop Insurance** (Ek Rupaya Pik Vima), **MahaDBT Krishi Yantrikikaran** (50% Tractor/Machinery Subsidy) |
| **Karnataka** | **Raitha Siri** (₹10,000/ha Minor Millet Incentive), **Krishi Bhagya** (50-90% Farm Pond & Drip Subsidy) |
| **Uttar Pradesh** | **UP Krishi Yantra Subsidy** (40-50% Machinery Grant via upagriculture.com), **Nishulk Boring Yojana** (Free Tube Well Boring) |
| **Madhya Pradesh** | **Mukhyamantri Kisan Kalyan** (₹6,000/yr top-up), **Krishak Surya Mitra** (Up to 90% Solar Pump Subsidy) |
| **Punjab** | **Crop Residue Management Subsidy** (50-80% Happy Seeder / Super Seeder), **Free Agricultural Power Supply** (Zero tariff tube wells) |
| **Haryana** | **Bhavantar Bharpayee Yojana** (Mandi price deficit compensation), **Mera Pani Meri Virasat** (₹7,000/ac for shifting from paddy) |
| **Odisha** | **KALIA Scheme** (₹10,000/yr for smallholders + ₹12,500 for landless agricultural workers) |
| **West Bengal** | **Krishak Bandhu** (Assured ₹10,000/yr + ₹2 Lakh death relief), **Bangla Shasya Bima** (100% Free State Crop Insurance) |
| **Tamil Nadu** | **CM Solar Powered Pump Sets Scheme** (70% Capital Subsidy on 10 HP Solar Pumps) |
| **Bihar** | **Bihar Rajya Fasal Sahayata Yojana** (100% Free Crop Loss Aid up to ₹10,000/ha for owners & tenant non-ryots), **Diesel Anudan** (₹75/L fuel subsidy) |
| **Rajasthan** | **Khet Tarbandi Yojana** (50-60% Barbed Wire Fencing Subsidy up to ₹48,000 against stray cattle) |
| **Gujarat** | **Saat Pagla Khedut Kalyan Na** (Mini-tractor subsidy ₹45,000, Cow maintenance ₹10,800/yr, Farm godowns) |
| **Kerala** | **Royalty to Wetland Paddy Cultivators** (₹3,000/ha annual direct deposit for wetland rice ecology conservation) |

---

## 🤝 Core API Handshake (For Person 2 UI & Person 3 Reminders)

```python
from engine import check_eligibility, evaluate_farmer_profile, get_scheme_documents, get_msp_vs_mandi

# 1. Main Eligibility Call (Deterministic - LLM never decides)
results = check_eligibility({
    "state": "Maharashtra",        # Any Indian State
    "district": "Yavatmal",
    "land_acres": 3.0,
    "is_tenant": False,
    "has_rofr_patta": False,
    "crops": ["Cotton", "Soybean"],
    "age": 42,
    "is_tax_payer": False
})

# 2. Document Checklist (For Person 3's check_documents)
docs = get_scheme_documents("pmfby")

# 3. Mandi vs MSP Arbitrage
mandi_intel = get_msp_vs_mandi("Cotton (Medium Staple)", "Warangal")
```

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run Person 1's Multi-State Benchmark Test (640 decisions, 100% accuracy)
node test_runner.js

# 3. Launch Streamlit Web App (Person 2)
streamlit run ui/streamlit_app/app.py

# 4. Launch Telegram Bot (Person 2)
python -m ui.telegram_bot.bot --test
```
