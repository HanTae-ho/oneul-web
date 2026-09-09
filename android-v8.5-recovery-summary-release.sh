#!/usr/bin/env bash
set -euo pipefail

# V8.5 adds a web/local recovery summary and fixed install-guide page.
# Reuse the physically verified V8.4 Android native reminder/TTS stack unchanged
# and only advance Android package metadata.
bash "$GITHUB_WORKSPACE/android-v8.4-relationship-context-release.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"

sed -i "s/versionCode 891/versionCode 892/; s/versionName '8.4'/versionName '8.5'/" "$GRADLE"

grep -q "versionCode 892" "$GRADLE"
grep -q "versionName '8.5'" "$GRADLE"

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

echo 'V8.5 Android version-only release patch PASS'
