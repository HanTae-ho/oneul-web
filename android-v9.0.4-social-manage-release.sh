#!/usr/bin/env bash
set -euo pipefail

# V9.0.4 changes web/social profile management and nickname reuse policy only.
# Reuse the proven V9.0.3 native reminder/TTS stack and advance package metadata.
bash "$GITHUB_WORKSPACE/android-v9.0.3-social-profile-release.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"

sed -i "s/versionCode 898/versionCode 899/; s/versionName '9.0.3'/versionName '9.0.4'/" "$GRADLE"

grep -q "versionCode 899" "$GRADLE"
grep -q "versionName '9.0.4'" "$GRADLE"

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

echo 'V9.0.4 Android versionCode 899 release patch PASS'
