const fs = require('fs');
const path = require('path');

const rootDir = path.join(__dirname, '..');
const schemesJson = JSON.parse(fs.readFileSync(path.join(rootDir, 'schemes.json'), 'utf8'));

// Extract existing 32 schemes from frontend/data.js
const oldDataFile = fs.readFileSync(path.join(rootDir, 'frontend', 'data.js'), 'utf8');

// Parse schemes data from current data.js safely by evaluating the array
let existingSchemes = [];
const arrayStart = oldDataFile.indexOf('const SCHEMES_DATA = [');
const arrayEnd = oldDataFile.indexOf('// All 36 Indian States & Union Territories');
const arrayContent = oldDataFile.slice(arrayStart + 'const SCHEMES_DATA = '.length, arrayEnd).trim();
// Strip trailing semicolon if present
const cleanArrayCode = arrayContent.endsWith(';') ? arrayContent.slice(0, -1) : arrayContent;
existingSchemes = eval(cleanArrayCode);

console.log(`Loaded ${existingSchemes.length} existing schemes from data.js`);

// Merge rules and criteria into existing schemes
const rulesMap = {};
schemesJson.forEach(s => {
  rulesMap[s.scheme_id] = s.rules;
});

existingSchemes.forEach(s => {
  const r = rulesMap[s.scheme_id] || {};
  s.rules = r;

  // Build criteria translations
  let catEn = r.tenant_allowed === false ? "Landowning farmers with Patta/RoR (Tenants excluded)" : (r.tenant_allowed ? "All farmers (Landowners and tenant cultivators)" : "Landowning farmers");
  let landEn = r.max_land_acres ? `Up to ${r.max_land_acres} Acres (Small & Marginal Farmers)` : "No land ceiling (All landholding sizes eligible)";
  let cropsEn = r.supported_crops && r.supported_crops.length ? r.supported_crops.slice(0, 4).join(', ') + "..." : "All agricultural crops";
  let locEn = s.state === 'All' ? "Pan-India (All Indian States & UTs)" : `Resident of ${s.state}`;
  let restEn = (r.excluded_categories || []).includes('income_tax_payer') ? "Income-tax payers & govt employees excluded" : (r.min_age || r.max_age ? `Age bracket ${r.min_age || 18} to ${r.max_age || 'Any'} years` : "Valid Aadhaar and land documentation required");

  s.criteria = {
    farmer_category: catEn,
    landholding: landEn,
    crops: cropsEn,
    location: locEn,
    restrictions: restEn
  };
});

// Import additional schemes from build_data.js
const buildScript = fs.readFileSync(path.join(__dirname, 'build_data.js'), 'utf8');
const addStart = buildScript.indexOf('const ADDITIONAL_SCHEMES = [');
const addEnd = buildScript.indexOf('console.log(\'Building script loaded successfully.\');');
const addCode = buildScript.slice(addStart + 'const ADDITIONAL_SCHEMES = '.length, addEnd).trim();
const cleanAddCode = addCode.endsWith(';') ? addCode.slice(0, -1) : addCode;
const additionalSchemes = eval(cleanAddCode);

console.log(`Loaded ${additionalSchemes.length} additional state schemes`);

const allSchemes = [...existingSchemes, ...additionalSchemes];

// 29 States list
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

// All 36 Indian States & UTs (for backward compatibility)
const ALL_STATES_UT = [
  ...ALL_29_STATES.map(s => s.name),
  "Andaman and Nicobar Islands",
  "Chandigarh",
  "Dadra and Nagar Haveli and Daman and Diu",
  "Delhi",
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
    hero_desc: "Select your State below to discover all eligible State Subsidies alongside Pan-India Central Government Schemes.",
    select_state_grid_title: "📍 Select Your State (All 29 Indian States)",
    select_state_hint: "Click your state box below to display available state subsidies and central schemes.",
    state_filter_placeholder: "🔍 Filter 29 states (e.g. Telangana, Punjab, Maharashtra)...",
    select_state_label: "Select Your State / Union Territory",
    select_state_placeholder: "Select your state",
    no_state_prompt: "Please select your State above to view available schemes and subsidies.",
    state_selected_banner: "Showing Agricultural Schemes for",
    badge_central: "🇮🇳 Central Govt Scheme",
    badge_state: "State Scheme",
    tab_all: "All Schemes",
    tab_state: "State Schemes",
    tab_central: "Central Schemes",
    filter_type: "Scheme Type",
    filter_eligibility: "Farmer Type",
    search_placeholder: "🔍 Search schemes by name, crop, or keyword (e.g. Paddy, Tractor, Insurance, Loan)...",
    benefit_label: "Key Benefits",
    eligibility_label: "Eligibility Summary",
    documents_label: "Required Documents",
    deadline_label: "Application Deadline & Window",
    apply_button: "Official Portal / Apply",
    last_verified_label: "Last Verified",
    no_results: "No agricultural schemes found matching your filter criteria.",
    clear_filters: "Clear Filters",
    emergency_rule: "Emergency Rule",
    check_eligibility_btn: "Check my eligibility",
    criteria_category: "Category",
    criteria_landholding: "Landholding",
    criteria_crops: "Eligible Crops",
    criteria_location: "Location",
    criteria_restrictions: "Key Rules",
    farmer_details_heading: "🧑‍🌾 Enter Your Farming Profile Details",
    form_subtitle: "Your details are matched in real-time against this scheme's verified statutory rules.",
    label_state: "📍 State / Location",
    label_farmer_type: "👥 Farmer Ownership Type",
    label_land_acres: "📐 Cultivated Land (in Acres)",
    label_crop: "🌾 Primary Crop Sown",
    label_age: "🎂 Farmer Age (Years)",
    label_tax_payer: "💼 Income Tax Payer?",
    evaluation_results_heading: "📊 Criteria Match Breakdown",
    verdict_eligible_title: "🟢 Eligible for This Scheme!",
    verdict_eligible_desc: "Based on verified statutory rules, your farming profile satisfies all criteria.",
    verdict_ineligible_title: "🔴 Criteria Not Met",
    verdict_ineligible_desc: "You do not satisfy 1 or more statutory criteria for this specific scheme.",
    btn_close: "Done / Close",
    btn_apply_portal: "Apply on Official Portal ↗"
  },
  te: {
    choose_lang: "🌐 భాషను ఎంచుకోండి",
    app_title: "కిసాన్ సేతు",
    app_subtitle: "రైతు పథకాలు & రాయితీల సహాయ కేంద్రం",
    hero_title: "మీ వ్యవసాయం కోసం ప్రభుత్వ పథకాలు మరియు సబ్సిడీలను కనుగొనండి",
    hero_desc: "రాష్ట్ర ప్రభుత్వ రాయితీలు మరియు కేంద్ర ప్రభుత్వ పథకాలను పొందడానికి క్రింద మీ రాష్ట్రాన్ని ఎంచుకోండి.",
    select_state_grid_title: "📍 మీ రాష్ట్రాన్ని ఎంచుకోండి (భారతదేశంలోని 29 రాష్ట్రాలు)",
    select_state_hint: "లభ్యమయ్యే రాష్ట్ర మరియు కేంద్ర పథకాలను చూడటానికి క్రింద మీ రాష్ట్ర పెట్టెపై క్లిక్ చేయండి.",
    state_filter_placeholder: "🔍 రాష్ట్రాన్ని శోధించండి (ఉదా: తెలంగాణ, ఆంధ్రప్రదేశ్, పంజాబ్)...",
    select_state_label: "మీ రాష్ట్రాన్ని ఎంచుకోండి",
    select_state_placeholder: "రాష్ట్రాన్ని ఎంచుకోండి",
    no_state_prompt: "పథకాలు మరియు సబ్సిడీలను వీక్షించడానికి దయచేసి పైన మీ రాష్ట్రాన్ని ఎంచుకోండి.",
    state_selected_banner: "వ్యవసాయ పథకాలు ప్రదర్శించబడుతున్న రాష్ట్రం",
    badge_central: "🇮🇳 కేంద్ర ప్రభుత్వ పథకం",
    badge_state: "రాష్ట్ర ప్రభుత్వ పథకం",
    tab_all: "అన్ని పథకాలు",
    tab_state: "రాష్ట్ర పథకాలు",
    tab_central: "కేంద్ర పథకాలు",
    filter_type: "పథకం రకం",
    filter_eligibility: "రైతు వర్గం",
    search_placeholder: "🔍 పేరు లేదా పంట ద్వారా వెతకండి (ఉదా: వరి, పత్తి, ట్రాక్టర్, పంట బీమా)...",
    benefit_label: "ప్రధాన ప్రయోజనాలు",
    eligibility_label: "అర్హత నిబంధనలు",
    documents_label: "అవసరమైన పత్రాలు",
    deadline_label: "దరఖాస్తు గడువు మరియు క్లెయిమ్ విండో",
    apply_button: "అధికారిక పోర్టల్ / దరఖాస్తు",
    last_verified_label: "చివరిగా ధృవీకరించబడింది",
    no_results: "మీ శోధనకు తగిన పథకాలు ఏవీ కనుగొనబడలేదు.",
    clear_filters: "ఫిల్టర్‌లను తొలగించండి",
    emergency_rule: "అత్యవసర నియమం",
    check_eligibility_btn: "నా అర్హతను తనిఖీ చేయండి",
    criteria_category: "రైతు వర్గం",
    criteria_landholding: "భూమి విస్తీర్ణం",
    criteria_crops: "అర్హతగల పంటలు",
    criteria_location: "ప్రాంతం",
    criteria_restrictions: "ముఖ్య నిబంధనలు",
    farmer_details_heading: "🧑‍🌾 మీ వ్యవసాయ వివరాలను నమోదు చేయండి",
    form_subtitle: "మీ వివరాలు ఈ పథకపు అధికారిక నిబంధనలతో నిజ సమయంలో సరిపోల్చబడతాయి.",
    label_state: "📍 రాష్ట్రం / నివాసం",
    label_farmer_type: "👥 భూమి యాజమాన్య రకం",
    label_land_acres: "📐 సాగు భూమి (ఎకరాలలో)",
    label_crop: "🌾 ప్రధాన సాగు పంట",
    label_age: "🎂 రైతు వయస్సు (సంవత్సరాలు)",
    label_tax_payer: "💼 ఆదాయపు పన్ను చెల్లిస్తున్నారా?",
    evaluation_results_heading: "📊 నిబంధనల సరిపోలిక నివేదిక",
    verdict_eligible_title: "🟢 మీరు ఈ పథకానికి అర్హులు!",
    verdict_eligible_desc: "అధికారిక నిబంధనల ప్రకారం, మీ వివరాలు అన్ని షరతులను సంతృప్తిపరుస్తాయి.",
    verdict_ineligible_title: "🔴 అర్హత నిబంధనలు సరిపోలలేదు",
    verdict_ineligible_desc: "ఈ పథకానికి సంబంధించి మీరు 1 లేదా అంతకంటే ఎక్కువ షరతులను అందుకోలేదు.",
    btn_close: "పూర్తయింది / మూసివేయి",
    btn_apply_portal: "అధికారిక పోర్టల్‌లో దరఖాస్తు చేసుకోండి ↗"
  },
  hi: {
    choose_lang: "🌐 भाषा चुनें",
    app_title: "किसान सेतु",
    app_subtitle: "एकीकृत कृषक योजना एवं सब्सिडी सहायक",
    hero_title: "अपने खेत के लिए सरकारी योजनाएं और सब्सिडी खोजें",
    hero_desc: "अपने राज्य की सरकारी सब्सिडी और अखिल भारतीय केंद्रीय योजनाओं को देखने के लिए नीचे अपना राज्य चुनें।",
    select_state_grid_title: "📍 अपना राज्य चुनें (भारत के सभी 29 राज्य)",
    select_state_hint: "उपलब्ध राज्य सब्सिडी और केंद्रीय योजनाएं देखने के लिए नीचे अपने राज्य बॉक्स पर क्लिक करें।",
    state_filter_placeholder: "🔍 29 राज्यों को खोजें (उदा: उत्तर प्रदेश, मध्य प्रदेश, पंजाब)...",
    select_state_label: "अपना राज्य चुनें",
    select_state_placeholder: "राज्य का चयन करें",
    no_state_prompt: "योजनाएं और सब्सिडी देखने के लिए कृपया ऊपर दिए गए बॉक्स में अपना राज्य चुनें।",
    state_selected_banner: "कृषि योजनाएं प्रदर्शित राज्य",
    badge_central: "🇮🇳 केंद्रीय सरकारी योजना",
    badge_state: "राज्य सरकारी योजना",
    tab_all: "सभी योजनाएं",
    tab_state: "राज्य योजनाएं",
    tab_central: "केंद्रीय योजनाएं",
    filter_type: "योजना का प्रकार",
    filter_eligibility: "किसान वर्ग",
    search_placeholder: "🔍 नाम या फसल से खोजें (उदा: धान, गेहूं, ट्रैक्टर, फसल बीमा, ऋण)...",
    benefit_label: "प्रमुख लाभ",
    eligibility_label: "पात्रता शर्तें",
    documents_label: "आवश्यक दस्तावेज",
    deadline_label: "आवेदन की अंतिम तिथि व विंडो",
    apply_button: "आधिकारिक पोर्टल / आवेदन करें",
    last_verified_label: "अंतिम सत्यापन",
    no_results: "कोई भी कृषि योजना नहीं मिली। कृपया फ़िल्टर हटाएं।",
    clear_filters: "फ़िल्टर हटाएं",
    emergency_rule: "आपातकालीन नियम",
    check_eligibility_btn: "मेरी पात्रता जांचें",
    criteria_category: "किसान श्रेणी",
    criteria_landholding: "भूमि सीमा",
    criteria_crops: "पात्र फसलें",
    criteria_location: "स्थान",
    criteria_restrictions: "प्रमुख नियम",
    farmer_details_heading: "🧑‍🌾 अपना कृषक प्रोफ़ाइल विवरण दर्ज करें",
    form_subtitle: "आपके विवरणों का इस योजना के आधिकारिक नियमों से वास्तविक समय में मिलान किया जाता है।",
    label_state: "📍 राज्य / स्थान",
    label_farmer_type: "👥 किसान भूमि स्वामित्व प्रकार",
    label_land_acres: "📐 कृषि भूमि (एकड़ में)",
    label_crop: "🌾 मुख्य बोई गई फसल",
    label_age: "🎂 किसान की आयु (वर्ष)",
    label_tax_payer: "💼 क्या आप आयकर दाता हैं?",
    evaluation_results_heading: "📊 पात्रता शर्तों का मिलान विवरण",
    verdict_eligible_title: "🟢 आप इस योजना के लिए पात्र हैं!",
    verdict_eligible_desc: "सत्यापित नियमों के अनुसार, आपकी प्रोफ़ाइल सभी शर्तों को पूरा करती है।",
    verdict_ineligible_title: "🔴 पात्रता शर्तें पूरी नहीं हुईं",
    verdict_ineligible_desc: "आप इस योजना की 1 या अधिक शर्तों को पूरा नहीं करते हैं।",
    btn_close: "पूर्ण / बंद करें",
    btn_apply_portal: "आधिकारिक पोर्टल पर आवेदन करें ↗"
  },
  mr: {
    choose_lang: "🌐 भाषा निवडा",
    app_title: "किसान सेतू",
    app_subtitle: "एकीकृत शेतकरी योजना व अनुदान सहाय्यक",
    hero_title: "आपल्या शेतीसाठी शासकीय योजना आणि अनुदाने शोधा",
    hero_desc: "स्थानिक राज्य अनुदाने आणि केंद्रीय योजना पाहण्यासाठी खाली आपले राज्य निवडा.",
    select_state_grid_title: "📍 आपले राज्य निवडा (भारतातील सर्व 29 राज्ये)",
    select_state_hint: "योजना पाहण्यासाठी खाली आपल्या राज्याच्या बॉक्सवर क्लिक करा.",
    state_filter_placeholder: "🔍 राज्य शोधा (उदा: महाराष्ट्र, गुजरात, पंजाब)...",
    select_state_label: "आपले राज्य निवडा",
    select_state_placeholder: "राज्य निवडा",
    no_state_prompt: "योजना आणि अनुदाने पाहण्यासाठी कृपया वर आपले राज्य निवडा.",
    state_selected_banner: "कृषी योजना दाखवत असलेले राज्य",
    badge_central: "🇮🇳 केंद्र शासन योजना",
    badge_state: "राज्य शासन योजना",
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
    no_results: "कोणतीही योजना जुळली नाही. कृपया फिल्टर काढा.",
    clear_filters: "फिल्टर काढा",
    emergency_rule: "तातडीचा नियम",
    check_eligibility_btn: "माझी पात्रता तपासा",
    criteria_category: "शेतकरी प्रवर्ग",
    criteria_landholding: "जमीन धारणा",
    criteria_crops: "पात्र पिके",
    criteria_location: "स्थान",
    criteria_restrictions: "प्रमुख अटी",
    farmer_details_heading: "🧑‍🌾 आपली शेतीविषयक माहिती प्रविष्ट करा",
    form_subtitle: "आपली माहिती या योजनेच्या अधिकृत नियमांशी तपासून पहिली जाईल.",
    label_state: "📍 राज्य / स्थान",
    label_farmer_type: "👥 जमीन मालकी प्रकार",
    label_land_acres: "📐 शेतजमीन (एकरमध्ये)",
    label_crop: "🌾 मुख्य पीक",
    label_age: "🎂 शेतकऱ्याचे वय (वर्षे)",
    label_tax_payer: "💼 आयकर भरता का?",
    evaluation_results_heading: "📊 पात्रता निकष पडताळणी",
    verdict_eligible_title: "🟢 आपण या योजनेसाठी पात्र आहात!",
    verdict_eligible_desc: "शासकीय नियमांनुसार आपली माहिती सर्व अटींची पूर्तता करते.",
    verdict_ineligible_title: "🔴 पात्रता अटी पूर्ण होत नाहीत",
    verdict_ineligible_desc: "आपण या योजनेची 1 किंवा अधिक अट पूर्ण करत नाही आहात.",
    btn_close: "पूर्ण / बंद करा",
    btn_apply_portal: "अधिकृत पोर्टलवर अर्ज करा ↗"
  },
  ta: {
    choose_lang: "🌐 மொழியைத் தேர்வுசெய்க",
    app_title: "கிசான் சேது",
    app_subtitle: "ஒருங்கிணைந்த உழவர் திட்டங்கள் & மானிய வழிகாட்டி",
    hero_title: "உங்கள் பண்ணைக்கான அரசு மானியங்கள் மற்றும் திட்டங்களை கண்டறியுங்கள்",
    hero_desc: "உங்கள் மாநிலத்தைத் தேர்வுசெய்து, மாநில மற்றும் மத்திய அரசின் திட்டங்களை ஒரே இடத்தில் பாருங்கள்.",
    select_state_grid_title: "📍 உங்கள் மாநிலத்தைத் தேர்ந்தெடுக்கவும் (அனைத்து 29 மாநிலங்கள்)",
    select_state_hint: "திட்டங்களைக் காண கீழே உங்கள் மாநிலப் பெட்டியை கிளிக் செய்யவும்.",
    state_filter_placeholder: "🔍 மாநிலங்களைத் தேடுங்கள் (எ.கா: தமிழ்நாடு, கேரளா, ஆந்திரா)...",
    select_state_label: "உங்கள் மாநிலத்தைத் தேர்ந்தெடுக்கவும்",
    select_state_placeholder: "மாநிலத்தைத் தேர்ந்தெடுக்கவும்",
    no_state_prompt: "மானியங்களைக் காண மேலே உள்ள பட்டியலில் உங்கள் மாநிலத்தைத் தேர்ந்தெடுக்கவும்.",
    state_selected_banner: "விவசாய திட்டங்கள் காட்டப்படும் மாநிலம்",
    badge_central: "🇮🇳 மத்திய அரசு திட்டம்",
    badge_state: "மாநில அரசு திட்டம்",
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
    emergency_rule: "அவசர விதி",
    check_eligibility_btn: "எனது தகுதியைச் சரிபார்க்கவும்",
    criteria_category: "விவசாயி வகை",
    criteria_landholding: "நில அளவு",
    criteria_crops: "தகுதியான பயிர்கள்",
    criteria_location: "இருப்பிடம்",
    criteria_restrictions: "முக்கிய நிபந்தனைகள்",
    farmer_details_heading: "🧑‍🌾 உங்கள் விவசாய விவரங்களை உள்ளிடவும்",
    form_subtitle: "உங்கள் விவரங்கள் இந்த திட்டத்தின் அதிகாரப்பூர்வ விதிகளுடன் ஒப்பிடப்படும்.",
    label_state: "📍 மாநிலம்",
    label_farmer_type: "👥 நில உரிமை வகை",
    label_land_acres: "📐 சாகுபடி நிலம் (ஏக்கரில்)",
    label_crop: "🌾 பயிரிடப்பட்ட பயிர்",
    label_age: "🎂 விவசாயியின் வயது",
    label_tax_payer: "💼 வருமான வரி செலுத்துபவரா?",
    evaluation_results_heading: "📊 தகுதி நிபந்தனை ஒப்பீடு",
    verdict_eligible_title: "🟢 நீங்கள் இந்த திட்டத்திற்கு தகுதியானவர்!",
    verdict_eligible_desc: "அரசு விதிகளின்படி, உங்கள் விவரங்கள் அனைத்து நிபந்தனைகளையும் பூர்த்தி செய்கின்றன.",
    verdict_ineligible_title: "🔴 தகுதி நிபந்தனைகள் பூர்த்தியாகவில்லை",
    verdict_ineligible_desc: "நீங்கள் 1 அல்லது அதற்கு மேற்பட்ட நிபந்தனைகளை பூர்த்தி செய்யவில்லை.",
    btn_close: "முடிந்தது / மூடு",
    btn_apply_portal: "அதிகாரப்பூர்வ தளத்தில் விண்ணப்பிக்கவும் ↗"
  },
  kn: {
    choose_lang: "🌐 ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    app_title: "ಕಿಸಾನ್ ಸೇತು",
    app_subtitle: "ರೈತ ಯೋಜನೆಗಳು ಮತ್ತು ಸಬ್ಸಿಡಿ ಸಹಾಯಕ",
    hero_title: "ನಿಮ್ಮ ಕೃಷಿಗಾಗಿ ಸರ್ಕಾರಿ ಸಬ್ಸಿಡಿಗಳು ಮತ್ತು ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ",
    hero_desc: "ನಿಮ್ಮ ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ ಮತ್ತು ರಾಜ್ಯ ಹಾಗೂ ಕೇಂದ್ರ ಸರ್ಕಾರದ ಕೃಷಿ ಯೋಜನೆಗಳನ್ನು ಪಡೆಯಿರಿ.",
    select_state_grid_title: "📍 ನಿಮ್ಮ ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ (ಭಾರತದ ಎಲ್ಲಾ 29 ರಾಜ್ಯಗಳು)",
    select_state_hint: "ಲಭ್ಯವಿರುವ ಯೋಜನೆಗಳನ್ನು ನೋಡಲು ಕೆಳಗೆ ನಿಮ್ಮ ರಾಜ್ಯದ ಬಾಕ್ಸ್ ಕ್ಲಿಕ್ ಮಾಡಿ.",
    state_filter_placeholder: "🔍 ರಾಜ್ಯ ಹುಡುಕಿ (ಉದಾ: ಕರ್ನಾಟಕ, ತೆಲಂಗಾಣ, ಮಹಾರಾಷ್ಟ್ರ)...",
    select_state_label: "ನಿಮ್ಮ ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    select_state_placeholder: "ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    no_state_prompt: "ಯೋಜನೆಗಳು ಮತ್ತು ಸಬ್ಸಿಡಿಗಳನ್ನು ನೋಡಲು ದಯವಿಟ್ಟು ಮೇಲೆ ನಿಮ್ಮ ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
    state_selected_banner: "ಕೃಷಿ ಯೋಜನೆಗಳನ್ನು ಪ್ರದರ್ಶಿಸುತ್ತಿರುವ ರಾಜ್ಯ",
    badge_central: "🇮🇳 ಕೇಂದ್ರ ಸರ್ಕಾರದ ಯೋಜನೆ",
    badge_state: "ರಾಜ್ಯ ಸರ್ಕಾರದ ಯೋಜನೆ",
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
    emergency_rule: "ತುರ್ತು ನಿಯಮ",
    check_eligibility_btn: "ನನ್ನ ಅರ್ಹತೆಯನ್ನು ಪರಿಶೀಲಿಸಿ",
    criteria_category: "ರೈತರ ವರ್ಗ",
    criteria_landholding: "ಭೂಮಿ ವಿಸ್ತೀರ್ಣ",
    criteria_crops: "ಅರ್ಹ ಬೆಳೆಗಳು",
    criteria_location: "ಸ್ಥಳ",
    criteria_restrictions: "ಪ್ರಮುಖ ನಿಯಮಗಳು",
    farmer_details_heading: "🧑‍🌾 ನಿಮ್ಮ ಕೃಷಿ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ",
    form_subtitle: "ನಿಮ್ಮ ವಿವರಗಳನ್ನು ಈ ಯೋಜನೆಯ ಅಧಿಕೃತ ನಿಯಮಗಳೊಂದಿಗೆ ಪರಿಶೀಲಿಸಲಾಗುತ್ತದೆ.",
    label_state: "📍 ರಾಜ್ಯ / ಸ್ಥಳ",
    label_farmer_type: "👥 ಭೂ ಒಡೆತನದ ಪ್ರಕಾರ",
    label_land_acres: "📐 ಸಾಗುವಳಿ ಭೂಮಿ (ಎಕರೆಗಳಲ್ಲಿ)",
    label_crop: "🌾 ಬೆಳೆದ ಮುಖ್ಯ ಬೆಳೆ",
    label_age: "🎂 ರೈತರ ವಯಸ್ಸು (ವರ್ಷಗಳು)",
    label_tax_payer: "💼 ಆದಾಯ ತೆರಿಗೆ ಪಾವತಿದಾರರೇ?",
    evaluation_results_heading: "📊 ಅರ್ಹತಾ ನಿಯಮಗಳ ಹೊಂದಾಣಿಕೆ ವಿವರ",
    verdict_eligible_title: "🟢 ನೀವು ಈ ಯೋಜನೆಗೆ ಅರ್ಹರಾಗಿದ್ದೀರಿ!",
    verdict_eligible_desc: "ಸರ್ಕಾರಿ ನಿಯಮಗಳ ಪ್ರಕಾರ, ನಿಮ್ಮ ವಿವರಗಳು ಎಲ್ಲಾ ಷರತ್ತುಗಳನ್ನು ಪೂರೈಸುತ್ತವೆ.",
    verdict_ineligible_title: "🔴 ಅರ್ಹತಾ ಷರತ್ತುಗಳು ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ",
    verdict_ineligible_desc: "ನೀವು ಈ ಯೋಜನೆಯ 1 ಅಥವಾ ಹೆಚ್ಚಿನ ಷರತ್ತುಗಳನ್ನು ಪೂರೈಸುತ್ತಿಲ್ಲ.",
    btn_close: "ಮುಕ್ತಾಯ / ಮುಚ್ಚಿ",
    btn_apply_portal: "ಅಧಿಕೃತ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ ↗"
  }
};

// Generate file content
const output = `// Master Scheme Data & Multi-Language Dictionary
const SCHEMES_DATA = ${JSON.stringify(allSchemes, null, 2)};

// All 29 Indian States for Clickable Grid Selection
const ALL_29_STATES = ${JSON.stringify(ALL_29_STATES, null, 2)};

// All 36 Indian States & Union Territories
const ALL_STATES_UT = ${JSON.stringify(ALL_STATES_UT, null, 2)};

// Multilingual UI Labels
const UI_TRANSLATIONS = ${JSON.stringify(UI_TRANSLATIONS, null, 2)};
`;

fs.writeFileSync(path.join(rootDir, 'frontend', 'data.js'), output, 'utf8');
console.log(`Successfully generated frontend/data.js with ${allSchemes.length} schemes across all 29 states.`);
