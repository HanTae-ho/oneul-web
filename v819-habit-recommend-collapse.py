from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,n=1):
    global s
    c=s.count(old)
    assert c==n, f'expected {n} occurrences, got {c}: {old[:120]}'
    s=s.replace(old,new,n)

rep("const BUILD = 'V8.1.8';", "const BUILD = 'V8.1.9';")

rep("  <div class=\"habit-head\"><h2>추천 습관</h2><span class=\"tiny\">예시를 복사해 사용합니다</span></div>\n  <div id=\"habit-templates\"></div>",
"  <button class=\"habit-recommend-toggle\" id=\"habit-template-toggle\" type=\"button\" aria-expanded=\"false\">\n    <span class=\"txt\"><b>추천 습관 <span id=\"habit-template-count\">8개</span></b><small id=\"habit-template-hint\">회복에 도움이 되는 기본 습관 · 눌러서 보기</small></span>\n    <span class=\"chev\" aria-hidden=\"true\">⌄</span>\n  </button>\n  <div id=\"habit-templates\" class=\"hide\"></div>")

rep("let habitEditState = null;", "let habitEditState = null;\nlet habitTemplatesOpen = false; /* V8.1.9: 추천 습관은 기본 접힘. 개인 습관 데이터에는 저장하지 않습니다. */")

old="  tmp.innerHTML=HABIT_TEMPLATES.map(t=>'<div class=\\\"habit-template\\\"><b>'+esc(t.name)+'</b><p>'+esc(habitPeriodText(t))+' · '+esc(habitFreqText(t))+' · '+esc(t.check)+' · '+esc(t.time)+' 알림</p><div class=\\\"rowbtn\\\"><button class=\\\"btn sec sm\\\" data-template-use=\\\"'+t.id+'\\\">그대로 사용</button><button class=\\\"btn ghost sm\\\" data-template-edit=\\\"'+t.id+'\\\">수정해서 사용</button></div></div>').join('');"
new=old+"\n  const tt=$('#habit-template-toggle'), tc=$('#habit-template-count'), th=$('#habit-template-hint');\n  if(tc) tc.textContent=HABIT_TEMPLATES.length+'개';\n  const syncHabitTemplates=()=>{\n    tmp.classList.toggle('hide',!habitTemplatesOpen);\n    if(tt){ tt.classList.toggle('on',habitTemplatesOpen); tt.setAttribute('aria-expanded',habitTemplatesOpen?'true':'false'); }\n    if(th) th.textContent=habitTemplatesOpen?'추천 예시를 접습니다':'회복에 도움이 되는 기본 습관 · 눌러서 보기';\n  };\n  syncHabitTemplates();\n  if(tt) tt.onclick=()=>{ habitTemplatesOpen=!habitTemplatesOpen; syncHabitTemplates(); };"
rep(old,new)

css="""
  /* V8.1.9 — 추천 습관은 필요할 때만 펼칩니다. 내 습관과 새 습관 버튼은 항상 보입니다. */
  .habit-recommend-toggle{width:100%;display:flex;align-items:center;gap:12px;margin:17px 0 9px;padding:13px 14px;text-align:left;background:var(--panel);border:1px solid var(--line);border-radius:14px;color:var(--tx)}
  .habit-recommend-toggle .txt{flex:1;min-width:0}.habit-recommend-toggle b{display:block;font-size:15px;font-weight:700}.habit-recommend-toggle b span{font-size:12px;color:var(--acc);margin-left:4px}
  .habit-recommend-toggle small{display:block;margin-top:3px;font-size:12px;line-height:1.45;color:var(--dim);font-weight:400}.habit-recommend-toggle .chev{flex:none;color:var(--faint);font-size:18px;line-height:1;transition:transform .18s ease}
  .habit-recommend-toggle.on{border-color:var(--acc2)}.habit-recommend-toggle.on .chev{transform:rotate(180deg);color:var(--acc)}
"""
assert css.strip() not in s
rep("</style>",css+"\n</style>")

p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
w=sw.read_text(encoding='utf-8')
assert "const APP_VERSION = 'V8.1.8';" in w
assert "const V = 'ohg-v818-pre-social';" in w
w=w.replace("const APP_VERSION = 'V8.1.8';","const APP_VERSION = 'V8.1.9';")
w=w.replace("const V = 'ohg-v818-pre-social';","const V = 'ohg-v819-habit-collapse';")
sw.write_text(w,encoding='utf-8')
print('V8.1.9 habit recommendation collapse patch PASS')
