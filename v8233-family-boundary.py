from pathlib import Path

root=Path('.')
idx=root/'index.html'
sw=root/'sw.js'
readme=root/'README.md'

def once(text, old, new, label):
    n=text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    return text.replace(old,new,1)

s=idx.read_text(encoding='utf-8')
s=once(s,"const BUILD = 'V8.2.32';","const BUILD = 'V8.2.33';",'BUILD')

# Add entry only to the existing family boundary guidance article.
old="""    {h:'경계를 지키는 것은 상대를 바꾸려는 것이 아닌 나를 지키는 것입니다',\n     b:"""
new="""    {h:'경계를 지키는 것은 상대를 바꾸려는 것이 아닌 나를 지키는 것입니다', a:'family-boundary', al:'내 경계 정리하기',\n     b:"""
s=once(s,old,new,'family boundary guide action')

old="""  if(action==='help'){ go('help'); return; }\n  if(['smart-cba','smart-abc','smart-balance-pie','smart-health'].includes(action)){ go(action); return; }"""
new="""  if(action==='help'){ go('help'); return; }\n  if(action==='family-boundary'){ go('family-boundary'); return; }\n  if(['smart-cba','smart-abc','smart-balance-pie','smart-health'].includes(action)){ go(action); return; }"""
s=once(s,old,new,'family guide route')

# Family boundary page: no new menu, reached from the existing family guidance article.
marker='''<!-- ══════════ SMART Recovery · 실천도구 허브 V8.2.11 ══════════ -->'''
page='''<!-- ══════════ 가족 · 내 경계 정리 V8.2.33 ══════════ -->\n<section class="pg" id="p-family-boundary">\n  <div class="sp" style="margin-bottom:11px">\n    <h1 style="margin:0">내 경계 정리</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('fam')">← 가족 안내</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    경계는 상대를 바꾸거나 벌주는 규칙이 아니라 <b>내가 지키고 싶은 기준과 내가 할 행동</b>을 정하는 것입니다. 지금 지킬 수 있는 것 하나부터 시작해도 됩니다.\n  </div>\n  <div class="card" style="border-color:var(--warn)">\n    <h3>안전이 먼저입니다</h3>\n    <p class="muted" style="margin:0 0 11px">폭력·위협이 있거나 안전이 불확실하면 경계를 설명하려고 그 자리에 머물지 마세요. 먼저 안전한 곳으로 이동하고 위기 안내를 확인하세요.</p>\n    <button class="btn ghost sm" id="family-boundary-sos">가족 위기 안내 보기</button>\n  </div>\n  <button class="btn pri" id="family-boundary-new">내 경계 정리하기</button>\n  <div id="family-boundary-list" style="margin-top:12px"></div>\n</section>\n\n'''+marker
s=once(s,marker,page,'family boundary page')

# Route through tools tab infrastructure without adding a menu card.
old="""|| p === 'smart-relax' || p === 'smart-health' || p === 'smart-tools') ? 'tools' : p;"""
new="""|| p === 'smart-relax' || p === 'smart-health' || p === 'family-boundary' || p === 'smart-tools') ? 'tools' : p;"""
s=once(s,old,new,'family boundary tab route')
old="""  if(p === 'smart-health') drawSmartHealth();\n  if(p === 'smart-tools') drawSmartTools();"""
new="""  if(p === 'smart-health') drawSmartHealth();\n  if(p === 'family-boundary') drawFamilyBoundary();\n  if(p === 'smart-tools') drawSmartTools();"""
s=once(s,old,new,'family boundary draw route')

# Insert the small record/view/editor implementation before the SMART tools hub JS.
marker='''/* ══════════ SMART Recovery · 실천도구 허브 V8.2.11 ══════════ */'''
js=r'''/* ══════════ 가족 · 내 경계 정리 V8.2.33 ══════════
   경계는 상대에게 지키게 할 규칙이 아니라 가족인 내가 실행할 보호 행동으로 작성합니다.
   기존 S.smartWorks를 재사용하며 DATA_SCHEMA는 바꾸지 않습니다. */
function familyBoundaryRows(){
  return (Array.isArray(S.smartWorks)?S.smartWorks:[])
    .filter(r=>r && r.tool==='family-boundary' && r.role==='family')
    .slice().sort((a,b)=>Number(b.updatedAt||b.t||0)-Number(a.updatedAt||a.t||0));
}
function familyBoundaryDate(v){
  const d=new Date(Number(v)||Date.now());
  try{return d.toLocaleDateString('ko-KR',{year:'numeric',month:'short',day:'numeric'});}catch(_){return d.toLocaleDateString();}
}
function openFamilyBoundarySafety(){
  closeModal(); famTab='sos'; famI=0; go('fam');
}
function drawFamilyBoundary(){
  if(!famMode()){ toast('가족모드에서 사용하는 도구입니다.'); go('tools'); return; }
  const rows=familyBoundaryRows(), box=$('#family-boundary-list');
  if(box){
    box.innerHTML=rows.length
      ? '<h2 style="margin-top:0">저장한 경계</h2>'+rows.map(r=>'<button class="card" style="width:100%;text-align:left" data-fb-view="'+esc(r.rid||String(r.t))+'"><b>'+esc(r.situation||'내 경계')+'</b><div class="muted" style="margin-top:4px">'+esc(familyBoundaryDate(r.updatedAt||r.t))+' · '+esc(r.action||'')+'</div></button>').join('')
      : '<div class="note">아직 저장한 경계가 없습니다. 지금 실제로 지킬 수 있는 작은 경계 하나부터 정리해보세요.</div>';
    $$('[data-fb-view]').forEach(b=>b.onclick=()=>openFamilyBoundaryView(b.dataset.fbView));
  }
  const add=$('#family-boundary-new'), sos=$('#family-boundary-sos');
  if(add) add.onclick=()=>openFamilyBoundaryEditor();
  if(sos) sos.onclick=openFamilyBoundarySafety;
}
function familyBoundaryRecord(key){
  return familyBoundaryRows().find(r=>(r.rid||String(r.t))===key)||null;
}
function familyBoundarySection(title,text){
  return '<div class="card"><h3>'+esc(title)+'</h3><div style="white-space:pre-wrap">'+(String(text||'').trim()?esc(text):'<span class="muted">작성하지 않음</span>')+'</div></div>';
}
function openFamilyBoundaryView(key){
  const r=familyBoundaryRecord(key); if(!r) return;
  const risk=r.safety==='risk' ? '<div class="note" style="margin-bottom:12px;border-left:3px solid var(--bad)"><b>안전 위험이 있거나 확실하지 않음</b><br>경계를 전달하는 것보다 안전한 곳으로 이동하고 도움을 요청하는 것이 먼저입니다.<div style="height:8px"></div><button class="btn ghost sm" id="fb-view-sos">가족 위기 안내 보기</button></div>' : '';
  modal('<h2>'+esc(r.situation||'내 경계')+'</h2><p class="tiny" style="margin:4px 0 12px">'+esc(familyBoundaryDate(r.updatedAt||r.t))+' 정리</p>'+risk
    +familyBoundarySection('내가 지키고 싶은 것',r.protect)
    +familyBoundarySection('안전한 때 알리거나 요청할 말',r.request)
    +familyBoundarySection('경계가 지켜지지 않을 때 내가 할 행동',r.action)
    +(r.feasible==='smaller'?familyBoundarySection('조금 더 작게 정한 행동',r.smaller):'')
    +'<button class="btn sec" id="fb-edit">수정</button><div style="height:8px"></div><button class="btn danger" id="fb-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
  const sos=$('#fb-view-sos'); if(sos) sos.onclick=openFamilyBoundarySafety;
  $('#fb-edit').onclick=()=>openFamilyBoundaryEditor(r);
  $('#fb-delete').onclick=()=>{
    modal('<h2>이 경계 기록을 삭제할까요?</h2><p class="muted" style="margin:6px 0 14px">이 기록 한 건만 기기에서 삭제하며 되돌릴 수 없습니다.</p><button class="btn danger" id="fb-delete-ok">삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
    $('#fb-delete-ok').onclick=()=>{ const k=r.rid||String(r.t); S.smartWorks=(S.smartWorks||[]).filter(x=>(x.rid||String(x.t))!==k); save(); closeModal(); drawFamilyBoundary(); toast('삭제했습니다.'); };
  };
}
function openFamilyBoundaryEditor(record){
  const edit=!!record, v=record||{};
  modal('<h2>'+(edit?'내 경계 수정':'내 경계 정리')+'</h2>'
    +'<div class="field"><label>1. 어떤 상황이 힘든가요?</label><textarea id="fb-situation" maxlength="500" placeholder="예: 술에 취한 상태에서 고성이 시작될 때">'+esc(v.situation||'')+'</textarea></div>'
    +'<div class="field"><label>2. 내가 지키고 싶은 것은 무엇인가요?</label><textarea id="fb-protect" maxlength="500" placeholder="예: 아이와 나의 안전, 밤에 쉴 수 있는 공간">'+esc(v.protect||'')+'</textarea></div>'
    +'<div class="field"><label>3. 안전한 때 상대에게 알리거나 요청할 말이 있나요? <span class="muted">(선택)</span></label><textarea id="fb-request" maxlength="500" placeholder="예: 목소리가 커지면 저는 대화를 멈추고 자리를 옮기겠습니다.">'+esc(v.request||'')+'</textarea><div class="tiny muted" style="margin-top:5px">상대를 설득하거나 벌주기 위한 문장보다, 내가 할 행동을 알려주는 문장이 좋습니다.</div></div>'
    +'<div class="field"><label>4. 경계가 지켜지지 않을 때 내가 할 행동은 무엇인가요?</label><textarea id="fb-action" maxlength="500" placeholder="예: 대화를 중단하고 다른 방이나 안전한 곳으로 이동한다">'+esc(v.action||'')+'</textarea></div>'
    +'<div class="field"><label>5. 지금 내가 실제로 지킬 수 있는 크기인가요?</label><select id="fb-feasible"><option value="yes"'+((v.feasible||'yes')==='yes'?' selected':'')+'>지킬 수 있음</option><option value="smaller"'+(v.feasible==='smaller'?' selected':'')+'>조금 더 작게 정해야 함</option></select></div>'
    +'<div class="field" id="fb-smaller-wrap"><label>조금 더 작게 정한다면?</label><textarea id="fb-smaller" maxlength="500" placeholder="예: 우선 고성이 시작되면 10분 동안 다른 공간으로 이동한다">'+esc(v.smaller||'')+'</textarea></div>'
    +'<div class="field"><label>폭력·위협 등 안전 위험이 있나요?</label><select id="fb-safety"><option value="no"'+((v.safety||'no')==='no'?' selected':'')+'>현재 즉각적인 안전 위험은 아님</option><option value="risk"'+(v.safety==='risk'?' selected':'')+'>있음 또는 잘 모르겠음</option></select></div>'
    +'<div id="fb-risk-note"></div>'
    +'<button class="btn pri" id="fb-save">'+(edit?'수정 저장':'저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
  const feasible=$('#fb-feasible'), smallerWrap=$('#fb-smaller-wrap'), safety=$('#fb-safety'), risk=$('#fb-risk-note');
  const syncFeasible=()=>{ smallerWrap.style.display=feasible.value==='smaller'?'block':'none'; };
  const syncSafety=()=>{ risk.innerHTML=safety.value==='risk'?'<div class="note" style="margin-bottom:12px;border-left:3px solid var(--bad)"><b>이 화면보다 안전이 먼저입니다.</b><br>경계를 설명하거나 지키게 하려고 머물지 말고 안전한 곳으로 이동하세요.<div style="height:8px"></div><button class="btn ghost sm" id="fb-editor-sos">가족 위기 안내 보기</button></div>':''; const b=$('#fb-editor-sos'); if(b) b.onclick=openFamilyBoundarySafety; };
  feasible.onchange=syncFeasible; safety.onchange=syncSafety; syncFeasible(); syncSafety();
  $('#fb-save').onclick=()=>{
    const situation=$('#fb-situation').value.trim(), protect=$('#fb-protect').value.trim(), request=$('#fb-request').value.trim(), action=$('#fb-action').value.trim(), feasibleVal=feasible.value, smaller=$('#fb-smaller').value.trim(), safetyVal=safety.value;
    if(!situation){ toast('힘든 상황을 구체적으로 적어주세요.'); return; }
    if(!protect){ toast('내가 지키고 싶은 것을 적어주세요.'); return; }
    if(!action){ toast('그 상황에서 내가 할 행동을 적어주세요.'); return; }
    if(feasibleVal==='smaller' && !smaller){ toast('조금 더 작게 지킬 행동을 적어주세요.'); return; }
    const now=Date.now();
    const rec={rid:edit?(record.rid||smartWorkId()):smartWorkId(),tool:'family-boundary',role:'family',t:edit?Number(record.t||now):now,updatedAt:now,situation,protect,request,action,feasible:feasibleVal,smaller,safety:safetyVal};
    if(!Array.isArray(S.smartWorks)) S.smartWorks=[];
    const key=edit?(record.rid||String(record.t)):'';
    const i=edit?S.smartWorks.findIndex(x=>(x.rid||String(x.t))===key):-1;
    if(i>=0) S.smartWorks[i]=rec; else S.smartWorks.push(rec);
    save(); closeModal(); drawFamilyBoundary(); toast(edit?'경계를 수정했습니다.':'내 경계를 저장했습니다.');
  };
}

'''+marker
s=once(s,marker,js,'family boundary JS')
idx.write_text(s,encoding='utf-8')

w=sw.read_text(encoding='utf-8')
w=once(w,"const APP_VERSION = 'V8.2.32';","const APP_VERSION = 'V8.2.33';",'SW version')
w=once(w,"const V = 'ohg-v8232-family-integration-links';","const V = 'ohg-v8233-family-boundary';",'SW cache')
sw.write_text(w,encoding='utf-8')

r=readme.read_text(encoding='utf-8')
intro='''# V8.2.33 — 가족 `내 경계 정리` 최소 실천도구\n\n- 가족 안내의 기존 `경계를 지키는 것은 상대를 바꾸려는 것이 아닌 나를 지키는 것입니다` 글에서만 진입합니다. 별도 가족 메인메뉴는 만들지 않습니다.\n- 상황 → 내가 지키고 싶은 것 → 안전한 때 알리거나 요청할 말(선택) → 경계가 지켜지지 않을 때 **내가 할 행동** → 실제로 지킬 수 있는 크기 순서로 정리합니다.\n- 경계를 상대에게 지키게 하는 규칙이나 처벌로 작성하지 않고, 가족 자신의 보호 행동으로 작성하도록 안내합니다.\n- 폭력·위협 또는 안전이 불확실한 경우 기존 가족 `위기일 때` 안내로 바로 연결합니다.\n- 기록은 기존 `S.smartWorks`에 `tool: family-boundary`, `role: family`로 저장하며 수정·삭제가 가능합니다. `DATA_SCHEMA=6`은 유지합니다.\n- `대화 준비`는 이번 버전에서 추가하지 않습니다.\n- Android 이완 TTS·화면 OFF 재생·속도선택과 습관·생활·치료·외래 정확알림 엔진은 변경하지 않습니다.\n\n'''
if r.startswith('# V8.2.33'):
    raise SystemExit('README already patched')
readme.write_text(intro+r,encoding='utf-8')

print('V8.2.33 family boundary patch applied')