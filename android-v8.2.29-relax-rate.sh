#!/usr/bin/env bash
set -euo pipefail

# Rebuild the proven V8.2.28 native relaxation stack first.
bash "$GITHUB_WORKSPACE/android-v8.2.28-native-relax-tts.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
JAVA="$PKG/RelaxTtsActivity.java"
MANIFEST="$SRC/app/src/main/AndroidManifest.xml"

# Package version.
grep -q "versionCode 848" "$GRADLE"
grep -q "versionName '8.2.28'" "$GRADLE"
sed -i "s/versionCode 848/versionCode 849/; s/versionName '8.2.28'/versionName '8.2.29'/" "$GRADLE"

python3 - <<'PY'
from pathlib import Path
import os
p=Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main/java/io/github/hantae_ho/twa/RelaxTtsActivity.java'
s=p.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    s=s.replace(old,new,1)

one('''    private static final String PREF_VOICE = "voice_name";\n    private static final float SPEECH_RATE = 0.80f;''','''    private static final String PREF_VOICE = "voice_name";\n    private static final String PREF_RATE = "speech_rate_tenths";\n    private static final int DEFAULT_RATE_TENTHS = 8;''','rate constants')

one('''    private Spinner voiceSpinner;\n    private Button previewButton;''','''    private Spinner voiceSpinner;\n    private Spinner rateSpinner;\n    private Button previewButton;''','rate spinner field')

one('''    private final List<Voice> koreanVoices = new ArrayList<>();\n\n    private String guideKey''','''    private final List<Voice> koreanVoices = new ArrayList<>();\n    private int speechRateTenths = DEFAULT_RATE_TENTHS;\n    private boolean rateSpinnerBinding = false;\n\n    private String guideKey''','rate state')

one('''        prefs = getSharedPreferences(PREFS, MODE_PRIVATE);\n        resolveGuide''','''        prefs = getSharedPreferences(PREFS, MODE_PRIVATE);\n        speechRateTenths = normalizeRate(prefs.getInt(PREF_RATE, DEFAULT_RATE_TENTHS));\n        resolveGuide''','load saved rate')

one('''        voiceSpinner = new Spinner(this);\n        LinearLayout.LayoutParams sp = lp(); sp.topMargin = dp(7); root.addView(voiceSpinner, sp);\n\n        previewButton = button("▶ 미리듣기");''','''        voiceSpinner = new Spinner(this);\n        LinearLayout.LayoutParams sp = lp(); sp.topMargin = dp(7); root.addView(voiceSpinner, sp);\n\n        TextView rl = text("말하기 속도", 16, true);\n        LinearLayout.LayoutParams rlp = lp(); rlp.topMargin = dp(18); root.addView(rl, rlp);\n\n        rateSpinner = new Spinner(this);\n        LinearLayout.LayoutParams rsp = lp(); rsp.topMargin = dp(7); root.addView(rateSpinner, rsp);\n\n        previewButton = button("▶ 미리듣기");''','rate UI')

# The proven code applies the fixed rate in onInit and applyVoice. Route both through the selected value.
s=s.replace('tts.setSpeechRate(SPEECH_RATE);','applySpeechRate();')
if 'SPEECH_RATE' in s:
    raise SystemExit('fixed SPEECH_RATE reference remains')

one('''        ready = true;\n        loadVoices();\n        previewButton.setEnabled(true);\n        playPauseButton.setEnabled(true);\n        statusView.setText("음성을 확인한 뒤 가이드를 시작하세요. 말하기 속도는 0.80입니다.");''','''        ready = true;\n        loadRateOptions();\n        loadVoices();\n        previewButton.setEnabled(true);\n        playPauseButton.setEnabled(true);\n        statusView.setText("음성과 말하기 속도를 확인한 뒤 가이드를 시작하세요. 현재 " + rateNumber() + "배입니다.");''','init rate UI')

methods='''    private int normalizeRate(int value) {\n        return (value >= 7 && value <= 10) ? value : DEFAULT_RATE_TENTHS;\n    }\n\n    private String rateNumber() {\n        return speechRateTenths == 10 ? "1.0" : "0." + speechRateTenths;\n    }\n\n    private void applySpeechRate() {\n        if (tts != null) tts.setSpeechRate(speechRateTenths / 10.0f);\n    }\n\n    private void loadRateOptions() {\n        if (rateSpinner == null) return;\n        List<String> labels = new ArrayList<>();\n        labels.add("느리게 · 0.7배");\n        labels.add("차분하게 · 0.8배 · 기본");\n        labels.add("조금 빠르게 · 0.9배");\n        labels.add("보통 · 1.0배");\n        rateSpinnerBinding = true;\n        ArrayAdapter<String> a = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, labels);\n        rateSpinner.setAdapter(a);\n        rateSpinner.setSelection(speechRateTenths - 7, false);\n        rateSpinnerBinding = false;\n        rateSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {\n            @Override public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {\n                if (rateSpinnerBinding || position < 0 || position > 3) return;\n                int next = position + 7;\n                if (next == speechRateTenths) return;\n                if (playing) stopGuide(false);\n                speechRateTenths = next;\n                prefs.edit().putInt(PREF_RATE, speechRateTenths).apply();\n                applySpeechRate();\n                if (statusView != null) statusView.setText("말하기 속도를 " + rateNumber() + "배로 저장했습니다. 미리듣기로 확인해보세요.");\n            }\n            @Override public void onNothingSelected(AdapterView<?> parent) { }\n        });\n    }\n\n'''
one('''    private void loadVoices() {''',methods+'''    private void loadVoices() {''','rate methods')

one('''        statusView.setText("미리듣기 중 · 말하기 속도 0.80");''','''        statusView.setText("미리듣기 중 · 말하기 속도 " + rateNumber() + "배");''','preview rate status')

p.write_text(s,encoding='utf-8')
PY

# Guardrails for this version and the new user-selectable rate.
grep -q "versionCode 849" "$GRADLE"
grep -q "versionName '8.2.29'" "$GRADLE"
grep -q 'android.permission.WAKE_LOCK' "$MANIFEST"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$MANIFEST"
grep -q 'android:name=".RelaxTtsActivity"' "$MANIFEST"
grep -q 'android:scheme="oneul" android:host="relax"' "$MANIFEST"
grep -q 'speech_rate_tenths' "$JAVA"
grep -q '느리게 · 0.7배' "$JAVA"
grep -q '차분하게 · 0.8배 · 기본' "$JAVA"
grep -q '조금 빠르게 · 0.9배' "$JAVA"
grep -q '보통 · 1.0배' "$JAVA"
grep -q 'prefs.edit().putInt(PREF_RATE' "$JAVA"
grep -q 'tts.setSpeechRate(speechRateTenths / 10.0f)' "$JAVA"
grep -q 'PARTIAL_WAKE_LOCK' "$JAVA"
grep -q 'releaseWakeLock' "$JAVA"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'HabitReminderScheduler.scheduleAll' "$PKG/BootReceiver.java"

echo 'V8.2.29 Android relaxation rate patch PASS'
