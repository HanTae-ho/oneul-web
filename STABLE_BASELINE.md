# 오늘 한 걸음 — 최신 정상 기준본

## 현재 기준본

- 앱 버전: `V9.1.0`
- Android versionCode: `916`
- Android versionName: `9.1.0`
- 기준 main 커밋: `60babce044d1014668d3939eec2e91b2ce1e8e0f`
- 정식 GitHub Release: `v9.1.0`
- Release 상태: stable / latest
- 실기기 확인: 완료
- 웹 전체 회귀검증: 통과
- Android APK/AAB 빌드·서명검증: 통과

## 기준본 운영 원칙

이 문서에 기록된 버전을 이후 수정 작업의 최신 정상 기준본으로 사용한다.

- 수정은 최신 정상 기준본에서 최소 범위로 진행한다.
- 관련 없는 정상 기능은 임의로 변경하지 않는다.
- 변경 후 실제 diff, JavaScript 문법, 연결 기능, 회귀검증을 확인한다.
- Android 네이티브 알림/TTS 계보는 특별한 필요가 없으면 변경하지 않는다.
- 새 버전이 실기기 확인까지 완료되기 전에는 이 문서의 정상 기준본을 교체하지 않는다.

## 보호 대상

다음 항목은 명확한 데이터 구조 변경 또는 별도 승인 없이는 유지한다.

- `DATA_SCHEMA = 6`
- 개인 저장키 `ohg.v1`
- 커뮤니티 저장키 `ohg.social.v1`
- Android exact alarm / `setExactAndAllowWhileIdle`
- 화면 OFF 상태 알림
- 부팅 후 알림 재등록
- 치료 일정 `scheduleNextForOffset`
- Relax TTS
- MindPro Voice TTS

## V9.1.0 확인 사항

V9.1.0은 다음 작업을 완료한 뒤 정상 기준본으로 확정되었다.

- 의미기록을 `나 → 내 발자취 → 실천기록 → 의미`에서 통합 조회
- FAQ·사용설명서·개인정보처리방침 사용자 문구 동기화
- 정적 검사 및 Playwright 전체 브라우저 회귀검증 통과
- Service Worker 캐시 V9.1.0 계열 갱신
- Android `versionCode 916 / versionName 9.1.0`
- signed APK/AAB 생성 및 서명자 연속성 검증
- GitHub `v9.1.0` 정식 Release 배포
- 실제 Android 기기에서 정상 동작 확인
