#!/usr/bin/env bash
set -euo pipefail

# V8.2.69: reuse the verified V8.2.68 native reminder/TTS stack unchanged.
# This patch only advances Android package version metadata for the V8.2.69 web release.
bash "$GITHUB_WORKSPACE/android-v8.2.68-reminder-sync.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"

sed -i "s/versionCode 888/versionCode 889/; s/versionName '8.2.68'/versionName '8.2.69'/" "$GRADLE"

grep -q "versionCode 889" "$GRADLE"
grep -q "versionName '8.2.69'" "$GRADLE"

# Preserve the V8.2.68 reminder bridge and all existing native engines.
grep -q 'handleSilentSync(getIntent())' "$PKG/NotificationSettingsActivity.java"
grep -q '"1".equals(val(u, "clear"))' "$PKG/NotificationSettingsActivity.java"
grep -q '"1".equals(val(u, "apply"))' "$PKG/NotificationSettingsActivity.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'PowerManager.PARTIAL_WAKE_LOCK' "$PKG/RelaxTtsActivity.java"
grep -q 'TextToSpeech.QUEUE_FLUSH' "$PKG/MindProVoiceService.java"

echo 'V8.2.69 Android version-only release patch PASS'
