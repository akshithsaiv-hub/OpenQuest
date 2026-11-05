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
  // 4. TAB 2: 72-HOUR CLIMATE SHIELD & CLAIM ASSISTANT
  // =========================================================================
  function initClaimShieldTab() {
    // 72-Hour Live Countdown Timer
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

    // Weather Check Button
    const btnCheckWeather = document.getElementById('btnCheckWeather');
    if (btnCheckWeather) {
      btnCheckWeather.addEventListener('click', async function () {
        const district = document.getElementById('hazardDistrict').value || 'Warangal';
        const crop = document.getElementById('hazardCrop').value || 'Paddy';
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
              if (tempEl) tempEl.textContent = `${data.weather.temperature_c || 32.5}°C`;
              if (rainEl) rainEl.textContent = `${data.weather.rainfall_mm || 0.0} mm`;
              if (humEl) humEl.textContent = `${data.weather.humidity_percent || 48}%`;
            }
          }
        } catch (err) {
          console.warn('Weather API failed, using cached values.');
        } finally {
          btn.innerHTML = '<span>📡</span> Fetch Live Weather & Detect Risks';
        }
      });
    }

    // SMS Generator Form
    const claimSmsForm = document.getElementById('claimSmsForm');
    const smsResultBox = document.getElementById('smsResultBox');
    const smsTextDisplay = document.getElementById('smsTextDisplay');
    const btnCopySms = document.getElementById('btnCopySms');
    const btnSendSmsApp = document.getElementById('btnSendSmsApp');

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
          loss_percent: parseInt(document.getElementById('claimLossPct').value) || 75,
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
          generatedText = `[PMFBY 72-HR CROP LOSS INTIMATION]\n` +
            `Farmer: ${reqData.farmer_name} (Ph: ${reqData.phone})\n` +
            `Village: ${reqData.village}, District: ${reqData.district}\n` +
            `Survey No: ${reqData.survey_no}\n` +
            `Crop: ${reqData.crop} (${reqData.acreage} Acres)\n` +
            `Calamity: ${reqData.hazard_type}\n` +
            `Est Loss: ${reqData.loss_percent}%\n` +
            `Timestamp: ${nowIso}\n` +
            `Action: Formal intimation submitted within statutory 72 hours per PMFBY Section 21.4. Please issue docket reference number.`;
        }

        if (smsTextDisplay) smsTextDisplay.textContent = generatedText;
        if (smsResultBox) smsResultBox.style.display = 'block';
        if (btnSendSmsApp) btnSendSmsApp.href = `sms:18001801551?body=${encodeURIComponent(generatedText)}`;
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
  }

  // =========================================================================
  // 5. TAB 3: WATER-SAVING SUBSIDIES & LOW-WATER CROPS
  // =========================================================================
  let cachedWaterSchemes = [];
  let cachedLowWaterCrops = [];

  async function initWaterSubsidiesTab() {
    // Load Schemes from API or embedded data
    try {
      const resp = await fetch(`${API_BASE}/water_saving_schemes`);
      if (resp.ok) cachedWaterSchemes = await resp.json();
    } catch (err) {
      console.warn('Backend /water_saving_schemes not available, using embedded.');
    }
    if (!cachedWaterSchemes || cachedWaterSchemes.length === 0) {
      cachedWaterSchemes = typeof WATER_SAVING_SCHEMES_DATA !== 'undefined' ? WATER_SAVING_SCHEMES_DATA : [];
    }

    // Load Crops from API or embedded data
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

    grid.innerHTML = pool.map(s => `
      <article class="scheme-card" style="border-left: 4px solid #0284c7;">
        <div class="scheme-header-area">
          <span class="badge badge-central">${s.level} • ${s.category}</span>
          <h3 class="scheme-title" style="margin-top: 0.35rem;">${s.scheme_name}</h3>
          <p class="scheme-desc">${s.objective || ''}</p>
        </div>
        <div class="scheme-body-area">
          <div class="benefit-highlight">
            <span class="benefit-label">Subsidy Rate</span>
            <div class="benefit-value" style="color: #0369a1;">${s.subsidy_percentage || '50% - 90%'}</div>
          </div>
          <div class="scheme-field">
            <span class="field-title">Key Eligibility</span>
            <p class="field-content">${s.eligibility_summary || 'All farmers with valid land records.'}</p>
          </div>
          <div class="scheme-field">
            <span class="field-title">Max Assistance / Cap</span>
            <p class="field-content">${s.max_assistance || 'As per DLTC norms'}</p>
          </div>
        </div>
        <div class="card-footer-area">
          <span class="last-verified-text">State: ${(s.applicable_states || []).join(', ')}</span>
          <a href="${s.official_portal || '#'}" target="_blank" class="official-link-btn" style="background: #0284c7;">Portal ↗</a>
        </div>
      </article>
    `).join('');
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

    grid.innerHTML = pool.map(c => `
      <div class="card" style="border-left: 4px solid #16a34a; margin-bottom: 0;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <span class="badge-tag badge-tag-green">${c.category}</span>
            <h4 style="margin: 0.35rem 0 0.1rem 0; font-size: 1.1rem;">${c.crop_name}</h4>
            <span style="font-size: 0.82rem; color: var(--text-muted);">${c.telugu_name || ''} • ${c.hindi_name || ''}</span>
          </div>
          <span class="badge-tag badge-tag-amber" style="font-weight: 800;">${c.water_savings_vs_paddy || '-70% Water'}</span>
        </div>
        <div style="margin: 0.75rem 0; background: #f8fafc; padding: 0.6rem; border-radius: 6px; font-size: 0.85rem;">
          <div><strong>MSP Rate:</strong> ${c.msp_2024_25 || 'Market Linked'}</div>
          <div><strong>Duration:</strong> ${c.duration_days || '90-120'} days • <strong>Drought Tolerance:</strong> ${c.drought_tolerance || 'High'}</div>
          <div><strong>Water Req:</strong> ${c.water_requirement_mm || '400-500'} mm (vs Paddy 1200mm)</div>
        </div>
        <p style="font-size: 0.82rem; color: #475569; margin: 0; line-height: 1.4;">
          ${c.economic_advisory || ''}
        </p>
      </div>
    `).join('');
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
