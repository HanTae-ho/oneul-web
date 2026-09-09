#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.10 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.10-smart-disarm.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 830" "$GRADLE"
grep -q "versionName '8.2.10'" "$GRADLE"
sed -i "s/versionCode 830/versionCode 831/; s/versionName '8.2.10'/versionName '8.2.11'/" "$GRADLE"

grep -q "versionCode 831" "$GRADLE"
grep -q "versionName '8.2.11'" "$GRADLE"
echo 'V8.2.11 Android version-only patch PASS'
