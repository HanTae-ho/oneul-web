#!/usr/bin/env bash
set -euo pipefail

# V9.0.7 changes only web version parsing/cache metadata.
# Reuse the proven V9.0.6 native reminder/TTS stack and advance package metadata.
bash "$GITHUB_WORKSPACE/android-v9.0.6-social-speed-release.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
MANIFEST="$SRC/app/src/main/AndroidManifest.xml"

sed -i "s/versionCode 901/versionCode 902/; s/versionName '9.0.6'/versionName '9.0.7'/" "$GRADLE"

python3 - <<'PY'
from pathlib import Path
import os
root=Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main'
old='https://hantae-ho.github.io/oneul-web/native.html?appv=9.0.6'
new='https://hantae-ho.github.io/oneul-web/native.html?appv=9.0.7'
changed=[]
for p in root.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in {'.java','.xml'}:
        continue
    s=p.read_text(encoding='utf-8')
    if old in s:
        p.write_text(s.replace(old,new),encoding='utf-8')
        changed.append(str(p.relative_to(root)))
if not changed:
    raise SystemExit('V9.0.6 native.html appv marker target not found')
print('appv marker files:',', '.join(changed))
PY

grep -q "versionCode 902" "$GRADLE"
grep -q "versionName '9.0.7'" "$GRADLE"
grep -Fq 'android:value="https://hantae-ho.github.io/oneul-web/native.html?appv=9.0.7"' "$MANIFEST"
grep -R -Fq 'https://hantae-ho.github.io/oneul-web/native.html?appv=9.0.7' "$PKG"

# Preserve the proven silent reminder bridge and native engines.
grep -q 'handleSilentSync(getIntent())' "$PKG/NotificationSettingsActivity.java"
grep -q '"1".equals(val(u, "clear"))' "$PKG/NotificationSettingsActivity.java"
grep -q '"1".equals(val(u, "apply"))' "$PKG/NotificationSettingsActivity.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'PowerManager.PARTIAL_WAKE_LOCK' "$PKG/RelaxTtsActivity.java"
grep -q 'TextToSpeech.QUEUE_FLUSH' "$PKG/MindProVoiceService.java"

echo 'V9.0.7 Android versionCode 902 + appv marker release patch PASS'
