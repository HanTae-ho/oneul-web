#!/usr/bin/env bash
set -euo pipefail

# Start from the verified V8.1.2 recurring outpatient reminder build.
bash "$GITHUB_WORKSPACE/android-v8.1.2-recurring.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
GRADLE="$SRC/app/build.gradle"

# UI-only native follow-up: keep all V8.1.2 reminder stores/schedulers intact.
sed -i "s/versionCode 812/versionCode 813/; s/versionName '8.1.2'/versionName '8.1.3'/" "$GRADLE"

python3 - <<'PY'
from pathlib import Path
import os
p = Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main/java/io/github/hantae_ho/twa/NotificationSettingsActivity.java'
s = p.read_text(encoding='utf-8')
repls = [
    ('TextView title = text("예약 알림", 27, true);', 'TextView title = text("일정·알림", 27, true);'),
    ('TextView intro = text("복약·식사·잠과 외래 일정 알림은 Android가 기기 안에서 예약합니다. 서버로 일정이나 회복기록을 보내지 않습니다.", 16, false);',
     'TextView intro = text("생활 일정과 치료 일정 알림은 Android가 기기 안에서 예약합니다. 서버로 일정이나 회복기록을 보내지 않습니다.", 16, false);'),
    ('enabledSwitch.setText("예약 알림 사용");', 'enabledSwitch.setText("일정·알림 사용");'),
    ('Toast.makeText(this, "예약알림 설정을 저장했습니다.", Toast.LENGTH_SHORT).show();',
     'Toast.makeText(this, "일정·알림 설정을 저장했습니다.", Toast.LENGTH_SHORT).show();')
]
for old, new in repls:
    if s.count(old) != 1:
        raise SystemExit('Native schedule hub anchor mismatch: '+old[:60])
    s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
PY

# Guardrails: V8.1.2 native scheduling logic must remain unchanged.
grep -q "versionCode 813" "$GRADLE"
grep -q "versionName '8.1.3'" "$GRADLE"
grep -q 'TextView title = text("일정·알림"' "$PKG/NotificationSettingsActivity.java"
grep -q '생활 일정과 치료 일정 알림은 Android가 기기 안에서 예약합니다' "$PKG/NotificationSettingsActivity.java"
grep -q 'TreatmentReminderStore' "$PKG/NotificationSettingsActivity.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'while (when <= System.currentTimeMillis()' "$PKG/TreatmentReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$SRC/app/src/main/AndroidManifest.xml"

echo 'V8.1.3 Android schedule hub UI patch PASS'
