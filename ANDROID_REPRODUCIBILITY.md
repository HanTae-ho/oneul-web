# Android V9.0.20 재현성 기준

이 문서는 현재 안정판 **V9.0.20 / versionCode 915**의 Android 네이티브 패키지를 다시 만들 때 사용할 기준을 고정한다. 웹앱 제품 코드와 Android 네이티브 동작을 변경하기 위한 문서가 아니다.

## 고정 원본

- 패키지: `io.github.hantae_ho.twa`
- versionName: `9.0.20`
- versionCode: `915`
- Android 릴리스 원본 커밋: `c79a2957e47818550444abeb83e1fafafd9bd572`
- 원본 브랜치: `android-v9.0.20-restore-practice-label-release`
- 기반 ZIP Git blob: `android-v8-source.zip` = `627c56a3a557cc2fc1be2e3d00b693b7e0aa99ab`
- V9.0.20 패치 Git blob: `android-v9.0.20-restore-practice-label-release.sh` = `d611514a0c4bf784c64a3155fa81a925621ccc33`
- 당시 릴리스 워크플로 Git blob: `.github/workflows/release-v9020-practice-label.yml` = `da122d09a68a00cdc6976a06d20d2dec144af74b`

재빌드 검증은 브랜치의 최신 상태가 아니라 위 **커밋 SHA를 직접 고정**해 사용한다.

## 빌드 환경

당시 검증된 릴리스 체인과 동일하게 사용한다.

- Ubuntu GitHub Actions runner
- Java 17 (Temurin)
- Android platform 36
- Android build-tools 36.0.0
- Gradle 8.11.1
- `android-v8-source.zip` 압축 해제 후 V9.0.20 패치 스크립트 적용
- release APK + AAB 빌드

## 서명

릴리스 서명키는 저장소에 커밋하지 않는다. GitHub Actions의 기존 보안 Secret만 사용한다.

- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_STORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

재빌드 검증은 새 APK를 배포하지 않으며, 공개된 V9.0.20 APK와 **서명 인증서 SHA-256 지문이 동일한지** 비교한다.

## 반드시 보존할 네이티브 기능

재빌드 결과에는 아래가 그대로 있어야 한다.

- `SCHEDULE_EXACT_ALARM`
- `POST_NOTIFICATIONS`
- `RECEIVE_BOOT_COMPLETED`
- `WAKE_LOCK`
- `setExactAndAllowWhileIdle` 기반 일반/습관/치료 알림
- 치료 알림 `scheduleNextForOffset`
- 재부팅 후 알림 복원
- silent sync bridge (`handleSilentSync`, clear/apply)
- Relax TTS의 partial wake lock
- MindPro Voice TTS (`TextToSpeech.QUEUE_FLUSH`)

카메라·마이크·연락처·정밀/대략 위치 권한은 추가되어서는 안 된다.

## 현재 안정 릴리스 대조값

- APK: `oneul-v9.0.20.apk`
- APK SHA-256: `711b68a3da5c5ac82f588b6756a6b8a2b214b1a7914790ee48645a4994a5f821`
- AAB: `oneul-v9.0.20.aab`
- AAB SHA-256: `b7e5d508c5161ea919ae5d1be4ca9112d694584f8c9f3844d6d95ecc3eec97b0`
- 릴리스 태그: `v9.0.20-test` (현재 안정 릴리스 자산 URL 보존을 위해 태그명은 유지)

빌드 도구가 생성하는 ZIP/APK 내부 타임스탬프 등으로 인해 새 산출물의 파일 SHA-256이 과거 산출물과 반드시 같아야 하는 것은 아니다. 재현성 판정은 **동일 고정 소스 + 동일 서명자 + 동일 패키지/버전 + 동일 핵심 권한/네이티브 엔진 + 성공적인 release APK/AAB 생성**을 기준으로 한다.

## 검증 방법

`Verify Android V9.0.20 reproducible build` GitHub Actions를 수동 실행한다. 이 작업은:

1. 고정 원본 커밋에서 기반 ZIP과 Android 패치 체인을 복원한다.
2. V9.0.20 패치를 적용한다.
3. 기존 release keystore Secret으로 APK/AAB를 빌드한다.
4. package/version/권한/네이티브 엔진을 확인한다.
5. 현재 공개 V9.0.20 APK를 내려받아 서명 인증서 지문을 대조한다.
6. 아무 릴리스·태그·앱 파일도 수정하거나 배포하지 않는다.

새 Android 버전을 만들 때는 현재 정상 V9.0.20 재현 검증이 먼저 통과한 상태에서 최소 변경으로 진행한다.
