#!/usr/bin/env bash
set -euo pipefail

bash "$GITHUB_WORKSPACE/android-v8.1.4-tools-practice.sh"
SRC="$GITHUB_WORKSPACE/android-v8"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
GRADLE="$SRC/app/build.gradle"

sed -i "s/versionCode 814/versionCode 815/; s/versionName '8.1.4'/versionName '8.1.5'/" "$GRADLE"

cat > "$PKG/HabitReminder.java" <<'JAVA'
package io.github.hantae_ho.twa;

final class HabitReminder {
    final String id, time, start, weekdays;
    final int days;
    HabitReminder(String id, String time, String start, int days, String weekdays) {
        this.id=id; this.time=time; this.start=start; this.days=days; this.weekdays=weekdays;
    }
}
JAVA

cat > "$PKG/HabitReminderStore.java" <<'JAVA'
package io.github.hantae_ho.twa;

import android.content.Context;
import android.content.SharedPreferences;
import java.util.ArrayList;
import java.util.List;

final class HabitReminderStore {
    static final String PREFS="oneul_habit_reminders_v1";
    static final String KEY_HABITS="habits";
    private HabitReminderStore() {}
    static SharedPreferences prefs(Context c){ return c.getSharedPreferences(PREFS,Context.MODE_PRIVATE); }
    static String packed(Context c){ return prefs(c).getString(KEY_HABITS,""); }
    static void importSchedule(Context c,String packed){
        HabitReminderScheduler.cancelAll(c);
        prefs(c).edit().putString(KEY_HABITS, packed==null?"":packed).apply();
    }
    static List<HabitReminder> reminders(Context c){ return fromPacked(packed(c)); }
    static int count(String p){ return fromPacked(p).size(); }
    static HabitReminder byId(Context c,String id){
        for(HabitReminder h:reminders(c)) if(h.id.equals(id)) return h;
        return null;
    }
    static List<HabitReminder> fromPacked(String packed){
        List<HabitReminder> out=new ArrayList<>();
        if(packed==null||packed.isEmpty()) return out;
        for(String item:packed.split("\\|")){
            String[] a=item.split("@",-1);
            if(a.length!=5) continue;
            String id=a[0], time=a[1], start=a[2], weekdays=a[4];
            if(!id.matches("[A-Za-z0-9_-]{1,80}") || !ReminderStore.validTime(time) || !start.matches("\\d{4}-\\d{2}-\\d{2}") || !weekdays.matches("[0-6]{1,7}")) continue;
            int days=0; try{days=Integer.parseInt(a[3]);}catch(Exception ignored){}
            if(days<0||days>3650) continue;
            boolean[] seen=new boolean[7]; StringBuilder wd=new StringBuilder();
            for(char ch:weekdays.toCharArray()){int n=ch-'0';if(!seen[n]){seen[n]=true;wd.append(ch);}}
            if(wd.length()==0) continue;
            out.add(new HabitReminder(id,time,start,days,wd.toString()));
        }
        return out;
    }
}
JAVA

cat > "$PKG/HabitReminderScheduler.java" <<'JAVA'
package io.github.hantae_ho.twa;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.List;
import java.util.Locale;

final class HabitReminderScheduler {
    static final String ACTION_HABIT_REMINDER="io.github.hantae_ho.twa.ACTION_HABIT_REMINDER";
    private HabitReminderScheduler() {}
    static void scheduleAll(Context c){
        if(!ReminderStore.enabled(c)) return;
        for(HabitReminder h:HabitReminderStore.reminders(c)) schedule(c,h);
    }
    static void cancelAll(Context c){
        List<HabitReminder> list=HabitReminderStore.reminders(c);
        AlarmManager am=(AlarmManager)c.getSystemService(Context.ALARM_SERVICE); if(am==null)return;
        for(HabitReminder h:list) am.cancel(pending(c,h));
    }
    static boolean schedule(Context c,HabitReminder h){
        if(h==null||!ReminderStore.enabled(c))return false;
        AlarmManager am=(AlarmManager)c.getSystemService(Context.ALARM_SERVICE);if(am==null)return false;
        long when=nextMillis(h); if(when<=0){am.cancel(pending(c,h));return false;}
        PendingIntent pi=pending(c,h);
        if(Build.VERSION.SDK_INT>=31&&!am.canScheduleExactAlarms()) am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP,when,pi);
        else if(Build.VERSION.SDK_INT>=23) am.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP,when,pi);
        else am.setExact(AlarmManager.RTC_WAKEUP,when,pi);
        return true;
    }
    static long nextMillis(HabitReminder h){
        try{
            SimpleDateFormat f=new SimpleDateFormat("yyyy-MM-dd",Locale.US);f.setLenient(false);
            Calendar start=Calendar.getInstance();start.setTime(f.parse(h.start));zero(start);
            Calendar end=null;if(h.days>0){end=(Calendar)start.clone();end.add(Calendar.DAY_OF_YEAR,h.days-1);}
            Calendar now=Calendar.getInstance();Calendar d=Calendar.getInstance();zero(d);
            if(d.before(start)) d=(Calendar)start.clone();
            String[] tm=h.time.split(":");int hh=Integer.parseInt(tm[0]),mm=Integer.parseInt(tm[1]);
            for(int i=0;i<=3660;i++){
                if(end!=null&&d.after(end))return -1L;
                int javaDow=d.get(Calendar.DAY_OF_WEEK); int jsDow=(javaDow==Calendar.SUNDAY)?0:javaDow-1;
                if(h.weekdays.indexOf(String.valueOf(jsDow))>=0){
                    Calendar t=(Calendar)d.clone();t.set(Calendar.HOUR_OF_DAY,hh);t.set(Calendar.MINUTE,mm);t.set(Calendar.SECOND,0);t.set(Calendar.MILLISECOND,0);
                    if(t.getTimeInMillis()>now.getTimeInMillis()+1000L)return t.getTimeInMillis();
                }
                d.add(Calendar.DAY_OF_YEAR,1);
            }
        }catch(Exception ignored){}
        return -1L;
    }
    private static void zero(Calendar c){c.set(Calendar.HOUR_OF_DAY,0);c.set(Calendar.MINUTE,0);c.set(Calendar.SECOND,0);c.set(Calendar.MILLISECOND,0);}
    private static PendingIntent pending(Context c,HabitReminder h){
        Intent i=new Intent(c,HabitAlarmReceiver.class);i.setAction(ACTION_HABIT_REMINDER);i.setData(Uri.parse("oneul-habit://"+Uri.encode(h.id)));i.putExtra("id",h.id);
        int flags=PendingIntent.FLAG_UPDATE_CURRENT;if(Build.VERSION.SDK_INT>=23)flags|=PendingIntent.FLAG_IMMUTABLE;
        return PendingIntent.getBroadcast(c,h.id.hashCode()&0x7fffffff,i,flags);
    }
}
JAVA

cat > "$PKG/HabitAlarmReceiver.java" <<'JAVA'
package io.github.hantae_ho.twa;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class HabitAlarmReceiver extends BroadcastReceiver {
    @Override public void onReceive(Context context, Intent intent){
        if(intent==null||!HabitReminderScheduler.ACTION_HABIT_REMINDER.equals(intent.getAction()))return;
        String id=intent.getStringExtra("id"); HabitReminder h=HabitReminderStore.byId(context,id==null?"":id);
        if(h==null||!ReminderStore.enabled(context))return;
        Reminder r=new Reminder("habit_"+h.id,"habit","습관",h.time,"정해둔 습관을 실천할 시간입니다.");
        NotificationHelper.showReminder(context,r);
        HabitReminderScheduler.schedule(context,h);
    }
}
JAVA

python3 - <<'PY'
from pathlib import Path
import os
pkg=Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main/java/io/github/hantae_ho/twa'

# Boot: habit schedules survive reboot/time changes/package update.
p=pkg/'BootReceiver.java';s=p.read_text(encoding='utf-8')
old='''            ReminderScheduler.scheduleAll(context);\n            TreatmentReminderScheduler.scheduleAll(context);'''
new='''            ReminderScheduler.scheduleAll(context);\n            HabitReminderScheduler.scheduleAll(context);\n            TreatmentReminderScheduler.scheduleAll(context);'''
if s.count(old)!=1: raise SystemExit('BootReceiver anchor')
p.write_text(s.replace(old,new,1),encoding='utf-8')

# Native unified notification editor.
p=pkg/'NotificationSettingsActivity.java';s=p.read_text(encoding='utf-8')
repls=[]
repls.append(('''    private Switch enabledSwitch, detailedSwitch;\n    private TextView status, summary;\n    private String pendingRisk = "", pendingMeds = "", pendingEats = "", pendingBed = "", pendingBuild = "";\n    private String pendingVisit = "", pendingVisitAlerts = "", pendingVisitTime = "09:00";''',
'''    private Switch enabledSwitch, detailedSwitch, visitD3Switch, visitD1Switch, visitDaySwitch;\n    private TextView status, summary;\n    private Button visitTimeButton;\n    private String pendingRisk = "", pendingMeds = "", pendingEats = "", pendingBed = "", pendingHabits = "", pendingBuild = "";\n    private String pendingVisit = "", pendingVisitAlerts = "3,1,0", pendingVisitTime = "09:00";'''))
repls.append(('''        pendingBed = p.getString(ReminderStore.KEY_BED, "");\n        pendingBuild = p.getString(ReminderStore.KEY_BUILD, "");\n        pendingVisit = TreatmentReminderStore.visit(this);\n        pendingVisitAlerts = TreatmentReminderStore.alertsPacked(this);''',
'''        pendingBed = p.getString(ReminderStore.KEY_BED, "");\n        pendingHabits = HabitReminderStore.packed(this);\n        pendingBuild = p.getString(ReminderStore.KEY_BUILD, "");\n        pendingVisit = TreatmentReminderStore.visit(this);\n        pendingVisitAlerts = TreatmentReminderStore.alertsPacked(this);\n        if (pendingVisitAlerts == null || pendingVisitAlerts.isEmpty()) pendingVisitAlerts = "3,1,0";'''))
repls.append(('''        pendingBed = val(u,"bed");\n        pendingBuild = val(u,"build");\n        pendingVisit = val(u,"visit");\n        pendingVisitAlerts = val(u,"visitAlerts");\n        pendingVisitTime = val(u,"visitTime");\n        try { pendingVisitInterval = Integer.parseInt(val(u,"visitInterval")); } catch (Exception ignored) { pendingVisitInterval = 0; }''',
'''        pendingBed = val(u,"bed");\n        pendingHabits = val(u,"habits");\n        pendingBuild = val(u,"build");\n        pendingVisit = val(u,"visit");\n        if (u.getQueryParameter("visitAlerts") != null) pendingVisitAlerts = val(u,"visitAlerts");\n        if (u.getQueryParameter("visitTime") != null && !val(u,"visitTime").isEmpty()) pendingVisitTime = val(u,"visitTime");\n        try { pendingVisitInterval = Integer.parseInt(val(u,"visitInterval")); } catch (Exception ignored) { pendingVisitInterval = 0; }'''))
repls.append(('''        TextView intro = text("생활 일정과 치료 일정 알림은 Android가 기기 안에서 예약합니다. 서버로 일정이나 회복기록을 보내지 않습니다.", 16, false);''',
'''        TextView intro = text("습관·생활 일정·치료 일정 알림을 Android가 기기 안에서 예약합니다. 서버로 일정이나 회복기록을 보내지 않습니다.", 16, false);'''))
for old,new in repls:
    if s.count(old)!=1: raise SystemExit('NotificationSettings anchor: '+old[:55])
    s=s.replace(old,new,1)

# Insert outpatient alert editor before status/permissions.
anchor='''        summary = text("", 16, false); summary.setPadding(dp(14),dp(14),dp(14),dp(14)); summary.setBackgroundColor(Color.WHITE); root.addView(summary);\n\n        status = text("", 14, false);'''
insert='''        summary = text("", 16, false); summary.setPadding(dp(14),dp(14),dp(14),dp(14)); summary.setBackgroundColor(Color.WHITE); root.addView(summary);\n\n        TextView vh = text("외래 알림", 19, true); vh.setPadding(0,dp(20),0,dp(6)); root.addView(vh);\n        TextView vhelp = text("외래 관리를 사용하는 경우 미리 알릴 시점과 시간을 여기에서 정합니다.", 14, false); vhelp.setTextColor(Color.GRAY); vhelp.setPadding(0,0,0,dp(6)); root.addView(vhelp);\n        visitD3Switch = new Switch(this); visitD3Switch.setText("3일 전"); visitD3Switch.setTextSize(16); root.addView(visitD3Switch);\n        visitD1Switch = new Switch(this); visitD1Switch.setText("1일 전"); visitD1Switch.setTextSize(16); root.addView(visitD1Switch);\n        visitDaySwitch = new Switch(this); visitDaySwitch.setText("당일"); visitDaySwitch.setTextSize(16); root.addView(visitDaySwitch);\n        visitTimeButton = button("외래 알림 시간 · " + pendingVisitTime);\n        visitTimeButton.setOnClickListener(v -> pickVisitTime()); root.addView(visitTimeButton);\n        applyVisitControls();\n\n        status = text("", 14, false);'''
if s.count(anchor)!=1: raise SystemExit('native UI insert anchor')
s=s.replace(anchor,insert,1)

# Counts, summary and save.
s=s.replace('''        int n = ReminderStore.fromPacked(pendingRisk, pendingMeds, pendingEats, pendingBed).size() +\n            TreatmentReminderStore.count(pendingVisit, pendingVisitAlerts);''',
'''        int n = ReminderStore.fromPacked(pendingRisk, pendingMeds, pendingEats, pendingBed).size() +\n            HabitReminderStore.count(pendingHabits) + TreatmentReminderStore.count(pendingVisit, currentVisitAlerts());''')
s=s.replace('''        List<Reminder> list = ReminderStore.fromPacked(pendingRisk, pendingMeds, pendingEats, pendingBed);\n        StringBuilder b = new StringBuilder();\n        for (Reminder r : list) b.append("• ").append(r.label).append("  ").append(r.time).append("\\n");''',
'''        List<Reminder> list = ReminderStore.fromPacked(pendingRisk, pendingMeds, pendingEats, pendingBed);\n        StringBuilder b = new StringBuilder();\n        for (Reminder r : list) b.append("• ").append(r.label).append("  ").append(r.time).append("\\n");\n        for (HabitReminder h : HabitReminderStore.fromPacked(pendingHabits)) b.append("• 습관  ").append(h.time).append(h.days > 0 ? "  · "+h.days+"일" : "  · 계속").append("\\n");''')
s=s.replace('''        if (TreatmentReminderStore.validDate(pendingVisit) && TreatmentReminderStore.count(pendingVisit, pendingVisitAlerts) > 0) {''',
'''        if (TreatmentReminderStore.validDate(pendingVisit) && TreatmentReminderStore.count(pendingVisit, currentVisitAlerts()) > 0) {''')
s=s.replace('''.append("  (매 ").append(pendingVisitInterval).append("일 · ").append(TreatmentReminderStore.alertLabels(pendingVisitAlerts)).append(")\\n");''',
'''.append("  (매 ").append(pendingVisitInterval).append("일 · ").append(TreatmentReminderStore.alertLabels(currentVisitAlerts())).append(")\\n");''')
s=s.replace('''        ReminderStore.importSchedule(this, pendingRisk, pendingMeds, pendingEats, pendingBed, pendingBuild);\n        TreatmentReminderStore.importSchedule(this, pendingVisit, pendingVisitAlerts, pendingVisitTime, pendingVisitInterval);''',
'''        ReminderStore.importSchedule(this, pendingRisk, pendingMeds, pendingEats, pendingBed, pendingBuild);\n        HabitReminderStore.importSchedule(this, pendingHabits);\n        pendingVisitAlerts = currentVisitAlerts();\n        TreatmentReminderStore.importSchedule(this, pendingVisit, pendingVisitAlerts, pendingVisitTime, pendingVisitInterval);''')
s=s.replace('''        if (enabledSwitch.isChecked()) TreatmentReminderScheduler.scheduleAll(this);\n        else TreatmentReminderScheduler.cancelAll(this);''',
'''        if (enabledSwitch.isChecked()) { HabitReminderScheduler.scheduleAll(this); TreatmentReminderScheduler.scheduleAll(this); }\n        else { HabitReminderScheduler.cancelAll(this); TreatmentReminderScheduler.cancelAll(this); }''')
s=s.replace('''            ReminderScheduler.scheduleAll(this);\n            TreatmentReminderScheduler.scheduleAll(this);''',
'''            ReminderScheduler.scheduleAll(this);\n            HabitReminderScheduler.scheduleAll(this);\n            TreatmentReminderScheduler.scheduleAll(this);''')

# Add helpers before testNotification.
anchor='''    private void testNotification() {'''
helpers='''    private String currentVisitAlerts() {\n        StringBuilder b = new StringBuilder();\n        if (visitD3Switch != null && visitD3Switch.isChecked()) b.append("3,");\n        if (visitD1Switch != null && visitD1Switch.isChecked()) b.append("1,");\n        if (visitDaySwitch != null && visitDaySwitch.isChecked()) b.append("0,");\n        if (b.length() > 0) b.setLength(b.length()-1);\n        return b.toString();\n    }\n\n    private boolean hasAlert(String x) {\n        if (pendingVisitAlerts == null || pendingVisitAlerts.isEmpty()) return false;\n        for (String v : pendingVisitAlerts.split(",")) if (x.equals(v.trim())) return true;\n        return false;\n    }\n\n    private void applyVisitControls() {\n        if (visitD3Switch != null) visitD3Switch.setChecked(hasAlert("3"));\n        if (visitD1Switch != null) visitD1Switch.setChecked(hasAlert("1"));\n        if (visitDaySwitch != null) visitDaySwitch.setChecked(hasAlert("0"));\n        boolean on = TreatmentReminderStore.validDate(pendingVisit) && pendingVisitInterval > 0;\n        if (visitD3Switch != null) visitD3Switch.setEnabled(on);\n        if (visitD1Switch != null) visitD1Switch.setEnabled(on);\n        if (visitDaySwitch != null) visitDaySwitch.setEnabled(on);\n        if (visitTimeButton != null) visitTimeButton.setEnabled(on);\n    }\n\n    private void pickVisitTime() {\n        String[] a = (pendingVisitTime == null || !pendingVisitTime.matches("\\\\d{2}:\\\\d{2}")) ? new String[]{"09","00"} : pendingVisitTime.split(":");\n        int h=9,m=0; try{h=Integer.parseInt(a[0]);m=Integer.parseInt(a[1]);}catch(Exception ignored){}\n        new android.app.TimePickerDialog(this, (view,hour,minute) -> {\n            pendingVisitTime=String.format(java.util.Locale.US,"%02d:%02d",hour,minute);\n            if(visitTimeButton!=null) visitTimeButton.setText("외래 알림 시간 · "+pendingVisitTime);\n            refresh();\n        }, h, m, true).show();\n    }\n\n'''+anchor
if s.count(anchor)!=1: raise SystemExit('helper insert anchor')
s=s.replace(anchor,helpers,1)

# refresh should re-enable controls after a new deep-link import, but must not overwrite user toggles on ordinary refresh.
s=s.replace('''        if (summary != null) summary.setText(summaryText());\n        refreshStatus();''',
'''        if (summary != null) summary.setText(summaryText());\n        applyVisitControls();\n        refreshStatus();''')
p.write_text(s,encoding='utf-8')

# Manifest receiver.
p=Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main/AndroidManifest.xml';s=p.read_text(encoding='utf-8')
old='''        <receiver android:name=".AlarmReceiver" android:exported="false" />\n        <receiver android:name=".TreatmentAlarmReceiver" android:exported="false" />'''
new='''        <receiver android:name=".AlarmReceiver" android:exported="false" />\n        <receiver android:name=".HabitAlarmReceiver" android:exported="false" />\n        <receiver android:name=".TreatmentAlarmReceiver" android:exported="false" />'''
if s.count(old)!=1: raise SystemExit('manifest receiver anchor')
p.write_text(s.replace(old,new,1),encoding='utf-8')
PY

# Guardrails.
grep -q "versionCode 815" "$GRADLE"
grep -q "versionName '8.1.5'" "$GRADLE"
grep -q 'HabitReminderScheduler.scheduleAll' "$PKG/BootReceiver.java"
grep -q 'HabitReminderStore.count' "$PKG/NotificationSettingsActivity.java"
grep -q '외래 알림 시간' "$PKG/NotificationSettingsActivity.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'TreatmentReminderStore' "$PKG/NotificationSettingsActivity.java"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$SRC/app/src/main/AndroidManifest.xml"
echo 'V8.1.5 Android habits/unified notifications patch PASS'
