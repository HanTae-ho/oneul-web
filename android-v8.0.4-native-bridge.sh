#!/usr/bin/env bash
set -euo pipefail

# Preserve all verified V8.0.3 TWA/status-bar/exact-alarm behavior.
bash "$GITHUB_WORKSPACE/android-v8.0.3-exact-alarm.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
MANIFEST="$SRC/app/src/main/AndroidManifest.xml"

# V8.0.4 changes only the package version. The live web now recognizes #native=1.
sed -i "s/versionCode 803/versionCode 804/; s/versionName '8.0.3'/versionName '8.0.4'/" "$GRADLE"

# Guardrails: keep the working hash marker and all exact-alarm/TWA fixes.
grep -q "versionCode 804" "$GRADLE"
grep -q "versionName '8.0.4'" "$GRADLE"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$MANIFEST"
grep -q 'STATUS_BAR_COLOR' "$MANIFEST"
grep -q 'android:name=".LauncherActivity"' "$MANIFEST"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'ACTION_REQUEST_SCHEDULE_EXACT_ALARM' "$PKG/NotificationSettingsActivity.java"
grep -q '#native=1' "$PKG/LauncherActivity.java"
! grep -R "?native=1" -n "$SRC/app/src/main" || exit 1
