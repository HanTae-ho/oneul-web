#!/usr/bin/env bash
set -euo pipefail

# Build on the verified V8.0.5 TWA/native exact-alarm base.
bash "$GITHUB_WORKSPACE/android-v8.0.5-native-entry.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
GRADLE="$SRC/app/build.gradle"
MANIFEST="$SRC/app/src/main/AndroidManifest.xml"

sed -i "s/versionCode 805/versionCode 810/; s/versionName '8.0.5'/versionName '8.1'/" "$GRADLE"

cat > "$PKG/TreatmentReminderStore.java" <<'EOF'
package io.github.hantae_ho.twa;

import android.content.Context;
import android.content.SharedPreferences;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

final class TreatmentReminderStore {
    private static final String PREF = "oneul_treatment_reminders";
    private static final String KEY_VISIT = "visit";
    private static final String KEY_ALERTS = "visit_alerts";
    private static final String KEY_TIME = "visit_time";
    private TreatmentReminderStore() {}

    static SharedPreferences prefs(Context c) { return c.getSharedPreferences(PREF, Context.MODE_PRIVATE); }
    static String visit(Context c) { return prefs(c).getString(KEY_VISIT, ""); }
    static String alertsPacked(Context c) { return prefs(c).getString(KEY_ALERTS, ""); }
    static String time(Context c) { return validTime(prefs(c).getString(KEY_TIME, "09:00")); }

    static void importSchedule(Context c, String visit, String alerts, String time) {
        TreatmentReminderScheduler.cancelAll(c);
        prefs(c).edit()
            .putString(KEY_VISIT, validDate(visit) ? visit : "")
            .putString(KEY_ALERTS, packAlerts(alerts))
            .putString(KEY_TIME, validTime(time))
            .apply();
        TreatmentReminderScheduler.scheduleAll(c);
    }

    static List<Integer> alerts(Context c) { return parseAlerts(alertsPacked(c)); }
    static int count(String visit, String alerts) { return validDate(visit) ? parseAlerts(alerts).size() : 0; }

    static String alertLabels(String alerts) {
        List<Integer> a = parseAlerts(alerts);
        if (a.isEmpty()) return "알림 없음";
        List<String> out = new ArrayList<>();
        for (int d : a) out.add(d == 0 ? "당일" : d == 1 ? "1일 전" : "3일 전");
        return android.text.TextUtils.join(" · ", out);
    }

    private static String packAlerts(String raw) {
        List<Integer> a = parseAlerts(raw);
        List<String> out = new ArrayList<>();
        for (int d : a) out.add(String.valueOf(d));
        return android.text.TextUtils.join(",", out);
    }

    private static List<Integer> parseAlerts(String raw) {
        Set<Integer> seen = new LinkedHashSet<>();
        if (raw != null) for (String x : raw.split(",")) {
            try {
                int d = Integer.parseInt(x.trim());
                if (d == 3 || d == 1 || d == 0) seen.add(d);
            } catch (Exception ignored) {}
        }
        return new ArrayList<>(seen);
    }

    static boolean validDate(String v) {
        return v != null && v.matches("\\d{4}-\\d{2}-\\d{2}");
    }
    private static String validTime(String v) {
        if (v != null && v.matches("(?:[01]\\d|2[0-3]):[0-5]\\d")) return v;
        return "09:00";
    }
}
EOF

cat > "$PKG/TreatmentReminderScheduler.java" <<'EOF'
package io.github.hantae_ho.twa;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import java.util.Calendar;

final class TreatmentReminderScheduler {
    static final String ACTION_VISIT = "io.github.hantae_ho.twa.ACTION_TREATMENT_VISIT";
    private static final int[] ALL = new int[]{3,1,0};
    private TreatmentReminderScheduler() {}

    static void scheduleAll(Context c) {
        cancelAll(c);
        if (!ReminderStore.enabled(c)) return;
        String visit = TreatmentReminderStore.visit(c);
        if (!TreatmentReminderStore.validDate(visit)) return;
        for (int d : TreatmentReminderStore.alerts(c)) schedule(c, visit, TreatmentReminderStore.time(c), d);
    }

    static void cancelAll(Context c) {
        AlarmManager am = (AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return;
        for (int d : ALL) am.cancel(pending(c, d));
    }

    private static boolean schedule(Context c, String date, String hhmm, int daysBefore) {
        long when = millis(date, hhmm, daysBefore);
        if (when <= System.currentTimeMillis() + 1000L) return false;
        AlarmManager am = (AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return false;
        PendingIntent pi = pending(c, daysBefore);
        if (Build.VERSION.SDK_INT >= 31 && !am.canScheduleExactAlarms()) {
            am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, when, pi);
            return false;
        }
        if (Build.VERSION.SDK_INT >= 23) am.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, when, pi);
        else am.setExact(AlarmManager.RTC_WAKEUP, when, pi);
        return true;
    }

    private static long millis(String date, String hhmm, int daysBefore) {
        try {
            String[] d = date.split("-"), t = hhmm.split(":");
            Calendar c = Calendar.getInstance();
            c.set(Calendar.YEAR, Integer.parseInt(d[0]));
            c.set(Calendar.MONTH, Integer.parseInt(d[1]) - 1);
            c.set(Calendar.DAY_OF_MONTH, Integer.parseInt(d[2]));
            c.set(Calendar.HOUR_OF_DAY, Integer.parseInt(t[0]));
            c.set(Calendar.MINUTE, Integer.parseInt(t[1]));
            c.set(Calendar.SECOND, 0); c.set(Calendar.MILLISECOND, 0);
            c.add(Calendar.DAY_OF_YEAR, -daysBefore);
            return c.getTimeInMillis();
        } catch (Exception e) { return 0L; }
    }

    private static PendingIntent pending(Context c, int daysBefore) {
        Intent i = new Intent(c, TreatmentAlarmReceiver.class);
        i.setAction(ACTION_VISIT);
        i.setData(Uri.parse("oneul-treatment://visit/" + daysBefore));
        i.putExtra("daysBefore", daysBefore);
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 23) flags |= PendingIntent.FLAG_IMMUTABLE;
        return PendingIntent.getBroadcast(c, 810100 + daysBefore, i, flags);
    }
}
EOF

cat > "$PKG/TreatmentAlarmReceiver.java" <<'EOF'
package io.github.hantae_ho.twa;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class TreatmentAlarmReceiver extends BroadcastReceiver {
    @Override public void onReceive(Context context, Intent intent) {
        if (intent == null || !TreatmentReminderScheduler.ACTION_VISIT.equals(intent.getAction())) return;
        if (!ReminderStore.enabled(context)) return;
        NotificationHelper.showOutpatient(context, intent.getIntExtra("daysBefore", 0));
    }
}
EOF

python3 - <<'PY'
from pathlib import Path
import os
pkg=Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main/java/io/github/hantae_ho/twa'

# NotificationHelper: add privacy-safe outpatient messages.
p=pkg/'NotificationHelper.java'
s=p.read_text(encoding='utf-8')
anchor='''    static boolean showScheduledTest(Context c) {\n        if (!canPost(c)) return false;\n        ensureChannel(c);\n        return post(c, 800003, "2분 예약 시험 알림입니다. 화면이 꺼진 상태에서도 이 알림이 오면 정확한 시간 알림이 정상입니다.");\n    }\n'''
insert=anchor+'''\n    static boolean showOutpatient(Context c, int daysBefore) {\n        if (!canPost(c)) return false;\n        ensureChannel(c);\n        String body = daysBefore == 0\n            ? "오늘은 외래 예정일입니다. 진료 일정을 확인해주세요."\n            : daysBefore == 1\n              ? "내일은 외래 예정일입니다. 진료 일정을 확인해주세요."\n              : "외래 예정일이 3일 남았습니다. 진료 일정을 확인해주세요.";\n        return post(c, 810100 + daysBefore, body);\n    }\n'''
if s.count(anchor)!=1: raise SystemExit('NotificationHelper anchor')
s=s.replace(anchor,insert,1)
p.write_text(s,encoding='utf-8')

# Application: re-schedule outpatient alarms after process startup too.
p=pkg/'Application.java'; s=p.read_text(encoding='utf-8')
anchor='        ReminderScheduler.scheduleAll(this);\n'
if s.count(anchor)!=1: raise SystemExit('Application schedule anchor')
s=s.replace(anchor,anchor+'        TreatmentReminderScheduler.scheduleAll(this);\n',1)
p.write_text(s,encoding='utf-8')

# Boot/time/package/exact-permission changes: restore both reminder families.
p=pkg/'BootReceiver.java'; s=p.read_text(encoding='utf-8')
anchor='            ReminderScheduler.scheduleAll(context);\n'
if s.count(anchor)!=1: raise SystemExit('BootReceiver schedule anchor')
s=s.replace(anchor,anchor+'            TreatmentReminderScheduler.scheduleAll(context);\n',1)
p.write_text(s,encoding='utf-8')

# Native settings bridge: carry outpatient date/reminder options without medicine names or diagnoses.
p=pkg/'NotificationSettingsActivity.java'; s=p.read_text(encoding='utf-8')
repls=[
('''    private String pendingRisk = "", pendingMeds = "", pendingEats = "", pendingBed = "", pendingBuild = "";\n''',
 '''    private String pendingRisk = "", pendingMeds = "", pendingEats = "", pendingBed = "", pendingBuild = "";\n    private String pendingVisit = "", pendingVisitAlerts = "", pendingVisitTime = "09:00";\n'''),
('''        pendingBuild = p.getString(ReminderStore.KEY_BUILD, "");\n''',
 '''        pendingBuild = p.getString(ReminderStore.KEY_BUILD, "");\n        pendingVisit = TreatmentReminderStore.visit(this);\n        pendingVisitAlerts = TreatmentReminderStore.alertsPacked(this);\n        pendingVisitTime = TreatmentReminderStore.time(this);\n'''),
('''        pendingBuild = val(u,"build");\n''',
 '''        pendingBuild = val(u,"build");\n        pendingVisit = val(u,"visit");\n        pendingVisitAlerts = val(u,"visitAlerts");\n        pendingVisitTime = val(u,"visitTime");\n'''),
('''        TextView intro = text("복약·식사·잠처럼 정해진 시각의 알림은 Android가 기기 안에서 예약합니다. 서버로 일정이나 회복기록을 보내지 않습니다.", 16, false);\n''',
 '''        TextView intro = text("복약·식사·잠과 외래 일정 알림은 Android가 기기 안에서 예약합니다. 서버로 일정이나 회복기록을 보내지 않습니다.", 16, false);\n'''),
('''        TextView h = text("현재 가져온 시간", 19, true); h.setPadding(0,dp(8),0,dp(8)); root.addView(h);\n''',
 '''        TextView h = text("현재 가져온 예약", 19, true); h.setPadding(0,dp(8),0,dp(8)); root.addView(h);\n'''),
('''        int n = ReminderStore.fromPacked(pendingRisk, pendingMeds, pendingEats, pendingBed).size();\n''',
 '''        int n = ReminderStore.fromPacked(pendingRisk, pendingMeds, pendingEats, pendingBed).size() +\n            TreatmentReminderStore.count(pendingVisit, pendingVisitAlerts);\n'''),
('''        ReminderStore.importSchedule(this, pendingRisk, pendingMeds, pendingEats, pendingBed, pendingBuild);\n''',
 '''        ReminderStore.importSchedule(this, pendingRisk, pendingMeds, pendingEats, pendingBed, pendingBuild);\n        TreatmentReminderStore.importSchedule(this, pendingVisit, pendingVisitAlerts, pendingVisitTime);\n'''),
('''        ReminderStore.setEnabled(this, enabledSwitch.isChecked());\n''',
 '''        ReminderStore.setEnabled(this, enabledSwitch.isChecked());\n        if (enabledSwitch.isChecked()) TreatmentReminderScheduler.scheduleAll(this);\n        else TreatmentReminderScheduler.cancelAll(this);\n'''),
('''            ReminderScheduler.scheduleAll(this);\n''',
 '''            ReminderScheduler.scheduleAll(this);\n            TreatmentReminderScheduler.scheduleAll(this);\n''')]
for a,b in repls:
    if s.count(a)!=1: raise SystemExit('NotificationSettingsActivity anchor: '+a[:60])
    s=s.replace(a,b,1)
old='''    private String summaryText() {\n        List<Reminder> list = ReminderStore.fromPacked(pendingRisk, pendingMeds, pendingEats, pendingBed);\n        if (list.isEmpty()) return "설정된 시간이 없습니다. 오늘 한 걸음 → 내 정보 → 챙기기에서 시간을 정한 뒤 다시 열어주세요.";\n        StringBuilder b = new StringBuilder();\n        for (Reminder r : list) b.append("• ").append(r.label).append("  ").append(r.time).append("\\n");\n        return b.toString().trim();\n    }\n'''
new='''    private String summaryText() {\n        List<Reminder> list = ReminderStore.fromPacked(pendingRisk, pendingMeds, pendingEats, pendingBed);\n        StringBuilder b = new StringBuilder();\n        for (Reminder r : list) b.append("• ").append(r.label).append("  ").append(r.time).append("\\n");\n        if (TreatmentReminderStore.validDate(pendingVisit) && TreatmentReminderStore.count(pendingVisit, pendingVisitAlerts) > 0) {\n            b.append("• 외래  ").append(pendingVisit).append("  ").append(pendingVisitTime == null || pendingVisitTime.isEmpty() ? "09:00" : pendingVisitTime)\n             .append("  (").append(TreatmentReminderStore.alertLabels(pendingVisitAlerts)).append(")\\n");\n        }\n        if (b.length() == 0) return "설정된 예약이 없습니다. 오늘 한 걸음에서 시간을 정한 뒤 다시 열어주세요.";\n        return b.toString().trim();\n    }\n'''
if s.count(old)!=1: raise SystemExit('summaryText anchor')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
PY

python3 - <<'PY'
from pathlib import Path
import os
p=Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main/AndroidManifest.xml'
s=p.read_text(encoding='utf-8')
anchor='        <receiver android:name=".AlarmReceiver" android:exported="false" />\n'
insert=anchor+'        <receiver android:name=".TreatmentAlarmReceiver" android:exported="false" />\n'
if s.count(anchor)!=1: raise SystemExit('manifest AlarmReceiver anchor')
s=s.replace(anchor,insert,1)
p.write_text(s,encoding='utf-8')
PY

grep -q "versionCode 810" "$GRADLE"
grep -q "versionName '8.1'" "$GRADLE"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$MANIFEST"
grep -q 'TreatmentAlarmReceiver' "$MANIFEST"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q '오늘은 외래 예정일입니다' "$PKG/NotificationHelper.java"
grep -q 'pendingVisitAlerts' "$PKG/NotificationSettingsActivity.java"
grep -q 'TreatmentReminderScheduler.scheduleAll' "$PKG/BootReceiver.java"
grep -q 'https://hantae-ho.github.io/oneul-web/native.html' "$MANIFEST"

echo 'V8.1 Android treatment reminder patch: PASS'
