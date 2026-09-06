#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.23 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.23-vaci-enjoyable-activities.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 843" "$GRADLE"
grep -q "versionName '8.2.23'" "$GRADLE"
sed -i "s/versionCode 843/versionCode 844/; s/versionName '8.2.23'/versionName '8.2.24'/" "$GRADLE"

grep -q "versionCode 844" "$GRADLE"
grep -q "versionName '8.2.24'" "$GRADLE"
echo 'V8.2.24 Android version-only patch PASS'
