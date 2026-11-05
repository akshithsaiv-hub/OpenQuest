import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_js_path = os.path.join(base_dir, "frontend", "app.js")

with open(app_js_path, "r", encoding="utf-8") as f:
    code = f.read()

target_start = "  // =========================================================================\n  // 5. TAB 3: WATER-SAVING SUBSIDIES & LOW-WATER CROPS\n  // ========================================================================="
target_end = "  function renderWaterSchemes() {"

idx_start = code.find(target_start)
idx_end = code.find(target_end)

if idx_start == -1 or idx_end == -1:
    print(f"Could not find targets: start={idx_start}, end={idx_end}")
    exit(1)

new_code = """  // =========================================================================
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
      forecastRow.innerHTML = data.weather.forecast_daily.map(d => `
        <div class="weather-day-chip ${d.rain_prob === '0%' ? 'dry-alert' : ''}">
          <div style="font-size: 0.72rem; font-weight: 700; color: #64748b;">${escapeHtml(d.day)}</div>
          <div style="font-size: 1.4rem; margin: 0.15rem 0;">${d.icon}</div>
          <div style="font-size: 0.85rem; font-weight: 800; color: #1e293b;">${escapeHtml(d.temp)}</div>
          <div style="font-size: 0.72rem; color: #0284c7; font-weight: 600;">Rain: ${escapeHtml(d.rain_prob)}</div>
        </div>
      `).join('');
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
    alert(`🌾 Crop Migration Sowing Guide: ${cropName}\\n\\n💧 Water Savings: ${waterSaved} reduction vs routine flood crop\\n🌱 Recommended ICAR Seeds: ${varieties}\\n🌍 Soil & Climate Advantage: ${soilBenefit}\\n\\nAction: Register on State Horticulture / Agriculture Portal for ₹7,000/acre Crop Diversification DBT Incentive.`);
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

"""

code = code[:idx_start] + new_code + code[idx_end:]

with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(code)

print("frontend/app.js updated with dynamic water ecosystem logic!")
