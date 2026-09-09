#!/usr/bin/env bash
set -euo pipefail

# V9.0.1 keeps the V9.0 / physically verified V8.5 native reminder/TTS stack
# unchanged. Web behavior is served by the V9.0.1 main app; this patch only
# advances Android package metadata for the V9.0.1 test build.
bash "$GITHUB_WORKSPACE/android-v9.0-social-stage1-release.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"

sed -i "s/versionCode 893/versionCode 894/; s/versionName '9.0'/versionName '9.0.1'/" "$GRADLE"

grep -q "versionCode 894" "$GRADLE"
grep -q "versionName '9.0.1'" "$GRADLE"

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

echo 'V9.0.1 Android version-only release patch PASS'
