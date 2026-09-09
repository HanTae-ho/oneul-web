#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.1.7 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.1.7-home-polish.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 817" "$GRADLE"
grep -q "versionName '8.1.7'" "$GRADLE"
sed -i "s/versionCode 817/versionCode 818/; s/versionName '8.1.7'/versionName '8.1.8'/" "$GRADLE"

grep -q "versionCode 818" "$GRADLE"
grep -q "versionName '8.1.8'" "$GRADLE"
echo 'V8.1.8 Android version-only patch PASS'
