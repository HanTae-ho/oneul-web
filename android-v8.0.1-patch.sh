#!/usr/bin/env bash
set -euo pipefail
SRC="$GITHUB_WORKSPACE/android-v8"
PKG="$SRC/app/src/main/java/io/github/hantae_ho/twa"
RES="$SRC/app/src/main/res"

sed -i "s/versionCode 800/versionCode 801/; s/versionName '8.0'/versionName '8.0.1'/" "$SRC/app/build.gradle"

rm -f "$PKG/MainActivity.java"
cat > "$PKG/LauncherActivity.java" <<'EOF'
package io.github.hantae_ho.twa;

import android.content.pm.ActivityInfo;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;

public class LauncherActivity extends com.google.androidbrowserhelper.trusted.LauncherActivity {
    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (Build.VERSION.SDK_INT > Build.VERSION_CODES.O) {
            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        } else {
            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED);
        }
    }

    @Override protected Uri getLaunchingUrl() {
        Uri uri = super.getLaunchingUrl();
        if (uri == null) return Uri.parse("https://hantae-ho.github.io/oneul-web/index.html#native=1");
        if ("hantae-ho.github.io".equalsIgnoreCase(uri.getHost()) &&
                uri.getPath() != null && uri.getPath().startsWith("/oneul-web/")) {
            return uri.buildUpon().fragment("native=1").build();
        }
        return uri;
    }
}
EOF
cat > "$PKG/Application.java" <<'EOF'
package io.github.hantae_ho.twa;

public class Application extends android.app.Application {
    @Override public void onCreate() {
        super.onCreate();
        NotificationHelper.ensureChannel(this);
    }
}
EOF
cat > "$PKG/DelegationService.java" <<'EOF'
package io.github.hantae_ho.twa;

public class DelegationService extends com.google.androidbrowserhelper.trusted.DelegationService {
    @Override public void onCreate() { super.onCreate(); }
}
EOF

sed -i 's/MainActivity.class/LauncherActivity.class/g' "$PKG/NotificationHelper.java" "$PKG/NotificationSettingsActivity.java"
sed -i 's|index.html?native=1&from=reminder|index.html#native=1|g; s|index.html?native=1|index.html#native=1|g' "$PKG/NotificationHelper.java" "$PKG/NotificationSettingsActivity.java"

cat > "$SRC/app/src/main/AndroidManifest.xml" <<'EOF'
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />

    <application
        android:name=".Application"
        android:allowBackup="true"
        android:icon="@drawable/ic_launcher"
        android:label="@string/app_name"
        android:manageSpaceActivity="com.google.androidbrowserhelper.trusted.ManageDataLauncherActivity"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.Translucent.NoTitleBar">

        <meta-data android:name="asset_statements" android:resource="@string/asset_statements" />
        <meta-data android:name="web_manifest_url" android:value="https://hantae-ho.github.io/oneul-web/manifest.json" />
        <meta-data android:name="twa_generator" android:value="PWABuilder" />

        <activity
            android:name="com.google.androidbrowserhelper.trusted.ManageDataLauncherActivity"
            android:enabled="true"
            android:exported="false"
            android:excludeFromRecents="true">
            <meta-data android:name="android.support.customtabs.trusted.MANAGE_SPACE_URL"
                android:value="https://hantae-ho.github.io/oneul-web/index.html" />
            <intent-filter>
                <action android:name="android.intent.action.APPLICATION_PREFERENCES" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </activity>

        <activity
            android:name=".LauncherActivity"
            android:label="@string/app_name"
            android:exported="true"
            android:alwaysRetainTaskState="true">
            <meta-data android:name="android.support.customtabs.trusted.DEFAULT_URL"
                android:value="https://hantae-ho.github.io/oneul-web/index.html" />
            <meta-data android:name="android.support.customtabs.trusted.FALLBACK_STRATEGY"
                android:value="customtabs" />
            <meta-data android:name="android.support.customtabs.trusted.SCREEN_ORIENTATION"
                android:value="portrait" />
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter android:autoVerify="true">
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="https" android:host="hantae-ho.github.io" android:pathPrefix="/oneul-web/" />
            </intent-filter>
        </activity>

        <activity android:name="com.google.androidbrowserhelper.trusted.FocusActivity" />
        <activity android:name="com.google.androidbrowserhelper.trusted.WebViewFallbackActivity"
            android:configChanges="orientation|screenSize" />
        <activity android:name="com.google.androidbrowserhelper.trusted.NotificationPermissionRequestActivity" />

        <activity
            android:name=".NotificationSettingsActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/NativeSettingsTheme">
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="oneul" android:host="reminders" />
            </intent-filter>
        </activity>

        <receiver android:name=".AlarmReceiver" android:exported="false" />
        <receiver android:name=".BootReceiver" android:enabled="true" android:exported="false">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <action android:name="android.intent.action.TIME_SET" />
                <action android:name="android.intent.action.TIMEZONE_CHANGED" />
                <action android:name="android.intent.action.MY_PACKAGE_REPLACED" />
            </intent-filter>
        </receiver>

        <service
            android:name=".DelegationService"
            android:enabled="true"
            android:exported="true">
            <meta-data android:name="android.support.customtabs.trusted.SMALL_ICON"
                android:resource="@drawable/ic_notification" />
            <intent-filter>
                <action android:name="android.support.customtabs.trusted.TRUSTED_WEB_ACTIVITY_SERVICE" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </service>
    </application>
</manifest>
EOF

cat > "$RES/values/styles.xml" <<'EOF'
<resources>
    <style name="NativeSettingsTheme" parent="android:style/Theme.Material.Light.NoActionBar">
        <item name="android:fontFamily">sans</item>
        <item name="android:colorAccent">@color/brand</item>
        <item name="android:statusBarColor">@color/brand_dark</item>
        <item name="android:navigationBarColor">@color/brand_dark</item>
        <item name="android:windowBackground">@color/surface</item>
    </style>
</resources>
EOF

cp "$GITHUB_WORKSPACE/icon-512.png" "$RES/drawable/ic_launcher.png"

! grep -R "MainActivity" -n "$SRC/app/src/main" || exit 1
! grep -R "?native=1" -n "$SRC/app/src/main" || exit 1
grep -q "versionCode 801" "$SRC/app/build.gradle"
grep -q 'android:name=".LauncherActivity"' "$SRC/app/src/main/AndroidManifest.xml"
