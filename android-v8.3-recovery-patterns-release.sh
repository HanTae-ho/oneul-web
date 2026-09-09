#!/usr/bin/env bash
set -euo pipefail

# V8.3: reuse the verified V8.2.69 Android native reminder/TTS stack unchanged.
# V8.3 itself is a web/local-record analysis change, so Android only advances package metadata.
bash "$GITHUB_WORKSPACE/android-v8.2.69-ui-release.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"

sed -i "s/versionCode 889/versionCode 890/; s/versionName '8.2.69'/versionName '8.3'/" "$GRADLE"

grep -q "versionCode 890" "$GRADLE"
grep -q "versionName '8.3'" "$GRADLE"

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

echo 'V8.3 Android version-only release patch PASS'
