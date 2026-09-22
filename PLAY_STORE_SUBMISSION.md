# 오늘 한 걸음 V9.1.3 — Google Play 제출 준비서

기준일: 2026-09-22  
대상: `오늘 한 걸음` Android 앱을 Google Play에 최초 등록하기 위한 사전 점검 및 Play Console 입력 준비

> 이 문서는 Play Console 제출을 돕기 위한 운영 체크리스트입니다. Google Play 정책과 Play Console 질문은 변경될 수 있으므로 실제 제출 화면의 최신 문구를 최종 기준으로 사용합니다.

---

## 0. 가장 먼저 확인할 사항 — 개인 계정이 아니라 조직 계정 경로

`오늘 한 걸음`은 중독 회복·정신건강 지원, 복약/치료 일정, 이완·스트레스 관리 등 **건강 관련 기능을 제공하는 앱**입니다.

Google Play의 현재 계정유형 정책은 건강 앱을 제공하는 개발자는 **Organization(조직) 개발자 계정**을 선택해야 한다고 안내합니다. 따라서 이 앱을 Google Play에 정식 배포할 목적이라면 **신규 Personal(개인) 계정을 기준으로 출시 준비를 진행하지 않습니다.**

### 조직 계정에서 준비할 것

- 조직/사업체의 공식 정보
- **D-U-N-S 번호**
- 공식 조직 웹사이트 및 웹사이트 확인 절차
- 조직 전화번호
- Google 연락용 이메일/전화번호
- Google Play에 공개되는 개발자 이메일/전화번호
- Google Payments 조직 프로필 및 필요한 신원/조직 확인

Google의 계정유형 안내에 따르면 조직 계정 생성에는 D-U-N-S 번호가 필요합니다.

공식 계정유형 정책: <https://support.google.com/googleplay/android-developer/answer/13634885>  
Play Console 요구사항: <https://support.google.com/googleplay/android-developer/answer/10788890>

### 이미 개인 개발자 계정을 만든 경우

2026년 현재 Google은 Personal → Organization 전환 절차를 제공합니다.

대략적인 순서:

1. Play Console `Developer account → About you`로 이동
2. 공식 조직 웹사이트를 제공하고 확인
3. `Change account type` 선택
4. D-U-N-S 번호가 포함된 조직용 Google Payments 프로필 생성/선택
5. 조직 정보·연락처 제공 및 확인
6. 필요한 신원/조직 확인 완료
7. 검증된 Payments 프로필을 개발자 계정에 연결
8. 전환 완료 후 Google 시스템 동기화를 위해 공식 안내에 따라 최소 72시간을 두고 새 앱 제출

공식 전환 안내: <https://support.google.com/googleplay/android-developer/answer/16260648>

> **중요:** 신규 개인계정에 적용되는 `12명·14일 closed test` 규칙은 Personal 계정용 요건입니다. 오늘 한 걸음의 권장/정책상 경로는 건강 앱에 맞는 Organization 계정이므로, 이를 출시 계획의 기본 일정으로 잡지 않습니다. 이미 개인계정에서 작업을 시작했다면 먼저 계정유형을 바로잡은 뒤 Play Console이 실제로 제시하는 테스트 요구사항을 확인합니다.

---

## 1. 현재 제출 기준본

- 앱 버전: `V9.1.3`
- Android package/applicationId: `io.github.hantae_ho.twa`
- Android versionCode: `919`
- Android versionName: `9.1.3`
- minSdk: `23`
- compileSdk: `36`
- targetSdk: `36`
- 정식 GitHub Release: `v9.1.3`
- AAB: `oneul-v9.1.3.aab`
  - SHA-256: `56c70732367691fa1303835d727d0af8d3fc6ee0b40561a90fc5b60f44db8a4e`
- APK: `oneul-v9.1.3.apk`
  - SHA-256: `f392bcba806ec3166fb446c20ce8cbbce8b44635422f9728c2707e2ee2607655`
- V9.1.3 실제 Android 기기 설치 확인: 별도 확인 필요
- Android 네이티브 알림·부팅복원·치료알림·TTS 계보: 기존 정상 계보 유지

### Target API 판정

2026-08-31부터 Google Play의 새 Android 모바일 앱과 앱 업데이트는 Android 16 / API 36 이상을 target 해야 합니다. 현재 V9.1.3은 `targetSdk 36`이므로 이 요건을 충족합니다.

공식 정책: <https://support.google.com/googleplay/android-developer/answer/11926878>

---

## 2. Play App Signing — 기존 서명 연속성 유지가 중요

현재 GitHub에서 직접 배포한 APK에는 기존 앱 서명키가 사용되고 있으며 V9.1.3도 이전 정상판과 서명 연속성을 검증했습니다.

Google Play 신규 앱은 기본적으로 Play App Signing에 등록됩니다. 그러나 `오늘 한 걸음`은 이미 동일 package의 APK를 외부에서 배포했으므로, **Google이 새롭고 다른 앱 서명키를 자동 생성한 상태로 그대로 공개하지 않는 것이 안전합니다.** 기존 직접설치 사용자가 Play 배포판으로 업데이트하려면 최종 설치 APK의 서명 계보가 맞아야 하기 때문입니다.

### 권장 절차

1. 올바른 Organization 개발자 계정에서 앱을 만든다.
2. AAB를 공개 트랙에 배포하기 전에 `Play App Signing` 설정으로 이동한다.
3. **현재 사용 중인 기존 app signing key의 사본을 Google Play에 제공하는 방식**을 선택한다.
4. 기존 키를 Play App Signing에 안전하게 이전한다(Play Console 안내/PEPK 절차 준수).
5. 이후 업로드 전용 키(upload key)는 별도로 생성·등록하는 방식을 권장한다.
6. Play Console에 표시되는 App signing key 인증서 SHA-256을 보관한다.
7. Play에서 생성된 설치본을 받은 뒤 기존 직접설치판과 업데이트 연속성을 실제 기기에서 확인한다.

> 기존 keystore 원본, 비밀번호, alias 비밀번호는 문서·GitHub·Play 스토어 설명에 기록하지 않는다.

공식 안내: <https://support.google.com/googleplay/android-developer/answer/9842756>

---

## 3. 개인정보처리방침 및 계정 삭제 URL

### 개인정보처리방침

Play Console 입력 URL:

`https://hantae-ho.github.io/oneul-web/privacy.html`

현재 방침은 다음 구조를 설명합니다.

- 일반 회복기록은 Local-first이며 기본적으로 사용자 기기에 저장
- 광고·행동추적용 분석 SDK 없음
- 마음프로 AI 사용 시 필요한 입력과 제한된 최근 대화만 외부 처리
- 선택형 익명 커뮤니티 데이터는 커뮤니티 전용 서버에서 처리
- Google Apps Script/Sheets, OpenAI API, GitHub Pages, Wikimedia Commons 등 외부 서비스 이용
- Android 권한 및 삭제·보관 원칙

### 커뮤니티 계정·데이터 삭제

Play Console의 외부 계정 삭제 요청 URL로 사용할 페이지:

`https://hantae-ho.github.io/oneul-web/account-deletion.html`

앱 내부에는 이미 다음 삭제 경로가 있습니다.

`커뮤니티 → 내 닉네임 → 내 커뮤니티 프로필 → ⋮ → 커뮤니티 탈퇴`

외부 페이지에서는 앱을 이미 삭제했거나 사용할 수 없는 사람도 `admin@maumpro.com`으로 삭제를 요청할 수 있도록 합니다.

현재 서버 삭제 로직은 익명 사용자 ID·인증 연결, 게시글·댓글 연결정보/내용, 응원 관계를 삭제 처리합니다. 신고 기록은 안전·운영 확인을 위해 최대 1년 보관될 수 있으나, 탈퇴자와 연결되는 익명 사용자 ID는 제거합니다. 탈퇴 닉네임은 30일 재사용 제한 판정을 위해 제한적으로 남을 수 있습니다.

공식 계정 삭제 정책: <https://support.google.com/googleplay/android-developer/answer/13327111>

---

## 4. Health apps declaration 권장 분류

`오늘 한 걸음`은 중독 회복·정신건강 지원, 복약/치료 일정, 이완·스트레스 관리 기능을 포함하므로 Health apps declaration에서 `건강 기능 없음`으로 신고하면 안 됩니다.

현재 기능을 기준으로 우선 검토할 분류:

- **Mental and Behavioral Health** — 정신건강 지원 및 addiction recovery 프로그램에 직접 해당
- **Medication and Treatment Management** — 복약·치료 일정 관리 기능에 해당
- **Stress Management, Relaxation, Mental Acuity** — 이완 및 회복 지원 기능에 해당
- **Sleep Management** — 수면 기록/관리 기능을 건강 기능으로 제공한다고 Play Console이 묻는 경우 선택 검토

`Healthcare Services and Management`는 의료기관 예약·원격진료·의료기록 관리 등 의료서비스 운영 기능을 직접 제공하는지에 따라 판단하며, 단순 개인 알림 기능만으로 자동 선택하지 않습니다.

공식 Health apps declaration 안내: <https://support.google.com/googleplay/android-developer/answer/14738291>

---

## 5. 건강·의료 관련 스토어 설명 필수 문구

Google Play Health Content and Services 정책상 의료기기로 규제되는 앱이 아닌 건강/의료 관련 앱은 스토어 설명에 명확한 비의료기기 고지와 의료전문가 상담 안내가 필요합니다.

### 스토어 설명에 넣을 권장 문구

> 오늘 한 걸음은 중독 회복과 자기관리를 돕기 위한 회복지원 도구이며 의료기기가 아닙니다. 이 앱은 어떠한 질환도 진단·치료·치유·예방하지 않습니다. 의료적 조언, 진단 또는 치료가 필요한 경우 의사 등 자격을 갖춘 의료전문가와 상담하세요. 생명이나 신체에 즉각적인 위험이 있는 경우 앱에 머물지 말고 112·119 또는 가까운 응급의료기관 등 즉시 이용 가능한 도움을 이용하세요.

앱 내부에는 이미 마음프로가 치료자·응급서비스를 대신하지 않는다는 안전 안내와 112/119 등 긴급 도움 연결이 있습니다. Play 제출 직전에는 위의 의료전문가 상담 문구가 스토어 설명에 실제 반영되었는지 확인합니다.

공식 정책: <https://support.google.com/googleplay/android-developer/answer/16679511>

---

## 6. Data Safety 입력 초안

### 원칙

Google Play Data Safety는 **기기에만 남는 정보**와 **기기 밖으로 전송되는 정보**를 구분해서 작성합니다. 아래 표는 현재 구현을 바탕으로 한 제출 초안이며, 실제 Play Console의 최신 질문과 데이터 유형 명칭을 보면서 최종 확정합니다.

| 데이터/기능 | 현재 처리 | Data Safety 판단 초안 |
|---|---|---|
| 회복 시작일, 감정/HALT, 충동·재발, 복약·외래·수면·습관, 자가점검, 12단계·회복 실천 기록 | 기본적으로 기기 로컬 저장, 자동 서버 백업 없음 | 로컬 전용 상태라면 서버 수집으로 신고하지 않음 |
| 마음프로 `clientId` | AI 요청 시 외부 전송 | User ID/식별자 성격으로 검토·신고 |
| 마음프로에 사용자가 직접 입력한 메시지 | AI 요청 시 전송 | 메시지/사용자 생성 콘텐츠로 검토·신고. 건강·중독 정보가 포함될 수 있음 |
| 최근 AI 대화 최대 8개 | AI 문맥 제공을 위해 전송 | 메시지/사용자 생성 콘텐츠로 검토·신고 |
| 현재 날짜·시간·시간대, 앱 버전, 주제 | AI 요청 처리에 사용 | Play Console의 해당 진단/앱 활동 유형 질문에 맞춰 최종 확인 |
| 커뮤니티 익명 내부 사용자 ID 및 인증정보 | 커뮤니티 서버 처리 | User ID/식별자 성격으로 신고 검토 |
| 커뮤니티 닉네임·게시글·댓글·응원·신고 | 사용자가 커뮤니티 사용 시 서버 처리 | 사용자 생성 콘텐츠/앱 활동 등 Play Console의 실제 유형에 맞춰 신고 |
| 앱에 바라는 점 | 사용자가 선택해 전송 | 사용자 생성 콘텐츠. 이용자가 건강/개인정보를 직접 적을 가능성도 고려 |
| 위치 | 사용자가 현재 위치 확인을 선택할 때 지역 결정을 위해 일시 사용; 현 방침상 원래 GPS 좌표는 저장/AI 전송하지 않음 | 위치가 서버로 전송되지 않는 현재 구현이 최종 확인되면 수집 데이터로 신고하지 않음 |

### 공통 보안/목적 답변 초안

- 광고 목적 수집: **아니오**
- 데이터 판매: **아니오**
- 광고/행동분석 SDK: **사용하지 않음**
- 전송 중 암호화: 외부 통신은 HTTPS 경로 사용
- 수집 목적: 앱 기능 제공, 커뮤니티 운영·안전, AI 답변, 이용자 의견 접수
- 수집 선택성: AI·커뮤니티·의견 기능은 사용자가 해당 기능을 선택하여 사용
- 계정 삭제 지원: **예**로 처리하는 것이 안전함(선택형 익명 커뮤니티 프로필이 서버 인증정보와 연결되므로)
- 계정 삭제 URL: `https://hantae-ho.github.io/oneul-web/account-deletion.html`

> **주의:** 사용자가 자유입력란에 건강·중독·복약 내용을 직접 입력해 서버로 전송할 수 있으므로, Play Console이 `Health info` 수집 여부를 묻는 경우 단순히 “회복기록은 로컬”이라는 이유만으로 `아니오`를 선택하지 않습니다. 마음프로·커뮤니티·의견 입력을 포함한 실제 전송 가능성을 기준으로 보수적으로 판단합니다.

공식 Data Safety 안내: <https://support.google.com/googleplay/android-developer/answer/10787469>

---

## 7. 개발자 계정·본인/조직 확인

### 권장 계정

- 계정 유형: **Organization**
- 이유: 건강 앱 제공
- 필수 핵심: **D-U-N-S 번호**
- 조직 웹사이트 확인 필요
- 조직/연락처 정보 검증 필요

조직 계정에서는 조직의 법적 이름·주소, 개발자 이메일과 전화번호 등 일부 정보가 Google Play에 공개될 수 있으므로 스토어에 공개해도 되는 전용 연락처를 준비하는 것이 좋습니다.

공식 계정 정보 요구사항: <https://support.google.com/googleplay/android-developer/answer/13628312>

### 12명·14일 테스트 규칙에 대한 정리

Google의 `12명·14일 closed test` 요건은 **2023-11-13 이후 생성된 새 Personal 개발자 계정**에 적용됩니다.

공식 안내: <https://support.google.com/googleplay/android-developer/answer/14151465>

그러나 오늘 한 걸음은 건강 앱이므로 Organization 계정을 사용해야 하는 것이 현재 공식 정책상의 기본 경로입니다. 따라서 **12명·14일 요건을 피하기 위해 조직 계정을 선택하는 것이 아니라, 앱 성격 때문에 올바른 계정유형을 Organization으로 선택하는 것**입니다. Play Console이 조직 계정에도 별도의 테스트나 검토를 요구하면 실제 Console 표시를 따릅니다.

---

## 8. 스토어 등록 정보 준비

Play Console에서 별도로 준비/입력해야 할 항목:

- 앱 이름: `오늘 한 걸음`
- 짧은 설명
- 전체 설명
  - 위 Health 정책용 비의료기기·의료전문가 상담 문구 포함
- 앱 아이콘 512×512
- 휴대전화 스크린샷
- Feature graphic 등 Play Console이 요구하는 그래픽 자산
- 앱 카테고리
- 연락처 이메일/웹사이트
- 개인정보처리방침 URL
- Data Safety
- Health apps declaration
- Content rating 설문
- Target audience and content
- Ads declaration: 현재 광고 없음
- App access: 로그인은 없으나 선택형 익명 커뮤니티가 있음을 필요한 경우 설명

### 대상연령

현재 앱의 중독 회복·복약·위기대응·정신건강 내용 특성을 고려하면, **실제 서비스 대상이 성인이라면 Play Console에서도 성인 대상(18+)으로 일관되게 설정**하는 편이 정책·콘텐츠 설계상 단순합니다. 실제로 미성년자를 대상으로 제공하려는 경우에는 가족/아동 정책과 건강 콘텐츠 적합성을 별도로 재검토해야 합니다.

---

## 9. Play 테스트 설치본에서 반드시 다시 확인할 기능

GitHub 직접배포 APK의 자동 검증과 별개로, Google Play에 올린 AAB에서 생성된 설치본을 실제 기기에 설치하여 아래를 다시 확인합니다.

- 기존 직접설치 V9.1.3에서 Play 설치본으로 업데이트 가능 여부(서명 연속성)
- 앱 실행 및 기존 `ohg.v1` 데이터 유지
- `DATA_SCHEMA = 6` 유지
- 화면 OFF 상태 예약 알림
- exact alarm
- 부팅 후 알림 재등록
- 일정·습관·복약/치료 알림
- 치료 일정 `scheduleNextForOffset`
- 알림 소리/진동/팝업
- Relax TTS
- MindPro Voice TTS
- 마음프로 AI
- 커뮤니티 가입·작성·신고·차단·탈퇴
- 계정 삭제 외부 URL 접근
- 개인정보처리방침 접근
- 오프라인 기본 기능 및 서비스워커

---

## 10. 현재 판정

### 이미 완료/충족

- V9.1.3 정식 배포 기준본 확정
- signed APK/AAB 생성
- GitHub Actions 웹 전체 회귀검증 통과
- package/version 정합성
- `targetSdk 36`
- 개인정보처리방침 공개 페이지
- 앱 내부 커뮤니티 탈퇴 기능
- Google Play용 외부 커뮤니티 계정·데이터 삭제 요청 페이지 준비
- 네이티브 알림/TTS 정상 계보 유지

### 별도 확인 필요

- V9.1.3 실기기 설치·알림·TTS 동작 확인

### 현재 가장 먼저 해결할 외부 준비사항

1. **개인 계정이 아닌 Organization 계정으로 출시 경로 확정**
2. 조직의 **D-U-N-S 번호** 준비
3. 조직 공식 웹사이트 및 공개 연락처 준비/확인
4. 이미 Personal Play 계정을 만들었다면 Organization 전환 완료
5. 올바른 조직 계정에서 앱 생성 및 package `io.github.hantae_ho.twa` 확정
6. **기존 app signing key를 Play App Signing에 제공하여 서명 계보 유지**
7. V9.1.3 AAB 업로드
8. Privacy / Data Safety / Health apps declaration 입력
9. 스토어 설명에 건강·의료 고지 반영
10. Content rating / Target audience / Ads / App access 작성
11. 스크린샷·Feature graphic 등 스토어 자산 준비
12. Play가 해당 계정에 요구하는 테스트 트랙 진행
13. Play 설치본 실기기 회귀검증
14. 조건 충족 후 정식 출시

---

## 11. 이번 준비 작업에서 변경하지 않는 항목

- 앱 버전 `V9.1.3`
- Android versionCode `919`
- `DATA_SCHEMA = 6`
- `ohg.v1`
- `ohg.social.v1`
- 기존 회복기록 구조
- Android exact alarm / 화면 OFF 알림 / 부팅복원
- `scheduleNextForOffset`
- Relax TTS
- MindPro Voice TTS
- 현재 GitHub Release APK/AAB 및 tag
