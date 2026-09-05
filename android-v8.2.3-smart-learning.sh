#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.2 native stack, then bump only the package version.
bash "$GITHUB_WORKSPACE/android-v8.2.2-urge-diary.sh"

GRADLE="$GITHUB_WORKSPACE/android-v8/app/build.gradle"
grep -q "versionCode 822" "$GRADLE"
grep -q "versionName '8.2.2'" "$GRADLE"
sed -i "s/versionCode 822/versionCode 823/; s/versionName '8.2.2'/versionName '8.2.3'/" "$GRADLE"

grep -q "versionCode 823" "$GRADLE"
grep -q "versionName '8.2.3'" "$GRADLE"
echo 'V8.2.3 Android version-only patch PASS'
