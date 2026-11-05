# 🌾 OpenQuest: Unified AI Assistant for Farmer Scheme, Subsidy, Insurance and MSP Awareness

**Theme:** Agriculture and Food Systems  
**Scope:** Pan-India Central Government Schemes + State-Specific Agriculture Subsidies (Telangana, Andhra Pradesh, Maharashtra, Karnataka, Uttar Pradesh, Madhya Pradesh, Punjab, Haryana, Odisha, West Bengal, Tamil Nadu, Bihar, Rajasthan, Gujarat, Kerala)  
**Target Beneficiaries:** Small & Marginal Farmers, Oral Tenant Cultivators, Tribal RoFR Patta Holders, and Village Intermediaries (CSC Operators, AEOs, FPOs)  
**Repository:** [https://github.com/akshithsaiv-hub/OpenQuest](https://github.com/akshithsaiv-hub/OpenQuest)

---

## 🏛️ System Architecture & Capabilities

This repository unites deterministic scheme eligibility, real-time climate risk mitigation, statutory insurance countdowns, institutional credit guidance, and complete farmer backend management:

```text
OpenQuest/
│
├── 🧠 KNOWLEDGE BASE & DETERMINISTIC ENGINES (Person 1)
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
├── 💾 FARMER BACKEND, CONSENT & VERIFICATION (Person 3)
│   ├── person3/
│   │   ├── farmer_database.py       # SQLite connection manager & auto-schema setup
│   │   ├── farmer_profiles.py       # Profile CRUD, validations & duplicate prevention
│   │   ├── consent_manager.py       # Mandatory opt-in terms & instant consent revocation
│   │   ├── document_checker.py      # RapidFuzz name mismatch detector & document readiness
│   │   ├── reminder_engine.py       # Smart deadline engine & claim-window priority
│   │   ├── intermediary_backend.py  # CSC/FPO facilitator operational dashboard backend
│   │   ├── test_person3.py          # 12 automated unit and integration tests (100% passing)
│   │   ├── README.md                # Comprehensive Person 3 technical guide
│   │   └── requirements.txt         # Person 3 dependencies (rapidfuzz)
│   ├── person3_backend.py           # Unified runnable demo & integration hub
│   └── database/farmer_data.db      # Auto-generated SQLite database
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
├── 🖥️ USER INTERFACES & RUNNERS (Person 2)
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
    ├── person3/test_person3.py  # 12 Person 3 backend unit tests (100% passing)
    ├── test_runner.js           # 640-decision Pan-India verification suite
    ├── evaluate_engine.py       # Python benchmark evaluation script
    └── demo.py                  # End-to-end multi-scenario CLI test runner
```

---

## 🌟 Key Functional Highlights

### 1. ⏱️ 72-Hour Claim Assistant with Live Countdown
- Under PMFBY and State Calamity regulations, individual crop losses (hail, flooding, cloudburst) **must be intimated within 72 hours**.
- Provides a real-time countdown timer (`00h 00m 00s`), color-coded urgency banner, geo-tagged photo guidance, and one-click SMS/WhatsApp intimation generator.

### 2. 🚿 Diversified Water-Saving Subsidy Matcher (18+ Schemes Across India)
- Automatically matches farmers across all Indian states to 18+ verified Central & State water conservation schemes:
  - **PMKSY - Per Drop More Crop (PDMC)**: 55% Central baseline for Drip & Sprinkler (up to 90-100% in progressive states).
  - **PMKSY - Har Khet Ko Pani (HKKP)** & **Watershed Development Component (WDC 2.0)**: Surface minor irrigation, RRR of tanks, and ridge-to-valley recharge.
  - **PM-KUSUM Components A, B & C**: 500kW-2MW solar plants on barren land, standalone solar pumps (up to 60% subsidy), and feeder level solarisation with net metering.
  - **State-Specific Schemes**: **TSMIP (Telangana)** (100% SC/ST, 90% BC), **APMIP (Andhra Pradesh)** (90-100% Rayalaseema dry tracts), **Magel Tyala Shet Tale (Maharashtra)** (₹50k-₹75k farm pond grant), **Krishi Bhagya (Karnataka)** (80-90% farm pond/micro-irrigation package), **GGRC & SKY (Gujarat)** (70% drip + solar power sale), **Mera Pani Meri Virasat (Haryana)** (₹7,000/ac cash incentive to shift from paddy + 85% drip subsidy), **UGPL (Punjab)** (50% subsidy on underground PVC irrigation piping), **Tamil Nadu Micro Irrigation** (100% subsidy for small/marginal farmers), **Rajasthan Khet Talai** (₹1.20 Lakh subsidy on plastic-lined ponds), and **MP Balram Talab** (up to ₹1 Lakh pond subsidy).

### 3. 🌱 Next-Season Crop & Water Planning (26+ Diversified Low-Water Alternatives)
- Proactively suggests 26+ resilient alternative crops after water-stressed seasons spanning all major agro-climatic zones:
  - **Pulses**: Bengal Gram (Chana - MSP ₹5,440), Kabuli Chickpea (₹9k-12k market), Green Gram (Moong - MSP ₹8,682, 60 days duration), Black Gram (Urad - MSP ₹7,400, zero-till rice fallow), Red Gram (Tur/Arhar - MSP ₹7,550), Horse Gram (Kulthi/Ulavalu - 88% water savings), Cowpea (Lobia), and Lentil (Masoor - MSP ₹6,700).
  - **Oilseeds**: Sesame (Til/Nuvvulu - MSP ₹9,267, highest MSP oilseed, 85% water savings), Groundnut (Peanut - MSP ₹6,783), Mustard & Rapeseed (Sarson - MSP ₹5,650), Safflower (Kardi/Kusum - MSP ₹5,800, deep taproot), Sunflower (MSP ₹7,280), Castor (Arandi), Linseed (Alsi - MSP ₹6,200), and Soybean (MSP ₹4,892).
  - **Nutri-Cereals / Shree Anna (Millets)**: Sorghum (Jowar - MSP ₹3,371), Pearl Millet (Bajra - MSP ₹2,625, heat tolerant to 45°C), Finger Millet (Ragi - MSP ₹4,290), Foxtail Millet (Korra - 70 days), Little Millet (Samalu), Barnyard Millet (Sanwa - ready in 6 weeks), Kodo Millet (Arikalu), and Proso Millet (Cheena - 88% water savings).
  - **Commercial & Fodder**: Cluster Bean (Guar - MSP ₹5,200, industrial export gum) and Barley (Jau - MSP ₹1,850, salinity & drought champion).

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

### 7. 💾 Person 3 Backend: Profile Persistence, Consent & Verification
- **SQLite Storage**: Zero-configuration local database at `database/farmer_data.db` with indexed `intermediary_id` and `consent_status`.
- **Mandatory Consent & Revocation**: Enforces explicit opt-in and provides immediate one-click consent withdrawal (`withdraw_consent`).
- **RapidFuzz Bank-Name Matching**: Detects spelling variations (`Ravi Kumar` vs `Ravi Kumer`) with similarity scores and flags records for manual review to prevent Direct Benefit Transfer (DBT) failures without accusing users of fraud.
- **Smart Deadline Prioritization**: Automatically prioritizes critical insurance claim-windows (Priority 1) over regular application deadlines.
- **CSC/FPO Intermediary Mode**: Actionable worklist backend (`get_intermediary_farmers`) filtered by facilitator ID.

### 8. 📶 Offline & Low-Tech Mode
- Gracefully operates with cached meteorology and deterministic local rules without cloud dependencies.
- Features standardized SMS keyword syntax for feature phone users without internet access.

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run All 17 Core Assistant Tests
python -m unittest discover -s tests

# 3. Run All 12 Person 3 Backend Tests
python person3/test_person3.py

# 4. Run Person 3 Interactive Demo
python person3_backend.py

# 5. Launch Streamlit Web App
python -m streamlit run ui/streamlit_app/app.py

# 6. Launch Telegram Bot (Interactive Test Mode)
python ui/telegram_bot/bot.py --test
```
