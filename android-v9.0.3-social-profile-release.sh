#!/usr/bin/env bash
set -euo pipefail

# V9.0.3 changes web/social UI and server behavior only. Reuse the proven
# V9.0.2 social-4 native reminder/TTS stack and advance package metadata.
bash "$GITHUB_WORKSPACE/android-v9.0.2-social4-refresh-release.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"

sed -i "s/versionCode 897/versionCode 898/; s/versionName '9.0.2'/versionName '9.0.3'/" "$GRADLE"

grep -q "versionCode 898" "$GRADLE"
grep -q "versionName '9.0.3'" "$GRADLE"

# Preserve the proven silent reminder bridge and native engines.
grep -q 'handleSilentSync(getIntent())' "$PKG/NotificationSettingsActivity.java"
grep -q '"1".equals(val(u, "clear"))' "$PKG/NotificationSettingsActivity.java"
grep -q '"1".equals(val(u, "apply"))' "$PKG/NotificationSettingsActivity.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'PowerManager.PARTIAL_WAKE_LOCK' "$PKG/RelaxTtsActivity.java"
grep -q 'TextToSpeech.QUEUE_FLUSH' "$PKG/MindProVoiceService.java"

echo 'V9.0.3 Android versionCode 898 release patch PASS'
