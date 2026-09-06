#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.16 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.16-smart-thinking-styles.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 836" "$GRADLE"
grep -q "versionName '8.2.16'" "$GRADLE"
sed -i "s/versionCode 836/versionCode 837/; s/versionName '8.2.16'/versionName '8.2.17'/" "$GRADLE"

grep -q "versionCode 837" "$GRADLE"
grep -q "versionName '8.2.17'" "$GRADLE"
echo 'V8.2.17 Android version-only patch PASS'
