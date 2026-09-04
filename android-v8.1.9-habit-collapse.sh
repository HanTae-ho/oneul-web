#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.1.8 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.1.8-pre-social.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 818" "$GRADLE"
grep -q "versionName '8.1.8'" "$GRADLE"
sed -i "s/versionCode 818/versionCode 819/; s/versionName '8.1.8'/versionName '8.1.9'/" "$GRADLE"

grep -q "versionCode 819" "$GRADLE"
grep -q "versionName '8.1.9'" "$GRADLE"
echo 'V8.1.9 Android version-only patch PASS'
