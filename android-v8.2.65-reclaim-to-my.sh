#!/usr/bin/env bash
set -euo pipefail

# Reuse the verified V8.2.64 native stack unchanged.
bash "$GITHUB_WORKSPACE/android-v8.2.64-reclaimed-summary.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
MAN="$SRC/app/src/main/AndroidManifest.xml"

grep -q "versionCode 884" "$GRADLE"
grep -q "versionName '8.2.64'" "$GRADLE"
sed -i "s/versionCode 884/versionCode 885/; s/versionName '8.2.64'/versionName '8.2.65'/" "$GRADLE"

grep -q "versionCode 885" "$GRADLE"
grep -q "versionName '8.2.65'" "$GRADLE"
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

echo 'V8.2.65 version-only rebuild from verified V8.2.64 native stack: PASS'
