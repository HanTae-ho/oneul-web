#!/usr/bin/env bash
set -euo pipefail

# Rebuild the verified V8.2.49 native stack first, then add only the MindPro TTS bridge.
bash "$GITHUB_WORKSPACE/android-v8.2.49-mindpro-guide-voice.sh"

SRC="$GITHUB_WORKSPACE/android-v8"
GRADLE="$SRC/app/build.gradle"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
MAN="$SRC/app/src/main/AndroidManifest.xml"

# Package version.
grep -q "versionCode 869" "$GRADLE"
grep -q "versionName '8.2.49'" "$GRADLE"
sed -i "s/versionCode 869/versionCode 870/; s/versionName '8.2.49'/versionName '8.2.50'/" "$GRADLE"

cat > "$PKG/MindProVoiceService.java" <<'EOF'
package io.github.hantae_ho.twa;

import android.app.Service;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.os.IBinder;
import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import android.speech.tts.Voice;

import java.util.Locale;
import java.util.Set;

public class MindProVoiceService extends Service implements TextToSpeech.OnInitListener {
    public static final String ACTION_SPEAK = "io.github.hantae_ho.twa.MINDPRO_SPEAK";
    public static final String ACTION_STOP = "io.github.hantae_ho.twa.MINDPRO_STOP";
    public static final String EXTRA_TEXT = "text";

    private static final String PREFS = "relax_tts";
    private static final String PREF_VOICE = "voice_name";
    private static final String PREF_RATE = "speech_rate_tenths";
    private static final int DEFAULT_RATE_TENTHS = 8;
    private static final int MAX_TEXT = 12000;

    private TextToSpeech tts;
    private boolean ready = false;
    private String pendingText = "";
    private long generation = 0L;
    private String currentUtterance = "";

    @Override public IBinder onBind(Intent intent) { return null; }

    @Override public int onStartCommand(Intent intent, int flags, int startId) {
        String action = intent != null ? intent.getAction() : "";
        if (ACTION_STOP.equals(action)) {
            stopNow();
            stopSelf();
            return START_NOT_STICKY;
        }
        if (ACTION_SPEAK.equals(action)) {
            String text = intent != null ? intent.getStringExtra(EXTRA_TEXT) : "";
            text = text == null ? "" : text.trim();
            if (text.length() > MAX_TEXT) text = text.substring(0, MAX_TEXT);
            if (text.isEmpty()) return START_NOT_STICKY;
            pendingText = text;
            if (tts == null) tts = new TextToSpeech(this, this);
            else if (ready) speakPending();
        }
        return START_NOT_STICKY;
    }

    @Override public void onInit(int status) {
        if (status != TextToSpeech.SUCCESS || tts == null) {
            ready = false;
            stopSelf();
            return;
        }
        int lang = tts.setLanguage(Locale.KOREAN);
        if (lang == TextToSpeech.LANG_MISSING_DATA || lang == TextToSpeech.LANG_NOT_SUPPORTED) {
            ready = false;
            stopSelf();
            return;
        }
        applySavedVoiceAndRate();
        tts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
            @Override public void onStart(String utteranceId) { }
            @Override public void onDone(String utteranceId) {
                if (utteranceId != null && utteranceId.equals(currentUtterance)) {
                    currentUtterance = "";
                    stopSelf();
                }
            }
            @Override public void onError(String utteranceId) {
                if (utteranceId != null && utteranceId.equals(currentUtterance)) {
                    currentUtterance = "";
                    stopSelf();
                }
            }
            @Override public void onStop(String utteranceId, boolean interrupted) { }
        });
        ready = true;
        speakPending();
    }

    private void applySavedVoiceAndRate() {
        if (tts == null) return;
        SharedPreferences prefs = getSharedPreferences(PREFS, MODE_PRIVATE);
        int rateTenths = prefs.getInt(PREF_RATE, DEFAULT_RATE_TENTHS);
        if (rateTenths < 7 || rateTenths > 10) rateTenths = DEFAULT_RATE_TENTHS;
        tts.setSpeechRate(rateTenths / 10.0f);
        tts.setPitch(1.0f);

        String savedVoice = prefs.getString(PREF_VOICE, "");
        if (savedVoice == null || savedVoice.isEmpty() || Build.VERSION.SDK_INT < Build.VERSION_CODES.LOLLIPOP) return;
        Set<Voice> voices = tts.getVoices();
        if (voices == null) return;
        for (Voice voice : voices) {
            if (savedVoice.equals(voice.getName())) {
                tts.setVoice(voice);
                break;
            }
        }
    }

    private void speakPending() {
        if (!ready || tts == null) return;
        String text = pendingText;
        pendingText = "";
        if (text == null || text.trim().isEmpty()) return;
        applySavedVoiceAndRate();
        generation++;
        currentUtterance = "mindpro:" + generation;
        Bundle params = new Bundle();
        int result = tts.speak(text, TextToSpeech.QUEUE_FLUSH, params, currentUtterance);
        if (result == TextToSpeech.ERROR) {
            currentUtterance = "";
            stopSelf();
        }
    }

    private void stopNow() {
        generation++;
        pendingText = "";
        currentUtterance = "";
        if (tts != null) tts.stop();
    }

    @Override public void onDestroy() {
        stopNow();
        if (tts != null) {
            tts.shutdown();
            tts = null;
        }
        ready = false;
        super.onDestroy();
    }
}
EOF

cat > "$PKG/MindProVoiceBridgeActivity.java" <<'EOF'
package io.github.hantae_ho.twa;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;

public class MindProVoiceBridgeActivity extends Activity {
    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        dispatch(getIntent());
    }

    @Override protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        dispatch(intent);
    }

    private void dispatch(Intent incoming) {
        Uri data = incoming != null ? incoming.getData() : null;
        if (data != null && "oneul".equalsIgnoreCase(data.getScheme()) && "mindpro-voice".equalsIgnoreCase(data.getHost())) {
            String action = data.getQueryParameter("action");
            Intent service = new Intent(this, MindProVoiceService.class);
            if ("stop".equalsIgnoreCase(action)) {
                service.setAction(MindProVoiceService.ACTION_STOP);
                startService(service);
            } else if ("speak".equalsIgnoreCase(action)) {
                String text = data.getQueryParameter("text");
                if (text != null && !text.trim().isEmpty()) {
                    service.setAction(MindProVoiceService.ACTION_SPEAK);
                    service.putExtra(MindProVoiceService.EXTRA_TEXT, text);
                    startService(service);
                }
            }
        }
        finish();
        overridePendingTransition(0, 0);
    }
}
EOF

python3 - <<'PY'
from pathlib import Path
import os
m=Path(os.environ['GITHUB_WORKSPACE'])/'android-v8/app/src/main/AndroidManifest.xml'
s=m.read_text(encoding='utf-8')
service='''        <service
            android:name=".MindProVoiceService"
            android:exported="false" />
'''
activity='''        <activity
            android:name=".MindProVoiceBridgeActivity"
            android:exported="true"
            android:excludeFromRecents="true"
            android:noHistory="true"
            android:launchMode="singleTop"
            android:theme="@android:style/Theme.Translucent.NoTitleBar">
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="oneul" android:host="mindpro-voice" />
            </intent-filter>
        </activity>
'''
if 'android:name=".MindProVoiceService"' not in s:
    s=s.replace('</application>',service+'    </application>',1)
if 'android:name=".MindProVoiceBridgeActivity"' not in s:
    s=s.replace('</application>',activity+'    </application>',1)
m.write_text(s,encoding='utf-8')
PY

# Guardrails: only the new bridge is added; proven native stack remains.
grep -q "versionCode 870" "$GRADLE"
grep -q "versionName '8.2.50'" "$GRADLE"
grep -q 'android.permission.WAKE_LOCK' "$MAN"
grep -q 'android.permission.SCHEDULE_EXACT_ALARM' "$MAN"
grep -q 'android:name=".MindProVoiceService"' "$MAN"
grep -q 'android:name=".MindProVoiceBridgeActivity"' "$MAN"
grep -q 'android:scheme="oneul" android:host="mindpro-voice"' "$MAN"
grep -q 'TextToSpeech.QUEUE_FLUSH' "$PKG/MindProVoiceService.java"
grep -q 'speech_rate_tenths' "$PKG/MindProVoiceService.java"
grep -q 'voice_name' "$PKG/MindProVoiceService.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/HabitReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/ReminderScheduler.java"
grep -q 'setExactAndAllowWhileIdle' "$PKG/TreatmentReminderScheduler.java"
grep -q 'HabitReminderScheduler.scheduleAll' "$PKG/BootReceiver.java"
grep -q 'scheduleNextForOffset' "$PKG/TreatmentAlarmReceiver.java"
grep -q 'PowerManager.PARTIAL_WAKE_LOCK' "$PKG/RelaxTtsActivity.java"

echo 'V8.2.50 Android native MindPro voice bridge PASS'
