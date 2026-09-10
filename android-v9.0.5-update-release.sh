#!/usr/bin/env bash
set -euo pipefail

# V9.0.5 changes web UI/update flow only. Reuse the proven V9.0.4 native
# reminder/TTS stack, advance package metadata, and add a package-version
# marker to the existing native.html entry URL.
bash "$GITHUB_WORKSPACE/android-v9.0.4-social-manage-release.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
MANIFEST="$SRC/app/src/main/AndroidManifest.xml"

sed -i "s/versionCode 899/versionCode 900/; s/versionName '9.0.4'/versionName '9.0.5'/" "$GRADLE"

python3 - <<'PY'
from pathlib import Path
import os
root=Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main'
old='https://hantae-ho.github.io/oneul-web/native.html'
new='https://hantae-ho.github.io/oneul-web/native.html?appv=9.0.5'
changed=[]
for p in root.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in {'.java','.xml'}:
        continue
    s=p.read_text(encoding='utf-8')
    if old in s:
        s=s.replace(old,new)
        p.write_text(s,encoding='utf-8')
        changed.append(str(p.relative_to(root)))
if not changed:
    raise SystemExit('native.html URL marker target not found')
print('appv marker files:',', '.join(changed))
PY

grep -q "versionCode 900" "$GRADLE"
grep -q "versionName '9.0.5'" "$GRADLE"
grep -Fq 'android:value="https://hantae-ho.github.io/oneul-web/native.html?appv=9.0.5"' "$MANIFEST"
grep -R -Fq 'https://hantae-ho.github.io/oneul-web/native.html?appv=9.0.5' "$PKG"

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

echo 'V9.0.5 Android versionCode 900 + appv marker release patch PASS'
