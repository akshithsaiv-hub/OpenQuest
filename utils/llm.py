import os
import json
import re
from typing import Dict, Any, List, Optional

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "te": "Telugu (తెలుగు)",
    "hi": "Hindi (हिंदी)"
}

FALLBACK_PMKISAN = {
    "en": (
        "ℹ️ **PM-KISAN Status & Grievance Notice**:\n\n"
        "For individual PM-KISAN installment disbursement status, e-KYC correction, and payment grievances, "
        "please use the official **Kisan e-Mitra AI Assistant**:\n"
        "🔗 [Kisan e-Mitra Portal](https://pmkisan.gov.in)\n"
        "📞 Toll-Free Helpline: **155261 / 011-24300606**\n"
        "🤖 Kisan e-Mitra Chatbot is accessible directly on the PM-KISAN homepage in 10+ languages."
    ),
    "te": (
        "ℹ️ **పీఎం-కిసాన్ చెల్లింపు & సమస్యల పరిష్కారం**:\n\n"
        "పీఎం-కిసాన్ వాయిదాల స్థితి, e-KYC ప్రక్రియ లేదా నిలిచిపోయిన చెల్లింపుల కోసం దయచేసి అధికారిక "
        "**కిసాన్ ఈ-మిత్ర (Kisan e-Mitra)** ఉపయోగించండి:\n"
        "🔗 [కిసాన్ ఈ-మిత్ర పోర్టల్](https://pmkisan.gov.in)\n"
        "📞 టోల్ ఫ్రీ నంబర్: **155261 / 011-24300606**\n"
        "మీరు అధికారిక వెబ్‌సైట్‌లో తెలుగు భాషలో నేరుగా మీ దరఖాస్తు స్థితిని తెలుసుకోవచ్చు."
    ),
    "hi": (
        "ℹ️ **पीएम-किसान भुगतान एवं शिकायत सूचना**:\n\n"
        "पीएम-किसान की किस्त स्थिति, e-KYC या अटके भुगतान की समस्या के समाधान के लिए कृपया आधिकारिक "
        "**किसान ई-मित्र (Kisan e-Mitra)** का उपयोग करें:\n"
        "🔗 [पीएम-किसान पोर्टल (Kisan e-Mitra)](https://pmkisan.gov.in)\n"
        "📞 टोल-फ्री हेल्पलाइन: **155261 / 011-24300606**\n"
        "यह सुविधा पीएम-किसान वेबसाइट पर हिंदी सहित अनेक भारतीय भाषाओं में उपलब्ध है।"
    )
}

FALLBACK_UNCERTAIN = {
    "en": (
        "⚠️ **Notice: Verification Needed**\n\n"
        "I do not have a verified, official rule or notification matching this specific query in the state database.\n\n"
        "👉 **Next Step**: Please contact your local **Agriculture Extension Officer (AEO)** at the nearest "
        "**Rythu Vedika** or visit the District Agriculture Office to verify accurate local guidelines."
    ),
    "te": (
        "⚠️ **ముఖ్య గమనిక: సమాచార ధృవీకరణ అవసరం**\n\n"
        "ఈ నిర్దిష్ట ప్రశ్నకు సంబంధించిన అధికారిక నిబంధనలు లేదా జీవోలు ప్రస్తుతం డేటాబేస్‌లో అందుబాటులో లేవు.\n\n"
        "👉 **తదుపరి చర్య**: సరైన మార్గదర్శకత్వం కోసం దయచేసి మీ గ్రామ సమీపంలోని **రైతు వేదిక** వద్ద గల "
        "**వ్యవసాయ విస్తరణ అధికారి (AEO)** ని లేదా మండల వ్యవసాయ కార్యాలయాన్ని సంప్రదించండి."
    ),
    "hi": (
        "⚠️ **सूचना: आधिकारिक पुष्टि आवश्यक**\n\n"
        "इस विशिष्ट प्रश्न के संबंध में वर्तमान राज्य डेटाबेस में सत्यापित सरकारी आदेश उपलब्ध नहीं है।\n\n"
        "👉 **अगला कदम**: सटीक एवं अद्यतन जानकारी के लिए कृपया अपने नजदीकी **कृषि विस्तार अधिकारी (AEO)** "
        "या विकास खंड कृषि कार्यालय (Rythu Vedika) से संपर्क करें।"
    )
}

def detect_pmkisan_intent(query_text: str) -> bool:
    if not query_text:
        return False
    q = query_text.lower()
    pmk_terms = ["pm kisan", "pm-kisan", "pmkisan", "kisan samman", "installment", "payment status", 
                 "hafta", "2000", "2,000", "ekyc", "e-kyc", "కిసాన్ డబ్బులు", "పీఎం కిసాన్", "వాయిదా", "किस्त", "पैसा कब आएगा"]
    return any(term in q for term in pmk_terms)

def detect_uncertainty(query_text: str) -> bool:
    if not query_text:
        return False
    q = query_text.lower()
    # If the user asks about out of scope topics e.g. crypto, gold loan, general politics, unknown states
    unrelated_terms = ["bitcoin", "crypto", "election vote", "gold loan", "car subsidy", "solar panel house", "punjab subsidy", "kerala loan"]
    return any(term in q for term in unrelated_terms)

def generate_plain_explanation(scheme: Dict[str, Any], language: str = "en") -> str:
    """
    STRICT LLM RULE:
    The LLM / generator only explains the deterministic eligibility result.
    It NEVER alters or calculates eligibility.
    Every answer MANDATORILY includes source_url and last_verified date.
    """
    lang = language.lower() if language else "en"
    if lang not in ["en", "te", "hi"]:
        lang = "en"

    name = scheme.get("name", "Government Scheme")
    benefits = scheme.get("benefits_summary", "")
    docs = scheme.get("documents_required", [])
    deadlines = scheme.get("deadlines", {})
    claim = scheme.get("claim_window")
    source_url = scheme.get("source_url", "https://agri.telangana.gov.in")
    last_verified = scheme.get("last_verified", "2026-11-01")
    where = scheme.get("where_to_apply", "Local Agriculture Office / CSC")
    reasons = scheme.get("reasons", [])

    # Format deadlines string
    deadline_strs = []
    if isinstance(deadlines, dict):
        for k, v in deadlines.items():
            formatted_k = k.replace("_", " ").title()
            deadline_strs.append(f"{formatted_k}: **{v}**")
    deadlines_text = " | ".join(deadline_strs) if deadline_strs else "Check official circular"

    # Format docs
    docs_text = "\n".join([f"  • {d}" for d in docs])

    if lang == "te":
        claim_section = ""
        if claim:
            claim_section = f"\n⏱️ **నష్ట పరిహార గడువు (Claim Window)**: {claim.get('window', '72 గంటల లోపు')}\n📞 హెల్ప్‌లైన్: {claim.get('helpline', '1800-180-1551')}\n"

        explanation = f"""🏛️ **పథకం**: {name}
📝 **ప్రయోజనాలు**: {benefits}

✅ **అర్హత కారణాలు**:
{chr(10).join(['  • ' + r for r in reasons])}

📋 **కావలసిన పత్రాలు**:
{docs_text}

⏰ **ముఖ్యమైన గడువులు (Deadlines)**:
  {deadlines_text}
{claim_section}
📍 **దరఖాస్తు ఎక్కడ చేయాలి**: {where}

🔗 **అధికారిక వెబ్‌సైట్**: [{source_url}]({source_url})
📅 **చివరిగా ధృవీకరించిన తేదీ**: {last_verified}
"""

    elif lang == "hi":
        claim_section = ""
        if claim:
            claim_section = f"\n⏱️ **दावा रिपोर्टिंग अवधि (Claim Window)**: {claim.get('window', '72 घंटे के भीतर')}\n📞 हेल्पलाइन: {claim.get('helpline', '1800-180-1551')}\n"

        explanation = f"""🏛️ **योजना**: {name}
📝 **लाभ का विवरण**: {benefits}

✅ **पात्रता के आधार**:
{chr(10).join(['  • ' + r for r in reasons])}

📋 **आवश्यक दस्तावेज**:
{docs_text}

⏰ **महत्वपूर्ण समय-सीमा (Deadlines)**:
  {deadlines_text}
{claim_section}
📍 **आवेदन कहाँ करें**: {where}

🔗 **आधिकारिक स्रोत लिंक**: [{source_url}]({source_url})
📅 **अंतिम सत्यापन तिथि**: {last_verified}
"""

    else:  # English
        claim_section = ""
        if claim:
            claim_section = f"\n⏱️ **Claim Reporting Window**: {claim.get('window', 'Within 72 hours')}\n📞 Helpline: {claim.get('helpline', '1800-180-1551')}\n"

        explanation = f"""🏛️ **Scheme**: {name}
📝 **Key Benefits**: {benefits}

✅ **Eligibility Determination**:
{chr(10).join(['  • ' + r for r in reasons])}

📋 **Required Documents**:
{docs_text}

⏰ **Deadlines & Cut-offs**:
  {deadlines_text}
{claim_section}
📍 **Where to Apply**: {where}

🔗 **Official Source**: [{source_url}]({source_url})
📅 **Last Verified**: {last_verified}
"""

    return explanation.strip()

def process_farmer_query(
    query_text: Optional[str],
    eligible_schemes: List[Dict[str, Any]],
    language: str = "en"
) -> Dict[str, Any]:
    """
    Orchestrates the chat explanation response with fallback routing.
    """
    lang = language if language in ["en", "te", "hi"] else "en"

    # Fallback 1: PM-KISAN specific payment inquiry redirect
    if query_text and detect_pmkisan_intent(query_text):
        return {
            "type": "redirect_kisan_emitra",
            "message": FALLBACK_PMKISAN[lang],
            "action": "redirect",
            "url": "https://pmkisan.gov.in"
        }

    # Fallback 2: Out of scope / uncertain queries
    if query_text and detect_uncertainty(query_text):
        return {
            "type": "uncertainty_fallback",
            "message": FALLBACK_UNCERTAIN[lang],
            "action": "contact_officer"
        }

    # Standard path: Explain eligible schemes
    if not eligible_schemes:
        no_schemes_msg = {
            "en": "No government schemes matched your exact land or crop criteria. Please verify if your state is Telangana.",
            "te": "మీ భూమి లేదా పంట వివరాలకు సరిపోలే పథకాలు ప్రస్తుతానికి అందుబాటులో లేవు. మీ వివరాలను పునఃపరిశీలించండి.",
            "hi": "आपकी भूमि या फसल विवरण के अनुसार कोई योजना नहीं मिली। कृपया अपने विवरण की पुनः जांच करें।"
        }
        return {
            "type": "no_match",
            "message": no_schemes_msg[lang],
            "explanations": []
        }

    explanations = [generate_plain_explanation(s, language=lang) for s in eligible_schemes]
    
    intro_map = {
        "en": f"✅ Based on your verified profile, you are eligible for **{len(eligible_schemes)} government schemes**:",
        "te": f"✅ మీ ధృవీకరించబడిన ప్రొఫైల్ ఆధారంగా, మీరు **{len(eligible_schemes)} ప్రభుత్వ పథకాలకు** అర్హులు:",
        "hi": f"✅ आपके सत्यापित विवरण के आधार पर, आप **{len(eligible_schemes)} सरकारी योजनाओं** के लिए पात्र हैं:"
    }

    full_response = intro_map[lang] + "\n\n" + "\n\n---\n\n".join(explanations)
    return {
        "type": "scheme_matches",
        "message": full_response,
        "explanations": explanations,
        "count": len(eligible_schemes)
    }
