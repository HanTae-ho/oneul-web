# 오늘 한 걸음 — 최신 정상 기준본

## 실기기까지 확인된 정상 기준본

- 앱 버전: `V9.1.3`
- Android versionCode: `919`
- Android versionName: `9.1.3`
- V9.1.3 릴리스 main 커밋: `da584d0ee38b35580cf488a64420a1d54ecf0ff9`
- 정식 GitHub Release: `v9.1.3`
- 웹 전체 회귀검증: 통과
- Android APK/AAB 빌드·서명 연속성 검증: 통과
- 실제 Android 기기 설치·동작 확인: 완료

## V9.1.4 정합성 패치

V9.1.4는 위 V9.1.3 정상 기준본 위에서 전체 소스 감사 후 확인된 현재판 문서·표기·배포 메타데이터 불일치만 정리한 패치다.

- 앱 기능 로직 신규 변경 없음
- Android versionCode: `920`
- Android versionName: `9.1.4`
- `DATA_SCHEMA = 6`, `ohg.v1`, `ohg.social.v1` 유지
- 기존 Android 알림/TTS 엔진 유지
- V9.1.4 실기기 확인 전까지 V9.1.3을 실기기 검증 완료 기준본으로 본다.

## 기준본 운영 원칙

- 수정은 실기기까지 확인된 최신 정상 기준본과 최신 정식 릴리스 상태를 구분해 기록한다.
- 관련 없는 정상 기능은 임의로 변경하지 않는다.
- 변경 후 실제 diff, JavaScript 문법, 연결 기능, 회귀검증을 확인한다.
- Android 네이티브 알림/TTS 계보는 특별한 필요가 없으면 변경하지 않는다.
- 새 릴리스의 실기기 확인이 완료되면 그 버전을 실기기 검증 완료 기준본으로 승격한다.

## 보호 대상

- `DATA_SCHEMA = 6`
- 개인 저장키 `ohg.v1`
- 커뮤니티 저장키 `ohg.social.v1`
- Android package `io.github.hantae_ho.twa`
- Android exact alarm / `setExactAndAllowWhileIdle`
- 화면 OFF 상태 알림
- 부팅 후 알림 재등록
- 치료 일정 `scheduleNextForOffset`
- Relax TTS
- MindPro Voice TTS
