import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_js_path = os.path.join(base_dir, "frontend", "data.js")

with open(data_js_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extended translations for all supported languages
tab_and_new_translations = {
    "en": {
        "nav_tab0": "Scheme Browser",
        "nav_tab1": "Eligibility & Voice AI",
        "nav_tab2": "72-Hr Claim Shield",
        "nav_tab3": "Water Subsidies & Crops",
        "nav_tab4": "KCC Loan & Tracker",
        "nav_tab5": "Document Wallet",
        "nav_tab6": "MSP vs Mandi",
        "nav_tab7": "Intermediary & Escalation",
        "doc_wallet_title": "Consent-Driven Farmer Document Wallet & DigiLocker",
        "doc_wallet_desc": "Store scanned land records (Pahani/Dharani), Aadhaar, Bank Passbooks, and CCRC agreements with explicit consent. Download official sample templates below.",
        "download_sample_btn": "Download Sample Copy",
        "preview_sample_btn": "Full Preview",
        "voice_title": "Multilingual AI Voice Assistant",
        "voice_subtitle": "Speak in any Indian language. OpenQuest understands and speaks back in your language!",
        "voice_click_speak": "Click microphone to speak...",
        "voice_listening": "Listening... Speak now",
        "voice_send_btn": "Send Question",
        "voice_placeholder": "Ask in your language or click microphone...",
        "listen_again_btn": "🔊 Listen to Answer",
        "stop_speaking_btn": "⏹️ Stop Voice"
    },
    "te": {
        "nav_tab0": "పథకాల జాబితా",
        "nav_tab1": "అర్హత & వాయిస్ AI",
        "nav_tab2": "72-గంటల క్లెయిమ్ షీల్డ్",
        "nav_tab3": "నీటి రాయితీలు & పంటలు",
        "nav_tab4": "KCC రుణం & ట్రాకర్",
        "nav_tab5": "పత్రాల వాలెట్",
        "nav_tab6": "మద్దతు ధర vs మార్కెట్",
        "nav_tab7": "మధ్యవర్తి & ఫిర్యాదులు",
        "doc_wallet_title": "రైతు పత్రాల వాలెట్ & డిజిలాకర్",
        "doc_wallet_desc": "పట్టాదార్ పాస్‌బుక్ (పహానీ), ఆధార్, బ్యాంక్ పాస్‌బుక్ మరియు CCRC నమూనా పత్రాలను ఇక్కడ డౌన్‌లోడ్ చేసుకోండి.",
        "download_sample_btn": "నమూనా పత్రం డౌన్‌లోడ్",
        "preview_sample_btn": "పూర్తి వీక్షణ",
        "voice_title": "బహుభాషా AI వాయిస్ అసిస్టెంట్",
        "voice_subtitle": "మీ స్వంత భాషలో మాట్లాడండి. ఓపెన్‌క్వెస్ట్ మీ భాషలోనే విని, సమాధానం ఇస్తుంది!",
        "voice_click_speak": "మాట్లాడటానికి మైక్రోఫోన్ పై క్లిక్ చేయండి...",
        "voice_listening": "వింటున్నాము... ఇప్పుడు మాట్లాడండి",
        "voice_send_btn": "ప్రశ్న పంపండి",
        "voice_placeholder": "మీ ప్రశ్నను తెలుగులో అడగండి లేదా మాట్లాడండి...",
        "listen_again_btn": "🔊 సమాధానం వినండి",
        "stop_speaking_btn": "⏹️ ఆపండి"
    },
    "hi": {
        "nav_tab0": "योजना ब्राउज़र",
        "nav_tab1": "पात्रता एवं वॉयस AI",
        "nav_tab2": "72-घंटे का क्लेम शील्ड",
        "nav_tab3": "जल सब्सिडी एवं फसलें",
        "nav_tab4": "केसीसी ऋण एवं ट्रैकर",
        "nav_tab5": "दस्तावेज़ वॉलेट",
        "nav_tab6": "एमएसपी बनाम मंडी",
        "nav_tab7": "सुविधा प्रदाता एवं निवारण",
        "doc_wallet_title": "कृषक दस्तावेज़ वॉलेट एवं डिजिलॉकर",
        "doc_wallet_desc": "खसरा-खतौनी, आधार कार्ड, बैंक पासबुक और बटाईदार अनुबंध के आधिकारिक नमूने नीचे से डाउनलोड करें।",
        "download_sample_btn": "नमूना कॉपी डाउनलोड करें",
        "preview_sample_btn": "पूर्ण दृश्य",
        "voice_title": "बहुभाषी AI वॉयस सहायक",
        "voice_subtitle": "अपनी मातृभाषा में बोलें। ओपनक्वेस्ट आपकी भाषा में सुनकर उत्तर देगा!",
        "voice_click_speak": "बोलने के लिए माइक दबाएं...",
        "voice_listening": "सुन रहे हैं... अब बोलें",
        "voice_send_btn": "प्रश्न भेजें",
        "voice_placeholder": "अपनी भाषा में पूछें या माइक दबाएं...",
        "listen_again_btn": "🔊 उत्तर सुनें",
        "stop_speaking_btn": "⏹️ बंद करें"
    },
    "mr": {
        "nav_tab0": "योजना यादी",
        "nav_tab1": "पात्रता व व्हॉईस AI",
        "nav_tab2": "७२-तास नुकसान भरपाई",
        "nav_tab3": "जलसंधारण व पिके",
        "nav_tab4": "केसीसी कर्ज व ट्रॅकर",
        "nav_tab5": "कागदपत्रे वॉलेट",
        "nav_tab6": "हमीभाव वि. बाजार समिती",
        "nav_tab7": "ग्राम ऑपरेटर डेस्क",
        "doc_wallet_title": "शेतकरी कागदपत्रे वॉलेट व डिजीलॉकर",
        "doc_wallet_desc": "७/१२ उतारा, आधार, बँक पासबुक व भाडेकरू कराराचे नमुने खाली डाउनलोड करा.",
        "download_sample_btn": "नमुना डाउनलोड करा",
        "preview_sample_btn": "पूर्ण पूर्वावलोकन",
        "voice_title": "बहुभाषिक AI व्हॉईस सहाय्यक",
        "voice_subtitle": "आपल्या भाषेत बोला. ओपनक्वेस्ट आपल्या भाषेत उत्तर देईल!",
        "voice_click_speak": "बोलण्यासाठी माइक दाबा...",
        "voice_listening": "ऐकत आहे... आता बोला",
        "voice_send_btn": "प्रश्न विचारा",
        "voice_placeholder": "मराठीत विचारा किंवा बोला...",
        "listen_again_btn": "🔊 उत्तर ऐका",
        "stop_speaking_btn": "⏹️ थांबवा"
    },
    "ta": {
        "nav_tab0": "திட்டங்கள் உலாவி",
        "nav_tab1": "தகுதி & குரல் AI",
        "nav_tab2": "72 மணி நேர இழப்பீட்டு கவசம்",
        "nav_tab3": "நீர்ப்பாசன மானியம் & பயிர்கள்",
        "nav_tab4": "KCC கடன் & கண்காணிப்பாளர்",
        "nav_tab5": "ஆவண பை (Wallet)",
        "nav_tab6": "ஆதரவு விலை vs மண்டி",
        "nav_tab7": "கிராம சேவை மையம்",
        "doc_wallet_title": "விவசாயி ஆவண பை மற்றும் டிஜிலாக்கர்",
        "doc_wallet_desc": "பட்டா சிட்டா, ஆதார் அட்டை, வங்கி பாஸ்புக் மற்றும் குத்தகை ஒப்பந்த மாதிரி ஆவணங்களை பதிவிறக்கவும்.",
        "download_sample_btn": "மாதிரி நகல் பதிவிறக்கம்",
        "preview_sample_btn": "முழு பார்வை",
        "voice_title": "பன்மொழி AI குரல் உதவியாளர்",
        "voice_subtitle": "உங்கள் மொழியில் பேசுங்கள். ஓபன் குவெஸ்ட் உங்கள் மொழியிலேயே பதிலளிக்கும்!",
        "voice_click_speak": "பேச மைக்கை அழுத்தவும்...",
        "voice_listening": "கேட்கிறது... இப்போது பேசுங்கள்",
        "voice_send_btn": "கேள்வி அனுப்பவும்",
        "voice_placeholder": "தமிழில் கேளுங்கள் அல்லது பேசுங்கள்...",
        "listen_again_btn": "🔊 பதில் கேட்க",
        "stop_speaking_btn": "⏹️ நிறுத்த"
    },
    "kn": {
        "nav_tab0": "ಯೋಜನೆಗಳ ಪಟ್ಟಿ",
        "nav_tab1": "ಅರ್ಹತೆ & ಧ್ವನಿ AI",
        "nav_tab2": "72-ಗಂಟೆಗಳ ಪರಿಹಾರ ರಕ್ಷೆ",
        "nav_tab3": "ನೀರಾವರಿ ಸಬ್ಸಿಡಿ & ಬೆಳೆಗಳು",
        "nav_tab4": "ಕೆಸಿಸಿ ಸಾಲ & ಟ್ರ್ಯಾಕರ್",
        "nav_tab5": "ದಾಖಲೆಗಳ ವಾಲೆಟ್",
        "nav_tab6": "ಬೆಂಬಲ ಬೆಲೆ vs ಮಾರುಕಟ್ಟೆ",
        "nav_tab7": "ಗ್ರಾಮ ಸೇವಾ ಡೆಸ್ಕ್",
        "doc_wallet_title": "ರೈತ ದಾಖಲೆಗಳ ವಾಲೆಟ್ & ಡಿಜಿಲಾಕರ್",
        "doc_wallet_desc": "ಪಹಣಿ/ಆರ್‌ಒಆರ್, ಆಧಾರ್, ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್ ಮತ್ತು ಗೇಣಿದಾರರ ಒಪ್ಪಂದದ ಮಾದರಿ ಪ್ರತಿಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ.",
        "download_sample_btn": "ಮಾದರಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ",
        "preview_sample_btn": "ಪೂರ್ಣ ನೋಟ",
        "voice_title": "ಬಹುಭಾಷಾ AI ಧ್ವನಿ ಸಹಾಯಕ",
        "voice_subtitle": "ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಮಾತನಾಡಿ. ಓಪನ್‌ಕ್ವೆಸ್ಟ್ ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲೇ ಉತ್ತರಿಸುತ್ತದೆ!",
        "voice_click_speak": "ಮಾತನಾಡಲು ಮೈಕ್ ಒತ್ತಿರಿ...",
        "voice_listening": "ಕೇಳಿಸಿಕೊಳ್ಳುತ್ತಿದೆ... ಈಗ ಮಾತನಾಡಿ",
        "voice_send_btn": "ಪ್ರಶ್ನೆ ಕಳುಹಿಸಿ",
        "voice_placeholder": "ಕನ್ನಡದಲ್ಲಿ ಕೇಳಿ ಅಥವಾ ಮಾತನಾಡಿ...",
        "listen_again_btn": "🔊 ಉತ್ತರವನ್ನು ಆಲಿಸಿ",
        "stop_speaking_btn": "⏹️ ನಿಲ್ಲಿಸಿ"
    }
}

# We can append an extension block to UI_TRANSLATIONS in data.js
patch_code = f"""
// EXTENDED MULTILINGUAL TAB & MODULE TRANSLATIONS
(function() {{
  if (typeof UI_TRANSLATIONS !== 'undefined') {{
    const ext = {json.dumps(tab_and_new_translations, ensure_ascii=False, indent=2)};
    Object.keys(ext).forEach(function(lang) {{
      if (UI_TRANSLATIONS[lang]) {{
        Object.assign(UI_TRANSLATIONS[lang], ext[lang]);
      }} else {{
        UI_TRANSLATIONS[lang] = ext[lang];
      }}
    }});
  }}
}})();
"""

if "EXTENDED MULTILINGUAL TAB & MODULE TRANSLATIONS" not in content:
    with open(data_js_path, "a", encoding="utf-8") as f:
        f.write("\n" + patch_code + "\n")
    print("UI_TRANSLATIONS patched successfully in data.js!")
else:
    print("Translations extension already present.")
