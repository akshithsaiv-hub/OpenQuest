import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Update utils/agro_climate_advisory.py
advisory_path = os.path.join(base_dir, "utils", "agro_climate_advisory.py")
with open(advisory_path, "r", encoding="utf-8") as f:
    adv_code = f.read()

helper_14d = """
def generate_14day_forecast_strip(base_temp: float = 37.5, alert_level: str = "CRITICAL") -> List[Dict[str, Any]]:
    \"\"\"Generates 14 distinct individual daily weather cards for horizontal agro-met forecast.\"\"\"
    icons = ["☀️", "☀️", "☀️", "⛅", "🔥", "☀️", "🌦️", "☀️", "☀️", "🔥", "⛅", "☀️", "☀️", "☀️"]
    statuses = ["Severe Dry", "Sunny & Dry", "Dry Spell", "Partly Cloudy", "Heatwave Alert", "Clear Sky", "Light Rain", "Dry", "Dry", "Extreme Heat", "Mild Cloud", "Hot & Dry", "Dry", "Dry"]
    days_data = []
    
    for i in range(1, 15):
        temp = round(base_temp + ((i % 4) - 1.5) * 0.7, 1)
        if i == 7:
            rain = "15%"
            icon = "🌦️"
            status = "Light Rain"
        elif i in [4, 11]:
            rain = "10%"
            icon = "⛅"
            status = "Partly Cloudy"
        elif i in [5, 10]:
            rain = "0%"
            icon = "🔥"
            status = "Heatwave Alert"
        else:
            rain = "0%"
            icon = "☀️"
            status = "Zero Rain / Dry"
            
        days_data.append({
            "day": f"Day {i}",
            "temp": f"{temp}°C",
            "rain_prob": rain,
            "icon": icon,
            "status": status
        })
    return days_data
"""

if "def generate_14day_forecast_strip" not in adv_code:
    # Inject helper before get_district_weather
    idx_weather = adv_code.find("def get_district_weather(")
    adv_code = adv_code[:idx_weather] + helper_14d + "\n" + adv_code[idx_weather:]
    
    # In get_district_weather, always assign 14-day strip
    adv_code = adv_code.replace(
        "return profile",
        "profile = profile.copy()\n        profile[\"forecast_daily\"] = generate_14day_forecast_strip(profile.get(\"max_temp_c\", 37.5), profile.get(\"drought_alert_level\", \"CRITICAL\"))\n        return profile"
    )
    with open(advisory_path, "w", encoding="utf-8") as f:
        f.write(adv_code)
    print("utils/agro_climate_advisory.py updated with 14-day forecast generator!")

# 2. Update frontend/styles.css
styles_path = os.path.join(base_dir, "frontend", "styles.css")
with open(styles_path, "r", encoding="utf-8") as f:
    css = f.read()

old_css_rule = """.weather-forecast-row {
  display: flex;
  gap: 0.65rem;
  overflow-x: auto;
  padding: 0.5rem 0 0.85rem 0;
  scrollbar-width: thin;
}

.weather-day-chip {
  flex: 0 0 auto;
  min-width: 105px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 0.65rem 0.5rem;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}"""

new_css_rule = """.weather-forecast-row {
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  gap: 12px !important;
  overflow-x: auto !important;
  overflow-y: hidden !important;
  padding: 10px 4px 14px 4px !important;
  scrollbar-width: thin !important;
  -webkit-overflow-scrolling: touch !important;
  width: 100% !important;
  box-sizing: border-box !important;
}

.weather-forecast-row::-webkit-scrollbar {
  height: 6px;
}
.weather-forecast-row::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}
.weather-forecast-row::-webkit-scrollbar-thumb {
  background: #94a3b8;
  border-radius: 4px;
}

.weather-day-chip {
  flex: 0 0 135px !important;
  min-width: 135px !important;
  max-width: 140px !important;
  background: #ffffff;
  border: 2px solid #cbd5e1;
  border-radius: 12px;
  padding: 10px 8px;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: space-between !important;
  box-sizing: border-box !important;
}"""

if old_css_rule in css:
    css = css.replace(old_css_rule, new_css_rule)
    with open(styles_path, "w", encoding="utf-8") as f:
        f.write(css)
    print("frontend/styles.css updated with robust horizontal forecast rules!")

# 3. Update frontend/index.html
index_path = os.path.join(base_dir, "frontend", "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Cache-busting stylesheet link
html = html.replace('<link rel="stylesheet" href="styles.css">', '<link rel="stylesheet" href="styles.css?v=2.5">')

old_forecast_container = """      <!-- 14-Day Micro-Forecast Scrollable Bar -->
      <div style="margin-top: 0.75rem;">
        <span style="font-size: 0.8rem; font-weight: 700; color: #475569; text-transform: uppercase;">14-Day Daily Agro-Met Strip:</span>
        <div id="ecoForecastRow" class="weather-forecast-row">
          <!-- Rendered dynamically -->
        </div>
      </div>"""

new_forecast_container = """      <!-- 14-Day Micro-Forecast Horizontal Scrollable Bar -->
      <div style="margin-top: 1rem; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <span style="font-size: 0.85rem; font-weight: 800; color: #1e293b; text-transform: uppercase; display: flex; align-items: center; gap: 6px;">
            <span>📅</span> 14-Day Horizontal Agro-Met Weather Forecast
          </span>
          <span style="font-size: 0.75rem; color: #0284c7; font-weight: 700; background: #e0f2fe; padding: 3px 8px; border-radius: 12px;">
            Slide Horizontally ↔
          </span>
        </div>
        <div id="ecoForecastRow" class="weather-forecast-row" style="display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; gap: 12px !important; overflow-x: auto !important; overflow-y: hidden !important; padding: 8px 4px !important; scroll-behavior: smooth; -webkit-overflow-scrolling: touch; width: 100%; box-sizing: border-box;">
          <!-- Rendered dynamically -->
        </div>
      </div>"""

if old_forecast_container in html:
    html = html.replace(old_forecast_container, new_forecast_container)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("frontend/index.html updated with explicit horizontal container!")

# 4. Update frontend/app.js render logic for forecastRow
app_path = os.path.join(base_dir, "frontend", "app.js")
with open(app_path, "r", encoding="utf-8") as f:
    app_code = f.read()

old_app_forecast = """    if (forecastRow && data.weather.forecast_daily) {
      forecastRow.innerHTML = data.weather.forecast_daily.map(d => `
        <div class="weather-day-chip ${d.rain_prob === '0%' ? 'dry-alert' : ''}">
          <div style="font-size: 0.72rem; font-weight: 700; color: #64748b;">${escapeHtml(d.day)}</div>
          <div style="font-size: 1.4rem; margin: 0.15rem 0;">${d.icon}</div>
          <div style="font-size: 0.85rem; font-weight: 800; color: #1e293b;">${escapeHtml(d.temp)}</div>
          <div style="font-size: 0.72rem; color: #0284c7; font-weight: 600;">Rain: ${escapeHtml(d.rain_prob)}</div>
        </div>
      `).join('');
    }"""

new_app_forecast = """    if (forecastRow && data.weather.forecast_daily) {
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
    }"""

if old_app_forecast in app_code:
    app_code = app_code.replace(old_app_forecast, new_app_forecast)
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app_code)
    print("frontend/app.js updated with horizontal farmer weather card generator!")
