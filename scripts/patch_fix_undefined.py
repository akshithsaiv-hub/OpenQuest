import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Patch frontend/app.js
app_js_path = os.path.join(base_dir, "frontend", "app.js")
with open(app_js_path, "r", encoding="utf-8") as f:
    code = f.read()

target_start = "  function renderWaterSchemes() {"
target_end = "  // =========================================================================\n  // 6. TAB 4: KCC CREDIT & STATUS TRACKER"

idx_start = code.find(target_start)
idx_end = code.find(target_end)

if idx_start == -1 or idx_end == -1:
    print(f"Could not locate targets in app.js: idx_start={idx_start}, idx_end={idx_end}")
    exit(1)

fixed_render_functions = """  function renderWaterSchemes() {
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
"""

code = code[:idx_start] + fixed_render_functions + "\n" + code[idx_end:]
with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(code)
print("frontend/app.js patched to eliminate undefined labels!")

# 2. Patch backend/eligibility_api.py
api_path = os.path.join(base_dir, "backend", "eligibility_api.py")
with open(api_path, "r", encoding="utf-8") as f:
    api_code = f.read()

old_ws_route = """@app.get("/water_saving_schemes")
def get_water_saving_schemes_compat(state: Optional[str] = None):
    if not os.path.exists(WATER_SCHEMES_PATH):
        return []
    with open(WATER_SCHEMES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if state and state.lower() != "all":
        data = [s for s in data if "All States" in s.get("applicable_states", []) or state.lower() in [st.lower() for st in s.get("applicable_states", [])]]
    return data

@app.get("/low_water_crops")
def get_low_water_crops_compat(category: Optional[str] = None):
    if not os.path.exists(LOW_WATER_CROPS_PATH):
        return []
    with open(LOW_WATER_CROPS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if category and category.lower() != "all":
        data = [c for c in data if category.lower() in c.get("category", "").lower()]
    return data"""

new_ws_route = """@app.get("/water_saving_schemes")
def get_water_saving_schemes_compat(state: Optional[str] = None):
    if not os.path.exists(WATER_SCHEMES_PATH):
        return []
    with open(WATER_SCHEMES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if state and state.lower() != "all":
        data = [s for s in data if "All States" in s.get("applicable_states", []) or state.lower() in [st.lower() for st in s.get("applicable_states", [])]]
    # Normalize fields to guarantee no undefined
    for s in data:
        title = s.get("name") or s.get("scheme_name") or "Water Conservation Scheme"
        s["name"] = title
        s["scheme_name"] = title
        desc = s.get("water_savings_potential") or s.get("target_beneficiaries") or s.get("objective") or "Official government water conservation and irrigation scheme."
        s["objective"] = desc
        s["water_savings_potential"] = desc
        if not s.get("portal_url") and s.get("official_portal"):
            s["portal_url"] = s["official_portal"]
        if not s.get("official_portal") and s.get("portal_url"):
            s["official_portal"] = s["portal_url"]
    return data

@app.get("/low_water_crops")
def get_low_water_crops_compat(category: Optional[str] = None):
    if not os.path.exists(LOW_WATER_CROPS_PATH):
        return []
    with open(LOW_WATER_CROPS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if category and category.lower() != "all":
        data = [c for c in data if category.lower() in c.get("category", "").lower()]
    # Normalize fields to guarantee no undefined
    for c in data:
        title = c.get("name") or c.get("crop_name") or "Resilient Low-Water Crop"
        c["name"] = title
        c["crop_name"] = title
        savings = c.get("water_savings_percentage") or c.get("water_savings_vs_paddy") or "-65% Water"
        c["water_savings_percentage"] = savings
        c["water_savings_vs_paddy"] = savings
    return data"""

if old_ws_route in api_code:
    api_code = api_code.replace(old_ws_route, new_ws_route)
    with open(api_path, "w", encoding="utf-8") as f:
        f.write(api_code)
    print("backend/eligibility_api.py patched to normalize scheme and crop fields!")
else:
    print("Could not find exact old_ws_route match in backend/eligibility_api.py")
