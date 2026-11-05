import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_html_path = os.path.join(base_dir, "frontend", "index.html")

with open(index_html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Let's locate view-tab3
start_marker = '  <!-- TAB 3: WATER-SAVING SUBSIDIES & LOW-WATER CROPS -->'
if start_marker not in html:
    start_marker = '<div id="view-tab3"'

end_marker = '  <!-- TAB 4: KCC CREDIT & STATUS TRACKER -->'

idx_start = html.find(start_marker)
idx_end = html.find(end_marker)

if idx_start == -1 or idx_end == -1:
    print(f"Could not locate Tab 3 bounds: idx_start={idx_start}, idx_end={idx_end}")
    exit(1)

new_tab3_html = """  <!-- TAB 3: CLIMATE-SMART WATER SUBSIDIES & DYNAMIC CROP MIGRATION ECOSYSTEM -->
  <div id="view-tab3" class="tab-view" role="tabpanel" aria-labelledby="btn-tab3">
    <div class="view-header">
      <h2 class="view-title"><span>💧</span> <span data-i18n="tab3_title">Climate-Smart Water Subsidies & Dynamic Crop Migration Ecosystem</span></h2>
      <p class="view-desc" data-i18n="tab3_desc">
        Dynamic agro-climatic intelligence: Forecasts near-future dry spells, evaluates your current irrigation system, and identifies statutory bodies offering up to 100% subsidies to BUY or RENT micro-irrigation systems. Plus, calculates all viable high-yield crop migrations away from routine water-guzzling crops.
      </p>
    </div>

    <!-- 1. Interactive Farmer & Climate Simulation Control Console -->
    <div class="card" style="border-top: 4px solid #0ea5e9; background: #f8fafc; margin-bottom: 1.5rem;">
      <div class="card-header" style="border-bottom: 1px solid #e2e8f0; padding-bottom: 0.75rem;">
        <h3 class="card-title" style="color: #0369a1; font-size: 1.15rem;">
          <span>🛰️</span> <span>Agro-Climate & Farm Diagnostic Simulator</span>
        </h3>
        <p class="card-subtitle">
          Configure your location, routine crop, and current irrigation source to generate real-time weather advisories and tailored subsidies.
        </p>
      </div>

      <div class="form-row form-row-3" style="margin-top: 1rem;">
        <div class="form-group">
          <label class="form-label" for="ecoStateSelect">📍 State</label>
          <select id="ecoStateSelect" class="form-select">
            <option value="Telangana" selected>Telangana</option>
            <option value="Andhra Pradesh">Andhra Pradesh</option>
            <option value="Maharashtra">Maharashtra</option>
            <option value="Karnataka">Karnataka</option>
            <option value="Gujarat">Gujarat</option>
            <option value="Tamil Nadu">Tamil Nadu</option>
            <option value="Madhya Pradesh">Madhya Pradesh</option>
            <option value="Punjab">Punjab</option>
            <option value="Haryana">Haryana</option>
            <option value="Rajasthan">Rajasthan</option>
            <option value="Uttar Pradesh">Uttar Pradesh</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label" for="ecoDistrictSelect">🗺️ District</label>
          <select id="ecoDistrictSelect" class="form-select">
            <option value="Warangal" selected>Warangal</option>
            <option value="Karimnagar">Karimnagar</option>
            <option value="Nalgonda">Nalgonda</option>
            <option value="Mahabubnagar">Mahabubnagar</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label" for="ecoRoutineCrop">🌾 Routine Current Crop</label>
          <select id="ecoRoutineCrop" class="form-select">
            <option value="Paddy" selected>Paddy / Rice (High Water ~1,250 mm)</option>
            <option value="Sugarcane">Sugarcane (Extreme Water ~2,100 mm)</option>
            <option value="Cotton">Cotton (Moderate-High ~750 mm)</option>
            <option value="Banana">Banana (High Water ~1,800 mm)</option>
            <option value="Wheat">Wheat (~550 mm)</option>
            <option value="Maize">Maize (~500 mm)</option>
          </select>
        </div>
      </div>

      <div class="form-row form-row-3">
        <div class="form-group">
          <label class="form-label" for="ecoIrrigation">🚿 Current Irrigation Method</label>
          <select id="ecoIrrigation" class="form-select">
            <option value="flood" selected>❌ Flood / Furrow (Canal / Surface Flood)</option>
            <option value="borewell">❌ Borewell / Open Well (No Drip/Sprinkler)</option>
            <option value="rainfed">❌ Rainfed Only (Monsoon Dependent)</option>
            <option value="drip">✅ Drip Micro-Irrigation (Already Installed)</option>
            <option value="sprinkler">✅ Sprinkler System (Already Installed)</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label" for="ecoAcres">📐 Farm Extent (Acres)</label>
          <input type="number" id="ecoAcres" class="form-input" min="0.5" max="50" step="0.5" value="2.5" />
        </div>

        <div class="form-group">
          <label class="form-label" for="ecoCategory">👤 Farmer Social Category</label>
          <select id="ecoCategory" class="form-select">
            <option value="small_marginal" selected>Small / Marginal Farmer (&lt;5 Acres - 90% Subsidy)</option>
            <option value="sc_st">SC / ST Farmer (100% Free Drip Installation)</option>
            <option value="general">General / Other Farmer (80% Subsidy)</option>
          </select>
        </div>
      </div>

      <div style="display: flex; justify-content: flex-end; margin-top: 0.5rem;">
        <button type="button" id="btnRunEcoSimulation" class="btn btn-primary" style="padding: 0.55rem 1.25rem;">
          <span>⚡</span> <span>Recalculate Ecosystem Advisory</span>
        </button>
      </div>
    </div>

    <!-- 2. Dynamic Near-Future Weather & Dry Spell Radar -->
    <div class="weather-ecosystem-card">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
        <div>
          <span id="ecoDroughtBadge" class="drought-alert-badge">🚨 CRITICAL DRY SPELL ALERT</span>
          <h3 style="margin: 0.35rem 0 0 0; color: #0f172a; font-size: 1.2rem;">
            <span>🌦️</span> <span id="ecoLocationTitle">Near-Future Agro-Met Weather Forecast: Warangal, Telangana</span>
          </h3>
          <p style="margin: 0.2rem 0 0 0; font-size: 0.85rem; color: #475569;">
            Real-time automated IMD & ICAR dry-spell projections for next 14 to 30 days.
          </p>
        </div>
        <span class="badge-tag badge-tag-blue" id="ecoWeatherHorizon">14-Day Outlook</span>
      </div>

      <!-- Live Weather Metrics Radar -->
      <div class="weather-radar-grid">
        <div class="weather-metric-box">
          <span class="weather-metric-icon">📉</span>
          <div>
            <div class="weather-metric-val" id="ecoRainDeficit" style="color: #dc2626;">-46%</div>
            <div class="weather-metric-lbl">Rainfall Deficit vs Normal</div>
          </div>
        </div>

        <div class="weather-metric-box">
          <span class="weather-metric-icon">🌧️</span>
          <div>
            <div class="weather-metric-val" id="ecoRainMm" style="color: #0284c7;">12.5 mm</div>
            <div class="weather-metric-lbl">Projected 14-Day Rain</div>
          </div>
        </div>

        <div class="weather-metric-box">
          <span class="weather-metric-icon">🌱</span>
          <div>
            <div class="weather-metric-val" id="ecoSoilMoisture" style="color: #ea580c;">18% (Low)</div>
            <div class="weather-metric-lbl">Soil Moisture Stress</div>
          </div>
        </div>

        <div class="weather-metric-box">
          <span class="weather-metric-icon">🚰</span>
          <div>
            <div class="weather-metric-val" id="ecoDryDays" style="color: #b91c1c;">19 Days</div>
            <div class="weather-metric-lbl">Continuous Dry Spell</div>
          </div>
        </div>
      </div>

      <!-- 14-Day Micro-Forecast Scrollable Bar -->
      <div style="margin-top: 0.75rem;">
        <span style="font-size: 0.8rem; font-weight: 700; color: #475569; text-transform: uppercase;">14-Day Daily Agro-Met Strip:</span>
        <div id="ecoForecastRow" class="weather-forecast-row">
          <!-- Rendered dynamically -->
        </div>
      </div>

      <!-- Advisory Banner -->
      <div class="drought-alert-banner" id="ecoAdvisoryBanner">
        <span style="font-size: 1.8rem;">⚠️</span>
        <div>
          <h4 style="margin: 0; color: #991b1b; font-size: 0.95rem;">Dry Spell Critical Early Warning</h4>
          <p id="ecoAdvisoryText" style="margin: 0.25rem 0 0 0; font-size: 0.86rem; color: #7f1d1d; line-height: 1.5;">
            High evaporation rates and zero significant precipitation forecast over next 21 days. Traditional flood or borewell irrigation on routine Paddy will cause massive water exhaustion. Immediate micro-irrigation deployment or crop migration is recommended.
          </p>
        </div>
      </div>
    </div>

    <!-- 3. Smart Micro-Irrigation Matchmaker (BUY vs RENT) -->
    <div id="ecoDripSection" class="card" style="border-left: 5px solid #16a34a; margin-bottom: 1.5rem;">
      <div class="card-header" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
        <div>
          <span class="badge-tag badge-tag-green" id="ecoDripUrgencyBadge">URGENT ACTION RECOMMENDED</span>
          <h3 class="card-title" style="margin-top: 0.35rem; color: #15803d; font-size: 1.2rem;">
            <span>🚿</span> Micro-Irrigation Solution: Buy with Government Subsidy vs Subsidized Rental
          </h3>
          <p class="card-subtitle" id="ecoDripSubtitle">
            You currently do not have a drip system. Drip irrigation reduces water consumption by up to 60% and saves ₹7,500/acre in power pumping.
          </p>
        </div>
      </div>

      <!-- Parallel Pathways: Buy vs Rent -->
      <div class="drip-pathway-container">
        <!-- Pathway A: Buy with Subsidy -->
        <div class="drip-pathway-card buy-card">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="badge-tag badge-tag-green" style="font-size: 0.75rem;">Permanent Asset</span>
              <span id="ecoBuyBadgePct" style="font-size: 1.1rem; font-weight: 800; color: #15803d;">90% Subsidy</span>
            </div>
            <h4 style="margin: 0.5rem 0 0.25rem 0; font-size: 1.05rem; color: #14532d;">
              Pathway 1: BUY via Government Drip Subsidy
            </h4>
            <p style="font-size: 0.82rem; color: #4b5563; margin: 0;" id="ecoAgencyName">
              Telangana State Micro Irrigation Project (TSMIP)
            </p>

            <table class="cost-breakdown-table">
              <tbody>
                <tr>
                  <td>Total Drip Market Cost (<span id="ecoCostAcres">2.5</span> Acres):</td>
                  <td id="ecoTotalMarketCost">₹80,000</td>
                </tr>
                <tr>
                  <td style="color: #16a34a;">Government Subsidy Share (<span id="ecoSubsidyPctText">90%</span>):</td>
                  <td id="ecoGovtSubsidyAmount" style="color: #16a34a;">- ₹72,000</td>
                </tr>
                <tr style="border-top: 2px solid #cbd5e1; font-weight: 800; font-size: 0.95rem;">
                  <td style="color: #15803d;">Farmer's Net Payable Share:</td>
                  <td id="ecoFarmerPayableShare" style="color: #15803d;">Only ₹8,000</td>
                </tr>
              </tbody>
            </table>

            <div style="background: #f0fdf4; padding: 0.5rem 0.75rem; border-radius: 6px; font-size: 0.8rem; color: #166534; margin: 0.5rem 0;">
              ℹ️ <strong>Payback Time:</strong> Recouped in 0.8 seasons via electricity and fertilizer savings.
            </div>
          </div>

          <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <a id="ecoPortalLink" href="https://horticulture.tg.gov.in" target="_blank" class="btn btn-primary" style="flex: 1; text-align: center; font-size: 0.85rem; padding: 0.5rem 0.75rem;">
              <span>📝</span> Apply on State Drip Portal ↗
            </a>
            <button type="button" class="btn btn-secondary" onclick="alert('Contact your District Horticulture Officer (DHO) or visit your nearest MeeSeva / Rythu Vedika center.')" style="font-size: 0.85rem; padding: 0.5rem 0.75rem;">
              <span>📞</span> Helpline: <span id="ecoHelpline">1800-425-3502</span>
            </button>
          </div>
        </div>

        <!-- Pathway B: Rent Equipment -->
        <div class="drip-pathway-card rent-card">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="badge-tag badge-tag-blue" style="font-size: 0.75rem;">Emergency Rescue</span>
              <span style="font-size: 1.1rem; font-weight: 800; color: #0284c7;">₹350 - ₹450 / day</span>
            </div>
            <h4 style="margin: 0.5rem 0 0.25rem 0; font-size: 1.05rem; color: #0369a1;">
              Pathway 2: RENT from Custom Hiring Center (CHC)
            </h4>
            <p style="font-size: 0.82rem; color: #4b5563; margin: 0;" id="ecoRentHub">
              Rythu Vedikas, PACS &amp; KVK Equipment Banks
            </p>

            <table class="cost-breakdown-table">
              <tbody>
                <tr>
                  <td>Equipment Available:</td>
                  <td>Portable Drip Kits &amp; Raingun Sprinklers</td>
                </tr>
                <tr>
                  <td>Subsidized Rental Rate:</td>
                  <td style="color: #0284c7;">₹350 / day (₹1,200 / acre cycle)</td>
                </tr>
                <tr>
                  <td>Upfront Capital Required:</td>
                  <td style="color: #16a34a;">₹0 (Zero Debt)</td>
                </tr>
                <tr style="border-top: 2px solid #cbd5e1; font-weight: 800; font-size: 0.95rem;">
                  <td style="color: #0369a1;">Best For:</td>
                  <td style="color: #0369a1;">Immediate 20-Day Dry Spell Rescue</td>
                </tr>
              </tbody>
            </table>

            <div style="background: #f0f9ff; padding: 0.5rem 0.75rem; border-radius: 6px; font-size: 0.8rem; color: #0369a1; margin: 0.5rem 0;">
              🚜 <strong>Immediate Delivery:</strong> Rent mobile solar pumping sets and quick-connect drip laterals from your local Gram Panchayat hiring hub.
            </div>
          </div>

          <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <button type="button" class="btn btn-primary" onclick="alert('Rental Request Generated! Present this token at your local Custom Hiring Center (CHC) or PACS Rythu Vedika.')" style="flex: 1; text-align: center; font-size: 0.85rem; padding: 0.5rem 0.75rem; background: #0284c7;">
              <span>🎟️</span> Request Subsidized CHC Rental
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 4. Dynamic Routine Crop vs Alternative Crop Migration Engine -->
    <div class="card" style="border-top: 4px solid #f59e0b; margin-bottom: 1.5rem;">
      <div class="card-header" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
        <div>
          <span class="badge-tag badge-tag-amber">Crop Diversification Intelligence</span>
          <h3 class="card-title" style="margin-top: 0.35rem; color: #92400e; font-size: 1.2rem;">
            <span>🌱</span> Dynamic Crop Migration Opportunities (Move away from <span id="ecoRoutineCropName">Paddy</span>)
          </h3>
          <p class="card-subtitle">
            Switching from high-water routine crops to resilient alternatives saves up to 79% water, cuts cultivation costs in half, and qualifies for ₹7,000/acre State Crop Diversification incentives.
          </p>
        </div>
      </div>

      <!-- Current Routine Crop Baseline vs Migration Summary -->
      <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 1rem; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.75rem;">
        <div>
          <span style="font-size: 0.82rem; font-weight: 700; color: #92400e; text-transform: uppercase;">Your Routine Crop Baseline:</span>
          <div style="font-size: 1.1rem; font-weight: 800; color: #78350f;">
            <span id="ecoBaselineCrop">Paddy / Rice</span> • <span id="ecoBaselineWater">1,250 mm</span> water demand (<span id="ecoBaselineLiters">3.1 Cr</span> Liters)
          </div>
        </div>
        <div style="font-size: 0.84rem; color: #92400e; text-align: right;">
          Pumping Electricity/Diesel Cost: <strong id="ecoBaselinePowerCost">₹18,750</strong><br>
          Vulnerability Rating: <span class="badge-tag badge-tag-amber" id="ecoBaselineRisk">CRITICAL IN DRY SPELL</span>
        </div>
      </div>

      <!-- Dynamic Migration Alternative Cards Grid -->
      <div id="ecoCropMigrationGrid" class="crop-migration-grid">
        <!-- Rendered dynamically -->
      </div>

      <!-- Side-by-side Comparative Analysis Matrix -->
      <div style="margin-top: 1.5rem; overflow-x: auto;">
        <h4 style="margin: 0 0 0.5rem 0; color: #1e293b; font-size: 1rem;">
          📊 Side-by-Side Economic &amp; Water Savings Comparison Matrix
        </h4>
        <table class="comparison-matrix-table" id="ecoComparisonTable">
          <thead>
            <tr>
              <th>Crop Name</th>
              <th>Water (mm)</th>
              <th>Water Saved %</th>
              <th>Total Liters Saved</th>
              <th>MSP / Procurement</th>
              <th>Turnaround (Days)</th>
              <th>State Bonus</th>
              <th>Net Profit Impact</th>
            </tr>
          </thead>
          <tbody id="ecoComparisonTableBody">
            <!-- Rendered dynamically -->
          </tbody>
        </table>
      </div>
    </div>

    <!-- 5. Searchable Reference Catalog (18+ Schemes & 26+ Crops) -->
    <div class="card" style="margin-top: 1.5rem;">
      <div class="card-header" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem;">
        <div>
          <h3 class="card-title"><span>🚿</span> Reference Catalog: Verified Water-Saving Subsidies (18+ Schemes)</h3>
          <p class="card-subtitle">PMKSY (PDMC/HKKP), PM-KUSUM (Components A/B/C), TSMIP, APMIP, Krishi Bhagya &amp; Magel Tyala Shet Tale.</p>
        </div>
        <div>
          <span class="badge-tag badge-tag-green" id="waterSchemesBadge">18 Schemes Loaded</span>
        </div>
      </div>

      <!-- State & Category Filter for Schemes -->
      <div class="form-row form-row-2" style="margin-bottom: 1rem;">
        <div class="form-group">
          <label class="form-label" for="waterStateFilter">Filter by State</label>
          <select id="waterStateFilter" class="form-select">
            <option value="All">All States (Pan-India)</option>
            <option value="Telangana">Telangana</option>
            <option value="Andhra Pradesh">Andhra Pradesh</option>
            <option value="Maharashtra">Maharashtra</option>
            <option value="Karnataka">Karnataka</option>
            <option value="Gujarat">Gujarat</option>
            <option value="Tamil Nadu">Tamil Nadu</option>
            <option value="Madhya Pradesh">Madhya Pradesh</option>
            <option value="Punjab">Punjab</option>
            <option value="Haryana">Haryana</option>
            <option value="Rajasthan">Rajasthan</option>
            <option value="Uttar Pradesh">Uttar Pradesh</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label" for="waterTypeFilter">Filter by Technology</label>
          <select id="waterTypeFilter" class="form-select">
            <option value="All">All Technologies</option>
            <option value="Micro-Irrigation">Micro-Irrigation (Drip &amp; Sprinkler)</option>
            <option value="Solar Pump">Solar Pumps (PM-KUSUM)</option>
            <option value="Farm Pond">Farm Ponds &amp; Water Harvesting</option>
          </select>
        </div>
      </div>

      <!-- Water Schemes Cards Grid -->
      <div id="waterSchemesGrid" class="schemes-grid">
        <!-- Rendered dynamically -->
      </div>
    </div>

    <!-- Section B: 26+ Low-Water Crops -->
    <div class="card" style="margin-top: 1.5rem;">
      <div class="card-header" style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem;">
        <div>
          <h3 class="card-title"><span>🌱</span> Reference Catalog: Low-Water Crop Alternatives (26+ Crops)</h3>
          <p class="card-subtitle">Official ICAR &amp; Ministry of Agriculture advisories for drought mitigation with up to 88% water savings.</p>
        </div>
        <div>
          <span class="badge-tag badge-tag-blue" id="lowWaterCropsBadge">26 Crops Available</span>
        </div>
      </div>

      <!-- Category Filter Pills -->
      <div class="pill-group" id="cropCategoryPills">
        <button class="pill-btn active" data-cropcat="All">All Categories (26)</button>
        <button class="pill-btn" data-cropcat="Pulses">Pulses / Dal (8)</button>
        <button class="pill-btn" data-cropcat="Oilseeds">Oilseeds (6)</button>
        <button class="pill-btn" data-cropcat="Millets">Millets / Shree Anna (7)</button>
        <button class="pill-btn" data-cropcat="Commercial">Commercial / Cash (5)</button>
      </div>

      <!-- Crops Cards Grid -->
      <div id="lowWaterCropsGrid" class="schemes-grid">
        <!-- Rendered dynamically -->
      </div>
    </div>
  </div>
"""

html = html[:idx_start] + new_tab3_html + "\n\n" + html[idx_end:]

with open(index_html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("frontend/index.html updated with dynamic Tab 3 ecosystem!")
