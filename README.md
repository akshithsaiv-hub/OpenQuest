# 🌾 OpenQuest: Unified AI Assistant for Farmer Scheme, Subsidy, Insurance and MSP Awareness

**Theme:** Agriculture and Food Systems  
**Pilot State:** Telangana  
**Target Beneficiaries:** Small & Marginal Farmers, Oral Tenant Cultivators, Tribal RoFR Patta Holders, and Village Intermediaries (CSC Operators, AEOs, FPOs)

---

## 🏛️ System Architecture & Team Roles

This repository unites the core intelligence and interactive interfaces across roles:

```text
OpenQuest/
│
├── 🧠 PERSON 1 (The "Brain" & Knowledge Base)
│   ├── schemes.json             # Curated, verified Central & Telangana scheme database
│   ├── msp_mandi.json           # MSP vs Mandi benchmark market data across Telangana APMCs
│   ├── farm_inputs.json         # PJTSAU/ICAR input budgets & direct PACS/FPO dealer contacts
│   ├── engine.py                # Deterministic rule engine (check_eligibility, evaluate_farmer_profile)
│   ├── engine_addons.py         # MSP comparison & input budgeting modules
│   ├── evaluate_engine.py       # Benchmark evaluation script (100% decision accuracy across 20 profiles)
│   ├── evaluation_results.json  # Full benchmark metrics report
│   ├── research_gap_analysis.md # Detailed gap research vs Kisan e-Mitra & Farmer.CHAT
│   └── technical_report.md      # Person 1 technical evaluation report
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
│   │   └── test_assistant.py    # 8 automated unit tests validating engine, fallbacks, climate API & fuzzy checks
│   └── DEMO_SCRIPT.md           # 3-minute hackathon presentation script with scene-by-scene narration
│
├── ⚙️ RUNNERS & SCRIPTS
│   ├── demo.py                  # End-to-end multi-scenario CLI test runner
│   ├── requirements.txt         # All Python dependencies
│   └── README.md                # Project architecture & user guide
```

---

## 🎯 What Sets This Solution Apart

| Traditional AI Agricultural Bots | **Our Unified Assistant (OpenQuest)** |
|---|---|
| **Hallucinates eligibility:** Guesses if a farmer qualifies for benefits. | **Deterministic eligibility engine:** 100% rule-based matching. LLM **only explains** the verified result. |
| **No provenance:** Quotas and dates are stated without references. | **Traceable grounding:** **Every** response includes official source URLs and **last verified dates**. |
| **Duplicates official portals:** Tries and fails to look up PM-KISAN installment status. | **Intelligent fallback routing:** Seamlessly redirects payment queries to the official **Kisan e-Mitra** portal (`https://pmkisan.gov.in`). |
| **Answers blindly:** Fabricates answers to unverified or out-of-scope policies. | **Graceful escalation:** Directs farmers to their local **Agriculture Extension Officer (AEO) at the nearest Rythu Vedika**. |
| **Ignores intermediaries:** Designed only for smartphone users typing in English. | **Intermediary mode:** Dedicated dashboard for CSC operators and AEOs with **Aadhaar-Bank fuzzy name mismatch checks (`rapidfuzz`)** to prevent DBT rejections. |

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Run Person 1 Benchmark Evaluation (100% Accuracy)
```powershell
python evaluate_engine.py
```

### 3. Run Person 1 End-to-End Demo
```powershell
python demo.py
```

### 4. Run Person 2 Automated Test Suite (6 Tests)
```powershell
python tests/test_assistant.py
```

### 5. Run Telegram Bot in CLI Validation Mode
```powershell
python ui/telegram_bot/bot.py --test
```

### 6. Launch the Interactive Web Application (Streamlit)
```powershell
python -m streamlit run ui/streamlit_app/app.py
```
*Opens at `http://localhost:8501` featuring:*
1. **Farmer Self-Service Tab:** Multilingual (Telugu/Hindi/English) consent-based scheme eligibility.
2. **Intermediary Desk Tab:** Pending document tracker, approaching cut-offs, and instant Aadhaar-Bank fuzzy name verification.
3. **MSP vs Mandi Tracker Tab:** Real-time price delta (+₹640/quintal for Telangana Paddy) and official procurement yard locations.
