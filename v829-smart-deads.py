from pathlib import Path

idx=Path('index.html'); learn=Path('learning-data.js'); sw=Path('sw.js')
s=idx.read_text(encoding='utf-8'); ld=learn.read_text(encoding='utf-8'); st=sw.read_text(encoding='utf-8')

assert "const BUILD = 'V8.2.8';" in s
s=s.replace("const BUILD = 'V8.2.8';","const BUILD = 'V8.2.9';",1)
assert "const DATA_SCHEMA = 6;" in s

# Keep recovery-tools nav highlighting for the DEADS subpage.
nav="p === 'smart-hov' || p === 'smart-cba' || p === 'smart-change-plan' || p === 'smart-three-questions'"
assert nav in s
s=s.replace(nav, nav+" || p === 'smart-deads'",1)

# Page
marker='<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->'
assert marker in s
page=r'''<!-- ══════════ SMART Recovery · DEADS V8.2.9 ══════════ -->
<section class="pg" id="p-smart-deads">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">DEADS · 충동 대처</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="go('learn-topic')">← SMART Recovery</button>
  </div>
  <div class="note" style="margin-bottom:12px">
    충동이 올라왔을 때 <b>거부·지연 → 벗어나기 → 회피·수용·반박 → 주의 돌리기 → 대체하기</b> 중 지금 맞는 전략을 골라 실행합니다. SMART Recovery의 DEADS를 앱에 맞게 재구성했으며, 내 계획은 <b>이 기기에만 저장</b>됩니다.
  </div>
  <div id="smart-deads-family-note"></div>
  <div id="smart-deads-self-tools">
    <button class="btn" id="smart-deads-now">지금 DEADS 사용하기</button>
    <div style="height:8px"></div>
    <button class="btn sec" id="smart-deads-new">+ 내 DEADS 계획 작성하기</button>
    <div style="height:8px"></div>
    <button class="btn ghost" onclick="go('urge-diary')">내 충동일기 열기</button>
    <div id="smart-deads-list" style="margin-top:12px"></div>
  </div>
</section>

'''
s=s.replace(marker,page+marker,1)

# Draw route
route="  if(p === 'smart-three-questions') drawSmartThreeQuestions();\n"
assert route in s
s=s.replace(route,route+"  if(p === 'smart-deads') drawSmartDeads();\n",1)

# Learning action handler
action="  if(type === 'smart-three-questions'){ go('smart-three-questions'); return; }\n"
assert action in s
s=s.replace(action,action+"  if(type === 'smart-deads'){ go('smart-deads'); return; }\n",1)

# Functions before generic learning action.
fn_anchor='function learningAction(type){\n'
assert fn_anchor in s
block=r'''/* ── SMART Recovery · DEADS V8.2.9 ── */
function smartDeadsRecords(){
  return (Array.isArray(S.smartWorks)?S.smartWorks:[])
    .filter(r=>r && r.kind==='deads' && (r.role||'self')==='self')
    .sort((a,b)=>(b.updatedAt||b.ts||0)-(a.updatedAt||a.ts||0));
}
function smartDeadsDate(ts){
  if(!ts) return '';
  const d=new Date(ts); return d.getFullYear()+'. '+(d.getMonth()+1)+'. '+d.getDate()+'.';
}
function smartDeadsFilled(r){
  if(!r) return 0;
  return ['denyDelay','escape','avoid','accept','attack','distract','substitute'].filter(k=>String(r[k]||'').trim()).length;
}
function drawSmartDeads(){
  const fam=$('#smart-deads-family-note'), tools=$('#smart-deads-self-tools');
  if(!fam||!tools) return;
  if(famMode()){
    fam.innerHTML='<div class="note"><b>가족을 위한 안내</b><br>DEADS는 충동을 직접 경험하는 사람이 자신의 충동에 대처하기 위한 도구입니다. 가족이 상대의 충동을 감시하거나 통제하는 용도로 사용하지 않습니다.<div style="height:10px"></div><button class="btn ghost" onclick="go(\'learn-topic\')">SMART Recovery로 돌아가기</button></div>';
    tools.style.display='none'; return;
  }
  fam.innerHTML=''; tools.style.display='block';
  const now=$('#smart-deads-now'), add=$('#smart-deads-new'), list=$('#smart-deads-list');
  if(now) now.onclick=()=>openSmartDeadsNow();
  if(add) add.onclick=()=>openSmartDeadsEditor(null);
  if(!list) return;
  const rows=smartDeadsRecords();
  if(!rows.length){
    list.innerHTML='<div class="card"><b>아직 저장한 DEADS 계획이 없습니다.</b><p class="muted" style="margin:5px 0 0">평소에 나에게 맞는 대응을 적어두면 충동이 왔을 때 바로 꺼내 쓸 수 있습니다.</p></div>';
    return;
  }
  list.innerHTML='<div class="card"><h3>저장한 DEADS 계획 '+rows.length+'건</h3>'+
    rows.map(r=>'<div class="sp" style="gap:10px;padding:11px 0;border-top:1px solid var(--line)"><div style="min-width:0;flex:1"><div class="tiny">'+esc(smartDeadsDate(r.updatedAt||r.ts))+'</div><b style="display:block;margin-top:2px">내 DEADS 계획</b><div class="muted" style="margin-top:3px">준비한 전략 '+smartDeadsFilled(r)+'개</div></div><button class="tiny" style="color:var(--acc);font-weight:600" onclick="openSmartDeadsView(\''+esc(r.id)+'\')">보기</button></div>').join('')+'</div>';
}
function smartDeadsField(title,id,value,placeholder,help){
  return '<div class="card"><label>'+esc(title)+'</label>'+(help?'<div class="tiny" style="margin:4px 0 7px">'+esc(help)+'</div>':'')+'<textarea id="'+id+'" maxlength="600" placeholder="'+esc(placeholder)+'">'+esc(value||'')+'</textarea></div>';
}
function openSmartDeadsEditor(record){
  if(famMode()) return;
  const r=record||{};
  modal('<h2>'+(record?'DEADS 계획 수정':'내 DEADS 계획 작성')+'</h2>'
    +'<p class="muted" style="margin:5px 0 14px">모든 칸을 채울 필요는 없습니다. 실제 충동이 왔을 때 내가 사용할 수 있는 방법부터 적어두세요.</p>'
    +smartDeadsField('D · 거부·지연하기','deads-delay',r.denyDelay,'예: 바로 결정하지 않고 10분 기다리기','충동이 얼마나 올라왔다 내려가는지 관찰하고, 행동을 미룰 방법을 정합니다.')
    +smartDeadsField('E · 벗어나기','deads-escape',r.escape,'예: 술자리를 나와 편의점이 없는 길로 걷기','가능한 촉발 상황·장소·사람의 영향권에서 벗어날 방법을 정합니다.')
    +smartDeadsField('A · 미리 회피하기','deads-avoid',r.avoid,'예: 급여일에는 혼자 번화가에 가지 않기','예측 가능한 촉발 상황을 미리 피하는 방법을 적습니다.')
    +smartDeadsField('A · 충동이 지나가도록 수용하기','deads-accept',r.accept,'예: 올라오는 감각을 판단하지 않고 호흡하며 지나가게 두기','굴복하지 않은 채 충동의 상승과 하강을 견디는 방법을 적습니다.')
    +smartDeadsField('A · 충동/생각에 반박하기','deads-attack',r.attack,'예: “지금 꼭 해야 해” → “충동은 명령이 아니고 지나간다”','원자료의 Attack은 사람을 공격한다는 뜻이 아니라 충동을 부추기는 생각을 정면으로 다루고 반박하는 의미입니다.')
    +smartDeadsField('D · 활동으로 주의 돌리기','deads-distract',r.distract,'예: 10분 산책, 샤워, 청소, 회복동료에게 전화','주의를 다른 안전한 활동으로 옮길 목록을 적습니다.')
    +smartDeadsField('S · 대체하기','deads-substitute',r.substitute,'예: 술 대신 탄산수, 사용 생각 대신 현실적인 대처 문장','중독행동이나 중독적 사고를 더 건강한 행동·생각으로 대체합니다.')
    +'<button class="btn" id="deads-save">'+(record?'수정 저장':'DEADS 계획 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
  $('#deads-save').onclick=()=>{
    const rec={
      id:record?record.id:('deads-'+Date.now()+'-'+Math.random().toString(36).slice(2,7)), kind:'deads', role:'self',
      ts:record?(record.ts||Date.now()):Date.now(), updatedAt:Date.now(),
      denyDelay:$('#deads-delay').value.trim(), escape:$('#deads-escape').value.trim(), avoid:$('#deads-avoid').value.trim(),
      accept:$('#deads-accept').value.trim(), attack:$('#deads-attack').value.trim(), distract:$('#deads-distract').value.trim(), substitute:$('#deads-substitute').value.trim()
    };
    if(!smartDeadsFilled(rec)){ toast('내가 사용할 수 있는 전략을 한 가지 이상 적어주세요.'); return; }
    if(!Array.isArray(S.smartWorks)) S.smartWorks=[];
    if(record){ const i=S.smartWorks.findIndex(x=>x&&x.id===record.id); if(i>=0) S.smartWorks[i]=rec; else S.smartWorks.push(rec); }
    else S.smartWorks.push(rec);
    save(); closeModal(); drawSmartDeads(); toast(record?'DEADS 계획을 수정했습니다.':'DEADS 계획을 저장했습니다.');
  };
}
function smartDeadsSection(title,text){
  return '<div class="card"><h3>'+esc(title)+'</h3><div style="white-space:pre-wrap">'+(String(text||'').trim()?esc(text):'<span class="muted">작성하지 않음</span>')+'</div></div>';
}
function openSmartDeadsView(id){
  const r=smartDeadsRecords().find(x=>x.id===id); if(!r) return;
  modal('<h2>내 DEADS 계획</h2><div class="muted" style="margin:-4px 0 12px">'+esc(smartDeadsDate(r.updatedAt||r.ts))+'</div>'
    +smartDeadsSection('D · 거부·지연하기',r.denyDelay)+smartDeadsSection('E · 벗어나기',r.escape)
    +smartDeadsSection('A · 미리 회피하기',r.avoid)+smartDeadsSection('A · 충동이 지나가도록 수용하기',r.accept)+smartDeadsSection('A · 충동/생각에 반박하기',r.attack)
    +smartDeadsSection('D · 활동으로 주의 돌리기',r.distract)+smartDeadsSection('S · 대체하기',r.substitute)
    +'<button class="btn" id="deads-use">지금 이 계획 사용하기</button><div style="height:8px"></div><button class="btn sec" id="deads-edit">수정</button><div style="height:8px"></div><button class="btn bad" id="deads-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
  $('#deads-use').onclick=()=>openSmartDeadsNow(r);
  $('#deads-edit').onclick=()=>openSmartDeadsEditor(r);
  $('#deads-delete').onclick=()=>{
    if(!confirm('이 DEADS 계획을 삭제할까요?')) return;
    S.smartWorks=(Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>!(x&&x.id===r.id)); save(); closeModal(); drawSmartDeads(); toast('기록을 삭제했습니다.');
  };
}
const SMART_DEADS_META={
  delay:{title:'D · 거부·지연하기',short:'거부·지연',guide:'지금 결정을 미루고 충동이 약해질 시간을 만듭니다. SMART 자료는 10~20분 정도의 지연을 활용하도록 설명합니다. 앱에서는 먼저 5분으로 시작하고 필요하면 15분·30분으로 연장할 수 있습니다.'},
  escape:{title:'E · 벗어나기',short:'벗어나기',guide:'가능하면 촉발 자극과 거리를 둡니다. 장소·사람·상황을 바꾸는 것도 충동에 대한 적극적인 대처입니다.'},
  accept:{title:'A · 회피·수용·반박하기',short:'회피·수용·반박',guide:'피할 수 있으면 미리 피하고, 피할 수 없다면 충동이 올라왔다 내려가는 경험을 판단하지 않고 지켜보거나 충동을 부추기는 생각에 반박합니다.'},
  distract:{title:'D · 활동으로 주의 돌리기',short:'주의 돌리기',guide:'주의를 안전한 다른 활동으로 옮깁니다. 산책·명상·읽기·청소처럼 행동을 먼저 시작하면 동기가 뒤따를 수도 있습니다.'},
  substitute:{title:'S · 대체하기',short:'대체하기',guide:'중독행동이나 중독적 사고를 더 건강한 행동과 현실적인 생각으로 바꿉니다.'}
};
function smartDeadsPersonal(r,key){
  if(!r) return '';
  if(key==='delay') return r.denyDelay||'';
  if(key==='escape') return r.escape||'';
  if(key==='accept') return [r.avoid,r.accept,r.attack].filter(Boolean).join('\n\n');
  if(key==='distract') return r.distract||'';
  if(key==='substitute') return r.substitute||'';
  return '';
}
function openSmartDeadsNow(plan){
  if(famMode()) return;
  const r=plan||smartDeadsRecords()[0]||null;
  modal('<h2>지금 DEADS 사용하기</h2><p class="muted" style="margin:5px 0 12px">다섯 전략을 모두 할 필요는 없습니다. 지금 가장 실행하기 쉬운 하나를 고르세요.</p>'
    +Object.keys(SMART_DEADS_META).map(k=>'<button class="btn sec" style="margin-bottom:8px" data-deads-key="'+k+'">'+esc(SMART_DEADS_META[k].title)+'</button>').join('')
    +'<button class="btn ghost" id="deads-now-diary">내 충동일기 열기</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
  document.querySelectorAll('[data-deads-key]').forEach(b=>b.onclick=()=>openSmartDeadsStrategy(b.dataset.deadsKey,r));
  $('#deads-now-diary').onclick=()=>{ closeModal(); go('urge-diary'); };
}
function openSmartDeadsStrategy(key,plan){
  const m=SMART_DEADS_META[key]; if(!m) return;
  const personal=smartDeadsPersonal(plan,key);
  modal('<h2>'+esc(m.title)+'</h2><div class="card"><b>지금 이렇게 해보세요</b><p style="margin:7px 0 0">'+esc(m.guide)+'</p></div>'
    +(personal?'<div class="card"><h3>내가 미리 정해둔 방법</h3><div style="white-space:pre-wrap">'+esc(personal)+'</div></div>':'<div class="note">저장한 개인 계획이 없어도 바로 사용할 수 있습니다. 나중에 내 DEADS 계획에 효과가 있었던 방법을 적어두세요.</div>')
    +'<button class="btn" id="deads-start-urge">이 전략으로 5분 버티기</button><div style="height:8px"></div><button class="btn sec" id="deads-strategy-back">다른 DEADS 전략 고르기</button><div style="height:8px"></div><button class="btn ghost" id="deads-strategy-diary">충동일기 열기</button>');
  $('#deads-start-urge').onclick=()=>startSmartDeadsUrge(key);
  $('#deads-strategy-back').onclick=()=>openSmartDeadsNow(plan);
  $('#deads-strategy-diary').onclick=()=>{ closeModal(); go('urge-diary'); };
}
function startSmartDeadsUrge(key){
  const m=SMART_DEADS_META[key]; if(!m) return;
  closeModal(); go('urge'); setTimeout(()=>urgeUseCope('DEADS · '+m.short),80);
}

'''
s=s.replace(fn_anchor,block+fn_anchor,1)

# Add DEADS before the existing urge diary action in Point 2.
old='''        "actions": [\n          {\n            "type": "urge-diary",\n            "label": "내 충동일기 열기"\n          }\n        ]'''
new='''        "actions": [\n          {\n            "type": "smart-deads",\n            "label": "DEADS 대처계획·실행하기"\n          },\n          {\n            "type": "urge-diary",\n            "label": "내 충동일기 열기"\n          }\n        ]'''
assert old in ld
ld=ld.replace(old,new,1)
ld=ld.replace('회복학습 데이터 V8.2.8','회복학습 데이터 V8.2.9',1)

assert "const APP_VERSION = 'V8.2.8';" in st
assert "const V = 'ohg-v828-smart-three-questions';" in st
st=st.replace("const APP_VERSION = 'V8.2.8';","const APP_VERSION = 'V8.2.9';",1)
st=st.replace("const V = 'ohg-v828-smart-three-questions';","const V = 'ohg-v829-smart-deads';",1)

idx.write_text(s,encoding='utf-8'); learn.write_text(ld,encoding='utf-8'); sw.write_text(st,encoding='utf-8')
print('V8.2.9 SMART DEADS patch applied')
