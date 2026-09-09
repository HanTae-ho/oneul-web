#!/usr/bin/env bash
set -euo pipefail

# V8.4 is a web/local-record relationship-context change.
# Reuse the verified V8.3 Android native reminder/TTS stack unchanged and only advance package metadata.
bash "$GITHUB_WORKSPACE/android-v8.3-recovery-patterns-release.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"

sed -i "s/versionCode 890/versionCode 891/; s/versionName '8.3'/versionName '8.4'/" "$GRADLE"

grep -q "versionCode 891" "$GRADLE"
grep -q "versionName '8.4'" "$GRADLE"

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

echo 'V8.4 Android version-only release patch PASS'
