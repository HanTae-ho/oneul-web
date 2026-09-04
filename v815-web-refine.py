from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

# Weekday selector must actually hide when '매일' is selected.
once('.weekday-opts{display:grid!important;grid-template-columns:repeat(7,minmax(0,1fr));gap:5px!important}',
     '.weekday-opts{grid-template-columns:repeat(7,minmax(0,1fr));gap:5px!important}',
     'weekday css')

# Outpatient page owns dates/interval only. Alert offsets/time move to Android 알림 설정.
once("""      '<label class=\"tiny\">다음 외래 예정일 <span class=\"muted\">(자동계산 · 수정 가능)</span></label><input type=\"date\" id=\"treat-next\" style=\"margin:5px 0 8px\">'+
      '<p class=\"tiny\" style=\"margin:0 0 12px\">실제 예약일이 자동계산 날짜와 다르면 이 날짜만 바꾸세요. 이후에는 설정한 외래 주기로 다시 반복됩니다.</p>'+
      '<div class=\"sep\"></div><h3 style=\"font-size:14px\">외래 알림</h3><div class=\"opts\" id=\"treat-alerts\"></div><div style=\"height:10px\"></div><label class=\"tiny\">알림 시간</label><input type=\"time\" id=\"treat-alert-time\" style=\"margin-top:5px\">'+
      '<p class=\"tiny\" style=\"margin:10px 0 0\">잠금화면에는 병명·약 이름을 표시하지 않고 외래 일정만 중립적으로 알려드립니다.</p>';
    const last=$('#treat-last'), days=$('#treat-days'), interval=$('#treat-interval'), next=$('#treat-next'), at=$('#treat-alert-time');""",
"""      '<label class=\"tiny\">다음 외래 예정일 <span class=\"muted\">(자동계산 · 수정 가능)</span></label><input type=\"date\" id=\"treat-next\" style=\"margin:5px 0 8px\">'+
      '<p class=\"tiny\" style=\"margin:0\">실제 예약일이 자동계산 날짜와 다르면 이 날짜만 바꾸세요. 이후에는 설정한 외래 주기로 다시 반복됩니다. 외래 알림 시점과 시간은 <b>일정·알림 → 알림 설정</b>에서 관리합니다.</p>';
    const last=$('#treat-last'), days=$('#treat-days'), interval=$('#treat-interval'), next=$('#treat-next');""",
     'remove outpatient alert html')
once("last.value=t.lastVisit||''; days.value=t.rxDays||''; interval.value=t.intervalDays||''; next.value=t.nextVisit||''; at.value=t.alertTime||'09:00';",
     "last.value=t.lastVisit||''; days.value=t.rxDays||''; interval.value=t.intervalDays||''; next.value=t.nextVisit||'';",
     'remove alert time value')
once("    at.onchange=()=>{t.alertTime=at.value||'09:00';save();};\n",'', 'remove alert time handler')
once("""    const ab=$('#treat-alerts');
    [[3,'3일 전','alertD3'],[1,'1일 전','alertD1'],[0,'당일','alertDay']].forEach(([d,l,k])=>{
      const b=el('button','opt'+(t[k]?' on':''),ico(t[k]?'check':'box')+'<span>'+l+'</span>');
      b.onclick=()=>{t[k]=t[k]?0:1;save();drawTreatment();}; ab.appendChild(b);
    });
""",'', 'remove alert toggle logic')

# Android owns actual outpatient alert offsets/time in V8.1.5. Web sends only visit date/interval.
once("""  const visitAlerts = visitActive ? [tr.alertD3 ? 3 : null, tr.alertD1 ? 1 : null, tr.alertDay ? 0 : null].filter(x => x !== null).join(',') : '';
  return {""", "  return {", 'remove visit alerts calc')
once("""    visit: visitActive ? visitDate : '',
    visitInterval: visitActive ? String(treatmentInterval()) : '',
    visitAlerts: visitAlerts,
    visitTime: visitActive && /^\\d{2}:\\d{2}$/.test(String(tr.alertTime || '')) ? tr.alertTime : '',
    build: BUILD""",
"""    visit: visitActive ? visitDate : '',
    visitInterval: visitActive ? String(treatmentInterval()) : '',
    build: BUILD""", 'remove visit alert payload fields')

# Native summary count: one configured outpatient schedule, regardless of alert offsets selected natively.
once("""      (p.habits ? p.habits.split('|').filter(Boolean).length : 0) +
      (p.visit && p.visitAlerts ? p.visitAlerts.split(',').filter(Boolean).length : 0);""",
"""      (p.habits ? p.habits.split('|').filter(Boolean).length : 0) +
      (p.visit ? 1 : 0);""", 'native web count')

# Browser/PWA notification page label should include habits too.
s=s.replace('<h3>생활 · 치료 알림</h3>','<h3>습관 · 생활 · 치료 알림</h3>',1)

p.write_text('\n'.join(x.rstrip() for x in s.splitlines())+'\n',encoding='utf-8')
