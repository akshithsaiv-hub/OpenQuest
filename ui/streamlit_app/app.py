import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
from rapidfuzz import fuzz

import sys
import os

# Add root folder to sys.path so utils can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.llm import process_farmer_query, generate_plain_explanation, FALLBACK_PMKISAN, FALLBACK_UNCERTAIN
from utils.translation import get_label, UI_LABELS

# Backend URL (can also run in embedded mode if backend is not running standalone)
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Rythu Sahayata - Unified Farmer Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f1f8e9;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
    }
    .warning-card {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
    }
    .danger-card {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
    }
    .scheme-badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        background-color: #e8f5e9;
        color: #2e7d32;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Language Selector in Sidebar
st.sidebar.image("https://img.icons8.com/color/96/wheat.png", width=64)
st.sidebar.title("రైతు సహాయత / किसान सहायता")

lang_option = st.sidebar.radio(
    "🌐 Choose Language / భాషను ఎంచుకోండి / भाषा चुनें",
    options=["English", "Telugu (తెలుగు)", "Hindi (हिंदी)"],
    index=0
)

LANG_MAP = {
    "English": "en",
    "Telugu (తెలుగు)": "te",
    "Hindi (हिंदी)": "hi"
}
curr_lang = LANG_MAP[lang_option]

st.markdown(f"""
<div class="main-header">
    <h1 style="margin:0; font-size: 2.1rem; color: #ffffff;">{get_label("app_title", curr_lang)}</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.05rem; opacity: 0.95; color: #f1f8e9;">
        {get_label("tagline", curr_lang)}
    </p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs([
    get_label("tab_farmer_chat", curr_lang),
    get_label("tab_intermediary", curr_lang),
    get_label("tab_msp", curr_lang)
])

# -------------------------------------------------------------
# TAB 1: Farmer Self-Service Chat & Eligibility Check
# -------------------------------------------------------------
with tab1:
    col_input, col_result = st.columns([1, 1.4], gap="large")

    with col_input:
        st.subheader(get_label("profile_header", curr_lang))

        # Consent Checkbox (Person 3 requirement)
        consent = st.checkbox(
            "🔒 I consent to storing my farm details to receive proactive deadline & payment alerts." if curr_lang == "en" else
            "🔒 గడువు మరియు చెల్లింపు సమాచారం కోసం నా వ్యవసాయ వివరాలను ఉపయోగించడానికి అంగీకరిస్తున్నాను." if curr_lang == "te" else
            "🔒 समय-सीमा एवं भुगतान संबंधी अलर्ट प्राप्त करने हेतु मैं अपनी कृषि जानकारी साझा करने की सहमति देता हूँ।",
            value=True
        )

        with st.form("farmer_profile_form"):
            state = st.selectbox(
                get_label("state_label", curr_lang),
                ["Telangana (Pilot State)", "Andhra Pradesh", "Karnataka", "Maharashtra"],
                index=0
            )
            clean_state = "Telangana" if "Telangana" in state else state

            district = st.selectbox(
                get_label("district_label", curr_lang),
                ["Warangal", "Nalgonda", "Khammam", "Karimnagar", "Nizamabad", "Mahabubnagar", "Suryapet"]
            )

            col_a, col_b = st.columns(2)
            with col_a:
                land_acres = st.number_input(
                    get_label("land_label", curr_lang),
                    min_value=0.1, max_value=50.0, value=2.2, step=0.1
                )
            with col_b:
                crop = st.selectbox(
                    get_label("crop_label", curr_lang),
                    ["Paddy", "Cotton", "Chilli", "Bengal Gram", "Maize", "Groundnut", "Soybean"]
                )

            col_c, col_d = st.columns(2)
            with col_c:
                category = st.selectbox(
                    get_label("category_label", curr_lang),
                    ["marginal (< 2.5 acres)", "small (2.5 - 5 acres)", "medium (5 - 10 acres)", "large (> 10 acres)"],
                    index=0 if land_acres < 2.5 else 1
                )
                clean_cat = "marginal" if "marginal" in category else ("small" if "small" in category else "medium")

            with col_d:
                caste = st.selectbox("Social Category / వర్గం", ["BC", "SC", "ST", "General"], index=0)

            is_tenant = st.checkbox(get_label("tenant_label", curr_lang), value=False)
            has_ccrc = False
            if is_tenant:
                has_ccrc = st.checkbox(get_label("ccrc_label", curr_lang), value=True)

            has_well = st.checkbox("Functional Irrigation Borewell / Open Well available?", value=True)

            submit_btn = st.form_submit_button(get_label("check_btn", curr_lang), use_container_width=True)

        st.markdown("---")
        st.write("💡 **Quick Test Triggers / ప్రశ్నలు:**")
        test_col1, test_col2 = st.columns(2)
        with test_col1:
            test_pmkisan = st.button("❓ PM-KISAN Payment Status (Test Fallback)", use_container_width=True)
        with test_col2:
            test_unclear = st.button("❓ Unverified Topic (Test AEO Fallback)", use_container_width=True)

    with col_result:
        st.subheader("📋 Eligibility & Application Guidance")

        query_text = None
        if test_pmkisan:
            query_text = "When will my PM-KISAN 19th installment 2000 rupees payment come?"
        elif test_unclear:
            query_text = "How to apply for bitcoin crypto subsidy loan?"

        if submit_btn or test_pmkisan or test_unclear:
            payload = {
                "farmer_id": "F-DEMO",
                "name": "Demo Farmer",
                "state": clean_state,
                "district": district,
                "land_holding_acres": land_acres,
                "crop": crop,
                "category": clean_cat,
                "is_tenant": is_tenant,
                "has_ccrc": has_ccrc,
                "caste_category": caste,
                "has_irrigation_well": has_well,
                "language": curr_lang
            }

            # Attempt API call; fallback to local evaluation if backend process is starting
            match_data = None
            try:
                resp = requests.post(f"{BACKEND_URL}/match", json=payload, timeout=0.5)
                if resp.status_code == 200:
                    match_data = resp.json()
            except Exception:
                # Direct module fallback
                from backend.eligibility_api import evaluate_farmer, load_schemes, FarmerProfile
                prof = FarmerProfile(**payload)
                schemes = load_schemes()
                eligible = [evaluate_farmer(prof, s).model_dump() for s in schemes if evaluate_farmer(prof, s).eligible]
                match_data = {
                    "eligible_schemes": eligible,
                    "total_eligible": len(eligible)
                }

            if query_text:
                st.info(f"**Farmer Query**: *\"{query_text}\"*")
                llm_res = process_farmer_query(query_text, match_data.get("eligible_schemes", []), language=curr_lang)
                if llm_res["type"] == "redirect_kisan_emitra":
                    st.warning(llm_res["message"])
                elif llm_res["type"] == "uncertainty_fallback":
                    st.error(llm_res["message"])
            else:
                eligible_list = match_data.get("eligible_schemes", [])
                st.success(f"🎯 **Found {len(eligible_list)} Eligible Government Schemes** for your profile in {clean_state}!")

                for s in eligible_list:
                    with st.expander(f"✅ **{s['name']}** ({s['category']})", expanded=True):
                        # Generate plain explanation strictly using verified scheme details
                        expl = generate_plain_explanation(s, language=curr_lang)
                        st.markdown(expl)
                        
                        # Interactive document readiness badge
                        st.markdown("---")
                        st.markdown("**📋 Ready to Apply Checklist:**")
                        for d in s.get("documents_required", []):
                            st.checkbox(f"I have {d}", key=f"chk_{s['scheme_id']}_{d}", value=True)
        else:
            st.info("👈 Fill your farm details on the left and click **'Check My Scheme Eligibility'** to see transparent, rule-matched schemes with deadlines and official source links.")

# -------------------------------------------------------------
# TAB 2: Intermediary Mode (CSC Operators, Extension Officers)
# -------------------------------------------------------------
with tab2:
    st.subheader("🏢 Intermediary Desk: Farmers with Pending Documents & Approaching Deadlines")
    st.markdown("""
    *Designed for Common Service Centre (CSC) operators, Agriculture Extension Officers (AEOs), and FPO managers assisting multiple farmers.*
    """)

    # Metric Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Farmers Tracked", "5", "+2 this week")
    with m2:
        st.metric("Pending Documents", "3", "-1 completed", delta_color="inverse")
    with m3:
        st.metric("Aadhaar-Bank Mismatches", "2", "Requires Attention", delta_color="inverse")
    with m4:
        st.metric("Urgent Deadlines (< 10 Days)", "2", "Critical")

    st.markdown("---")

    # Filters
    f_col1, f_col2, f_col3 = st.columns([1, 1, 2])
    with f_col1:
        dist_filter = st.selectbox("Filter District", ["All", "Warangal", "Nalgonda", "Khammam", "Nizamabad", "Karimnagar"])
    with f_col2:
        status_filter = st.selectbox("Document Status", ["All", "pending", "complete"])

    # Load farmers
    farmers_data = []
    try:
        r = requests.get(f"{BACKEND_URL}/farmer_status", timeout=0.5)
        if r.status_code == 200:
            farmers_data = r.json()
    except Exception:
        from backend.eligibility_api import MOCK_FARMERS_DB
        farmers_data = MOCK_FARMERS_DB

    if dist_filter != "All":
        farmers_data = [f for f in farmers_data if f["district"].lower() == dist_filter.lower()]
    if status_filter != "All":
        farmers_data = [f for f in farmers_data if f["doc_status"].lower() == status_filter.lower()]

    # Render Farmer Cards
    for idx, farmer in enumerate(farmers_data):
        card_class = "danger-card" if farmer.get("days_left", 99) <= 2 else ("warning-card" if farmer["doc_status"] == "pending" else "metric-card")
        
        with st.container():
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="margin:0; color:#1b5e20;">👤 {farmer['farmer_name']} ({farmer['farmer_id']})</h3>
                    <span class="scheme-badge">{farmer['scheme_name']}</span>
                </div>
                <p style="margin: 0.3rem 0;">📍 <b>Village</b>: {farmer['village']}, {farmer['district']} | 🌾 <b>Crop</b>: {farmer['crop']} ({farmer['land_holding_acres']} Acres) | 📞 <b>Phone</b>: {farmer['phone']}</p>
                <p style="margin: 0.2rem 0; color:#c62828;">⚠️ <b>Urgent Action</b>: {farmer['urgent_alert']} (<b>{farmer.get('days_left', 'N/A')} days remaining</b>)</p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns([1.5, 1.5, 1])
            with c1:
                st.write("**Document Readiness:**")
                if farmer["pending_documents"]:
                    for doc in farmer["pending_documents"]:
                        st.markdown(f"❌ *Missing*: {doc}")
                else:
                    st.markdown("✅ *All primary documents uploaded & verified.*")

            with c2:
                st.write("**Aadhaar vs Bank Passbook Name Check:**")
                score = farmer.get("name_match_score", 100)
                score_color = "green" if score >= 90 else ("orange" if score >= 80 else "red")
                st.markdown(f"- Aadhaar: `{farmer['aadhaar_name']}`")
                st.markdown(f"- Bank Passbook: `{farmer['bank_account_name']}`")
                st.markdown(f"- Fuzzy Match Score: <span style='color:{score_color}; font-weight:bold;'>{score}%</span> ({farmer['name_match_status']})", unsafe_allow_html=True)

            with c3:
                st.write("**Action Dispatch:**")
                if st.button(f"📲 Send Alert SMS / WhatsApp", key=f"btn_alert_{farmer['farmer_id']}"):
                    st.success(f"✅ Proactive alert sent to {farmer['phone']} in Telugu!")
                    st.toast(f"Alert delivered to {farmer['farmer_name']}")

        st.markdown("---")

    # Interactive Aadhaar-Bank Name Match Simulator for Intermediary
    st.subheader("🔍 Instant Aadhaar-Bank Name Match Validator")
    st.caption("Tests Person 3's rapidfuzz matching rule to prevent rejected DBT / PM-KISAN / Rythu Bharosa payments before submission.")
    
    col_t1, col_t2, col_t3 = st.columns([1.5, 1.5, 1])
    with col_t1:
        test_aadhaar = st.text_input("Name on Aadhaar Card", value="Komirelli Ramulu")
    with col_t2:
        test_bank = st.text_input("Name in Bank Passbook", value="K. Ramulu")
    with col_t3:
        st.write("")
        st.write("")
        calc_match = st.button("Check Similarity", use_container_width=True)

    if calc_match or test_aadhaar:
        sim_score = int(fuzz.token_set_ratio(test_aadhaar.strip().lower().replace(".", " "), test_bank.strip().lower().replace(".", " ")))
        if sim_score >= 80:
            st.success(f"✅ Match Score: **{sim_score}%** – Acceptable for DBT crediting.")
        else:
            st.error(f"❌ Match Score: **{sim_score}%** – High risk of DBT rejection! Recommend CSC name correction affidavit before submission.")

# -------------------------------------------------------------
# TAB 3: MSP vs Mandi Price Tracker
# -------------------------------------------------------------
with tab3:
    st.subheader("⚖️ Minimum Support Price (MSP) vs Mandi Benchmark (Telangana 2026)")
    st.markdown("""
    *Protects small and marginal farmers from distress selling below support price to local commission agents.*
    """)

    msp_data = [
        {
            "Crop": "Paddy (Grade A)",
            "MSP (₹/Quintal)": 2320,
            "Telangana State Bonus (₹)": 500,
            "Effective Govt Rate (₹)": 2820,
            "Local Mandi Rate (₹)": 2180,
            "Farmer Net Gain (₹/Qtl)": "+ ₹640 / qtl",
            "Recommendation": "Sell at PACS / IKP Centre"
        },
        {
            "Crop": "Cotton (Medium Staple)",
            "MSP (₹/Quintal)": 7121,
            "Telangana State Bonus (₹)": 0,
            "Effective Govt Rate (₹)": 7121,
            "Local Mandi Rate (₹)": 6850,
            "Farmer Net Gain (₹/Qtl)": "+ ₹271 / qtl",
            "Recommendation": "Sell at CCI Centre"
        },
        {
            "Crop": "Maize",
            "MSP (₹/Quintal)": 2225,
            "Telangana State Bonus (₹)": 0,
            "Effective Govt Rate (₹)": 2225,
            "Local Mandi Rate (₹)": 2100,
            "Farmer Net Gain (₹/Qtl)": "+ ₹125 / qtl",
            "Recommendation": "Sell at Markfed Centre"
        }
    ]

    msp_df = pd.DataFrame(msp_data)
    st.table(msp_df)

    st.info("💡 **Telangana Farmer Tip**: For Paddy, the state government bonus of ₹500/quintal is applicable on 33 superfine varieties. Register on OPMS through your local Rythu Vedika.")
    st.caption("Official Sources: Commission for Agricultural Costs and Prices (cacp.dacnet.nic.in) & Telangana Civil Supplies (epds.telangana.gov.in) | Last Verified: 2026-11-02")
