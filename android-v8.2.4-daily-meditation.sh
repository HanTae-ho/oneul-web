#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.3 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.3-smart-learning.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 823" "$GRADLE"
grep -q "versionName '8.2.3'" "$GRADLE"
sed -i "s/versionCode 823/versionCode 824/; s/versionName '8.2.3'/versionName '8.2.4'/" "$GRADLE"

grep -q "versionCode 824" "$GRADLE"
grep -q "versionName '8.2.4'" "$GRADLE"
echo 'V8.2.4 Android version-only patch PASS'
