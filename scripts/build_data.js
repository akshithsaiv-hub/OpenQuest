// Script to build updated frontend/data.js with all 29 states, criteria, and translations
const fs = require('fs');
const path = require('path');

const rootDir = path.join(__dirname, '..');
const currentDataPath = path.join(rootDir, 'frontend', 'data.js');

// 29 Indian States
const ALL_29_STATES = [
  { name: "Andhra Pradesh", code: "AP" },
  { name: "Arunachal Pradesh", code: "AR" },
  { name: "Assam", code: "AS" },
  { name: "Bihar", code: "BR" },
  { name: "Chhattisgarh", code: "CG" },
  { name: "Goa", code: "GA" },
  { name: "Gujarat", code: "GJ" },
  { name: "Haryana", code: "HR" },
  { name: "Himachal Pradesh", code: "HP" },
  { name: "Jammu and Kashmir", code: "JK" },
  { name: "Jharkhand", code: "JH" },
  { name: "Karnataka", code: "KA" },
  { name: "Kerala", code: "KL" },
  { name: "Madhya Pradesh", code: "MP" },
  { name: "Maharashtra", code: "MH" },
  { name: "Manipur", code: "MN" },
  { name: "Meghalaya", code: "ML" },
  { name: "Mizoram", code: "MZ" },
  { name: "Nagaland", code: "NL" },
  { name: "Odisha", code: "OD" },
  { name: "Punjab", code: "PB" },
  { name: "Rajasthan", code: "RJ" },
  { name: "Sikkim", code: "SK" },
  { name: "Tamil Nadu", code: "TN" },
  { name: "Telangana", code: "TS" },
  { name: "Tripura", code: "TR" },
  { name: "Uttar Pradesh", code: "UP" },
  { name: "Uttarakhand", code: "UK" },
  { name: "West Bengal", code: "WB" }
];

// 14 Additional State Schemes
const ADDITIONAL_SCHEMES = [
  {
    scheme_id: "as_cmsguy_tractor",
    name: {
      en: "CMSGUY Tractor Distribution Scheme",
      te: "సీఎంఎస్‌జీయూవై ట్రాక్టర్ పంపిణీ పథకం (అస్సాం)",
      hi: "सीएमएसजीयूवाई ट्रैक्टर वितरण योजना (असम)",
      mr: "सीएमएसजीयूवाय ट्रॅक्टर वाटप योजना (आसाम)",
      ta: "சிஎம்எஸ்ஜியுவை டிராக்டர் விநியோகத் திட்டம் (அசாம்)",
      kn: "ಸಿಎಂಎಸ್‌ಜಿಯು ವೈ ಟ್ರ್ಯಾಕ್ಟರ್ ವಿತರಣಾ ಯೋಜನೆ (ಅಸ್ಸಾಂ)"
    },
    level: "State",
    state: "Assam",
    category: "machinery",
    description: {
      en: "70% capital subsidy (up to ₹5.5 Lakhs) on agricultural tractors and equipment for farmer groups and cooperatives in Assam.",
      te: "అస్సాంలోని రైతు సంఘాలు మరియు సహకార సంఘాలకు ట్రాక్టర్లు మరియు వ్యవసాయ పరికరాలపై 70% సబ్సిడీ (గరిష్టంగా ₹5.5 లక్షలు).",
      hi: "असम में किसान समूहों और सोसायटियों के लिए ट्रैक्टर व कृषि उपकरणों पर 70% सरकारी सब्सिडी (अधिकतम ₹5.5 लाख)।",
      mr: "आसाममधील शेतकरी गट आणि संस्थांसाठी ट्रॅक्टर आणि उपकरणांवर 70% सरकारी अनुदान (कमाल ₹5.5 लाख).",
      ta: "அசாமில் உள்ள விவசாயக் குழுக்களுக்கு டிராக்டர்கள் மற்றும் உபகரணங்களுக்கு 70% மானியம் (ரூ. 5.5 லட்சம் வரை).",
      kn: "ಅಸ್ಸಾಂನಲ್ಲಿ ರೈತ ಗುಂಪುಗಳಿಗೆ ಟ್ರ್ಯಾಕ್ಟರ್‌ಗಳು ಮತ್ತು ಕೃಷಿ ಉಪಕರಣಗಳ ಮೇಲೆ 70% ಸಬ್ಸಿಡಿ (ಗರಿಷ್ಠ ₹5.5 ಲಕ್ಷ)."
    },
    benefit: "70% Subsidy (Up to ₹5,50,000 on tractor package)",
    eligibility: {
      en: "Farmer groups, PACS, and small/marginal landholders with min 2.5 acres land in Assam.",
      te: "అస్సాంలో కనీసం 2.5 ఎకరాల భూమి ఉన్న రైతు సంఘాలు మరియు చిన్న/సన్నకారు రైతులు.",
      hi: "असम में न्यूनतम 2.5 एकड़ भूमि वाले किसान समूह और छोटे/सीमांत किसान।",
      mr: "आसाममध्ये किमान 2.5 एकर जमीन असलेले शेतकरी गट आणि अल्पभूधारक शेतकरी.",
      ta: "அசாமில் குறைந்தபட்சம் 2.5 ஏக்கர் நிலம் கொண்ட விவசாயக் குழுக்கள்.",
      kn: "ಅಸ್ಸಾಂನಲ್ಲಿ ಕನಿಷ್ಠ 2.5 ಎಕರೆ ಜಮೀನು ಹೊಂದಿರುವ ರೈತ ಗುಂಪುಗಳು."
    },
    criteria: {
      farmer_category: "Farmer groups, PACS & small/marginal farmers",
      landholding: "Minimum 2.5 acres cultivated land",
      crops: "All agricultural crops",
      location: "Resident of Assam",
      restrictions: "One tractor per farmer group/collective"
    },
    rules: {
      requires_land_ownership: true,
      tenant_allowed: false,
      max_land_acres: null,
      min_age: 18,
      max_age: null,
      supported_crops: null,
      state_restriction: "Assam"
    },
    documents: ["Group Resolution", "Aadhaar Card of members", "Jamabandi Land Record", "Bank Account Details"],
    deadline: "Apply seasonally via mmgys.assam.gov.in",
    claim_window: "Verification by District Agriculture Officer before release",
    source_url: "https://mmgys.assam.gov.in/",
    last_verified: "2026-09-15"
  },
  {
    scheme_id: "cg_krishi_unnati",
    name: {
      en: "Krishi Unnati Yojana (Paddy ₹3,100 Support)",
      te: "కృషి ఉన్నతి యోజన (వరి ₹3,100 మద్దతు - ఛత్తీస్‌గఢ్)",
      hi: "कृषि उन्नति योजना (धान ₹3,100 समर्थन - छत्तीसगढ़)",
      mr: "कृषी उन्नती योजना (भात ₹3,100 हमीभाव मदत - छत्तीसगड)",
      ta: "கிருஷி உன்னதி திட்டம் (நெல் ₹3,100 ஆதரவு - சத்தீஸ்கர்)",
      kn: "ಕೃಷಿ ಉನ್ನತಿ ಯೋಜನೆ (ಭತ್ತ ₹3,100 ಬೆಂಬಲ - ಛತ್ತೀಸ್‌ಗಢ)"
    },
    level: "State",
    state: "Chhattisgarh",
    category: "income_support",
    description: {
      en: "Assures ₹3,100 per quintal for paddy procurement via direct DBT differential payment (up to ₹10,000/acre input assistance) for Chhattisgarh farmers.",
      te: "ఛత్తీస్‌గఢ్ రైతులకు వరి సేకరణలో క్వింటాలుకు ₹3,100 ధర లభించేలా DBT ద్వారా ఎకరాకు సుమారు ₹10,000 వరకు ఇన్‌పుట్ సాయం.",
      hi: "छत्तीसगढ़ के किसानों को धान उपार्जन पर ₹3,100 प्रति क्विंटल का सुनिश्चित मूल्य (लगभग ₹10,000/एकड़ इनपुट सहायता डीबीटी)।",
      mr: "छत्तीसगडच्या शेतकऱ्यांना भात खरेदीवर ₹3,100 हमीभाव आणि थेट बँक खात्यात इनपुट अनुदान.",
      ta: "சத்தீஸ்கர் விவசாயிகளுக்கு நெல் கொள்முதலில் குவிண்டாலுக்கு ₹3,100 உறுதி செய்யும் நேரடி நிதி உதவி.",
      kn: "ಛತ್ತೀಸ್‌ಗಢದ ರೈತರಿಗೆ ಭತ್ತ ಖರೀದಿಯಲ್ಲಿ ಕ್ವಿಂಟಾಲ್‌ಗೆ ₹3,100 ಖಚಿತಪಡಿಸುವ ಡಿಬಿಟಿ ಇನ್‌ಪುಟ್ ನೆರವು."
    },
    benefit: "₹3,100 / quintal realized price (DBT differential payment)",
    eligibility: {
      en: "All paddy cultivating farmers registered on Chhattisgarh Unified Farmer Portal.",
      te: "ఛత్తీస్‌గఢ్ కిసాన్ పోర్టల్‌లో నమోదైన వరి సాగుదారులు.",
      hi: "छत्तीसगढ़ एकीकृत किसान पोर्टल पर पंजीकृत सभी धान उत्पादक किसान।",
      mr: "छत्तीसगड शेतकरी पोर्टलवर नोंदणीकृत सर्व भात उत्पादक शेतकरी.",
      ta: "சத்தீஸ்கர் போர்ட்டலில் பதிவு செய்த அனைத்து நெல் விவசாயிகள்.",
      kn: "ಛತ್ತೀಸ್‌ಗಢ ಕಿಸಾನ್ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನೋಂದಾಯಿಸಿದ ಎಲ್ಲಾ ಭತ್ತದ ರೈತರು."
    },
    criteria: {
      farmer_category: "All registered farmers growing paddy (landowners & tenant farmers)",
      landholding: "Up to 21 quintals/acre procurement limit",
      crops: "Paddy",
      location: "Resident of Chhattisgarh",
      restrictions: "Must be registered on kisan.cg.nic.in before harvest"
    },
    rules: {
      requires_land_ownership: false,
      tenant_allowed: true,
      max_land_acres: null,
      min_age: 18,
      max_age: null,
      supported_crops: ["Paddy"],
      state_restriction: "Chhattisgarh"
    },
    documents: ["Aadhaar Card", "Khasra B1/P2 Passbook", "Bank Account with IFSC", "Paddy Sowing Token"],
    deadline: "Procurement season: 1st Nov - 31st Jan annually",
    claim_window: "Direct payment to bank account within 72 hours of mandi procurement",
    source_url: "https://kisan.cg.nic.in/",
    last_verified: "2026-10-18"
  },
  {
    scheme_id: "jh_fasal_rahat",
    name: {
      en: "Jharkhand Rajya Fasal Rahat Yojana (JRFRY)",
      te: "జార్ఖండ్ రాజ్య ఫసల్ రాహత్ యోజన (ఉచిత పంట నష్ట పరిహారం)",
      hi: "झारखंड राज्य फसल राहत योजना (जेआरएफआरवाई)",
      mr: "झारखंड राज्य पीक मदत योजना (मोफत पीक नुकसान भरपाई)",
      ta: "ஜார்கண்ட் மாநில பயிர் நிவாரணத் திட்டம்",
      kn: "ಜಾರ್ಖಂಡ್ ರಾಜ್ಯ ಬೆಳೆ ಪರಿಹಾರ ಯೋಜನೆ"
    },
    level: "State",
    state: "Jharkhand",
    category: "insurance",
    description: {
      en: "Free compensation of ₹3,000/acre (30-50% crop loss) to ₹4,000/acre (>50% loss) for drought and localized crop damage without any farmer premium.",
      te: "కరువు మరియు పంట నష్టానికి రైతు ప్రీమియం లేకుండా ఎకరాకు ₹3,000 నుండి ₹4,000 వరకు ఉచిత ఆర్థిక సాయం.",
      hi: "सूखा और फसल नुकसान पर किसानों को बिना किसी प्रीमियम के ₹3,000 से ₹4,000 प्रति एकड़ की मुफ्त राहत सहायता।",
      mr: "दुष्काळ व पीक नुकसानीसाठी कोणत्याही हप्त्याशिवाय ₹3,000 ते ₹4,000 प्रति एकर मोफत मदत.",
      ta: "வறட்சி மற்றும் பயிர் இழப்பிற்கு விவசாயி கட்டணம் இல்லாமல் ஏக்கருக்கு ₹3,000 முதல் ₹4,000 வரை இலவச இழப்பீடு.",
      kn: "ಬರ ಮತ್ತು ಬೆಳೆ ಹಾನಿಗೆ ಯಾವುದೇ ಪ್ರೀಮಿಯಂ ಇಲ್ಲದೆ ಎಕರೆಗೆ ₹3,000 ದಿಂದ ₹4,000 ವರೆಗೆ ಉಚಿತ ಪರಿಹಾರ."
    },
    benefit: "₹3,000 to ₹4,000 / acre free compensation for crop damage",
    eligibility: {
      en: "All landowning and tenant farmers cultivating land in Jharkhand.",
      te: "జార్ఖండ్‌లో సాగుచేసే భూ యజమానులు మరియు కౌలు రైతులందరూ.",
      hi: "झारखंड में खेती करने वाले सभी रैयत और गैर-रैयत (बटाईदार) किसान।",
      mr: "झारखंडमधील सर्व जमीन मालक आणि कुळ शेतकरी.",
      ta: "ஜார்கண்டில் பயிரிடும் அனைத்து நில உரிமையாளர்கள் மற்றும் குத்தகைதாரர்கள்.",
      kn: "ಜಾರ್ಖಂಡ್‌ನಲ್ಲಿ ಕೃಷಿ ಮಾಡುವ ಎಲ್ಲಾ ಭೂಮಾಲೀಕರು ಮತ್ತು ಗೇಣಿದಾರರು."
    },
    criteria: {
      farmer_category: "Landowning (Raiyat) and tenant (Non-Raiyat) farmers",
      landholding: "1 to 5 acres covered for assistance",
      crops: "Paddy, Maize",
      location: "Resident of Jharkhand",
      restrictions: "Free enrollment; compensation triggered on crop loss verification"
    },
    rules: {
      requires_land_ownership: false,
      tenant_allowed: true,
      max_land_acres: 5,
      min_age: 18,
      max_age: null,
      supported_crops: ["Paddy", "Maize"],
      state_restriction: "Jharkhand"
    },
    documents: ["Aadhaar Card", "Land Possession Certificate (LPC) or Vamsawali/Tenant Affidavit", "Bank Passbook"],
    deadline: "Enrollment cut-off: 15th September annually on jrfry.jharkhand.gov.in",
    claim_window: "Assessment via satellite and mobile crop cut survey",
    source_url: "https://jrfry.jharkhand.gov.in/",
    last_verified: "2026-09-22"
  },
  {
    scheme_id: "hp_prakritik_kheti",
    name: {
      en: "Prakritik Kheti Khushhal Kisan Yojana (PK3Y)",
      te: "ప్రాకృతిక ఖేతీ ఖుషాల్ కిసాన్ యోజన (హిమాచల్ ప్రదేశ్)",
      hi: "प्राकृतिक खेती खुशहाल किसान योजना (पीके3वाई - हिमाचल)",
      mr: "प्राकृतिक शेती खुशहाल शेतकरी योजना (हिमाचल प्रदेश)",
      ta: "இயற்கை வேளாண்மை திட்டம் (இமாச்சல பிரதேசம்)",
      kn: "ಪ್ರಾಕೃತಿಕ ಕೃಷಿ ಖುಷಾಲ್ ಕಿಸಾನ್ ಯೋಜನೆ (ಹಿಮಾಚಲ ಪ್ರದೇಶ)"
    },
    level: "State",
    state: "Himachal Pradesh",
    category: "income_support",
    description: {
      en: "Provides ₹25,000 subsidy on indigenous cow purchase, ₹5,000 for drums and input preparation, promoting chemical-free natural farming across Himachal.",
      te: "దేశీ ఆవు కొనుగోలుకు ₹25,000 సబ్సిడీ మరియు సహజ వ్యవసాయ ఇన్పుట్ల తయారీకి ఉచిత కిట్ అందించే హిమాచల్ ప్రదేశ్ పథకం.",
      hi: "देसी गाय की खरीद पर ₹25,000 की सब्सिडी और प्राकृतिक खेती इनपुट तैयार करने के लिए ₹5,000 की किट।",
      mr: "देशी गाय खरेदीवर ₹25,000 अनुदान आणि नैसर्गिक शेतीसाठी मोफत साहित्य किट.",
      ta: "நாட்டுப் பசு வாங்குவதற்கு ₹25,000 மானியம் மற்றும் இயற்கை விவசாய இடுபொருள் தயாரிப்பு உதவி.",
      kn: "ನಾಟಿ ಹಸು ಖರೀದಿಗೆ ₹25,000 ಸಬ್ಸಿಡಿ ಮತ್ತು ನೈಸರ್ಗಿಕ ಕೃಷಿ ಕಿಟ್ ನೆರವು."
    },
    benefit: "₹25,000 cow subsidy + ₹5,000 natural farming inputs",
    eligibility: {
      en: "All farmers practicing or adopting natural farming in Himachal Pradesh.",
      te: "హిమాచల్ ప్రదేశ్‌లో సహజ వ్యవసాయం చేసే రైతులందరూ.",
      hi: "हिमाचल प्रदेश में प्राकृतिक खेती अपनाने वाले सभी किसान।",
      mr: "हिमाचल प्रदेशातील नैसर्गिक शेती करणारे सर्व शेतकरी.",
      ta: "இமாச்சல பிரதேசத்தில் இயற்கை விவசாயம் செய்யும் அனைத்து விவசாயிகள்.",
      kn: "ಹಿಮಾಚಲ ಪ್ರದೇಶದಲ್ಲಿ ನೈಸರ್ಗಿಕ ಕೃಷಿ ಮಾಡುವ ಎಲ್ಲಾ ರೈತರು."
    },
    criteria: {
      farmer_category: "All small, marginal and progressive farmers",
      landholding: "No upper ceiling",
      crops: "Apple, Maize, Wheat, Vegetables",
      location: "Resident of Himachal Pradesh",
      restrictions: "Must undergo 3-day Subhash Palekar Natural Farming training"
    },
    rules: {
      requires_land_ownership: true,
      tenant_allowed: true,
      max_land_acres: null,
      min_age: 18,
      max_age: null,
      supported_crops: null,
      state_restriction: "Himachal Pradesh"
    },
    documents: ["Aadhaar Card", "Bonafide Himachali Certificate", "Land Revenue Record", "Bank Passbook"],
    deadline: "Continuous registration via spnfhp.nic.in",
    claim_window: "Verification by Block Technology Manager (ATMA)",
    source_url: "https://spnfhp.nic.in/",
    last_verified: "2026-10-02"
  },
  {
    scheme_id: "uk_kisan_kalyan",
    name: {
      en: "Pt. Deen Dayal Upadhyaya Kisan Kalyan Yojana (0% Loan)",
      te: "దీన్ దయాళ్ ఉపాధ్యాయ కిసాన్ కళ్యాణ్ యోజన (0% వడ్డీ రుణం - ఉత్తరాఖండ్)",
      hi: "पं. दीन दयाल उपाध्याय किसान कल्याण योजना (0% ब्याज ऋण - उत्तराखंड)",
      mr: "दीन दयाल उपाध्याय शेतकरी कल्याण योजना (0% व्याज कर्ज - उत्तराखंड)",
      ta: "தீன் தயாள் உபாத்யாயா உழவர் நலத் திட்டம் (0% வட்டி கடன் - உத்தரகண்ட்)",
      kn: "ದೀನ್ ದಯಾಳ್ ಉಪಾಧ್ಯಾಯ ರೈತ ಕಲ್ಯಾಣ ಯೋಜನೆ (0% ಬಡ್ಡಿ ಸಾಲ - ಉತ್ತರಾಖಂಡ)"
    },
    level: "State",
    state: "Uttarakhand",
    category: "credit",
    description: {
      en: "0% interest short-term crop loans up to ₹3,00,000 for individual farmers and ₹5,00,000 for SHGs to eliminate private moneylender debt in Uttarakhand.",
      te: "ఉత్తరాఖండ్‌లోని రైతులకు ₹3,00,000 వరకు మరియు స్వయం సహాయక సంఘాలకు ₹5,00,000 వరకు సున్నా శాతం వడ్డీకే స్వల్పకాలిక వ్యవసాయ రుణాలు.",
      hi: "उत्तराखंड के किसानों को ₹3 लाख तक और स्वयं सहायता समूहों को ₹5 लाख तक का पूर्णतः 0% ब्याज मुक्त फसली ऋण।",
      mr: "उत्तराखंडमधील शेतकऱ्यांना ₹3 लाख आणि बचत गटांना ₹5 लाखांपर्यंत 0% व्याजदराने पीक कर्ज.",
      ta: "உத்தரகண்ட் விவசாயிகளுக்கு ₹3 லட்சம் வரை 0% வட்டியில் குறுகிய கால பயிர் கடன்.",
      kn: "ಉತ್ತರಾಖಂಡದ ರೈತರಿಗೆ ₹3 ಲಕ್ಷದವರೆಗೆ ಸಂಪೂರ್ಣ 0% ಬಡ್ಡಿದರದಲ್ಲಿ ಕೃಷಿ ಸಾಲ."
    },
    benefit: "0% Interest (Interest-Free) Crop Loan up to ₹3,00,000",
    eligibility: {
      en: "Small, marginal and hill terrain farmers cultivating land in Uttarakhand.",
      te: "ఉత్తరాఖండ్‌లోని చిన్న, సన్నకారు మరియు కొండ ప్రాంత రైతులు.",
      hi: "उत्तराखंड के छोटे, सीमांत एवं पर्वतीय क्षेत्रों के किसान।",
      mr: "उत्तराखंडमधील लहान, सीमांत आणि डोंगरी भागातील शेतकरी.",
      ta: "உத்தரகண்ட் மாநில சிறு மற்றும் குறு விவசாயிகள்.",
      kn: "ಉತ್ತರಾಖಂಡದ ಸಣ್ಣ ಮತ್ತು ಅತಿ ಸಣ್ಣ ರೈತರು."
    },
    criteria: {
      farmer_category: "Small, marginal and hill terrain farmers",
      landholding: "No ceiling",
      crops: "All agricultural and horticultural crops",
      location: "Resident of Uttarakhand",
      restrictions: "Loan must be repaid within 1 year for 0% interest benefit"
    },
    rules: {
      requires_land_ownership: true,
      tenant_allowed: false,
      max_land_acres: null,
      min_age: 18,
      max_age: 70,
      supported_crops: null,
      state_restriction: "Uttarakhand"
    },
    documents: ["Aadhaar Card", "Khatoni (Land Record)", "Domicile Certificate", "Bank Account Details"],
    deadline: "Available through District Cooperative Banks and PACS year-round",
    claim_window: "Annual renewal upon 100% timely repayment",
    source_url: "https://cooperative.uk.gov.in/",
    last_verified: "2026-08-30"
  },
  {
    scheme_id: "ga_shetkari_samruddhi",
    name: {
      en: "Goa Assured Price & Farm Mechanisation Scheme",
      te: "గోవా హామీ ధర మరియు వ్యవసాయ యంత్రీకరణ పథకం",
      hi: "गोवा सुनिश्चित मूल्य एवं कृषि यांत्रिकीकरण योजना",
      mr: "गोवा हमीभाव व कृषी यांत्रिकीकरण योजना (शेतकरी समृद्धी)",
      ta: "கோவா விலை உத்தரவாதம் மற்றும் பண்ணை இயந்திரமயமாக்கல் திட்டம்",
      kn: "ಗೋವಾ ಖಚಿತ ಬೆಲೆ ಮತ್ತು ಕೃಷಿ ಯಾಂತ್ರೀಕರಣ ಯೋಜನೆ"
    },
    level: "State",
    state: "Goa",
    category: "machinery",
    description: {
      en: "Provides 50% to 75% subsidy on power tillers and harvesters, plus assured minimum prices for traditional paddy, cashew, and coconut farmers in Goa.",
      te: "గోవాలోని వరి, జీడిమామిడి మరియు కొబ్బరి రైతులకు వ్యవసాయ యంత్రాలపై 50% నుండి 75% సబ్సిడీ మరియు గిట్టుబాటు ధర సహాయం.",
      hi: "गोवा के किसानों को पावर टिलर, हार्वेस्टर पर 50% से 75% सब्सिडी और धान व काजू के लिए सुनिश्चित मूल्य सहायता।",
      mr: "गोव्यातील शेतकऱ्यांना पॉवर टिलर, हार्वेस्टरवर 50% ते 75% अनुदान आणि भात व काजूला हमीभाव मदत.",
      ta: "கோவாவில் பவர் டில்லர்கள் மற்றும் அறுவடை இயந்திரங்களுக்கு 50% முதல் 75% வரை மானியம்.",
      kn: "ಗೋವಾದಲ್ಲಿ ಪವರ್ ಟಿಲ್ಲರ್ ಮತ್ತು ಯಂತ್ರೋಪಕರಣಗಳಿಗೆ 50% ರಿಂದ 75% ಸಬ್ಸಿಡಿ."
    },
    benefit: "50% - 75% Subsidy on machinery + Assured price top-up",
    eligibility: {
      en: "Goan farmers possessing a valid Krishi Card.",
      te: "చెల్లుబాటు అయ్యే కృషి కార్డు ఉన్న గోవా రైతులు.",
      hi: "वैध कृषि कार्ड धारक गोवा के सभी किसान।",
      mr: "वैध कृषी कार्डधारक गोव्यातील सर्व शेतकरी.",
      ta: "செல்லுபடியாகும் கிருஷி அட்டை வைத்துள்ள கோவா விவசாயிகள்.",
      kn: "ಮಾನ್ಯ ಕೃಷಿ ಕಾರ್ಡ್ ಹೊಂದಿರುವ ಗೋವಾದ ರೈತರು."
    },
    criteria: {
      farmer_category: "Krishi Card holding farmers and tenant cultivators (Mundkars)",
      landholding: "No limit",
      crops: "Paddy, Cashew, Coconut, Arecanut",
      location: "Resident of Goa",
      restrictions: "Valid Krishi Card issued by Goa Agri Dept mandatory"
    },
    rules: {
      requires_land_ownership: false,
      tenant_allowed: true,
      max_land_acres: null,
      min_age: 18,
      max_age: null,
      supported_crops: null,
      state_restriction: "Goa"
    },
    documents: ["Krishi Card", "Aadhaar Card", "Land Form I & XIV / Mundkar certificate", "Bank Passbook"],
    deadline: "Apply via agri.goa.gov.in portal",
    claim_window: "Zonal Agriculture Office (ZAO) inspection within 3 weeks",
    source_url: "https://agri.goa.gov.in/",
    last_verified: "2026-09-08"
  },
  {
    scheme_id: "sk_organic_incentive",
    name: {
      en: "Sikkim Organic Production Incentive Scheme",
      te: "సిక్కిం సేంద్రీయ ఉత్పత్తి ప్రోత్సాహక పథకం",
      hi: "सिक्किम जैविक उत्पादन प्रोत्साहन योजना",
      mr: "सिक्कीम सेंद्रिय उत्पादन प्रोत्साहन योजना",
      ta: "சிக்கிம் இயற்கை உற்பத்தி ஊக்கத்தொகை திட்டம்",
      kn: "ಸಿಕ್ಕಿಂ ಸಾವಯವ ಉತ್ಪಾದನಾ ಪ್ರೋತ್ಸಾಹಕ ಯೋಜನೆ"
    },
    level: "State",
    state: "Sikkim",
    category: "income_support",
    description: {
      en: "Direct DBT production incentive of ₹10,000 per hectare for certified organic cultivation of large cardamom, ginger, turmeric, and buckwheat in Sikkim.",
      te: "సిక్కింలో సేంద్రీయ పెద్ద ఏలకులు, అల్లం, పసుపు సాగుచేసే రైతులకు హెక్టారుకు ₹10,000 ప్రత్యక్ష డీబీటీ ప్రోత్సాహకం.",
      hi: "सिक्किम में बड़ी इलायची, अदरक, हल्दी और कूटू की जैविक खेती के लिए ₹10,000 प्रति हेक्टेयर का सीधा डीबीटी प्रोत्साहन।",
      mr: "सिक्कीममध्ये वेलची, आले आणि हळदीच्या सेंद्रिय शेतीसाठी ₹10,000 प्रति हेक्टर थेट अनुदान.",
      ta: "சிக்கிமில் இயற்கை ஏலக்காய், இஞ்சி மற்றும் மஞ்சள் பயிரிடும் விவசாயிகளுக்கு ஹெக்டேருக்கு ₹10,000 நேரடி உதவி.",
      kn: "ಸಿಕ್ಕಿಂನಲ್ಲಿ ಸಾವಯವ ಏಲಕ್ಕಿ, ಶುಂಠಿ ಮತ್ತು ಅರಿಶಿನ ಬೆಳೆಯುವ ರೈತರಿಗೆ ಹೆಕ್ಟೇರ್‌ಗೆ ₹10,000 ಡಿಬಿಟಿ ಪ್ರೋತ್ಸಾಹ ಧನ."
    },
    benefit: "₹10,000 / hectare DBT incentive for certified organic crops",
    eligibility: {
      en: "Certified organic farmers registered with Sikkim Organic Mission.",
      te: "సిక్కిం ఆర్గానిక్ మిషన్‌లో నమోదైన ధృవీకృత సేంద్రీయ రైతులు.",
      hi: "सिक्किम ऑर्गेनिक मिशन के तहत पंजीकृत प्रमाणित जैविक किसान।",
      mr: "सिक्कीम ऑरगॅनिक मिशन अंतर्गत नोंदणीकृत प्रमाणित सेंद्रिय शेतकरी.",
      ta: "சிக்கிம் ஆர்கானிக் மிஷனில் பதிவு செய்த இயற்கை விவசாயிகள்.",
      kn: "ಸಿಕ್ಕಿಂ ಆರ್ಗ್ಯಾನಿಕ್ ಮಿಷನ್‌ನಲ್ಲಿ ನೋಂದಾಯಿಸಿದ ಪ್ರಮಾಣೀಕೃತ ಸಾವಯವ ರೈತರು."
    },
    criteria: {
      farmer_category: "All certified organic farmers",
      landholding: "Up to 5 hectares per farmer",
      crops: "Cardamom, Ginger, Turmeric, Buckwheat, Orange",
      location: "Resident of Sikkim",
      restrictions: "100% organic certification mandatory"
    },
    rules: {
      requires_land_ownership: true,
      tenant_allowed: true,
      max_land_acres: 12.5,
      min_age: 18,
      max_age: null,
      supported_crops: ["Cardamom", "Ginger", "Turmeric", "Buckwheat", "Orange"],
      state_restriction: "Sikkim"
    },
    documents: ["Sikkim Subject / COI", "Aadhaar Card", "Organic Scope Certificate", "Bank Details"],
    deadline: "Annual application through Horticulture Department, Gangtok",
    claim_window: "Direct bank credit upon yield verification by Field Inspector",
    source_url: "https://sikkim.gov.in/",
    last_verified: "2026-08-28"
  },
  {
    scheme_id: "tr_mukhyamantri_fasal_bima",
    name: {
      en: "Tripura Mukhyamantri Fasal Bima Sahayata",
      te: "త్రిపుర ముఖ్యమంత్రి ఫసల్ బీమా సహాయత (100% ఉచిత బీమా)",
      hi: "त्रिपुरा मुख्यमंत्री फसल बीमा सहायता (100% मुफ्त फसल बीमा)",
      mr: "त्रिपुरा मुख्यमंत्री पीक विमा सहाय्यता (100% मोफत पीक विमा)",
      ta: "திரிபுரா முதலமைச்சர் பயிர் காப்பீட்டு உதவி (100% இலவச காப்பீடு)",
      kn: "ತ್ರಿಪುರ ಮುಖ್ಯಮಂತ್ರಿ ಬೆಳೆ ವಿಮೆ ಸಹಾಯತಾ (100% ಉಚಿತ ಬೆಳೆ ವಿಮೆ)"
    },
    level: "State",
    state: "Tripura",
    category: "insurance",
    description: {
      en: "Tripura state government pays 100% of the farmer's premium share for paddy and maize, providing zero-cost comprehensive crop insurance.",
      te: "త్రిపుర ప్రభుత్వం వరి మరియు మొక్కజొన్న రైతులకు ప్రీమియం వాటాను 100% తానే చెల్లించి ఉచిత పంట బీమా కల్పిస్తుంది.",
      hi: "त्रिपुरा सरकार किसानों की ओर से 100% प्रीमियम वहन कर धान और मक्का के लिए पूर्णतः निःशुल्क फसल बीमा प्रदान करती है।",
      mr: "त्रिपुरा सरकार शेतकऱ्यांचा 100% हप्ता स्वतः भरून भात व मक्यासाठी मोफत पीक विमा संरक्षण देते.",
      ta: "திரிபுரா அரசு விவசாயிகளின் முழு காப்பீட்டுத் தொகையையும் செலுத்தி 100% இலவச பயிர் காப்பீடு வழங்குகிறது.",
      kn: "ತ್ರಿಪುರಾ ಸರ್ಕಾರವು ರೈತರ ಸಂಪೂರ್ಣ ಪ್ರೀಮಿಯಂ ಭರಿಸಿ ಭತ್ತ ಮತ್ತು ಮೆಕ್ಕೆಜೋಳಕ್ಕೆ 100% ಉಚಿತ ಬೆಳೆ ವಿಮೆ ನೀಡುತ್ತದೆ."
    },
    benefit: "100% Free Crop Insurance (State bears entire farmer premium)",
    eligibility: {
      en: "All paddy and maize cultivating farmers in Tripura.",
      te: "త్రిపురలో వరి మరియు మొక్కజొన్న సాగుచేసే రైతులందరూ.",
      hi: "त्रिपुरा में धान और मक्का उगाने वाले सभी किसान।",
      mr: "त्रिपुरातील भात आणि मका घेणारे सर्व शेतकरी.",
      ta: "திரிபுராவில் நெல் மற்றும் மக்காச்சோளம் பயிரிடும் அனைத்து விவசாயிகள்.",
      kn: "ತ್ರಿಪುರಾದಲ್ಲಿ ಭತ್ತ ಮತ್ತು ಮೆಕ್ಕೆಜೋಳ ಬೆಳೆಯುವ ಎಲ್ಲಾ ರೈತರು."
    },
    criteria: {
      farmer_category: "Landowners and sharecroppers",
      landholding: "No ceiling",
      crops: "Paddy, Maize",
      location: "Resident of Tripura",
      restrictions: "Sowing declaration certified by Village Panchayat Secretary"
    },
    rules: {
      requires_land_ownership: false,
      tenant_allowed: true,
      max_land_acres: null,
      min_age: 18,
      max_age: null,
      supported_crops: ["Paddy", "Maize"],
      state_restriction: "Tripura"
    },
    documents: ["Aadhaar Card", "Khatian or Sharecropper Sowing Certificate", "Bank Passbook"],
    deadline: "Kharif cut-off: 31st July / Rabi cut-off: 31st December",
    claim_window: "Report localized calamity within 72 hours via toll-free helpline",
    source_url: "https://agri.tripura.gov.in/",
    last_verified: "2026-09-19"
  },
  {
    scheme_id: "mn_mission_organic",
    name: {
      en: "Manipur Mission Organic Development Scheme (MMODA)",
      te: "మణిపూర్ మిషన్ ఆర్గానిక్ డెవలప్‌మెంట్ స్కీమ్ (సహజ ఎరువులు & సబ్సిడీ)",
      hi: "मणिपुर मिशन ऑर्गेनिक डेवलपमेंट स्कीम (एमएमओडीए)",
      mr: "मणिपूर मिशन ऑरगॅनिक डेव्हलपमेंट योजना",
      ta: "மணிப்பூர் இயற்கை வேளாண்மை மேம்பாட்டுத் திட்டம்",
      kn: "ಮಣಿಪುರ ಮಿಷನ್ ಸಾವಯವ ಅಭಿವೃದ್ಧಿ ಯೋಜನೆ"
    },
    level: "State",
    state: "Manipur",
    category: "income_support",
    description: {
      en: "Provides ₹11,200 per hectare for organic inputs, seeds, bio-fertilizers, and free organic certification for hill and valley farmers in Manipur.",
      te: "మణిపూర్‌లోని కొండ మరియు లోయ ప్రాంత రైతులకు సేంద్రీయ విత్తనాలు, ఎరువులు మరియు ఉచిత ధృవీకరణ కోసం హెక్టారుకు ₹11,200 సాయం.",
      hi: "मणिपुर के किसानों को जैविक बीज, जैव-उर्वरक और निःशुल्क प्रमाणन के लिए ₹11,200 प्रति हेक्टेयर की सहायता।",
      mr: "मणिपूरमधील शेतकऱ्यांना सेंद्रिय खते, बियाणे आणि प्रमाणपत्रासाठी ₹11,200 प्रति हेक्टर मदत.",
      ta: "மணிப்பூர் விவசாயிகளுக்கு இயற்கை விதைகள் மற்றும் உரங்களுக்காக ஹெக்டேருக்கு ₹11,200 உதவித்தொகை.",
      kn: "ಮಣಿಪುರದ ರೈತರಿಗೆ ಸಾವಯವ ಬೀಜಗಳು ಮತ್ತು ಗೊಬ್ಬರಗಳಿಗಾಗಿ ಹೆಕ್ಟೇರ್‌ಗೆ ₹11,200 ನೆರವು."
    },
    benefit: "₹11,200 / hectare financial grant for organic inputs",
    eligibility: {
      en: "Hill and valley farmers practicing organic agriculture in Manipur.",
      te: "మణిపూర్‌లో సేంద్రీయ వ్యవసాయం చేసే కొండ మరియు లోయ ప్రాంత రైతులు.",
      hi: "मणिपुर में जैविक खेती करने वाले पर्वतीय एवं घाटी के किसान।",
      mr: "मणिपूरमधील सेंद्रिय शेती करणारे सर्व शेतकरी.",
      ta: "மணிப்பூரில் இயற்கை விவசாயம் செய்யும் விவசாயிகள்.",
      kn: "ಮಣಿಪುರದಲ್ಲಿ ಸಾವಯವ ಕೃಷಿ ಮಾಡುವ ರೈತರು."
    },
    criteria: {
      farmer_category: "All hill and valley cultivators",
      landholding: "Minimum 1 acre",
      crops: "Chak-Hao (Black Rice), Pineapple, Ginger, King Chilli",
      location: "Resident of Manipur",
      restrictions: "Must register with MMODA farmer cluster"
    },
    rules: {
      requires_land_ownership: false,
      tenant_allowed: true,
      max_land_acres: null,
      min_age: 18,
      max_age: null,
      supported_crops: null,
      state_restriction: "Manipur"
    },
    documents: ["Aadhaar Card", "Village Authority Land Certificate", "Bank Passbook"],
    deadline: "Enrollment via District Agriculture Officer",
    claim_window: "Direct DBT upon inspection of organic plot",
    source_url: "https://manipur.gov.in/",
    last_verified: "2026-09-04"
  },
  {
    scheme_id: "ml_focus_farmers",
    name: {
      en: "Meghalaya FOCUS (Farmers' Collectives Scheme)",
      te: "మేఘాలయ ఫోకస్ రైతు సంఘాల పథకం (రూ. 5,000 నగదు గ్రాంట్)",
      hi: "मेघालय फोकस योजना (किसान उत्पादक समूह अनुदान - ₹5,000)",
      mr: "मेघालय फोकस शेतकरी उत्पादक गट योजना (₹5,000 थेट मदत)",
      ta: "மேகாலயா ஃபோகஸ் உழவர் உற்பத்தியாளர் குழு திட்டம் (ரூ. 5,000 மானியம்)",
      kn: "ಮೇಘಾಲಯ ಫೋಕಸ್ ರೈತ ಉತ್ಪಾದಕರ ಗುಂಪು ಯೋಜನೆ (₹5,000 ನೇರ ಅನುದಾನ)"
    },
    level: "State",
    state: "Meghalaya",
    category: "income_support",
    description: {
      en: "Direct financial grant of ₹5,000 per producer household (up to ₹1,00,000 per Producer Group) for working capital, inputs, and post-harvest machinery in Meghalaya.",
      te: "మేఘాలయలోని ప్రతి రైతు కుటుంబానికి ₹5,000 (రైతు సంఘానికి ₹1 లక్ష వరకు) వర్కింగ్ క్యాపిటల్ మరియు యంత్రాల కోసం ప్రత్యక్ష నగదు గ్రాంట్.",
      hi: "मेघालय में प्रत्येक कृषक परिवार को ₹5,000 (प्रत्येक उत्पादक समूह को ₹1 लाख तक) का सीधा वित्तीय अनुदान।",
      mr: "मेघालयमधील प्रत्येक शेतकरी कुटुंबाला ₹5,000 थेट आर्थिक मदत.",
      ta: "மேகாலயாவில் உள்ள ஒவ்வொரு விவசாய குடும்பத்திற்கும் ₹5,000 நேரடி பண உதவி.",
      kn: "ಮೇಘಾಲಯದ ಪ್ರತಿಯೊಂದು ರೈತ ಕುಟುಂಬಕ್ಕೆ ₹5,000 ನೇರ ಆರ್ಥಿಕ ಅನುದಾನ."
    },
    benefit: "₹5,000 direct cash grant per farming household",
    eligibility: {
      en: "Rural farming households organized into Producer Groups (PGs) in Meghalaya.",
      te: "మేఘాలయలో ప్రొడ్యూసర్ గ్రూపులుగా ఏర్పడిన గ్రామీణ రైతు కుటుంబాలు.",
      hi: "मेघालय में उत्पादक समूहों (पीजी) में संगठित ग्रामीण किसान परिवार।",
      mr: "मेघालयमधील उत्पादक गटांचे सदस्य असणारे शेतकरी.",
      ta: "மேகாலயாவில் உற்பத்தியாளர் குழுக்களில் உள்ள கிராமப்புற விவசாயிகள்.",
      kn: "ಮೇಘಾಲಯದ ಉತ್ಪಾದಕರ ಗುಂಪುಗಳಲ್ಲಿರುವ ರೈತ ಕುಟುಂಬಗಳು."
    },
    criteria: {
      farmer_category: "All farming households in producer groups",
      landholding: "No land size requirement",
      crops: "Ginger, Turmeric, Broomstick, Black Pepper, Vegetables",
      location: "Resident of Meghalaya",
      restrictions: "Must be a registered member of a 10-20 farmer Producer Group"
    },
    rules: {
      requires_land_ownership: false,
      tenant_allowed: true,
      max_land_acres: null,
      min_age: 18,
      max_age: null,
      supported_crops: null,
      state_restriction: "Meghalaya"
    },
    documents: ["Aadhaar Card", "Epic Card", "Producer Group Bank Account", "PG Membership List"],
    deadline: "Continuous enrollment through Basin Development Authority (MBDA)",
    claim_window: "Direct transfer into Producer Group account",
    source_url: "https://focus.meghalaya.gov.in/",
    last_verified: "2026-10-12"
  },
  {
    scheme_id: "mz_bana_chhuan",
    name: {
      en: "Mizoram Bana Chhuan (Agri Hand-Holding Scheme)",
      te: "మిజోరం బనా చువాన్ (రైతు చేయూత పథకం)",
      hi: "मिजोरम बना छुआन (कृषि हैंड-होल्डिंग योजना)",
      mr: "मिझोरम बना छुआन (शेतकरी आधार योजना)",
      ta: "மிசோரம் பனா சுவான் (விவசாய கை கொடுக்கும் திட்டம்)",
      kn: "ಮಿಜೋರಾಂ ಬನಾ ಚುವಾನ್ (ರೈತ ಬೆಂಬಲ ಯೋಜನೆ)"
    },
    level: "State",
    state: "Mizoram",
    category: "income_support",
    description: {
      en: "Comprehensive financial assistance of ₹10,000 - ₹50,000 per farmer for oil palm, ginger, turmeric, and settled agriculture to replace jhum shifting cultivation.",
      te: "పోడు వ్యవసాయం మాని శాశ్వత సాగు చేసే మిజోరం రైతులకు ఆయిల్ పామ్, అల్లం మరియు పసుపు సాగు కోసం ₹10,000 నుండి ₹50,000 ఆర్థిక సాయం.",
      hi: "झूम खेती के स्थान पर स्थायी खेती, पाम ऑयल, अदरक और हल्दी की खेती के लिए ₹10,000 से ₹50,000 की वित्तीय सहायता।",
      mr: "मिझोरममधील शेतकऱ्यांना पाम तेल, आले आणि हळदीच्या शेतीसाठी ₹10,000 ते ₹50,000 आर्थिक मदत.",
      ta: "மிசோரமில் ஆயில் பாம், இஞ்சி மற்றும் மஞ்சள் பயிரிடும் விவசாயிகளுக்கு ₹10,000 முதல் ₹50,000 வரை நிதி உதவி.",
      kn: "ಮಿಜೋರಾಂನಲ್ಲಿ ಆಯಿಲ್ ಪಾಮ್, ಶುಂಠಿ ಮತ್ತು ಅರಿಶಿನ ಬೆಳೆಯುವ ರೈತರಿಗೆ ₹10,000 ದಿಂದ ₹50,000 ವರೆಗೆ ಆರ್ಥಿಕ ನೆರವು."
    },
    benefit: "₹10,000 to ₹50,000 input & marketing grant",
    eligibility: {
      en: "Resident farmers of Mizoram engaged in settled agriculture.",
      te: "మిజోరంలో శాశ్వత వ్యవసాయం చేసే స్థానిక రైతులు.",
      hi: "मिजोरम के स्थायी खेती करने वाले स्थानीय किसान।",
      mr: "मिझोरममधील शेती करणारे स्थानिक शेतकरी.",
      ta: "மிசோரமில் விவசாயம் செய்யும் உள்ளூர் விவசாயிகள்.",
      kn: "ಮಿಜೋರಾಂನಲ್ಲಿ ಕೃಷಿ ಮಾಡುವ ಸ್ಥಳೀಯ ರೈತರು."
    },
    criteria: {
      farmer_category: "Settled farmers and jhum rehabilitation cultivators",
      landholding: "Minimum 0.5 acre",
      crops: "Ginger, Turmeric, Oil Palm, Arecanut, Mizo Chilli",
      location: "Resident of Mizoram",
      restrictions: "Must transition to permanent settled agriculture"
    },
    rules: {
      requires_land_ownership: false,
      tenant_allowed: true,
      max_land_acres: null,
      min_age: 18,
      max_age: null,
      supported_crops: null,
      state_restriction: "Mizoram"
    },
    documents: ["Aadhaar Card", "Land Settlement Certificate (LSC) / Village Council Pass", "Bank Passbook"],
    deadline: "Apply seasonally through District Agriculture Offices",
    claim_window: "Verification by Agriculture Extension Officer",
    source_url: "https://agriculture.mizoram.gov.in/",
    last_verified: "2026-09-12"
  },
  {
    scheme_id: "nl_farm_mechanisation",
    name: {
      en: "Nagaland Farm Mechanisation & Power Tiller Subsidy",
      te: "నాగాలాండ్ వ్యవసాయ యంత్రీకరణ & పవర్ టిల్లర్ సబ్సిడీ",
      hi: "नागालैंड कृषि यांत्रिकीकरण एवं पावर टिलर सब्सिडी",
      mr: "नागालँड कृषी यांत्रिकीकरण व पॉवर टिलर अनुदान",
      ta: "நாகாலாந்து பண்ணை இயந்திரமயமாக்கல் மற்றும் பவர் டில்லர் மானியம்",
      kn: "ನಾಗಾಲ್ಯಾಂಡ್ ಕೃಷಿ ಯಾಂತ್ರೀಕರಣ ಮತ್ತು ಪವರ್ ಟಿಲ್ಲರ್ ಸಬ್ಸಿಡಿ"
    },
    level: "State",
    state: "Nagaland",
    category: "machinery",
    description: {
      en: "50% to 60% capital subsidy on mini power tillers, paddy transplanters, and terrace cultivators tailored for Nagaland hilly terrain.",
      te: "నాగాలాండ్ కొండ ప్రాంతాల కోసం మినీ పవర్ టిల్లర్లు మరియు వరి నాటు యంత్రాలపై 50% నుండి 60% సబ్సిడీ.",
      hi: "नागालैंड के पर्वतीय एवं सीढ़ीदार खेतों के लिए मिनी पावर टिलर और ट्रांसप्लांटर पर 50% से 60% सब्सिडी।",
      mr: "डोंगराळ भागातील शेतीसाठी पॉवर टिलर आणि भात लावणी यंत्रांवर 50% ते 60% अनुदान.",
      ta: "மலைப்பாங்கான நிலங்களில் விவசாயம் செய்ய பவர் டில்லர்களுக்கு 50% முதல் 60% மானியம்.",
      kn: "ಬೆಟ್ಟಗುಡ್ಡಗಳ ಪ್ರದೇಶದ ಕೃಷಿಗಾಗಿ ಪವರ್ ಟಿಲ್ಲರ್‌ಗಳಿಗೆ 50% ರಿಂದ 60% ಸಬ್ಸಿಡಿ."
    },
    benefit: "50% - 60% Subsidy on lightweight hill farm machinery",
    eligibility: {
      en: "Active terrace and jhum farmers belonging to indigenous Naga tribes.",
      te: "నాగాలాండ్‌లోని గిరిజన తెగలకు చెందిన చురుకైన రైతులు.",
      hi: "नागालैंड की मूल नागा जनजातियों से संबंधित सक्रिय किसान।",
      mr: "नागालँडमधील मूळ आदिवासी शेतकरी.",
      ta: "நாகாலாந்தின் பூர்வீக பழங்குடி விவசாயிகள்.",
      kn: "ನಾಗಾಲ್ಯಾಂಡ್‌ನ ಸ್ಥಳೀಯ ಬುಡಕಟ್ಟು ರೈತರು."
    },
    criteria: {
      farmer_category: "Individual farmers and village agricultural councils",
      landholding: "Terrace or cultivable hill plot",
      crops: "Paddy, Maize, Millets, Naga Mircha",
      location: "Resident of Nagaland",
      restrictions: "Indigenous Naga Inhabitant Certificate required"
    },
    rules: {
      requires_land_ownership: false,
      tenant_allowed: true,
      max_land_acres: null,
      min_age: 18,
      max_age: null,
      supported_crops: null,
      state_restriction: "Nagaland"
    },
    documents: ["Indigenous Inhabitant Certificate (IIC)", "Aadhaar Card", "Village Council Recommendation", "Bank Passbook"],
    deadline: "Apply via Directorate of Agriculture, Kohima",
    claim_window: "Machinery handover with field inspection",
    source_url: "https://agri.nagaland.gov.in/",
    last_verified: "2026-08-25"
  },
  {
    scheme_id: "ar_atmanirbhar_krishi",
    name: {
      en: "Arunachal Atma Nirbhar Krishi Yojana (ANKY)",
      te: "అరుణాచల్ ఆత్మనిర్భర్ కృషి యోజన (45% గ్రాంట్ + 45% రుణం)",
      hi: "अरुणाचल आत्मनिर्भर कृषि योजना (एएनकेवाई)",
      mr: "अरुणाचल आत्मनिर्भर कृषी योजना (45% सरकारी अनुदान)",
      ta: "அருணாச்சல ஆத்மநிர்பார் கிருஷி திட்டம்",
      kn: "ಅರುಣಾಚಲ ಆತ್ಮನಿರ್ಭರ ಕೃಷಿ ಯೋಜನೆ"
    },
    level: "State",
    state: "Arunachal Pradesh",
    category: "machinery",
    description: {
      en: "Provides 45% government subsidy + 45% bank credit + only 10% farmer contribution for farm machinery and tractors without mortgage or collateral in Arunachal Pradesh.",
      te: "అరుణాచల్ ప్రదేశ్‌లో పూచీకత్తు లేకుండా వ్యవసాయ యంత్రాలపై 45% ప్రభుత్వ సబ్సిడీ + 45% బ్యాంకు రుణం + కేవలం 10% రైతు వాటా.",
      hi: "अरुणाचल प्रदेश में बिना किसी बंधक या गारंटी के कृषि उपकरणों पर 45% सरकारी सब्सिडी + 45% बैंक ऋण + केवल 10% किसान अंश।",
      mr: "विनातारण शेती अवजारांवर 45% सरकारी अनुदान + 45% बँक कर्ज + फक्त 10% शेतकरी हिस्सा.",
      ta: "அடமானம் இல்லாமல் 45% அரசு மானியம் + 45% வங்கி கடன் + 10% விவசாயி பங்கு.",
      kn: "ಯಾವುದೇ ಅಡಮಾನವಿಲ್ಲದೆ 45% ಸರ್ಕಾರಿ ಸಬ್ಸಿಡಿ + 45% ಬ್ಯಾಂಕ್ ಸಾಲ + ಕೇವಲ 10% ರೈತರ ಪಾಲು."
    },
    benefit: "45% Govt Grant + 45% Bank Loan (Collateral-Free)",
    eligibility: {
      en: "Farmers, SHGs, and FPOs registered in Arunachal Pradesh.",
      te: "అరుణాచల్ ప్రదేశ్‌లో నమోదైన రైతులు, స్వయం సహాయక సంఘాలు.",
      hi: "अरुणाचल प्रदेश में पंजीकृत किसान, स्वयं सहायता समूह एवं एफपीओ।",
      mr: "अरुणाचल प्रदेशातील नोंदणीकृत शेतकरी आणि बचत गट.",
      ta: "அருணாச்சல பிரதேசத்தில் பதிவு செய்த விவசாயிகள் மற்றும் குழுக்கள்.",
      kn: "ಅರುಣಾಚಲ ಪ್ರದೇಶದಲ್ಲಿ ನೋಂದಾಯಿಸಿದ ರೈತರು ಮತ್ತು ಗುಂಪುಗಳು."
    },
    criteria: {
      farmer_category: "Individual farmers, SHGs, and FPOs",
      landholding: "No ceiling",
      crops: "Kiwi, Orange, Large Cardamom, Paddy, Maize",
      location: "Resident of Arunachal Pradesh",
      restrictions: "Collateral-free credit limit up to ₹10 Lakhs"
    },
    rules: {
      requires_land_ownership: true,
      tenant_allowed: false,
      max_land_acres: null,
      min_age: 18,
      max_age: null,
      supported_crops: null,
      state_restriction: "Arunachal Pradesh"
    },
    documents: ["APST (Arunachal Scheduled Tribe) Certificate", "Aadhaar Card", "Land Possession Certificate (LPC)", "Bank Account"],
    deadline: "Apply online at arunachalpradesh.gov.in portal",
    claim_window: "Direct credit of 45% subsidy into bank account upon delivery",
    source_url: "https://arunachalpradesh.gov.in/",
    last_verified: "2026-09-28"
  },
  {
    scheme_id: "jk_hadp_mechanisation",
    name: {
      en: "J&K HADP Farm Mechanisation & Orchard Subsidy",
      te: "జమ్మూ & కాశ్మీర్ హెచ్‌ఏడీపీ వ్యవసాయ యంత్రీకరణ & పండ్లతోటల సబ్సిడీ",
      hi: "जम्मू-कश्मीर एचएडीपी कृषि यांत्रिकीकरण एवं बागवानी सब्सिडी",
      mr: "जम्मू-काश्मीर एचएडीपी कृषी यांत्रिकीकरण व फळबाग अनुदान",
      ta: "ஜம்மு & காஷ்மீர் பண்ணை இயந்திரமயமாக்கல் மற்றும் பழத்தோட்ட மானியம்",
      kn: "ಜಮ್ಮು ಮತ್ತು ಕಾಶ್ಮೀರ ಕೃಷಿ ಯಾಂತ್ರೀಕರಣ ಮತ್ತು ತೋಟಗಾರಿಕೆ ಸಬ್ಸಿಡಿ"
    },
    level: "State",
    state: "Jammu and Kashmir",
    category: "machinery",
    description: {
      en: "50% capital subsidy on tractors, power weeders, high-density apple orchards, and micro-irrigation under the Holistic Agriculture Development Programme in J&K.",
      te: "జమ్మూ కాశ్మీర్‌లో ట్రాక్టర్లు, హై-డెన్సిటీ ఆపిల్ తోటల పెంపకం మరియు సూక్ష్మ సేద్యంపై 50% భారీ సబ్సిడీ.",
      hi: "जम्मू-कश्मीर में हॉलिस्टिक एग्रीकल्चर डेवलपमेंट प्रोग्राम के तहत ट्रैक्टर, पावर वीडर व सेब बागवानी पर 50% की सीधी सब्सिडी।",
      mr: "जम्मू-काश्मीरमध्ये ट्रॅक्टर, पॉवर विडर आणि सफरचंद बागांवर 50% थेट अनुदान.",
      ta: "ஜம்மு காஷ்மீரில் டிராக்டர்கள் மற்றும் ஆப்பிள் தோட்டங்களுக்கு 50% மானியம்.",
      kn: "ಜಮ್ಮು-ಕಾಶ್ಮೀರದಲ್ಲಿ ಟ್ರ್ಯಾಕ್ಟರ್‌ಗಳು ಮತ್ತು ಸೇಬು ತೋಟಗಳಿಗೆ 50% ಸಬ್ಸಿಡಿ."
    },
    benefit: "50% Capital Subsidy on farm machinery & high-density orchards",
    eligibility: {
      en: "Farmers cultivating agricultural and horticultural land in Jammu & Kashmir.",
      te: "జమ్మూ కాశ్మీర్‌లో వ్యవసాయ మరియు ఉద్యానవన పంటలు సాగుచేసే రైతులు.",
      hi: "जम्मू और कश्मीर में कृषि एवं बागवानी भूमि पर खेती करने वाले किसान।",
      mr: "जम्मू-काश्मीरमधील शेतकरी आणि फळबाग उत्पादक.",
      ta: "ஜம்மு காஷ்மீரில் விவசாயம் செய்யும் விவசாயிகள் மற்றும் பழத்தோட்ட உரிமையாளர்கள்.",
      kn: "ಜಮ್ಮು ಮತ್ತು ಕಾಶ್ಮೀರದಲ್ಲಿ ಕೃಷಿ ಮತ್ತು ತೋಟಗಾರಿಕೆ ಮಾಡುವ ರೈತರು."
    },
    criteria: {
      farmer_category: "All orchardists, small and marginal farmers",
      landholding: "No upper limit",
      crops: "Apple, Saffron, Walnut, Paddy, Maize, Mustard",
      location: "Resident of Jammu and Kashmir",
      restrictions: "Apply through KISAN SAATHI portal"
    },
    rules: {
      requires_land_ownership: true,
      tenant_allowed: false,
      max_land_acres: null,
      min_age: 18,
      max_age: null,
      supported_crops: null,
      state_restriction: "Jammu and Kashmir"
    },
    documents: ["Domicile Certificate", "Aadhaar Card", "Revenue Record (Fard Intikhab)", "Bank Passbook"],
    deadline: "Apply year-round on hadp.jk.gov.in portal",
    claim_window: "Joint inspection by Horticulture & Agri Officers within 15 days",
    source_url: "https://hadp.jk.gov.in/",
    last_verified: "2026-10-15"
  }
];

console.log('Building script loaded successfully.');
