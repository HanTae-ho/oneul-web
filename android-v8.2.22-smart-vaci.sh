#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.21 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.21-smart-learning-links.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 841" "$GRADLE"
grep -q "versionName '8.2.21'" "$GRADLE"
sed -i "s/versionCode 841/versionCode 842/; s/versionName '8.2.21'/versionName '8.2.22'/" "$GRADLE"

grep -q "versionCode 842" "$GRADLE"
grep -q "versionName '8.2.22'" "$GRADLE"
echo 'V8.2.22 Android version-only patch PASS'
