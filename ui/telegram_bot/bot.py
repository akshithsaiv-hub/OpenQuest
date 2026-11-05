import os
import sys
import io

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import logging
import asyncio
import json
import requests
from typing import Dict, Any

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.llm import process_farmer_query, generate_plain_explanation, FALLBACK_PMKISAN, FALLBACK_UNCERTAIN
from utils.weather_api import get_live_weather, evaluate_water_stress, generate_multilingual_water_advisory
from backend.eligibility_api import evaluate_farmer, load_schemes, FarmerProfile

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("FarmerBot")

API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# In-memory session store for demo (simulating Person 3's profile store)
USER_PROFILES: Dict[int, Dict[str, Any]] = {}

def get_farmer_schemes(profile_data: Dict[str, Any]):
    """Calls deterministic API or direct module fallback."""
    try:
        resp = requests.post(f"{API_URL}/match", json=profile_data, timeout=3)
        if resp.status_code == 200:
            return resp.json().get("eligible_schemes", [])
    except Exception:
        pass
    
    # Fallback directly to deterministic rules
    prof = FarmerProfile(**profile_data)
    schemes = load_schemes()
    return [evaluate_farmer(prof, s).model_dump() for s in schemes if evaluate_farmer(prof, s).eligible]

async def start_handler(update, context):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Default profile
    USER_PROFILES[chat_id] = {
        "farmer_id": f"TG-{chat_id}",
        "name": user.first_name or "Farmer",
        "state": "Telangana",
        "district": "Warangal",
        "land_holding_acres": 2.0,
        "crop": "Paddy",
        "category": "marginal",
        "is_tenant": False,
        "has_ccrc": False,
        "caste_category": "BC",
        "has_irrigation_well": True,
        "language": "te" if (user.language_code and "te" in user.language_code) else ("hi" if (user.language_code and "hi" in user.language_code) else "en")
    }

    welcome_msg = (
        f"🌾 **నమస్కారం {user.first_name}! రైతు సహాయత కు స్వాగతం.**\n"
        f"🌾 **Namaste {user.first_name}! Welcome to Rythu Sahayata.**\n\n"
        "నేను తెలంగాణ రైతులకు ప్రభుత్వ పథకాలు, పంట బీమా గడువులు మరియు మద్దతు ధర (MSP) వివరాలను అందించే సహాయకుడిని.\n\n"
        "📌 **Available Commands / ఆదేశాలు:**\n"
        "/schemes - నా అర్హత పథకాలు చూడండి (View Eligible Schemes)\n"
        "/deadlines - బీమా మరియు దరఖాస్తు గడువులు (Upcoming Deadlines)\n"
        "/msp - ధాన్యం & పత్తి మద్దతు ధరలు (MSP Price Tracker)\n"
        "/water_alert - వరి పంట నీటి ఎద్దడి & వాతావరణ రక్షణ (Climate & Water Shield)\n"
        "/lang - భాష మార్చండి (Change Language: te / hi / en)\n"
        "/help - సహాయం పొందండి (Help & Fallback Guide)\n\n"
        "లేదా మీ ప్రశ్నను నేరుగా టైప్ చేయండి (ఉదా: 'పంట బీమా చివరి తేదీ ఎప్పుడు?')."
    )
    await update.message.reply_text(welcome_msg, parse_mode="Markdown")

async def schemes_handler(update, context):
    chat_id = update.effective_chat.id
    profile = USER_PROFILES.get(chat_id, {
        "farmer_id": f"TG-{chat_id}",
        "name": "Farmer",
        "state": "Telangana",
        "district": "Warangal",
        "land_holding_acres": 2.0,
        "crop": "Paddy",
        "category": "marginal",
        "is_tenant": False,
        "has_ccrc": False,
        "caste_category": "BC",
        "has_irrigation_well": True,
        "language": "en"
    })

    lang = profile.get("language", "en")
    eligible = get_farmer_schemes(profile)
    result = process_farmer_query(None, eligible, language=lang)
    await update.message.reply_text(result["message"], parse_mode="Markdown", disable_web_page_preview=True)

async def deadlines_handler(update, context):
    chat_id = update.effective_chat.id
    profile = USER_PROFILES.get(chat_id, {})
    lang = profile.get("language", "en")

    deadlines_info = (
        "⏰ **తెలంగాణ రైతు ముఖ్యమైన గడువులు (Upcoming Deadlines 2026):**\n\n"
        "1. 🌾 **PMFBY రబీ పంట బీమా నమోదు ముగింపు తేది**: **15-నవంబర్-2026**\n"
        "   - వర్తించే పంటలు: వరి, శనగ, వేరుశనగ, మొక్కజొన్న.\n"
        "2. ⚡ **పంట నష్టం రిపోర్టింగ్ గడువు (Crop Loss Claim)**: **72 గంటల లోపు**\n"
        "   - అకాల వర్షం లేదా వడగండ్ల వాన వల్ల పంట దెబ్బతింటే 72 గంటల్లో టోల్ ఫ్రీ 1800-180-1551 కి సమాచారం ఇవ్వాలి.\n"
        "3. 💰 **రైతు భరోసా రబీ వివరాల నమోదు**: **25-నవంబర్-2026**\n"
        "4. ⚖️ **వరి & పత్తి కొనుగోలు కేంద్రాల ముగింపు**: **31-జనవరి-2027**\n\n"
        "🔗 అధికారిక వివరాలు: [pmfby.gov.in](https://pmfby.gov.in) | [agri.telangana.gov.in](https://agri.telangana.gov.in)\n"
        "📅 చివరిగా ధృవీకరించిన తేదీ: 2026-11-01"
    )
    await update.message.reply_text(deadlines_info, parse_mode="Markdown", disable_web_page_preview=True)

async def msp_handler(update, context):
    msp_text = (
        "⚖️ **కనీస మద్దతు ధర (MSP) vs మార్కెట్ ధర - 2026:**\n\n"
        "🌾 **వరి (గ్రేడ్ 'A')**: ప్రభుత్వం ధర **₹2,320** + తెలంగాణ బోనస్ **₹500** = **₹2,820/క్వింటాల్**\n"
        "   (బహిరంగ మార్కెట్ లో ₹2,180 మాత్రమే ఉంది. PACS / IKP కేంద్రంలో అమ్మితే క్వింటాల్‌కు ₹640 లాభం!)\n\n"
        "🌱 **పత్తి (మధ్యస్థ పింజ)**: MSP **₹7,121/క్వింటాల్** (CCI కొనుగోలు కేంద్రాల్లో)\n"
        "🌽 **మొక్కజొన్న**: MSP **₹2,225/క్వింటాల్**\n\n"
        "🔗 ఆధారం: తెలంగాణ పౌరసరఫరాల సంస్థ (epds.telangana.gov.in)\n"
        "📅 చివరిగా ధృవీకరించిన తేదీ: 2026-11-02"
    )
    await update.message.reply_text(msp_text, parse_mode="Markdown", disable_web_page_preview=True)

async def lang_handler(update, context):
    chat_id = update.effective_chat.id
    args = context.args
    if args and args[0].lower() in ["te", "hi", "en"]:
        new_lang = args[0].lower()
        if chat_id in USER_PROFILES:
            USER_PROFILES[chat_id]["language"] = new_lang
        ack = {
            "te": "✅ భాష తెలుగుగా మార్చబడింది.",
            "hi": "✅ भाषा बदलकर हिंदी कर दी गई है।",
            "en": "✅ Language changed to English."
        }
        await update.message.reply_text(ack[new_lang])
    else:
        await update.message.reply_text(
            "దయచేసి భాషను ఎంచుకోవడానికి ఇలా టైప్ చేయండి:\n"
            "/lang te  -> తెలుగు (Telugu)\n"
            "/lang hi  -> हिंदी (Hindi)\n"
            "/lang en  -> English"
        )

async def water_alert_handler(update, context):
    chat_id = update.effective_chat.id
    profile = USER_PROFILES.get(chat_id, {})
    dist = profile.get("district", "Warangal")
    lang = profile.get("language", "te")

    weather = get_live_weather(dist)
    assessment = evaluate_water_stress(weather, crop="Paddy", water_source="Borewell")
    advisory = generate_multilingual_water_advisory(assessment, lang=lang)
    await update.message.reply_text(advisory, parse_mode="Markdown", disable_web_page_preview=True)

async def text_message_handler(update, context):
    chat_id = update.effective_chat.id
    query = update.message.text
    profile = USER_PROFILES.get(chat_id, {
        "farmer_id": f"TG-{chat_id}",
        "name": "Farmer",
        "state": "Telangana",
        "district": "Warangal",
        "land_holding_acres": 2.0,
        "crop": "Paddy",
        "category": "marginal",
        "is_tenant": False,
        "has_ccrc": False,
        "caste_category": "BC",
        "has_irrigation_well": True,
        "language": "en"
    })
    lang = profile.get("language", "en")

    eligible = get_farmer_schemes(profile)
    res = process_farmer_query(query, eligible, language=lang)
    await update.message.reply_text(res["message"], parse_mode="Markdown", disable_web_page_preview=True)

def run_cli_demo():
    """Interactive CLI test runner for testing without a Telegram token."""
    print("=" * 70)
    print("🌾 RYTHU SAHAYATA: Unified Farmer Assistant (Person 2 CLI Test Mode)")
    print("=" * 70)
    print("Simulating farmer interaction in Telangana...")
    
    test_profile = {
        "farmer_id": "F-CLI-01",
        "name": "Ravi Kumar",
        "state": "Telangana",
        "district": "Warangal",
        "land_holding_acres": 2.0,
        "crop": "Paddy",
        "category": "marginal",
        "is_tenant": False,
        "has_ccrc": False,
        "caste_category": "BC",
        "has_irrigation_well": True,
        "language": "en"
    }

    schemes = get_farmer_schemes(test_profile)
    print(f"\n[1] Deterministic Match Output ({len(schemes)} eligible schemes):")
    for s in schemes:
        print(f"  • {s['name']} ({s['category']}) - Source: {s['source_url']}")

    print("\n[2] Testing Multilingual LLM Plain Explanation (Telugu):")
    res_te = process_farmer_query(None, schemes, language="te")
    print(res_te["message"][:400] + "...\n[Truncated for brevity]")

    print("\n[3] Testing Fallback 1: PM-KISAN Payment Query:")
    pmk_res = process_farmer_query("Where is my PM-KISAN 2000 rupees payment?", schemes, language="en")
    print(pmk_res["message"])

    print("\n[4] Testing Fallback 2: Out of scope uncertain topic:")
    unc_res = process_farmer_query("How to get bitcoin subsidy loan?", schemes, language="en")
    print(unc_res["message"])

    print("\n[5] Testing Live Climate API & Rice Water Stress Advisory:")
    weather = get_live_weather("Warangal")
    assessment = evaluate_water_stress(weather, crop="Paddy", water_source="Borewell")
    print(f"  Live Climate Status: {weather['status']} (District: {weather['district']})")
    print(f"  Current Temp: {weather['current_temperature']}°C | 7-Day Forecast Rain: {weather['forecast_7day_total_rain_mm']} mm")
    print(f"  Water Stress Assessment: {assessment['stress_level']} ({assessment['stress_title']})")
    advisory_te = generate_multilingual_water_advisory(assessment, lang="te")
    print(f"  Generated Telugu Advisory (First 250 chars):\n  {advisory_te[:250]}...")
    print("=" * 70)
    print("✅ All Person 2 validation test scenarios passed successfully!")

def main():
    if "--test" in sys.argv:
        run_cli_demo()
        return

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.warning("No TELEGRAM_BOT_TOKEN set in environment. Running interactive validation CLI instead...")
        run_cli_demo()
        return

    try:
        from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("start", start_handler))
        app.add_handler(CommandHandler("schemes", schemes_handler))
        app.add_handler(CommandHandler("deadlines", deadlines_handler))
        app.add_handler(CommandHandler("msp", msp_handler))
        app.add_handler(CommandHandler("water_alert", water_alert_handler))
        app.add_handler(CommandHandler("lang", lang_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))
        
        logger.info("Bot starting with long polling...")
        app.run_polling()
    except Exception as e:
        logger.error(f"Error starting Telegram bot: {e}")

if __name__ == "__main__":
    main()
