import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_js_path = os.path.join(base_dir, "frontend", "app.js")

with open(app_js_path, "r", encoding="utf-8") as f:
    code = f.read()

# Let's define the new block to add right before `// =========================================================================\n  // 9. INITIALIZATION ENTRY POINT`
new_methods = """
  // =========================================================================
  // 8B. MULTILINGUAL DYNAMIC TRANSLATION & VOICE ASSISTANT ENGINE
  // =========================================================================
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function applyLanguage(lang) {
    if (!lang) return;
    state.lang = lang;
    localStorage.setItem('kisan_lang', lang);

    if (langSelect && langSelect.value !== lang) {
      langSelect.value = lang;
    }

    // Update all text nodes with data-i18n
    const translatableElements = document.querySelectorAll('[data-i18n]');
    translatableElements.forEach(el => {
      const key = el.getAttribute('data-i18n');
      const val = t(key);
      if (val && val !== key) {
        el.textContent = val;
      }
    });

    // Update all input placeholders with data-i18n-placeholder
    const placeholderElements = document.querySelectorAll('[data-i18n-placeholder]');
    placeholderElements.forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      const val = t(key);
      if (val && val !== key) {
        el.placeholder = val;
      }
    });

    // Sync voice assistant language dropdown
    const voiceLangSelect = document.getElementById('voiceLangSelect');
    if (voiceLangSelect) {
      const localeMap = {
        'en': 'en-IN',
        'te': 'te-IN',
        'hi': 'hi-IN',
        'mr': 'mr-IN',
        'ta': 'ta-IN',
        'kn': 'kn-IN',
        'bn': 'bn-IN',
        'gu': 'gu-IN',
        'ml': 'ml-IN',
        'pa': 'pa-IN',
        'or': 'or-IN'
      };
      if (localeMap[lang]) {
        voiceLangSelect.value = localeMap[lang];
      }
    }

    // Re-render Scheme Browser & State dropdown with the new language
    populateStateDropdown();
    renderSchemeBrowser();
  }

  // Sample Document Modal Preview Functions
  window.openDocPreviewModal = function (docType, docTitle, docSrc) {
    const modal = document.getElementById('sampleDocModal');
    const titleEl = document.getElementById('sampleDocModalTitle');
    const imgEl = document.getElementById('sampleDocModalImg');
    const dlLink = document.getElementById('sampleDocModalDownloadLink');

    if (titleEl) titleEl.textContent = docTitle || 'Sample Document Preview';
    if (imgEl) imgEl.src = docSrc;
    if (dlLink) {
      dlLink.href = API_BASE + '/api/documents/download/' + docType;
      dlLink.download = 'Sample_' + docType + '.svg';
    }
    if (modal) {
      modal.style.display = 'flex';
      modal.setAttribute('aria-hidden', 'false');
    }
  };

  window.closeDocPreviewModal = function () {
    const modal = document.getElementById('sampleDocModal');
    if (modal) {
      modal.style.display = 'none';
      modal.setAttribute('aria-hidden', 'true');
    }
  };

  function initVoiceAssistant() {
    const voiceMicBtn = document.getElementById('voiceMicBtn');
    const voiceStatusText = document.getElementById('voiceStatusText');
    const voiceTranscriptInput = document.getElementById('voiceTranscriptInput');
    const voiceSendBtn = document.getElementById('voiceSendBtn');
    const voiceLangSelect = document.getElementById('voiceLangSelect');
    const voiceChatHistory = document.getElementById('voiceChatHistory');

    if (!voiceMicBtn || !voiceChatHistory) return;

    let recognition = null;
    let isListening = false;

    // Check Web Speech API support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      try {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = function () {
          isListening = true;
          voiceMicBtn.classList.add('listening');
          if (voiceStatusText) {
            voiceStatusText.textContent = t('voice_listening') || 'Listening... Speak now';
          }
        };

        recognition.onresult = function (event) {
          isListening = false;
          voiceMicBtn.classList.remove('listening');
          if (event.results && event.results.length > 0 && event.results[0].length > 0) {
            const transcript = event.results[0][0].transcript;
            if (voiceTranscriptInput) {
              voiceTranscriptInput.value = transcript;
            }
            if (voiceStatusText) {
              voiceStatusText.textContent = 'Voice detected: "' + transcript + '"';
            }
            submitVoiceQuery(transcript);
          }
        };

        recognition.onerror = function (event) {
          console.warn('Speech recognition error:', event.error);
          isListening = false;
          voiceMicBtn.classList.remove('listening');
          if (voiceStatusText) {
            voiceStatusText.textContent = t('voice_click_speak') || 'Click microphone to speak...';
          }
        };

        recognition.onend = function () {
          isListening = false;
          voiceMicBtn.classList.remove('listening');
          if (voiceStatusText && !voiceStatusText.textContent.startsWith('Voice detected')) {
            voiceStatusText.textContent = t('voice_click_speak') || 'Click microphone to speak...';
          }
        };
      } catch (err) {
        console.warn('SpeechRecognition initialization error:', err);
      }
    }

    voiceMicBtn.addEventListener('click', function () {
      if (!recognition) {
        alert('Web Speech Recognition is not supported or permission is blocked in this browser. You can type your query in your language in the input box below!');
        if (voiceTranscriptInput) voiceTranscriptInput.focus();
        return;
      }

      if (isListening) {
        recognition.stop();
        isListening = false;
        voiceMicBtn.classList.remove('listening');
        if (voiceStatusText) {
          voiceStatusText.textContent = t('voice_click_speak') || 'Click microphone to speak...';
        }
      } else {
        let targetLang = 'te-IN';
        if (voiceLangSelect && voiceLangSelect.value && voiceLangSelect.value !== 'auto') {
          targetLang = voiceLangSelect.value;
        } else {
          const map = {
            'en': 'en-IN', 'te': 'te-IN', 'hi': 'hi-IN', 'mr': 'mr-IN',
            'ta': 'ta-IN', 'kn': 'kn-IN', 'bn': 'bn-IN', 'gu': 'gu-IN',
            'ml': 'ml-IN', 'pa': 'pa-IN', 'or': 'or-IN'
          };
          targetLang = map[state.lang] || 'te-IN';
        }
        recognition.lang = targetLang;
        try {
          recognition.start();
        } catch (e) {
          console.warn('Could not start recognition:', e);
        }
      }
    });

    if (voiceSendBtn && voiceTranscriptInput) {
      voiceSendBtn.addEventListener('click', function () {
        const text = voiceTranscriptInput.value.trim();
        if (text) {
          submitVoiceQuery(text);
        }
      });

      voiceTranscriptInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          const text = voiceTranscriptInput.value.trim();
          if (text) {
            submitVoiceQuery(text);
          }
        }
      });
    }

    // Global quick voice prompt handler for chips
    window.askQuickVoicePrompt = function (promptText) {
      if (voiceTranscriptInput) {
        voiceTranscriptInput.value = promptText;
      }
      submitVoiceQuery(promptText);
    };

    // Text to Speech playback function
    function speakText(text, langCode) {
      if (!window.speechSynthesis) return;
      try {
        window.speechSynthesis.cancel();
        const cleanText = text.replace(/[*_#`\\n]/g, ' ').substring(0, 350);
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = langCode || 'te-IN';
        utterance.rate = 0.95;

        const voices = window.speechSynthesis.getVoices();
        if (voices && voices.length > 0) {
          const matched = voices.find(v => v.lang === utterance.lang || v.lang.startsWith(utterance.lang.split('-')[0]));
          if (matched) utterance.voice = matched;
        }

        window.speechSynthesis.speak(utterance);
      } catch (e) {
        console.warn('TTS speak error:', e);
      }
    }
    window.speakVoiceText = speakText;

    // Send query to /api/voice_assistant
    async function submitVoiceQuery(query) {
      if (!query || !query.trim()) return;

      // Append user chat bubble
      const userBubble = document.createElement('div');
      userBubble.className = 'voice-bubble voice-bubble-user';
      userBubble.innerHTML = `
        <div style="font-size: 0.75rem; opacity: 0.85; margin-bottom: 0.2rem;">Farmer / రైతు / किसान</div>
        <div>${escapeHtml(query)}</div>
      `;
      voiceChatHistory.appendChild(userBubble);

      // Append loading bubble
      const loadingBubble = document.createElement('div');
      loadingBubble.className = 'voice-bubble voice-bubble-bot';
      loadingBubble.id = 'voiceLoadingBubble';
      loadingBubble.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.5rem; color: #166534; font-weight: 600;">
          <span>⏳</span>
          <span>Processing voice query in your language... / విశ్లేషిస్తున్నాము...</span>
        </div>
      `;
      voiceChatHistory.appendChild(loadingBubble);
      voiceChatHistory.scrollTop = voiceChatHistory.scrollHeight;

      let chosenLang = 'auto';
      if (voiceLangSelect && voiceLangSelect.value) {
        chosenLang = voiceLangSelect.value;
      }

      try {
        const response = await fetch(API_BASE + '/api/voice_assistant', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: query,
            language: chosenLang
          })
        });

        const data = await response.json();
        const loadEl = document.getElementById('voiceLoadingBubble');
        if (loadEl) loadEl.remove();

        if (data.ok) {
          const botBubble = document.createElement('div');
          botBubble.className = 'voice-bubble voice-bubble-bot';

          const detectedLangName = data.detected_language || 'Multilingual';
          const detectedLangCode = data.detected_code || 'te-IN';
          const spokenText = data.spoken_response || data.speech_text || 'No response available.';
          const ruleBadge = data.key_statute_or_rule ? `<div style="margin-top: 0.4rem; font-size: 0.78rem; background: #ecfdf5; padding: 4px 8px; border-radius: 4px; border: 1px solid #a7f3d0; color: #065f46;"><strong>Statutory Rule:</strong> ${escapeHtml(data.key_statute_or_rule)}</div>` : '';

          const schemesHtml = (data.schemes_recommended && data.schemes_recommended.length > 0)
            ? `<div style="margin-top: 0.4rem; display: flex; flex-wrap: wrap; gap: 0.35rem;">
                ${data.schemes_recommended.map(s => `<span class="badge-tag badge-tag-green" style="font-size: 0.75rem;">🌾 ${escapeHtml(s)}</span>`).join('')}
               </div>`
            : '';

          botBubble.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
              <span style="font-weight: 700; color: #15803d; font-size: 0.82rem;">
                🌾 OpenQuest Voice AI • ${escapeHtml(detectedLangName)}
              </span>
              <span style="font-size: 0.75rem; background: #dcfce7; color: #166534; padding: 2px 6px; border-radius: 4px; font-weight: 600;">
                ${escapeHtml(data.query_category || 'Advisory')}
              </span>
            </div>
            <div style="font-size: 0.88rem; color: #1f2937; line-height: 1.5; white-space: pre-line;">
              ${escapeHtml(spokenText)}
            </div>
            ${ruleBadge}
            ${schemesHtml}
            <div class="voice-playback-bar">
              <button type="button" class="btn btn-secondary voice-listen-btn" style="padding: 3px 8px; font-size: 0.78rem;">
                <span>🔊</span> <span>Listen / వినండి</span>
              </button>
              <button type="button" class="btn btn-secondary voice-stop-btn" style="padding: 3px 8px; font-size: 0.78rem;">
                <span>⏹️</span> <span>Stop</span>
              </button>
            </div>
          `;

          const listenBtn = botBubble.querySelector('.voice-listen-btn');
          const stopBtn = botBubble.querySelector('.voice-stop-btn');
          if (listenBtn) {
            listenBtn.addEventListener('click', () => {
              speakText(data.speech_text || spokenText, detectedLangCode);
            });
          }
          if (stopBtn) {
            stopBtn.addEventListener('click', () => {
              if (window.speechSynthesis) window.speechSynthesis.cancel();
            });
          }

          voiceChatHistory.appendChild(botBubble);
          voiceChatHistory.scrollTop = voiceChatHistory.scrollHeight;

          speakText(data.speech_text || spokenText, detectedLangCode);
        } else {
          const errBubble = document.createElement('div');
          errBubble.className = 'voice-bubble voice-bubble-bot';
          errBubble.innerHTML = `
            <div style="color: #dc2626; font-weight: 600;">⚠️ Could not process query: ${escapeHtml(data.error || 'Server error')}</div>
          `;
          voiceChatHistory.appendChild(errBubble);
        }
      } catch (err) {
        const loadEl = document.getElementById('voiceLoadingBubble');
        if (loadEl) loadEl.remove();

        const errBubble = document.createElement('div');
        errBubble.className = 'voice-bubble voice-bubble-bot';
        errBubble.innerHTML = `
          <div style="color: #dc2626; font-weight: 600;">⚠️ Voice Service Offline: ${escapeHtml(err.message)}</div>
        `;
        voiceChatHistory.appendChild(errBubble);
      }
      voiceChatHistory.scrollTop = voiceChatHistory.scrollHeight;
    }
  }
"""

marker = "  // =========================================================================\n  // 9. INITIALIZATION ENTRY POINT"
if marker in code and "initVoiceAssistant" not in code:
    code = code.replace(marker, new_methods + "\n" + marker)
    print("Injected Voice Assistant and Language Switcher methods!")

# Update init() to call applyLanguage(state.lang) and initVoiceAssistant()
old_init_start = """  function init() {
    populateStateDropdown();
    renderSchemeBrowser();
    initPrimaryTabs();"""

new_init_start = """  function init() {
    applyLanguage(state.lang);
    initPrimaryTabs();
    initVoiceAssistant();"""

if old_init_start in code:
    code = code.replace(old_init_start, new_init_start)
    print("Updated init() start!")

# Update langSelect event listener inside init()
old_lang_listener = """    if (langSelect) {
      langSelect.value = state.lang;
      langSelect.addEventListener('change', function () {
        state.lang = this.value;
        localStorage.setItem('kisan_lang', this.value);
        populateStateDropdown();
        renderSchemeBrowser();
      });
    }"""

new_lang_listener = """    if (langSelect) {
      langSelect.value = state.lang;
      langSelect.addEventListener('change', function () {
        applyLanguage(this.value);
      });
    }"""

if old_lang_listener in code:
    code = code.replace(old_lang_listener, new_lang_listener)
    print("Updated langSelect event listener to applyLanguage!")

with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(code)

print("frontend/app.js patched successfully!")
