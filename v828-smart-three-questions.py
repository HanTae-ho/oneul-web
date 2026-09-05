from pathlib import Path

idx=Path('index.html')
learn=Path('learning-data.js')
sw=Path('sw.js')

s=idx.read_text(encoding='utf-8')
ld=learn.read_text(encoding='utf-8')
swt=sw.read_text(encoding='utf-8')

assert "const BUILD = 'V8.2.7';" in s
s=s.replace("const BUILD = 'V8.2.7';","const BUILD = 'V8.2.8';",1)
ld=ld.replace('회복학습 데이터 V8.2.7','회복학습 데이터 V8.2.8',1)
assert "const APP_VERSION = 'V8.2.7';" in swt
assert "const V = 'ohg-v827-smart-change-plan';" in swt
swt=swt.replace("const APP_VERSION = 'V8.2.7';","const APP_VERSION = 'V8.2.8';",1)
swt=swt.replace("const V = 'ohg-v827-smart-change-plan';","const V = 'ohg-v828-smart-three-questions';",1)

# Add page after Change Plan page.
anchor='''  <div id="smart-change-plan-role-note"></div>\n  <button class="btn sec" id="smart-change-plan-new">+ 변화 계획 새로 작성하기</button>\n  <div id="smart-change-plan-list" style="margin-top:12px"></div>\n</section>\n'''
assert anchor in s
page='''\n<!-- ══════════ SMART Recovery · My Three Questions V8.2.8 ══════════ -->\n<section class="pg" id="p-smart-three-questions">\n  <div class="sp" style="margin-bottom:11px">\n    <h1 style="margin:0">나의 3가지 질문</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="go('learn-topic')">← SMART Recovery</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    내가 원하는 미래와 현재 행동의 차이를 알아차리고, 그 차이를 변화 동기로 활용합니다. SMART Recovery의 <b>My Three Questions worksheet</b>를 앱에 맞게 재구성했으며, <b>내용은 이 기기에만 저장</b>됩니다.\n  </div>\n  <div id="smart-three-role-note"></div>\n  <button class="btn sec" id="smart-three-new">+ 새로 작성하기</button>\n  <div id="smart-three-list" style="margin-top:12px"></div>\n</section>\n'''
s=s.replace(anchor,anchor+page,1)

# Route/action.
route="  if(p === 'smart-change-plan') drawSmartChangePlan();\n"
assert route in s
s=s.replace(route,route+"  if(p === 'smart-three-questions') drawSmartThreeQuestions();\n",1)
action="  if(type === 'smart-change-plan'){ go('smart-change-plan'); return; }\n"
assert action in s
s=s.replace(action,action+"  if(type === 'smart-three-questions'){ go('smart-three-questions'); return; }\n",1)

# Functions before learningAction.
fn_anchor="function learningAction(type){\n"
assert fn_anchor in s
block=r'''/* ── SMART Recovery · 나의 3가지 질문 V8.2.8 ──
   원자료 명칭은 My Three Questions이지만 실제 워크시트는 처음 3문항 뒤 추가 2문항으로 이어집니다.
   3번(현재 행동의 느낌)과 5번(변화 뒤 예상 느낌)의 차이를 변화 동기로 확인합니다. */
function smartThreeRecords(){
  return (Array.isArray(S.smartWorks)?S.smartWorks:[])
    .filter(r=>r && r.kind==='three-questions' && (r.role||'self')===(famMode()?'family':'self'))
    .sort((a,b)=>(b.updatedAt||b.ts||0)-(a.updatedAt||a.ts||0));
}
function smartThreeDate(ts){
  if(!ts) return '';
  const d=new Date(ts); return d.getFullYear()+'. '+(d.getMonth()+1)+'. '+d.getDate()+'.';
}
function drawSmartThreeQuestions(){
  const list=$('#smart-three-list'), rn=$('#smart-three-role-note'), add=$('#smart-three-new');
  if(!list||!add) return;
  if(rn){
    rn.innerHTML=famMode()
      ? '<div class="note" style="margin-bottom:12px"><b>가족도 내 미래와 내 행동을 질문합니다.</b><br>상대의 변화 여부가 아니라, 내가 원하는 삶과 현재 내가 하고 있는 행동 사이의 차이를 살펴봅니다.</div>'
      : '';
  }
  add.onclick=()=>openSmartThreeEditor(null);
  const rows=smartThreeRecords();
  if(!rows.length){
    list.innerHTML='<div class="card"><b>아직 작성한 기록이 없습니다.</b><p class="muted" style="margin:5px 0 0">먼저 내가 원하는 미래를 한 문장으로 적어보세요.</p></div>';
    return;
  }
  list.innerHTML='<div class="card"><h3>저장한 기록 '+rows.length+'건</h3>'
    +rows.map(r=>'<div class="sp" style="gap:10px;padding:11px 0;border-top:1px solid var(--line)"><div style="min-width:0;flex:1"><div class="tiny">'+esc(smartThreeDate(r.updatedAt||r.ts))+'</div><b style="display:block;margin-top:2px">'+esc(r.future||'나의 3가지 질문')+'</b><div class="muted" style="margin-top:3px">현재와 원하는 미래의 차이를 돌아본 기록</div></div><button class="tiny" style="color:var(--acc);font-weight:600" onclick="openSmartThreeView(\''+esc(r.id)+'\')">보기</button></div>').join('')
    +'</div>';
}
function openSmartThreeEditor(record){
  const edit=!!record;
  const q=(n,title,help,id,val,ph)=>'<div class="card"><div class="tiny" style="color:var(--acc);font-weight:700">질문 '+n+'</div><h3 style="margin-top:4px">'+esc(title)+'</h3>'+(help?'<p class="muted" style="margin:-5px 0 9px">'+esc(help)+'</p>':'')+'<textarea id="'+id+'" maxlength="900" placeholder="'+esc(ph)+'">'+esc(edit?(val||''):'')+'</textarea></div>';
  modal('<h2>'+(edit?'나의 3가지 질문 수정':'나의 3가지 질문 작성')+'</h2>'
    +'<p class="muted" style="margin:5px 0 14px">도구 이름은 ‘3가지 질문’이지만, 처음 세 질문 뒤에 두 질문을 더 이어서 답합니다.</p>'
    +'<div class="note" style="margin-bottom:12px"><b>먼저 세 가지 질문</b><br>내가 원하는 미래와 지금의 행동을 비교합니다.</div>'
    +q(1,'내 미래에 대해 어떤 것을 원하나요?','', 'three-future', edit?record.future:'','예: 좋은 부모가 되고 싶다. 건강하고 안정된 생활을 하고 싶다.')
    +q(2,'그것을 달성하기 위해 나는 현재 무엇을 하고 있나요?','현재 실제로 하고 있는 행동을 적어보세요.', 'three-current', edit?record.current:'','예: 술을 마시며 약속을 미루고 있다. 반대로 모임과 외래는 유지하고 있다.')
    +q(3,'현재 내가 하고 있는 일(행동)에 대해 어떤 느낌을 가지고 있나요?','감정을 옳고 그름으로 판단하지 말고 있는 그대로 적어보세요.', 'three-feeling-now', edit?record.feelingNow:'','예: 죄책감, 답답함, 불안, 지침, 갇힌 느낌')
    +'<div class="note" style="margin:14px 0 12px"><b>이제 다음 두 질문</b><br>원하는 미래를 위해 달리할 수 있는 행동과, 변화 뒤의 느낌을 생각합니다.</div>'
    +q(4,'내가 원하는 미래를 달성하거나 이루기 위해 무엇을 달리할 수 있을까요?','가능하면 작고 구체적인 행동으로 적어보세요.', 'three-different', edit?record.different:'','예: 오늘 술자리를 피하고 회복 동료에게 연락한다.')
    +q(5,'내가 하는 일(행동)을 바꾸거나 내가 원하는 것을 얻으면 어떤 느낌이 들까요?','3번에서 적은 현재의 느낌과 비교해보세요.', 'three-feeling-after', edit?record.feelingAfter:'','예: 안도감, 자신감, 자유로움, 가족에게 떳떳함')
    +'<div class="card"><h3>내가 발견한 차이</h3><p class="muted" style="margin:-5px 0 9px">3번과 5번의 느낌 차이에서, 지금 변화를 시작할 이유를 한 문장으로 적어보세요.</p><textarea id="three-gap" maxlength="500" placeholder="예: 지금은 갇힌 느낌이지만, 행동을 바꾸면 자유롭고 떳떳해질 수 있다.">'+esc(edit?(record.gap||''):'')+'</textarea></div>'
    +'<button class="btn" id="three-save">'+(edit?'수정 저장':'기록 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
  $('#three-save').onclick=()=>{
    const future=$('#three-future').value.trim(), current=$('#three-current').value.trim(), feelingNow=$('#three-feeling-now').value.trim(), different=$('#three-different').value.trim(), feelingAfter=$('#three-feeling-after').value.trim();
    if(!future||!current||!feelingNow||!different||!feelingAfter){ toast('다섯 질문에 모두 답해 주세요.'); return; }
    const now=Date.now();
    const rec={
      id:edit?record.id:('tq-'+now+'-'+Math.random().toString(36).slice(2,7)), kind:'three-questions', role:famMode()?'family':'self',
      ts:edit?(record.ts||now):now, updatedAt:now,
      future, current, feelingNow, different, feelingAfter, gap:$('#three-gap').value.trim()
    };
    if(!Array.isArray(S.smartWorks)) S.smartWorks=[];
    if(edit){ const i=S.smartWorks.findIndex(x=>x&&x.id===record.id); if(i>=0) S.smartWorks[i]=rec; else S.smartWorks.push(rec); }
    else S.smartWorks.push(rec);
    save(); closeModal(); drawSmartThreeQuestions(); toast(edit?'기록을 수정했습니다.':'기록을 저장했습니다.');
  };
}
function openSmartThreeView(id){
  const r=(Array.isArray(S.smartWorks)?S.smartWorks:[]).find(x=>x&&x.id===id&&x.kind==='three-questions');
  if(!r) return;
  const sec=(n,title,text)=>'<div class="card"><div class="tiny" style="color:var(--acc);font-weight:700">질문 '+n+'</div><h3 style="margin-top:4px">'+esc(title)+'</h3><div style="white-space:pre-wrap">'+esc(text||'')+'</div></div>';
  modal('<h2>나의 3가지 질문</h2><div class="muted" style="margin:-4px 0 12px">'+esc(smartThreeDate(r.updatedAt||r.ts))+'</div>'
    +sec(1,'내 미래에 대해 원하는 것',r.future)
    +sec(2,'그것을 위해 현재 하고 있는 것',r.current)
    +sec(3,'현재 행동에 대한 느낌',r.feelingNow)
    +sec(4,'달리할 수 있는 것',r.different)
    +sec(5,'행동을 바꾸거나 원하는 것을 얻었을 때의 느낌',r.feelingAfter)
    +(r.gap?'<div class="note" style="margin-bottom:12px"><b>내가 발견한 차이</b><br><span style="white-space:pre-wrap">'+esc(r.gap)+'</span></div>':'')
    +'<button class="btn" id="three-to-plan">이 답을 바탕으로 변화 계획 작성하기</button><div style="height:8px"></div><button class="btn sec" id="three-edit">수정</button><div style="height:8px"></div><button class="btn bad" id="three-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
  $('#three-to-plan').onclick=()=>{
    closeModal(); go('smart-change-plan');
    setTimeout(()=>openSmartChangePlanEditor({
      id:'', ts:Date.now(), change:r.future||'', importance:8, confidence:5,
      reasons:r.gap||r.feelingAfter||'', steps:r.different||'', help:'', signs:'', obstacles:''
    }),60);
  };
  $('#three-edit').onclick=()=>openSmartThreeEditor(r);
  $('#three-delete').onclick=()=>{
    if(!confirm('이 질문 기록을 삭제할까요?')) return;
    S.smartWorks=(Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>!(x&&x.id===r.id));
    save(); closeModal(); drawSmartThreeQuestions(); toast('기록을 삭제했습니다.');
  };
}

'''
s=s.replace(fn_anchor,block+fn_anchor,1)

# Correct action order based on uploaded appendix: HOV -> My Three Questions -> Change Plan -> CBA.
old='''          {\n            "type": "smart-hov",\n            "label": "HOV 가치의 계층 작성하기"\n          },\n          {\n            "type": "smart-change-plan",\n            "label": "변화 계획 워크시트 작성하기"\n          },\n          {\n            "type": "smart-cba",\n            "label": "CBA 비용-편익 분석 작성하기"\n          }'''
new='''          {\n            "type": "smart-hov",\n            "label": "HOV 가치의 계층 작성하기"\n          },\n          {\n            "type": "smart-three-questions",\n            "label": "나의 3가지 질문 작성하기"\n          },\n          {\n            "type": "smart-change-plan",\n            "label": "변화 계획 워크시트 작성하기"\n          },\n          {\n            "type": "smart-cba",\n            "label": "CBA 비용-편익 분석 작성하기"\n          }'''
assert old in ld
ld=ld.replace(old,new,1)

idx.write_text(s,encoding='utf-8')
learn.write_text(ld,encoding='utf-8')
sw.write_text(swt,encoding='utf-8')
print('V8.2.8 My Three Questions patch applied')
