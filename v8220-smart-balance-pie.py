from pathlib import Path

idx=Path('index.html'); sw=Path('sw.js')
s=idx.read_text(encoding='utf-8'); w=sw.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 match, found {n}')
    s=s.replace(old,new,1)

once("const BUILD = 'V8.2.19';","const BUILD = 'V8.2.20';",'BUILD')

page='''<!-- ══════════ SMART Recovery · Lifestyle Balance Pie V8.2.20 ══════════ -->
<section class="pg" id="p-smart-balance-pie">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">라이프스타일 밸런스 파이</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back onclick="appBack('smart-tools')">← SMART 실천도구</button>
  </div>
  <div class="note" style="margin-bottom:12px">
    내 삶에서 중요한 영역을 나누고 각 영역의 현재 만족도를 <b>0~10</b>으로 표시해 전체적인 균형을 살펴봅니다. 바깥쪽은 매우 만족스러운 상태(10), 중심은 매우 불만족스러운 상태(0)로 봅니다. SMART Recovery 번역본의 <b>Lifestyle Balance Pie</b>를 모바일에 맞게 옮겼으며, 내용은 <b>이 기기에만 저장</b>됩니다.
  </div>
  <div id="smart-balance-role-note"></div>
  <button class="btn sec" id="smart-balance-new">+ 밸런스 파이 새로 작성하기</button>
  <div id="smart-balance-list" style="margin-top:12px"></div>
</section>

'''
marker='<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->'
once(marker,page+marker,'balance page marker')

once("    'smart-problem-solving':'문제 해결 · 5단계'\n", "    'smart-problem-solving':'문제 해결 · 5단계',\n    'smart-balance-pie':'라이프스타일 밸런스 파이'\n", 'back label')
once("'smart-thinking-styles':'smart-thinking-styles', 'smart-problem-solving':'smart-problem-solving'", "'smart-thinking-styles':'smart-thinking-styles', 'smart-problem-solving':'smart-problem-solving', 'smart-balance-pie':'smart-balance-pie'", 'back fallback')
once("p === 'smart-thinking-styles' || p === 'smart-problem-solving' || p === 'smart-tools'", "p === 'smart-thinking-styles' || p === 'smart-problem-solving' || p === 'smart-balance-pie' || p === 'smart-tools'", 'tab route')
once("  if(p === 'smart-problem-solving') drawSmartProblemSolving();\n", "  if(p === 'smart-problem-solving') drawSmartProblemSolving();\n  if(p === 'smart-balance-pie') drawSmartBalancePie();\n", 'draw route')

old_p4="  h+='<div class=\"card\"><h3>Point 4 · 균형 잡힌 삶 살기</h3><p class=\"muted\" style=\"margin:-4px 0 0\">생활 균형 · 가치에 맞는 활동 · 목표와 주간계획 도구를 순차적으로 추가할 예정입니다.</p><div class=\"tiny\" style=\"margin-top:8px\">준비 중</div></div>';"
new_p4="  h+='<div class=\"card\"><h3>Point 4 · 균형 잡힌 삶 살기</h3><p class=\"muted\" style=\"margin:-4px 0 11px\">삶의 여러 영역을 살펴보고, 가치에 맞는 활동과 목표로 균형을 만들어갑니다.</p>'+smartToolButton('라이프스타일 밸런스 파이','삶의 영역별 만족도 0~10 → 먼저 돌볼 영역과 작은 변화 찾기','smart-balance-pie','sprout')+'</div>';"
once(old_p4,new_p4,'Point4 hub')

funcs=r'''/* ── SMART Recovery · Lifestyle Balance Pie V8.2.20 ──
   번역본 Point 4의 Lifestyle Balance Pie: 삶의 영역을 정하고 0~10 만족도를 표시한 뒤
   전체 균형을 돌아보고 가장 먼저 돌볼 영역과 시작 행동을 정합니다. */
const SMART_BALANCE_DEFAULT_AREAS=['가족','친구','영성','연애·관계','건강','일','여가·레크리에이션','재정'];
function smartBalanceRecords(){return (Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(r=>r&&r.kind==='lifestyle-balance-pie'&&(r.role||'self')===(famMode()?'family':'self')).sort((a,b)=>(b.updatedAt||b.ts||0)-(a.updatedAt||a.ts||0));}
function smartBalanceClamp(v){v=parseInt(v,10);return Number.isFinite(v)?Math.max(0,Math.min(10,v)):0;}
function smartBalanceDate(ts){return smartProblemDate(ts);}
function smartBalanceWheel(areas){
 const rows=(Array.isArray(areas)?areas:[]).filter(x=>x&&x.name);if(rows.length<3)return '<div class="empty">삶의 영역을 3개 이상 남겨주세요.</div>';
 const cx=120,cy=120,R=88,n=rows.length;let spokes='',dots='',pts=[];
 for(let j=1;j<=5;j++){const rr=R*j/5;spokes+='<circle cx="'+cx+'" cy="'+cy+'" r="'+rr+'" fill="none" stroke="var(--line)" stroke-width="1"/>';}
 rows.forEach((a,i)=>{const ang=-Math.PI/2+(Math.PI*2*i/n),ox=cx+Math.cos(ang)*R,oy=cy+Math.sin(ang)*R,r=R*smartBalanceClamp(a.score)/10,x=cx+Math.cos(ang)*r,y=cy+Math.sin(ang)*r;spokes+='<line x1="'+cx+'" y1="'+cy+'" x2="'+ox.toFixed(2)+'" y2="'+oy.toFixed(2)+'" stroke="var(--line2)" stroke-width="1"/>';pts.push(x.toFixed(2)+','+y.toFixed(2));dots+='<circle cx="'+x.toFixed(2)+'" cy="'+y.toFixed(2)+'" r="3.5" fill="var(--acc)"/>';});
 const poly='<polygon points="'+pts.join(' ')+'" fill="var(--acc)" fill-opacity=".16" stroke="var(--acc)" stroke-width="2"/>';
 return '<div class="card"><div style="max-width:290px;margin:0 auto"><svg viewBox="0 0 240 240" width="100%" role="img" aria-label="라이프스타일 밸런스 파이">'+spokes+poly+dots+'<circle cx="120" cy="120" r="3" fill="var(--ink2)"/></svg></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:5px 10px;margin-top:5px">'+rows.map(a=>'<div class="tiny"><b>'+esc(a.name)+'</b> · '+smartBalanceClamp(a.score)+'/10</div>').join('')+'</div></div>';
}
function drawSmartBalancePie(){
 const list=$('#smart-balance-list'),rn=$('#smart-balance-role-note'),add=$('#smart-balance-new');if(!list||!add)return;
 if(rn)rn.innerHTML=famMode()?'<div class="note" style="margin-bottom:12px"><b>가족도 내 삶의 균형을 봅니다.</b><br>상대의 음주·도박·약물사용이나 회복 상태를 점수 매기는 도구가 아닙니다. 가족인 나 자신의 관계·건강·일·여가·재정 등 삶의 영역을 살펴봅니다.</div>':'';
 add.onclick=()=>openSmartBalanceEditor(null);
 const rows=smartBalanceRecords();
 if(!rows.length){list.innerHTML='<div class="card"><b>아직 저장한 밸런스 파이가 없습니다.</b><p class="muted" style="margin:5px 0 0">삶의 영역을 나누고 지금의 만족도를 0~10으로 표시해보세요.</p></div>';return;}
 list.innerHTML='<div class="card"><h3>저장한 밸런스 파이 '+rows.length+'건</h3>'+rows.map(r=>'<div class="sp" style="gap:10px;padding:11px 0;border-top:1px solid var(--line)"><div style="min-width:0;flex:1"><div class="tiny">'+esc(smartBalanceDate(r.updatedAt||r.ts))+'</div><b style="display:block;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(r.focus||'라이프스타일 밸런스 파이')+'</b><div class="muted" style="margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(r.action||'삶의 균형을 돌아본 기록')+'</div></div><button class="tiny" style="color:var(--acc);font-weight:600" onclick="openSmartBalanceView(\''+esc(r.id)+'\')">보기</button></div>').join('')+'</div>';
}
function smartBalanceAreaRow(a,i){return '<div class="card tight" data-balance-row="'+i+'"><div class="sp" style="margin-bottom:8px"><b>'+esc(a.name)+'</b><button type="button" class="tiny" style="color:var(--bad);font-weight:600" data-balance-remove="'+i+'">빼기</button></div><div class="sp"><span class="tiny">현재 만족도</span><b data-balance-score-label="'+i+'">'+smartBalanceClamp(a.score)+' / 10</b></div><input type="range" min="0" max="10" value="'+smartBalanceClamp(a.score)+'" data-balance-score="'+i+'"><div class="axis"><span>0 · 매우 불만족</span><span>10 · 매우 만족</span></div></div>';}
function openSmartBalanceEditor(record){
 const r=record||{};let areas=(Array.isArray(r.areas)&&r.areas.length?r.areas:SMART_BALANCE_DEFAULT_AREAS.map(name=>({name,score:5}))).map(x=>({name:String(x.name||'').trim(),score:smartBalanceClamp(x.score)})).filter(x=>x.name);let focus=String(r.focus||'');
 const setAcc=(node,on)=>{if(!node)return;node.classList.toggle('on',!!on);const b=node.querySelector(':scope > .acc-h');if(b)b.setAttribute('aria-expanded',on?'true':'false');};
 const collectAreas=()=>{areas=areas.map((a,i)=>({name:a.name,score:smartBalanceClamp(($('[data-balance-score="'+i+'"]')||{}).value)}));return areas;};
 const renderPreview=()=>{collectAreas();const p=$('#balance-preview');if(p)p.innerHTML=smartBalanceWheel(areas);};
 const renderFocus=()=>{collectAreas();const sel=$('#balance-focus');if(!sel)return;sel.innerHTML='<option value="">먼저 돌볼 영역 선택</option>'+areas.map(a=>'<option value="'+esc(a.name)+'"'+(a.name===focus?' selected':'')+'>'+esc(a.name)+'</option>').join('');};
 const renderAreas=()=>{const box=$('#balance-areas');if(!box)return;box.innerHTML=areas.map(smartBalanceAreaRow).join('');box.querySelectorAll('[data-balance-score]').forEach(inp=>inp.oninput=()=>{const l=box.querySelector('[data-balance-score-label="'+inp.dataset.balanceScore+'"]');if(l)l.textContent=inp.value+' / 10';});box.querySelectorAll('[data-balance-remove]').forEach(b=>b.onclick=()=>{if(areas.length<=3){toast('삶의 영역을 3개 이상 남겨주세요.');return;}collectAreas();const gone=areas.splice(+b.dataset.balanceRemove,1)[0];if(gone&&focus===gone.name)focus='';renderAreas();});};
 const openStep=(name,scroll)=>{if(name==='review')renderPreview();if(name==='focus')renderFocus();const root=$('#balance-editor');if(!root)return;root.querySelectorAll('[data-balance-step]').forEach(a=>setAcc(a,false));const target=root.querySelector('[data-balance-step="'+name+'"]');setAcc(target,true);if(scroll&&target)setTimeout(()=>target.scrollIntoView({behavior:'smooth',block:'start'}),30);};
 modal('<h2>'+(record?'밸런스 파이 수정':'라이프스타일 밸런스 파이')+'</h2><p class="muted" style="margin:5px 0 14px">전체 삶의 모습을 한꺼번에 완벽하게 바꾸려 하지 않습니다. 영역별 현재 상태를 보고, 가장 먼저 손이 가는 한 영역부터 시작합니다.</p><div id="balance-editor">'
 +'<div class="acc on" data-balance-step="areas"><button class="acc-h" type="button" data-balance-step-toggle="areas" aria-expanded="true"><div class="acc-n"><b>1 · 삶의 영역과 만족도</b><span>중요한 영역을 정하고 현재 만족도를 0~10으로 표시합니다.</span></div><svg class="acc-v" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg></button><div class="acc-b"><div id="balance-areas"></div><div class="card tight"><label>다른 삶의 영역 추가 <span class="tiny">(선택)</span></label><div style="display:grid;grid-template-columns:minmax(0,1fr) auto;gap:7px"><input id="balance-add-name" maxlength="30" placeholder="예: 공부, 지역사회, 취미"><button class="btn sec sm" type="button" id="balance-add" style="width:auto;margin:0">추가</button></div></div><button class="btn sec" type="button" id="balance-next-review">다음 · 파이 돌아보기</button></div></div>'
 +'<div class="acc" data-balance-step="review"><button class="acc-h" type="button" data-balance-step-toggle="review" aria-expanded="false"><div class="acc-n"><b>2 · 완성된 파이 돌아보기</b><span>전체 모양과 가치·우선순위, 더 필요한 영역을 살펴봅니다.</span></div><svg class="acc-v" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg></button><div class="acc-b"><div id="balance-preview"></div><div class="note" style="margin-bottom:10px"><b>번역본의 돌아보기 질문</b><br>나는 균형 잡힌 삶을 살고 있나요?<br>나의 참된 가치와 우선순위가 반영되어 있나요?<br>더 많은 관심이 필요한 영역이나 계속 미뤄진 꿈·욕망이 있나요?<br>어떤 영역에 더 관심을 주고, 어떤 영역에는 덜 집중해야 할까요?</div><label>파이를 보며 든 생각과 감정 <span class="tiny">(선택)</span></label><textarea id="balance-reflection" maxlength="900" placeholder="전체 모양을 보며 알아차린 점을 적어보세요.">'+esc(r.reflection||'')+'</textarea><button class="btn sec" type="button" id="balance-next-focus" style="margin-top:10px">다음 · 먼저 돌볼 영역</button></div></div>'
 +'<div class="acc" data-balance-step="focus"><button class="acc-h" type="button" data-balance-step-toggle="focus" aria-expanded="false"><div class="acc-n"><b>3 · 먼저 돌볼 영역과 작은 변화</b><span>가장 먼저 끌리는 한 영역을 고르고 시작 행동을 정합니다.</span></div><svg class="acc-v" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg></button><div class="acc-b"><div class="field"><label>가장 먼저 더 관심을 주고 싶은 영역</label><select id="balance-focus"></select></div><div class="field"><label>두려움이나 불편함 때문에 막히는 것이 있나요? <span class="tiny">(선택)</span></label><textarea id="balance-barrier" maxlength="600" placeholder="있다면 적어보세요.">'+esc(r.barrier||'')+'</textarea></div><div class="field"><label>균형을 위해 시작할 작은 행동</label><textarea id="balance-action" maxlength="700" placeholder="예: 이번 주 토요일 오전에 친구에게 연락해 함께 30분 걷기">'+esc(r.action||'')+'</textarea></div><div class="field"><label>언제부터 시작할까요? <span class="tiny">(선택)</span></label><input id="balance-start" type="date" value="'+esc(r.start||'')+'"></div></div></div></div><button class="btn" id="balance-save">'+(record?'수정 저장':'밸런스 파이 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
 renderAreas();
 $$('[data-balance-step-toggle]').forEach(b=>b.onclick=()=>{const target=b.closest('[data-balance-step]'),was=target.classList.contains('on');$('#balance-editor').querySelectorAll('[data-balance-step]').forEach(a=>setAcc(a,false));if(!was){setAcc(target,true);if(target.dataset.balanceStep==='review')renderPreview();if(target.dataset.balanceStep==='focus')renderFocus();}});
 $('#balance-add').onclick=()=>{collectAreas();const inp=$('#balance-add-name'),name=inp.value.trim();if(!name){toast('추가할 삶의 영역 이름을 적어주세요.');return;}if(areas.some(a=>a.name===name)){toast('이미 있는 영역입니다.');return;}if(areas.length>=10){toast('삶의 영역은 10개까지 사용할 수 있습니다.');return;}areas.push({name,score:5});inp.value='';renderAreas();setTimeout(()=>{const rs=$$('[data-balance-row]');if(rs.length)rs[rs.length-1].scrollIntoView({behavior:'smooth',block:'center'});},30);};
 $('#balance-next-review').onclick=()=>{collectAreas();if(areas.length<3){toast('삶의 영역을 3개 이상 남겨주세요.');return;}openStep('review',true);};
 $('#balance-next-focus').onclick=()=>openStep('focus',true);
 $('#balance-save').onclick=()=>{collectAreas();focus=$('#balance-focus').value;if(!focus){openStep('focus',true);toast('가장 먼저 돌볼 영역 하나를 선택해주세요.');return;}const action=$('#balance-action').value.trim();if(!action){openStep('focus',true);toast('그 영역에서 시작할 작은 행동을 적어주세요.');return;}const rec={id:record?record.id:('balance-'+Date.now()+'-'+Math.random().toString(36).slice(2,7)),kind:'lifestyle-balance-pie',role:famMode()?'family':'self',ts:record?(record.ts||Date.now()):Date.now(),updatedAt:Date.now(),areas:areas.map(a=>({name:a.name,score:smartBalanceClamp(a.score)})),reflection:$('#balance-reflection').value.trim(),focus,barrier:$('#balance-barrier').value.trim(),action,start:$('#balance-start').value};if(!Array.isArray(S.smartWorks))S.smartWorks=[];if(record){const i=S.smartWorks.findIndex(x=>x&&x.id===record.id);if(i>=0)S.smartWorks[i]=rec;else S.smartWorks.push(rec);}else S.smartWorks.push(rec);save();closeModal();drawSmartBalancePie();toast(record?'밸런스 파이를 수정했습니다.':'밸런스 파이를 저장했습니다.');};
}
function openSmartBalanceView(id){
 const r=smartBalanceRecords().find(x=>x.id===id);if(!r)return;const areas=Array.isArray(r.areas)?r.areas:[];
 const sec=(t,v)=>'<div class="card"><h3>'+esc(t)+'</h3><div style="white-space:pre-wrap">'+(String(v||'').trim()?esc(v):'<span class="muted">작성하지 않음</span>')+'</div></div>';
 modal('<h2>라이프스타일 밸런스 파이</h2><div class="muted" style="margin:-4px 0 12px">'+esc(smartBalanceDate(r.updatedAt||r.ts))+'</div>'+smartBalanceWheel(areas)+sec('파이를 보며 알아차린 점',r.reflection)+sec('먼저 돌볼 영역',r.focus)+sec('막히는 점',r.barrier)+sec('시작할 작은 행동',r.action)+sec('시작 날짜',r.start)+'<button class="btn sec" id="balance-edit">수정</button><div style="height:8px"></div><button class="btn bad" id="balance-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
 $('#balance-edit').onclick=()=>openSmartBalanceEditor(r);$('#balance-delete').onclick=()=>{if(!confirm('이 밸런스 파이 기록을 삭제할까요?'))return;S.smartWorks=(Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>!(x&&x.id===r.id));save();closeModal();drawSmartBalancePie();toast('밸런스 파이 기록을 삭제했습니다.');};
}

'''
once('function learningAction(type){',funcs+'function learningAction(type){','balance functions')
once("  if(type === 'smart-problem-solving'){ go('smart-problem-solving'); return; }\n", "  if(type === 'smart-problem-solving'){ go('smart-problem-solving'); return; }\n  if(type === 'smart-balance-pie'){ go('smart-balance-pie'); return; }\n", 'learning route')

for old,new,label in [
    ("const APP_VERSION = 'V8.2.19';","const APP_VERSION = 'V8.2.20';",'SW version'),
    ("const V = 'ohg-v8219-smart-problem-numbering';","const V = 'ohg-v8220-smart-balance-pie';",'SW cache')]:
    n=w.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 match, found {n}')
    w=w.replace(old,new,1)

if "const DATA_SCHEMA = 6;" not in s: raise SystemExit('DATA_SCHEMA changed unexpectedly')
idx.write_text(s,encoding='utf-8'); sw.write_text(w,encoding='utf-8')
print('V8.2.20 balance pie patch PASS')
