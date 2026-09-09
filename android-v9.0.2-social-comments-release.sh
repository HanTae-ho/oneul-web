#!/usr/bin/env bash
set -euo pipefail

# V9.0.2 changes web/social behavior only. Reuse the proven V9.0.1 Android
# native stack and advance package metadata without touching reminder/TTS code.
bash "$GITHUB_WORKSPACE/android-v9.0.1-ai-social-release.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"

sed -i "s/versionCode 895/versionCode 896/; s/versionName '9.0.1'/versionName '9.0.2'/" "$GRADLE"

grep -q "versionCode 896" "$GRADLE"
grep -q "versionName '9.0.2'" "$GRADLE"

# Preserve the proven silent reminder bridge and existing native engines.
grep -q 'handleSilentSync(getIntent())' "$PKG/NotificationSettingsActivity.java"
grep -q '"1".equals(val(u, "clear"))' "$PKG/NotificationSettingsActivity.java"
grep -q '"1".equals(val(u, "apply"))' "$PKG/NotificationSettingsActivity.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'PowerManager.PARTIAL_WAKE_LOCK' "$PKG/RelaxTtsActivity.java"
grep -q 'TextToSpeech.QUEUE_FLUSH' "$PKG/MindProVoiceService.java"

echo 'V9.0.2 Android version-only release patch PASS'
