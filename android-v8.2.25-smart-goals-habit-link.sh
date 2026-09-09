#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.24 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.24-vaci-fix-chips.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 844" "$GRADLE"
grep -q "versionName '8.2.24'" "$GRADLE"
sed -i "s/versionCode 844/versionCode 845/; s/versionName '8.2.24'/versionName '8.2.25'/" "$GRADLE"

grep -q "versionCode 845" "$GRADLE"
grep -q "versionName '8.2.25'" "$GRADLE"
echo 'V8.2.25 Android version-only patch PASS'
