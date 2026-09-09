#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.1.5 native reminder stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.1.5-habits.sh"
bash "$GITHUB_WORKSPACE/android-v8.1.5-ui-fix.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 815" "$GRADLE"
grep -q "versionName '8.1.5'" "$GRADLE"
sed -i "s/versionCode 815/versionCode 816/; s/versionName '8.1.5'/versionName '8.1.6'/" "$GRADLE"

grep -q "versionCode 816" "$GRADLE"
grep -q "versionName '8.1.6'" "$GRADLE"
echo 'V8.1.6 Android version-only patch PASS'
