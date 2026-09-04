from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,n=1):
    global s
    c=s.count(old)
    assert c==n, f'expected {n}, got {c}: {old[:140]}'
    s=s.replace(old,new,n)

rep("const BUILD = 'V8.1.9';", "const BUILD = 'V8.2.0';")
rep("const DATA_SCHEMA = 2;", "const DATA_SCHEMA = 3;")

rep("  familyStepWorks: [], familyStepDrafts: {},\n  aiChat: [], aiClient: '', aiConsent: 0,       /* AI 대화는 이 기기에만 저장 */",
"  familyStepWorks: [], familyStepDrafts: {},\n  timeCapsule: { text:'', createdAt:0, updatedAt:0 }, /* 미래의 나에게 — 개인 회복기록, 기기 안에만 저장 */\n  aiChat: [], aiClient: '', aiConsent: 0,       /* AI 대화는 이 기기에만 저장 */")

rep("  if(!Array.isArray(s.familyStepWorks)) s.familyStepWorks = [];\n  if(!s.familyStepDrafts || typeof s.familyStepDrafts !== 'object' || Array.isArray(s.familyStepDrafts)) s.familyStepDrafts = {};",
"  if(!Array.isArray(s.familyStepWorks)) s.familyStepWorks = [];\n  if(!s.familyStepDrafts || typeof s.familyStepDrafts !== 'object' || Array.isArray(s.familyStepDrafts)) s.familyStepDrafts = {};\n  if(!s.timeCapsule || typeof s.timeCapsule !== 'object' || Array.isArray(s.timeCapsule)) s.timeCapsule = { text:'', createdAt:0, updatedAt:0 };\n  s.timeCapsule = Object.assign({ text:'', createdAt:0, updatedAt:0 }, s.timeCapsule);\n  s.timeCapsule.text = String(s.timeCapsule.text || '');")

rep("      <div class=\"rxacts\">\n        <button class=\"btn sec sm\" id=\"go-read\">도움이 되는 글</button>\n        <button class=\"btn sec sm\" id=\"go-listen\">듣는 글</button>\n      </div>\n    </div>",
"      <div class=\"rxacts\">\n        <button class=\"btn sec sm\" id=\"go-read\">도움이 되는 글</button>\n        <button class=\"btn sec sm\" id=\"go-listen\">듣는 글</button>\n      </div>\n      <button class=\"btn sec sm hide\" id=\"go-capsule-panic\" style=\"width:100%;margin-top:7px\">초심 다시 보기</button>\n    </div>")

rep("      <button class=\"minitool\" id=\"tool-listen\">\n        <span class=\"ic\" data-ico=\"wave\"></span><b>듣는 글</b><span>마음에 도움이 되는 이야기</span>\n      </button>\n    </div>\n  </div>",
"      <button class=\"minitool\" id=\"tool-listen\">\n        <span class=\"ic\" data-ico=\"wave\"></span><b>듣는 글</b><span>마음에 도움이 되는 이야기</span>\n      </button>\n    </div>\n    <button class=\"toolcard\" id=\"tool-capsule\" style=\"margin-top:9px\">\n      <span class=\"ic\" data-ico=\"speak\"></span>\n      <span class=\"b\"><b>미래의 나에게</b><span id=\"tool-capsule-s\">회복을 시작한 마음을 남겨두기</span></span>\n      <span class=\"go\">열기</span>\n    </button>\n  </div>")

marker="""</section>\n\n<!-- ══════════ 자가점검 V7.1 ══════════ -->"""
capsule="""</section>\n\n<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->\n<section class=\"pg\" id=\"p-capsule\">\n  <div class=\"sp\" style=\"margin-bottom:11px\">\n    <h1 style=\"margin:0\">미래의 나에게</h1>\n    <button class=\"tiny\" style=\"color:var(--acc);font-weight:600\" id=\"capsule-back\">← 회복도구</button>\n  </div>\n  <div class=\"note\" style=\"margin-bottom:12px\">\n    회복을 시작한 날의 마음을 남겨두세요. 힘든 순간에 그때의 내가 지금의 나에게 해주고 싶은 말을 다시 볼 수 있습니다. <b>내용은 이 기기에만 저장</b>됩니다.\n  </div>\n\n  <div id=\"capsule-view\" class=\"hide\">\n    <div class=\"card\">\n      <h3>그날의 내가 지금의 나에게</h3>\n      <div class=\"quote\" id=\"capsule-message\" style=\"text-align:left;white-space:pre-wrap\"></div>\n      <p class=\"tiny\" id=\"capsule-meta\" style=\"margin:10px 1px 0\"></p>\n    </div>\n    <div id=\"capsule-manage\">\n      <button class=\"btn sec\" id=\"capsule-edit-btn\">수정하기</button>\n      <div style=\"height:8px\"></div>\n      <button class=\"btn ghost\" id=\"capsule-delete\">삭제</button>\n    </div>\n    <div id=\"capsule-panic-actions\" class=\"hide\">\n      <button class=\"btn\" id=\"capsule-urge\">충동 대응 계속하기</button>\n      <div style=\"height:8px\"></div>\n      <button class=\"btn ghost\" id=\"capsule-panic-back\">위기 도움으로 돌아가기</button>\n    </div>\n  </div>\n\n  <div id=\"capsule-edit\" class=\"hide\">\n    <div class=\"card\">\n      <h3>어떤 말을 남기고 싶나요?</h3>\n      <p class=\"muted\" style=\"margin:-4px 0 11px\">\n        왜 회복을 시작했는지, 다시 돌아가고 싶지 않은 이유, 힘든 날의 나에게 해주고 싶은 말을 자유롭게 적어보세요.\n      </p>\n      <textarea id=\"capsule-text\" maxlength=\"800\" style=\"min-height:190px\" placeholder=\"예: 내가 왜 여기까지 오게 되었는지 기억하자. 오늘 하루만 지나가도 된다. 힘들면 혼자 견디지 말고 사람에게 연락하자.\"></textarea>\n      <p class=\"tiny\" id=\"capsule-count\" style=\"text-align:right;margin:5px 1px 0\">0 / 800</p>\n    </div>\n    <button class=\"btn\" id=\"capsule-save\">이 말을 남겨두기</button>\n    <div style=\"height:8px\"></div>\n    <button class=\"btn ghost\" id=\"capsule-cancel\">취소</button>\n  </div>\n</section>\n\n<!-- ══════════ 자가점검 V7.1 ══════════ -->"""
rep(marker,capsule)

rep("  let tabP = (p === 'qa' || p === 'learn' || p === 'learn-topic' || p === 'workbook-list' || p === 'workbook' || p === 'screening' || p === 'screen-test' || p === 'habit' || p === 'habit-edit' || p === 'schedule' || p === 'life-schedule' || p === 'notify-schedule' || p === 'treatment') ? 'tools' : p;",
"  let tabP = (p === 'qa' || p === 'learn' || p === 'learn-topic' || p === 'workbook-list' || p === 'workbook' || p === 'screening' || p === 'screen-test' || p === 'habit' || p === 'habit-edit' || p === 'schedule' || p === 'life-schedule' || p === 'notify-schedule' || p === 'treatment' || p === 'capsule') ? 'tools' : p;")
rep("  if(p === 'habit-edit') drawHabitEdit();\n  if(p === 'schedule') drawScheduleHub();",
"  if(p === 'habit-edit') drawHabitEdit();\n  if(p === 'capsule') drawCapsule();\n  if(p === 'schedule') drawScheduleHub();")

rep("function drawPanic(){\n  const w = (S.types || []).map(k => URGEWORD[k]).filter(Boolean);\n  $('#pk-urge-t').textContent = w.length\n    ? w.join('·') + ' 생각이 올라와요'\n    : '충동이 올라와요';\n}",
"function drawPanic(){\n  const w = (S.types || []).map(k => URGEWORD[k]).filter(Boolean);\n  $('#pk-urge-t').textContent = w.length\n    ? w.join('·') + ' 생각이 올라와요'\n    : '충동이 올라와요';\n  const cp=$('#go-capsule-panic');\n  if(cp) cp.classList.toggle('hide', famMode() || !capsuleHas());\n}")

insert_before="""/* ══════════ 회복도구 · 중독 Q&A V6.5 ══════════ */"""
cap_js="""/* ══════════ 미래의 나에게 V8.2.0 ══════════\n   처음에는 텍스트만 저장합니다. 음성은 별도 단계에서 검토합니다.\n   개인 회복기록 S에 들어가므로 기존 JSON 백업에는 포함되지만 서버로 자동 전송되지 않습니다. */\nlet capsuleEditing=false;\nlet capsuleFrom='tools';\nfunction capsuleData(){\n  if(!S.timeCapsule || typeof S.timeCapsule!=='object' || Array.isArray(S.timeCapsule)) S.timeCapsule={text:'',createdAt:0,updatedAt:0};\n  S.timeCapsule=Object.assign({text:'',createdAt:0,updatedAt:0},S.timeCapsule);\n  S.timeCapsule.text=String(S.timeCapsule.text||'');\n  return S.timeCapsule;\n}\nfunction capsuleHas(){ return !!capsuleData().text.trim(); }\nfunction capsuleDate(ts){\n  if(!ts) return '';\n  const d=new Date(ts);\n  return d.getFullYear()+'. '+(d.getMonth()+1)+'. '+d.getDate()+'.';\n}\nfunction openCapsule(from,edit){\n  capsuleFrom=from==='panic'?'panic':'tools';\n  capsuleEditing=!!edit || !capsuleHas();\n  go('capsule');\n}\nfunction drawCapsule(){\n  const c=capsuleData(), has=!!c.text.trim();\n  if(!has) capsuleEditing=true;\n  const view=$('#capsule-view'), edit=$('#capsule-edit');\n  if(!view||!edit) return;\n  const back=$('#capsule-back');\n  if(back){\n    back.textContent=capsuleFrom==='panic'?'← 위기 도움':'← 회복도구';\n    back.onclick=()=>capsuleFrom==='panic'?go('panic'):go('tools');\n  }\n  view.classList.toggle('hide',capsuleEditing||!has);\n  edit.classList.toggle('hide',!capsuleEditing);\n  const manage=$('#capsule-manage'), pa=$('#capsule-panic-actions');\n  if(manage) manage.classList.toggle('hide',capsuleFrom==='panic');\n  if(pa) pa.classList.toggle('hide',capsuleFrom!=='panic');\n\n  if(has && !capsuleEditing){\n    $('#capsule-message').textContent=c.text;\n    $('#capsule-meta').textContent=(c.updatedAt?'마지막 수정 ':'처음 남긴 ')+capsuleDate(c.updatedAt||c.createdAt);\n    $('#capsule-edit-btn').onclick=()=>{ capsuleEditing=true; drawCapsule(); };\n    $('#capsule-delete').onclick=()=>{\n      modal('<h2>이 메시지를 삭제할까요?</h2><p class=\"muted\" style=\"margin:7px 0 14px\">삭제하면 복구할 수 없습니다. 필요하면 먼저 내 정보에서 기록을 내보내세요.</p><button class=\"btn danger\" id=\"capsule-delete-ok\">삭제</button><div style=\"height:8px\"></div><button class=\"btn ghost\" onclick=\"closeModal()\">취소</button>');\n      $('#capsule-delete-ok').onclick=()=>{ S.timeCapsule={text:'',createdAt:0,updatedAt:0}; save(); closeModal(); capsuleEditing=true; capsuleFrom='tools'; drawCapsule(); drawTools(); drawPanic(); toast('삭제했습니다.'); };\n    };\n    $('#capsule-urge').onclick=()=>go('urge');\n    $('#capsule-panic-back').onclick=()=>go('panic');\n  }\n\n  if(capsuleEditing){\n    const ta=$('#capsule-text'), cnt=$('#capsule-count');\n    ta.value=has?c.text:'';\n    const sync=()=>{ if(cnt) cnt.textContent=ta.value.length+' / 800'; };\n    ta.oninput=sync; sync();\n    $('#capsule-save').onclick=()=>{\n      const text=ta.value.trim();\n      if(!text){ toast('미래의 나에게 남길 말을 적어주세요.'); return; }\n      const now=Date.now();\n      S.timeCapsule={text:text,createdAt:c.createdAt||now,updatedAt:now};\n      save(); capsuleEditing=false; capsuleFrom='tools'; drawCapsule(); drawTools(); drawPanic(); toast('미래의 나에게 남겨두었습니다.');\n    };\n    const cancel=$('#capsule-cancel');\n    cancel.style.display=has?'block':'none';\n    cancel.onclick=()=>{ capsuleEditing=false; drawCapsule(); };\n  }\n  refreshIcons();\n}\n\n"""
rep(insert_before,cap_js+insert_before)

rep("  const m = $('#tool-qa-s');\n  if(m) m.textContent = '회복 Q&A · 총 ' + n + '문답';",
"  const m = $('#tool-qa-s');\n  if(m) m.textContent = '회복 Q&A · 총 ' + n + '문답';\n  const cap=$('#tool-capsule'), caps=$('#tool-capsule-s');\n  if(cap) cap.style.display=famMode()?'none':'flex';\n  if(caps) caps.textContent=capsuleHas()?'내가 남긴 메시지가 있습니다 · 힘들 때 다시 보기':'회복을 시작한 마음을 남겨두기';")

rep("$('#tool-habit').onclick = () => go('habit');\n$('#tool-schedule').onclick = () => go('schedule');",
"$('#tool-habit').onclick = () => go('habit');\n$('#tool-capsule').onclick = () => openCapsule('tools',false);\n$('#tool-schedule').onclick = () => go('schedule');")
rep("$('#pk-urge').onclick = () => go('urge');", "$('#pk-urge').onclick = () => go('urge');\n$('#go-capsule-panic').onclick = () => openCapsule('panic',false);")

p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
w=sw.read_text(encoding='utf-8')
assert "const APP_VERSION = 'V8.1.9';" in w
assert "const V = 'ohg-v819-habit-collapse';" in w
w=w.replace("const APP_VERSION = 'V8.1.9';","const APP_VERSION = 'V8.2.0';")
w=w.replace("const V = 'ohg-v819-habit-collapse';","const V = 'ohg-v820-future-self';")
sw.write_text(w,encoding='utf-8')
print('V8.2.0 future self text patch PASS')
