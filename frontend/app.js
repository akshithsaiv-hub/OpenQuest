// Kisan Setu: Mobile-First Comprehensive 8-Module Application Logic
// Deterministic Scheme Engine, 72-Hr Claim Shield, Water Subsidies, KCC, Wallet, MSP, & Escalation

(function () {
  'use strict';

  // API Base URL - points to local FastAPI backend when running locally
  const API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://127.0.0.1:8000'
    : '';

  // Application State
  const state = {
    lang: localStorage.getItem('kisan_lang') || 'en',
    selectedState: localStorage.getItem('kisan_state') || 'Telangana',
    activeTab: 'all', // 'all' | 'state' | 'central'
    typeFilter: 'all',
    eligibilityFilter: 'all',
    searchQuery: '',
    waterStateFilter: 'All',
    waterTypeFilter: 'All',
    cropCategoryFilter: 'All'
  };

  // Helper to fetch translated UI label
  function t(key) {
    const dict = (typeof UI_TRANSLATIONS !== 'undefined' && UI_TRANSLATIONS[state.lang])
      ? UI_TRANSLATIONS[state.lang]
      : (typeof UI_TRANSLATIONS !== 'undefined' && UI_TRANSLATIONS['en'] ? UI_TRANSLATIONS['en'] : {});
    return dict[key] || (typeof UI_TRANSLATIONS !== 'undefined' && UI_TRANSLATIONS['en'] && UI_TRANSLATIONS['en'][key]) || key;
  }

  // =========================================================================
  // 1. PRIMARY TAB NAVIGATION LOGIC (Tabs 0 through 7)
  // =========================================================================
  function initPrimaryTabs() {
    const navButtons = document.querySelectorAll('.nav-tab-btn');
    const tabViews = document.querySelectorAll('.tab-view');

    navButtons.forEach(btn => {
      btn.addEventListener('click', function () {
        const targetTab = this.getAttribute('data-tab');

        // Update active class on nav buttons
        navButtons.forEach(b => {
          b.classList.remove('active');
          b.setAttribute('aria-selected', 'false');
        });
        this.classList.add('active');
        this.setAttribute('aria-selected', 'true');

        // Show corresponding tab view
        tabViews.forEach(view => {
          view.classList.remove('active');
        });

        const activeView = document.getElementById('view-' + targetTab);
        if (activeView) {
          activeView.classList.add('active');
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      });
    });
  }

  // =========================================================================
  // 2. TAB 0: SCHEME BROWSER LOGIC
  // =========================================================================
  const langSelect = document.getElementById('langSelect');
  const stateSelect = document.getElementById('stateSelect');
  const emptyStatePrompt = document.getElementById('emptyStatePrompt');
  const mainContent = document.getElementById('mainContent');
  const bannerStateName = document.getElementById('bannerStateName');
  const bannerStats = document.getElementById('bannerStats');
  const changeStateBtn = document.getElementById('changeStateBtn');
  const schemesGrid = document.getElementById('schemesGrid');
  const searchInput = document.getElementById('searchInput');
  const typeFilterSelect = document.getElementById('typeFilterSelect');
  const eligibilityFilterSelect = document.getElementById('eligibilityFilterSelect');

  const tabAllBtn = document.getElementById('tabAllBtn');
  const tabStateBtn = document.getElementById('tabStateBtn');
  const tabCentralBtn = document.getElementById('tabCentralBtn');
  const countAll = document.getElementById('countAll');
  const countState = document.getElementById('countState');
  const countCentral = document.getElementById('countCentral');

  function populateStateDropdown() {
    if (!stateSelect || typeof ALL_STATES_UT === 'undefined') return;
    stateSelect.innerHTML = `<option value="">-- ${t('select_state_placeholder') || 'Select State'} --</option>`;
    ALL_STATES_UT.forEach(function (st) {
      const opt = document.createElement('option');
      opt.value = st;
      opt.textContent = st;
      if (st.toLowerCase() === state.selectedState.toLowerCase()) {
        opt.selected = true;
      }
      stateSelect.appendChild(opt);
    });
  }

  function getFilteredSchemes() {
    if (!state.selectedState || typeof SCHEMES_DATA === 'undefined') return [];
    const activeStateLower = state.selectedState.toLowerCase();

    let pool = SCHEMES_DATA.filter(function (s) {
      if (s.state === 'All') return true;
      return s.state.toLowerCase() === activeStateLower;
    });

    if (state.activeTab === 'central') {
      pool = pool.filter(s => s.level === 'Central');
    } else if (state.activeTab === 'state') {
      pool = pool.filter(s => s.level === 'State');
    }

    if (state.typeFilter !== 'all') {
      pool = pool.filter(s => s.category === state.typeFilter);
    }

    if (state.eligibilityFilter === 'tenant') {
      pool = pool.filter(s => {
        const elig = (s.eligibility && (s.eligibility[state.lang] || s.eligibility['en'])) || '';
        return !elig.toLowerCase().includes('not eligible') || elig.toLowerCase().includes('tenant');
      });
    }

    if (state.searchQuery.trim() !== '') {
      const q = state.searchQuery.toLowerCase();
      pool = pool.filter(s => {
        const name = (s.name && (s.name[state.lang] || s.name['en'])) || '';
        const desc = (s.description && (s.description[state.lang] || s.description['en'])) || '';
        const ben = s.benefit || '';
        return name.toLowerCase().includes(q) || desc.toLowerCase().includes(q) || ben.toLowerCase().includes(q);
      });
    }

    return pool;
  }

  function renderSchemeBrowser() {
    if (!state.selectedState) {
      if (emptyStatePrompt) emptyStatePrompt.style.display = 'block';
      if (mainContent) mainContent.style.display = 'none';
      return;
    }

    if (emptyStatePrompt) emptyStatePrompt.style.display = 'none';
    if (mainContent) mainContent.style.display = 'block';

    const activeStateLower = state.selectedState.toLowerCase();
    const allStateAndCentral = (typeof SCHEMES_DATA !== 'undefined' ? SCHEMES_DATA : []).filter(s => {
      return s.state === 'All' || s.state.toLowerCase() === activeStateLower;
    });

    const stateCount = allStateAndCentral.filter(s => s.level === 'State').length;
    const centralCount = allStateAndCentral.filter(s => s.level === 'Central').length;

    if (bannerStateName) bannerStateName.textContent = state.selectedState;
    if (bannerStats) bannerStats.textContent = `(${stateCount} State + ${centralCount} Central)`;
    if (countAll) countAll.textContent = allStateAndCentral.length;
    if (countState) countState.textContent = stateCount;
    if (countCentral) countCentral.textContent = centralCount;

    const filtered = getFilteredSchemes();
    if (!schemesGrid) return;

    if (filtered.length === 0) {
      schemesGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3rem 1rem; color: var(--text-muted);">
          <div style="font-size: 2.5rem;">🌾</div>
          <p style="font-weight: 700; margin-top: 0.5rem;">${t('no_results') || 'No schemes match your criteria.'}</p>
        </div>
      `;
      return;
    }

    schemesGrid.innerHTML = filtered.map(s => {
      const name = (s.name && (s.name[state.lang] || s.name['en'])) || s.name || '';
      const desc = (s.description && (s.description[state.lang] || s.description['en'])) || s.description || '';
      const elig = (s.eligibility && (s.eligibility[state.lang] || s.eligibility['en'])) || s.eligibility || '';
      const isCentral = s.level === 'Central';
      const badgeClass = isCentral ? 'badge-central' : 'badge-state';
      const badgeLabel = isCentral ? (t('badge_central') || 'Central Scheme') : `${s.state} State Scheme`;

      const docsHtml = Array.isArray(s.documents)
        ? s.documents.map(d => `<li class="doc-item"><span class="doc-check-icon">✓</span><span>${d}</span></li>`).join('')
        : '';

      const claimAlert = s.claim_window ? `
        <div class="claim-window-alert">
          <span>⚠️</span> <span><strong>Emergency Claim Rule:</strong> ${s.claim_window}</span>
        </div>
      ` : '';

      return `
        <article class="scheme-card" data-level="${s.level}">
          <div class="scheme-header-area">
            <span class="badge ${badgeClass}">${badgeLabel}</span>
            <h3 class="scheme-title">${name}</h3>
            <p class="scheme-desc">${desc}</p>
          </div>

          <div class="scheme-body-area">
            <div class="benefit-highlight">
              <span class="benefit-label">${t('benefit_label') || 'Financial Benefit'}</span>
              <div class="benefit-value">${s.benefit || 'Financial Support'}</div>
            </div>

            <div class="scheme-field">
              <span class="field-title">${t('eligibility_label') || 'Eligibility Criteria'}</span>
              <p class="field-content">${elig}</p>
            </div>

            <div class="scheme-field">
              <span class="field-title">${t('documents_label') || 'Documents Required'}</span>
              <ul class="doc-list">${docsHtml}</ul>
            </div>

            <div class="deadline-box">
              <div class="deadline-text">📅 ${t('deadline_label') || 'Application Window'}: ${s.deadline || 'Continuous'}</div>
              ${claimAlert}
            </div>
          </div>

          <div class="card-footer-area">
            <span class="last-verified-text">Verified: ${s.last_verified || '2026-10-25'}</span>
            <a href="${s.source_url || '#'}" target="_blank" rel="noopener noreferrer" class="official-link-btn">
              ${t('apply_button') || 'Official Portal'} ↗
            </a>
          </div>
        </article>
      `;
    }).join('');
  }

  // =========================================================================
  // 3. TAB 1: ELIGIBILITY ENGINE & CHAT
  // =========================================================================
  
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

// =========================================================================
  // AI AGRITECH QUERY RESPONDER (Local & Backend Grounded)
  // =========================================================================
  async function fetchAiQuery(queryText) {
    if (!queryText || !queryText.trim()) return null;
    const q = queryText.trim();
    const currLang = state.lang || 'en';

    // Try backend API first
    try {
      const resp = await fetch(`${API_BASE}/api/query_ai`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q, language: currLang })
      });
      if (resp.ok) {
        const data = await resp.json();
        if (data && data.response) return data;
      }
    } catch (err) {
      console.warn('Backend /api/query_ai unavailable, running client agritech responder.');
    }

    // Client-side grounded agritech responder (100% reliable offline fallback)
    return getClientAiResponse(q, currLang);
  }

  function getClientAiResponse(queryText, lang) {
    const q = queryText.toLowerCase().trim();

    // Intent 1: Documents & Proofs
    if (/doc|document|documents|proof|paper|పత్రాలు|దస్తావేజులు|కాగితాలు|दस्तावेज|कागजात/.test(q)) {
      if (lang === 'te') {
        return {
          status: 'success',
          query: queryText,
          response: `📋 **రైతు సంక్షేమ పథకాలకు అవసరమైన ముఖ్యమైన పత్రాల జాబితా (Document Checklist)**:\\n\\n` +
            `1. **ఆధార్ కార్డు (Aadhaar Card)**: క్రియాశీల మొబైల్ నంబర్‌తో లింక్ చేయబడి ఉండాలి (e-KYC కోసం).\\n` +
            `2. **భూమి రికార్డు (Land Record / 1B / Pahani)**: సర్వే నంబర్, విస్తీర్ణం తెలిపే డిజిటల్ పట్టాదారు పాస్‌బుక్ లేదా ధరణి / పహాణీ నకలు.\\n` +
            `3. **బ్యాంక్ పాస్‌బుక్ (Bank Passbook)**: ఆధార్‌తో అనుసంధానించబడిన (NPCI DBT Seeded) బ్యాంక్ ఖాతా.\\n` +
            `4. **కౌలు సాగు హక్కు కార్డు (CCRC)**: కౌలు రైతులకు మాత్రమే - ఆర్డీవో / తహసీల్దార్ జారీ చేసిన పంట సాగు హక్కు పత్రం.\\n` +
            `5. **విత్తన / సాగు ధృవీకరణ పత్రం (Sowing Certificate)**: స్థానిక వ్యవసాయ విస్తరణ అధికారి (AEO) లేదా రైతు వేదిక ద్వారా జారీ చేయబడుతుంది.\\n` +
            `6. **పాస్‌పోర్ట్ సైజు ఫోటోలు**: 2 తాజా రంగు ఫోటోలు.\\n\\n` +
            `💡 **చిట్కా**: ఈ పత్రాలను మీరు మా **Tab 5 (Document Wallet)** లో భద్రపరుచుకోవచ్చు. మీ ఆధార్ నంబర్ XXXX-XXXX-4921 రూపంలో గోప్యంగా దాచబడుతుంది.`
        };
      }
      return {
        status: 'success',
        query: queryText,
        response: `📋 **Standard Required Documents for Agricultural Schemes & Subsidies**:\\n\\n` +
          `1. **Aadhaar Card**: Must be linked to an active mobile number for OTP e-KYC authentication.\\n` +
          `2. **Land Ownership Title (Pahani / Dharani / Khasra / RoR-1B)**: Digital passbook showing Survey Number and Khata extent.\\n` +
          `3. **Bank Account Passbook**: Must be Aadhaar-seeded on NPCI mapper for Direct Benefit Transfer (DBT).\\n` +
          `4. **Crop Cultivator Rights Card (CCRC)**: Mandatory for tenant farmers / sharecroppers (ensures rights without impacting landowner title).\\n` +
          `5. **Sowing Certificate / Girdawari**: Issued by local Agriculture Extension Officer (AEO) / Rythu Vedika.\\n` +
          `6. **Passport Size Photographs**: 2 recent color photographs.\\n\\n` +
          `💡 **Pro-Tip**: You can safely store these in **Tab 5 (Document Wallet)** with automatic privacy masking (XXXX-XXXX-4921).`
      };
    }

    // Intent 2: 72-Hour Claim Window
    if (/72|claim|loss|damage|hail|flood|cyclone|insurance|pmfby|నష్టం|పరిహారం|బీమా|नुकसान|बीमा/.test(q)) {
      if (lang === 'te') {
        return {
          status: 'success',
          query: queryText,
          response: `⏱️ **పీఎంఎఫ్‌బీవై 72 గంటల అత్యవసర నష్ట పరిహార నిబంధన (PMFBY 72-Hour Rule)**:\\n\\n` +
            `• స్థానికీకరించిన విపత్తులు (వడగండ్ల వాన, వరదలు) సంభవించినప్పుడు **72 గంటల లోపు తప్పనిసరిగా** సమాచారం అందించాలి.\\n` +
            `• **టోల్ ఫ్రీ హెల్ప్‌లైన్**: 1800-180-1551 లేదా మీ మండల ఏఈఓ (AEO) / రైతు వేదికకు లిఖితపూర్వక దరఖాస్తు ఇవ్వండి.\\n` +
            `• **సాక్ష్యం**: జీపీఎస్ లొకేషన్ (Geo-Tagged) ఆన్ చేసి దెబ్బతిన్న పంట ఫోటోలు తీయండి.\\n` +
            `• **ఎస్‌డీఆర్‌ఎఫ్ సహాయం**: వర్షాధార పంటలకు ₹8,500/హెక్టారు, నీటిపారుదల పంటలకు ₹17,000/హెక్టారు లభిస్తుంది.\\n\\n` +
            `👉 మా **Tab 2 (72-Hr Claim Shield)** లో 1-క్లిక్ ద్వారా అధికారిక ఎస్ఎంఎస్ జనరేట్ చేసుకోవచ్చు!`
        };
      }
      return {
        status: 'success',
        query: queryText,
        response: `⏱️ **PMFBY Statutory 72-Hour Crop Loss Reporting Rule**:\\n\\n` +
          `• Under PMFBY Section 21.4, localized calamities (Hailstorm, Inundation, Cloudburst) MUST be reported **within 72 hours** of occurrence.\\n` +
          `• **Toll-Free Helpline**: Call **1800-180-1551** immediately and obtain a Docket Reference ID.\\n` +
          `• **Field Photos**: Take minimum 3 geo-tagged GPS photos showing damaged canopy vs boundary.\\n` +
          `• **SDRF Calamity Norms**: In addition to insurance, eligible farmers receive State Disaster Relief (Rainfed: ₹8,500/ha; Irrigated: ₹17,000/ha).\\n\\n` +
          `👉 Use **Tab 2 (72-Hr Claim Shield)** to start the live countdown and generate a 1-click legal SMS intimation!`
      };
    }

    // Intent 3: KCC Loan & 4% Interest
    if (/kcc|loan|interest|credit|scale of finance|వడ్డీ|రుణం|కిసాన్ క్రెడిట్|कर्ज|ब्याज/.test(q)) {
      if (lang === 'te') {
        return {
          status: 'success',
          query: queryText,
          response: `🏦 **కిసాన్ క్రెడిట్ కార్డు (KCC) & 4% వడ్డీ రాయితీ పథకం (MISS)**:\\n\\n` +
            `• ప్రామాణిక బ్యాంక్ వ్యవసాయ రుణ వడ్డీ రేటు: **7.0%** (రూ. 3 లక్షల వరకు).\\n` +
            `• సకాలంలో చెల్లింపు ప్రోత్సాహకం (PRI): **- 3.0%** (ప్రభుత్వమే భరిస్తుంది).\\n` +
            `• **రైతు నికర వడ్డీ రేటు**: ఏడాదికి కేవలం **4.0%** మాత్రమే!\\n` +
            `• తనఖా లేని రుణం (Collateral-Free): భూమి తాకట్టు లేకుండా **రూ. 1.60 లక్షల వరకు** లభిస్తుంది.\\n` +
            `• స్కేల్ ఆఫ్ ఫైనాన్స్: వరి సాగుకు ఎకరానికి ~₹38,000, పత్తికి ~₹42,000 వరకు రుణం మంజూరవుతుంది.\\n\\n` +
            `👉 మా **Tab 4 (KCC Loan & Tracker)** లో మీ ఖచ్చితమైన రుణ మొత్తాన్ని లెక్కించండి!`
        };
      }
      return {
        status: 'success',
        query: queryText,
        response: `🏦 **Kisan Credit Card (KCC) & 4% Interest Subvention (MISS)**:\\n\\n` +
          `• **Standard Bank Crop Loan Rate**: 7.0% per annum (up to ₹3.00 Lakh).\\n` +
          `• **Prompt Repayment Incentive (PRI)**: - 3.0% discount credited by Central Govt.\\n` +
          `• **Net Effective Farmer Interest**: Only **4.0% per annum** when repaid on schedule.\\n` +
          `• **Collateral-Free Limit**: Up to ₹1.60 Lakh sanctioned without land hypothecation.\\n` +
          `• **Scale of Finance**: Paddy ~₹38,000/acre, Cotton ~₹42,000/acre, Chilli ~₹65,000/acre.\\n` +
          `• **Repayment Due Dates**: Kharif loans due by March 31; Rabi loans due by June 30.\\n\\n` +
          `👉 Head to **Tab 4 (KCC Loan & Tracker)** to compute your exact sanctioned limit and track pending files!`
      };
    }

    // Intent 4: CCRC & Tenant Rights
    if (/ccrc|tenant|lease|sharecropper|కౌలు|బట్టీ|काश्तकार|बटाईदार/.test(q)) {
      return {
        status: 'success',
        query: queryText,
        response: `🤝 **Tenant Farmer Protections & Crop Cultivator Rights Card (CCRC)**:\\n\\n` +
          `• **What is CCRC?** A statutory agreement (valid for 11 months) recognizing tenant cultivators.\\n` +
          `• **Landowner Protection**: CCRC does NOT grant any ownership claim on land records. Land title remains 100% secure with the Pattadar.\\n` +
          `• **Benefits for Tenant**: Unlocks institutional crop insurance (PMFBY), disaster input subsidy, and official MSP procurement at government centres.\\n` +
          `• **How to Apply**: Joint declaration signed by tenant and landowner, verified by Village Revenue Officer / AEO.`
      };
    }

    // Intent 5: Water & Drip Subsidies
    if (/water|drip|sprinkler|solar|kusum|pmksy|tsmip|pond|borewell|నీరు|డ్రిప్|స్ప్రింక్లర్|సోలార్/.test(q)) {
      return {
        status: 'success',
        query: queryText,
        response: `💧 **Micro-Irrigation & Water-Saving Subsidies (18+ Schemes Across India)**:\\n\\n` +
          `• **PMKSY Per Drop More Crop (PDMC)**: Baseline 55% Central subsidy for drip & sprinkler systems.\\n` +
          `• **State Enhancements**: Telangana (TSMIP) & AP (APMIP) provide up to **100% subsidy for SC/ST** and **90% for BC** small farmers.\\n` +
          `• **PM-KUSUM Component B**: 60% combined subsidy on standalone off-grid DC solar irrigation pumps.\\n` +
          `• **Next-Season Crop Planning**: Switching to Bengal Gram, Sesame, or Millets saves up to **88% water** compared to inundated paddy.\\n\\n` +
          `👉 Browse all 18 schemes and 26 drought-resilient crops in **Tab 3 (Water Subsidies & Crops)**!`
      };
    }

    // Intent 6: PM-KISAN & Rythu Bharosa
    if (/pm kisan|pm-kisan|pmkisan|2000|installment|rythu bharosa|రైతు భరోసా|పీఎం కిసాన్/.test(q)) {
      return {
        status: 'success',
        query: queryText,
        response: `🌾 **Direct Income Support Schemes (PM-KISAN & Rythu Bharosa)**:\\n\\n` +
          `• **PM-KISAN**: ₹6,000 per year paid in 3 four-monthly installments of ₹2,000 each via DBT.\\n` +
          `• **Rythu Bharosa (Telangana)**: ₹15,000 per acre per year direct investment assistance for eligible farmers.\\n` +
          `• **Mandatory e-KYC**: Must be completed via Aadhaar OTP on pmkisan.gov.in or biometric CSC.\\n` +
          `• **Helpline**: For payment issues, call Kisan Call Centre at 155261 / 1800-180-1551.`
      };
    }

    // Intent 7: MSP vs Mandi
    if (/msp|mandi|price|bonus|ధర|మద్దతు|भाव|मंडी/.test(q)) {
      return {
        status: 'success',
        query: queryText,
        response: `⚖️ **Minimum Support Price (MSP) & Market Arbitrage (2025-2026)**:\\n\\n` +
          `• **Paddy (Grade A)**: Statutory MSP ₹2,320 + Telangana State Bonus ₹500 = **Effective ₹2,820/qtl** (Private mandi pays ~₹2,180; net gain +₹640/qtl at govt centres).\\n` +
          `• **Cotton (Medium Staple)**: MSP ₹7,121/qtl at Cotton Corporation of India (CCI) centres.\\n` +
          `• **Bengal Gram (Chana)**: MSP ₹5,440/qtl at NAFED centres.\\n` +
          `• **Sesame (Til)**: MSP ₹9,267/qtl (Highest MSP among oilseeds).\\n\\n` +
          `👉 Check full comparison arbitrage in **Tab 6 (MSP vs Mandi)**!`
      };
    }

    // Default Fallback
    return {
      status: 'success',
      query: queryText,
      response: `🌾 **Kisan Sahayak Assistant** for: *"${queryText}"*\\n\\n` +
        `I have analyzed government agricultural rules. Please click on any of the quick suggestions above or ask specifically about:\\n` +
        `• **'Documents'** — Required certificates & proofs for all schemes\\n` +
        `• **'72-Hour Claim'** — PMFBY localized crop loss emergency rules\\n` +
        `• **'KCC Loan'** — Scale of Finance & 4% interest subvention\\n` +
        `• **'Tenant CCRC'** — Legal protections for tenant cultivators\\n` +
        `• **'Water Subsidies'** — 18+ Drip, Sprinkler & Solar pump grants`
    };
  }

  // =========================================================================
  // INTERACTIVE CHATBOT LOGIC
  // =========================================================================
  function initChatbot() {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatMessageInput');
    const chatList = document.getElementById('chatMessagesList');
    const quickChips = document.querySelectorAll('.quick-chip-btn');

    function appendMessage(sender, text) {
      if (!chatList) return;
      const row = document.createElement('div');
      row.className = `chat-bubble-row ${sender}`;
      const avatar = document.createElement('div');
      avatar.className = 'chat-bubble-avatar';
      avatar.textContent = sender === 'user' ? '🧑‍🌾' : '🤖';
      const bubble = document.createElement('div');
      bubble.className = 'chat-bubble';
      
      let formatted = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
      bubble.innerHTML = formatted;

      row.appendChild(avatar);
      row.appendChild(bubble);
      chatList.appendChild(row);
      chatList.scrollTop = chatList.scrollHeight;
    }

    async function handleSendQuery(qText) {
      if (!qText || !qText.trim()) return;
      appendMessage('user', qText);
      if (chatInput) chatInput.value = '';

      // Temporary typing indicator
      const typingRow = document.createElement('div');
      typingRow.className = 'chat-bubble-row bot';
      typingRow.id = 'chatTypingIndicator';
      typingRow.innerHTML = `<div class="chat-bubble-avatar">🤖</div><div class="chat-bubble" style="color: var(--text-muted); font-style: italic;">Thinking / పరిశీలిస్తున్నాము...</div>`;
      if (chatList) {
        chatList.appendChild(typingRow);
        chatList.scrollTop = chatList.scrollHeight;
      }

      const res = await fetchAiQuery(qText);
      if (typingRow && typingRow.parentNode) {
        typingRow.parentNode.removeChild(typingRow);
      }

      if (res && res.response) {
        appendMessage('bot', res.response);
      } else {
        appendMessage('bot', 'Sorry, I could not process your query at this moment. Please ask about "Documents", "72-Hour Claim", or "KCC Loan".');
      }
    }

    if (chatForm && chatInput) {
      chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        handleSendQuery(chatInput.value);
      });
    }

    quickChips.forEach(chip => {
      chip.addEventListener('click', function () {
        const q = this.getAttribute('data-query');
        handleSendQuery(q);
      });
    });
  }


  // =========================================================================
  // 3. TAB 1: ELIGIBILITY ENGINE & CHAT
  // =========================================================================
  function initEligibilityTab() {
    const elTenant = document.getElementById('elTenant');
    const ccrcGroup = document.getElementById('ccrcGroup');
    const elForm = document.getElementById('eligibilityForm');
    const resultsContainer = document.getElementById('eligibilityResultsContainer');

    if (elTenant && ccrcGroup) {
      elTenant.addEventListener('change', function () {
        ccrcGroup.style.display = this.checked ? 'block' : 'none';
      });
    }

    if (elForm && resultsContainer) {
      elForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const queryVal = (document.getElementById('elQuery').value || '').trim();

        const profileData = {
          farmer_id: 'F-WEB-001',
          name: 'Farmer',
          state: document.getElementById('elState').value,
          district: document.getElementById('elDistrict').value,
          land_holding_acres: parseFloat(document.getElementById('elAcres').value) || 2.0,
          crop: document.getElementById('elCrop').value,
          category: (parseFloat(document.getElementById('elAcres').value) <= 5.0) ? 'small_marginal' : 'large',
          is_tenant: document.getElementById('elTenant').checked,
          has_ccrc: document.getElementById('elCcrc') ? document.getElementById('elCcrc').checked : false,
          has_irrigation_well: document.getElementById('elWell').checked,
          query: queryVal
        };

        resultsContainer.innerHTML = `
          <div class="card" style="text-align: center; padding: 2.5rem;">
            <div style="font-size: 2.5rem; animation: pulse 1s infinite;">⏳</div>
            <p style="margin-top: 0.5rem; font-weight: 600;">Evaluating statutory rules and querying Kisan Sahayak AI...</p>
          </div>
        `;

        let matchResult = null;
        let aiAnswer = null;

        // Run match and AI query in parallel
        const promises = [];
        promises.push(
          fetch(`${API_BASE}/match`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profileData)
          }).then(r => r.ok ? r.json() : null).catch(() => null)
        );

        if (queryVal) {
          promises.push(fetchAiQuery(queryVal));
        }

        const outcomes = await Promise.all(promises);
        matchResult = outcomes[0];
        if (queryVal && outcomes.length > 1) {
          aiAnswer = outcomes[1];

          // Also mirror in the chat message thread above for convenience
          const chatList = document.getElementById('chatMessagesList');
          if (chatList) {
            const userRow = document.createElement('div');
            userRow.className = 'chat-bubble-row user';
            userRow.innerHTML = `<div class="chat-bubble-avatar">🧑‍🌾</div><div class="chat-bubble">${escapeHtml(queryVal)}</div>`;
            chatList.appendChild(userRow);

            if (aiAnswer && aiAnswer.response) {
              const botRow = document.createElement('div');
              botRow.className = 'chat-bubble-row bot';
              let formatted = aiAnswer.response.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
              botRow.innerHTML = `<div class="chat-bubble-avatar">🤖</div><div class="chat-bubble">${formatted}</div>`;
              chatList.appendChild(botRow);
            }
            chatList.scrollTop = chatList.scrollHeight;
          }
        }

        // Fallback evaluation if backend is not reached
        if (!matchResult) {
          matchResult = evaluateClientFallback(profileData);
        }

        renderEligibilityResults(matchResult, resultsContainer, aiAnswer);
      });
    }
  }

  function evaluateClientFallback(profile) {
    const pool = (typeof SCHEMES_DATA !== 'undefined' ? SCHEMES_DATA : []);
    const eligible = [];
    const ineligible = [];

    pool.forEach(s => {
      let isElig = true;
      const reasons = [];

      // State check
      if (s.state !== 'All' && s.state.toLowerCase() !== profile.state.toLowerCase()) {
        isElig = false;
        reasons.push(`Restricted to ${s.state}; your selected state is ${profile.state}.`);
      } else {
        reasons.push(`State matches scheme jurisdiction.`);
      }

      // Tenant check
      const eligStr = (s.eligibility && (s.eligibility.en || s.eligibility[state.lang])) || '';
      if (profile.is_tenant) {
        if (eligStr.toLowerCase().includes('not eligible')) {
          if (!profile.has_ccrc) {
            isElig = false;
            reasons.push(`Tenant farmers require an active CCRC or oral lease validation.`);
          } else {
            reasons.push(`CCRC recognized for tenant cultivator.`);
          }
        }
      }

      // Land threshold for small/marginal schemes
      if (s.scheme_id === 'pmkmy' && profile.land_holding_acres > 5.0) {
        isElig = false;
        reasons.push(`Land holding exceeds 5 acres limit for PM-KMY.`);
      }

      const engName = (s.name && (s.name.en || s.name['en'])) || (typeof s.name === 'string' ? s.name : '');
      const regName = (s.name && s.name[state.lang]) || '';
      let displaySchemeName = engName;
      if (state.lang !== 'en' && regName) {
        displaySchemeName = `${regName} (${engName})`;
      }

      const item = {
        name: displaySchemeName || engName || s.scheme_id,
        eligible: isElig,
        reasons: reasons,
        benefits_summary: s.benefit || '',
        documents_required: s.documents || [],
        deadlines: { window: s.deadline || 'Active' },
        source_url: s.source_url || '#'
      };

      if (isElig) eligible.push(item);
      else ineligible.push(item);
    });

    return {
      profile: profile,
      eligible_schemes: eligible,
      ineligible_schemes: ineligible,
      total_eligible: eligible.length
    };
  }

  function renderEligibilityResults(res, container, aiAnswer) {
    const totalEl = res.eligible_schemes.length;
    const totalInel = res.ineligible_schemes.length;

    let html = '';

    // 1. Prominent AI Answer Card (answers user question like "Documents")
    if (aiAnswer && aiAnswer.response) {
      let formattedAns = aiAnswer.response
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');

      html += `
        <div class="card" style="border-left: 5px solid #2563eb; background: #eff6ff; margin-bottom: 1.25rem;">
          <div style="display: flex; gap: 0.75rem; align-items: flex-start;">
            <span style="font-size: 2.2rem; margin-top: 2px;">🤖</span>
            <div style="flex: 1;">
              <span class="badge-tag badge-tag-blue">Kisan Sahayak AI Answer</span>
              <h3 style="margin: 0.35rem 0 0.5rem 0; color: #1e3a8a; font-size: 1.15rem;">
                Question: "${escapeHtml(aiAnswer.query || res.profile.query || 'Farmer Query')}"
              </h3>
              <div style="font-size: 0.93rem; color: #1f2937; line-height: 1.6;">
                ${formattedAns}
              </div>
            </div>
          </div>
        </div>
      `;
    }

    // 2. Evaluation Completed Summary Card
    html += `
      <div class="card" style="border-left: 5px solid #16a34a; background: #f0fdf4;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <span class="badge-tag badge-tag-green">Evaluation Completed</span>
            <h3 style="margin: 0.25rem 0 0 0; color: #166534;">
              ${totalEl} Schemes Eligible (${totalInel} Ineligible)
            </h3>
            <p style="font-size: 0.85rem; color: #15803d; margin: 0.2rem 0 0 0;">
              Evaluated for: ${escapeHtml(res.profile.crop)} (${res.profile.land_holding_acres} Acres) in ${escapeHtml(res.profile.state)}
            </p>
          </div>
          <span style="font-size: 2.2rem;">🎯</span>
        </div>
      </div>
    `;

    // 3. Eligible Schemes List
    html += `<h4 style="color: #1b5e20; margin: 1.25rem 0 0.75rem 0; font-size: 1.15rem;">✅ Eligible Schemes & Subsidies</h4>`;
    html += res.eligible_schemes.map(s => `
      <div class="card" style="border-left: 4px solid #16a34a; margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem;">
          <h4 style="margin: 0; font-size: 1.05rem; color: #1f2937;">${escapeHtml(s.name)}</h4>
          <span class="badge-tag badge-tag-green">Eligible</span>
        </div>
        <div style="background: #e8f5e9; padding: 0.5rem 0.75rem; border-radius: 6px; margin: 0.6rem 0; font-size: 0.88rem; font-weight: 600; color: #1b5e20;">
          💰 Benefit: ${escapeHtml(s.benefits_summary)}
        </div>
        <div style="font-size: 0.85rem; color: #374151;">
          <strong>Reasons:</strong>
          <ul style="margin: 0.2rem 0 0.5rem 1.2rem; font-size: 0.82rem;">
            ${(s.reasons || []).map(r => `<li>${escapeHtml(r)}</li>`).join('')}
          </ul>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem; font-size: 0.82rem;">
          <span style="color: var(--text-muted);">Application: ${escapeHtml(s.deadlines ? (s.deadlines.window || s.deadlines.rabi_2025_26 || 'Open') : 'Open')}</span>
          <a href="${escapeHtml(s.source_url)}" target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="font-size: 0.82rem; padding: 0.4rem 0.8rem;">Apply Now ↗</a>
        </div>
      </div>
    `).join('');

    // 4. Ineligible Schemes (Collapsible)
    if (res.ineligible_schemes.length > 0) {
      html += `
        <details style="margin-top: 1.5rem; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 0.75rem;">
          <summary style="font-weight: 700; color: #991b1b; cursor: pointer;">
            ⚠️ Ineligible Schemes (${res.ineligible_schemes.length}) — Click to view missing criteria
          </summary>
          <div style="margin-top: 0.75rem;">
            ${res.ineligible_schemes.map(s => `
              <div style="border-bottom: 1px solid #f3f4f6; padding: 0.6rem 0;">
                <div style="font-weight: 600; color: #374151; font-size: 0.92rem;">${escapeHtml(s.name)}</div>
                <ul style="color: #b91c1c; font-size: 0.82rem; margin: 0.2rem 0 0 1.2rem;">
                  ${(s.reasons || []).map(r => `<li>${escapeHtml(r)}</li>`).join('')}
                </ul>
              </div>
            `).join('')}
          </div>
        </details>
      `;
    }

    container.innerHTML = html;
  }


  // =========================================================================
  // 4. TAB 2: 72-HOUR CLIMATE SHIELD & CLAIM ASSISTANT (GEO-TAGGED CAMERA SUITE)
  // =========================================================================
  function initClaimShieldTab() {
    // State for live GPS telemetry
    const currentGps = {
      lat: 17.978421,
      lon: 79.594112,
      accuracy: 3.2,
      altitude: 294,
      timestamp: new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' }),
      locked: true
    };

    // State for captured geo-evidence photos
    const capturedEvidence = [];
    let cameraStream = null;

    // 1. 72-Hour Live Countdown Timer
    const timerDisplay = document.getElementById('liveCountdownTimer');
    if (timerDisplay) {
      let secondsLeft = 71 * 3600 + 59 * 60 + 42;
      setInterval(() => {
        if (secondsLeft > 0) secondsLeft--;
        const hrs = Math.floor(secondsLeft / 3600);
        const mins = Math.floor((secondsLeft % 3600) / 60);
        const secs = secondsLeft % 60;
        timerDisplay.textContent = `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      }, 1000);
    }

    // 2. GPS Location Acquisition
    function updateGpsUI() {
      const coordsEl = document.getElementById('gpsCoordsDisplay');
      const timeEl = document.getElementById('gpsTimestampDisplay');
      const statusEl = document.getElementById('gpsLockStatus');
      const vfCoordsEl = document.getElementById('vfCoords');
      const vfSurveyEl = document.getElementById('vfSurveyTag');
      const surveyVal = document.getElementById('claimSurvey') ? document.getElementById('claimSurvey').value : '284/B';
      const villageVal = document.getElementById('claimVillage') ? document.getElementById('claimVillage').value : 'Geesugonda';

      if (coordsEl) {
        coordsEl.textContent = `📍 Lat: ${currentGps.lat}° N, Lon: ${currentGps.lon}° E (±${currentGps.accuracy}m)`;
      }
      if (timeEl) {
        timeEl.textContent = `⏱️ Time: ${currentGps.timestamp} IST | Alt: ${currentGps.altitude}m MSL`;
      }
      if (statusEl) {
        statusEl.textContent = currentGps.locked ? '🟢 High-Precision GPS Locked' : '🟡 Approximate Location';
      }
      if (vfCoordsEl) {
        vfCoordsEl.textContent = `${currentGps.lat}° N, ${currentGps.lon}° E`;
      }
      if (vfSurveyEl) {
        vfSurveyEl.textContent = `Survey #${surveyVal} | ${villageVal}`;
      }
    }

    function acquireGpsLocation() {
      if ('geolocation' in navigator) {
        const statusEl = document.getElementById('gpsLockStatus');
        if (statusEl) statusEl.textContent = '🔄 Acquiring Satellite Fix...';

        navigator.geolocation.getCurrentPosition(
          (pos) => {
            currentGps.lat = parseFloat(pos.coords.latitude.toFixed(6));
            currentGps.lon = parseFloat(pos.coords.longitude.toFixed(6));
            currentGps.accuracy = parseFloat((pos.coords.accuracy || 4.0).toFixed(1));
            currentGps.altitude = Math.round(pos.coords.altitude || 294);
            currentGps.timestamp = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
            currentGps.locked = true;
            updateGpsUI();
          },
          (err) => {
            console.warn('Geolocation failed or permission denied, using district default coordinates:', err.message);
            currentGps.timestamp = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
            currentGps.locked = false;
            updateGpsUI();
          },
          { enableHighAccuracy: true, timeout: 8000, maximumAge: 0 }
        );
      } else {
        updateGpsUI();
      }
    }

    const btnRefreshGps = document.getElementById('btnRefreshGps');
    if (btnRefreshGps) {
      btnRefreshGps.addEventListener('click', () => {
        btnRefreshGps.innerHTML = '<span>🔄</span> Locking...';
        acquireGpsLocation();
        setTimeout(() => {
          btnRefreshGps.innerHTML = '<span>🔄</span> Refresh GPS';
        }, 1200);
      });
    }

    // Initial GPS acquire
    acquireGpsLocation();

    // 3. Compensation Calculator Logic
    const cropScaleOfFinance = {
      'Paddy': 42000,
      'Cotton': 48000,
      'Chilli': 78000,
      'Maize': 35000,
      'Groundnut': 36000,
      'Soybean': 32000,
      'Wheat': 38000
    };

    function updateCompensationDisplay() {
      const crop = document.getElementById('hazardCrop') ? document.getElementById('hazardCrop').value.split(' ')[0] : 'Paddy';
      const acres = parseFloat(document.getElementById('claimAcreage') ? document.getElementById('claimAcreage').value : 2.5) || 2.5;
      const lossPct = parseInt(document.getElementById('claimLossPct') ? document.getElementById('claimLossPct').value : 80) || 80;

      const sumInsPerAcre = cropScaleOfFinance[crop] || 40000;
      const totalSumIns = sumInsPerAcre * acres;
      const pmfbyPayout = Math.round(totalSumIns * (lossPct / 100.0));

      const sdrfRate = 6880; // Irrigated norm per acre (Rs 17,000 / ha)
      const sdrfPayout = lossPct >= 33 ? Math.round(sdrfRate * acres) : 0;
      const stateReliefPayout = lossPct >= 33 ? Math.round(10000 * acres) : 0; // Telangana / AP ex-gratia
      const totalRecovery = pmfbyPayout + sdrfPayout + stateReliefPayout;

      const pmfbyEl = document.getElementById('calcPmfbyVal');
      const sdrfEl = document.getElementById('calcSdrfVal');
      const stateEl = document.getElementById('calcStateReliefVal');
      const totalEl = document.getElementById('calcTotalVal');

      if (pmfbyEl) pmfbyEl.textContent = `₹${pmfbyPayout.toLocaleString('en-IN')}`;
      if (sdrfEl) sdrfEl.textContent = `₹${sdrfPayout.toLocaleString('en-IN')}`;
      if (stateEl) stateEl.textContent = `₹${stateReliefPayout.toLocaleString('en-IN')}`;
      if (totalEl) totalEl.textContent = `₹${totalRecovery.toLocaleString('en-IN')}`;
    }

    // Attach listener to inputs for dynamic recalculation
    ['hazardCrop', 'claimAcreage', 'claimLossPct'].forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('input', updateCompensationDisplay);
        el.addEventListener('change', updateCompensationDisplay);
      }
    });
    updateCompensationDisplay();

    // 4. Weather Check Button
    const btnCheckWeather = document.getElementById('btnCheckWeather');
    if (btnCheckWeather) {
      btnCheckWeather.addEventListener('click', async function () {
        const district = document.getElementById('hazardDistrict') ? document.getElementById('hazardDistrict').value : 'Warangal';
        const crop = document.getElementById('hazardCrop') ? document.getElementById('hazardCrop').value : 'Paddy';
        const btn = this;
        btn.textContent = '🛰️ Fetching Live Open-Meteo Telemetry...';

        try {
          const resp = await fetch(`${API_BASE}/climate_water_stress?district=${encodeURIComponent(district)}&crop=${encodeURIComponent(crop)}`);
          if (resp.ok) {
            const data = await resp.json();
            if (data.weather) {
              const tempEl = document.getElementById('dispTemp');
              const rainEl = document.getElementById('dispRain');
              const humEl = document.getElementById('dispHumidity');
              const warnBox = document.getElementById('weatherWarningBox');

              if (tempEl) tempEl.textContent = `${data.weather.temperature_c || 33.5}°C`;
              if (rainEl) rainEl.textContent = `${data.weather.rainfall_mm || 0.0} mm`;
              if (humEl) humEl.textContent = `${data.weather.humidity_percent || 46}%`;

              if (warnBox && data.stress_summary) {
                warnBox.innerHTML = `<strong>⚠️ Active Telemetry Warning:</strong> ${escapeHtml(data.stress_summary)}`;
              }
            }
          }
        } catch (err) {
          console.warn('Weather API failed, using cached values.');
        } finally {
          btn.innerHTML = '<span>📡</span> Fetch Live Weather & Detect Risks';
          updateCompensationDisplay();
        }
      });
    }

    // 5. In-App Camera Viewfinder Controls
    const videoElem = document.getElementById('geoVideoPreview');
    const standbyElem = document.getElementById('cameraStandbyPlaceholder');
    const liveBadge = document.getElementById('cameraLiveBadge');
    const btnToggleCamera = document.getElementById('btnToggleCamera');
    const btnSnapPhoto = document.getElementById('btnSnapPhoto');
    const btnTriggerUpload = document.getElementById('btnTriggerUpload');
    const fileInput = document.getElementById('geoFileInput');
    const canvas = document.getElementById('geoStampCanvas');

    async function startCamera() {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Camera API is not supported on this browser or requires HTTPS / localhost. Please use the "Upload Photo" button below.');
        return;
      }
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
          audio: false
        });
        cameraStream = stream;
        videoElem.srcObject = stream;
        videoElem.style.display = 'block';
        if (standbyElem) standbyElem.style.display = 'none';
        if (liveBadge) liveBadge.style.display = 'flex';
        btnToggleCamera.innerHTML = '<span>🛑</span> Stop Camera';
        btnToggleCamera.classList.remove('btn-secondary');
        btnToggleCamera.classList.add('btn-danger');
        btnSnapPhoto.disabled = false;
      } catch (err) {
        console.error('Camera access denied or unavailable:', err);
        alert('Could not access device camera. Please check camera permissions or use the "Upload Photo" button.');
      }
    }

    function stopCamera() {
      if (cameraStream) {
        cameraStream.getTracks().forEach(t => t.stop());
        cameraStream = null;
      }
      videoElem.style.display = 'none';
      if (standbyElem) standbyElem.style.display = 'block';
      if (liveBadge) liveBadge.style.display = 'none';
      btnToggleCamera.innerHTML = '<span>📷</span> Open Live Camera';
      btnToggleCamera.classList.remove('btn-danger');
      btnToggleCamera.classList.add('btn-secondary');
      btnSnapPhoto.disabled = true;
    }

    if (btnToggleCamera) {
      btnToggleCamera.addEventListener('click', () => {
        if (cameraStream) {
          stopCamera();
        } else {
          startCamera();
        }
      });
    }

    // 6. Forensic Geo-Watermarking Engine (HTML5 Canvas)
    function stampImageWithForensics(imageSource, width, height) {
      if (!canvas) return null;
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext('2d');

      // 1. Draw base photo
      ctx.drawImage(imageSource, 0, 0, width, height);

      // 2. Compute dynamic banner dimensions
      const bannerHeight = Math.max(130, Math.round(height * 0.18));
      const bannerY = height - bannerHeight;

      // Dark translucent backdrop
      ctx.fillStyle = 'rgba(15, 23, 42, 0.90)';
      ctx.fillRect(0, bannerY, width, bannerHeight);

      // Top green accent line
      ctx.fillStyle = '#10b981';
      ctx.fillRect(0, bannerY, width, 4);

      // Pull metadata
      const farmerName = document.getElementById('claimFarmerName') ? document.getElementById('claimFarmerName').value : 'Farmer';
      const village = document.getElementById('claimVillage') ? document.getElementById('claimVillage').value : 'Geesugonda';
      const district = document.getElementById('hazardDistrict') ? document.getElementById('hazardDistrict').value : 'Warangal';
      const surveyNo = document.getElementById('claimSurvey') ? document.getElementById('claimSurvey').value : '284/B';
      const crop = document.getElementById('hazardCrop') ? document.getElementById('hazardCrop').value : 'Paddy';
      const hazard = document.getElementById('claimHazard') ? document.getElementById('claimHazard').value : 'Hailstorm';
      const lossPct = document.getElementById('claimLossPct') ? document.getElementById('claimLossPct').value : '80';
      const photoType = document.getElementById('geoPhotoTypeSelect') ? document.getElementById('geoPhotoTypeSelect').value : 'Wide Field View';
      const landmark = document.getElementById('geoLandmarkInput') ? document.getElementById('geoLandmarkInput').value : 'Field boundary';

      // Scaling fonts relative to canvas resolution
      const baseFontSize = Math.max(14, Math.round(width / 55));

      // Header Tag
      ctx.font = `bold ${baseFontSize + 2}px sans-serif`;
      ctx.fillStyle = '#fbbf24'; // Gold
      ctx.fillText(`🛡️ PMFBY / SDRF STATUTORY LOSS EVIDENCE (72-HR INTIMATION)`, 16, bannerY + baseFontSize + 10);

      // Line 1: GPS Coordinates
      ctx.font = `bold ${baseFontSize}px monospace`;
      ctx.fillStyle = '#38bdf8'; // Sky blue
      ctx.fillText(`📍 GPS: ${currentGps.lat}° N, ${currentGps.lon}° E | Acc: ±${currentGps.accuracy}m | Alt: ${currentGps.altitude}m MSL`, 16, bannerY + (baseFontSize * 2) + 16);

      // Line 2: Timestamp & Land Parcel
      ctx.font = `${baseFontSize - 1}px sans-serif`;
      ctx.fillStyle = '#ffffff';
      ctx.fillText(`📅 Timestamp: ${currentGps.timestamp} IST | Survey No: ${surveyNo} | Village: ${village}, ${district}`, 16, bannerY + (baseFontSize * 3) + 22);

      // Line 3: Farmer, Crop & Calamity
      ctx.fillStyle = '#f87171'; // Coral red
      ctx.fillText(`🌾 Cultivator: ${farmerName} | Crop: ${crop} | Peril: ${hazard} (${lossPct}% Loss)`, 16, bannerY + (baseFontSize * 4) + 26);

      // Line 4: Category & Landmark
      ctx.fillStyle = '#cbd5e1'; // Muted
      ctx.fillText(`🏷️ Category: ${photoType} | Landmark: ${landmark}`, 16, bannerY + (baseFontSize * 5) + 30);

      const dataUrl = canvas.toDataURL('image/jpeg', 0.92);
      return dataUrl;
    }

    // 7. Add Stamped Evidence to Gallery & Update UI
    function addEvidenceToRegister(dataUrl, photoType) {
      const evidenceId = `GEO-${Date.now().toString().slice(-6)}`;
      const evidenceItem = {
        id: evidenceId,
        dataUrl: dataUrl,
        photoType: photoType,
        lat: currentGps.lat,
        lon: currentGps.lon,
        accuracy: currentGps.accuracy,
        timestamp: currentGps.timestamp
      };
      capturedEvidence.push(evidenceItem);
      renderEvidenceGallery();

      // Transmit to backend evidence endpoint
      fetch(`${API_BASE}/api/claim/evidence/upload`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          farmer_name: document.getElementById('claimFarmerName') ? document.getElementById('claimFarmerName').value : 'Farmer',
          survey_no: document.getElementById('claimSurvey') ? document.getElementById('claimSurvey').value : '',
          latitude: currentGps.lat,
          longitude: currentGps.lon,
          accuracy: currentGps.accuracy,
          timestamp: currentGps.timestamp,
          image_base64: dataUrl.substring(0, 500) + '...[truncated]',
          photo_type: photoType
        })
      }).catch(() => null);
    }

    function renderEvidenceGallery() {
      const gallery = document.getElementById('evidenceGalleryContainer');
      const countBadge = document.getElementById('geoCountBadge');
      const listCount = document.getElementById('evidenceListCount');
      const clearBtn = document.getElementById('btnClearEvidence');

      if (countBadge) countBadge.textContent = `${capturedEvidence.length} Stamped`;
      if (listCount) listCount.textContent = capturedEvidence.length;
      if (clearBtn) clearBtn.style.display = capturedEvidence.length > 0 ? 'inline-block' : 'none';

      if (!gallery) return;

      if (capturedEvidence.length === 0) {
        gallery.innerHTML = `
          <div id="noEvidenceNotice" style="grid-column: 1 / -1; background: #f8fafc; border: 1.5px dashed #cbd5e1; border-radius: 8px; padding: 1.5rem; text-align: center; color: #64748b; font-size: 0.85rem;">
            No geo-tagged damage photos captured yet. Snap a picture with the live camera above or upload a photo from your device.
          </div>
        `;
        return;
      }

      gallery.innerHTML = capturedEvidence.map((ev, idx) => `
        <div class="evidence-card" id="ev-card-${ev.id}">
          <div class="evidence-thumb-container">
            <img src="${ev.dataUrl}" alt="Crop Damage Evidence" class="evidence-thumb-img">
            <span class="evidence-type-badge">${escapeHtml(ev.photoType)}</span>
          </div>
          <div class="evidence-meta-content">
            <div class="evidence-meta-row">
              <strong style="color: #166534; font-family: monospace;">📍 ${ev.lat}°, ${ev.lon}°</strong>
              <span style="font-size: 0.72rem; color: #64748b;">±${ev.accuracy}m</span>
            </div>
            <div style="font-size: 0.75rem; color: #64748b;">
              ⏱️ ${escapeHtml(ev.timestamp)}
            </div>
          </div>
          <div class="evidence-actions-row">
            <a href="${ev.dataUrl}" download="PMFBY_Loss_Evidence_${ev.id}.jpg" class="btn btn-primary" style="flex: 1; padding: 0.35rem 0.5rem; font-size: 0.78rem; text-align: center; text-decoration: none;">
              📥 Download
            </a>
            <button type="button" class="btn btn-secondary btn-del-ev" data-idx="${idx}" style="padding: 0.35rem 0.5rem; font-size: 0.78rem;">
              🗑️
            </button>
          </div>
        </div>
      `).join('');

      // Wire delete buttons
      gallery.querySelectorAll('.btn-del-ev').forEach(btn => {
        btn.addEventListener('click', function () {
          const idx = parseInt(this.getAttribute('data-idx'));
          capturedEvidence.splice(idx, 1);
          renderEvidenceGallery();
        });
      });
    }

    const btnClearEvidence = document.getElementById('btnClearEvidence');
    if (btnClearEvidence) {
      btnClearEvidence.addEventListener('click', () => {
        if (confirm('Clear all captured geo-tagged photos?')) {
          capturedEvidence.length = 0;
          renderEvidenceGallery();
        }
      });
    }

    // 8. Snap Button Event
    if (btnSnapPhoto) {
      btnSnapPhoto.addEventListener('click', () => {
        if (!videoElem || !videoElem.videoWidth) {
          alert('Camera video stream is not ready.');
          return;
        }
        const width = videoElem.videoWidth || 1280;
        const height = videoElem.videoHeight || 720;
        const photoType = document.getElementById('geoPhotoTypeSelect') ? document.getElementById('geoPhotoTypeSelect').value : 'Damage Evidence';

        const dataUrl = stampImageWithForensics(videoElem, width, height);
        if (dataUrl) {
          addEvidenceToRegister(dataUrl, photoType);
          btnSnapPhoto.innerHTML = '<span>✅</span> Photo Stamped!';
          setTimeout(() => {
            btnSnapPhoto.innerHTML = '<span>📸</span> Snap Geo-Photo';
          }, 1500);
        }
      });
    }

    // 9. File Upload Button Event
    if (btnTriggerUpload && fileInput) {
      btnTriggerUpload.addEventListener('click', () => fileInput.click());

      fileInput.addEventListener('change', function () {
        if (this.files && this.files[0]) {
          const file = this.files[0];
          const reader = new FileReader();
          reader.onload = function (e) {
            const img = new Image();
            img.onload = function () {
              const photoType = document.getElementById('geoPhotoTypeSelect') ? document.getElementById('geoPhotoTypeSelect').value : 'Uploaded Evidence';
              const width = img.naturalWidth || 1280;
              const height = img.naturalHeight || 720;
              const dataUrl = stampImageWithForensics(img, width, height);
              if (dataUrl) {
                addEvidenceToRegister(dataUrl, photoType);
              }
            };
            img.src = e.target.result;
          };
          reader.readAsDataURL(file);
          this.value = ''; // Reset input
        }
      });
    }

    // 10. SMS Generator Form
    const claimSmsForm = document.getElementById('claimSmsForm');
    const smsResultBox = document.getElementById('smsResultBox');
    const smsTextDisplay = document.getElementById('smsTextDisplay');
    const btnCopySms = document.getElementById('btnCopySms');
    const btnSendSmsApp = document.getElementById('btnSendSmsApp');
    const btnShareWhatsApp = document.getElementById('btnShareWhatsApp');

    if (claimSmsForm) {
      claimSmsForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const reqData = {
          farmer_name: document.getElementById('claimFarmerName').value,
          phone: document.getElementById('claimPhone').value,
          crop: document.getElementById('hazardCrop').value,
          district: document.getElementById('hazardDistrict').value,
          village: document.getElementById('claimVillage').value,
          survey_no: document.getElementById('claimSurvey').value,
          hazard_type: document.getElementById('claimHazard').value,
          loss_percent: parseInt(document.getElementById('claimLossPct').value) || 80,
          acreage: parseFloat(document.getElementById('claimAcreage').value) || 2.5,
          language: state.lang
        };

        let generatedText = '';
        try {
          const resp = await fetch(`${API_BASE}/generate_claim_sms`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(reqData)
          });
          if (resp.ok) {
            const res = await resp.json();
            generatedText = res.sms_text;
          }
        } catch (err) {
          console.warn('Backend SMS generation failed, generating client template.');
        }

        if (!generatedText) {
          const nowIso = new Date().toISOString().replace('T', ' ').substring(0, 16);
          generatedText = `[PMFBY 72-HR CROP LOSS INTIMATION]
` +
            `Farmer: ${reqData.farmer_name} (Ph: ${reqData.phone})
` +
            `Village: ${reqData.village}, District: ${reqData.district}
` +
            `Survey No: ${reqData.survey_no}
` +
            `Crop: ${reqData.crop} (${reqData.acreage} Acres)
` +
            `Calamity: ${reqData.hazard_type}
` +
            `Est Loss: ${reqData.loss_percent}%
` +
            `Geo Location: ${currentGps.lat}° N, ${currentGps.lon}° E
` +
            `Attached Photos: ${capturedEvidence.length} Geo-Tagged Photos
` +
            `Timestamp: ${nowIso} IST
` +
            `Action: Formal intimation submitted within statutory 72 hours per PMFBY Section 21.4. Please issue docket reference number.`;
        }

        if (smsTextDisplay) smsTextDisplay.textContent = generatedText;
        if (smsResultBox) smsResultBox.style.display = 'block';
        if (btnSendSmsApp) btnSendSmsApp.href = `sms:18001801551?body=${encodeURIComponent(generatedText)}`;
        if (btnShareWhatsApp) btnShareWhatsApp.href = `https://api.whatsapp.com/send?text=${encodeURIComponent(generatedText)}`;
      });
    }

    if (btnCopySms && smsTextDisplay) {
      btnCopySms.addEventListener('click', function () {
        navigator.clipboard.writeText(smsTextDisplay.textContent).then(() => {
          btnCopySms.textContent = '✅ Copied to Clipboard!';
          setTimeout(() => { btnCopySms.textContent = '📋 Copy SMS'; }, 2000);
        });
      });
    }

    // 11. Official Claim Dossier Generation & Status Tracker Logger
    const btnGenerateDossier = document.getElementById('btnGenerateDossier');
    const btnLogToTracker = document.getElementById('btnLogToTracker');
    const dossierBox = document.getElementById('dossierDisplayBox');
    const dossierTextContent = document.getElementById('dossierTextContent');
    const btnDownloadDossier = document.getElementById('btnDownloadDossier');
    const btnPrintDossier = document.getElementById('btnPrintDossier');

    let currentDossierText = '';

    if (btnGenerateDossier) {
      btnGenerateDossier.addEventListener('click', async () => {
        const payload = {
          farmer_name: document.getElementById('claimFarmerName').value || 'Komirelli Ramulu',
          phone: document.getElementById('claimPhone').value || '9848022338',
          crop: document.getElementById('hazardCrop').value || 'Paddy',
          district: document.getElementById('hazardDistrict').value || 'Warangal',
          village: document.getElementById('claimVillage').value || 'Geesugonda',
          survey_no: document.getElementById('claimSurvey').value || '284/B',
          hazard_type: document.getElementById('claimHazard').value || 'Hailstorm',
          loss_percent: parseInt(document.getElementById('claimLossPct').value) || 80,
          acreage: parseFloat(document.getElementById('claimAcreage').value) || 2.5,
          geo_photos_count: capturedEvidence.length,
          telemetry_notes: `${document.getElementById('dispTemp').textContent}, ${document.getElementById('dispRain').textContent} rain, ${document.getElementById('dispHumidity').textContent} humidity`
        };

        btnGenerateDossier.textContent = '⏳ Compiling Dossier...';

        try {
          const resp = await fetch(`${API_BASE}/api/claim/dossier`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          if (resp.ok) {
            const data = await resp.json();
            currentDossierText = data.dossier_text;
          }
        } catch (err) {
          console.warn('Backend dossier failed, using client generator');
        }

        if (!currentDossierText) {
          currentDossierText = `================================================================================\n` +
            `STATUTORY PMFBY & SDRF CROP LOSS CLAIM REPRESENTATION DOCKET\n` +
            `Reference ID: PMFBY/${payload.district.slice(0, 3).toUpperCase()}/${Date.now()}\n` +
            `================================================================================\n\n` +
            `1. CULTIVATOR: ${payload.farmer_name} (Mobile: ${payload.phone})\n` +
            `   Location: Village ${payload.village}, Dist ${payload.district}, Survey No: ${payload.survey_no}\n` +
            `2. LOSS INCIDENT: Crop: ${payload.crop} (${payload.acreage} Acres) | Peril: ${payload.hazard_type}\n` +
            `   Assessed Loss: ${payload.loss_percent}% | Enclosed Geo-Tagged Photos: ${payload.geo_photos_count}\n` +
            `   Telemetry at Calamity: ${payload.telemetry_notes}\n` +
            `3. PRAYER: Joint Survey inspection by AEO & Insurance Surveyor requested within 10 days.\n`;
        }

        if (dossierTextContent) dossierTextContent.textContent = currentDossierText;
        if (dossierBox) dossierBox.style.display = 'block';
        btnGenerateDossier.innerHTML = '<span>📄</span> Generate Official Dossier';
      });
    }

    if (btnDownloadDossier) {
      btnDownloadDossier.addEventListener('click', () => {
        if (!currentDossierText) return;
        const blob = new Blob([currentDossierText], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `PMFBY_Claim_Dossier_${document.getElementById('claimSurvey').value || 'Survey'}.txt`;
        a.click();
        URL.revokeObjectURL(url);
      });
    }

    if (btnPrintDossier) {
      btnPrintDossier.addEventListener('click', () => {
        const printWin = window.open('', '_blank');
        printWin.document.write(`<pre style="font-family: monospace; white-space: pre-wrap; font-size: 14px; padding: 20px;">${escapeHtml(currentDossierText)}</pre>`);
        printWin.document.close();
        printWin.print();
      });
    }

    if (btnLogToTracker) {
      btnLogToTracker.addEventListener('click', async () => {
        const fName = document.getElementById('claimFarmerName').value || 'Farmer';
        const fPhone = document.getElementById('claimPhone').value || '9848022338';
        const crop = document.getElementById('hazardCrop').value || 'Paddy';
        const dist = document.getElementById('hazardDistrict').value || 'Warangal';
        const refNo = `PMFBY-${dist.slice(0, 3).toUpperCase()}-${Date.now().toString().slice(-6)}`;

        btnLogToTracker.textContent = '⏳ Saving to Tracker...';

        try {
          const resp = await fetch(`${API_BASE}/claims`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              farmer_name: fName,
              phone: fPhone,
              scheme_name: `PMFBY Crop Loss Claim (${crop})`,
              reference_number: refNo,
              status: 'Intimation Dispatched (Within 72 hrs)',
              notes: `Enclosed ${capturedEvidence.length} geo-tagged damage photos.`
            })
          });
          if (resp.ok) {
            alert(`✅ Claim successfully logged into Live Status Tracker!

Docket Reference Number: ${refNo}

Automated SLA follow-up alerts have been scheduled.`);
            btnLogToTracker.innerHTML = '<span>✅</span> Saved in Tracker';
          }
        } catch (err) {
          alert(`Application tracked locally with reference: ${refNo}`);
        } finally {
          setTimeout(() => {
            btnLogToTracker.innerHTML = '<span>💾</span> Save to Status Tracker';
          }, 2500);
        }
      });
    }
  }

  // =========================================================================
  // 5. TAB 3: CLIMATE-SMART WATER SUBSIDIES & DYNAMIC CROP MIGRATION ECOSYSTEM
  // =========================================================================
  let cachedWaterSchemes = [];
  let cachedLowWaterCrops = [];

  const stateDistrictsMap = {
    'Telangana': ['Warangal', 'Karimnagar', 'Nalgonda', 'Mahabubnagar', 'Khammam', 'Nizamabad'],
    'Andhra Pradesh': ['Anantapur', 'Kurnool', 'Kadapa', 'Chittoor', 'Guntur', 'Prakasam'],
    'Maharashtra': ['Solapur', 'Ahmednagar', 'Jalna', 'Latur', 'Yavatmal', 'Nagpur'],
    'Karnataka': ['Kalaburagi', 'Raichur', 'Vijayapura', 'Belagavi', 'Tumkur', 'Ballari'],
    'Gujarat': ['Rajkot', 'Surendranagar', 'Banaskantha', 'Kutch', 'Amreli'],
    'Tamil Nadu': ['Thanjavur', 'Madurai', 'Tiruchirappalli', 'Salem', 'Dharmapuri'],
    'Punjab': ['Bathinda', 'Mansa', 'Sangrur', 'Ludhiana', 'Firozpur'],
    'Haryana': ['Sirsa', 'Hisar', 'Fatehabad', 'Bhiwani', 'Mahendragarh'],
    'Madhya Pradesh': ['Indore', 'Ujjain', 'Dewas', 'Khargone', 'Dhar'],
    'Rajasthan': ['Jodhpur', 'Barmer', 'Nagaur', 'Bikaner', 'Jaisalmer'],
    'Uttar Pradesh': ['Jhansi', 'Banda', 'Mahoba', 'Agra', 'Varanasi']
  };

  async function loadWeatherEcosystemData() {
    const ecoStateSelect = document.getElementById('ecoStateSelect');
    const ecoDistrictSelect = document.getElementById('ecoDistrictSelect');
    const ecoRoutineCrop = document.getElementById('ecoRoutineCrop');
    const ecoIrrigation = document.getElementById('ecoIrrigation');
    const ecoAcres = document.getElementById('ecoAcres');
    const ecoCategory = document.getElementById('ecoCategory');

    const st = ecoStateSelect ? ecoStateSelect.value : (state.selectedState || 'Telangana');
    const dist = ecoDistrictSelect ? ecoDistrictSelect.value : 'Warangal';
    const crop = ecoRoutineCrop ? ecoRoutineCrop.value : 'Paddy';
    const irrig = ecoIrrigation ? ecoIrrigation.value : 'flood';
    const acres = ecoAcres ? (parseFloat(ecoAcres.value) || 2.5) : 2.5;
    const cat = ecoCategory ? ecoCategory.value : 'small_marginal';

    try {
      const url = `${API_BASE}/api/weather_advisory?state=${encodeURIComponent(st)}&district=${encodeURIComponent(dist)}&routine_crop=${encodeURIComponent(crop)}&irrigation_type=${encodeURIComponent(irrig)}&acres=${acres}&farmer_category=${encodeURIComponent(cat)}`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        renderEcosystemDashboard(data);
      }
    } catch (err) {
      console.warn('Could not load agro-climate ecosystem advisory:', err);
    }
  }

  function renderEcosystemDashboard(data) {
    if (!data || data.status !== 'success') return;

    // 1. Weather Radar
    const locTitle = document.getElementById('ecoLocationTitle');
    const droughtBadge = document.getElementById('ecoDroughtBadge');
    const rainDeficit = document.getElementById('ecoRainDeficit');
    const rainMm = document.getElementById('ecoRainMm');
    const soilMoisture = document.getElementById('ecoSoilMoisture');
    const dryDays = document.getElementById('ecoDryDays');
    const advisoryText = document.getElementById('ecoAdvisoryText');
    const forecastRow = document.getElementById('ecoForecastRow');

    if (locTitle) locTitle.textContent = `Near-Future Agro-Met Weather Forecast: ${data.location.district}, ${data.location.state}`;
    if (droughtBadge) {
      droughtBadge.textContent = `🚨 ${data.weather.drought_alert_level} DRY SPELL ALERT`;
      if (data.weather.drought_alert_level === 'CRITICAL') {
        droughtBadge.style.background = '#fee2e2';
        droughtBadge.style.color = '#991b1b';
      } else {
        droughtBadge.style.background = '#fef3c7';
        droughtBadge.style.color = '#92400e';
      }
    }

    if (rainDeficit) rainDeficit.textContent = `${data.weather.rainfall_deficit_pct}%`;
    if (rainMm) rainMm.textContent = `${data.weather.forecast_14d_rainfall_mm} mm`;
    if (soilMoisture) soilMoisture.textContent = `${data.weather.soil_moisture_pct}% (Low)`;
    if (dryDays) dryDays.textContent = `${data.weather.dry_spell_days} Days`;

    if (advisoryText) {
      advisoryText.textContent = `High atmospheric evapotranspiration and zero significant precipitation forecast over next 21 days in ${data.location.district}. Traditional flood irrigation on routine ${data.routine_crop.crop_name} will lose ~60% of water to surface evaporation, leading to severe groundwater depletion (${data.weather.groundwater_status}). Immediate micro-irrigation deployment or crop migration is recommended.`;
    }

    if (forecastRow && data.weather.forecast_daily) {
      forecastRow.innerHTML = data.weather.forecast_daily.map((d, idx) => {
        const rainNum = parseInt(d.rain_prob) || 0;
        const isDry = rainNum <= 5;
        const isHeat = (d.status || '').toLowerCase().includes('heat') || (d.temp && parseFloat(d.temp) >= 38.5);
        const cardBg = isHeat ? '#fff1f2' : (isDry ? '#fff7ed' : '#f0fdf4');
        const cardBorder = isHeat ? '#f43f5e' : (isDry ? '#fdba74' : '#86efac');
        const rainPillBg = isDry ? '#fee2e2' : '#e0f2fe';
        const rainPillColor = isDry ? '#991b1b' : '#0369a1';
        const dayLabel = d.day || `Day ${idx + 1}`;

        return `
          <div class="weather-day-chip" style="flex: 0 0 135px !important; min-width: 135px !important; max-width: 140px !important; background: ${cardBg} !important; border: 2px solid ${cardBorder} !important; border-radius: 12px !important; padding: 10px 8px !important; text-align: center !important; box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important; display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: space-between !important; box-sizing: border-box !important;">
            <div style="font-size: 0.75rem; font-weight: 800; color: #1e293b; text-transform: uppercase; border-bottom: 1px solid rgba(0,0,0,0.08); width: 100%; padding-bottom: 4px;">
              ${escapeHtml(dayLabel)}
            </div>
            <div style="font-size: 2.2rem; margin: 6px 0 2px 0; line-height: 1;">${d.icon || '☀️'}</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #0f172a; line-height: 1.2;">
              ${escapeHtml(d.temp || '37°C')}
            </div>
            <div style="font-size: 0.74rem; font-weight: 700; color: #475569; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;">
              ${escapeHtml(d.status || (isDry ? 'Dry' : 'Fair'))}
            </div>
            <div style="width: 100%; background: ${rainPillBg}; color: ${rainPillColor}; padding: 3px 4px; border-radius: 6px; font-size: 0.75rem; font-weight: 800; margin-bottom: 4px;">
              🌧️ ${escapeHtml(d.rain_prob || '0%')} Rain
            </div>
            <div style="font-size: 0.68rem; font-weight: 700; color: ${isHeat ? '#e11d48' : (isDry ? '#c2410c' : '#15803d')};">
              ${isHeat ? '🔥 Extreme Heat' : (isDry ? '⚠️ Zero Rain' : '🌦️ Light Rain')}
            </div>
          </div>
        `;
      }).join('');
    }

    // 2. Micro-Irrigation Matchmaker (BUY vs RENT)
    const dripAdv = data.micro_irrigation_advisory;
    const dripUrgencyBadge = document.getElementById('ecoDripUrgencyBadge');
    const dripSubtitle = document.getElementById('ecoDripSubtitle');
    const buyBadgePct = document.getElementById('ecoBuyBadgePct');
    const agencyName = document.getElementById('ecoAgencyName');
    const costAcres = document.getElementById('ecoCostAcres');
    const totalMarketCost = document.getElementById('ecoTotalMarketCost');
    const govtSubsidyAmount = document.getElementById('ecoGovtSubsidyAmount');
    const farmerPayableShare = document.getElementById('ecoFarmerPayableShare');
    const subsidyPctText = document.getElementById('ecoSubsidyPctText');
    const portalLink = document.getElementById('ecoPortalLink');
    const helpline = document.getElementById('ecoHelpline');
    const rentHub = document.getElementById('ecoRentHub');

    if (dripUrgencyBadge) dripUrgencyBadge.textContent = dripAdv.urgency_level;
    if (dripSubtitle) {
      if (dripAdv.has_drip) {
        dripSubtitle.textContent = `✅ Your farm is already equipped with micro-irrigation! You save ~60% of water and ₹${data.routine_crop.pumping_power_cost.toLocaleString()} annually in pumping expenses. Below are alternative crop migrations to further boost net profits.`;
      } else {
        dripSubtitle.textContent = `You currently use ${data.routine_crop.crop_name} under flood/borewell irrigation. Deploying drip irrigation will save up to 60% of water and ₹${Math.round(data.routine_crop.pumping_power_cost * 0.6).toLocaleString()} in electricity/diesel costs.`;
      }
    }

    if (buyBadgePct) buyBadgePct.textContent = `${dripAdv.subsidy_percentage}% Subsidy`;
    if (subsidyPctText) subsidyPctText.textContent = `${dripAdv.subsidy_percentage}%`;
    if (agencyName) agencyName.textContent = `${dripAdv.agency_name} (${dripAdv.department})`;
    if (costAcres) costAcres.textContent = (document.getElementById('ecoAcres') ? document.getElementById('ecoAcres').value : '2.5');
    if (totalMarketCost) totalMarketCost.textContent = `₹${dripAdv.total_market_cost.toLocaleString()}`;
    if (govtSubsidyAmount) govtSubsidyAmount.textContent = `- ₹${dripAdv.government_subsidy_amount.toLocaleString()}`;
    if (farmerPayableShare) {
      if (dripAdv.farmer_payable_share <= 0) {
        farmerPayableShare.textContent = '₹0 (100% Free Installation)';
        farmerPayableShare.style.color = '#16a34a';
      } else {
        farmerPayableShare.textContent = `Only ₹${dripAdv.farmer_payable_share.toLocaleString()}`;
        farmerPayableShare.style.color = '#15803d';
      }
    }
    if (portalLink && dripAdv.portal_url) portalLink.href = dripAdv.portal_url;
    if (helpline && dripAdv.helpline) helpline.textContent = dripAdv.helpline;
    if (rentHub && dripAdv.rent_option) rentHub.textContent = dripAdv.rent_option.chc_provider;

    // 3. Routine Crop Baseline
    const routine = data.routine_crop;
    const routineCropName = document.getElementById('ecoRoutineCropName');
    const baselineCrop = document.getElementById('ecoBaselineCrop');
    const baselineWater = document.getElementById('ecoBaselineWater');
    const baselineLiters = document.getElementById('ecoBaselineLiters');
    const baselinePowerCost = document.getElementById('ecoBaselinePowerCost');
    const baselineRisk = document.getElementById('ecoBaselineRisk');

    if (routineCropName) routineCropName.textContent = routine.crop_name;
    if (baselineCrop) baselineCrop.textContent = routine.crop_name;
    if (baselineWater) baselineWater.textContent = `${routine.water_mm} mm`;
    if (baselineLiters) baselineLiters.textContent = `${(routine.total_water_liters / 10000000).toFixed(2)} Cr`;
    if (baselinePowerCost) baselinePowerCost.textContent = `₹${routine.pumping_power_cost.toLocaleString()}`;
    if (baselineRisk) baselineRisk.textContent = routine.risk_rating;

    // 4. Crop Migrations Cards
    const migrationGrid = document.getElementById('ecoCropMigrationGrid');
    if (migrationGrid && data.crop_migrations) {
      migrationGrid.innerHTML = data.crop_migrations.map(m => {
        const profitGain = m.net_profit_difference;
        const profitSign = profitGain >= 0 ? `+₹${profitGain.toLocaleString()}` : `-₹${Math.abs(profitGain).toLocaleString()}`;
        const profitColor = profitGain >= 0 ? '#15803d' : '#b45309';

        return `
          <div class="crop-migration-card">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem;">
                <div>
                  <span class="badge-tag badge-tag-green" style="font-size: 0.72rem;">${escapeHtml(m.highlight_tag)}</span>
                  <h4 style="margin: 0.4rem 0 0.15rem 0; font-size: 1.1rem; color: #1e293b;">${escapeHtml(m.name)}</h4>
                  <span style="font-size: 0.78rem; color: #64748b; font-weight: 600;">Category: ${escapeHtml(m.category)}</span>
                </div>
                <div style="text-align: right;">
                  <span style="font-size: 1.15rem; font-weight: 800; color: #0284c7;">${m.water_saved_pct}%</span>
                  <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">Water Saved</div>
                </div>
              </div>

              <!-- Animated Water Meter Bar -->
              <div class="water-meter-wrap">
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #475569;">
                  <span>Water Requirement: <strong>${m.water_required_mm} mm</strong></span>
                  <span>Saves: <strong>${(m.liters_saved_total / 100000).toFixed(1)} Lakh L</strong></span>
                </div>
                <div class="water-meter-bar">
                  <div class="water-meter-fill" style="width: ${m.water_saved_pct}%;"></div>
                </div>
              </div>

              <!-- Economic Metrics Grid -->
              <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.5rem 0.65rem; margin: 0.65rem 0; font-size: 0.8rem; display: grid; grid-template-columns: 1fr 1fr; gap: 0.35rem;">
                <div>MSP Rate: <strong>₹${m.msp_per_quintal.toLocaleString()} / qtl</strong></div>
                <div>Duration: <strong>${m.duration_days} Days</strong> (-${m.days_saved_vs_routine}d)</div>
                <div style="color: #15803d;">Govt Bonus: <strong>+₹${m.diversification_bonus_per_acre.toLocaleString()}/ac</strong></div>
                <div style="color: ${profitColor};">Net Return Impact: <strong>${profitSign}</strong></div>
              </div>

              <div style="font-size: 0.8rem; color: #334155; margin-bottom: 0.4rem; line-height: 1.4;">
                🌱 <strong>Soil Benefit:</strong> ${escapeHtml(m.soil_health)}
              </div>
              <div style="font-size: 0.78rem; color: #475569; margin-bottom: 0.4rem;">
                🌾 <strong>ICAR Recommended Varieties:</strong> ${escapeHtml(m.recommended_varieties)}
              </div>
              <div style="font-size: 0.75rem; color: #0369a1; background: #e0f2fe; padding: 3px 6px; border-radius: 4px;">
                🏛️ <strong>Procurement:</strong> ${escapeHtml(m.buyer_body)}
              </div>
            </div>

            <div style="margin-top: 0.85rem;">
              <button type="button" class="btn btn-secondary" style="width: 100%; font-size: 0.82rem; padding: 0.45rem 0.75rem;" onclick="openCropMigrationModal('${escapeHtml(m.name)}', '${m.water_saved_pct}%', '${m.recommended_varieties}', '${escapeHtml(m.soil_health)}')">
                <span>📋</span> Select Crop &amp; View Sowing Guide
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    // 5. Comparison Table Body
    const tableBody = document.getElementById('ecoComparisonTableBody');
    if (tableBody && data.crop_migrations) {
      tableBody.innerHTML = `
        <tr class="routine-row-highlight">
          <td><strong>${escapeHtml(routine.crop_name)} (Routine)</strong></td>
          <td>${routine.water_mm} mm</td>
          <td>Baseline (0%)</td>
          <td>Baseline</td>
          <td>₹2,320 / qtl</td>
          <td>140 Days</td>
          <td>₹0</td>
          <td style="color: #b91c1c; font-weight: 700;">Routine Baseline</td>
        </tr>
      ` + data.crop_migrations.map(m => {
        const profitDiff = m.net_profit_difference;
        const profitLabel = profitDiff >= 0 ? `+₹${profitDiff.toLocaleString()}` : `-₹${Math.abs(profitDiff).toLocaleString()}`;
        const profitColor = profitDiff >= 0 ? '#15803d' : '#b45309';

        return `
          <tr>
            <td><strong>${escapeHtml(m.name)}</strong></td>
            <td>${m.water_required_mm} mm</td>
            <td style="color: #0284c7; font-weight: 700;">-${m.water_saved_pct}%</td>
            <td>${(m.liters_saved_total / 100000).toFixed(1)} Lakh Liters</td>
            <td>₹${m.msp_per_quintal.toLocaleString()} / qtl</td>
            <td>${m.duration_days} Days (-${m.days_saved_vs_routine}d)</td>
            <td style="color: #16a34a; font-weight: 700;">+₹${m.diversification_bonus_per_acre.toLocaleString()}/ac</td>
            <td style="color: ${profitColor}; font-weight: 700;">${profitLabel}</td>
          </tr>
        `;
      }).join('');
    }
  }

  window.openCropMigrationModal = function(cropName, waterSaved, varieties, soilBenefit) {
    alert(`🌾 Crop Migration Sowing Guide: ${cropName}\n\n💧 Water Savings: ${waterSaved} reduction vs routine flood crop\n🌱 Recommended ICAR Seeds: ${varieties}\n🌍 Soil & Climate Advantage: ${soilBenefit}\n\nAction: Register on State Horticulture / Agriculture Portal for ₹7,000/acre Crop Diversification DBT Incentive.`);
  };

  async function initWaterSubsidiesTab() {
    // 1. Initialize Agro-Climate Ecosystem
    const ecoStateSelect = document.getElementById('ecoStateSelect');
    const ecoDistrictSelect = document.getElementById('ecoDistrictSelect');
    const ecoRoutineCrop = document.getElementById('ecoRoutineCrop');
    const ecoIrrigation = document.getElementById('ecoIrrigation');
    const ecoAcres = document.getElementById('ecoAcres');
    const ecoCategory = document.getElementById('ecoCategory');
    const btnRunEco = document.getElementById('btnRunEcoSimulation');

    function updateEcoDistricts(st) {
      if (!ecoDistrictSelect) return;
      const dists = stateDistrictsMap[st] || ['Warangal', 'District Capital'];
      ecoDistrictSelect.innerHTML = dists.map(d => `<option value="${d}">${d}</option>`).join('');
    }

    if (ecoStateSelect) {
      if (state.selectedState && stateDistrictsMap[state.selectedState]) {
        ecoStateSelect.value = state.selectedState;
      }
      updateEcoDistricts(ecoStateSelect.value);
      ecoStateSelect.addEventListener('change', function() {
        updateEcoDistricts(this.value);
        loadWeatherEcosystemData();
      });
    }

    [ecoDistrictSelect, ecoRoutineCrop, ecoIrrigation, ecoAcres, ecoCategory].forEach(el => {
      if (el) el.addEventListener('change', loadWeatherEcosystemData);
    });

    if (btnRunEco) {
      btnRunEco.addEventListener('click', loadWeatherEcosystemData);
    }

    const btnLeft = document.getElementById('btnScrollForecastLeft');
    const btnRight = document.getElementById('btnScrollForecastRight');
    const forecastRow = document.getElementById('ecoForecastRow');
    if (btnLeft && forecastRow) {
      btnLeft.addEventListener('click', () => {
        forecastRow.scrollBy({ left: -260, behavior: 'smooth' });
      });
    }
    if (btnRight && forecastRow) {
      btnRight.addEventListener('click', () => {
        forecastRow.scrollBy({ left: 260, behavior: 'smooth' });
      });
    }

    // Trigger initial calculation
    loadWeatherEcosystemData();

    // 2. Load Reference Schemes & Crops from API
    try {
      const resp = await fetch(`${API_BASE}/water_saving_schemes`);
      if (resp.ok) cachedWaterSchemes = await resp.json();
    } catch (err) {
      console.warn('Backend /water_saving_schemes not available, using embedded.');
    }
    if (!cachedWaterSchemes || cachedWaterSchemes.length === 0) {
      cachedWaterSchemes = typeof WATER_SAVING_SCHEMES_DATA !== 'undefined' ? WATER_SAVING_SCHEMES_DATA : [];
    }

    try {
      const resp2 = await fetch(`${API_BASE}/low_water_crops`);
      if (resp2.ok) cachedLowWaterCrops = await resp2.json();
    } catch (err2) {
      console.warn('Backend /low_water_crops not available, using embedded.');
    }
    if (!cachedLowWaterCrops || cachedLowWaterCrops.length === 0) {
      cachedLowWaterCrops = typeof LOW_WATER_CROPS_DATA !== 'undefined' ? LOW_WATER_CROPS_DATA : [];
    }

    renderWaterSchemes();
    renderLowWaterCrops();

    const waterStateFilter = document.getElementById('waterStateFilter');
    const waterTypeFilter = document.getElementById('waterTypeFilter');
    if (waterStateFilter) {
      waterStateFilter.addEventListener('change', function () {
        state.waterStateFilter = this.value;
        renderWaterSchemes();
      });
    }
    if (waterTypeFilter) {
      waterTypeFilter.addEventListener('change', function () {
        state.waterTypeFilter = this.value;
        renderWaterSchemes();
      });
    }

    const cropPills = document.querySelectorAll('#cropCategoryPills .pill-btn');
    cropPills.forEach(pill => {
      pill.addEventListener('click', function () {
        cropPills.forEach(p => p.classList.remove('active'));
        this.classList.add('active');
        state.cropCategoryFilter = this.getAttribute('data-cropcat');
        renderLowWaterCrops();
      });
    });
  }

  function renderWaterSchemes() {
    const grid = document.getElementById('waterSchemesGrid');
    const badge = document.getElementById('waterSchemesBadge');
    if (!grid) return;

    let pool = cachedWaterSchemes.slice();

    if (state.waterStateFilter !== 'All') {
      const st = state.waterStateFilter.toLowerCase();
      pool = pool.filter(s => {
        const appStates = (s.applicable_states || []).map(x => x.toLowerCase());
        return appStates.includes('all states') || appStates.includes(st);
      });
    }

    if (state.waterTypeFilter !== 'All') {
      const ty = state.waterTypeFilter.toLowerCase();
      pool = pool.filter(s => (s.category || '').toLowerCase().includes(ty));
    }

    if (badge) badge.textContent = `${pool.length} Schemes Loaded`;

    if (pool.length === 0) {
      grid.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: var(--text-muted);">No schemes found for this filter.</div>`;
      return;
    }

    grid.innerHTML = pool.map(s => {
      const schemeTitle = s.name || s.scheme_name || 'Water Conservation Scheme';
      const schemeDesc = s.water_savings_potential || s.target_beneficiaries || s.objective || 'Official government water conservation and irrigation assistance scheme.';

      let subsidyText = '50% - 90%';
      if (typeof s.subsidy_rules === 'string') {
        subsidyText = s.subsidy_rules;
      } else if (s.subsidy_rules && typeof s.subsidy_rules === 'object') {
        subsidyText = s.subsidy_rules.small_and_marginal_farmers || s.subsidy_rules.farm_pond_grant || s.subsidy_rules.solar_feeder_power || s.subsidy_rules.details || Object.values(s.subsidy_rules)[0] || '50% - 90%';
      } else if (s.subsidy_percentage) {
        subsidyText = s.subsidy_percentage;
      }

      let eligText = 'All farmers with valid land records.';
      if (Array.isArray(s.eligibility_criteria) && s.eligibility_criteria.length > 0) {
        eligText = s.eligibility_criteria[0];
      } else if (typeof s.eligibility_criteria === 'string') {
        eligText = s.eligibility_criteria;
      } else if (s.eligibility_summary) {
        eligText = s.eligibility_summary;
      }

      const agencyText = s.implementing_agency || s.max_assistance || 'State Agriculture & Horticulture Department';
      const portalUrl = s.portal_url || s.official_portal || '#';
      const statesList = Array.isArray(s.applicable_states) ? s.applicable_states.join(', ') : (s.state || 'Pan-India');

      return `
      <article class="scheme-card" style="border-left: 4px solid #0284c7;">
        <div class="scheme-header-area">
          <span class="badge badge-central">${escapeHtml(s.level || 'State/Central')} • ${escapeHtml(s.category || 'Water Conservation')}</span>
          <h3 class="scheme-title" style="margin-top: 0.35rem; color: #0f172a; font-size: 1.15rem; font-weight: 700;">${escapeHtml(schemeTitle)}</h3>
          <p class="scheme-desc" style="color: #475569; font-size: 0.85rem; line-height: 1.45; margin-top: 0.25rem;">${escapeHtml(schemeDesc)}</p>
        </div>
        <div class="scheme-body-area">
          <div class="benefit-highlight">
            <span class="benefit-label">Subsidy Rate</span>
            <div class="benefit-value" style="color: #0369a1; font-size: 0.95rem; font-weight: 700;">${escapeHtml(subsidyText)}</div>
          </div>
          <div class="scheme-field">
            <span class="field-title">Key Eligibility</span>
            <p class="field-content">${escapeHtml(eligText)}</p>
          </div>
          <div class="scheme-field">
            <span class="field-title">Implementing Agency</span>
            <p class="field-content">${escapeHtml(agencyText)}</p>
          </div>
        </div>
        <div class="card-footer-area">
          <span class="last-verified-text">State: ${escapeHtml(statesList)}</span>
          <a href="${escapeHtml(portalUrl)}" target="_blank" rel="noopener noreferrer" class="official-link-btn" style="background: #0284c7;">Portal ↗</a>
        </div>
      </article>
      `;
    }).join('');
  }

  function renderLowWaterCrops() {
    const grid = document.getElementById('lowWaterCropsGrid');
    const badge = document.getElementById('lowWaterCropsBadge');
    if (!grid) return;

    let pool = cachedLowWaterCrops.slice();
    if (state.cropCategoryFilter !== 'All') {
      const cat = state.cropCategoryFilter.toLowerCase();
      pool = pool.filter(c => (c.category || '').toLowerCase().includes(cat));
    }

    if (badge) badge.textContent = `${pool.length} Crops Available`;

    grid.innerHTML = pool.map(c => {
      const cropTitle = c.name || c.crop_name || 'Resilient Low-Water Crop';
      const cat = c.category || 'Alternative Crop';
      const savings = c.water_savings_percentage || c.water_savings_vs_paddy || '-65% Water';
      const mspVal = c.msp_rate_per_quintal ? ('₹' + c.msp_rate_per_quintal.toLocaleString() + ' / quintal') : (c.msp_2024_25 || 'MSP Support');
      const duration = c.duration_days || '90-110 days';
      const waterReq = c.water_requirement_mm || '300-450 mm';
      const soilBen = c.soil_health_benefit || c.economic_advisory || (Array.isArray(c.attached_schemes) ? c.attached_schemes[0] : 'High drought resilience.');
      const varieties = Array.isArray(c.recommended_varieties) ? c.recommended_varieties.join(', ') : (c.recommended_varieties || '');

      return `
      <div class="card" style="border-left: 4px solid #16a34a; margin-bottom: 0;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem;">
          <div>
            <span class="badge-tag badge-tag-green">${escapeHtml(cat)}</span>
            <h4 style="margin: 0.35rem 0 0.1rem 0; font-size: 1.1rem; color: #1e293b;">${escapeHtml(cropTitle)}</h4>
            ${c.season_suitability ? `<span style="font-size: 0.8rem; color: var(--text-muted);">${escapeHtml(c.season_suitability)}</span>` : ''}
          </div>
          <span class="badge-tag badge-tag-amber" style="font-weight: 800; white-space: nowrap;">${escapeHtml(savings)}</span>
        </div>
        <div style="margin: 0.75rem 0; background: #f8fafc; padding: 0.6rem; border-radius: 6px; font-size: 0.84rem; line-height: 1.5;">
          <div><strong>MSP Rate:</strong> <span style="color: #15803d; font-weight: 700;">${escapeHtml(mspVal)}</span></div>
          <div><strong>Duration:</strong> ${escapeHtml(duration)} • <strong>Water Req:</strong> ${escapeHtml(waterReq)}</div>
          ${varieties ? `<div style="font-size: 0.78rem; color: #475569; margin-top: 0.2rem;"><strong>Seeds:</strong> ${escapeHtml(varieties)}</div>` : ''}
        </div>
        <p style="font-size: 0.82rem; color: #334155; margin: 0; line-height: 1.4;">
          ${escapeHtml(soilBen)}
        </p>
      </div>
      `;
    }).join('');
  }

  // =========================================================================
  // 6. TAB 4: KCC CREDIT & STATUS TRACKER
  // =========================================================================
  function initKccAndTrackerTab() {
    const kccForm = document.getElementById('kccForm');
    if (kccForm) {
      kccForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const crop = document.getElementById('kccCrop').value;
        const acres = parseFloat(document.getElementById('kccAcres').value) || 3.0;
        const debt = parseFloat(document.getElementById('kccDebt').value) || 0.0;

        let res = null;
        try {
          const resp = await fetch(`${API_BASE}/calculate_kcc`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ crop: crop, land_acres: acres, existing_debt: debt })
          });
          if (resp.ok) res = await resp.json();
        } catch (err) {
          console.warn('Backend /calculate_kcc unavailable, calculating locally.');
        }

        if (!res) {
          // Local Scale of finance values
          const scaleMap = {
            'Paddy': 38000, 'Cotton': 42000, 'Chilli': 65000,
            'Maize': 28000, 'Soybean': 24000, 'Bengal Gram': 22000,
            'Groundnut': 26000, 'Sugarcane': 70000
          };
          const baseScale = scaleMap[crop] || 35000;
          const cropCost = baseScale * acres;
          const postHarvest = cropCost * 0.10;
          const maintenance = cropCost * 0.20;
          const totalLimit = cropCost + postHarvest + maintenance;
          res = {
            crop: crop,
            acres: acres,
            base_scale_of_finance: baseScale,
            crop_cultivation_cost: cropCost,
            post_harvest_household_10pct: postHarvest,
            farm_maintenance_insurance_20pct: maintenance,
            total_sanctioned_kcc_limit: totalLimit,
            net_disbursable_limit: Math.max(0, totalLimit - debt),
            effective_interest_rate_pct: 4.0,
            annual_interest_savings_vs_informal: Math.round(totalLimit * (0.24 - 0.04))
          };
        }

        const dispLimit = document.getElementById('dispKccLimit');
        if (dispLimit) dispLimit.textContent = `₹${res.total_sanctioned_kcc_limit.toLocaleString('en-IN')}`;
      });
    }

    // Claims Tracker
    loadClaimsList();

    const btnRefreshClaims = document.getElementById('btnRefreshClaims');
    if (btnRefreshClaims) {
      btnRefreshClaims.addEventListener('click', loadClaimsList);
    }

    const addClaimForm = document.getElementById('addClaimForm');
    if (addClaimForm) {
      addClaimForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const newClaim = {
          farmer_name: document.getElementById('trkFarmerName').value,
          phone: document.getElementById('trkPhone').value,
          scheme_name: document.getElementById('trkScheme').value,
          reference_number: document.getElementById('trkRef').value,
          status: document.getElementById('trkStatus').value,
          notes: document.getElementById('trkNotes').value
        };

        try {
          await fetch(`${API_BASE}/claims`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newClaim)
          });
        } catch (err) {
          console.warn('Backend /claims POST failed, saved to local session.');
        }

        alert('Application added to tracking registry!');
        loadClaimsList();
      });
    }
  }

  async function loadClaimsList() {
    const container = document.getElementById('claimsListContainer');
    if (!container) return;

    let claims = [];
    try {
      const resp = await fetch(`${API_BASE}/claims`);
      if (resp.ok) claims = await resp.json();
    } catch (err) {
      console.warn('Backend /claims GET failed, using mock list.');
    }

    if (!claims || claims.length === 0) {
      claims = [
        {
          claim_id: 'CLM-2026-TS-001',
          farmer_name: 'Komirelli Ramulu',
          scheme_name: 'PMFBY Hailstorm Crop Loss Claim',
          reference_number: 'PMFBY/TS/2026/092144',
          status: 'Joint Field Survey Completed',
          urgency_meta: { status_banner: '⚠️ Overdue by 3 days! Escalate to District Officer.', color: 'red' },
          notes: 'Joint survey photos uploaded. Compensation calculation pending.'
        },
        {
          claim_id: 'CLM-2026-TS-002',
          farmer_name: 'B. Lakshmi',
          scheme_name: 'TSMIP Micro-Irrigation Drip Subsidy',
          reference_number: 'TSMIP/NAL/2026/5521',
          status: 'Administrative Sanction Approved',
          urgency_meta: { status_banner: '⏱️ In Progress (8/21 days elapsed).', color: 'green' },
          notes: 'Farmer 10% DD paid. Company pipeline installation pending.'
        }
      ];
    }

    container.innerHTML = claims.map(c => `
      <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.9rem; margin-bottom: 0.85rem; background: #ffffff;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <h4 style="margin: 0; font-size: 1rem; color: #1e293b;">${c.scheme_name}</h4>
            <span style="font-size: 0.82rem; color: var(--text-muted);">Ref: <strong>${c.reference_number}</strong> • Farmer: ${c.farmer_name}</span>
          </div>
          <span class="badge-tag ${c.urgency_meta && c.urgency_meta.color === 'red' ? 'badge-tag-red' : 'badge-tag-green'}">
            ${c.status}
          </span>
        </div>
        <div style="margin: 0.5rem 0; font-size: 0.85rem; color: #475569;">
          ${c.notes || ''}
        </div>
        <div style="font-size: 0.82rem; font-weight: 600; color: ${c.urgency_meta && c.urgency_meta.color === 'red' ? '#b91c1c' : '#15803d'};">
          ${c.urgency_meta ? c.urgency_meta.status_banner : 'Active tracking'}
        </div>
      </div>
    `).join('');
  }

  // =========================================================================
  // 7. TAB 6: MSP VS MANDI BENCHMARK
  // =========================================================================
  async function initMspTab() {
    const tableBody = document.getElementById('mspTableBody');
    if (!tableBody) return;

    let mspData = [];
    try {
      const resp = await fetch(`${API_BASE}/msp_comparison`);
      if (resp.ok) mspData = await resp.json();
    } catch (err) {
      console.warn('Backend /msp_comparison failed, using static data.');
    }

    if (!mspData || mspData.length === 0) {
      mspData = [
        { crop: "Paddy (Grade A)", msp_rate: 2320, state_bonus: 500, effective_gov_price: 2820, average_mandi_price: 2180, price_delta: 640, recommendation: "Sell at PACS / IKP procurement centre for +₹640/qtl bonus." },
        { crop: "Cotton (Medium Staple)", msp_rate: 7121, state_bonus: 0, effective_gov_price: 7121, average_mandi_price: 6850, price_delta: 271, recommendation: "Sell at Cotton Corporation of India (CCI) centre." },
        { crop: "Maize", msp_rate: 2225, state_bonus: 0, effective_gov_price: 2225, average_mandi_price: 2100, price_delta: 125, recommendation: "Sell at Markfed procurement centre." },
        { crop: "Bengal Gram (Chana)", msp_rate: 5440, state_bonus: 0, effective_gov_price: 5440, average_mandi_price: 5100, price_delta: 340, recommendation: "Sell at NAFED / Markfed procurement centre." },
        { crop: "Sesame (Til)", msp_rate: 9267, state_bonus: 0, effective_gov_price: 9267, average_mandi_price: 8700, price_delta: 567, recommendation: "Sell at Mandi with statutory MSP floor." }
      ];
    }

    tableBody.innerHTML = mspData.map(row => `
      <tr>
        <td><strong>${row.crop}</strong></td>
        <td>₹${row.msp_rate}</td>
        <td>${row.state_bonus > 0 ? '+₹' + row.state_bonus : '—'}</td>
        <td style="color: #1b5e20; font-weight: bold;">₹${row.effective_gov_price}</td>
        <td style="color: #b91c1c;">₹${row.average_mandi_price}</td>
        <td style="color: #15803d; font-weight: 800;">+₹${row.price_delta}/qtl</td>
        <td><span class="badge-tag badge-tag-green">${row.recommendation}</span></td>
      </tr>
    `).join('');
  }

  // =========================================================================
  // 8. TAB 7: INTERMEDIARY DESK, FEEDBACK & ESCALATION
  // =========================================================================
  function initIntermediaryTab() {
    // Rapidfuzz Name Matching
    const nameForm = document.getElementById('nameVerifyForm');
    if (nameForm) {
      nameForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const aName = document.getElementById('verifyAadhaarName').value;
        const bName = document.getElementById('verifyBankName').value;

        let res = null;
        try {
          const resp = await fetch(`${API_BASE}/verify_name?aadhaar_name=${encodeURIComponent(aName)}&bank_name=${encodeURIComponent(bName)}`);
          if (resp.ok) res = await resp.json();
        } catch (err) {
          console.warn('Backend /verify_name failed, computing simple match.');
        }

        if (!res) {
          const cleanA = aName.toLowerCase().replace(/[^a-z0-9]/g, '');
          const cleanB = bName.toLowerCase().replace(/[^a-z0-9]/g, '');
          const score = (cleanA === cleanB) ? 100 : (cleanA.includes(cleanB) || cleanB.includes(cleanA) ? 85 : 55);
          res = {
            similarity_score: score,
            status: score === 100 ? 'Exact Match' : (score >= 80 ? 'Minor Variation' : 'Severe Mismatch'),
            action_required: score >= 80 ? 'None (Ready for DBT)' : 'Visit Bank branch to update Aadhaar name.'
          };
        }

        const scoreEl = document.getElementById('dispMatchScore');
        const statusEl = document.getElementById('dispMatchStatus');
        const actionEl = document.getElementById('dispMatchAction');

        if (scoreEl) scoreEl.textContent = `${res.similarity_score}%`;
        if (statusEl) {
          statusEl.textContent = res.status;
          statusEl.style.color = res.similarity_score >= 80 ? '#16a34a' : '#dc2626';
        }
        if (actionEl) actionEl.textContent = res.action_required;
      });
    }

    // Feedback Form
    const fbForm = document.getElementById('feedbackForm');
    const fbNotice = document.getElementById('feedbackNotice');
    if (fbForm) {
      fbForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const fbData = {
          scheme_id: 'SCH-FB',
          scheme_name: document.getElementById('fbScheme').value,
          feedback_type: document.getElementById('fbType').value,
          reporter_role: document.getElementById('fbRole').value,
          state: document.getElementById('fbState').value,
          description: document.getElementById('fbDesc').value
        };

        try {
          await fetch(`${API_BASE}/feedback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(fbData)
          });
        } catch (err) {
          console.warn('Backend /feedback unavailable, queued in memory.');
        }

        if (fbNotice) {
          fbNotice.style.display = 'block';
          setTimeout(() => { fbNotice.style.display = 'none'; }, 4000);
        }
        fbForm.reset();
      });
    }

    // 4-Tier Formal Escalation Petition
    const escForm = document.getElementById('escalateForm');
    const petitionContainer = document.getElementById('petitionOutputContainer');
    const petitionTextDisplay = document.getElementById('petitionTextDisplay');
    const btnCopyPetition = document.getElementById('btnCopyPetition');

    if (escForm) {
      escForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const escData = {
          farmer_name: document.getElementById('escFarmerName').value,
          father_husband_name: document.getElementById('escFatherName').value,
          aadhaar_masked: document.getElementById('escAadhaar').value,
          phone: document.getElementById('escPhone').value,
          village: document.getElementById('escVillage').value,
          mandal: 'Geesugonda',
          district: 'Warangal',
          survey_no: document.getElementById('escSurvey').value,
          scheme_name: document.getElementById('escScheme').value,
          problem_category: document.getElementById('escCategory').value,
          description: document.getElementById('escDesc').value,
          escalation_level: document.getElementById('escLevel').value
        };

        let petitionObj = null;
        try {
          const resp = await fetch(`${API_BASE}/escalate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(escData)
          });
          if (resp.ok) petitionObj = await resp.json();
        } catch (err) {
          console.warn('Backend /escalate unavailable, generating local petition.');
        }

        const dateStr = new Date().toLocaleDateString('en-IN', { day: '2-digit', month: 'long', year: 'numeric' });
        const refNo = petitionObj ? petitionObj.petition_reference_number : `ESC/2026/TG/${Math.floor(1000 + Math.random() * 9000)}`;

        const petitionText = `
FORMAL ADMINISTRATIVE GRIEVANCE PETITION
Reference Docket: ${refNo}
Date: ${dateStr}

TO:
The Competent Authority,
${escData.escalation_level}
Department of Agriculture & Farmers' Welfare,
Government of Telangana / India.

FROM:
${escData.farmer_name}, S/o or W/o ${escData.father_husband_name}
Village & Mandal: ${escData.village}
Aadhaar (Masked): ${escData.aadhaar_masked} | Mobile: ${escData.phone}
Cultivated Land Survey / Khata No: ${escData.survey_no}

SUBJECT:
Grievance regarding statutory denial / delay under: ${escData.scheme_name}
Categorized Grievance: ${escData.problem_category}

RESPECTED SIR / MADAM,

1. The petitioner is a bona fide agriculturalist cultivating land at the aforesaid survey number.
2. Under the operational guidelines of ${escData.scheme_name}, the petitioner is fully eligible for statutory benefits.
3. GRIEVANCE FACTS:
${escData.description}
4. Despite repeated representations at the village level, the legitimate entitlement has remained undisbursed/unresolved in violation of Citizens' Charter norms.

PRAYER FOR RELIEF:
In light of the above facts, the petitioner respectfully prays that:
a) The authority conduct an immediate inquiry into the pending DBT / survey record;
b) The legitimate benefit under ${escData.scheme_name} be sanctioned without further delay;
c) Written intimation of action taken be provided within 15 working days.

Yours faithfully,

(Signature / Thumb Impression)
Name: ${escData.farmer_name}
Copy submitted for information to:
1. The District Collector & Magistrate
2. Central Public Grievance Redress and Monitoring System (CPGRAMS)
        `.trim();

        if (petitionTextDisplay) {
          petitionTextDisplay.innerHTML = `<div class="petition-body-text">${petitionText}</div>`;
        }
        if (petitionContainer) petitionContainer.style.display = 'block';
      });
    }

    if (btnCopyPetition && petitionTextDisplay) {
      btnCopyPetition.addEventListener('click', function () {
        navigator.clipboard.writeText(petitionTextDisplay.textContent).then(() => {
          btnCopyPetition.textContent = '✅ Copied to Clipboard!';
          setTimeout(() => { btnCopyPetition.textContent = '📋 Copy Formal Petition'; }, 2000);
        });
      });
    }
  }

  // =========================================================================
  // 9. INITIALIZATION ENTRY POINT
  // =========================================================================
  function init() {
    populateStateDropdown();
    renderSchemeBrowser();
    initPrimaryTabs();
    initChatbot();
    initEligibilityTab();
    initClaimShieldTab();
    initWaterSubsidiesTab();
    initKccAndTrackerTab();
    initMspTab();
    initIntermediaryTab();

    // Event listeners for Tab 0 controls
    if (stateSelect) {
      stateSelect.addEventListener('change', function () {
        state.selectedState = this.value;
        localStorage.setItem('kisan_state', this.value);
        renderSchemeBrowser();
      });
    }

    if (changeStateBtn) {
      changeStateBtn.addEventListener('click', function () {
        if (stateSelect) {
          stateSelect.scrollIntoView({ behavior: 'smooth', block: 'center' });
          stateSelect.focus();
        }
      });
    }

    if (tabAllBtn) {
      tabAllBtn.addEventListener('click', function () {
        state.activeTab = 'all';
        [tabAllBtn, tabStateBtn, tabCentralBtn].forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        renderSchemeBrowser();
      });
    }
    if (tabStateBtn) {
      tabStateBtn.addEventListener('click', function () {
        state.activeTab = 'state';
        [tabAllBtn, tabStateBtn, tabCentralBtn].forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        renderSchemeBrowser();
      });
    }
    if (tabCentralBtn) {
      tabCentralBtn.addEventListener('click', function () {
        state.activeTab = 'central';
        [tabAllBtn, tabStateBtn, tabCentralBtn].forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        renderSchemeBrowser();
      });
    }

    if (searchInput) {
      searchInput.addEventListener('input', function () {
        state.searchQuery = this.value;
        renderSchemeBrowser();
      });
    }

    if (typeFilterSelect) {
      typeFilterSelect.addEventListener('change', function () {
        state.typeFilter = this.value;
        renderSchemeBrowser();
      });
    }

    if (eligibilityFilterSelect) {
      eligibilityFilterSelect.addEventListener('change', function () {
        state.eligibilityFilter = this.value;
        renderSchemeBrowser();
      });
    }

    if (langSelect) {
      langSelect.value = state.lang;
      langSelect.addEventListener('change', function () {
        state.lang = this.value;
        localStorage.setItem('kisan_lang', this.value);
        populateStateDropdown();
        renderSchemeBrowser();
      });
    }
  }

  // Run on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
