from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def once(old, new, name):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{name}: expected 1 match, got {n}')
    s = s.replace(old, new, 1)

once("const BUILD='V8.4';", "const BUILD='V8.5';", 'BUILD')

css = r'''

  /* V8.5 — 최근 4주 회복요약. 기록 탭을 늘리지 않고 통계·패턴에서 한 장으로 엽니다. */
  .summary-launch{width:100%;display:flex;align-items:center;gap:12px;text-align:left;background:var(--accbg);border:1px solid var(--acc2);border-radius:var(--r);padding:14px 15px;margin-bottom:12px;color:var(--tx)}
  .summary-launch .ic{width:38px;height:38px;flex:none;border-radius:12px;display:flex;align-items:center;justify-content:center;background:var(--panel);color:var(--acc)}
  .summary-launch .ic svg{width:22px;height:22px}.summary-launch .b{flex:1;min-width:0}.summary-launch .b b{display:block;font-size:15.5px}.summary-launch .b span{display:block;margin-top:2px;font-size:12px;line-height:1.45;color:var(--dim)}
  .summary-launch .go{flex:none;color:var(--acc);font-size:12px;font-weight:700}
  .summary-sheet{display:flex;flex-direction:column;gap:12px}.summary-sheet .card{margin:0}
  .summary-period{display:flex;align-items:flex-end;justify-content:space-between;gap:10px}.summary-period b{font-size:17px}.summary-period span{font-size:12px;color:var(--dim);text-align:right}
  .summary-section h2{margin:0 0 9px;font-size:14px;color:var(--dim)}
  .summary-row{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;padding:9px 0;border-bottom:1px solid var(--line)}
  .summary-row:last-child{border-bottom:0}.summary-row>span{font-size:13px;color:var(--dim);flex:0 0 88px}.summary-row>div{flex:1;text-align:right;font-size:13.5px;line-height:1.55}.summary-row>div b{font-size:14px}
  .summary-screen-row{padding:9px 0;border-bottom:1px solid var(--line)}.summary-screen-row:last-child{border-bottom:0}.summary-screen-row b{display:block;font-size:13.5px}.summary-screen-row span{display:block;margin-top:2px;font-size:12px;color:var(--dim);line-height:1.5}
  .summary-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px}.summary-actions .btn{margin:0}
  .summary-consult-only{display:none}
  body.summary-consult #tabs{display:none!important}
  body.summary-consult .summary-normal-only{display:none!important}
  body.summary-consult .summary-consult-only{display:block!important}
  body.summary-consult #p-recovery-summary{max-width:760px;padding-bottom:34px}
  body.summary-consult #view{padding-bottom:0}
  @media(max-width:380px){.summary-actions{grid-template-columns:1fr}}
  @media print{
    html,body{height:auto!important;overflow:visible!important;background:#fff!important}
    #app{height:auto!important;display:block!important}#view{overflow:visible!important}
    #tabs,.summary-normal-only,.summary-consult-only,.summary-actions{display:none!important}
    .pg{display:none!important}
    #p-recovery-summary.pg.on{display:block!important;max-width:none!important;padding:0!important;margin:0!important;color:#111!important}
    #p-recovery-summary .card,#p-recovery-summary .note,#p-recovery-summary .empty{break-inside:avoid;background:#fff!important;color:#111!important;border-color:#ccc!important;box-shadow:none!important}
    #p-recovery-summary .muted,#p-recovery-summary .tiny,#p-recovery-summary .summary-row>span,#p-recovery-summary .summary-screen-row span{color:#555!important}
    #p-recovery-summary h1,#p-recovery-summary h2,#p-recovery-summary h3,#p-recovery-summary b,#p-recovery-summary span,#p-recovery-summary div,#p-recovery-summary p{color:inherit}
  }
'''
once('</style>', css + '\n</style>', 'summary css')

summary_section = r'''

<!-- ══════════ 내 회복요약 V8.5 ══════════ -->
<section class="pg" id="p-recovery-summary">
  <div class="sp" style="margin-bottom:8px">
    <h1 style="margin:0">내 회복요약</h1>
    <button class="tiny summary-normal-only" style="color:var(--acc);font-weight:600" onclick="appBack('rec')">← 통계 · 패턴</button>
    <button class="tiny summary-consult-only" id="summary-consult-exit" style="color:var(--acc);font-weight:700">상담 화면 끝내기</button>
  </div>
  <p class="muted summary-normal-only" style="margin:0 0 14px">최근 4주 기록을 한 장으로 정리합니다. 저장된 기록을 새로 전송하거나 공유하지 않습니다.</p>
  <div id="recovery-summary-body"></div>
  <div class="summary-actions summary-normal-only">
    <button class="btn" id="summary-consult">상담할 때 보여주기</button>
    <button class="btn sec" id="summary-print">인쇄 · PDF 저장</button>
  </div>
</section>
'''
once('\n<!-- ══════════ 모임 찾기 ══════════ -->', summary_section + '\n<!-- ══════════ 모임 찾기 ══════════ -->', 'summary section')

old_share = r'''function shareApp(){
  const url = location.origin && location.origin !== 'null' ? location.origin + location.pathname : location.href.split('#')[0];
  const data={ title:'오늘 한 걸음', text:'회복을 하루씩 이어가는 데 사용할 수 있는 웹앱 오늘 한 걸음입니다.', url:url };
  if(navigator.share){ navigator.share(data).catch(()=>{}); return; }
  if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(url).then(()=>toast('앱 주소를 복사했습니다.')).catch(()=>toast('주소를 복사하지 못했습니다.')); return; }
  modal('<h2>오늘 한 걸음 추천하기</h2><p class="muted">아래 주소를 복사해 전달해주세요. 내 회복 기록은 포함되지 않습니다.</p><input value="'+esc(url)+'" readonly onclick="this.select()"><div style="height:10px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
}'''
new_share = r'''function shareApp(){
  /* 추천 주소는 버전별 APK가 아니라 고정 설치 안내 페이지입니다.
     install.html의 배포 대상만 바꾸면 예전 앱에서 공유한 링크도 최신 안내를 보여줄 수 있습니다. */
  const url = new URL('./install.html', location.href.split('#')[0]).href;
  const data={ title:'오늘 한 걸음 설치 안내', text:'오늘 한 걸음의 현재 설치 방법과 확인된 Android 버전을 안내합니다.', url:url };
  if(navigator.share){ navigator.share(data).catch(()=>{}); return; }
  if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(url).then(()=>toast('설치 안내 주소를 복사했습니다.')).catch(()=>toast('주소를 복사하지 못했습니다.')); return; }
  modal('<h2>오늘 한 걸음 추천하기</h2><p class="muted">아래 고정 설치 안내 주소를 전달해주세요. 내 회복 기록은 포함되지 않습니다.</p><input value="'+esc(url)+'" readonly onclick="this.select()"><div style="height:10px"></div><button class="btn sec" id="share-install-open">설치 안내 열기</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
  const b=$('#share-install-open'); if(b) b.onclick=()=>{ window.open(url,'_blank','noopener'); };
}'''
once(old_share, new_share, 'shareApp')

once('<span class="acc-n"><b>추천하기</b><span>회복에 도움이 될 사람에게 오늘 한 걸음을 알려주세요</span></span>',
     '<span class="acc-n"><b>추천하기</b><span>최신 설치 안내 페이지를 공유합니다</span></span>', 'recommend subtitle')

old_recstat = r'''function recStat(){
  if(famMode()) return recStatCore();
  const w=el('div');
  const nav=el('div','opts');
  nav.style.marginBottom='12px';
  [{v:'stat',l:'기록 통계'},{v:'pattern',l:'내 회복 패턴'}].forEach(o=>{
    const b=el('button','opt'+(recStatView===o.v?' on':''),o.l);
    b.onclick=()=>{ recStatView=o.v; drawRec(); };
    nav.appendChild(b);
  });
  w.appendChild(nav);
  w.appendChild(recStatView==='pattern'?recPattern():recStatCore());
  return w;
}'''
new_recstat = r'''function recStat(){
  if(famMode()) return recStatCore();
  const w=el('div');
  const sum=el('button','summary-launch');
  sum.type='button';
  sum.innerHTML='<span class="ic">'+ico('check')+'</span><span class="b"><b>최근 4주 내 회복요약</b><span>회복일 · 충동 · HALT · 수면 · 회복 실천 · 자가점검 · 다시 시작을 한 장으로 봅니다</span></span><span class="go">요약 보기</span>';
  sum.onclick=()=>go('recovery-summary');
  w.appendChild(sum);
  const nav=el('div','opts');
  nav.style.marginBottom='12px';
  [{v:'stat',l:'기록 통계'},{v:'pattern',l:'내 회복 패턴'}].forEach(o=>{
    const b=el('button','opt'+(recStatView===o.v?' on':''),o.l);
    b.onclick=()=>{ recStatView=o.v; drawRec(); };
    nav.appendChild(b);
  });
  w.appendChild(nav);
  w.appendChild(recStatView==='pattern'?recPattern():recStatCore());
  return w;
}'''
once(old_recstat, new_recstat, 'recStat')

summary_funcs = r'''

/* ══════════ V8.5 · 내 회복요약 ══════════
   별도 상담자 계정이나 서버를 만들지 않습니다. 사용자가 자기 기기에서 최근 4주 기록을
   한 장으로 보고, 필요할 때 화면 또는 브라우저 인쇄/PDF로 직접 보여주는 기능입니다. */
window.recoverySummaryConsult=false;
function recoverySummaryWindow(){
  const end=new Date(); end.setHours(23,59,59,999);
  const start=new Date(); start.setHours(0,0,0,0); start.setDate(start.getDate()-27);
  return {since:start.getTime(),start:ymd(start),end:ymd(end)};
}
function recoverySummaryData(){
  const win=recoverySummaryWindow();
  const timed=r=>r&&Number.isFinite(+r.t)&&+r.t>=win.since;
  const urges=(S.urges||[]).filter(timed);
  const halts=(S.halts||[]).filter(timed);
  const sleeps=(S.sleepLog||[]).filter(timed);
  const relapses=(S.relapses||[]).filter(timed);

  const haltCount={};
  halts.forEach(r=>new Set(Array.isArray(r.v)?r.v:[]).forEach(k=>{ if(k) haltCount[k]=(haltCount[k]||0)+1; }));
  const haltTop=Object.entries(haltCount).map(([k,n])=>({k,n,m:HALT.find(x=>x.k===k)})).sort((a,b)=>b.n-a.n).slice(0,4);

  const sleepCount={good:0,soso:0,bad:0};
  sleeps.forEach(r=>{ if(sleepCount[r.q]!=null) sleepCount[r.q]++; });

  const habitDays=new Set(); let habitTotal=0;
  (Array.isArray(S.habits)?S.habits:[]).forEach(h=>{
    (Array.isArray(h&&h.done)?h.done:[]).forEach(d=>{
      const v=String(d||'');
      if(/^\d{4}-\d{2}-\d{2}$/.test(v)&&v>=win.start&&v<=win.end){ habitDays.add(v); habitTotal++; }
    });
  });

  const recentScreen=(S.screenings||[]).filter(timed);
  const screenIds=[...new Set(recentScreen.map(r=>r.id).filter(Boolean))];
  const screens=screenIds.map(id=>{
    const tool=screenTool(id), hist=screenHistory(id); if(!tool||!hist.length) return null;
    const last=hist[hist.length-1]; if(!timed(last)) return null;
    const prev=hist.length>1?hist[hist.length-2]:null;
    return {tool,last,prev};
  }).filter(Boolean);

  const relapseCount={};
  relapses.forEach(r=>{ const k=String(r.type||'etc'); relapseCount[k]=(relapseCount[k]||0)+1; });

  const recovery=(S.types||[]).map(k=>({k,label:(typeOf(k)||{}).n||k,day:(S.dates&&S.dates[k])?recoveryDay(S.dates[k]):null}));
  const urgeAvg=urges.length?urges.reduce((n,r)=>n+(Number.isFinite(+r.b)?+r.b:0),0)/urges.length:null;
  return {win,urges,urgeAvg,halts,haltTop,sleeps,sleepCount,habitDays,habitTotal,screens,relapses,relapseCount,recovery};
}
function recoverySummaryRow(label,html){
  return '<div class="summary-row"><span>'+esc(label)+'</span><div>'+html+'</div></div>';
}
function recoverySummaryMainHtml(d){
  const recovery=d.recovery.length?d.recovery.map(r=>'<b>'+esc(r.label)+'</b> · '+(r.day==null?'시작일 미설정':r.day+'일째')).join('<br>'):'회복영역 미설정';
  const urge=d.urges.length?'<b>'+d.urges.length+'회</b> · 시작 강도 평균 '+d.urgeAvg.toFixed(1)+'/10':'기록 없음';
  const halt=d.halts.length?'<b>'+d.halts.length+'회 기록</b>'+(d.haltTop.length?' · '+d.haltTop.map(x=>esc((x.m&&x.m.l)||x.k)+' '+x.n+'회').join(' · '):''):'기록 없음';
  const sleep=d.sleeps.length?'<b>'+d.sleeps.length+'일 기록</b> · 잘 잠 '+d.sleepCount.good+' · 보통 '+d.sleepCount.soso+' · 못 잠 '+d.sleepCount.bad:'기록 없음';
  const habit=d.habitTotal?'<b>실천한 날 '+d.habitDays.size+'일</b> · 총 '+d.habitTotal+'회':'기록 없음';
  const relapse=d.relapses.length?'<b>'+d.relapses.length+'회</b> · '+Object.entries(d.relapseCount).map(([k,n])=>esc((typeOf(k)||{}).n||k)+' '+n+'회').join(' · '):'<b>0회</b>';
  return '<div class="card summary-section"><h2>한눈에</h2>'+recoverySummaryRow('회복일',recovery)+recoverySummaryRow('충동',urge)+recoverySummaryRow('HALT',halt)+recoverySummaryRow('수면',sleep)+recoverySummaryRow('회복 실천',habit)+recoverySummaryRow('다시 시작',relapse)+'</div>';
}
function recoverySummaryScreenHtml(d){
  let h='<div class="card summary-section"><h2>자가점검 변화</h2>';
  if(!d.screens.length) h+='<p class="tiny" style="margin:0">최근 4주에 저장한 자가점검 결과가 없습니다.</p>';
  else d.screens.forEach(x=>{
    let line='최근 '+x.last.score+'점 · 첫 기록';
    if(x.prev){ const diff=x.last.score-x.prev.score; line=ymd(x.prev.t)+' '+x.prev.score+'점 → '+ymd(x.last.t)+' '+x.last.score+'점'+(diff===0?' · 변화 없음':' · '+Math.abs(diff)+'점 '+(diff>0?'증가':'감소')); }
    h+='<div class="summary-screen-row"><b>'+esc(x.tool.title)+'</b><span>'+esc(line)+'</span></div>';
  });
  h+='<p class="tiny" style="margin:9px 0 0">검사마다 척도가 다르므로 점수를 서로 합산하지 않습니다. 증가·감소만으로 회복이나 악화를 단정하지 않습니다.</p></div>';
  return h;
}
function drawRecoverySummary(){
  const body=$('#recovery-summary-body'); if(!body) return;
  const d=recoverySummaryData();
  document.body.classList.toggle('summary-consult',!!window.recoverySummaryConsult);
  body.innerHTML='<div class="summary-sheet">'+
    '<div class="card summary-period"><div><b>최근 4주</b><div class="tiny">내가 직접 남긴 기기 내 기록 요약</div></div><span>'+esc(d.win.start.replaceAll('-','.'))+' ~ '+esc(d.win.end.replaceAll('-','.'))+'</span></div>'+ 
    '<div class="note"><b>기록 요약 안내</b><br>이 화면은 사용자가 직접 기록한 내용을 정리한 것이며 진단·위험도 점수·재발예측이 아닙니다. 자유기록 원문은 표시하지 않으며 서버나 마음프로로 자동 전송하지 않습니다.</div>'+ 
    recoverySummaryMainHtml(d)+recoverySummaryScreenHtml(d)+
    '<div class="card summary-section" id="summary-patterns"><h2>반복된 흐름 · 최근 90일</h2><p class="tiny" style="margin:0 0 9px">최근 4주 요약과 별도로, 기존 내 회복 패턴 엔진에서 반복이 확인된 항목만 최대 4개 참고합니다.</p></div>'+ 
    '</div>';

  const pb=$('#summary-patterns');
  const pattern=recPattern();
  const cards=[...pattern.children].filter(x=>x.classList&&x.classList.contains('card'));
  if(cards.length) cards.slice(0,4).forEach(c=>pb.appendChild(c));
  else pb.insertAdjacentHTML('beforeend','<div class="empty">아직 반복되는 흐름을 말하기에 기록이 충분하지 않습니다.</div>');

  const consult=$('#summary-consult'); if(consult) consult.onclick=()=>{ window.recoverySummaryConsult=true; document.body.classList.add('summary-consult'); drawRecoverySummary(); };
  const exit=$('#summary-consult-exit'); if(exit) exit.onclick=()=>{ window.recoverySummaryConsult=false; document.body.classList.remove('summary-consult'); drawRecoverySummary(); };
  const pr=$('#summary-print'); if(pr) pr.onclick=()=>{ if(typeof window.print==='function') window.print(); else toast('이 기기에서는 인쇄 기능을 열 수 없습니다.'); };
}
'''
once('\nfunction recPattern(){', summary_funcs + '\nfunction recPattern(){', 'summary functions')

once("function go(p,opt){\n  opt=opt||{};", "function go(p,opt){\n  opt=opt||{};\n  if(p!=='recovery-summary'){ window.recoverySummaryConsult=false; document.body.classList.remove('summary-consult'); }", 'go reset')
once("  if(p === 'rec')   drawRec();\n  if(p === 'treatment') drawTreatment();", "  if(p === 'rec')   drawRec();\n  if(p === 'recovery-summary') drawRecoverySummary();\n  if(p === 'treatment') drawTreatment();", 'go summary dispatch')

old_help = '<p style="margin-top:8px"><b>통계 · 패턴</b>에서는 기존 기록 통계와 <b>내 회복 패턴</b>을 전환해 볼 수 있습니다. 내 회복 패턴은 최근 90일 기기 기록에서 시간·HALT·감정·수면·회복 실천·관계처럼 반복된 사실을 설명할 뿐 진단·재발예측이 아니며, 특정 사람을 원인으로 판단하거나 자가점검 점수를 다른 기록과 합쳐 위험점수로 만들지 않습니다.</p>'
new_help = old_help + '\n      <p style="margin-top:8px"><b>최근 4주 내 회복요약</b>은 통계 · 패턴 상단에서 열 수 있습니다. 회복일·충동·HALT·수면·회복 실천·자가점검 변화·다시 시작을 한 장으로 정리하며, 상담할 때 화면으로 보여주거나 브라우저의 인쇄 기능을 이용해 PDF로 저장할 수 있습니다. 요약을 만드는 과정에서 기록을 서버로 보내지 않습니다.</p>'
once(old_help, new_help, 'help summary')

p.write_text(s, encoding='utf-8')

swp = Path('sw.js')
sw = swp.read_text(encoding='utf-8')
for old,new,name in [
    ("const APP_VERSION = 'V8.4';", "const APP_VERSION = 'V8.5';", 'sw version'),
    ("const V = 'ohg-v840-relationship-context';", "const V = 'ohg-v850-summary-install';", 'sw cache'),
    ("'./qa-data.js', './learning-data.js'", "'./install.html', './qa-data.js', './learning-data.js'", 'sw install shell'),
]:
    if sw.count(old)!=1: raise SystemExit(f'{name}: expected 1 match, got {sw.count(old)}')
    sw=sw.replace(old,new,1)
swp.write_text(sw, encoding='utf-8')

for fn in ['privacy.html','legal.html']:
    q=Path(fn); x=q.read_text(encoding='utf-8')
    old='<span class="ver">V8.4</span>'
    if x.count(old)!=1: raise SystemExit(f'{fn}: version badge expected 1, got {x.count(old)}')
    q.write_text(x.replace(old,'<span class="ver">V8.5</span>',1), encoding='utf-8')

readme=Path('README.md').read_text(encoding='utf-8')
note='''## V8.5 — 최근 4주 회복요약 · 고정 설치 안내
- `내 발자취 → 통계 · 패턴`의 탭 수는 늘리지 않고 상단에 `최근 4주 내 회복요약` 진입 카드를 추가했습니다. 회복일·충동·HALT·수면·회복 실천·자가점검 변화·다시 시작을 기기 내 기록으로 한 장에 정리합니다.
- `상담할 때 보여주기`는 읽기 전용 화면으로 전환하고, `인쇄 · PDF 저장`은 브라우저/기기의 인쇄 기능을 이용합니다. 기록을 서버나 마음프로로 자동 전송하지 않으며 자유기록 원문은 요약에 표시하지 않습니다. 반복 패턴은 기존 90일 `내 회복 패턴` 엔진 결과 중 최대 4개를 참고합니다.
- `추천하기`는 버전별 웹앱 주소가 아니라 고정 `install.html` 설치 안내 페이지를 공유합니다. 현재 설치 페이지는 실기기 확인이 끝난 V8.4 APK를 안내하며, 향후 Google Play 등록 시 같은 페이지의 배포 대상만 Play Store로 전환할 수 있게 분리했습니다.
- `DATA_SCHEMA=6`, 저장키 `ohg.v1`, 자가점검 채점, Android 정확알림·화면 OFF·부팅 재예약·복약/외래/생활/습관 알림·마음프로 TTS·이완 TTS 엔진은 변경하지 않습니다.

'''
Path('README.md').write_text(note+readme, encoding='utf-8')

install = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#1f6f8a">
<title>오늘 한 걸음 설치 안내</title>
<style>
:root{--bg:#f2f7f9;--panel:#fff;--line:#dbe6ea;--tx:#1b262c;--dim:#657781;--acc:#1f6f8a;--accbg:#e2eff4;--warn:#8b5b16;--warnbg:#fdf1e0}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.7 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;-webkit-font-smoothing:antialiased}main{max-width:620px;margin:0 auto;padding:28px 16px 52px}.brand{width:58px;height:58px;border-radius:18px;background:var(--accbg);display:flex;align-items:center;justify-content:center;color:var(--acc);margin-bottom:15px}.brand svg{width:32px;height:32px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}h1{font-size:25px;line-height:1.35;margin:0 0 7px}.lead{color:var(--dim);margin:0 0 18px}.card{background:var(--panel);border:1px solid var(--line);border-radius:17px;padding:17px;margin:12px 0}.badge{display:inline-block;padding:5px 9px;border-radius:999px;background:var(--accbg);color:var(--acc);font-size:11.5px;font-weight:700;margin-bottom:9px}.btn{display:block;width:100%;padding:13px 14px;border-radius:13px;background:var(--acc);color:#fff;text-align:center;text-decoration:none;font-weight:700;margin-top:12px}.btn.sec{background:var(--panel);color:var(--acc);border:1px solid var(--acc)}.tiny{font-size:12px;color:var(--dim);line-height:1.6}.note{background:var(--warnbg);color:var(--warn);border-radius:13px;padding:12px 14px;margin-top:12px}ol{padding-left:21px;margin:8px 0 0}li+li{margin-top:6px}footer{margin-top:26px;padding-top:16px;border-top:1px solid var(--line);font-size:12px;color:var(--dim)}
</style>
</head>
<body><main>
<div class="brand"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21c4.5-3.2 7-7 7-11.2A5.8 5.8 0 0 0 12 4a5.8 5.8 0 0 0-7 5.8C5 14 7.5 17.8 12 21Z"/><path d="M9 10.5c1.1.1 2.1.7 3 1.8 1-2.1 2.4-3.3 4.2-3.8"/></svg></div>
<h1>오늘 한 걸음 설치 안내</h1>
<p class="lead">추천 링크는 이 페이지로 고정됩니다. 설치 버전이나 배포처가 바뀌어도 같은 주소에서 최신 안내를 확인할 수 있습니다.</p>
<div class="card" id="install-card"></div>
<div class="card">
  <b>APK로 설치할 때</b>
  <ol class="tiny"><li>Android에서 APK 받기를 누릅니다.</li><li>처음 한 번은 브라우저의 ‘알 수 없는 앱 설치’ 허용이 필요할 수 있습니다.</li><li>기존 오늘 한 걸음 앱 위에 설치하면 같은 서명인 경우 기존 기기 기록을 유지한 채 업데이트됩니다.</li></ol>
  <div class="note tiny">설치 파일은 GitHub의 오늘 한 걸음 릴리즈에서 제공합니다. Google Play 등록 전까지의 설치 방식입니다.</div>
</div>
<a class="btn sec" href="./index.html">웹으로 오늘 한 걸음 열기</a>
<footer>이 페이지에는 개인 회복기록이 포함되지 않으며 설치 안내만 제공합니다.</footer>
<script>
/* 배포처 전환점은 여기 한 곳입니다. Google Play 등록 후 mode를 play로 바꾸고 playUrl만 채웁니다. */
const INSTALL={mode:'apk',verifiedVersion:'V8.4',apkUrl:'https://github.com/HanTae-ho/oneul-web/releases/download/v8.4-test/oneul-v8.4.apk',releaseUrl:'https://github.com/HanTae-ho/oneul-web/releases/tag/v8.4-test',playUrl:''};
const c=document.getElementById('install-card');
if(INSTALL.mode==='play'&&INSTALL.playUrl){
  c.innerHTML='<span class="badge">Google Play</span><h2 style="margin:0 0 6px;font-size:19px">Google Play에서 설치</h2><p class="tiny" style="margin:0">공식 스토어의 최신 버전을 설치합니다.</p><a class="btn" href="'+INSTALL.playUrl+'">Google Play 열기</a>';
}else{
  c.innerHTML='<span class="badge">실기기 동작 확인 · '+INSTALL.verifiedVersion+'</span><h2 style="margin:0 0 6px;font-size:19px">현재 확인된 Android 설치 버전</h2><p class="tiny" style="margin:0">새 테스트 빌드가 만들어져도 실기기 확인이 끝나기 전에는 이 추천 대상을 자동으로 바꾸지 않습니다.</p><a class="btn" href="'+INSTALL.apkUrl+'">Android APK '+INSTALL.verifiedVersion+' 받기</a><a class="btn sec" href="'+INSTALL.releaseUrl+'">릴리즈 정보 보기</a>';
}
</script>
</main></body></html>'''
Path('install.html').write_text(install, encoding='utf-8')
