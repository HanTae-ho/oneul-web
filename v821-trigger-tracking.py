from pathlib import Path


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    return text.replace(old, new, 1)

p = Path('index.html')
s = p.read_text(encoding='utf-8')

s = replace_once(s,
'''    <span class="b"><b>몸이 이상해요</b>\n      <span>손떨림·식은땀·경련·환각이 있다면 응급 상황입니다</span></span>''',
'''    <span class="b"><b>몸이 이상해요</b>\n      <span>손떨림·식은땀·경련·환각은 응급상황일 수 있습니다</span></span>''',
'urgent-copy')

s = replace_once(s,
'''  <button class="btn" id="ur-start">5분만 같이 버텨보기</button>\n  <div style="height:9px"></div>\n  <button class="btn sec" id="ur-read">도움이 되는 글 읽기</button>''',
'''  <button class="btn" id="ur-start">5분만 같이 버텨보기</button>\n  <div style="height:9px"></div>\n\n  <button class="btn ghost" id="ur-track-toggle" aria-expanded="false">상황·촉발 기록 (선택) · 눌러서 기록</button>\n  <div id="ur-track" class="hide" style="margin-top:9px">\n    <div class="card">\n      <h3>지금 어떤 상황인가요? <span class="tiny" style="font-weight:400">(선택)</span></h3>\n      <p class="muted" style="margin:-4px 0 11px">해당하는 것을 골라주세요. 정확한 위치는 저장하지 않습니다.</p>\n      <div class="opts" id="ur-ctx"></div>\n      <div class="sep"></div>\n      <h3>무엇이 촉발했나요? <span class="tiny" style="font-weight:400">(선택)</span></h3>\n      <p class="muted" style="margin:-4px 0 11px">여러 개를 골라도 되고, 건너뛰어도 됩니다.</p>\n      <div class="opts" id="ur-trg"></div>\n    </div>\n  </div>\n\n  <button class="btn sec" id="ur-read">도움이 되는 글 읽기</button>''',
'urge-tracking-ui')

s = replace_once(s, "const BUILD = 'V8.2.0';", "const BUILD = 'V8.2.1';", 'build-version')
s = replace_once(s, 'const DATA_SCHEMA = 3;', 'const DATA_SCHEMA = 4;', 'data-schema')

s = replace_once(s,
'''/* ══════════ 충동 대응 ══════════ */\nlet urge = { before: 5, after: null, thoughts: [], start: 0, type: null };\n\nfunction drawUrge(){''',
'''/* ══════════ 충동 대응 ══════════ */\n/* Trigger Tracking V2 — 정확한 위치나 자유서술 대신 범주만 기기 안에 저장합니다.\n   위기 대응을 늦추지 않도록 선택 기록은 기본 접힘이며 건너뛰어도 됩니다. */\nconst URGE_CONTEXTS = ['집','직장·학교','이동 중','혼자','사람들과 함께','모임·약속 중'];\nconst URGE_TRIGGERS = ['갈등','외로움','지루함','스트레스','돈 문제','과거 기억','중독 관련 노출','특정 사람'];\nlet urgeTrackOpen = false;\nlet urge = { before: 5, after: null, thoughts: [], contexts: [], triggers: [], start: 0, type: null };\n\nfunction drawUrgeTrack(){\n  const ctx=$('#ur-ctx'), trg=$('#ur-trg');\n  if(!ctx || !trg) return;\n  ctx.innerHTML=''; trg.innerHTML='';\n  URGE_CONTEXTS.forEach(x=>{\n    const b=el('button','opt'+(urge.contexts.indexOf(x)>=0?' on':''),x);\n    b.onclick=()=>{\n      urge.touched=true;\n      const i=urge.contexts.indexOf(x);\n      if(i<0) urge.contexts.push(x); else urge.contexts.splice(i,1);\n      drawUrgeTrack();\n    };\n    ctx.appendChild(b);\n  });\n  URGE_TRIGGERS.forEach(x=>{\n    const b=el('button','opt'+(urge.triggers.indexOf(x)>=0?' on':''),x);\n    b.onclick=()=>{\n      urge.touched=true;\n      const i=urge.triggers.indexOf(x);\n      if(i<0) urge.triggers.push(x); else urge.triggers.splice(i,1);\n      drawUrgeTrack();\n    };\n    trg.appendChild(b);\n  });\n}\nfunction setUrgeTrackOpen(open){\n  urgeTrackOpen=!!open;\n  const box=$('#ur-track'), btn=$('#ur-track-toggle');\n  if(box) box.classList.toggle('hide',!urgeTrackOpen);\n  if(btn){\n    btn.setAttribute('aria-expanded',urgeTrackOpen?'true':'false');\n    btn.textContent=urgeTrackOpen?'상황·촉발 기록 접기':'상황·촉발 기록 (선택) · 눌러서 기록';\n  }\n  if(urgeTrackOpen) drawUrgeTrack();\n}\n\nfunction drawUrge(){''',
'urge-tracking-state')

s = replace_once(s,
'''  urge = { before: 5, after: null, thoughts: [], start: 0, touched: false, saved: false,\n           type: S.types[0] || 'etc' };\n  $('#ur-r').value = 5;''',
'''  urge = { before: 5, after: null, thoughts: [], contexts: [], triggers: [], start: 0, touched: false, saved: false,\n           type: S.types[0] || 'etc' };\n  setUrgeTrackOpen(false);\n  $('#ur-r').value = 5;''',
'urge-reset')

s = replace_once(s,
'''$('#ur-start').onclick = () => { urge.touched = true; startTimer(0); };\n\n/* ★ 예전에는 이 두 갈래가 저장 없이 화면만 넘겼습니다.''',
'''$('#ur-start').onclick = () => { urge.touched = true; startTimer(0); };\n$('#ur-track-toggle').onclick = () => setUrgeTrackOpen(!urgeTrackOpen);\n\n/* ★ 예전에는 이 두 갈래가 저장 없이 화면만 넘겼습니다.''',
'track-toggle-handler')

s = replace_once(s,
'''    sec: urge.start ? Math.round((Date.now() - urge.start) / 1000) : 0,\n    th: urge.thoughts.slice(),\n    ok: urge.ok ? 1 : 0''',
'''    sec: urge.start ? Math.round((Date.now() - urge.start) / 1000) : 0,\n    th: urge.thoughts.slice(),\n    ctx: urge.contexts.slice(),\n    trg: urge.triggers.slice(),\n    ok: urge.ok ? 1 : 0''',
'save-trigger-fields')

p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
w = replace_once(w, "const APP_VERSION = 'V8.2.0';", "const APP_VERSION = 'V8.2.1';", 'sw-version')
w = replace_once(w, "const V = 'ohg-v820-future-self';", "const V = 'ohg-v821-trigger-tracking';", 'sw-cache')
sw.write_text(w, encoding='utf-8')

print('V8.2.1 Trigger Tracking V2 patch applied')
