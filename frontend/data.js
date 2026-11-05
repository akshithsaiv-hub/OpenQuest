// Master Scheme Data & Multi-Language Dictionary
const SCHEMES_DATA = [
  {
    scheme_id: "pm_kisan",
    name: {
      en: "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
      te: "పీఎం-కిసాన్ (ప్రధానమంత్రి కిసాన్ సమ్మాన్ నిధి)",
      hi: "पीएम-किसान (प्रधानमंत्री किसान सम्मान निधि)",
      mr: "पीएम-किसान (प्रधानमंत्री किसान सन्मान निधी)",
      ta: "பிஎம்-கிசான் (பிரதான் மந்திரி கிசான் சம்மான் நிதி)",
      kn: "ಪಿಎಂ-ಕಿಸಾನ್ (ಪ್ರಧಾನ ಮಂತ್ರಿ ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿ)"
    },
    level: "Central",
    state: "All",
    category: "income_support",
    description: {
      en: "Direct income support of ₹6,000 per year in three equal four-monthly installments of ₹2,000 each credited directly to farmer bank accounts.",
      te: "రైతులకు ప్రతి సంవత్సరం ₹6,000 ఆర్థిక సాయం, మూడు విడతల్లో ₹2,000 చొప్పున నేరుగా బ్యాంకు ఖాతాలో జమ చేయబడుతుంది.",
      hi: "किसानों को प्रति वर्ष ₹6,000 की प्रत्यक्ष आय सहायता, तीन समान किस्तों में ₹2,000 सीधे बैंक खाते में भेजी जाती है।",
      mr: "शेतकऱ्यांना दरवर्षी ₹6,000 थेट मदत, प्रत्येकी ₹2,000 चे तीन हप्ते थेट बँक खात्यात जमा केले जातात.",
      ta: "விவசாயிகளுக்கு ஆண்டுக்கு ₹6,000 நேரடி நிதி உதவி, மூன்று தவணைகளில் தலா ₹2,000 நேரடியாக வங்கிக் கணக்கில் செலுத்தப்படும்.",
      kn: "ರೈತರಿಗೆ ವರ್ಷಕ್ಕೆ ₹6,000 ನೇರ ಆರ್ಥಿಕ ನೆರವು, ತಲಾ ₹2,000 ನಂತೆ ಮೂರು ಕಂತುಗಳಲ್ಲಿ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಜಮಾ ಮಾಡಲಾಗುತ್ತದೆ."
    },
    benefit: "₹6,000 / year (3 installments of ₹2,000 via DBT)",
    eligibility: {
      en: "Landowning farmer families with valid land record. Income-tax payers and government employees excluded. (Oral tenants not eligible).",
      te: "భూమి యాజమాన్యం గల రైతు కుటుంబాలు. ఆదాయపు పన్ను చెల్లించేవారు మినహాయింపు. (కౌలు రైతులు అర్హులు కారు).",
      hi: "भूमिधारक किसान परिवार। आयकर दाता और सरकारी कर्मचारी बाहर हैं। (बटाईदार किसान पात्र नहीं हैं)।",
      mr: "जमीन मालक शेतकरी कुटुंबे. आयकर भरणारे अपात्र. (कुळ शेतकरी पात्र नाहीत).",
      ta: "நில உரிமை உள்ள விவசாயக் குடும்பங்கள். வருமான வரி செலுத்துபவர்கள் விலக்கப்பட்டுள்ளனர்.",
      kn: "ಸ್ವಂತ ಜಮೀನು ಹೊಂದಿರುವ ರೈತ ಕುಟುಂಬಗಳು. ಆದಾಯ ತೆರಿಗೆ ಪಾವತಿದಾರರಿಗೆ ಅನ್ವಯಿಸುವುದಿಲ್ಲ."
    },
    documents: [
      "Aadhaar Card linked to active mobile",
      "Land Record (Pahani / Khasra / RoR-1B)",
      "Aadhaar-seeded Bank Account (NPCI enabled)",
      "Completed e-KYC on PM-KISAN portal"
    ],
    deadline: "Continuous enrollment; e-KYC required before each tranche",
    claim_window: "Grievances redirected to Kisan e-Mitra AI chatbot",
    source_url: "https://pmkisan.gov.in/",
    last_verified: "2026-10-25"
  },
  {
    scheme_id: "pmfby",
    name: {
      en: "PMFBY (Pradhan Mantri Fasal Bima Yojana)",
      te: "పీఎంఎఫ్‌బీవై (ప్రధానమంత్రి ఫసల్ బీమా యోజన)",
      hi: "पीएमएफबीवाई (प्रधानमंत्री फसल बीमा योजना)",
      mr: "पीएमएफबीवाय (प्रधानमंत्री पीक विमा योजना)",
      ta: "பிஎம்எஃப்பிஒய் (பிரதான் மந்திரி பயிர் காப்பீட்டுத் திட்டம்)",
      kn: "ಪಿಎಂಎಫ್‌ಬಿವೈ (ಪ್ರಧಾನ ಮಂತ್ರಿ ಫಸಲ್ ಬಿಮಾ ಯೋಜನೆ)"
    },
    level: "Central",
    state: "All",
    category: "insurance",
    description: {
      en: "Comprehensive crop loss insurance against drought, floods, hailstorms, and unseasonal rains. Farmer pays nominal premium (2% Kharif, 1.5% Rabi).",
      te: "కరువు, వరదలు, వడగండ్లు మరియు అకాల వర్షాల వల్ల కలిగే పంట నష్టానికి సమగ్ర పంట బీమా. రైతు నామమాత్రపు ప్రీమియం చెల్లిస్తారు (ఖరీఫ్ 2%, రబీ 1.5%).",
      hi: "सूखा, बाढ़, ओलावृष्टि और बेमौसम बारिश से होने वाले नुकसान के लिए व्यापक फसल बीमा। किसान केवल 2% खरीफ और 1.5% रबी प्रीमियम भरते हैं।",
      mr: "दुष्काळ, पूर, गारपीट आणि अवकाळी पावसामुळे होणाऱ्या नुकसानीसाठी व्यापक पीक विमा. शेतकरी नाममात्र हप्ता भरतात.",
      ta: "வறட்சி, வெள்ளம் மற்றும் பருவம் தவறிய மழையால் ஏற்படும் பயிர் இழப்பிற்கு விரிவான பயிர் காப்பீடு.",
      kn: "ಬರ, ಪ್ರವಾಹ ಮತ್ತು ಅಕಾಲಿಕ ಮಳೆಯಿಂದ ಉಂಟಾಗುವ ಬೆಳೆ ನಷ್ಟಕ್ಕೆ ಸಮಗ್ರ ಬೆಳೆ ವಿಮೆ."
    },
    benefit: "Full sum-insured payout for yield loss threshold (Farmer pays 1.5% - 2%)",
    eligibility: {
      en: "All farmers growing notified crops (both landowners and tenant farmers with sowing certificates).",
      te: "నోటిఫై చేయబడిన పంటలు సాగుచేసే రైతులందరూ (భూ యజమానులు మరియు కౌలు రైతులు).",
      hi: "अधिसूचित फसलें उगाने वाले सभी किसान (जमीन मालिक और बटाईदार दोनों)।",
      mr: "अधिसूचित पिके घेणारे सर्व शेतकरी (जमीन मालक आणि कुळ शेतकरी).",
      ta: "அறிவிக்கப்பட்ட பயிர்களை பயிரிடும் அனைத்து விவசாயிகள் (நில உரிமையாளர்கள் மற்றும் குத்தகைதாரர்கள்).",
      kn: "ಅಧಿಸೂಚಿತ ಬೆಳೆಗಳನ್ನು ಬೆಳೆಯುವ ಎಲ್ಲಾ ರೈತರು (ಭೂಮಾಲೀಕರು ಮತ್ತು ಗೇಣಿದಾರರು)."
    },
    documents: [
      "Aadhaar Card",
      "Land Record / Tenant Sowing Certificate",
      "Bank Passbook with IFSC",
      "Geo-tagged photos via Crop Insurance App"
    ],
    deadline: "Cut-off: 31st July (Kharif) / 31st December (Rabi)",
    claim_window: "CRITICAL: Intimate localized loss within 72 HOURS via 14447 or App",
    source_url: "https://pmfby.gov.in/",
    last_verified: "2026-10-20"
  },
  {
    scheme_id: "kcc",
    name: {
      en: "Kisan Credit Card (KCC) Crop Loan",
      te: "కిసాన్ క్రెడిట్ కార్డ్ (KCC) రాయితీ పంట రుణం",
      hi: "किसान क्रेडिट कार्ड (केसीसी) रियायती फसली ऋण",
      mr: "किसान क्रेडिट कार्ड (केसीसी) सवलतीचे पीक कर्ज",
      ta: "விவசாய கடன் அட்டை (KCC) மானியக் கடன்",
      kn: "ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ (ಕೆಸಿಸಿ) ರಿಯಾಯಿತಿ ಕೃಷಿ ಸಾಲ"
    },
    level: "Central",
    state: "All",
    category: "credit",
    description: {
      en: "Institutional short-term crop loans up to ₹3,00,000 at subsidized 4% effective interest with prompt repayment. Collateral-free limit up to ₹1,60,000.",
      te: "సకాలంలో చెల్లింపుతో 4% రాయితీ వడ్డీకే ₹3,00,000 వరకు స్వల్పకాలిక పంట రుణం. పూచీకత్తు లేకుండా ₹1,60,000 వరకు పరిమితి.",
      hi: "समय पर पुनर्भुगतान करने पर मात्र 4% ब्याज पर ₹3 लाख तक का फसली ऋण। ₹1.60 लाख तक बिना किसी बंधक (कोलैटरल) के उपलब्ध।",
      mr: "वेळेवर परतफेड केल्यास 4% सवलतीच्या व्याजाने ₹3 लाखांपर्यंत पीक कर्ज.",
      ta: "சரியான நேரத்தில் திருப்பிச் செலுத்தினால் 4% வட்டியில் ₹3 லட்சம் வரை பயிர் கடன்.",
      kn: "ಸಕಾಲದಲ್ಲಿ ಮರುಪಾವತಿಸಿದರೆ ಕೇವಲ 4% ಬಡ್ಡಿದರದಲ್ಲಿ ₹3 ಲಕ್ಷದವರೆಗೆ ಬೆಳೆ ಸಾಲ."
    },
    benefit: "Loans up to ₹1.60 Lakh collateral-free @ 4% annual interest",
    eligibility: {
      en: "Owner cultivators, tenant farmers, sharecroppers, and SHG/JLGs cultivating crops. Age 18–75.",
      te: "స్వంత రైతులు, కౌలు రైతులు మరియు స్వయం సహాయక బృందాలు. వయస్సు 18-75 సంవత్సరాలు.",
      hi: "स्वयं खेती करने वाले मालिक, बटाईदार और काश्तकार। आयु 18 से 75 वर्ष।",
      mr: "स्वतः शेती करणारे मालक आणि कुळ शेतकरी. वय 18 ते 75 वर्षे.",
      ta: "நில உரிமையாளர்கள் மற்றும் குத்தகை விவசாயிகள். வயது 18-75.",
      kn: "ಸ್ವಂತ ಸಾಗುವಳಿ ಮಾಡುವವರು ಮತ್ತು ಗೇಣಿದಾರ ರೈತರು. ವಯಸ್ಸು 18-75."
    },
    documents: [
      "Filled KCC Application Form",
      "Land Record / Lease agreement",
      "Identity Proof (Aadhaar / Voter ID)",
      "No-due certificate from local cooperative bank"
    ],
    deadline: "Continuous round-the-year availability at banks and PACS",
    claim_window: "3% interest subvention credited upon 1-year repayment",
    source_url: "https://www.myscheme.gov.in/schemes/kcc",
    last_verified: "2026-09-30"
  },
  {
    scheme_id: "pm_kmy",
    name: {
      en: "PM-KMY (Kisan Maan-Dhan Pension Yojana)",
      te: "పీఎం-కేఎంవై (కిసాన్ మాన్-ధన్ పెన్షన్ యోజన)",
      hi: "पीएम-केएमवाई (किसान मान-धन पेंशन योजना)",
      mr: "पीएम-केएमवाय (शेतकरी मानधन पेन्शन योजना)",
      ta: "பிஎம்-கேஎம்வை (விவசாயிகள் மான்-தன் ஓய்வூதிய திட்டம்)",
      kn: "ಪಿಎಂ-ಕೆಎಂವೈ (ಕಿಸಾನ್ ಮಾನ್-ಧನ್ ಪಿಂಚಣಿ ಯೋಜನೆ)"
    },
    level: "Central",
    state: "All",
    category: "pension",
    description: {
      en: "Assured old-age monthly pension of ₹3,000 for Small and Marginal Farmers upon reaching 60 years of age.",
      te: "చిన్న మరియు సన్నకారు రైతులకు 60 సంవత్సరాలు నిండిన తర్వాత ప్రతి నెలా ₹3,000 హామీ పెన్షన్.",
      hi: "60 वर्ष की आयु पूर्ण होने पर लघु एवं सीमांत किसानों को ₹3,000 मासिक सुनिश्चित पेंशन।",
      mr: "60 वर्षे पूर्ण झाल्यावर अल्प व अत्यल्प भूधारक शेतकऱ्यांना दरमहा ₹3,000 खात्रीशीर पेन्शन.",
      ta: "60 வயது நிறைவடைந்த பிறகு சிறு மற்றும் குறு விவசாயிகளுக்கு மாதம் ₹3,000 உறுதிசெய்யப்பட்ட ஓய்வூதியம்.",
      kn: "60 ವರ್ಷ ವಯಸ್ಸಾದ ನಂತರ ಸಣ್ಣ ಮತ್ತು ಅತಿ ಸಣ್ಣ ರೈತರಿಗೆ ತಿಂಗಳಿಗೆ ₹3,000 ಖಚಿತ ಪಿಂಚಣಿ."
    },
    benefit: "₹3,000 / month pension after age 60",
    eligibility: {
      en: "Small and marginal farmers owning cultivable land up to 5 acres (2 hectares). Entry age 18 to 40.",
      te: "5 ఎకరాల లోపు భూమి ఉన్న చిన్న, సన్నకారు రైతులు. చేరిక వయస్సు 18 నుండి 40 సంవత్సరాలు.",
      hi: "5 एकड़ (2 हेक्टेयर) तक कृषि भूमि वाले लघु एवं सीमांत किसान। प्रवेश आयु 18 से 40 वर्ष।",
      mr: "5 एकरांपर्यंत जमीन असलेले शेतकरी. वय 18 ते 40 वर्षे.",
      ta: "5 ஏக்கர் வரை நிலம் வைத்துள்ள விவசாயிகள். சேரும் வயது 18 முதல் 40.",
      kn: "5 ಎಕರೆವರೆಗೆ ಕೃಷಿ ಜಮೀನು ಹೊಂದಿರುವ ರೈತರು. ವಯೋಮಿತಿ 18 ರಿಂದ 40."
    },
    documents: ["Aadhaar Card", "Bank Account Passbook", "Land Record showing land <= 5 acres"],
    deadline: "Continuous enrollment at Common Service Centres (CSCs)",
    claim_window: "Pension starts automatically at age 60",
    source_url: "https://maandhan.in/",
    last_verified: "2026-09-15"
  },
  {
    scheme_id: "smam_farm_machinery",
    name: {
      en: "SMAM (Sub-Mission on Agricultural Mechanization)",
      te: "ఎస్ఎంఏఎం (వ్యవసాయ యాంత్రీకరణ సబ్సిడీ)",
      hi: "एसएमएएम (कृषि यंत्रीकरण उप-मिशन)",
      mr: "कृषी यांत्रिकीकरण उप-अभियान (ट्रॅक्टर/यंत्रे अनुदान)",
      ta: "வேளாண் இயந்திரமயமாக்கல் துணை இயக்கம்",
      kn: "ಕೃಷಿ ಯಾಂತ್ರೀಕರಣ ಉಪ-ಅಭಿಯಾನ"
    },
    level: "Central",
    state: "All",
    category: "machinery",
    description: {
      en: "40% to 60% capital subsidy on purchasing modern farm equipment: tractors, rotavators, power tillers, and threshers.",
      te: "ట్రాక్టర్లు, రోటవేటర్లు, పవర్ టిల్లర్లు కొనుగోలుపై 40% నుండి 60% వరకు భారీ సబ్సిడీ.",
      hi: "ट्रैक्टर, रोटावेटर, पावर टिलर और थ्रेशर की खरीद पर 40% से 60% तक की प्रत्यक्ष पूंजीगत सब्सिडी।",
      mr: "ट्रॅक्टर, रोटाव्हेटर आणि आधुनिक कृषी अवजारे खरेदीवर 40% ते 60% पर्यंत सरकारी अनुदान.",
      ta: "டிராக்டர், ரோட்டவேட்டர் போன்ற வேளாண் இயந்திரங்கள் வாங்க 40% முதல் 60% வரை மானியம்.",
      kn: "ಟ್ರಾಕ್ಟರ್, ರೋಟಾವೇಟರ್ ಮುಂತಾದ ಕೃಷಿ ಯಂತ್ರೋಪಕರಣಗಳ ಖರೀದಿಗೆ 40% ರಿಂದ 60% ಸಬ್ಸಿಡಿ."
    },
    benefit: "40% to 60% capital subsidy (up to ₹1,25,000 - ₹3,00,000)",
    eligibility: {
      en: "Landowning farmers across all states. Higher 50-60% slab for SC/ST, small/marginal, and women farmers.",
      te: "అన్ని రాష్ట్రాల రైతులకు వర్తిస్తుంది. ఎస్సీ/ఎస్టీ, మహిళా రైతులకు 50-60% అధిక సబ్సిడీ.",
      hi: "सभी राज्यों के जमीन मालिक किसान। एससी/एसटी, छोटे एवं महिला किसानों को 50-60% अधिक सब्सिडी।",
      mr: "सर्व जमीन मालक शेतकरी. महिला, एससी/एसटी शेतकऱ्यांसाठी 50-60% वाढीव अनुदान.",
      ta: "நில உரிமையுள்ள விவசாயிகள். எஸ்சி/எஸ்டி மற்றும் பெண் விவசாயிகளுக்கு கூடுதல் மானியம்.",
      kn: "ಎಲ್ಲಾ ರಾಜ್ಯಗಳ ರೈತರು. ಮಹಿಳೆಯರು ಮತ್ತು ಎಸ್‌ಸಿ/ಎಸ್‌ಟಿ ರೈತರಿಗೆ ಗರಿಷ್ಠ ಸಬ್ಸಿಡಿ."
    },
    documents: ["Aadhaar Card", "Land Passbook", "Dealer Proforma Quotation", "Bank Details"],
    deadline: "Apply seasonally via agrimachinery.nic.in DBT portal",
    claim_window: "Inspection within 30 days of delivery before DBT payout",
    source_url: "https://agrimachinery.nic.in/",
    last_verified: "2026-09-20"
  },
  {
    scheme_id: "pmksy_pdmc",
    name: {
      en: "PMKSY - Per Drop More Crop (Drip & Sprinkler Subsidy)",
      te: "పీఎంకేఎస్వై - బిందు & తుంపర సేద్యం సబ్సిడీ",
      hi: "पीएमकेएसवाई - प्रति बूंद अधिक फसल (ड्रिप एवं स्प्रिंकलर सब्सिडी)",
      mr: "ठिबक व तुषार सिंचन अनुदान योजना",
      ta: "சொட்டு நீர் மற்றும் தெளிப்பு நீர் பாசன மானியத் திட்டம்",
      kn: "ಹನಿ ಮತ್ತು ತುಂತುರು ನೀರಾವರಿ ಸಬ್ಸಿಡಿ ಯೋಜನೆ"
    },
    level: "Central",
    state: "All",
    category: "irrigation",
    description: {
      en: "45% to 55% capital subsidy for installing Drip and Sprinkler micro-irrigation systems to maximize water conservation.",
      te: "నీటి సంరక్షణ కోసం డ్రిప్ మరియు స్ప్రింక్లర్ సూక్ష్మ సేద్యం ఏర్పాటుపై 45% నుండి 55% రాయితీ.",
      hi: "पानी की बचत और अधिक उपज के लिए ड्रिप एवं स्प्रिंकलर सिस्टम लगाने पर 45% से 55% सब्सिडी।",
      mr: "पाण्याची बचत करण्यासाठी ठिबक व तुषार सिंचन संच बसविण्याकरिता 45% ते 55% अनुदान.",
      ta: "சொட்டு நீர் மற்றும் தெளிப்பு நீர் பாசனக் கருவிகள் அமைக்க 45% முதல் 55% வரை மானியம்.",
      kn: "ಹನಿ ಮತ್ತು ತುಂತುರು ನೀರಾವರಿ ಪದ್ಧತಿ ಅಳವಡಿಕೆಗೆ 45% ರಿಂದ 55% ಸಹಾಯಧನ."
    },
    benefit: "45% (General) to 55% (Small/Marginal) micro-irrigation subsidy",
    eligibility: {
      en: "Farmers owning agricultural land with an assured water source (well, borewell, or canal).",
      te: "వ్యవసాయ భూమి మరియు నీటి వనరు (బోరుబావి/బావి) కలిగిన రైతులు.",
      hi: "सुनिश्चित जल स्रोत (कुआं/नलकूप) वाले कृषि भूमि धारक किसान।",
      mr: "पाण्याची सोय असणारे शेतकरी.",
      ta: "பாசன நீர் வசதியுள்ள விவசாய நில உரிமையாளர்கள்.",
      kn: "ಖಚಿತ ನೀರಿನ ಮೂಲ ಹೊಂದಿರುವ ಕೃಷಿ ಭೂಮಿಯ ರೈತರು."
    },
    documents: ["Aadhaar Card", "Land Record", "Water/Electricity proof", "System Layout Plan"],
    deadline: "Rolling applications through District Horticulture / Agriculture Offices",
    claim_window: "Joint physical inspection within 45 days of installation",
    source_url: "https://pmksy.gov.in/microirrigation/",
    last_verified: "2026-08-30"
  },
  // --- TELANGANA ---
  {
    scheme_id: "ts_rythu_bharosa",
    name: {
      en: "Telangana Rythu Bharosa (Investment Support)",
      te: "తెలంగాణ రైతు భరోసా (రైతు పెట్టుబడి సాయం)",
      hi: "तेलंगाना रैतु भरोसा (कृषि निवेश सहायता)",
      mr: "तेलंगणा रयतू भरोसा (गुंतवणूक मदत)",
      ta: "தெலுங்கானா ரைத்து பரோசா (முதலீட்டு உதவி)",
      kn: "ತೆಲಂಗಾಣ ರೈತು ಭರೋಸಾ (ಬೆಳೆ ಹೂಡಿಕೆ ನೆರವು)"
    },
    level: "State",
    state: "Telangana",
    category: "income_support",
    description: {
      en: "₹12,000 per acre per year (₹6,000 for Kharif and ₹6,000 for Rabi) directly deposited to bank accounts for actively cultivated lands.",
      te: "సాగులో ఉన్న భూములకు సంవత్సరానికి ఎకరాకు ₹12,000 (ఖరీఫ్‌కు ₹6,000, రబీకి ₹6,000) నేరుగా బ్యాంకు ఖాతాలో జమ.",
      hi: "सक्रिय खेती वाली भूमि के लिए प्रति एकड़ ₹12,000 प्रति वर्ष (खरीफ में ₹6,000 और रबी में ₹6,000) प्रत्यक्ष बैंक जमा।",
      mr: "लागवडीखालील जमिनीसाठी दरवर्षी ₹12,000 प्रति एकर (खरीप ₹6,000 आणि रब्बी ₹6,000) थेट बँक खात्यात.",
      ta: "சாகுபடி செய்யப்படும் நிலத்திற்கு ஏக்கருக்கு ஆண்டுக்கு ₹12,000 (பருவத்திற்கு ₹6,000).",
      kn: "ಸಾಗುವಳಿ ಜಮೀನಿಗೆ ಎಕರೆಗೆ ವರ್ಷಕ್ಕೆ ₹12,000 (ಮುಂಗಾರು ₹6,000 ಮತ್ತು ಹಿಂಗಾರು ₹6,000) ನೆರವು."
    },
    benefit: "₹12,000 / acre / year (up to 10 acres cultivable ceiling)",
    eligibility: {
      en: "Landowning pattadars in Dharani / Bhu Bharati portal and tribal RoFR patta holders in Telangana. (Tenant farmers not covered).",
      te: "ధరణి పోర్టల్‌లో పట్టాదారులు మరియు గిరిజన RoFR పట్టాదారులు. (కౌలు రైతులకు వర్తించదు).",
      hi: "धरणी पोर्टल में पंजीकृत पट्टादार और रोफ़्र (RoFR) वन अधिकार पट्टा धारक। (बटाईदार शामिल नहीं)।",
      mr: "धरणी पोर्टलवर नोंदणीकृत पट्टेदार आणि वनहक्क पट्टाधारक.",
      ta: "தரணி இணையதளத்தில் பதிவான நில உரிமையாளர்கள் மற்றும் வன உரிமை பெற்றவர்கள்.",
      kn: "ಧರಣಿ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನೋಂದಾಯಿತ ಭೂಮಾಲೀಕರು ಮತ್ತು ಅರಣ್ಯ ಹಕ್ಕು ಪಟ್ಟಾ ಹೊಂದಿರುವವರು."
    },
    documents: ["Pattadar Passbook / Dharani Land Title", "Aadhaar Card", "NPCI-linked Bank Account"],
    deadline: "Disbursed at seasonal onsets: Kharif (June-July) & Rabi (Oct-Nov)",
    claim_window: "Report payment failures to Mandal Agricultural Officer (MAO) within 30 days",
    source_url: "https://rythubharosa.telangana.gov.in/",
    last_verified: "2026-10-15"
  },
  {
    scheme_id: "ts_rythu_bima",
    name: {
      en: "Telangana Rythu Bima (Group Life Insurance)",
      te: "తెలంగాణ రైతు బీమా (రైతుల సమూహ జీవిత బీమా)",
      hi: "तेलंगाना रैतु बीमा (सामूहिक जीवन बीमा योजना)",
      mr: "तेलंगणा रयतू विमा (गट जीवन विमा योजना)",
      ta: "தெலுங்கானா ரைத்து பீமா (குழு ஆயுள் காப்பீடு)",
      kn: "ತೆಲಂಗಾಣ ರೈತು ಭೀಮಾ (ಗುಂಪು ಜೀವ ವಿಮೆ)"
    },
    level: "State",
    state: "Telangana",
    category: "insurance",
    description: {
      en: "₹5,00,000 financial relief to nominee family within 10–15 days upon demise of enrolled farmer (100% premium paid by Telangana Govt to LIC).",
      te: "రైతు మరణిస్తే నామినీ కుటుంబానికి 10-15 రోజుల్లో ₹5,00,000 ఆర్థిక సాయం (పూర్తి ప్రీమియం ప్రభుత్వమే ఎల్‌ఐసీకి చెల్లిస్తుంది).",
      hi: "किसान की मृत्यु होने पर नामित परिवार को 10-15 दिनों में ₹5,00,000 की वित्तीय सहायता (100% प्रीमियम राज्य सरकार देती है)।",
      mr: "शेतकऱ्याचा मृत्यू झाल्यास वारसदारास ₹5,00,000 चे सहाय्य (संपूर्ण हप्ता राज्य सरकार भरते).",
      ta: "விவசாயி உயிரிழந்தால் அவரது குடும்பத்திற்கு 10-15 நாட்களில் ₹5,00,000 இழப்பீடு.",
      kn: "ರೈತ ಮೃತಪಟ್ಟರೆ ಕುಟುಂಬದ ನಾಮಿನಿಗೆ 10-15 ದಿನಗಳಲ್ಲಿ ₹5,00,000 ಪರಿಹಾರ."
    },
    benefit: "₹5,00,000 life insurance cover (100% free, state funded)",
    eligibility: {
      en: "Registered pattadars on Dharani aged between 18 and 59 years in Telangana.",
      te: "ధరణిలో నమోదైన 18 నుండి 59 సంవత్సరాల వయస్సు గల పట్టాదారు రైతులు.",
      hi: "18 से 59 वर्ष की आयु के धरणी पोर्टल पर पंजीकृत पट्टादार किसान।",
      mr: "18 ते 59 वर्षे वयाचे धरणी पोर्टलवरील नोंदणीकृत शेतकरी.",
      ta: "18 முதல் 59 வயதுடைய நில உரிமையாளர்கள்.",
      kn: "18 ರಿಂದ 59 ವರ್ಷ ವಯಸ್ಸಿನ ಪಟ್ಟಾದಾರ ರೈತರು."
    },
    documents: ["Pattadar Passbook", "Aadhaar of Farmer & Nominee", "Death Certificate", "Nominee Bank Passbook"],
    deadline: "Annual enrollment closes on August 13 of each policy year",
    claim_window: "CRITICAL: Nominee must submit claim to local AEO at Rythu Vedika within 10 DAYS of demise",
    source_url: "https://rythubima.telangana.gov.in/",
    last_verified: "2026-10-10"
  },
  // --- ANDHRA PRADESH ---
  {
    scheme_id: "ap_annadata_sukhibhava",
    name: {
      en: "Andhra Pradesh Annadata Sukhibhava / Rythu Bharosa",
      te: "ఆంధ్రప్రదేశ్ అన్నదాత సుఖీభవ / రైతు భరోసా",
      hi: "आंध्र प्रदेश अन्नदाता सुखीभव / रैतु भरोसा",
      mr: "आंध्र प्रदेश अन्नदाता सुखीभव योजना",
      ta: "ஆந்திரப் பிரதேசம் அன்னதாதா சுகிபவா",
      kn: "ಆಂಧ್ರಪ್ರದೇಶ ಅನ್ನದಾತ ಸುಖೀಭವ ಯೋಜನೆ"
    },
    level: "State",
    state: "Andhra Pradesh",
    category: "income_support",
    description: {
      en: "Direct financial assistance of ₹20,000/year (PM-KISAN ₹6k + State ₹14k). Extends coverage to SC/ST/BC/Minority tenant farmers holding CCRC cards.",
      te: "సంవత్సరానికి ₹20,000 ఆర్థిక సాయం (పీఎం-కిసాన్ ₹6 వేలు + రాష్ట్రం ₹14 వేలు). CCRC కార్డులు ఉన్న కౌలు రైతులకు కూడా వర్తిస్తుంది.",
      hi: "प्रति वर्ष ₹20,000 की प्रत्यक्ष सहायता (पीएम-किसान ₹6,000 + राज्य ₹14,000)। सीसीआरसी कार्ड धारक बटाईदार भी शामिल।",
      mr: "दरवर्षी ₹20,000 थेट मदत. भाडेकरू (कुळ) शेतकऱ्यांनाही लाभ.",
      ta: "ஆண்டுக்கு ₹20,000 நிதி உதவி. குத்தகை விவசாயிகளுக்கும் பயன்.",
      kn: "ವರ್ಷಕ್ಕೆ ₹20,000 ಆರ್ಥಿಕ ನೆರವು. ಗೇಣಿದಾರ ರೈತರಿಗೂ ಲಭ್ಯ."
    },
    benefit: "₹14,000 / year state grant (Total ₹20,000 with PM-KISAN, CCRC tenants covered)",
    eligibility: {
      en: "Landowning farmers and tenant farmers holding Crop Cultivator Rights Cards (CCRC) in Andhra Pradesh.",
      te: "ఆంధ్రప్రదేశ్‌లోని భూ యజమానులు మరియు CCRC కార్డులు కలిగిన కౌలు రైతులు.",
      hi: "आंध्र प्रदेश के भूमिधारक किसान और सीसीआरसी (CCRC) कार्ड धारक बटाईदार।",
      mr: "आंध्र प्रदेशातील जमीन मालक आणि सीसीआरसी कार्डधारक कुळ शेतकरी.",
      ta: "ஆந்திராவில் நில உரிமையாளர்கள் மற்றும் சிசிஆர்சி அட்டை வைத்திருக்கும் குத்தகை விவசாயிகள்.",
      kn: "ಆಂಧ್ರಪ್ರದೇಶದ ಭೂಮಾಲೀಕರು ಮತ್ತು ಸಿಸಿಆರ್‌ಸಿ ಕಾರ್ಡ್ ಹೊಂದಿರುವ ಗೇಣಿದಾರರು."
    },
    documents: ["Aadhaar Card", "Webland Land Record OR CCRC Tenant Card", "Aadhaar-seeded Bank Passbook"],
    deadline: "Disbursed in 3 installments (May, October, January)",
    claim_window: "Report grievances via Village Secretariats / Rythu Bharosa Kendras (RBKs)",
    source_url: "https://ysrrythubharosa.ap.gov.in/",
    last_verified: "2026-10-01"
  },
  {
    scheme_id: "ap_free_crop_insurance",
    name: {
      en: "Andhra Pradesh 100% Free Crop Insurance",
      te: "ఆంధ్రప్రదేశ్ ఉచిత పంటల బీమా పథకం",
      hi: "आंध्र प्रदेश मुफ्त फसल बीमा योजना",
      mr: "आंध्र प्रदेश १००% मोफत पीक विमा",
      ta: "ஆந்திரப் பிரதேசம் 100% இலவச பயிர் காப்பீடு",
      kn: "ಆಂಧ್ರಪ್ರದೇಶ 100% ಉಚಿತ ಬೆಳೆ ವಿಮೆ"
    },
    level: "State",
    state: "Andhra Pradesh",
    category: "insurance",
    description: {
      en: "Universal crop insurance where the State Government pays 100% farmer premium share for all crops registered in the e-Crop digital survey.",
      te: "రైతులకు రూపాయి కూడా ప్రీమియం లేకుండా 100% ఉచిత పంటల బీమా. ఈ-క్రాప్ (e-Crop) నమోదైన ప్రతి రైతుకు వర్తిస్తుంది.",
      hi: "ई-क्रॉप (e-Crop) डिजिटल पोर्टल पर पंजीकृत सभी फसलों के लिए 100% मुफ्त फसल बीमा। किसानों को ₹0 प्रीमियम भरना पड़ता है।",
      mr: "ई-क्रॉप नोंदणी केलेल्या शेतकऱ्यांसाठी १००% मोफत पीक विमा.",
      ta: "ஈ-கிராப் மூலம் பதிவு செய்யப்பட்ட அனைத்து பயிர்களுக்கும் 100% இலவச பயிர் காப்பீடு.",
      kn: "ಇ-ಕ್ರಾಪ್‌ನಲ್ಲಿ ನೋಂದಾಯಿಸಲಾದ ಎಲ್ಲಾ ಬೆಳೆಗಳಿಗೆ 100% ಉಚಿತ ಬೆಳೆ ವಿಮೆ."
    },
    benefit: "100% Free Crop Insurance (Zero farmer premium; automated e-Crop settlement)",
    eligibility: {
      en: "All farmers (landowners and tenants) in Andhra Pradesh whose crops are entered in the seasonal e-Crop booking.",
      te: "ఈ-క్రాప్ బుకింగ్‌లో పంట నమోదు చేసుకున్న ఆంధ్రప్రదేశ్ రైతులందరూ.",
      hi: "आंध्र प्रदेश के सभी किसान जिनकी फसल ई-क्रॉप सर्वेक्षण में दर्ज है।",
      mr: "ई-क्रॉप नोंदणी झालेले सर्व शेतकरी.",
      ta: "ஈ-கிராப் பதிவில் உள்ள அனைத்து ஆந்திர விவசாயிகள்.",
      kn: "ಇ-ಕ್ರಾಪ್ ಬುಕಿಂಗ್ ಮಾಡಿರುವ ಎಲ್ಲಾ ಆಂಧ್ರ ರೈತರು."
    },
    documents: ["Aadhaar Card", "e-Crop Booking Receipt", "CCRC Card / Pattadar Passbook"],
    deadline: "Complete e-Crop registration before August 31 (Kharif) / Jan 15 (Rabi)",
    claim_window: "Direct bank transfer based on automated Crop Cutting Experiments (CCEs)",
    source_url: "https://karshak.ap.gov.in/",
    last_verified: "2026-09-28"
  },
  // --- MAHARASHTRA ---
  {
    scheme_id: "mh_namo_shetkari",
    name: {
      en: "Maharashtra Namo Shetkari Mahasanman Nidhi",
      te: "మహారాష్ట్ర నమో శేత్కరి మహాసమ్మాన్ నిధి",
      hi: "महाराष्ट्र नमो शेतकरी महासन्मान निधि योजना",
      mr: "महाराष्ट्र नमो शेतकरी महासन्मान निधी योजना",
      ta: "மகாராஷ்டிரா நமோ ஷேத்கரி திட்டம்",
      kn: "ಮಹಾರಾಷ್ಟ್ರ ನಮೋ ಶೇತ್ಕರಿ ಮಹಾಸಮ್ಮಾನ್ ನಿಧಿ"
    },
    level: "State",
    state: "Maharashtra",
    category: "income_support",
    description: {
      en: "State top-up of ₹6,000/year to all PM-KISAN beneficiary farmers in Maharashtra, delivering a combined benefit of ₹12,000 per year.",
      te: "మహారాష్ట్ర రైతులకు పీఎం-కిసాన్ సాయంతో పాటు అదనంగా ₹6,000 రాష్ట్ర సాయం (మొత్తం ₹12,000).",
      hi: "महाराष्ट्र के पीएम-किसान लाभार्थियों को ₹6,000 प्रति वर्ष का अतिरिक्त राज्य टॉप-अप (कुल ₹12,000 प्रति वर्ष)।",
      mr: "महाराष्ट्रातील पीएम-किसान पात्र शेतकऱ्यांना राज्य सरकारकडून दरवर्षी अतिरिक्त ₹6,000 (एकूण ₹12,000 प्रति वर्ष).",
      ta: "மகாராஷ்டிராவில் பிஎம்-கிசானுடன் சேர்த்து மாநில அரசின் ₹6,000 கூடுதல் உதவி (மொத்தம் ₹12,000).",
      kn: "ಪಿಎಂ-ಕಿಸಾನ್ ಜತೆಗೆ ಮಹಾರಾಷ್ಟ್ರ ಸರ್ಕಾರದ ₹6,000 ಹೆಚ್ಚುವರಿ ನೆರವು (ಒಟ್ಟು ₹12,000)."
    },
    benefit: "₹6,000 / year state top-up (Total ₹12,000/yr with PM-KISAN in 3 tranches)",
    eligibility: {
      en: "Active PM-KISAN beneficiary landowning farmers in Maharashtra with verified 7/12 land records.",
      te: "7/12 భూమి పత్రాలు సరిచూడబడిన మహారాష్ట్ర పీఎం-కిసాన్ లబ్ధిదారులు.",
      hi: "महाराष्ट्र के भूमिधारक किसान जो पीएम-किसान योजना के सक्रिय लाभार्थी हैं।",
      mr: "महाराष्ट्रातील 7/12 व 8A नोंद असलेले पीएम-किसान लाभार्थी शेतकरी.",
      ta: "மகாராஷ்டிராவில் உள்ள பிஎம்-கிசான் பயனாளிகள்.",
      kn: "ಮಹಾರಾಷ್ಟ್ರದ ಪಿಎಂ-ಕಿಸಾನ್ ಫಲಾನುಭವಿ ರೈತರು."
    },
    documents: ["Aadhaar Card", "7/12 & 8A Land Extract", "Active PM-KISAN ID", "Bank Passbook"],
    deadline: "Credited in parallel with PM-KISAN tranches via MahaDBT",
    claim_window: "Verify land seeding (Bhumikaran) at Taluka Krishi Karyalaya if pending",
    source_url: "https://nsmn.mahadbt.maharashtra.gov.in/",
    last_verified: "2026-10-05"
  },
  {
    scheme_id: "mh_one_rupee_crop_insurance",
    name: {
      en: "Maharashtra ₹1 Crop Insurance (Ek Rupaya Pik Vima)",
      te: "మహారాష్ట్ర ₹1 రూపాయి పంటల బీమా పథకం",
      hi: "महाराष्ट्र ₹1 रुपया फसल बीमा योजना",
      mr: "महाराष्ट्र १ रुपयात पीक विमा योजना",
      ta: "மகாராஷ்டிரா ₹1 பயிர் காப்பீட்டு திட்டம்",
      kn: "ಮಹಾರಾಷ್ಟ್ರ ₹1 ಬೆಳೆ ವಿಮೆ ಯೋಜನೆ"
    },
    level: "State",
    state: "Maharashtra",
    category: "insurance",
    description: {
      en: "Crop loss protection for just ₹1 token fee. Government of Maharashtra pays 100% of the farmer's premium share under PMFBY.",
      te: "కేవలం ₹1 టోకెన్ రుసుముతో పూర్తి పంట బీమా రక్షణ. రైతుల ప్రీమియం మొత్తాన్ని మహారాష్ట్ర ప్రభుత్వమే చెల్లిస్తుంది.",
      hi: "मात्र ₹1 के टोकन शुल्क पर व्यापक फसल सुरक्षा। किसानों का संपूर्ण प्रीमियम राज्य सरकार भरती है।",
      mr: "शेतकऱ्यांसाठी अवघ्या १ रुपयात पीक विमा संरक्षण. उर्वरित सर्व हप्ता राज्य सरकार भरते.",
      ta: "வெறும் ₹1 கட்டணத்தில் முழுமையான பயிர் காப்பீடு.",
      kn: "ಕೇವಲ ₹1 ಟೋಕನ್ ಶುಲ್ಕದಲ್ಲಿ ಸಂಪೂರ್ಣ ಬೆಳೆ ವಿಮೆ ರಕ್ಷಣೆ."
    },
    benefit: "Comprehensive crop loss protection for just ₹1 token fee",
    eligibility: {
      en: "All farmers cultivating notified crops in Maharashtra with crop sowing recorded via e-Pik Pahani.",
      te: "ఈ-పీక్ పహానీ (e-Pik Pahani) ద్వారా పంట నమోదు చేసిన మహారాష్ట్ర రైతులందరూ.",
      hi: "महाराष्ट्र के वे सभी किसान जिनकी फसल ई-पीक पाहणी (e-Pik Pahani) में दर्ज है।",
      mr: "ई-पीक पाहणी नोंदणी केलेले महाराष्ट्रातील सर्व शेतकरी.",
      ta: "ஈ-பீக் பஹானியில் பயிர் பதிவு செய்த அனைத்து விவசாயிகள்.",
      kn: "ಇ-ಪೀಕ್ ಪಹಣಿಯಲ್ಲಿ ಬೆಳೆ ದಾಖಲಿಸಿರುವ ಎಲ್ಲಾ ರೈತರು."
    },
    documents: ["Aadhaar Card", "7/12 Extract with e-Pik Pahani entry", "Bank Passbook"],
    deadline: "Seasonal cut-off: 31st July (Kharif) / 31st Dec (Rabi)",
    claim_window: "CRITICAL: Intimate localized loss within 72 hours on Crop Insurance App",
    source_url: "https://krishi.maharashtra.gov.in/",
    last_verified: "2026-09-25"
  },
  {
    scheme_id: "mh_krishi_yantrikikaran",
    name: {
      en: "Maharashtra Krishi Yantrikikaran (MahaDBT Machinery)",
      te: "మహారాష్ట్ర వ్యవసాయ పరికరాల రాయితీ",
      hi: "महाराष्ट्र कृषि यंत्रीकरण योजना (महाडीबीटी)",
      mr: "महाराष्ट्र कृषी यांत्रिकीकरण योजना (महाडीबीटी लॉटरी)",
      ta: "மகாராஷ்டிரா வேளாண் இயந்திர மானியம்",
      kn: "ಮಹಾರಾಷ್ಟ್ರ ಕೃಷಿ ಯಂತ್ರೋಪಕರಣ ಸಬ್ಸಿಡಿ"
    },
    level: "State",
    state: "Maharashtra",
    category: "machinery",
    description: {
      en: "Up to 50% capital subsidy on purchasing tractors, power tillers, rotavators, and sprayers via the transparent MahaDBT lottery portal.",
      te: "మహాడీబీటీ లాటరీ ద్వారా ట్రాక్టర్లు, రోటవేటర్లు, పవర్ టిల్లర్లపై 50% వరకు రాయితీ.",
      hi: "महाडीबीटी पोर्टल के माध्यम से ट्रैक्टर, रोटावेटर और कृषि यंत्रों पर 50% तक अनुदान।",
      mr: "महाडीबीटी प्रणालीद्वारे ट्रॅक्टर, रोटाव्हेटर व इतर कृषी अवजारांसाठी ५०% पर्यंत थेट अनुदान.",
      ta: "டிராக்டர் மற்றும் விவசாய கருவிகளுக்கு 50% வரை மானியம்.",
      kn: "ಟ್ರಾಕ್ಟರ್ ಮತ್ತು ಕೃಷಿ ಸಲಕರಣೆಗಳ ಮೇಲೆ 50% ವರೆಗೆ ಸಬ್ಸಿಡಿ."
    },
    benefit: "40% to 50% capital subsidy on tractors and farm equipment",
    eligibility: {
      en: "Landowning farmers in Maharashtra registered on the MahaDBT portal.",
      te: "మహాడీబీటీ పోర్టల్‌లో నమోదైన మహారాష్ట్ర భూ యజమానులు.",
      hi: "महाडीबीटी पोर्टल पर पंजीकृत महाराष्ट्र के भूमिधारक किसान।",
      mr: "महाडीबीटी शेतकरी पोर्टलवर नोंदणी केलेले 7/12 धारक शेतकरी.",
      ta: "மகாடிபிடி இணையதளத்தில் பதிவு செய்த விவசாயிகள்.",
      kn: "ಮಹಾಡಿಬಿಟಿ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನೋಂದಾಯಿತ ರೈತರು."
    },
    documents: ["Aadhaar Card", "7/12 & 8A extracts", "Authorized Quotation", "Bank Details"],
    deadline: "Apply during seasonal lottery windows on mahadbt.maharashtra.gov.in",
    claim_window: "Upload invoice and machinery photos within 30 days of lottery selection",
    source_url: "https://mahadbt.maharashtra.gov.in/",
    last_verified: "2026-09-12"
  },
  // --- KARNATAKA ---
  {
    scheme_id: "ka_raitha_siri",
    name: {
      en: "Karnataka Raitha Siri (Millet Incentive Scheme)",
      te: "కర్ణాటక రైత సిరి (చిరుధాన్యాల ప్రోత్సాహకం)",
      hi: "कर्नाटक रैता सिरी (श्रीअन्न/मिलेट प्रोत्साहन योजना)",
      mr: "कर्नाटक रैता सिरी भरडधान्य प्रोत्साहन योजना",
      ta: "கர்நாடகா ரைதா சிரி சிறுதானிய திட்டம்",
      kn: "ಕರ್ನಾಟಕ ರೈತ ಸಿರಿ (ಸಿರಿಧಾನ್ಯ ಪ್ರೋತ್ಸಾಹಕ ಯೋಜನೆ)"
    },
    level: "State",
    state: "Karnataka",
    category: "income_support",
    description: {
      en: "Direct financial incentive of ₹10,000 per hectare (max 2 ha / ₹20,000) for cultivating minor millets (Foxtail, Kodo, Little, Barnyard millets).",
      te: "చిరుధాన్యాలు (కొర్రలు, అరికెలు, సామలు) సాగుచేసే రైతులకు హెక్టారుకు ₹10,000 నేరుగా ఆర్థిక ప్రోత్సాహకం.",
      hi: "लघु मिलेट्स (कोदो, कुटकी, सांवा, रागी) उगाने वाले किसानों को ₹10,000 प्रति हेक्टेयर सीधा प्रोत्साहन।",
      mr: "भरडधान्य पिकविणाऱ्या शेतकऱ्यांना ₹10,000 प्रति हेक्टर थेट अनुदान.",
      ta: "சிறுதானியங்கள் பயிரிடும் விவசாயிகளுக்கு ஹெக்டேருக்கு ₹10,000 நேரடி உதவி.",
      kn: "ಸಿರಿಧಾನ್ಯಗಳನ್ನು (ನವಣೆ, ಹಾರಕ, ಸಾಮೆ, ಊದಲು, ಕೊರಲೆ) ಬೆಳೆಯುವ ರೈತರಿಗೆ ಪ್ರತಿ ಹೆಕ್ಟೇರ್‌ಗೆ ₹10,000 ನೇರ ಪ್ರೋತ್ಸಾಹಧನ."
    },
    benefit: "₹10,000 / hectare incentive (up to 2 hectares / ₹20,000)",
    eligibility: {
      en: "Farmers in Karnataka cultivating notified minor millets registered on the FRUITS portal.",
      te: "ఫ్రూట్స్ (FRUITS) పోర్టల్‌లో నమోదై చిరుధాన్యాలు సాగుచేసే కర్ణాటక రైతులు.",
      hi: "कर्नाटक के किसान जो फ्रूट्स (FRUITS) पोर्टल पर पंजीकृत हैं और मिलेट्स उगाते हैं।",
      mr: "फ्रूट्स पोर्टलवर नोंदणी केलेले कर्नाटकचे भरडधान्य उत्पादक शेतकरी.",
      ta: "கர்நாடகாவில் சிறுதானிய பயிரிடும் விவசாயிகள்.",
      kn: "ಫ್ರೂಟ್ಸ್ (FRUITS) ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನೋಂದಾಯಿಸಿ ಸಿರಿಧಾನ್ಯ ಬೆಳೆಯುವ ಕರ್ನಾಟಕದ ರೈತರು."
    },
    documents: ["Aadhaar Card", "FRUITS FID Number", "RTC / Pahani showing millet crop", "Bank Passbook"],
    deadline: "Kharif registration during July-August / Rabi in Oct-Nov on FRUITS",
    claim_window: "Disbursed post field verification by Raitha Samparka Kendra (RSK)",
    source_url: "https://fruits.karnataka.gov.in/",
    last_verified: "2026-09-10"
  },
  {
    scheme_id: "ka_krishi_bhagya",
    name: {
      en: "Karnataka Krishi Bhagya (Farm Ponds & Drip)",
      te: "కర్ణాటక కృషి భాగ్య పథకం",
      hi: "कर्नाटक कृषि भाग्य योजना (खेत तालाब एवं ड्रिप)",
      mr: "कर्नाटक कृषी भाग्य शेततळे योजना",
      ta: "கர்நாடகா கிருஷி பாக்யா திட்டம்",
      kn: "ಕರ್ನಾಟಕ ಕೃಷಿ ಭಾಗ್ಯ ಯೋಜನೆ (ಕೃಷಿ ಹೊಂಡ & ಹನಿ ನೀರಾವರಿ)"
    },
    level: "State",
    state: "Karnataka",
    category: "irrigation",
    description: {
      en: "50% to 90% subsidy for constructing farm ponds (Krishi Honda), polythene lining, diesel pumpsets, and micro-irrigation in rainfed areas.",
      te: "వర్షాధార ప్రాంతాల్లో పంట కుంటలు (కృషి హొండ), పాలిథిన్ లైనింగ్, డీజిల్ పంపుసెట్లకు 50% నుండి 90% సబ్సిడీ.",
      hi: "वर्षा आधारित क्षेत्रों में खेत तालाब (कृषि होंडा), पॉलीथीन लाइनिंग और पंपसेट के लिए 50% से 90% सब्सिडी।",
      mr: "कोरडवाहू भागात शेततळे, अस्तरीकरण व पंपसेटसाठी 50% ते 90% अनुदान.",
      ta: "மழை சார் நிலங்களில் பண்ணைக் குட்டை அமைக்க 50% முதல் 90% வரை மானியம்.",
      kn: "ಮಳೆಯಾಶ್ರಿತ ಪ್ರದೇಶಗಳಲ್ಲಿ ಕೃಷಿ ಹೊಂಡ, ಪಾಲಿಥೀನ್ ಹೊದಿಕೆ, ಡೀಸೆಲ್ ಪಂಪ್‌ಸೆಟ್‌ಗಳಿಗೆ 50% ರಿಂದ 90% ಸಬ್ಸಿಡಿ."
    },
    benefit: "50% (General) to 90% (SC/ST) subsidy on Farm Ponds and irrigation equipment",
    eligibility: {
      en: "Farmers owning rainfed/dryland agricultural land in designated Karnataka talukas.",
      te: "కర్ణాటకలోని వర్షాధార ప్రాంతాల భూ యజమానులు.",
      hi: "कर्नाटक के निर्धारित तालुकों में वर्षा आधारित भूमि के स्वामी किसान।",
      mr: "कर्नाटकातील कोरडवाहू शेतजमीन धारक.",
      ta: "மழைப்பகுதி நில உரிமையாளர்கள்.",
      kn: "ಮಳೆಯಾಶ್ರಿತ ಒಣಭೂಮಿ ಹೊಂದಿರುವ ಕರ್ನಾಟಕದ ರೈತರು."
    },
    documents: ["Aadhaar Card", "FRUITS FID Number", "RTC / Pahani", "Caste Certificate (for SC/ST 90% subsidy)"],
    deadline: "Apply through local Raitha Samparka Kendras (RSK)",
    claim_window: "Multi-stage geo-tagged photographic inspection before and after pond digging",
    source_url: "https://raitamitra.karnataka.gov.in/",
    last_verified: "2026-08-20"
  },
  // --- UTTAR PRADESH ---
  {
    scheme_id: "up_krishi_yantra",
    name: {
      en: "Uttar Pradesh Krishi Yantra Subsidy (upagriculture.com)",
      te: "ఉత్తరప్రదేశ్ వ్యవసాయ యంత్రాల సబ్సిడీ",
      hi: "उत्तर प्रदेश कृषि यंत्र सब्सिडी योजना (upagriculture.com)",
      mr: "उत्तर प्रदेश कृषी अवजारे अनुदान",
      ta: "உத்தரப் பிரதேசம் வேளாண் இயந்திர மானியம்",
      kn: "ಉತ್ತರ ಪ್ರದೇಶ ಕೃಷಿ ಯಂತ್ರೋಪಕರಣ ಸಬ್ಸಿಡಿ"
    },
    level: "State",
    state: "Uttar Pradesh",
    category: "machinery",
    description: {
      en: "40% to 50% capital subsidy on farm machinery (rotavators, laser levellers, threshers, seed drills) booked online via upagriculture.com.",
      te: "upagriculture.com ద్వారా ఆన్‌లైన్‌లో బుక్ చేసుకున్న రోటవేటర్లు, లేజర్ లెవలర్లపై 40% నుండి 50% రాయితీ.",
      hi: "रोटावेटर, लेजर लैंड लेवलर, थ्रेशर और सीड ड्रिल पर 40% से 50% तक सब्सिडी। टोकन बुकिंग प्रणाली upagriculture.com पर।",
      mr: "रोटाव्हेटर, थ्रेशर व आधुनिक यंत्रांवर ४०% ते ५०% अनुदान.",
      ta: "ரோட்டவேட்டர் மற்றும் விவசாய கருவிகளுக்கு 40% முதல் 50% மானியம்.",
      kn: "ರೋಟಾವೇಟರ್ ಮತ್ತು ಕೃಷಿ ಉಪಕರಣಗಳ ಮೇಲೆ 40% ರಿಂದ 50% ಸಬ್ಸಿಡಿ."
    },
    benefit: "40% to 50% capital subsidy on agricultural implements (Token booking system)",
    eligibility: {
      en: "Registered farmers on the UP Agriculture portal owning agricultural land in Uttar Pradesh.",
      te: "యూపీ అగ్రికల్చర్ పోర్టల్‌లో నమోదైన ఉత్తరప్రదేశ్ రైతులు.",
      hi: "यूपी कृषि विभाग के पोर्टल पर पंजीकृत भूमिधारक किसान।",
      mr: "यूपी कृषी पोर्टलवर नोंदणी केलेले शेतकरी.",
      ta: "உத்தரப் பிரதேச விவசாய போர்ட்டலில் பதிவு செய்த விவசாயிகள்.",
      kn: "ಉತ್ತರ ಪ್ರದೇಶ ಕೃಷಿ ಇಲಾಖೆ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನೋಂದಾಯಿತ ರೈತರು."
    },
    documents: ["Aadhaar Card", "UP Kisan Panjikaran Number", "Khatauni Land Record", "Token deposit slip"],
    deadline: "District-wise token booking slots announced in May-June & Oct-Nov",
    claim_window: "Verification by Deputy Director of Agriculture within 20 days of upload",
    source_url: "http://upagriculture.com/",
    last_verified: "2026-09-05"
  },
  {
    scheme_id: "up_free_boring",
    name: {
      en: "Uttar Pradesh Nishulk Boring Yojana (Tube Wells)",
      te: "ఉత్తరప్రదేశ్ ఉచిత బోరింగ్ పథకం",
      hi: "उत्तर प्रदेश निःशुल्क बोरिंग योजना (नलकूप अनुदान)",
      mr: "उत्तर प्रदेश मोफत बोअरवेल योजना",
      ta: "உத்தரப் பிரதேசம் இலவச ஆழ்துளை கிணறு திட்டம்",
      kn: "ಉತ್ತರ ಪ್ರದೇಶ ಉಚಿತ ಕೊಳವೆ ಬಾವಿ ಕೊರೆಯುವ ಯೋಜನೆ"
    },
    level: "State",
    state: "Uttar Pradesh",
    category: "irrigation",
    description: {
      en: "Grant up to ₹10,000 for shallow tube-well boring plus subsidized pump set and HDPE pipes for Small and Marginal farmers.",
      te: "చిన్న, సన్నకారు రైతులకు లోతు తక్కువ బోరింగ్ కోసం ₹10,000 వరకు గ్రాంట్ మరియు రాయితీ పంపుసెట్లు.",
      hi: "लघु एवं सीमांत किसानों को सुरक्षित सिंचाई हेतु उथले नलकूप बोरिंग के लिए ₹10,000 तक का सरकारी अनुदान।",
      mr: "अल्पभूधारक शेतकऱ्यांसाठी बोअरवेलकरिता ₹10,000 पर्यंत सरकारी अनुदान.",
      ta: "சிறு விவசாயிகளுக்கு ஆழ்துளை கிணறு அமைக்க ₹10,000 வரை மானியம்.",
      kn: "ಸಣ್ಣ ಮತ್ತು ಅತಿ ಸಣ್ಣ ರೈತರಿಗೆ ಕೊಳವೆ ಬಾವಿ ಕೊರೆಯಲು ₹10,000 ವರೆಗೆ ಸಹಾಯಧನ."
    },
    benefit: "Grant up to ₹10,000 for shallow tube-well boring + HDPE pipe assistance",
    eligibility: {
      en: "Small and marginal farmers holding cultivable land up to 5 acres in Uttar Pradesh.",
      te: "5 ఎకరాల లోపు భూమి ఉన్న ఉత్తరప్రదేశ్ చిన్న, సన్నకారు రైతులు.",
      hi: "उत्तर प्रदेश के 5 एकड़ तक कृषि भूमि वाले लघु एवं सीमांत किसान।",
      mr: "५ एकरांपर्यंत जमीन असणारे अल्पभूधारक शेतकरी.",
      ta: "5 ஏக்கர் வரை நிலம் வைத்துள்ள விவசாயிகள்.",
      kn: "5 ಎಕರೆವರೆಗೆ ಕೃಷಿ ಭೂಮಿ ಹೊಂದಿರುವ ಸಣ್ಣ ರೈತರು."
    },
    documents: ["Aadhaar Card", "Khatauni showing land <= 5 acres", "Small/Marginal Farmer Certificate"],
    deadline: "Processed year-round by District Minor Irrigation Department",
    claim_window: "Verification of functional installation by Junior Engineer",
    source_url: "http://upagriculture.com/",
    last_verified: "2026-08-15"
  },
  // --- MADHYA PRADESH ---
  {
    scheme_id: "mp_kisan_kalyan",
    name: {
      en: "Madhya Pradesh Mukhyamantri Kisan Kalyan Yojana",
      te: "మధ్యప్రదేశ్ ముఖ్యమంత్రి కిసాన్ కళ్యాణ్ యోజన",
      hi: "मध्य प्रदेश मुख्यमंत्री किसान कल्याण योजना",
      mr: "मध्य प्रदेश मुख्यमंत्री किसान कल्याण योजना",
      ta: "மத்தியப் பிரதேசம் முதலமைச்சர் கிசான் கல்யாண் திட்டம்",
      kn: "ಮಧ್ಯಪ್ರದೇಶ ಮುಖ್ಯಮಂತ್ರಿ ಕಿಸಾನ್ ಕಲ್ಯಾಣ ಯೋಜನೆ"
    },
    level: "State",
    state: "Madhya Pradesh",
    category: "income_support",
    description: {
      en: "₹6,000 per year state top-up in 3 installments of ₹2,000 directly to bank accounts of PM-KISAN beneficiary farmers in MP (Total ₹12,000/yr).",
      te: "మధ్యప్రదేశ్‌లోని పీఎం-కిసాన్ లబ్ధిదారులకు రాష్ట్ర ప్రభుత్వం నుండి అదనంగా ₹6,000 (మొత్తం ₹12,000).",
      hi: "मध्य प्रदेश के पीएम-किसान लाभार्थी किसानों को ₹6,000 प्रति वर्ष की अतिरिक्त सहायता (कुल ₹12,000 प्रति वर्ष)।",
      mr: "मध्य प्रदेशातील शेतकऱ्यांना राज्य सरकारकडून दरवर्षी ₹6,000 अतिरिक्त मदत.",
      ta: "மத்தியப் பிரதேச விவசாயிகளுக்கு மாநில அரசின் ₹6,000 கூடுதல் உதவி.",
      kn: "ಮಧ್ಯಪ್ರದೇಶದ ಪಿಎಂ-ಕಿಸಾನ್ ಫಲಾನುಭವಿಗಳಿಗೆ ರಾಜ್ಯ ಸರ್ಕಾರದ ₹6,000 ಹೆಚ್ಚುವರಿ ನೆರವು."
    },
    benefit: "₹6,000 / year state top-up (Total ₹12,000/yr with PM-KISAN)",
    eligibility: {
      en: "Resident landowning farmers in Madhya Pradesh registered under PM-KISAN and SAARA portal.",
      te: "మధ్యప్రదేశ్‌లోని భూ యజమానులు మరియు పీఎం-కిసాన్ లబ్ధిదారులు.",
      hi: "मध्य प्रदेश के भूमिधारक किसान जो पीएम-किसान और सारा (SAARA) पोर्टल पर पंजीकृत हैं।",
      mr: "मध्य प्रदेशातील सारा पोर्टलवर नोंदणी असलेले शेतकरी.",
      ta: "மத்தியப் பிரதேச நில உரிமையாளர்கள்.",
      kn: "ಮಧ್ಯಪ್ರದೇಶದ ಸಾರಾ (SAARA) ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನೋಂದಾಯಿತ ಭೂಮಾಲೀಕರು."
    },
    documents: ["Aadhaar Card", "Samagra ID", "Khasra / B-1 Land Record", "Bank Account Details"],
    deadline: "Disbursed concurrently with central PM-KISAN installments",
    claim_window: "Patwari / Tehsildar verification via SAARA portal for pending cases",
    source_url: "https://saara.mp.gov.in/",
    last_verified: "2026-09-18"
  },
  {
    scheme_id: "mp_solar_pump",
    name: {
      en: "Madhya Pradesh Solar Agricultural Pump Subsidy",
      te: "మధ్యప్రదేశ్ సోలార్ పంప్ సబ్సిడీ",
      hi: "मध्य प्रदेश मुख्यमंत्री सोलर पंप योजना (MPUVNL)",
      mr: "मध्य प्रदेश सौर कृषी पंप योजना",
      ta: "மத்தியப் பிரதேசம் சூரிய சக்தி பம்ப் திட்டம்",
      kn: "ಮಧ್ಯಪ್ರದೇಶ ಸೌರ ಕೃಷಿ ಪಂಪ್ ಸಬ್ಸಿಡಿ"
    },
    level: "State",
    state: "Madhya Pradesh",
    category: "irrigation",
    description: {
      en: "Up to 85% to 90% capital subsidy on standalone Solar Agriculture Water Pumps (2 HP to 7.5 HP) in fields without electricity connections.",
      te: "విద్యుత్ సౌకర్యం లేని వ్యవసాయ భూములలో సోలార్ పంపుల ఏర్పాటుపై 85% నుండి 90% వరకు సబ్సిడీ.",
      hi: "बिजली ग्रिड से दूर खेतों में सोलर सिंचाई पंप (2 एचपी से 7.5 एचपी) लगाने पर 85% से 90% तक सब्सिडी।",
      mr: "सौर कृषी पंपांवर ८५% ते ९०% पर्यंत भरीव अनुदान.",
      ta: "சூரிய சக்தி பாசன பம்புகளுக்கு 85% முதல் 90% வரை மானியம்.",
      kn: "ವಿದ್ಯುತ್ ಸಂಪರ್ಕವಿಲ್ಲದ ಜಮೀನುಗಳಲ್ಲಿ ಸೌರ ನೀರಾವರಿ ಪಂಪ್‌ಗಳಿಗೆ 85% ರಿಂದ 90% ಸಬ್ಸಿಡಿ."
    },
    benefit: "Up to 85-90% subsidy on Solar Agriculture Pump installation",
    eligibility: {
      en: "Landowning farmers in Madhya Pradesh with a water source and no existing grid power connection.",
      te: "నీటి వనరు ఉండి విద్యుత్ కనెక్షన్ లేని మధ్యప్రదేశ్ భూ యజమానులు.",
      hi: "मध्य प्रदेश के किसान जिनके पास जल स्रोत है और बिजली का कृषि कनेक्शन नहीं है।",
      mr: "पाण्याची सोय असणारे व वीज जोडणी नसलेले शेतकरी.",
      ta: "மின் இணைப்பு இல்லாத நீர் வசதியுள்ள விவசாயிகள்.",
      kn: "ವಿದ್ಯುತ್ ಸಂಪರ್ಕವಿಲ್ಲದ ನೀರಿನ ಮೂಲವಿರುವ ರೈತರು."
    },
    documents: ["Aadhaar Card", "Khasra copy", "No-Electricity-Connection Certificate", "Bank Passbook"],
    deadline: "Apply online during registration slots on cmsolarpump.mp.gov.in",
    claim_window: "5-year comprehensive warranty and commissioning by MPUVNL certified vendor",
    source_url: "https://cmsolarpump.mp.gov.in/",
    last_verified: "2026-08-25"
  },
  // --- PUNJAB ---
  {
    scheme_id: "pb_crop_residue_mgmt",
    name: {
      en: "Punjab Crop Residue Management (Happy/Super Seeder)",
      te: "పంజాబ్ పంట వ్యర్థాల నిర్వహణ యంత్రాల సబ్సిడీ",
      hi: "पंजाब फसल अवशेष प्रबंधन (हैप्पी/सुपर सीडर सब्सिडी)",
      mr: "पंजाब पीक अवशेष व्यवस्थापन यंत्रे अनुदान",
      ta: "பஞ்சாப் வைக்கோல் மேலாண்மை இயந்திர மானியம்",
      kn: "ಪಂಜಾಬ್ ಬೆಳೆ ತ್ಯಾಜ್ಯ ನಿರ್ವಹಣೆ ಯಂತ್ರಗಳ ಸಬ್ಸಿಡಿ"
    },
    level: "State",
    state: "Punjab",
    category: "machinery",
    description: {
      en: "50% subsidy for individual farmers and 80% for Custom Hiring Centres on purchasing Super Seeder, Happy Seeder, and Balers to eliminate stubble burning.",
      te: "కొయ్యకాళ్ళను కాల్చకుండా ఆపేందుకు హ్యాపీ సీడర్, సూపర్ సీడర్ యంత్రాలపై 50% నుండి 80% సబ్సిడీ.",
      hi: "पराली जलाने से रोकने के लिए सुपर सीडर, हैप्पी सीडर और बेलर मशीनों पर किसानों को 50% और कस्टम हायरिंग सेंटरों को 80% सब्सिडी।",
      mr: "भाताचे तण न जाळण्यासाठी सुपर सीडर व आधुनिक यंत्रांवर ५०% ते ८०% अनुदान.",
      ta: "வைக்கோல் எரிப்பதை தடுக்க சூப்பர் சீடர் இயந்திரங்களுக்கு 50% முதல் 80% வரை மானியம்.",
      kn: "ಕೂಳೆ ಸುಡುವುದನ್ನು ತಡೆಯಲು ಸೂಪರ್ ಸೀಡರ್ ಮತ್ತು ಬೆಳೆ ತ್ಯಾಜ್ಯ ಯಂತ್ರಗಳಿಗೆ 50% ರಿಂದ 80% ಸಬ್ಸಿಡಿ."
    },
    benefit: "50% (Individual) / 80% (Custom Hiring Centres) machinery subsidy",
    eligibility: {
      en: "Farmers in Punjab undertaking not to burn paddy straw.",
      te: "వరి కొయ్యలను కాల్చబోమని హామీ ఇచ్చే పంజాబ్ రైతులు.",
      hi: "पंजाब के किसान जो पराली न जलाने का शपथ पत्र देते हैं।",
      mr: "पराली न जाळण्याचे हमीपत्र देणारे पंजाबमधील शेतकरी.",
      ta: "வைக்கோல் எரிக்க மாட்டோம் என உறுதிமொழி அளிக்கும் பஞ்சாப் விவசாயிகள்.",
      kn: "ಬೆಳೆ ತ್ಯಾಜ್ಯ ಸುಡುವುದಿಲ್ಲ ಎಂದು ಪ್ರಮಾಣಪತ್ರ ನೀಡುವ ಪಂಜಾಬ್ ರೈತರು."
    },
    documents: ["Aadhaar Card", "Jamabandi (Land Record)", "No-Stubble-Burning Undertaking", "Bank Passbook"],
    deadline: "Apply via agrimachinerypb.com between May and July",
    claim_window: "Physical chassis stamping by Chief Agriculture Officer (CAO) team",
    source_url: "https://agrimachinerypb.com/",
    last_verified: "2026-08-10"
  },
  {
    scheme_id: "pb_free_power",
    name: {
      en: "Punjab Free Agricultural Power Supply",
      te: "పంజాబ్ ఉచిత వ్యవసాయ విద్యుత్ పథకం",
      hi: "पंजाब मुफ्त कृषि बिजली आपूर्ति योजना",
      mr: "पंजाब मोफत कृषी वीज पुरवठा योजना",
      ta: "பஞ்சாப் இலவச விவசாய மின்சாரம்",
      kn: "ಪಂಜಾಬ್ ಉಚಿತ ಕೃಷಿ ವಿದ್ಯುತ್ ಯೋಜನೆ"
    },
    level: "State",
    state: "Punjab",
    category: "irrigation",
    description: {
      en: "100% free electricity supply for agricultural tube-well motors with zero monthly electricity tariff paid by farmers.",
      te: "వ్యవసాయ బోరుబావులకు 100% ఉచిత విద్యుత్ సరఫరా. రైతులు ఎలాంటి కరెంట్ బిల్లు చెల్లించాల్సిన అవసరం లేదు.",
      hi: "किसानों के कृषि नलकूपों के लिए 100% मुफ्त बिजली आपूर्ति। किसानों को कोई मासिक बिजली बिल नहीं देना होता।",
      mr: "शेतकऱ्यांच्या कृषी पंपांसाठी १००% मोफत वीज.",
      ta: "விவசாய பம்புகளுக்கு 100% இலவச மின்சாரம்.",
      kn: "ಕೃಷಿ ಕೊಳವೆ ಬಾವಿಗಳಿಗೆ 100% ಉಚಿತ ವಿದ್ಯುತ್ ಪೂರೈಕೆ."
    },
    benefit: "100% Free electricity for agricultural tube-wells (Zero tariff)",
    eligibility: {
      en: "All registered agricultural tube-well consumers with PSPCL in Punjab.",
      te: "పంజాబ్‌లో రిజిస్టర్ అయిన వ్యవసాయ విద్యుత్ కనెక్షన్ ఉన్న రైతులందరూ.",
      hi: "पंजाब स्टेट पावर कॉर्पोरेशन (PSPCL) के सभी पंजीकृत कृषि उपभोक्ता।",
      mr: "पंजाबमधील सर्व नोंदणीकृत कृषी वीज ग्राहक.",
      ta: "பதிவு செய்யப்பட்ட அனைத்து பஞ்சாப் விவசாய மின் நுகர்வோர்.",
      kn: "ನೋಂದಾಯಿತ ಎಲ್ಲಾ ಕೃಷಿ ವಿದ್ಯುತ್ ಗ್ರಾಹಕರು."
    },
    documents: ["Aadhaar Card", "PSPCL Consumer Account Number", "Jamabandi Land Record"],
    deadline: "Continuous automatic benefit for authorized AP connections",
    claim_window: "Regularization via Voluntary Disclosure Schemes (VDS) at sub-division offices",
    source_url: "https://www.pspcl.in/",
    last_verified: "2026-07-30"
  },
  // --- HARYANA ---
  {
    scheme_id: "hr_bhavantar_bharpai",
    name: {
      en: "Haryana Bhavantar Bharpayee (Price Deficit Scheme)",
      te: "హర్యానా భావాంతర్ భర్పాయీ (ధరల నష్టపరిహారం)",
      hi: "हरियाणा भावांतर भरपाई योजना (मूल्य घाटा भरपाई)",
      mr: "हरियाणा भावांतर भरपाई योजना",
      ta: "ஹரியானா பாவாந்தர் பார்பாய் திட்டம்",
      kn: "ಹರಿಯಾಣ ಭಾವಾಂತರ್ ಭರಪಾಯಿ ಯೋಜನೆ"
    },
    level: "State",
    state: "Haryana",
    category: "income_support",
    description: {
      en: "Price deficiency compensation for vegetables, fruits, and bajra/mustard: state pays the exact difference if mandi rates fall below protected base price.",
      te: "కూరగాయలు, పండ్లు, సజ్జల ధరలు ప్రభుత్వం నిర్ణయించిన కనీస ధర కంటే తగ్గితే ఆ తేడాను ప్రభుత్వం నేరుగా రైతు ఖాతాలో జమ చేస్తుంది.",
      hi: "मंडी में सब्जियों, फलों और बाजरा/सरसों के दाम सरकारी संरक्षित भाव से कम होने पर घाटे की पूरी राशि सीधे किसान के खाते में।",
      mr: "बाजारभाव हमीभावापेक्षा कमी झाल्यास फरकाची रक्कम थेट खात्यात.",
      ta: "சந்தை விலை குறைந்தால் இழப்பீட்டுத் தொகையை அரசே வழங்குகிறது.",
      kn: "ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ನಿಗದಿತ ಬೆಲೆಗಿಂತ ಕಡಿಮೆಯಾದರೆ ವ್ಯತ್ಯಾಸದ ಮೊತ್ತವನ್ನು ಸರ್ಕಾರ ನೀಡುತ್ತದೆ."
    },
    benefit: "Direct cash compensation for market price drop below government base price",
    eligibility: {
      en: "Farmers in Haryana registered on the Meri Fasal Mera Byora (MFMB) portal selling through e-NAM mandis.",
      te: "మేరీ ఫసల్ మేరా బ్యోరా (MFMB)లో నమోదైన హర్యానా రైతులు.",
      hi: "मेरी फसल मेरा ब्योरा (MFMB) पोर्टल पर पंजीकृत हरियाणा के किसान।",
      mr: "मेरी फसल मेरा ब्योरा पोर्टलवर नोंदणी असलेले शेतकरी.",
      ta: "மேரி பாசல் மேரா பியோரா போர்ட்டலில் பதிவு செய்த விவசாயிகள்.",
      kn: "ಮೇರಿ ಫಸಲ್ ಮೇರಾ ಬ್ಯೋರಾ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನೋಂದಾಯಿತ ರೈತರು."
    },
    documents: ["Aadhaar Card", "MFMB Registration Slip", "J-Form Mandi Sale Receipt", "Bank Passbook"],
    deadline: "Register on fasal.haryana.gov.in before seasonal crop cut-off",
    claim_window: "Automated deficiency calculation based on verified J-Form mandi entries",
    source_url: "https://fasal.haryana.gov.in/",
    last_verified: "2026-09-01"
  },
  {
    scheme_id: "hr_mera_pani_meri_virasat",
    name: {
      en: "Haryana Mera Pani Meri Virasat (Crop Diversification)",
      te: "హర్యానా మేరా పానీ మేరీ విరాసత్ (పంటల మార్పిడి ప్రోత్సాహకం)",
      hi: "हरियाणा मेरा पानी मेरी विरासत योजना (फसल विविधीकरण)",
      mr: "हरियाणा मेरा पाणी मेरी विरासत योजना",
      ta: "ஹரியானா மேரா பானி மேரி விராஸத் திட்டம்",
      kn: "ಹರಿಯಾಣ ಮೇರಾ ಪಾನಿ ಮೇರಿ ವಿರಾಸತ್ ಯೋಜನೆ"
    },
    level: "State",
    state: "Haryana",
    category: "income_support",
    description: {
      en: "Direct financial grant of ₹7,000 per acre paid to farmers who switch from water-intensive paddy to maize, cotton, pulses, or leave land fallow.",
      te: "వరి సాగుకు బదులుగా మొక్కజొన్న, పత్తి, పప్పుధాన్యాలు సాగుచేసే రైతులకు ఎకరాకు ₹7,000 నగదు ప్రోత్సాహకం.",
      hi: "अधिक पानी वाली धान की खेती छोड़कर मक्का, कपास, दलहन उगाने वाले किसानों को ₹7,000 प्रति एकड़ सीधा प्रोत्साहन अनुदान।",
      mr: "भाताऐवजी मका, कापूस किंवा डाळी पिकविणाऱ्या शेतकऱ्यांना ₹7,000 प्रति एकर मदत.",
      ta: "நெற்பயிருக்கு பதிலாக மக்காச்சோளம், பருத்தி பயிரிட ஏக்கருக்கு ₹7,000 மானியம்.",
      kn: "ಭತ್ತದ ಬದಲಿಗೆ ಮೆಕ್ಕೆಜೋಳ, ಹತ್ತಿ ಬೆಳೆಯುವ ರೈತರಿಗೆ ಎಕರೆಗೆ ₹7,000 ಪ್ರೋತ್ಸಾಹಧನ."
    },
    benefit: "₹7,000 / acre direct financial grant for switching from paddy",
    eligibility: {
      en: "Farmers in Haryana who cultivated paddy in the previous year and shift to alternative crops.",
      te: "గత సంవత్సరం వరి పండించి, ఈ సంవత్సరం ప్రత్యామ్నాయ పంటలకు మారిన హర్యానా రైతులు.",
      hi: "हरियाणा के किसान जिन्होंने पिछले वर्ष धान उगाया था और अब वैकल्पिक फसलें बोई हैं।",
      mr: "मागील वर्षी भात पिकवून यंदा पर्यायी पीक घेणारे शेतकरी.",
      ta: "முந்தைய ஆண்டு நெல் பயிரிட்டு மாற்றுப் பயிருக்கு மாறும் விவசாயிகள்.",
      kn: "ಹಿಂದಿನ ವರ್ಷ ಭತ್ತ ಬೆಳೆದು ಈಗ ಪರ್ಯಾಯ ಬೆಳೆಗೆ ಬದಲಾದ ರೈತರು."
    },
    documents: ["Aadhaar Card", "MFMB Registration indicating crop shift", "Khasra Number proof", "Bank Passbook"],
    deadline: "Annual registration closes in July-August on fasal.haryana.gov.in",
    claim_window: "Satellite remote sensing and physical field ground-truthing in August-September",
    source_url: "https://fasal.haryana.gov.in/",
    last_verified: "2026-08-15"
  },
  // --- ODISHA ---
  {
    scheme_id: "od_kalia",
    name: {
      en: "Odisha KALIA Scheme (Farmer & Laborer Assistance)",
      te: "ఒడిశా కాలియా పథకం (రైతులు & వ్యవసాయ కూలీల సాయం)",
      hi: "ओडिशा कालिया योजना (कृषक आजीविका एवं आय सहायता)",
      mr: "ओडिशा कालिया योजना",
      ta: "ஒடிசா காலியா திட்டம்",
      kn: "ಒಡಿಶಾ ಕಾಲಿಯಾ ಯೋಜನೆ (ರೈತ ಮತ್ತು ಕೃಷಿ ಕಾರ್ಮಿಕರ ನೆರವು)"
    },
    level: "State",
    state: "Odisha",
    category: "income_support",
    description: {
      en: "₹10,000/year for small & marginal farmers, plus ₹12,500 one-time livelihood financial grant for landless agricultural laborers for goat rearing, poultry, etc.",
      te: "చిన్న, సన్నకారు రైతులకు సంవత్సరానికి ₹10,000 మరియు భూమిలేని వ్యవసాయ కూలీలకు ₹12,500 జీవనోపాధి గ్రాంట్.",
      hi: "लघु एवं सीमांत किसानों को ₹10,000 प्रति वर्ष, तथा भूमिहीन कृषि मजदूरों को बकरी पालन/मुर्गी पालन हेतु ₹12,500 की आजीविका सहायता।",
      mr: "अल्पभूधारक शेतकऱ्यांना दरवर्षी ₹10,000 आणि भूमिहीन शेतमजुरांना ₹12,500 उपजीविका मदत.",
      ta: "சிறு விவசாயிகளுக்கு ₹10,000 மற்றும் நிலமற்ற விவசாய கூலிகளுக்கு ₹12,500 உதவி.",
      kn: "ಸಣ್ಣ ರೈತರಿಗೆ ವರ್ಷಕ್ಕೆ ₹10,000 ಮತ್ತು ಭೂಹೀನ ಕೃಷಿ ಕಾರ್ಮಿಕರಿಗೆ ₹12,500 ಜೀವನೋಪಾಯ ನೆರವು."
    },
    benefit: "₹10,000/yr for farmers + ₹12,500 for Landless Agricultural Laborers",
    eligibility: {
      en: "Small and marginal farmers and landless agricultural households in Odisha. (Large landholders > 5 acres excluded).",
      te: "ఒడిశాలోని చిన్న, సన్నకారు రైతులు మరియు భూమిలేని వ్యవసాయ కుటుంబాలు.",
      hi: "ओडिशा के लघु एवं सीमांत किसान और भूमिहीन कृषि मजदूर परिवार। (5 एकड़ से अधिक भूमि वाले बाहर)।",
      mr: "ओडिशातील अल्पभूधारक शेतकरी व भूमिहीन शेतमजूर कुटुंबे.",
      ta: "ஒடிசாவின் சிறு விவசாயிகள் மற்றும் நிலமற்ற தொழிலாளர்கள்.",
      kn: "ಒಡಿಶಾದ ಸಣ್ಣ ರೈತರು ಮತ್ತು ಭೂಹೀನ ಕೃಷಿ ಕಾರ್ಮಿಕ ಕುಟುಂಬಗಳು."
    },
    documents: ["Aadhaar Card", "Ration/NFSA Card", "RoR Patta OR MGNREGA Job Card (for landless)", "Bank Details"],
    deadline: "Continuous enrollment verified through the Krushak Odisha portal",
    claim_window: "e-KYC and grievance redressal available at Gram Panchayat headquarters",
    source_url: "https://kalia.odisha.gov.in/",
    last_verified: "2026-09-12"
  },
  // --- WEST BENGAL ---
  {
    scheme_id: "wb_krishak_bandhu",
    name: {
      en: "West Bengal Krishak Bandhu (Income & Demise Relief)",
      te: "పశ్చిమ బెంగాల్ కృషక్ బంధు పథకం",
      hi: "पश्चिम बंगाल कृषक बंधु योजना",
      mr: "पश्चिम बंगाल कृषक बंधू योजना",
      ta: "மேற்கு வங்காளம் கிருஷக் பந்து திட்டம்",
      kn: "ಪಶ್ಚಿಮ ಬಂಗಾಳ ಕೃಷಕ್ ಬಂಧು ಯೋಜನೆ"
    },
    level: "State",
    state: "West Bengal",
    category: "income_support",
    description: {
      en: "Assured ₹10,000/year (min ₹4,000/yr for small land) in 2 seasons for all farmers and sharecroppers (Bargadars), plus ₹2 Lakh life insurance demise benefit.",
      te: "రైతులు మరియు కౌలు రైతులకు (బర్గదార్లు) సంవత్సరానికి ₹10,000 సాయం మరియు రైతు మరణిస్తే కుటుంబానికి ₹2,00,000 బీమా పరిహారం.",
      hi: "किसानों व बटाईदारों (बर्गदारों) को प्रति वर्ष ₹10,000 की सुनिश्चित सहायता (न्यूनतम ₹4,000) तथा मृत्यु होने पर परिवार को ₹2 लाख की बीमा सहायता।",
      mr: "शेतकऱ्यांना खात्रीशीर दरवर्षी ₹10,000 मदत व अपघाती/नैसर्गिक मृत्यूनंतर ₹2 लाख वारसाला.",
      ta: "விவசாயிகளுக்கு ஆண்டுக்கு ₹10,000 உதவி மற்றும் குடும்பத்திற்கு ₹2 லட்சம் காப்பீடு.",
      kn: "ರೈತರಿಗೆ ವರ್ಷಕ್ಕೆ ₹10,000 ಖಚಿತ ನೆರವು ಮತ್ತು ಸಾವಿನ ಸಂದರ್ಭದಲ್ಲಿ ಕುಟುಂಬಕ್ಕೆ ₹2 ಲಕ್ಷ ಪರಿಹಾರ."
    },
    benefit: "Assured ₹10,000/yr (min ₹4,000) + ₹2,00,000 family demise relief (Bargadars covered)",
    eligibility: {
      en: "All farmers and recorded sharecroppers (Bargadars) owning or cultivating land in West Bengal.",
      te: "పశ్చిమ బెంగాల్‌లోని భూ యజమానులు మరియు రికార్డు అయిన కౌలుదారులు (బర్గదార్లు).",
      hi: "पश्चिम बंगाल के सभी भूमिधारक किसान एवं पंजीकृत बटाईदार (बर्गदार)।",
      mr: "पश्चिम बंगालमधील सर्व जमीन मालक व नोंदणीकृत बटाईदार शेतकरी.",
      ta: "மேற்கு வங்க நில உரிமையாளர்கள் மற்றும் பதிவு செய்யப்பட்ட குத்தகை விவசாயிகள்.",
      kn: "ಪಶ್ಚಿಮ ಬಂಗಾಳದ ಭೂಮಾಲೀಕರು ಮತ್ತು ದಾಖಲಿತ ಗೇಣಿದಾರರು (ಬರ್ಗಾದಾರರು)."
    },
    documents: ["Aadhaar Card", "Voter ID (EPIC)", "Khatian / RoR OR Bargadar Record", "Bank Passbook"],
    deadline: "Disbursed in 2 seasonal tranches: Kharif (June-July) & Rabi (Dec-Jan)",
    claim_window: "Nominee must apply to Assistant Director of Agriculture within 30 days of demise",
    source_url: "https://krishakbandhu.wb.gov.in/",
    last_verified: "2026-09-15"
  },
  {
    scheme_id: "wb_bangla_shasya_bima",
    name: {
      en: "West Bengal Bangla Shasya Bima (100% Free Insurance)",
      te: "పశ్చిమ బెంగాల్ బంగ్లా శస్య బీమా (ఉచిత పంటల బీమా)",
      hi: "पश्चिम बंगाल बांग्ला शस्य बीमा (100% मुफ्त फसल बीमा)",
      mr: "पश्चिम बंगाल बांग्ला शस्य विमा (मोफत पीक विमा)",
      ta: "மேற்கு வங்காளம் பங்களா சஸ்ய பீமா",
      kn: "ಪಶ್ಚಿಮ ಬಂಗಾಳ ಬಾಂಗ್ಲಾ ಶಸ್ಯ ಬಿಮಾ (ಉಚಿತ ಬೆಳೆ ವಿಮೆ)"
    },
    level: "State",
    state: "West Bengal",
    category: "insurance",
    description: {
      en: "100% state-funded crop insurance where the Government of West Bengal pays the entire premium for all food and oilseed crops.",
      te: "రైతులపై పైసా కూడా భారం లేకుండా 100% రాష్ట్ర ప్రభుత్వ ఖర్చుతోనే ఉచిత పంటల బీమా పథకం.",
      hi: "100% राज्य सरकार द्वारा वित्तपोषित फसल बीमा योजना। किसानों को ₹0 प्रीमियम देना होता है।",
      mr: "१००% मोफत पीक विमा. संपूर्ण हप्ता राज्य सरकार भरते.",
      ta: "100% இலவச பயிர் காப்பீட்டுத் திட்டம்.",
      kn: "100% ಉಚಿತ ಬೆಳೆ ವಿಮೆ. ಸಂಪೂರ್ಣ ಪ್ರೀಮಿಯಂ ರಾಜ್ಯ ಸರ್ಕಾರವೇ ಭರಿಸುತ್ತದೆ."
    },
    benefit: "100% Free Crop Insurance (Zero farmer premium, entirely state funded)",
    eligibility: {
      en: "All farmers and sharecroppers (Bargadars) cultivating notified crops in West Bengal.",
      te: "పశ్చిమ బెంగాల్‌లో పంటలు సాగుచేసే రైతులు మరియు బర్గదార్లు అందరూ.",
      hi: "पश्चिम बंगाल में अधिसूचित फसलें उगाने वाले सभी किसान एवं बटाईदार।",
      mr: "पश्चिम बंगालमधील सर्व शेतकरी व बटाईदार.",
      ta: "மேற்கு வங்கத்தில் அறிவிக்கப்பட்ட பயிர்களை பயிரிடும் விவசாயிகள்.",
      kn: "ಪಶ್ಚಿಮ ಬಂಗಾಳದಲ್ಲಿ ಅಧಿಸೂಚಿತ ಬೆಳೆಗಳನ್ನು ಬೆಳೆಯುವ ಎಲ್ಲಾ ರೈತರು."
    },
    documents: ["Aadhaar Card", "Khatian / Parcha OR Sowing Certificate from Panchayat", "Bank Passbook"],
    deadline: "Kharif cut-off: 31st August / Rabi cut-off: 31st December",
    claim_window: "Direct satellite crop-cutting evaluation, transferred directly via DBT",
    source_url: "https://bsb.karmatha.com/",
    last_verified: "2026-09-10"
  },
  // --- TAMIL NADU ---
  {
    scheme_id: "tn_solar_pump",
    name: {
      en: "Tamil Nadu CM Solar Powered Pump Sets Scheme",
      te: "తమిళనాడు ముఖ్యమంత్రి సోలార్ పంపుసెట్ల పథకం",
      hi: "तमिलनाडु मुख्यमंत्री सोलर पंप सेट योजना (70% सब्सिडी)",
      mr: "तामिळनाडू सौर कृषी पंप योजना",
      ta: "தமிழ்நாடு முதலமைச்சரின் சூரிய சக்தியால் இயங்கும் பம்புசெட்டுகள் திட்டம் (70% மானியம்)",
      kn: "ತಮಿಳುನಾಡು ಮುಖ್ಯಮಂತ್ರಿ ಸೌರ ಪಂಪ್‌ಸೆಟ್ ಯೋಜನೆ"
    },
    level: "State",
    state: "Tamil Nadu",
    category: "irrigation",
    description: {
      en: "70% capital subsidy on standalone solar agriculture pumping systems (up to 10 HP) to provide daytime irrigation without grid power dependency.",
      te: "పగటిపూట నిరంతరాయ సేద్యం కోసం 10 హెచ్‌పీ వరకు గల సోలార్ పంపుసెట్ల కొనుగోలుపై 70% సబ్సిడీ.",
      hi: "बिजली ग्रिड पर निर्भरता समाप्त करने हेतु 10 एचपी तक के सोलर पंप सेट लगाने पर 70% सरकारी सब्सिडी।",
      mr: "१० एचपी पर्यंतच्या सौर पंपांवर ७०% थेट अनुदान.",
      ta: "பகலில் பாசன வசதி பெற 10 எச்பி வரையிலான சூரிய சக்தி பம்புசெட்டுகளுக்கு 70% அரசு மானியம்.",
      kn: "10 ಹೆಚ್‌ಪಿ ವರೆಗಿನ ಸೌರ ನೀರಾವರಿ ಪಂಪ್‌ಸೆಟ್‌ಗಳಿಗೆ 70% ಸಹಾಯಧನ."
    },
    benefit: "70% subsidy on Solar Agriculture Pump sets up to 10 HP",
    eligibility: {
      en: "Landowning farmers in Tamil Nadu with a viable open well or borewell and no existing free grid connection.",
      te: "బావి లేదా బోరుబావి ఉండి, ఉచిత కరెంట్ కనెక్షన్ లేని తమిళనాడు భూ యజమానులు.",
      hi: "तमिलनाडु के भूमिधारक किसान जिनके पास चालू कुआं/नलकूप है और मुफ्त बिजली कनेक्शन नहीं है।",
      mr: "पाण्याची सोय असणारे व मोफत वीज कनेक्शन नसलेले शेतकरी.",
      ta: "பாசன கிணறு/ஆழ்துளை கிணறு வைத்துள்ள நில உரிமையாளர்கள்.",
      kn: "ಬಾವಿ ಅಥವಾ ಕೊಳವೆ ಬಾವಿ ಹೊಂದಿರುವ ತಮಿಳುನಾಡಿನ ರೈತರು."
    },
    documents: ["Aadhaar Card", "Patta / Chitta Land Extract", "Water source certificate", "Bank Passbook"],
    deadline: "Apply online through Uzhavan App and Agricultural Engineering Dept",
    claim_window: "5-year comprehensive maintenance contract (CMC) verified by Assistant Executive Engineer",
    source_url: "https://aed.tn.gov.in/",
    last_verified: "2026-08-18"
  },
  // --- BIHAR ---
  {
    scheme_id: "br_fasal_sahayata",
    name: {
      en: "Bihar Rajya Fasal Sahayata Yojana (BRFSY)",
      te: "బీహార్ రాజ్య ఫసల్ సహాయత యోజన (ఉచిత పంట నష్ట పరిహారం)",
      hi: "बिहार राज्य फसल सहायता योजना (बीआरएफएसवाई - 100% मुफ्त फसल सहायता)",
      mr: "बिहार राज्य पीक मदत योजना",
      ta: "பீகார் மாநில பயிர் உதவித் திட்டம்",
      kn: "ಬಿಹಾರ ರಾಜ್ಯ ಫಸಲ್ ಸಹಾಯತಾ ಯೋಜನೆ"
    },
    level: "State",
    state: "Bihar",
    category: "insurance",
    description: {
      en: "Universal zero-premium crop loss compensation: pays ₹7,500/ha for yield loss < 20% and ₹10,000/ha for loss > 20%. Open to both landowners and tenant farmers.",
      te: "రూపాయి ప్రీమియం లేకుండా పంట నష్ట పరిహారం: 20% నష్టానికి ₹7,500/హెక్టారు, 20% పైగా నష్టానికి ₹10,000/హెక్టారు.",
      hi: "बिना किसी प्रीमियम के 100% मुफ्त फसल सहायता: 20% तक नुकसान पर ₹7,500/हेक्टेयर तथा 20% से अधिक पर ₹10,000/हेक्टेयर। बटाईदार भी पात्र।",
      mr: "कोणताही हप्ता न भरता मोफत पीक नुकसान भरपाई (प्रति हेक्टरी ₹१०,००० पर्यंत).",
      ta: "பிரீமியம் இல்லாத இலவச பயிர் இழப்பீட்டு உதவி (ஹெக்டேருக்கு ₹10,000 வரை).",
      kn: "ಯಾವುದೇ ಪ್ರೀಮಿಯಂ ಇಲ್ಲದೆ ಬೆಳೆ ನಷ್ಟ ಪರಿಹಾರ (ಪ್ರತಿ ಹೆಕ್ಟೇರ್‌ಗೆ ₹10,000 ವರೆಗೆ)."
    },
    benefit: "Free Crop Loss Compensation up to ₹10,000/ha (Zero premium, tenants covered)",
    eligibility: {
      en: "Landowning farmers (Ryots) and tenant cultivators (Non-Ryots) in Bihar registered on the PACS portal.",
      te: "బీహార్‌లోని భూ యజమానులు (రైతులు) మరియు కౌలు రైతులు (నాన్-రైతులు).",
      hi: "बिहार के रैयत (जमीन मालिक) और गैर-रैयत (बटाईदार/काश्तकार) दोनों किसान।",
      mr: "बिहारमधील जमीन मालक व बटाईदार दोन्ही शेतकरी.",
      ta: "நில உரிமையாளர்கள் மற்றும் குத்தகை விவசாயிகள் இருவருமே தகுதியானவர்கள்.",
      kn: "ಭೂಮಾಲೀಕರು ಮತ್ತು ಗೇಣಿದಾರ ರೈತರು ಇಬ್ಬರೂ ಅರ್ಹರು."
    },
    documents: ["Aadhaar Card", "LPC / Land Receipt (for Ryot) OR Self-declaration (for Non-Ryot tenant)", "Bank Passbook"],
    deadline: "Apply on pacs.bih.nic.in: Kharif cut-off: 31st August / Rabi: 31st January",
    claim_window: "Direct transfer based on Panchayat Crop Cutting Experiments (CCEs)",
    source_url: "https://pacsonline.bih.nic.in/fsy/",
    last_verified: "2026-09-08"
  },
  {
    scheme_id: "br_diesel_anudan",
    name: {
      en: "Bihar Diesel Anudan (Irrigation Fuel Subsidy)",
      te: "బీహార్ డీజిల్ అనుదాన్ (సేద్యం ఇంధన రాయితీ)",
      hi: "बिहार डीजल अनुदान योजना (सिंचाई हेतु ईंधन सब्सिडी)",
      mr: "बिहार डिझेल अनुदान योजना",
      ta: "பீகார் டீசல் மானியத் திட்டம்",
      kn: "ಬಿಹಾರ ಡೀಸೆಲ್ ಸಹಾಯಧನ ಯೋಜನೆ"
    },
    level: "State",
    state: "Bihar",
    category: "irrigation",
    description: {
      en: "Irrigation diesel subsidy during drought: ₹75 per litre (up to ₹750 per acre per irrigation) for running diesel pump sets (up to 3-4 irrigations).",
      te: "వర్షాభావ పరిస్థితుల్లో డీజిల్ పంపుసెట్లకు లీటరుకు ₹75 (ఎకరాకు ₹750) ఇంధన సబ్సిడీ.",
      hi: "सूखे या अल्प वर्षा में डीजल पंपसेट चलाने हेतु ₹75 प्रति लीटर (अधिकतम ₹750 प्रति एकड़ प्रति सिंचाई) की सब्सिडी।",
      mr: "पावसाअभावी डिझेल पंपासाठी प्रति लिटर ₹75 अनुदान.",
      ta: "வறட்சி காலத்தில் பாசன டீசல் பம்புகளுக்கு லிட்டருக்கு ₹75 மானியம்.",
      kn: "ಬರಗಾಲದಲ್ಲಿ ಡೀಸೆಲ್ ಪಂಪ್‌ಸೆಟ್‌ಗಳಿಗೆ ಪ್ರತಿ ಲೀಟರ್‌ಗೆ ₹75 ಇಂಧನ ಸಬ್ಸಿಡಿ."
    },
    benefit: "₹75 / litre (up to ₹750/acre per irrigation) diesel subsidy during dry spells",
    eligibility: {
      en: "Farmers in Bihar cultivating crops using diesel pump sets during rainfall deficit periods.",
      te: "వర్షాలు లేని సమయంలో డీజిల్ పంపులతో సాగుచేసే బీహార్ రైతులు.",
      hi: "बिहार के किसान जो कम वर्षा के दौरान डीजल पंपसेट से सिंचाई करते हैं।",
      mr: "कमी पावसात डिझेल पंपाने सिंचन करणारे शेतकरी.",
      ta: "டீசல் பம்புகள் மூலம் பாசனம் செய்யும் பீகார் விவசாயிகள்.",
      kn: "ಕಡಿಮೆ ಮಳೆಯ ಸಮಯದಲ್ಲಿ ಡೀಸೆಲ್ ಪಂಪ್‌ಸೆಟ್ ಬಳಸುವ ರೈತರು."
    },
    documents: ["Aadhaar Card", "Kisan Registration Number", "Petrol Pump Diesel Cash Memo with Reg Number", "Land Receipt"],
    deadline: "Apply on dbtagriculture.bihar.gov.in during notified dry months",
    claim_window: "Field verification by Agriculture Coordinator within 15 days",
    source_url: "https://dbtagriculture.bihar.gov.in/",
    last_verified: "2026-08-28"
  },
  // --- RAJASTHAN ---
  {
    scheme_id: "rj_tarbandi",
    name: {
      en: "Rajasthan Khet Tarbandi (Farm Fencing Subsidy)",
      te: "రాజస్థాన్ పొలం కంచె సబ్సిడీ (తార్‌బందీ యోజన)",
      hi: "राजस्थान खेत तारबंदी योजना (आवारा पशुओं से सुरक्षा हेतु)",
      mr: "राजस्थान शेत कुंपण योजना (तारबंदी)",
      ta: "ராஜஸ்தான் பண்ணை வேலி மானியத் திட்டம்",
      kn: "ರಾಜಸ್ಥಾನ ಕೃಷಿ ಜಮೀನು ತಂತಿ ಬೇಲಿ ಸಬ್ಸಿಡಿ ಯೋಜನೆ"
    },
    level: "State",
    state: "Rajasthan",
    category: "fencing",
    description: {
      en: "50% to 60% capital grant (up to ₹40,000 - ₹48,000) for erecting barbed-wire farm fencing up to 400 running meters to protect crops from stray cattle and nilgai.",
      te: "అడవి పందులు, రోజ్‌డా (నీల్‌గాయ్), పశువుల నుండి పంటలను కాపాడటానికి ముళ్ళకంచె ఏర్పాటుపై 50% నుండి 60% సబ్సిడీ.",
      hi: "नीलगाय और आवारा पशुओं से फसलों की सुरक्षा के लिए 400 मीटर तक कंटीले तार की बाड़ लगाने पर 50% से 60% (अधिकतम ₹48,000) अनुदान।",
      mr: "रानटी जनावरांपासून पिकांच्या संरक्षणासाठी काटेरी तारेच्या कुंपणासाठी ५०% ते ६०% अनुदान.",
      ta: "விலங்குகளிடமிருந்து பயிர்களைப் பாதுகாக்க கம்பி வேலி அமைக்க 50% முதல் 60% வரை மானியம்.",
      kn: "ಕಾಡು ಪ್ರಾಣಿಗಳಿಂದ ಬೆಳೆ ರಕ್ಷಣೆಗಾಗಿ ಮುಳ್ಳುತಂತಿ ಬೇಲಿ ನಿರ್ಮಿಸಲು 50% ರಿಂದ 60% ಸಹಾಯಧನ."
    },
    benefit: "50% to 60% subsidy (up to ₹40,000 - ₹48,000) for barbed wire fencing",
    eligibility: {
      en: "Farmers in Rajasthan holding minimum 1.5 hectares cultivable land (or group cluster).",
      te: "కనీసం 1.5 హెక్టార్ల భూమి ఉన్న రాజస్థాన్ రైతులు.",
      hi: "राजस्थान के किसान जिनके पास न्यूनतम 1.5 हेक्टेयर कृषि भूमि है (या समूह क्लस्टर)।",
      mr: "किमान १.५ हेक्टर शेतजमीन असलेले शेतकरी.",
      ta: "குறைந்தது 1.5 ஹெக்டேர் நிலம் வைத்துள்ள விவசாயிகள்.",
      kn: "ಕನಿಷ್ಠ 1.5 ಹೆಕ್ಟೇರ್ ಕೃಷಿ ಭೂಮಿ ಹೊಂದಿರುವ ರೈತರು."
    },
    documents: ["Aadhaar / Jan Aadhaar Card", "Jamabandi (Land Record < 6 months old)", "Field Map Trace (Naksha)"],
    deadline: "Apply online on RajKisan Sathi Portal (rajkisan.rajasthan.gov.in)",
    claim_window: "Physical verification by Agriculture Supervisor before and after wire erection",
    source_url: "https://rajkisan.rajasthan.gov.in/",
    last_verified: "2026-09-02"
  },
  // --- GUJARAT ---
  {
    scheme_id: "gj_saat_pagla_khedut",
    name: {
      en: "Gujarat Saat Pagla Khedut Kalyan Na",
      te: "గుజరాత్ సాత్ పగ్లా ఖేడుత్ కళ్యాణ్ పథకం",
      hi: "गुजरात सात पगला खेड़ूत कल्याण ना योजना",
      mr: "गुजरात सात पगला शेतकरी कल्याण योजना",
      ta: "குஜராத் சாத் பக்லா விவசாய திட்டம்",
      kn: "ಗುಜರಾತ್ ಸಾತ್ ಪಗ್ಲಾ ಖೇಡುತ್ ಕಲ್ಯಾಣ ಯೋಜನೆ"
    },
    level: "State",
    state: "Gujarat",
    category: "machinery",
    description: {
      en: "Comprehensive assistance: ₹45,000 subsidy on mini-tractors, ₹900/month (₹10,800/yr) assistance for maintaining one desi cow for natural farming, and farm godowns.",
      te: "మినీ ట్రాక్టర్లపై ₹45,000 సబ్సిడీ, ప్రకృతి వ్యవసాయం చేసే దేశీ ఆవు పోషణకు నెలకు ₹900 (సంవత్సరానికి ₹10,800) సాయం.",
      hi: "मिनी-ट्रैक्टर पर ₹45,000 सब्सिडी, प्राकृतिक खेती हेतु देशी गाय पालन पर ₹900/माह (₹10,800/वर्ष) तथा खेत में गोदाम सब्सिडी।",
      mr: "मिनी ट्रॅक्टरवर ₹45,000 अनुदान, देशी गाय पालनासाठी दरमहा ₹900 मदत.",
      ta: "மினி டிராக்டருக்கு ₹45,000 மானியம் மற்றும் நாட்டு மாடு பராமரிக்க மாதம் ₹900 உதவி.",
      kn: "ಮಿನಿ ಟ್ರಾಕ್ಟರ್‌ಗೆ ₹45,000 ಸಬ್ಸಿಡಿ ಮತ್ತು ನೈಸರ್ಗಿಕ ಕೃಷಿಗಾಗಿ ದೇಸಿ ಹಸು ನಿರ್ವಹಣೆಗೆ ತಿಂಗಳಿಗೆ ₹900 ಸಹಾಯಧನ."
    },
    benefit: "Mini-tractor subsidy (₹45,000) + Cow maintenance (₹10,800/yr) + Godowns",
    eligibility: {
      en: "Landowning farmers in Gujarat registered on the i-Khedut portal.",
      te: "ఐ-ఖేడుత్ (i-Khedut) పోర్టల్‌లో నమోదైన గుజరాత్ భూ యజమానులు.",
      hi: "आई-खेड़ूत (i-Khedut) पोर्टल पर पंजीकृत गुजरात के भूमिधारक किसान।",
      mr: "आय-खेडूत पोर्टलवर नोंदणी केलेले शेतकरी.",
      ta: "ஐ-கேடுத் இணையதளத்தில் பதிவு செய்த விவசாயிகள்.",
      kn: "ಐ-ಖೇಡುತ್ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನೋಂದಾಯಿತ ಗುಜರಾತ್ ರೈತರು."
    },
    documents: ["Aadhaar Card", "8-A and 7/12 Land Records (AnyRoR)", "Cow Ear-tag Number", "Bank Passbook"],
    deadline: "Apply on ikhedut.gujarat.gov.in during seasonal open windows",
    claim_window: "Verification by Taluka Agricultural Officer before direct DBT payout",
    source_url: "https://ikhedut.gujarat.gov.in/",
    last_verified: "2026-08-22"
  },
  // --- KERALA ---
  {
    scheme_id: "kl_paddy_royalty",
    name: {
      en: "Kerala Royalty to Wetland Paddy Cultivators",
      te: "కేరళ చిత్తడి నేల వరి రైతుల రాయల్టీ పథకం",
      hi: "केरल वेटलैंड धान कृषक रॉयल्टी योजना",
      mr: "केरळ भातशेती संवर्धन रॉयल्टी योजना",
      ta: "கேரளா நெல் விவசாயிகளுக்கான ராயல்டி திட்டம்",
      kn: "ಕೇರಳ ಗದ್ದೆ ಭತ್ತ ಬೆಳೆಗಾರರ ರಾಯಲ್ಟಿ ಯೋಜನೆ"
    },
    level: "State",
    state: "Kerala",
    category: "income_support",
    description: {
      en: "Annual cash royalty of ₹3,000 per hectare directly deposited to bank accounts of farmers cultivating paddy in registered wetlands to conserve ecology.",
      te: "పర్యావరణ పరిరక్షణ మరియు వరి సాగును ప్రోత్సహించేందుకు చిత్తడి నేలల్లో వరి పండించే రైతులకు హెక్టారుకు ₹3,000 వార్షిక రాయల్టీ.",
      hi: "पर्यावरण और भूजल संरक्षण हेतु पंजीकृत वेटलैंड (निलम) में धान की खेती करने वाले किसानों को ₹3,000 प्रति हेक्टेयर वार्षिक रॉयल्टी।",
      mr: "भाताची शेती टिकवून ठेवण्यासाठी प्रति हेक्टरी ₹3,000 वार्षिक रॉयल्टी मदत.",
      ta: "நெல் சாகுபடியை பாதுகாப்பதற்காக ஹெக்டேருக்கு ₹3,000 வருடாந்திர ராயல்டி.",
      kn: "ಪರಿಸರ ರಕ್ಷಣೆಗಾಗಿ ನೋಂದಾಯಿತ ಗದ್ದೆಗಳಲ್ಲಿ ಭತ್ತ ಬೆಳೆಯುವ ರೈತರಿಗೆ ಪ್ರತಿ ಹೆಕ್ಟೇರ್‌ಗೆ ₹3,000 ವಾರ್ಷಿಕ ರಾಯಧನ."
    },
    benefit: "₹3,000 / hectare annual direct cash royalty for wetland paddy cultivation",
    eligibility: {
      en: "Farmers and Padasekhara Samithi members cultivating paddy on registered wetland fields in Kerala.",
      te: "కేరళలోని రిజిస్టర్ అయిన చిత్తడి నేలల్లో వరి పండించే రైతులు.",
      hi: "केरल के किसान जो डेटा बैंक में पंजीकृत वेटलैंड में धान की खेती कर रहे हैं।",
      mr: "नोंदणीकृत पाणथळ जमिनीत भात शेती करणारे केरळमधील शेतकरी.",
      ta: "கேரளாவில் நெல் பயிரிடும் நில உரிமையாளர்கள் மற்றும் குத்தகைதாரர்கள்.",
      kn: "ದಾಖಲಿತ ಗದ್ದೆಗಳಲ್ಲಿ ಭತ್ತ ಬೆಳೆಯುವ ಕೇರಳದ ರೈತರು."
    },
    documents: ["Aadhaar Card", "Land Tax Receipt showing Wetland / Nilam classification", "Bank Passbook"],
    deadline: "Apply seasonally on aims.kerala.gov.in (AIMS portal)",
    claim_window: "Field verification by Agricultural Officer of local Krishi Bhavan",
    source_url: "https://aims.kerala.gov.in/",
    last_verified: "2026-08-12"
  }
];

// All 36 Indian States & Union Territories
const ALL_STATES_UT = [
  "Andhra Pradesh",
  "Arunachal Pradesh",
  "Assam",
  "Bihar",
  "Chhattisgarh",
  "Goa",
  "Gujarat",
  "Haryana",
  "Himachal Pradesh",
  "Jharkhand",
  "Karnataka",
  "Kerala",
  "Madhya Pradesh",
  "Maharashtra",
  "Manipur",
  "Meghalaya",
  "Mizoram",
  "Nagaland",
  "Odisha",
  "Punjab",
  "Rajasthan",
  "Sikkim",
  "Tamil Nadu",
  "Telangana",
  "Tripura",
  "Uttar Pradesh",
  "Uttarakhand",
  "West Bengal",
  "Andaman and Nicobar Islands",
  "Chandigarh",
  "Dadra and Nagar Haveli and Daman and Diu",
  "Delhi",
  "Jammu and Kashmir",
  "Ladakh",
  "Lakshadweep",
  "Puducherry"
];

// Multilingual UI Labels
const UI_TRANSLATIONS = {
  en: {
    choose_lang: "🌐 Choose Language",
    app_title: "Kisan Setu",
    app_subtitle: "Unified Farmer Scheme & Subsidy Assistant",
    hero_title: "Find Government Schemes & Subsidies for Your Farm",
    hero_desc: "Select your State or Union Territory below to discover all eligible State Subsidies alongside Pan-India Central Government Schemes.",
    select_state_label: "Select Your State / Union Territory",
    select_state_placeholder: "🔍 Type or choose your State (e.g. Telangana, Maharashtra, UP, Punjab)...",
    no_state_prompt: "Please select your State above to view available schemes and subsidies.",
    state_selected_banner: "Showing Agricultural Schemes for",
    badge_central: "🇮🇳 Central Govt Scheme",
    badge_state: "🏛️ State Scheme",
    tab_all: "All Schemes",
    tab_state: "State Schemes",
    tab_central: "Central Schemes",
    filter_type: "Scheme Type",
    filter_eligibility: "Farmer Type",
    search_placeholder: "🔍 Search schemes by name, crop, or keyword (e.g. Paddy, Tractor, Insurance, Loan)...",
    benefit_label: "Key Benefit",
    eligibility_label: "Eligibility Summary",
    documents_label: "Required Documents",
    deadline_label: "Deadlines & Reporting Window",
    apply_button: "Official Portal / Apply Link",
    last_verified_label: "Last Verified",
    no_results: "No schemes match your active filter or search query. Try clearing filters.",
    clear_filters: "Clear Filters",
    emergency_rule: "Emergency Rule"
  },
  te: {
    choose_lang: "🌐 భాషను ఎంచుకోండి",
    app_title: "కిసాన్ సేతు / రైతు సహాయత",
    app_subtitle: "రైతు ప్రభుత్వ పథకాలు & రాయితీల సహాయకుడు",
    hero_title: "మీ వ్యవసాయానికి ప్రభుత్వ రాయితీలు & పథకాలను తెలుసుకోండి",
    hero_desc: "మీ రాష్ట్రం లేదా కేంద్రపాలిత ప్రాంతాన్ని ఎంచుకుని, రాష్ట్ర ప్రభుత్వ పథకాలు మరియు కేంద్ర పథకాలను ఒకే చోట చూడండి.",
    select_state_label: "మీ రాష్ట్రం / కేంద్రపాలిత ప్రాంతాన్ని ఎంచుకోండి",
    select_state_placeholder: "🔍 మీ రాష్ట్రాన్ని ఎంచుకోండి (ఉదా: తెలంగాణ, ఆంధ్రప్రదేశ్, మహారాష్ట్ర)...",
    no_state_prompt: "పథకాలు మరియు రాయితీలను చూడటానికి దయచేసి పైన మీ రాష్ట్రాన్ని ఎంచుకోండి.",
    state_selected_banner: "రైతు పథకాలు చూపబడుతున్న రాష్ట్రం",
    badge_central: "🇮🇳 కేంద్ర ప్రభుత్వ పథకం",
    badge_state: "🏛️ రాష్ట్ర ప్రభుత్వ పథకం",
    tab_all: "అన్ని పథకాలు",
    tab_state: "రాష్ట్ర పథకాలు",
    tab_central: "కేంద్ర పథకాలు",
    filter_type: "పథకం రకం",
    filter_eligibility: "రైతు వర్గం",
    search_placeholder: "🔍 పేరు లేదా పంట ద్వారా వెతకండి (ఉదా: వరి, పత్తి, ట్రాక్టర్, బీమా, రుణం)...",
    benefit_label: "ప్రధాన ప్రయోజనం",
    eligibility_label: "అర్హత వివరాలు",
    documents_label: "కావలసిన పత్రాలు",
    deadline_label: "గడువు & క్లెయిమ్ సమయం",
    apply_button: "అధికారిక వెబ్‌సైట్ / దరఖాస్తు",
    last_verified_label: "చివరిగా ధృవీకరించిన తేదీ",
    no_results: "మీరు వెతికిన వివరాలకు సరిపడే పథకాలు లభించలేదు. ఫిల్టర్లు తీసివేసి మళ్ళీ ప్రయత్నించండి.",
    clear_filters: "ఫిల్టర్లు క్లియర్ చేయండి",
    emergency_rule: "అత్యవసర గడువు"
  },
  hi: {
    choose_lang: "🌐 भाषा चुनें",
    app_title: "किसान सेतु",
    app_subtitle: "एकीकृत किसान योजना एवं सब्सिडी सहायक",
    hero_title: "अपने खेत के लिए सरकारी योजनाएं और सब्सिडी खोजें",
    hero_desc: "अपने राज्य या केंद्र शासित प्रदेश का चयन करें और राज्य व केंद्र सरकार की सभी कृषि योजनाओं की पूरी जानकारी प्राप्त करें।",
    select_state_label: "अपना राज्य / केंद्र शासित प्रदेश चुनें",
    select_state_placeholder: "🔍 राज्य चुनें (उदा: उत्तर प्रदेश, मध्य प्रदेश, बिहार, पंजाब, महाराष्ट्र)...",
    no_state_prompt: "उपलब्ध कृषि योजनाएं और सब्सिडी देखने के लिए कृपया ऊपर अपना राज्य चुनें।",
    state_selected_banner: "कृषि योजनाएं प्रदर्शित राज्य",
    badge_central: "🇮🇳 केंद्र सरकार की योजना",
    badge_state: "🏛️ राज्य सरकार की योजना",
    tab_all: "सभी योजनाएं",
    tab_state: "राज्य योजनाएं",
    tab_central: "केंद्रीय योजनाएं",
    filter_type: "योजना का प्रकार",
    filter_eligibility: "किसान श्रेणी",
    search_placeholder: "🔍 नाम, फसल या कीवर्ड से खोजें (उदा: धान, गेहूं, ट्रैक्टर, बीमा, केसीसी)...",
    benefit_label: "मुख्य लाभ",
    eligibility_label: "पात्रता विवरण",
    documents_label: "आवश्यक दस्तावेज",
    deadline_label: "आवेदन समय-सीमा व दावा विंडो",
    apply_button: "आधिकारिक पोर्टल / आवेदन लिंक",
    last_verified_label: "अंतिम सत्यापन",
    no_results: "आपकी खोज के अनुसार कोई योजना नहीं मिली। कृपया फ़िल्टर साफ़ करके पुनः प्रयास करें।",
    clear_filters: "फ़िल्टर हटाएं",
    emergency_rule: "आपातकालीन नियम"
  },
  mr: {
    choose_lang: "🌐 भाषा निवडा",
    app_title: "किसान सेतू",
    app_subtitle: "शेतकरी सरकारी योजना व अनुदान सहाय्यक",
    hero_title: "आपल्या शेतीसाठी सरकारी योजना आणि अनुदान शोधा",
    hero_desc: "आपले राज्य निवडा आणि राज्य व केंद्र सरकारच्या सर्व शेतकरी योजनांची सविस्तर माहिती मिळवा.",
    select_state_label: "आपले राज्य / केंद्रशासित प्रदेश निवडा",
    select_state_placeholder: "🔍 राज्य निवडा (उदा: महाराष्ट्र, गुजरात, कर्नाटक)...",
    no_state_prompt: "उपलब्ध योजना आणि अनुदान पाहण्यासाठी कृपया वर आपले राज्य निवडा.",
    state_selected_banner: "शेती योजना दाखवत आहे",
    badge_central: "🇮🇳 केंद्र सरकारची योजना",
    badge_state: "🏛️ राज्य सरकारची योजना",
    tab_all: "सर्व योजना",
    tab_state: "राज्य योजना",
    tab_central: "केंद्रीय योजना",
    filter_type: "योजनेचा प्रकार",
    filter_eligibility: "शेतकरी प्रवर्ग",
    search_placeholder: "🔍 नाव किंवा पिकाने शोधा (उदा: कापूस, सोयाबीन, ट्रॅक्टर, पीक विमा)...",
    benefit_label: "प्रमुख लाभ",
    eligibility_label: "पात्रता अटी",
    documents_label: "आवश्यक कागदपत्रे",
    deadline_label: "मुदत व तक्रार निवारण विंडो",
    apply_button: "अधिकृत पोर्टल / अर्ज करा",
    last_verified_label: "शेवटची पडताळणी",
    no_results: "कोणतीही योजना जुळली नाही. कृपया फिल्टर क्लिअर करा.",
    clear_filters: "फिल्टर काढा",
    emergency_rule: "तातडीचा नियम"
  },
  ta: {
    choose_lang: "🌐 மொழியைத் தேர்வுசெய்க",
    app_title: "கிசான் சேது",
    app_subtitle: "ஒருங்கிணைந்த உழவர் திட்டங்கள் & மானிய வழிகாட்டி",
    hero_title: "உங்கள் பண்ணைக்கான அரசு மானியங்கள் மற்றும் திட்டங்களை கண்டறியுங்கள்",
    hero_desc: "உங்கள் மாநிலத்தைத் தேர்வுசெய்து, மாநில மற்றும் மத்திய அரசின் திட்டங்களை ஒரே இடத்தில் பாருங்கள்.",
    select_state_label: "உங்கள் மாநிலத்தைத் தேர்ந்தெடுக்கவும்",
    select_state_placeholder: "🔍 உங்கள் மாநிலத்தைத் தேர்ந்தெடுக்கவும் (எ.கா: தமிழ்நாடு, கேரளா)...",
    no_state_prompt: "மானியங்களைக் காண மேலே உள்ள பட்டியலில் உங்கள் மாநிலத்தைத் தேர்ந்தெடுக்கவும்.",
    state_selected_banner: "விவசாய திட்டங்கள் காட்டப்படும் மாநிலம்",
    badge_central: "🇮🇳 மத்திய அரசு திட்டம்",
    badge_state: "🏛️ மாநில அரசு திட்டம்",
    tab_all: "அனைத்து திட்டங்கள்",
    tab_state: "மாநில திட்டங்கள்",
    tab_central: "மத்திய திட்டங்கள்",
    filter_type: "திட்ட வகை",
    filter_eligibility: "விவசாயி வகை",
    search_placeholder: "🔍 பெயர் அல்லது பயிர் மூலம் தேடுங்கள் (எ.கா: நெல், சோலார், காப்பீடு)...",
    benefit_label: "முக்கிய பயன்",
    eligibility_label: "தகுதி விவரம்",
    documents_label: "தேவையான ஆவணங்கள்",
    deadline_label: "விண்ணப்பக் காலக்கெடு",
    apply_button: "அதிகாரப்பூர்வ தளம் / விண்ணப்பிக்க",
    last_verified_label: "கடைசியாக சரிபார்க்கப்பட்டது",
    no_results: "பொருத்தமான திட்டங்கள் எதுவும் காணப்படவில்லை.",
    clear_filters: "வடிகட்டிகளை அழிக்கவும்",
    emergency_rule: "அவசர விதி"
  },
  kn: {
    choose_lang: "🌐 ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    app_title: "ಕಿಸಾನ್ ಸೇತು",
    app_subtitle: "ರೈತ ಯೋಜನೆಗಳು ಮತ್ತು ಸಬ್ಸಿಡಿ ಸಹಾಯಕ",
    hero_title: "ನಿಮ್ಮ ಕೃಷಿಗಾಗಿ ಸರ್ಕಾರಿ ಸಬ್ಸಿಡಿಗಳು ಮತ್ತು ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ",
    hero_desc: "ನಿಮ್ಮ ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ ಮತ್ತು ರಾಜ್ಯ ಹಾಗೂ ಕೇಂದ್ರ ಸರ್ಕಾರದ ಕೃಷಿ ಯೋಜನೆಗಳನ್ನು ಒಂದೇ ವೇದಿಕೆಯಲ್ಲಿ ಪಡೆಯಿರಿ.",
    select_state_label: "ನಿಮ್ಮ ರಾಜ್ಯ / ಕೇಂದ್ರಾಡಳಿತ ಪ್ರದೇಶವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    select_state_placeholder: "🔍 ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ (ಉದಾ: ಕರ್ನಾಟಕ, ತೆಲಂಗಾಣ, ಮಹಾರಾಷ್ಟ್ರ)...",
    no_state_prompt: "ಯೋಜನೆಗಳು ಮತ್ತು ಸಬ್ಸಿಡಿಗಳನ್ನು ನೋಡಲು ದಯವಿಟ್ಟು ಮೇಲೆ ನಿಮ್ಮ ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
    state_selected_banner: "ಕೃಷಿ ಯೋಜನೆಗಳನ್ನು ಪ್ರದರ್ಶಿಸುತ್ತಿರುವ ರಾಜ್ಯ",
    badge_central: "🇮🇳 ಕೇಂದ್ರ ಸರ್ಕಾರದ ಯೋಜನೆ",
    badge_state: "🏛️ ರಾಜ್ಯ ಸರ್ಕಾರದ ಯೋಜನೆ",
    tab_all: "ಎಲ್ಲಾ ಯೋಜನೆಗಳು",
    tab_state: "ರಾಜ್ಯ ಯೋಜನೆಗಳು",
    tab_central: "ಕೇಂದ್ರ ಯೋಜನೆಗಳು",
    filter_type: "ಯೋಜನೆಯ ಪ್ರಕಾರ",
    filter_eligibility: "ರೈತರ ವರ್ಗ",
    search_placeholder: "🔍 ಹೆಸರು ಅಥವಾ ಬೆಳೆಯ ಮೂಲಕ ಹುಡುಕಿ (ಉದಾ: ಭತ್ತ, ರಾಗಿ, ಟ್ರಾಕ್ಟರ್, ವಿಮೆ)...",
    benefit_label: "ಪ್ರಮುಖ ಪ್ರಯೋಜನ",
    eligibility_label: "ಅರ್ಹತೆಯ ಸಾರಾಂಶ",
    documents_label: "ಅಗತ್ಯವಿರುವ ದಾಖಲೆಗಳು",
    deadline_label: "ಕೊನೆಯ ದಿನಾಂಕ ಮತ್ತು ಸಮಯ",
    apply_button: "ಅಧಿಕೃತ ಪೋರ್ಟಲ್ / ಅರ್ಜಿ ಸಲ್ಲಿಸಿ",
    last_verified_label: "ಕೊನೆಯ ಪರಿಶೀಲನೆ",
    no_results: "ಯಾವುದೇ ಯೋಜನೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ಫಿಲ್ಟರ್ ತೆರವುಗೊಳಿಸಿ.",
    clear_filters: "ಫಿಲ್ಟರ್‌ಗಳನ್ನು ತೆರವುಗೊಳಿಸಿ",
    emergency_rule: "ತುರ್ತು ನಿಯಮ"
  }
};


const WATER_SAVING_SCHEMES_DATA = [
  {
    "scheme_id": "PMKSY_PDMC",
    "name": "PMKSY - Per Drop More Crop (Micro Irrigation Drip & Sprinkler)",
    "level": "Central & Pan-India State Top-Up",
    "category": "Micro Irrigation Subsidy (Drip & Sprinkler)",
    "implementing_agency": "Ministry of Agriculture & Farmers Welfare & State Horticulture/Agriculture Depts",
    "target_beneficiaries": "Small, Marginal and Other Farmers across all 28 Indian States & 8 UTs",
    "applicable_states": [
      "All States",
      "Telangana",
      "Andhra Pradesh",
      "Maharashtra",
      "Karnataka",
      "Gujarat",
      "Tamil Nadu",
      "Haryana",
      "Punjab",
      "Rajasthan",
      "Madhya Pradesh",
      "Uttar Pradesh"
    ],
    "subsidy_rules": {
      "small_and_marginal_farmers": "55% Central/State baseline (up to 90% in Telangana TSMIP, AP, and TN; 100% for SC/ST)",
      "other_farmers": "45% baseline (up to 80% in progressive states)",
      "sc_st_farmers": "90% to 100% subsidy depending on state top-up guidelines"
    },
    "eligible_systems": [
      "Drip Irrigation System (Inline & Online)",
      "Micro Sprinkler & Mini Sprinkler Systems",
      "Portable & Semi-Permanent Sprinkler Sets",
      "Rain-gun Sprinkler Units"
    ],
    "water_savings_potential": "40% to 60% water savings compared to traditional flood irrigation; 20-30% yield boost",
    "eligibility_criteria": [
      "Cultivable land holding with functional water source (borewell, open well, or farm pond)",
      "Electricity connection or solar pump setup",
      "Valid RoR (Pahani / Dharani / Patta Passbook / 7/12 / Khasra)",
      "One-time benefit per survey land holding for 7 years"
    ],
    "documents_required": [
      "Aadhaar Card copy",
      "Land Record (Pahani / 1B / RoR / 7/12 / Khasra-Khatauni)",
      "Bank Passbook showing active IFSC",
      "Soil & Water Test Report (where mandated)",
      "Caste Certificate (for SC/ST subsidy tier)"
    ],
    "current_status": "Active pan-India under revised PMKSY 2.0 framework",
    "portal_url": "https://pmksy.gov.in",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "PMKSY_HKKP",
    "name": "PMKSY - Har Khet Ko Pani (Groundwater & Surface Minor Irrigation)",
    "level": "Central Scheme",
    "category": "Assured Irrigation & Water Body Renovation",
    "implementing_agency": "Ministry of Jal Shakti & State Water Resources Departments",
    "target_beneficiaries": "Cultivators in command areas, rainfed gaps, and water-stressed assessment units",
    "applicable_states": [
      "All States"
    ],
    "subsidy_rules": {
      "community_irrigation": "Up to 60% Central grant for surface minor irrigation lift projects and community tank command development",
      "individual_groundwater": "Targeted groundwater extraction units for small & marginal farmers in safe assessment units"
    },
    "eligible_systems": [
      "Repair, Renovation and Restoration (RRR) of traditional water bodies / village tanks",
      "Surface Minor Irrigation (SMI) lift channels",
      "Community tube-wells in non-overexploited blocks"
    ],
    "water_savings_potential": "Revives localized aquifer recharge; eliminates tail-end canal water starvation",
    "eligibility_criteria": [
      "Land located within notified minor irrigation command zone or safe groundwater block",
      "Water Users Association (WUA) or Panchayat participatory membership"
    ],
    "documents_required": [
      "Panchayat NOC",
      "Land ownership extract (Khatauni / RoR)",
      "Aadhaar of beneficiary group"
    ],
    "current_status": "Active across identified command clusters",
    "portal_url": "https://pmksy.gov.in/hkkp/",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "PMKSY_WDC",
    "name": "PMKSY - Watershed Development Component (WDC 2.0 / Ridge-to-Valley)",
    "level": "Central Scheme",
    "category": "Soil Moisture & Rainwater Harvesting Infrastructure",
    "implementing_agency": "Department of Land Resources (DoLR), Ministry of Rural Development",
    "target_beneficiaries": "Rainfed, dryland, and degraded land agricultural communities",
    "applicable_states": [
      "All States",
      "Telangana",
      "Andhra Pradesh",
      "Karnataka",
      "Maharashtra",
      "Madhya Pradesh",
      "Rajasthan"
    ],
    "subsidy_rules": {
      "community_and_individual_structures": "100% grant funded for community check-dams, percolation tanks, and continuous contour trenches; 70-80% for individual on-farm ponds"
    },
    "eligible_systems": [
      "Earthen Check Dams & Masonry Weirs",
      "Percolation Tanks & Farm Ponds (Khet Talab)",
      "Loose Boulder Structures & Gabions",
      "Sub-surface dykes in stream beds"
    ],
    "water_savings_potential": "Increases localized groundwater table by 1.5 to 3.0 meters; traps 100% of monsoon runoff",
    "eligibility_criteria": [
      "Land situated within notified micro-watershed project area",
      "Willingness to contribute community maintenance labor/share"
    ],
    "documents_required": [
      "Gram Sabha resolution extract",
      "Survey parcel coordinates",
      "Aadhaar Card"
    ],
    "current_status": "Active under WDC-PMKSY 2.0 (2021-2026)",
    "portal_url": "https://dolr.gov.in/programmes-schemes/wdc-pmksy",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "PM_KUSUM_A",
    "name": "PM-KUSUM Component A (Decentralized Ground/Stilt Mounted Solar Plants 500kW to 2MW)",
    "level": "Central Scheme",
    "category": "Renewable Energy Farmer Power Producer",
    "implementing_agency": "MNRE & State Electricity Distribution Companies (DISCOMs)",
    "target_beneficiaries": "Individual farmers, FPOs, Cooperatives, and Panchayats with barren, fallow, or pasture land within 5 km of 33/11 kV substations",
    "applicable_states": [
      "All States",
      "Rajasthan",
      "Maharashtra",
      "Gujarat",
      "Madhya Pradesh",
      "Haryana",
      "Telangana"
    ],
    "subsidy_rules": {
      "tariff_support": "DISCOM buys power for 25 years at pre-fixed feed-in tariff (approx ₹3.10 - ₹3.30/unit); farmer earns steady ₹1.5 - ₹2.5 Lakh/acre/year on barren land"
    },
    "eligible_systems": [
      "500 kW to 2 MW Solar PV Plants on barren/cultivable land (stilt mounting allows dual farming)"
    ],
    "water_savings_potential": "Monetizes water-parched unproductive land with solar farming; zero water required for power generation",
    "eligibility_criteria": [
      "Barren / cultivable land within 5 km radius of rural 33/11 kV substation",
      "Title deed ownership or 25-year registered lease"
    ],
    "documents_required": [
      "Land Registry / RoR",
      "Substation connectivity clearance from DISCOM",
      "Aadhaar & PAN Card",
      "Bank Account details"
    ],
    "current_status": "Active across participating state DISCOM tenders",
    "portal_url": "https://pmkusum.mnre.gov.in",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "PM_KUSUM_B",
    "name": "PM-KUSUM Component B (Standalone Off-Grid Solar Agriculture Pumps)",
    "level": "Central Scheme",
    "category": "Solar Energy & Renewable Irrigation",
    "implementing_agency": "Ministry of New and Renewable Energy (MNRE) & State Nodal Agencies (TSREDCO, MEDA, HAREDA, KREDL)",
    "target_beneficiaries": "Individual farmers with agricultural land and functional water source without grid electricity connection",
    "applicable_states": [
      "All States"
    ],
    "subsidy_rules": {
      "central_subsidy": "30% Benchmark Cost from MNRE",
      "state_subsidy": "30% State Govt Share (increases to 50% in NE/Hill States/Tribal Regions)",
      "farmer_share": "10% to 40% (remaining can be financed through bank loans under Agri Infrastructure Fund)"
    },
    "eligible_systems": [
      "3 HP, 5 HP, 7.5 HP, 10 HP Standalone DC/AC Surface and Submersible Solar Pumps"
    ],
    "water_savings_potential": "Guaranteed daytime uninterrupted irrigation; eliminates diesel pump recurring expenses (₹40,000-60,000/year savings)",
    "eligibility_criteria": [
      "Farmer must own agricultural land with an existing open well, borewell, or farm pond",
      "No existing grid power connection for the applied borewell",
      "Land title clearance and groundwater availability certificate"
    ],
    "documents_required": [
      "Aadhaar Card",
      "Land Ownership Passbook / Pahani / 7/12 / Khasra",
      "Affidavit of No Existing Grid Connection",
      "Bank Account details",
      "Borewell / Source Depth Certificate"
    ],
    "current_status": "Active pan-India; target 14 lakh standalone solar pumps extended through 2026",
    "portal_url": "https://pmkusum.mnre.gov.in",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "PM_KUSUM_C",
    "name": "PM-KUSUM Component C (Solarisation of Grid-Connected Agricultural Pumps & Feeders)",
    "level": "Central Scheme",
    "category": "Solarised Feeder & Net Metering",
    "implementing_agency": "MNRE & State DISCOMs",
    "target_beneficiaries": "Farmers with existing grid-connected electric pump sets and rural agricultural feeders",
    "applicable_states": [
      "All States"
    ],
    "subsidy_rules": {
      "feeder_level_solarisation": "CFA of ₹1.05 Cr/MW for feeder solarisation; DISCOM installs solar plant; farmer gets free daytime solar power",
      "individual_pump_solarisation": "Up to 60% combined subsidy (30% Central + 30% State); farmer sells surplus power back to grid"
    },
    "eligible_systems": [
      "Feeder Level Solarisation (FLS)",
      "Individual Pump Solarisation with Net Metering"
    ],
    "water_savings_potential": "Solar power day-time usage prevents wasteful night flood irrigation; solar earnings incentivize water conservation",
    "eligibility_criteria": [
      "Existing agricultural electricity meter connection",
      "Valid land ownership and operational water pump"
    ],
    "documents_required": [
      "Electricity Bill / Consumer No.",
      "Aadhaar Card",
      "Bank Details",
      "Land Passbook"
    ],
    "current_status": "Active under DISCOM feeder solarisation drives",
    "portal_url": "https://pmkusum.mnre.gov.in",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "TSMIP_TELANGANA",
    "name": "Telangana State Micro Irrigation Project (TSMIP)",
    "level": "Telangana State Scheme",
    "category": "State Micro Irrigation Top-Up Scheme",
    "implementing_agency": "Horticulture Department, Government of Telangana",
    "target_beneficiaries": "All farmers in Telangana cultivating agriculture or horticulture crops",
    "applicable_states": [
      "Telangana"
    ],
    "subsidy_rules": {
      "sc_st_farmers": "100% subsidy (Free drip/sprinkler up to 5 acres)",
      "bc_small_marginal": "90% subsidy (farmer pays only 10% GST/share)",
      "general_small_marginal": "80% subsidy",
      "other_farmers": "50% subsidy up to 12.5 acres max ceiling"
    },
    "eligible_systems": [
      "Drip for Paddy (AWD), Chilli, Cotton, Vegetable & Fruit Orchards",
      "Micro & Raingun Sprinklers for Maize, Groundnut, Pulses"
    ],
    "water_savings_potential": "Reduces groundwater overdraft by 50%; cuts power consumption by 35%",
    "eligibility_criteria": [
      "Farmer in Telangana with Dharani Passbook / Digital RoR",
      "Borewell or canal lift source available"
    ],
    "documents_required": [
      "Dharani Land Passbook",
      "Aadhaar Card linked to Mobile",
      "Bank Account IFSC Passbook",
      "Caste Certificate (MeeSeva issued for SC/ST/BC)"
    ],
    "current_status": "Active with ongoing allocations across all 33 Telangana districts",
    "portal_url": "https://horticulturedept.telangana.gov.in / Rythu Vedika",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "APMIP_ANDHRA_PRADESH",
    "name": "Andhra Pradesh Micro Irrigation Project (APMIP)",
    "level": "Andhra Pradesh State Scheme",
    "category": "Comprehensive Micro Irrigation & Rayalaseema Drought Shield",
    "implementing_agency": "Department of Horticulture, Government of Andhra Pradesh",
    "target_beneficiaries": "Small, marginal, and tenant farmers across all 26 AP districts with special focus on Rayalaseema & Prakasam dry tracts",
    "applicable_states": [
      "Andhra Pradesh"
    ],
    "subsidy_rules": {
      "sc_st_farmers": "100% subsidy for SC/ST farmers up to 5.0 acres",
      "bc_farmers_rayalaseema": "90% subsidy for BC farmers in Rayalaseema & Prakasam districts",
      "other_small_marginal": "90% subsidy for all other small/marginal farmers up to 5 acres; 70% for 5 to 10 acres"
    },
    "eligible_systems": [
      "Inline & Online Drip Irrigation for Horticulture & Sugarcane",
      "Micro-jets & Portable Sprinklers for Groundnut, Bengal Gram, and Millets"
    ],
    "water_savings_potential": "Saves up to 65% groundwater; prevents borewell drying in summer",
    "eligibility_criteria": [
      "Land ownership recorded on Meebhoomi / e-Crop or registered CCRC card for tenant cultivators",
      "Functional borewell or open water point"
    ],
    "documents_required": [
      "Meebhoomi 1B / Pattadar Passbook or CCRC Card",
      "Aadhaar Card copy",
      "Bank Passbook copy",
      "Integrated Caste Certificate"
    ],
    "current_status": "Active across all AP districts with digital registration via Rythu Bharosa Kendras (RBKs)",
    "portal_url": "https://apmip.ap.gov.in",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "MAHA_SHET_TALE",
    "name": "Maharashtra Magel Tyala Shet Tale (Farm Pond On Demand)",
    "level": "Maharashtra State Scheme",
    "category": "Farm Pond Construction & Water Storage",
    "implementing_agency": "Agriculture Department, Government of Maharashtra (MahaDBT)",
    "target_beneficiaries": "Farmers in Maharashtra experiencing dry spells in Vidarbha, Marathwada, and drought-prone talukas",
    "applicable_states": [
      "Maharashtra"
    ],
    "subsidy_rules": {
      "farm_pond_grant": "₹50,000 to ₹75,000 direct DBT grant for farm pond excavation (size 30m x 30m x 3m)",
      "plastic_lining_add_on": "Additional ₹1,00,000 grant under State Plastic Lining Scheme to prevent seepage"
    },
    "eligible_systems": [
      "Individual Farm Pond (Shet Tale) with inlet/outlet channels",
      "Plastic geomembrane film lining (500 micron)"
    ],
    "water_savings_potential": "Stores 15 to 25 lakh liters of rainwater; provides 2-3 life-saving irrigations for cotton & soybean",
    "eligibility_criteria": [
      "Minimum 0.50 hectare (1.25 acre) cultivable land",
      "Technical feasibility certificate from Agriculture Assistant (Krishi Sahayak)"
    ],
    "documents_required": [
      "7/12 Extract and 8-A Extract",
      "Aadhaar Card",
      "Bank Account details",
      "Self-declaration of not owning an existing subsidised pond"
    ],
    "current_status": "Active on MahaDBT portal under Farmer Schemes",
    "portal_url": "https://mahadbt.maharashtra.gov.in",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "MAHA_MSKVY_SOLAR",
    "name": "Maharashtra Mukhyamantri Saur Krushi Vahini Yojana (MSKVY 2.0 / Solar Feeders)",
    "level": "Maharashtra State Scheme",
    "category": "Daytime Solar Power for Agriculture",
    "implementing_agency": "MSEDCL (Mahavitaran) & Energy Department, Maharashtra",
    "target_beneficiaries": "Agricultural electricity consumers and farmers leasing barren land for solar projects",
    "applicable_states": [
      "Maharashtra"
    ],
    "subsidy_rules": {
      "solar_feeder_power": "Provides 100% uninterrupted daytime electricity (8 hours daily) for farm pumps",
      "land_lease_rent": "Farmers leasing land within 5 km of substation receive ₹1,25,000/acre/year guaranteed rent with 3% annual escalation"
    },
    "eligible_systems": [
      "Solar Agriculture Feeders connected directly to rural substations"
    ],
    "water_savings_potential": "Eliminates dangerous nighttime flood watering; enables daytime precision water management",
    "eligibility_criteria": [
      "Agricultural pump consumers connected to MSEDCL rural feeders",
      "Barren land parcel near 33/11kV substations for land lease"
    ],
    "documents_required": [
      "Consumer electricity billing number",
      "7/12 extract",
      "Aadhaar Card"
    ],
    "current_status": "Active mission aiming for 7,000 MW solar capacity by 2026",
    "portal_url": "https://www.mahadiscom.in/solar-mskvy/",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "KARNATAKA_KRISHI_BHAGYA",
    "name": "Karnataka Krishi Bhagya Scheme (Farm Ponds, Polythene Lining & Micro Irrigation)",
    "level": "Karnataka State Scheme",
    "category": "Comprehensive Dryland Rainwater Harvesting Package",
    "implementing_agency": "Department of Agriculture, Government of Karnataka",
    "target_beneficiaries": "Dryland farmers in 130+ rain-dependent talukas of Karnataka (North & Central Karnataka dry belts)",
    "applicable_states": [
      "Karnataka"
    ],
    "subsidy_rules": {
      "sc_st_farmers": "90% subsidy for farm pond excavation, polythene lining, pump set, and micro-irrigation package",
      "general_small_marginal": "80% package subsidy (total benefit up to ₹1,75,000 per farm unit)"
    },
    "eligible_systems": [
      "Farm Pond excavation with silt trap",
      "UV-stabilised polythene lining (500 micron)",
      "Solar or Diesel pump sets for lifting stored water",
      "Drip / Sprinkler distribution package"
    ],
    "water_savings_potential": "Stores surface runoff to guarantee kharif crop rescue irrigation during 3-4 week monsoon breaks",
    "eligibility_criteria": [
      "Resident cultivator in notified dryland talukas of Karnataka",
      "Pahani / RTC land record"
    ],
    "documents_required": [
      "RTC / Pahani document",
      "Aadhaar Card",
      "Bank Account details",
      "Caste Certificate (for 90% SC/ST tier)"
    ],
    "current_status": "Active with annual allocations across Karnataka dryland districts",
    "portal_url": "https://raitamitra.karnataka.gov.in",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "GUJARAT_GGRC_SKY",
    "name": "Gujarat Micro Irrigation Scheme (GGRC) & Suryashakti Kisan Yojana (SKY)",
    "level": "Gujarat State Scheme",
    "category": "State Micro Irrigation & Grid-Connected Solar Pumps",
    "implementing_agency": "Gujarat Green Revolution Company (GGRC) & GUVNL",
    "target_beneficiaries": "All farmers in Gujarat cultivating groundnut, cotton, vegetables, and cumin",
    "applicable_states": [
      "Gujarat"
    ],
    "subsidy_rules": {
      "tribal_and_sc_farmers": "Up to 85% subsidy on Drip and Sprinkler systems",
      "general_small_marginal": "70% subsidy; other farmers 50%",
      "sky_solar_pumps": "Farmer contributes only 5%; 60% Govt subsidy + 35% low-interest loan; farmer earns ₹7/unit for surplus solar power fed to grid"
    },
    "eligible_systems": [
      "Inline Drip System for Cotton and Groundnut",
      "Micro-sprinkler systems for summer pulses",
      "Grid-interactive solar pump sets"
    ],
    "water_savings_potential": "Cuts water usage by 55%; earns farmers ₹12,000-24,000 annually selling green solar electricity",
    "eligibility_criteria": [
      "7/12 & 8-A land record in Gujarat",
      "Existing water source (borewell or well) with water test report"
    ],
    "documents_required": [
      "7/12 & 8-A Extracts",
      "Aadhaar Card",
      "Bank Passbook copy",
      "Electricity consumer number (if grid connected)"
    ],
    "current_status": "Active on GGRC online portal (ggrc.co.in) and i-Khedut portal",
    "portal_url": "https://ggrc.co.in / https://ikhedut.gujarat.gov.in",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "HARYANA_MERA_PANI",
    "name": "Haryana Mera Pani Meri Virasat & Water Recharge Borewell Scheme",
    "level": "Haryana State Scheme",
    "category": "Crop Diversification Direct Incentive & Water Table Shield",
    "implementing_agency": "Department of Agriculture & Farmers Welfare, Government of Haryana",
    "target_beneficiaries": "Farmers in dark/overexploited groundwater zones replacing water-guzzling Paddy with maize, pulses, cotton, or agroforestry",
    "applicable_states": [
      "Haryana"
    ],
    "subsidy_rules": {
      "crop_diversification_cash": "₹7,000 per acre direct cash incentive transferred to farmer bank account for switching from paddy",
      "micro_irrigation_top_up": "85% subsidy on Drip and Sprinkler systems on diversified acreage",
      "underground_recharge_wells": "Subsidy for constructing rooftop/farm water injection recharge borewells"
    },
    "eligible_systems": [
      "Direct DBT Cash incentive for crop substitution",
      "Drip & Mini Sprinkler setups",
      "Borewell Groundwater Recharge Chambers"
    ],
    "water_savings_potential": "Saves 30 to 40 lakh liters of groundwater per acre per season; prevents water table drop",
    "eligibility_criteria": [
      "Farmer in Haryana who cultivated paddy in previous kharif and diversifies into non-paddy crops",
      "Registration on Meri Fasal Mera Byora (MFMB) portal"
    ],
    "documents_required": [
      "Meri Fasal Mera Byora (MFMB) acknowledgment ID",
      "Parivar Pehchan Patra (PPP) Family ID",
      "Aadhaar Card",
      "Bank Passbook"
    ],
    "current_status": "Active with annual kharif enrollment window on fasal.haryana.gov.in",
    "portal_url": "https://fasal.haryana.gov.in",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "PUNJAB_UGPL_PIPELINE",
    "name": "Punjab Underground Pipeline System (UGPL) & Micro Irrigation",
    "level": "Punjab State Scheme",
    "category": "Conveyance Loss Elimination & Subsidised PVC Piping",
    "implementing_agency": "Department of Soil and Water Conservation, Government of Punjab",
    "target_beneficiaries": "Farmers facing high canal/borewell seepage losses and electricity consumption in Punjab",
    "applicable_states": [
      "Punjab"
    ],
    "subsidy_rules": {
      "individual_pipeline": "50% capital subsidy (up to ₹60,000 per farmer or ₹84,000/ha) for laying underground PVC pipelines",
      "community_pipeline_sc": "Up to 90% subsidy for SC/ST and community pipeline projects benefiting smallholders"
    },
    "eligible_systems": [
      "Underground PVC irrigation pipeline networks (110mm to 160mm)",
      "Automated inlet valves and distribution hydrants",
      "Drip irrigation for cotton and kinnow orchards"
    ],
    "water_savings_potential": "Eliminates 30% to 35% conveyance seepage evaporation losses in open unlined field watercourses",
    "eligibility_criteria": [
      "Cultivated land in Punjab with operational tube-well or canal outlet",
      "Joint consent if pipeline crosses neighboring survey numbers"
    ],
    "documents_required": [
      "Fard / Jamabandi land extract",
      "Aadhaar Card",
      "Bank Account details",
      "Tube-well electricity bill or Canal outlet certificate"
    ],
    "current_status": "Active under State Soil & Water Conservation allocation",
    "portal_url": "https://dswcpunjab.gov.in",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "TAMILNADU_MICRO_IRRIGATION",
    "name": "Tamil Nadu Micro Irrigation Scheme (100% Subsidy for Small/Marginal Farmers)",
    "level": "Tamil Nadu State Scheme",
    "category": "State Top-Up Precision Micro Irrigation",
    "implementing_agency": "Department of Horticulture & Plantation Crops, Government of Tamil Nadu",
    "target_beneficiaries": "Small, marginal, and large farmers cultivating sugarcane, banana, coconut, pulses, and oilseeds",
    "applicable_states": [
      "Tamil Nadu"
    ],
    "subsidy_rules": {
      "small_and_marginal_farmers": "100% subsidy (55% PMKSY Central share + 45% Tamil Nadu State Government top-up)",
      "other_large_farmers": "75% subsidy (45% Central + 30% State top-up)"
    },
    "eligible_systems": [
      "Drip Irrigation System with disc filters and venturi injectors",
      "Portable and Semi-Permanent Sprinklers for Pulses and Groundnut"
    ],
    "water_savings_potential": "Saves 50% to 60% Cauvery / Vaigai basin groundwater; boosts crop productivity by 35%",
    "eligibility_criteria": [
      "Patta / Chitta ownership in Tamil Nadu",
      "Functional borewell or open well with water quality fit for irrigation"
    ],
    "documents_required": [
      "Patta / Chitta extract and FMB sketch",
      "Aadhaar Card",
      "Small / Marginal Farmer Certificate issued by Revenue Tahsildar",
      "Bank Passbook copy"
    ],
    "current_status": "Active with registrations open on TN Horticulture portal (tnhorticulture.tn.gov.in)",
    "portal_url": "https://tnhorticulture.tn.gov.in",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "RAJASTHAN_KHET_TALAI",
    "name": "Rajasthan Farm Pond (Khet Talai) & Drip Subsidy (Rajkisan Sathi)",
    "level": "Rajasthan State Scheme",
    "category": "Arid Zone Rainwater Harvesting & High Subsidy Drip",
    "implementing_agency": "Department of Agriculture, Government of Rajasthan",
    "target_beneficiaries": "Farmers in arid and semi-arid districts (Barmer, Jodhpur, Bikaner, Nagaur, Kota, Alwar)",
    "applicable_states": [
      "Rajasthan"
    ],
    "subsidy_rules": {
      "plastic_lined_farm_pond": "Up to ₹1,20,000 (or 70% of cost) subsidy for small/marginal farmers constructing plastic-lined farm ponds; ₹90,000 for other farmers",
      "raw_earthen_pond": "₹63,000 (small/marginal) and ₹50,000 (general)",
      "drip_sprinkler_topup": "70% subsidy for small/marginal; 75% for SC/ST"
    },
    "eligible_systems": [
      "Plastic Film Lined Farm Ponds (Khet Talai - 400/500 micron)",
      "Solar Water Pumps (under PM-KUSUM Component B)",
      "Mini & Micro Sprinkler systems"
    ],
    "water_savings_potential": "Traps flash desert monsoon showers; provides winter crop irrigation without borewells",
    "eligibility_criteria": [
      "Minimum 0.50 hectare agricultural land in Rajasthan",
      "Registration on Rajkisan Sathi portal with Jan Aadhaar card"
    ],
    "documents_required": [
      "Jan Aadhaar Card",
      "Jamabandi copy (within 6 months)",
      "Aadhaar Card",
      "Bank Account linked to Jan Aadhaar"
    ],
    "current_status": "Active via online lottery and queue on Rajkisan Sathi portal",
    "portal_url": "https://rajkisan.rajasthan.gov.in",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "MP_BALRAM_TALAB",
    "name": "Madhya Pradesh Balram Talab Yojana & e-Krishi Anudan",
    "level": "Madhya Pradesh State Scheme",
    "category": "Groundwater Recharge Farm Pond & Micro Irrigation",
    "implementing_agency": "Farmers Welfare & Agriculture Development Department, Government of MP",
    "target_beneficiaries": "Farmers in Malwa, Bundelkhand, and Mahakoshal belts facing declining water tables",
    "applicable_states": [
      "Madhya Pradesh"
    ],
    "subsidy_rules": {
      "sc_st_farmers": "75% subsidy up to maximum of ₹1,00,000 for Balram Talab construction",
      "small_marginal_farmers": "50% subsidy up to maximum of ₹80,000",
      "other_farmers": "40% subsidy up to ₹50,000",
      "drip_sprinkler_subsidy": "55% subsidy under PMKSY on MP e-Krishi Anudan"
    },
    "eligible_systems": [
      "Balram Talab (Farm Pond for water storage & aquifer recharge)",
      "Sprinkler sets for wheat, gram, and mustard",
      "Drip systems for soybean, cotton, and vegetables"
    ],
    "water_savings_potential": "Enhances surrounding tube-well discharge by 40%; provides supplementary irrigation during dry spells",
    "eligibility_criteria": [
      "Khasra/B-1 land ownership in Madhya Pradesh",
      "Farmer must construct pond on own cultivable land"
    ],
    "documents_required": [
      "Khasra / B-1 copy",
      "Aadhaar Card",
      "Bank Passbook copy",
      "Caste Certificate (for SC/ST 75% tier)"
    ],
    "current_status": "Active on MP DBT e-Krishi Anudan portal (dbt.mpdage.org)",
    "portal_url": "https://dbt.mpdage.org",
    "last_verified": "2026-11-05"
  },
  {
    "scheme_id": "UP_KHET_TALAB",
    "name": "Uttar Pradesh Khet Talab Yojana & Solar Pump Token Booking",
    "level": "Uttar Pradesh State Scheme",
    "category": "Bundelkhand Water Harvest & Subsidised Solar Pumps",
    "implementing_agency": "Agriculture Department, Government of Uttar Pradesh",
    "target_beneficiaries": "Farmers across all 75 UP districts with special priority for Bundelkhand (7 districts)",
    "applicable_states": [
      "Uttar Pradesh"
    ],
    "subsidy_rules": {
      "khet_talab_subsidy": "50% direct subsidy (₹52,500 for small pond of 22m x 20m x 3m; ₹1,14,200 for medium pond) disbursed in 3 direct DBT tranches",
      "solar_pump_token": "Up to 60% subsidy on 2 HP, 3 HP, 5 HP, and 7.5 HP solar pumps under PM-KUSUM with online token booking"
    },
    "eligible_systems": [
      "Khet Talab (Rainwater storage farm ponds)",
      "Solar DC/AC submersible and surface pump sets",
      "Sprinkler irrigation sets for pulse and oilseed clusters"
    ],
    "water_savings_potential": "Saves Bundelkhand pulses from drought failure; stores 2,000 to 4,500 cubic meters of monsoon runoff",
    "eligibility_criteria": [
      "Registered farmer on upagriculture.com portal (Kisan Panjikaran)",
      "Clear land title in Uttar Pradesh"
    ],
    "documents_required": [
      "Kisan Panjikaran Number (UP Agriculture registration)",
      "Khatauni land record",
      "Aadhaar Card",
      "Bank Passbook"
    ],
    "current_status": "Active with token booking sessions announced on upagriculture.com",
    "portal_url": "https://upagriculture.com",
    "last_verified": "2026-11-05"
  }
];

const LOW_WATER_CROPS_DATA = [
  {
    "crop_id": "bengal_gram",
    "name": "Bengal Gram / Desi Chickpea (శనగ / चना)",
    "category": "Pulses (Rabi / Winter)",
    "season_suitability": "Rabi (Post-Kharif Paddy or rainfed fallow)",
    "water_requirement_mm": "250 - 350 mm (vs 1200 - 1400 mm for Paddy)",
    "water_savings_percentage": "75% less water than flooded Paddy",
    "msp_rate_per_quintal": 5440,
    "recommended_varieties": [
      "JG 11",
      "JAKI 9218",
      "NBeG 3",
      "KAK 2",
      "Vishal"
    ],
    "sowing_window": "October 15 to November 15 (Ideal with residual soil moisture)",
    "duration_days": "95 - 105 days",
    "expected_yield_qtl_per_acre": "8 - 10 Quintals",
    "net_income_estimate_per_acre": "₹35,000 - ₹45,000",
    "soil_suitability": "Medium to deep black cotton soils and loamy soils with good water-holding capacity",
    "attached_schemes": [
      "NFSM-Pulses: 50% certified seed subsidy & free biofertilizer (Rhizobium + PSB) packets",
      "PM-AASHA: Guaranteed MSP procurement through NAFED & State Markfed",
      "Pradhan Mantri Krishi Sinchayee Yojana (PMKSY) for sprinkler sets"
    ],
    "soil_health_benefit": "Fixes 40-50 kg atmospheric Nitrogen/ha; reduces subsequent crop urea requirement by 25%"
  },
  {
    "crop_id": "kabuli_chickpea",
    "name": "Kabuli Chickpea / Dollar Chana (కాబూలీ శనగ / काबुली चना)",
    "category": "High-Value Export Pulses (Rabi)",
    "season_suitability": "Rabi (Irrigated dry)",
    "water_requirement_mm": "250 - 320 mm",
    "water_savings_percentage": "78% less water than Paddy",
    "msp_rate_per_quintal": 5440,
    "market_price_per_quintal": "₹9,000 - ₹12,000 (Premium export market valuation)",
    "recommended_varieties": [
      "MNK 1",
      "PKV Kabuli 2",
      "Phule G 0517",
      "Kripa"
    ],
    "sowing_window": "October 20 to November 10",
    "duration_days": "100 - 110 days",
    "expected_yield_qtl_per_acre": "7 - 9 Quintals",
    "net_income_estimate_per_acre": "₹55,000 - ₹75,000",
    "soil_suitability": "Deep, well-drained black clay loams; sensitive to excess moisture",
    "attached_schemes": [
      "Agricultural and Processed Food Products Export Development Authority (APEDA) export credit",
      "NFSM-Pulses demonstration clusters"
    ],
    "soil_health_benefit": "Leaves deep root channels that improve soil aeration and infiltration for the next season"
  },
  {
    "crop_id": "green_gram",
    "name": "Green Gram / Moong (పెసర / मूंग)",
    "category": "Short-Duration Pulses (Summer / Catch Crop / Kharif)",
    "season_suitability": "Summer (March-May) or Kharif onset (June-July)",
    "water_requirement_mm": "200 - 280 mm",
    "water_savings_percentage": "80% less water than Paddy",
    "msp_rate_per_quintal": 8682,
    "recommended_varieties": [
      "MGG 295",
      "WGG 42",
      "IPM 02-14",
      "Shikha",
      "Samrat"
    ],
    "sowing_window": "March 1 to March 25 (Summer) or June 15 to July 15 (Kharif)",
    "duration_days": "60 - 65 days (Fastest cash liquidity turnaround)",
    "expected_yield_qtl_per_acre": "5 - 7 Quintals",
    "net_income_estimate_per_acre": "₹38,000 - ₹48,000",
    "soil_suitability": "Well-drained loams, sandy loams, and light red soils; highly responsive to micro-sprinklers",
    "attached_schemes": [
      "National Food Security Mission: Free Certified Mini-Kit Seed Distribution at Rythu Vedikas",
      "MSP Procurement Operations through NAFED and State Oilfed",
      "Summer Moong Promotion under State Pulses Missions"
    ],
    "soil_health_benefit": "Biomass incorporation after 2 pickings adds 3 to 4 tonnes of green manure per acre"
  },
  {
    "crop_id": "black_gram",
    "name": "Black Gram / Urad (మినుములు / उड़द)",
    "category": "Pulses (Zero-Tillage Rice Fallows / Kharif)",
    "season_suitability": "Rabi Rice-Fallows (November-December) or Kharif",
    "water_requirement_mm": "250 - 320 mm",
    "water_savings_percentage": "78% less water than Paddy",
    "msp_rate_per_quintal": 7400,
    "recommended_varieties": [
      "PU 31",
      "LBG 752",
      "TBG 104",
      "VBN 8",
      "Shekhar 2"
    ],
    "sowing_window": "Broadcast into standing paddy 2-3 days before harvest or sown November-December",
    "duration_days": "75 - 85 days",
    "expected_yield_qtl_per_acre": "6 - 8 Quintals",
    "net_income_estimate_per_acre": "₹40,000 - ₹50,000",
    "soil_suitability": "Clayey loams and residual moisture black soils; ideal relay crop in delta and canal commands",
    "attached_schemes": [
      "Zero-Tillage Rice Fallows Promotion Scheme (Subsidised seeds and pre-emergence weedicides)",
      "NAFED Price Support Scheme (PSS) Procurement"
    ],
    "soil_health_benefit": "Zero tillage saves ₹4,000/acre in land preparation; deep taproot breaks plough-pan layer"
  },
  {
    "crop_id": "red_gram",
    "name": "Red Gram / Pigeonpea / Tur (కందులు / अरहर-तुअर)",
    "category": "Deep-Rooted Drought Avoidance Pulses (Kharif / Annual)",
    "season_suitability": "Kharif (June to July)",
    "water_requirement_mm": "350 - 450 mm",
    "water_savings_percentage": "70% less water than flooded Paddy",
    "msp_rate_per_quintal": 7550,
    "recommended_varieties": [
      "PRG 176",
      "ICPL 87119 (Asha)",
      "WRG 65",
      "BDN 711",
      "Maruti"
    ],
    "sowing_window": "June 15 to July 20",
    "duration_days": "150 - 180 days (Intercropped with Cotton/Soybean or Sole Crop)",
    "expected_yield_qtl_per_acre": "7 - 10 Quintals",
    "net_income_estimate_per_acre": "₹45,000 - ₹60,000",
    "soil_suitability": "Deep, well-drained red and black soils with no waterlogging",
    "attached_schemes": [
      "Targeted Pulses Production Programme (TPPD) under NFSM",
      "Special Tur Procurement Portal via e-Samridhi NAFED/NCCF with 100% procurement commitment",
      "Drip fertigation subsidy under PMKSY"
    ],
    "soil_health_benefit": "Root depth of 2 meters mines sub-soil nutrients and moisture; recycles 1.5 tonnes leaf litter"
  },
  {
    "crop_id": "horse_gram",
    "name": "Horse Gram / Kulthi (ఉలవలు / कुलथी / కొల్లూ)",
    "category": "Ultra Drought-Hardy Poor Soil Pulses (Late Kharif / Rabi)",
    "season_suitability": "Late Kharif / Post-flood / Contingency crop (August to October)",
    "water_requirement_mm": "150 - 220 mm (Survives where other crops fail)",
    "water_savings_percentage": "88% less water than Paddy",
    "msp_rate_per_quintal": 4500,
    "recommended_varieties": [
      "CRIDA 18R",
      "Palem 1",
      "Palem 2",
      "AK 21",
      "Madhu"
    ],
    "sowing_window": "August 15 to October 15",
    "duration_days": "80 - 90 days",
    "expected_yield_qtl_per_acre": "4 - 6 Quintals",
    "net_income_estimate_per_acre": "₹22,000 - ₹30,000 with near-zero chemical input cost",
    "soil_suitability": "Shallow, gravelly, poor, eroded red gravels and degraded marginal wastelands",
    "attached_schemes": [
      "State Contingent Crop Planning mini-kits after delayed or failed monsoon",
      "Traditional Nutri-Feed Promotion for dairy and poultry"
    ],
    "soil_health_benefit": "Extreme ground cover prevents topsoil erosion; thrives on zero synthetic fertilizer"
  },
  {
    "crop_id": "cowpea",
    "name": "Cowpea / Lobia / Black-Eyed Pea (బొబ్బర్లు / అలసందలు / लोबिया)",
    "category": "Dual-Purpose Pulse & Nutritious Green Fodder",
    "season_suitability": "Kharif, Summer, or Pre-Rabi",
    "water_requirement_mm": "220 - 300 mm",
    "water_savings_percentage": "82% less water than Paddy",
    "msp_rate_per_quintal": 5800,
    "recommended_varieties": [
      "C 152",
      "CP 4",
      "VBN 1",
      "Pusa Komal"
    ],
    "sowing_window": "June-July or February-March",
    "duration_days": "70 - 80 days",
    "expected_yield_qtl_per_acre": "5 - 7 Quintals grain + 60 quintals green fodder",
    "net_income_estimate_per_acre": "₹32,000 - ₹42,000",
    "soil_suitability": "Wide range from light sandy to loamy soils; tolerates heat and shade",
    "attached_schemes": [
      "National Livestock Mission: Fodder & Grain seed subsidy",
      "NFSM-Pulses demonstration kits"
    ],
    "soil_health_benefit": "Dense canopy smothers 90% of weeds naturally; adds high nitrogen organic matter"
  },
  {
    "crop_id": "lentil",
    "name": "Lentil / Masoor (మసూర్ / मसूर)",
    "category": "Cool Season Low-Water Pulses (Rabi)",
    "season_suitability": "Rabi (October-November)",
    "water_requirement_mm": "200 - 260 mm",
    "water_savings_percentage": "82% less water than Paddy",
    "msp_rate_per_quintal": 6700,
    "recommended_varieties": [
      "HUL 57",
      "KLS 218",
      "Pusa Ageti",
      "IPL 316"
    ],
    "sowing_window": "October 25 to November 20",
    "duration_days": "110 - 120 days",
    "expected_yield_qtl_per_acre": "6 - 8 Quintals",
    "net_income_estimate_per_acre": "₹38,000 - ₹50,000",
    "soil_suitability": "All types of soils from light loams to heavy black clays; tolerates light salinity",
    "attached_schemes": [
      "National Food Security Mission Pulses Component (100% domestic procurement pledge)",
      "Central seed distribution on e-Samridhi portal"
    ],
    "soil_health_benefit": "Enriches soil micro-flora with cold-tolerant rhizobium nodules"
  },
  {
    "crop_id": "sesame",
    "name": "Sesame / Til / Gingelly (నువ్వులు / तिल)",
    "category": "High-Value Arid Oilseeds (Summer / Spring)",
    "season_suitability": "Summer (January to March) or Kharif",
    "water_requirement_mm": "180 - 240 mm (Extremely water-thrifty)",
    "water_savings_percentage": "85% less water than Paddy",
    "msp_rate_per_quintal": 9267,
    "recommended_varieties": [
      "Swetha (JCS 1020)",
      "Rajeshwari",
      "Hima",
      "Chandana",
      "GT 10"
    ],
    "sowing_window": "January 15 to February 28 (Summer) or June-July (Kharif)",
    "duration_days": "80 - 85 days",
    "expected_yield_qtl_per_acre": "3.5 - 5.0 Quintals",
    "net_income_estimate_per_acre": "₹32,000 - ₹45,000 with very low input costs",
    "soil_suitability": "Well-drained sandy loams and light red soils; highly sensitive to standing water",
    "attached_schemes": [
      "Highest Minimum Support Price (MSP) among all oilseeds in India (₹9,267/qtl)",
      "National Mission on Edible Oils - Oilseeds (NMEO-OS)",
      "High global demand for Hulled Sesame Export"
    ],
    "soil_health_benefit": "Survives on only 2 to 3 light irrigations in total life cycle; breaks pest cycles"
  },
  {
    "crop_id": "groundnut",
    "name": "Groundnut / Peanut (వేరుశనగ / मूंगफली)",
    "category": "Oilseeds & Food Crop (Rabi / Summer / Kharif)",
    "season_suitability": "Rabi/Summer (November to January) or Kharif (June-July)",
    "water_requirement_mm": "380 - 450 mm",
    "water_savings_percentage": "65% less water than flooded Paddy",
    "msp_rate_per_quintal": 6783,
    "recommended_varieties": [
      "Kadiri 6 (K6)",
      "Kadiri 9",
      "TAG 24",
      "Dharani",
      "Greeshma"
    ],
    "sowing_window": "November 15 to January 15 (Rabi/Summer)",
    "duration_days": "105 - 115 days",
    "expected_yield_qtl_per_acre": "10 - 14 Quintals",
    "net_income_estimate_per_acre": "₹50,000 - ₹68,000",
    "soil_suitability": "Sandy loam or loose red soils with good calcium content; easy peg penetration and pod lifting",
    "attached_schemes": [
      "National Mission on Edible Oils - Oilseeds (NMEO-OS)",
      "Gypsum 50% Subsidy via Agriculture Extension Officers (AEOs)",
      "Micro-sprinkler subsidy under TSMIP / PMKSY (reduces water usage by 40%)"
    ],
    "soil_health_benefit": "High protein haulm provides ₹8,000/acre in cattle fodder value; fixes soil nitrogen"
  },
  {
    "crop_id": "mustard_rapeseed",
    "name": "Mustard & Rapeseed (ఆవాలు / सरसों-राई)",
    "category": "Rabi Oilseeds (Low-Water Winter Crop)",
    "season_suitability": "Rabi (October to November)",
    "water_requirement_mm": "240 - 300 mm",
    "water_savings_percentage": "80% less water than Paddy",
    "msp_rate_per_quintal": 5650,
    "recommended_varieties": [
      "Pusa Bold",
      "Pusa Mustard 25",
      "RH 749",
      "Giriraj",
      "Kranti"
    ],
    "sowing_window": "October 1 to October 25",
    "duration_days": "115 - 125 days",
    "expected_yield_qtl_per_acre": "7 - 10 Quintals",
    "net_income_estimate_per_acre": "₹38,000 - ₹52,000",
    "soil_suitability": "Light to heavy soils with good drainage; tolerates salinity and alkalinity",
    "attached_schemes": [
      "Special Mustard Promotion Clusters under NMEO-OS",
      "Free hybrid seed mini-kit distribution",
      "Guaranteed procurement through NAFED and HAFED"
    ],
    "soil_health_benefit": "Glucosinolate root exudates act as natural biofumigants, suppressing soil nematodes and fungal spores"
  },
  {
    "crop_id": "safflower",
    "name": "Safflower / Kardi (కుసుమలు / कुसुम-करडी)",
    "category": "Deep-Rooted Drought Champion Oilseeds (Rabi)",
    "season_suitability": "Rabi (Post-Kharif residual moisture)",
    "water_requirement_mm": "220 - 300 mm",
    "water_savings_percentage": "82% less water than Paddy",
    "msp_rate_per_quintal": 5800,
    "recommended_varieties": [
      "PBNS 12",
      "NARI 6",
      "Manjira",
      "DSH 129",
      "Bhima"
    ],
    "sowing_window": "September 25 to October 25",
    "duration_days": "120 - 130 days",
    "expected_yield_qtl_per_acre": "6 - 8 Quintals",
    "net_income_estimate_per_acre": "₹32,000 - ₹44,000",
    "soil_suitability": "Deep black vertisols capable of holding moisture at depth; spiny leaves protect against wild boar and cattle",
    "attached_schemes": [
      "Technology Mission on Oilseeds (NMEO-OS)",
      "State crop border planting incentive against wild animals"
    ],
    "soil_health_benefit": "Deep 2.5m taproot draws moisture and nutrient reserves from sub-soil; opens compacted clay"
  },
  {
    "crop_id": "sunflower",
    "name": "Sunflower (పొద్దుతిరుగుడు / सूरजमुखी)",
    "category": "Day-Neutral Irrigated Dry Oilseeds (Rabi / Summer)",
    "season_suitability": "Rabi (October-November) or Summer (January-February)",
    "water_requirement_mm": "300 - 380 mm",
    "water_savings_percentage": "75% less water than Paddy",
    "msp_rate_per_quintal": 7280,
    "recommended_varieties": [
      "KBSH 41",
      "KBSH 53",
      "DRSH 1",
      "NDSH 1012"
    ],
    "sowing_window": "November 1 to November 30 or January 15 to February 15",
    "duration_days": "85 - 95 days",
    "expected_yield_qtl_per_acre": "7 - 9 Quintals",
    "net_income_estimate_per_acre": "₹42,000 - ₹55,000",
    "soil_suitability": "Well-drained soils; adaptable across sandy loams and deep vertisols",
    "attached_schemes": [
      "NMEO-OS: ₹4,000/ha input subsidy on hybrid seeds and boron",
      "Assured procurement by State Cooperative Oil Federations"
    ],
    "soil_health_benefit": "Photo-insensitive nature allows perfect fitting into any crop gap after water-stressed paddy failure"
  },
  {
    "crop_id": "castor",
    "name": "Castor (ఆముదము / अरंडी)",
    "category": "Industrial Semi-Arid Oilseeds (Kharif / Rabi)",
    "season_suitability": "Kharif (July-August) or Rabi (September-October)",
    "water_requirement_mm": "300 - 400 mm",
    "water_savings_percentage": "72% less water than Paddy",
    "msp_rate_per_quintal": 6000,
    "recommended_varieties": [
      "GCH 7",
      "DCH 519",
      "PCH 111",
      "DCH 177",
      "Jyoti"
    ],
    "sowing_window": "July 1 to August 15",
    "duration_days": "150 - 180 days (Multiple pickings)",
    "expected_yield_qtl_per_acre": "8 - 12 Quintals",
    "net_income_estimate_per_acre": "₹45,000 - ₹65,000",
    "soil_suitability": "Sandy and red loamy soils; ideal for poor, well-drained rainfed uplands",
    "attached_schemes": [
      "High global demand for castor oil and sebacic acid derivatives",
      "Drip irrigation subsidy under PMKSY yields 35% extra production"
    ],
    "soil_health_benefit": "Not grazed by stray cattle or wild boars; deep root system binds soil against wind erosion"
  },
  {
    "crop_id": "linseed",
    "name": "Linseed / Flaxseed (అవిసెలు / अलसी)",
    "category": "High-Value Omega-3 Dual Purpose Oilseed & Fiber (Rabi)",
    "season_suitability": "Rabi (October-November)",
    "water_requirement_mm": "200 - 260 mm",
    "water_savings_percentage": "82% less water than Paddy",
    "msp_rate_per_quintal": 6200,
    "recommended_varieties": [
      "T 397",
      "Padmini",
      "JLS 67",
      "Deepika"
    ],
    "sowing_window": "October 15 to November 15",
    "duration_days": "110 - 120 days",
    "expected_yield_qtl_per_acre": "5 - 7 Quintals",
    "net_income_estimate_per_acre": "₹30,000 - ₹42,000",
    "soil_suitability": "Clayey loams and vertisols with good moisture retention; ideal utera/paira crop in paddy fallow",
    "attached_schemes": [
      "Promotion under Nutraceutical and Functional Foods Mission",
      "Subsidised certified seed kits under NFSM-OS"
    ],
    "soil_health_benefit": "Minimal fertilizer requirement; excellent cool-season intercrop with gram or mustard"
  },
  {
    "crop_id": "soybean",
    "name": "Soybean (సోయాబీన్ / सोयाबीन)",
    "category": "Rainfed Protein & Edible Oil Crop (Kharif)",
    "season_suitability": "Kharif (June to July)",
    "water_requirement_mm": "350 - 450 mm",
    "water_savings_percentage": "68% less water than flooded Paddy",
    "msp_rate_per_quintal": 4892,
    "recommended_varieties": [
      "JS 335",
      "JS 95-60",
      "JS 20-34",
      "NRC 127",
      "MACS 1407"
    ],
    "sowing_window": "June 15 to July 10",
    "duration_days": "85 - 95 days",
    "expected_yield_qtl_per_acre": "8 - 12 Quintals",
    "net_income_estimate_per_acre": "₹38,000 - ₹52,000",
    "soil_suitability": "Well-drained medium to deep black clay soils with pH 6.5 to 7.5",
    "attached_schemes": [
      "National Mission on Edible Oils - Oilseeds (NMEO-OS)",
      "Broad-Bed Furrow (BBF) machine subsidy to counter rainfed dry spells"
    ],
    "soil_health_benefit": "Fixes 60-80 kg atmospheric nitrogen per hectare; leaves rich organic nitrogen in soil"
  },
  {
    "crop_id": "sorghum_jowar",
    "name": "Sorghum / Jowar (జొన్నలు / ज्वार)",
    "category": "Nutri-Cereals / Shree Anna (Kharif & Rabi Dual-Purpose)",
    "season_suitability": "Kharif (June-July) or Rabi (September-October)",
    "water_requirement_mm": "250 - 350 mm",
    "water_savings_percentage": "75% less water than flooded Paddy",
    "msp_rate_per_quintal": 3371,
    "recommended_varieties": [
      "CSH 16",
      "CSH 24MF",
      "CSV 29R",
      "Maldandi (M 35-1)",
      "Parbhani Moti"
    ],
    "sowing_window": "June 15 - July 15 (Kharif) or September 15 - October 15 (Rabi)",
    "duration_days": "100 - 110 days",
    "expected_yield_qtl_per_acre": "12 - 16 Quintals grain + 35 quintals nutritious stover",
    "net_income_estimate_per_acre": "₹36,000 - ₹50,000",
    "soil_suitability": "Wide soil range from shallow red gravels to deep black soils; highly tolerant to drought and heat",
    "attached_schemes": [
      "National Shree Anna Mission: Free seed kits, custom hiring center machinery",
      "Public Distribution System (PDS) & Mid-Day Meal state procurement at MSP"
    ],
    "soil_health_benefit": "Extracts water down to 1.5m; deep fibrous root system binds soil against desertification"
  },
  {
    "crop_id": "pearl_millet_bajra",
    "name": "Pearl Millet / Bajra (సజ్జలు / बाजरा)",
    "category": "Nutri-Cereals / Shree Anna (Extreme Heat & Arid Climate)",
    "season_suitability": "Kharif or Summer",
    "water_requirement_mm": "200 - 300 mm (Lowest water need among major cereals)",
    "water_savings_percentage": "82% less water than Paddy",
    "msp_rate_per_quintal": 2625,
    "recommended_varieties": [
      "HHB 67 Improved",
      "Dhanashakti (Biofortified Iron)",
      "RHB 177",
      "GHB 558"
    ],
    "sowing_window": "June 25 to July 15 (Kharif) or February (Summer)",
    "duration_days": "70 - 80 days",
    "expected_yield_qtl_per_acre": "10 - 14 Quintals",
    "net_income_estimate_per_acre": "₹28,000 - ₹38,000",
    "soil_suitability": "Drought-prone sandy loams and light arid soils; thrives even under 45°C ambient temperatures",
    "attached_schemes": [
      "National Shree Anna Mission: Biofortified high-iron variety promotion",
      "Decentralized MSP procurement for ICDS and Anganwadi programs"
    ],
    "soil_health_benefit": "Super-fast photosynthetic C4 pathway; zero irrigation required after seedling establishment"
  },
  {
    "crop_id": "finger_millet_ragi",
    "name": "Finger Millet / Ragi (రాగులు / रागी-मडुआ)",
    "category": "Nutri-Cereals / Shree Anna (Calcium & Iron Powerhouse)",
    "season_suitability": "Kharif (June-August) or Rabi (September-October)",
    "water_requirement_mm": "280 - 350 mm",
    "water_savings_percentage": "75% less water than Paddy",
    "msp_rate_per_quintal": 4290,
    "recommended_varieties": [
      "GPU 28",
      "ML 365",
      "Indaf 5",
      "Vakula",
      "Birsa Marua 2"
    ],
    "sowing_window": "July 1 to August 15",
    "duration_days": "95 - 110 days",
    "expected_yield_qtl_per_acre": "9 - 13 Quintals",
    "net_income_estimate_per_acre": "₹38,000 - ₹52,000",
    "soil_suitability": "Red sandy loams, gravelly laterites, and upland light soils; tolerates acidic soils",
    "attached_schemes": [
      "National Shree Anna Mission: MSP procurement via FCI & Civil Supplies Corporations",
      "Special Ragi Processing Machinery Subsidies for Women Self Help Groups (SHGs)"
    ],
    "soil_health_benefit": "Contains 344 mg calcium per 100g grain; straw makes premium digestible livestock feed"
  },
  {
    "crop_id": "foxtail_millet_korra",
    "name": "Foxtail Millet / Kangni (కొర్రలు / कांगनी)",
    "category": "Small Millets / Shree Anna (Short-Duration 70 Days)",
    "season_suitability": "Kharif or Contingency early rabi",
    "water_requirement_mm": "180 - 250 mm",
    "water_savings_percentage": "85% less water than Paddy",
    "msp_rate_per_quintal": 3200,
    "recommended_varieties": [
      "SIA 3088",
      "SIA 3156",
      "Pratap Kangani 1",
      "Meera"
    ],
    "sowing_window": "July 15 to August 15 (Best crop when main monsoon is delayed)",
    "duration_days": "70 - 75 days",
    "expected_yield_qtl_per_acre": "6 - 9 Quintals",
    "net_income_estimate_per_acre": "₹24,000 - ₹35,000",
    "soil_suitability": "Shallow to medium soils, light red soils; highly resilient to intermittent dry spells",
    "attached_schemes": [
      "State Small Millet Mission seed mini-kits",
      "Local Mandi procurement support and FPO direct-to-consumer processing hubs"
    ],
    "soil_health_benefit": "Mature crop ready in just 10 weeks; frees up land quickly for subsequent rabi pulse sowing"
  },
  {
    "crop_id": "little_millet_samalu",
    "name": "Little Millet / Kutki (సామలు / कुटकी)",
    "category": "Small Millets / Shree Anna (Extreme Flood & Drought Flexibility)",
    "season_suitability": "Kharif (June to July)",
    "water_requirement_mm": "180 - 240 mm",
    "water_savings_percentage": "85% less water than Paddy",
    "msp_rate_per_quintal": 3000,
    "recommended_varieties": [
      "OLM 203",
      "JK 8",
      "Kolab",
      "Paiyur 2"
    ],
    "sowing_window": "June 25 to July 20",
    "duration_days": "75 - 85 days",
    "expected_yield_qtl_per_acre": "5 - 8 Quintals",
    "net_income_estimate_per_acre": "₹22,000 - ₹32,000",
    "soil_suitability": "Tolerates waterlogging as well as severe drought; excels on steep tribal undulating slopes",
    "attached_schemes": [
      "Tribal Sub-Plan (TSP) free seed distributions and de-hulling machine grants",
      "High urban demand for low-glycemic diabetic lifestyle foods"
    ],
    "soil_health_benefit": "Survives without pesticide or synthetic fertilizers; ideal certified organic crop"
  },
  {
    "crop_id": "barnyard_millet_oodalu",
    "name": "Barnyard Millet / Sanwa (ఊదలు / सांवा)",
    "category": "Small Millets / Shree Anna (Fastest Maturing Cereal on Earth)",
    "season_suitability": "Kharif or Contingency",
    "water_requirement_mm": "200 - 260 mm",
    "water_savings_percentage": "82% less water than Paddy",
    "msp_rate_per_quintal": 3100,
    "recommended_varieties": [
      "PRJ 1",
      "VL Madira 207",
      "CO 2"
    ],
    "sowing_window": "July 1 to July 31",
    "duration_days": "60 - 65 days (Ready in 6 weeks)",
    "expected_yield_qtl_per_acre": "6 - 9 Quintals",
    "net_income_estimate_per_acre": "₹25,000 - ₹34,000",
    "soil_suitability": "Poor marginal soils; highly tolerant to salinity, alkalinity, and water stagnation",
    "attached_schemes": [
      "National Shree Anna Mission Fast-Track Food Aid",
      "Fasting food (Vrat Ka Chawal) premium market sales"
    ],
    "soil_health_benefit": "Produces rapid high-tonnage green fodder within 40 days of sowing"
  },
  {
    "crop_id": "kodo_millet_arikalu",
    "name": "Kodo Millet / Kodra (అరికెలు / कोदो)",
    "category": "Small Millets / Shree Anna (Centuries-Old Drought Survivor)",
    "season_suitability": "Kharif (June to July)",
    "water_requirement_mm": "200 - 280 mm",
    "water_savings_percentage": "80% less water than Paddy",
    "msp_rate_per_quintal": 3200,
    "recommended_varieties": [
      "GPUK 3",
      "RBK 155",
      "TNAU 86",
      "Jawahar Kodo 48"
    ],
    "sowing_window": "June 20 to July 15",
    "duration_days": "95 - 105 days",
    "expected_yield_qtl_per_acre": "7 - 10 Quintals",
    "net_income_estimate_per_acre": "₹26,000 - ₹38,000",
    "soil_suitability": "Gravelly, stoney, infertile soils where other grains perish completely",
    "attached_schemes": [
      "State Millet Missions and Millets-in-Ration PDS distribution initiatives",
      "High anti-oxidant polyphenolic market demand"
    ],
    "soil_health_benefit": "Grain stores for 10+ years without pest damage; ancient famine reserve grain"
  },
  {
    "crop_id": "proso_millet_varigalu",
    "name": "Proso Millet / Cheena (వరిగలు / चीना)",
    "category": "Small Millets / Shree Anna (Lowest Water Footprint Grain)",
    "season_suitability": "Summer (Catch crop) or Rabi",
    "water_requirement_mm": "160 - 220 mm",
    "water_savings_percentage": "88% less water than Paddy",
    "msp_rate_per_quintal": 2900,
    "recommended_varieties": [
      "TNAU 202",
      "DHPM 2769",
      "Meenakshi"
    ],
    "sowing_window": "February 15 to March 15 (Summer) or September-October (Rabi)",
    "duration_days": "55 - 65 days",
    "expected_yield_qtl_per_acre": "6 - 8 Quintals",
    "net_income_estimate_per_acre": "₹22,000 - ₹30,000",
    "soil_suitability": "Sandy loam, alluvial, and red soils with moderate drainage",
    "attached_schemes": [
      "Summer catch-crop diversification packages",
      "Export bird-feed and specialty flour processing contracts"
    ],
    "soil_health_benefit": "Consumes less water per gram of dry matter produced than any other domestic grain crop"
  },
  {
    "crop_id": "cluster_bean_guar",
    "name": "Cluster Bean / Guar (గోరుచిక్కుడు / ग्वार)",
    "category": "Industrial Export & Fodder Arid Crop",
    "season_suitability": "Kharif (July to August)",
    "water_requirement_mm": "180 - 250 mm (Extreme desert drought hardy)",
    "water_savings_percentage": "85% less water than Paddy",
    "msp_rate_per_quintal": 5200,
    "recommended_varieties": [
      "RGC 936",
      "RGC 1002",
      "HG 365",
      "HG 563"
    ],
    "sowing_window": "July 1 to July 31",
    "duration_days": "85 - 95 days",
    "expected_yield_qtl_per_acre": "5 - 8 Quintals",
    "net_income_estimate_per_acre": "₹30,000 - ₹48,000 depending on global gum exports",
    "soil_suitability": "Arid sandy soils, light red soils; highly sensitive to stagnant water and clay compaction",
    "attached_schemes": [
      "Industrial Guar Gum Export Council market linkages",
      "National Mission on Sustainable Agriculture (NMSA) dryland support"
    ],
    "soil_health_benefit": "Root nodules fix generous atmospheric nitrogen; enriches depleted sandy soils"
  },
  {
    "crop_id": "barley_jau",
    "name": "Barley / Jau (బార్లీ / जौ)",
    "category": "Salinity & Drought Resilient Cereal (Rabi)",
    "season_suitability": "Rabi (November-December)",
    "water_requirement_mm": "220 - 280 mm",
    "water_savings_percentage": "80% less water than Paddy",
    "msp_rate_per_quintal": 1850,
    "recommended_varieties": [
      "RD 2552",
      "RD 2035",
      "DWRB 123",
      "PL 426",
      "K 551"
    ],
    "sowing_window": "November 5 to December 5",
    "duration_days": "110 - 120 days",
    "expected_yield_qtl_per_acre": "14 - 18 Quintals",
    "net_income_estimate_per_acre": "₹28,000 - ₹38,000",
    "soil_suitability": "Tolerates high salinity (EC up to 8 dS/m) and sodicity where wheat and rice dry up completely",
    "attached_schemes": [
      "Malting industry contract farming and buyback guarantees",
      "FCI MSP procurement operations"
    ],
    "soil_health_benefit": "Tolerates brackish and saline borewell water; acts as a soil reclamation grain"
  }
];

const DISASTER_RELIEF_DATA = {
  "statutory_framework": "State Disaster Response Fund (SDRF) & National Disaster Response Fund (NDRF) Norms",
  "administered_by": "Ministry of Home Affairs (MHA), Ministry of Agriculture & State Revenue / Disaster Management Departments",
  "calamity_eligibility_threshold": "Crop loss of 33% and above caused by notified natural calamities (Hailstorm, Unseasonal Heavy Rains, Flooding, Cyclone, Drought, Pest Outbreak deemed natural calamity)",
  "input_subsidy_compensation_rates": [
    {
      "category": "Rainfed / Unirrigated Crops (e.g. Dryland Pulses, Millets, Rainfed Cotton)",
      "rate_per_hectare": "₹8,500 per hectare",
      "approx_per_acre": "₹3,440 per acre",
      "max_limit": "Subject to ceiling of 2 hectares (5 acres) per farmer",
      "loss_criteria": ">= 33% verified crop damage"
    },
    {
      "category": "Irrigated Crops (e.g. Paddy, Irrigated Cotton, Maize, Chilli)",
      "rate_per_hectare": "₹17,000 per hectare",
      "approx_per_acre": "₹6,880 per acre",
      "max_limit": "Subject to ceiling of 2 hectares (5 acres) per farmer",
      "loss_criteria": ">= 33% verified crop damage"
    },
    {
      "category": "Perennial Horticulture Crops (e.g. Mango, Citrus, Guava, Oil Palm)",
      "rate_per_hectare": "₹22,500 per hectare",
      "approx_per_acre": "₹9,100 per acre",
      "max_limit": "Subject to ceiling of 2 hectares (5 acres) per farmer",
      "loss_criteria": ">= 33% verified crop damage"
    },
    {
      "category": "Desiltation of Agricultural Land (Silt deposition > 3 inches after flash floods)",
      "rate_per_hectare": "₹18,000 per hectare",
      "approx_per_acre": "₹7,285 per acre",
      "max_limit": "Eligible for small and marginal farmers",
      "loss_criteria": "Sand/silt deposition > 3 inches rendering field uncultivable"
    }
  ],
  "telangana_special_ex_gratia": {
    "scheme_name": "Telangana Calamity Relief Assistance (Rythu Runa & Crop Relief)",
    "rate_per_acre": "₹10,000 per acre for damaged standing crops during declared unseasonal hailstorms/floods",
    "verification_team": "Joint inspection team of Agriculture Extension Officer (AEO) and Village Revenue Officer (VRO)",
    "portal": "Government Order (GO) notifications via ccla.telangana.gov.in"
  },
  "claim_enumeration_procedure": [
    "Step 1: Joint Field Enumeration (Azmoish) by Revenue Inspector / VRO and Agriculture Extension Officer (AEO) within 7 days of calamity event",
    "Step 2: Geo-tagged photo documentation with survey numbers and GPS coordinates",
    "Step 3: Preparation of draft beneficiary list displayed at Gram Panchayat / Rythu Vedika for 48 hours for public verification & objection filing",
    "Step 4: Approval by District Collector / District Disaster Management Authority (DDMA)",
    "Step 5: Direct Benefit Transfer (DBT) directly into farmer's Aadhaar-seeded bank account"
  ],
  "critical_difference_pmfby_vs_sdrf": "SDRF/NDRF is non-insurance sovereign disaster relief ex-gratia provided by the Government regardless of whether the crop was insured under PMFBY. A farmer can receive SDRF input subsidy in addition to statutory PMFBY insurance payouts.",
  "official_sources": [
    "Ministry of Home Affairs SDRF/NDRF Revised Norms 2023-2026",
    "Disaster Management Division, Ministry of Agriculture & Farmers Welfare",
    "Telangana State Disaster Management Authority (TSDMA)"
  ],
  "last_verified": "2026-11-05"
};
