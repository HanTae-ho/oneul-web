#!/usr/bin/env bash
set -euo pipefail

# Start from the verified V8.1 treatment Android build.
bash "$GITHUB_WORKSPACE/android-v8.1-treatment.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
GRADLE="$SRC/app/build.gradle"

sed -i "s/versionCode 810/versionCode 812/; s/versionName '8.1'/versionName '8.1.2'/" "$GRADLE"

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
    private static final String KEY_INTERVAL = "visit_interval";
    private TreatmentReminderStore() {}

    static SharedPreferences prefs(Context c) { return c.getSharedPreferences(PREF, Context.MODE_PRIVATE); }
    static String visit(Context c) { return prefs(c).getString(KEY_VISIT, ""); }
    static String alertsPacked(Context c) { return prefs(c).getString(KEY_ALERTS, ""); }
    static String time(Context c) { return validTime(prefs(c).getString(KEY_TIME, "09:00")); }
    static int interval(Context c) { return validInterval(prefs(c).getInt(KEY_INTERVAL, 0)); }

    static void importSchedule(Context c, String visit, String alerts, String time, int interval) {
        TreatmentReminderScheduler.cancelAll(c);
        prefs(c).edit()
            .putString(KEY_VISIT, validDate(visit) ? visit : "")
            .putString(KEY_ALERTS, packAlerts(alerts))
            .putString(KEY_TIME, validTime(time))
            .putInt(KEY_INTERVAL, validInterval(interval))
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

    static boolean validDate(String v) { return v != null && v.matches("\\d{4}-\\d{2}-\\d{2}"); }
    private static String validTime(String v) {
        if (v != null && v.matches("(?:[01]\\d|2[0-3]):[0-5]\\d")) return v;
        return "09:00";
    }
    static int validInterval(int v) { return v >= 1 && v <= 365 ? v : 0; }
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
        int interval = TreatmentReminderStore.interval(c);
        if (!TreatmentReminderStore.validDate(visit) || interval <= 0) return;
        for (int d : TreatmentReminderStore.alerts(c)) scheduleNext(c, d);
    }

    static void scheduleNextForOffset(Context c, int daysBefore) {
        if (!ReminderStore.enabled(c)) return;
        if (!TreatmentReminderStore.alerts(c).contains(daysBefore)) return;
        scheduleNext(c, daysBefore);
    }

    static void cancelAll(Context c) {
        AlarmManager am = (AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return;
        for (int d : ALL) am.cancel(pending(c, d));
    }

    private static boolean scheduleNext(Context c, int daysBefore) {
        String date = TreatmentReminderStore.visit(c);
        String hhmm = TreatmentReminderStore.time(c);
        int interval = TreatmentReminderStore.interval(c);
        if (!TreatmentReminderStore.validDate(date) || interval <= 0) return false;
        long when = millis(date, hhmm, daysBefore);
        int guard = 0;
        while (when <= System.currentTimeMillis() + 1000L && guard++ < 2000) {
            date = addDays(date, interval);
            when = millis(date, hhmm, daysBefore);
        }
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

    private static String addDays(String date, int days) {
        try {
            String[] d = date.split("-");
            Calendar c = Calendar.getInstance();
            c.clear();
            c.set(Integer.parseInt(d[0]), Integer.parseInt(d[1]) - 1, Integer.parseInt(d[2]));
            c.add(Calendar.DAY_OF_YEAR, days);
            return String.format(java.util.Locale.US, "%04d-%02d-%02d", c.get(Calendar.YEAR), c.get(Calendar.MONTH)+1, c.get(Calendar.DAY_OF_MONTH));
        } catch (Exception e) { return ""; }
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
        return PendingIntent.getBroadcast(c, 812100 + daysBefore, i, flags);
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
        int daysBefore = intent.getIntExtra("daysBefore", 0);
        NotificationHelper.showOutpatient(context, daysBefore);
        // Each alert schedules the same offset for the next outpatient cycle.
        TreatmentReminderScheduler.scheduleNextForOffset(context, daysBefore);
    }
}
EOF

python3 - <<'PY'
from pathlib import Path
import os
p=Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main/java/io/github/hantae_ho/twa/NotificationSettingsActivity.java'
s=p.read_text(encoding='utf-8')

old='''    private String pendingVisit = "", pendingVisitAlerts = "", pendingVisitTime = "09:00";\n'''
new='''    private String pendingVisit = "", pendingVisitAlerts = "", pendingVisitTime = "09:00";\n    private int pendingVisitInterval = 0;\n'''
assert s.count(old)==1; s=s.replace(old,new,1)
old='''        pendingVisitTime = TreatmentReminderStore.time(this);\n'''
new='''        pendingVisitTime = TreatmentReminderStore.time(this);\n        pendingVisitInterval = TreatmentReminderStore.interval(this);\n'''
assert s.count(old)==1; s=s.replace(old,new,1)
old='''        pendingVisitTime = val(u,"visitTime");\n'''
new='''        pendingVisitTime = val(u,"visitTime");\n        try { pendingVisitInterval = Integer.parseInt(val(u,"visitInterval")); } catch (Exception ignored) { pendingVisitInterval = 0; }\n'''
assert s.count(old)==1; s=s.replace(old,new,1)
old='''        TreatmentReminderStore.importSchedule(this, pendingVisit, pendingVisitAlerts, pendingVisitTime);\n'''
new='''        TreatmentReminderStore.importSchedule(this, pendingVisit, pendingVisitAlerts, pendingVisitTime, pendingVisitInterval);\n'''
assert s.count(old)==1; s=s.replace(old,new,1)
old='''             .append("  (").append(TreatmentReminderStore.alertLabels(pendingVisitAlerts)).append(")\\n");\n'''
new='''             .append("  (매 ").append(pendingVisitInterval).append("일 · ").append(TreatmentReminderStore.alertLabels(pendingVisitAlerts)).append(")\\n");\n'''
assert s.count(old)==1; s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
PY

grep -q "versionCode 812" "$GRADLE"
grep -q "versionName '8.1.2'" "$GRADLE"
grep -q 'visitInterval' "$PKG/NotificationSettingsActivity.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'while (when <= System.currentTimeMillis()' "$PKG/TreatmentReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"

echo 'V8.1.2 recurring outpatient Android patch PASS'
