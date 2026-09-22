# 오늘 한 걸음 — 최신 정식 배포 기준본

## 현재 기준본

- 앱 버전: `V9.1.3`
- Android versionCode: `919`
- Android versionName: `9.1.3`
- V9.1.3 릴리스 main 커밋: `da584d0ee38b35580cf488a64420a1d54ecf0ff9`
- 정식 GitHub Release: `v9.1.3`
- Release 상태: stable / latest
- 웹 전체 회귀검증: 통과
- Android APK/AAB 빌드·서명 연속성 검증: 통과
- V9.1.3 실기기 설치 확인: 별도 확인 필요

## 기준본 운영 원칙

이 문서에는 현재 정식 배포 기준과 검증 상태를 구분해 기록한다.

- 수정은 최신 정식 배포 기준본에서 최소 범위로 진행한다.
- 관련 없는 정상 기능은 임의로 변경하지 않는다.
- 변경 후 실제 diff, JavaScript 문법, 연결 기능, 회귀검증을 확인한다.
- Android 네이티브 알림/TTS 계보는 특별한 필요가 없으면 변경하지 않는다.
- 정식 릴리스가 완료되면 버전·커밋·Release 정보를 갱신하고, 실기기 확인 여부는 별도 상태로 기록한다.

## 보호 대상

다음 항목은 명확한 데이터 구조 변경 또는 별도 승인 없이는 유지한다.

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

## V9.1.3 확인 사항

V9.1.3은 다음 자동 검증과 배포 절차를 완료했다.

- 기록 관리 내보내기·불러오기·전체 지우기·recovery-backup/quarantine 흐름 보강
- JavaScript syntax 및 `no-undef` 검사 통과
- 정적 앱 셸·버전 일관성·전체 불변식 검사 통과
- Playwright 전체 브라우저 회귀검증 통과
- Android `versionCode 919 / versionName 9.1.3`
- signed APK/AAB 생성 및 V9.1.2와 서명자 연속성 검증
- GitHub `v9.1.3` 정식 Release 배포
- 기존 Android exact alarm·화면 OFF·부팅 재등록·치료관리 알림·Relax/MindPro TTS 엔진 보존 확인

실제 Android 기기에서 V9.1.3 설치·알림·TTS 동작을 확인하면 위의 실기기 확인 상태만 갱신한다.
