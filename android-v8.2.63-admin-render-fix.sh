#!/usr/bin/env bash
set -euo pipefail

# Reuse the verified V8.2.62 native stack unchanged.
bash "$GITHUB_WORKSPACE/android-v8.2.62-me-menu-back.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
MAN="$SRC/app/src/main/AndroidManifest.xml"

grep -q "versionCode 882" "$GRADLE"
grep -q "versionName '8.2.62'" "$GRADLE"
sed -i "s/versionCode 882/versionCode 883/; s/versionName '8.2.62'/versionName '8.2.63'/" "$GRADLE"

grep -q "versionCode 883" "$GRADLE"
grep -q "versionName '8.2.63'" "$GRADLE"
grep -q 'android.permission.WAKE_LOCK' "$MAN"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$MAN"
grep -q 'android:name=".MindProVoiceService"' "$MAN"
grep -q 'android:name=".MindProVoiceBridgeActivity"' "$MAN"
grep -q 'TextToSpeech.QUEUE_FLUSH' "$PKG/MindProVoiceService.java"
grep -q 'PowerManager.PARTIAL_WAKE_LOCK' "$PKG/RelaxTtsActivity.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'HabitReminderScheduler.scheduleAll' "$PKG/BootReceiver.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"

echo 'V8.2.63 version-only rebuild from verified V8.2.62 native stack: PASS'
