from pathlib import Path

idx = Path('index.html')
learn = Path('learning-data.js')
sw = Path('sw.js')

s = idx.read_text(encoding='utf-8')
ld = learn.read_text(encoding='utf-8')
swtxt = sw.read_text(encoding='utf-8')

assert "const BUILD = 'V8.2.6';" in s
s = s.replace("const BUILD = 'V8.2.6';", "const BUILD = 'V8.2.7';", 1)

# Add Change Plan page directly after the CBA page.
anchor = '''  <div id="smart-cba-role-note"></div>\n  <button class="btn sec" id="smart-cba-new">+ CBA 새로 작성하기</button>\n  <div id="smart-cba-list" style="margin-top:12px"></div>\n</section>\n'''
assert anchor in s
page = '''\n<!-- ══════════ SMART Recovery · Change Plan V8.2.7 ══════════ -->\n<section class="pg" id="p-smart-change-plan">\n  <div class="sp" style="margin-bottom:11px">\n    <h1 style="margin:0">변화 계획 워크시트</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="go('learn-topic')">← SMART Recovery</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    원하는 변화를 분명히 하고, 이유·단계·도움·진전의 신호·방해요인을 한 장의 계획으로 정리합니다. SMART Recovery의 <b>Change Plan Worksheet</b>를 앱에 맞게 재구성했으며, <b>내용은 이 기기에만 저장</b>됩니다.\n  </div>\n  <div id="smart-change-plan-role-note"></div>\n  <button class="btn sec" id="smart-change-plan-new">+ 변화 계획 새로 작성하기</button>\n  <div id="smart-change-plan-list" style="margin-top:12px"></div>\n</section>\n'''
s = s.replace(anchor, anchor + page, 1)

# Route and action handler.
route = "  if(p === 'smart-cba') drawSmartCba();\n"
assert route in s
s = s.replace(route, route + "  if(p === 'smart-change-plan') drawSmartChangePlan();\n", 1)

action = "  if(type === 'smart-cba'){ go('smart-cba'); return; }\n"
assert action in s
s = s.replace(action, action + "  if(type === 'smart-change-plan'){ go('smart-change-plan'); return; }\n", 1)

# Change Plan functions. Use the existing shared smartWorks array and role separation.
fn_anchor = "function learningAction(type){\n"
assert fn_anchor in s
block = r'''/* ── SMART Recovery · Change Plan V8.2.7 ── */
function smartChangePlanRecords(){
  return (Array.isArray(S.smartWorks)?S.smartWorks:[])
    .filter(r=>r && r.kind==='change-plan' && (r.role||'self')===(famMode()?'family':'self'))
    .sort((a,b)=>(b.updatedAt||b.ts||0)-(a.updatedAt||a.ts||0));
}
function smartChangePlanText(v){ return String(v||'').trim(); }
function smartChangePlanLines(v){
  return smartChangePlanText(v).split(/\n+/).map(x=>x.trim()).filter(Boolean);
}
function smartChangePlanDate(ts){
  if(!ts) return '';
  const d=new Date(ts); return d.getFullYear()+'. '+(d.getMonth()+1)+'. '+d.getDate()+'.';
}
function drawSmartChangePlan(){
  const list=$('#smart-change-plan-list'), rn=$('#smart-change-plan-role-note'), add=$('#smart-change-plan-new');
  if(!list||!add) return;
  if(rn){
    rn.innerHTML=famMode()
      ? '<div class="note" style="margin-bottom:12px"><b>가족의 변화 계획은 상대를 바꾸는 계획이 아닙니다.</b><br>내가 줄이거나 시작하고 싶은 행동, 나의 경계·자기돌봄·생활 변화처럼 내가 직접 할 수 있는 목표를 적습니다.</div>'
      : '';
  }
  add.onclick=()=>openSmartChangePlanEditor(null);
  const rows=smartChangePlanRecords();
  if(!rows.length){
    list.innerHTML='<div class="card"><b>아직 저장한 변화 계획이 없습니다.</b><p class="muted" style="margin:5px 0 0">큰 변화를 한 번에 해결하기보다, 지금 만들고 싶은 변화 하나부터 계획해보세요.</p></div>';
    return;
  }
  list.innerHTML='<div class="card"><h3>저장한 변화 계획 '+rows.length+'건</h3>'
    +rows.map(r=>'<div class="sp" style="gap:10px;padding:11px 0;border-top:1px solid var(--line)"><div style="min-width:0;flex:1"><div class="tiny">'+esc(smartChangePlanDate(r.updatedAt||r.ts))+'</div><b style="display:block;margin-top:2px">'+esc(r.change||'변화 계획')+'</b><div class="muted" style="margin-top:3px">중요도 '+esc(r.importance||'-')+'/10 · 자신감 '+esc(r.confidence||'-')+'/10</div></div><button class="tiny" style="color:var(--acc);font-weight:600" onclick="openSmartChangePlanView(\''+esc(r.id)+'\')">보기</button></div>').join('')
    +'</div>';
}
function smartChangePlanRating(label,id,value,help){
  const n=Math.max(1,Math.min(10,Number(value)||5));
  let opts=''; for(let i=1;i<=10;i++) opts+='<option value="'+i+'"'+(i===n?' selected':'')+'>'+i+'</option>';
  return '<div><label>'+esc(label)+'</label><select id="'+id+'">'+opts+'</select><div class="tiny" style="margin-top:4px">'+esc(help)+'</div></div>';
}
function openSmartChangePlanEditor(record){
  const edit=!!record;
  modal('<h2>'+(edit?'변화 계획 수정':'변화 계획 작성')+'</h2>'
    +'<p class="muted" style="margin:5px 0 14px">목표를 작은 단계로 나누고, 도움과 방해요인까지 미리 적어두면 계획을 실행하기 쉬워집니다.</p>'
    +'<div class="card"><label>내가 만들고 싶은 변화</label><input id="cp-change" maxlength="120" value="'+esc(edit?(record.change||''):'')+'" placeholder="예: 술을 마시지 않는 생활을 시작하기"></div>'
    +'<div class="card"><div class="grid2">'
      +smartChangePlanRating('이 변화는 얼마나 중요한가요?','cp-importance',edit?record.importance:8,'1 = 중요하지 않음 · 10 = 매우 중요함')
      +smartChangePlanRating('이 변화를 할 수 있다고 얼마나 자신하나요?','cp-confidence',edit?record.confidence:5,'1 = 전혀 자신 없음 · 10 = 매우 자신 있음')
    +'</div></div>'
    +'<div class="card"><label>이 변화를 만들고 싶은 가장 중요한 이유</label><textarea id="cp-reasons" maxlength="800" placeholder="이유를 한 줄에 하나씩 적어도 좋습니다.">'+esc(edit?(record.reasons||''):'')+'</textarea></div>'
    +'<div class="card"><label>변화를 위해 내가 계획하는 단계</label><textarea id="cp-steps" maxlength="1200" placeholder="예:\n1. 오늘 집에 있는 술을 치운다.\n2. 이번 주 모임에 한 번 참여한다.\n3. 외래 예약을 지킨다.">'+esc(edit?(record.steps||''):'')+'</textarea></div>'
    +'<div class="card"><label>다른 사람들이 나를 도울 수 있는 방법</label><textarea id="cp-help" maxlength="800" placeholder="누가, 어떤 방식으로 도와줄 수 있는지 적어보세요.">'+esc(edit?(record.help||''):'')+'</textarea></div>'
    +'<div class="card"><label>내 계획이 작동하고 있음을 알 수 있는 신호</label><textarea id="cp-signs" maxlength="800" placeholder="예: 술집을 피하고 있다, 수면이 규칙적이다, 약속을 지키고 있다">'+esc(edit?(record.signs||''):'')+'</textarea></div>'
    +'<div class="card"><label>내 계획을 방해할 수 있는 것</label><textarea id="cp-obstacles" maxlength="800" placeholder="예: 회식, 외로움, 돈 문제, 갈등, 피로">'+esc(edit?(record.obstacles||''):'')+'</textarea></div>'
    +'<button class="btn" id="cp-save">'+(edit?'수정 저장':'변화 계획 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
  $('#cp-save').onclick=()=>{
    const change=$('#cp-change').value.trim();
    if(!change){ toast('만들고 싶은 변화를 적어주세요.'); return; }
    const steps=$('#cp-steps').value.trim();
    if(!steps){ toast('변화를 위한 계획 단계를 한 가지 이상 적어주세요.'); return; }
    const now=Date.now();
    const rec={
      id:edit?record.id:('cp-'+now+'-'+Math.random().toString(36).slice(2,7)),
      kind:'change-plan', role:famMode()?'family':'self',
      ts:edit?(record.ts||now):now, updatedAt:now,
      change, importance:Number($('#cp-importance').value)||1, confidence:Number($('#cp-confidence').value)||1,
      reasons:$('#cp-reasons').value.trim(), steps,
      help:$('#cp-help').value.trim(), signs:$('#cp-signs').value.trim(), obstacles:$('#cp-obstacles').value.trim()
    };
    if(!Array.isArray(S.smartWorks)) S.smartWorks=[];
    if(edit){ const i=S.smartWorks.findIndex(x=>x&&x.id===record.id); if(i>=0) S.smartWorks[i]=rec; else S.smartWorks.push(rec); }
    else S.smartWorks.push(rec);
    save(); closeModal(); drawSmartChangePlan(); toast(edit?'변화 계획을 수정했습니다.':'변화 계획을 저장했습니다.');
  };
}
function openSmartChangePlanView(id){
  const r=(Array.isArray(S.smartWorks)?S.smartWorks:[]).find(x=>x&&x.id===id&&x.kind==='change-plan');
  if(!r) return;
  const section=(title,text)=>'<div class="card"><h3>'+esc(title)+'</h3><div style="white-space:pre-wrap">'+(smartChangePlanText(text)?esc(text):'<span class="muted">작성하지 않음</span>')+'</div></div>';
  modal('<h2>'+esc(r.change||'변화 계획')+'</h2><div class="muted" style="margin:-4px 0 12px">'+esc(smartChangePlanDate(r.updatedAt||r.ts))+' · 중요도 '+esc(r.importance||'-')+'/10 · 자신감 '+esc(r.confidence||'-')+'/10</div>'
    +section('변화를 원하는 이유',r.reasons)
    +section('계획하는 단계',r.steps)
    +section('도움을 받을 사람과 방법',r.help)
    +section('계획이 작동하는 신호',r.signs)
    +section('계획을 방해할 수 있는 것',r.obstacles)
    +'<button class="btn sec" id="cp-edit">수정</button><div style="height:8px"></div><button class="btn bad" id="cp-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
  $('#cp-edit').onclick=()=>openSmartChangePlanEditor(r);
  $('#cp-delete').onclick=()=>{
    if(!confirm('이 변화 계획 기록을 삭제할까요?')) return;
    S.smartWorks=(Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>!(x&&x.id===r.id));
    save(); closeModal(); drawSmartChangePlan(); toast('기록을 삭제했습니다.');
  };
}

'''
s = s.replace(fn_anchor, block + fn_anchor, 1)

# Learning topic action: preserve the handbook order HOV -> Change Plan -> CBA.
old = '''          {\n            "type": "smart-hov",\n            "label": "HOV 가치의 계층 작성하기"\n          },\n          {\n            "type": "smart-cba",\n            "label": "CBA 비용-편익 분석 작성하기"\n          }'''
new = '''          {\n            "type": "smart-hov",\n            "label": "HOV 가치의 계층 작성하기"\n          },\n          {\n            "type": "smart-change-plan",\n            "label": "변화 계획 워크시트 작성하기"\n          },\n          {\n            "type": "smart-cba",\n            "label": "CBA 비용-편익 분석 작성하기"\n          }'''
assert old in ld
ld = ld.replace(old,new,1)
ld = ld.replace('회복학습 데이터 V8.2.6','회복학습 데이터 V8.2.7',1)

assert "const APP_VERSION = 'V8.2.6';" in swtxt
assert "const V = 'ohg-v826-smart-cba';" in swtxt
swtxt = swtxt.replace("const APP_VERSION = 'V8.2.6';", "const APP_VERSION = 'V8.2.7';",1)
swtxt = swtxt.replace("const V = 'ohg-v826-smart-cba';", "const V = 'ohg-v827-smart-change-plan';",1)

idx.write_text(s,encoding='utf-8')
learn.write_text(ld,encoding='utf-8')
sw.write_text(swtxt,encoding='utf-8')
print('V8.2.7 Change Plan patch applied')
