#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.11 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.11-smart-tools-hub.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 831" "$GRADLE"
grep -q "versionName '8.2.11'" "$GRADLE"
sed -i "s/versionCode 831/versionCode 832/; s/versionName '8.2.11'/versionName '8.2.12'/" "$GRADLE"

grep -q "versionCode 832" "$GRADLE"
grep -q "versionName '8.2.12'" "$GRADLE"
echo 'V8.2.12 Android version-only patch PASS'
