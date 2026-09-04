from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

def sub1(pattern,repl,label,flags=0):
    global s
    s2,n=re.subn(pattern,repl,s,count=1,flags=flags)
    if n!=1: raise SystemExit(f'{label}: expected 1, got {n}')
    s=s2

# 1. Habit card becomes a real feature.
once('''      <button class="practicecard habit soon" id="tool-habit">\n        <span class="ic" data-ico="sprout"></span>\n        <span class="b"><b>습관</b><span>매일 반복할 작은 실천</span><small>준비 중</small></span>\n      </button>''','''      <button class="practicecard habit" id="tool-habit">\n        <span class="ic" data-ico="sprout"></span>\n        <span class="b"><b>습관</b><span id="tool-habit-s">추천 습관과 내 습관 관리</span><small>열기</small></span>\n      </button>''','habit card')

# 2. Habit UI CSS.
css_anchor='''  .schedulecard .go{font-size:18px;color:var(--faint)}\n  @media(max-width:350px){.learnmini{grid-template-columns:1fr}.minitool{min-height:0;flex-direction:row;text-align:left;gap:10px;padding:12px}.minitool .ic{margin:0;flex:none}.minitool b{min-width:70px}.minitool span{margin:0;flex:1}.practicegrid,.checkmini{grid-template-columns:1fr}.practicecard{min-height:0}}\n'''
css_add=css_anchor+'''  /* V8.1.5 — 습관: 추천 예시를 복사해 쓰고, 내 습관은 자유롭게 수정합니다. */\n  .habit-head{display:flex;align-items:flex-end;justify-content:space-between;gap:10px;margin:17px 0 9px}.habit-head h2{margin:0!important;color:var(--tx)!important;font-weight:700!important}.habit-list{display:grid;gap:9px}.habit-card{background:var(--panel);border:1px solid var(--line);border-radius:15px;padding:14px}.habit-card.done{opacity:.72}.habit-card .top{display:flex;align-items:flex-start;gap:10px}.habit-card .top .grow b{display:block;font-size:15.5px}.habit-card .meta{font-size:12px;color:var(--dim);margin-top:3px;line-height:1.5}.habit-card .checkline{display:flex;align-items:center;gap:8px;margin-top:11px;padding-top:10px;border-top:1px solid var(--line)}.habit-card .checkline button{width:31px;height:31px;border-radius:9px;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--acc);background:var(--bg)}.habit-card .checkline button.on{background:var(--acc);color:#fff;border-color:var(--acc)}.habit-card .checkline span{flex:1;font-size:13px;line-height:1.45}.habit-actions{display:flex;gap:7px;margin-top:10px}.habit-actions .btn{margin:0;width:auto;flex:1;padding:8px 7px;font-size:12px}.habit-template{background:var(--bg2);border:1px solid var(--line);border-radius:14px;padding:13px;margin-bottom:8px}.habit-template b{font-size:14.5px}.habit-template p{margin:3px 0 9px;font-size:12px;color:var(--dim);line-height:1.5}.habit-template .rowbtn{display:flex;gap:7px}.habit-template .rowbtn .btn{margin:0;padding:8px 7px;font-size:12px}.habit-edit .field{margin-bottom:15px}.habit-edit .field>label{display:block;font-size:13px;font-weight:700;margin-bottom:6px}.habit-edit .opts{gap:6px}.habit-edit .opt{padding:8px 10px;font-size:12.5px}.weekday-opts{display:grid!important;grid-template-columns:repeat(7,minmax(0,1fr));gap:5px!important}.weekday-opts .opt{padding:8px 2px;justify-content:center}.habit-home{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:14px;margin-bottom:12px}.habit-home h3{margin:0 0 9px}.habit-home-row{display:flex;align-items:center;gap:9px;padding:8px 0;border-top:1px solid var(--line)}.habit-home-row:first-of-type{border-top:0}.habit-home-row .hcheck{width:31px;height:31px;flex:none;border-radius:9px;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--acc)}.habit-home-row .hcheck.on{background:var(--acc);color:#fff;border-color:var(--acc)}.habit-home-row .txt{flex:1;min-width:0}.habit-home-row .txt b{display:block;font-size:13.5px}.habit-home-row .txt span{display:block;font-size:11.5px;color:var(--dim);margin-top:1px}.habit-home-row .time{font-size:11.5px;color:var(--faint);white-space:nowrap}\n'''
once(css_anchor,css_add,'habit css')

# 3. Habit pages before schedule hub.
anchor='<!-- ══════════ 일정·알림 허브 V8.1.4 ══════════ -->\n'
habit_pages='''<!-- ══════════ 습관 V8.1.5 ══════════ -->\n<section class="pg" id="p-habit">\n  <div class="sp" style="margin-bottom:8px">\n    <h1 style="margin:0">습관</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('tools')">← 회복도구</button>\n  </div>\n  <p class="muted" style="margin:0 0 14px">작은 실천을 정하고 오늘 했는지만 체크합니다. 추천 예시는 그대로 쓰거나 내 방식으로 바꿀 수 있습니다.</p>\n  <div class="habit-head"><h2>내 습관</h2><button class="btn sec sm" style="width:auto;margin:0" id="habit-new">+ 새 습관</button></div>\n  <div id="habit-my" class="habit-list"></div>\n  <div class="habit-head"><h2>추천 습관</h2><span class="tiny">예시를 복사해 사용합니다</span></div>\n  <div id="habit-templates"></div>\n</section>\n\n<section class="pg" id="p-habit-edit">\n  <div class="sp" style="margin-bottom:8px">\n    <h1 style="margin:0" id="habit-edit-title">습관 만들기</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('habit')">← 습관</button>\n  </div>\n  <div id="habit-edit-body" class="habit-edit"></div>\n</section>\n\n'''
once(anchor,habit_pages+anchor,'habit pages')

# 4. Home container for today's habits.
once('''  <div id="home-alert"></div>''','''  <div id="home-habits"></div>\n  <div id="home-alert"></div>''','home habits container')

# 5. Schedule copy: notification includes habits and direct native entry.
s=s.replace('생활 · 치료 알림 관리','습관 · 생활 · 치료 알림 관리')
s=s.replace('생활 일정과 치료 일정에서 정한 시간을 실제 알림으로 연결합니다.','습관과 생활·치료 일정에서 정한 시간을 실제 알림으로 연결합니다.')
s=s.replace('위험시간 · 복약 · 식사 · 잠 · 외래 알림을 한곳에서 관리합니다.','습관 · 위험시간 · 복약 · 식사 · 잠 · 외래 알림을 한곳에서 관리합니다.')

# 6. Navigation maps habit pages to Recovery Tools.
old="let tabP = (p === 'qa' || p === 'learn' || p === 'learn-topic' || p === 'workbook-list' || p === 'workbook' || p === 'screening' || p === 'screen-test' || p === 'schedule' || p === 'life-schedule' || p === 'notify-schedule' || p === 'treatment') ? 'tools' : p;"
new="let tabP = (p === 'qa' || p === 'learn' || p === 'learn-topic' || p === 'workbook-list' || p === 'workbook' || p === 'screening' || p === 'screen-test' || p === 'habit' || p === 'habit-edit' || p === 'schedule' || p === 'life-schedule' || p === 'notify-schedule' || p === 'treatment') ? 'tools' : p;"
once(old,new,'tab mapping')
once("  if(p === 'tools') drawTools();\n", "  if(p === 'tools') drawTools();\n  if(p === 'habit') drawHabits();\n  if(p === 'habit-edit') drawHabitEdit();\n", 'go habit draw')

# 7. Habit click + notification shortcut.
once("$('#tool-habit').onclick = () => toast('습관 기능은 준비 중입니다.');", "$('#tool-habit').onclick = () => go('habit');", 'habit click')
once("$('#schedule-notify').onclick = () => go('notify-schedule');", "$('#schedule-notify').onclick = () => { if(nativeAndroidApp()) openNativeReminderSettings(); else go('notify-schedule'); };", 'notify direct')

# 8. Treatment master switch removed; individual med/outpatient switches remain.
once("    S.treat = {on:0,medOn:0,outpatientOn:0,lastVisit:'',rxDays:0,intervalDays:0,nextVisit:'',alertD3:1,alertD1:1,alertDay:1,alertTime:'09:00'};", "    S.treat = {on:1,medOn:0,outpatientOn:0,lastVisit:'',rxDays:0,intervalDays:0,nextVisit:'',alertD3:1,alertD1:1,alertDay:1,alertTime:'09:00'};", 'treat init')
once("  if(S.treat.intervalDays == null || isNaN(+S.treat.intervalDays)) S.treat.intervalDays = Math.max(0, parseInt(S.treat.rxDays,10) || 0);\n  return S.treat;", "  if(S.treat.intervalDays == null || isNaN(+S.treat.intervalDays)) S.treat.intervalDays = Math.max(0, parseInt(S.treat.rxDays,10) || 0);\n  S.treat.on = 1; /* V8.1.5: 상위 사용 스위치는 없애고 복약·외래를 각각 켭니다. */\n  return S.treat;", 'force treat on')
s=s.replace("function treatmentMedOn(){ const t=treatmentCfg(); return !famMode() && !!t.on && !!t.medOn; }","function treatmentMedOn(){ const t=treatmentCfg(); return !famMode() && !!t.medOn; }")
s=s.replace("const t=treatmentCfg(); if(!t.on||!t.outpatientOn) return '';","const t=treatmentCfg(); if(!t.outpatientOn) return '';")
s=s.replace("if(!t.on || !t.outpatientOn) return;","if(!t.outpatientOn) return;")
s=s.replace("const visitActive = !famMode() && tr.on && tr.outpatientOn &&", "const visitActive = !famMode() && tr.outpatientOn &&")
s=s.replace("const nTreat = !famMode() && t.on ? ((t.medOn && (S.meds||[]).length ? 1 : 0) + (t.outpatientOn ? 1 : 0)) : 0;", "const nTreat = !famMode() ? ((t.medOn && (S.meds||[]).length ? 1 : 0) + (t.outpatientOn ? 1 : 0)) : 0;")
s=s.replace("if(t.on && t.medOn && (S.meds||[]).length) parts.push('복약 ' + S.meds.length + '회');", "if(t.medOn && (S.meds||[]).length) parts.push('복약 ' + S.meds.length + '회');")
s=s.replace("if(t.on && t.outpatientOn){ const v=treatmentVisitLabel(); parts.push(v || '외래 일정 사용'); }", "if(t.outpatientOn){ const v=treatmentVisitLabel(); parts.push(v || '외래 일정 사용'); }")

master_pat=r'''  master\.innerHTML='<div class=\\?"card\\?"><h3>치료 일정 사용</h3>.*?\n    return;\n  \}\n\n(?=  body\.innerHTML=)'''
# Pattern operates on real quotes, not escaped JSON.
master_pat=r'''  master\.innerHTML='<div class="card"><h3>치료 일정 사용</h3>.*?\n    return;\n  \}\n\n(?=  body\.innerHTML=)'''
sub1(master_pat,"  master.innerHTML='';\n  t.on=1;\n\n",'remove treatment master',re.S)

once("    '<div class=\"card\"><h3>외래 관리</h3><p class=\"muted\" style=\"margin:-4px 0 11px\">이번 외래일과 외래 주기를 기준으로 다음 외래일을 자동 계산하고 같은 간격으로 반복합니다. 실제 예약일이 다르면 직접 수정할 수 있습니다.</p><div class=\"opts\" id=\"treat-out-on\"></div><div id=\"treat-out-settings\" style=\"margin-top:13px\"></div></div>'+\n    '<div class=\"note\" id=\"treat-native-note\"></div>';", "    '<div class=\"card\"><h3>외래 관리</h3><p class=\"muted\" style=\"margin:-4px 0 11px\">이번 외래일과 외래 주기를 기준으로 다음 외래일을 자동 계산하고 같은 간격으로 반복합니다. 실제 예약일이 다르면 직접 수정할 수 있습니다.</p><div class=\"opts\" id=\"treat-out-on\"></div><div id=\"treat-out-settings\" style=\"margin-top:13px\"></div></div>';", 'remove treatment native note html')
sub1(r'''\n  const nn=\$\('#treat-native-note'\);\n  if\(nativeAndroidApp\(\)\)\{.*?\n  \} else nn\.innerHTML=.*?;\n''','\n','remove treatment native note logic',re.S)

# 9. Habit functions and data model.
habit_js=r'''/* ══════════ 습관 V8.1.5 ══════════ */
const HABIT_TEMPLATES = [
  {id:'meeting100',name:'모임 백일작전',days:100,freq:'daily',weekdays:[0,1,2,3,4,5,6],check:'오늘 모임에 참여했습니다',notify:1,time:'18:30'},
  {id:'recovery21',name:'회복 21일 시작하기',days:21,freq:'daily',weekdays:[0,1,2,3,4,5,6],check:'오늘 회복을 위한 한 가지를 실천했습니다',notify:1,time:'20:00'},
  {id:'peer66',name:'회복 동료에게 연락하기',days:66,freq:'daily',weekdays:[0,1,2,3,4,5,6],check:'오늘 회복 동료에게 연락했습니다',notify:1,time:'19:00'},
  {id:'walk21',name:'10분 걷기',days:21,freq:'daily',weekdays:[0,1,2,3,4,5,6],check:'오늘 10분 이상 걸었습니다',notify:1,time:'17:30'},
  {id:'thanks21',name:'감사 3가지 적기',days:21,freq:'daily',weekdays:[0,1,2,3,4,5,6],check:'오늘 감사한 것 3가지를 적었습니다',notify:1,time:'21:00'},
  {id:'morning66',name:'아침 회복 다짐',days:66,freq:'daily',weekdays:[0,1,2,3,4,5,6],check:'오늘 회복 다짐을 확인했습니다',notify:1,time:'08:00'},
  {id:'review100',name:'하루 돌아보기',days:100,freq:'daily',weekdays:[0,1,2,3,4,5,6],check:'오늘 하루를 돌아보았습니다',notify:1,time:'21:30'},
  {id:'exercise3',name:'주 3회 운동',days:0,freq:'weekdays',weekdays:[1,3,5],check:'오늘 운동을 했습니다',notify:1,time:'18:00'}
];
let habitEditState = null;
function habitList(){
  if(!Array.isArray(S.habits)) S.habits=[];
  S.habits.forEach(h=>{ if(!Array.isArray(h.done)) h.done=[]; if(!Array.isArray(h.weekdays)) h.weekdays=[0,1,2,3,4,5,6]; if(!h.start) h.start=today(); });
  return S.habits;
}
function habitClone(x){ return JSON.parse(JSON.stringify(x)); }
function habitNewId(){ return 'h'+Date.now().toString(36)+Math.random().toString(36).slice(2,7); }
function habitDate(v){ const d=ymdDate(v); return d && !isNaN(d.getTime()) ? d : null; }
function habitDayNo(h,d){ const n=diffYmd(h.start,d||today()); return n==null?0:n+1; }
function habitEnded(h,d){ const n=habitDayNo(h,d); return +h.days>0 && n>+h.days; }
function habitActiveOn(h,d){
  d=d||today(); const n=habitDayNo(h,d); if(n<1) return false; if(+h.days>0 && n>+h.days) return false;
  if(h.freq==='weekdays'){
    const dt=habitDate(d); if(!dt) return false; return (h.weekdays||[]).indexOf(dt.getDay())>=0;
  }
  return true;
}
function habitDoneOn(h,d){ return (h.done||[]).indexOf(d||today())>=0; }
function habitToggle(h,d){ d=d||today(); h.done=h.done||[]; const i=h.done.indexOf(d); if(i<0)h.done.push(d); else h.done.splice(i,1); save(); }
function habitPeriodText(h){ return +h.days>0 ? h.days+'일' : '계속하기'; }
function habitFreqText(h){
  if(h.freq!=='weekdays') return '매일';
  const ko=['일','월','화','수','목','금','토']; return (h.weekdays||[]).map(x=>ko[x]).join('·')+'요일';
}
function habitProgressText(h){
  const n=habitDayNo(h,today()); if(n<1) return '시작 전 · '+h.start;
  if(+h.days>0 && n>+h.days) return '완료 · '+h.days+'일';
  return +h.days>0 ? n+'일차 / '+h.days+'일' : n+'일차 · 계속하기';
}
function habitToday(){ return habitList().filter(h=>habitActiveOn(h,today())); }
function habitNotifyPack(){
  return habitList().filter(h=>h.notify && /^\d{2}:\d{2}$/.test(String(h.time||''))).map(h=>{
    const wd=(h.freq==='weekdays'?(h.weekdays||[]):[0,1,2,3,4,5,6]).join('');
    return [String(h.id||''),h.time,h.start,String(Math.max(0,parseInt(h.days,10)||0)),wd].join('@');
  }).filter(x=>x.split('@')[0]).join('|');
}
function drawHabitHome(){
  const box=$('#home-habits'); if(!box) return; const rows=habitToday();
  if(!rows.length){ box.innerHTML=''; return; }
  box.innerHTML='<div class="habit-home"><div class="sp"><h3>오늘의 습관</h3><button class="tiny link" id="home-habit-all">전체 보기</button></div>'+rows.map(h=>
    '<div class="habit-home-row"><button class="hcheck'+(habitDoneOn(h,today())?' on':'')+'" data-home-habit="'+esc(h.id)+'">'+ico(habitDoneOn(h,today())?'check':'box')+'</button><div class="txt"><b>'+esc(h.name)+'</b><span>'+esc(h.check||'오늘 실천했습니다')+' · '+esc(habitProgressText(h))+'</span></div><span class="time">'+(h.notify?esc(h.time||''):'')+'</span></div>'
  ).join('')+'</div>';
  const all=$('#home-habit-all'); if(all) all.onclick=()=>go('habit');
  $$('[data-home-habit]').forEach(b=>b.onclick=()=>{ const h=habitList().find(x=>x.id===b.dataset.homeHabit); if(!h)return; habitToggle(h,today()); drawHabitHome(); drawTools(); });
  refreshIcons();
}
function startHabitNew(data){
  const d=habitClone(data||{name:'',days:21,freq:'daily',weekdays:[0,1,2,3,4,5,6],check:'오늘 실천했습니다',notify:0,time:'18:00'});
  d.id=d.id&&String(d.id).startsWith('h')?d.id:habitNewId(); d.start=d.start||today(); d.done=d.done||[];
  habitEditState={mode:'new',data:d}; go('habit-edit');
}
function editHabit(id){ const h=habitList().find(x=>x.id===id); if(!h)return; habitEditState={mode:'edit',data:habitClone(h)}; go('habit-edit'); }
function useHabitTemplate(id,edit){ const t=HABIT_TEMPLATES.find(x=>x.id===id); if(!t)return; const d=habitClone(t); d.id=habitNewId(); d.start=today(); d.done=[]; if(edit){habitEditState={mode:'new',data:d};go('habit-edit');return;} habitList().push(d);save();toast('내 습관에 추가했습니다.');drawHabits();drawTools(); }
function deleteHabit(id){
  const h=habitList().find(x=>x.id===id); if(!h)return;
  modal('<h2>습관을 삭제할까요?</h2><p class="muted" style="margin:7px 0 14px">'+esc(h.name)+'의 체크 기록도 함께 삭제됩니다.</p><button class="btn danger" id="habit-del-ok">삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
  $('#habit-del-ok').onclick=()=>{ S.habits=habitList().filter(x=>x.id!==id);save();closeModal();drawHabits();drawTools();toast('삭제했습니다.'); };
}
function drawHabits(){
  const mine=$('#habit-my'), tmp=$('#habit-templates'); if(!mine||!tmp)return; const rows=habitList();
  mine.innerHTML=rows.length?rows.map(h=>{
    const active=habitActiveOn(h,today()), done=active&&habitDoneOn(h,today()), ended=habitEnded(h,today());
    return '<div class="habit-card'+(ended?' done':'')+'"><div class="top"><span class="ic" style="color:var(--leaf)">'+ico('sprout')+'</span><div class="grow"><b>'+esc(h.name)+'</b><div class="meta">'+esc(habitProgressText(h))+' · '+esc(habitFreqText(h))+(h.notify?' · '+esc(h.time)+' 알림':' · 알림 없음')+'</div></div></div>'+(active?'<div class="checkline"><button class="'+(done?'on':'')+'" data-habit-check="'+esc(h.id)+'">'+ico(done?'check':'box')+'</button><span>'+esc(h.check||'오늘 실천했습니다')+'</span></div>':'')+'<div class="habit-actions"><button class="btn ghost sm" data-habit-edit="'+esc(h.id)+'">수정</button><button class="btn ghost sm" data-habit-del="'+esc(h.id)+'">삭제</button></div></div>';
  }).join(''):'<div class="empty">아직 만든 습관이 없습니다.<br>추천 예시를 사용하거나 새 습관을 만들어보세요.</div>';
  tmp.innerHTML=HABIT_TEMPLATES.map(t=>'<div class="habit-template"><b>'+esc(t.name)+'</b><p>'+esc(habitPeriodText(t))+' · '+esc(habitFreqText(t))+' · '+esc(t.check)+' · '+esc(t.time)+' 알림</p><div class="rowbtn"><button class="btn sec sm" data-template-use="'+t.id+'">그대로 사용</button><button class="btn ghost sm" data-template-edit="'+t.id+'">수정해서 사용</button></div></div>').join('');
  $('#habit-new').onclick=()=>startHabitNew();
  $$('[data-habit-check]').forEach(b=>b.onclick=()=>{const h=habitList().find(x=>x.id===b.dataset.habitCheck);if(h){habitToggle(h,today());drawHabits();drawHabitHome();}});
  $$('[data-habit-edit]').forEach(b=>b.onclick=()=>editHabit(b.dataset.habitEdit));
  $$('[data-habit-del]').forEach(b=>b.onclick=()=>deleteHabit(b.dataset.habitDel));
  $$('[data-template-use]').forEach(b=>b.onclick=()=>useHabitTemplate(b.dataset.templateUse,false));
  $$('[data-template-edit]').forEach(b=>b.onclick=()=>useHabitTemplate(b.dataset.templateEdit,true));
  refreshIcons();
}
function drawHabitEdit(){
  if(!habitEditState){ startHabitNew(); return; } const h=habitEditState.data, box=$('#habit-edit-body'); if(!box)return;
  $('#habit-edit-title').textContent=habitEditState.mode==='edit'?'습관 수정':'습관 만들기';
  const presets=[3,7,21,66,100], custom=(+h.days>0&&presets.indexOf(+h.days)<0), wko=['일','월','화','수','목','금','토'];
  box.innerHTML='<div class="card"><div class="field"><label>습관 이름</label><input id="habit-name" maxlength="40" placeholder="예: 모임 백일작전" value="'+esc(h.name||'')+'"></div>'+ 
    '<div class="field"><label>시작일</label><input id="habit-start" type="date" value="'+esc(h.start||today())+'"></div>'+ 
    '<div class="field"><label>실천 기간</label><div class="opts" id="habit-period">'+presets.map(n=>'<button class="opt'+(+h.days===n?' on':'')+'" data-habit-days="'+n+'">'+n+'일</button>').join('')+'<button class="opt'+(+h.days===0?' on':'')+'" data-habit-days="0">계속하기</button><button class="opt'+(custom?' on':'')+'" data-habit-days="custom">직접 설정</button></div><div id="habit-custom-wrap" style="margin-top:8px;display:'+(custom?'block':'none')+'"><input id="habit-custom-days" type="number" min="1" max="3650" value="'+(custom?+h.days:30)+'" placeholder="일수"></div></div>'+ 
    '<div class="field"><label>실천 빈도</label><div class="opts"><button class="opt'+(h.freq!=='weekdays'?' on':'')+'" id="habit-freq-daily">매일</button><button class="opt'+(h.freq==='weekdays'?' on':'')+'" id="habit-freq-week">요일 선택</button></div><div class="opts weekday-opts" id="habit-weekdays" style="margin-top:8px;display:'+(h.freq==='weekdays'?'grid':'none')+'">'+wko.map((x,i)=>'<button class="opt'+((h.weekdays||[]).indexOf(i)>=0?' on':'')+'" data-habit-week="'+i+'">'+x+'</button>').join('')+'</div></div>'+ 
    '<div class="field"><label>오늘의 체크 문구</label><input id="habit-check-text" maxlength="60" value="'+esc(h.check||'오늘 실천했습니다')+'"></div>'+ 
    '<div class="field"><label>알림</label><div class="opts"><button class="opt'+(h.notify?' on':'')+'" id="habit-notify-on">사용함</button><button class="opt'+(!h.notify?' on':'')+'" id="habit-notify-off">사용 안 함</button></div><div id="habit-time-wrap" style="margin-top:8px;display:'+(h.notify?'block':'none')+'"><input id="habit-time" type="time" value="'+esc(h.time||'18:00')+'"></div><p class="tiny" style="margin:7px 0 0">Android 앱에서는 회복도구 → 일정·알림 → 알림 설정에서 예약 상태를 한 번에 확인할 수 있습니다.</p></div>'+ 
    '<button class="btn" id="habit-save">저장</button><div style="height:8px"></div><button class="btn ghost" onclick="appBack(\'habit\')">취소</button></div>';
  const sync=()=>{ h.name=$('#habit-name').value.trim();h.start=$('#habit-start').value||today();h.check=$('#habit-check-text').value.trim();const tm=$('#habit-time');if(tm)h.time=tm.value||'18:00'; };
  $('#habit-name').oninput=sync;$('#habit-start').onchange=sync;$('#habit-check-text').oninput=sync; if($('#habit-time'))$('#habit-time').onchange=sync;
  $$('[data-habit-days]').forEach(b=>b.onclick=()=>{sync(); if(b.dataset.habitDays==='custom')h.days=Math.max(1,parseInt($('#habit-custom-days')?.value||30,10)||30);else h.days=+b.dataset.habitDays;drawHabitEdit();});
  const cd=$('#habit-custom-days');if(cd)cd.onchange=()=>{h.days=Math.max(1,parseInt(cd.value,10)||1);drawHabitEdit();};
  $('#habit-freq-daily').onclick=()=>{sync();h.freq='daily';h.weekdays=[0,1,2,3,4,5,6];drawHabitEdit();};
  $('#habit-freq-week').onclick=()=>{sync();h.freq='weekdays';if(!Array.isArray(h.weekdays)||!h.weekdays.length)h.weekdays=[1,3,5];drawHabitEdit();};
  $$('[data-habit-week]').forEach(b=>b.onclick=()=>{sync();const n=+b.dataset.habitWeek,i=h.weekdays.indexOf(n);if(i<0)h.weekdays.push(n);else if(h.weekdays.length>1)h.weekdays.splice(i,1);h.weekdays.sort();drawHabitEdit();});
  $('#habit-notify-on').onclick=()=>{sync();h.notify=1;drawHabitEdit();}; $('#habit-notify-off').onclick=()=>{sync();h.notify=0;drawHabitEdit();};
  $('#habit-save').onclick=()=>{sync();if(!h.name){toast('습관 이름을 적어주세요.');return;}if(!h.check){toast('오늘 체크할 문구를 적어주세요.');return;}if(h.freq==='weekdays'&&!(h.weekdays||[]).length){toast('실천할 요일을 골라주세요.');return;}if(h.notify&&!/^\d{2}:\d{2}$/.test(h.time||'')){toast('알림 시간을 정해주세요.');return;}const rows=habitList();if(habitEditState.mode==='edit'){const i=rows.findIndex(x=>x.id===h.id);if(i>=0){const done=rows[i].done||[];rows[i]=habitClone(h);rows[i].done=done;}}else rows.push(habitClone(h));save();habitEditState=null;toast('습관을 저장했습니다.');go('habit');};
  refreshIcons();
}

'''
marker='/* ══════════ 회복도구 · 중독 Q&A V6.5 ══════════ */'
once(marker,habit_js+marker,'habit js insert')

# 10. drawTools shows habit status.
old="function drawTools(){\n  const n = QA.length;"
new="function drawTools(){\n  const habits=habitList(), ht=habitToday(), hd=ht.filter(h=>habitDoneOn(h,today())).length;\n  const hs=$('#tool-habit-s'); if(hs) hs.textContent=habits.length ? ('진행 '+habits.filter(h=>!habitEnded(h,today())).length+'개 · 오늘 '+hd+'/'+ht.length+'개') : '추천 습관과 내 습관 관리';\n  const n = QA.length;"
once(old,new,'drawTools habit status')

# 11. Home draws today's habit checks.
once("function drawHome(){\n  const fam = famMode();\n  drawDailyHome();", "function drawHome(){\n  const fam = famMode();\n  drawDailyHome();\n  drawHabitHome();", 'drawHome habit')

# 12. Habit reminders are packed into the common Android settings payload.
old="""  const tr = treatmentCfg();\n  const visitDate = treatmentEffectiveVisit();"""
new="""  const habitsPacked = habitNotifyPack();\n  const tr = treatmentCfg();\n  const visitDate = treatmentEffectiveVisit();"""
once(old,new,'habit payload var')
once("    bed: sp.on && /^\\d{2}:\\d{2}$/.test(String(sp.bed || '')) ? String(sp.bed) : '',", "    bed: sp.on && /^\\d{2}:\\d{2}$/.test(String(sp.bed || '')) ? String(sp.bed) : '',\n    habits: habitsPacked,", 'habit payload field')

# 13. Native reservation counts include habits.
old="""    const n = (p.risk ? p.risk.split(',').filter(Boolean).length : 0) +\n      (p.meds ? p.meds.split('|').filter(Boolean).length : 0) +\n      (p.eats ? p.eats.split('|').filter(Boolean).length : 0) + (p.bed ? 1 : 0) +\n      (p.visit && p.visitAlerts ? p.visitAlerts.split(',').filter(Boolean).length : 0);"""
new="""    const n = (p.risk ? p.risk.split(',').filter(Boolean).length : 0) +\n      (p.meds ? p.meds.split('|').filter(Boolean).length : 0) +\n      (p.eats ? p.eats.split('|').filter(Boolean).length : 0) + (p.bed ? 1 : 0) +\n      (p.habits ? p.habits.split('|').filter(Boolean).length : 0) +\n      (p.visit && p.visitAlerts ? p.visitAlerts.split(',').filter(Boolean).length : 0);"""
once(old,new,'native count habits')

# 14. Schedule hub summaries no longer depend on treatment master and mention habit alerts.
s=s.replace("if(ns) ns.textContent = nativeAndroidApp() ? 'Android 예약알림 · 생활 · 치료 알림' : (S.notify ? '알림 사용 중 · 생활 · 치료 알림' : '습관 · 생활 · 치료 알림 관리');", "if(ns) ns.textContent = nativeAndroidApp() ? 'Android 예약알림 · 습관 · 생활 · 치료' : (S.notify ? '알림 사용 중 · 습관 · 생활 · 치료' : '습관 · 생활 · 치료 알림 관리');")

# 15. Version.
once("const BUILD = 'V8.1.4';","const BUILD = 'V8.1.5';",'build version')
p.write_text(s,encoding='utf-8')

sw=Path('sw.js'); w=sw.read_text(encoding='utf-8')
w=w.replace("const APP_VERSION = 'V8.1.4';","const APP_VERSION = 'V8.1.5';")
w=w.replace("const V = 'ohg-v814-tools-practice';","const V = 'ohg-v815-habits';")
sw.write_text(w,encoding='utf-8')
