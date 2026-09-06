from pathlib import Path
idx=Path('index.html'); sw=Path('sw.js')
s=idx.read_text(encoding='utf-8'); w=sw.read_text(encoding='utf-8')
assert "const BUILD = 'V8.2.16';" in s
assert "const DATA_SCHEMA = 6;" in s
s=s.replace("const BUILD = 'V8.2.16';","const BUILD = 'V8.2.17';",1)

# Page after Unhelpful Thinking Styles
anchor='''  <div id="smart-thinking-list" style="margin-top:12px"></div>\n</section>\n'''
assert anchor in s
page='''\n<!-- ══════════ SMART Recovery · Problem Solving V8.2.17 ══════════ -->\n<section class="pg" id="p-smart-problem-solving">\n  <div class="sp" style="margin-bottom:11px">\n    <h1 style="margin:0">문제 해결 · 5단계</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back onclick="appBack('smart-tools')">← SMART 실천도구</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    상황을 어떻게 처리해야 할지 확신이 없을 때, 문제를 구체적으로 정의하고 <b>브레인스토밍 → 평가 → 선택 → 서면 계획</b>으로 이어갑니다. SMART Recovery 번역본의 <b>문제 해결을 위한 5단계</b>와 문제 해결 워크시트를 앱에 맞게 옮겼으며, 내용은 <b>이 기기에만 저장</b>됩니다.\n  </div>\n  <div id="smart-problem-role-note"></div>\n  <button class="btn sec" id="smart-problem-new">+ 문제 해결 새로 작성하기</button>\n  <div id="smart-problem-list" style="margin-top:12px"></div>\n</section>\n'''
s=s.replace(anchor,anchor+page,1)

# route / bottom-tab / draw
needle="p === 'smart-thinking-styles' || p === 'smart-tools'"
assert needle in s
s=s.replace(needle,"p === 'smart-thinking-styles' || p === 'smart-problem-solving' || p === 'smart-tools'",1)
needle="  if(p === 'smart-thinking-styles') drawSmartThinkingStyles();\n"
assert needle in s
s=s.replace(needle,needle+"  if(p === 'smart-problem-solving') drawSmartProblemSolving();\n",1)

# back labels
needle="    'smart-thinking-styles':'도움이 되지 않는 사고방식'\n"
assert needle in s
s=s.replace(needle,"    'smart-thinking-styles':'도움이 되지 않는 사고방식',\n    'smart-problem-solving':'문제 해결 · 5단계'\n",1)
needle="'smart-dibs':'smart-dibs', 'smart-thinking-styles':'smart-thinking-styles'\n"
assert needle in s
s=s.replace(needle,"'smart-dibs':'smart-dibs', 'smart-thinking-styles':'smart-thinking-styles', 'smart-problem-solving':'smart-problem-solving'\n",1)

# Point 3 hub
needle="""+smartToolButton('도움이 되지 않는 사고방식','내가 자주 쓰는 사고방식 찾기 → ABC 또는 DIBS로 이어보기','smart-thinking-styles','speak')+'<div class=\"tiny\" style=\"margin-top:6px\">문제해결 도구는 순차적으로 추가됩니다.</div>'"""
assert needle in s
repl="""+smartToolButton('도움이 되지 않는 사고방식','내가 자주 쓰는 사고방식 찾기 → ABC 또는 DIBS로 이어보기','smart-thinking-styles','speak')+smartToolButton('문제 해결 · 5단계','문제 정의 → 브레인스토밍 → 평가 → 선택 → 서면 계획','smart-problem-solving','check')"""
s=s.replace(needle,repl,1)

# learning action handler
needle="  if(type === 'smart-thinking-styles'){ go('smart-thinking-styles'); return; }\n"
assert needle in s
s=s.replace(needle,needle+"  if(type === 'smart-problem-solving'){ go('smart-problem-solving'); return; }\n",1)

# Problem Solving logic before learningAction
fn_anchor='function learningAction(type){\n'
assert fn_anchor in s
block=r'''/* ── SMART Recovery · Problem Solving V8.2.17 ──
   번역본 Point 3의 '삶의 문제 해결 / 문제 해결을 위한 5단계'와
   부록 Problem Solving 워크시트의 질문 순서를 유지합니다. */
function smartProblemRecords(){return (Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(r=>r&&r.kind==='problem-solving'&&(r.role||'self')===(famMode()?'family':'self')).sort((a,b)=>(b.updatedAt||b.ts||0)-(a.updatedAt||a.ts||0));}
function smartProblemDate(ts){if(!ts)return '';const d=new Date(ts);return d.getFullYear()+'. '+(d.getMonth()+1)+'. '+d.getDate()+'.';}
function smartProblemStrategyLabel(r){const rows=Array.isArray(r&&r.strategies)?r.strategies:[];const hit=rows.find(x=>x&&x.id===r.selectedId);return hit&&hit.text?hit.text:(r&&r.selectedText)||'';}
function drawSmartProblemSolving(){
 const list=$('#smart-problem-list'),rn=$('#smart-problem-role-note'),add=$('#smart-problem-new');if(!list||!add)return;
 if(rn)rn.innerHTML=famMode()?'<div class="note" style="margin-bottom:12px"><b>가족도 내 문제와 내 선택을 중심으로 작성합니다.</b><br>상대를 바꾸거나 통제하는 계획이 아니라, 내가 처한 상황에서 내가 선택할 수 있는 행동과 경계를 구체적으로 찾는 데 사용합니다.</div>':'';
 add.onclick=()=>openSmartProblemEditor(null);
 const rows=smartProblemRecords();
 if(!rows.length){list.innerHTML='<div class="card"><b>아직 저장한 문제 해결 기록이 없습니다.</b><p class="muted" style="margin:5px 0 0">지금 어떻게 처리해야 할지 막막한 문제 하나를 최대한 구체적으로 정의하는 것부터 시작해 보세요.</p></div>';return;}
 list.innerHTML='<div class="card"><h3>저장한 문제 해결 '+rows.length+'건</h3>'+rows.map(r=>'<div class="sp" style="gap:10px;padding:11px 0;border-top:1px solid var(--line)"><div style="min-width:0;flex:1"><div class="tiny">'+esc(smartProblemDate(r.updatedAt||r.ts))+'</div><b style="display:block;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(r.what||r.when||'문제 해결 기록')+'</b><div class="muted" style="margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(smartProblemStrategyLabel(r)||r.plan||'')+'</div></div><button class="tiny" style="color:var(--acc);font-weight:600" onclick="openSmartProblemView(\''+esc(r.id)+'\')">보기</button></div>').join('')+'</div>';
}
function smartProblemField(title,id,value,placeholder,help,max){return '<div class="field"><label>'+esc(title)+'</label>'+(help?'<div class="tiny" style="margin:4px 0 7px">'+esc(help)+'</div>':'')+'<textarea id="'+id+'" maxlength="'+(max||800)+'" placeholder="'+esc(placeholder||'')+'">'+esc(value||'')+'</textarea></div>';}
function smartProblemClamp(v){v=parseInt(v,10);return Number.isFinite(v)?Math.max(0,Math.min(10,v)):0;}
function smartProblemStrategyCard(x,i){x=x||{};return '<div class="card" data-ps-row="'+i+'"><div class="sp" style="gap:8px"><h3 style="margin:0">전략 '+(i+1)+'</h3><button type="button" class="tiny" style="color:var(--bad);font-weight:600" data-ps-remove="'+i+'">삭제</button></div><div class="field" style="margin-top:10px"><label>가능한 전략</label><textarea data-ps-text="'+i+'" maxlength="500" placeholder="판단하지 말고 가능한 아이디어를 적어보세요.">'+esc(x.text||'')+'</textarea></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div class="field"><label>실행 가능성 0~10</label><input data-ps-feasible="'+i+'" type="number" min="0" max="10" value="'+smartProblemClamp(x.feasible)+'"></div><div class="field"><label>시도할 준비 0~10</label><input data-ps-ready="'+i+'" type="number" min="0" max="10" value="'+smartProblemClamp(x.ready)+'"></div></div><div class="field"><label>좋은 점</label><textarea data-ps-good="'+i+'" maxlength="500" placeholder="이 전략의 좋은 점은 무엇인가요?">'+esc(x.good||'')+'</textarea></div><div class="field"><label>가능한 위험</label><textarea data-ps-risk="'+i+'" maxlength="500" placeholder="어떤 위험이나 어려움이 있을 수 있나요?">'+esc(x.risk||'')+'</textarea></div><div class="field"><label>종합 점수 0~10</label><input data-ps-score="'+i+'" type="number" min="0" max="10" value="'+smartProblemClamp(x.score)+'"></div><label style="display:flex;gap:9px;align-items:center;margin-top:8px"><input type="radio" name="ps-selected" data-ps-selected="'+i+'" style="width:19px;height:19px;flex:0 0 auto" '+(x.selected?'checked':'')+'><span><b>이 전략을 선택하기</b></span></label></div>';}
function openSmartProblemEditor(record){
 const r=record||{};let strategies=(Array.isArray(r.strategies)&&r.strategies.length?r.strategies:[{id:'ps-'+Date.now(),text:'',feasible:0,ready:0,good:'',risk:'',score:0}]).map(x=>Object.assign({},x,{selected:x.id===r.selectedId}));
 const renderRows=()=>{const box=$('#ps-strategies');if(!box)return;box.innerHTML=strategies.map((x,i)=>smartProblemStrategyCard(x,i)).join('');box.querySelectorAll('[data-ps-remove]').forEach(b=>b.onclick=()=>{if(strategies.length<=1){toast('전략을 하나 이상 남겨주세요.');return;}collectRows();strategies.splice(+b.dataset.psRemove,1);renderRows();});};
 const collectRows=()=>{strategies=strategies.map((x,i)=>({id:x.id||('ps-'+Date.now()+'-'+i),text:($('[data-ps-text="'+i+'"]')||{}).value?.trim()||'',feasible:smartProblemClamp(($('[data-ps-feasible="'+i+'"]')||{}).value),ready:smartProblemClamp(($('[data-ps-ready="'+i+'"]')||{}).value),good:($('[data-ps-good="'+i+'"]')||{}).value?.trim()||'',risk:($('[data-ps-risk="'+i+'"]')||{}).value?.trim()||'',score:smartProblemClamp(($('[data-ps-score="'+i+'"]')||{}).value),selected:!!(($('[data-ps-selected="'+i+'"]')||{}).checked)}));return strategies;};
 modal('<h2>'+(record?'문제 해결 수정':'문제 해결 · 5단계')+'</h2><p class="muted" style="margin:5px 0 14px">문제를 작게 나누고, 해결책을 판단하기 전에 충분히 떠올린 다음, 현실적으로 평가하고 하나를 골라 글로 계획합니다.</p><div class="card"><h3>1 · 문제 정의</h3>'+smartProblemField('문제는 일반적으로 언제 발생합니까? 언제 일어날 가능성이 있습니까?','ps-when',r.when,'언제, 어떤 때 반복되나요?','최대한 구체적으로 작성합니다.',700)+smartProblemField('누가 관련되어 있나요? 또 누가 참여할 가능성이 있나요?','ps-who',r.who,'관련된 사람을 적어보세요.','',500)+smartProblemField('보통 무슨 일이 일어나나요? 무슨 일이 일어날 것 같나요?','ps-what',r.what,'실제로 일어나는 일을 구체적으로 적어보세요.','',800)+smartProblemField('이 상황에 대한 나의 일반적인 생각과 감정은 무엇입니까?','ps-thoughts',r.thoughts,'그때 반복되는 생각과 감정을 적어보세요.','',900)+'</div><div class="note" style="margin-bottom:12px"><b>2 · 브레인스토밍</b><br>먼저 판단하지 말고 가능한 해결책을 최대한 많이 떠올립니다. “그건 안 될 거야”라고 미리 제외하지 않습니다.</div><div id="ps-strategies"></div><button class="btn sec" type="button" id="ps-add">+ 가능한 전략 추가</button><div class="card" style="margin-top:12px"><h3>4 · 선택</h3><p class="muted" style="margin:-4px 0 0">위 전략을 평가한 뒤, 실제로 시도할 전략 하나의 <b>‘이 전략을 선택하기’</b>를 체크하세요.</p></div><div class="card"><h3>5 · 서면으로 계획 작성하기</h3>'+smartProblemField('선택한 해결책을 어떻게 실행할까요?','ps-plan',r.plan,'무엇을, 어떤 순서로 실행할지 적어보세요.','머릿속 계획보다 글로 적은 계획이 실행에 도움이 됩니다.',1000)+'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div class="field"><label>시작 날짜</label><input id="ps-start" type="date" value="'+esc(r.start||'')+'"></div><div class="field"><label>장소</label><input id="ps-place" maxlength="120" value="'+esc(r.place||'')+'" placeholder="어디에서 시작할까요?"></div></div>'+smartProblemField('성공에 필요한 것·도움','ps-needs',r.needs,'필요한 준비, 사람, 자원 등을 적어보세요.','',700)+smartProblemField('실행 후 결과 점검','ps-review',r.review,'계획이 효과가 있었나요? 무엇을 수정하거나 다른 해결책을 시도해야 하나요?','실행 후 다시 열어 기록해도 됩니다.',800)+'</div><button class="btn" id="ps-save">'+(record?'수정 저장':'문제 해결 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
 renderRows();
 $('#ps-add').onclick=()=>{collectRows();strategies.push({id:'ps-'+Date.now()+'-'+Math.random().toString(36).slice(2,6),text:'',feasible:0,ready:0,good:'',risk:'',score:0,selected:false});renderRows();setTimeout(()=>{const rows=$$('[data-ps-row]');if(rows.length)rows[rows.length-1].scrollIntoView({behavior:'smooth',block:'center'});},30);};
 $('#ps-save').onclick=()=>{const rows=collectRows().filter(x=>x.text);const what=$('#ps-what').value.trim();if(!what){toast('보통 무슨 일이 일어나는지 적어주세요.');return;}if(!rows.length){toast('가능한 전략을 하나 이상 적어주세요.');return;}const selected=rows.find(x=>x.selected);if(!selected){toast('시도할 전략 하나를 선택해주세요.');return;}const plan=$('#ps-plan').value.trim();if(!plan){toast('선택한 해결책의 실행 계획을 적어주세요.');return;}const rec={id:record?record.id:('problem-'+Date.now()+'-'+Math.random().toString(36).slice(2,7)),kind:'problem-solving',role:famMode()?'family':'self',ts:record?(record.ts||Date.now()):Date.now(),updatedAt:Date.now(),when:$('#ps-when').value.trim(),who:$('#ps-who').value.trim(),what,thoughts:$('#ps-thoughts').value.trim(),strategies:rows.map(x=>({id:x.id,text:x.text,feasible:x.feasible,ready:x.ready,good:x.good,risk:x.risk,score:x.score})),selectedId:selected.id,selectedText:selected.text,plan,start:$('#ps-start').value,place:$('#ps-place').value.trim(),needs:$('#ps-needs').value.trim(),review:$('#ps-review').value.trim()};if(!Array.isArray(S.smartWorks))S.smartWorks=[];if(record){const i=S.smartWorks.findIndex(x=>x&&x.id===record.id);if(i>=0)S.smartWorks[i]=rec;else S.smartWorks.push(rec);}else S.smartWorks.push(rec);save();closeModal();drawSmartProblemSolving();toast(record?'문제 해결 기록을 수정했습니다.':'문제 해결 기록을 저장했습니다.');};
}
function smartProblemSection(title,text){return '<div class="card"><h3>'+esc(title)+'</h3><div style="white-space:pre-wrap">'+(String(text||'').trim()?esc(text):'<span class="muted">작성하지 않음</span>')+'</div></div>';}
function openSmartProblemView(id){
 const r=smartProblemRecords().find(x=>x.id===id);if(!r)return;const rows=Array.isArray(r.strategies)?r.strategies:[];
 const evals=rows.map((x,i)=>'<div style="padding:10px 0;'+(i?'border-top:1px solid var(--line)':'')+'"><b>'+(x.id===r.selectedId?'✓ ':'')+esc(x.text||('전략 '+(i+1)))+'</b><div class="tiny" style="margin-top:4px">실행 가능성 '+smartProblemClamp(x.feasible)+'/10 · 시도 준비 '+smartProblemClamp(x.ready)+'/10 · 종합 '+smartProblemClamp(x.score)+'/10</div>'+(x.good?'<div class="muted" style="margin-top:4px">좋은 점 · '+esc(x.good)+'</div>':'')+(x.risk?'<div class="muted" style="margin-top:3px">위험 · '+esc(x.risk)+'</div>':'')+'</div>').join('');
 modal('<h2>문제 해결 · 5단계</h2><div class="muted" style="margin:-4px 0 12px">'+esc(smartProblemDate(r.updatedAt||r.ts))+'</div>'+smartProblemSection('1 · 언제 발생하나요?',r.when)+smartProblemSection('1 · 누가 관련되어 있나요?',r.who)+smartProblemSection('1 · 무슨 일이 일어나나요?',r.what)+smartProblemSection('1 · 생각과 감정',r.thoughts)+'<div class="card"><h3>2·3 · 브레인스토밍과 평가</h3>'+(evals||'<span class="muted">작성하지 않음</span>')+'</div>'+smartProblemSection('4 · 선택한 전략',smartProblemStrategyLabel(r))+smartProblemSection('5 · 실행 계획',r.plan)+smartProblemSection('시작 날짜·장소',[r.start,r.place].filter(Boolean).join(' · '))+smartProblemSection('필요한 것·도움',r.needs)+smartProblemSection('실행 후 결과 점검',r.review)+'<button class="btn sec" id="ps-edit">수정</button><div style="height:8px"></div><button class="btn bad" id="ps-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
 $('#ps-edit').onclick=()=>openSmartProblemEditor(r);$('#ps-delete').onclick=()=>{if(!confirm('이 문제 해결 기록을 삭제할까요?'))return;S.smartWorks=(Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>!(x&&x.id===r.id));save();closeModal();drawSmartProblemSolving();toast('문제 해결 기록을 삭제했습니다.');};
}

'''
s=s.replace(fn_anchor,block+fn_anchor,1)

# Service worker version/cache only; reminder engine is untouched.
assert "const APP_VERSION = 'V8.2.16';" in w
assert "const V = 'ohg-v8216-smart-thinking-styles';" in w
w=w.replace("const APP_VERSION = 'V8.2.16';","const APP_VERSION = 'V8.2.17';",1)
w=w.replace("const V = 'ohg-v8216-smart-thinking-styles';","const V = 'ohg-v8217-smart-problem-solving';",1)

idx.write_text(s,encoding='utf-8'); sw.write_text(w,encoding='utf-8')
print('V8.2.17 SMART problem solving patch applied')
