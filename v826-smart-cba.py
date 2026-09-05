from pathlib import Path

idx = Path('index.html')
learn = Path('learning-data.js')
sw = Path('sw.js')

index = idx.read_text(encoding='utf-8')
learning = learn.read_text(encoding='utf-8')
swt = sw.read_text(encoding='utf-8')

# versions: CBA reuses smartWorks schema introduced in V8.2.5, so DATA_SCHEMA stays 6.
index = index.replace("const BUILD = 'V8.2.5';", "const BUILD = 'V8.2.6';", 1)
swt = swt.replace("const APP_VERSION = 'V8.2.5';", "const APP_VERSION = 'V8.2.6';", 1)
swt = swt.replace("const V = 'ohg-v825-smart-hov';", "const V = 'ohg-v826-smart-cba';", 1)
learning = learning.replace('/* 오늘 한 걸음 — 회복학습 데이터 V8.2.5', '/* 오늘 한 걸음 — 회복학습 데이터 V8.2.6', 1)

# CBA page
page_anchor = '<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->'
page = '''<!-- ══════════ SMART Recovery · CBA V8.2.6 ══════════ -->
<section class="pg" id="p-smart-cba">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">비용-편익 분석 CBA</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="go('learn-topic')">← SMART Recovery</button>
  </div>
  <div class="note" style="margin-bottom:12px">
    지금 행동의 이득과 대가, 중단했을 때의 이득과 어려움을 한곳에서 비교합니다. 각 항목은 <b>단기·장기</b>로 구분합니다. SMART Recovery의 <b>Cost-Benefit Analysis(CBA)</b>를 앱에 맞게 재구성했으며, <b>내용은 이 기기에만 저장</b>됩니다.
  </div>
  <div id="smart-cba-role-note"></div>
  <button class="btn sec" id="smart-cba-new">+ CBA 새로 작성하기</button>
  <div id="smart-cba-list" style="margin-top:12px"></div>
</section>

'''
if page_anchor not in index:
    raise SystemExit('CBA page anchor not found')
index = index.replace(page_anchor, page + page_anchor, 1)

# route and draw
old = "|| p === 'urge-diary' || p === 'smart-hov') ? 'tools' : p;"
new = "|| p === 'urge-diary' || p === 'smart-hov' || p === 'smart-cba') ? 'tools' : p;"
if old not in index:
    raise SystemExit('CBA tools route anchor not found')
index = index.replace(old, new, 1)

anchor = "  if(p === 'smart-hov') drawSmartHov();\n"
if anchor not in index:
    raise SystemExit('CBA draw route anchor not found')
index = index.replace(anchor, anchor + "  if(p === 'smart-cba') drawSmartCba();\n", 1)

anchor = "  if(type === 'smart-hov'){ go('smart-hov'); return; }\n"
if anchor not in index:
    raise SystemExit('CBA learningAction anchor not found')
index = index.replace(anchor, anchor + "  if(type === 'smart-cba'){ go('smart-cba'); return; }\n", 1)

# CBA functions. smartWorkId/smartRole/smartHovDate are shared from V8.2.5.
fn_anchor = "function drawScheduleHub(){"
functions = r'''/* ══════════ SMART Recovery · 비용-편익 분석(CBA) V8.2.6 ══════════
   사용자 번역 SMART Recovery 핸드북의 CBA 4사분면과 단기/장기 구분을 앱용으로 재구성했습니다.
   네 사분면을 모두 보게 하여 '중단의 어려움'도 회피하지 않고 다음 대처계획으로 연결합니다. */
const SMART_CBA_GROUPS = [
  {key:'useBenefits', title:'사용·실행할 때 좋은 점', sub:'혜택 · 보상 및 이익', tone:'acc'},
  {key:'useCosts', title:'사용·실행할 때 치르는 대가', sub:'비용 · 위험 및 단점', tone:'bad'},
  {key:'stopBenefits', title:'사용하지 않거나 중단할 때 좋은 점', sub:'혜택 · 보상 및 이익', tone:'acc'},
  {key:'stopCosts', title:'사용하지 않거나 중단할 때 어려운 점', sub:'비용 · 위험 및 단점', tone:'warn'}
];
function smartCbaRows(){
  return (S.smartWorks||[]).filter(r=>r && r.tool==='cba' && (r.role||'self')===smartRole())
    .slice().sort((a,b)=>Number(b.t||0)-Number(a.t||0));
}
function smartCbaItems(r,key){
  return (r&&Array.isArray(r[key])?r[key]:[]).map(x=>({text:String((x&&x.text)||'').trim(),term:String((x&&x.term)||'').trim()})).filter(x=>x.text);
}
function smartCbaTermLabel(term){ return term==='short'?'단기':term==='long'?'장기':term==='both'?'단기·장기':''; }
function smartCbaBadge(term){ const t=smartCbaTermLabel(term); return t?'<span class="pill" style="margin-left:6px">'+esc(t)+'</span>':''; }
function drawSmartCba(){
  const list=$('#smart-cba-list'), rn=$('#smart-cba-role-note'), add=$('#smart-cba-new');
  if(!list||!add) return;
  if(rn){
    rn.innerHTML=famMode()
      ? '<div class="note" style="margin-bottom:12px"><b>가족은 상대의 중독행동이 아니라 내 행동을 봅니다.</b><br>예: 확인하기, 대신 수습하기, 반복해서 설득하기처럼 내가 줄이거나 바꾸고 싶은 행동을 하나 정해 네 면을 살펴봅니다.</div>'
      : '';
  }
  const rows=smartCbaRows();
  if(!rows.length){
    list.innerHTML='<div class="empty">아직 작성한 CBA가 없습니다.<br>바꾸고 싶은 물질·행동의 네 가지 면을 함께 살펴보세요.</div>';
  }else{
    let h='<div class="card"><h3>저장한 CBA '+rows.length+'건</h3>';
    rows.forEach(r=>{
      const pos=smartCbaItems(r,'stopBenefits')[0]||smartCbaItems(r,'useCosts')[0];
      h+='<button class="ws-saved" style="width:100%;text-align:left" data-cba-rid="'+esc(r.rid||String(r.t))+'">'
        +'<span class="date">'+esc(smartHovDate(r.t))+'</span>'
        +'<span class="body"><b>'+esc(r.subject||'비용-편익 분석')+'</b><span>'+esc(pos?pos.text:'네 가지 면을 비교한 기록')+'</span></span>'
        +'<span class="go">보기</span></button>';
    });
    h+='</div>'; list.innerHTML=h;
    list.querySelectorAll('[data-cba-rid]').forEach(b=>b.onclick=()=>{
      const r=rows.find(x=>(x.rid||String(x.t))===b.dataset.cbaRid); if(r) openSmartCbaRecord(r);
    });
  }
  add.onclick=()=>openSmartCbaEditor();
}
function smartCbaGroupView(r,g){
  const items=smartCbaItems(r,g.key);
  return '<div class="card"><h3>'+esc(g.title)+'</h3><p class="tiny" style="margin:-6px 0 9px">'+esc(g.sub)+'</p>'
    +(items.length?'<ul style="margin:0;padding-left:20px">'+items.map(x=>'<li style="padding:4px 0">'+esc(x.text)+smartCbaBadge(x.term)+'</li>').join('')+'</ul>':'<p class="muted">기록 없음</p>')+'</div>';
}
function openSmartCbaRecord(r){
  let body='<h2>나의 비용-편익 분석</h2><p class="tiny" style="margin:4px 0 12px">'+esc(smartHovDate(r.t))+' 작성</p>'
    +'<div class="note" style="margin-bottom:12px"><b>고려한 물질 또는 행동</b><br>'+esc(r.subject||'')+'</div>';
  SMART_CBA_GROUPS.forEach(g=>body+=smartCbaGroupView(r,g));
  if(r.nextStep) body+='<div class="card"><h3>다음 대처 계획</h3><p style="white-space:pre-wrap">'+esc(r.nextStep)+'</p></div>';
  body+='<button class="btn sec" id="smart-cba-edit">수정</button><div style="height:8px"></div><button class="btn danger" id="smart-cba-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>';
  modal(body);
  $('#smart-cba-edit').onclick=()=>openSmartCbaEditor(r);
  $('#smart-cba-delete').onclick=()=>{
    const key=r.rid||String(r.t);
    modal('<h2>이 CBA 기록을 삭제할까요?</h2><p class="muted" style="margin:6px 0 14px">이 기록 한 건만 기기에서 삭제하며 되돌릴 수 없습니다.</p><button class="btn danger" id="smart-cba-delete-ok">삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
    $('#smart-cba-delete-ok').onclick=()=>{ S.smartWorks=(S.smartWorks||[]).filter(x=>(x.rid||String(x.t))!==key); save(); closeModal(); drawSmartCba(); toast('삭제했습니다.'); };
  };
}
function smartCbaRowHtml(key,item){
  const text=(item&&item.text)||'', term=(item&&item.term)||'';
  return '<div class="cba-row" data-cba-group="'+esc(key)+'" style="display:grid;grid-template-columns:minmax(0,1fr) 104px 34px;gap:6px;margin:7px 0">'
    +'<input class="cba-text" maxlength="120" value="'+esc(text)+'" placeholder="한 가지씩 적어보세요">'
    +'<select class="cba-term"><option value="">기간</option><option value="short"'+(term==='short'?' selected':'')+'>단기</option><option value="long"'+(term==='long'?' selected':'')+'>장기</option><option value="both"'+(term==='both'?' selected':'')+'>둘 다</option></select>'
    +'<button class="tiny cba-remove" type="button" aria-label="항목 삭제" style="font-size:20px;color:var(--faint)">×</button></div>';
}
function bindSmartCbaRows(root){
  root.querySelectorAll('.cba-remove').forEach(b=>b.onclick=()=>{
    const row=b.closest('.cba-row'), box=row&&row.parentElement;
    if(row) row.remove();
    if(box && !box.querySelector('.cba-row')) box.insertAdjacentHTML('beforeend',smartCbaRowHtml(box.dataset.cbaBox,{}));
    bindSmartCbaRows(root);
  });
  root.querySelectorAll('[data-cba-add]').forEach(b=>{
    b.onclick=()=>{
      const box=root.querySelector('[data-cba-box="'+b.dataset.cbaAdd+'"]'); if(!box) return;
      box.insertAdjacentHTML('beforeend',smartCbaRowHtml(b.dataset.cbaAdd,{})); bindSmartCbaRows(root);
    };
  });
}
function smartCbaCollect(root,key){
  return Array.from(root.querySelectorAll('.cba-row[data-cba-group="'+key+'"]')).map(row=>({text:(row.querySelector('.cba-text').value||'').trim(),term:row.querySelector('.cba-term').value||''})).filter(x=>x.text);
}
function openSmartCbaEditor(record){
  const edit=!!record;
  const subjectLabel=famMode()?'내가 줄이거나 바꾸고 싶은 행동':'고려할 물질 또는 행위';
  let groups='';
  SMART_CBA_GROUPS.forEach((g,i)=>{
    let items=smartCbaItems(record,g.key); if(!items.length) items=[{},{}];
    groups+='<div class="card"><h3>'+(i+1)+'. '+esc(g.title)+'</h3><p class="tiny" style="margin:-6px 0 7px">'+esc(g.sub)+' · 각 항목에 단기/장기를 표시하세요.</p><div data-cba-box="'+g.key+'">'+items.map(x=>smartCbaRowHtml(g.key,x)).join('')+'</div><button class="tiny" type="button" data-cba-add="'+g.key+'" style="color:var(--acc);font-weight:600;margin-top:5px">+ 항목 추가</button></div>';
  });
  modal('<h2>'+(edit?'CBA 수정':'비용-편익 분석 CBA 작성')+'</h2>'
    +'<p class="muted" style="margin:5px 0 14px">단기적으로 좋아 보이는 점과 장기적인 영향을 한 화면에서 비교합니다. <b>네 영역을 모두</b> 적는 것이 중요합니다.</p>'
    +'<div class="card"><label>'+esc(subjectLabel)+'</label><input id="cba-subject" maxlength="80" value="'+esc(edit?(record.subject||''):'')+'" placeholder="예: 음주, 도박, 약물 사용, 반복 확인하기"></div>'
    +groups
    +'<div class="card"><h3>5. 다음 대처 계획</h3><p class="tiny" style="margin:-6px 0 8px">특히 ‘중단했을 때 어려운 점’을 다른 방법으로 어떻게 다룰지 적어보세요.</p><textarea id="cba-next" maxlength="400" placeholder="예: 스트레스 해소가 어려우면 산책하거나 회복 동료에게 연락한다">'+esc(edit?(record.nextStep||''):'')+'</textarea></div>'
    +'<button class="btn" id="cba-save">'+(edit?'수정 저장':'CBA 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
  const root=document.querySelector('#modal .modal-sheet')||document.querySelector('#modal')||document.body;
  bindSmartCbaRows(root);
  $('#cba-save').onclick=()=>{
    const subject=$('#cba-subject').value.trim();
    if(!subject){ toast(subjectLabel+'을 적어주세요.'); return; }
    const data={};
    for(const g of SMART_CBA_GROUPS){
      data[g.key]=smartCbaCollect(root,g.key);
      if(!data[g.key].length){ toast('네 영역을 모두 한 가지 이상 적어주세요.'); return; }
      if(data[g.key].some(x=>!x.term)){ toast('작성한 항목마다 단기·장기를 선택해주세요.'); return; }
    }
    const now=Date.now();
    const rec={rid:edit?(record.rid||smartWorkId()):smartWorkId(),tool:'cba',role:smartRole(),t:edit?Number(record.t||now):now,updatedAt:now,subject,nextStep:$('#cba-next').value.trim(),...data};
    const rows=S.smartWorks||[], key=edit?(record.rid||String(record.t)):'';
    const i=edit?rows.findIndex(x=>(x.rid||String(x.t))===key):-1;
    if(i>=0) rows[i]=rec; else rows.push(rec);
    S.smartWorks=rows; save(); closeModal(); drawSmartCba(); toast(edit?'CBA를 수정했습니다.':'CBA를 저장했습니다.');
  };
}

'''
if fn_anchor not in index:
    raise SystemExit('CBA function anchor not found')
index = index.replace(fn_anchor, functions + fn_anchor, 1)

# Add CBA after HOV in SMART Point 1 actions.
old_actions = '''        "actions": [
          {
            "type": "smart-hov",
            "label": "HOV 가치의 계층 작성하기"
          }
        ]'''
new_actions = '''        "actions": [
          {
            "type": "smart-hov",
            "label": "HOV 가치의 계층 작성하기"
          },
          {
            "type": "smart-cba",
            "label": "CBA 비용-편익 분석 작성하기"
          }
        ]'''
if old_actions not in learning:
    raise SystemExit('SMART Point1 action block not found')
learning = learning.replace(old_actions, new_actions, 1)

idx.write_text(index, encoding='utf-8')
learn.write_text(learning, encoding='utf-8')
sw.write_text(swt, encoding='utf-8')
