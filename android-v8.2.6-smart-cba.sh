#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.5 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.5-smart-hov.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 825" "$GRADLE"
grep -q "versionName '8.2.5'" "$GRADLE"
sed -i "s/versionCode 825/versionCode 826/; s/versionName '8.2.5'/versionName '8.2.6'/" "$GRADLE"

grep -q "versionCode 826" "$GRADLE"
grep -q "versionName '8.2.6'" "$GRADLE"
echo 'V8.2.6 Android version-only patch PASS'
