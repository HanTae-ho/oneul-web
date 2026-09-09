#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.8 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.8-smart-three-questions.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 828" "$GRADLE"
grep -q "versionName '8.2.8'" "$GRADLE"
sed -i "s/versionCode 828/versionCode 829/; s/versionName '8.2.8'/versionName '8.2.9'/" "$GRADLE"

grep -q "versionCode 829" "$GRADLE"
grep -q "versionName '8.2.9'" "$GRADLE"
echo 'V8.2.9 Android version-only patch PASS'
