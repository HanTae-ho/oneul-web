#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.7 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.7-smart-change-plan.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 827" "$GRADLE"
grep -q "versionName '8.2.7'" "$GRADLE"
sed -i "s/versionCode 827/versionCode 828/; s/versionName '8.2.7'/versionName '8.2.8'/" "$GRADLE"

grep -q "versionCode 828" "$GRADLE"
grep -q "versionName '8.2.8'" "$GRADLE"
echo 'V8.2.8 Android version-only patch PASS'
