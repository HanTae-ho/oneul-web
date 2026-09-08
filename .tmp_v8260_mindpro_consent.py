from pathlib import Path
import re

idx=Path('index.html')
priv=Path('privacy.html')
sw=Path('sw.js')
readme=Path('README.md')

s=idx.read_text(encoding='utf-8')
assert "const BUILD = 'V8.2.59';" in s
assert "const KEY = 'ohg.v1';" in s
assert "const DATA_SCHEMA = 6;" in s
assert "aiConsent: 0" in s
assert "function aiEnsureExternalConsent" not in s
s=s.replace("const BUILD = 'V8.2.59';", "const BUILD = 'V8.2.60';", 1)

# 마음프로 안내 안에 현재 동의 상태와 철회 버튼을 추가합니다.
old='''      <p class="muted" style="margin:0">앱 기능은 기기에서 먼저 처리하고, <b>내가 직접 적은 일반 대화만</b> AI로 보냅니다. 개인 회복기록은 자동 전송하지 않습니다.</p>\n    </div>\n  </div>'''
new='''      <p class="muted" style="margin:0">앱 기능은 기기에서 먼저 처리하고, <b>내가 직접 적은 일반 대화만</b> AI로 보냅니다. 개인 회복기록은 자동 전송하지 않습니다.</p>\n      <div class="sp" style="align-items:center;margin-top:9px;gap:8px">\n        <p class="tiny" id="ai-consent-state" style="margin:0;flex:1"></p>\n        <button class="tiny hide" id="ai-consent-revoke" type="button" style="color:var(--acc);font-weight:600">동의 철회</button>\n      </div>\n    </div>\n  </div>'''
assert old in s
s=s.replace(old,new,1)

# 동의 버전과 실제 전송 직전의 명시적 고지/동의 UI.
anchor='''function aiClientId(){\n  if(S.aiClient) return S.aiClient;\n  try{ S.aiClient = crypto.randomUUID(); }\n  catch(e){ S.aiClient = 'ohg-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2); }\n  save();\n  return S.aiClient;\n}\n'''
assert anchor in s
insert=anchor+'''const AI_CONSENT_VERSION = 1;\nfunction drawAIConsentState(){\n  const st=$('#ai-consent-state'), rv=$('#ai-consent-revoke');\n  const on = Number(S.aiConsent || 0) === AI_CONSENT_VERSION;\n  if(st) st.textContent = on ? 'AI 외부 전송 동의: 동의함' : 'AI 외부 전송 동의: 아직 동의하지 않음';\n  if(rv) rv.classList.toggle('hide', !on);\n}\nfunction aiWithdrawExternalConsent(){\n  S.aiConsent = 0; save(); drawAIConsentState();\n  toast('마음프로 AI 외부 전송 동의를 철회했습니다.');\n}\nfunction aiEnsureExternalConsent(text, topic){\n  if(Number(S.aiConsent || 0) === AI_CONSENT_VERSION) return true;\n  /* 서버가 연결되지 않은 상태에서는 외부 전송 자체가 없으므로 동의를 묻지 않습니다. */\n  if(!aiEndpoint()) return true;\n  modal(\n    '<h3>마음프로 AI 대화 전송 안내</h3>' +\n    '<p class="muted">일반 AI 답변을 받기 위해 <b>내가 직접 보내는 문장</b>, 최근 일반 AI 대화 최대 8개, 익명형 식별값, 대화 주제와 앱 버전이 Google Apps Script를 거쳐 OpenAI API로 전송됩니다.</p>' +\n    '<div class="note" style="margin:10px 0"><b>자동으로 보내지 않는 내용</b><br>내 발자취 · 자가점검 점수 · 12단계 · 회복 실천도구 · 복약 등 기기에 저장된 회복기록은 자동 첨부하지 않습니다.</div>' +\n    '<p class="muted">내가 직접 적은 문장에 건강 · 중독 · 복약 등 민감한 내용이 들어 있으면 그 내용도 함께 전송될 수 있습니다. 이름 · 전화번호 · 주소 · 병원명처럼 나를 알아볼 수 있는 정보는 적지 않는 것을 권합니다.</p>' +\n    '<p class="tiny">Google 및 OpenAI의 글로벌 인프라에서 국외 처리될 수 있습니다. <a href="./privacy.html" target="_blank" rel="noopener" style="color:var(--acc);font-weight:600">개인정보처리방침 보기</a></p>' +\n    '<button class="btn" id="ai-consent-yes">동의하고 계속</button>' +\n    '<div style="height:8px"></div><button class="btn ghost" id="ai-consent-no">취소</button>'\n  );\n  const yes=$('#ai-consent-yes'), no=$('#ai-consent-no');\n  if(yes) yes.onclick=()=>{\n    S.aiConsent = AI_CONSENT_VERSION; save(); drawAIConsentState(); closeModal(); aiSend(text, topic);\n  };\n  if(no) no.onclick=closeModal;\n  return false;\n}\n'''
s=s.replace(anchor,insert,1)

# 로컬 기능 의도는 그대로 기기에서 처리하고, 실제 일반 AI 전송만 동의 대상으로 제한합니다.
old_gate='''  const isLocal = !!(crisis || voiceCommand || timerMin || wantsRead || knowledge || localIntent);\n\n  const prior = (Array.isArray(S.aiChat) ? S.aiChat : [])'''
new_gate='''  const isLocal = !!(crisis || voiceCommand || timerMin || wantsRead || knowledge || localIntent);\n\n  if(!isLocal && !aiEnsureExternalConsent(text, topic)) return;\n\n  const prior = (Array.isArray(S.aiChat) ? S.aiChat : [])'''
assert old_gate in s
s=s.replace(old_gate,new_gate,1)

# 마음프로 안내에서 사용자가 언제든 동의를 철회할 수 있도록 연결합니다.
old_bind="$('#ai-guide-toggle').onclick = () => { if(ai.guideTimer){ clearTimeout(ai.guideTimer); ai.guideTimer=0; } ai.guideOpen=!ai.guideOpen; drawAIGuide(); };\n"
new_bind=old_bind+"const aiConsentRevoke=$('#ai-consent-revoke'); if(aiConsentRevoke) aiConsentRevoke.onclick=aiWithdrawExternalConsent;\ndrawAIConsentState();\n"
assert old_bind in s
s=s.replace(old_bind,new_bind,1)
idx.write_text(s,encoding='utf-8')

p=priv.read_text(encoding='utf-8')
assert 'V8.2.59' in p
p=p.replace('V8.2.59','V8.2.60')
old='''<p><b>마음프로</b><br>AI 답변이 필요한 경우에만 익명형 기기 식별값, 현재 메시지, 대화 주제, 앱 버전, 최근 일반 AI 대화 최대 8개가 Google Apps Script를 거쳐 OpenAI API로 전송됩니다.</p>'''
new='''<p><b>마음프로</b><br>일반 AI 대화를 처음 전송하기 전에 전송 항목과 외부 처리를 안내하고 사용자의 명시적 동의를 받습니다. 동의한 경우에만 익명형 기기 식별값, 현재 메시지, 대화 주제, 앱 버전, 최근 일반 AI 대화 최대 8개가 Google Apps Script를 거쳐 OpenAI API로 전송됩니다.</p>'''
assert old in p
p=p.replace(old,new,1)
old='''<li>위치 권한, 마음프로, 의견 보내기는 사용자가 선택할 수 있습니다.</li>'''
new='''<li>위치 권한, 마음프로, 의견 보내기는 사용자가 선택할 수 있으며, 마음프로 AI 외부 전송 동의는 마음프로 안내에서 철회할 수 있습니다.</li>'''
assert old in p
p=p.replace(old,new,1)
priv.write_text(p,encoding='utf-8')

w=sw.read_text(encoding='utf-8')
assert "const APP_VERSION = 'V8.2.59';" in w
assert "const V = 'ohg-v8259-single-accordion';" in w
w=w.replace("const APP_VERSION = 'V8.2.59';", "const APP_VERSION = 'V8.2.60';", 1)
w=w.replace("const V = 'ohg-v8259-single-accordion';", "const V = 'ohg-v8260-mindpro-consent';", 1)
sw.write_text(w,encoding='utf-8')

r=readme.read_text(encoding='utf-8')
assert not r.startswith('## V8.2.60')
entry='''## V8.2.60 — 마음프로 AI 외부 전송 고지 · 동의\n- 마음프로의 로컬 기능은 기존처럼 기기에서 먼저 처리하며, 일반 AI 대화를 실제 외부 서버로 보내기 직전에만 전송 내용을 안내하고 명시적 동의를 받습니다.\n- 동의 안내에는 현재 메시지, 최근 일반 AI 대화 최대 8개, 익명형 식별값, 대화 주제·앱 버전의 전송과 Google Apps Script → OpenAI API 처리, 국외 처리 가능성을 표시합니다.\n- 내 발자취·자가점검·12단계·회복 실천도구·복약 등 저장된 회복기록은 자동 첨부하지 않는 원칙을 함께 표시합니다.\n- 마음프로 안내에서 현재 동의 상태를 확인하고 언제든 외부 전송 동의를 철회할 수 있습니다. 동의하지 않거나 철회해도 타이머·도움글·모임·센터·병원·헬프콜·기록 등 로컬 기능은 계속 사용할 수 있습니다.\n- 개인정보처리방침도 실제 동의 동작에 맞춰 최소 문구만 보강했습니다. `DATA_SCHEMA=6`, `ohg.v1`, 기존 기록형식과 Android 정확알림·화면 OFF 알림·부팅 재예약·네이티브 TTS·이완 TTS는 변경하지 않습니다.\n\n'''
readme.write_text(entry+r,encoding='utf-8')
