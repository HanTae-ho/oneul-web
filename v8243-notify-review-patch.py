from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def rep(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'MISSING: {label}')
    if s.count(old) != 1:
        raise SystemExit(f'AMBIGUOUS {label}: {s.count(old)}')
    s = s.replace(old, new, 1)

# Version
rep("const BUILD = 'V8.2.42';", "const BUILD = 'V8.2.43';", 'BUILD')

# Schedule card attention style.
rep(
"  .schedulecard .go{font-size:18px;color:var(--faint)}\n",
"  .schedulecard .go{font-size:18px;color:var(--faint)}\n"
"  .schedulecard.attn{border-color:var(--acc);background:var(--accbg)}\n"
"  .schedulecard.attn .go{color:var(--acc)}\n"
"  .notify-flag{display:inline-block;margin-left:6px;padding:2px 7px;border-radius:99px;background:var(--acc);color:#fff;font-size:10.5px;font-weight:700;vertical-align:1px}\n",
'schedule CSS')

# Habit -> notification settings connection.
rep(
"  <div id=\"habit-templates\" class=\"hide\"></div>\n</section>\n\n<section class=\"pg\" id=\"p-habit-edit\">",
"  <div id=\"habit-templates\" class=\"hide\"></div>\n"
"  <div class=\"note\" style=\"margin-top:14px\">\n"
"    습관의 시간이나 알림을 바꿨다면 알림 설정에서 예약을 확인해 주세요.\n"
"    <div style=\"height:8px\"></div>\n"
"    <button class=\"btn sec sm\" type=\"button\" onclick=\"go('notify-schedule')\">알림 설정 확인 →</button>\n"
"  </div>\n"
"</section>\n\n<section class=\"pg\" id=\"p-habit-edit\">",
'habit notify link')

# Schedule hub badge.
rep(
"      <span class=\"b\"><b>알림 설정</b><span id=\"schedule-notify-s\">습관 · 생활 · 치료 알림 관리</span></span><span class=\"go\">›</span>",
"      <span class=\"b\"><b>알림 설정 <span class=\"notify-flag hide\" id=\"schedule-notify-flag\">확인 필요</span></b><span id=\"schedule-notify-s\">습관 · 생활 · 치료 알림 관리</span></span><span class=\"go\">›</span>",
'notify badge')

# Life schedule -> notification settings connection.
rep(
"    <div id=\"me-sleep\" style=\"margin-top:11px\"></div>\n  </div>\n</section>\n\n<section class=\"pg\" id=\"p-notify-schedule\">",
"    <div id=\"me-sleep\" style=\"margin-top:11px\"></div>\n  </div>\n"
"  <div class=\"note\" style=\"margin-top:14px\">\n"
"    생활 일정을 바꿨다면 알림 설정에서 예약을 확인해 주세요.\n"
"    <div style=\"height:8px\"></div>\n"
"    <button class=\"btn sec sm\" type=\"button\" onclick=\"go('notify-schedule')\">알림 설정 확인 →</button>\n"
"  </div>\n"
"</section>\n\n<section class=\"pg\" id=\"p-notify-schedule\">",
'life notify link')

# Treatment -> notification settings connection.
rep(
"  <div id=\"treat-master\"></div>\n  <div id=\"treat-body\"></div>\n</section>\n\n<!-- ══════════ 내 발자취 ══════════ -->",
"  <div id=\"treat-master\"></div>\n  <div id=\"treat-body\"></div>\n"
"  <div class=\"note\" style=\"margin-top:14px\">\n"
"    복약·외래 일정을 바꿨다면 알림 설정에서 예약을 확인해 주세요.\n"
"    <div style=\"height:8px\"></div>\n"
"    <button class=\"btn sec sm\" type=\"button\" onclick=\"go('notify-schedule')\">알림 설정 확인 →</button>\n"
"  </div>\n"
"</section>\n\n<!-- ══════════ 내 발자취 ══════════ -->",
'treatment notify link')

# Fingerprint of the schedule actually passed to Android. Stored separately from recovery records.
marker = "function drawScheduleHub(){\n"
insert = r'''const NOTIFY_REVIEW_KEY = 'ohg.notify.review.v1';
function notifyPlanSignature(){
  const rawHabits=Array.isArray(S.habits)?S.habits:[];
  const habits=rawHabits.map(h=>({
    id:String(h.id||''),name:String(h.name||''),check:String(h.check||''),days:+h.days||0,
    freq:String(h.freq||''),weekdays:(h.weekdays||[]).slice().map(Number).sort((a,b)=>a-b),
    start:String(h.start||''),notify:h.notify?1:0,time:String(h.time||'')
  })).sort((a,b)=>a.id.localeCompare(b.id));
  const eats=(S.eats||[]).map(x=>({s:String(x.s||''),t:String(x.t||'')})).sort((a,b)=>a.s.localeCompare(b.s));
  const meds=(S.meds||[]).map(x=>({s:String(x.s||''),t:String(x.t||'')})).sort((a,b)=>a.s.localeCompare(b.s));
  const sp=S.sleep||{};
  const t=(S.treat && typeof S.treat==='object' && !Array.isArray(S.treat))?S.treat:{};
  return JSON.stringify({
    role:famMode()?'family':'self',
    habits,
    hours:(famMode()?[]:(S.hours||[])).slice().map(Number).sort((a,b)=>a-b),
    eats,
    sleep:{on:sp.on?1:0,bed:String(sp.bed||''),up:String(sp.up||'')},
    treatment:famMode()?null:{
      medOn:t.medOn?1:0,medCnt:+S.medCnt||0,meds,
      outpatientOn:t.outpatientOn?1:0,lastVisit:String(t.lastVisit||''),rxDays:+t.rxDays||0,
      intervalDays:+(t.intervalDays==null?t.rxDays:t.intervalDays)||0,nextVisit:String(t.nextVisit||'')
    }
  });
}
function notifyReviewStored(){
  try{return localStorage.getItem(NOTIFY_REVIEW_KEY)||'';}catch(_){return '';}
}
function markNotifyReviewed(){
  if(!nativeAndroidApp()) return;
  try{localStorage.setItem(NOTIFY_REVIEW_KEY,notifyPlanSignature());}catch(_){}
}
function ensureNotifyReviewBaseline(){
  if(!nativeAndroidApp()) return;
  if(!notifyReviewStored()) markNotifyReviewed();
}
function notifyNeedsReview(){
  if(!nativeAndroidApp()) return false;
  const prev=notifyReviewStored();
  return !!prev && prev!==notifyPlanSignature();
}
ensureNotifyReviewBaseline();

function drawScheduleHub(){
'''
rep(marker, insert, 'notification signature')

# Update hub status based on fingerprint.
rep(
"  const ns=$('#schedule-notify-s');\n  if(ns) ns.textContent = nativeAndroidApp() ? 'Android 예약알림 · 습관 · 생활 · 치료' : (S.notify ? '알림 사용 중 · 습관 · 생활 · 치료' : '습관 · 생활 · 치료 알림 관리');\n  refreshIcons();",
"  const ns=$('#schedule-notify-s'), nc=$('#schedule-notify'), nf=$('#schedule-notify-flag');\n"
"  const pending=notifyNeedsReview();\n"
"  if(nc) nc.classList.toggle('attn',pending);\n"
"  if(nf) nf.classList.toggle('hide',!pending);\n"
"  if(ns) ns.textContent = pending ? '변경한 일정이 있습니다 · 알림 예약 확인 필요' : (nativeAndroidApp() ? 'Android 예약알림 · 습관 · 생활 · 치료' : (S.notify ? '알림 사용 중 · 습관 · 생활 · 치료' : '습관 · 생활 · 치료 알림 관리'));\n"
"  refreshIcons();",
'hub pending state')

# Clear the review-needed state when the user actually opens Android reminder settings.
rep(
"function openNativeReminderSettings(){\n  const p = nativeReminderPayload();",
"function openNativeReminderSettings(){\n  markNotifyReviewed();\n  const p = nativeReminderPayload();",
'native settings reviewed')

p.write_text(s, encoding='utf-8')

# Service worker version/cache.
sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
if "const APP_VERSION = 'V8.2.42';" not in w:
    raise SystemExit('MISSING sw APP_VERSION')
w = w.replace("const APP_VERSION = 'V8.2.42';", "const APP_VERSION = 'V8.2.43';", 1)
if "const V = 'ohg-v8242-practice-card-polish';" not in w:
    raise SystemExit('MISSING sw cache key')
w = w.replace("const V = 'ohg-v8242-practice-card-polish';", "const V = 'ohg-v8243-notify-review-flow';", 1)
sw.write_text(w, encoding='utf-8')

# README release note.
rp=Path('README.md')
r=rp.read_text(encoding='utf-8')
head="""# V8.2.43 — 일정 변경 후 알림 확인 동선 보강\n\n- 습관·생활·치료 일정은 기존처럼 먼저 저장하고, Android 예약알림은 `알림 설정`에서 최종 확인하는 구조를 유지합니다.\n- 일정 설정이 마지막으로 알림을 확인한 상태와 달라지면 `일정 · 알림` 허브의 `알림 설정` 카드에 `확인 필요`를 표시합니다.\n- 습관·생활 일정·치료 일정 화면 하단에서 `알림 설정 확인 →`으로 바로 이어집니다.\n- Android 예약알림 설정을 열면 현재 일정 기준으로 확인 상태를 갱신합니다. 별도 UI 상태 키만 사용하며 개인 회복기록 스키마는 변경하지 않습니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, 정확알림·화면 OFF 알림·부팅 후 재예약·이완 TTS 네이티브 엔진은 변경하지 않습니다.\n\n"""
rp.write_text(head+r, encoding='utf-8')
print('V8.2.43 patch applied')
