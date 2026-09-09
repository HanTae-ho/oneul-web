#!/usr/bin/env bash
set -euo pipefail

# Start from the verified V8.1.3 native schedule-hub build.
bash "$GITHUB_WORKSPACE/android-v8.1.3-schedule-hub.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"

# V8.1.4 is a web information-architecture update. Native reminder logic is unchanged.
sed -i "s/versionCode 813/versionCode 814/; s/versionName '8.1.3'/versionName '8.1.4'/" "$GRADLE"

grep -q "versionCode 814" "$GRADLE"
grep -q "versionName '8.1.4'" "$GRADLE"
grep -q 'TextView title = text("일정·알림"' "$PKG/NotificationSettingsActivity.java"
grep -q 'TreatmentReminderStore' "$PKG/NotificationSettingsActivity.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$SRC/app/src/main/AndroidManifest.xml"

echo 'V8.1.4 Android version-only patch PASS'
