from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def sub1(pattern, repl, label, flags=0):
    global s
    s2, n = re.subn(pattern, repl, s, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 replacement, got {n}')
    s = s2

# 1) Recovery-tools layout: daily practice first, then learning, then self-check.
old_section = r'''<!-- ══════════ 회복도구 V6\.1 ══════════ -->\n<section class="pg" id="p-tools">.*?</section>\n\n(?=<!-- ══════════ 자가점검 V7\.1 ══════════ -->)'''
new_section = '''<!-- ══════════ 회복도구 V8.1.4 ══════════ -->
<section class="pg" id="p-tools">
  <h1>회복도구</h1>

  <div class="toolsec">
    <h2>오늘의 실천</h2>
    <div class="practicegrid">
      <button class="practicecard habit soon" id="tool-habit">
        <span class="ic" data-ico="sprout"></span>
        <span class="b"><b>습관</b><span>매일 반복할 작은 실천</span><small>준비 중</small></span>
      </button>
      <button class="practicecard schedule" id="tool-schedule">
        <span class="ic" data-ico="cal"></span>
        <span class="b"><b>일정 · 알림</b><span id="tool-schedule-s">생활 · 치료 일정을 한곳에서 관리</span><small>열기</small></span>
      </button>
    </div>
  </div>

  <div class="toolsec">
    <h2>배우고 연습하기</h2>
    <div class="learnmini">
      <button class="minitool" id="tool-learn">
        <span class="ic" data-ico="sprout"></span><b>회복학습</b><span>회복을 더 잘 이해하기</span>
      </button>
      <button class="minitool" id="tool-workbook">
        <span class="ic" data-ico="check"></span><b>단계별 점검</b><span>현재 상태를 단계별로 점검</span>
      </button>
      <button class="minitool" id="tool-listen">
        <span class="ic" data-ico="wave"></span><b>듣는 글</b><span>마음에 도움이 되는 이야기</span>
      </button>
    </div>
  </div>

  <div class="toolsec">
    <h2>나를 점검하기</h2>
    <div class="checkmini">
      <button class="minitool wide" id="tool-check">
        <span class="ic" data-ico="check"></span><b>자가점검</b><span>내 상태를 스스로 확인하기</span>
      </button>
      <button class="minitool wide" id="tool-qa">
        <span class="ic" data-ico="speak"></span><b>중독 Q&A</b><span id="tool-qa-s">궁금한 내용을 질문하고 답변 보기</span>
      </button>
    </div>
  </div>
</section>

'''
sub1(old_section, new_section, 'recovery tools section', re.S)

# 2) Add styles without disturbing existing components.
css_anchor = "  .toolcard.soon{opacity:.78}.toolcard.soon .go{color:var(--faint)}\n"
css_add = '''  .toolcard.soon{opacity:.78}.toolcard.soon .go{color:var(--faint)}
  /* V8.1.4 — 회복도구는 기능 나열이 아니라 목적별로 찾습니다. */
  .toolsec{margin:0 0 20px}.toolsec>h2{margin:0 0 9px!important;font-size:15px!important;color:var(--tx)!important;font-weight:700!important}
  .practicegrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
  .practicecard{min-height:150px;padding:15px 13px;text-align:left;border:1px solid var(--line);border-radius:16px;background:var(--panel);display:flex;flex-direction:column;align-items:flex-start;color:var(--tx)}
  .practicecard.habit{background:color-mix(in srgb,var(--panel) 72%,#dff3df)}
  .practicecard.schedule{background:color-mix(in srgb,var(--panel) 72%,var(--accbg))}
  .practicecard .ic{width:45px;height:45px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--panel);color:var(--acc);margin-bottom:15px}
  .practicecard.habit .ic{color:var(--leaf)}
  .practicecard .ic .ic-s{width:24px;height:24px}.practicecard .b{display:block;width:100%}
  .practicecard .b b{display:block;font-size:16px;line-height:1.3}.practicecard .b span{display:block;margin-top:5px;font-size:12.5px;line-height:1.45;color:var(--dim)}
  .practicecard .b small{display:block;margin-top:10px;font-size:11px;font-weight:700;color:var(--acc)}
  .practicecard.soon .b small{color:var(--faint)}
  .learnmini{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.checkmini{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
  .minitool{min-height:134px;padding:13px 8px;border:1px solid var(--line);border-radius:14px;background:var(--panel);text-align:center;display:flex;flex-direction:column;align-items:center;color:var(--tx)}
  .minitool .ic{width:40px;height:40px;border-radius:12px;background:var(--accbg);color:var(--acc);display:flex;align-items:center;justify-content:center;margin-bottom:9px}
  .minitool .ic .ic-s{width:21px;height:21px}.minitool b{font-size:13.5px;line-height:1.3}.minitool span{font-size:11.5px;line-height:1.4;color:var(--dim);margin-top:5px;word-break:keep-all}
  .minitool.wide{min-height:126px}
  .schedulecards{display:grid;gap:10px}.schedulecard{width:100%;padding:16px 15px;border:1px solid var(--line);border-radius:16px;background:var(--panel);display:flex;align-items:center;gap:13px;text-align:left;color:var(--tx)}
  .schedulecard .ic{width:46px;height:46px;flex:none;border-radius:14px;background:var(--accbg);color:var(--acc);display:flex;align-items:center;justify-content:center}
  .schedulecard .ic .ic-s{width:24px;height:24px}.schedulecard .b{flex:1;min-width:0}.schedulecard .b b{display:block;font-size:16px}.schedulecard .b span{display:block;margin-top:3px;font-size:12.5px;line-height:1.45;color:var(--dim)}
  .schedulecard .go{font-size:18px;color:var(--faint)}
  @media(max-width:350px){.learnmini{grid-template-columns:1fr}.minitool{min-height:0;flex-direction:row;text-align:left;gap:10px;padding:12px}.minitool .ic{margin:0;flex:none}.minitool b{min-width:70px}.minitool span{margin:0;flex:1}.practicegrid,.checkmini{grid-template-columns:1fr}.practicecard{min-height:0}}
'''
if s.count(css_anchor) != 1:
    raise SystemExit('css anchor not unique')
s = s.replace(css_anchor, css_add, 1)

# 3) Dedicated schedule hub + life schedule + notification schedule.
anchor = '<!-- ══════════ 일정·알림 · 치료 일정 V8.1.3 ══════════ -->\n'
insert = '''<!-- ══════════ 일정·알림 허브 V8.1.4 ══════════ -->
<section class="pg" id="p-schedule">
  <div class="sp" style="margin-bottom:8px">
    <h1 style="margin:0">일정 · 알림</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('tools')">← 회복도구</button>
  </div>
  <p class="muted" style="margin:0 0 14px">생활과 치료 일정을 나누어 정하고, 알림은 한곳에서 관리합니다.</p>
  <div class="schedulecards">
    <button class="schedulecard" id="schedule-life">
      <span class="ic" data-ico="cal"></span>
      <span class="b"><b>생활 일정</b><span id="schedule-life-s">위험시간 · 식사 · 잠</span></span><span class="go">›</span>
    </button>
    <button class="schedulecard me-self" id="schedule-treatment">
      <span class="ic" data-ico="check"></span>
      <span class="b"><b>치료 일정</b><span id="schedule-treatment-s">복약 · 처방 · 외래 · 반복 외래</span></span><span class="go">›</span>
    </button>
    <button class="schedulecard" id="schedule-notify">
      <span class="ic" data-ico="bell"></span>
      <span class="b"><b>알림 설정</b><span id="schedule-notify-s">생활 · 치료 알림 관리</span></span><span class="go">›</span>
    </button>
  </div>
</section>

<section class="pg" id="p-life-schedule">
  <div class="sp" style="margin-bottom:8px">
    <h1 style="margin:0">생활 일정</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('schedule')">← 일정·알림</button>
  </div>
  <p class="muted" style="margin:0 0 14px">위험한 시간대와 식사·잠처럼 매일의 생활 리듬을 정합니다.</p>
  <div class="card me-self" id="life-risk">
    <h3>위험한 시간대</h3>
    <p class="muted" style="margin:-4px 0 11px" id="me-hours-d"></p>
    <div class="opts" id="me-hours"></div>
  </div>
  <div class="card">
    <h3>식사</h3>
    <p class="muted" style="margin:-4px 0 11px">챙길 끼니와 시간을 정합니다. 양이나 칼로리는 기록하지 않습니다.</p>
    <div id="me-eats"></div>
    <p class="tiny" id="me-eat-hint" style="margin:9px 0 0"></p>
  </div>
  <div class="card">
    <h3>잠</h3>
    <p class="muted" style="margin:-4px 0 11px">잘 시간과 일어날 시간을 정해 생활 리듬을 챙깁니다.</p>
    <div class="opts" id="me-sleep-on"></div>
    <div id="me-sleep" style="margin-top:11px"></div>
  </div>
</section>

<section class="pg" id="p-notify-schedule">
  <div class="sp" style="margin-bottom:8px">
    <h1 style="margin:0">알림 설정</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('schedule')">← 일정·알림</button>
  </div>
  <p class="muted" style="margin:0 0 14px">생활 일정과 치료 일정에서 정한 시간을 실제 알림으로 연결합니다.</p>
  <div class="card">
    <h3>생활 · 치료 알림</h3>
    <p class="muted" style="margin:-4px 0 11px">위험시간 · 복약 · 식사 · 잠 · 외래 알림을 한곳에서 관리합니다.</p>
    <div class="opts" id="me-notify"></div>
    <p class="tiny" id="me-notify-st" style="margin:10px 0 0"></p>
  </div>
</section>

<!-- ══════════ 일정·알림 · 치료 일정 V8.1.4 ══════════ -->
'''
if s.count(anchor) != 1:
    raise SystemExit('schedule insert anchor not unique')
s = s.replace(anchor, insert, 1)

# 4) Remove detailed schedule settings from My Info; this page returns to profile/app settings only.
pat = r'''\n  <!-- V8\.1\.3: 생활·치료·알림의 진입점을 하나로 합칩니다\. 내부 저장·예약 엔진은 그대로 유지합니다\. -->\n  <div class="acc">.*?\n  </div>\n\n(?=  <div class="acc">\n    <button class="acc-h">\n      <span class="acc-n"><b>앱</b>)'''
sub1(pat, '\n', 'remove my-info schedule block', re.S)

# 5) Treatment screen returns to the new schedule hub.
s = s.replace("onclick=\"appBack('me')\">← 일정·알림</button>", "onclick=\"appBack('schedule')\">← 일정·알림</button>", 1)

# 6) Navigation: schedule pages belong to Recovery Tools tab.
old = "let tabP = (p === 'qa' || p === 'learn' || p === 'learn-topic' || p === 'workbook-list' || p === 'workbook' || p === 'screening' || p === 'screen-test') ? 'tools' : p;"
new = "let tabP = (p === 'qa' || p === 'learn' || p === 'learn-topic' || p === 'workbook-list' || p === 'workbook' || p === 'screening' || p === 'screen-test' || p === 'schedule' || p === 'life-schedule' || p === 'notify-schedule' || p === 'treatment') ? 'tools' : p;"
if s.count(old) != 1:
    raise SystemExit('tab map anchor not unique')
s = s.replace(old, new, 1)

old = "  if(p === 'tools') drawTools();\n"
new = "  if(p === 'tools') drawTools();\n  if(p === 'schedule') drawScheduleHub();\n  if(p === 'life-schedule') drawLifeSchedule();\n  if(p === 'notify-schedule') drawNotifySchedule();\n"
if s.count(old) != 1:
    raise SystemExit('go draw anchor not unique')
s = s.replace(old, new, 1)

# 7) Tools + schedule draw helpers.
old = '''function drawTools(){
  const n = QA.length;
  const m = $('#tool-qa-s');
  if(m) m.textContent = '회복 Q&A · 총 ' + n + '문답';
  refreshIcons();
}
'''
new = '''function drawTools(){
  const n = QA.length;
  const m = $('#tool-qa-s');
  if(m) m.textContent = '회복 Q&A · 총 ' + n + '문답';
  const ss = $('#tool-schedule-s');
  if(ss){
    const t = treatmentCfg();
    const nLife = (S.eats||[]).length + ((S.sleep||{}).on ? 1 : 0) + ((!famMode() && (S.hours||[]).length) ? 1 : 0);
    const nTreat = !famMode() && t.on ? ((t.medOn && (S.meds||[]).length ? 1 : 0) + (t.outpatientOn ? 1 : 0)) : 0;
    ss.textContent = (nLife + nTreat) ? '설정된 일정 ' + (nLife+nTreat) + '종 · 눌러서 관리' : '생활 · 치료 일정을 한곳에서 관리';
  }
  refreshIcons();
}

function drawScheduleHub(){
  const fam = famMode();
  const life = [];
  if(!fam && (S.hours||[]).length) life.push('위험시간 ' + S.hours.length + '개');
  if((S.eats||[]).length) life.push('식사 ' + S.eats.length + '끼');
  if((S.sleep||{}).on) life.push('잠');
  const ls = $('#schedule-life-s'); if(ls) ls.textContent = life.length ? life.join(' · ') : '위험시간 · 식사 · 잠';
  const tc = $('#schedule-treatment'); if(tc) tc.style.display = fam ? 'none' : '';
  if(!fam){
    const t = treatmentCfg(), parts=[];
    if(t.on && t.medOn && (S.meds||[]).length) parts.push('복약 ' + S.meds.length + '회');
    if(t.on && t.outpatientOn){ const v=treatmentVisitLabel(); parts.push(v || '외래 일정 사용'); }
    const ts=$('#schedule-treatment-s'); if(ts) ts.textContent = parts.length ? parts.join(' · ') : '복약 · 처방 · 외래 · 반복 외래';
  }
  const ns=$('#schedule-notify-s');
  if(ns) ns.textContent = nativeAndroidApp() ? 'Android 예약알림 · 생활 · 치료 알림' : (S.notify ? '알림 사용 중 · 생활 · 치료 알림' : '생활 · 치료 알림 관리');
  refreshIcons();
}

function drawLifeSchedule(){
  const fam=famMode();
  const risk=$('#life-risk'); if(risk) risk.style.display=fam?'none':'';
  if(!fam){
    $('#me-hours-d').textContent = '예전에 ' + riskVerb(S.types) + ' 시간을 골라두면, 그 시간에 앱을 열었을 때 홈 화면에서 먼저 챙겨드립니다.';
    hourChips($('#me-hours'), () => S.hours || [], h => {
      S.hours = S.hours || [];
      const i=S.hours.indexOf(h); if(i<0) S.hours.push(h); else S.hours.splice(i,1);
      save(); drawLifeSchedule();
    });
  }
  drawBody();
  refreshIcons();
}
function drawNotifySchedule(){ drawNotify(); refreshIcons(); }
'''
if s.count(old) != 1:
    raise SystemExit('drawTools anchor not unique')
s = s.replace(old, new, 1)

# 8) My Info no longer renders schedule controls or references removed acc-care-s.
s = s.replace("  /* 가족에게는 '위험한 시간대' 가 없으니 묶음 설명에서도 뺍니다 */\n  $('#acc-care-s').textContent = fam\n    ? '생활 일정 · 알림'\n    : '생활 일정 · 치료 일정 · 알림';\n\n", '', 1)
pat = r'''\n  \$\('#me-hours-d'\)\.textContent =\n    '예전에 ' \+ riskVerb\(S\.types\) \+ ' 시간을 골라두면, 그 시간에 앱을 열었을 때 ' \+\n    '홈 화면에서 먼저 챙겨드립니다\.';\n\n  hourChips\(\$\('#me-hours'\), \(\) => S\.hours \|\| \[\], h => \{.*?\n  /\* V8\.1\.1: 복약 설정은 치료관리 화면에서만 그립니다\. \*/\n  drawBody\(\);\n  drawNotify\(\);\n  drawAdmin\(\);'''
sub1(pat, '\n  drawAdmin();', 'remove schedule rendering from drawMe', re.S)

# 9) New card handlers.
old = "$('#tool-qa').onclick = () => { qaState.selected=0; qaState.cat='전체'; qaState.q=''; qaState.limit=30; go('qa'); };\n$('#tool-learn').onclick = () => go('learn');\n$('#tool-listen').onclick = () => openListen('tools');\n"
new = "$('#tool-qa').onclick = () => { qaState.selected=0; qaState.cat='전체'; qaState.q=''; qaState.limit=30; go('qa'); };\n$('#tool-habit').onclick = () => toast('습관 기능은 준비 중입니다.');\n$('#tool-schedule').onclick = () => go('schedule');\n$('#tool-learn').onclick = () => go('learn');\n$('#tool-workbook').onclick = () => go('workbook-list');\n$('#tool-listen').onclick = () => openListen('tools');\n$('#schedule-life').onclick = () => go('life-schedule');\n$('#schedule-treatment').onclick = () => go('treatment');\n$('#schedule-notify').onclick = () => go('notify-schedule');\n"
if s.count(old) != 1:
    raise SystemExit('tool handlers anchor not unique')
s = s.replace(old, new, 1)

# 10) Version.
if s.count("const BUILD = 'V8.1.3';") != 1:
    raise SystemExit('BUILD anchor not unique')
s = s.replace("const BUILD = 'V8.1.3';", "const BUILD = 'V8.1.4';", 1)

# Guardrails.
checks = [
    '오늘의 실천', 'id="tool-habit"', 'id="tool-schedule"', 'id="tool-workbook"',
    'id="p-schedule"', 'id="p-life-schedule"', 'id="p-notify-schedule"',
    'id="me-hours"', 'id="me-eats"', 'id="me-notify"',
    "if(p === 'schedule') drawScheduleHub();", "$('#schedule-treatment').onclick = () => go('treatment');",
    "const BUILD = 'V8.1.4';"
]
for x in checks:
    if x not in s: raise SystemExit('missing guard: '+x)
if s.count('id="me-hours"') != 1 or s.count('id="me-notify"') != 1:
    raise SystemExit('schedule control IDs duplicated')
if '<b>일정·알림</b><span id="acc-care-s"' in s:
    raise SystemExit('old My Info schedule accordion remains')

p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
if w.count("const APP_VERSION = 'V8.1.3';") != 1: raise SystemExit('sw app version anchor')
w = w.replace("const APP_VERSION = 'V8.1.3';", "const APP_VERSION = 'V8.1.4';", 1)
if w.count("const V = 'ohg-v813-schedulehub';") != 1: raise SystemExit('sw cache anchor')
w = w.replace("const V = 'ohg-v813-schedulehub';", "const V = 'ohg-v814-tools-practice';", 1)
sw.write_text(w, encoding='utf-8')

print('V8.1.4 recovery tools / schedule hub patch PASS')
