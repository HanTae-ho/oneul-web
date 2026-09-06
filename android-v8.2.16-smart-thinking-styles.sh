#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.15 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.15-smart-dibs.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 835" "$GRADLE"
grep -q "versionName '8.2.15'" "$GRADLE"
sed -i "s/versionCode 835/versionCode 836/; s/versionName '8.2.15'/versionName '8.2.16'/" "$GRADLE"

grep -q "versionCode 836" "$GRADLE"
grep -q "versionName '8.2.16'" "$GRADLE"
echo 'V8.2.16 Android version-only patch PASS'
