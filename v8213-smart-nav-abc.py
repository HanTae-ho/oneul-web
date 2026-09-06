from pathlib import Path

idx = Path('index.html')
learn = Path('learning-data.js')
sw = Path('sw.js')

s = idx.read_text(encoding='utf-8')
ld = learn.read_text(encoding='utf-8')
swtxt = sw.read_text(encoding='utf-8')

# Version
assert "const BUILD = 'V8.2.12';" in s
s = s.replace("const BUILD = 'V8.2.12';", "const BUILD = 'V8.2.13';", 1)

# Preserve navigation origin so SMART back labels match the actual entry route.
old_state = "const st={ohg:1,p:p,depth:opt.replace?navDepth():navDepth()+1};"
assert old_state in s
s = s.replace(old_state, "const st={ohg:1,p:p,from:prev,depth:opt.replace?navDepth():navDepth()+1};", 1)

# All existing SMART worksheet headers use a common dynamic back marker.
old_back = '<button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack(\'smart-tools\')">← SMART Recovery</button>'
assert s.count(old_back) == 6, s.count(old_back)
new_back = '<button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back onclick="appBack(\'smart-tools\')">← SMART 실천도구</button>'
s = s.replace(old_back, new_back)

# Common route-aware label sync.
anchor = "/* ══════════ SMART Recovery · 실천도구 허브 V8.2.11 ══════════ */"
assert anchor in s
helper = r'''/* ── SMART Recovery · route-aware back labels V8.2.13 ── */
function syncSmartBack(){
  const b=$('#p-'+cur+' [data-smart-back]'); if(!b) return;
  const st=(history.state&&history.state.ohg)?history.state:{};
  const from=String(st.from||'');
  const labels={
    'smart-tools':'SMART 실천도구',
    'learn-topic':'SMART Recovery',
    'capsule':'미래의 나에게',
    'smart-hov':'가치의 계층 HOV',
    'smart-three-questions':'나의 3가지 질문',
    'smart-change-plan':'변화 계획',
    'smart-cba':'비용-편익 분석 CBA',
    'smart-deads':'DEADS',
    'smart-disarm':'DISARM',
    'smart-abc':'ABC 문제 해결'
  };
  const fallbacks={
    'learn-topic':'learn-topic', 'capsule':'capsule', 'smart-tools':'smart-tools',
    'smart-hov':'smart-hov', 'smart-three-questions':'smart-three-questions',
    'smart-change-plan':'smart-change-plan', 'smart-cba':'smart-cba',
    'smart-deads':'smart-deads', 'smart-disarm':'smart-disarm', 'smart-abc':'smart-abc'
  };
  b.textContent='← '+(labels[from]||'SMART 실천도구');
  b.onclick=()=>appBack(fallbacks[from]||'smart-tools');
}

'''
s = s.replace(anchor, helper + anchor, 1)

# Re-sync label whenever route changes.
old_cur = "  cur = p;\n  $('#tabs').style.display = (p === 'intro') ? 'none' : 'flex';"
assert old_cur in s
s = s.replace(old_cur, "  cur = p;\n  syncSmartBack();\n  $('#tabs').style.display = (p === 'intro') ? 'none' : 'flex';", 1)

# Fix bottom-tab ownership for all SMART pages.
old_tabs = "p === 'smart-hov' || p === 'smart-cba' || p === 'smart-deads' || p === 'smart-disarm' || p === 'smart-tools'"
assert old_tabs in s
new_tabs = "p === 'smart-hov' || p === 'smart-cba' || p === 'smart-change-plan' || p === 'smart-three-questions' || p === 'smart-deads' || p === 'smart-disarm' || p === 'smart-abc' || p === 'smart-tools'"
s = s.replace(old_tabs, new_tabs, 1)

# Add ABC page after DISARM, before Future Self.
page_anchor = '''</section>\n\n<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->'''
assert page_anchor in s
abc_page = r'''</section>

<!-- ══════════ SMART Recovery · ABC V8.2.13 ══════════ -->
<section class="pg" id="p-smart-abc">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">ABC 문제 해결</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back onclick="appBack('smart-tools')">← SMART 실천도구</button>
  </div>
  <div class="note" style="margin-bottom:12px">
    힘든 <b>사건(A)</b>과 그 사건에 대한 <b>생각·신념(B)</b>, 그로 인한 <b>감정·행동의 결과(C)</b>를 나누어 봅니다. 이어서 생각에 질문하고 <b>반박(D)</b>한 뒤, 더 현실적이고 도움이 되는 <b>새로운 생각(E)</b>을 만들어봅니다. 내용은 <b>이 기기에만 저장</b>됩니다.
  </div>
  <div id="smart-abc-role-note"></div>
  <button class="btn sec" id="smart-abc-new">+ ABC 새로 작성하기</button>
  <div id="smart-abc-list" style="margin-top:12px"></div>
</section>'''
s = s.replace(page_anchor, abc_page + "\n\n<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->", 1)

# Route draw.
route_anchor = "  if(p === 'smart-disarm') drawSmartDisarm();\n  if(p === 'smart-tools') drawSmartTools();"
assert route_anchor in s
s = s.replace(route_anchor, "  if(p === 'smart-disarm') drawSmartDisarm();\n  if(p === 'smart-abc') drawSmartAbc();\n  if(p === 'smart-tools') drawSmartTools();", 1)

# Point 3 now exposes ABC and keeps later tools as planned.
old_p3 = "  h+='<div class=\"card\"><h3>Point 3 · 생각·감정·행동 관리하기</h3><p class=\"muted\" style=\"margin:-4px 0 0\">ABC · DIB/DIBS 등 작성형 도구를 순차적으로 추가할 예정입니다.</p><div class=\"tiny\" style=\"margin-top:8px\">준비 중</div></div>';"
assert old_p3 in s
new_p3 = "  h+='<div class=\"card\"><h3>Point 3 · 생각·감정·행동 관리하기</h3><p class=\"muted\" style=\"margin:-4px 0 11px\">사건과 생각을 구분하고, 감정·행동에 도움이 되는 더 균형 잡힌 관점을 연습합니다.</p>'+smartToolButton('ABC 문제 해결','A 사건 → B 생각 → C 결과 → D 반박 → E 새로운 생각','smart-abc','speak')+'<div class=\"tiny\" style=\"margin-top:6px\">DIB/DIBS · 도움이 되지 않는 사고방식 · 문제해결 도구는 순차적으로 추가됩니다.</div></div>';"
s = s.replace(old_p3, new_p3, 1)

# ABC functions use the existing shared smartWorks store.
fn_anchor = "function learningAction(type){\n"
assert fn_anchor in s
abc_fn = r'''/* ── SMART Recovery · ABC V8.2.13 ── */
function smartAbcRecords(){
  return (Array.isArray(S.smartWorks)?S.smartWorks:[])
    .filter(r=>r && r.kind==='abc' && (r.role||'self')===(famMode()?'family':'self'))
    .sort((a,b)=>(b.updatedAt||b.ts||0)-(a.updatedAt||a.ts||0));
}
function smartAbcDate(ts){
  if(!ts) return '';
  const d=new Date(ts); return d.getFullYear()+'. '+(d.getMonth()+1)+'. '+d.getDate()+'.';
}
function drawSmartAbc(){
  const list=$('#smart-abc-list'), rn=$('#smart-abc-role-note'), add=$('#smart-abc-new');
  if(!list||!add) return;
  if(rn){
    rn.innerHTML=famMode()
      ? '<div class="note" style="margin-bottom:12px"><b>가족도 내 반응을 ABC로 살펴봅니다.</b><br>상대의 생각을 진단하거나 논박하는 도구가 아닙니다. 내가 경험한 사건과 내 생각·감정·행동을 구분하고, 내가 선택할 수 있는 더 도움이 되는 반응을 찾습니다.</div>'
      : '';
  }
  add.onclick=()=>openSmartAbcEditor(null);
  const rows=smartAbcRecords();
  if(!rows.length){
    list.innerHTML='<div class="card"><b>아직 작성한 ABC가 없습니다.</b><p class="muted" style="margin:5px 0 0">최근 마음이 크게 흔들렸던 상황 하나를 A부터 E까지 천천히 나누어 보세요.</p></div>';
    return;
  }
  list.innerHTML='<div class="card"><h3>저장한 ABC '+rows.length+'건</h3>'+rows.map(r=>'<div class="sp" style="gap:10px;padding:11px 0;border-top:1px solid var(--line)"><div style="min-width:0;flex:1"><div class="tiny">'+esc(smartAbcDate(r.updatedAt||r.ts))+'</div><b style="display:block;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(r.a||'ABC 기록')+'</b><div class="muted" style="margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(r.e||r.b||'')+'</div></div><button class="tiny" style="color:var(--acc);font-weight:600" onclick="openSmartAbcView(\''+esc(r.id)+'\')">보기</button></div>').join('')+'</div>';
}
function smartAbcField(title,id,value,placeholder,help,max){
  return '<div class="card"><label>'+esc(title)+'</label>'+(help?'<div class="tiny" style="margin:4px 0 7px">'+esc(help)+'</div>':'')+'<textarea id="'+id+'" maxlength="'+(max||800)+'" placeholder="'+esc(placeholder)+'">'+esc(value||'')+'</textarea></div>';
}
function openSmartAbcEditor(record){
  const r=record||{};
  modal('<h2>'+(record?'ABC 수정':'ABC 문제 해결 작성')+'</h2>'
    +'<p class="muted" style="margin:5px 0 14px">사건 자체와 그 사건에 대한 내 생각을 분리해 적는 것이 핵심입니다. 감정을 틀렸다고 판단하기보다, 그 감정과 행동에 영향을 준 생각을 더 현실적으로 점검합니다.</p>'
    +smartAbcField('A · 활성화 사건','abc-a',r.a,'무슨 일이 있었나요? 무엇을 보거나 들었고, 무엇이 나를 흔들었나요?','사건·상황·촉발요인을 가능한 사실 중심으로 적습니다.',700)
    +smartAbcField('B · 그때 떠오른 생각·신념','abc-b',r.b,'예: “나는 절대 이런 대우를 받아서는 안 돼.”','“반드시”, “절대”, “참을 수 없어”, “나는/상대는 …해야 해” 같은 강한 요구가 있는지도 살펴봅니다.',700)
    +smartAbcField('C · 감정·행동·결과','abc-c',r.c,'예: 화가 치밀었고 술을 마시고 싶어졌다. 이후 대화를 피했다.','그 생각을 믿었을 때 어떻게 느꼈고, 무엇을 했거나 하고 싶었으며, 결과가 어땠는지 적습니다.',900)
    +smartAbcField('D · 생각에 질문하고 반박하기','abc-d',r.d,'예: “상대가 그러면 안 된다는 절대적인 근거가 있나? 이 생각이 내 회복에 도움이 되나?”','돌이켜보며 사실인지, 논리적인지, 장기적으로 도움이 되는지 질문하고 다른 관점을 찾아봅니다.',1000)
    +smartAbcField('E · 효과적인 새로운 생각','abc-e',r.e,'예: “마음에 들지 않지만 견딜 수 있다. 나는 이 일 때문에 회복을 포기할 필요가 없다.”','A를 더 현실적이고 균형 있게 바라보는 새로운 생각과, 그 생각으로 선택하고 싶은 행동을 적습니다.',900)
    +'<button class="btn" id="abc-save">'+(record?'수정 저장':'ABC 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
  $('#abc-save').onclick=()=>{
    const rec={
      id:record?record.id:('abc-'+Date.now()+'-'+Math.random().toString(36).slice(2,7)), kind:'abc', role:famMode()?'family':'self',
      ts:record?(record.ts||Date.now()):Date.now(), updatedAt:Date.now(),
      a:$('#abc-a').value.trim(), b:$('#abc-b').value.trim(), c:$('#abc-c').value.trim(), d:$('#abc-d').value.trim(), e:$('#abc-e').value.trim()
    };
    if(!rec.a){ toast('활성화 사건(A)을 적어주세요.'); return; }
    if(!rec.b){ toast('그때 떠오른 생각·신념(B)을 적어주세요.'); return; }
    if(!rec.c){ toast('감정·행동의 결과(C)를 적어주세요.'); return; }
    if(!rec.d){ toast('생각에 질문하고 반박하는 내용(D)을 적어주세요.'); return; }
    if(!rec.e){ toast('효과적인 새로운 생각(E)을 적어주세요.'); return; }
    if(!Array.isArray(S.smartWorks)) S.smartWorks=[];
    if(record){ const i=S.smartWorks.findIndex(x=>x&&x.id===record.id); if(i>=0) S.smartWorks[i]=rec; else S.smartWorks.push(rec); }
    else S.smartWorks.push(rec);
    save(); closeModal(); drawSmartAbc(); toast(record?'ABC를 수정했습니다.':'ABC를 저장했습니다.');
  };
}
function smartAbcSection(title,text){
  return '<div class="card"><h3>'+esc(title)+'</h3><div style="white-space:pre-wrap">'+(String(text||'').trim()?esc(text):'<span class="muted">작성하지 않음</span>')+'</div></div>';
}
function openSmartAbcView(id){
  const r=smartAbcRecords().find(x=>x.id===id); if(!r) return;
  modal('<h2>ABC 문제 해결</h2><div class="muted" style="margin:-4px 0 12px">'+esc(smartAbcDate(r.updatedAt||r.ts))+'</div>'
    +smartAbcSection('A · 활성화 사건',r.a)+smartAbcSection('B · 생각·신념',r.b)+smartAbcSection('C · 감정·행동·결과',r.c)+smartAbcSection('D · 질문하고 반박하기',r.d)+smartAbcSection('E · 효과적인 새로운 생각',r.e)
    +'<button class="btn sec" id="abc-edit">수정</button><div style="height:8px"></div><button class="btn bad" id="abc-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
  $('#abc-edit').onclick=()=>openSmartAbcEditor(r);
  $('#abc-delete').onclick=()=>{
    if(!confirm('이 ABC 기록을 삭제할까요?')) return;
    S.smartWorks=(Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>!(x&&x.id===r.id));
    save(); closeModal(); drawSmartAbc(); toast('ABC 기록을 삭제했습니다.');
  };
}

'''
s = s.replace(fn_anchor, abc_fn + fn_anchor, 1)

# Learning action handler.
action_anchor = "  if(type === 'smart-disarm'){ go('smart-disarm'); return; }\n"
assert action_anchor in s
s = s.replace(action_anchor, action_anchor + "  if(type === 'smart-abc'){ go('smart-abc'); return; }\n", 1)

# Point 3 learning content gets an ABC action.
old_practice = '        "practice": "오늘 힘들었던 상황 하나를 A-사건, B-생각, C-감정과 행동으로 나누어 살펴보세요."\n      },'
assert old_practice in ld
new_practice = '        "practice": "오늘 힘들었던 상황 하나를 A-사건, B-생각, C-감정과 행동으로 나누어 살펴보세요.",\n        "actions": [\n          {\n            "type": "smart-abc",\n            "label": "ABC 문제 해결 작성하기"\n          }\n        ]\n      },'
ld = ld.replace(old_practice, new_practice, 1)
ld = ld.replace('회복학습 데이터 V8.2.10','회복학습 데이터 V8.2.13',1)

# SW version/cache.
assert "const APP_VERSION = 'V8.2.12';" in swtxt
assert "const V = 'ohg-v8212-capsule-disarm-link';" in swtxt
swtxt = swtxt.replace("const APP_VERSION = 'V8.2.12';", "const APP_VERSION = 'V8.2.13';",1)
swtxt = swtxt.replace("const V = 'ohg-v8212-capsule-disarm-link';", "const V = 'ohg-v8213-smart-nav-abc';",1)

idx.write_text(s,encoding='utf-8')
learn.write_text(ld,encoding='utf-8')
sw.write_text(swtxt,encoding='utf-8')
print('V8.2.13 SMART navigation + ABC patch applied')
