from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
assert s.count("const BUILD = 'V8.1.1';") == 1
s=s.replace("const BUILD = 'V8.1.1';", "const BUILD = 'V8.1.2';", 1)

# Remove the dead pre-V8.1 medication renderer. Its DOM was moved to treatment management.
pat=r"/\* ── 복약 ──.*?\nfunction drawMed\(\)\{.*?\n\}\n\n(?=/\* ── 식사 · 잠 ──)"
s,n=re.subn(pat,'',s,count=1,flags=re.S)
assert n==1, f'legacy drawMed block: {n}'

old="""function treatmentCfg(){
  if(!S.treat || typeof S.treat !== 'object'){
    S.treat = {on:0,medOn:0,outpatientOn:0,lastVisit:'',rxDays:0,nextVisit:'',alertD3:1,alertD1:1,alertDay:1,alertTime:'09:00'};
  }
  return S.treat;
}"""
new="""function treatmentCfg(){
  if(!S.treat || typeof S.treat !== 'object'){
    S.treat = {on:0,medOn:0,outpatientOn:0,lastVisit:'',rxDays:0,intervalDays:0,nextVisit:'',alertD3:1,alertD1:1,alertDay:1,alertTime:'09:00'};
  }
  if(S.treat.intervalDays == null || isNaN(+S.treat.intervalDays)) S.treat.intervalDays = Math.max(0, parseInt(S.treat.rxDays,10) || 0);
  return S.treat;
}"""
assert s.count(old)==1
s=s.replace(old,new,1)

old="""function treatmentRxEnd(){ const t=treatmentCfg(), n=parseInt(t.rxDays,10); return t.lastVisit && n>0 ? addYmd(t.lastVisit,n-1) : ''; }
function treatmentSuggestedVisit(){ const t=treatmentCfg(), n=parseInt(t.rxDays,10); return t.lastVisit && n>0 ? addYmd(t.lastVisit,n) : ''; }
function treatmentVisitLabel(){
  const t=treatmentCfg(); if(!t.on||!t.outpatientOn||!t.nextVisit) return '';
  const d=diffYmd(today(),t.nextVisit);
  if(d===null) return '';
  if(d===0) return '오늘은 외래 예정일입니다.';
  if(d>0) return '다음 외래 D-' + d + ' · ' + t.nextVisit;
  return '외래 예정일이 ' + Math.abs(d) + '일 지났습니다. 일정을 확인해주세요.';
}"""
new="""function treatmentRxEnd(){ const t=treatmentCfg(), n=parseInt(t.rxDays,10); return t.lastVisit && n>0 ? addYmd(t.lastVisit,n-1) : ''; }
function treatmentInterval(){ const t=treatmentCfg(); return Math.max(0, parseInt(t.intervalDays,10) || 0); }
function treatmentSuggestedVisit(){ const t=treatmentCfg(), n=treatmentInterval(); return t.lastVisit && n>0 ? addYmd(t.lastVisit,n) : ''; }
function treatmentEffectiveVisit(){
  const t=treatmentCfg(), n=treatmentInterval();
  let v=t.nextVisit || treatmentSuggestedVisit();
  if(!v) return '';
  let guard=0;
  while(n>0 && diffYmd(v,today())>0 && guard++<1000) v=addYmd(v,n);
  return v;
}
function treatmentVisitLabel(){
  const t=treatmentCfg(); if(!t.on||!t.outpatientOn) return '';
  const v=treatmentEffectiveVisit(); if(!v) return '';
  const d=diffYmd(today(),v);
  if(d===null) return '';
  if(d===0) return '오늘은 외래 예정일입니다.';
  if(d>0) return '다음 외래 D-' + d + ' · ' + v;
  return '외래 예정일이 ' + Math.abs(d) + '일 지났습니다. 일정을 확인해주세요.';
}"""
assert s.count(old)==1
s=s.replace(old,new,1)

old="""  const t=treatmentCfg();
  if(!t.on || !t.outpatientOn || !t.nextVisit) return;
  const label=treatmentVisitLabel();
  if(!label) return;
  const d=diffYmd(today(),t.nextVisit);"""
new="""  const t=treatmentCfg();
  if(!t.on || !t.outpatientOn) return;
  const v=treatmentEffectiveVisit(); if(!v) return;
  const label=treatmentVisitLabel();
  if(!label) return;
  const d=diffYmd(today(),v);"""
assert s.count(old)==1
s=s.replace(old,new,1)

s=s.replace("<div class=\"card\"><h3>외래 관리</h3><p class=\"muted\" style=\"margin:-4px 0 11px\">처방일수로 약이 끝날 예상일과 다음 외래일을 계산해 제안합니다. 실제 예약일은 직접 확정해주세요.</p>",
            "<div class=\"card\"><h3>외래 관리</h3><p class=\"muted\" style=\"margin:-4px 0 11px\">이번 외래일과 외래 주기를 기준으로 다음 외래일을 자동 계산하고 같은 간격으로 반복합니다. 실제 예약일이 다르면 직접 수정할 수 있습니다.</p>",1)

old="""    [[0,'안 먹습니다'],[1,'1일 1회'],[2,'1일 2회'],[3,'1일 3회'],[4,'1일 4회']].forEach(([n,l])=>{
      const b=el('button','opt'+((S.medCnt||0)===n?' on':''),l);
      b.onclick=()=>{ S.medCnt=n; if(!n) t.medOn=0; save(); drawTreatment(); drawHome(); };
      cb.appendChild(b);
    });"""
new="""    [[1,'1일 1회'],[2,'1일 2회'],[3,'1일 3회'],[4,'1일 4회']].forEach(([n,l])=>{
      const b=el('button','opt'+((S.medCnt||0)===n?' on':''),l);
      b.onclick=()=>{ S.medCnt=n; save(); drawTreatment(); drawHome(); };
      cb.appendChild(b);
    });"""
assert s.count(old)==1
s=s.replace(old,new,1)

start=s.index("  if(t.outpatientOn){", s.index("treatToggle($('#treat-out-on')"))
end=s.index("  } else os.innerHTML='';",start)+len("  } else os.innerHTML='';")
newblock="""  if(t.outpatientOn){
    os.innerHTML='<label class=\"tiny\">이번 외래·처방일</label><input type=\"date\" id=\"treat-last\" style=\"margin:5px 0 12px\">'+
      '<label class=\"tiny\">처방일수</label><div class=\"sp\" style=\"margin:5px 0 12px\"><input type=\"number\" id=\"treat-days\" min=\"1\" max=\"365\" inputmode=\"numeric\" placeholder=\"예: 7\" style=\"flex:1\"><span class=\"muted\">일분</span></div>'+
      '<label class=\"tiny\">외래 주기</label><div class=\"sp\" style=\"margin:5px 0 12px\"><input type=\"number\" id=\"treat-interval\" min=\"1\" max=\"365\" inputmode=\"numeric\" placeholder=\"예: 7\" style=\"flex:1\"><span class=\"muted\">일 간격</span></div>'+
      '<div class=\"note\" id=\"treat-calc\" style=\"margin-bottom:12px\"></div>'+
      '<label class=\"tiny\">다음 외래 예정일 <span class=\"muted\">(자동계산 · 수정 가능)</span></label><input type=\"date\" id=\"treat-next\" style=\"margin:5px 0 8px\">'+
      '<p class=\"tiny\" style=\"margin:0 0 12px\">실제 예약일이 자동계산 날짜와 다르면 이 날짜만 바꾸세요. 이후에는 설정한 외래 주기로 다시 반복됩니다.</p>'+
      '<div class=\"sep\"></div><h3 style=\"font-size:14px\">외래 알림</h3><div class=\"opts\" id=\"treat-alerts\"></div><div style=\"height:10px\"></div><label class=\"tiny\">알림 시간</label><input type=\"time\" id=\"treat-alert-time\" style=\"margin-top:5px\">'+
      '<p class=\"tiny\" style=\"margin:10px 0 0\">잠금화면에는 병명·약 이름을 표시하지 않고 외래 일정만 중립적으로 알려드립니다.</p>';
    const last=$('#treat-last'), days=$('#treat-days'), interval=$('#treat-interval'), next=$('#treat-next'), at=$('#treat-alert-time');
    if(!t.intervalDays && t.rxDays) t.intervalDays=parseInt(t.rxDays,10)||0;
    if(!t.nextVisit && t.lastVisit && treatmentInterval()) t.nextVisit=addYmd(t.lastVisit,treatmentInterval());
    last.value=t.lastVisit||''; days.value=t.rxDays||''; interval.value=t.intervalDays||''; next.value=t.nextVisit||''; at.value=t.alertTime||'09:00';
    last.onchange=()=>{ t.lastVisit=last.value; if(t.lastVisit&&treatmentInterval()) t.nextVisit=addYmd(t.lastVisit,treatmentInterval()); save(); drawTreatment(); drawHome(); };
    days.onchange=()=>{ t.rxDays=Math.max(0,parseInt(days.value,10)||0); if(t.rxDays>0) t.intervalDays=t.rxDays; if(t.lastVisit&&treatmentInterval()) t.nextVisit=addYmd(t.lastVisit,treatmentInterval()); save(); drawTreatment(); drawHome(); };
    interval.onchange=()=>{ t.intervalDays=Math.max(0,parseInt(interval.value,10)||0); if(t.lastVisit&&treatmentInterval()) t.nextVisit=addYmd(t.lastVisit,treatmentInterval()); save(); drawTreatment(); drawHome(); };
    next.onchange=()=>{t.nextVisit=next.value;save();drawTreatment();drawHome();};
    at.onchange=()=>{t.alertTime=at.value||'09:00';save();};
    const end=treatmentRxEnd(), n=treatmentInterval(), eff=treatmentEffectiveVisit();
    $('#treat-calc').innerHTML=t.lastVisit&&n>0
      ? (end?'약 소진 예상일 <b>'+esc(end)+'</b><br>':'')+'다음 외래 예정일 <b>'+esc(t.nextVisit||treatmentSuggestedVisit())+'</b><br><span class=\"tiny\">이후 매 '+n+'일 간격으로 자동 반복'+(eff&&eff!==(t.nextVisit||'')?' · 현재 다음 회차 '+esc(eff):'')+'</span>'
      : '이번 외래일과 외래 주기를 입력하면 다음 외래일을 자동 계산합니다.';
    const ab=$('#treat-alerts');
    [[3,'3일 전','alertD3'],[1,'1일 전','alertD1'],[0,'당일','alertDay']].forEach(([d,l,k])=>{
      const b=el('button','opt'+(t[k]?' on':''),ico(t[k]?'check':'box')+'<span>'+l+'</span>');
      b.onclick=()=>{t[k]=t[k]?0:1;save();drawTreatment();}; ab.appendChild(b);
    });
  } else os.innerHTML='';"""
s=s[:start]+newblock+s[end:]

old="""  const visitActive = !famMode() && tr.on && tr.outpatientOn && /^\\d{4}-\\d{2}-\\d{2}$/.test(String(tr.nextVisit || ''));
  const visitAlerts = visitActive ? [tr.alertD3 ? 3 : null, tr.alertD1 ? 1 : null, tr.alertDay ? 0 : null].filter(x => x !== null).join(',') : '';"""
new="""  const visitDate = treatmentEffectiveVisit();
  const visitActive = !famMode() && tr.on && tr.outpatientOn && /^\\d{4}-\\d{2}-\\d{2}$/.test(String(visitDate || '')) && treatmentInterval()>0;
  const visitAlerts = visitActive ? [tr.alertD3 ? 3 : null, tr.alertD1 ? 1 : null, tr.alertDay ? 0 : null].filter(x => x !== null).join(',') : '';"""
assert s.count(old)==1
s=s.replace(old,new,1)
s=s.replace("    visit: visitActive ? tr.nextVisit : '',\n    visitAlerts: visitAlerts,",
            "    visit: visitActive ? visitDate : '',\n    visitInterval: visitActive ? String(treatmentInterval()) : '',\n    visitAlerts: visitAlerts,",1)

# Static guarantees for the user-visible behavior.
assert "'안 먹습니다'" not in s
assert 'function drawMed()' not in s
assert 'id="me-med-cnt"' not in s
assert 'intervalDays' in s and 'visitInterval' in s
assert '자동계산 · 수정 가능' in s
assert "const BUILD = 'V8.1.2';" in s
p.write_text(s,encoding='utf-8')

p=Path('sw.js'); sw=p.read_text(encoding='utf-8')
assert sw.count("const APP_VERSION = 'V8.1.1';")==1
assert sw.count("const V = 'ohg-v811-treatment';")==1
sw=sw.replace("const APP_VERSION = 'V8.1.1';","const APP_VERSION = 'V8.1.2';",1)
sw=sw.replace("const V = 'ohg-v811-treatment';","const V = 'ohg-v812-treatment';",1)
p.write_text(sw,encoding='utf-8')
