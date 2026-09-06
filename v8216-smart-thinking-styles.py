from pathlib import Path
idx=Path('index.html'); sw=Path('sw.js')
s=idx.read_text(encoding='utf-8'); w=sw.read_text(encoding='utf-8')
assert "const BUILD = 'V8.2.15';" in s
s=s.replace("const BUILD = 'V8.2.15';","const BUILD = 'V8.2.16';",1)

# Page after DIBS
anchor='''  <div id="smart-dibs-list" style="margin-top:12px"></div>\n</section>\n'''
assert anchor in s
page='''\n<!-- ══════════ SMART Recovery · Unhelpful Thinking Styles V8.2.16 ══════════ -->\n<section class="pg" id="p-smart-thinking-styles">\n  <div class="sp" style="margin-bottom:11px">\n    <h1 style="margin:0">도움이 되지 않는 사고방식</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back onclick="appBack('smart-tools')">← SMART 실천도구</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    자주 반복되는 사고방식을 <b>빨리 알아차리는 연습</b>입니다. 유형을 고른 뒤 최근 실제 생각을 적어보고, 필요하면 <b>ABC 또는 DIBS</b>로 바로 이어서 점검할 수 있습니다. 진단이 아니라 자기점검 도구이며, 내용은 <b>이 기기에만 저장</b>됩니다.\n  </div>\n  <div id="smart-thinking-role-note"></div>\n  <button class="btn sec" id="smart-thinking-new">+ 내 사고방식 점검하기</button>\n  <div id="smart-thinking-list" style="margin-top:12px"></div>\n</section>\n'''
s=s.replace(anchor,anchor+page,1)

# route / bottom-tab / draw
s=s.replace("p === 'smart-dibs' || p === 'smart-tools'","p === 'smart-dibs' || p === 'smart-thinking-styles' || p === 'smart-tools'",1)
s=s.replace("  if(p === 'smart-dibs') drawSmartDibs();\n","  if(p === 'smart-dibs') drawSmartDibs();\n  if(p === 'smart-thinking-styles') drawSmartThinkingStyles();\n",1)

# back labels
s=s.replace("    'smart-dibs':'DIBS 생각 반박하기'\n","    'smart-dibs':'DIBS 생각 반박하기',\n    'smart-thinking-styles':'도움이 되지 않는 사고방식'\n",1)
s=s.replace("    'smart-deads':'smart-deads', 'smart-disarm':'smart-disarm', 'smart-abc':'smart-abc', 'smart-dibs':'smart-dibs'\n","    'smart-deads':'smart-deads', 'smart-disarm':'smart-disarm', 'smart-abc':'smart-abc', 'smart-dibs':'smart-dibs', 'smart-thinking-styles':'smart-thinking-styles'\n",1)

# learning action handler for future cross-links
s=s.replace("  if(type === 'smart-dibs'){ go('smart-dibs'); return; }\n","  if(type === 'smart-dibs'){ go('smart-dibs'); return; }\n  if(type === 'smart-thinking-styles'){ go('smart-thinking-styles'); return; }\n",1)

# Point 3 hub
old="""smartToolButton('ABC 문제 해결','A 사건 → B 생각 → C 결과 → D 반박 → E 새로운 생각','smart-abc','speak')+smartToolButton('DIBS · 생각 반박하기','도움되지 않는 신념 → 질문·증거점검 → 균형 잡힌 합리적 신념','smart-dibs','speak')+'<div class=\"tiny\" style=\"margin-top:6px\">도움이 되지 않는 사고방식 · 문제해결 도구는 순차적으로 추가됩니다.</div>'+'"""
# tolerate exact current construction without artificial trailing quote
needle="""smartToolButton('ABC 문제 해결','A 사건 → B 생각 → C 결과 → D 반박 → E 새로운 생각','smart-abc','speak')+smartToolButton('DIBS · 생각 반박하기','도움되지 않는 신념 → 질문·증거점검 → 균형 잡힌 합리적 신념','smart-dibs','speak')+'<div class=\"tiny\" style=\"margin-top:6px\">도움이 되지 않는 사고방식 · 문제해결 도구는 순차적으로 추가됩니다.</div>'"""
assert needle in s
repl="""smartToolButton('ABC 문제 해결','A 사건 → B 생각 → C 결과 → D 반박 → E 새로운 생각','smart-abc','speak')+smartToolButton('DIBS · 생각 반박하기','도움되지 않는 신념 → 질문·증거점검 → 균형 잡힌 합리적 신념','smart-dibs','speak')+smartToolButton('도움이 되지 않는 사고방식','내가 자주 쓰는 사고방식 찾기 → ABC 또는 DIBS로 이어보기','smart-thinking-styles','speak')+'<div class=\"tiny\" style=\"margin-top:6px\">문제해결 도구는 순차적으로 추가됩니다.</div>'"""
s=s.replace(needle,repl,1)

# Allow seeded ABC/DIBS from thinking styles without changing edit behavior
s=s.replace("function openSmartAbcEditor(record){\n  const r=record||{};","function openSmartAbcEditor(record,seed){\n  const r=record||seed||{};",1)
s=s.replace("function openSmartDibsEditor(record){\n const r=record||{};","function openSmartDibsEditor(record,seed){\n const r=record||seed||{};",1)

fn_anchor='function learningAction(type){\n'
assert fn_anchor in s
block=r'''/* ── SMART Recovery · Unhelpful Thinking Styles V8.2.16 ── */
const SMART_THINKING_STYLES=[
  {id:'filter',name:'정신적 여과',en:'Mental filter / Selective abstraction',desc:'상황의 한 가지 요소, 특히 부정적인 부분만 보고 다른 정보는 배제하는 터널 비전입니다.',cue:'“좋았던 건 하나도 없어.”'},
  {id:'mind',name:'성급한 결론 / 독심술',en:'Jumping to conclusions / mind reading',desc:'사용 가능한 증거를 충분히 살피기 전에 결론을 내리거나 상대의 생각을 안다고 가정합니다.',cue:'“저 사람이 날 싫어하는 게 분명해.”'},
  {id:'personal',name:'개인화(귀인)',en:'Taking it personally',desc:'여러 요인이 있을 수 있는데도 결과를 지나치게 나 때문이라고 받아들입니다.',cue:'“전부 내 잘못이야.”'},
  {id:'catastrophe',name:'파국',en:'Catastrophising',desc:'최악의 시나리오를 예상하고 상황을 끔찍하고 견딜 수 없는 일처럼 확대합니다.',cue:'“이건 완전히 끝장이야.”'},
  {id:'blackwhite',name:'흑백사고',en:'Black and white thinking',desc:'전부 아니면 전무처럼 중간 지점이나 정도의 차이를 허용하지 않습니다.',cue:'“완벽하지 않으면 실패야.”'},
  {id:'should',name:'‘Shoulds’ and ‘musts’',en:'~해야 한다 / 반드시 ~해야 한다',desc:'나·다른 사람·세상에 경직된 요구를 하고 비현실적인 기대를 갖게 합니다.',cue:'“나는 절대 실수하면 안 돼.”'},
  {id:'overgeneral',name:'과잉 일반화',en:'Over-generalising',desc:'한 번의 경험을 여러 상황 전체에 적용하며 ‘항상’, ‘절대’, ‘모두’ 같은 표현이 자주 나타납니다.',cue:'“나는 항상 일을 망쳐.”'},
  {id:'label',name:'낙인 찍기',en:'Labelling',desc:'한 상황에서의 행동이나 실수를 근거로 나 또는 다른 사람 전체를 큰 말로 규정합니다.',cue:'“나는 완전 실패자야.”'}
];
function smartThinkingRecords(){return (Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(r=>r&&r.kind==='thinking-styles'&&(r.role||'self')===(famMode()?'family':'self')).sort((a,b)=>(b.updatedAt||b.ts||0)-(a.updatedAt||a.ts||0));}
function smartThinkingDate(ts){if(!ts)return '';const d=new Date(ts);return d.getFullYear()+'. '+(d.getMonth()+1)+'. '+d.getDate()+'.';}
function smartThinkingNames(ids){return (Array.isArray(ids)?ids:[]).map(id=>(SMART_THINKING_STYLES.find(x=>x.id===id)||{}).name).filter(Boolean);}
function drawSmartThinkingStyles(){
 const list=$('#smart-thinking-list'),rn=$('#smart-thinking-role-note'),add=$('#smart-thinking-new');if(!list||!add)return;
 if(rn)rn.innerHTML=famMode()?'<div class="note" style="margin-bottom:12px"><b>가족도 내 사고방식을 대상으로 점검합니다.</b><br>상대의 사고를 평가하거나 진단하는 목록이 아닙니다. 내가 상황을 해석하는 방식과 내 반응을 살펴봅니다.</div>':'';
 add.onclick=()=>openSmartThinkingEditor(null);
 const rows=smartThinkingRecords();
 if(!rows.length){list.innerHTML='<div class="card"><b>아직 저장한 사고방식 점검이 없습니다.</b><p class="muted" style="margin:5px 0 0">아래 8가지 유형을 읽고 최근 내 생각에서 자주 나타난 것을 골라보세요.</p></div>'+smartThinkingReference();return;}
 list.innerHTML='<div class="card"><h3>저장한 점검 '+rows.length+'건</h3>'+rows.map(r=>'<div class="sp" style="gap:10px;padding:11px 0;border-top:1px solid var(--line)"><div style="min-width:0;flex:1"><div class="tiny">'+esc(smartThinkingDate(r.updatedAt||r.ts))+'</div><b style="display:block;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(smartThinkingNames(r.styles).join(' · ')||'사고방식 점검')+'</b><div class="muted" style="margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(r.thought||'')+'</div></div><button class="tiny" style="color:var(--acc);font-weight:600" onclick="openSmartThinkingView(\''+esc(r.id)+'\')">보기</button></div>').join('')+'</div>'+smartThinkingReference();
}
function smartThinkingReference(){
 return '<div class="card"><h3>8가지 사고방식 빠르게 보기</h3>'+SMART_THINKING_STYLES.map((x,i)=>'<div style="padding:10px 0;'+(i?'border-top:1px solid var(--line)':'')+'"><b>'+(i+1)+'. '+esc(x.name)+'</b><div class="tiny" style="margin-top:2px">'+esc(x.en)+'</div><div class="muted" style="margin-top:4px">'+esc(x.desc)+'</div></div>').join('')+'</div>';
}
function openSmartThinkingEditor(record){
 const r=record||{},sel=new Set(Array.isArray(r.styles)?r.styles:[]);
 const opts=SMART_THINKING_STYLES.map((x,i)=>'<label style="display:flex;gap:10px;align-items:flex-start;padding:11px 0;'+(i?'border-top:1px solid var(--line)':'')+'"><input type="checkbox" data-thinking-style="'+esc(x.id)+'" style="width:20px;height:20px;flex:0 0 auto;margin-top:2px" '+(sel.has(x.id)?'checked':'')+'><span><b>'+esc(x.name)+'</b><span class="tiny" style="display:block;margin-top:1px">'+esc(x.en)+'</span><span class="muted" style="display:block;margin-top:3px">'+esc(x.desc)+'</span><span class="tiny" style="display:block;margin-top:3px">예: '+esc(x.cue)+'</span></span></label>').join('');
 modal('<h2>'+(record?'사고방식 점검 수정':'내 사고방식 점검')+'</h2><p class="muted" style="margin:5px 0 14px">정답을 고르는 검사가 아닙니다. 최근 내 생각에서 반복되는 패턴을 알아차리는 연습입니다.</p><div class="card"><h3>내게 자주 나타나는 유형</h3>'+opts+'</div><div class="card"><label>최근 실제로 떠오른 생각</label><textarea id="thinking-thought" maxlength="700" placeholder="예: ‘이번에도 실수했으니 나는 항상 실패할 거야.’">'+esc(r.thought||'')+'</textarea></div><div class="card"><label>그때의 상황</label><textarea id="thinking-situation" maxlength="700" placeholder="무슨 일이 있었나요?">'+esc(r.situation||'')+'</textarea></div><div class="card"><label>그 생각이 내 감정·행동에 미친 영향</label><textarea id="thinking-impact" maxlength="800" placeholder="예: 불안이 커졌고, 사람을 피하거나 술 생각이 강해졌다.">'+esc(r.impact||'')+'</textarea></div><button class="btn" id="thinking-save">'+(record?'수정 저장':'점검 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
 $('#thinking-save').onclick=()=>{
   const styles=$$('[data-thinking-style]').filter(x=>x.checked).map(x=>x.dataset.thinkingStyle), thought=$('#thinking-thought').value.trim();
   if(!styles.length){toast('내게 나타나는 사고방식을 하나 이상 골라주세요.');return;} if(!thought){toast('최근 실제로 떠오른 생각을 적어주세요.');return;}
   const rec={id:record?record.id:('thinking-'+Date.now()+'-'+Math.random().toString(36).slice(2,7)),kind:'thinking-styles',role:famMode()?'family':'self',ts:record?(record.ts||Date.now()):Date.now(),updatedAt:Date.now(),styles,thought,situation:$('#thinking-situation').value.trim(),impact:$('#thinking-impact').value.trim()};
   if(!Array.isArray(S.smartWorks))S.smartWorks=[]; if(record){const i=S.smartWorks.findIndex(x=>x&&x.id===record.id);if(i>=0)S.smartWorks[i]=rec;else S.smartWorks.push(rec);}else S.smartWorks.push(rec);
   save();closeModal();drawSmartThinkingStyles();toast(record?'사고방식 점검을 수정했습니다.':'사고방식 점검을 저장했습니다.');
 };
}
function smartThinkingOpenAbc(r){closeModal();go('smart-abc');setTimeout(()=>openSmartAbcEditor(null,{a:r.situation||'',b:r.thought||'',c:r.impact||''}),80);}
function smartThinkingOpenDibs(r){closeModal();go('smart-dibs');setTimeout(()=>openSmartDibsEditor(null,{ib:r.thought||'',impact:r.impact||''}),80);}
function openSmartThinkingView(id){
 const r=(Array.isArray(S.smartWorks)?S.smartWorks:[]).find(x=>x&&x.id===id&&x.kind==='thinking-styles');if(!r)return;
 const selected=(Array.isArray(r.styles)?r.styles:[]).map(id=>SMART_THINKING_STYLES.find(x=>x.id===id)).filter(Boolean);
 const sec=(t,v)=>'<div class="card"><h3>'+esc(t)+'</h3><div style="white-space:pre-wrap">'+(String(v||'').trim()?esc(v):'<span class="muted">작성하지 않음</span>')+'</div></div>';
 modal('<h2>도움이 되지 않는 사고방식</h2><div class="muted" style="margin:-4px 0 12px">'+esc(smartThinkingDate(r.updatedAt||r.ts))+'</div><div class="card"><h3>내가 알아차린 유형</h3>'+selected.map(x=>'<div style="padding:7px 0"><b>'+esc(x.name)+'</b><div class="tiny">'+esc(x.en)+'</div></div>').join('')+'</div>'+sec('최근 실제 생각',r.thought)+sec('그때의 상황',r.situation)+sec('감정·행동에 미친 영향',r.impact)+'<button class="btn" id="thinking-to-abc">이 생각으로 ABC 작성하기</button><div style="height:8px"></div><button class="btn sec" id="thinking-to-dibs">이 생각으로 DIBS 작성하기</button><div style="height:8px"></div><button class="btn ghost" id="thinking-edit">수정</button><div style="height:8px"></div><button class="btn bad" id="thinking-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
 $('#thinking-to-abc').onclick=()=>smartThinkingOpenAbc(r);$('#thinking-to-dibs').onclick=()=>smartThinkingOpenDibs(r);$('#thinking-edit').onclick=()=>openSmartThinkingEditor(r);$('#thinking-delete').onclick=()=>{if(!confirm('이 사고방식 점검 기록을 삭제할까요?'))return;S.smartWorks=(Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>!(x&&x.id===r.id));save();closeModal();drawSmartThinkingStyles();toast('기록을 삭제했습니다.');};
}

'''
s=s.replace(fn_anchor,block+fn_anchor,1)

assert "const APP_VERSION = 'V8.2.15';" in w and "const V = 'ohg-v8215-smart-dibs';" in w
w=w.replace("const APP_VERSION = 'V8.2.15';","const APP_VERSION = 'V8.2.16';",1).replace("const V = 'ohg-v8215-smart-dibs';","const V = 'ohg-v8216-smart-thinking-styles';",1)
idx.write_text(s,encoding='utf-8');sw.write_text(w,encoding='utf-8')
print('V8.2.16 thinking styles patch applied')
