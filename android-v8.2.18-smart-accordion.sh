#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.17 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.17-smart-problem-solving.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 837" "$GRADLE"
grep -q "versionName '8.2.17'" "$GRADLE"
sed -i "s/versionCode 837/versionCode 838/; s/versionName '8.2.17'/versionName '8.2.18'/" "$GRADLE"

grep -q "versionCode 838" "$GRADLE"
grep -q "versionName '8.2.18'" "$GRADLE"
echo 'V8.2.18 Android version-only patch PASS'
