from pathlib import Path


def replace_one(text, old, new, label):
    if old not in text:
        raise SystemExit(f'{label} target not found')
    if text.count(old) != 1:
        raise SystemExit(f'{label} target count={text.count(old)}')
    return text.replace(old, new, 1)

idx = Path('index.html')
s = idx.read_text(encoding='utf-8')

s = replace_one(s, "const BUILD = 'V8.2.24';", "const BUILD = 'V8.2.25';", 'build')

# Add SMART Goals page after VACI.
anchor = '''</section>\n\n<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->'''
goal_page = '''</section>\n\n<!-- ══════════ SMART Recovery · SMART Goals V8.2.25 ══════════ -->\n<section class="pg" id="p-smart-goal">\n  <div class="sp" style="margin-bottom:11px">\n    <h1 style="margin:0">SMART 목표 설정</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back onclick="appBack('smart-tools')">← SMART 실천도구</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    삶의 영역과 중요한 가치를 연결해 목표를 적고, <b>구체적 · 측정가능 · 동의가능 · 현실적 · 시간제한</b>의 다섯 기준으로 점검합니다. 마지막에는 실제로 할 행동을 정합니다. 반복해서 이어가고 싶은 행동은 기존 <b>습관</b>으로 바로 연결할 수 있습니다. 내용은 <b>이 기기에만 저장</b>됩니다.\n  </div>\n  <div id="smart-goal-role-note"></div>\n  <button class="btn sec" id="smart-goal-new">+ SMART 목표 새로 작성하기</button>\n  <div id="smart-goal-list" style="margin-top:12px"></div>\n</section>\n\n<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->'''
s = replace_one(s, anchor, goal_page, 'goal page')

# Habit editor back button gets a stable id so SMART-goal origin can be shown correctly.
s = replace_one(s,
'''<button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('habit')">← 습관</button>''',
'''<button class="tiny" style="color:var(--acc);font-weight:600" id="habit-edit-back" onclick="appBack('habit')">← 습관</button>''',
'habit edit back')

# Add route/tab/draw support.
s = replace_one(s,
"p === 'smart-balance-pie' || p === 'smart-vaci' || p === 'smart-tools'",
"p === 'smart-balance-pie' || p === 'smart-vaci' || p === 'smart-goal' || p === 'smart-tools'",
'tab route')
s = replace_one(s,
"  if(p === 'smart-vaci') drawSmartVaci();\n  if(p === 'smart-tools') drawSmartTools();",
"  if(p === 'smart-vaci') drawSmartVaci();\n  if(p === 'smart-goal') drawSmartGoal();\n  if(p === 'smart-tools') drawSmartTools();",
'draw route')

# SMART back label/fallback support.
s = replace_one(s,
"    'smart-balance-pie':'라이프스타일 밸런스 파이',\n    'smart-vaci':'VACI · 활력 넘치는 창의적 관심사'",
"    'smart-balance-pie':'라이프스타일 밸런스 파이',\n    'smart-vaci':'VACI · 활력 넘치는 창의적 관심사',\n    'smart-goal':'SMART 목표 설정'",
'back labels')
s = replace_one(s,
"'smart-problem-solving':'smart-problem-solving', 'smart-balance-pie':'smart-balance-pie', 'smart-vaci':'smart-vaci'",
"'smart-problem-solving':'smart-problem-solving', 'smart-balance-pie':'smart-balance-pie', 'smart-vaci':'smart-vaci', 'smart-goal':'smart-goal'",
'back fallbacks')

# Point 4 hub gets SMART Goals as the next tool.
old_hub = "smartToolButton('라이프스타일 밸런스 파이','삶의 영역별 만족도 0~10 → 먼저 돌볼 영역과 작은 변화 찾기','smart-balance-pie','sprout')+smartToolButton('VACI · 활력 넘치는 창의적 관심사','새 활동 → 시도 전 점수 → 시도 후 점수와 생각 정리','smart-vaci','sprout')"
new_hub = old_hub + "+smartToolButton('SMART 목표 설정','삶의 영역·가치 → 목표 → SMART 5기준 → 실행 행동','smart-goal','check')"
s = replace_one(s, old_hub, new_hub, 'Point 4 hub')

# Learning action route.
s = replace_one(s,
"  if(type === 'smart-vaci'){ go('smart-vaci'); return; }\n  if(type === 'halt')",
"  if(type === 'smart-vaci'){ go('smart-vaci'); return; }\n  if(type === 'smart-goal'){ go('smart-goal'); return; }\n  if(type === 'halt')",
'learning action')

# Preserve source page when creating a habit from SMART Goals.
s = replace_one(s,
"function startHabitNew(data){\n  const d=habitClone(data||{name:'',days:21,freq:'daily',weekdays:[0,1,2,3,4,5,6],check:'오늘 실천했습니다',notify:0,time:'18:00'});\n  d.id=d.id&&String(d.id).startsWith('h')?d.id:habitNewId(); d.start=d.start||today(); d.done=d.done||[];\n  habitEditState={mode:'new',data:d}; go('habit-edit');\n}",
"function startHabitNew(data,origin){\n  const d=habitClone(data||{name:'',days:21,freq:'daily',weekdays:[0,1,2,3,4,5,6],check:'오늘 실천했습니다',notify:0,time:'18:00'});\n  d.id=d.id&&String(d.id).startsWith('h')?d.id:habitNewId(); d.start=d.start||today(); d.done=d.done||[];\n  habitEditState={mode:'new',data:d,origin:origin||''}; go('habit-edit');\n}",
'habit origin')

s = replace_one(s,
"function drawHabitEdit(){\n  if(!habitEditState){ startHabitNew(); return; } const h=habitEditState.data, box=$('#habit-edit-body'); if(!box)return;\n  $('#habit-edit-title').textContent=habitEditState.mode==='edit'?'습관 수정':'습관 만들기';",
"function drawHabitEdit(){\n  if(!habitEditState){ startHabitNew(); return; } const h=habitEditState.data, box=$('#habit-edit-body'); if(!box)return;\n  $('#habit-edit-title').textContent=habitEditState.mode==='edit'?'습관 수정':'습관 만들기';\n  const habitFromGoal=habitEditState.origin==='smart-goal', habitBack=$('#habit-edit-back');\n  if(habitBack){habitBack.textContent=habitFromGoal?'← SMART 목표 설정':'← 습관';habitBack.onclick=()=>appBack(habitFromGoal?'smart-goal':'habit');}",
'habit editor source label')

s = replace_one(s,
"'<button class=\"btn\" id=\"habit-save\">저장</button><div style=\"height:8px\"></div><button class=\"btn ghost\" onclick=\"appBack(\\'habit\\')\">취소</button></div>';",
"'<button class=\"btn\" id=\"habit-save\">저장</button><div style=\"height:8px\"></div><button class=\"btn ghost\" id=\"habit-edit-cancel\">취소</button></div>';",
'habit cancel button')

s = replace_one(s,
"  $('#habit-notify-on').onclick=()=>{sync();h.notify=1;drawHabitEdit();}; $('#habit-notify-off').onclick=()=>{sync();h.notify=0;drawHabitEdit();};\n  $('#habit-save').onclick=()=>{sync();if(!h.name){toast('습관 이름을 적어주세요.');return;}if(!h.check){toast('오늘 체크할 문구를 적어주세요.');return;}if(h.freq==='weekdays'&&!(h.weekdays||[]).length){toast('실천할 요일을 골라주세요.');return;}if(h.notify&&!/^\\d{2}:\\d{2}$/.test(h.time||'')){toast('알림 시간을 정해주세요.');return;}const rows=habitList();if(habitEditState.mode==='edit'){const i=rows.findIndex(x=>x.id===h.id);if(i>=0){const done=rows[i].done||[];rows[i]=habitClone(h);rows[i].done=done;}}else rows.push(habitClone(h));save();habitEditState=null;toast('습관을 저장했습니다.');go('habit');};",
"  $('#habit-notify-on').onclick=()=>{sync();h.notify=1;drawHabitEdit();}; $('#habit-notify-off').onclick=()=>{sync();h.notify=0;drawHabitEdit();};\n  const habitCancel=$('#habit-edit-cancel');if(habitCancel)habitCancel.onclick=()=>appBack(habitFromGoal?'smart-goal':'habit');\n  $('#habit-save').onclick=()=>{sync();if(!h.name){toast('습관 이름을 적어주세요.');return;}if(!h.check){toast('오늘 체크할 문구를 적어주세요.');return;}if(h.freq==='weekdays'&&!(h.weekdays||[]).length){toast('실천할 요일을 골라주세요.');return;}if(h.notify&&!/^\\d{2}:\\d{2}$/.test(h.time||'')){toast('알림 시간을 정해주세요.');return;}const rows=habitList(),origin=habitEditState.origin||'';if(habitEditState.mode==='edit'){const i=rows.findIndex(x=>x.id===h.id);if(i>=0){const done=rows[i].done||[];rows[i]=habitClone(h);rows[i].done=done;}}else rows.push(habitClone(h));save();habitEditState=null;toast('습관을 저장했습니다.');if(origin==='smart-goal')appBack('smart-goal');else go('habit');};",
'habit save origin')

# SMART Goals implementation. Insert before learningAction so existing SMART helpers are already available.
goal_js = r'''/* ══════════ SMART Recovery · SMART 목표 설정 V8.2.25 ══════════
   삶의 카테고리(Lifestyle Balance Pie)와 가치(HOV)를 목표에 연결합니다.
   목표를 구체적·측정가능·동의가능·현실적·시간제한으로 점검한 뒤 실행 행동을 정합니다.
   반복 행동은 기존 습관 편집기로 넘기며 습관/알림 저장구조는 그대로 사용합니다. */
const SMART_GOAL_CRITERIA=[
  {k:'specific',l:'구체적',d:'무엇을 할지 분명한가?'},
  {k:'measurable',l:'측정가능',d:'했는지 확인할 수 있는가?'},
  {k:'agreed',l:'동의가능',d:'내가 동의하고 실제로 해볼 수 있는가?'},
  {k:'realistic',l:'현실적',d:'현재 상황에서 현실적인가?'},
  {k:'timed',l:'시간제한',d:'언제까지 할지 정했는가?'}
];
function smartGoalRecords(){
 const role=famMode()?'family':'self';
 return (Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>x&&x.kind==='smart-goal'&&(x.role||'self')===role).sort((a,b)=>(b.updatedAt||b.ts||0)-(a.updatedAt||a.ts||0));
}
function smartGoalDate(ts){return smartProblemDate(ts);}
function smartGoalSuggestions(){
 const cats=[],vals=[],add=(arr,v)=>{v=String(v||'').trim();if(v&&arr.indexOf(v)<0)arr.push(v);};
 smartBalanceRecords().forEach(r=>(Array.isArray(r.areas)?r.areas:[]).forEach(a=>add(cats,a&&a.name)));
 const role=famMode()?'family':'self';
 (Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>x&&x.tool==='hov'&&(x.role||'self')===role).sort((a,b)=>(b.updatedAt||b.t||0)-(a.updatedAt||a.t||0)).forEach(r=>smartHovValues(r).forEach(v=>add(vals,v)));
 return {cats:cats.slice(0,20),vals:vals.slice(0,20)};
}
function smartGoalCriteriaCount(r){const c=r&&r.checks||{};return SMART_GOAL_CRITERIA.filter(x=>!!c[x.k]).length;}
function drawSmartGoal(){
 const list=$('#smart-goal-list'),rn=$('#smart-goal-role-note'),add=$('#smart-goal-new');if(!list||!add)return;
 if(rn)rn.innerHTML=famMode()?'<div class="note" style="margin-bottom:12px"><b>가족도 내 목표를 세웁니다.</b><br>상대가 무엇을 하게 만들지 정하는 도구가 아니라, 가족인 내가 중요하게 여기는 삶의 영역·가치와 내 행동을 구체화합니다.</div>':'';
 add.onclick=()=>openSmartGoalEditor(null);
 const rows=smartGoalRecords();
 if(!rows.length){list.innerHTML='<div class="card"><b>아직 저장한 SMART 목표가 없습니다.</b><p class="muted" style="margin:5px 0 0">삶의 한 영역에서 지금 바꾸고 싶은 작은 목표부터 적어보세요.</p></div>';return;}
 list.innerHTML='<div class="card"><h3>저장한 SMART 목표 '+rows.length+'건</h3>'+rows.map(r=>{const tags=[r.category,r.value].filter(Boolean).map(v=>'<span style="display:inline-flex;padding:3px 8px;border-radius:999px;background:var(--accbg);color:var(--acc);font-size:11.5px">'+esc(v)+'</span>').join('');return '<div class="sp" style="gap:10px;padding:11px 0;border-top:1px solid var(--line);align-items:flex-start"><div style="min-width:0;flex:1"><div class="tiny">'+esc(smartGoalDate(r.updatedAt||r.ts))+' · SMART '+smartGoalCriteriaCount(r)+'/5'+(r.repeat?' · 습관 연결 가능':'')+'</div><b style="display:block;margin-top:3px">'+esc(r.revised||r.goal||'SMART 목표')+'</b>'+(tags?'<div style="display:flex;flex-wrap:wrap;gap:5px;margin-top:6px">'+tags+'</div>':'')+'<div class="muted" style="margin-top:5px">'+esc(r.action||'실행 행동 미작성')+'</div></div><button class="tiny" style="color:var(--acc);font-weight:600;flex:0 0 auto" onclick="openSmartGoalView(\''+esc(r.id)+'\')">보기</button></div>';}).join('')+'</div>';
}
function openSmartGoalEditor(record){
 const r=record||{},sug=smartGoalSuggestions();
 let checks=Object.assign({specific:0,measurable:0,agreed:0,realistic:0,timed:0},r.checks||{}),repeat=!!r.repeat;
 const setAcc=(node,on)=>{if(!node)return;node.classList.toggle('on',!!on);const b=Array.from(node.children).find(x=>x.classList&&x.classList.contains('acc-h'));if(b)b.setAttribute('aria-expanded',on?'true':'false');};
 const options=a=>a.map(v=>'<option value="'+esc(v)+'"></option>').join('');
 const crit=()=>SMART_GOAL_CRITERIA.map(x=>'<button type="button" class="opt wide'+(checks[x.k]?' on':'')+'" data-goal-crit="'+x.k+'" aria-pressed="'+(checks[x.k]?'true':'false')+'"><span><b>'+esc(x.l)+'</b><small style="display:block;font-weight:400;margin-top:2px">'+esc(x.d)+'</small></span></button>').join('');
 modal('<h2>'+(record?'SMART 목표 수정':'SMART 목표 설정')+'</h2><p class="muted" style="margin:5px 0 14px">삶의 방향을 정한 뒤 목표를 SMART 기준으로 점검하고, 실제로 할 행동까지 연결합니다.</p><div id="smart-goal-editor">'
  +'<div class="acc on" data-goal-step="direction"><button class="acc-h" type="button" data-goal-step-toggle="direction" aria-expanded="true"><div class="acc-n"><b>1 · 삶의 방향과 목표</b><span>밸런스 파이의 삶의 영역과 HOV의 가치를 연결합니다.</span></div><svg class="acc-v" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg></button><div class="acc-b"><div class="field"><label>삶의 카테고리 <span class="tiny">(선택)</span></label><input id="goal-category" list="goal-category-list" maxlength="60" value="'+esc(r.category||'')+'" placeholder="예: 건강, 가족, 일, 여가"><datalist id="goal-category-list">'+options(sug.cats)+'</datalist><p class="tiny" style="margin:5px 0 0">밸런스 파이를 작성했다면 그 영역이 제안됩니다.</p></div><div class="field"><label>관련 가치 <span class="tiny">(선택)</span></label><input id="goal-value" list="goal-value-list" maxlength="80" value="'+esc(r.value||'')+'" placeholder="예: 건강, 가족, 성실, 성장"><datalist id="goal-value-list">'+options(sug.vals)+'</datalist><p class="tiny" style="margin:5px 0 0">HOV를 작성했다면 나의 가치가 제안됩니다.</p></div><div class="field"><label>목표</label><textarea id="goal-text" maxlength="800" placeholder="예: 좀 더 적극적으로 해본다.">'+esc(r.goal||'')+'</textarea></div><button class="btn sec" type="button" id="goal-next-check">다음 · SMART 기준 점검</button></div></div>'
  +'<div class="acc" data-goal-step="check"><button class="acc-h" type="button" data-goal-step-toggle="check" aria-expanded="false"><div class="acc-n"><b>2 · SMART 기준 점검</b><span>구체적 · 측정가능 · 동의가능 · 현실적 · 시간제한을 확인합니다.</span></div><svg class="acc-v" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg></button><div class="acc-b"><div class="opts" id="goal-criteria">'+crit()+'</div><div class="field" style="margin-top:12px"><label>수정된 목표 <span class="tiny">(필요한 경우)</span></label><textarea id="goal-revised" maxlength="800" placeholder="점검 후 목표를 더 구체적으로 고쳐 적어보세요.">'+esc(r.revised||'')+'</textarea></div><button class="btn sec" type="button" id="goal-next-action">다음 · 실행 행동</button></div></div>'
  +'<div class="acc" data-goal-step="action"><button class="acc-h" type="button" data-goal-step-toggle="action" aria-expanded="false"><div class="acc-n"><b>3 · 실행 행동</b><span>목표 달성을 위해 실제로 할 한 가지 행동을 정합니다.</span></div><svg class="acc-v" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg></button><div class="acc-b"><div class="field"><label>실행할 행동</label><input id="goal-action" maxlength="80" value="'+esc(r.action||'')+'" placeholder="예: 공원 3Km 걷기"></div><div class="field"><label>언제 · 어디서 · 얼마나 <span class="tiny">(선택)</span></label><textarea id="goal-task" maxlength="900" placeholder="예: 이번 주 수·목·일 아침에 주변 공원을 약 3Km 걷습니다.">'+esc(r.task||'')+'</textarea></div><div class="field"><label>시작 날짜 <span class="tiny">(선택)</span></label><input id="goal-start" type="date" value="'+esc(r.start||'')+'"></div><div class="field"><label>이 행동을 어떻게 이어갈까요?</label><div class="opts"><button type="button" class="opt'+(!repeat?' on':'')+'" id="goal-repeat-no">이번 목표에서 실행</button><button type="button" class="opt'+(repeat?' on':'')+'" id="goal-repeat-yes">반복해서 습관화</button></div><p class="tiny" id="goal-repeat-note" style="margin:7px 0 0">'+(repeat?'저장 후 기록 보기에서 기존 습관으로 연결할 수 있습니다.':'반복이 필요한 행동이면 습관으로 연결할 수 있습니다.')+'</p></div></div></div></div><button class="btn" id="goal-save">'+(record?'수정 저장':'SMART 목표 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
 const root=$('#smart-goal-editor');
 const openStep=(name,scroll)=>{if(!root)return;root.querySelectorAll('[data-goal-step]').forEach(a=>setAcc(a,false));const t=root.querySelector('[data-goal-step="'+name+'"]');setAcc(t,true);if(scroll&&t)setTimeout(()=>t.scrollIntoView({behavior:'smooth',block:'start'}),30);};
 root.querySelectorAll('[data-goal-step-toggle]').forEach(b=>b.onclick=()=>{const t=b.closest('[data-goal-step]'),was=t.classList.contains('on');root.querySelectorAll('[data-goal-step]').forEach(a=>setAcc(a,false));if(!was)setAcc(t,true);});
 $('#goal-next-check').onclick=()=>{if(!$('#goal-text').value.trim()){toast('목표를 적어주세요.');return;}openStep('check',true);};
 $('#goal-next-action').onclick=()=>openStep('action',true);
 $('#goal-criteria').querySelectorAll('[data-goal-crit]').forEach(b=>b.onclick=()=>{checks[b.dataset.goalCrit]=checks[b.dataset.goalCrit]?0:1;b.classList.toggle('on',!!checks[b.dataset.goalCrit]);b.setAttribute('aria-pressed',checks[b.dataset.goalCrit]?'true':'false');});
 const syncRepeat=()=>{const y=$('#goal-repeat-yes'),n=$('#goal-repeat-no'),note=$('#goal-repeat-note');if(y)y.classList.toggle('on',repeat);if(n)n.classList.toggle('on',!repeat);if(note)note.textContent=repeat?'저장 후 기록 보기에서 기존 습관으로 연결할 수 있습니다.':'반복이 필요한 행동이면 습관으로 연결할 수 있습니다.';};
 $('#goal-repeat-no').onclick=()=>{repeat=false;syncRepeat();};$('#goal-repeat-yes').onclick=()=>{repeat=true;syncRepeat();};
 $('#goal-save').onclick=()=>{const goal=$('#goal-text').value.trim();if(!goal){openStep('direction',true);toast('목표를 적어주세요.');return;}const action=$('#goal-action').value.trim();if(!action){openStep('action',true);toast('실행할 행동을 적어주세요.');return;}const now=Date.now(),rec={id:record?record.id:('goal-'+now+'-'+Math.random().toString(36).slice(2,7)),kind:'smart-goal',role:famMode()?'family':'self',ts:record?(record.ts||now):now,updatedAt:now,category:$('#goal-category').value.trim(),value:$('#goal-value').value.trim(),goal,checks:Object.assign({},checks),revised:$('#goal-revised').value.trim(),action,task:$('#goal-task').value.trim(),start:$('#goal-start').value,repeat:repeat?1:0};if(!Array.isArray(S.smartWorks))S.smartWorks=[];if(record){const i=S.smartWorks.findIndex(x=>x&&x.id===record.id);if(i>=0)S.smartWorks[i]=rec;else S.smartWorks.push(rec);}else S.smartWorks.push(rec);save();closeModal();drawSmartGoal();toast(repeat?'SMART 목표를 저장했습니다. 반복 행동은 기록 보기에서 습관으로 연결할 수 있습니다.':'SMART 목표를 저장했습니다.');};
}
function openSmartGoalView(id){
 const r=smartGoalRecords().find(x=>x.id===id);if(!r)return,c=r.checks||{};
 const sec=(t,v)=>'<div class="card"><h3>'+esc(t)+'</h3><div style="white-space:pre-wrap">'+(String(v||'').trim()?esc(v):'<span class="muted">작성하지 않음</span>')+'</div></div>';
 const criteria='<div class="card"><h3>SMART 기준</h3><div style="display:flex;flex-wrap:wrap;gap:6px">'+SMART_GOAL_CRITERIA.map(x=>'<span style="display:inline-flex;padding:4px 9px;border-radius:999px;background:'+(c[x.k]?'var(--accbg)':'var(--bg2)')+';color:'+(c[x.k]?'var(--acc)':'var(--dim)')+';font-size:12px">'+(c[x.k]?'✓ ':'○ ')+esc(x.l)+'</span>').join('')+'</div></div>';
 modal('<h2>SMART 목표 설정</h2><div class="muted" style="margin:-4px 0 12px">'+esc(smartGoalDate(r.updatedAt||r.ts))+'</div>'+sec('삶의 카테고리',r.category)+sec('관련 가치',r.value)+sec('목표',r.goal)+criteria+sec('수정된 목표',r.revised)+sec('실행할 행동',r.action)+sec('언제 · 어디서 · 얼마나',r.task)+sec('시작 날짜',r.start)+(r.repeat?'<button class="btn" id="smart-goal-habit">이 실행을 습관으로 추가</button><div style="height:8px"></div>':'')+'<button class="btn sec" id="smart-goal-edit">수정</button><div style="height:8px"></div><button class="btn bad" id="smart-goal-delete">이 목표 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
 const hb=$('#smart-goal-habit');if(hb)hb.onclick=()=>smartGoalToHabit(r);
 $('#smart-goal-edit').onclick=()=>openSmartGoalEditor(r);
 $('#smart-goal-delete').onclick=()=>{if(!confirm('이 SMART 목표를 삭제할까요?'))return;S.smartWorks=(Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>!(x&&x.id===r.id));save();closeModal();drawSmartGoal();toast('SMART 목표를 삭제했습니다.');};
}
function smartGoalToHabit(r){
 const name=String(r.action||r.revised||r.goal||'SMART 목표 실천').replace(/\s+/g,' ').trim().slice(0,40)||'SMART 목표 실천';
 const check=('오늘 '+name+' 실천했습니다').slice(0,60);
 closeModal();
 startHabitNew({name,days:0,freq:'daily',weekdays:[0,1,2,3,4,5,6],check,notify:0,time:'18:00',start:r.start||today()},'smart-goal');
}

'''
s = replace_one(s, "function learningAction(type,sectionId){", goal_js + "function learningAction(type,sectionId){", 'goal implementation')

idx.write_text(s, encoding='utf-8')

# Point 4 learning action button.
ld = Path('learning-data.js')
t = ld.read_text(encoding='utf-8')
old_action = '''          {\n            "type": "smart-vaci",\n            "label": "VACI 관심사 목록 작성하기"\n          }\n        ]'''
new_action = '''          {\n            "type": "smart-vaci",\n            "label": "VACI 관심사 목록 작성하기"\n          },\n          {\n            "type": "smart-goal",\n            "label": "SMART 목표 설정하기"\n          }\n        ]'''
if old_action not in t:
    raise SystemExit('Point 4 learning action target not found')
t = t.replace(old_action, new_action, 1)
ld.write_text(t, encoding='utf-8')

sw = Path('sw.js')
u = sw.read_text(encoding='utf-8')
u = replace_one(u, "const APP_VERSION = 'V8.2.24';", "const APP_VERSION = 'V8.2.25';", 'sw version')
u = replace_one(u, "const V = 'ohg-v8224-vaci-fix-chips';", "const V = 'ohg-v8225-smart-goals-habit-link';", 'sw cache')
sw.write_text(u, encoding='utf-8')
