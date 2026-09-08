from pathlib import Path

ROOT = Path(__file__).resolve().parent


def apply_replacements(rel, replacements):
    path = ROOT / rel
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new, expected in replacements:
        count = text.count(old)
        if count != expected:
            raise SystemExit(f'{rel}: expected {expected} occurrence(s), found {count}: {old[:90]!r}')
        text = text.replace(old, new)
    if text == original:
        raise SystemExit(f'{rel}: no changes made')
    path.write_text(text, encoding='utf-8')
    print(f'updated {rel}: {len(replacements)} replacements')


apply_replacements('learning-data.js', [
    ('/* 오늘 한 걸음 — 회복학습 데이터 V8.2.32', '/* 오늘 한 걸음 — 회복학습 데이터 V8.2.54', 1),
    ('SMART는 나에게 중요한 가치와 현재 행동이 얼마나 맞는지 살펴보고, 변화의 장점과 어려움을 함께 검토하도록 돕습니다. 이를 위해 가치의 계층(HOV), 세 가지 질문, 변화계획, 비용-편익 분석(CBA), 중요성·자신감 척도 같은 도구를 사용합니다.', 'SMART는 나에게 중요한 가치와 현재 행동이 얼마나 맞는지 살펴보고, 변화의 장점과 어려움을 함께 검토하도록 돕습니다. 이를 위해 가치 우선순위 정하기, 내 선택 돌아보기, 변화 계획 세우기, 의사결정 저울, 변화 준비도 점검 같은 도구를 사용합니다.', 1),
    ('"label": "중요성 · 자신감 빠른 점검"', '"label": "변화 준비도 점검"', 1),
    ('"label": "HOV 가치의 계층 작성하기"', '"label": "가치 우선순위 정하기"', 1),
    ('"label": "나의 3가지 질문 작성하기"', '"label": "내 선택 돌아보기"', 1),
    ('"label": "변화 계획 워크시트 작성하기"', '"label": "변화 계획 세우기"', 1),
    ('"label": "CBA 비용-편익 분석 작성하기"', '"label": "의사결정 저울"', 1),
    ('SMART에서는 DEADS처럼 지연하기, 촉발상황에서 벗어나기, 충동을 지나가게 두기, 다른 활동으로 주의를 돌리기, 건강한 생각과 행동으로 대체하기를 활용합니다. DISARM과 ABC는 충동을 부추기는 자기대화와 믿음을 알아차리고 다른 방식으로 바라보는 데 사용합니다.', 'SMART에서는 충동 다루기처럼 지연하기, 촉발상황에서 벗어나기, 충동을 지나가게 두기, 다른 활동으로 주의를 돌리기, 건강한 생각과 행동으로 대체하기를 활용합니다. 중독 생각과 거리두기와 상황·생각·감정 돌아보기는 충동을 부추기는 자기대화와 믿음을 알아차리고 다른 방식으로 바라보는 데 사용합니다.', 1),
    ('"label": "DEADS 대처계획·실행하기"', '"label": "충동 다루기"', 1),
    ('"label": "DISARM 충동의 목소리 다루기"', '"label": "중독 생각과 거리두기"', 1),
    ('그러나 상대가 지금 얼마나 충동적인지 확인하거나 DEADS·DISARM을 대신 적용하려고 하지는 않습니다.', '그러나 상대가 지금 얼마나 충동적인지 확인하거나 충동 다루기·중독 생각과 거리두기를 대신 적용하려고 하지는 않습니다.', 1),
    ('가족인 나는 Point 3의 ABC·사고방식·문제해결처럼 내 생각과 반응을 다루는 도구를 사용하는 편이 맞습니다.', '가족인 나는 Point 3의 상황·생각·감정 돌아보기·생각의 함정 알아차리기·문제 해결하기처럼 내 생각과 반응을 다루는 도구를 사용하는 편이 맞습니다.', 1),
    ('지금 내 반응을 돌아보기 위해 ABC나 문제해결이 도움이 될 상황이 있나요?', '지금 내 반응을 돌아보기 위해 상황·생각·감정 돌아보기나 문제 해결하기가 도움이 될 상황이 있나요?', 1),
    ('ABC는 활성화 사건(A), 신념과 생각(B), 감정·행동의 결과(C)를 구분해서 살펴봅니다. 이어서 도움이 되지 않는 믿음에 질문을 던지고(D), 더 현실적이고 균형 잡힌 새로운 생각(E)을 만들어볼 수 있습니다.', '상황·생각·감정 돌아보기는 활성화 사건(A), 신념과 생각(B), 감정·행동의 결과(C)를 구분해서 살펴봅니다. 이어서 도움이 되지 않는 믿음에 질문을 던지고(D), 더 현실적이고 균형 잡힌 새로운 생각(E)을 만들어볼 수 있습니다.', 1),
    ('이 영역에서는 비합리적 신념에 이의제기하는 DIB/DIBS, 도움이 되지 않는 사고방식 알아차리기, 무조건적 자기·타인·삶의 수용, 문제 해결, 역할연습과 거절기술 같은 도구도 활용합니다. 목적은 감정을 없애는 것이 아니라 감정 속에서도 더 도움이 되는 선택을 할 수 있도록 연습하는 것입니다.', '이 영역에서는 생각 점검하기, 생각의 함정 알아차리기, 무조건적 자기·타인·삶의 수용, 문제 해결하기, 역할연습과 거절기술 같은 도구도 활용합니다. 목적은 감정을 없애는 것이 아니라 감정 속에서도 더 도움이 되는 선택을 할 수 있도록 연습하는 것입니다.', 1),
    ('"label": "ABC 문제 해결 작성하기"', '"label": "상황·생각·감정 돌아보기"', 1),
    ('"label": "DIBS 생각 반박하기"', '"label": "생각 점검하기"', 1),
    ('"label": "도움이 되지 않는 사고방식 점검하기"', '"label": "생각의 함정 알아차리기"', 1),
    ('"label": "문제 해결 · 5단계 작성하기"', '"label": "문제 해결하기"', 1),
    ('라이프스타일 평가와 Balance Pie는 건강, 가족, 일, 친구, 여가, 성장, 재정, 영적 삶처럼 중요한 영역의 만족도를 돌아보게 합니다.', '삶의 균형 살펴보기는 건강, 가족, 일, 친구, 여가, 성장, 재정, 영적 삶처럼 중요한 영역의 만족도를 돌아보게 합니다.', 1),
    ('VACI와 즐거운 활동 도구는 몰입할 수 있는 건강한 관심사와 새로운 즐거움을 찾도록 돕습니다.', '건강한 관심사 찾기와 즐거운 활동 도구는 몰입할 수 있는 건강한 관심사와 새로운 즐거움을 찾도록 돕습니다.', 1),
    ('SMART 목표와 주간 플래너는 원하는 변화를 구체적인 행동으로 바꾸는 데 사용합니다.', '실천 목표 세우기와 주간 플래너는 원하는 변화를 구체적인 행동으로 바꾸는 데 사용합니다.', 1),
    ('"label": "라이프스타일 밸런스 파이 작성하기"', '"label": "삶의 균형 살펴보기"', 1),
    ('"label": "VACI 관심사 목록 작성하기"', '"label": "건강한 관심사 찾기"', 1),
    ('"label": "SMART 목표 설정하기"', '"label": "실천 목표 세우기"', 1),
])

apply_replacements('index.html', [
    ("const BUILD = 'V8.2.53';", "const BUILD = 'V8.2.54';", 1),
    ('<div class="acc-n"><b>내 생각과 행동 살펴보기</b><span>상황·생각·감정 · 의사결정 저울 · 문제 해결</span></div>', '<div class="acc-n"><b>내 생각과 행동 살펴보기</b><span>상황·생각·감정 돌아보기 · 의사결정 저울 · 문제 해결하기</span></div>', 1),
    ('<b>내 생각과 반응 살펴보기</b>', '<b>상황·생각·감정 돌아보기</b>', 1),
    ('<b>내 행동의 득실 살펴보기</b>', '<b>의사결정 저울</b>', 1),
    ('<div class="acc-n"><b>내 생활 돌보기</b><span>삶의 균형 · 건강한 관심사 · 이완 · 건강 회복</span></div>', '<div class="acc-n"><b>내 생활 돌보기</b><span>삶의 균형 살펴보기 · 건강한 관심사 찾기 · 이완 · 건강 회복</span></div>', 1),
    ('<b>내 삶의 균형</b>', '<b>삶의 균형 살펴보기</b>', 1),
    ('<b>나를 살리는 건강한 관심사</b>', '<b>건강한 관심사 찾기</b>', 1),
    ("al:'내 생각과 반응 살펴보기'", "al:'상황·생각·감정 돌아보기'", 1),
    ("al:'내 행동의 득실 살펴보기로 살펴보기'", "al:'의사결정 저울로 살펴보기'", 1),
    ("al:'내 삶의 균형 살펴보기'", "al:'삶의 균형 살펴보기'", 1),
    ("'smart-change-plan':'변화 계획',", "'smart-change-plan':'변화 계획 세우기',", 1),
    ("'nav-smart-hov':['가치 우선순위 열기','smart-hov']", "'nav-smart-hov':['가치 우선순위 정하기 열기','smart-hov']", 1),
    ("'nav-smart-disarm':['생각과 거리두기 열기','smart-disarm']", "'nav-smart-disarm':['중독 생각과 거리두기 열기','smart-disarm']", 1),
    ("'nav-smart-dibs':['생각 점검 열기','smart-dibs']", "'nav-smart-dibs':['생각 점검하기 열기','smart-dibs']", 1),
    ("'nav-smart-problem':['문제 해결 열기','smart-problem-solving']", "'nav-smart-problem':['문제 해결하기 열기','smart-problem-solving']", 1),
    ("'nav-smart-balance':['삶의 균형 열기','smart-balance-pie']", "'nav-smart-balance':['삶의 균형 살펴보기 열기','smart-balance-pie']", 1),
    ("'nav-smart-goal':['실천 목표 열기','smart-goal']", "'nav-smart-goal':['실천 목표 세우기 열기','smart-goal']", 1),
    ("'goal':'실천 목표'", "'goal':'실천 목표 세우기'", 1),
    ("famMode()?'당사자의 충동 대처를 이해하는 참고 영역':'즉시 대처 · 충동 다루기 · 생각과 거리두기 · 충동일기'", "famMode()?'당사자의 충동 대처를 이해하는 참고 영역':'즉시 대처 · 충동 다루기 · 중독 생각과 거리두기 · 충동일기'", 1),
    ("smartPointAccordion('Point 3 · 생각·감정·행동 관리하기','상황·생각·감정 · 생각 점검 · 생각의 함정 · 문제해결'", "smartPointAccordion('Point 3 · 생각·감정·행동 관리하기','상황·생각·감정 돌아보기 · 생각 점검하기 · 생각의 함정 알아차리기 · 문제 해결하기'", 1),
    ("smartPointAccordion('Point 4 · 균형 잡힌 삶 살기','삶의 균형 · 건강한 관심사 · 목표 · 이완 · 건강'", "smartPointAccordion('Point 4 · 균형 잡힌 삶 살기','삶의 균형 살펴보기 · 건강한 관심사 찾기 · 실천 목표 세우기 · 이완 · 건강'", 1),
    ('회복 실천도구는 4-Point를 순서대로 통과하는 방식이 아니라 지금 필요한 영역에서 가치 우선순위, 의사결정 저울, 충동 다루기, 생각과 거리두기, 생각 점검, 건강한 관심사 찾기 같은 도구를 반복해서 사용합니다.', '회복 실천도구는 4-Point를 순서대로 통과하는 방식이 아니라 지금 필요한 영역에서 가치 우선순위 정하기, 의사결정 저울, 충동 다루기, 중독 생각과 거리두기, 생각 점검하기, 건강한 관심사 찾기 같은 도구를 반복해서 사용합니다.', 1),
    ('아직 저장한 밸런스 파이가 없습니다.', '아직 저장한 삶의 균형 기록이 없습니다.', 1),
    ('저장한 밸런스 파이 ', '저장한 삶의 균형 기록 ', 1),
    ("record?'밸런스 파이 수정':'삶의 균형 살펴보기'", "record?'삶의 균형 수정':'삶의 균형 살펴보기'", 1),
    ('다음 · 파이 돌아보기', '다음 · 전체 균형 돌아보기', 1),
    ('2 · 완성된 파이 돌아보기', '2 · 전체 균형 돌아보기', 1),
    ('파이를 보며 든 생각과 감정', '전체 균형을 보며 든 생각과 감정', 1),
    ("(record?'수정 저장':'밸런스 파이 저장')", "(record?'수정 저장':'삶의 균형 저장')", 1),
    ("toast(record?'밸런스 파이를 수정했습니다.':'밸런스 파이를 저장했습니다.')", "toast(record?'삶의 균형 기록을 수정했습니다.':'삶의 균형 기록을 저장했습니다.')", 1),
    ("sec('파이를 보며 알아차린 점',r.reflection)", "sec('전체 균형에서 알아차린 점',r.reflection)", 1),
    ('밸런스 파이를 작성했다면 그 영역이 제안됩니다.', '삶의 균형 기록이 있다면 그 영역이 제안됩니다.', 1),
    ("<h3>SMART 기준</h3>", "<h3>목표 기준</h3>", 1),
    ("+' · SMART '+smartGoalCriteriaCount(r)+'/5'", "+' · 기준 '+smartGoalCriteriaCount(r)+'/5'", 1),
])

apply_replacements('sw.js', [
    ("const APP_VERSION = 'V8.2.53';", "const APP_VERSION = 'V8.2.54';", 1),
    ("const V = 'ohg-v8253-generic-tool-names';", "const V = 'ohg-v8254-smart-copy-completion';", 1),
])

readme = ROOT / 'README.md'
text = readme.read_text(encoding='utf-8')
if not text.startswith('## V8.2.53 — 회복 실천도구 범용 명칭 정리'):
    raise SystemExit('README.md: unexpected top version')
entry = '''## V8.2.54 — 회복 실천도구 문구 통합 마무리
- V8.2.53의 범용 명칭 원칙을 `회복학습 → SMART Recovery` Point 1~4의 본문·실천 버튼까지 적용했습니다.
- 가족도구·마음프로·삶의 균형·실천 목표 화면에 남아 있던 우회 표현과 `밸런스 파이`·축약 도구명을 같은 한국어 명칭으로 통일했습니다.
- `SMART Recovery`·4-Point 소개와 A~E 등 학습 구조는 유지하며, 기존 `hov`, `cba`, `deads`, `disarm`, `abc`, `dibs`, `vaci` 등 내부 식별값과 `smartWorks` 저장형식은 변경하지 않습니다.
- `DATA_SCHEMA=6`, `ohg.v1`, Android 네이티브 TTS·정확알림·화면 OFF 알림·부팅 재예약·외래 반복예약·이완 TTS는 변경하지 않습니다.

'''
readme.write_text(entry + text, encoding='utf-8')
print('updated README.md')

# Guardrails: user-visible legacy labels that should be gone from live UI/data.
index = (ROOT / 'index.html').read_text(encoding='utf-8')
learning = (ROOT / 'learning-data.js').read_text(encoding='utf-8')
prohibited_index = [
    'SMART 실천도구', '내 생각과 반응 살펴보기', '내 행동의 득실 살펴보기',
    '나를 살리는 건강한 관심사', '내 삶의 균형 살펴보기', '밸런스 파이',
    'SMART 기준', ' · SMART '
]
prohibited_learning = [
    '중요성 · 자신감 빠른 점검', 'HOV 가치의 계층 작성하기', '나의 3가지 질문 작성하기',
    '변화 계획 워크시트 작성하기', 'CBA 비용-편익 분석 작성하기',
    'DEADS 대처계획·실행하기', 'DISARM 충동의 목소리 다루기',
    'ABC 문제 해결 작성하기', 'DIBS 생각 반박하기',
    '도움이 되지 않는 사고방식 점검하기', '문제 해결 · 5단계 작성하기',
    '라이프스타일 밸런스 파이 작성하기', 'VACI 관심사 목록 작성하기', 'SMART 목표 설정하기'
]
for s in prohibited_index:
    if s in index:
        raise SystemExit(f'index.html: legacy user copy remains: {s}')
for s in prohibited_learning:
    if s in learning:
        raise SystemExit(f'learning-data.js: legacy user copy remains: {s}')

# Guardrails for storage/native boundaries.
for s in ["const DATA_SCHEMA = 6", "const KEY = 'ohg.v1'"]:
    if s not in index:
        raise SystemExit(f'index.html: required storage invariant missing: {s}')
for s in ["kind:'deads'", "kind:'disarm'", "kind:'abc'", "kind:'dibs'", "kind:'vaci'", "kind:'smart-goal'", "kind:'lifestyle-balance-pie'"]:
    if s not in index:
        raise SystemExit(f'index.html: internal identifier missing: {s}')
if "r.tool==='hov'" not in index or "r.tool==='cba'" not in index:
    raise SystemExit('index.html: HOV/CBA internal tool identifiers changed')

print('copy audit and invariants OK')
