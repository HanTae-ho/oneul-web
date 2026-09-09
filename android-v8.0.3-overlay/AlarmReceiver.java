package io.github.hantae_ho.twa;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class AlarmReceiver extends BroadcastReceiver {
    @Override public void onReceive(Context context, Intent intent) {
        String action = intent == null ? null : intent.getAction();
        if (ReminderScheduler.ACTION_TEST_REMINDER.equals(action)) {
            NotificationHelper.showScheduledTest(context);
            return;
        }
        if (!ReminderScheduler.ACTION_REMINDER.equals(action)) return;
        String id = intent.getStringExtra("id");
        Reminder r = ReminderStore.byId(context, id == null ? "" : id);
        if (r == null || !ReminderStore.enabled(context)) return;
        NotificationHelper.showReminder(context, r);
        ReminderScheduler.schedule(context, r);
    }
}
