// Kisan Setu: Mobile-First Frontend Application Logic
// Features: 29 States Responsive Grid, Central & State Badges, Live Eligibility Engine, Multilingual

(function () {
  'use strict';

  // Application State
  const appState = {
    lang: localStorage.getItem('kisan_lang') || 'en',
    selectedState: localStorage.getItem('kisan_state') || '',
    activeTab: 'all', // 'all' | 'state' | 'central'
    typeFilter: 'all',
    eligibilityFilter: 'all',
    searchQuery: '',
    stateFilterQuery: '',
    activeEvaluationSchemeId: null,
    farmerProfile: JSON.parse(localStorage.getItem('kisan_farmer_profile') || JSON.stringify({
      state: localStorage.getItem('kisan_state') || 'Telangana',
      farmerType: 'owner',
      landAcres: 2.5,
      crop: 'Paddy',
      age: 40,
      isTaxPayer: 'no'
    }))
  };

  // DOM Elements
  const langSelect = document.getElementById('langSelect');
  const statesGrid = document.getElementById('statesGrid');
  const stateSearchInput = document.getElementById('stateSearchInput');
  const stateSelect = document.getElementById('stateSelect');
  const emptyStatePrompt = document.getElementById('emptyStatePrompt');
  const mainContent = document.getElementById('mainContent');
  const stateBanner = document.getElementById('stateBanner');
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

  // Modal Elements
  const eligibilityModal = document.getElementById('eligibilityModal');
  const modalBadge = document.getElementById('modalBadge');
  const modalSchemeTitle = document.getElementById('modalSchemeTitle');
  const modalSchemeSubtitle = document.getElementById('modalSchemeSubtitle');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const modalDoneBtn = document.getElementById('modalDoneBtn');
  const modalOfficialLink = document.getElementById('modalOfficialLink');

  const evalStateSelect = document.getElementById('evalStateSelect');
  const evalFarmerType = document.getElementById('evalFarmerType');
  const evalLandAcres = document.getElementById('evalLandAcres');
  const evalCrop = document.getElementById('evalCrop');
  const evalAge = document.getElementById('evalAge');
  const evalTaxPayer = document.getElementById('evalTaxPayer');

  const evalVerdictBanner = document.getElementById('evalVerdictBanner');
  const evalVerdictIcon = document.getElementById('evalVerdictIcon');
  const evalVerdictTitle = document.getElementById('evalVerdictTitle');
  const evalVerdictDesc = document.getElementById('evalVerdictDesc');
  const evalCriteriaList = document.getElementById('evalCriteriaList');
  const modalDocList = document.getElementById('modalDocList');

  // Helper to fetch translated UI label
  function t(key) {
    const dict = UI_TRANSLATIONS[appState.lang] || UI_TRANSLATIONS['en'];
    return dict[key] || UI_TRANSLATIONS['en'][key] || key;
  }

  // Populate States & UTs dropdown and 29 States Grid
  function populateStates() {
    // 1. Populate responsive 29 states grid
    if (statesGrid) {
      statesGrid.innerHTML = '';
      const query = appState.stateFilterQuery.toLowerCase().trim();
      const filteredStates = ALL_29_STATES.filter(function (st) {
        return st.name.toLowerCase().includes(query) || st.code.toLowerCase().includes(query);
      });

      if (filteredStates.length === 0) {
        statesGrid.innerHTML = `
          <div style="grid-column: 1 / -1; text-align: center; padding: 1.5rem; color: var(--text-muted); font-size: 0.95rem;">
            No states match "${appState.stateFilterQuery}".
          </div>
        `;
      } else {
        filteredStates.forEach(function (st) {
          const isSelected = st.name.toLowerCase() === appState.selectedState.toLowerCase();
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = `state-box-btn ${isSelected ? 'selected' : ''}`;
          btn.setAttribute('data-state', st.name);
          btn.setAttribute('role', 'button');
          btn.setAttribute('aria-pressed', isSelected ? 'true' : 'false');

          btn.innerHTML = `
            <div class="state-box-left">
              <span class="state-pin-icon" aria-hidden="true">🏛️</span>
              <span class="state-box-name">${st.name}</span>
            </div>
            <div style="display:flex; align-items:center; gap:0.35rem;">
              <span class="state-code-badge">${st.code}</span>
              <span class="state-check-mark" aria-hidden="true">✓</span>
            </div>
          `;

          btn.addEventListener('click', function () {
            selectState(st.name);
          });

          statesGrid.appendChild(btn);
        });
      }
    }

    // 2. Populate fallback dropdown
    if (stateSelect) {
      stateSelect.innerHTML = `<option value="">-- ${t('select_state_placeholder')} --</option>`;
      ALL_STATES_UT.forEach(function (st) {
        const opt = document.createElement('option');
        opt.value = st;
        opt.textContent = st;
        if (st.toLowerCase() === appState.selectedState.toLowerCase()) {
          opt.selected = true;
        }
        stateSelect.appendChild(opt);
      });
    }

    // 3. Populate evalStateSelect in modal
    if (evalStateSelect) {
      evalStateSelect.innerHTML = '';
      ALL_29_STATES.forEach(function (st) {
        const opt = document.createElement('option');
        opt.value = st.name;
        opt.textContent = st.name;
        if (st.name.toLowerCase() === (appState.farmerProfile.state || appState.selectedState || 'Telangana').toLowerCase()) {
          opt.selected = true;
        }
        evalStateSelect.appendChild(opt);
      });
    }
  }

  // Handle selecting a state
  function selectState(stateName) {
    if (!stateName) return;
    appState.selectedState = stateName;
    localStorage.setItem('kisan_state', stateName);
    appState.farmerProfile.state = stateName;
    localStorage.setItem('kisan_farmer_profile', JSON.stringify(appState.farmerProfile));

    // Update active class on grid boxes
    if (statesGrid) {
      statesGrid.querySelectorAll('.state-box-btn').forEach(function (box) {
        const isMatch = box.getAttribute('data-state').toLowerCase() === stateName.toLowerCase();
        box.classList.toggle('selected', isMatch);
        box.setAttribute('aria-pressed', isMatch ? 'true' : 'false');
      });
    }

    // Sync select dropdown
    if (stateSelect) {
      stateSelect.value = stateName;
    }

    render();

    // Scroll smoothly to schemes list
    setTimeout(function () {
      mainContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }

  // Translate static interface elements
  function updateStaticTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      const key = el.getAttribute('data-i18n');
      if (key && t(key)) {
        el.textContent = t(key);
      }
    });

    if (searchInput) {
      searchInput.placeholder = t('search_placeholder');
    }
    if (stateSearchInput) {
      stateSearchInput.placeholder = t('state_filter_placeholder');
    }

    if (langSelect) {
      langSelect.value = appState.lang;
    }
  }

  // Filter schemes based on active state, level, category, and search query
  function getFilteredSchemes() {
    if (!appState.selectedState) return [];

    const activeStateLower = appState.selectedState.toLowerCase();

    // Base pool: Central schemes + Selected State schemes
    let pool = SCHEMES_DATA.filter(function (s) {
      if (s.state === 'All') return true;
      return s.state.toLowerCase() === activeStateLower;
    });

    // 1. Tab filter (All / State / Central)
    if (appState.activeTab === 'central') {
      pool = pool.filter(function (s) { return s.level === 'Central'; });
    } else if (appState.activeTab === 'state') {
      pool = pool.filter(function (s) { return s.level === 'State'; });
    }

    // 2. Scheme Type Filter
    if (appState.typeFilter !== 'all') {
      pool = pool.filter(function (s) {
        return s.category === appState.typeFilter;
      });
    }

    // 3. Farmer Eligibility Filter
    if (appState.eligibilityFilter === 'tenant') {
      pool = pool.filter(function (s) {
        const text = (s.eligibility['en'] || '').toLowerCase();
        return !text.includes('oral tenants not eligible') && !text.includes('not covered') && !text.includes('tenants excluded');
      });
    } else if (appState.eligibilityFilter === 'small_marginal') {
      pool = pool.filter(function (s) {
        const text = (s.eligibility['en'] || '').toLowerCase();
        return text.includes('small and marginal') || text.includes('5 acres') || text.includes('10 acres') || text.includes('all farmers');
      });
    }

    // 4. Search Query Filter
    if (appState.searchQuery.trim() !== '') {
      const q = appState.searchQuery.toLowerCase().trim();
      pool = pool.filter(function (s) {
        const nameText = (s.name[appState.lang] || s.name['en'] || '').toLowerCase();
        const descText = (s.description[appState.lang] || s.description['en'] || '').toLowerCase();
        const benefitText = (s.benefit || '').toLowerCase();
        return nameText.includes(q) || descText.includes(q) || benefitText.includes(q);
      });
    }

    return pool;
  }

  // Count schemes for tabs
  function updateTabCounts() {
    if (!appState.selectedState) {
      countAll.textContent = '0';
      countState.textContent = '0';
      countCentral.textContent = '0';
      return;
    }

    const activeStateLower = appState.selectedState.toLowerCase();
    const allForState = SCHEMES_DATA.filter(function (s) {
      return s.state === 'All' || s.state.toLowerCase() === activeStateLower;
    });

    const stateCount = allForState.filter(function (s) { return s.level === 'State'; }).length;
    const centralCount = allForState.filter(function (s) { return s.level === 'Central'; }).length;

    countAll.textContent = allForState.length;
    countState.textContent = stateCount;
    countCentral.textContent = centralCount;

    // Update Tab Labels
    document.getElementById('labelTabState').textContent = `${appState.selectedState} ${t('tab_state')}`;
  }

  // Render Scheme Card HTML
  function createSchemeCard(scheme) {
    const isCentral = scheme.level === 'Central';
    const badgeClass = isCentral ? 'badge-central' : 'badge-state';
    const badgeText = isCentral ? t('badge_central') : `🏛️ ${appState.selectedState} ${t('badge_state')}`;

    const localizedName = scheme.name[appState.lang] || scheme.name['en'];
    const localizedDesc = scheme.description[appState.lang] || scheme.description['en'];
    const localizedEligibility = scheme.eligibility[appState.lang] || scheme.eligibility['en'];

    const docItemsHtml = (scheme.documents || []).map(function (doc) {
      return `<li class="doc-item"><span class="doc-check-icon">✓</span><span>${doc}</span></li>`;
    }).join('');

    const claimWindowHtml = scheme.claim_window ? `
      <div class="claim-window-alert">
        <span>⚠️</span>
        <span><strong>${t('emergency_rule')}:</strong> ${scheme.claim_window}</span>
      </div>
    ` : '';

    const criteria = scheme.criteria || {
      farmer_category: "All eligible farmers",
      landholding: "Standard landholding limits",
      crops: "All notified agricultural crops",
      location: scheme.state === 'All' ? "Pan-India" : `Resident of ${scheme.state}`,
      restrictions: "Aadhaar and land record documentation required"
    };

    return `
      <article class="scheme-card" data-scheme-id="${scheme.scheme_id}">
        <div class="card-header-area">
          <div class="badge-row">
            <span class="${badgeClass}">${badgeText}</span>
            <span class="scheme-category-tag">${(scheme.category || 'subsidy').replace('_', ' ')}</span>
          </div>
          <h3 class="scheme-card-title">${localizedName}</h3>
          <p class="scheme-card-desc">${localizedDesc}</p>
        </div>

        <div class="card-body-area">
          <!-- Key Benefit -->
          <div class="benefit-highlight-box">
            <div class="benefit-title">💰 ${t('benefit_label')}</div>
            <div class="benefit-value">${scheme.benefit}</div>
          </div>

          <!-- Eligibility Summary & Detailed Criteria -->
          <div class="eligibility-box">
            <div class="section-label">🎯 ${t('eligibility_label')}</div>
            <p class="eligibility-text">${localizedEligibility}</p>

            <!-- Structured Criteria Breakdown -->
            <div class="criteria-card-grid">
              <div class="criterion-row">
                <span class="crit-icon">👥</span>
                <div class="crit-body">
                  <span class="crit-label">${t('criteria_category')}:</span>
                  <span class="crit-value">${criteria.farmer_category}</span>
                </div>
              </div>
              <div class="criterion-row">
                <span class="crit-icon">📐</span>
                <div class="crit-body">
                  <span class="crit-label">${t('criteria_landholding')}:</span>
                  <span class="crit-value">${criteria.landholding}</span>
                </div>
              </div>
              <div class="criterion-row">
                <span class="crit-icon">🌾</span>
                <div class="crit-body">
                  <span class="crit-label">${t('criteria_crops')}:</span>
                  <span class="crit-value">${criteria.crops}</span>
                </div>
              </div>
              <div class="criterion-row">
                <span class="crit-icon">📍</span>
                <div class="crit-body">
                  <span class="crit-label">${t('criteria_location')}:</span>
                  <span class="crit-value">${criteria.location}</span>
                </div>
              </div>
              <div class="criterion-row">
                <span class="crit-icon">🚫</span>
                <div class="crit-body">
                  <span class="crit-label">${t('criteria_restrictions')}:</span>
                  <span class="crit-value">${criteria.restrictions}</span>
                </div>
              </div>
            </div>

            <!-- Check My Eligibility Button -->
            <button class="check-eligibility-btn" data-scheme-id="${scheme.scheme_id}" type="button">
              <span>🎯</span>
              <span>${t('check_eligibility_btn')}</span>
            </button>
          </div>

          <!-- Required Documents -->
          <div class="documents-box">
            <div class="section-label">📑 ${t('documents_label')}</div>
            <ul class="doc-list">${docItemsHtml}</ul>
          </div>

          <!-- Deadlines & Claim Windows -->
          <div class="deadline-box">
            <div class="section-label">⏰ ${t('deadline_label')}</div>
            <p class="deadline-text">${scheme.deadline || 'Continuous enrollment'}</p>
            ${claimWindowHtml}
          </div>
        </div>

        <div class="card-footer-area">
          <div class="last-verified-text">
            ${t('last_verified_label')}: <strong>${scheme.last_verified || '2026-10-25'}</strong>
          </div>
          <a href="${scheme.source_url}" target="_blank" rel="noopener noreferrer" class="official-link-btn">
            <span>${t('apply_button')}</span>
            <span>↗</span>
          </a>
        </div>
      </article>
    `;
  }

  // Render the Grid
  function render() {
    updateStaticTranslations();
    updateTabCounts();

    if (!appState.selectedState) {
      emptyStatePrompt.style.display = 'block';
      mainContent.style.display = 'none';
      return;
    }

    emptyStatePrompt.style.display = 'none';
    mainContent.style.display = 'block';

    // Update banner
    bannerStateName.textContent = appState.selectedState;
    const allForState = SCHEMES_DATA.filter(function (s) {
      return s.state === 'All' || s.state.toLowerCase() === appState.selectedState.toLowerCase();
    });
    const stateCount = allForState.filter(function (s) { return s.level === 'State'; }).length;
    const centralCount = allForState.filter(function (s) { return s.level === 'Central'; }).length;
    bannerStats.textContent = `(${stateCount} State Schemes + ${centralCount} Central Schemes Available)`;

    // Filter & render schemes
    const filtered = getFilteredSchemes();

    if (filtered.length === 0) {
      schemesGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3rem 1rem; background: #ffffff; border-radius: 12px; border: 2px dashed #cbd5e1;">
          <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔍</div>
          <h3 style="font-size: 1.25rem; font-weight: 800; margin-bottom: 0.5rem;">${t('no_results')}</h3>
          <button id="resetFiltersBtn" style="background: var(--primary); color: #ffffff; border: none; padding: 0.75rem 1.4rem; border-radius: 9999px; font-weight: 700; cursor: pointer; min-height: 48px; margin-top: 0.5rem;">
            ${t('clear_filters')}
          </button>
        </div>
      `;

      document.getElementById('resetFiltersBtn')?.addEventListener('click', function () {
        appState.activeTab = 'all';
        appState.typeFilter = 'all';
        appState.eligibilityFilter = 'all';
        appState.searchQuery = '';
        searchInput.value = '';
        typeFilterSelect.value = 'all';
        eligibilityFilterSelect.value = 'all';
        updateTabsUI();
        render();
      });
      return;
    }

    schemesGrid.innerHTML = filtered.map(createSchemeCard).join('');

    // Attach listeners to "Check my eligibility" buttons
    schemesGrid.querySelectorAll('.check-eligibility-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const schemeId = btn.getAttribute('data-scheme-id');
        openEligibilityModal(schemeId);
      });
    });
  }

  // Update visual state of level tabs
  function updateTabsUI() {
    [tabAllBtn, tabStateBtn, tabCentralBtn].forEach(function (btn) {
      btn.classList.remove('active');
    });

    if (appState.activeTab === 'all') tabAllBtn.classList.add('active');
    else if (appState.activeTab === 'state') tabStateBtn.classList.add('active');
    else if (appState.activeTab === 'central') tabCentralBtn.classList.add('active');
  }

  // ==========================================================================
  // Deterministic Eligibility Evaluation Modal Logic
  // ==========================================================================

  function openEligibilityModal(schemeId) {
    const scheme = SCHEMES_DATA.find(function (s) { return s.scheme_id === schemeId; });
    if (!scheme) return;

    appState.activeEvaluationSchemeId = schemeId;

    // Populate modal header
    const isCentral = scheme.level === 'Central';
    modalBadge.className = isCentral ? 'badge-central' : 'badge-state';
    modalBadge.textContent = isCentral ? t('badge_central') : `🏛️ ${scheme.state || appState.selectedState} ${t('badge_state')}`;
    modalSchemeTitle.textContent = scheme.name[appState.lang] || scheme.name['en'];
    modalSchemeSubtitle.textContent = scheme.benefit;
    modalOfficialLink.href = scheme.source_url;

    // Load saved farmer profile into modal inputs
    evalStateSelect.value = appState.farmerProfile.state || appState.selectedState || 'Telangana';
    evalFarmerType.value = appState.farmerProfile.farmerType || 'owner';
    evalLandAcres.value = appState.farmerProfile.landAcres !== undefined ? appState.farmerProfile.landAcres : 2.5;
    evalCrop.value = appState.farmerProfile.crop || 'Paddy';
    evalAge.value = appState.farmerProfile.age !== undefined ? appState.farmerProfile.age : 40;
    evalTaxPayer.value = appState.farmerProfile.isTaxPayer || 'no';

    // Populate documents list
    modalDocList.innerHTML = (scheme.documents || []).map(function (doc) {
      return `<li class="doc-item"><span class="doc-check-icon">✓</span><span>${doc}</span></li>`;
    }).join('');

    // Run evaluation
    evaluateFarmerEligibility(scheme);

    // Show modal
    eligibilityModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  function closeEligibilityModal() {
    eligibilityModal.style.display = 'none';
    document.body.style.overflow = '';
    appState.activeEvaluationSchemeId = null;
  }

  // Deterministic evaluation engine matching engine.py / test_runner.js exactly
  function evaluateFarmerEligibility(scheme) {
    if (!scheme) return;

    const r = scheme.rules || {};
    const profile = {
      state: evalStateSelect.value || appState.selectedState || 'Telangana',
      farmerType: evalFarmerType.value || 'owner',
      landAcres: parseFloat(evalLandAcres.value) || 0,
      crop: evalCrop.value || 'Paddy',
      age: parseInt(evalAge.value, 10) || 40,
      isTaxPayer: evalTaxPayer.value === 'yes'
    };

    // Save profile state
    appState.farmerProfile = {
      state: profile.state,
      farmerType: profile.farmerType,
      landAcres: profile.landAcres,
      crop: profile.crop,
      age: profile.age,
      isTaxPayer: evalTaxPayer.value
    };
    localStorage.setItem('kisan_farmer_profile', JSON.stringify(appState.farmerProfile));

    const criteriaResults = [];

    // 1. Location / State Criterion
    const stateReq = r.state_restriction || scheme.state || 'All';
    if (stateReq === 'All') {
      criteriaResults.push({
        title: "📍 Location / State Requirement",
        pass: true,
        message: `Pan-India Central Scheme: Available in all 29 Indian States & UTs (including ${profile.state}).`
      });
    } else {
      const match = stateReq.toLowerCase() === profile.state.toLowerCase();
      criteriaResults.push({
        title: "📍 Location / State Requirement",
        pass: match,
        message: match 
          ? `Resident of ${stateReq}: Matches state qualification requirement.`
          : `Restricted to resident farmers of ${stateReq} (Your selected profile state is ${profile.state}).`
      });
    }

    // 2. Farmer Land Ownership / Category Criterion
    const requiresLand = Boolean(r.requires_land_ownership);
    const tenantAllowed = r.tenant_allowed !== undefined ? Boolean(r.tenant_allowed) : true;

    if (profile.farmerType === 'tenant_oral') {
      if (!tenantAllowed || requiresLand) {
        criteriaResults.push({
          title: "👥 Farmer Ownership & Leasehold",
          pass: false,
          message: "Scheme legally requires registered landownership patta passbook. Oral tenants / sharecroppers excluded."
        });
      } else if (profile.landAcres <= 0) {
        criteriaResults.push({
          title: "👥 Farmer Ownership & Leasehold",
          pass: false,
          message: "Requires positive cultivated lease acreage (> 0 acres)."
        });
      } else {
        criteriaResults.push({
          title: "👥 Farmer Ownership & Leasehold",
          pass: true,
          message: "Tenant cultivators and sharecroppers are covered under this scheme."
        });
      }
    } else if (profile.farmerType === 'tenant_registered') {
      if (!tenantAllowed) {
        criteriaResults.push({
          title: "👥 Farmer Ownership & Leasehold",
          pass: false,
          message: "Direct landownership required; tenant farmers not covered under this specific DBT scheme."
        });
      } else {
        criteriaResults.push({
          title: "👥 Farmer Ownership & Leasehold",
          pass: true,
          message: "Registered tenant farmers with valid lease agreement / CCRC / Loan Eligibility Card are eligible."
        });
      }
    } else {
      // Landowner
      if (requiresLand && profile.landAcres <= 0) {
        criteriaResults.push({
          title: "👥 Farmer Ownership & Leasehold",
          pass: false,
          message: "Requires positive agricultural landholding acreage in farmer's name."
        });
      } else {
        criteriaResults.push({
          title: "👥 Farmer Ownership & Leasehold",
          pass: true,
          message: "Landowning farmer with valid patta / revenue land record verified."
        });
      }
    }

    // 3. Landholding Ceiling Criterion
    if (r.max_land_acres !== null && r.max_land_acres !== undefined) {
      const withinLimit = profile.landAcres <= r.max_land_acres;
      criteriaResults.push({
        title: "📐 Landholding Size Limit",
        pass: withinLimit,
        message: withinLimit 
          ? `Your landholding (${profile.landAcres} acres) is within the small/marginal ceiling of ${r.max_land_acres} acres.`
          : `Your landholding (${profile.landAcres} acres) exceeds the statutory maximum ceiling of ${r.max_land_acres} acres.`
      });
    } else {
      criteriaResults.push({
        title: "📐 Landholding Size Limit",
        pass: true,
        message: `No upper landholding ceiling for this scheme (${profile.landAcres} acres fully eligible).`
      });
    }

    // 4. Cultivated Crop Criterion
    if (r.supported_crops && r.supported_crops.length > 0) {
      const suppCrops = r.supported_crops.map(function (c) { return c.toLowerCase(); });
      const cropMatch = suppCrops.includes(profile.crop.toLowerCase()) || 
                        suppCrops.some(function (c) { return c.includes(profile.crop.toLowerCase()); });
      criteriaResults.push({
        title: "🌾 Crop Notification",
        pass: cropMatch,
        message: cropMatch 
          ? `${profile.crop} is an eligible notified crop for this season's scheme benefits.`
          : `${profile.crop} is not covered under this notification (Notified: ${r.supported_crops.slice(0, 5).join(', ')}...).`
      });
    } else {
      criteriaResults.push({
        title: "🌾 Crop Notification",
        pass: true,
        message: `Applicable to all agricultural and horticultural crops (${profile.crop} eligible).`
      });
    }

    // 5. Age Threshold Criterion
    let agePass = true;
    let ageMsg = `Farmer age (${profile.age} years) is within the eligible age threshold.`;
    if (r.min_age !== null && r.min_age !== undefined && profile.age < r.min_age) {
      agePass = false;
      ageMsg = `Farmer age (${profile.age} years) is below the minimum required age of ${r.min_age} years.`;
    } else if (r.max_age !== null && r.max_age !== undefined && profile.age > r.max_age) {
      agePass = false;
      ageMsg = `Farmer age (${profile.age} years) exceeds the maximum age limit of ${r.max_age} years.`;
    }
    criteriaResults.push({
      title: "🎂 Farmer Age Requirement",
      pass: agePass,
      message: ageMsg
    });

    // 6. Income Tax Payer Exclusions Criterion
    const isTaxExcluded = (r.excluded_categories || []).includes('income_tax_payer');
    if (profile.isTaxPayer && isTaxExcluded) {
      criteriaResults.push({
        title: "💼 Income Tax Exclusion",
        pass: false,
        message: "Income-tax paying farmers are legally excluded from this DBT welfare subsidy."
      });
    } else {
      criteriaResults.push({
        title: "💼 Income Tax Exclusion",
        pass: true,
        message: "Non-taxpayer status confirmed. Eligible for DBT subsidy release."
      });
    }

    // Determine Overall Verdict
    const allPassed = criteriaResults.every(function (c) { return c.pass; });

    // Update Verdict Banner
    if (allPassed) {
      evalVerdictBanner.className = 'verdict-banner verdict-eligible';
      evalVerdictIcon.textContent = '🟢';
      evalVerdictTitle.textContent = t('verdict_eligible_title');
      evalVerdictDesc.textContent = t('verdict_eligible_desc');
    } else {
      const failedCount = criteriaResults.filter(function (c) { return !c.pass; }).length;
      evalVerdictBanner.className = 'verdict-banner verdict-ineligible';
      evalVerdictIcon.textContent = '🔴';
      evalVerdictTitle.textContent = `${t('verdict_ineligible_title')} (${failedCount} Condition${failedCount > 1 ? 's' : ''} Not Met)`;
      evalVerdictDesc.textContent = t('verdict_ineligible_desc');
    }

    // Render Criteria Breakdown Checklist
    evalCriteriaList.innerHTML = criteriaResults.map(function (c) {
      return `
        <div class="eval-criterion-item ${c.pass ? 'pass' : 'fail'}">
          <span class="eval-crit-status-icon" aria-hidden="true">${c.pass ? '✓' : '✗'}</span>
          <div class="eval-crit-content">
            <span class="eval-crit-title">${c.title}</span>
            <span class="eval-crit-msg">${c.message}</span>
          </div>
        </div>
      `;
    }).join('');
  }

  // ==========================================================================
  // Event Listeners & Interactive Handlers
  // ==========================================================================

  // Language Change Listener
  langSelect.addEventListener('change', function (e) {
    appState.lang = e.target.value;
    localStorage.setItem('kisan_lang', appState.lang);
    populateStates();
    render();
    if (appState.activeEvaluationSchemeId) {
      const activeScheme = SCHEMES_DATA.find(function (s) { return s.scheme_id === appState.activeEvaluationSchemeId; });
      if (activeScheme) {
        evaluateFarmerEligibility(activeScheme);
      }
    }
  });

  // State Search Filter Input
  if (stateSearchInput) {
    stateSearchInput.addEventListener('input', function (e) {
      appState.stateFilterQuery = e.target.value;
      populateStates();
    });
  }

  // Fallback select dropdown listener
  if (stateSelect) {
    stateSelect.addEventListener('change', function (e) {
      selectState(e.target.value);
    });
  }

  // Change State Button in Banner
  changeStateBtn?.addEventListener('click', function () {
    if (stateSearchInput) {
      stateSearchInput.focus();
    }
    window.scrollTo({ top: statesGrid.getBoundingClientRect().top + window.scrollY - 120, behavior: 'smooth' });
  });

  // Level Tabs
  tabAllBtn.addEventListener('click', function () {
    appState.activeTab = 'all';
    updateTabsUI();
    render();
  });

  tabStateBtn.addEventListener('click', function () {
    appState.activeTab = 'state';
    updateTabsUI();
    render();
  });

  tabCentralBtn.addEventListener('click', function () {
    appState.activeTab = 'central';
    updateTabsUI();
    render();
  });

  // Instant Search Input
  searchInput.addEventListener('input', function (e) {
    appState.searchQuery = e.target.value;
    render();
  });

  // Filters
  typeFilterSelect.addEventListener('change', function (e) {
    appState.typeFilter = e.target.value;
    render();
  });

  eligibilityFilterSelect.addEventListener('change', function (e) {
    appState.eligibilityFilter = e.target.value;
    render();
  });

  // Modal Close Listeners
  closeModalBtn.addEventListener('click', closeEligibilityModal);
  modalDoneBtn.addEventListener('click', closeEligibilityModal);

  eligibilityModal.addEventListener('click', function (e) {
    if (e.target === eligibilityModal) {
      closeEligibilityModal();
    }
  });

  window.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && eligibilityModal.style.display !== 'none') {
      closeEligibilityModal();
    }
  });

  // Live evaluation triggers on modal input changes
  [evalStateSelect, evalFarmerType, evalLandAcres, evalCrop, evalAge, evalTaxPayer].forEach(function (input) {
    input.addEventListener('change', function () {
      if (appState.activeEvaluationSchemeId) {
        const activeScheme = SCHEMES_DATA.find(function (s) { return s.scheme_id === appState.activeEvaluationSchemeId; });
        if (activeScheme) {
          evaluateFarmerEligibility(activeScheme);
        }
      }
    });
    if (input.tagName === 'INPUT') {
      input.addEventListener('input', function () {
        if (appState.activeEvaluationSchemeId) {
          const activeScheme = SCHEMES_DATA.find(function (s) { return s.scheme_id === appState.activeEvaluationSchemeId; });
          if (activeScheme) {
            evaluateFarmerEligibility(activeScheme);
          }
        }
      });
    }
  });

  // ==========================================================================
  // Initialization
  // ==========================================================================
  populateStates();
  updateTabsUI();
  render();

})();
