/**
 * OpenQuest - Civic Agritech Client Integration Script
 * Connects Stitch UI with FastAPI Backend & SQLite Database.
 */

// Global State
const API_BASE = "";

// Document Ready
document.addEventListener("DOMContentLoaded", () => {
  initCountdownTimer();
  initLanguageSelector();
  initEligibilityMatcher();
  initQueryAI();
  initNameMatcher();
  initKCCCalculator();
  initClaimDispatcher();
  initIntermediaryPortal();
  loadMspComparison();
});

// 1. Live Countdown Timer (72-Hour PMFBY Statutory Window)
function initCountdownTimer() {
  let secondsLeft = 48 * 3600 + 12 * 60 + 30;
  const timerElement = document.getElementById("countdown-timer");
  if (!timerElement) return;

  setInterval(() => {
    if (secondsLeft > 0) {
      secondsLeft--;
      const hours = Math.floor(secondsLeft / 3600);
      const mins = Math.floor((secondsLeft % 3600) / 60);
      const secs = secondsLeft % 60;
      timerElement.textContent = `${hours}h ${mins.toString().padStart(2, "0")}m ${secs.toString().padStart(2, "0")}s`;
    }
  }, 1000);
}

// 2. Multilingual Translations Dictionary
const I18N_STRINGS = {
  en: {
    heroTitle: "Empowering Indian Farmers with Instant Subsidy & Loss Claim Intelligence",
    heroDesc: "Pan-India Central & State Schemes • 72-Hour Statutory PMFBY Claim Countdown • AgriStack & DigiLocker Ready • Offline & SMS Capable.",
    matcherTitle: "Interactive Eligibility Matcher",
    checkBtn: "Check Matched Schemes Instantly",
    emergencyBtn: "Dispatch Emergency Loss Intimation Now",
    mandiTitle: "Interactive Live MSP vs APMC Mandi Benchmark",
    operatorTitle: "Village Facilitator Operational Toolkit",
  },
  te: {
    heroTitle: "రైతులకు తక్షణ రాయితీలు & పంట నష్ట పరిహార సమాచారం అందించే వేదిక",
    heroDesc: "అన్ని రాష్ట్రాల & కేంద్ర పథకాలు • 72 గంటల PMFBY నష్ట నివేదిక కౌంట్‌డౌన్ • అగ్రిస్టాక్ & డిజిలాకర్ అనుసంధానం • ఆఫ్‌లైన్ & SMS మోడ్.",
    matcherTitle: "అర్హత పథకాల తనిఖీ యంత్రం",
    checkBtn: "అర్హత ఉన్న పథకాలను ఇప్పుడే చూడండి",
    emergencyBtn: "72 గంటల నష్ట నివేదికను పంపండి",
    mandiTitle: "ప్రత్యక్ష మద్దతు ధర (MSP) vs మార్కెట్ ధరల విశ్లేషణ",
    operatorTitle: "గ్రామ స్థాయి ఆపరేటర్ / CSC డాష్‌బోర్డ్",
  },
  hi: {
    heroTitle: "भारतीय किसानों के लिए तत्काल सब्सिडी और फसल क्षति दावा मंच",
    heroDesc: "अखिल भारतीय केंद्रीय एवं राज्य योजनाएं • 72 घंटे की पीएमएफबीवाई क्षति सूचना • एग्रीस्टैक एवं डिजिलॉकर एकीकृत • ऑफलाइन एवं एसएमएस सक्षम।",
    matcherTitle: "इंटरएक्टिव पात्रता मिलानकर्ता",
    checkBtn: "तत्काल पात्र योजनाओं की जांच करें",
    emergencyBtn: "72 घंटे की आपातकालीन फसल हानि दर्ज करें",
    mandiTitle: "लाइव एमएसपी बनाम मंडी मूल्य तुलना",
    operatorTitle: "ग्राम सुविधा प्रदाता एवं सीएससी ऑपरेटर डेस्क",
  },
  mr: {
    heroTitle: "शेतकऱ्यांसाठी त्वरित अनुदान व पीक विमा नुकसान भरपाई सहाय्यक",
    heroDesc: "सर्व राज्य व केंद्र योजना • ७२ तासांत पीक नुकसान सूचना • ॲग्रीस्टॅक व डिजी-लॉकर सक्षम • ऑफलाइन एसएमएस मोड.",
    matcherTitle: "पात्रता तपासणी यंत्र",
    checkBtn: "पात्र योजनांची त्वरित तपासणी करा",
    emergencyBtn: "७२ तासांत पीक नुकसान सूचना पाठवा",
    mandiTitle: "थेट हमीभाव (MSP) वि. बाजार समिती दर",
    operatorTitle: "ग्रामस्तरीय ऑपरेटर व सीएससी डेस्क",
  },
  ta: {
    heroTitle: "விவசாயிகளுக்கான உடனடி மானியம் மற்றும் பயிர் இழப்பீடு தகவல் தளம்",
    heroDesc: "அனைத்து மாநில மற்றும் மத்திய திட்டங்கள் • 72 மணி நேர PMFBY இழப்பீட்டு அறிக்கை • அக்ரிஸ்டாக் & டிஜிலாக்கர் இணைப்பு.",
    matcherTitle: "திட்ட தகுதி சரிபார்ப்பு",
    checkBtn: "தகுதியான திட்டங்களை பார்க்கவும்",
    emergencyBtn: "72 மணி நேர அவசர இழப்பீட்டு அறிக்கை அனுப்பவும்",
    mandiTitle: "நேரடி குறைந்தபட்ச ஆதரவு விலை vs மண்டி விலை",
    operatorTitle: "கிராம சேவை மைய ஆபரேட்டர் தளம்",
  }
};

function initLanguageSelector() {
  const langSelect = document.getElementById("lang-select-box");
  if (!langSelect) return;

  langSelect.addEventListener("change", (e) => {
    const lang = e.target.value;
    const trans = I18N_STRINGS[lang] || I18N_STRINGS.en;

    const heroTitle = document.getElementById("hero-main-title");
    if (heroTitle) heroTitle.textContent = trans.heroTitle;

    const heroDesc = document.getElementById("hero-main-desc");
    if (heroDesc) heroDesc.textContent = trans.heroDesc;

    const matcherBtn = document.getElementById("matcher-submit-btn");
    if (matcherBtn) {
      const span = matcherBtn.querySelector("span:last-child");
      if (span) span.textContent = trans.checkBtn;
    }
  });
}

// 3. Interactive Eligibility Matcher
function initEligibilityMatcher() {
  const form = document.getElementById("matcher-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const state = document.getElementById("state-select")?.value || "Telangana";
    const landVal = document.getElementById("land-select")?.value || "2.5";
    const category = document.getElementById("category-select")?.value || "BC";
    const cropInput = document.getElementById("crop-input")?.value || "Paddy";

    let landAcres = 2.5;
    let isTenant = false;
    if (landVal.includes("< 2.5")) landAcres = 1.5;
    else if (landVal.includes("2.5 - 5")) landAcres = 3.5;
    else if (landVal.includes("> 5")) landAcres = 6.0;
    else if (landVal.includes("Tenant") || landVal.includes("CCRC")) {
      landAcres = 2.0;
      isTenant = true;
    }

    const payload = {
      state: state,
      land_acres: landAcres,
      is_tenant: isTenant,
      crops: cropInput.split("/").map(c => c.trim()).filter(Boolean),
      category: category,
      has_rofr_patta: category.includes("RoFR"),
      age: 40,
      is_tax_payer: false
    };

    const submitBtn = document.getElementById("matcher-submit-btn");
    const resultsContainer = document.getElementById("match-results");
    if (submitBtn) submitBtn.disabled = true;

    try {
      const res = await fetch(`${API_BASE}/api/match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (resultsContainer && data.status === "success") {
        resultsContainer.classList.remove("hidden");
        
        let cashFormatted = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(data.total_direct_cash_annual);

        let schemesHtml = `
          <div class="space-y-4 w-full">
            <div class="flex flex-wrap items-center justify-between gap-2 p-3 bg-primary-fixed/30 border border-primary-fixed-dim rounded-lg">
              <div>
                <span class="font-extrabold text-primary text-base">✅ ${data.total_eligible} Verified Schemes Matched</span>
                <span class="text-xs text-on-surface-variant block">For ${state} • ${landAcres} Acres • ${cropInput}</span>
              </div>
              <div class="text-right">
                <span class="text-xs text-on-surface-variant uppercase font-bold block">Annual Direct Support</span>
                <span class="text-lg font-extrabold text-primary font-mono">${cashFormatted}</span>
              </div>
            </div>

            <div class="max-h-80 overflow-y-auto space-y-2.5 pr-1">
        `;

        data.eligible_schemes.forEach((s) => {
          schemesHtml += `
            <div class="p-3 bg-surface border border-outline-variant rounded-lg space-y-1.5 hover:border-primary transition-all">
              <div class="flex items-center justify-between">
                <span class="font-bold text-sm text-primary flex items-center gap-1.5">
                  <span class="material-symbols-outlined text-base">check_circle</span>
                  ${s.scheme || s.name}
                </span>
                <span class="text-[11px] font-bold px-2 py-0.5 rounded ${s.level === 'Central' ? 'bg-secondary-fixed text-on-secondary-fixed' : 'bg-primary-fixed text-on-primary-fixed'}">
                  ${s.level} Scheme
                </span>
              </div>
              <p class="text-xs text-on-surface-variant leading-relaxed">${s.benefit_summary || s.benefits_summary || ''}</p>
              <div class="flex flex-wrap items-center justify-between text-[11px] pt-1 border-t border-outline-variant/60 text-outline">
                <span>📋 Docs: ${(s.docs || s.documents_required || []).slice(0, 2).join(', ')}...</span>
                ${s.source_url ? `<a href="${s.source_url}" target="_blank" class="text-primary font-bold hover:underline flex items-center gap-0.5">Portal <span class="material-symbols-outlined text-xs">open_in_new</span></a>` : ''}
              </div>
            </div>
          `;
        });

        if (data.total_ineligible > 0) {
          schemesHtml += `
            <details class="text-xs pt-2">
              <summary class="cursor-pointer text-outline font-semibold hover:text-primary py-1">
                View ${data.total_ineligible} filtered out schemes (with statutory reasons)
              </summary>
              <div class="space-y-1.5 mt-2">
                ${data.ineligible_schemes.slice(0, 5).map(ins => `
                  <div class="p-2 bg-surface-container rounded border border-outline-variant/40">
                    <span class="font-bold text-on-surface">${ins.scheme || ins.name}:</span>
                    <span class="text-error">${ins.reasons ? ins.reasons.join(', ') : 'Criteria not met'}</span>
                  </div>
                `).join('')}
              </div>
            </details>
          `;
        }

        schemesHtml += `</div></div>`;
        resultsContainer.innerHTML = schemesHtml;
      }
    } catch (err) {
      console.error("Match error:", err);
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  });
}

// 4. Conversational AI Query Bar
function initQueryAI() {
  const queryInput = document.getElementById("ai-query-input");
  const queryBtn = document.getElementById("ai-query-btn");
  const resultBox = document.getElementById("ai-query-result");

  if (!queryBtn || !queryInput) return;

  const runQuery = async () => {
    const q = queryInput.value.trim();
    if (!q) return;

    queryBtn.disabled = true;
    queryBtn.textContent = "Querying...";

    try {
      const res = await fetch(`${API_BASE}/api/query_ai`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q, language: "en" })
      });
      const data = await res.json();

      if (resultBox) {
        resultBox.classList.remove("hidden");
        resultBox.innerHTML = `
          <div class="p-4 bg-surface-container-lowest border-2 border-primary rounded-xl shadow-md space-y-2 mt-3 animate-fade-in">
            <div class="flex items-center justify-between pb-2 border-b border-outline-variant">
              <span class="font-bold text-sm text-primary flex items-center gap-1.5">
                <span class="material-symbols-outlined text-lg">smart_toy</span>
                OpenQuest Agricultural Intelligence
              </span>
              <button onclick="document.getElementById('ai-query-result').classList.add('hidden')" class="text-xs text-outline hover:text-on-surface">✕ Close</button>
            </div>
            <div class="text-xs text-on-surface leading-relaxed whitespace-pre-line">${data.response || data.message || 'No response returned.'}</div>
            ${data.url ? `<div class="pt-1"><a href="${data.url}" target="_blank" class="inline-flex items-center gap-1 text-xs font-bold text-primary underline">Visit Official Portal ↗</a></div>` : ''}
          </div>
        `;
      }
    } catch (err) {
      console.error("AI query failed:", err);
    } finally {
      queryBtn.disabled = false;
      queryBtn.textContent = "Query AI";
    }
  };

  queryBtn.addEventListener("click", runQuery);
  queryInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      runQuery();
    }
  });
}

// 5. RapidFuzz Aadhaar vs Bank Account Name Matcher & Consent Vault
function initNameMatcher() {
  const aadhaarInput = document.getElementById("fuzzy-aadhaar-input");
  const bankInput = document.getElementById("fuzzy-bank-input");
  const verifyBtn = document.getElementById("fuzzy-verify-btn");
  const resultBox = document.getElementById("fuzzy-result-badge");
  const consentToggleBtn = document.getElementById("consent-toggle-btn");

  if (verifyBtn && aadhaarInput && bankInput) {
    verifyBtn.addEventListener("click", async () => {
      const aName = aadhaarInput.value.trim();
      const bName = bankInput.value.trim();
      if (!aName || !bName) {
        alert("Please enter both Aadhaar Name and Bank Account Name.");
        return;
      }

      verifyBtn.disabled = true;
      try {
        const res = await fetch(`${API_BASE}/api/verify_name_match`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ aadhaar_name: aName, bank_name: bName })
        });
        const data = await res.json();

        if (resultBox) {
          resultBox.classList.remove("hidden");
          const isGood = data.similarity_score >= 80;
          resultBox.className = `p-3 rounded-lg border text-xs space-y-1 ${isGood ? 'bg-primary-fixed/20 border-primary-fixed-dim text-primary' : 'bg-error-container border-error text-on-error-container'}`;
          resultBox.innerHTML = `
            <div class="flex items-center justify-between font-bold">
              <span>Score: ${data.similarity_score}% (${data.status})</span>
              <span>${data.similarity_score >= 90 ? '🟢 DBT Active' : (data.similarity_score >= 80 ? '🟡 CSC Review' : '🔴 Severe Mismatch')}</span>
            </div>
            <div>${data.action_required}</div>
          `;
        }
      } catch (err) {
        console.error("Name match failed:", err);
      } finally {
        verifyBtn.disabled = false;
      }
    });
  }

  if (consentToggleBtn) {
    consentToggleBtn.addEventListener("click", async () => {
      try {
        const res = await fetch(`${API_BASE}/api/consent/toggle`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ farmer_id: "DEMO_F001" })
        });
        const data = await res.json();
        alert(data.message || "Consent status updated in SQLite database.");
        consentToggleBtn.textContent = data.consent_status ? "Active Consent (Revoke?)" : "Consent Revoked (Grant?)";
        consentToggleBtn.className = data.consent_status 
          ? "text-[11px] font-bold px-2 py-1 rounded bg-primary text-on-primary"
          : "text-[11px] font-bold px-2 py-1 rounded bg-error text-on-error";
      } catch (err) {
        console.error("Consent toggle error:", err);
      }
    });
  }
}

// 6. Interactive KCC Scale of Finance & 4% MISS Calculator
function initKCCCalculator() {
  const calcBtn = document.getElementById("kcc-calc-btn");
  const modal = document.getElementById("kcc-modal");
  const closeBtn = document.getElementById("kcc-modal-close");
  const form = document.getElementById("kcc-calc-form");
  const resultDiv = document.getElementById("kcc-calc-result");

  if (calcBtn && modal) {
    calcBtn.addEventListener("click", (e) => {
      e.preventDefault();
      modal.classList.remove("hidden");
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const crop = document.getElementById("kcc-crop-select")?.value || "Paddy";
      const acres = parseFloat(document.getElementById("kcc-acres-input")?.value || "2.5");
      const debt = parseFloat(document.getElementById("kcc-debt-input")?.value || "0.0");

      try {
        const res = await fetch(`${API_BASE}/api/kcc/calculate`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ crop: crop, land_acres: acres, existing_debt: debt })
        });
        const json = await res.json();
        const d = json.data;

        if (resultDiv && d) {
          resultDiv.classList.remove("hidden");
          const fmt = (num) => new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(num);

          resultDiv.innerHTML = `
            <div class="p-4 bg-surface-container-low border border-outline-variant rounded-xl space-y-3 text-xs">
              <div class="flex justify-between items-center pb-2 border-b border-outline-variant">
                <span class="font-bold text-sm text-secondary">Year 1 Sanction Limit:</span>
                <span class="font-benefit-number text-lg text-secondary font-mono">${fmt(d.total_sanction_limit_year1)}</span>
              </div>
              <div class="grid grid-cols-2 gap-2 text-on-surface">
                <div>Scale of Finance: <strong>${fmt(d.scale_of_finance_per_acre)} / acre</strong></div>
                <div>5-Year Limit: <strong>${fmt(d.five_year_limit)}</strong></div>
                <div>Crop Cultivation: <strong>${fmt(d.crop_cultivation_cost)}</strong></div>
                <div>Post-Harvest (20%): <strong>${fmt(d.post_harvest_consumption_add_on)}</strong></div>
              </div>
              <div class="p-2.5 rounded bg-primary-fixed/20 border border-primary-fixed-dim text-primary">
                <div class="font-bold">Modified Interest Subvention Scheme (MISS):</div>
                <div>7.0% Bank Rate - 3.0% Prompt Repayment = <strong>4.0% Net Annual Interest</strong></div>
              </div>
              <div class="text-[11px] text-on-surface-variant">${d.collateral_note}</div>
            </div>
          `;
        }
      } catch (err) {
        console.error("KCC calculation error:", err);
      }
    });
  }
}

// 7. Emergency 72-Hour Crop Loss Claim Dispatcher
function initClaimDispatcher() {
  const dispatchBtns = document.querySelectorAll(".dispatch-claim-trigger");
  const modal = document.getElementById("claim-modal");
  const closeBtn = document.getElementById("claim-modal-close");
  const form = document.getElementById("claim-dispatch-form");
  const resultDiv = document.getElementById("claim-dispatch-result");

  dispatchBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      if (modal) modal.classList.remove("hidden");
    });
  });

  if (closeBtn && modal) {
    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const payload = {
        farmer_name: document.getElementById("claim-farmer-name")?.value || "Ravi Kumar",
        phone: document.getElementById("claim-phone")?.value || "9876543210",
        state: document.getElementById("claim-state")?.value || "Telangana",
        district: document.getElementById("claim-district")?.value || "Warangal",
        village: document.getElementById("claim-village")?.value || "Geesugonda",
        survey_no: document.getElementById("claim-survey")?.value || "402/A",
        crop: document.getElementById("claim-crop")?.value || "Paddy",
        calamity_cause: document.getElementById("claim-cause")?.value || "Hailstorm",
        loss_percentage: parseInt(document.getElementById("claim-loss-pct")?.value || "75"),
        notes: document.getElementById("claim-notes")?.value || "Lodged field photos attached."
      };

      const submitBtn = document.getElementById("claim-submit-btn");
      if (submitBtn) submitBtn.disabled = true;

      try {
        const res = await fetch(`${API_BASE}/api/claim/dispatch`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (resultDiv && data.status === "dispatched") {
          resultDiv.classList.remove("hidden");
          resultDiv.innerHTML = `
            <div class="p-4 bg-primary-fixed/30 border-2 border-primary rounded-xl space-y-2 text-xs text-primary animate-fade-in">
              <div class="flex items-center justify-between font-extrabold text-sm pb-1 border-b border-primary/20">
                <span>✅ Emergency Loss Intimation Logged</span>
                <span class="font-mono text-xs bg-primary text-on-primary px-2 py-0.5 rounded">${data.docket_number}</span>
              </div>
              <p>Your loss declaration has been queued with the State Crop Calamity Portal.</p>
              <div class="bg-surface-container p-2.5 rounded font-mono text-[11px] text-on-surface">
                <strong>Statutory SMS String (Sent to 51969):</strong><br/>
                <code>${data.sms_string}</code>
              </div>
              <div class="text-[11px] text-on-surface-variant">
                <strong>Next Step:</strong> ${data.next_step}<br/>
                <strong>Helpline:</strong> ${data.pmfby_toll_free}
              </div>
            </div>
          `;
          form.reset();
        }
      } catch (err) {
        console.error("Claim dispatch error:", err);
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }
}

// 8. Intermediary & Village Operator Desk (SQLite Driven)
async function initIntermediaryPortal() {
  const container = document.getElementById("intermediary-records-container");
  if (!container) return;

  try {
    const res = await fetch(`${API_BASE}/api/intermediary`);
    const data = await res.json();

    if (data.status === "success" && data.records) {
      if (data.records.length === 0) {
        container.innerHTML = `<div class="p-4 text-xs text-on-surface-variant">No active follow-up actions required. All profiles verified.</div>`;
        return;
      }

      let html = `<div class="space-y-3">`;
      data.records.slice(0, 6).forEach((rec) => {
        const isUrgent = rec.priority_label?.includes("CRITICAL") || rec.remaining_days <= 7;
        html += `
          <div class="p-3 bg-surface-container-low border ${isUrgent ? 'border-error' : 'border-outline-variant'} rounded-lg space-y-2 text-xs">
            <div class="flex flex-wrap items-center justify-between gap-1">
              <span class="font-bold text-on-surface flex items-center gap-1.5">
                <span class="material-symbols-outlined text-base ${isUrgent ? 'text-error' : 'text-primary'}">person</span>
                ${rec.farmer_name} (${rec.farmer_id})
              </span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded ${isUrgent ? 'bg-error text-on-error' : 'bg-secondary-fixed text-on-secondary-fixed'}">
                ${rec.priority_label || 'Attention Required'}
              </span>
            </div>
            <div class="text-on-surface-variant">
              Scheme: <strong>${rec.scheme}</strong> • Days Left: <strong class="${rec.remaining_days <= 5 ? 'text-error' : ''}">${rec.remaining_days}</strong>
            </div>
            ${rec.missing_documents?.length ? `
              <div class="text-[11px] text-error font-medium">
                Missing Docs: ${rec.missing_documents.join(", ")}
              </div>
            ` : ''}
            ${rec.name_mismatch_warning ? `
              <div class="text-[11px] text-secondary font-medium">
                ${rec.name_mismatch_warning}
              </div>
            ` : ''}
            <div class="flex items-center justify-end gap-2 pt-1 border-t border-outline-variant/60">
              <button onclick="sendAlert('${rec.farmer_id}', '${rec.farmer_name}')" class="bg-primary hover:bg-primary-container text-on-primary px-2.5 py-1 rounded text-[11px] font-bold flex items-center gap-1">
                <span class="material-symbols-outlined text-xs">send</span> Dispatch SMS
              </button>
            </div>
          </div>
        `;
      });
      html += `</div>`;
      container.innerHTML = html;
    }
  } catch (err) {
    console.error("Intermediary loading error:", err);
  }
}

// Global alert dispatcher
window.sendAlert = async function(farmerId, farmerName) {
  try {
    const res = await fetch(`${API_BASE}/api/send_alert`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        farmer_id: farmerId,
        channel: "sms",
        message: `Kisan Setu Alert: Please submit missing scheme documents before deadline.`
      })
    });
    const d = await res.json();
    alert(`✅ Alert successfully sent to ${farmerName} (${d.sent_to}) via ${d.channel.toUpperCase()}`);
  } catch (err) {
    alert("Alert dispatch failed. Check network.");
  }
};

// 9. Live MSP vs Mandi Benchmark Table Loader
async function loadMspComparison() {
  const tbody = document.getElementById("msp-table-body");
  if (!tbody) return;

  try {
    const res = await fetch(`${API_BASE}/api/msp_comparison`);
    const list = await res.json();

    if (Array.isArray(list) && list.length > 0) {
      tbody.innerHTML = list.map((item) => {
        const isPositive = item.price_delta >= 0;
        const fmt = (n) => `₹${n.toLocaleString('en-IN')}`;
        return `
          <tr class="hover:bg-surface-container-low transition-colors">
            <td class="py-3.5 px-4 font-bold flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full ${isPositive ? 'bg-primary' : 'bg-secondary'}"></span>
              <span>${item.crop}</span>
            </td>
            <td class="py-3.5 px-4 text-on-surface-variant">${item.category}</td>
            <td class="py-3.5 px-4 font-benefit-number text-benefit-number text-primary">${fmt(item.msp_rate)}</td>
            <td class="py-3.5 px-4 font-mono font-bold text-on-surface">${fmt(item.average_mandi_price)}</td>
            <td class="py-3.5 px-4 font-bold ${isPositive ? 'text-primary' : 'text-secondary'}">
              ${isPositive ? '+' : ''}${fmt(item.price_delta)}
            </td>
            <td class="py-3.5 px-4">
              <span class="inline-flex items-center gap-1 text-xs ${isPositive ? 'bg-surface-container text-on-surface' : 'bg-primary-fixed text-on-primary-fixed'} px-2.5 py-1 rounded font-bold">
                <span class="material-symbols-outlined text-xs">${isPositive ? 'local_shipping' : 'store'}</span>
                ${item.recommendation.split('.')[0]}
              </span>
            </td>
          </tr>
        `;
      }).join('');
    }
  } catch (err) {
    console.error("MSP loading error:", err);
  }
}
