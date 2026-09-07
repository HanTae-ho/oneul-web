from pathlib import Path

# V8.2.44 focused patch, rerun after validation workflow correction.
ROOT = Path(__file__).resolve().parent
idx_p = ROOT / 'index.html'
readme_p = ROOT / 'README.md'
sw_p = ROOT / 'sw.js'

idx = idx_p.read_text(encoding='utf-8')
readme = readme_p.read_text(encoding='utf-8')
sw = sw_p.read_text(encoding='utf-8')


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 anchor, found {n}')
    return text.replace(old, new, 1)

# V8.2.44 intentionally starts from the verified V8.2.42 tree.
idx = replace_once(idx, "const BUILD = 'V8.2.42';", "const BUILD = 'V8.2.44';", 'BUILD')

# Habit: add only the final native-reminder handoff. Do not recreate the V8.2.43 web intermediate page flow.
habit_old = '''  <div id="habit-templates" class="hide"></div>\n</section>'''
habit_new = '''  <div id="habit-templates" class="hide"></div>\n  <div class="note" style="margin-top:14px">\n    습관 시간을 정했다면 실제 알림 예약을 확인해 주세요.\n    <div style="height:8px"></div>\n    <button class="btn sec sm" type="button" onclick="openScheduleReminderSettings()">알림 설정 확인 →</button>\n  </div>\n</section>'''
idx = replace_once(idx, habit_old, habit_new, 'habit reminder link')

# Life schedule: direct handoff after the schedule settings.
life_old = '''    <div id="me-sleep" style="margin-top:11px"></div>\n  </div>\n</section>\n\n<section class="pg" id="p-notify-schedule">'''
life_new = '''    <div id="me-sleep" style="margin-top:11px"></div>\n  </div>\n  <div class="note" style="margin-top:14px">\n    생활 일정을 정했다면 실제 알림 예약을 확인해 주세요.\n    <div style="height:8px"></div>\n    <button class="btn sec sm" type="button" onclick="openScheduleReminderSettings()">알림 설정 확인 →</button>\n  </div>\n</section>\n\n<section class="pg" id="p-notify-schedule">'''
idx = replace_once(idx, life_old, life_new, 'life reminder link')

# Treatment schedule: direct handoff after medication/outpatient settings.
treat_old = '''  <div id="treat-master"></div>\n  <div id="treat-body"></div>\n</section>\n\n<!-- ══════════ 내 발자취 ══════════ -->'''
treat_new = '''  <div id="treat-master"></div>\n  <div id="treat-body"></div>\n  <div class="note" style="margin-top:14px">\n    복약·외래 일정을 정했다면 실제 알림 예약을 확인해 주세요.\n    <div style="height:8px"></div>\n    <button class="btn sec sm" type="button" onclick="openScheduleReminderSettings()">알림 설정 확인 →</button>\n  </div>\n</section>\n\n<!-- ══════════ 내 발자취 ══════════ -->'''
idx = replace_once(idx, treat_old, treat_new, 'treatment reminder link')

# Centralize the navigation rule: Android -> native AlarmManager settings directly.
open_old = '''function openNativeReminderSettings(){\n  const p = nativeReminderPayload();\n  const q = new URLSearchParams();\n  Object.keys(p).forEach(k => q.set(k, p[k]));\n  /* package를 명시해 다른 앱이 oneul 스킴을 가로채지 못하게 합니다. */\n  const u = 'intent://reminders?' + q.toString() +\n    '#Intent;scheme=oneul;package=io.github.hantae_ho.twa;end';\n  location.href = u;\n}\n\nfunction drawNotify(){'''
open_new = '''function openNativeReminderSettings(){\n  const p = nativeReminderPayload();\n  const q = new URLSearchParams();\n  Object.keys(p).forEach(k => q.set(k, p[k]));\n  /* package를 명시해 다른 앱이 oneul 스킴을 가로채지 못하게 합니다. */\n  const u = 'intent://reminders?' + q.toString() +\n    '#Intent;scheme=oneul;package=io.github.hantae_ho.twa;end';\n  location.href = u;\n}\nfunction openScheduleReminderSettings(){\n  /* Android 앱은 웹 알림설정 화면을 거치지 않고 네이티브 예약알림 화면으로 직행합니다. */\n  if(nativeAndroidApp()){ openNativeReminderSettings(); return; }\n  go('notify-schedule');\n}\n\nfunction drawNotify(){'''
idx = replace_once(idx, open_old, open_new, 'native reminder helper')

handler_old = "$('#schedule-notify').onclick = () => { if(nativeAndroidApp()) openNativeReminderSettings(); else go('notify-schedule'); };"
handler_new = "$('#schedule-notify').onclick = openScheduleReminderSettings;"
idx = replace_once(idx, handler_old, handler_new, 'schedule notify handler')

# Guard against accidentally reintroducing the V8.2.43 regression state.
for bad in ('NOTIFY_REVIEW_KEY', 'schedule-notify-flag', 'notifyNeedsReview()', 'markNotifyReviewed()'):
    if bad in idx:
        raise SystemExit(f'V8.2.43 regression token remains: {bad}')

# Service worker version/cache.
sw = replace_once(sw, "const APP_VERSION = 'V8.2.42';", "const APP_VERSION = 'V8.2.44';", 'APP_VERSION')
sw = replace_once(sw, "const V = 'ohg-v8242-practice-card-polish';", "const V = 'ohg-v8244-native-notify-direct';", 'cache key')

section = '''# V8.2.44 — Android 알림설정 네이티브 직행\n\n- V8.2.42 정상본(`65469cae…`)에서 다시 시작했습니다. V8.2.43에서 추가된 웹 알림설정 중간화면/확인상태 추적은 가져오지 않습니다.\n- `일정·알림 > 알림 설정`은 V8.2.42와 동일하게 Android 네이티브 예약알림 화면으로 바로 이동합니다.\n- 습관·생활 일정·치료 일정 화면 하단의 `알림 설정 확인 →`도 같은 네이티브 예약알림 화면으로 바로 이동합니다. Android 앱에서는 웹 `알림 설정` 중간화면을 거치지 않습니다.\n- 기존 AlarmManager 정확알림, 화면 OFF 알림, 부팅 후 재예약, 외래 반복예약, 이완 TTS 네이티브 엔진은 변경하지 않습니다.\n- 기록 저장형식, `DATA_SCHEMA=6`, `ohg.v1`은 변경하지 않습니다.\n\n'''
if not readme.startswith('# V8.2.44'):
    readme = section + readme
else:
    raise SystemExit('README already has V8.2.44')

# Final structural assertions.
if idx.count('onclick="openScheduleReminderSettings()"') != 3:
    raise SystemExit('expected exactly 3 detail-screen direct reminder buttons')
if "$('#schedule-notify').onclick = openScheduleReminderSettings;" not in idx:
    raise SystemExit('schedule hub direct handler missing')
if "const DATA_SCHEMA = 6;" not in idx or "const KEY = 'ohg.v1';" not in idx:
    raise SystemExit('storage invariants changed')

idx_p.write_text(idx, encoding='utf-8')
readme_p.write_text(readme, encoding='utf-8')
sw_p.write_text(sw, encoding='utf-8')
print('V8.2.44 native notification direct patch: PASS')
