from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')


def one(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s = s.replace(old, new, 1)

# Version
one("const BUILD = 'V8.0.5';", "const BUILD = 'V8.1';", 'BUILD')

# State: keep treatment config nested and local-only.
one("  hours: [], meds: [], medCnt: 0, medLog: [], area: '',\n", "  hours: [], meds: [], medCnt: 0, medLog: [], area: '',\n  treat: null,                                  /* 치료관리 — migrate()에서 안전하게 초기화 */\n", 'BLANK treat')

# Migration. Existing users with medication schedules automatically keep them visible.
needle = "function migrate(s){\n  if(!Array.isArray(s.screenings)) s.screenings = [];\n"
insert = "function migrate(s){\n  if(!s.treat || typeof s.treat !== 'object' || Array.isArray(s.treat)){\n    const hadMeds = Array.isArray(s.meds) && s.meds.length > 0;\n    s.treat = { on: hadMeds ? 1 : 0, medOn: hadMeds ? 1 : 0, outpatientOn: 0,\n      lastVisit: '', rxDays: 0, nextVisit: '', alertD3: 1, alertD1: 1, alertDay: 1, alertTime: '09:00' };\n  } else {\n    s.treat = Object.assign({ on:0, medOn:0, outpatientOn:0, lastVisit:'', rxDays:0, nextVisit:'',\n      alertD3:1, alertD1:1, alertDay:1, alertTime:'09:00' }, s.treat);\n  }\n  if(!Array.isArray(s.screenings)) s.screenings = [];\n"
one(needle, insert, 'migrate treatment')

# Independent treatment-management page.
marker = '<!-- ══════════ 내 발자취 ══════════ -->\n'
page = '''<!-- ══════════ 치료관리 V8.1 ══════════ -->
<section class="pg" id="p-treatment">
  <div class="sp" style="margin-bottom:8px">
    <h1 style="margin:0">치료관리</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('me')">← 돌아가기</button>
  </div>
  <p class="muted" style="margin:0 0 14px">
    복약과 외래 일정을 한곳에서 관리합니다. 약 이름이나 진단명은 묻지 않습니다. 기록은 이 기기에만 저장됩니다.
  </p>
  <div id="treat-master"></div>
  <div id="treat-body"></div>
</section>

'''
one(marker, page + marker, 'treatment page')

# Move medication configuration out of the generic care accordion.
old_med = '''      <h3>복약</h3>
      <p class="muted" style="margin:-4px 0 11px">
        하루에 몇 번 드시는지 고른 다음, 챙기는 때를 표시해두세요.
        홈 화면에서 그날 먹었는지 체크할 수 있습니다.
      </p>
      <div class="opts" id="me-med-cnt"></div>
      <div id="me-meds" style="margin-top:13px"></div>
      <p class="tiny" id="me-med-hint" style="margin:9px 0 0"></p>
      <p class="tiny" style="margin:11px 0 0">
        약에 대한 설명이나 복용 판단은 이 앱이 하지 않습니다.
        처방한 의사나 약사에게 확인하세요.
      </p>

      <div class="sep"></div>
      <h3>식사 · 잠</h3>'''
new_med = '''      <div class="me-self">
        <h3>복약 · 외래</h3>
        <p class="muted" style="margin:-4px 0 11px">
          복약 시간, 처방일수와 다음 외래일은 별도의 치료관리에서 설정합니다.
        </p>
        <button class="btn sec sm" onclick="go('treatment')">치료관리 열기</button>
        <div class="sep"></div>
      </div>
      <h3>식사 · 잠</h3>'''
one(old_med, new_med, 'move medication settings')

# Add a dedicated entry in My Info, without consuming the future Social bottom-tab slot.
app_marker = '''  <div class="acc">
    <button class="acc-h">
      <span class="acc-n"><b>앱</b><span id="acc-app-s">자원 목록 · 화면 설정 · 앱 새로고침 · 앱 설치</span></span>'''
treatment_entry = '''  <div class="acc me-self">
    <button class="acc-h">
      <span class="acc-n"><b>치료관리</b><span>복약 · 처방일수 · 외래 일정 · 치료 알림</span></span>
      <svg class="acc-v" viewBox="0 0 24 24"><path d="M6.5 9.5l5.5 5.5 5.5-5.5"/></svg>
    </button>
    <div class="acc-b">
      <p class="muted" style="margin:0 0 11px">
        필요한 경우에만 켜서 사용합니다. 끄더라도 기존 복약·외래 설정과 기록은 지우지 않습니다.
      </p>
      <button class="btn sec sm" onclick="go('treatment')">치료관리 설정</button>
    </div>
  </div>

'''
one(app_marker, treatment_entry + app_marker, 'treatment me entry')

# Care summary no longer pretends medication is configured there.
old_summary = "  $('#acc-care-s').textContent = fam\n    ? '복약 · 식사 · 잠 · 알림'\n    : '위험한 시간대 · 복약 · 식사 · 잠 · 알림';"
new_summary = "  $('#acc-care-s').textContent = fam\n    ? '식사 · 잠 · 알림'\n    : '위험한 시간대 · 식사 · 잠 · 알림';"
one(old_summary, new_summary, 'care summary')

# Routing.
one("  if(p === 'rec')   drawRec();\n", "  if(p === 'rec')   drawRec();\n  if(p === 'treatment') drawTreatment();\n", 'route treatment')

# Home medication check only when treatment + medication are active.
one("  /* 복약 */\n  if((S.meds || []).length){\n", "  /* 복약 — 치료관리에서 사용할 때만 홈에 표시합니다. */\n  if(treatmentMedOn() && (S.meds || []).length){\n", 'home med condition')

# Outpatient home summary sits with body/treatment information.
one("  /* 식사 · 잠 */\n  drawBodyHome(a);\n", "  /* 외래 일정 요약 */\n  drawTreatmentHome(a);\n\n  /* 식사 · 잠 */\n  drawBodyHome(a);\n", 'home outpatient summary')

# Browser in-app reminder loop must also respect treatment medication OFF.
one("  const doneToday = todayRec(S.medLog).map(x => x.n);\n  (S.meds || []).forEach(m => {\n", "  const doneToday = todayRec(S.medLog).map(x => x.n);\n  (treatmentMedOn() ? (S.meds || []) : []).forEach(m => {\n", 'browser medication reminder')

# Native payload: treatment medication can be suppressed; outpatient date/reminder options are passed separately.
old_payload = '''  const sp = S.sleep || {};
  return {
    risk: (S.role === 'family' ? [] : (S.hours || [])).filter(h => Number.isInteger(+h)).map(Number).join(','),
    meds: pack(S.meds),
    eats: pack(S.eats),
    bed: sp.on && /^\\d{2}:\\d{2}$/.test(String(sp.bed || '')) ? String(sp.bed) : '',
    build: BUILD
  };'''
new_payload = '''  const sp = S.sleep || {};
  const tr = treatmentCfg();
  const visitActive = !famMode() && tr.on && tr.outpatientOn && /^\\d{4}-\\d{2}-\\d{2}$/.test(String(tr.nextVisit || ''));
  const visitAlerts = visitActive ? [tr.alertD3 ? 3 : null, tr.alertD1 ? 1 : null, tr.alertDay ? 0 : null].filter(x => x !== null).join(',') : '';
  return {
    risk: (S.role === 'family' ? [] : (S.hours || [])).filter(h => Number.isInteger(+h)).map(Number).join(','),
    meds: treatmentMedOn() ? pack(S.meds) : '',
    eats: pack(S.eats),
    bed: sp.on && /^\\d{2}:\\d{2}$/.test(String(sp.bed || '')) ? String(sp.bed) : '',
    visit: visitActive ? tr.nextVisit : '',
    visitAlerts: visitAlerts,
    visitTime: visitActive && /^\\d{2}:\\d{2}$/.test(String(tr.alertTime || '')) ? tr.alertTime : '',
    build: BUILD
  };'''
one(old_payload, new_payload, 'native treatment payload')

# Native status count/text includes outpatient one-time reminders.
old_count = '''    const n = (p.risk ? p.risk.split(',').filter(Boolean).length : 0) +
      (p.meds ? p.meds.split('|').filter(Boolean).length : 0) +
      (p.eats ? p.eats.split('|').filter(Boolean).length : 0) + (p.bed ? 1 : 0);
    st.textContent = 'Android 앱 연결 확인됨 · ' + BUILD + ' · 앱이 완전히 닫혀 있어도 Android가 예약알림을 보낼 수 있습니다. 현재 설정된 시간 ' + n + '개. ' +
      '[Android 예약알림 설정]에서 내용을 확인한 뒤 [저장하고 앱으로 돌아가기]를 눌러 반영해주세요. ' +
      '복약·식사·잠 또는 위험시간대를 바꾸면 이 과정을 다시 해주세요.';'''
new_count = '''    const n = (p.risk ? p.risk.split(',').filter(Boolean).length : 0) +
      (p.meds ? p.meds.split('|').filter(Boolean).length : 0) +
      (p.eats ? p.eats.split('|').filter(Boolean).length : 0) + (p.bed ? 1 : 0) +
      (p.visit && p.visitAlerts ? p.visitAlerts.split(',').filter(Boolean).length : 0);
    st.textContent = 'Android 앱 연결 확인됨 · ' + BUILD + ' · 앱이 완전히 닫혀 있어도 Android가 예약알림을 보낼 수 있습니다. 현재 예약 ' + n + '개. ' +
      '[Android 예약알림 설정]에서 내용을 확인한 뒤 [저장하고 앱으로 돌아가기]를 눌러 반영해주세요. ' +
      '복약·외래·식사·잠 또는 위험시간대를 바꾸면 이 과정을 다시 해주세요.';'''
one(old_count, new_count, 'native status count')

# Treatment-management implementation. Function declarations are hoisted, so insertion point is intentionally near notification helpers.
js_marker = "/* ── 알림 켜기/끄기 ──\n"
js = r'''/* ── 치료관리 V8.1 ──
   복약·외래는 치료를 판단하지 않고, 사용자가 정한 일정만 보관·상기합니다.
   처방일수는 다음 외래일을 '제안'하는 계산에만 쓰며 실제 예약일을 확정하지 않습니다. */
function treatmentCfg(){
  if(!S.treat || typeof S.treat !== 'object'){
    S.treat = {on:0,medOn:0,outpatientOn:0,lastVisit:'',rxDays:0,nextVisit:'',alertD3:1,alertD1:1,alertDay:1,alertTime:'09:00'};
  }
  return S.treat;
}
function treatmentMedOn(){ const t=treatmentCfg(); return !famMode() && !!t.on && !!t.medOn; }
function ymdDate(v){
  const a=String(v||'').split('-').map(Number);
  if(a.length!==3 || !a[0] || !a[1] || !a[2]) return null;
  const d=new Date(a[0],a[1]-1,a[2]);
  return isNaN(d.getTime()) ? null : d;
}
function addYmd(v,n){ const d=ymdDate(v); if(!d) return ''; d.setDate(d.getDate()+Number(n||0)); return ymd(d); }
function diffYmd(from,to){
  const a=String(from||'').split('-').map(Number), b=String(to||'').split('-').map(Number);
  if(a.length!==3||b.length!==3||!a[0]||!b[0]) return null;
  return Math.round((Date.UTC(b[0],b[1]-1,b[2])-Date.UTC(a[0],a[1]-1,a[2]))/86400000);
}
function treatmentRxEnd(){ const t=treatmentCfg(), n=parseInt(t.rxDays,10); return t.lastVisit && n>0 ? addYmd(t.lastVisit,n-1) : ''; }
function treatmentSuggestedVisit(){ const t=treatmentCfg(), n=parseInt(t.rxDays,10); return t.lastVisit && n>0 ? addYmd(t.lastVisit,n) : ''; }
function treatmentVisitLabel(){
  const t=treatmentCfg(); if(!t.on||!t.outpatientOn||!t.nextVisit) return '';
  const d=diffYmd(today(),t.nextVisit);
  if(d===null) return '';
  if(d===0) return '오늘은 외래 예정일입니다.';
  if(d>0) return '다음 외래 D-' + d + ' · ' + t.nextVisit;
  return '외래 예정일이 ' + Math.abs(d) + '일 지났습니다. 일정을 확인해주세요.';
}
function drawTreatmentHome(box){
  if(famMode()) return;
  const t=treatmentCfg();
  if(!t.on || !t.outpatientOn || !t.nextVisit) return;
  const label=treatmentVisitLabel();
  if(!label) return;
  const d=diffYmd(today(),t.nextVisit);
  const cls=d===0 ? 'note' : 'card tight';
  box.insertAdjacentHTML('beforeend','<div class="'+cls+'" style="margin-bottom:12px">'+
    '<div class="sp"><div><b>'+esc(d===0?'오늘 외래':'치료관리')+'</b><div class="muted" style="margin-top:3px">'+esc(label)+'</div></div>'+
    '<button class="btn sec sm" style="width:auto;padding:7px 12px" id="home-treatment-open">보기</button></div></div>');
  const b=$('#home-treatment-open'); if(b) b.onclick=()=>go('treatment');
}
function treatToggle(box, on, onLabel, offLabel, setter){
  box.innerHTML='';
  [[1,onLabel],[0,offLabel]].forEach(([v,l])=>{
    const b=el('button','opt'+((on?1:0)===v?' on':''),ico((on?1:0)===v?'check':'box')+'<span>'+l+'</span>');
    b.onclick=()=>setter(v);
    box.appendChild(b);
  });
}
function drawTreatment(){
  const master=$('#treat-master'), body=$('#treat-body');
  if(!master||!body) return;
  if(famMode()){
    master.innerHTML='<div class="note w">치료관리는 현재 본인 회복모드에서만 사용합니다. 가족의 복약·진료를 대신 관리하는 기능은 별도로 설계합니다.</div>';
    body.innerHTML=''; return;
  }
  const t=treatmentCfg();
  master.innerHTML='<div class="card"><h3>치료관리 사용</h3><p class="muted" style="margin:-4px 0 11px">필요한 경우에만 켜세요. 끄더라도 기존 설정과 기록은 삭제하지 않습니다.</p><div class="opts" id="treat-on"></div></div>';
  treatToggle($('#treat-on'),t.on,'사용함','사용하지 않음',v=>{ t.on=v; save(); drawTreatment(); drawHome(); });
  if(!t.on){ body.innerHTML=''; return; }

  body.innerHTML='<div class="card"><h3>복약 관리</h3><p class="muted" style="margin:-4px 0 11px">약 이름은 적지 않습니다. 하루 몇 번, 언제 챙길지만 정합니다.</p><div class="opts" id="treat-med-on"></div><div id="treat-med-settings" style="margin-top:13px"></div></div>'+
    '<div class="card"><h3>외래 관리</h3><p class="muted" style="margin:-4px 0 11px">처방일수로 약이 끝날 예상일과 다음 외래일을 계산해 제안합니다. 실제 예약일은 직접 확정해주세요.</p><div class="opts" id="treat-out-on"></div><div id="treat-out-settings" style="margin-top:13px"></div></div>'+
    '<div class="note" id="treat-native-note"></div>';

  treatToggle($('#treat-med-on'),t.medOn,'복약 관리 사용','복약 관리 안 함',v=>{ t.medOn=v; save(); drawTreatment(); drawHome(); });
  const ms=$('#treat-med-settings');
  if(t.medOn){
    ms.innerHTML='<p class="tiny" style="margin:0 0 8px">하루 복약 횟수</p><div class="opts" id="treat-med-cnt"></div><div id="treat-meds" style="margin-top:12px"></div><p class="tiny" id="treat-med-hint" style="margin:9px 0 0"></p><p class="tiny" style="margin:11px 0 0">복용 여부·용량·약 변경은 처방한 의사나 약사와 상의하세요.</p>';
    const cb=$('#treat-med-cnt');
    [[0,'안 먹습니다'],[1,'1일 1회'],[2,'1일 2회'],[3,'1일 3회'],[4,'1일 4회']].forEach(([n,l])=>{
      const b=el('button','opt'+((S.medCnt||0)===n?' on':''),l);
      b.onclick=()=>{ S.medCnt=n; if(!n) t.medOn=0; save(); drawTreatment(); drawHome(); };
      cb.appendChild(b);
    });
    if(S.medCnt){
      S.meds=S.meds||[]; const mb=$('#treat-meds');
      MEDSLOT.forEach(slot=>{
        const cur=S.meds.filter(m=>m.s===slot.k)[0];
        const r=el('div','sp'); r.style.padding='5px 0';
        const b=el('button','opt'+(cur?' on':''),ico(cur?'check':'box')+'<span>'+slot.l+'</span>');
        b.style.flex='1'; b.style.justifyContent='flex-start';
        b.onclick=()=>{ if(cur) S.meds=S.meds.filter(m=>m.s!==slot.k); else S.meds.push({s:slot.k,t:slot.d}); save(); drawTreatment(); drawHome(); };
        r.appendChild(b);
        if(cur){ const ti=el('input'); ti.type='time'; ti.value=cur.t||slot.d; ti.style.width='132px'; ti.onchange=()=>{cur.t=ti.value;save();}; r.appendChild(ti); }
        mb.appendChild(r);
      });
      const n=S.meds.length,w=S.medCnt; $('#treat-med-hint').textContent=n===w?'하루 '+w+'번, 다 정하셨습니다.':n<w?'하루 '+w+'번 중 '+n+'개를 정하셨습니다. '+(w-n)+'개 더 골라주세요.':'하루 '+w+'번인데 '+n+'개를 고르셨습니다. 횟수를 다시 확인해주세요.';
    }
  } else ms.innerHTML='';

  treatToggle($('#treat-out-on'),t.outpatientOn,'외래 관리 사용','외래 관리 안 함',v=>{t.outpatientOn=v;save();drawTreatment();drawHome();});
  const os=$('#treat-out-settings');
  if(t.outpatientOn){
    os.innerHTML='<label class="tiny">이번 외래·처방일</label><input type="date" id="treat-last" style="margin:5px 0 12px">'+
      '<label class="tiny">처방일수</label><div class="sp" style="margin:5px 0 12px"><input type="number" id="treat-days" min="1" max="365" inputmode="numeric" placeholder="예: 14" style="flex:1"><span class="muted">일분</span></div>'+
      '<div class="note" id="treat-calc" style="margin-bottom:12px"></div>'+
      '<label class="tiny">실제 다음 외래 예정일</label><input type="date" id="treat-next" style="margin:5px 0 8px"><button class="btn ghost sm" id="treat-apply-suggest">제안 날짜로 입력</button>'+
      '<div class="sep"></div><h3 style="font-size:14px">외래 알림</h3><div class="opts" id="treat-alerts"></div><div style="height:10px"></div><label class="tiny">알림 시간</label><input type="time" id="treat-alert-time" style="margin-top:5px">'+
      '<p class="tiny" style="margin:10px 0 0">잠금화면에는 병명·약 이름을 표시하지 않고 외래 일정만 중립적으로 알려드립니다.</p>';
    const last=$('#treat-last'), days=$('#treat-days'), next=$('#treat-next'), at=$('#treat-alert-time');
    last.value=t.lastVisit||''; days.value=t.rxDays||''; next.value=t.nextVisit||''; at.value=t.alertTime||'09:00';
    const saveDate=()=>{ t.lastVisit=last.value; t.rxDays=Math.max(0,parseInt(days.value,10)||0); save(); drawTreatment(); drawHome(); };
    last.onchange=saveDate; days.onchange=saveDate;
    next.onchange=()=>{t.nextVisit=next.value;save();drawTreatment();drawHome();};
    at.onchange=()=>{t.alertTime=at.value||'09:00';save();};
    const end=treatmentRxEnd(), sug=treatmentSuggestedVisit();
    $('#treat-calc').innerHTML=end&&sug?'약 소진 예상일 <b>'+esc(end)+'</b><br>다음 외래 제안일 <b>'+esc(sug)+'</b><br><span class="tiny">처방일수 기준 계산일 뿐 실제 예약일은 아닙니다.</span>':'처방일과 처방일수를 입력하면 약 소진 예상일과 다음 외래 제안일을 보여드립니다.';
    const apply=$('#treat-apply-suggest'); apply.disabled=!sug; apply.onclick=()=>{if(!sug)return;t.nextVisit=sug;save();drawTreatment();drawHome();};
    const ab=$('#treat-alerts');
    [[3,'3일 전','alertD3'],[1,'1일 전','alertD1'],[0,'당일','alertDay']].forEach(([d,l,k])=>{
      const b=el('button','opt'+(t[k]?' on':''),ico(t[k]?'check':'box')+'<span>'+l+'</span>');
      b.onclick=()=>{t[k]=t[k]?0:1;save();drawTreatment();}; ab.appendChild(b);
    });
  } else os.innerHTML='';

  const nn=$('#treat-native-note');
  if(nativeAndroidApp()){
    nn.innerHTML='<b>Android 예약알림</b><br><span class="muted">설정을 바꾼 뒤 아래 버튼에서 Android 예약을 저장해야 앱을 완전히 닫아도 반영됩니다.</span><div style="height:9px"></div><button class="btn sec sm" id="treat-sync-native">Android 예약알림 반영</button>';
    $('#treat-sync-native').onclick=openNativeReminderSettings;
  } else nn.innerHTML='<b>알림 안내</b><br><span class="muted">정확한 복약·외래 예약알림은 Android 앱에서 지원합니다.</span>';
}

'''
one(js_marker, js + js_marker, 'treatment JS')

# Update generic care comment.
s = s.replace("  <!-- 복약 · 식사 · 잠 · 알림은 결국 '때가 되면 챙기는 것' 하나입니다.\n       알림만 저 아래 따로 두었더니 무엇을 알려준다는 것인지 안 보였습니다. -->",
              "  <!-- 위험시간·식사·잠은 일상 챙기기입니다. 복약·외래는 V8.1부터 별도 치료관리로 분리합니다. -->", 1)

p.write_text(s, encoding='utf-8')

# Service worker version/cache.
sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
if w.count("const APP_VERSION = 'V8.0.5';") != 1 or w.count("const V = 'ohg-v805';") != 1:
    raise SystemExit('sw version anchors not found exactly once')
w = w.replace("const APP_VERSION = 'V8.0.5';", "const APP_VERSION = 'V8.1';", 1)
w = w.replace("const V = 'ohg-v805';", "const V = 'ohg-v810-treatment';", 1)
sw.write_text(w, encoding='utf-8')

print('V8.1 treatment patch applied')
