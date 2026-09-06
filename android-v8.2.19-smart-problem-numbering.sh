#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.18 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.18-smart-accordion.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 838" "$GRADLE"
grep -q "versionName '8.2.18'" "$GRADLE"
sed -i "s/versionCode 838/versionCode 839/; s/versionName '8.2.18'/versionName '8.2.19'/" "$GRADLE"

grep -q "versionCode 839" "$GRADLE"
grep -q "versionName '8.2.19'" "$GRADLE"
echo 'V8.2.19 Android version-only patch PASS'
