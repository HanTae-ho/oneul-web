#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.27 native stack first. Existing reminder engines stay untouched.
bash "$GITHUB_WORKSPACE/android-v8.2.27-relax-tts.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
MANIFEST="$SRC/app/src/main/AndroidManifest.xml"

# Package version only after the proven stack has been recreated.
grep -q "versionCode 847" "$GRADLE"
grep -q "versionName '8.2.27'" "$GRADLE"
sed -i "s/versionCode 847/versionCode 848/; s/versionName '8.2.27'/versionName '8.2.28'/" "$GRADLE"

cat > "$PKG/RelaxTtsActivity.java" <<'EOF'
package io.github.hantae_ho.twa;

import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.media.AudioManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.PowerManager;
import android.os.SystemClock;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.speech.tts.Voice;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.Spinner;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Set;

public class RelaxTtsActivity extends Activity implements TextToSpeech.OnInitListener {
    private static final String PREFS = "relax_tts";
    private static final String PREF_VOICE = "voice_name";
    private static final float SPEECH_RATE = 0.80f;
    private static final long WAKELOCK_MAX_MS = 30L * 60L * 1000L;

    private final Handler handler = new Handler(Looper.getMainLooper());
    private TextToSpeech tts;
    private PowerManager.WakeLock wakeLock;
    private SharedPreferences prefs;
    private Spinner voiceSpinner;
    private Button previewButton;
    private Button playPauseButton;
    private Button stopButton;
    private TextView guideTitleView;
    private TextView statusView;
    private final List<Voice> koreanVoices = new ArrayList<>();

    private String guideKey = "meditation";
    private String guideTitle = "명상";
    private Step[] steps = new Step[0];
    private int index = 0;
    private long generation = 0;
    private boolean ready = false;
    private boolean playing = false;
    private boolean paused = false;
    private boolean speaking = false;
    private boolean waiting = false;
    private long waitDeadline = 0;
    private long waitRemaining = 0;
    private Runnable waitRunnable;
    private boolean spinnerBinding = false;

    private static final class Step {
        final String text;
        final long pauseMs;
        Step(String text, long pauseMs) { this.text = text; this.pauseMs = pauseMs; }
    }

    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setVolumeControlStream(AudioManager.STREAM_MUSIC);
        prefs = getSharedPreferences(PREFS, MODE_PRIVATE);
        resolveGuide(getIntent() != null ? getIntent().getData() : null);
        buildUi();
        PowerManager pm = (PowerManager) getSystemService(POWER_SERVICE);
        wakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "oneul:RelaxGuide");
        wakeLock.setReferenceCounted(false);
        tts = new TextToSpeech(this, this);
    }

    private void resolveGuide(Uri data) {
        String key = null;
        if (data != null && "oneul".equalsIgnoreCase(data.getScheme()) && "relax".equalsIgnoreCase(data.getHost())) {
            List<String> seg = data.getPathSegments();
            if (seg != null && !seg.isEmpty()) key = seg.get(0);
        }
        if ("pmr".equals(key)) {
            guideKey = "pmr"; guideTitle = "점진적 근육 이완 · PMR"; steps = pmrSteps();
        } else if ("visual".equals(key)) {
            guideKey = "visual"; guideTitle = "심상화"; steps = visualSteps();
        } else {
            guideKey = "meditation"; guideTitle = "명상"; steps = meditationSteps();
        }
    }

    private void buildUi() {
        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(20), dp(22), dp(20), dp(28));
        root.setBackgroundColor(Color.rgb(248, 250, 251));
        scroll.addView(root, new ScrollView.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        TextView h = text("이완 음성 가이드", 24, true);
        h.setTextColor(Color.rgb(27, 67, 78));
        root.addView(h);

        guideTitleView = text(guideTitle, 19, true);
        guideTitleView.setTextColor(Color.rgb(31, 111, 138));
        LinearLayout.LayoutParams hp = lp(); hp.topMargin = dp(8); root.addView(guideTitleView, hp);

        TextView note = text("화면은 자연스럽게 꺼져도 됩니다. 재생 중에는 화면을 켜두지 않고 음성 안내와 문장 사이의 쉼만 계속 진행합니다.", 14, false);
        note.setTextColor(Color.rgb(78, 91, 96));
        LinearLayout.LayoutParams np = lp(); np.topMargin = dp(10); root.addView(note, np);

        TextView vl = text("가이드 음성", 16, true);
        LinearLayout.LayoutParams vlp = lp(); vlp.topMargin = dp(22); root.addView(vl, vlp);

        voiceSpinner = new Spinner(this);
        LinearLayout.LayoutParams sp = lp(); sp.topMargin = dp(7); root.addView(voiceSpinner, sp);

        previewButton = button("▶ 미리듣기");
        previewButton.setEnabled(false);
        LinearLayout.LayoutParams pp = lp(); pp.topMargin = dp(9); root.addView(previewButton, pp);

        statusView = text("음성 엔진을 준비하고 있습니다.", 14, false);
        statusView.setTextColor(Color.rgb(90, 101, 105));
        LinearLayout.LayoutParams stp = lp(); stp.topMargin = dp(18); root.addView(statusView, stp);

        playPauseButton = button("▶ 가이드 시작");
        playPauseButton.setEnabled(false);
        LinearLayout.LayoutParams bp = lp(); bp.topMargin = dp(10); root.addView(playPauseButton, bp);

        stopButton = button("■ 종료");
        stopButton.setEnabled(false);
        LinearLayout.LayoutParams sbp = lp(); sbp.topMargin = dp(8); root.addView(stopButton, sbp);

        Button back = button("앱으로 돌아가기");
        LinearLayout.LayoutParams backp = lp(); backp.topMargin = dp(18); root.addView(back, backp);

        previewButton.setOnClickListener(v -> previewVoice());
        playPauseButton.setOnClickListener(v -> {
            if (!playing) startGuide();
            else if (!paused) pauseGuide();
            else resumeGuide();
        });
        stopButton.setOnClickListener(v -> stopGuide(true));
        back.setOnClickListener(v -> { stopGuide(false); finish(); });
        setContentView(scroll);
    }

    @Override public void onInit(int status) {
        if (status != TextToSpeech.SUCCESS) {
            statusView.setText("기기의 TTS 엔진을 시작하지 못했습니다. Android 음성 설정을 확인해주세요.");
            return;
        }
        int lang = tts.setLanguage(Locale.KOREAN);
        if (lang == TextToSpeech.LANG_MISSING_DATA || lang == TextToSpeech.LANG_NOT_SUPPORTED) {
            statusView.setText("이 기기에는 한국어 TTS 음성이 준비되어 있지 않습니다.");
            return;
        }
        tts.setSpeechRate(SPEECH_RATE);
        tts.setPitch(1.0f);
        tts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
            @Override public void onStart(String utteranceId) {
                if (!utteranceId.startsWith("guide:")) return;
                final long g = parseGeneration(utteranceId);
                handler.post(() -> { if (g == generation) { speaking = true; updateStatus(); } });
            }
            @Override public void onDone(String utteranceId) {
                if (!utteranceId.startsWith("guide:")) return;
                final long g = parseGeneration(utteranceId);
                handler.post(() -> onGuideUtteranceDone(g));
            }
            @Override public void onError(String utteranceId) {
                if (!utteranceId.startsWith("guide:")) return;
                final long g = parseGeneration(utteranceId);
                handler.post(() -> { if (g == generation && playing && !paused) { statusView.setText("음성 재생 중 오류가 발생했습니다."); stopGuide(false); } });
            }
        });
        ready = true;
        loadVoices();
        previewButton.setEnabled(true);
        playPauseButton.setEnabled(true);
        statusView.setText("음성을 확인한 뒤 가이드를 시작하세요. 말하기 속도는 0.80입니다.");
    }

    private void loadVoices() {
        koreanVoices.clear();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Set<Voice> all = tts.getVoices();
            if (all != null) {
                for (Voice v : all) {
                    Locale l = v.getLocale();
                    if (l != null && "ko".equalsIgnoreCase(l.getLanguage())) koreanVoices.add(v);
                }
            }
        }
        Collections.sort(koreanVoices, Comparator.comparing(Voice::getName, String.CASE_INSENSITIVE_ORDER));
        List<String> labels = new ArrayList<>();
        labels.add("기기 기본 한국어 음성");
        for (Voice v : koreanVoices) labels.add(v.getName() + " · " + v.getLocale().toLanguageTag());
        spinnerBinding = true;
        ArrayAdapter<String> a = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, labels);
        voiceSpinner.setAdapter(a);
        String saved = prefs.getString(PREF_VOICE, "");
        int selected = 0;
        for (int i = 0; i < koreanVoices.size(); i++) if (koreanVoices.get(i).getName().equals(saved)) { selected = i + 1; break; }
        voiceSpinner.setSelection(selected, false);
        applyVoice(selected);
        spinnerBinding = false;
        voiceSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                if (spinnerBinding) return;
                if (playing) stopGuide(false);
                applyVoice(position);
            }
            @Override public void onNothingSelected(AdapterView<?> parent) { }
        });
    }

    private void applyVoice(int position) {
        if (!ready) return;
        if (position > 0 && position - 1 < koreanVoices.size()) {
            Voice v = koreanVoices.get(position - 1);
            tts.setVoice(v);
            prefs.edit().putString(PREF_VOICE, v.getName()).apply();
        } else {
            tts.setLanguage(Locale.KOREAN);
            tts.setSpeechRate(SPEECH_RATE);
            prefs.edit().remove(PREF_VOICE).apply();
        }
        tts.setSpeechRate(SPEECH_RATE);
    }

    private void previewVoice() {
        if (!ready) return;
        if (playing) stopGuide(false);
        tts.stop();
        Bundle b = new Bundle();
        tts.speak("안녕하세요. 이 목소리로 이완 가이드를 천천히 안내해드릴게요.", TextToSpeech.QUEUE_FLUSH, b, "preview");
        statusView.setText("미리듣기 중 · 말하기 속도 0.80");
    }

    private void startGuide() {
        if (!ready || steps.length == 0) return;
        tts.stop();
        cancelWait();
        generation++;
        index = 0;
        playing = true;
        paused = false;
        speaking = false;
        waiting = false;
        acquireWakeLock();
        playPauseButton.setText("⏸ 일시정지");
        stopButton.setEnabled(true);
        speakCurrent();
    }

    private void speakCurrent() {
        if (!playing || paused || index >= steps.length) {
            if (playing && index >= steps.length) finishGuide();
            return;
        }
        acquireWakeLock();
        speaking = true;
        waiting = false;
        updateStatus();
        Bundle b = new Bundle();
        String id = "guide:" + generation + ":" + index;
        int r = tts.speak(steps[index].text, TextToSpeech.QUEUE_FLUSH, b, id);
        if (r == TextToSpeech.ERROR) {
            statusView.setText("음성 재생을 시작하지 못했습니다.");
            stopGuide(false);
        }
    }

    private void onGuideUtteranceDone(long g) {
        if (g != generation || !playing || paused) return;
        speaking = false;
        long pause = steps[index].pauseMs;
        index++;
        if (index >= steps.length) { finishGuide(); return; }
        scheduleWait(pause);
    }

    private void scheduleWait(long ms) {
        waiting = true;
        waitRemaining = Math.max(0, ms);
        waitDeadline = SystemClock.elapsedRealtime() + waitRemaining;
        updateStatus();
        final long g = generation;
        waitRunnable = () -> {
            if (g != generation || !playing || paused) return;
            waiting = false;
            waitRemaining = 0;
            speakCurrent();
        };
        handler.postDelayed(waitRunnable, waitRemaining);
    }

    private void pauseGuide() {
        if (!playing || paused) return;
        paused = true;
        generation++;
        if (waiting && waitRunnable != null) {
            waitRemaining = Math.max(0, waitDeadline - SystemClock.elapsedRealtime());
            handler.removeCallbacks(waitRunnable);
            waitRunnable = null;
        }
        if (speaking) {
            tts.stop();
            speaking = false;
            waiting = false;
        }
        releaseWakeLock();
        playPauseButton.setText("▶ 계속");
        statusView.setText("일시정지됨");
    }

    private void resumeGuide() {
        if (!playing || !paused) return;
        paused = false;
        acquireWakeLock();
        playPauseButton.setText("⏸ 일시정지");
        if (waitRemaining > 0) {
            long remain = waitRemaining;
            waitRemaining = 0;
            scheduleWait(remain);
        } else {
            speakCurrent();
        }
    }

    private void finishGuide() {
        String done = guideTitle + " 가이드를 마쳤습니다.";
        stopGuide(false);
        statusView.setText(done);
    }

    private void stopGuide(boolean user) {
        generation++;
        cancelWait();
        if (tts != null) tts.stop();
        playing = false;
        paused = false;
        speaking = false;
        waiting = false;
        index = 0;
        waitRemaining = 0;
        releaseWakeLock();
        if (playPauseButton != null) { playPauseButton.setText("▶ 가이드 시작"); playPauseButton.setEnabled(ready); }
        if (stopButton != null) stopButton.setEnabled(false);
        if (user && statusView != null) statusView.setText("음성 가이드를 종료했습니다.");
    }

    private void cancelWait() {
        if (waitRunnable != null) handler.removeCallbacks(waitRunnable);
        waitRunnable = null;
        waitDeadline = 0;
    }

    private void acquireWakeLock() {
        if (wakeLock != null && !wakeLock.isHeld()) wakeLock.acquire(WAKELOCK_MAX_MS);
    }

    private void releaseWakeLock() {
        if (wakeLock != null && wakeLock.isHeld()) wakeLock.release();
    }

    private void updateStatus() {
        if (statusView == null) return;
        if (paused) statusView.setText("일시정지됨");
        else if (waiting) statusView.setText("잠시 쉬는 중 · " + Math.min(index + 1, steps.length) + " / " + steps.length);
        else if (speaking) statusView.setText("안내 중 · " + Math.min(index + 1, steps.length) + " / " + steps.length);
    }

    private long parseGeneration(String id) {
        try { return Long.parseLong(id.split(":")[1]); } catch (Exception e) { return -1; }
    }

    @Override public void onBackPressed() {
        stopGuide(false);
        super.onBackPressed();
    }

    @Override protected void onDestroy() {
        stopGuide(false);
        if (tts != null) { tts.shutdown(); tts = null; }
        super.onDestroy();
    }

    private LinearLayout.LayoutParams lp() {
        return new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    }

    private TextView text(String value, int sp, boolean bold) {
        TextView t = new TextView(this);
        t.setText(value);
        t.setTextSize(sp);
        t.setLineSpacing(0, 1.18f);
        if (bold) t.setTypeface(t.getTypeface(), android.graphics.Typeface.BOLD);
        return t;
    }

    private Button button(String label) {
        Button b = new Button(this);
        b.setText(label);
        b.setAllCaps(false);
        b.setGravity(Gravity.CENTER);
        return b;
    }

    private int dp(int v) { return Math.round(v * getResources().getDisplayMetrics().density); }

    private Step[] pmrSteps() {
        return new Step[]{
            new Step("편안하게 앉거나 누워보세요. 발과 손을 편하게 두고, 통증이 있는 부위는 억지로 힘주지 않아도 됩니다.",5000),
            new Step("먼저 이마에 천천히 힘을 줍니다.",5000),
            new Step("이제 힘을 놓고, 이마가 부드러워지는 느낌을 알아차립니다.",8000),
            new Step("눈을 부드럽게 꼭 감고, 얼굴의 긴장을 느껴봅니다.",5000),
            new Step("이제 눈과 볼의 힘을 풀어봅니다.",8000),
            new Step("턱을 가볍게 다물어 힘을 줍니다.",5000),
            new Step("턱을 놓고 입 주변의 힘도 함께 풀어봅니다.",8000),
            new Step("어깨를 귀 쪽으로 천천히 올립니다.",5000),
            new Step("이제 어깨를 내려놓고, 목과 어깨가 느슨해지는 것을 느껴봅니다.",10000),
            new Step("양손을 가볍게 주먹 쥐고 팔에도 힘을 줍니다.",5000),
            new Step("손을 펴고 팔 전체의 힘을 놓습니다.",10000),
            new Step("배와 등에 가볍게 힘을 줍니다. 무리하지 않습니다.",5000),
            new Step("이제 몸통의 힘을 풀고, 호흡이 자연스럽게 오가는 것을 느껴봅니다.",10000),
            new Step("허벅지와 종아리, 발에 가볍게 힘을 줍니다.",5000),
            new Step("이제 다리와 발의 힘을 모두 풀어봅니다.",10000),
            new Step("머리부터 발끝까지 남아 있는 긴장이 있는지 천천히 살펴봅니다.",12000),
            new Step("숨을 천천히 들이쉬고, 내쉬면서 남아 있는 힘을 한 번 더 놓아봅니다.",10000),
            new Step("준비가 되면 손가락과 발가락을 가볍게 움직이고, 천천히 눈을 뜹니다.",0)
        };
    }

    private Step[] visualSteps() {
        return new Step[]{
            new Step("편안한 자세를 잡고, 가능하면 눈을 감아봅니다. 지금은 조용하고 안전한 장소를 떠올리는 시간입니다.",7000),
            new Step("혼자 편안하게 머물 수 있는 장소 하나를 떠올려보세요. 실제로 가본 곳이어도 좋고, 상상 속의 장소여도 좋습니다.",15000),
            new Step("그곳의 빛과 색, 주변의 모습을 천천히 살펴봅니다.",15000),
            new Step("이제 그곳에서 들리는 소리에 귀를 기울여봅니다. 가까운 소리와 멀리 있는 소리를 차례로 떠올려보세요.",15000),
            new Step("공기의 냄새와 온도도 느껴봅니다. 따뜻한지, 시원한지, 바람이 있는지도 천천히 알아차립니다.",15000),
            new Step("몸이 닿아 있는 느낌을 떠올립니다. 발밑의 감촉, 의자나 바닥의 느낌, 피부에 닿는 공기를 느껴봅니다.",15000),
            new Step("나를 편안하게 해주는 작은 세부 모습을 하나씩 더 채워봅니다.",20000),
            new Step("어깨와 얼굴의 힘을 풀고, 숨을 천천히 들이쉬고 내쉽니다.",15000),
            new Step("잠시 그 장소에 그대로 머물러봅니다. 무엇을 해야 할 필요는 없습니다.",20000),
            new Step("준비가 되면 지금 있는 공간으로 천천히 돌아옵니다. 손과 발을 가볍게 움직이고 눈을 뜹니다.",0)
        };
    }

    private Step[] meditationSteps() {
        return new Step[]{
            new Step("등을 편안하게 곧게 펴고 앉아봅니다. 손은 편하게 두고, 시선은 감거나 아래쪽에 둡니다.",6000),
            new Step("첫 번째로, 숨을 조금 깊게 들이쉬고 천천히 내쉽니다.",8000),
            new Step("두 번째로, 다시 천천히 들이쉬고 길게 내쉽니다.",8000),
            new Step("세 번째로, 한 번 더 천천히 들이쉬고 내쉽니다.",8000),
            new Step("이제 호흡을 바꾸려 하지 말고 자연스러운 리듬을 느껴봅니다.",7000),
            new Step("하나.",3500), new Step("둘.",3500), new Step("셋.",3500), new Step("넷.",3500), new Step("다섯.",3500),
            new Step("여섯.",3500), new Step("일곱.",3500), new Step("여덟.",3500), new Step("아홉.",3500), new Step("열.",5000),
            new Step("생각이 떠오르면 밀어내지 않아도 됩니다. 생각이 있다는 것을 알아차린 뒤, 다시 호흡과 숫자로 천천히 돌아옵니다.",10000),
            new Step("숫자를 잊었거나 마음이 멀리 갔다면 괜찮습니다. 다시 하나부터 시작해봅니다.",8000),
            new Step("한 번 더 자연스럽게 숨을 들이쉬고 내쉬면서 몸이 지금 이 자리에 있는 느낌을 알아차립니다.",8000),
            new Step("준비가 되면 눈을 천천히 뜨고 주변을 바라봅니다.",0)
        };
    }
}
EOF

python3 - <<'PY'
from pathlib import Path
import os
m = Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main/AndroidManifest.xml'
s = m.read_text(encoding='utf-8')
perm = '<uses-permission android:name="android.permission.WAKE_LOCK" />'
if perm not in s:
    marker = '<application'
    if marker not in s: raise SystemExit('application marker missing')
    s = s.replace(marker, perm+'\n    '+marker, 1)
activity = '''        <activity
            android:name=".RelaxTtsActivity"
            android:exported="true"
            android:excludeFromRecents="true"
            android:launchMode="singleTop"
            android:screenOrientation="portrait"
            android:theme="@android:style/Theme.DeviceDefault.Light.NoActionBar">
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="oneul" android:host="relax" />
            </intent-filter>
        </activity>
'''
if 'android:name=".RelaxTtsActivity"' not in s:
    if '</application>' not in s: raise SystemExit('application close missing')
    s = s.replace('</application>', activity+'    </application>', 1)
m.write_text(s,encoding='utf-8')
PY

# Guardrails: native guide is new, reminder engines and TWA entry remain unchanged.
grep -q "versionCode 848" "$GRADLE"
grep -q "versionName '8.2.28'" "$GRADLE"
grep -q 'android.permission.WAKE_LOCK' "$MANIFEST"
grep -q 'android:name=".RelaxTtsActivity"' "$MANIFEST"
grep -q 'android:scheme="oneul" android:host="relax"' "$MANIFEST"
grep -q 'PowerManager.PARTIAL_WAKE_LOCK' "$PKG/RelaxTtsActivity.java"
grep -q 'SPEECH_RATE = 0.80f' "$PKG/RelaxTtsActivity.java"
grep -q 'getVoices' "$PKG/RelaxTtsActivity.java"
grep -q '미리듣기' "$PKG/RelaxTtsActivity.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'HabitReminderScheduler.scheduleAll' "$PKG/BootReceiver.java"
grep -q 'android.support.customtabs.trusted.DEFAULT_URL' "$MANIFEST"

echo 'V8.2.28 Android native relaxation TTS patch PASS'
