#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.19 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.19-smart-problem-numbering.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 839" "$GRADLE"
grep -q "versionName '8.2.19'" "$GRADLE"
sed -i "s/versionCode 839/versionCode 840/; s/versionName '8.2.19'/versionName '8.2.20'/" "$GRADLE"

grep -q "versionCode 840" "$GRADLE"
grep -q "versionName '8.2.20'" "$GRADLE"
echo 'V8.2.20 Android version-only patch PASS'
