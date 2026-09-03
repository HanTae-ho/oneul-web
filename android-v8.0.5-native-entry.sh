#!/usr/bin/env bash
set -euo pipefail

# Start from the verified exact-alarm/status-bar/TWA build.
bash "$GITHUB_WORKSPACE/android-v8.0.3-exact-alarm.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
MANIFEST="$SRC/app/src/main/AndroidManifest.xml"

# Package version.
sed -i "s/versionCode 803/versionCode 805/; s/versionName '8.0.3'/versionName '8.0.5'/" "$GRADLE"

# Launcher: remove URL query/hash marker logic entirely. The dedicated same-origin
# native.html page sets a sessionStorage marker, then redirects to index.html.
cat > "$PKG/LauncherActivity.java" <<'EOF'
package io.github.hantae_ho.twa;

import android.content.pm.ActivityInfo;
import android.os.Build;
import android.os.Bundle;

public class LauncherActivity extends com.google.androidbrowserhelper.trusted.LauncherActivity {
    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (Build.VERSION.SDK_INT > Build.VERSION_CODES.O) {
            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        } else {
            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED);
        }
    }
}
EOF

# TWA launcher default URL must always pass through native.html.
python3 - <<'PY'
from pathlib import Path
import os
root = Path(os.environ['GITHUB_WORKSPACE']) / 'android-v8'
manifest = root / 'app/src/main/AndroidManifest.xml'
s = manifest.read_text(encoding='utf-8')
old = 'android:value="https://hantae-ho.github.io/oneul-web/index.html" />'
# There are two index.html metadata values: MANAGE_SPACE_URL and DEFAULT_URL.
# Change only DEFAULT_URL by anchoring its preceding meta-data name.
anchor = '''<meta-data android:name="android.support.customtabs.trusted.DEFAULT_URL"\n                android:value="https://hantae-ho.github.io/oneul-web/index.html" />'''
replacement = '''<meta-data android:name="android.support.customtabs.trusted.DEFAULT_URL"\n                android:value="https://hantae-ho.github.io/oneul-web/native.html" />'''
if s.count(anchor) != 1:
    raise SystemExit(f'DEFAULT_URL anchor count={s.count(anchor)}')
s = s.replace(anchor, replacement, 1)
manifest.write_text(s, encoding='utf-8')

# Any native-app return/tap URL in Java should also pass through native.html.
pkg = root / 'app/src/main/java/io/github/hantae_ho/twa'
old_urls = [
    'https://hantae-ho.github.io/oneul-web/index.html#native=1',
    'https://hantae-ho.github.io/oneul-web/index.html?native=1',
    'https://hantae-ho.github.io/oneul-web/index.html?native=1&from=reminder',
]
for p in pkg.glob('*.java'):
    t = p.read_text(encoding='utf-8')
    for old_url in old_urls:
        t = t.replace(old_url, 'https://hantae-ho.github.io/oneul-web/native.html')
    p.write_text(t, encoding='utf-8')
PY

# Guardrails: exact alarms/TWA/status bar must remain; old marker mechanism must not.
grep -q "versionCode 805" "$GRADLE"
grep -q "versionName '8.0.5'" "$GRADLE"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$MANIFEST"
grep -q 'STATUS_BAR_COLOR' "$MANIFEST"
grep -q 'android:name=".LauncherActivity"' "$MANIFEST"
grep -q 'android.support.customtabs.trusted.DEFAULT_URL' "$MANIFEST"
grep -q 'android:value="https://hantae-ho.github.io/oneul-web/native.html"' "$MANIFEST"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'canScheduleExactAlarms' "$PKG/ReminderScheduler.java"
grep -q 'ACTION_REQUEST_SCHEDULE_EXACT_ALARM' "$PKG/NotificationSettingsActivity.java"
grep -q '2분 뒤 예약 시험' "$PKG/NotificationSettingsActivity.java"
grep -R -q 'https://hantae-ho.github.io/oneul-web/native.html' "$PKG"
! grep -R "native=1" -n "$SRC/app/src/main" || exit 1
! grep -R "getLaunchingUrl" -n "$PKG/LauncherActivity.java" || exit 1

echo 'V8.0.5 Android native-entry patch: PASS'
