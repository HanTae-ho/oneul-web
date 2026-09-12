from pathlib import Path
import json


def replace_once(text, old, new, label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 occurrence, got {n}')
    return text.replace(old,new,1)

# index.html: version, direct entry, status, help/manual copy.
p=Path('index.html'); s=p.read_text(encoding='utf-8')
s=replace_once(s,"const BUILD='V9.0.16';","const BUILD='V9.0.17';",'BUILD')
s=replace_once(s,'<!-- ══════════ 의미 돌아보기 V9.0.16 · 하루 한 장 + 기록 다시보기 + 의미회복 간편점검 ══════════','<!-- ══════════ 의미 돌아보기 V9.0.17 · 하루 한 장 + 기록 다시보기 + 의미회복 간편점검 UX ══════════','meaning comment')
old='''    <button class="toolcard" id="tool-meaning">\n      <span class="ic" data-ico="sprout"></span><span class="b"><b>의미 돌아보기</b><span id="tool-meaning-s">오늘의 경험에서 나에게 중요한 것을 돌아보기</span></span><span class="go">열기</span>\n    </button>'''
new=old+'''\n    <button class="toolcard" id="tool-meaning-check-direct" style="margin-top:9px" onclick="openMeaningCheckDirect()">\n      <span class="ic" data-ico="check"></span><span class="b"><b>의미점검 바로하기</b><span id="tool-meaning-check-s">10문항으로 내 의미의 흐름을 짧게 점검하기</span></span><span class="go">열기</span>\n    </button>'''
s=replace_once(s,old,new,'direct meaning check card')
old='''  const mnb=$('#tool-meaning'), mns=$('#tool-meaning-s');\n  if(mnb) mnb.style.display=famMode()?'none':'flex';\n  if(mns && !famMode()){\n    const todayMeaning=(S.wbDays&&typeof S.wbDays==='object')?S.wbDays[ymd(new Date())]:null;\n    mns.textContent=todayMeaning?'오늘 기록이 있습니다 · 다시 돌아보기':'오늘의 경험에서 나에게 중요한 것을 돌아보기';\n  }'''
new=old+'''\n  const mcb=$('#tool-meaning-check-direct'), mcs=$('#tool-meaning-check-s');\n  if(mcb) mcb.style.display=famMode()?'none':'flex';\n  if(mcs && !famMode()){\n    const d=ymd(new Date()), checks=Array.isArray(S.meaningChecks)?S.meaningChecks:[], todayCheck=checks.find(x=>x&&x.d===d), draft=S.meaningCheckDraft&&Array.isArray(S.meaningCheckDraft.answers)?S.meaningCheckDraft:null;\n    const done=draft?draft.answers.filter(v=>Number.isInteger(v)&&v>=0&&v<=4).length:0;\n    mcs.textContent=draft?('작성 중 '+done+'/10문항 · 이어서 하기'):(todayCheck?('오늘 결과 '+Number(todayCheck.total||0)+'/40 · 결과 보기'):(checks.length?'10문항 점검 · 이전 결과와 비교':'10문항으로 내 의미의 흐름을 짧게 점검하기'));\n  }'''
s=replace_once(s,old,new,'tools meaning check status')
old='''<details class="faq"><summary>의미 돌아보기는 무엇인가요?</summary><div class="faq-a"><p><b>회복도구 → 실천하기 → 의미 돌아보기</b>에서 세 가지를 사용할 수 있습니다. <b>오늘 돌아보기</b>는 공허감·아팠던 것·남아 있던 힘·내가 선택하거나 지킨 것을 짧게 기록하고, <b>지난 기록</b>은 기록에서 보인 힘과 지킨 가치, 같은 날짜의 충동기록을 함께 돌아봅니다. <b>의미점검</b>은 10문항의 의미회복 간편점검으로 이전의 나와 변화를 확인합니다. 직접 적은 글은 자동 분류하지 않으며 모든 기록은 현재 기기에만 저장됩니다. 이 기능은 당사자 모드에서만 사용합니다.</p><button class="btn ghost sm faq-go" type="button" onclick="go('meaning')">의미 돌아보기 열기</button></div></details>'''
new='''<details class="faq"><summary>의미 돌아보기는 무엇인가요?</summary><div class="faq-a"><p><b>회복도구 → 실천하기 → 의미 돌아보기</b>에서 오늘 돌아보기와 지난 기록을 사용할 수 있습니다. <b>의미회복 간편점검</b>은 같은 화면의 의미점검 탭에서도 할 수 있고, <b>회복도구 → 실천하기 → 의미점검 바로하기</b>로 들어가면 오늘 의미기록의 보기·수정 절차를 거치지 않고 곧바로 점검할 수 있습니다. 의미점검의 작성 중 답변은 임시저장되고, 10문항 뒤 <b>결과 저장</b>을 눌러야 완료기록으로 저장됩니다. 모든 기록은 현재 기기에만 저장됩니다.</p><button class="btn ghost sm faq-go" type="button" onclick="go('meaning')">의미 돌아보기 열기</button><button class="btn ghost sm faq-go" type="button" onclick="openMeaningCheckDirect()">의미점검 바로하기</button></div></details>'''
s=replace_once(s,old,new,'meaning FAQ')
old='''<details class="faq"><summary>의미회복 간편점검은 MIL 검사인가요?</summary><div class="faq-a"><p>아닙니다. <b>MIL-II의 자기인식·수용, 희망, 책임, 사랑, 자기초월, 관계, 자기만족, 헌신이라는 구성개념을 참고</b>해 오늘 한 걸음에서 새로 만든 10문항 자기점검입니다. 원 MIL-II 문항이나 원채점체계를 사용하지 않으며 진단·위험판정도 하지 않습니다. 0~4로 답한 결과는 같은 방식으로 응답한 <b>내 이전 기록과의 변화</b>를 볼 때만 참고하세요.</p></div></details>'''
new='''<details class="faq"><summary>의미회복 간편점검은 MIL 검사인가요?</summary><div class="faq-a"><p>아닙니다. <b>MIL-II의 자기인식·수용, 희망, 책임, 사랑, 자기초월, 관계, 자기만족, 헌신이라는 구성개념을 참고</b>해 오늘 한 걸음에서 새로 만든 10문항 자기점검입니다. 원 MIL-II 문항이나 원채점체계를 사용하지 않으며 진단·위험판정도 하지 않습니다. 저장한 결과는 <b>의미점검 → 점검 기록</b>에서 날짜별 총점과 4개 영역, 이전 기록과의 변화를 다시 볼 수 있습니다. 같은 날 다시 점검해 결과를 저장하면 그날의 완료결과 하나를 새 결과로 교체합니다.</p><button class="btn ghost sm faq-go" type="button" onclick="openMeaningCheckDirect()">의미점검 바로하기</button></div></details>'''
s=replace_once(s,old,new,'meaning check FAQ')
old='<p style="margin-top:8px"><b>실천하기</b> — 의미 돌아보기(오늘 돌아보기 · 지난 기록 · 의미회복 간편점검), 12단계 점검, 회복 실천도구, 충동일기, 미래의 나에게 등을 사용합니다. 가족·보호자 모드에서는 가족을 위한 도구 중심으로 구성이 달라집니다.</p>'
new='<p style="margin-top:8px"><b>실천하기</b> — 의미 돌아보기(오늘 돌아보기 · 지난 기록), 의미점검 바로하기(점검하기 · 점검 기록), 12단계 점검, 회복 실천도구, 충동일기, 미래의 나에게 등을 사용합니다. 의미점검은 작성 중 답변과 완료결과를 구분하며, 완료결과는 점검 기록에서 다시 볼 수 있습니다. 가족·보호자 모드에서는 가족을 위한 도구 중심으로 구성이 달라집니다.</p>'
s=replace_once(s,old,new,'manual tools section')
p.write_text(s,encoding='utf-8')

# meaning-check-feature.js: preserve 10 questions/scoring, replace access/history/save UX.
mc=r'''/* 오늘 한 걸음 V9.0.17 — 3단계 의미회복 간편점검 UX
   MIL-II의 8개 구성개념을 참고하되 원문항·원채점체계를 복제하지 않은 앱 독자 자기점검입니다.
   진단·위험판정·사람 간 비교를 하지 않고, 같은 사용자의 이전 응답과 변화만 참고합니다. */
const MCQ=[
  {id:'q1',axis:'self',text:'요즘 나는 내 상태와 마음을 비교적 솔직하게 알아차리고 받아들일 수 있다.'},
  {id:'q2',axis:'future',text:'앞으로의 삶에서 기대해 볼 만한 것이 있다고 느낀다.'},
  {id:'q3',axis:'choice',text:'오늘 내가 맡아야 할 몫이나 책임을 하나씩 해낼 수 있다고 느낀다.'},
  {id:'q4',axis:'relation',text:'나를 아끼거나 내가 아끼는 사람과의 관계에서 힘을 얻을 수 있다.'},
  {id:'q5',axis:'relation',text:'내 어려움을 넘어 다른 사람이나 더 큰 가치를 위해 할 수 있는 일이 있다고 느낀다.'},
  {id:'q6',axis:'relation',text:'나는 적어도 한 사람 또는 한 공동체와 연결되어 있다고 느낀다.'},
  {id:'q7',axis:'self',text:'완벽하지 않아도 지금의 나에게 괜찮은 부분이 있다고 느낀다.'},
  {id:'q8',axis:'future',text:'내게 중요하다고 생각하는 것을 위해 꾸준히 힘써볼 마음이 있다.'},
  {id:'q9',axis:'choice',text:'상황을 모두 바꿀 수 없어도 내가 선택할 태도나 행동은 남아 있다고 느낀다.'},
  {id:'q10',axis:'future',text:'오늘 또는 가까운 시일 안에 삶을 의미 있게 만드는 작은 행동을 하나는 할 수 있다고 느낀다.'}
];
const MC_AXIS={self:'나를 보는 힘',future:'앞으로 향하는 힘',choice:'책임·선택',relation:'관계·넘어섬'};
let mcPanelMode='check';
function mcState(){if(!Array.isArray(S.meaningChecks))S.meaningChecks=[];if(S.meaningCheckDraft&&(typeof S.meaningCheckDraft!=='object'||Array.isArray(S.meaningCheckDraft)))S.meaningCheckDraft=null;return S;}
function mcRecords(){mcState();return S.meaningChecks.filter(x=>x&&x.d&&Array.isArray(x.answers)&&x.answers.length===MCQ.length).slice().sort((a,b)=>String(b.d).localeCompare(String(a.d))||Number(b.ts||0)-Number(a.ts||0));}
function mcRecordByDate(d){return mcRecords().find(x=>x.d===d)||null;}
function mcPreviousRecord(rec){const rows=mcRecords(),i=rows.findIndex(x=>x.d===rec.d);return i>=0?(rows[i+1]||null):(rows.find(x=>String(x.d)<String(rec.d))||null);}
function mcNewDraft(){S.meaningCheckDraft={startedAt:Date.now(),answers:Array(MCQ.length).fill(null)};save();return S.meaningCheckDraft;}
function mcDraft(){mcState();const d=S.meaningCheckDraft;if(!d||!Array.isArray(d.answers)||d.answers.length!==MCQ.length)return null;d.answers=d.answers.map(v=>Number.isInteger(v)&&v>=0&&v<=4?v:null);return d;}
function mcScore(a){return a.reduce((n,v)=>n+Number(v||0),0);}
function mcAxes(a){const sums={},counts={};MCQ.forEach((q,i)=>{const v=Number(a[i]||0);sums[q.axis]=(sums[q.axis]||0)+v;counts[q.axis]=(counts[q.axis]||0)+1;});const out={};Object.keys(MC_AXIS).forEach(k=>out[k]=counts[k]?Math.round((sums[k]/counts[k])*10)/10:0);return out;}
function mcDateLabel(d){return typeof wbDateLabel==='function'?wbDateLabel(d):String(d||'');}
function mcComparison(rec){const prev=mcPreviousRecord(rec);if(!prev)return '<p class="tiny" style="margin:8px 0 0">이 날짜보다 앞선 저장 결과가 없습니다.</p>';const diff=Number(rec.total)-Number(prev.total),sign=diff>0?'+':'';return '<p class="tiny" style="margin:8px 0 0">이전 '+esc(mcDateLabel(prev.d))+' '+Number(prev.total)+'/40 → 이 기록 '+Number(rec.total)+'/40 · 차이 '+sign+diff+'</p>';}
function mcResultCard(rec,complete){const axes=rec.domains&&typeof rec.domains==='object'?rec.domains:mcAxes(rec.answers),axisHtml=Object.keys(MC_AXIS).map(k=>'<span class="badge" style="margin:3px 5px 3px 0">'+esc(MC_AXIS[k])+' '+Number(axes[k]||0).toFixed(1)+'/4</span>').join('');return (complete?'<div class="note" style="margin-bottom:12px"><b>결과 저장 완료</b><br><span class="tiny">완료결과가 이 기기의 점검 기록에 저장되었습니다.</span></div>':'')+'<div class="card"><div class="sp"><div><b>'+esc(mcDateLabel(rec.d))+'</b><div class="tiny">의미회복 간편점검 · 저장된 결과</div></div><b style="font-size:20px">'+Number(rec.total)+'/40</b></div>'+mcComparison(rec)+'<div style="margin-top:10px">'+axisHtml+'</div><p class="tiny" style="margin:10px 0 0">점수에 정상·위험 기준은 없습니다. 같은 방식으로 응답한 내 기록의 흐름만 참고하세요.</p></div>';}
function mcHistoryListHtml(){const rows=mcRecords();if(!rows.length)return '<div class="empty">아직 저장한 의미점검 결과가 없습니다.</div>';return '<div class="card"><h3>저장한 점검 기록</h3><p class="tiny" style="margin:0 0 6px">날짜를 골라 총점·4개 영역·이전 결과와의 변화를 다시 볼 수 있습니다.</p>'+rows.slice(0,20).map(r=>'<div class="sp" style="padding:9px 0;border-top:1px solid var(--line);gap:8px"><span class="tiny" style="flex:1">'+esc(mcDateLabel(r.d))+'</span><b>'+Number(r.total)+'/40</b><button class="btn ghost sm" type="button" data-mc-result-date="'+esc(r.d)+'" style="width:auto;margin:0">보기</button></div>').join('')+'</div>';}
function mcBindHistoryButtons(host){host.querySelectorAll('[data-mc-result-date]').forEach(b=>b.onclick=()=>mcShowResult(b.dataset.mcResultDate));}
function mcShowResult(d){const rec=mcRecordByDate(d);if(!rec){toast('저장된 결과를 찾지 못했습니다.');return;}modal('<h2>의미점검 결과</h2>'+mcResultCard(rec,false)+'<button class="btn ghost" type="button" onclick="closeModal()">닫기</button>');}
function mcShell(host,bodyHtml){host.innerHTML='<div class="mn-view-tabs" id="mc-view-tabs"><button type="button" data-mc-view="check" class="'+(mcPanelMode==='check'?'on':'')+'">점검하기</button><button type="button" data-mc-view="history" class="'+(mcPanelMode==='history'?'on':'')+'">점검 기록</button></div><div id="mc-body">'+(bodyHtml||'')+'</div>';host.querySelectorAll('[data-mc-view]').forEach(b=>b.onclick=()=>{mcPanelMode=b.dataset.mcView==='history'?'history':'check';drawMeaningCheck();});mcBindHistoryButtons(host);return $('#mc-body');}
function mcUpdateProgress(){const d=mcDraft(),done=d?d.answers.filter(v=>Number.isInteger(v)).length:0,p=$('#mc-progress'),saveBtn=$('#mc-save');if(p)p.textContent=done+' / '+MCQ.length+'문항 답함 · 현재 답변은 임시저장됩니다. [결과 저장] 전에는 완료기록이 아닙니다.';if(saveBtn)saveBtn.disabled=done!==MCQ.length;}
function mcCommitResult(d){const rec={d:wbToday(),ts:Date.now(),answers:d.answers.slice(),total:mcScore(d.answers),domains:mcAxes(d.answers)},s=mcState(),idx=s.meaningChecks.findIndex(x=>x&&x.d===rec.d),replaced=idx>=0;if(replaced)s.meaningChecks[idx]=rec;else s.meaningChecks.push(rec);s.meaningCheckDraft=null;save();mcPanelMode='check';toast(replaced?'오늘 점검 결과를 새 결과로 교체해 저장했습니다.':'의미회복 점검 결과를 저장했습니다.');drawMeaningCheck(true);}
function mcRenderQuestions(host,draft){const today=mcRecordByDate(wbToday()),body=mcShell(host,'');body.innerHTML='<div class="note" style="margin-bottom:12px"><b>의미회복 간편점검 · 10문항</b><br>최근의 나를 기준으로 답해보세요. 0은 전혀 아니다, 4는 매우 그렇다입니다.<br><span class="tiny">답을 고를 때마다 <b>작성 중 답변만 임시저장</b>됩니다. 완료결과는 아래 <b>결과 저장</b>을 눌러야 저장됩니다.</span>'+(today?'<br><span class="tiny"><b>오늘 저장된 결과가 이미 있습니다.</b> 이 답변을 결과 저장하면 오늘 완료결과 하나를 새 결과로 교체합니다.</span>':'')+'</div><p class="tiny" id="mc-progress" style="margin:0 0 10px"></p><div id="mc-questions"></div><button class="btn" id="mc-save" type="button">결과 저장</button><div style="height:8px"></div><button class="btn ghost sm" id="mc-reset" type="button">처음부터 다시 답하기</button><p class="tiny" style="margin:10px 0 0">0 전혀 아니다 · 1 별로 아니다 · 2 보통이다 · 3 대체로 그렇다 · 4 매우 그렇다</p>';
 const box=$('#mc-questions');MCQ.forEach((q,i)=>{const card=document.createElement('div');card.className='card';card.innerHTML='<h3>'+(i+1)+'. '+esc(q.text)+'</h3><div class="mn-empty mc-scale" data-i="'+i+'"></div>';const scale=card.querySelector('.mc-scale');[0,1,2,3,4].forEach(v=>{const b=document.createElement('button');b.type='button';b.className=draft.answers[i]===v?'on':'';b.textContent=String(v);b.dataset.v=String(v);b.onclick=()=>{draft.answers[i]=v;save();scale.querySelectorAll('button').forEach(x=>x.classList.toggle('on',Number(x.dataset.v)===v));mcUpdateProgress();};scale.appendChild(b);});box.appendChild(card);});
 $('#mc-save').onclick=()=>{const d=mcDraft();if(!d||d.answers.some(v=>!Number.isInteger(v))){toast('10문항을 모두 답해주세요.');return;}mcCommitResult(d);};
 $('#mc-reset').onclick=()=>{S.meaningCheckDraft=null;mcNewDraft();drawMeaningCheck();};mcUpdateProgress();}
function mcBeginRecheck(){const today=mcRecordByDate(wbToday());if(!today){mcNewDraft();drawMeaningCheck();return;}modal('<h2>오늘 다시 점검할까요?</h2><p class="muted" style="margin:6px 0 14px">지금 저장된 오늘 결과는 그대로 유지됩니다. 새로 10문항을 모두 답하고 <b>결과 저장</b>을 누를 때만 오늘 결과가 새 결과로 교체됩니다.</p><button class="btn" id="mc-recheck-yes" type="button">다시 점검 시작</button><div style="height:8px"></div><button class="btn ghost" type="button" onclick="closeModal()">그만두기</button>');$('#mc-recheck-yes').onclick=()=>{closeModal();mcNewDraft();drawMeaningCheck();};}
function drawMeaningCheck(justSaved){const host=$('#mn-view-check');if(!host)return;if(typeof famMode==='function'&&famMode()){host.innerHTML='<div class="empty">의미회복 간편점검은 당사자 모드에서 사용합니다.</div>';return;}mcState();if(mcPanelMode==='history'){const d=mcDraft(),done=d?d.answers.filter(v=>Number.isInteger(v)).length:0;mcShell(host,(d?'<div class="note" style="margin-bottom:12px"><b>작성 중인 답변 '+done+'/10문항이 임시저장되어 있습니다.</b><br><span class="tiny">점검하기 탭으로 돌아가 이어서 답할 수 있습니다.</span></div>':'')+mcHistoryListHtml());mcBindHistoryButtons(host);return;}const draft=mcDraft();if(draft){mcRenderQuestions(host,draft);return;}const today=mcRecordByDate(wbToday());if(today){const body=mcShell(host,'');body.innerHTML=mcResultCard(today,!!justSaved)+'<button class="btn ghost" id="mc-history-open" type="button">점검 기록 보기</button><div style="height:8px"></div><button class="btn ghost" id="mc-recheck" type="button">오늘 다시 점검하기</button>';$('#mc-history-open').onclick=()=>{mcPanelMode='history';drawMeaningCheck();};$('#mc-recheck').onclick=mcBeginRecheck;return;}const body=mcShell(host,'');body.innerHTML='<div class="note" style="margin-bottom:12px"><b>내 의미의 흐름을 짧게 점검합니다.</b><br>10문항, 약 1~2분입니다. 점수로 나를 판정하지 않고 이전의 나와 비교합니다.</div><div class="card"><h3>무엇을 살펴보나요?</h3><p class="muted" style="margin:0">나를 보는 힘 · 앞으로 향하는 힘 · 책임과 선택 · 관계와 나를 넘어서는 가치를 함께 돌아봅니다.</p><p class="tiny" style="margin:8px 0 0">MIL-II의 자기인식·수용, 희망, 책임, 사랑, 자기초월, 관계, 자기만족, 헌신 구성개념을 참고했지만 문항과 채점은 오늘 한 걸음에서 새로 구성했습니다.</p></div><button class="btn" id="mc-start" type="button">점검 시작하기</button>';$('#mc-start').onclick=()=>{mcNewDraft();drawMeaningCheck();};}

/* 기존 의미 돌아보기는 유지하고, 의미점검 직접 진입만 오늘 기록 팝업을 건너뜁니다. */
const setMeaningViewV9016=setMeaningView;
setMeaningView=function(v){if(v!=='check'){setMeaningViewV9016(v);const check=$('#mn-view-check');if(check)check.classList.add('hide');return;}mnView='check';const today=$('#mn-view-today'),history=$('#mn-view-history'),check=$('#mn-view-check');if(today)today.classList.add('hide');if(history)history.classList.add('hide');if(check)check.classList.remove('hide');$$('[data-mn-view]').forEach(b=>b.classList.toggle('on',b.dataset.mnView==='check'));drawMeaningCheck();const view=$('#view');if(view)view.scrollTop=0;};
const drawMeaningV9016=drawMeaning;
drawMeaning=function(opts){const direct=!!window.__meaningDirectCheck;if(direct)window.__meaningDirectCheck=false;drawMeaningV9016(direct?{skipExistingPrompt:true}:opts);if(direct){mcPanelMode='check';setMeaningView('check');}};
function openMeaningCheckDirect(){mcPanelMode='check';window.__meaningDirectCheck=true;go('meaning');}
'''
Path('meaning-check-feature.js').write_text(mc,encoding='utf-8')

# Service worker + release metadata.
p=Path('sw.js'); s=p.read_text(encoding='utf-8')
s=replace_once(s,"const APP_VERSION = 'V9.0.16';","const APP_VERSION = 'V9.0.17';",'sw app version')
s=replace_once(s,"const V = 'ohg-v9016-meaning-quick-check-r1';","const V = 'ohg-v9017-meaning-check-ux-r1';",'sw cache')
p.write_text(s,encoding='utf-8')
Path('latest-release.json').write_text(json.dumps({'version':'V9.0.17','versionCode':912,'apk':'https://github.com/HanTae-ho/oneul-web/releases/download/v9.0.17-test/oneul-v9.0.17.apk','release':'https://github.com/HanTae-ho/oneul-web/releases/tag/v9.0.17-test'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Regression checks: update phase-3 assertions and version markers.
p=Path('verify-meaning.js'); s=p.read_text(encoding='utf-8')
s=replace_once(s,"ok(/meaningCheckDraft/.test(checkFeature)&&/답할 때마다 이 기기에 자동 저장됩니다/.test(checkFeature)&&/save\\(\\)/.test(checkFeature),'중간답변 자동 저장·이어쓰기');","ok(/meaningCheckDraft/.test(checkFeature)&&/현재 답변은 임시저장됩니다/.test(checkFeature)&&/결과 저장.*완료기록/.test(checkFeature)&&/save\\(\\)/.test(checkFeature),'중간답변 임시저장과 완료결과 저장 구분');",'verify draft wording')
s=replace_once(s,"ok(/function mcComparison\\(rec\\)/.test(checkFeature)&&/이전 .*이번/.test(checkFeature),'이전 나와 변화 비교');","ok(/function mcPreviousRecord\\(rec\\)/.test(checkFeature)&&/function mcComparison\\(rec\\)/.test(checkFeature)&&/이전 .*이 기록/.test(checkFeature),'과거 날짜 기준 이전 나와 변화 비교');",'verify comparison')
s=replace_once(s,"ok(index.includes('의미회복 간편점검은 MIL 검사인가요?')&&index.includes('원 MIL-II 문항이나 원채점체계를 사용하지 않으며'),'사용설명서에 3단계 성격·한계 반영');","ok(index.includes('의미회복 간편점검은 MIL 검사인가요?')&&index.includes('원 MIL-II 문항이나 원채점체계를 사용하지 않으며')&&index.includes('의미점검 → 점검 기록'),'사용설명서에 3단계 성격·저장결과 조회 반영');",'verify help')
s=replace_once(s,"ok(index.includes('의미 돌아보기(오늘 돌아보기 · 지난 기록 · 의미회복 간편점검)'),'전체 사용설명서 회복도구 항목 현행화');","ok(index.includes('의미점검 바로하기(점검하기 · 점검 기록)'),'전체 사용설명서 의미점검 독립 진입 현행화');\nok(index.includes('id=\"tool-meaning-check-direct\"')&&/function openMeaningCheckDirect\\(\\)/.test(checkFeature)&&/__meaningDirectCheck/.test(checkFeature)&&/skipExistingPrompt:true/.test(checkFeature),'의미점검 바로하기는 오늘 의미기록 팝업 우회');\nok(/data-mc-view=\"check\"/.test(checkFeature)&&/data-mc-view=\"history\"/.test(checkFeature),'의미점검 점검하기·점검 기록 분리');\nok(/data-mc-result-date/.test(checkFeature)&&/function mcShowResult\\(d\\)/.test(checkFeature)&&/저장한 점검 기록/.test(checkFeature),'과거 의미점검 결과 상세조회');\nok(/결과 저장 완료/.test(checkFeature)&&/저장된 결과/.test(checkFeature),'결과 저장 완료 상태 명확화');\nok(/오늘 저장된 결과가 이미 있습니다/.test(checkFeature)&&/새 결과로 교체/.test(checkFeature)&&/function mcBeginRecheck\\(\\)/.test(checkFeature),'같은 날 재점검 교체 규칙 안내');",'verify direct/history')
s=replace_once(s,"console.log('\\\\nV9.0.16 의미 돌아보기·기록 다시보기·의미회복 간편점검 회귀검증 통과');","console.log('\\\\nV9.0.17 의미 돌아보기·기록 다시보기·의미회복 간편점검 UX 회귀검증 통과');",'verify version footer')
p.write_text(s,encoding='utf-8')

p=Path('verify.js'); s=p.read_text(encoding='utf-8')
s=replace_once(s,"if(!index.includes(\"const BUILD='V9.0.16';\")) throw new Error('V9.0.16 BUILD 불일치');","if(!index.includes(\"const BUILD='V9.0.17';\")) throw new Error('V9.0.17 BUILD 불일치');",'verify.js BUILD')
p.write_text(s,encoding='utf-8')
