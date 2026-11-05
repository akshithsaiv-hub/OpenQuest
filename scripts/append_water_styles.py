import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
styles_path = os.path.join(base_dir, "frontend", "styles.css")

with open(styles_path, "r", encoding="utf-8") as f:
    css = f.read()

water_css = """
/* =========================================================================
   CLIMATE-SMART WATER ECOSYSTEM & CROP MIGRATION ENGINE
   ========================================================================= */

.weather-ecosystem-card {
  background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 100%);
  border: 1px solid #bae6fd;
  border-radius: var(--radius-lg, 12px);
  padding: 1.25rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.08);
}

.weather-radar-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}

.weather-metric-box {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.weather-metric-icon {
  font-size: 2rem;
  line-height: 1;
}

.weather-metric-val {
  font-size: 1.35rem;
  font-weight: 800;
  line-height: 1.2;
}

.weather-metric-lbl {
  font-size: 0.78rem;
  color: var(--text-muted, #64748b);
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.weather-forecast-row {
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
}

.weather-day-chip.dry-alert {
  border-color: #fca5a5;
  background: #fff5f5;
}

.drought-alert-banner {
  background: #fef2f2;
  border-left: 5px solid #ef4444;
  border-radius: 8px;
  padding: 1rem 1.2rem;
  margin: 1rem 0;
  display: flex;
  gap: 0.85rem;
  align-items: flex-start;
}

.drought-alert-badge {
  display: inline-block;
  padding: 2px 8px;
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #f87171;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 800;
  animation: pulse-ring 2s infinite;
}

.drip-pathway-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.25rem;
  margin: 1.25rem 0;
}

.drip-pathway-card {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 1.2rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.drip-pathway-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.drip-pathway-card.buy-card {
  border-top: 4px solid #16a34a;
}

.drip-pathway-card.rent-card {
  border-top: 4px solid #0284c7;
}

.cost-breakdown-table {
  width: 100%;
  font-size: 0.84rem;
  margin: 0.75rem 0;
  border-collapse: collapse;
}

.cost-breakdown-table td {
  padding: 0.4rem 0;
  border-bottom: 1px dashed #e2e8f0;
}

.cost-breakdown-table td:last-child {
  text-align: right;
  font-weight: 700;
}

.crop-migration-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
  gap: 1.25rem;
  margin: 1.25rem 0;
}

.crop-migration-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1.15rem;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.crop-migration-card:hover {
  border-color: #86efac;
  box-shadow: 0 6px 14px rgba(22, 163, 74, 0.08);
}

.water-meter-wrap {
  margin: 0.65rem 0;
}

.water-meter-bar {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 0.35rem;
}

.water-meter-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #06b6d4 100%);
  border-radius: 4px;
}

.comparison-matrix-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
  margin-top: 1rem;
}

.comparison-matrix-table th {
  background: #f1f5f9;
  padding: 0.6rem 0.75rem;
  text-align: left;
  border-bottom: 2px solid #cbd5e1;
  font-weight: 700;
}

.comparison-matrix-table td {
  padding: 0.6rem 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}

.routine-row-highlight {
  background: #fff1f2;
}
"""

if "CLIMATE-SMART WATER ECOSYSTEM & CROP MIGRATION ENGINE" not in css:
    with open(styles_path, "a", encoding="utf-8") as f:
        f.write("\n" + water_css + "\n")
    print("styles.css updated with water ecosystem styling!")
else:
    print("Water ecosystem styling already in styles.css")
