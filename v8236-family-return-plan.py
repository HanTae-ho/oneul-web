from pathlib import Path

idx=Path('index.html'); sw=Path('sw.js'); readme=Path('README.md')

def once(text, old, new, label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    return text.replace(old,new,1)

s=idx.read_text(encoding='utf-8')
s=once(s,"const BUILD = 'V8.2.35';","const BUILD = 'V8.2.36';",'BUILD')

# 1) Add a family-only reusable response plan page before the conversation tool.
marker='<!-- ══════════ 가족 · 대화 준비 V8.2.35 ══════════ -->'
page='''<!-- ══════════ 가족 · 다시 사용했을 때 내 대응계획 V8.2.36 ══════════ -->
<section class="pg" id="p-family-return-plan">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">다시 사용했을 때 내 대응계획</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('fam')">← 가족 안내</button>
  </div>
  <div class="note" style="margin-bottom:12px">상대의 재발일·사용량을 기록하거나 평가하는 화면이 아닙니다. 다시 사용하는 상황이 생겼을 때 <b>가족인 내가 안전하게 무엇을 하고, 무엇을 하지 않을지</b> 미리 정리하는 계획입니다.</div>
  <div class="card" style="border-color:var(--warn)">
    <h3>위험 신호가 있으면 계획보다 안전이 먼저입니다</h3>
    <p class="muted" style="margin:0 0 11px">의식·호흡·심한 금단, 자해·자살·타해, 폭력·위협 또는 아이의 안전이 걱정되면 대화를 이어가기보다 기존 가족 위기 안내를 먼저 확인하세요.</p>
    <button class="btn ghost sm" id="family-return-plan-sos">가족 위기 안내 보기</button>
  </div>
  <button class="btn pri" id="family-return-plan-new">내 대응계획 정리하기</button>
  <div id="family-return-plan-list" style="margin-top:12px"></div>
</section>

'''
s=once(s,marker,page+marker,'return plan page')

# 2) Add storage/view/editor using the existing S.smartWorks family pattern.
func_marker='function familyConversationRows(){'
funcs=r'''function familyReturnPlanRows(){
  return (S.smartWorks||[]).filter(r=>r && r.tool==='family-return-plan' && (r.role||'family')==='family')
    .slice().sort((a,b)=>Number(b.updatedAt||b.t||0)-Number(a.updatedAt||a.t||0));
}
function familyReturnPlanRiskLabel(v){
  if(v==='medical') return '몸 상태·금단이 걱정됨';
  if(v==='selfharm') return '자해·자살·타해가 걱정됨';
  if(v==='violence') return '폭력·위협·아이 안전이 걱정됨';
  if(v==='unknown') return '안전 여부를 잘 모르겠음';
  return '뚜렷한 위험 신호는 없음';
}
function familyReturnPlanNeedsSafety(v){ return v && v!=='safe'; }
function openFamilyReturnPlanSafety(){
  closeModal(); famTab='sos'; famI=0; go('fam');
}
function drawFamilyReturnPlan(){
  if(!famMode()){ toast('가족모드에서 사용하는 도구입니다.'); go('tools'); return; }
  const rows=familyReturnPlanRows(), box=$('#family-return-plan-list');
  if(box){
    box.innerHTML=rows.length
      ? '<h2 style="margin-top:0">저장한 대응계획</h2>'+rows.map(r=>'<button class="card" style="width:100%;text-align:left" data-frp-view="'+esc(r.rid||String(r.t))+'"><b>'+esc(r.situation||'내 대응계획')+'</b><div class="muted" style="margin-top:4px">'+esc(familyBoundaryDate(r.updatedAt||r.t))+' · '+esc(familyReturnPlanRiskLabel(r.risk))+(r.action?' · '+esc(r.action):'')+'</div></button>').join('')
      : '<div class="note">아직 저장한 대응계획이 없습니다. 일이 생긴 뒤 판단하기 어려울 수 있으니, 평온할 때 내가 할 행동 한두 가지부터 정리해두세요.</div>';
    $$('[data-frp-view]').forEach(b=>b.onclick=()=>openFamilyReturnPlanView(b.dataset.frpView));
  }
  const add=$('#family-return-plan-new'), sos=$('#family-return-plan-sos');
  if(add) add.onclick=()=>openFamilyReturnPlanEditor();
  if(sos) sos.onclick=openFamilyReturnPlanSafety;
}
function familyReturnPlanRecord(key){
  return familyReturnPlanRows().find(r=>(r.rid||String(r.t))===key)||null;
}
function openFamilyReturnPlanView(key){
  const r=familyReturnPlanRecord(key); if(!r) return;
  const part=(label,value)=>value?'<div class="field"><label>'+label+'</label><div class="note">'+esc(value)+'</div></div>':'';
  modal('<h2>다시 사용했을 때 내 대응계획</h2>'
    +part('예상하는 상황',r.situation)
    +part('먼저 확인할 안전',familyReturnPlanRiskLabel(r.risk))
    +part('그 순간 하지 않으려는 행동',r.avoid)
    +part('대신 내가 할 행동',r.action)
    +part('연락하거나 도움받을 사람·곳',r.support)
    +part('상황이 가라앉은 뒤 다음 행동',r.next)
    +(familyReturnPlanNeedsSafety(r.risk)?'<div class="note" style="margin-bottom:10px"><b>안전 우려가 있는 계획입니다.</b><br>실제 상황에서 위험 신호가 있으면 이 계획을 끝까지 수행하려 하지 말고 위기 도움을 먼저 사용하세요.</div><button class="btn ghost" id="frp-view-sos">가족 위기 안내 보기</button><div style="height:8px"></div>':'')
    +'<button class="btn sec" id="frp-edit">수정</button><div style="height:8px"></div><button class="btn ghost" id="frp-delete">삭제</button>');
  const vs=$('#frp-view-sos'); if(vs) vs.onclick=openFamilyReturnPlanSafety;
  $('#frp-edit').onclick=()=>{ closeModal(); openFamilyReturnPlanEditor(r); };
  $('#frp-delete').onclick=()=>{
    modal('<h2>이 대응계획을 삭제할까요?</h2><p class="muted" style="margin:6px 0 14px">이 계획 한 건만 기기에서 삭제하며 되돌릴 수 없습니다.</p><button class="btn danger" id="frp-delete-ok">삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
    $('#frp-delete-ok').onclick=()=>{ const k=r.rid||String(r.t); S.smartWorks=(S.smartWorks||[]).filter(x=>(x.rid||String(x.t))!==k); save(); closeModal(); drawFamilyReturnPlan(); toast('삭제했습니다.'); };
  };
}
function openFamilyReturnPlanEditor(record){
  const edit=!!record, v=record||{};
  modal('<h2>'+(edit?'대응계획 수정':'다시 사용했을 때 내 대응계획')+'</h2>'
    +'<div class="field"><label>1. 어떤 상황을 미리 준비해둘까요?</label><textarea id="frp-situation" maxlength="600" placeholder="예: 다시 술을 마신 상태로 집에 들어왔을 때">'+esc(v.situation||'')+'</textarea><div class="tiny muted" style="margin-top:5px">날짜·횟수·사용량을 기록하지 않고, 내가 준비할 상황만 적습니다.</div></div>'
    +'<div class="field"><label>2. 그때 가장 먼저 확인할 안전은?</label><select id="frp-risk"><option value="safe">뚜렷한 위험 신호는 없음</option><option value="medical">몸 상태·의식·호흡·금단이 걱정됨</option><option value="selfharm">자해·자살·타해가 걱정됨</option><option value="violence">폭력·위협 또는 아이 안전이 걱정됨</option><option value="unknown">안전 여부를 잘 모르겠음</option></select><div id="frp-risk-note" style="margin-top:7px"></div></div>'
    +'<div class="field"><label>3. 그 순간 하지 않으려는 행동 한 가지</label><textarea id="frp-avoid" maxlength="700" placeholder="예: 취한 상태에서 길게 따지거나 약속을 받아내지 않기">'+esc(v.avoid||'')+'</textarea></div>'
    +'<div class="field"><label>4. 대신 내가 할 행동은?</label><textarea id="frp-action" maxlength="700" placeholder="예: 아이와 안전한 공간으로 이동하고, 대화는 다음 날로 미루기">'+esc(v.action||'')+'</textarea><div class="tiny muted" style="margin-top:5px">상대를 통제하는 행동보다 내가 실제로 할 수 있는 행동을 적습니다.</div></div>'
    +'<div class="field"><label>5. 연락하거나 도움받을 사람·곳</label><textarea id="frp-support" maxlength="700" placeholder="예: 형제에게 연락, 가족모임, 상담기관">'+esc(v.support||'')+'</textarea></div>'
    +'<div class="field"><label>6. 상황이 가라앉은 뒤 내가 할 다음 행동</label><textarea id="frp-next" maxlength="700" placeholder="예: 다음 날 내 경계를 다시 확인하고, 필요하면 상담을 요청하기">'+esc(v.next||'')+'</textarea></div>'
    +'<button class="btn pri" id="frp-save">'+(edit?'수정 저장':'저장')+'</button>');
  const risk=$('#frp-risk'); risk.value=v.risk||'safe';
  const updateRisk=()=>{
    const n=$('#frp-risk-note'), val=risk.value;
    if(!n) return;
    if(familyReturnPlanNeedsSafety(val)) n.innerHTML='<div class="note"><b>안전이 먼저입니다.</b><br>실제 상황에서 위험 신호가 있으면 설득·추궁·경계 설명을 이어가기보다 안전한 곳으로 이동하고 즉시 도움을 요청하세요.<div style="height:8px"></div><button class="btn ghost sm" id="frp-risk-sos">가족 위기 안내 보기</button></div>';
    else n.innerHTML='<div class="tiny muted">위험 신호가 새로 생기면 계획보다 위기 도움을 먼저 사용합니다.</div>';
    const sb=$('#frp-risk-sos'); if(sb) sb.onclick=openFamilyReturnPlanSafety;
  };
  risk.onchange=updateRisk; updateRisk();
  $('#frp-save').onclick=()=>{
    const situation=$('#frp-situation').value.trim(), riskVal=risk.value, avoid=$('#frp-avoid').value.trim(), action=$('#frp-action').value.trim(), support=$('#frp-support').value.trim(), next=$('#frp-next').value.trim();
    if(!situation){ toast('미리 준비할 상황을 적어주세요.'); return; }
    if(!avoid){ toast('그 순간 하지 않으려는 행동 한 가지를 적어주세요.'); return; }
    if(!action){ toast('대신 내가 할 행동을 적어주세요.'); return; }
    if(!support){ toast('연락하거나 도움받을 사람·곳을 적어주세요.'); return; }
    const now=Date.now();
    const rec={rid:edit?(record.rid||smartWorkId()):smartWorkId(),tool:'family-return-plan',role:'family',t:edit?Number(record.t||now):now,updatedAt:now,situation,risk:riskVal,avoid,action,support,next};
    if(!Array.isArray(S.smartWorks)) S.smartWorks=[];
    const key=edit?(record.rid||String(record.t)):'';
    const i=edit?S.smartWorks.findIndex(x=>(x.rid||String(x.t))===key):-1;
    if(i>=0) S.smartWorks[i]=rec; else S.smartWorks.push(rec);
    save(); closeModal(); drawFamilyReturnPlan(); toast(edit?'대응계획을 수정했습니다.':'내 대응계획을 저장했습니다.');
  };
}

'''
s=once(s,func_marker,funcs+func_marker,'return plan functions')

# 3) Existing family relapse article becomes the entry point. Keep its wording; only add the practice action.
old="{h:'재발은 흔한 일입니다',\n     b:'재발은 회복이 실패한 증거가 아니라, 회복 과정에서 자주 일어나는 일입니다."
new="{h:'재발은 흔한 일입니다', a:'family-return-plan', al:'내 대응계획 정리하기',\n     b:'재발은 회복이 실패한 증거가 아니라, 회복 과정에서 자주 일어나는 일입니다."
s=once(s,old,new,'relapse article action')

# 4) Family guide route.
s=once(s,"  if(action==='family-conversation'){ go('family-conversation'); return; }","  if(action==='family-return-plan'){ go('family-return-plan'); return; }\n  if(action==='family-conversation'){ go('family-conversation'); return; }",'family guide return route')

# 5) Page draw dispatch.
s=once(s,"  if(p === 'family-conversation') drawFamilyConversation();","  if(p === 'family-return-plan') drawFamilyReturnPlan();\n  if(p === 'family-conversation') drawFamilyConversation();",'return plan dispatch')

idx.write_text(s,encoding='utf-8')

w=sw.read_text(encoding='utf-8')
w=once(w,"const APP_VERSION = 'V8.2.35';","const APP_VERSION = 'V8.2.36';",'sw version')
w=once(w,"const V = 'ohg-v8235-family-conversation';","const V = 'ohg-v8236-family-return-plan';",'sw cache')
sw.write_text(w,encoding='utf-8')

r=readme.read_text(encoding='utf-8')
head='''# V8.2.36 — 가족 `다시 사용했을 때 내 대응계획`\n\n- 상대의 재발일·사용량을 기록하지 않고, 다시 사용하는 상황에서 가족 자신의 안전·행동·지원 계획만 정리합니다.\n- 가족 안내의 `재발은 흔한 일입니다` 글에서 `내 대응계획 정리하기`로 들어갑니다.\n- 작성 흐름: 준비할 상황 → 먼저 확인할 안전 → 하지 않으려는 행동 → 대신 내가 할 행동 → 연락·지원 → 상황이 가라앉은 뒤 다음 행동.\n- 몸 상태·금단, 자해·자살·타해, 폭력·위협·아이 안전 또는 안전 여부가 불확실한 경우 기존 가족 위기 안내를 우선 연결합니다.\n- 기록은 기존 `S.smartWorks`에 `tool: family-return-plan / role: family`로 저장하며 보기·수정·삭제를 지원합니다.\n- Family & Friends의 `Coping with Lapses`는 실수에서 배우고 자신의 반응을 다시 계획한다는 관점만 참고하고, 기계번역 문구·워크시트 구조는 복제하지 않습니다.\n- `DATA_SCHEMA=6`, 가족 충동·재발 비기록, 기존 경계·대화 준비, SMART/12단계, Local-first를 유지합니다.\n- Android 이완 TTS·화면 OFF 재생·속도선택·정확알림 엔진은 변경하지 않습니다.\n\n'''
readme.write_text(head+r,encoding='utf-8')
