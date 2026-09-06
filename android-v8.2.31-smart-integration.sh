#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.30 native stack unchanged.
bash "$GITHUB_WORKSPACE/android-v8.2.30-smart-health.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
JAVA="$PKG/RelaxTtsActivity.java"
MANIFEST="$SRC/app/src/main/AndroidManifest.xml"

# V8.2.31 is web-only. Native code stays unchanged; package version only.
grep -q "versionCode 850" "$GRADLE"
grep -q "versionName '8.2.30'" "$GRADLE"
sed -i "s/versionCode 850/versionCode 851/; s/versionName '8.2.30'/versionName '8.2.31'/" "$GRADLE"

# Guardrails: V8.2.29 relaxation TTS and all reminder engines must remain intact.
grep -q "versionCode 851" "$GRADLE"
grep -q "versionName '8.2.31'" "$GRADLE"
grep -q 'android.permission.WAKE_LOCK' "$MANIFEST"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$MANIFEST"
grep -q 'android:name=".RelaxTtsActivity"' "$MANIFEST"
grep -q 'android:scheme="oneul" android:host="relax"' "$MANIFEST"
grep -q 'speech_rate_tenths' "$JAVA"
grep -q '느리게 · 0.7배' "$JAVA"
grep -q '차분하게 · 0.8배 · 기본' "$JAVA"
grep -q '조금 빠르게 · 0.9배' "$JAVA"
grep -q '보통 · 1.0배' "$JAVA"
grep -q 'prefs.edit().putInt(PREF_RATE' "$JAVA"
grep -q 'tts.setSpeechRate(speechRateTenths / 10.0f)' "$JAVA"
grep -q 'PowerManager.PARTIAL_WAKE_LOCK' "$JAVA"
grep -q 'releaseWakeLock' "$JAVA"
grep -q 'HabitReminderScheduler.scheduleAll' "$PKG/BootReceiver.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"

echo 'V8.2.31 Android version-only patch PASS'
