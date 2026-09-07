#!/usr/bin/env bash
set -euo pipefail

# V8.2.46 keeps the verified V8.2.45 native notification/TTS stack unchanged.
# This release only advances the Android package version for the V8.2.46 web UI update.
bash "$GITHUB_WORKSPACE/android-v8.2.45-mobile-scroll.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
MAN="$SRC/app/src/main/AndroidManifest.xml"

sed -i "s/versionCode 865/versionCode 866/; s/versionName '8.2.45'/versionName '8.2.46'/" "$GRADLE"

grep -q "versionCode 866" "$GRADLE"
grep -q "versionName '8.2.46'" "$GRADLE"
grep -q 'android.permission.WAKE_LOCK' "$MAN"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$MAN"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'HabitReminderScheduler.scheduleAll' "$PKG/BootReceiver.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'PowerManager.PARTIAL_WAKE_LOCK' "$PKG/RelaxTtsActivity.java"

echo 'V8.2.46 Android version-only rebuild from V8.2.45 native stack: PASS'
