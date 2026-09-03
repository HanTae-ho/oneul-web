package io.github.hantae_ho.twa;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import java.util.Calendar;
import java.util.List;

final class ReminderScheduler {
    static final String ACTION_REMINDER = "io.github.hantae_ho.twa.ACTION_REMINDER";
    static final String ACTION_TEST_REMINDER = "io.github.hantae_ho.twa.ACTION_TEST_REMINDER";
    private ReminderScheduler() {}

    static boolean canScheduleExact(Context c) {
        AlarmManager am = (AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return false;
        if (Build.VERSION.SDK_INT < 31) return true;
        return am.canScheduleExactAlarms();
    }

    static void scheduleAll(Context c) {
        if (!ReminderStore.enabled(c)) return;
        for (Reminder r : ReminderStore.reminders(c)) schedule(c, r);
    }

    static void cancelAll(Context c) {
        List<Reminder> list = ReminderStore.reminders(c);
        AlarmManager am = (AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return;
        for (Reminder r : list) am.cancel(pending(c, r));
        am.cancel(testPending(c));
    }

    static boolean schedule(Context c, Reminder r) {
        if (r == null || !ReminderStore.enabled(c)) return false;
        AlarmManager am = (AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return false;
        long when = nextMillis(r.time);
        return scheduleAt(am, when, pending(c, r));
    }

    static boolean scheduleExactTest(Context c, long delayMillis) {
        AlarmManager am = (AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
        if (am == null || !canScheduleExact(c)) return false;
        long when = System.currentTimeMillis() + Math.max(30_000L, delayMillis);
        PendingIntent pi = testPending(c);
        if (Build.VERSION.SDK_INT >= 23) {
            am.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, when, pi);
        } else {
            am.setExact(AlarmManager.RTC_WAKEUP, when, pi);
        }
        return true;
    }

    private static boolean scheduleAt(AlarmManager am, long when, PendingIntent pi) {
        if (Build.VERSION.SDK_INT >= 31 && !am.canScheduleExactAlarms()) {
            am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, when, pi);
            return false;
        }
        if (Build.VERSION.SDK_INT >= 23) {
            am.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, when, pi);
        } else {
            am.setExact(AlarmManager.RTC_WAKEUP, when, pi);
        }
        return true;
    }

    private static PendingIntent pending(Context c, Reminder r) {
        Intent i = new Intent(c, AlarmReceiver.class);
        i.setAction(ACTION_REMINDER);
        i.setData(Uri.parse("oneul-reminder://" + Uri.encode(r.id)));
        i.putExtra("id", r.id);
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 23) flags |= PendingIntent.FLAG_IMMUTABLE;
        return PendingIntent.getBroadcast(c, requestCode(r.id), i, flags);
    }

    private static PendingIntent testPending(Context c) {
        Intent i = new Intent(c, AlarmReceiver.class);
        i.setAction(ACTION_TEST_REMINDER);
        i.setData(Uri.parse("oneul-reminder://exact-test"));
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 23) flags |= PendingIntent.FLAG_IMMUTABLE;
        return PendingIntent.getBroadcast(c, 800003, i, flags);
    }

    private static int requestCode(String id) { return id.hashCode() & 0x7fffffff; }

    static long nextMillis(String hhmm) {
        String[] a = hhmm.split(":");
        int h = Integer.parseInt(a[0]), m = Integer.parseInt(a[1]);
        Calendar now = Calendar.getInstance();
        Calendar t = Calendar.getInstance();
        t.set(Calendar.HOUR_OF_DAY, h);
        t.set(Calendar.MINUTE, m);
        t.set(Calendar.SECOND, 0);
        t.set(Calendar.MILLISECOND, 0);
        if (t.getTimeInMillis() <= now.getTimeInMillis() + 1000L) t.add(Calendar.DAY_OF_YEAR, 1);
        return t.getTimeInMillis();
    }
}
