#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.1.9 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.1.9-habit-collapse.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 819" "$GRADLE"
grep -q "versionName '8.1.9'" "$GRADLE"
sed -i "s/versionCode 819/versionCode 820/; s/versionName '8.1.9'/versionName '8.2.0'/" "$GRADLE"

grep -q "versionCode 820" "$GRADLE"
grep -q "versionName '8.2.0'" "$GRADLE"
echo 'V8.2.0 Android version-only patch PASS'
