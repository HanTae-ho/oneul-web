#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.4 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.4-daily-meditation.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 824" "$GRADLE"
grep -q "versionName '8.2.4'" "$GRADLE"
sed -i "s/versionCode 824/versionCode 825/; s/versionName '8.2.4'/versionName '8.2.5'/" "$GRADLE"

grep -q "versionCode 825" "$GRADLE"
grep -q "versionName '8.2.5'" "$GRADLE"
echo 'V8.2.5 Android version-only patch PASS'
