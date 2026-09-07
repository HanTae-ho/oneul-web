#!/usr/bin/env bash
set -euo pipefail

# V8.2.44 Android is a version-only rebuild of the verified V8.2.42 native stack.
# The notification direct-routing change is web-side; AlarmManager/TTS code must remain unchanged.
bash "$GITHUB_WORKSPACE/android-v8.2.42-practice-card-polish.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
MAN="$SRC/app/src/main/AndroidManifest.xml"

sed -i "s/versionCode 862/versionCode 864/; s/versionName '8.2.42'/versionName '8.2.44'/" "$GRADLE"

grep -q "versionCode 864" "$GRADLE"
grep -q "versionName '8.2.44'" "$GRADLE"
grep -q 'android.permission.WAKE_LOCK' "$MAN"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$MAN"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'HabitReminderScheduler.scheduleAll' "$PKG/BootReceiver.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'PowerManager.PARTIAL_WAKE_LOCK' "$PKG/RelaxTtsActivity.java"
grep -q 'oneul://relax' "$GITHUB_WORKSPACE/android-v8.2.28-native-relax-tts.sh"

echo 'V8.2.44 Android version-only rebuild from V8.2.42 native stack: PASS'
