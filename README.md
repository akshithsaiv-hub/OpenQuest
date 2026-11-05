# 🌾 OpenQuest: Unified AI Assistant for Farmer Scheme, Subsidy, Insurance and MSP Awareness

**Theme:** Agriculture and Food Systems  
**Scope:** Pan-India Central Government Schemes + State-Specific Agriculture Subsidies (Telangana, Andhra Pradesh, Maharashtra, Karnataka, Uttar Pradesh, Madhya Pradesh, Punjab, Haryana, Odisha, West Bengal, Tamil Nadu, Bihar, Rajasthan, Gujarat, Kerala)  
**Target Beneficiaries:** Small & Marginal Farmers, Oral Tenant Cultivators, Tribal RoFR Patta Holders, and Village Intermediaries (CSC Operators, AEOs, FPOs)  
**Repository:** [https://github.com/akshithsaiv-hub/OpenQuest](https://github.com/akshithsaiv-hub/OpenQuest)

---

## 🏛️ System Architecture & Capabilities

This repository unites deterministic scheme eligibility, real-time climate risk mitigation, statutory insurance countdowns, and institutional credit guidance:

```text
OpenQuest/
│
├── 🧠 KNOWLEDGE BASE & DETERMINISTIC ENGINES
│   ├── schemes.json             # 32+ Pan-India Central & State-Specific Farmer Agriculture Subsidies
│   ├── data/water_saving_schemes.json # PMKSY-PDMC (Drip/Sprinkler 55-100%), PM-KUSUM B/C, TSMIP
│   ├── data/disaster_relief.json      # SDRF/NDRF statutory norms (₹8.5k-₹22.5k/ha) & calamity ex-gratia
│   ├── data/low_water_crops.json      # ID crops post-drought (Bengal Gram, Moong, Sesame, Groundnut) + MSP
│   ├── msp_mandi.json           # MSP vs Mandi benchmark market data across Indian APMCs
│   ├── farm_inputs.json         # PJTSAU/ICAR input budgets & direct PACS/FPO dealer contacts
│   ├── engine.py                # Deterministic rule engine (check_eligibility, evaluate_farmer_profile)
│   ├── engine_addons.py         # MSP comparison & input budgeting modules
│   └── test_profiles.json       # 20 diverse farmer benchmark profiles across Indian states
│
├── ⚡ 72-HOUR CLAIM ASSISTANT & CLIMATE SHIELD
│   ├── utils/claim_assistant.py # 72-hr countdown timer, geo-tagged photo checklist, legal intimation SMS
│   ├── utils/weather_api.py     # Open-Meteo multi-hazard engine (Drought, Flood, Heat Wave, Pests)
│   ├── utils/credit_kcc.py      # KCC Scale of finance, 4% interest subvention (MISS), repayment scheduler
│   ├── utils/document_wallet.py # Consent-based vault for Aadhaar, Pahani, CCRC; DigiLocker & AgriStack ID
│   ├── utils/status_tracker.py  # Manual application status logger with SLA breach warnings
│   ├── utils/escalation_feedback.py # Scheme feedback flags & formal higher authority grievance petitions
│   ├── utils/llm.py             # Multilingual explainer, strict rules & fallback routing
│   └── utils/translation.py     # Localized Telugu (తెలుగు), Hindi (हिंदी), and English strings
│
├── 🖥️ USER INTERFACES & RUNNERS
│   ├── ui/streamlit_app/app.py  # 8-Tab Unified Web App:
│   │                            # 0. State & Central Scheme Browser (Mobile-First Explorer)
│   │                            # 1. Scheme Eligibility & Chat
│   │                            # 2. Climate Risk & 72-Hr Claim Shield (with SDRF/NDRF)
│   │                            # 3. Water Subsidies & Next-Crop Planning
│   │                            # 4. KCC Credit Help & Application Status Tracker
│   │                            # 5. Document Wallet & DigiLocker
│   │                            # 6. MSP vs Mandi Tracker
│   │                            # 7. Intermediary Desk, Feedback Loop & Grievance Escalation
│   ├── ui/telegram_bot/bot.py   # Telegram bot with CLI demo & commands (/claim_alert, /kcc_help, etc.)
│   ├── frontend/                # Lightweight mobile-responsive static web interface (HTML/CSS/JS)
│   └── backend/eligibility_api.py # FastAPI backend with fuzzy document verification & mock DB
│
└── 🧪 BENCHMARKS & TESTS
    ├── tests/test_assistant.py  # 17 automated unit tests (100% passing)
    ├── test_runner.js           # 640-decision Pan-India verification suite
    ├── evaluate_engine.py       # Python benchmark evaluation script
    └── demo.py                  # End-to-end multi-scenario CLI test runner
```

---

## 🌟 Key Functional Highlights

### 1. ⏱️ 72-Hour Claim Assistant with Live Countdown
- Under PMFBY and State Calamity regulations, individual crop losses (hail, flooding, cloudburst) **must be intimated within 72 hours**.
- Provides a real-time countdown timer (`00h 00m 00s`), color-coded urgency banner, geo-tagged photo guidance, and one-click SMS/WhatsApp intimation generator.

### 2. 🚿 Water-Saving Subsidy Matcher (PMKSY, PM-KUSUM, TSMIP)
- Automatically suggests drip/sprinkler and solar pump schemes when water risk is detected.
- Incorporates state-specific rules: 100% subsidy for SC/ST farmers and 90% for BC smallholders in Telangana (TSMIP).
- Standalone off-grid solar pumps covered up to 60% under PM-KUSUM Component B.

### 3. 🌱 Next-Season Crop & Water Planning
- Proactively suggests low-water alternative crops (Bengal Gram, Green Gram, Sesame, Groundnut, Millets) after a water-stressed season.
- Displays water savings % (up to 85%), expected duration, and statutory MSP support (e.g., Sesame MSP ₹9,267/qtl).

### 4. 💳 Kisan Credit Card (KCC) & 4% Interest Subvention
- Calculates District Level Technical Committee (DLTC) Scale of Finance per acre.
- Illustrates Modified Interest Subvention Scheme (MISS): 9% commercial rate - 2% Govt subvention - 3% prompt repayment incentive = **4% net effective annual interest**.
- Warns farmers regarding seasonal due dates (Kharif: March 31; Rabi: June 30).

### 5. 📁 Consent-Driven Document Wallet & DigiLocker
- Stores encrypted records of Aadhaar, Pahani/Dharani passbooks, CCRC tenancy agreements, and bank passbooks.
- Privacy-first automatic masking (e.g. `XXXX-XXXX-4921`).
- Evaluates document readiness percentage for each scheme before application.

### 6. 🏛️ Report to Higher Official (Grievance Escalation)
- When a claim or subsidy is stalled or rejected unlawfully, generates a formal, legally grounded grievance petition.
- Configured for 4 escalation tiers: AEO (Rythu Vedika) ➔ Mandal Agriculture Officer ➔ District Agriculture Officer / Prajavani ➔ Central CPGRAMS (`pgportal.gov.in`).

### 7. 📶 Offline & Low-Tech Mode
- Gracefully operates with cached meteorology and deterministic local rules without cloud dependencies.
- Features standardized SMS keyword syntax for feature phone users without internet access.

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run All 17 Unit Tests
python -m unittest discover -s tests

# 3. Launch Streamlit Web App
python -m streamlit run ui/streamlit_app/app.py

# 4. Launch Telegram Bot (Interactive Test Mode)
python ui/telegram_bot/bot.py --test
```
