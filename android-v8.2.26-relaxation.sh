#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.25 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.25-smart-goals-habit-link.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 845" "$GRADLE"
grep -q "versionName '8.2.25'" "$GRADLE"
sed -i "s/versionCode 845/versionCode 846/; s/versionName '8.2.25'/versionName '8.2.26'/" "$GRADLE"

grep -q "versionCode 846" "$GRADLE"
grep -q "versionName '8.2.26'" "$GRADLE"
echo 'V8.2.26 Android version-only patch PASS'
