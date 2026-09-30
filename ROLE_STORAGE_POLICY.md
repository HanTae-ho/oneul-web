# 역할별 저장 완전 분리 정책

기준 버전: V9.2.6  
개인 저장 키: `ohg.v1` 유지  
데이터 스키마: 6 → 7

## 원칙

1. 당사자와 가족·보호자가 직접 남기는 **개인 기록은 역할별 물리 저장소로 분리**한다.
2. 기존 스키마 6에서 역할 정보가 없던 공용 기록은 임의로 가족 기록으로 추정하지 않고 **당사자 저장소에 그대로 보존**한다.
3. 기존 SMART 기록은 각 레코드에 이미 `role`이 있으므로 `role:"family"` 레코드만 가족 저장소로 안전 이동한다.
4. 당사자 전용 임상·회복 기록은 가족모드에서 읽거나 기록하지 않는다.
5. 백업·복원·전체삭제는 역할별 저장소를 포함한 `ohg.v1` 전체를 한 단위로 처리한다.
6. 내 발자취·통계·알림은 현재 역할의 저장소만 읽는다.
7. 커뮤니티 데이터 `ohg.social.v1`은 개인 회복기록과 계속 분리한다.

## 역할별 저장 매트릭스

| 영역 | 당사자 | 가족·보호자 | 정책 |
|---|---|---|---|
| 자가점검 | `screenings` | `familyScreenings` | 완전 분리 |
| 기분 | `moods` | `familyMoods` | 완전 분리 |
| HALT/현재상태 | `halts` | `familyHalts` | 완전 분리 |
| 하루마무리 | `nights` | `familyNights` | 완전 분리 |
| 습관 정의·체크 | `habits` | `familyHabits` | 완전 분리 |
| 식사 일정 | `eats` | `familyEats` | 완전 분리 |
| 식사 체크 | `eatLog` | `familyEatLog` | 완전 분리 |
| 수면 설정 | `sleep` | `familySleep` | 완전 분리 |
| 수면 체크 | `sleepLog` | `familySleepLog` | 완전 분리 |
| SMART/가족 작성도구 | `smartWorks` | `familySmartWorks` | 완전 분리 |
| 웹 알림 발송 이력 | `fired` | `familyFired` | 생활알림 역할 간 상호 억제 방지 |
| 의미 돌아보기 | `wbDays` | `familyWbDays` | 기존 완전 분리 유지 |
| 의미점검 | `meaningChecks` | `familyMeaningChecks` | 기존 완전 분리 유지 |
| 의미점검 초안 | `meaningCheckDraft` | `familyMeaningCheckDraft` | 기존 완전 분리 유지 |
| 12단계 점검 | `stepWorks/stepDrafts` | `familyStepWorks/familyStepDrafts` | 기존 완전 분리 유지 |
| 충동/충동일기 | `urges/urgeDraft` | 없음 | 당사자 전용 |
| 다시 시작/재발 | `relapses` | 없음 | 당사자 전용 |
| 치료관리·복약·외래 | `treat/meds/medLog` | 없음 | 당사자 전용 |
| 위험시간 | `hours` | 없음 | 당사자 전용 |
| 미래의 나에게 | `timeCapsule` | 없음 | 당사자 전용 |
| 협심자·후원자 연락처 | `supportContacts` | 없음 | 당사자 전용 · 최대 3명 · 직접 입력 |
| 내가 되찾은 것 | `reclaim` | 없음 | 당사자 전용 |

## 의도적으로 공용인 앱 설정

다음 항목은 기록 자체가 아니라 앱 전역 환경·콘텐츠 맥락이므로 이번 역할별 기록 분리 대상에서 제외한다.

- 현재 선택 역할: `role`
- 회복영역·시작일·누적일: `types/dates/cum`
- 목표·지역: `goal/area`
- 테마·홈 보기 방식: `theme/viewMode`
- 자원시트 캐시: `res/resAt/resVer/sheet`
- AI 사용·읽기 설정: `aiEnabled/aiAutoRead` 등
- 알림 허용 의사: `notify`
- 앱 관리 설정

생활 알림의 실제 일정 데이터(습관·식사·수면)는 역할별 저장소를 사용한다. 당사자 치료 알림은 계속 당사자 전용이다.

## 전체 `ohg.v1` 필드 결정표

아래 표는 현재 개인상태 객체의 모든 주요 필드를 역할 관점에서 빠짐없이 분류한 최종 설계 기준이다.

| 필드 | 분류 | 결정 |
|---|---|---|
| `ver / dataSchema / started` | 앱 메타데이터 | 공용 |
| `role` | 현재 화면 역할 | 공용 |
| `types` | 회복영역/가족이 지원하는 영역 | 공용 콘텐츠 맥락 |
| `dates / cum / recoveryHome` | 회복일 계산 | 당사자 전용 표시·계산 |
| `recordStart` | 앱 기록 시작 기준 | 공용 메타데이터 |
| `goal` | 사용자가 적는 앱 전역 안내문구 | 현재는 공용 설정으로 유지. 통계/역할기록 집계에는 사용하지 않음 |
| `smoking` | 금연 실천 | 당사자 전용 |
| `hours` | 위험시간 | 당사자 전용 |
| `treat / meds / medCnt / medLog` | 치료·복약·외래 | 당사자 전용 |
| `eats / eatLog` | 식사 설정·체크 | 당사자 저장소 |
| `familyEats / familyEatLog` | 식사 설정·체크 | 가족 저장소 |
| `sleep / sleepLog` | 수면 설정·체크 | 당사자 저장소 |
| `familySleep / familySleepLog` | 수면 설정·체크 | 가족 저장소 |
| `habits` | 습관 정의·체크 | 당사자 저장소 |
| `familyHabits` | 습관 정의·체크 | 가족 저장소 |
| `moods / halts / nights` | 기분·HALT·하루마무리 | 당사자 저장소 |
| `familyMoods / familyHalts / familyNights` | 기분·HALT·하루마무리 | 가족 저장소 |
| `screenings` | 자가점검 결과 | 당사자 저장소 |
| `familyScreenings` | 자가점검 결과 | 가족 저장소 |
| `urges / urgeDraft` | 충동·충동일기 | 당사자 전용 |
| `relapses` | 다시 시작/재발 | 당사자 전용 |
| `stepWorks / stepDrafts` | 12단계 점검 | 당사자 저장소 |
| `familyStepWorks / familyStepDrafts` | 12단계 점검 | 가족 저장소 |
| `wbDays / meaningChecks / meaningCheckDraft` | 의미 돌아보기·의미점검 | 당사자 저장소 |
| `familyWbDays / familyMeaningChecks / familyMeaningCheckDraft` | 의미 돌아보기·의미점검 | 가족 저장소 |
| `smartWorks` | SMART 작성도구 | 당사자 저장소 |
| `familySmartWorks` | SMART·가족 작성도구 | 가족 저장소 |
| `timeCapsule` | 미래의 나에게 | 당사자 전용 |
| `supportContacts` | 협심자·후원자 이름·전화번호 | 당사자 전용 · 최대 3명 · 연락처 권한 없이 직접 입력 |
| `reclaim` | 내가 되찾은 것 | 당사자 전용 |
| `aiChat` | 마음프로 대화기록 | 앱 전역 대화 이력으로 유지. 이번 회복도구 역할분리의 통계·내 발자취에는 포함하지 않음 |
| `aiClient / aiConsent / aiEnabled / aiAutoRead` | AI 연결·사용 설정 | 공용 설정 |
| `area` | 지역 | 공용 설정 |
| `sheet / res / resAt / resVer` | 자원시트·캐시 | 공용 콘텐츠 캐시 |
| `theme / viewMode` | 화면 설정 | 공용 설정 |
| `notify` | 알림 사용 의사 | 공용 OS/앱 설정 |
| `fired` | 웹 생활알림 발송 이력 | 당사자 저장소 |
| `familyFired` | 웹 생활알림 발송 이력 | 가족 저장소 |
| `admin / adminUrl` | 관리 기능 설정 | 공용 설정 |

### 설계상 공용과 기록 분리의 경계

- **공용 설정**은 역할별 통계·내 발자취에 합산되는 개인기록이 아니다.
- **역할별 기록**은 입력·조회·통계·알림·백업복원에서 상대 역할의 저장소를 읽지 않는다.
- **당사자 전용** 데이터는 가족모드 UI에서 기록·조회하지 않는다.
- `supportContacts`는 이름·전화번호만 최대 3명까지 저장하고, 연락처 권한·자동 문자·자동 통화·AI/커뮤니티 자동전송을 사용하지 않는다.
- `aiChat`은 별도 AI 대화 도메인으로 유지하며, 이번 역할별 회복기록 통계에는 연결하지 않는다. 향후 AI 대화 자체를 역할별 대화방으로 분리하는 경우에는 별도 데이터 구조 변경으로 다룬다.

## 마이그레이션 6 → 7

- `screenings/moods/halts/nights/habits/eats/eatLog/sleep/sleepLog`: 기존 값을 당사자 저장소에 그대로 둔다.
- 새 가족 저장소는 빈 값으로 초기화한다.
- `smartWorks`: `role:"family"` 레코드는 `familySmartWorks`로 이동하고, 나머지는 `smartWorks`에 유지한다.
- 의미·12단계의 기존 역할별 저장소는 그대로 보존한다.
- 데이터 삭제나 역할 추정은 하지 않는다.

## 검증 기준

각 분리 대상은 다음 순서로 검증한다.

1. 당사자 기록 저장
2. 가족모드 전환 후 당사자 기록 비노출 확인
3. 가족 기록 저장
4. 당사자모드 복귀 후 가족 기록 비노출 확인
5. 내 발자취·통계가 현재 역할 자료만 읽는지 확인
6. 백업 JSON에 두 역할 저장소가 모두 포함되는지 확인
7. 백업 복원 후 두 역할 자료가 원위치에 복원되는지 확인
8. 전체삭제 후 두 역할 저장소가 모두 비는지 확인
9. 앱 종료→재실행(cold-start) 후 역할별 자료가 섞이지 않는지 확인
10. Android 생활 알림 payload가 현재 역할의 습관·식사·수면만 사용하는지 확인
11. 웹 알림의 발송 이력도 역할별로 분리되어 한 역할의 알림이 다른 역할의 알림을 억제하지 않는지 확인
