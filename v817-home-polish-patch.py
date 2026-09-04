from pathlib import Path


def once(s, old, new, label):
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1, got {n}')
    return s.replace(old, new, 1)

p = Path('index.html')
s = p.read_text(encoding='utf-8')

s = once(s,
    "  .today-sleepq{margin-top:8px;padding-top:11px;border-top:1px solid var(--line)}.today-sleepq p{margin:0 0 8px;font-size:12px;color:var(--dim)}\n",
    "  .today-sleepq{margin-top:8px;padding-top:11px;border-top:1px solid var(--line)}.today-sleepq p{margin:0 0 8px;font-size:12px;color:var(--dim)}\n"
    "  /* V8.1.7 — 오늘 일정이 많으면 홈은 5개까지만 보여주고 필요할 때 펼칩니다. */\n"
    "  .today-more{width:100%;margin-top:5px;padding:9px 4px;border-top:1px dashed var(--line);text-align:center;font-size:12px;font-weight:700;color:var(--acc);background:transparent}\n",
    'today more css')

s = once(s,
    "  cal:   '<rect x=\"3.5\" y=\"5.2\" width=\"17\" height=\"15.3\" rx=\"2.5\"/><path d=\"M7.2 3.5v3.4M16.8 3.5v3.4M3.5 9.2h17\"/><path d=\"M7.5 13h2M12 13h2M16.5 13h.1M7.5 16.7h2M12 16.7h2\"/>',\n  bell:",
    "  cal:   '<rect x=\"3.5\" y=\"5.2\" width=\"17\" height=\"15.3\" rx=\"2.5\"/><path d=\"M7.2 3.5v3.4M16.8 3.5v3.4M3.5 9.2h17\"/><path d=\"M7.5 13h2M12 13h2M16.5 13h.1M7.5 16.7h2M12 16.7h2\"/>',\n  sleep: '<path d=\"M19.8 15.2A8.4 8.4 0 1 1 10.1 4.1a6.8 6.8 0 0 0 9.7 11.1z\"/><path d=\"M16.2 4.4h3.2l-3.2 3.4h3.2\"/>',\n  bell:",
    'sleep icon')

s = once(s, "const BUILD = 'V8.1.6';", "const BUILD = 'V8.1.7';", 'build version')

s = once(s,
    "function homeTimeKey(v){\n",
    "let homeTodayExpanded=false;\nfunction homeTimeKey(v){\n",
    'home expansion state')

s = once(s,
    "      items.push({kind:'med',id:m.s,time:m.t||'',label:slot.l+' 약',sub:'복약',done:ok,action:1});",
    "      const medLabel=/약$/.test(String(slot.l||''))?slot.l:slot.l+' 약';\n      items.push({kind:'med',id:m.s,time:m.t||'',label:medLabel,sub:'복약',done:ok,action:1});",
    'med label')

s = once(s,
    "  let html='<div class=\"today-home\"><div class=\"sp\" style=\"align-items:flex-start\"><div><h3>오늘 일정</h3>'+\n    (actionable?'<div class=\"today-summary\">'+completed+' / '+actionable+' 완료</div>':'')+\n    '</div><button class=\"tiny link\" id=\"home-today-manage\">일정 관리</button></div>';\n  items.forEach((x,i)=>{\n    const icon=(x.kind==='sleep'||x.kind==='visit')?'cal':(x.done?'check':'box');",
    "  const homeLimit=5, canFold=items.length>homeLimit;\n  const shown=(canFold&&!homeTodayExpanded)?items.slice(0,homeLimit):items;\n  let html='<div class=\"today-home\"><div class=\"sp\" style=\"align-items:flex-start\"><div><h3>오늘 일정</h3>'+\n    (actionable?'<div class=\"today-summary\">오늘 실천 '+completed+' / '+actionable+' 완료</div>':'')+\n    '</div><button class=\"tiny link\" id=\"home-today-manage\">일정 관리</button></div>';\n  shown.forEach((x,i)=>{\n    const icon=x.kind==='sleep'?'sleep':(x.kind==='visit'?'cal':(x.done?'check':'box'));",
    'summary, folding and icons')

s = once(s,
    "  html+=visitHtml;\n  if(askSleep){",
    "  if(canFold){\n    const hidden=Math.max(0,items.length-homeLimit);\n    html+='<button class=\"today-more\" id=\"home-today-more\">'+(homeTodayExpanded?'간단히 보기':'전체 보기 · '+hidden+'개 더')+'</button>';\n  }\n  html+=visitHtml;\n  if(askSleep){",
    'fold button')

s = once(s,
    "  const manage=$('#home-today-manage'); if(manage) manage.onclick=()=>go('schedule');\n  const visit=$('#home-today-visit');",
    "  const manage=$('#home-today-manage'); if(manage) manage.onclick=()=>go('schedule');\n  const more=$('#home-today-more'); if(more) more.onclick=()=>{homeTodayExpanded=!homeTodayExpanded;drawTodayScheduleHome();};\n  const visit=$('#home-today-visit');",
    'fold handler')

p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
w = once(w, "const APP_VERSION = 'V8.1.6';", "const APP_VERSION = 'V8.1.7';", 'sw app version')
w = once(w, "const V = 'ohg-v816-home-today';", "const V = 'ohg-v817-home-polish';", 'sw cache version')
sw.write_text(w, encoding='utf-8')
print('V8.1.7 home schedule polish patch PASS')
