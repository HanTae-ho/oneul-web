#!/usr/bin/env bash
set -euo pipefail

# V8.2.68: keep the verified V8.2.67 alarm/TTS engines intact.
# Only add silent apply/clear handling to the existing oneul://reminders bridge.
bash "$GITHUB_WORKSPACE/android-v8.2.67-legal-release.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
GRADLE="$SRC/app/build.gradle"
ACT="$PKG/NotificationSettingsActivity.java"

sed -i "s/versionCode 887/versionCode 888/; s/versionName '8.2.67'/versionName '8.2.68'/" "$GRADLE"

python3 - <<'PY'
from pathlib import Path
import os
p=Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main/java/io/github/hantae_ho/twa/NotificationSettingsActivity.java'
s=p.read_text(encoding='utf-8')

old='''        NotificationHelper.ensureChannel(this);\n        loadPendingFromPrefs();\n        importFromIntent(getIntent());\n        buildUi();'''
new='''        NotificationHelper.ensureChannel(this);\n        loadPendingFromPrefs();\n        if (handleSilentSync(getIntent())) return;\n        importFromIntent(getIntent());\n        buildUi();'''
assert s.count(old)==1, 'onCreate anchor'
s=s.replace(old,new,1)

old='''        setIntent(i);\n        importFromIntent(i);\n        applyVisitControls();\n        refresh();'''
new='''        setIntent(i);\n        if (handleSilentSync(i)) return;\n        importFromIntent(i);\n        applyVisitControls();\n        refresh();'''
assert s.count(old)==1, 'onNewIntent anchor'
s=s.replace(old,new,1)

anchor='''    private void loadPendingFromPrefs() {'''
helper='''    private boolean handleSilentSync(Intent i) {\n        Uri u = i == null ? null : i.getData();\n        if (u == null || !"oneul".equals(u.getScheme()) || !"reminders".equals(u.getHost())) return false;\n\n        if ("1".equals(val(u, "clear"))) {\n            // Each importSchedule cancels the old AlarmManager PendingIntents before storing empty data.\n            // Keep the user's Android notification permission / enabled toggle itself unchanged.\n            ReminderStore.importSchedule(this, "", "", "", "", val(u, "build"));\n            HabitReminderStore.importSchedule(this, "");\n            TreatmentReminderStore.importSchedule(this, "", "", TreatmentReminderStore.time(this), 0);\n            finish();\n            return true;\n        }\n\n        if ("1".equals(val(u, "apply"))) {\n            // Outpatient lead-time/time are native-only preferences, so web schedule sync must preserve them.\n            String visitAlerts = TreatmentReminderStore.alertsPacked(this);\n            String visitTime = TreatmentReminderStore.time(this);\n            importFromIntent(i);\n            ReminderStore.importSchedule(this, pendingRisk, pendingMeds, pendingEats, pendingBed, pendingBuild);\n            HabitReminderStore.importSchedule(this, pendingHabits);\n            TreatmentReminderStore.importSchedule(this, pendingVisit, visitAlerts, visitTime, pendingVisitInterval);\n            if (ReminderStore.enabled(this)) {\n                ReminderScheduler.scheduleAll(this);\n                HabitReminderScheduler.scheduleAll(this);\n                TreatmentReminderScheduler.scheduleAll(this);\n            } else {\n                ReminderScheduler.cancelAll(this);\n                HabitReminderScheduler.cancelAll(this);\n                TreatmentReminderScheduler.cancelAll(this);\n            }\n            finish();\n            return true;\n        }\n        return false;\n    }\n\n'''
assert s.count(anchor)==1, 'helper anchor'
s=s.replace(anchor,helper+anchor,1)
p.write_text(s,encoding='utf-8')
PY

grep -q "versionCode 888" "$GRADLE"
grep -q "versionName '8.2.68'" "$GRADLE"
grep -q 'handleSilentSync(getIntent())' "$ACT"
grep -q '"1".equals(val(u, "clear"))' "$ACT"
grep -q '"1".equals(val(u, "apply"))' "$ACT"
grep -q 'HabitReminderStore.importSchedule(this, "")' "$ACT"
grep -q 'TreatmentReminderStore.alertsPacked(this)' "$ACT"

# Native engines must remain intact.
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'PowerManager.PARTIAL_WAKE_LOCK' "$PKG/RelaxTtsActivity.java"
grep -q 'TextToSpeech.QUEUE_FLUSH' "$PKG/MindProVoiceService.java"

echo 'V8.2.68 native reminder sync bridge PASS'
