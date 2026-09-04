#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.1 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.1-trigger-tracking.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 821" "$GRADLE"
grep -q "versionName '8.2.1'" "$GRADLE"
sed -i "s/versionCode 821/versionCode 822/; s/versionName '8.2.1'/versionName '8.2.2'/" "$GRADLE"

grep -q "versionCode 822" "$GRADLE"
grep -q "versionName '8.2.2'" "$GRADLE"
echo 'V8.2.2 Android version-only patch PASS'
