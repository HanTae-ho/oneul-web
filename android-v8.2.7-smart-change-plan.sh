#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.6 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.6-smart-cba.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 826" "$GRADLE"
grep -q "versionName '8.2.6'" "$GRADLE"
sed -i "s/versionCode 826/versionCode 827/; s/versionName '8.2.6'/versionName '8.2.7'/" "$GRADLE"

grep -q "versionCode 827" "$GRADLE"
grep -q "versionName '8.2.7'" "$GRADLE"
echo 'V8.2.7 Android version-only patch PASS'
