#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.13 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.13-smart-nav-abc.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 833" "$GRADLE"
grep -q "versionName '8.2.13'" "$GRADLE"
sed -i "s/versionCode 833/versionCode 834/; s/versionName '8.2.13'/versionName '8.2.14'/" "$GRADLE"

grep -q "versionCode 834" "$GRADLE"
grep -q "versionName '8.2.14'" "$GRADLE"
echo 'V8.2.14 Android version-only patch PASS'
