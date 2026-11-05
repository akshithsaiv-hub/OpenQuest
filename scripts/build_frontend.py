import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
layout_path = os.path.join(base_dir, 'frontend', 'stitch_layout.html')
index_path = os.path.join(base_dir, 'frontend', 'index.html')

with open(layout_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update language selector
old_lang = '<select class="bg-transparent border-0 text-label-lg font-label-lg font-bold text-on-surface focus:ring-0 p-0 pr-4 cursor-pointer">'
new_lang = '<select id="lang-select-box" class="bg-transparent border-0 text-label-lg font-label-lg font-bold text-on-surface focus:ring-0 p-0 pr-4 cursor-pointer"><option value="en">English</option><option value="te">తెలుగు (Telugu)</option><option value="hi">हिन्दी (Hindi)</option><option value="mr">मराठी (Marathi)</option><option value="ta">தமிழ் (Tamil)</option></select>'
if old_lang in html:
    start_pos = html.find(old_lang)
    end_pos = html.find('</select>', start_pos) + len('</select>')
    html = html[:start_pos] + new_lang + html[end_pos:]
    print('Language selector updated!')

# 2. Add dispatch-claim-trigger to Emergency 72h Hotline link in header
html = html.replace(
    'href="#claim-shield">\n<span class="material-symbols-outlined text-lg" style="font-variation-settings: \'FILL\' 1;">emergency</span>\n<span>Emergency 72h Hotline</span>',
    'href="#claim-shield" class="dispatch-claim-trigger">\n<span class="material-symbols-outlined text-lg" style="font-variation-settings: \'FILL\' 1;">emergency</span>\n<span>Emergency 72h Hotline</span>'
)

# 3. Add IDs to hero titles
html = html.replace(
    '<h1 class="text-display font-display text-primary tracking-tight leading-tight">',
    '<h1 id="hero-main-title" class="text-display font-display text-primary tracking-tight leading-tight">'
)
html = html.replace(
    '<p class="text-body-lg font-body-lg text-on-surface-variant max-w-2xl">',
    '<p id="hero-main-desc" class="text-body-lg font-body-lg text-on-surface-variant max-w-2xl">'
)

# 4. Hero Query AI input
old_ai_box = """<input class="w-full bg-transparent border-none text-body-md font-body-md focus:ring-0 text-on-surface placeholder:text-outline" placeholder="Ask in Hindi, Telugu, or English: 'KCC scale of finance for 3 acres cotton?'" type="text"/>
<button aria-label="Voice Search" class="bg-primary-container text-on-primary p-2.5 rounded-lg hover:bg-primary transition-colors flex items-center justify-center shrink-0" title="Voice Search">
<span class="material-symbols-outlined text-xl">mic</span>
</button>
<button class="bg-primary text-on-primary px-4 py-2.5 rounded-lg text-label-lg font-label-lg font-bold hover:bg-primary-container transition-colors shrink-0">
              Query AI
            </button>"""

new_ai_box = """<input id="ai-query-input" class="w-full bg-transparent border-none text-body-md font-body-md focus:ring-0 text-on-surface placeholder:text-outline" placeholder="Ask in Hindi, Telugu, or English: 'KCC scale of finance for 3 acres cotton?'" type="text"/>
<button id="ai-query-btn" class="bg-primary text-on-primary px-4 py-2.5 rounded-lg text-label-lg font-label-lg font-bold hover:bg-primary-container transition-colors shrink-0">
              Query AI
            </button>"""

if old_ai_box in html:
    html = html.replace(old_ai_box, new_ai_box)
    print('Hero AI box updated!')

# Add container for AI query results right after the AI input box div
html = html.replace(
    '<!-- Live Stat Counters -->',
    '<div id="ai-query-result" class="hidden"></div>\n<!-- Live Stat Counters -->'
)

# 5. Interactive Matcher Form
old_form_tag = '<form class="space-y-4" onsubmit="event.preventDefault(); document.getElementById(\'match-results\').classList.remove(\'hidden\');">'
new_form_tag = '<form id="matcher-form" class="space-y-4">'
html = html.replace(old_form_tag, new_form_tag)

states_list = [
    'Telangana', 'Andhra Pradesh', 'Maharashtra', 'Punjab', 'Haryana', 
    'Karnataka', 'Tamil Nadu', 'Uttar Pradesh', 'Madhya Pradesh', 'Gujarat', 
    'Rajasthan', 'Bihar', 'West Bengal', 'Odisha', 'Kerala', 'Assam', 
    'Chhattisgarh', 'Jharkhand', 'Himachal Pradesh', 'Uttarakhand'
]
state_options = '\n'.join([f'<option value="{s}">{s}</option>' for s in states_list])
old_select = """<select class="w-full bg-surface border border-outline-variant rounded-lg py-2.5 px-3 text-body-md font-body-md focus:border-primary focus:ring-1 focus:ring-primary" id="state-select">
<option value="Telangana">Telangana (Semi-Arid Deccan)</option>
<option value="Andhra Pradesh">Andhra Pradesh (Rayalaseema &amp; Coastal)</option>
<option value="Maharashtra">Maharashtra (Vidarbha / Marathwada)</option>
<option value="Punjab">Punjab (Indo-Gangetic Basin)</option>
<option value="Haryana">Haryana (Semi-Arid Irrigated)</option>
<option value="Karnataka">Karnataka (Southern Transition)</option>
</select>"""
new_select = f'<select class="w-full bg-surface border border-outline-variant rounded-lg py-2.5 px-3 text-body-md font-body-md focus:border-primary focus:ring-1 focus:ring-primary" id="state-select">{state_options}</select>'
html = html.replace(old_select, new_select)

# Land and Category selects
html = html.replace(
    '<label class="block text-label-lg font-label-lg text-on-surface mb-1.5">Land Holding</label>\n<select class="w-full bg-surface border border-outline-variant rounded-lg py-2.5 px-3 text-body-md font-body-md focus:border-primary focus:ring-1 focus:ring-primary">',
    '<label class="block text-label-lg font-label-lg text-on-surface mb-1.5">Land Holding</label>\n<select id="land-select" class="w-full bg-surface border border-outline-variant rounded-lg py-2.5 px-3 text-body-md font-body-md focus:border-primary focus:ring-1 focus:ring-primary">'
)
html = html.replace(
    '<label class="block text-label-lg font-label-lg text-on-surface mb-1.5">Social Category</label>\n<select class="w-full bg-surface border border-outline-variant rounded-lg py-2.5 px-3 text-body-md font-body-md focus:border-primary focus:ring-1 focus:ring-primary">',
    '<label class="block text-label-lg font-label-lg text-on-surface mb-1.5">Social Category</label>\n<select id="category-select" class="w-full bg-surface border border-outline-variant rounded-lg py-2.5 px-3 text-body-md font-body-md focus:border-primary focus:ring-1 focus:ring-primary">'
)
html = html.replace(
    '<label class="block text-label-lg font-label-lg text-on-surface mb-1.5">Current Standing Crop</label>\n<input class="w-full bg-surface border border-outline-variant rounded-lg py-2.5 px-3 text-body-md font-body-md focus:border-primary focus:ring-1 focus:ring-primary" type="text" value="Paddy / Cotton / Bengal Gram"/>',
    '<label class="block text-label-lg font-label-lg text-on-surface mb-1.5">Current Standing Crop</label>\n<input id="crop-input" class="w-full bg-surface border border-outline-variant rounded-lg py-2.5 px-3 text-body-md font-body-md focus:border-primary focus:ring-1 focus:ring-primary" type="text" value="Paddy"/>'
)
html = html.replace(
    '<button class="w-full bg-primary hover:bg-primary-container text-on-primary py-3 rounded-lg text-label-lg font-label-lg font-bold flex items-center justify-center gap-2 active:scale-95 transition-all shadow-sm" type="submit">',
    '<button id="matcher-submit-btn" class="w-full bg-primary hover:bg-primary-container text-on-primary py-3 rounded-lg text-label-lg font-label-lg font-bold flex items-center justify-center gap-2 active:scale-95 transition-all shadow-sm" type="submit">'
)
html = html.replace(
    '<div class="p-3 bg-primary-fixed/20 border border-primary-fixed-dim rounded-lg text-body-sm font-body-sm text-primary flex items-start gap-2" id="match-results">',
    '<div class="p-3 bg-primary-fixed/20 border border-primary-fixed-dim rounded-lg text-body-sm font-body-sm text-primary flex items-start gap-2 hidden" id="match-results">'
)

# 6. Claim Shield section button
html = html.replace(
    '<button class="bg-error hover:bg-error/90 text-on-error px-5 py-2.5 rounded-lg text-label-lg font-label-lg font-bold flex items-center gap-2 active:scale-95 transition-all shadow-sm">',
    '<button class="dispatch-claim-trigger bg-error hover:bg-error/90 text-on-error px-5 py-2.5 rounded-lg text-label-lg font-label-lg font-bold flex items-center gap-2 active:scale-95 transition-all shadow-sm">'
)

# 7. KCC Card button
html = html.replace(
    '<a class="inline-flex items-center gap-1 text-label-lg font-label-lg text-secondary font-bold hover:underline" href="#kcc-calc">',
    '<a id="kcc-calc-btn" class="inline-flex items-center gap-1 text-label-lg font-label-lg text-secondary font-bold hover:underline cursor-pointer" href="#kcc-calc">'
)

# 8. Consent Vault Card enhancement
old_vault_content = """<div class="p-2.5 rounded bg-surface border border-outline-variant flex items-center justify-between text-xs">
<span class="font-mono text-on-surface-variant">Passbook: 'Ravi Kumer'</span>
<span class="text-primary font-bold bg-primary-fixed px-1.5 py-0.5 rounded">94% Fuzzy Match</span>
</div>
<div class="text-xs text-on-surface-variant">
            Zero-knowledge Aadhaar masking + instant consent revocation toggle.
          </div>"""

new_vault_content = """<div class="space-y-2 mt-2">
  <div class="grid grid-cols-2 gap-2 text-xs">
    <input id="fuzzy-aadhaar-input" type="text" class="bg-surface border border-outline-variant rounded p-1.5 text-xs font-mono" value="Ravi Kumar" placeholder="Aadhaar Name" />
    <input id="fuzzy-bank-input" type="text" class="bg-surface border border-outline-variant rounded p-1.5 text-xs font-mono" value="Ravi Kumer" placeholder="Bank Name" />
  </div>
  <div class="flex items-center justify-between gap-2">
    <button id="fuzzy-verify-btn" type="button" class="bg-primary text-on-primary px-2.5 py-1 rounded text-xs font-bold hover:bg-primary-container transition-colors">
      Verify Name Match
    </button>
    <button id="consent-toggle-btn" type="button" class="bg-primary text-on-primary px-2 py-1 rounded text-[11px] font-bold">
      Active Consent (Revoke?)
    </button>
  </div>
  <div id="fuzzy-result-badge" class="hidden p-2.5 rounded text-xs border"></div>
</div>"""
html = html.replace(old_vault_content, new_vault_content)

# 9. MSP Benchmark table body
html = html.replace('<tbody class="divide-y divide-outline-variant">', '<tbody id="msp-table-body" class="divide-y divide-outline-variant">')

# 10. Intermediary / CSC section container
old_csc_toolkit = """<div class="grid grid-cols-2 gap-4">
<div class="p-3 bg-surface-container-low rounded-lg border border-outline-variant space-y-1">
<span class="material-symbols-outlined text-primary text-xl">checklist</span>
<div class="font-bold text-sm text-on-surface">Batch Applications</div>
<div class="text-xs text-on-surface-variant">Process 20+ farmers simultaneously with single village survey upload.</div>
</div>
<div class="p-3 bg-surface-container-low rounded-lg border border-outline-variant space-y-1">
<span class="material-symbols-outlined text-secondary text-xl">fingerprint</span>
<div class="font-bold text-sm text-on-surface">Consent Manager</div>
<div class="text-xs text-on-surface-variant">UIDAI compliant opt-in with immediate one-click consent revocation.</div>
</div>
</div>"""

new_csc_toolkit = """<div class="space-y-3">
  <div class="text-xs font-bold text-primary flex items-center justify-between">
    <span>Live Grama Priority Cases (SQLite Database)</span>
    <span class="bg-primary-fixed text-on-primary-fixed px-2 py-0.5 rounded text-[10px]">Sync Active</span>
  </div>
  <div id="intermediary-records-container" class="space-y-2 max-h-64 overflow-y-auto pr-1">
    <div class="p-3 bg-surface-container-low rounded-lg border border-outline-variant text-xs text-on-surface-variant">Loading SQLite database cases...</div>
  </div>
</div>"""
html = html.replace(old_csc_toolkit, new_csc_toolkit)

# 11. Inject Modals and app.js before </body>
modals_and_script = """
<!-- KCC Calculator Modal -->
<div id="kcc-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
  <div class="bg-surface-container-lowest max-w-lg w-full rounded-2xl border-2 border-secondary p-6 shadow-2xl space-y-4 animate-fade-in">
    <div class="flex items-center justify-between pb-3 border-b border-outline-variant">
      <div class="flex items-center gap-2">
        <span class="material-symbols-outlined text-secondary text-2xl">credit_card</span>
        <h3 class="text-headline-sm font-headline-sm text-on-surface">KCC Loan Scale Calculator</h3>
      </div>
      <button id="kcc-modal-close" class="text-on-surface-variant hover:text-on-surface text-xl">✕</button>
    </div>
    <form id="kcc-calc-form" class="space-y-3">
      <div>
        <label class="block text-xs font-bold text-on-surface mb-1">Crop</label>
        <select id="kcc-crop-select" class="w-full bg-surface border border-outline-variant rounded-lg p-2.5 text-sm">
          <option value="Paddy">Paddy (₹42,000 / Acre)</option>
          <option value="Cotton">Cotton (₹45,000 / Acre)</option>
          <option value="Chilli">Chilli (₹65,000 / Acre)</option>
          <option value="Maize">Maize (₹28,000 / Acre)</option>
          <option value="Bengal Gram">Bengal Gram (₹24,000 / Acre)</option>
          <option value="Groundnut">Groundnut (₹30,000 / Acre)</option>
        </select>
      </div>
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-bold text-on-surface mb-1">Land (Acres)</label>
          <input id="kcc-acres-input" type="number" step="0.5" value="2.5" min="0.5" class="w-full bg-surface border border-outline-variant rounded-lg p-2.5 text-sm" />
        </div>
        <div>
          <label class="block text-xs font-bold text-on-surface mb-1">Existing Debt (₹)</label>
          <input id="kcc-debt-input" type="number" step="1000" value="0" min="0" class="w-full bg-surface border border-outline-variant rounded-lg p-2.5 text-sm" />
        </div>
      </div>
      <button type="submit" class="w-full bg-secondary hover:bg-secondary/90 text-on-secondary py-2.5 rounded-lg font-bold text-sm transition-colors">
        Compute Statutory Credit Limit
      </button>
    </form>
    <div id="kcc-calc-result" class="hidden"></div>
  </div>
</div>

<!-- 72-Hour Emergency Loss Claim Modal -->
<div id="claim-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
  <div class="bg-surface-container-lowest max-w-lg w-full rounded-2xl border-2 border-error p-6 shadow-2xl space-y-4 animate-fade-in">
    <div class="flex items-center justify-between pb-3 border-b border-outline-variant">
      <div class="flex items-center gap-2">
        <span class="material-symbols-outlined text-error text-2xl">emergency</span>
        <div>
          <h3 class="text-headline-sm font-headline-sm text-on-surface">72-Hour Statutory Claim Intimation</h3>
          <span class="text-[11px] text-error font-bold font-mono">PMFBY Section 19(4) Filing</span>
        </div>
      </div>
      <button id="claim-modal-close" class="text-on-surface-variant hover:text-on-surface text-xl">✕</button>
    </div>
    <form id="claim-dispatch-form" class="space-y-3 text-xs">
      <div class="grid grid-cols-2 gap-2">
        <div>
          <label class="block font-bold mb-1">Farmer Name</label>
          <input id="claim-farmer-name" type="text" class="w-full bg-surface border border-outline-variant rounded p-2" value="Ravi Kumar" required />
        </div>
        <div>
          <label class="block font-bold mb-1">Phone Number</label>
          <input id="claim-phone" type="text" class="w-full bg-surface border border-outline-variant rounded p-2" value="9876543210" required />
        </div>
      </div>
      <div class="grid grid-cols-3 gap-2">
        <div>
          <label class="block font-bold mb-1">State</label>
          <input id="claim-state" type="text" class="w-full bg-surface border border-outline-variant rounded p-2" value="Telangana" required />
        </div>
        <div>
          <label class="block font-bold mb-1">District</label>
          <input id="claim-district" type="text" class="w-full bg-surface border border-outline-variant rounded p-2" value="Warangal" required />
        </div>
        <div>
          <label class="block font-bold mb-1">Village</label>
          <input id="claim-village" type="text" class="w-full bg-surface border border-outline-variant rounded p-2" value="Geesugonda" required />
        </div>
      </div>
      <div class="grid grid-cols-3 gap-2">
        <div>
          <label class="block font-bold mb-1">Survey No</label>
          <input id="claim-survey" type="text" class="w-full bg-surface border border-outline-variant rounded p-2" value="402/A" required />
        </div>
        <div>
          <label class="block font-bold mb-1">Calamity Type</label>
          <select id="claim-cause" class="w-full bg-surface border border-outline-variant rounded p-2">
            <option value="Hailstorm">Hailstorm</option>
            <option value="Inundation">Inundation / Flood</option>
            <option value="Pest Lodging">Pest Lodging</option>
            <option value="Cyclonic Rain">Cyclonic Rain</option>
            <option value="Drought">Drought</option>
          </select>
        </div>
        <div>
          <label class="block font-bold mb-1">Loss (%)</label>
          <input id="claim-loss-pct" type="number" min="10" max="100" value="75" class="w-full bg-surface border border-outline-variant rounded p-2" required />
        </div>
      </div>
      <div>
        <label class="block font-bold mb-1">Field Assessment Notes</label>
        <input id="claim-notes" type="text" class="w-full bg-surface border border-outline-variant rounded p-2" value="Waterlogging with lodged crop canopy. 3 geo-tagged photos ready." />
      </div>
      <button id="claim-submit-btn" type="submit" class="w-full bg-error hover:bg-error/90 text-on-error py-2.5 rounded-lg font-bold text-sm flex items-center justify-center gap-1.5 transition-colors">
        <span class="material-symbols-outlined text-base">send_and_archive</span>
        <span>Submit Official Intimation &amp; Generate Docket</span>
      </button>
    </form>
    <div id="claim-dispatch-result" class="hidden"></div>
  </div>
</div>

<script src="app.js"></script>
"""

html = html.replace('</body></html>', modals_and_script + '\n</body></html>')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('frontend/index.html generated successfully!')
