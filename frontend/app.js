// Kisan Setu: Mobile-First Frontend Application Logic

(function () {
  'use strict';

  // Application State
  const state = {
    lang: localStorage.getItem('kisan_lang') || 'en',
    selectedState: localStorage.getItem('kisan_state') || '',
    activeTab: 'all', // 'all' | 'state' | 'central'
    typeFilter: 'all',
    eligibilityFilter: 'all',
    searchQuery: ''
  };

  // DOM Elements
  const langSelect = document.getElementById('langSelect');
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

  // Helper to fetch translated UI label
  function t(key) {
    const dict = UI_TRANSLATIONS[state.lang] || UI_TRANSLATIONS['en'];
    return dict[key] || UI_TRANSLATIONS['en'][key] || key;
  }

  // Populate States & UTs dropdown
  function populateStateDropdown() {
    stateSelect.innerHTML = `<option value="">-- ${t('select_state_placeholder')} --</option>`;
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

    if (langSelect) {
      langSelect.value = state.lang;
    }
  }

  // Filter schemes based on active state, level, category, and search query
  function getFilteredSchemes() {
    if (!state.selectedState) return [];

    const activeStateLower = state.selectedState.toLowerCase();

    // Base pool: Central schemes + Selected State schemes
    let pool = SCHEMES_DATA.filter(function (s) {
      if (s.state === 'All') return true;
      return s.state.toLowerCase() === activeStateLower;
    });

    // 1. Tab filter (All / State / Central)
    if (state.activeTab === 'central') {
      pool = pool.filter(function (s) { return s.level === 'Central'; });
    } else if (state.activeTab === 'state') {
      pool = pool.filter(function (s) { return s.level === 'State'; });
    }

    // 2. Scheme Type Filter
    if (state.typeFilter !== 'all') {
      pool = pool.filter(function (s) {
        return s.category === state.typeFilter;
      });
    }

    // 3. Farmer Eligibility Filter
    if (state.eligibilityFilter === 'tenant') {
      // Must allow tenant
      pool = pool.filter(function (s) {
        const text = (s.eligibility['en'] || '').toLowerCase();
        return !text.includes('oral tenants not eligible') && !text.includes('not covered');
      });
    } else if (state.eligibilityFilter === 'small_marginal') {
      pool = pool.filter(function (s) {
        const text = (s.eligibility['en'] || '').toLowerCase();
        return text.includes('small and marginal') || text.includes('5 acres') || text.includes('10 acres') || text.includes('all farmers');
      });
    }

    // 4. Search Query Filter
    if (state.searchQuery.trim() !== '') {
      const q = state.searchQuery.toLowerCase().trim();
      pool = pool.filter(function (s) {
        const nameText = (s.name[state.lang] || s.name['en'] || '').toLowerCase();
        const descText = (s.description[state.lang] || s.description['en'] || '').toLowerCase();
        const benefitText = (s.benefit || '').toLowerCase();
        return nameText.includes(q) || descText.includes(q) || benefitText.includes(q);
      });
    }

    return pool;
  }

  // Count schemes for tabs
  function updateTabCounts() {
    if (!state.selectedState) {
      countAll.textContent = '0';
      countState.textContent = '0';
      countCentral.textContent = '0';
      return;
    }

    const activeStateLower = state.selectedState.toLowerCase();
    const allForState = SCHEMES_DATA.filter(function (s) {
      return s.state === 'All' || s.state.toLowerCase() === activeStateLower;
    });

    const stateCount = allForState.filter(function (s) { return s.level === 'State'; }).length;
    const centralCount = allForState.filter(function (s) { return s.level === 'Central'; }).length;

    countAll.textContent = allForState.length;
    countState.textContent = stateCount;
    countCentral.textContent = centralCount;

    // Update Tab Labels
    document.getElementById('labelTabState').textContent = `${state.selectedState} ${t('tab_state')}`;
  }

  // Render Scheme Card HTML
  function createSchemeCard(scheme) {
    const isCentral = scheme.level === 'Central';
    const badgeClass = isCentral ? 'badge-central' : 'badge-state';
    const badgeText = isCentral ? t('badge_central') : `🏛️ ${state.selectedState} ${t('badge_state')}`;

    const localizedName = scheme.name[state.lang] || scheme.name['en'];
    const localizedDesc = scheme.description[state.lang] || scheme.description['en'];
    const localizedEligibility = scheme.eligibility[state.lang] || scheme.eligibility['en'];

    const docItemsHtml = scheme.documents.map(function (doc) {
      return `<li class="doc-item"><span class="doc-check-icon">✓</span><span>${doc}</span></li>`;
    }).join('');

    const claimWindowHtml = scheme.claim_window ? `
      <div class="claim-window-alert">
        <span>⚠️</span>
        <span><strong>${t('emergency_rule')}:</strong> ${scheme.claim_window}</span>
      </div>
    ` : '';

    return `
      <article class="scheme-card" data-scheme-id="${scheme.scheme_id}">
        <div class="card-header-area">
          <div class="badge-row">
            <span class="${badgeClass}">${badgeText}</span>
            <span class="scheme-category-tag">${scheme.category.replace('_', ' ')}</span>
          </div>
          <h2 class="scheme-card-title">${localizedName}</h2>
          <p class="scheme-card-desc">${localizedDesc}</p>
        </div>

        <div class="card-body-area">
          <!-- Key Benefit -->
          <div class="benefit-highlight-box">
            <div class="benefit-title">💰 ${t('benefit_label')}</div>
            <div class="benefit-value">${scheme.benefit}</div>
          </div>

          <!-- Eligibility -->
          <div class="eligibility-box">
            <div class="section-label">🎯 ${t('eligibility_label')}</div>
            <p class="eligibility-text">${localizedEligibility}</p>
          </div>

          <!-- Required Documents -->
          <div class="documents-box">
            <div class="section-label">📑 ${t('documents_label')}</div>
            <ul class="doc-list">${docItemsHtml}</ul>
          </div>

          <!-- Deadlines & Claim Windows -->
          <div class="deadline-box">
            <div class="section-label">⏰ ${t('deadline_label')}</div>
            <p class="deadline-text">${scheme.deadline}</p>
            ${claimWindowHtml}
          </div>
        </div>

        <div class="card-footer-area">
          <div class="last-verified-text">
            ${t('last_verified_label')}: <strong>${scheme.last_verified}</strong>
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

    if (!state.selectedState) {
      emptyStatePrompt.style.display = 'block';
      mainContent.style.display = 'none';
      return;
    }

    emptyStatePrompt.style.display = 'none';
    mainContent.style.display = 'block';

    // Update banner
    bannerStateName.textContent = state.selectedState;
    const allForState = SCHEMES_DATA.filter(function (s) {
      return s.state === 'All' || s.state.toLowerCase() === state.selectedState.toLowerCase();
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
          <button id="resetFiltersBtn" style="background: var(--primary); color: #ffffff; border: none; padding: 0.6rem 1.2rem; border-radius: 9999px; font-weight: 700; cursor: pointer; margin-top: 0.5rem;">
            ${t('clear_filters')}
          </button>
        </div>
      `;

      document.getElementById('resetFiltersBtn')?.addEventListener('click', function () {
        state.activeTab = 'all';
        state.typeFilter = 'all';
        state.eligibilityFilter = 'all';
        state.searchQuery = '';
        searchInput.value = '';
        typeFilterSelect.value = 'all';
        eligibilityFilterSelect.value = 'all';
        updateTabsUI();
        render();
      });
      return;
    }

    schemesGrid.innerHTML = filtered.map(createSchemeCard).join('');
  }

  // Update visual state of level tabs
  function updateTabsUI() {
    [tabAllBtn, tabStateBtn, tabCentralBtn].forEach(function (btn) {
      btn.classList.remove('active');
    });

    if (state.activeTab === 'all') tabAllBtn.classList.add('active');
    else if (state.activeTab === 'state') tabStateBtn.classList.add('active');
    else if (state.activeTab === 'central') tabCentralBtn.classList.add('active');
  }

  // Event Listeners
  langSelect.addEventListener('change', function (e) {
    state.lang = e.target.value;
    localStorage.setItem('kisan_lang', state.lang);
    populateStateDropdown();
    render();
  });

  stateSelect.addEventListener('change', function (e) {
    state.selectedState = e.target.value;
    localStorage.setItem('kisan_state', state.selectedState);
    render();
    if (state.selectedState) {
      mainContent.scrollIntoView({ behavior: 'smooth' });
    }
  });

  changeStateBtn?.addEventListener('click', function () {
    stateSelect.focus();
    window.scrollTo({ top: stateSelect.getBoundingClientRect().top + window.scrollY - 100, behavior: 'smooth' });
  });

  tabAllBtn.addEventListener('click', function () {
    state.activeTab = 'all';
    updateTabsUI();
    render();
  });

  tabStateBtn.addEventListener('click', function () {
    state.activeTab = 'state';
    updateTabsUI();
    render();
  });

  tabCentralBtn.addEventListener('click', function () {
    state.activeTab = 'central';
    updateTabsUI();
    render();
  });

  searchInput.addEventListener('input', function (e) {
    state.searchQuery = e.target.value;
    render();
  });

  typeFilterSelect.addEventListener('change', function (e) {
    state.typeFilter = e.target.value;
    render();
  });

  eligibilityFilterSelect.addEventListener('change', function (e) {
    state.eligibilityFilter = e.target.value;
    render();
  });

  // Initialization
  populateStateDropdown();
  updateTabsUI();
  render();

})();
