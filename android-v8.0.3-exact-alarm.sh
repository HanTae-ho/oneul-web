#!/usr/bin/env bash
set -euo pipefail

# Preserve the verified V8.0.2 TWA/status-bar build, then change only reminder timing.
bash "$GITHUB_WORKSPACE/android-v8.0.2-fix.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
GRADLE="$SRC/app/build.gradle"
MANIFEST="$SRC/app/src/main/AndroidManifest.xml"
OVERLAY="$GITHUB_WORKSPACE/android-v8.0.3-overlay"

# Android package version.
sed -i "s/versionCode 802/versionCode 803/; s/versionName '8.0.2'/versionName '8.0.3'/" "$GRADLE"

# Replace only native reminder components.
cp "$OVERLAY/ReminderScheduler.java" "$PKG/ReminderScheduler.java"
cp "$OVERLAY/AlarmReceiver.java" "$PKG/AlarmReceiver.java"
cp "$OVERLAY/BootReceiver.java" "$PKG/BootReceiver.java"
cp "$OVERLAY/NotificationSettingsActivity.java" "$PKG/NotificationSettingsActivity.java"

# Add a distinct notification body for the scheduled screen-off test.
python3 - <<'PY'
from pathlib import Path
import os
p = Path(os.environ['GITHUB_WORKSPACE']) / 'android-v8/app/src/main/java/io/github/hantae_ho/twa/NotificationHelper.java'
s = p.read_text(encoding='utf-8')
needle = '''    static boolean showTest(Context c) {\n        if (!canPost(c)) return false;\n        ensureChannel(c);\n        return post(c, 800001, "시험 알림입니다. 앱을 완전히 닫아도 예약알림은 Android가 보관합니다.");\n    }\n'''
insert = needle + '''\n    static boolean showScheduledTest(Context c) {\n        if (!canPost(c)) return false;\n        ensureChannel(c);\n        return post(c, 800003, "2분 예약 시험 알림입니다. 화면이 꺼진 상태에서도 이 알림이 오면 정확한 시간 알림이 정상입니다.");\n    }\n'''
if needle not in s:
    raise SystemExit('NotificationHelper showTest anchor not found')
s = s.replace(needle, insert, 1)
p.write_text(s, encoding='utf-8')
PY

# Add exact-alarm special access and re-schedule when the user grants it.
python3 - <<'PY'
from pathlib import Path
import os
base = Path(os.environ['GITHUB_WORKSPACE']) / 'android-v8'
manifest = base / 'app/src/main/AndroidManifest.xml'
s = manifest.read_text(encoding='utf-8')
perm = '    <uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" />\n'
anchor = '    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />\n'
if 'android.permission.SCHEDULE_EXACT_ALARM' not in s:
    if anchor not in s:
        raise SystemExit('manifest permission anchor not found')
    s = s.replace(anchor, anchor + perm, 1)
receiver_anchor = '                <action android:name="android.intent.action.MY_PACKAGE_REPLACED" />\n'
exact_action = '                <action android:name="android.app.action.SCHEDULE_EXACT_ALARM_PERMISSION_STATE_CHANGED" />\n'
if 'SCHEDULE_EXACT_ALARM_PERMISSION_STATE_CHANGED' not in s:
    if receiver_anchor not in s:
        raise SystemExit('BootReceiver action anchor not found')
    s = s.replace(receiver_anchor, receiver_anchor + exact_action, 1)
manifest.write_text(s, encoding='utf-8')

app = base / 'app/src/main/java/io/github/hantae_ho/twa/Application.java'
a = app.read_text(encoding='utf-8')
needle = '        NotificationHelper.ensureChannel(this);\n'
if 'ReminderScheduler.scheduleAll(this);' not in a:
    if needle not in a:
        raise SystemExit('Application anchor not found')
    a = a.replace(needle, needle + '        ReminderScheduler.scheduleAll(this);\n', 1)
app.write_text(a, encoding='utf-8')
PY

# Guardrails: V8.0.2 TWA recovery must remain intact; exact alarm changes must be present.
grep -q "versionCode 803" "$GRADLE"
grep -q "versionName '8.0.3'" "$GRADLE"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$MANIFEST"
grep -q 'STATUS_BAR_COLOR' "$MANIFEST"
grep -q 'android:name=".LauncherActivity"' "$MANIFEST"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'canScheduleExactAlarms' "$PKG/ReminderScheduler.java"
grep -q 'ACTION_REQUEST_SCHEDULE_EXACT_ALARM' "$PKG/NotificationSettingsActivity.java"
grep -q '2분 뒤 예약 시험' "$PKG/NotificationSettingsActivity.java"
! grep -R "?native=1" -n "$SRC/app/src/main" || exit 1
