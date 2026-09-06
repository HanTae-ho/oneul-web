#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.12 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.12-capsule-disarm-link.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 832" "$GRADLE"
grep -q "versionName '8.2.12'" "$GRADLE"
sed -i "s/versionCode 832/versionCode 833/; s/versionName '8.2.12'/versionName '8.2.13'/" "$GRADLE"

grep -q "versionCode 833" "$GRADLE"
grep -q "versionName '8.2.13'" "$GRADLE"
echo 'V8.2.13 Android version-only patch PASS'
