"""
Translation and localization utility for Farmer Assistant UI.
Provides localized UI labels, common agricultural phrases, and fallback translation.
"""

UI_LABELS = {
    "app_title": {
        "en": "🌾 Rythu Sahayata: Unified Farmer Scheme & Deadline Assistant",
        "te": "🌾 రైతు సహాయత: ప్రభుత్వ పథకాలు & గడువుల సహాయకుడు",
        "hi": "🌾 किसान सहायता: एकीकृत योजना एवं समय-सीमा सहायक"
    },
    "tagline": {
        "en": "Proactive, profile-driven scheme eligibility, insurance timelines, document checks & MSP awareness for Telangana farmers.",
        "te": "తెలంగాణ రైతులకు వ్యక్తిగత పథక అర్హత, పంట బీమా గడువులు, పత్రాల తనిఖీ మరియు మద్దతు ధర (MSP) మార్గదర్శి.",
        "hi": "तेलंगाना के किसानों हेतु व्यक्तिगत योजना पात्रता, फसल बीमा समय-सीमा, दस्तावेज सत्यापन और न्यूनतम समर्थन मूल्य (MSP) सहायक।"
    },
    "tab_scheme_explorer": {
        "en": "🏛️ State & Central Scheme Browser",
        "te": "🏛️ రాష్ట్ర & కేంద్ర పథకాల దర్శిని",
        "hi": "🏛️ राज्य एवं केंद्रीय योजना एक्सप्लोरर"
    },
    "tab_farmer_chat": {
        "en": "🧑‍🌾 Farmer Self-Service Chat",
        "te": "🧑‍🌾 రైతు సహాయక చాట్",
        "hi": "🧑‍🌾 किसान चैट सहायक"
    },
    "tab_intermediary": {
        "en": "🏢 Intermediary Mode (CSC / Extension / FPO)",
        "te": "🏢 సీఎస్‌సీ & వ్యవసాయ అధికారుల విభాగం",
        "hi": "🏢 सीएससी एवं कृषि अधिकारी डैशबोर्ड"
    },
    "tab_msp": {
        "en": "⚖️ MSP vs Mandi Price Tracker",
        "te": "⚖️ మద్దతు ధర (MSP) vs మార్కెట్ ధర",
        "hi": "⚖️ एमएसपी बनाम मंडी भाव ट्रैकर"
    },
    "tab_climate_shield": {
        "en": "🛡️ Multi-Crop Climate Risk & Protective Shield",
        "te": "🛡️ బహుళ పంటల వాతావరణ రక్షణ కవచం",
        "hi": "🛡️ बहु-फसल मौसम एवं आपदा सुरक्षा कवच"
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
