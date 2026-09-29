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

## V9.2.0 간단히 보기 · 사용설명서/FAQ 현행화 · Android 릴리스

V9.2.0은 V9.1.4 정합성 패치 위에서 홈 복잡도를 줄이는 간단히 보기와 자기점검→자기이해 흐름을 적용한 릴리스다.

- Web BUILD: `V9.2.0`
- Android versionCode: `921`
- Android versionName: `9.2.0`
- 신규 설치: 홈 간단히 보기 기본
- 기존 사용자·viewMode 없는 구형 백업: 전체 보기 유지
- 간단히 보기 차이: 매일의 명상 숨김 · 오늘의 문장 숨김 · 오늘 일정 최초 표시 5→3
- 사용설명서·도움말/FAQ를 V9.2.0 실제 동작에 맞게 함께 현행화
- 헬프 상단 119·109 고정, 기존 가족 위기 112 유지
- `DATA_SCHEMA = 6`, `ohg.v1`, `ohg.social.v1` 유지
- Android 네이티브 알림/TTS 엔진 변경 없음
- APK/AAB 빌드·서명 연속성·자동회귀검증 통과 후 GitHub Release `v9.2.0` 배포
- 실기기 확인 전까지는 V9.1.3을 실기기 검증 완료 기준본으로 유지하고, V9.2.0은 사용자가 설치 후 알림·TTS·화면 OFF·재부팅 동작을 확인하면 승격한다.

## V9.2.1 헬프콜 영역별 표시 · 도움화면 간소화

V9.2.1은 V9.2.0 위에서 헬프 화면의 정보량을 줄이고 선택한 회복영역에 맞는 상담전화를 우선 표시하는 패치 릴리스다.

- Web BUILD: `V9.2.1`
- Android versionCode: `922`
- Android versionName: `9.2.1`
- 119·109는 설명문 없이 상단 고정
- 기본 헬프콜: 정신건강 상담전화 1577-0199 · 보건복지상담센터 129
- 도박 영역 선택 시 1336 추가
- 약물 영역 선택 시 1342 추가
- 복수 영역 선택 시 해당 전화 중복 없이 함께 표시
- 내 주변에서 찾기의 중복 설명문 제거
- 사용설명서·도움말/FAQ를 같은 규칙으로 현행화
- 기기 안전백업 관리 화면의 버튼 연결 오류 수정 및 실제 UI 회귀검증 추가
- `DATA_SCHEMA = 6`, `ohg.v1`, `ohg.social.v1` 유지
- Android 알림·부팅복원·치료알림·Relax/MindPro TTS 엔진 변경 없음
- APK/AAB 빌드·서명 연속성·자동회귀검증 통과 후 GitHub Release `v9.2.1` 배포
- 실기기 확인 전까지 기존 실기기 검증 완료 기준본은 그대로 유지하며, V9.2.1 설치 후 알림·TTS·화면 OFF·재부팅 동작을 확인하면 승격한다.

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
