#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.26 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.26-relaxation.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 846" "$GRADLE"
grep -q "versionName '8.2.26'" "$GRADLE"
sed -i "s/versionCode 846/versionCode 847/; s/versionName '8.2.26'/versionName '8.2.27'/" "$GRADLE"

grep -q "versionCode 847" "$GRADLE"
grep -q "versionName '8.2.27'" "$GRADLE"
echo 'V8.2.27 Android version-only patch PASS'
