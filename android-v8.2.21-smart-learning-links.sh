#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.20 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.20-smart-balance-pie.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 840" "$GRADLE"
grep -q "versionName '8.2.20'" "$GRADLE"
sed -i "s/versionCode 840/versionCode 841/; s/versionName '8.2.20'/versionName '8.2.21'/" "$GRADLE"

grep -q "versionCode 841" "$GRADLE"
grep -q "versionName '8.2.21'" "$GRADLE"
echo 'V8.2.21 Android version-only patch PASS'
