import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_js_path = os.path.join(base_dir, "frontend", "app.js")

with open(app_js_path, "r", encoding="utf-8") as f:
    code = f.read()

target = """        if (data.ok) {
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
        }"""

replacement = """        if (data.status === 'success' || data.ok) {
          const botBubble = document.createElement('div');
          botBubble.className = 'voice-bubble voice-bubble-bot';

          const detectedLangName = data.language_name || data.detected_language || 'Multilingual';
          const detectedLangFlag = data.language_flag || '🌾';
          const detectedTtsCode = data.tts_code || data.detected_code || 'te-IN';
          const fullText = data.response_text || data.spoken_response || data.speak_text || 'No response available.';
          const speechVoiceText = data.speak_text || fullText;

          const helplineBadge = data.helpline
            ? `<div style="margin-top: 0.4rem; font-size: 0.78rem; background: #ecfdf5; padding: 4px 8px; border-radius: 4px; border: 1px solid #a7f3d0; color: #065f46;">📞 <strong>Toll-Free Helpline:</strong> ${escapeHtml(data.helpline)}</div>`
            : '';

          const ruleBadge = data.key_statute_or_rule
            ? `<div style="margin-top: 0.4rem; font-size: 0.78rem; background: #fefce8; padding: 4px 8px; border-radius: 4px; border: 1px solid #fde047; color: #854d0e;">⚖️ <strong>Statutory Rule:</strong> ${escapeHtml(data.key_statute_or_rule)}</div>`
            : '';

          botBubble.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
              <span style="font-weight: 700; color: #15803d; font-size: 0.84rem;">
                ${escapeHtml(detectedLangFlag)} OpenQuest Voice AI • ${escapeHtml(detectedLangName)}
              </span>
              <span style="font-size: 0.72rem; background: #dcfce7; color: #166534; padding: 2px 6px; border-radius: 4px; font-weight: 600;">
                Verified Advisory
              </span>
            </div>
            <div style="font-size: 0.88rem; color: #1f2937; line-height: 1.55; white-space: pre-line;">
              ${escapeHtml(fullText)}
            </div>
            ${helplineBadge}
            ${ruleBadge}
            <div class="voice-playback-bar">
              <button type="button" class="btn btn-secondary voice-listen-btn" style="padding: 3px 8px; font-size: 0.78rem;">
                <span>🔊</span> <span>Listen / వినండి / सुनें</span>
              </button>
              <button type="button" class="btn btn-secondary voice-stop-btn" style="padding: 3px 8px; font-size: 0.78rem;">
                <span>⏹️</span> <span>Stop Voice</span>
              </button>
            </div>
          `;

          const listenBtn = botBubble.querySelector('.voice-listen-btn');
          const stopBtn = botBubble.querySelector('.voice-stop-btn');
          if (listenBtn) {
            listenBtn.addEventListener('click', () => {
              speakText(speechVoiceText, detectedTtsCode);
            });
          }
          if (stopBtn) {
            stopBtn.addEventListener('click', () => {
              if (window.speechSynthesis) window.speechSynthesis.cancel();
            });
          }

          voiceChatHistory.appendChild(botBubble);
          voiceChatHistory.scrollTop = voiceChatHistory.scrollHeight;

          // Speak phonetic voice output
          speakText(speechVoiceText, detectedTtsCode);
        }"""

if target in code:
    code = code.replace(target, replacement)
    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("Updated app.js response handler for voice engine response fields!")
else:
    print("Target not found in app.js")
