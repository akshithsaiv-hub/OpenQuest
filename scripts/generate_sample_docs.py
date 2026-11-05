import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
samples_dir = os.path.join(base_dir, "frontend", "samples")
os.makedirs(samples_dir, exist_ok=True)

# 1. Aadhaar Card Sample SVG
aadhaar_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 380" width="100%" height="100%">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff9933"/>
      <stop offset="50%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#138808"/>
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.15"/>
    </filter>
  </defs>
  
  <!-- Card Background -->
  <rect width="596" height="376" x="2" y="2" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" filter="url(#shadow)"/>
  
  <!-- Tricolor Header Bar -->
  <rect x="2" y="2" width="596" height="14" rx="8" fill="url(#headerGrad)"/>
  
  <!-- Header Branding -->
  <g transform="translate(24, 30)">
    <circle cx="20" cy="20" r="18" fill="#1e3a8a"/>
    <path d="M20 6 A14 14 0 0 1 20 34 A14 14 0 0 1 20 6" fill="none" stroke="#ffffff" stroke-width="2"/>
    <text x="50" y="16" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#0f172a">భారత విశిష్ట గుర్తింపు ప్రాధికార సంస్థ</text>
    <text x="50" y="32" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#475569">Unique Identification Authority of India (UIDAI)</text>
  </g>
  <text x="500" y="46" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#dc2626">GOVT OF INDIA</text>

  <!-- Watermark -->
  <text x="300" y="210" font-family="Arial, sans-serif" font-size="34" font-weight="bold" fill="#e2e8f0" text-anchor="middle" transform="rotate(-18, 300, 210)">SAMPLE MASKED COPY</text>
  
  <line x1="24" y1="74" x2="572" y2="74" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Photo Box -->
  <g transform="translate(32, 95)">
    <rect width="110" height="135" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
    <circle cx="55" cy="50" r="26" fill="#cbd5e1"/>
    <path d="M25 110 C25 85, 85 85, 85 110 Z" fill="#94a3b8"/>
    <rect x="5" y="142" width="100" height="20" rx="3" fill="#e2e8f0"/>
    <text x="55" y="156" font-family="Arial, sans-serif" font-size="10" font-weight="bold" fill="#64748b" text-anchor="middle">VERIFIED PHOTO</text>
  </g>

  <!-- Farmer Demographics -->
  <g transform="translate(160, 105)">
    <text x="0" y="16" font-family="Arial, sans-serif" font-size="13" fill="#64748b">పేరు / Name:</text>
    <text x="0" y="36" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#0f172a">కొమిరెల్లి రాములు / Komirelli Ramulu</text>
    
    <text x="0" y="65" font-family="Arial, sans-serif" font-size="12" fill="#64748b">పుట్టిన తేదీ / DOB:</text>
    <text x="120" y="65" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">14/08/1982</text>
    
    <text x="0" y="90" font-family="Arial, sans-serif" font-size="12" fill="#64748b">లింగం / Gender:</text>
    <text x="120" y="90" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">పురుషుడు / MALE</text>
    
    <text x="0" y="115" font-family="Arial, sans-serif" font-size="12" fill="#64748b">చిరునామా / Address:</text>
    <text x="0" y="132" font-family="Arial, sans-serif" font-size="11" fill="#334155">H.No 3-84, Geesugonda, Warangal Rural, Telangana - 506330</text>
  </g>

  <!-- QR Code Mock -->
  <g transform="translate(460, 95)">
    <rect width="105" height="105" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.5"/>
    <rect x="12" y="12" width="26" height="26" fill="#0f172a"/>
    <rect x="67" y="12" width="26" height="26" fill="#0f172a"/>
    <rect x="12" y="67" width="26" height="26" fill="#0f172a"/>
    <rect x="18" y="18" width="14" height="14" fill="#ffffff"/>
    <rect x="73" y="18" width="14" height="14" fill="#ffffff"/>
    <rect x="18" y="73" width="14" height="14" fill="#ffffff"/>
    <circle cx="52" cy="52" r="8" fill="#0f172a"/>
    <text x="52" y="124" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#15803d" text-anchor="middle">DIGILOCKER SECURE</text>
  </g>

  <!-- Masked Aadhaar Number -->
  <g transform="translate(300, 290)">
    <rect x="-180" y="-22" width="360" height="40" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="0" y="5" font-family="Courier, monospace" font-size="24" font-weight="bold" fill="#1e293b" text-anchor="middle" letter-spacing="3">
      XXXX  XXXX  4921
    </text>
  </g>

  <!-- Bottom Bar -->
  <rect x="2" y="336" width="596" height="42" rx="0 0 12 12" fill="#dc2626"/>
  <text x="300" y="362" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">
    నా ఆధార్, నా గుర్తింపు  |  Mera Aadhaar, Meri Pehchan (Masked for DBT Verification)
  </text>
</svg>
"""

# 2. Pahani / Dharani Land Record Sample SVG
pahani_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 420" width="100%" height="100%">
  <defs>
    <filter id="shadow2" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.12"/>
    </filter>
  </defs>

  <rect width="596" height="416" x="2" y="2" rx="10" fill="#fffdfa" stroke="#d97706" stroke-width="2" filter="url(#shadow2)"/>
  
  <!-- Header Bar -->
  <rect x="2" y="2" width="596" height="54" rx="10 10 0 0" fill="#78350f"/>
  <text x="300" y="25" font-family="Arial, sans-serif" font-size="15" font-weight="bold" fill="#fef3c7" text-anchor="middle">తెలంగాణ ప్రభుత్వం - రెవెన్యూ శాఖ (DHARANI PORTAL)</text>
  <text x="300" y="44" font-family="Arial, sans-serif" font-size="11" fill="#fde68a" text-anchor="middle">RECORD OF RIGHTS (RoR 1-B / PAHALI CULTIVATION REGISTER 2025-26)</text>

  <!-- Official Seal Watermark -->
  <text x="300" y="240" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="#fef3c7" text-anchor="middle" transform="rotate(-15, 300, 240)">OFFICIAL PAHALI EXTRACT</text>

  <!-- Grid Details -->
  <g transform="translate(30, 75)" font-family="Arial, sans-serif" font-size="12">
    <!-- Row 1 -->
    <rect x="0" y="0" width="540" height="32" fill="#fef3c7" stroke="#cbd5e1"/>
    <text x="12" y="21" font-weight="bold" fill="#78350f">జిల్లా / District:</text>
    <text x="120" y="21" fill="#0f172a">Warangal (వరంగల్)</text>
    <text x="280" y="21" font-weight="bold" fill="#78350f">మండలం / Mandal:</text>
    <text x="390" y="21" fill="#0f172a">Geesugonda (గీసుకొండ)</text>

    <!-- Row 2 -->
    <rect x="0" y="32" width="540" height="32" fill="#ffffff" stroke="#cbd5e1"/>
    <text x="12" y="53" font-weight="bold" fill="#78350f">గ్రామం / Village:</text>
    <text x="120" y="53" fill="#0f172a">Geesugonda (గీసుకొండ)</text>
    <text x="280" y="53" font-weight="bold" fill="#78350f">ఖాతా నం / Khata No:</text>
    <text x="390" y="53" font-weight="bold" fill="#0f172a">1420</text>

    <!-- Row 3 -->
    <rect x="0" y="64" width="540" height="32" fill="#fef3c7" stroke="#cbd5e1"/>
    <text x="12" y="85" font-weight="bold" fill="#78350f">సర్వే నంబరు / Survey No:</text>
    <text x="160" y="85" font-weight="bold" fill="#0369a1">284/B</text>
    <text x="280" y="85" font-weight="bold" fill="#78350f">మొత్తం విస్తీర్ణం / Extent:</text>
    <text x="420" y="85" font-weight="bold" fill="#15803d">Ac. 2.20 Gts (2.50 Acres)</text>

    <!-- Row 4 -->
    <rect x="0" y="96" width="540" height="42" fill="#ffffff" stroke="#cbd5e1"/>
    <text x="12" y="116" font-weight="bold" fill="#78350f">పట్టాదారు పేరు / Pattadar Name:</text>
    <text x="12" y="132" font-size="13" font-weight="bold" fill="#0f172a">కొమిరెల్లి రాములు S/o మల్లయ్య (Komirelli Ramulu)</text>
    <text x="360" y="116" font-weight="bold" fill="#78350f">భూమి రకం / Land Nature:</text>
    <text x="360" y="132" fill="#0f172a">మెట్ట / డ్రై (Borewell Irrigated)</text>

    <!-- Row 5 -->
    <rect x="0" y="138" width="540" height="32" fill="#fef3c7" stroke="#cbd5e1"/>
    <text x="12" y="159" font-weight="bold" fill="#78350f">సాగుదారు / Cultivator:</text>
    <text x="150" y="159" font-weight="bold" fill="#0f172a">స్వంత సాగు (Self-Cultivator)</text>
    <text x="320" y="159" font-weight="bold" fill="#78350f">పంట / Crop Sown:</text>
    <text x="430" y="159" font-weight="bold" fill="#047857">వరి (Paddy) / దూది (Cotton)</text>
  </g>

  <!-- Passbook Card Callout -->
  <g transform="translate(30, 275)">
    <rect width="540" height="65" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
    <text x="16" y="24" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#166534">E-PATTADAR PASSBOOK NUMBER (ధరణి పాస్ బుక్ సంఖ్య):</text>
    <text x="16" y="50" font-family="Courier, monospace" font-size="20" font-weight="bold" fill="#14532d">T28090041284</text>
    <text x="360" y="38" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#15803d">✅ RYTHU BHAROSA VERIFIED</text>
  </g>

  <!-- Signatures -->
  <g transform="translate(50, 365)" font-family="Arial, sans-serif" font-size="11">
    <text x="0" y="14" fill="#64748b">Verified by: Agriculture Extension Officer (AEO)</text>
    <text x="0" y="28" font-weight="bold" fill="#0f172a">Rythu Vedika, Geesugonda Node #402</text>
    
    <text x="340" y="14" fill="#64748b">Digitally Endorsed by Tahsildar</text>
    <text x="340" y="28" font-weight="bold" fill="#0f172a">Govt of Telangana MeeSeva Hub</text>
  </g>
</svg>
"""

# 3. Bank Passbook Sample SVG
passbook_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 390" width="100%" height="100%">
  <defs>
    <filter id="shadow3" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.12"/>
    </filter>
  </defs>

  <rect width="596" height="386" x="2" y="2" rx="10" fill="#ffffff" stroke="#1d4ed8" stroke-width="2" filter="url(#shadow3)"/>
  
  <!-- Bank Header -->
  <rect x="2" y="2" width="596" height="60" rx="10 10 0 0" fill="#1e40af"/>
  <circle cx="45" cy="32" r="18" fill="#ffffff"/>
  <circle cx="45" cy="32" r="9" fill="#1e40af"/>
  <rect x="42" y="32" width="6" height="15" fill="#ffffff"/>
  <text x="80" y="28" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#ffffff">భారతీయ స్టేట్ బ్యాంక్ / STATE BANK OF INDIA</text>
  <text x="80" y="47" font-family="Arial, sans-serif" font-size="12" fill="#bfdbfe">WARANGAL AGRI-COMMERCIAL BRANCH (0020144)</text>

  <!-- Passbook Header Bar -->
  <rect x="2" y="62" width="596" height="24" fill="#dbeafe"/>
  <text x="300" y="78" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#1e3a8a" text-anchor="middle">KCC &amp; DBT SAVINGS BANK PASSBOOK (సేవింగ్స్ ఖాతా పాస్‌బుక్)</text>

  <!-- Details Grid -->
  <g transform="translate(30, 105)" font-family="Arial, sans-serif" font-size="12">
    <text x="0" y="16" font-weight="bold" fill="#64748b">Account Holder Name (ఖాతాదారుని పేరు):</text>
    <text x="0" y="36" font-size="15" font-weight="bold" fill="#0f172a">KOMIRELLI RAMULU (కొమిరెల్లి రాములు)</text>

    <text x="0" y="65" font-weight="bold" fill="#64748b">Account Number (ఖాతా సంఖ్య):</text>
    <text x="0" y="86" font-family="Courier, monospace" font-size="17" font-weight="bold" fill="#1d4ed8">304928173492</text>

    <text x="280" y="65" font-weight="bold" fill="#64748b">CIF Number / Customer ID:</text>
    <text x="280" y="86" font-family="Courier, monospace" font-size="15" font-weight="bold" fill="#0f172a">88492019481</text>

    <text x="0" y="115" font-weight="bold" fill="#64748b">IFS Code (ఐఎఫ్ఎస్ కోడ్):</text>
    <text x="0" y="134" font-family="Courier, monospace" font-size="15" font-weight="bold" fill="#0f172a">SBIN0020144</text>

    <text x="280" y="115" font-weight="bold" fill="#64748b">MICR Code:</text>
    <text x="280" y="134" font-family="Courier, monospace" font-size="15" fill="#0f172a">506002008</text>

    <text x="0" y="165" font-weight="bold" fill="#64748b">Branch Address (శాఖ చిరునామా):</text>
    <text x="0" y="182" fill="#334155">Main Road, Warangal City, Telangana - 506002. Ph: 0870-2421004</text>
  </g>

  <!-- DBT & NPCI Active Status Badge -->
  <g transform="translate(30, 305)">
    <rect width="540" height="60" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
    <circle cx="30" cy="30" r="14" fill="#22c55e"/>
    <text x="30" y="35" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">✓</text>
    <text x="56" y="24" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#15803d">Aadhaar NPCI Mapping Status: ACTIVE &amp; SEEDED (DBT Enabled)</text>
    <text x="56" y="44" font-family="Arial, sans-serif" font-size="11" fill="#166534">Eligible for instant Direct Benefit Transfer (PM-KISAN, Rythu Bharosa, PMFBY Claims)</text>
  </g>
</svg>
"""

# 4. CCRC (Crop Cultivator Rights Card) Sample SVG
ccrc_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 410" width="100%" height="100%">
  <defs>
    <filter id="shadow4" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.12"/>
    </filter>
  </defs>

  <rect width="596" height="406" x="2" y="2" rx="10" fill="#ffffff" stroke="#ea580c" stroke-width="2" filter="url(#shadow4)"/>
  
  <!-- Header Bar -->
  <rect x="2" y="2" width="596" height="56" rx="10 10 0 0" fill="#c2410c"/>
  <text x="300" y="25" font-family="Arial, sans-serif" font-size="15" font-weight="bold" fill="#ffffff" text-anchor="middle">కౌలు రైతు హక్కుల ధృవీకరణ పత్రం (CCRC)</text>
  <text x="300" y="44" font-family="Arial, sans-serif" font-size="11" fill="#fed7aa" text-anchor="middle">CROP CULTIVATOR RIGHTS CARD - STATUTORY LEASE ENDORSEMENT</text>

  <!-- Watermark -->
  <text x="300" y="230" font-family="Arial, sans-serif" font-size="34" font-weight="bold" fill="#ffedd5" text-anchor="middle" transform="rotate(-15, 300, 230)">STATUTORY TENANT CARD</text>

  <!-- Body Content -->
  <g transform="translate(30, 75)" font-family="Arial, sans-serif" font-size="12">
    <!-- Card ID -->
    <rect x="0" y="0" width="540" height="34" rx="4" fill="#fff7ed" stroke="#fdba74"/>
    <text x="16" y="22" font-weight="bold" fill="#9a3412">CCRC Registration ID:</text>
    <text x="180" y="22" font-family="Courier, monospace" font-size="15" font-weight="bold" fill="#c2410c">CCRC-TS-2026-9912</text>
    <text x="370" y="22" font-weight="bold" fill="#9a3412">Validity Season:</text>
    <text x="470" y="22" font-weight="bold" fill="#047857">Rabi 2025-26</text>

    <!-- Tenant Details -->
    <rect x="0" y="44" width="540" height="70" rx="4" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="16" y="66" font-weight="bold" fill="#64748b">కౌలు రైతు పేరు / Tenant Farmer:</text>
    <text x="16" y="86" font-size="15" font-weight="bold" fill="#0f172a">బానోత్ పద్మ (Banoth Padma) W/o రామ్ సింగ్</text>
    <text x="16" y="104" font-size="11" fill="#475569">Aadhaar: XXXX-XXXX-7721 • Social Category: ST (Lambada) • Phone: 9701234567</text>

    <!-- Land Owner Details -->
    <rect x="0" y="124" width="540" height="70" rx="4" fill="#ffffff" stroke="#e2e8f0"/>
    <text x="16" y="146" font-weight="bold" fill="#64748b">భూ యజమాని పేరు / Landowner (Pattadar):</text>
    <text x="16" y="166" font-size="14" font-weight="bold" fill="#0f172a">K. Venkat Reddy S/o నారాయణ రెడ్డి</text>
    <text x="16" y="184" font-size="11" fill="#475569">Pattadar Passbook: T192004210 • Village: Kallur, Khammam</text>

    <!-- Land & Crop Details -->
    <rect x="0" y="204" width="540" height="60" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
    <text x="16" y="226" font-weight="bold" fill="#64748b">సర్వే నం / Survey No:</text>
    <text x="135" y="226" font-weight="bold" fill="#0f172a">142/A</text>
    
    <text x="230" y="226" font-weight="bold" fill="#64748b">కౌలు విస్తీర్ణం / Extent:</text>
    <text x="350" y="226" font-weight="bold" fill="#15803d">1.80 Acres</text>

    <text x="16" y="250" font-weight="bold" fill="#64748b">సాగు పంట / Leased Crop:</text>
    <text x="145" y="250" font-weight="bold" fill="#c2410c">మిర్చి / Chilli &amp; పత్తి / Cotton</text>
  </g>

  <!-- Legal Protection Notice -->
  <g transform="translate(30, 350)" font-family="Arial, sans-serif">
    <rect width="540" height="42" rx="4" fill="#fff7ed" stroke="#fed7aa"/>
    <text x="14" y="18" font-size="10" font-weight="bold" fill="#9a3412">చట్టపరమైన హామీ / Statutory Protection:</text>
    <text x="14" y="32" font-size="9.5" fill="#7c2d12">Under AP/TS Land Licensed Cultivators Act, CCRC confers crop insurance &amp; subsidy rights to tenant WITHOUT affecting landowner's ownership.</text>
  </g>
</svg>
"""

with open(os.path.join(samples_dir, "sample_aadhaar.svg"), "w", encoding="utf-8") as f:
    f.write(aadhaar_svg)

with open(os.path.join(samples_dir, "sample_pahani.svg"), "w", encoding="utf-8") as f:
    f.write(pahani_svg)

with open(os.path.join(samples_dir, "sample_passbook.svg"), "w", encoding="utf-8") as f:
    f.write(passbook_svg)

with open(os.path.join(samples_dir, "sample_ccrc.svg"), "w", encoding="utf-8") as f:
    f.write(ccrc_svg)

print("All 4 sample documents generated successfully in frontend/samples/!")
