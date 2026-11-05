"""
Translation and localization utility for Farmer Assistant UI.
Provides localized UI labels, common agricultural phrases, and fallback translation.
Supports English, Telugu (తెలుగు), and Hindi (हिंदी).
"""

UI_LABELS = {
    "app_title": {
        "en": "🌾 Rythu Sahayata: Unified Farmer Scheme & Deadline Assistant",
        "te": "🌾 రైతు సహాయత: ప్రభుత్వ పథకాలు & గడువుల సహాయకుడు",
        "hi": "🌾 किसान सहायता: एकीकृत योजना एवं समय-सीमा सहायक"
    },
    "tagline": {
        "en": "Pan-India proactive scheme eligibility, 72-hr claim assistant, water-saving subsidies, KCC credit help & document wallet.",
        "te": "భారతీయ రైతులకు సమగ్ర పథక అర్హత, 72 గంటల నష్ట పరిహార క్లెయిమ్ సహాయకుడు, నీటి పొదుపు సబ్సిడీలు మరియు కేసీసీ రుణ మార్గదర్శి.",
        "hi": "अखिल भारतीय किसान योजना पात्रता, 72-घंटे दावा सहायक, जल-बचत सब्सिडी, केसीसी ऋण मार्गदर्शन एवं दस्तावेज़ वॉलेट।"
    },
    "tab_scheme_explorer": {
        "en": "🌾 State & Central Scheme Browser",
        "te": "🌾 రాష్ట్ర & కేంద్ర ప్రభుత్వ పథకాల బ్రౌజర్",
        "hi": "🌾 राज्य एवं केंद्र सरकार योजनाएं"
    },
    "tab_farmer_chat": {
        "en": "🧑‍🌾 Scheme Eligibility & Chat",
        "te": "🧑‍🌾 రైతు సహాయక చాట్ & అర్హత",
        "hi": "🧑‍🌾 किसान चैट एवं पात्रता"
    },
    "tab_climate_shield": {
        "en": "🛡️ Climate Risk & 72-Hr Claim Shield",
        "te": "🛡️ వాతావరణ రక్షణ & 72 గంటల క్లెయిమ్",
        "hi": "🛡️ मौसम जोखिम व 72-घंटे दावा कवच"
    },
    "tab_water_saving": {
        "en": "💧 Water Subsidies & Next-Crop Planning",
        "te": "💧 నీటి పొదుపు సబ్సిడీలు & ప్రత్యామ్నాయ పంటలు",
        "hi": "💧 जल-बचत सब्सिडी व फसल नियोजन"
    },
    "tab_credit_kcc": {
        "en": "💳 KCC Credit Help & Status Tracker",
        "te": "💳 కేసీసీ రుణాలు & దరఖాస్తు ట్రాకర్",
        "hi": "💳 केसीसी ऋण व आवेदन ट्रैकर"
    },
    "tab_doc_wallet": {
        "en": "📁 Document Wallet & DigiLocker",
        "te": "📁 పత్రాల వాలెట్ & డిజిలాకర్",
        "hi": "📁 दस्तावेज़ वॉलेट व डिजिलॉकर"
    },
    "tab_msp": {
        "en": "⚖️ MSP vs Mandi Tracker",
        "te": "⚖️ మద్దతు ధర (MSP) vs మార్కెట్ ధర",
        "hi": "⚖️ एमएसपी बनाम मंडी भाव"
    },
    "tab_intermediary": {
        "en": "🏢 Intermediary Desk & Escalation",
        "te": "🏢 సీఎస్‌సీ డెస్క్ & ఫిర్యాదుల పరిష్కారం",
        "hi": "🏢 सीएससी डेस्क व उच्चाधिकारी शिकायत"
    },
    "profile_header": {
        "en": "📋 Enter Your Farming Profile",
        "te": "📋 మీ వ్యవసాయ వివరాలను నమోదు చేయండి",
        "hi": "📋 अपनी कृषि प्रोफाइल दर्ज करें"
    },
    "state_label": {
        "en": "State",
        "te": "రాష్ట్రం",
        "hi": "राज्य"
    },
    "district_label": {
        "en": "District",
        "te": "జిల్లా",
        "hi": "जिला"
    },
    "land_label": {
        "en": "Land Holding (Acres)",
        "te": "భూమి విస్తీర్ణం (ఎకరాల్లో)",
        "hi": "भूमि का रकबा (एकड़ में)"
    },
    "crop_label": {
        "en": "Current Season Crop",
        "te": "ప్రస్తుత పంట",
        "hi": "वर्तमान फसल"
    },
    "category_label": {
        "en": "Farmer Category",
        "te": "రైతు వర్గం",
        "hi": "किसान श्रेणी"
    },
    "tenant_label": {
        "en": "Are you a Tenant Farmer?",
        "te": "మీరు కౌలు రైతులా?",
        "hi": "क्या आप बटाईदार/किरायेदार किसान हैं?"
    },
    "ccrc_label": {
        "en": "Do you hold a valid CCRC card?",
        "te": "మీ వద్ద చెల్లుబాటు అయ్యే CCRC కార్డు ఉందా?",
        "hi": "क्या आपके पास CCRC कार्ड है?"
    },
    "check_btn": {
        "en": "🔍 Check My Scheme Eligibility",
        "te": "🔍 నా పథక అర్హతను పరిశీలించండి",
        "hi": "🔍 मेरी योजना पात्रता जांचें"
    }
}

def get_label(key: str, lang: str = "en") -> str:
    lang = lang.lower() if lang in ["en", "te", "hi"] else "en"
    return UI_LABELS.get(key, {}).get(lang, UI_LABELS.get(key, {}).get("en", key))
