#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.1.6 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.1.6-home-today.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 816" "$GRADLE"
grep -q "versionName '8.1.6'" "$GRADLE"
sed -i "s/versionCode 816/versionCode 817/; s/versionName '8.1.6'/versionName '8.1.7'/" "$GRADLE"

grep -q "versionCode 817" "$GRADLE"
grep -q "versionName '8.1.7'" "$GRADLE"
echo 'V8.1.7 Android version-only patch PASS'
