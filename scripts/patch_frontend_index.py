import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_html_path = os.path.join(base_dir, "frontend", "index.html")

with open(index_html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Navigation Tabs to have data-i18n tags on their text labels
old_nav_tabs = """    <div class="main-nav-container" id="mainNavContainer" role="tablist">
      <button class="nav-tab-btn active" role="tab" aria-selected="true" data-tab="tab0" id="btn-tab0">
        <span class="nav-tab-icon">📜</span>
        <span>Scheme Browser</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab1" id="btn-tab1">
        <span class="nav-tab-icon">🤖</span>
        <span>Eligibility & Chat</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab2" id="btn-tab2">
        <span class="nav-tab-icon">⚡</span>
        <span>72-Hr Claim Shield</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab3" id="btn-tab3">
        <span class="nav-tab-icon">💧</span>
        <span>Water Subsidies & Crops</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab4" id="btn-tab4">
        <span class="nav-tab-icon">💳</span>
        <span>KCC Loan & Tracker</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab5" id="btn-tab5">
        <span class="nav-tab-icon">📁</span>
        <span>Document Wallet</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab6" id="btn-tab6">
        <span class="nav-tab-icon">📈</span>
        <span>MSP vs Mandi</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab7" id="btn-tab7">
        <span class="nav-tab-icon">🏛️</span>
        <span>Intermediary & Escalation</span>
      </button>
    </div>"""

new_nav_tabs = """    <div class="main-nav-container" id="mainNavContainer" role="tablist">
      <button class="nav-tab-btn active" role="tab" aria-selected="true" data-tab="tab0" id="btn-tab0">
        <span class="nav-tab-icon">📜</span>
        <span data-i18n="nav_tab0">Scheme Browser</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab1" id="btn-tab1">
        <span class="nav-tab-icon">🤖</span>
        <span data-i18n="nav_tab1">Eligibility & Voice AI</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab2" id="btn-tab2">
        <span class="nav-tab-icon">⚡</span>
        <span data-i18n="nav_tab2">72-Hr Claim Shield</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab3" id="btn-tab3">
        <span class="nav-tab-icon">💧</span>
        <span data-i18n="nav_tab3">Water Subsidies & Crops</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab4" id="btn-tab4">
        <span class="nav-tab-icon">💳</span>
        <span data-i18n="nav_tab4">KCC Loan & Tracker</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab5" id="btn-tab5">
        <span class="nav-tab-icon">📁</span>
        <span data-i18n="nav_tab5">Document Wallet</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab6" id="btn-tab6">
        <span class="nav-tab-icon">📈</span>
        <span data-i18n="nav_tab6">MSP vs Mandi</span>
      </button>
      <button class="nav-tab-btn" role="tab" aria-selected="false" data-tab="tab7" id="btn-tab7">
        <span class="nav-tab-icon">🏛️</span>
        <span data-i18n="nav_tab7">Intermediary & Escalation</span>
      </button>
    </div>"""

if old_nav_tabs in html:
    html = html.replace(old_nav_tabs, new_nav_tabs)
    print("Nav tabs updated with data-i18n!")

# 2. Update Tab 1 (Eligibility & Chat) to add the Multilingual AI Voice Assistant
old_tab1_start = """  <!-- TAB 1: ELIGIBILITY & CHAT -->
  <div id="view-tab1" class="tab-view" role="tabpanel" aria-labelledby="btn-tab1">
    <div class="view-header">
      <h2 class="view-title"><span>🤖</span> Farmer Self-Service Chat & Eligibility Engine</h2>
      <p class="view-desc">
        100% Deterministic evaluation with zero hallucinations. Checks your land holding, tenancy (CCRC), crop, and irrigation source against statutory Central and State eligibility rules.
      </p>
    </div>

    <div class="content-grid-2">
      <!-- Profile Form -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title"><span>🌾</span> Enter Farmer Profile</h3>
          <p class="card-subtitle">Fill in your land and crop details to compute eligible subsidies.</p>
        </div>"""

new_tab1_start = """  <!-- TAB 1: ELIGIBILITY & MULTILINGUAL VOICE ASSISTANT -->
  <div id="view-tab1" class="tab-view" role="tabpanel" aria-labelledby="btn-tab1">
    <div class="view-header">
      <h2 class="view-title"><span>🎙️</span> <span data-i18n="tab1_title">Farmer Self-Service Chat & Multilingual Voice AI Assistant</span></h2>
      <p class="view-desc" data-i18n="tab1_desc">
        Speak or ask questions in any major Indian language. 100% Deterministic scheme evaluation with zero hallucinations. Checks your land holding, tenancy (CCRC), crop, and irrigation source against statutory Central and State eligibility rules.
      </p>
    </div>

    <div class="content-grid-2">
      <!-- Profile Form -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title"><span>🌾</span> <span data-i18n="enter_profile_title">Enter Farmer Profile</span></h3>
          <p class="card-subtitle" data-i18n="enter_profile_subtitle">Fill in your land and crop details to compute eligible subsidies.</p>
        </div>"""

if old_tab1_start in html:
    html = html.replace(old_tab1_start, new_tab1_start)
    print("Tab 1 header updated!")

# Now inject the Multilingual Voice Assistant card right next to the Profile Form in Tab 1
voice_card_html = """
      <!-- Multilingual AI Voice Assistant Console -->
      <div class="voice-assistant-card card">
        <div class="card-header" style="border-bottom: 1px solid #bbf7d0; padding-bottom: 0.75rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
            <div>
              <h3 class="card-title" style="color: #15803d; font-size: 1.15rem;">
                <span>🎙️</span> <span data-i18n="voice_title">Multilingual AI Voice Assistant</span>
              </h3>
              <p class="card-subtitle" style="margin-top: 0.2rem; font-size: 0.8rem; color: #166534;" data-i18n="voice_subtitle">
                Understands & responds in any major Indian language with voice speech.
              </p>
            </div>
            <!-- Language Selector Dropdown for Voice -->
            <div style="display: flex; align-items: center; gap: 0.35rem; background: #ffffff; padding: 4px 8px; border-radius: 8px; border: 1px solid #86efac;">
              <span style="font-size: 0.9rem;">🌐</span>
              <select id="voiceLangSelect" style="border: none; background: transparent; font-size: 0.82rem; font-weight: 700; color: #166534; cursor: pointer; outline: none;">
                <option value="auto">🌐 Auto Detect Language</option>
                <option value="te-IN">🌾 Telugu (తెలుగు)</option>
                <option value="hi-IN">🇮🇳 Hindi (हिन्दी)</option>
                <option value="ta-IN">🏛️ Tamil (தமிழ்)</option>
                <option value="kn-IN">🌿 Kannada (ಕನ್ನಡ)</option>
                <option value="mr-IN">🌻 Marathi (मराठी)</option>
                <option value="bn-IN">🌾 Bengali (বাংলা)</option>
                <option value="gu-IN">🪷 Gujarati (ગુજરાતી)</option>
                <option value="ml-IN">🌴 Malayalam (മലയാളം)</option>
                <option value="pa-IN">🌾 Punjabi (ਪੰਜਾਬੀ)</option>
                <option value="or-IN">🌊 Odia (ଓଡ଼ିଆ)</option>
                <option value="en-IN">🌐 English (India)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Voice Microphone Interaction Center -->
        <div class="voice-mic-container">
          <button type="button" id="voiceMicBtn" class="voice-mic-btn" title="Click to Speak in your language" aria-label="Microphone">
            <span>🎙️</span>
          </button>
          <div id="voiceStatusText" class="voice-status-text" data-i18n="voice_click_speak">Click microphone to speak...</div>
        </div>

        <!-- Text or Speech Input Row -->
        <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
          <input type="text" id="voiceTranscriptInput" class="form-input" style="flex: 1; font-size: 0.88rem;" placeholder="Ask question or click microphone..." data-i18n-placeholder="voice_placeholder" />
          <button type="button" id="voiceSendBtn" class="btn btn-primary" style="padding: 0.5rem 1rem;">
            <span>➤</span> <span data-i18n="voice_send_btn">Send</span>
          </button>
        </div>

        <!-- Quick Prompt Chips -->
        <div class="voice-chips-container">
          <button type="button" class="voice-chip" onclick="askQuickVoicePrompt('Drip irrigation subsidy rules')">💧 Drip Subsidy 100%</button>
          <button type="button" class="voice-chip" onclick="askQuickVoicePrompt('KCC loan 4% interest rate')">🏦 KCC 4% Interest</button>
          <button type="button" class="voice-chip" onclick="askQuickVoicePrompt('72-hour crop loss insurance claim')">⚡ 72-Hr Loss Claim</button>
          <button type="button" class="voice-chip" onclick="askQuickVoicePrompt('Tenant farmer CCRC card rights')">🤝 Tenant CCRC Rights</button>
          <button type="button" class="voice-chip" onclick="askQuickVoicePrompt('PM-KISAN installment status')">🌾 PM-KISAN ₹6,000</button>
        </div>

        <!-- Chat & Voice History -->
        <div id="voiceChatHistory" class="voice-chat-history">
          <div class="voice-bubble voice-bubble-bot">
            <div style="font-weight: 700; color: #15803d; font-size: 0.82rem; margin-bottom: 0.2rem;">
              🌾 OpenQuest Voice Assistant • సిద్ధంగా ఉంది / तैयार है
            </div>
            <div style="font-size: 0.85rem; color: #374151;">
              నమస్కారం! మీరు తెలుగు, హిందీ, తమిళం, కన్నడ లేదా మరేదైనా భారతీయ భాషలో మాట్లాడి సబ్సిడీలు, KCC రుణాలు లేదా 72 గంటల పంట నష్ట పరిహారం గురించి అడగవచ్చు. మాట్లాడటానికి పైన ఉన్న మైక్ బటన్ క్లిక్ చేయండి!
            </div>
          </div>
        </div>
      </div>
"""

old_tab1_results = """      <!-- Results Display -->
      <div id="eligibilityResultsContainer">"""

new_tab1_results = voice_card_html + """
    </div>

    <!-- Full-Width Eligibility Matching Results Container -->
    <div id="eligibilityResultsContainer" style="margin-top: 1.5rem;">"""

# In the current HTML, resultsContainer was inside content-grid-2
if old_tab1_results in html:
    html = html.replace(old_tab1_results, new_tab1_results)
    # also close the extra div if needed
    print("Voice Assistant Card injected into Tab 1!")

# 3. Update Document Wallet (Tab 5) to include sample previews and download buttons
old_tab5_grid = """    <!-- Document Cards Grid -->
    <div class="schemes-grid" id="docWalletGrid">
      <!-- Card 1 -->
      <div class="scheme-card" style="border-left: 4px solid #16a34a;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <span class="badge-tag badge-tag-green">DigiLocker Verified</span>
            <h3 style="margin: 0.35rem 0; font-size: 1.15rem;">Aadhaar Identity Card</h3>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin:0;">UIDAI Masked ID</p>
          </div>
          <span style="font-size: 1.8rem;">🪪</span>
        </div>
        <div style="background: #f8fafc; padding: 0.75rem; border-radius: 6px; margin: 0.85rem 0; font-family: monospace; font-size: 0.95rem;">
          XXXX - XXXX - 4921
        </div>
        <div style="font-size: 0.82rem; color: var(--text-muted);">
          Verified Name: <strong>Komirelli Ramulu</strong> • Status: <strong>NPCI DBT Seeded</strong>
        </div>
      </div>

      <!-- Card 2 -->
      <div class="scheme-card" style="border-left: 4px solid #2563eb;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <span class="badge-tag badge-tag-blue">Revenue Record Verified</span>
            <h3 style="margin: 0.35rem 0; font-size: 1.15rem;">Land Title / Pahani / Dharani</h3>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin:0;">Record of Rights (RoR-1B)</p>
          </div>
          <span style="font-size: 1.8rem;">📜</span>
        </div>
        <div style="background: #f8fafc; padding: 0.75rem; border-radius: 6px; margin: 0.85rem 0; font-size: 0.88rem;">
          <strong>Survey No:</strong> 284/B • <strong>Extent:</strong> 2 Acres 20 Guntas • <strong>Village:</strong> Geesugonda
        </div>
        <div style="font-size: 0.82rem; color: var(--text-muted);">
          Passbook No: <strong>T28090041284</strong> • Cultivator: <strong>Self / Pattadar</strong>
        </div>
      </div>

      <!-- Card 3 -->
      <div class="scheme-card" style="border-left: 4px solid #f59e0b;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <span class="badge-tag badge-tag-amber">Statutory Agreement</span>
            <h3 style="margin: 0.35rem 0; font-size: 1.15rem;">Crop Cultivator Rights Card (CCRC)</h3>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin:0;">Tenant Cultivator Legal Card</p>
          </div>
          <span style="font-size: 1.8rem;">🤝</span>
        </div>
        <div style="background: #f8fafc; padding: 0.75rem; border-radius: 6px; margin: 0.85rem 0; font-size: 0.88rem;">
          <strong>Card ID:</strong> CCRC-TS-2026-9912 • <strong>Validity:</strong> Rabi 2025-26
        </div>
        <div style="font-size: 0.82rem; color: var(--text-muted);">
          Gives full legal PMFBY & Rythu Bharosa access without affecting owner title.
        </div>
      </div>

      <!-- Card 4 -->
      <div class="scheme-card" style="border-left: 4px solid #8b5cf6;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <span class="badge-tag badge-tag-blue">Bank Verified</span>
            <h3 style="margin: 0.35rem 0; font-size: 1.15rem;">Bank Passbook / DBT Mandate</h3>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin:0;">State Bank of India</p>
          </div>
          <span style="font-size: 1.8rem;">🏦</span>
        </div>
        <div style="background: #f8fafc; padding: 0.75rem; border-radius: 6px; margin: 0.85rem 0; font-size: 0.88rem;">
          <strong>A/C:</strong> ******3492 • <strong>IFSC:</strong> SBIN0020144 • <strong>Branch:</strong> Warangal Main
        </div>
        <div style="font-size: 0.82rem; color: var(--text-muted);">
          Aadhaar Authentication: <strong>Active (Aadhaar Enabled Payment System ready)</strong>
        </div>
      </div>
    </div>"""

new_tab5_grid = """    <!-- Document Cards Grid with Photos & Direct Sample Downloads -->
    <div class="schemes-grid" id="docWalletGrid">
      <!-- Card 1: Aadhaar -->
      <div class="scheme-card" style="border-left: 4px solid #16a34a;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <span class="badge-tag badge-tag-green">DigiLocker Verified</span>
            <h3 style="margin: 0.35rem 0; font-size: 1.15rem;">Aadhaar Identity Card</h3>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin:0;">UIDAI Masked ID • Official Template</p>
          </div>
          <span style="font-size: 1.8rem;">🪪</span>
        </div>
        
        <!-- Thumbnail Sample Preview -->
        <div class="doc-thumbnail-wrap" onclick="openDocPreviewModal('aadhaar', 'Sample Masked Aadhaar Card', 'samples/sample_aadhaar.svg')">
          <img src="samples/sample_aadhaar.svg" alt="Sample Aadhaar Preview" class="doc-sample-img" />
          <span class="doc-badge-overlay">👁️ Click to Inspect</span>
        </div>

        <div style="background: #f8fafc; padding: 0.5rem 0.75rem; border-radius: 6px; margin: 0.5rem 0; font-family: monospace; font-size: 0.95rem;">
          XXXX - XXXX - 4921
        </div>
        <div style="font-size: 0.82rem; color: var(--text-muted);">
          Verified Name: <strong>Komirelli Ramulu</strong> • Status: <strong>NPCI DBT Seeded</strong>
        </div>

        <!-- Download & Full Preview Actions -->
        <div class="doc-actions-row">
          <a href="/api/documents/download/aadhaar" download="Sample_Aadhaar_Card_Masked.svg" class="doc-download-btn">
            <span>📥</span> <span data-i18n="download_sample_btn">Download Sample Copy</span>
          </a>
          <button type="button" class="btn btn-secondary doc-preview-btn" onclick="openDocPreviewModal('aadhaar', 'Sample Masked Aadhaar Card', 'samples/sample_aadhaar.svg')">
            <span>👁️</span> <span data-i18n="preview_sample_btn">Preview</span>
          </button>
        </div>
      </div>

      <!-- Card 2: Pahani / Land Record -->
      <div class="scheme-card" style="border-left: 4px solid #2563eb;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <span class="badge-tag badge-tag-blue">Revenue Record Verified</span>
            <h3 style="margin: 0.35rem 0; font-size: 1.15rem;">Land Title / Pahani / Dharani</h3>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin:0;">Record of Rights (RoR-1B) Template</p>
          </div>
          <span style="font-size: 1.8rem;">📜</span>
        </div>

        <!-- Thumbnail Sample Preview -->
        <div class="doc-thumbnail-wrap" onclick="openDocPreviewModal('pahani', 'Sample Pahani / Dharani Land Record (RoR-1B)', 'samples/sample_pahani.svg')">
          <img src="samples/sample_pahani.svg" alt="Sample Pahani Preview" class="doc-sample-img" />
          <span class="doc-badge-overlay">👁️ Click to Inspect</span>
        </div>

        <div style="background: #f8fafc; padding: 0.5rem 0.75rem; border-radius: 6px; margin: 0.5rem 0; font-size: 0.88rem;">
          <strong>Survey No:</strong> 284/B • <strong>Extent:</strong> 2 Acres 20 Guntas • <strong>Village:</strong> Geesugonda
        </div>
        <div style="font-size: 0.82rem; color: var(--text-muted);">
          Passbook No: <strong>T28090041284</strong> • Cultivator: <strong>Self / Pattadar</strong>
        </div>

        <!-- Download & Full Preview Actions -->
        <div class="doc-actions-row">
          <a href="/api/documents/download/pahani" download="Sample_Pahani_Land_Record_RoR1B.svg" class="doc-download-btn">
            <span>📥</span> <span data-i18n="download_sample_btn">Download Sample Copy</span>
          </a>
          <button type="button" class="btn btn-secondary doc-preview-btn" onclick="openDocPreviewModal('pahani', 'Sample Pahani / Dharani Land Record (RoR-1B)', 'samples/sample_pahani.svg')">
            <span>👁️</span> <span data-i18n="preview_sample_btn">Preview</span>
          </button>
        </div>
      </div>

      <!-- Card 3: CCRC Tenancy Card -->
      <div class="scheme-card" style="border-left: 4px solid #f59e0b;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <span class="badge-tag badge-tag-amber">Statutory Agreement</span>
            <h3 style="margin: 0.35rem 0; font-size: 1.15rem;">Crop Cultivator Rights Card (CCRC)</h3>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin:0;">Tenant Cultivator Legal Card Template</p>
          </div>
          <span style="font-size: 1.8rem;">🤝</span>
        </div>

        <!-- Thumbnail Sample Preview -->
        <div class="doc-thumbnail-wrap" onclick="openDocPreviewModal('ccrc', 'Sample Crop Cultivator Rights Card (CCRC)', 'samples/sample_ccrc.svg')">
          <img src="samples/sample_ccrc.svg" alt="Sample CCRC Preview" class="doc-sample-img" />
          <span class="doc-badge-overlay">👁️ Click to Inspect</span>
        </div>

        <div style="background: #f8fafc; padding: 0.5rem 0.75rem; border-radius: 6px; margin: 0.5rem 0; font-size: 0.88rem;">
          <strong>Card ID:</strong> CCRC-TS-2026-9912 • <strong>Validity:</strong> Rabi 2025-26
        </div>
        <div style="font-size: 0.82rem; color: var(--text-muted);">
          Gives full legal PMFBY &amp; Rythu Bharosa access without affecting owner title.
        </div>

        <!-- Download & Full Preview Actions -->
        <div class="doc-actions-row">
          <a href="/api/documents/download/ccrc" download="Sample_CCRC_Tenant_Card.svg" class="doc-download-btn">
            <span>📥</span> <span data-i18n="download_sample_btn">Download Sample Copy</span>
          </a>
          <button type="button" class="btn btn-secondary doc-preview-btn" onclick="openDocPreviewModal('ccrc', 'Sample Crop Cultivator Rights Card (CCRC)', 'samples/sample_ccrc.svg')">
            <span>👁️</span> <span data-i18n="preview_sample_btn">Preview</span>
          </button>
        </div>
      </div>

      <!-- Card 4: Bank Passbook -->
      <div class="scheme-card" style="border-left: 4px solid #8b5cf6;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <span class="badge-tag badge-tag-blue">Bank Verified</span>
            <h3 style="margin: 0.35rem 0; font-size: 1.15rem;">Bank Passbook / DBT Mandate</h3>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin:0;">State Bank of India • Official Template</p>
          </div>
          <span style="font-size: 1.8rem;">🏦</span>
        </div>

        <!-- Thumbnail Sample Preview -->
        <div class="doc-thumbnail-wrap" onclick="openDocPreviewModal('passbook', 'Sample Bank Passbook (DBT & NPCI Active)', 'samples/sample_passbook.svg')">
          <img src="samples/sample_passbook.svg" alt="Sample Passbook Preview" class="doc-sample-img" />
          <span class="doc-badge-overlay">👁️ Click to Inspect</span>
        </div>

        <div style="background: #f8fafc; padding: 0.5rem 0.75rem; border-radius: 6px; margin: 0.5rem 0; font-size: 0.88rem;">
          <strong>A/C:</strong> ******3492 • <strong>IFSC:</strong> SBIN0020144 • <strong>Branch:</strong> Warangal Main
        </div>
        <div style="font-size: 0.82rem; color: var(--text-muted);">
          Aadhaar Authentication: <strong>Active (Aadhaar Enabled Payment System ready)</strong>
        </div>

        <!-- Download & Full Preview Actions -->
        <div class="doc-actions-row">
          <a href="/api/documents/download/passbook" download="Sample_Bank_Passbook_DBT_Active.svg" class="doc-download-btn">
            <span>📥</span> <span data-i18n="download_sample_btn">Download Sample Copy</span>
          </a>
          <button type="button" class="btn btn-secondary doc-preview-btn" onclick="openDocPreviewModal('passbook', 'Sample Bank Passbook (DBT & NPCI Active)', 'samples/sample_passbook.svg')">
            <span>👁️</span> <span data-i18n="preview_sample_btn">Preview</span>
          </button>
        </div>
      </div>
    </div>"""

if old_tab5_grid in html:
    html = html.replace(old_tab5_grid, new_tab5_grid)
    print("Tab 5 Document Wallet grid updated with sample previews and downloads!")

# 4. Inject Document Preview Modal before </body>
preview_modal_html = """
  <!-- Sample Document Full-Size Preview Modal -->
  <div id="sampleDocModal" class="modal-backdrop" style="display: none;" role="dialog" aria-modal="true" aria-labelledby="sampleDocModalTitle">
    <div class="modal-dialog" style="max-width: 700px; width: 95%;">
      <div class="modal-header">
        <div>
          <span class="badge-tag badge-tag-green">Official Verification Template</span>
          <h3 id="sampleDocModalTitle" class="modal-title" style="margin-top: 0.25rem;">Sample Document Preview</h3>
        </div>
        <button type="button" class="modal-close-btn" onclick="closeDocPreviewModal()" aria-label="Close modal">✕</button>
      </div>
      <div class="modal-body" style="text-align: center; padding: 1rem;">
        <div style="max-height: 480px; overflow-y: auto; border: 1px solid #cbd5e1; border-radius: 8px; background: #f8fafc; padding: 0.5rem;">
          <img id="sampleDocModalImg" src="" alt="Document Preview" style="width: 100%; height: auto; display: block; border-radius: 4px;" />
        </div>
      </div>
      <div class="modal-footer" style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1.25rem; border-top: 1px solid #e5e7eb;">
        <span style="font-size: 0.8rem; color: var(--text-muted);">Format: High-Definition Official Vector (SVG)</span>
        <div style="display: flex; gap: 0.5rem;">
          <a id="sampleDocModalDownloadLink" href="" download="" class="btn btn-primary" style="font-size: 0.85rem; padding: 0.5rem 1rem;">
            <span>📥</span> Download Sample Copy
          </a>
          <button type="button" class="btn btn-secondary" onclick="closeDocPreviewModal()" style="font-size: 0.85rem; padding: 0.5rem 1rem;">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
"""

if "id=\"sampleDocModal\"" not in html:
    html = html.replace("</body>", preview_modal_html + "\n</body>")
    print("Sample Document Modal added before </body>!")

with open(index_html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("frontend/index.html patched successfully!")
