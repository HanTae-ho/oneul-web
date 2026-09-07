from pathlib import Path

idx=Path('index.html'); sw=Path('sw.js'); readme=Path('README.md')

def once(text, old, new, label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    return text.replace(old,new,1)

s=idx.read_text(encoding='utf-8')
s=once(s,"const BUILD = 'V8.2.34';","const BUILD = 'V8.2.35';",'BUILD')

# 1) Add a compact family-only conversation preparation page before the existing boundary tool.
marker='<!-- ══════════ 가족 · 내 경계 정리 V8.2.33 ══════════ -->'
page='''<!-- ══════════ 가족 · 대화 준비 V8.2.35 ══════════ -->
<section class="pg" id="p-family-conversation">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">대화 준비</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('fam')">← 가족 안내</button>
  </div>
  <div class="note" style="margin-bottom:12px">상대를 설득하거나 바꾸는 대화법이 아닙니다. 내가 말하려는 <b>사실 · 느낌과 필요 · 구체적인 부탁</b>을 미리 정리해, 불필요한 비난과 긴 논쟁을 줄이는 데 사용합니다.</div>
  <div class="card" style="border-color:var(--warn)">
    <h3>대화보다 때와 안전이 먼저입니다</h3>
    <p class="muted" style="margin:0 0 11px">취해 있거나 감정이 크게 격한 때는 지금 해결하려 하지 않아도 됩니다. 폭력·위협이 있거나 안전이 걱정되면 대화를 준비하기보다 먼저 안전한 곳으로 이동하고 위기 안내를 확인하세요.</p>
    <button class="btn ghost sm" id="family-conversation-sos">가족 위기 안내 보기</button>
  </div>
  <button class="btn pri" id="family-conversation-new">대화 준비하기</button>
  <div id="family-conversation-list" style="margin-top:12px"></div>
</section>

'''
s=once(s,marker,page+marker,'conversation page')

# 2) Add family conversation storage/view/editor using the existing S.smartWorks pattern.
func_marker='function openFamilyBoundarySafety(){'
funcs=r'''function familyConversationRows(){
  return (S.smartWorks||[]).filter(r=>r && r.tool==='family-conversation' && (r.role||'family')==='family')
    .slice().sort((a,b)=>Number(b.updatedAt||b.t||0)-Number(a.updatedAt||a.t||0));
}
function familyConversationDate(v){
  const d=new Date(Number(v||Date.now()));
  try{return d.toLocaleDateString('ko-KR',{year:'numeric',month:'short',day:'numeric'});}catch(_){return d.toLocaleDateString();}
}
function familyConversationTimingLabel(v){
  if(v==='wait') return '지금은 미루기';
  if(v==='unsafe') return '안전 먼저';
  return '대화할 수 있음';
}
function openFamilyConversationSafety(){
  closeModal(); famTab='sos'; famI=0; go('fam');
}
function drawFamilyConversation(){
  if(!famMode()){ toast('가족모드에서 사용하는 도구입니다.'); go('tools'); return; }
  const rows=familyConversationRows(), box=$('#family-conversation-list');
  if(box){
    box.innerHTML=rows.length
      ? '<h2 style="margin-top:0">저장한 대화 준비</h2>'+rows.map(r=>'<button class="card" style="width:100%;text-align:left" data-fc-view="'+esc(r.rid||String(r.t))+'"><b>'+esc(r.topic||'대화 준비')+'</b><div class="muted" style="margin-top:4px">'+esc(familyConversationDate(r.updatedAt||r.t))+' · '+esc(familyConversationTimingLabel(r.timing))+(r.sentence?' · '+esc(r.sentence):'')+'</div></button>').join('')
      : '<div class="note">아직 저장한 대화 준비가 없습니다. 지금 말할 때인지부터 확인하고, 실제로 전하고 싶은 한 가지를 짧게 정리해보세요.</div>';
    $$('[data-fc-view]').forEach(b=>b.onclick=()=>openFamilyConversationView(b.dataset.fcView));
  }
  const add=$('#family-conversation-new'), sos=$('#family-conversation-sos');
  if(add) add.onclick=()=>openFamilyConversationEditor();
  if(sos) sos.onclick=openFamilyConversationSafety;
}
function familyConversationRecord(key){
  return familyConversationRows().find(r=>(r.rid||String(r.t))===key)||null;
}
function openFamilyConversationView(key){
  const r=familyConversationRecord(key); if(!r) return;
  const part=(label,value)=>value?'<div class="field"><label>'+label+'</label><div class="note">'+esc(value)+'</div></div>':'';
  modal('<h2>대화 준비</h2>'
    +part('이야기하려는 상황',r.topic)
    +part('지금 이야기할 때인가요?',familyConversationTimingLabel(r.timing))
    +part('사실만 적어보기',r.fact)
    +part('내 느낌 · 필요한 것',r.feeling)
    +part('구체적으로 부탁할 한 가지',r.request)
    +part('내가 실제로 말할 한 문장',r.sentence)
    +(r.timing==='unsafe'?'<div class="note" style="margin-bottom:10px"><b>안전이 먼저입니다.</b><br>폭력·위협 또는 안전 우려가 있다면 대화를 이어가기보다 안전한 곳으로 이동하고 도움을 요청하세요.</div><button class="btn ghost" id="fc-view-sos">가족 위기 안내 보기</button><div style="height:8px"></div>':'')
    +'<button class="btn sec" id="fc-edit">수정</button><div style="height:8px"></div><button class="btn ghost" id="fc-delete">삭제</button>');
  const vs=$('#fc-view-sos'); if(vs) vs.onclick=openFamilyConversationSafety;
  $('#fc-edit').onclick=()=>{ closeModal(); openFamilyConversationEditor(r); };
  $('#fc-delete').onclick=()=>{
    modal('<h2>이 대화 준비 기록을 삭제할까요?</h2><p class="muted" style="margin:6px 0 14px">이 기록 한 건만 기기에서 삭제하며 되돌릴 수 없습니다.</p><button class="btn danger" id="fc-delete-ok">삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
    $('#fc-delete-ok').onclick=()=>{ const k=r.rid||String(r.t); S.smartWorks=(S.smartWorks||[]).filter(x=>(x.rid||String(x.t))!==k); save(); closeModal(); drawFamilyConversation(); toast('삭제했습니다.'); };
  };
}
function openFamilyConversationEditor(record){
  const edit=!!record, v=record||{};
  modal('<h2>'+(edit?'대화 준비 수정':'대화 준비')+'</h2>'
    +'<div class="field"><label>1. 무슨 이야기를 하려 하나요?</label><textarea id="fc-topic" maxlength="500" placeholder="예: 어제 연락 없이 늦게 귀가한 일">'+esc(v.topic||'')+'</textarea></div>'
    +'<div class="field"><label>2. 지금 이야기해도 되는 때인가요?</label><select id="fc-timing"><option value="ready">비교적 안정되어 있고 대화할 수 있음</option><option value="wait">취해 있거나 감정이 격함 — 지금은 미루기</option><option value="unsafe">폭력·위협 또는 안전이 걱정됨 — 안전 먼저</option></select><div id="fc-timing-note" style="margin-top:7px"></div></div>'
    +'<div class="field"><label>3. 판단하지 않고 사실만 적어보면?</label><textarea id="fc-fact" maxlength="700" placeholder="예: 어제 연락 없이 밤 11시를 넘겨 귀가했다.">'+esc(v.fact||'')+'</textarea><div class="tiny muted" style="margin-top:5px">“항상”, “절대”, “왜 그 모양이야” 같은 평가보다 실제 있었던 일을 적습니다.</div></div>'
    +'<div class="field"><label>4. 그 일에서 내가 느낀 것 · 필요한 것은?</label><textarea id="fc-feeling" maxlength="700" placeholder="예: 많이 불안했다. 늦어질 때는 연락이 필요하다.">'+esc(v.feeling||'')+'</textarea></div>'
    +'<div class="field"><label>5. 구체적으로 부탁할 한 가지는?</label><textarea id="fc-request" maxlength="700" placeholder="예: 늦어질 것 같으면 문자 한 통을 부탁하고 싶다.">'+esc(v.request||'')+'</textarea><div class="tiny muted" style="margin-top:5px">상대를 통제하는 명령보다, 지금 필요한 행동 한 가지를 구체적으로 적습니다.</div></div>'
    +'<div class="field"><label>6. 내가 실제로 말할 한 문장</label><textarea id="fc-sentence" maxlength="900" placeholder="사실 → 내 느낌·필요 → 구체적인 부탁 순서로 짧게 정리해보세요.">'+esc(v.sentence||'')+'</textarea></div>'
    +'<button class="btn pri" id="fc-save">'+(edit?'수정 저장':'저장')+'</button>');
  const timing=$('#fc-timing'); timing.value=v.timing||'ready';
  const updateTiming=()=>{
    const n=$('#fc-timing-note'), val=timing.value;
    if(!n) return;
    if(val==='wait') n.innerHTML='<div class="note">지금 해결하려 하지 않아도 됩니다. 취기가 가시고 감정이 조금 가라앉은 뒤 다시 이야기해도 됩니다.</div>';
    else if(val==='unsafe') n.innerHTML='<div class="note"><b>대화보다 안전이 먼저입니다.</b><br>폭력·위협이 있거나 안전이 불확실하면 자리를 벗어나고 도움을 요청하세요.<div style="height:8px"></div><button class="btn ghost sm" id="fc-timing-sos">가족 위기 안내 보기</button></div>';
    else n.innerHTML='<div class="tiny muted">서로 비교적 안정되어 있을 때, 짧고 구체적으로 이야기하는 편이 좋습니다.</div>';
    const sb=$('#fc-timing-sos'); if(sb) sb.onclick=openFamilyConversationSafety;
  };
  timing.onchange=updateTiming; updateTiming();
  $('#fc-save').onclick=()=>{
    const topic=$('#fc-topic').value.trim(), timingVal=timing.value, fact=$('#fc-fact').value.trim(), feeling=$('#fc-feeling').value.trim(), request=$('#fc-request').value.trim(), sentence=$('#fc-sentence').value.trim();
    if(!topic){ toast('이야기하려는 상황을 적어주세요.'); return; }
    if(!fact){ toast('평가하지 않은 사실을 한 가지 적어주세요.'); return; }
    if(timingVal==='ready' && !feeling){ toast('내가 느낀 것 또는 필요한 것을 적어주세요.'); return; }
    if(timingVal==='ready' && !request){ toast('구체적으로 부탁할 한 가지를 적어주세요.'); return; }
    if(timingVal==='ready' && !sentence){ toast('실제로 말할 한 문장을 적어주세요.'); return; }
    const now=Date.now();
    const rec={rid:edit?(record.rid||smartWorkId()):smartWorkId(),tool:'family-conversation',role:'family',t:edit?Number(record.t||now):now,updatedAt:now,topic,timing:timingVal,fact,feeling,request,sentence};
    if(!Array.isArray(S.smartWorks)) S.smartWorks=[];
    const key=edit?(record.rid||String(record.t)):'';
    const i=edit?S.smartWorks.findIndex(x=>(x.rid||String(x.t))===key):-1;
    if(i>=0) S.smartWorks[i]=rec; else S.smartWorks.push(rec);
    save(); closeModal(); drawFamilyConversation(); toast(edit?'대화 준비를 수정했습니다.':'대화 준비를 저장했습니다.');
  };
}

'''
s=once(s,func_marker,funcs+func_marker,'conversation functions')

# 3) Family guide article: use the new tool and soften a deterministic causal sentence.
old_head="{h:'말할 때는 그 사람이 아니라 일에 대해', a:'smart-abc', al:'내 반응을 ABC로 살펴보기',"
new_head="{h:'말할 때는 그 사람이 아니라 일에 대해', a:'family-conversation', al:'대화 준비하기',"
s=once(s,old_head,new_head,'conversation article action')
old_body='''     b:'"너는 왜 그 모양이냐" 는 사람을 공격하고, 공격받으면 숨습니다. 숨으면 다시 마십니다.\\\n' +'''
new_body='''     b:'"너는 왜 그 모양이냐" 같은 말은 사람 전체를 평가하는 말로 들려 대화가 닫히거나 방어가 커질 수 있습니다.\\\n' +'''
s=once(s,old_body,new_body,'conversation article wording')

# 4) Family guide action route.
s=once(s,"""  if(action==='help'){ go('help'); return; }\n  if(action==='family-boundary'){ go('family-boundary'); return; }""","""  if(action==='help'){ go('help'); return; }\n  if(action==='family-conversation'){ go('family-conversation'); return; }\n  if(action==='family-boundary'){ go('family-boundary'); return; }""",'family guide route')

# 5) Add a discoverable shortcut at the top of the '중독 이해하기' family guide tab.
old_top='''      : '';\n  const fbs=$('#fam-boundary-shortcut'); if(fbs) fbs.onclick=()=>go('family-boundary');'''
new_top='''      : (famTab === 'know')\n        ? '<div class="card tight">' +\n          '<h3 style="margin:0 0 5px">바로 해보기</h3>' +\n          '<p class="muted" style="margin:0 0 10px">말하기 전에 사실·내 마음·구체적인 부탁 한 가지를 짧게 정리합니다.</p>' +\n          '<button class="btn sec sm" id="fam-conversation-shortcut">대화 준비</button></div>'\n        : '';\n  const fbs=$('#fam-boundary-shortcut'); if(fbs) fbs.onclick=()=>go('family-boundary');\n  const fcs=$('#fam-conversation-shortcut'); if(fcs) fcs.onclick=()=>go('family-conversation');'''
s=once(s,old_top,new_top,'conversation shortcut')

# 6) Page draw dispatch.
s=once(s,"""  if(p === 'smart-health') drawSmartHealth();\n  if(p === 'family-boundary') drawFamilyBoundary();""","""  if(p === 'smart-health') drawSmartHealth();\n  if(p === 'family-conversation') drawFamilyConversation();\n  if(p === 'family-boundary') drawFamilyBoundary();""",'draw dispatch')

idx.write_text(s,encoding='utf-8')

w=sw.read_text(encoding='utf-8')
w=once(w,"const APP_VERSION = 'V8.2.34';","const APP_VERSION = 'V8.2.35';",'SW version')
w=once(w,"const V = 'ohg-v8234-family-navigation';","const V = 'ohg-v8235-family-conversation';",'SW cache')
sw.write_text(w,encoding='utf-8')

r=readme.read_text(encoding='utf-8')
intro='''# V8.2.35 — 가족 대화 준비 최소 실천도구\n\n- 가족 안내의 `말할 때는 그 사람이 아니라 일에 대해` 글에서 `대화 준비하기`로 이어집니다.\n- `중독 이해하기` 화면 상단에도 `대화 준비` 바로가기를 둡니다.\n- 작성 흐름: 이야기할 상황 → 지금 말할 때인지 → 사실 → 내 느낌·필요 → 구체적인 부탁 → 실제로 말할 한 문장.\n- 취해 있거나 감정이 격하면 `지금은 미루기`, 폭력·위협·안전 우려가 있으면 `안전 먼저`를 선택할 수 있습니다.\n- 안전 우려 시 기존 가족 위기 안내로 바로 연결합니다.\n- 기록은 기존 `S.smartWorks`에 `tool: family-conversation / role: family`로 저장하며 목록·보기·수정·삭제를 지원합니다.\n- 가족 안내의 단정적 문구 `공격받으면 숨습니다. 숨으면 다시 마십니다.`는 대화가 닫히거나 방어가 커질 수 있다는 비단정적 표현으로 수정했습니다.\n- Family & Friends의 전문용어·워크시트 문구를 복제하지 않고 오늘 한 걸음의 가족 원칙에 맞게 독자적으로 구성했습니다.\n- `DATA_SCHEMA=6`, 기존 family-boundary 기록, 가족 충동·재발 비기록, SMART/12단계, Local-first를 유지합니다.\n- Android 이완 TTS·화면 OFF 재생·속도선택·정확알림 엔진은 변경하지 않습니다.\n\n'''
readme.write_text(intro+r,encoding='utf-8')
print('V8.2.35 family conversation patch applied')
