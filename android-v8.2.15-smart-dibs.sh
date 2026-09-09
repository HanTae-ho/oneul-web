#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.14 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.14-home-longpress-edit.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 834" "$GRADLE"
grep -q "versionName '8.2.14'" "$GRADLE"
sed -i "s/versionCode 834/versionCode 835/; s/versionName '8.2.14'/versionName '8.2.15'/" "$GRADLE"

grep -q "versionCode 835" "$GRADLE"
grep -q "versionName '8.2.15'" "$GRADLE"
echo 'V8.2.15 Android version-only patch PASS'
