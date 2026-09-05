from pathlib import Path

idx = Path('index.html')
learn = Path('learning-data.js')
sw = Path('sw.js')

index = idx.read_text(encoding='utf-8')
learning = learn.read_text(encoding='utf-8')
swt = sw.read_text(encoding='utf-8')

# versions
index = index.replace("const BUILD = 'V8.2.4';", "const BUILD = 'V8.2.5';", 1)
index = index.replace("const DATA_SCHEMA = 5;", "const DATA_SCHEMA = 6;", 1)
swt = swt.replace("const APP_VERSION = 'V8.2.4';", "const APP_VERSION = 'V8.2.5';", 1)
swt = swt.replace("const V = 'ohg-v824-daily-meditation';", "const V = 'ohg-v825-smart-hov';", 1)
learning = learning.replace('/* 오늘 한 걸음 — 회복학습 데이터 V8.2.3', '/* 오늘 한 걸음 — 회복학습 데이터 V8.2.5', 1)

# scalable SMART worksheet store
anchor = "  stepWorks: [], stepDrafts: {},\n  familyStepWorks: [], familyStepDrafts: {},"
repl = "  stepWorks: [], stepDrafts: {},\n  smartWorks: [],                         /* SMART Recovery 작성형 도구 — [{tool, role, ...}] */\n  familyStepWorks: [], familyStepDrafts: {},"
if anchor not in index:
    raise SystemExit('default smartWorks anchor not found')
index = index.replace(anchor, repl, 1)

anchor = "  if(!Array.isArray(s.stepWorks)) s.stepWorks = [];\n"
repl = anchor + "  if(!Array.isArray(s.smartWorks)) s.smartWorks = [];\n"
if anchor not in index:
    raise SystemExit('migrate smartWorks anchor not found')
index = index.replace(anchor, repl, 1)

# HOV page
page_anchor = '<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->'
page = '''<!-- ══════════ SMART Recovery · HOV V8.2.5 ══════════ -->
<section class="pg" id="p-smart-hov">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">가치의 계층 HOV</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="go('learn-topic')">← SMART Recovery</button>
  </div>
  <div class="note" style="margin-bottom:12px">
    내 삶에서 가장 중요한 가치를 분명히 하고, 지금의 행동이 그 가치와 얼마나 맞는지 돌아봅니다. SMART Recovery의 <b>Hierarchy of Values(HOV)</b>를 앱에 맞게 재구성했으며, <b>내용은 이 기기에만 저장</b>됩니다.
  </div>
  <div id="smart-hov-role-note"></div>
  <button class="btn sec" id="smart-hov-new">+ HOV 새로 작성하기</button>
  <div id="smart-hov-list" style="margin-top:12px"></div>
</section>

'''
if page_anchor not in index:
    raise SystemExit('HOV page anchor not found')
index = index.replace(page_anchor, page + page_anchor, 1)

# route and draw
old = "|| p === 'urge-diary') ? 'tools' : p;"
new = "|| p === 'urge-diary' || p === 'smart-hov') ? 'tools' : p;"
if old not in index:
    raise SystemExit('tools route anchor not found')
index = index.replace(old, new, 1)

anchor = "  if(p === 'urge-diary') drawUrgeDiary();\n"
if anchor not in index:
    raise SystemExit('draw smart hov route anchor not found')
index = index.replace(anchor, anchor + "  if(p === 'smart-hov') drawSmartHov();\n", 1)

# learning action route
anchor = "  if(type === 'urge-diary'){ go('urge-diary'); return; }\n"
if anchor not in index:
    raise SystemExit('learningAction anchor not found')
index = index.replace(anchor, anchor + "  if(type === 'smart-hov'){ go('smart-hov'); return; }\n", 1)

# HOV functions
fn_anchor = "function drawScheduleHub(){"
functions = r'''/* ══════════ SMART Recovery · 가치의 계층(HOV) V8.2.5 ══════════
   사용자 번역 SMART Recovery 핸드북의 HOV 구조를 앱용으로 재구성했습니다.
   상대를 평가하는 도구가 아니라 '내가 중요하게 여기는 가치'와 실제 행동의 불일치를 돌아봅니다. */
function smartWorkId(){ return 'sw'+Date.now().toString(36)+Math.random().toString(36).slice(2,7); }
function smartRole(){ return famMode() ? 'family' : 'self'; }
function smartHovRows(){
  return (S.smartWorks||[]).filter(r=>r && r.tool==='hov' && (r.role||'self')===smartRole())
    .slice().sort((a,b)=>Number(b.t||0)-Number(a.t||0));
}
function smartHovValues(r){ return (r&&Array.isArray(r.values)?r.values:[]).map(x=>String(x||'').trim()).filter(Boolean).slice(0,5); }
function smartHovDate(ts){
  if(!ts) return '';
  const d=new Date(ts); return d.getFullYear()+'. '+(d.getMonth()+1)+'. '+d.getDate()+'.';
}
function drawSmartHov(){
  const list=$('#smart-hov-list'), rn=$('#smart-hov-role-note'), add=$('#smart-hov-new');
  if(!list||!add) return;
  if(rn){
    rn.innerHTML=famMode()
      ? '<div class="note" style="margin-bottom:12px"><b>가족의 자리에서도 내 가치부터 봅니다.</b><br>상대의 행동을 평가하지 않고, 중독 문제에 내 삶이 붙들릴 때 내가 중요하게 여기는 가치가 어떻게 밀려났는지 돌아봅니다.</div>'
      : '';
  }
  const rows=smartHovRows();
  if(!rows.length){
    list.innerHTML='<div class="empty">아직 작성한 HOV가 없습니다.<br>내 삶에서 가장 중요한 다섯 가치를 적어보세요.</div>';
  }else{
    let h='<div class="card"><h3>저장한 HOV '+rows.length+'건</h3>';
    rows.forEach(r=>{
      const vals=smartHovValues(r);
      h+='<button class="ws-saved" style="width:100%;text-align:left" data-hov-rid="'+esc(r.rid||String(r.t))+'">'
        +'<span class="date">'+esc(smartHovDate(r.t))+'</span>'
        +'<span class="body"><b>'+esc(vals.slice(0,3).join(' · ') || '가치 기록')+'</b><span>'+(vals.length>3?esc('외 '+(vals.length-3)+'개'):'내 가치와 행동을 돌아본 기록')+'</span></span>'
        +'<span class="go">보기</span></button>';
    });
    h+='</div>'; list.innerHTML=h;
    list.querySelectorAll('[data-hov-rid]').forEach(b=>b.onclick=()=>{
      const r=rows.find(x=>(x.rid||String(x.t))===b.dataset.hovRid); if(r) openSmartHovRecord(r);
    });
  }
  add.onclick=()=>openSmartHovEditor();
}
function openSmartHovRecord(r){
  const vals=smartHovValues(r);
  let v='<ol style="margin:0;padding-left:22px">'+vals.map(x=>'<li style="padding:4px 0"><b>'+esc(x)+'</b></li>').join('')+'</ol>';
  let extra='';
  if(r.conflict) extra+='<div class="sep"></div><h3>가치와 어긋났던 모습</h3><p style="white-space:pre-wrap">'+esc(r.conflict)+'</p>';
  if(r.protect) extra+='<div class="sep"></div><h3>먼저 보호하고 싶은 가치</h3><p><b>'+esc(r.protect)+'</b></p>';
  if(r.action) extra+='<div class="sep"></div><h3>오늘의 작은 행동</h3><p style="white-space:pre-wrap">'+esc(r.action)+'</p>';
  modal('<h2>나의 가치의 계층</h2><p class="tiny" style="margin:4px 0 12px">'+esc(smartHovDate(r.t))+' 작성</p><div class="card"><h3>내 삶에서 중요한 가치</h3>'+v+extra+'</div><button class="btn sec" id="smart-hov-edit">수정</button><div style="height:8px"></div><button class="btn danger" id="smart-hov-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
  $('#smart-hov-edit').onclick=()=>openSmartHovEditor(r);
  $('#smart-hov-delete').onclick=()=>{
    const key=r.rid||String(r.t);
    modal('<h2>이 HOV 기록을 삭제할까요?</h2><p class="muted" style="margin:6px 0 14px">이 기록 한 건만 기기에서 삭제하며 되돌릴 수 없습니다.</p><button class="btn danger" id="smart-hov-delete-ok">삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
    $('#smart-hov-delete-ok').onclick=()=>{ S.smartWorks=(S.smartWorks||[]).filter(x=>(x.rid||String(x.t))!==key); save(); closeModal(); drawSmartHov(); toast('삭제했습니다.'); };
  };
}
function openSmartHovEditor(record){
  const edit=!!record, vals=smartHovValues(record);
  while(vals.length<5) vals.push('');
  const conflictPrompt=famMode()
    ? '중독 문제에 내 삶이 붙들려 있을 때, 이 가치들은 실제 생활에서 어떻게 밀려났나요?'
    : '중독행동을 할 때, 이 가치들은 실제 생활에서 어떻게 밀려났나요?';
  const valueInputs=vals.map((x,i)=>'<div class="field"><label>'+(i+1)+'순위 가치</label><input class="hov-value" maxlength="40" value="'+esc(x)+'" placeholder="'+(i===0?'예: 가족, 건강, 신뢰, 자유처럼 나에게 중요한 것':'가치 '+(i+1))+'"></div>').join('');
  modal('<h2>'+(edit?'HOV 수정':'가치의 계층 HOV 작성')+'</h2>'
    +'<p class="muted" style="margin:5px 0 14px">SMART Recovery HOV는 내 목표와 현재 행동의 차이를 알아차리는 도구입니다. 가장 중요한 가치부터 순서대로 다섯 가지를 적어보세요.</p>'
    +'<div class="card"><h3>1. 내 삶에서 가장 중요한 다섯 가치</h3>'+valueInputs+'</div>'
    +'<div class="card"><h3>2. 가치와 실제 행동 돌아보기</h3><p class="muted" style="margin:-4px 0 9px">'+esc(conflictPrompt)+'</p><textarea id="hov-conflict" maxlength="400" placeholder="예: 가족과 보내려던 시간보다 중독행동에 시간과 주의를 더 많이 썼다">'+esc(edit?(record.conflict||''):'')+'</textarea></div>'
    +'<div class="card"><h3>3. 회복으로 다시 보호할 것</h3><label>지금 가장 먼저 보호하고 싶은 가치</label><input id="hov-protect" maxlength="40" value="'+esc(edit?(record.protect||''):'')+'" placeholder="위의 가치 중 하나를 적어보세요"><div class="field" style="margin-top:12px"><label>오늘 할 수 있는 작은 행동</label><textarea id="hov-action" maxlength="220" placeholder="예: 오늘 저녁 가족과 20분 산책하기">'+esc(edit?(record.action||''):'')+'</textarea></div></div>'
    +'<button class="btn" id="hov-save">'+(edit?'수정 저장':'HOV 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
  $('#hov-save').onclick=()=>{
    const values=Array.from(document.querySelectorAll('.hov-value')).map(x=>x.value.trim());
    if(values.some(x=>!x)){ toast('가장 중요한 가치 다섯 가지를 모두 적어주세요.'); return; }
    const now=Date.now();
    const rec={rid:edit?(record.rid||smartWorkId()):smartWorkId(),tool:'hov',role:smartRole(),t:edit?Number(record.t||now):now,updatedAt:now,values:values.slice(0,5),conflict:$('#hov-conflict').value.trim(),protect:$('#hov-protect').value.trim(),action:$('#hov-action').value.trim()};
    const rows=S.smartWorks||[];
    const key=edit?(record.rid||String(record.t)):'';
    const i=edit?rows.findIndex(x=>(x.rid||String(x.t))===key):-1;
    if(i>=0) rows[i]=rec; else rows.push(rec);
    S.smartWorks=rows; save(); closeModal(); drawSmartHov(); toast(edit?'HOV를 수정했습니다.':'HOV를 저장했습니다.');
  };
}

'''
if fn_anchor not in index:
    raise SystemExit('HOV function anchor not found')
index = index.replace(fn_anchor, functions + fn_anchor, 1)

# Point 1 action in learning data
practice = '        "practice": "오늘 내가 지키고 싶은 가치 한 가지와, 그 가치를 위해 할 수 있는 작은 행동 한 가지를 정해보세요."\n'
replacement = '        "practice": "오늘 내가 지키고 싶은 가치 한 가지와, 그 가치를 위해 할 수 있는 작은 행동 한 가지를 정해보세요.",\n        "actions": [\n          {\n            "type": "smart-hov",\n            "label": "HOV 가치의 계층 작성하기"\n          }\n        ]\n'
if practice not in learning:
    raise SystemExit('SMART Point1 HOV action anchor not found')
learning = learning.replace(practice, replacement, 1)

idx.write_text(index, encoding='utf-8')
learn.write_text(learning, encoding='utf-8')
sw.write_text(swt, encoding='utf-8')
