package io.github.hantae_ho.twa;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;
import java.util.List;

public class NotificationSettingsActivity extends Activity {
    private static final int REQ_NOTIFY = 800;
    private Switch enabledSwitch, detailedSwitch;
    private TextView status, summary;
    private String pendingRisk = "", pendingMeds = "", pendingEats = "", pendingBed = "", pendingBuild = "";

    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        NotificationHelper.ensureChannel(this);
        loadPendingFromPrefs();
        importFromIntent(getIntent());
        buildUi();
    }

    @Override protected void onNewIntent(Intent i) {
        super.onNewIntent(i);
        setIntent(i);
        importFromIntent(i);
        refresh();
    }

    private void loadPendingFromPrefs() {
        android.content.SharedPreferences p = ReminderStore.prefs(this);
        pendingRisk = p.getString(ReminderStore.KEY_RISK, "");
        pendingMeds = p.getString(ReminderStore.KEY_MEDS, "");
        pendingEats = p.getString(ReminderStore.KEY_EATS, "");
        pendingBed = p.getString(ReminderStore.KEY_BED, "");
        pendingBuild = p.getString(ReminderStore.KEY_BUILD, "");
    }

    private void importFromIntent(Intent i) {
        Uri u = i == null ? null : i.getData();
        if (u == null || !"oneul".equals(u.getScheme()) || !"reminders".equals(u.getHost())) return;
        pendingRisk = val(u,"risk");
        pendingMeds = val(u,"meds");
        pendingEats = val(u,"eats");
        pendingBed = val(u,"bed");
        pendingBuild = val(u,"build");
    }

    private String val(Uri u, String k) { String v = u.getQueryParameter(k); return v == null ? "" : v; }

    private void buildUi() {
        ScrollView sc = new ScrollView(this);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        final int padH = dp(22), padTop = dp(22), padBottom = dp(30);
        root.setPadding(padH, padTop, padH, padBottom);
        root.setBackgroundColor(Color.rgb(244,248,250));
        root.setOnApplyWindowInsetsListener((v, insets) -> {
            v.setPadding(padH, padTop + insets.getSystemWindowInsetTop(),
                padH, padBottom + insets.getSystemWindowInsetBottom());
            return insets;
        });
        sc.addView(root);

        TextView title = text("예약 알림", 27, true);
        root.addView(title);
        TextView intro = text("복약·식사·잠처럼 정해진 시각의 알림은 Android가 기기 안에서 예약합니다. 서버로 일정이나 회복기록을 보내지 않습니다.", 16, false);
        intro.setTextColor(Color.rgb(70,85,90)); intro.setPadding(0,dp(8),0,dp(20)); root.addView(intro);

        enabledSwitch = new Switch(this);
        enabledSwitch.setText("예약 알림 사용");
        enabledSwitch.setTextSize(18); enabledSwitch.setPadding(0,dp(8),0,dp(8));
        enabledSwitch.setChecked(ReminderStore.enabled(this));
        root.addView(enabledSwitch);

        detailedSwitch = new Switch(this);
        detailedSwitch.setText("잠금화면 알림에 구체적 내용 표시");
        detailedSwitch.setTextSize(16); detailedSwitch.setPadding(0,dp(8),0,dp(8));
        detailedSwitch.setChecked(ReminderStore.detailed(this));
        root.addView(detailedSwitch);
        TextView privacy = text("기본값은 꺼짐입니다. 꺼두면 ‘챙길 시간입니다’처럼 중립적인 문구만 보여 개인정보 노출을 줄입니다.", 14, false);
        privacy.setTextColor(Color.GRAY); privacy.setPadding(0,0,0,dp(18)); root.addView(privacy);

        TextView h = text("현재 가져온 시간", 19, true); h.setPadding(0,dp(8),0,dp(8)); root.addView(h);
        summary = text("", 16, false); summary.setPadding(dp(14),dp(14),dp(14),dp(14)); summary.setBackgroundColor(Color.WHITE); root.addView(summary);

        status = text("", 14, false); status.setPadding(0,dp(14),0,dp(8)); root.addView(status);

        Button permission = button("Android 알림 권한 확인");
        permission.setOnClickListener(v -> openAppNotificationSettings()); root.addView(permission);

        if (Build.VERSION.SDK_INT >= 31) {
            Button exact = button("정확한 시간 알림 허용");
            exact.setOnClickListener(v -> openExactAlarmSettings()); root.addView(exact);
        }

        Button immediateTest = button("즉시 알림 시험");
        immediateTest.setOnClickListener(v -> testNotification()); root.addView(immediateTest);

        Button exactTest = button("2분 뒤 예약 시험");
        exactTest.setOnClickListener(v -> scheduleExactTest()); root.addView(exactTest);
        TextView testHelp = text("시험 후 앱을 최근 앱에서 밀어 닫고 화면을 꺼둔 채 2분 동안 기다려주세요. 화면을 켜지 않아도 알림이 와야 정상입니다.", 13, false);
        testHelp.setTextColor(Color.GRAY); testHelp.setPadding(0,0,0,dp(8)); root.addView(testHelp);

        Button save = button("저장하고 앱으로 돌아가기");
        save.setOnClickListener(v -> { saveState(); openWebApp(); }); root.addView(save);

        TextView note = text("※ Android 12 이상에서는 정해진 시각에 화면이 꺼져 있어도 알리기 위해 ‘알람 및 리마인더’ 특별 접근 권한이 필요합니다. 권한을 허용하지 않아도 일반 예약은 유지되지만 절전 상태에서는 늦어질 수 있습니다. 앱을 시스템 설정에서 ‘강제중지’하면 예약은 중단됩니다.", 13, false);
        note.setTextColor(Color.GRAY); note.setPadding(0,dp(18),0,0); root.addView(note);

        enabledSwitch.setOnCheckedChangeListener((buttonView, isChecked) -> {
            if (isChecked && !NotificationHelper.canPost(this) && Build.VERSION.SDK_INT >= 33) {
                requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, REQ_NOTIFY);
            }
            refreshStatus();
        });

        setContentView(sc);
        refresh();
    }

    private void refresh() {
        if (summary != null) summary.setText(summaryText());
        refreshStatus();
    }

    private void refreshStatus() {
        if (status == null) return;
        int n = ReminderStore.fromPacked(pendingRisk, pendingMeds, pendingEats, pendingBed).size();
        boolean post = NotificationHelper.canPost(this);
        boolean exact = ReminderScheduler.canScheduleExact(this);
        String p = post ? "알림 허용됨" : "알림 권한 필요";
        String e = exact ? "정확시간 허용됨" : "정확시간 권한 필요";
        status.setText("예약 " + n + "개 · " + p + " · " + e +
            (enabledSwitch != null && enabledSwitch.isChecked() ? " · 저장 시 사용" : " · 저장 시 끔"));
        status.setTextColor(post && exact ? Color.rgb(30,115,90) : Color.rgb(180,80,40));
    }

    private String summaryText() {
        List<Reminder> list = ReminderStore.fromPacked(pendingRisk, pendingMeds, pendingEats, pendingBed);
        if (list.isEmpty()) return "설정된 시간이 없습니다. 오늘 한 걸음 → 내 정보 → 챙기기에서 시간을 정한 뒤 다시 열어주세요.";
        StringBuilder b = new StringBuilder();
        for (Reminder r : list) b.append("• ").append(r.label).append("  ").append(r.time).append("\n");
        return b.toString().trim();
    }

    private void saveState() {
        ReminderStore.importSchedule(this, pendingRisk, pendingMeds, pendingEats, pendingBed, pendingBuild);
        ReminderStore.setDetailed(this, detailedSwitch.isChecked());
        ReminderStore.setEnabled(this, enabledSwitch.isChecked());
        if (enabledSwitch.isChecked() && !NotificationHelper.canPost(this)) {
            Toast.makeText(this, "Android 알림 권한을 허용해야 알림이 표시됩니다.", Toast.LENGTH_LONG).show();
        } else if (enabledSwitch.isChecked() && !ReminderScheduler.canScheduleExact(this)) {
            Toast.makeText(this, "저장했습니다. 정확한 시간 권한이 없어 화면이 꺼진 동안 알림이 늦어질 수 있습니다.", Toast.LENGTH_LONG).show();
        } else {
            Toast.makeText(this, "예약알림 설정을 저장했습니다.", Toast.LENGTH_SHORT).show();
        }
    }

    private void testNotification() {
        if (!NotificationHelper.canPost(this)) {
            if (Build.VERSION.SDK_INT >= 33) requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, REQ_NOTIFY);
            else openAppNotificationSettings();
            return;
        }
        boolean ok = NotificationHelper.showTest(this);
        Toast.makeText(this, ok ? "즉시 시험 알림을 보냈습니다." : "알림을 보내지 못했습니다.", Toast.LENGTH_SHORT).show();
    }

    private void scheduleExactTest() {
        if (!NotificationHelper.canPost(this)) {
            Toast.makeText(this, "먼저 Android 알림 권한을 허용해주세요.", Toast.LENGTH_LONG).show();
            if (Build.VERSION.SDK_INT >= 33) requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, REQ_NOTIFY);
            else openAppNotificationSettings();
            return;
        }
        if (!ReminderScheduler.canScheduleExact(this)) {
            Toast.makeText(this, "먼저 ‘정확한 시간 알림’을 허용해주세요.", Toast.LENGTH_LONG).show();
            openExactAlarmSettings();
            return;
        }
        boolean ok = ReminderScheduler.scheduleExactTest(this, 2 * 60 * 1000L);
        Toast.makeText(this, ok ? "2분 뒤 시험 알림을 예약했습니다. 앱을 닫고 화면을 꺼주세요." : "예약하지 못했습니다.", Toast.LENGTH_LONG).show();
    }

    @Override protected void onResume() {
        super.onResume();
        if (ReminderStore.enabled(this) && ReminderScheduler.canScheduleExact(this)) {
            ReminderScheduler.scheduleAll(this);
        }
        if (status != null) refreshStatus();
    }

    @Override public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] results) {
        super.onRequestPermissionsResult(requestCode, permissions, results);
        if (requestCode == REQ_NOTIFY) {
            refreshStatus();
            if (results.length > 0 && results[0] == PackageManager.PERMISSION_GRANTED)
                Toast.makeText(this, "알림 권한을 허용했습니다.", Toast.LENGTH_SHORT).show();
            else
                Toast.makeText(this, "알림 권한이 허용되지 않았습니다.", Toast.LENGTH_LONG).show();
        }
    }

    private void openAppNotificationSettings() {
        Intent i = new Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS);
        i.putExtra(Settings.EXTRA_APP_PACKAGE, getPackageName());
        startActivity(i);
    }

    private void openExactAlarmSettings() {
        if (Build.VERSION.SDK_INT < 31) {
            Toast.makeText(this, "이 Android 버전에서는 별도 정확시간 권한이 필요하지 않습니다.", Toast.LENGTH_SHORT).show();
            return;
        }
        try {
            Intent i = new Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM);
            i.setData(Uri.parse("package:" + getPackageName()));
            startActivity(i);
        } catch (Exception e) {
            Intent i = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
            i.setData(Uri.parse("package:" + getPackageName()));
            startActivity(i);
        }
    }

    private void openWebApp() {
        Intent i = new Intent(this, LauncherActivity.class);
        i.setAction(Intent.ACTION_VIEW);
        i.setData(Uri.parse("https://hantae-ho.github.io/oneul-web/index.html#native=1"));
        i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
        startActivity(i);
        finish();
    }

    private TextView text(String s, int sp, boolean bold) {
        TextView v = new TextView(this); v.setText(s); v.setTextSize(sp); v.setTextColor(Color.rgb(25,35,38));
        if (bold) v.setTypeface(android.graphics.Typeface.DEFAULT, android.graphics.Typeface.BOLD);
        return v;
    }

    private Button button(String s) {
        Button b = new Button(this); b.setText(s); b.setTextSize(16); b.setAllCaps(false);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, dp(54)); lp.setMargins(0,dp(8),0,0); b.setLayoutParams(lp); return b;
    }

    private int dp(int x) { return Math.round(x * getResources().getDisplayMetrics().density); }
}
