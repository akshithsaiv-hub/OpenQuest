# 🌾 Product Specification: Kisan Setu (OpenQuest)

## 1. Product Overview
- **Name:** Kisan Setu / Rythu Sahayata
- **Theme:** Agriculture & Food Systems
- **Core Purpose:** An accessible, multilingual, and deterministic agricultural welfare assistant that bridges the gap between fragmented government portals and Indian farmers. Identifies central and state subsidies, crop insurance claim windows, and MSP pricing without AI hallucination or bureaucratic jargon.

---

## 2. Target Users & User Mindset

### Primary Personas
1. **Small & Marginal Farmers (< 5 Acres):**
   - *Context:* Rely on seasonal rains, have limited digital literacy, operate low-to-mid range Android smartphones on intermittent 4G/5G networks.
   - *Mindset:* Anxious about deadlines, skeptical of complex circulars, fear of application rejection due to mismatched documents.
2. **Tenant Farmers & Sharecroppers (Oral Lessees):**
   - *Context:* Cultivate land without registered ownership deeds (Dharani/Webland/Khatauni).
   - *Mindset:* Often falsely believe they qualify for zero government assistance; need clear guidance on tenant-eligible schemes (e.g., PMFBY, KCC, BRFSY, CCRC cards).
3. **Village Intermediaries (CSC / VLE Operators & AEOs):**
   - *Context:* Run village kiosks or Rythu Vedikas helping 50–100 farmers a week apply for benefits.
   - *Mindset:* Need rapid batch lookup, document readiness checklists, and statutory claim-window alerts to assist farmers before windows expire.

---

## 3. Core Problems Solved
- **Scattered Information:** Replaces 30+ fragmented central and state portals with a single unified location-aware discovery tool.
- **Missed Emergency Windows:** Prioritizes critical time-sensitive cut-offs—specifically the **72-hour reporting rule** for localized crop insurance (PMFBY).
- **Distress Selling Below MSP:** Compares live modal APMC mandi rates against official CCEA Minimum Support Prices with instant "Sell at MSP" vs "Sell at Mandi" recommendations.
- **Predatory Middlemen:** Exposes statutory capped fertilizer MRPs (e.g., Urea @ ₹266.50/bag) and connects farmers directly to verified **PACS & FPO** cooperatives.

---

## 4. Key Product Invariants & Hard Constraints
1. **The LLM Never Decides Eligibility:** Legal entitlement is 100% deterministic (Python `if/else` rule engine with 100% test accuracy across 640 decisions). Generative AI only translates and simplifies.
2. **State-First Discovery:** Do not display schemes for a state until the user actively selects their State or Union Territory.
3. **Clear Government Attribution:** Every card must unmistakably communicate whether it is an `🇮🇳 Central Govt Scheme` or `🏛️ [State] State Scheme`.
4. **Mandatory Source Grounding:** Every recommendation provides a direct link to the official government portal (`source_url`) and a `last_verified` date.
5. **Persistent Multilingualism:** English is the default; selecting Telugu, Hindi, Marathi, Tamil, or Kannada instantly translates the UI and persists across the user's session.
