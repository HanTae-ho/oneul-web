from pathlib import Path

idx=Path('index.html')
sw=Path('sw.js')
s=idx.read_text(encoding='utf-8')
swt=sw.read_text(encoding='utf-8')

assert "const BUILD = 'V8.2.13';" in s
s=s.replace("const BUILD = 'V8.2.13';","const BUILD = 'V8.2.14';",1)

# Small discoverability hint for completed items.
css_anchor="  .today-more{width:100%;margin-top:5px;padding:9px 4px;border-top:1px dashed var(--line);text-align:center;font-size:12px;font-weight:700;color:var(--acc);background:transparent}\n"
assert css_anchor in s
s=s.replace(css_anchor,css_anchor+"  .today-edit-hint{margin-top:8px;padding-top:8px;border-top:1px dashed var(--line);font-size:11.5px;line-height:1.45;color:var(--dim)}\n",1)

# Mark completion state for interaction/accessibility.
old_btn="    const btn=x.action?'<button class=\"tcheck'+(x.done?' on':'')+'\" data-today-kind=\"'+x.kind+'\" data-today-id=\"'+esc(x.id)+'\">'+ico(icon)+'</button>':'<span class=\"tcheck static\">'+ico(icon)+'</span>';"
assert old_btn in s
new_btn="    const btn=x.action?'<button class=\"tcheck'+(x.done?' on':'')+'\" data-today-kind=\"'+x.kind+'\" data-today-id=\"'+esc(x.id)+'\" data-today-done=\"'+(x.done?'1':'0')+'\" aria-label=\"'+esc(x.label+(x.done?' 완료. 길게 눌러 수정':' 완료로 표시'))+'\">'+ico(icon)+'</button>':'<span class=\"tcheck static\">'+ico(icon)+'</span>';"
s=s.replace(old_btn,new_btn,1)

# Show the hint only when there is at least one editable completed item.
fold_anchor="  if(canFold){\n    const hidden=Math.max(0,items.length-homeLimit);\n    html+='<button class=\"today-more\" id=\"home-today-more\">'+(homeTodayExpanded?'간단히 보기':'전체 보기 · '+hidden+'개 더')+'</button>';\n  }\n  html+=visitHtml;"
assert fold_anchor in s
fold_new="  if(canFold){\n    const hidden=Math.max(0,items.length-homeLimit);\n    html+='<button class=\"today-more\" id=\"home-today-more\">'+(homeTodayExpanded?'간단히 보기':'전체 보기 · '+hidden+'개 더')+'</button>';\n  }\n  if(items.some(x=>x.action&&x.done)) html+='<div class=\"today-edit-hint\">잘못 체크했다면 완료 표시를 길게 눌러 수정할 수 있어요.</div>';\n  html+=visitHtml;"
s=s.replace(fold_anchor,fold_new,1)

# Replace one-way completion click handler with one-tap-complete / long-press-undo.
old_handler="""  box.querySelectorAll('[data-today-kind]').forEach(b=>b.onclick=()=>{\n    if(b.dataset.todayKind==='habit'){\n      const h=habitList().find(x=>x.id===b.dataset.todayId); if(h) habitToggle(h,d);\n    }else if(b.dataset.todayKind==='med'){\n      S.medLog=S.medLog||[]; if(todayRec(S.medLog).map(x=>x.n).indexOf(b.dataset.todayId)<0) S.medLog.push({t:Date.now(),n:b.dataset.todayId});\n    }else if(b.dataset.todayKind==='eat'){\n      S.eatLog=S.eatLog||[]; if(todayRec(S.eatLog).map(x=>x.n).indexOf(b.dataset.todayId)<0) S.eatLog.push({t:Date.now(),n:b.dataset.todayId});\n    }\n    save(); drawTodayScheduleHome(); drawTools();\n  });\n"""
assert old_handler in s
new_handler="""  function removeTodayNamed(list,id){\n    return (Array.isArray(list)?list:[]).filter(r=>!(ymd(r.t)===d && r.n===id));\n  }\n  function completeToday(kind,id){\n    if(kind==='habit'){\n      const h=habitList().find(x=>x.id===id); if(h && !habitDoneOn(h,d)) habitToggle(h,d);\n    }else if(kind==='med'){\n      S.medLog=S.medLog||[]; if(todayRec(S.medLog).map(x=>x.n).indexOf(id)<0) S.medLog.push({t:Date.now(),n:id});\n    }else if(kind==='eat'){\n      S.eatLog=S.eatLog||[]; if(todayRec(S.eatLog).map(x=>x.n).indexOf(id)<0) S.eatLog.push({t:Date.now(),n:id});\n    }\n    save(); drawTodayScheduleHome(); drawTools();\n  }\n  function undoToday(kind,id){\n    if(kind==='med'){\n      if(!confirm('복약 완료 기록을 취소할까요?\\n실제로 복용하지 않았거나 잘못 체크한 경우에만 취소하세요.')) return false;\n      S.medLog=removeTodayNamed(S.medLog,id);\n    }else if(kind==='eat'){\n      S.eatLog=removeTodayNamed(S.eatLog,id);\n    }else if(kind==='habit'){\n      const h=habitList().find(x=>x.id===id); if(h && habitDoneOn(h,d)) habitToggle(h,d);\n    }else return false;\n    save();\n    if(navigator.vibrate) try{navigator.vibrate(25);}catch(e){}\n    drawTodayScheduleHome(); drawTools(); toast('오늘 완료 기록을 수정했습니다.');\n    return true;\n  }\n  box.querySelectorAll('[data-today-kind]').forEach(b=>{\n    let hold=0, held=false;\n    const clearHold=()=>{ if(hold){ clearTimeout(hold); hold=0; } };\n    b.oncontextmenu=e=>e.preventDefault();\n    b.addEventListener('pointerdown',()=>{\n      held=false;\n      if(b.dataset.todayDone!=='1') return;\n      clearHold();\n      hold=setTimeout(()=>{ hold=0; held=undoToday(b.dataset.todayKind,b.dataset.todayId); },650);\n    });\n    b.addEventListener('pointerup',clearHold);\n    b.addEventListener('pointercancel',clearHold);\n    b.onclick=e=>{\n      if(held){ held=false; e.preventDefault(); return; }\n      if(b.dataset.todayDone==='1'){ toast('완료 기록은 길게 눌러 수정할 수 있어요.'); return; }\n      completeToday(b.dataset.todayKind,b.dataset.todayId);\n    };\n  });\n"""
s=s.replace(old_handler,new_handler,1)

assert "const APP_VERSION = 'V8.2.13';" in swt
assert "const V = 'ohg-v8213-smart-nav-abc';" in swt
swt=swt.replace("const APP_VERSION = 'V8.2.13';","const APP_VERSION = 'V8.2.14';",1)
swt=swt.replace("const V = 'ohg-v8213-smart-nav-abc';","const V = 'ohg-v8214-home-longpress-edit';",1)

idx.write_text(s,encoding='utf-8')
sw.write_text(swt,encoding='utf-8')
print('V8.2.14 home long-press edit patch applied')
