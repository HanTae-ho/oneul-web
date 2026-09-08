from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

if "const BUILD = 'V8.2.52';" not in s:
    raise SystemExit('unexpected BUILD baseline')
s=s.replace("const BUILD = 'V8.2.52';","const BUILD = 'V8.2.53';",1)

# User-facing recovery-tool names only. Internal ids/kinds/storage keys stay unchanged.
repls=[
('SMART 실천도구','회복 실천도구'),
('내 SMART 기록 보기','내 실천도구 기록 보기'),
('SMART 전체 도구 더 보기','회복 실천도구 더 보기'),
("{v:'smart',l:'SMART'}","{v:'smart',l:'실천도구'}"),
("smart:'저장된 SMART 기록이 없습니다.'","smart:'저장된 실천도구 기록이 없습니다.'"),

('중요성 · 자신감 빠른 점검','변화 준비도 점검'),
('가치의 계층 HOV','가치 우선순위 정하기'),
('나의 3가지 질문','내 선택 돌아보기'),
('변화 계획 워크시트','변화 계획 세우기'),
('비용-편익 분석 CBA','의사결정 저울'),
('DEADS · 충동 대처','충동 다루기'),
('DISARM · 충동의 목소리 분리하기','중독 생각과 거리두기'),
('DISARM · 충동의 목소리','중독 생각과 거리두기'),
('ABC 문제 해결','상황·생각·감정 돌아보기'),
('DIBS · 생각 반박하기','생각 점검하기'),
('DIBS 생각 반박하기','생각 점검하기'),
('도움이 되지 않는 사고방식','생각의 함정 알아차리기'),
('문제 해결 · 5단계','문제 해결하기'),
('라이프스타일 밸런스 파이','삶의 균형 살펴보기'),
('VACI · 활력 넘치는 창의적 관심사','건강한 관심사 찾기'),
('SMART 목표 설정','실천 목표 세우기'),
('SMART 목표','실천 목표'),

# Family-tool display wording.
('ABC · CBA · 문제 해결 5단계','상황·생각·감정 · 의사결정 저울 · 문제 해결'),
('내 행동 CBA','내 행동의 득실 살펴보기'),
('삶의 균형 · VACI · 이완 · 건강 회복','삶의 균형 · 건강한 관심사 · 이완 · 건강 회복'),
('VACI · 나를 살리는 활동','나를 살리는 건강한 관심사'),

# Saved-record labels/back labels.
("'importance-confidence':'중요성 · 자신감'","'importance-confidence':'변화 준비도 점검'"),
("'change-plan':'변화 계획'","'change-plan':'변화 계획 세우기'"),
("'disarm':'DISARM'","'disarm':'중독 생각과 거리두기'"),
("'abc':'ABC · 생각과 행동 살펴보기'","'abc':'상황·생각·감정 돌아보기'"),
("'dibs':'DIBS · 생각 반박'","'dibs':'생각 점검하기'"),
("'thinking-styles':'사고방식 점검'","'thinking-styles':'생각의 함정 알아차리기'"),
("'balance-pie':'삶의 균형'","'balance-pie':'삶의 균형 살펴보기'"),
("'vaci':'VACI'","'vaci':'건강한 관심사 찾기'"),

# Hub summaries: keep SMART Recovery learning/source name, but show generic tool labels.
('DEADS·DISARM·충동일기는','충동 다루기·중독 생각과 거리두기·충동일기는'),
("'즉시 대처 · DEADS · DISARM · 충동일기'","'즉시 대처 · 충동 다루기 · 생각과 거리두기 · 충동일기'"),
("'ABC · DIBS · 사고방식 · 문제해결'","'상황·생각·감정 · 생각 점검 · 생각의 함정 · 문제해결'"),
("'삶의 균형 · VACI · 목표 · 이완 · 건강'","'삶의 균형 · 건강한 관심사 · 목표 · 이완 · 건강'"),

# HOV editor display labels only.
("'HOV 수정'","'가치 우선순위 수정'"),
("'가치 우선순위 정하기 작성'","'가치 우선순위 작성'"),
("'HOV 저장'","'가치 우선순위 저장'"),
('SMART Recovery HOV는 내 목표와 현재 행동의 차이를 알아차리는 도구입니다.','가치 우선순위를 정하면서 내 목표와 현재 행동의 차이를 알아차리는 도구입니다.'),

# CBA editor display labels only.
("'CBA 수정'","'의사결정 저울 수정'"),
("'CBA 저장'","'의사결정 저울 저장'"),

# DEADS display labels only; strategy content and internal kind remain unchanged.
('지금 DEADS 사용하기','지금 충동 다루기'),
('+ 내 DEADS 계획 작성하기','+ 충동 대처 계획 작성하기'),
('DEADS는 충동을 직접 경험하는 사람이','이 도구는 충동을 직접 경험하는 사람이'),
('아직 저장한 DEADS 계획이 없습니다.','아직 저장한 충동 대처 계획이 없습니다.'),
('저장한 DEADS 계획 ','저장한 충동 대처 계획 '),
('내 DEADS 계획','내 충동 대처 계획'),
('DEADS 계획 수정','충동 대처 계획 수정'),
('DEADS 계획 저장','충동 대처 계획 저장'),
('DEADS 계획을 수정했습니다.','충동 대처 계획을 수정했습니다.'),
('DEADS 계획을 저장했습니다.','충동 대처 계획을 저장했습니다.'),
('이 DEADS 계획을 삭제할까요?','이 충동 대처 계획을 삭제할까요?'),
('다른 DEADS 전략 고르기','다른 충동 대처 방법 고르기'),
("urgeUseCope('DEADS · '+m.short)","urgeUseCope('충동 다루기 · '+m.short)"),

# DISARM display labels only; internal kind remains unchanged.
('지금 DISARM 사용하기','지금 중독 생각과 거리두기'),
('+ 내 DISARM 대처문장 만들기','+ 거리두기 문장 만들기'),
('이 초심으로 DISARM 해보기','이 초심으로 생각과 거리두기'),
("'← DISARM'","'← 생각과 거리두기'"),
('DISARM은 충동을 직접 경험하는 사람이','이 도구는 충동을 직접 경험하는 사람이'),
('아직 저장한 DISARM 대처문장이 없습니다.','아직 저장한 거리두기 문장이 없습니다.'),
('저장한 DISARM 대처문장 ','저장한 거리두기 문장 '),
('DISARM 대처문장 수정','거리두기 문장 수정'),
('내 DISARM 대처문장 만들기','거리두기 문장 만들기'),
('DISARM 대처문장 저장','거리두기 문장 저장'),
('DISARM 대처문장을 수정했습니다.','거리두기 문장을 수정했습니다.'),
('DISARM 대처문장을 저장했습니다.','거리두기 문장을 저장했습니다.'),
('내 DISARM 대처문장','내 거리두기 문장'),
('이 DISARM 대처문장을 삭제할까요?','이 거리두기 문장을 삭제할까요?'),
('DISARM으로 5분 버티기','생각과 거리두기로 5분 버티기'),
('다른 DISARM 기록 보기','다른 거리두기 기록 보기'),
("urgeUseCope('DISARM · 자기대화 거부·대체')","urgeUseCope('중독 생각과 거리두기 · 자기대화 거부·대체')"),

# ABC/DIBS/Thinking display labels only; A-B-C-D-E fields and record keys stay unchanged.
('+ ABC 새로 작성하기','+ 새로 작성하기'),
("'ABC 수정'","'상황·생각·감정 돌아보기 수정'"),
("'ABC 저장'","'저장'"),
('아직 작성한 ABC가 없습니다.','아직 작성한 상황·생각·감정 기록이 없습니다.'),
('저장한 ABC ','저장한 상황·생각·감정 기록 '),
("r.a||'ABC 기록'","r.a||'상황 돌아보기 기록'"),
('이 ABC 기록을 삭제할까요?','이 상황·생각·감정 기록을 삭제할까요?'),
('ABC 기록을 삭제했습니다.','기록을 삭제했습니다.'),
('+ DIBS 새로 작성하기','+ 새로 작성하기'),
("'DIBS 수정'","'생각 점검 수정'"),
("'DIBS 저장'","'생각 점검 저장'"),
('아직 저장한 DIBS 기록이 없습니다.','아직 저장한 생각 점검 기록이 없습니다.'),
('저장한 DIBS ','저장한 생각 점검 기록 '),
("r.ib||'DIBS 기록'","r.ib||'생각 점검 기록'"),
('<h2>DIBS 기록</h2>','<h2>생각 점검 기록</h2>'),
('이 DIBS 기록을 삭제할까요?','이 생각 점검 기록을 삭제할까요?'),
('+ 내 사고방식 점검하기','+ 생각의 함정 점검하기'),
('사고방식 점검 기록을 삭제할까요?','생각의 함정 기록을 삭제할까요?'),
('이 생각으로 ABC 작성하기','이 상황·생각·감정 돌아보기'),
('이 생각으로 DIBS 작성하기','이 생각 점검하기'),

# Balance/VACI/goal display labels only.
('+ 밸런스 파이 새로 작성하기','+ 삶의 균형 새로 작성하기'),
('밸런스 파이 기록','삶의 균형 기록'),
('+ VACI 목록 새로 작성하기','+ 건강한 관심사 목록 만들기'),
('아직 저장한 VACI 목록이 없습니다.','아직 저장한 건강한 관심사 목록이 없습니다.'),
('저장한 VACI 목록 ','저장한 건강한 관심사 목록 '),
("'VACI 목록 수정'","'건강한 관심사 목록 수정'"),
("'VACI 관심사 찾기'","'건강한 관심사 찾기'"),
("'VACI 목록 저장'","'건강한 관심사 목록 저장'"),
('선택한 활동 VACI에 추가','선택한 활동 목록에 추가'),
('선택한 활동이 이미 VACI에 있습니다.','선택한 활동이 이미 목록에 있습니다.'),
('개 활동을 VACI에 추가했습니다.','개 활동을 목록에 추가했습니다.'),
('VACI 목록을 수정했습니다.','건강한 관심사 목록을 수정했습니다.'),
('VACI 목록을 저장했습니다.','건강한 관심사 목록을 저장했습니다.'),
('이 VACI 목록 삭제','이 건강한 관심사 목록 삭제'),
('이 VACI 목록을 삭제할까요?','이 건강한 관심사 목록을 삭제할까요?'),
('VACI 목록을 삭제했습니다.','건강한 관심사 목록을 삭제했습니다.'),
]

critical=['SMART 실천도구','가치의 계층 HOV','비용-편익 분석 CBA','DEADS · 충동 대처','DISARM · 충동의 목소리 분리하기','ABC 문제 해결','DIBS · 생각 반박하기','VACI · 활력 넘치는 창의적 관심사']
for old in critical:
    if old not in s:
        raise SystemExit('missing critical source: '+old)

for old,new in repls:
    s=s.replace(old,new)

# AI local helper: understand both legacy SMART terms and the new generic labels, but reply with generic names.
s=s.replace("{re:/\\bHOV\\b|가치의\\s*계층/i,name:'가치 우선순위 정하기'", "{re:/\\bHOV\\b|가치의\\s*계층|가치\\s*우선순위/i,name:'가치 우선순위 정하기'")
s=s.replace("{re:/\\bCBA\\b|비용.?편익/i,name:'의사결정 저울'", "{re:/\\bCBA\\b|비용.?편익|의사결정\\s*저울|선택의\\s*득실/i,name:'의사결정 저울'")
s=s.replace("{re:/\\bDEADS\\b/i,name:'DEADS'", "{re:/\\bDEADS\\b|충동\\s*다루기/i,name:'충동 다루기'")
s=s.replace("{re:/\\bDISARM\\b/i,name:'DISARM'", "{re:/\\bDISARM\\b|중독\\s*생각.*거리두기|생각과\\s*거리두기/i,name:'중독 생각과 거리두기'")
s=s.replace("{re:/\\bABC\\b/i,name:'ABC'", "{re:/\\bABC\\b|상황.*생각.*감정/i,name:'상황·생각·감정 돌아보기'")
s=s.replace("{re:/\\bDIBS\\b/i,name:'DIBS'", "{re:/\\bDIBS\\b|생각\\s*점검/i,name:'생각 점검하기'")
s=s.replace("{re:/\\bVACI\\b/i,name:'VACI'", "{re:/\\bVACI\\b|건강한\\s*관심사/i,name:'건강한 관심사 찾기'")
s=s.replace("{re:/사고방식.*(점검|도구)|생각의\\s*함정|도움이\\s*되지\\s*않는\\s*사고/i,name:'사고방식 점검'", "{re:/사고방식.*(점검|도구)|생각의\\s*함정|도움이\\s*되지\\s*않는\\s*사고/i,name:'생각의 함정 알아차리기'")
s=s.replace("{re:/문제\\s*해결.*(5|다섯|도구|단계)/i,name:'문제 해결 5단계'", "{re:/문제\\s*해결.*(5|다섯|도구|단계|하기)/i,name:'문제 해결하기'")
s=s.replace("{re:/삶의\\s*균형/i,name:'삶의 균형'", "{re:/삶의\\s*균형/i,name:'삶의 균형 살펴보기'")
s=s.replace("{re:/SMART\\s*목표|스마트\\s*목표/i,name:'실천 목표'", "{re:/SMART\\s*목표|스마트\\s*목표|실천\\s*목표/i,name:'실천 목표 세우기'")

p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
t=sw.read_text(encoding='utf-8')
if "const APP_VERSION = 'V8.2.52';" not in t:
    raise SystemExit('unexpected sw baseline')
t=t.replace("const APP_VERSION = 'V8.2.52';","const APP_VERSION = 'V8.2.53';",1)
t=t.replace("const V = 'ohg-v8252-selfcheck-card-guide';","const V = 'ohg-v8253-generic-tool-names';",1)
sw.write_text(t,encoding='utf-8')

rd=Path('README.md')
r=rd.read_text(encoding='utf-8')
head="""## V8.2.53 — 회복 실천도구 범용 명칭 정리
- `회복학습 → SMART Recovery` 소개는 그대로 유지하고, 실제 실천도구의 사용자 표시 명칭만 쉬운 한국어·범용 용어로 정리했습니다.
- 예: `가치 우선순위 정하기`, `의사결정 저울`, `충동 다루기`, `중독 생각과 거리두기`, `상황·생각·감정 돌아보기`, `생각 점검하기`, `건강한 관심사 찾기`, `실천 목표 세우기`.
- `내 발자취 → 실천기록`, 가족도구, 마음프로의 도구 안내와 바로가기 명칭도 같은 용어로 맞췄습니다.
- 기존 `hov`, `cba`, `deads`, `disarm`, `abc`, `dibs`, `vaci` 등 내부 식별값과 `smartWorks` 저장형식은 변경하지 않습니다.
- `DATA_SCHEMA=6`, `ohg.v1`, Android 네이티브 TTS·정확알림·화면 OFF 알림·부팅 재예약·외래 반복예약·이완 TTS는 변경하지 않습니다.

"""
rd.write_text(head+r,encoding='utf-8')
