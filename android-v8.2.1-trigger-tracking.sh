#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.0 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.0-future-self.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 820" "$GRADLE"
grep -q "versionName '8.2.0'" "$GRADLE"
sed -i "s/versionCode 820/versionCode 821/; s/versionName '8.2.0'/versionName '8.2.1'/" "$GRADLE"

grep -q "versionCode 821" "$GRADLE"
grep -q "versionName '8.2.1'" "$GRADLE"
echo 'V8.2.1 Android version-only patch PASS'
