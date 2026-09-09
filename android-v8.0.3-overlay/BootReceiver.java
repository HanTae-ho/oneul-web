package io.github.hantae_ho.twa;

import android.app.AlarmManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

public class BootReceiver extends BroadcastReceiver {
    @Override public void onReceive(Context context, Intent intent) {
        String a = intent == null ? null : intent.getAction();
        boolean exactGranted = Build.VERSION.SDK_INT >= 31 &&
            AlarmManager.ACTION_SCHEDULE_EXACT_ALARM_PERMISSION_STATE_CHANGED.equals(a);
        if (Intent.ACTION_BOOT_COMPLETED.equals(a) || Intent.ACTION_TIME_CHANGED.equals(a) ||
            Intent.ACTION_TIMEZONE_CHANGED.equals(a) || Intent.ACTION_MY_PACKAGE_REPLACED.equals(a) || exactGranted) {
            ReminderScheduler.scheduleAll(context);
        }
    }
}
