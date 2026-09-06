#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.22 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.22-smart-vaci.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 842" "$GRADLE"
grep -q "versionName '8.2.22'" "$GRADLE"
sed -i "s/versionCode 842/versionCode 843/; s/versionName '8.2.22'/versionName '8.2.23'/" "$GRADLE"

grep -q "versionCode 843" "$GRADLE"
grep -q "versionName '8.2.23'" "$GRADLE"
echo 'V8.2.23 Android version-only patch PASS'
