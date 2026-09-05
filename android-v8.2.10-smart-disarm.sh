#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.9 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.9-smart-deads.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 829" "$GRADLE"
grep -q "versionName '8.2.9'" "$GRADLE"
# versionCode is an opaque monotonic integer; 830 follows 829 while versionName carries 8.2.10.
sed -i "s/versionCode 829/versionCode 830/; s/versionName '8.2.9'/versionName '8.2.10'/" "$GRADLE"

grep -q "versionCode 830" "$GRADLE"
grep -q "versionName '8.2.10'" "$GRADLE"
echo 'V8.2.10 Android version-only patch PASS'
