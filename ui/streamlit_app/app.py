import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
from rapidfuzz import fuzz
import sys
import os

# Add root folder to sys.path so utils and data can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.llm import process_farmer_query, generate_plain_explanation, FALLBACK_PMKISAN, FALLBACK_UNCERTAIN
from utils.translation import get_label, UI_LABELS
from utils.weather_api import get_live_weather, evaluate_multi_crop_climate_risk, generate_multilingual_water_advisory, INDIAN_STATES_DISTRICTS
from utils.claim_assistant import calculate_72hr_window, generate_intimation_sms, GEO_PHOTO_CHECKLIST, DOCUMENT_CHECKLIST, PMFBY_HELPLINE
from utils.document_wallet import get_farmer_documents, add_farmer_document, check_scheme_document_readiness, SUPPORTED_DOC_TYPES
from utils.credit_kcc import calculate_kcc_eligibility
from utils.status_tracker import get_all_claims, add_claim_entry, compute_claim_urgency
from utils.escalation_feedback import record_feedback, get_all_feedbacks, generate_formal_escalation_petition

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
        margin-bottom: 1.2rem;
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
    .offline-banner {
        background-color: #eceff1;
        border: 1px dashed #78909c;
        padding: 0.6rem 1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        margin-bottom: 1rem;
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
    .countdown-box {
        font-size: 1.8rem;
        font-weight: 700;
        font-family: monospace;
        padding: 0.6rem 1.2rem;
        background-color: #212121;
        color: #ff5252;
        border-radius: 8px;
        display: inline-block;
        text-align: center;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Language Selector in Sidebar
st.sidebar.image("https://img.icons8.com/color/96/wheat.png", width=64)
st.sidebar.title("రైతు సహాయత / किसान सहायता")

lang_option = st.sidebar.radio(
    "🌐 Language / భాష / भाषा",
    options=["English", "Telugu (తెలుగు)", "Hindi (हिंदी)"],
    index=0
)

LANG_MAP = {"English": "en", "Telugu (తెలుగు)": "te", "Hindi (हिंदी)": "hi"}
curr_lang = LANG_MAP[lang_option]

# Offline / Low-Tech Mode Toggle in Sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("📡 Connectivity & Low-Tech Mode")
is_offline_forced = st.sidebar.checkbox("Simulate Offline Mode (Zero Internet)", value=False)
if is_offline_forced:
    st.sidebar.warning("⚡ Operating in Offline Mode. Using local cached data & SMS fallback.")

st.sidebar.markdown("---")
st.sidebar.markdown("📞 **Emergency Helplines**:")
st.sidebar.markdown("• **PMFBY Insurance**: `1800-180-1551`")
st.sidebar.markdown("• **Kisan Call Centre**: `1800-180-1551`")
st.sidebar.markdown("• **PM-KISAN Helpline**: `155261`")
st.sidebar.markdown("• **Rythu Bharosa / AEO Help**: Nearest Rythu Vedika")

st.markdown(f"""
<div class="main-header">
    <h1 style="margin:0; font-size: 2.1rem; color: #ffffff;">{get_label("app_title", curr_lang)}</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.02rem; opacity: 0.95; color: #f1f8e9;">
        {get_label("tagline", curr_lang)}
    </p>
</div>
""", unsafe_allow_html=True)

if is_offline_forced:
    st.markdown("""
    <div class="offline-banner">
        📶 <b>Low-Tech / Offline Safe Mode Active</b>: Live cloud calls paused. All features are running on deterministic local rule engines and cached agrometeorology. Feature phone users can use the SMS templates below.
    </div>
    """, unsafe_allow_html=True)

# Tabs Navigation (8 comprehensive tabs)
tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    get_label("tab_scheme_explorer", curr_lang),
    get_label("tab_farmer_chat", curr_lang),
    get_label("tab_climate_shield", curr_lang),
    get_label("tab_water_saving", curr_lang),
    get_label("tab_credit_kcc", curr_lang),
    get_label("tab_doc_wallet", curr_lang),
    get_label("tab_msp", curr_lang),
    get_label("tab_intermediary", curr_lang)
])

# -------------------------------------------------------------
# TAB 0: State & Central Scheme Browser (Mobile-First Scheme Explorer)
# -------------------------------------------------------------
with tab0:
    st.markdown("""
    <div style="background:#e8f5e9; border: 1.5px solid #a5d6a7; border-radius: 12px; padding: 1.25rem; margin-bottom: 1.25rem;">
        <h2 style="color: #1b5e20; margin:0 0 0.4rem 0; font-size: 1.5rem;">
            🌾 Find Government Subsidies & Agricultural Schemes
        </h2>
        <p style="color: #4b5563; margin:0; font-size: 0.98rem;">
            Select your State or Union Territory to discover eligible State Government subsidies alongside Pan-India Central Government schemes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    ALL_INDIAN_STATES = [
        "-- Select State / Union Territory --",
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
        "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
        "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
        "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
        "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
        "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
        "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
    ]

    selected_st = st.selectbox(
        "📍 Choose your State or Union Territory / మీ రాష్ట్రాన్ని ఎంచుకోండి / अपना राज्य चुनें:",
        options=ALL_INDIAN_STATES,
        index=0,
        key="global_state_selector"
    )

    if selected_st == "-- Select State / Union Territory --":
        st.info("🚜 **Please select your State above to view available schemes and subsidies.** Agricultural schemes will appear immediately upon choosing your state.")
    else:
        schemes_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "schemes.json")
        with open(schemes_path, "r", encoding="utf-8") as f:
            all_schemes = json.load(f)

        state_schemes = [s for s in all_schemes if s.get("state", "").lower() == selected_st.lower()]
        central_schemes = [s for s in all_schemes if s.get("state", "") == "All"]

        st.success(f"Showing **{len(state_schemes)} {selected_st} State Schemes** + **{len(central_schemes)} Central Government Schemes**")

        col_f1, col_f2, col_f3 = st.columns([1.5, 1, 1])
        with col_f1:
            search_query = st.text_input("🔍 Search schemes by name or crop:", placeholder="e.g. Paddy, Cotton, Tractor, Insurance, Loan...", key="scheme_search_kw")
        with col_f2:
            gov_level = st.radio("Government Level:", ["All Schemes", f"{selected_st} State Schemes", "Central Schemes"], horizontal=True, key="gov_level_radio")
        with col_f3:
            farmer_type = st.selectbox("Farmer Category:", ["All Farmers", "Small & Marginal Farmers (< 5 Acres)", "Tenant Farmers"], key="farmer_cat_filter")

        pool = []
        if gov_level == "All Schemes":
            pool = state_schemes + central_schemes
        elif gov_level == f"{selected_st} State Schemes":
            pool = state_schemes
        else:
            pool = central_schemes

        if search_query.strip():
            sq = search_query.lower().strip()
            pool = [s for s in pool if sq in s["scheme_name"].lower() or sq in s.get("description", "").lower() or sq in str(s.get("rules", {}).get("supported_crops", [])).lower()]

        if farmer_type == "Tenant Farmers":
            pool = [s for s in pool if s.get("rules", {}).get("tenant_allowed", True)]
        elif farmer_type == "Small & Marginal Farmers (< 5 Acres)":
            pool = [s for s in pool if s.get("rules", {}).get("max_land_acres") is None or s.get("rules", {}).get("max_land_acres") >= 5.0]

        if not pool:
            st.warning("No schemes match your active search or filter. Try clearing filters.")
        else:
            for i in range(0, len(pool), 2):
                col_c1, col_c2 = st.columns(2, gap="medium")
                cols = [col_c1, col_c2]
                for j in range(2):
                    if i + j < len(pool):
                        sc = pool[i + j]
                        with cols[j]:
                            is_central = sc.get("level") == "Central"
                            badge_html = f"""
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.5rem;">
                                <span style="background: {'#e8eaf6' if is_central else '#e8f5e9'}; color: {'#1a237e' if is_central else '#1b5e20'}; border: 1.5px solid {'#9fa8da' if is_central else '#a5d6a7'}; padding: 0.25rem 0.65rem; border-radius: 9999px; font-weight: 800; font-size: 0.8rem;">
                                    {'🇮🇳 Central Govt Scheme' if is_central else f'🏛️ {selected_st} State Scheme'}
                                </span>
                                <span style="font-size: 0.8rem; color: #6b7280; font-weight: 600;">Verified: {sc.get('last_verified', '2026')}</span>
                            </div>
                            """
                            st.markdown(badge_html, unsafe_allow_html=True)
                            st.markdown(f"### {sc['scheme_name']}")
                            st.markdown(f"*{sc.get('description', '')}*")

                            st.markdown(f"""
                            <div style="background: #fffde7; border-left: 4px solid #f57f17; padding: 0.6rem 0.8rem; border-radius: 6px; margin: 0.6rem 0;">
                                <span style="font-size: 0.8rem; font-weight: 800; color: #b75300; text-transform: uppercase;">💰 Key Benefit</span><br>
                                <strong style="font-size: 1.05rem; color: #2e7d32;">{sc.get('benefit_summary', 'Financial & Scheme Benefit')}</strong>
                            </div>
                            """, unsafe_allow_html=True)

                            rules_desc = []
                            rules = sc.get("rules", {})
                            if rules.get("tenant_allowed"):
                                rules_desc.append("✅ Tenant farmers allowed")
                            elif rules.get("requires_land_ownership"):
                                rules_desc.append("⚠️ Registered landownership required")
                            if rules.get("max_land_acres"):
                                rules_desc.append(f"Land ceiling: up to {rules.get('max_land_acres')} acres")
                            
                            st.markdown(f"**🎯 Eligibility:** {'; '.join(rules_desc) if rules_desc else 'All active farmers'}")

                            with st.expander("📑 Required Documents"):
                                for d in sc.get("documents_required", []):
                                    st.markdown(f"- {d}")

                            if sc.get("deadlines"):
                                st.markdown(f"⏰ **Deadline:** {sc['deadlines']}")
                            if sc.get("claim_window"):
                                st.markdown(f"""
                                <div style="background: #fff3e0; border: 1px solid #ffcc80; padding: 0.4rem 0.6rem; border-radius: 6px; font-size: 0.85rem; color: #c43e00; margin: 0.4rem 0;">
                                    ⚠️ <strong>Emergency Claim Rule:</strong> {sc['claim_window']}
                                </div>
                                """, unsafe_allow_html=True)

                            st.link_button("🌐 Official Portal / Apply Link ↗", sc.get("source_url", "#"))
                            st.markdown("---")

# -------------------------------------------------------------
# TAB 1: Farmer Self-Service Chat & Eligibility Check
# -------------------------------------------------------------
with tab1:
    col_input, col_result = st.columns([1, 1.4], gap="large")

    with col_input:
        st.subheader(get_label("profile_header", curr_lang))

        consent = st.checkbox(
            "🔒 I consent to storing my farm details to receive proactive deadline & payment alerts." if curr_lang == "en" else
            "🔒 గడువు మరియు చెల్లింపు సమాచారం కోసం నా వ్యవసాయ వివరాలను ఉపయోగించడానికి అంగీకరిస్తున్నాను." if curr_lang == "te" else
            "🔒 समय-सीमा एवं भुगतान संबंधी अलर्ट प्राप्त करने हेतु मैं अपनी कृषि जानकारी साझा करने की सहमति देता हूँ।",
            value=True
        )

        with st.form("farmer_profile_form"):
            state = st.selectbox(
                get_label("state_label", curr_lang),
                ["Telangana (Pilot State)", "Andhra Pradesh", "Karnataka", "Maharashtra", "Punjab", "Uttar Pradesh"],
                index=0
            )
            clean_state = "Telangana" if "Telangana" in state else state

            district = st.selectbox(
                get_label("district_label", curr_lang),
                INDIAN_STATES_DISTRICTS.get(clean_state, ["Warangal", "Nalgonda", "Khammam", "Karimnagar"])
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
                caste = st.selectbox("Social Category / వర్గం / जाति", ["BC", "SC", "ST", "General"], index=0)

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

            match_data = None
            if not is_offline_forced:
                try:
                    resp = requests.post(f"{BACKEND_URL}/match", json=payload, timeout=0.5)
                    if resp.status_code == 200:
                        match_data = resp.json()
                except Exception:
                    pass

            if match_data is None:
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
                        expl = generate_plain_explanation(s, language=curr_lang)
                        st.markdown(expl)

                        readiness = check_scheme_document_readiness(s.get("documents_required", []), farmer_id="DEMO_FARMER_1")
                        st.markdown("---")
                        st.markdown(f"**📁 Digital Document Wallet Readiness**: `{readiness['readiness_percent']}% Ready`")
                        if readiness["is_ready"]:
                            st.success("🎉 All required documents are verified and available in your Document Wallet!")
                        else:
                            st.warning(f"⚠️ Missing {len(readiness['missing_docs'])} documents: {', '.join(readiness['missing_docs'])}. Upload in Tab 5.")

                        st.caption("Is this information accurate? Flag outdated rules below.")
                        f_col_a, f_col_b = st.columns([2, 1])
                        with f_col_a:
                            fb_text = st.text_input("Report scheme discrepancy / feedback", key=f"fb_in_{s['scheme_id']}", placeholder="e.g. Portal server error, updated deadline...")
                        with f_col_b:
                            st.write("")
                            if st.button("Submit Feedback", key=f"fb_btn_{s['scheme_id']}"):
                                record_feedback(s["scheme_id"], s["name"], "USER_REPORT", "Farmer", fb_text or "General verification check", clean_state)
                                st.success("✅ Feedback logged! Thank you for keeping scheme data current.")
        else:
            st.info("👈 Fill your farm details on the left and click **'Check My Scheme Eligibility'** to see transparent, rule-matched schemes with deadlines and official source links.")

# -------------------------------------------------------------
# TAB 2: Multi-Crop Climate Risk & 72-Hr Claim Shield
# -------------------------------------------------------------
with tab2:
    st.subheader("🛡️ Pan-India Climate Risk Shield & 72-Hour Loss Claim Assistant")
    st.markdown("""
    *Detects drought, excess rain, heat waves, and pest outbreaks in real-time. Immediately unlocks statutory PMFBY insurance intimation with an active 72-hour countdown to prevent claim rejection.*
    """)

    c_col0, c_col1, c_col2, c_col3 = st.columns(4)
    with c_col0:
        w_state = st.selectbox("State (Pan-India)", list(INDIAN_STATES_DISTRICTS.keys()), index=0, key="tab2_state")
    with c_col1:
        dist_options = INDIAN_STATES_DISTRICTS.get(w_state, ["Warangal"])
        w_dist = st.selectbox(f"District in {w_state}", dist_options, key="tab2_dist")
    with c_col2:
        w_crop = st.selectbox("Crop", ["Paddy (Rice)", "Cotton", "Chilli (Red Pepper)", "Maize (Corn)", "Pulses (Bengal Gram)", "Groundnut & Oilseeds"], key="tab2_crop")
    with c_col3:
        w_source = st.selectbox("Irrigation Source", ["Borewell (Deep > 200 ft)", "Canal Tail-end", "Tank / Open Well", "Rainfed / Rain-dependent", "Borewell (Normal)"], key="tab2_water")

    custom_loc = st.text_input("🔍 Or enter any custom district / tehsil in India", "", key="tab2_custom_loc")
    active_dist = custom_loc.strip() if custom_loc.strip() else w_dist

    weather_data = get_live_weather(active_dist, state=w_state)
    stress_eval = evaluate_multi_crop_climate_risk(weather_data, crop=w_crop, water_source=w_source)

    st.markdown(f"#### 🛰️ Live Agrometeorology: {weather_data['location']}")
    wc1, wc2, wc3, wc4 = st.columns(4)
    with wc1:
        st.metric("Temperature", f"{weather_data['current_temperature']} °C", f"Avg Max: {weather_data['avg_max_temp']} °C")
    with wc2:
        st.metric("Relative Humidity", f"{weather_data['current_humidity']} %", "High Pest Risk" if weather_data['current_humidity'] >= 68 else "Optimal")
    with wc3:
        st.metric("7-Day Forecast Rain", f"{weather_data['forecast_7day_total_rain_mm']} mm", "Inundation risk" if weather_data['forecast_7day_total_rain_mm'] >= 35 else ("Rain deficit" if weather_data['forecast_7day_total_rain_mm'] < 5.0 else "Adequate"))
    with wc4:
        st.metric("Consecutive Dry Days", f"{weather_data['consecutive_dry_days']} Days", "Dry spell alert" if weather_data['consecutive_dry_days'] >= 5 else "Normal")

    st.markdown("**🚨 Active Climate Perils Detected:**")
    hazards_list = stress_eval.get("all_hazards", [])
    if hazards_list:
        h_cols = st.columns(len(hazards_list))
        for idx, hz in enumerate(hazards_list):
            with h_cols[idx]:
                st.warning(f"⚠️ **{hz['title']}**\n\n*{hz['description']}*")

    st.markdown("---")

    # 72-HOUR CLAIM ASSISTANT MODULE
    st.subheader("⏱️ 72-Hour Crop Loss Claim Assistant (PMFBY & Calamity Shield)")
    st.markdown("""
    > [!IMPORTANT]
    > **Statutory Rule**: Under PMFBY guidelines and State Disaster norms, individual farm losses (hailstorm, cloudburst, flash inundation, pest disaster) **must be intimated within 72 hours** of the weather event. Intimations after 72 hours are rejected by insurance companies!
    """)

    if "calamity_reported_at" not in st.session_state:
        st.session_state.calamity_reported_at = datetime.now() - timedelta(hours=14)

    countdown = calculate_72hr_window(st.session_state.calamity_reported_at)

    timer_col1, timer_col2, timer_col3 = st.columns([1.2, 1.2, 1.6])
    with timer_col1:
        st.markdown("**Window Countdown Remaining:**")
        box_style = f"background-color: {'#b71c1c' if countdown['color'] == 'red' else ('#e65100' if countdown['color'] == 'orange' else '#1b5e20')}; color: white;"
        st.markdown(f'<div class="countdown-box" style="{box_style}">⏳ {countdown["display_str"]}</div>', unsafe_allow_html=True)
    with timer_col2:
        st.markdown(f"**Event Registered**: `{countdown['incident_str']}`")
        st.markdown(f"**Strict Deadline**: `{countdown['deadline_str']}`")
        st.markdown(f"**Urgency**: `{countdown['urgency']}`")
    with timer_col3:
        if st.button("🔄 Reset / Report New Weather Event Now", use_container_width=True):
            st.session_state.calamity_reported_at = datetime.now()
            st.rerun()

    chk_col1, chk_col2 = st.columns(2)
    with chk_col1:
        st.markdown("#### 📸 Geo-Tagged Photo Evidence Checklist")
        st.caption("Evidence required by Joint Survey Team (Insurance surveyor + AEO)")
        for item in GEO_PHOTO_CHECKLIST:
            st.checkbox(f"✅ **{item['item']}** ({'Mandatory' if item['mandatory'] else 'Recommended'})\n*{item['requirement']}*", value=True, key=f"photo_{item['item']}")

    with chk_col2:
        st.markdown("#### 📑 Mandatory Documents for Claim Settlement")
        st.caption("Keep these ready for physical or digital upload")
        for doc in DOCUMENT_CHECKLIST:
            st.checkbox(f"📄 **{doc['doc']}**\n*(Source: {doc['source']})*", value=True, key=f"doc_{doc['doc']}")

    st.markdown("#### 📲 One-Click Loss Intimation Dispatch")
    c_sub1, c_sub2, c_sub3, c_sub4 = st.columns(4)
    with c_sub1:
        f_name = st.text_input("Farmer Name", "Komirelli Ramulu", key="sms_f_name")
    with c_sub2:
        f_phone = st.text_input("Phone Number", "9848022338", key="sms_f_phone")
    with c_sub3:
        f_survey = st.text_input("Survey / Parcel No.", "142/A", key="sms_f_survey")
    with c_sub4:
        f_loss = st.slider("Estimated Loss %", 10, 100, 65, key="sms_f_loss")

    sms_draft = generate_intimation_sms(
        farmer_name=f_name,
        phone=f_phone,
        crop=w_crop,
        district=active_dist,
        village="Geesugonda",
        survey_no=f_survey,
        loss_percent=f_loss,
        hazard_type=stress_eval["primary_hazard"]["title"],
        acreage=2.2,
        language=curr_lang
    )

    st.text_area("Generated Formal Intimation Notice (Copy & Send to 1800-180-1551 / AEO WhatsApp)", sms_draft["text"], height=130)

    btn_s1, btn_s2 = st.columns(2)
    with btn_s1:
        if st.button("📤 Send SMS to PMFBY Toll-Free (1800-180-1551) & Log Claim", use_container_width=True):
            add_claim_entry(
                farmer_name=f_name,
                phone=f_phone,
                scheme_name=f"PMFBY Loss Claim - {w_crop}",
                reference_number=f"PMFBY-{active_dist[:3].upper()}-{datetime.now().strftime('%m%d%H%M')}",
                status="Intimation Dispatched (Within 72 hrs)",
                notes=f"Hazard: {stress_eval['primary_hazard']['title']}, Estimated loss: {f_loss}%"
            )
            st.success("✅ Intimation logged into Claims Tracker and transmitted to PMFBY & District AEO!")
    with btn_s2:
        st.link_button("🌐 Open Official PMFBY Portal (pmfby.gov.in)", "https://pmfby.gov.in", use_container_width=True)

    st.markdown("---")
    st.subheader("🏛️ Government Disaster Relief (SDRF / NDRF) & Input Subsidies")
    st.markdown("""
    *Non-insurance sovereign calamity relief provided by Revenue & Disaster Management Departments for loss >= 33%:*\n
    • **Rainfed Crops**: ₹8,500/hectare (~ ₹3,440/acre)\n
    • **Irrigated Crops (Paddy/Cotton/Chilli)**: ₹17,000/hectare (~ ₹6,880/acre)\n
    • **Perennial Horticulture Crops**: ₹22,500/hectare (~ ₹9,100/acre)\n
    • **Telangana Calamity Relief**: ₹10,000/acre ex-gratia assistance announced during declared hailstorms.
    """)

# -------------------------------------------------------------
# TAB 3: Water-Saving Subsidies & Next-Crop Planning
# -------------------------------------------------------------
with tab3:
    st.subheader("💧 Diversified Pan-India Water-Saving Subsidies & Next-Season Crop Planning")
    st.markdown("""
    *Turns water stress into action: Matches farmers to 18+ verified Central and State drip/sprinkler, solar pump and farm pond schemes (PMKSY, PM-KUSUM, TSMIP, APMIP, Krishi Bhagya, Magel Tyala Shet Tale) and 26+ lower-water crop alternatives with MSP support.*
    """)

    st.markdown("### 1. 🚿 Drip, Sprinkler, Solar Pump and Farm Pond Subsidy Matcher")
    
    water_schemes_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "water_saving_schemes.json")
    try:
        with open(water_schemes_path, "r", encoding="utf-8") as f:
            water_schemes = json.load(f)
    except Exception:
        water_schemes = []

    sub_col1, sub_col2 = st.columns([1.1, 1.9], gap="large")
    with sub_col1:
        st.markdown("**Your Farm Configuration:**")
        w_sub_st = st.selectbox("Your State", [
            "All States / Central", "Telangana", "Andhra Pradesh", "Maharashtra", "Karnataka",
            "Gujarat", "Haryana", "Punjab", "Tamil Nadu", "Rajasthan", "Madhya Pradesh", "Uttar Pradesh"
        ], key="w_sub_st_sel")
        w_sub_caste = st.selectbox("Social Category", ["BC", "SC", "ST", "General"], key="w_sub_caste")
        w_sub_land = st.number_input("Land Holding (Acres)", 0.5, 25.0, 2.5, 0.5, key="w_sub_land")
        w_sub_type = st.radio("Equipment Category", ["Micro Irrigation (Drip / Sprinkler)", "Solar Pump (PM-KUSUM A/B/C)", "Farm Pond / Water Harvesting (Shet Tale / Talab)"])

        if "Micro" in w_sub_type:
            if w_sub_caste in ["SC", "ST"] and w_sub_land <= 5.0:
                subsidy_pct = 100
                farmer_share_pct = 0
            elif w_sub_caste == "BC" and w_sub_land <= 5.0:
                subsidy_pct = 90
                farmer_share_pct = 10
            elif w_sub_land <= 5.0:
                subsidy_pct = 80
                farmer_share_pct = 20
            else:
                subsidy_pct = 50
                farmer_share_pct = 50
            unit_cost = int(w_sub_land * 35000)
            subsidy_amount = int(unit_cost * (subsidy_pct / 100))
            farmer_amount = unit_cost - subsidy_amount
        elif "Solar" in w_sub_type:
            subsidy_pct = 60
            farmer_share_pct = 40
            unit_cost = 240000
            subsidy_amount = int(unit_cost * 0.60)
            farmer_amount = unit_cost - subsidy_amount
        else:
            subsidy_pct = 75 if w_sub_caste in ["SC", "ST"] else 50
            farmer_share_pct = 100 - subsidy_pct
            unit_cost = 100000
            subsidy_amount = int(unit_cost * (subsidy_pct / 100))
            farmer_amount = unit_cost - subsidy_amount

        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0; color:#1b5e20;">💰 Estimated Government Subsidy: {subsidy_pct}%</h4>
            <p style="margin:0.3rem 0;">• Estimated System Benchmark: <b>₹{unit_cost:,}</b></p>
            <p style="margin:0.3rem 0; color:#2e7d32;">• <b>Govt Subsidy: ₹{subsidy_amount:,}</b></p>
            <p style="margin:0.3rem 0; color:#c62828;">• Farmer Contribution: <b>₹{farmer_amount:,} ({farmer_share_pct}%)</b></p>
        </div>
        """, unsafe_allow_html=True)

    with sub_col2:
        filtered_water_schemes = water_schemes
        if w_sub_st != "All States / Central":
            filtered_water_schemes = [
                s for s in water_schemes 
                if "All States" in s.get("applicable_states", []) or w_sub_st in s.get("applicable_states", [])
            ]

        st.markdown(f"**Verified Government Subsidy Schemes ({len(filtered_water_schemes)} Available):**")
        for ws in filtered_water_schemes:
            with st.expander(f"💧 **{ws['name']}** ({ws.get('level', 'Govt Scheme')})", expanded=False):
                st.markdown(f"**Category**: `{ws['category']}` | **Status**: `{ws['current_status']}`")
                st.markdown(f"**Water Savings Impact**: {ws['water_savings_potential']}")
                st.markdown(f"**Subsidy Rules**: {json.dumps(ws['subsidy_rules'], indent=1, ensure_ascii=False) if isinstance(ws['subsidy_rules'], dict) else ws['subsidy_rules']}")
                st.markdown(f"**Eligible Systems**: {', '.join(ws.get('eligible_systems', []))}")
                st.markdown(f"**Portal**: [{ws['portal_url']}]({ws['portal_url']}) | *Last Verified: {ws['last_verified']}*")

    st.markdown("---")

    # Part B: Next-Season Crop and Water Planning (Diversified Across 26 Crops)
    st.markdown("### 2. 🌱 Next-Season Crop & Water Planning (Diversified Low-Water Alternatives)")
    st.markdown("""
    *When groundwater levels deplete or monsoon dry spells strike, shift from water-guzzling Paddy (which consumes 1,200–1,400 mm) to ID (Irrigated Dry) crops, pulses, oilseeds, and nutri-cereals. These crops consume 65% to 88% less water, restore soil nitrogen, and carry guaranteed Minimum Support Price (MSP) protection.*
    """)

    crops_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "low_water_crops.json")
    try:
        with open(crops_path, "r", encoding="utf-8") as f:
            low_water_crops = json.load(f)
    except Exception:
        low_water_crops = []

    flt_col1, flt_col2 = st.columns([1.5, 2.5])
    with flt_col1:
        crop_cat_filter = st.selectbox("Filter Crop Category", [
            "All Categories (26 Crops)",
            "Pulses (Bengal Gram, Moong, Urad, Tur, Horse Gram, Cowpea, Lentil)",
            "Oilseeds (Sesame, Groundnut, Mustard, Safflower, Sunflower, Castor, Linseed)",
            "Nutri-Cereals / Millets (Jowar, Bajra, Ragi, Foxtail, Little, Barnyard, Kodo, Proso)",
            "Commercial & Fodder Diversification (Guar, Barley)"
        ], key="crop_cat_filter_sel")
    with flt_col2:
        crop_search_kw = st.text_input("🔍 Search alternative crops by name, variety, or MSP:", placeholder="e.g. Sesame, Moong, Ragi, 9267, JG 11...", key="crop_kw_search")

    active_crops = low_water_crops
    if "Pulses" in crop_cat_filter:
        active_crops = [c for c in active_crops if "Pulse" in c.get("category", "")]
    elif "Oilseeds" in crop_cat_filter:
        active_crops = [c for c in active_crops if "Oilseed" in c.get("category", "")]
    elif "Millets" in crop_cat_filter:
        active_crops = [c for c in active_crops if "Millet" in c.get("category", "") or "Cereal" in c.get("category", "")]
    elif "Commercial" in crop_cat_filter:
        active_crops = [c for c in active_crops if "Commercial" in c.get("category", "") or "Salinity" in c.get("category", "")]

    if crop_search_kw.strip():
        kw = crop_search_kw.lower().strip()
        active_crops = [
            c for c in active_crops 
            if kw in c["name"].lower() or kw in c.get("category", "").lower() or kw in str(c.get("msp_rate_per_quintal", "")) or kw in str(c.get("recommended_varieties", [])).lower()
        ]

    st.caption(f"Showing {len(active_crops)} alternative crops:")

    crop_cards = st.columns(3)
    for idx, c in enumerate(active_crops):
        col_target = crop_cards[idx % 3]
        with col_target:
            with st.container():
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin:0; color:#1b5e20;">🌾 {c['name']}</h4>
                    <p style="margin:0.2rem 0; font-size:0.85rem;"><b>Category</b>: {c['category']}</p>
                    <p style="margin:0.2rem 0; color:#1565c0;">💧 <b>Water Need</b>: {c.get('water_requirement_mm', 'Low')} (<b>{c['water_savings_percentage']}</b>)</p>
                    <p style="margin:0.2rem 0;">⚖️ <b>MSP / Rate</b>: <span style="font-size:1.1rem; font-weight:700; color:#2e7d32;">₹{c['msp_rate_per_quintal']:,} / qtl</span></p>
                    <p style="margin:0.2rem 0; font-size:0.85rem;">⏳ Duration: {c['duration_days']} | Yield: {c['expected_yield_qtl_per_acre']}</p>
                    <p style="margin:0.2rem 0; font-size:0.85rem;">🌱 <b>Varieties</b>: {', '.join(c.get('recommended_varieties', [])[:2])}</p>
                    <p style="margin:0.2rem 0; font-size:0.85rem; color:#424242;"><i>{c['soil_health_benefit']}</i></p>
                </div>
                """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 4: KCC Credit Help & Application Status Tracker
# -------------------------------------------------------------
with tab4:
    st.subheader("💳 Kisan Credit Card (KCC) Guidance & Application Status Tracker")

    col_kcc, col_trk = st.columns([1.1, 1.3], gap="large")

    with col_kcc:
        st.markdown("### 🏦 1. KCC Credit & Subvention Calculator")
        k_crop = st.selectbox("Cultivated Crop", ["Paddy", "Cotton", "Chilli", "Maize", "Bengal Gram", "Groundnut"], key="kcc_crop_sel")
        k_acres = st.number_input("Cultivated Land (Acres)", 0.5, 20.0, 2.5, 0.5, key="kcc_acres_in")
        k_debt = st.number_input("Existing KCC Loan Outstanding (₹)", 0, 500000, 0, 10000, key="kcc_debt_in")

        kcc_res = calculate_kcc_eligibility(crop=k_crop, land_acres=k_acres, existing_kcc_debt=float(k_debt))

        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0; color:#1b5e20;">💳 First-Year Sanction Limit: ₹{kcc_res['first_year_limit']:,}</h4>
            <p style="margin:0.2rem 0;">• 5-Year Card Ceiling: <b>₹{kcc_res['five_year_card_limit']:,}</b></p>
            <p style="margin:0.2rem 0;">• Net Available Limit: <b>₹{kcc_res['available_limit']:,}</b></p>
            <p style="margin:0.2rem 0;">{kcc_res['collateral_note']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### ⚡ Modified Interest Subvention Breakdown:")
        ins_sub = kcc_res["interest_subvention"]
        st.markdown(f"• Standard Commercial Rate: `{ins_sub['commercial_bank_rate']}`")
        st.markdown(f"• Central Govt Subvention: `{ins_sub['govt_interest_subvention']}`")
        st.markdown(f"• Prompt Repayment Discount: `{ins_sub['prompt_repayment_incentive']}`")
        st.markdown(f"• **Net Effective Rate: :green[{ins_sub['effective_net_rate']}]**")
        st.markdown(f"• Annual Interest Payable: **₹{ins_sub['annual_interest_payable_timely']:,}** (You save ₹{ins_sub['annual_interest_saved_vs_moneylender']:,} vs non-institutional credit)")

        st.warning(f"⏰ **Repayment Deadline**: {kcc_res['repayment_reminder']['statutory_due_date']}\n\n*{kcc_res['repayment_reminder']['critical_warning']}*")

    with col_trk:
        st.markdown("### 📋 2. Claim & Application Status Tracker")
        st.caption("Track manual applications for PMFBY, KCC, TSMIP, and Rythu Bharosa with automatic SLA reminders.")

        with st.expander("➕ Log New Application / Claim Status", expanded=False):
            t_farmer = st.text_input("Farmer Name", "Komirelli Ramulu", key="trk_fname")
            t_phone = st.text_input("Phone", "9848022338", key="trk_phone")
            t_scheme = st.selectbox("Scheme Applied", ["PMFBY Crop Loss Claim", "TSMIP Drip Subsidy", "KCC Loan Application", "PM-KUSUM Solar Pump", "Rythu Bharosa Land Verification"], key="trk_sch")
            t_ref = st.text_input("Application / ACK Reference Number", "TS/2026/APP/0048", key="trk_ref")
            t_stat = st.selectbox("Current Status", ["Submitted at CSC / Rythu Vedika", "Joint Field Survey Pending", "Approved by Mandal Officer", "Sanction Letter Issued", "Bank Disbursal Pending"], key="trk_st")
            t_notes = st.text_input("Notes / Remarks", "Application submitted with passbook copy", key="trk_notes")

            if st.button("Save Application to Tracker", use_container_width=True):
                add_claim_entry(t_farmer, t_phone, t_scheme, t_ref, t_stat, t_notes)
                st.success("✅ Application saved! Automatic follow-up alerts scheduled.")
                st.rerun()

        claims_list = get_all_claims()
        for cl in reversed(claims_list[-4:]):
            urg = compute_claim_urgency(cl)
            card_color = "danger-card" if urg["urgency"] == "HIGH" else ("warning-card" if urg["urgency"] == "MEDIUM" else "metric-card")
            st.markdown(f"""
            <div class="{card_color}">
                <div style="display:flex; justify-content:space-between;">
                    <h4 style="margin:0; color:#1b5e20;">📑 {cl['scheme_name']}</h4>
                    <span class="scheme-badge">{cl['status']}</span>
                </div>
                <p style="margin:0.2rem 0;">👤 <b>{cl['farmer_name']}</b> | Ref: <code>{cl['reference_number']}</code> | Filed: {cl['filing_date']}</p>
                <p style="margin:0.2rem 0; color:#c62828;"><b>{urg['status_banner']}</b></p>
                <p style="margin:0.2rem 0; font-size:0.85rem; color:#555;"><i>Notes: {cl.get('notes', 'N/A')}</i></p>
            </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 5: Farmer Document Wallet & DigiLocker
# -------------------------------------------------------------
with tab5:
    st.subheader("📁 Consent-Driven Farmer Document Wallet & DigiLocker Integration")
    st.markdown("""
    *Safely store scanned land records (Pahani/Dharani), Aadhaar, Bank Passbooks, and CCRC agreements with explicit farmer consent. Integrated with DigiLocker and AgriStack Farmer ID metadata.*
    """)

    f_doc_data = get_farmer_documents("DEMO_FARMER_1")

    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin:0; color:#1b5e20;">👤 {f_doc_data.get('farmer_name', 'Komirelli Ramulu')}</h3>
        <p style="margin:0.2rem 0;">🆔 <b>AgriStack Farmer ID</b>: <code>{f_doc_data.get('agristack_farmer_id', 'AGRI-IN-TS-WAR-88392')}</code> | 🔗 <b>DigiLocker Status</b>: {'🟢 Linked' if f_doc_data.get('digilocker_linked') else '⚪ Not Linked'}</p>
        <p style="margin:0.2rem 0; font-size:0.85rem; color:#2e7d32;">🔒 Consent verified on {f_doc_data.get('consent_timestamp', '2026-11-01')}</p>
    </div>
    """, unsafe_allow_html=True)

    col_docs_list, col_docs_add = st.columns([1.5, 1], gap="large")

    with col_docs_list:
        st.markdown("#### 📑 Verified Stored Documents in Vault")
        docs = f_doc_data.get("documents", [])
        if docs:
            for d in docs:
                with st.container():
                    st.markdown(f"""
                    **{d['title']}** (`{d['doc_type']}`)
                    • ID: `{d['identifier_masked']}` | Source: *{d['source']}*
                    • URI: `{d['uri']}` | Status: {'✅ Verified' if d['verified'] else '⏳ Pending Verification'}
                    """)
                    st.markdown("---")
        else:
            st.info("No documents uploaded yet.")

    with col_docs_add:
        st.markdown("#### ➕ Add New Document with Consent")
        doc_type_sel = st.selectbox("Document Type", [dt["name"] for dt in SUPPORTED_DOC_TYPES], key="doc_type_in")
        raw_type = [dt["id"] for dt in SUPPORTED_DOC_TYPES if dt["name"] == doc_type_sel][0]
        doc_title = st.text_input("Document Label", f"{doc_type_sel} - Copy", key="doc_label_in")
        doc_id = st.text_input("Document Number / Passbook No.", "T192008892", key="doc_num_in")
        doc_src = st.selectbox("Verification Source", ["DigiLocker Sync", "MeeSeva Certified Scan", "Manual Upload", "Rythu Vedika Attested"])
        doc_consent = st.checkbox("I consent to store this document for scheme applications", value=True, key="doc_consent_in")

        if st.button("Save to Document Wallet", use_container_width=True):
            if doc_consent:
                add_farmer_document(
                    farmer_id="DEMO_FARMER_1",
                    farmer_name="Komirelli Ramulu",
                    doc_type=raw_type,
                    title=doc_title,
                    identifier=doc_id,
                    source=doc_src,
                    consent=doc_consent
                )
                st.success("✅ Document safely encrypted and saved to local wallet!")
                st.rerun()
            else:
                st.error("Consent is required to save records.")

# -------------------------------------------------------------
# TAB 6: MSP vs Mandi Price Tracker
# -------------------------------------------------------------
with tab6:
    st.subheader("⚖️ Minimum Support Price (MSP) vs Mandi Benchmark (2025-2026)")
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
        },
        {
            "Crop": "Bengal Gram (Chana)",
            "MSP (₹/Quintal)": 5440,
            "Telangana State Bonus (₹)": 0,
            "Effective Govt Rate (₹)": 5440,
            "Local Mandi Rate (₹)": 5100,
            "Farmer Net Gain (₹/Qtl)": "+ ₹340 / qtl",
            "Recommendation": "Sell at NAFED / Markfed Centre"
        },
        {
            "Crop": "Sesame (Til)",
            "MSP (₹/Quintal)": 9267,
            "Telangana State Bonus (₹)": 0,
            "Effective Govt Rate (₹)": 9267,
            "Local Mandi Rate (₹)": 8700,
            "Farmer Net Gain (₹/Qtl)": "+ ₹567 / qtl",
            "Recommendation": "Sell at Mandi with MSP floor"
        }
    ]

    msp_df = pd.DataFrame(msp_data)
    st.table(msp_df)

    st.info("💡 **Telangana Farmer Tip**: For Paddy, the state government bonus of ₹500/quintal is applicable on 33 superfine varieties. Register on OPMS through your local Rythu Vedika.")
    st.caption("Official Sources: Commission for Agricultural Costs and Prices (cacp.dacnet.nic.in) & Telangana Civil Supplies (epds.telangana.gov.in) | Last Verified: 2026-11-05")

# -------------------------------------------------------------
# TAB 7: Intermediary Desk, Feedback Loop & Higher Official Escalation
# -------------------------------------------------------------
with tab7:
    st.subheader("🏢 Intermediary Desk, Feedback Curation & Higher Official Escalation")
    st.markdown("""
    *Equips CSC Operators, Extension Officers (AEOs), and FPOs to resolve farmer issues, curate scheme updates, and escalate unaddressed grievances to Mandal, District, or State Authorities.*
    """)

    sub_t1, sub_t2, sub_t3 = st.tabs(["👥 Intermediary Operations", "📣 Feedback Loop & Flags", "🏛️ Report to Higher Official (Escalation)"])

    with sub_t1:
        st.markdown("#### Intermediary Queue & Aadhaar Name Validator")
        c_v1, c_v2, c_v3 = st.columns([1.5, 1.5, 1])
        with c_v1:
            t_aadhaar = st.text_input("Name on Aadhaar Card", value="Komirelli Ramulu", key="tab7_aadh")
        with c_v2:
            t_bank = st.text_input("Name in Bank Passbook", value="K. Ramulu", key="tab7_bank")
        with c_v3:
            st.write("")
            st.write("")
            chk_m = st.button("Check Similarity", use_container_width=True, key="tab7_btn_sim")

        sim_score = int(fuzz.token_set_ratio(t_aadhaar.strip().lower().replace(".", " "), t_bank.strip().lower().replace(".", " ")))
        if sim_score >= 80:
            st.success(f"✅ Match Score: **{sim_score}%** – Acceptable for DBT payment crediting.")
        else:
            st.error(f"❌ Match Score: **{sim_score}%** – High risk of rejection! Recommend CSC name correction affidavit before submission.")

    with sub_t2:
        st.markdown("#### 📣 Scheme Data Feedback Loop")
        st.markdown("Review and submit community flags regarding outdated deadlines, server outages, or incorrect eligibility criteria.")

        with st.form("feedback_form"):
            fb_sch_name = st.selectbox("Scheme Name", ["PMKSY-PDMC Drip", "PMFBY Insurance", "Rythu Bharosa", "PM-KISAN", "TSMIP Telangana", "KCC Loan"])
            fb_type = st.selectbox("Issue Type", ["OUTDATED_DEADLINE", "PORTAL_DOWN", "INCORRECT_CRITERIA", "DOCUMENT_MISMATCH", "OTHER"])
            fb_role = st.selectbox("Your Role", ["Farmer", "CSC Operator", "Agriculture Extension Officer (AEO)", "FPO Representative"])
            fb_desc = st.text_area("Detailed Issue Description", "e.g. The portal link has been migrated to pmksy.nic.in/new; application fee increased to ₹50.")
            fb_sub = st.form_submit_button("Submit Scheme Feedback", use_container_width=True)

            if fb_sub:
                res = record_feedback("SCHEME_GEN", fb_sch_name, fb_type, fb_role, fb_desc)
                st.success(f"✅ Feedback logged with ID: `{res['feedback_id']}`. Added to knowledge base review queue.")

        st.markdown("---")
        st.markdown("##### 📋 Recent Flagged Scheme Feedbacks:")
        fbs = get_all_feedbacks()
        if fbs:
            for fb in reversed(fbs[-3:]):
                st.markdown(f"• **{fb['scheme_name']}** ({fb['feedback_type']}): *\"{fb['description']}\"* — Reported by {fb['reporter_role']} ({fb['created_at'][:10]})")
        else:
            st.info("No active flags logged.")

    with sub_t3:
        st.markdown("#### 🏛️ Report to Higher Official (Formal Grievance Escalation)")
        st.markdown("""
        *If a farmer's claim, subsidy, or payment is stuck, denied without valid reason, or exceeds the statutory Citizens' Charter SLA, generate a formal, legally grounded grievance petition addressed to the competent authority.*
        """)

        with st.form("escalation_form"):
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                e_fname = st.text_input("Farmer Full Name", "Komirelli Ramulu", key="e_fname")
                e_parent = st.text_input("Father / Husband Name", "K. Venkaiah", key="e_parent")
                e_aadh = st.text_input("Masked Aadhaar Number", "XXXX-XXXX-4921", key="e_aadh")
                e_phone = st.text_input("Phone Number", "9848022338", key="e_phone")
            with e_col2:
                e_village = st.text_input("Village", "Geesugonda", key="e_village")
                e_mandal = st.text_input("Mandal", "Geesugonda", key="e_mandal")
                e_district = st.selectbox("District", ["Warangal", "Nalgonda", "Khammam", "Karimnagar", "Nizamabad"], key="e_district")
                e_survey = st.text_input("Survey / Parcel No.", "142/A", key="e_survey")

            e_cat = st.selectbox("Grievance Category", [
                "72-Hour PMFBY Loss Survey Not Conducted by Insurance Assessor",
                "DBT Payment Rejected due to False Name Mismatch",
                "TSMIP Drip Subsidy Equipment Not Dispatched after 10% DD Payment",
                "Rythu Bharosa / PM-KISAN Installment Not Credited",
                "PACS / Bank Demanding Unlawful Collateral for Loan under ₹1.60 Lakh"
            ])
            e_scheme = st.selectbox("Related Scheme", ["PMFBY Crop Insurance", "PM-KISAN", "Rythu Bharosa", "TSMIP Micro Irrigation", "Kisan Credit Card (KCC)"])
            e_level = st.selectbox("Escalation Authority Level", [
                "Level 1: Agriculture Extension Officer (AEO) - Rythu Vedika",
                "Level 2: Mandal Agriculture Officer (MAO) & Tahsildar",
                "Level 3: District Agriculture Officer (DAO) & District Collector (Prajavani)",
                "Level 4: Central Government CPGRAMS (pgportal.gov.in)"
            ])
            e_details = st.text_area("Detailed Facts & Timeline of Problem", "Crop loss due to unseasonal hailstorm occurred 5 days ago. Intimation was filed within 24 hours, but insurance company representative has not visited the parcel, violating the 72-hour survey rule.")

            gen_esc = st.form_submit_button("📜 Generate Formal Grievance Petition Letter", use_container_width=True)

        if gen_esc:
            petition = generate_formal_escalation_petition(
                farmer_name=e_fname,
                father_husband_name=e_parent,
                aadhaar_masked=e_aadh,
                phone=e_phone,
                village=e_village,
                mandal=e_mandal,
                district=e_district,
                survey_no=e_survey,
                problem_category=e_cat,
                scheme_name=e_scheme,
                description=e_details,
                escalation_level=e_level
            )
            st.success(f"✅ Formal Grievance Petition generated! Petition Ref: `{petition['petition_ref']}`")
            st.text_area("Official Grievance Petition (Ready to Print / Submit to Prajavani / CPGRAMS)", petition["petition_text"], height=320)
            st.download_button("📥 Download Petition as Text Document", petition["petition_text"], file_name=f"grievance_{e_fname.replace(' ', '_')}.txt", mime="text/plain", use_container_width=True)
