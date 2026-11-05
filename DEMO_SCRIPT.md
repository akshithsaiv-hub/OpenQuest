# 🌾 Rythu Sahayata: Demo Script & Presentation Guide

**Role:** Person 2 — Chat Interface, Multilingual Explanation & Intermediary Dashboard  
**Pilot State:** Telangana  
**Theme:** Agriculture and Food Systems

---

## 🎯 What Makes This Different From Generic Chatbots

| Generic Agricultural Chatbots (e.g. ChatGPT, Basic Bots) | **Rythu Sahayata (Our Unified Assistant)** |
|---|---|
| **Hallucinates eligibility:** LLM guesses if a farmer qualifies for a subsidy. | **Deterministic eligibility engine:** Pure rule-based matching (Person 1). The LLM **only explains** the result; it **never decides eligibility**. |
| **No traceability:** Gives dates and figures with zero provenance. | **Auditable provenance:** **Every** scheme response includes the official government source URL and a "Last Verified" date. |
| **Duplicates official portals:** Tries and fails to look up PM-KISAN payment status. | **Intelligent Fallback Routing:** Seamlessly redirects payment & grievance queries to the official **Kisan e-Mitra** portal. |
| **Answers blindly:** Fabricates answers to unknown or unverified local policies. | **Graceful Escalation:** When a rule is unverified, directs the farmer to their local **Agriculture Extension Officer (AEO) at the nearest Rythu Vedika**. |
| **Ignores intermediaries:** Designed only for smartphone users who type English. | **Dual-Channel Reach:** Farmer chat in Telugu/Hindi/English + an **Intermediary Mode** for CSC operators, AEOs, and FPO staff managing dozens of farmers. |

---

## 🎬 3-Minute Live Demo Walkthrough

### **Scene 1: Farmer Self-Service in Telugu & Multilingual Chat (0:00 - 1:00)**
1. **Open the Streamlit App:**
   - Notice the Language selector in the sidebar: Toggle between **English**, **Telugu (తెలుగు)**, and **Hindi (हिंदी)**.
   - All UI headers, form fields, and explanations switch instantly to the farmer's language.
2. **Profile Input & Consent:**
   - Enter profile: State = **Telangana**, District = **Warangal**, Land = **2.2 Acres** (Marginal farmer), Crop = **Paddy**, Farmer Category = **Marginal**, Functional well = **Yes**.
   - Notice the **Consent Checkbox** ("I consent to storing my farm details to receive proactive alerts").
3. **Run Eligibility:**
   - Click **"Check My Scheme Eligibility"**.
   - Show the 5 matched schemes:
     - **Rythu Bharosa (Telangana)**: ₹15,000/acre/year directly via DBT.
     - **PM-KISAN (Central)**: ₹6,000/year in 3 installments.
     - **PMFBY Rabi Crop Insurance**: Enrolment cut-off date (`2026-11-15`) and **critical 72-hour crop loss reporting window**.
     - **Telangana Micro Irrigation Project (TSMIP)**: 90% subsidy for marginal farmers.
     - **MSP Procurement**: Guaranteed procurement at ₹2,820/quintal (MSP ₹2,320 + Telangana state bonus ₹500).
   - Point out: **Every scheme card features the official government URL and last verified date (`2026-10-28` to `2026-11-02`).**

---

### **Scene 2: Fallback Handling (1:00 - 1:40)**
1. **PM-KISAN Status Inquiry:**
   - Click the test button: *"When will my PM-KISAN 19th installment 2000 rupees payment come?"*
   - **Observe:** The system does **NOT** hallucinate a payment date. It cleanly triggers the **Kisan e-Mitra redirect notice** with the direct link to `https://pmkisan.gov.in` and the toll-free helpline `155261`.
2. **Unverified / Out-of-Scope Query:**
   - Click the test button: *"How to get bitcoin crypto subsidy loan?"*
   - **Observe:** The system flags uncertainty and immediately triggers the **Local Agriculture Officer (AEO) at Rythu Vedika fallback** to prevent misleading the farmer.

---

### **Scene 3: Intermediary Mode (CSC Operators & Extension Staff) (1:40 - 2:30)**
1. Switch to **Tab 2: Intermediary Mode**.
2. **Dashboard Overview:**
   - See high-level metrics: *Total Farmers Tracked (5)*, *Pending Documents (3)*, *Aadhaar-Bank Mismatches (2)*, *Urgent Deadlines (2)*.
3. **Farmer Tracking Table & Fuzzy Document Matcher:**
   - Inspect Farmer **Komirelli Ramulu** (`TS-WAR-001`):
     - Aadhaar Name: `Komirelli Ramulu`
     - Bank Passbook Name: `K. Ramulu`
     - Rapidfuzz match score: **85%** (Minor mismatch flagged for CSC attestation before DBT rejection).
   - Inspect Farmer **Banoth Padma** (`TS-KHM-003`):
     - **Critical Red Alert**: *72-hour crop loss claim reporting window closes in 48 hours!*
     - Missing: Crop damage photos and CCRC agreement copy.
4. **Proactive Alert Dispatch:**
   - Click **"📲 Send Alert SMS / WhatsApp"**.
   - Notice the instant notification dispatched directly to the farmer in Telugu, demonstrating proactive outreach.

---

### **Scene 4: MSP vs Mandi Price Tracker (2:30 - 3:00)**
1. Switch to **Tab 3: MSP vs Mandi Price Tracker**.
2. Show the real economic impact:
   - Paddy open mandi price: **₹2,180/quintal**.
   - Government procurement price (MSP + Telangana ₹500 bonus): **₹2,820/quintal**.
   - Net gain to farmer: **+₹640/quintal** by selling through official PACS/IKP procurement centers.

---

## 💻 How to Run the Demo Locally

```powershell
# In terminal:
cd C:\Users\akshi\.gemini\antigravity\scratch\farmer-assistant

# Run Streamlit (Farmer Chat + Intermediary Dashboard + MSP Tracker)
streamlit run ui/streamlit_app/app.py

# Optional: Run Telegram Bot CLI validation
python ui/telegram_bot/bot.py --test

# Run unit tests
python tests/test_assistant.py
```
