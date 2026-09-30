# 역할별 저장 완전 분리 정책

기준 버전: V9.2.4 → 차기 구조변경 버전  
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
