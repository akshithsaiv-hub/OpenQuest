import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_js_path = os.path.join(base_dir, "frontend", "data.js")

with open(data_js_path, "r", encoding="utf-8") as f:
    content = f.read()

tab3_translations = {
    "en": {
        "tab3_title": "Climate-Smart Water Subsidies & Dynamic Crop Migration Ecosystem",
        "tab3_desc": "Dynamic agro-climatic intelligence: Forecasts near-future dry spells, evaluates your current irrigation system, and identifies statutory bodies offering up to 100% subsidies to BUY or RENT micro-irrigation systems. Plus, calculates all viable high-yield crop migrations away from routine water-guzzling crops."
    },
    "te": {
        "tab3_title": "వాతావరణ ఆధారిత నీటి రాయితీలు & పంట మార్పిడి వేదిక",
        "tab3_desc": "రాబోయే వర్షాభావ పరిస్థితులను పసిగట్టి, బిందు సేద్యం (డ్రిప్) కొనుగోలుకు లేదా అద్దెకు ప్రభుత్వం అందించే 100% వరకు సబ్సిడీలను తెలియజేస్తుంది మరియు తక్కువ నీటితో అధిక లాభాలనిచ్చే ప్రత్యామ్నాయ పంటలను సూచిస్తుంది."
    },
    "hi": {
        "tab3_title": "मौसम-आधारित जल सब्सिडी एवं फसल विविधीकरण पारितंत्र",
        "tab3_desc": "आगामी सूखे की चेतावनी, ड्रिप/स्प्रिंकलर सिंचाई खरीदने या किराए पर लेने हेतु 100% तक सरकारी सब्सिडी, तथा धान/गन्ने की जगह कम पानी वाली लाभदायक फसलों के विकल्प प्रदान करता है।"
    },
    "mr": {
        "tab3_title": "हवामान-आधारित जलसंधारण सबसिडी व पीक बदल परिसंस्था",
        "tab3_desc": "नजीकच्या दुष्काळी स्थितीचा अंदाज घेऊन ठिबक सिंचन खरेदी अथवा भाड्याने घेण्यासाठी मिळणारे शासकीय अनुदान व कमी पाण्याच्या पर्यायी पिकांची परिपूर्ण माहिती."
    },
    "ta": {
        "tab3_title": "வானிலை அடிப்படையிலான பாசன மானியங்கள் & பயிர் மாற்று சுற்றுச்சூழல்",
        "tab3_desc": "எதிர்கால வறட்சி முன்னறிவிப்பு, சொட்டு நீர் பாசனம் வாங்க அல்லது வாடகைக்கு எடுக்க அரசு வழங்கும் மானியங்கள் மற்றும் குறைந்த நீர் மாற்றுப் பயிர்களின் வழிகாட்டுதல்."
    },
    "kn": {
        "tab3_title": "ಹವಾಮಾನ-ಆಧಾರಿತ ನೀರಾವರಿ ಸಬ್ಸಿಡಿ & ಬೆಳೆ ಬದಲಾವಣೆ ವ್ಯವಸ್ಥೆ",
        "tab3_desc": "ಮುಂಬರುವ ಬರಗಾಲದ ಮುನ್ಸೂಚನೆ, ಹನಿ ನೀರಾವರಿ ಖರೀದಿ ಅಥವಾ ಬಾಡಿಗೆಗೆ ಲಭ್ಯವಿರುವ 100% ವರೆಗಿನ ಸಬ್ಸಿಡಿ ಹಾಗೂ ಕಡಿಮೆ ನೀರಿನ ಪರ್ಯಾಯ ಬೆಳೆಗಳ ವಿವರ."
    }
}

patch_code = f"""
// TAB 3 ECOSYSTEM TRANSLATIONS EXTENSION
(function() {{
  if (typeof UI_TRANSLATIONS !== 'undefined') {{
    const ext = {json.dumps(tab3_translations, ensure_ascii=False, indent=2)};
    Object.keys(ext).forEach(function(lang) {{
      if (UI_TRANSLATIONS[lang]) {{
        Object.assign(UI_TRANSLATIONS[lang], ext[lang]);
      }}
    }});
  }}
}})();
"""

if "TAB 3 ECOSYSTEM TRANSLATIONS EXTENSION" not in content:
    with open(data_js_path, "a", encoding="utf-8") as f:
        f.write("\n" + patch_code + "\n")
    print("Tab 3 translations appended to data.js!")
else:
    print("Tab 3 translations already present in data.js")
