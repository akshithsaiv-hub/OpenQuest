import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_html_path = os.path.join(base_dir, "frontend", "index.html")

with open(index_html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Header Language Selector to all 11 Indian Languages
old_lang_select = """        <select id="langSelect" class="lang-select" aria-label="Choose Language">
          <option value="en">English (Default)</option>
          <option value="te">తెలుగు (Telugu)</option>
          <option value="hi">हिंदी (Hindi)</option>
          <option value="mr">मराठी (Marathi)</option>
          <option value="ta">தமிழ் (Tamil)</option>
          <option value="kn">ಕನ್ನಡ (Kannada)</option>
        </select>"""

new_lang_select = """        <select id="langSelect" class="lang-select" aria-label="Choose Language">
          <option value="en">🌐 English (Default)</option>
          <option value="te">🌾 తెలుగు (Telugu)</option>
          <option value="hi">🇮🇳 हिंदी (Hindi)</option>
          <option value="mr">🌻 मराठी (Marathi)</option>
          <option value="ta">🏛️ தமிழ் (Tamil)</option>
          <option value="kn">🌿 ಕನ್ನಡ (Kannada)</option>
          <option value="bn">🌾 বাংলা (Bengali)</option>
          <option value="gu">🪷 ગુજરાતી (Gujarati)</option>
          <option value="ml">🌴 മലയാളം (Malayalam)</option>
          <option value="pa">🌾 ਪੰਜਾਬੀ (Punjabi)</option>
          <option value="or">🌊 ଓଡ଼ିଆ (Odia)</option>
        </select>"""

if old_lang_select in html:
    html = html.replace(old_lang_select, new_lang_select)
    print("Header language selector updated with all 11 languages!")

# 2. Update Tab 5 header with data-i18n
old_wallet_header = """    <div class="view-header">
      <h2 class="view-title"><span>📁</span> Consent-Driven Farmer Document Wallet & DigiLocker</h2>
      <p class="view-desc">
        Store scanned land records (Pahani/Dharani), Aadhaar, Bank Passbooks, and CCRC agreements with explicit farmer consent. Integrated with DigiLocker and AgriStack Farmer ID metadata.
      </p>
    </div>"""

new_wallet_header = """    <div class="view-header">
      <h2 class="view-title"><span>📁</span> <span data-i18n="doc_wallet_title">Consent-Driven Farmer Document Wallet & DigiLocker</span></h2>
      <p class="view-desc" data-i18n="doc_wallet_desc">
        Store scanned land records (Pahani/Dharani), Aadhaar, Bank Passbooks, and CCRC agreements with explicit farmer consent. Download official sample templates below.
      </p>
    </div>"""

if old_wallet_header in html:
    html = html.replace(old_wallet_header, new_wallet_header)
    print("Tab 5 Document Wallet header updated with data-i18n!")

with open(index_html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("index.html enhancements completed!")
