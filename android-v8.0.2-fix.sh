#!/usr/bin/env bash
set -euo pipefail

# Start from the already verified V8.0.1 compatibility patch.
bash "$GITHUB_WORKSPACE/android-v8.0.1-patch.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
MANIFEST="$SRC/app/src/main/AndroidManifest.xml"

# Bump only the Android package version.
sed -i "s/versionCode 801/versionCode 802/; s/versionName '8.0.1'/versionName '8.0.2'/" "$GRADLE"

# Give Chrome/TWA an explicit status-bar color so Samsung's status icons remain visible.
python3 - <<'PY'
from pathlib import Path
p = Path(__import__('os').environ['GITHUB_WORKSPACE']) / 'android-v8/app/src/main/AndroidManifest.xml'
s = p.read_text(encoding='utf-8')
needle = '''            <meta-data android:name="android.support.customtabs.trusted.DEFAULT_URL"\n                android:value="https://hantae-ho.github.io/oneul-web/index.html" />'''
insert = needle + '''\n            <meta-data android:name="android.support.customtabs.trusted.STATUS_BAR_COLOR"\n                android:resource="@color/brand" />\n            <meta-data android:name="android.support.customtabs.trusted.STATUS_BAR_COLOR_DARK"\n                android:resource="@color/brand_dark" />'''
if needle not in s:
    raise SystemExit('DEFAULT_URL metadata anchor not found')
s = s.replace(needle, insert, 1)
p.write_text(s, encoding='utf-8')
PY

grep -q "versionCode 802" "$GRADLE"
grep -q "versionName '8.0.2'" "$GRADLE"
grep -q 'android.support.customtabs.trusted.STATUS_BAR_COLOR' "$MANIFEST"
