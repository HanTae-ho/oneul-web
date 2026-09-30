# 역할별 저장 완전 분리 설계

## 목적
당사자(self)와 가족·보호자(family)가 같은 기기에서 역할을 전환해도 서로의 회복기록이 섞이지 않도록 한다.

## 기본 원칙
1. 역할을 판별할 정보가 없는 기존 공용 기록은 추측해서 나누지 않고 **당사자 기록으로 보존**한다.
2. 가족 기록은 신규 가족 저장소에만 쓴다.
3. 기존 기록에 이미 role 정보가 있는 SMART 기록은 안전하게 당사자/가족 저장소로 실제 분리한다.
4. 입력 → 저장 → 조회 → 내 발자취 → 통계/요약 → 백업/복원 → 전체삭제 → 알림 → cold-start를 같은 역할 저장소로 연결한다.
5. 당사자 전용 데이터는 가족모드에서 쓰거나 읽지 않는다.
6. 앱 표시 역할(role)은 공용 설정이지만 역할별 기록 저장소를 선택하는 스위치로만 사용한다.

## 전체 데이터 분류

### A. 이번 작업에서 물리 분리하는 양방향 기록
| 기능 | 당사자 저장 | 가족 저장 | 기존 기록 마이그레이션 |
|---|---|---|---|
| 자가점검 | screenings | familyScreenings | 기존 screenings → 당사자 유지 |
| 기분 | moods | familyMoods | 기존 moods → 당사자 유지 |
| HALT | halts | familyHalts | 기존 halts → 당사자 유지 |
| 하루마무리 | nights | familyNights | 기존 nights → 당사자 유지 |
| 습관 | habits | familyHabits | 기존 habits → 당사자 유지 |
| 식사 설정 | eats | familyEats | 기존 eats → 당사자 유지 |
| 식사 기록 | eatLog | familyEatLog | 기존 eatLog → 당사자 유지 |
| 수면 설정 | sleep | familySleep | 기존 sleep → 당사자 유지 |
| 수면 기록 | sleepLog | familySleepLog | 기존 sleepLog → 당사자 유지 |
| SMART/가족도구 | smartWorks | familySmartWorks | role=family 기록만 familySmartWorks로 이동, 나머지는 smartWorks |

### B. 이미 물리 분리되어 유지하는 양방향 기록
| 기능 | 당사자 저장 | 가족 저장 |
|---|---|---|
| 의미 돌아보기 | wbDays | familyWbDays |
| 의미점검 | meaningChecks / meaningCheckDraft | familyMeaningChecks / familyMeaningCheckDraft |
| 12단계 | stepWorks / stepDrafts | familyStepWorks / familyStepDrafts |

### C. 당사자 전용 — 가족 저장소를 만들지 않음
- 충동/충동초안: urges / urgeDraft
- 다시 시작(재발기록): relapses
- 치료관리·복약·외래: treat / meds / medCnt / medLog
- 미래의 나에게: timeCapsule
- 내가 되찾은 것: reclaim
- 금연 실천: smoking
- 위험시간대: hours (가족모드 알림에는 사용하지 않음)

### D. 역할 중립 앱 설정/캐시 — 공용 유지
- started, role, recordStart
- theme, viewMode, notify, fired
- area, sheet, res, resAt, resVer
- admin, adminUrl
- aiEnabled, aiAutoRead, aiConsent, aiClient
- 커뮤니티 데이터는 별도 키 ohg.social.v1 유지

### E. 역할 전환 의미가 있을 수 있으나 이번 회복도구 저장분리 범위 밖
- types / dates / cum / goal: 회복영역·시작일·목표 프로필
- aiChat: 마음프로 대화 기록

이 항목들은 회복도구 기록 저장소와 별개이며, 이번 ①~④ 작업에서 임의로 구조를 바꾸지 않는다. 추후 역할별 프로필·AI 대화까지 분리할 때 별도 마이그레이션 설계가 필요하다.

## 역할별 조회 원칙
- 가족모드 내 발자취의 감정/하루/몸/자가점검/실천기록은 가족 저장소만 읽는다.
- 당사자모드 내 발자취와 회복요약/회복패턴은 당사자 저장소만 읽는다.
- 충동·재발·치료 관련 통계는 항상 당사자 데이터만 읽는다.
- 가족모드 통계에는 가족 기분/HALT/하루마무리/자가점검만 사용한다.

## 알림 원칙
- Android/PWA 식사·수면·습관 알림은 현재 role의 역할별 설정을 사용한다.
- 복약·외래·위험시간대 알림은 기존 당사자 전용 규칙을 유지한다.
- 역할을 바꾸면 native reminder payload/signature가 달라져 현재 역할의 일정으로 재동기화한다.

## 백업·복원·삭제
- ohg.v1 백업에는 당사자/가족 저장소를 모두 포함한다.
- 구버전 백업 복원 시 DATA_SCHEMA 마이그레이션으로 가족 저장소를 안전 초기화한다.
- SMART만 기존 role 필드가 있으므로 정확히 분리 이동한다.
- 전체삭제는 BLANK 기반 초기화이므로 양쪽 역할 저장소를 함께 삭제한다.

## 필수 회귀검증
1. 당사자 기록 생성 → 가족 전환 시 비노출
2. 가족 기록 생성 → 당사자 전환 시 비노출
3. 각 역할에서 수정·삭제가 반대 역할 저장소를 건드리지 않음
4. 내 발자취/통계가 현재 역할만 읽음
5. 구버전 DATA_SCHEMA=6 복원 후 기존 기록은 당사자에 보존되고 가족 저장소는 비어 있음
6. 백업 → 전체삭제 → 복원 후 양쪽 역할 기록이 각각 복구됨
7. 앱 종료 → 재실행(cold-start) 후 역할별 기록 분리 유지
8. 역할 전환 뒤 식사·수면·습관 알림 payload가 현재 역할 값으로 바뀜
