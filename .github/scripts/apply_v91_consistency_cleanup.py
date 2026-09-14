from pathlib import Path

# 1) index.html 조사 오류: 사용자 문구 + 인접 주석 모두 정리
p=Path('index.html')
s=p.read_text(encoding='utf-8')
count=s.count('커뮤니티은')
if count < 1:
    raise SystemExit('index: 커뮤니티은 not found')
s=s.replace('커뮤니티은','커뮤니티는')
p.write_text(s,encoding='utf-8')
print('index replacements',count)

# 2) privacy.html 공개 문서의 사용자 명칭 통일
p=Path('privacy.html')
s=p.read_text(encoding='utf-8')
count=s.count('소셜')
if count < 1:
    raise SystemExit('privacy: 소셜 not found')
s=s.replace('소셜','커뮤니티')
p.write_text(s,encoding='utf-8')
print('privacy replacements',count)

# 3) README V9.0.7~V9.0.20 변경이력 복원
p=Path('README.md')
s=p.read_text(encoding='utf-8')
if '## V9.0.20' in s:
    raise SystemExit('README already contains V9.0.20')
anchor='## V9.0.6 — 초심 보기 런타임 수정 · 소셜 반응속도 개선'
if anchor not in s:
    raise SystemExit('README V9.0.6 anchor not found')
entries='''## V9.0.20 — 회복 실천도구 명칭 복원 · 안정판 검증
- V9.0.19에서 잠시 바뀌었던 `필요한 도구` 명칭을 사용자에게 익숙한 `회복 실천도구`로 복원했습니다.
- 웹 정적검사와 Playwright 전체 회귀검증을 통과한 Android `versionCode 915 / versionName 9.0.20`을 검증 설치 버전으로 승격했습니다.
- 엘가 `위풍당당 행진곡 1번`에 미 연방정부 공개도메인 백업 음원 2개를 추가해 재생 후보를 3개로 보강했습니다.
- `DATA_SCHEMA=6`, `ohg.v1`, `ohg.social.v1`, Android 알림/TTS 엔진은 유지합니다.

## V9.0.19 — 실천하기 카드 압축 · 메뉴 문구 정리
- `배우기`와 `실천하기`의 3열 카드 높이와 간격을 줄여 한 화면에서 더 빠르게 훑을 수 있게 했습니다.
- 실천도구 카드의 사용자 문구를 짧게 정리했으며, 기능 경로와 저장 데이터는 바꾸지 않았습니다.
- 이후 사용자 명칭 일관성을 위해 V9.0.20에서 `회복 실천도구` 명칭을 다시 복원했습니다.

## V9.0.18 — 회복도구 배우기·실천하기 3열 그리드
- `배우기`와 `실천하기`를 아이콘·제목 중심의 3열 카드로 정리해 회복도구 화면의 복잡도를 낮췄습니다.
- `회복학습`, `중독 Q&A`, `듣는 글`과 의미·12단계·실천도구·충동·미래의 나 기능을 기존 경로 그대로 유지했습니다.
- 자가점검 영역은 별도 구조를 유지해 기능 성격을 구분했습니다.

## V9.0.17 — 의미회복 간편점검 UX 보완
- 의미점검을 `점검하기 / 점검 기록`으로 분리하고 작성 중 답변 임시저장과 완료결과 저장 상태를 명확히 했습니다.
- 같은 날 재점검 시 기존 완료결과를 새 결과 저장 전까지 보존하고, 저장 시 그날 결과 하나만 교체하도록 정리했습니다.
- 지난 결과에서 총점·4개 영역·이전 나와의 변화를 다시 확인할 수 있게 했습니다.

## V9.0.16 — 의미회복 간편점검 추가
- MIL-II의 구성개념을 참고하되 원문항·원채점체계를 복제하지 않은 앱 자체 10문항 `의미회복 간편점검`을 추가했습니다.
- 0~4 응답, 총점 40점과 `나를 보는 힘 / 앞으로 향하는 힘 / 책임·선택 / 관계·넘어섬` 4개 묶음으로 자기 변화를 확인합니다.
- 정상·위험·중증 절단점 없이 자신의 이전 결과와만 비교하며 `meaningCheckDraft / meaningChecks`를 기존 `ohg.v1` 안에서 사용합니다.

## V9.0.15 — 지난 의미기록과 충동기록 연결
- 지난 의미 돌아보기 기록에서도 같은 날짜의 충동기록을 동적으로 찾아 함께 확인할 수 있게 했습니다.
- 충동 원문을 의미기록에 복사하지 않고 기존 `S.urges`를 읽어 연결해 중복저장을 피했습니다.
- 기록 보기에서 기존 충동일기 상세 경로로 이동하도록 연결했습니다.

## V9.0.14 — 의미 지난 기록 모바일 정리
- 지난 의미기록 카드에서 날짜를 상단 전체폭으로 배치하고 본문과 `오늘의 문장`을 분리해 모바일 가독성을 높였습니다.
- 연도를 포함한 날짜 표시와 기록별 전체폭 구성을 적용했습니다.
- 기존 의미기록 데이터 구조와 같은 날짜 upsert 규칙은 유지했습니다.

## V9.0.13 — 의미 돌아보기와 오늘 충동 연결
- 의미 돌아보기에서 같은 날 기록된 충동 건수를 로컬 날짜 기준으로 동적으로 표시하고 충동일기로 바로 이동할 수 있게 했습니다.
- 오늘 기존 의미기록이 있을 때 `오늘 기록 보기 / 기존 기록 수정하기 / 처음부터 다시 작성` 흐름을 추가했습니다.
- 처음부터 다시 작성해도 새 기록을 실제 저장하기 전에는 기존 기록을 삭제하지 않도록 보호했습니다.

## V9.0.12 — 커뮤니티 명칭 정리 · 의미 UI 보완
- 사용자 화면의 다섯 번째 하단 메뉴와 관련 안내를 `커뮤니티` 중심 표현으로 정리하면서 내부 `social` 경로와 `ohg.social.v1` 저장키는 유지했습니다.
- 의미 돌아보기의 진입·기록 화면을 기존 회복도구 구조에 맞게 다듬었습니다.
- 개인 회복기록과 커뮤니티 서버 데이터의 분리 원칙은 그대로 유지했습니다.

## V9.0.11 — 의미 돌아보기 정제
- `오늘 아팠던 것`, `남아 있던 힘`, `선택·지킨 것`, `오늘의 문장`을 중심으로 의미 돌아보기 문항과 표현을 정제했습니다.
- 선택형 힘·행동을 기반으로 `기록에서 보인 힘 / 기록에서 지킨 가치`를 요약하고 자유입력은 임의 분류하지 않도록 했습니다.
- 가족모드 직접 진입 차단과 로컬 저장 원칙을 유지했습니다.

## V9.0.10 — 회복패턴·회복요약 안내 자동 접기
- `내 회복 패턴`과 `최근 4주 내 회복요약`의 일반 안내를 세션 최초에만 잠깐 보여준 뒤 자동으로 접도록 정리했습니다.
- 응급·긴급 경고는 자동 접기 대상에서 제외해 안전 안내가 가려지지 않도록 했습니다.
- 분석 결과의 진단·재발예측 과잉해석 방지 문구는 유지했습니다.

## V9.0.9 — 일반 안내 자동 접기
- 중독 Q&A, 자가점검, 내 정보, 가족 화면의 일반 안내를 처음에는 보여주고 잠시 뒤 자동으로 접는 공통 동작을 추가했습니다.
- 사용자가 다시 펼치거나 접을 수 있으며 세션 안에서는 불필요한 반복 노출을 줄였습니다.
- 안전·응급 안내는 별도 유지했습니다.

## V9.0.8 — 커뮤니티 화면 가독성 정리
- 커뮤니티 피드·댓글·프로필의 시각적 구분과 안내 문구를 다듬어 게시물과 댓글 맥락을 쉽게 구분하도록 했습니다.
- 기존 익명 인증·차단·신고·닉네임 보호 규칙과 서버 계약은 변경하지 않았습니다.
- 개인 회복기록이 커뮤니티에 자동 전송되지 않는 원칙을 유지했습니다.

## V9.0.7 — 버전 일관성 · 커뮤니티 서버 계약 정리
- `Vx.y`와 `Vx.y.z`를 모두 안전하게 비교하도록 업데이트 버전 파서를 보강하고 웹·서비스워커·설치 안내의 버전 일관성 검사를 강화했습니다.
- 커뮤니티 앱/서버의 오류 계약과 운영 기준본을 정리하고 `SOCIAL_VERSION = V9.0.7-social-1` 계열을 기준으로 유지했습니다.
- `DATA_SCHEMA=6`, `ohg.v1`, `ohg.social.v1` 및 Android 네이티브 알림/TTS 엔진은 변경하지 않았습니다.

'''
s=s.replace(anchor,entries+anchor,1)
p.write_text(s,encoding='utf-8')
print('README changelog inserted V9.0.7~V9.0.20')

# 4) 정적 불변식: 화면 조사와 공개 개인정보처리방침 용어 일관성
p=Path('verify.js')
s=p.read_text(encoding='utf-8')
old="const index=read('index.html'), sw=read('sw.js'), test=read('test.js'), manifest=read('manifest.json');"
new="const index=read('index.html'), privacy=read('privacy.html'), sw=read('sw.js'), test=read('test.js'), manifest=read('manifest.json');"
if s.count(old)!=1:
    raise SystemExit('verify read line mismatch')
s=s.replace(old,new,1)
anchor="ok(!/탈퇴는 두 번 확인하며/.test(index),'도움말 탈퇴 1회 확인 현행화');"
add="""ok(!index.includes('커뮤니티은'),'커뮤니티 사용자 문구 조사 오류 없음');
ok(!privacy.includes('소셜'),'개인정보처리방침 사용자 명칭 커뮤니티로 통일');"""
if s.count(anchor)!=1:
    raise SystemExit('verify anchor mismatch')
s=s.replace(anchor,anchor+'\n'+add,1)
p.write_text(s,encoding='utf-8')
print('verify invariants added')
