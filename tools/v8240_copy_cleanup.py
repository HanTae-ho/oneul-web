from pathlib import Path

idx = Path('index.html')
sw = Path('sw.js')
readme = Path('README.md')
text = idx.read_text(encoding='utf-8')


def repl(old, new, count=1):
    global text
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f'replace count mismatch: expected {count}, got {actual} for: {old[:120]!r}')
    text = text.replace(old, new, count)

# Version
repl("const BUILD = 'V8.2.39';", "const BUILD = 'V8.2.40';")

# 가족도구: 임상적 경계는 유지하고 화면 구조 설명은 제거
repl(
    '<div class="note" style="margin-bottom:14px">상대를 감시하거나 바꾸기 위한 도구가 아닙니다. 가족인 <b>내가 내 생각·행동·경계·생활을 돌보기 위해</b> 사용합니다. 가족 전용 도구 3개는 바로 보이고, 기존 보조도구는 필요할 때만 펼칩니다.</div>',
    '<div class="note" style="margin-bottom:14px">상대를 감시하거나 바꾸기 위한 도구가 아닙니다. 가족인 <b>내가 내 생각·행동·경계·생활을 돌보기 위해</b> 사용합니다.</div>'
)
repl(
    '  <div class="note" style="margin-top:14px">가족 12단계 점검, 가족 모임, 긴급 도움은 각각 기존 <b>내 발자취 · 모임 · 헬프</b> 위치에서 그대로 사용합니다.</div>\n  <button class="btn ghost" id="family-smart-all" style="margin-top:9px">SMART 전체 도구 더 보기</button>',
    '  <button class="btn sec" id="family-smart-all" style="margin-top:14px;background:var(--accbg);border:1px solid var(--acc2);color:var(--acc);font-weight:700">SMART 전체 도구 더 보기</button>'
)

# 자가점검: 모드/표시 로직 설명 제거
repl(
    "    h+='<div class=\"screen-group\"><h2>내 회복영역 점검</h2><p class=\"tiny\">내정보에서 선택한 회복영역에 맞는 검사만 표시합니다.</p>';",
    "    h+='<div class=\"screen-group\"><h2>내 회복영역 점검</h2>';"
)
repl(
    "  } else {\n    h+='<div class=\"note\" style=\"margin-bottom:13px\">가족·보호자 모드에서는 당사자 대신 중독 선별검사를 작성하지 않습니다. 아래 마음건강 점검은 이 앱을 사용하는 본인의 상태를 살펴보는 용도입니다.</div>';\n  }\n  h+='<div class=\"screen-group\"><h2>마음건강 공통점검</h2><p class=\"tiny\">우울 · 불안 · 스트레스는 모든 사용자에게 공통으로 표시합니다.</p>'+g.common.map(screenCardHtml).join('')+'</div>';",
    "  }\n  h+='<div class=\"screen-group\"><h2>마음건강 공통점검</h2>'+g.common.map(screenCardHtml).join('')+'</div>';"
)
repl(
    "    h+='<div class=\"screen-group\"><h2>기타중독 점검</h2><p class=\"tiny\">내정보에서 기타 회복영역을 선택한 경우 표시됩니다.</p>'+g.other.map(screenCardHtml).join('')+'</div>';",
    "    h+='<div class=\"screen-group\"><h2>기타중독 점검</h2>'+g.other.map(screenCardHtml).join('')+'</div>';"
)

# 내 정보: 아코디언 동작 설명 제거
repl(
    '  <p class="muted" style="margin:-10px 0 16px">\n    누르면 펼쳐집니다. 한 번에 하나씩 열립니다.\n  </p>\n',
    ''
)

# 내 발자취 > 실천기록: 저장 구현 설명은 대체 없이 삭제
repl(
    "    c.appendChild(el('p','muted','기존 저장방식은 그대로 두고 최근 기록부터 한곳에서 보여줍니다. 기록을 누르면 해당 도구의 저장목록으로 이동합니다.'));\n",
    ''
)
repl(
    "    if(rows.length>30) c.appendChild(el('p','tiny','최근 30건을 표시합니다. 각 도구 안의 기존 기록은 그대로 유지됩니다.'));",
    "    if(rows.length>30) c.appendChild(el('p','tiny','최근 30건을 표시합니다.'));"
)

# SMART 허브: 4-Point 의미만 남기고 화면 구현/저장 구현 설명 제거
repl(
    '    SMART Recovery의 4-Point는 순서대로 통과하는 단계가 아닙니다. 아래 <b>4개 영역 중 지금 필요한 한 곳</b>을 눌러 도구를 펼쳐보세요. 한 번에 한 영역만 열리며, 작성 내용은 기존 원칙대로 <b>이 기기에만 저장</b>됩니다.',
    '    SMART Recovery의 4-Point는 순서대로 통과하는 단계가 아닙니다. <b>지금 필요한 영역</b>을 골라 도구를 사용해보세요.'
)

# SMART 개별 도구: 사용자에게 필요한 목적 설명만 남김
repl(
    '    내 삶에서 가장 중요한 가치를 분명히 하고, 지금의 행동이 그 가치와 얼마나 맞는지 돌아봅니다. SMART Recovery의 <b>Hierarchy of Values(HOV)</b>를 앱에 맞게 재구성했으며, <b>내용은 이 기기에만 저장</b>됩니다.',
    '    내 삶에서 가장 중요한 가치를 분명히 하고, 지금의 행동이 그 가치와 얼마나 맞는지 돌아봅니다.'
)
repl(
    '    지금 행동의 이득과 대가, 중단했을 때의 이득과 어려움을 한곳에서 비교합니다. 각 항목은 <b>단기·장기</b>로 구분합니다. SMART Recovery의 <b>Cost-Benefit Analysis(CBA)</b>를 앱에 맞게 재구성했으며, <b>내용은 이 기기에만 저장</b>됩니다.',
    '    지금 행동의 이득과 대가, 중단했을 때의 이득과 어려움을 한곳에서 비교합니다. 각 항목은 <b>단기·장기</b>로 구분합니다.'
)
repl(
    '    원하는 변화를 분명히 하고, 이유·단계·도움·진전의 신호·방해요인을 한 장의 계획으로 정리합니다. SMART Recovery의 <b>Change Plan Worksheet</b>를 앱에 맞게 재구성했으며, <b>내용은 이 기기에만 저장</b>됩니다.',
    '    원하는 변화를 분명히 하고, 이유·단계·도움·진전의 신호·방해요인을 한 장의 계획으로 정리합니다.'
)
repl(
    '    내가 원하는 미래와 현재 행동의 차이를 알아차리고, 그 차이를 변화 동기로 활용합니다. SMART Recovery의 <b>My Three Questions worksheet</b>를 앱에 맞게 재구성했으며, <b>내용은 이 기기에만 저장</b>됩니다.',
    '    내가 원하는 미래와 현재 행동의 차이를 알아차리고, 그 차이를 변화 동기로 활용합니다.'
)
repl(
    '    충동이 올라왔을 때 <b>거부·지연 → 벗어나기 → 회피·수용·반박 → 주의 돌리기 → 대체하기</b> 중 지금 맞는 전략을 골라 실행합니다. SMART Recovery의 DEADS를 앱에 맞게 재구성했으며, 내 계획은 <b>이 기기에만 저장</b>됩니다.',
    '    충동이 올라왔을 때 <b>거부·지연 → 벗어나기 → 회피·수용·반박 → 주의 돌리기 → 대체하기</b> 중 지금 맞는 전략을 골라 실행합니다.'
)
repl(
    '    <b>DISARM(Destructive Images and Self-talk Awareness and Refusal Method)</b>은 충동을 부추기는 파괴적인 이미지·자기대화를 알아차리고, 현실적이고 건설적인 생각으로 거부·대체하는 도구입니다. 충동이나 그 목소리에 이름을 붙이는 것은 <b>선택</b>이며, 내 계획은 <b>이 기기에만 저장</b>됩니다.',
    '    <b>DISARM(Destructive Images and Self-talk Awareness and Refusal Method)</b>은 충동을 부추기는 파괴적인 이미지·자기대화를 알아차리고, 현실적이고 건설적인 생각으로 거부·대체하는 도구입니다. 충동이나 그 목소리에 이름을 붙이는 것은 <b>선택</b>입니다.'
)
repl(
    '    힘든 <b>사건(A)</b>과 그 사건에 대한 <b>생각·신념(B)</b>, 그로 인한 <b>감정·행동의 결과(C)</b>를 나누어 봅니다. 이어서 생각에 질문하고 <b>반박(D)</b>한 뒤, 더 현실적이고 도움이 되는 <b>새로운 생각(E)</b>을 만들어봅니다. 내용은 <b>이 기기에만 저장</b>됩니다.',
    '    힘든 <b>사건(A)</b>과 그 사건에 대한 <b>생각·신념(B)</b>, 그로 인한 <b>감정·행동의 결과(C)</b>를 나누어 봅니다. 이어서 생각에 질문하고 <b>반박(D)</b>한 뒤, 더 현실적이고 도움이 되는 <b>새로운 생각(E)</b>을 만들어봅니다.'
)
repl(
    '  <div class="note" style="margin-bottom:12px">도움이 되지 않는 신념을 알아차리고, 그것을 <b>질문으로 바꾸어 사실·논리·장기적 도움 여부를 점검</b>한 뒤 더 균형 잡힌 합리적 신념으로 바꿔봅니다. 내용은 <b>이 기기에만 저장</b>됩니다.</div>',
    '  <div class="note" style="margin-bottom:12px">도움이 되지 않는 신념을 알아차리고, 그것을 <b>질문으로 바꾸어 사실·논리·장기적 도움 여부를 점검</b>한 뒤 더 균형 잡힌 합리적 신념으로 바꿔봅니다.</div>'
)
repl(
    '    자주 반복되는 사고방식을 <b>빨리 알아차리는 연습</b>입니다. 유형을 고른 뒤 최근 실제 생각을 적어보고, 필요하면 <b>ABC 또는 DIBS</b>로 바로 이어서 점검할 수 있습니다. 진단이 아니라 자기점검 도구이며, 내용은 <b>이 기기에만 저장</b>됩니다.',
    '    자주 반복되는 사고방식을 <b>빨리 알아차리는 연습</b>입니다. 유형을 고른 뒤 최근 실제 생각을 적어보고, 필요하면 <b>ABC 또는 DIBS</b>로 바로 이어서 점검할 수 있습니다. 진단이 아니라 자기점검 도구입니다.'
)
repl(
    '    상황을 어떻게 처리해야 할지 확신이 없을 때, 문제를 구체적으로 정의하고 <b>브레인스토밍 → 평가 → 선택 → 서면 계획</b>으로 이어갑니다. SMART Recovery의 <b>문제 해결을 위한 5단계</b>와 문제 해결 워크시트를 바탕으로 앱에 맞게 구성했으며, 내용은 <b>이 기기에만 저장</b>됩니다.',
    '    상황을 어떻게 처리해야 할지 확신이 없을 때, 문제를 구체적으로 정의하고 <b>브레인스토밍 → 평가 → 선택 → 서면 계획</b>으로 이어갑니다.'
)
repl(
    '    내 삶에서 중요한 영역을 나누고 각 영역의 현재 만족도를 <b>0~10</b>으로 표시해 전체적인 균형을 살펴봅니다. 바깥쪽은 매우 만족스러운 상태(10), 중심은 매우 불만족스러운 상태(0)로 봅니다. SMART Recovery의 <b>Lifestyle Balance Pie</b>를 바탕으로 모바일에 맞게 구성했으며, 내용은 <b>이 기기에만 저장</b>됩니다.',
    '    내 삶에서 중요한 영역을 나누고 각 영역의 현재 만족도를 <b>0~10</b>으로 표시해 전체적인 균형을 살펴봅니다. 바깥쪽은 매우 만족스러운 상태(10), 중심은 매우 불만족스러운 상태(0)로 봅니다.'
)
repl(
    '    중독행동이 차지하던 시간과 즐거움의 자리에 <b>건강하게 몰입할 수 있는 관심사</b>를 다시 찾아봅니다. 활동이 잘 떠오르지 않으면 <b>즐거운 활동 아이디어</b>에서 몇 가지를 골라 VACI에 바로 추가할 수 있습니다. 해보고 싶은 활동을 <b>시도 전 1~10점</b>으로 표시한 뒤 실제로 해본 후 <b>시도 후 점수와 생각</b>을 다시 기록합니다. 한 가지 활동이 또 다른 과도한 몰입이 되지 않도록 균형 있게 시도해보세요. 내용은 <b>이 기기에만 저장</b>됩니다.',
    '    중독행동이 차지하던 시간과 즐거움의 자리에 <b>건강하게 몰입할 수 있는 관심사</b>를 다시 찾아봅니다. 활동이 잘 떠오르지 않으면 <b>즐거운 활동 아이디어</b>에서 몇 가지를 골라 VACI에 바로 추가할 수 있습니다. 해보고 싶은 활동을 <b>시도 전 1~10점</b>으로 표시한 뒤 실제로 해본 후 <b>시도 후 점수와 생각</b>을 다시 기록합니다. 한 가지 활동이 또 다른 과도한 몰입이 되지 않도록 균형 있게 시도해보세요.'
)
repl(
    '    삶의 영역과 중요한 가치를 연결해 목표를 적고, <b>구체적 · 측정가능 · 동의가능 · 현실적 · 시간제한</b>의 다섯 기준으로 점검합니다. 마지막에는 실제로 할 행동을 정합니다. 반복해서 이어가고 싶은 행동은 기존 <b>습관</b>으로 바로 연결할 수 있습니다. 내용은 <b>이 기기에만 저장</b>됩니다.',
    '    삶의 영역과 중요한 가치를 연결해 목표를 적고, <b>구체적 · 측정가능 · 동의가능 · 현실적 · 시간제한</b>의 다섯 기준으로 점검합니다. 마지막에는 실제로 할 행동을 정합니다. 반복해서 이어가고 싶은 행동은 <b>습관</b>으로 바로 연결할 수 있습니다.'
)

# 충동일기: 도구 출처/구현 설명 제거
repl(
    '    충동은 특정 시간·상황·촉발요인에서 반복될 수 있습니다. 기록을 모아 내 패턴과 나에게 도움이 된 대처를 찾아봅니다. SMART Recovery의 충동일지 구조를 참고해 앱에 맞게 재구성했으며, <b>내용은 이 기기에만 저장</b>됩니다.',
    '    충동은 특정 시간·상황·촉발요인에서 반복될 수 있습니다. 기록을 모아 내 패턴과 나에게 도움이 된 대처를 찾아봅니다.'
)

# 이완: 중복 기능 설명을 사용자 행동 중심으로 수정
repl('<h3>이미 있는 호흡 가이드</h3>', '<h3>호흡 가이드</h3>')
repl(
    '    <p class="muted" style="margin:-3px 0 11px">앱의 충동 대응에는 이미 <b>4초 들이쉬기 · 6초 내쉬기</b> 호흡 가이드가 있습니다. 같은 기능을 하나 더 만들지 않고 기존 도구로 연결합니다.</p>',
    '    <p class="muted" style="margin:-3px 0 11px"><b>4초 들이쉬기 · 6초 내쉬기</b> 호흡 가이드를 바로 사용할 수 있습니다.</p>'
)
repl('>기존 호흡 가이드로 이동</button>', '>호흡 가이드로 이동</button>')
repl(
    '    <p class="tiny" style="margin:8px 0 0">가이드는 조금 느린 속도로 읽습니다. 기기·브라우저에 따라 화면이 꺼지면 음성이 중단될 수 있습니다.</p>',
    '    <p class="tiny" style="margin:8px 0 0">가이드는 조금 느린 속도로 읽습니다. 브라우저에서는 화면이 꺼지면 음성이 중단될 수 있습니다.</p>'
)

# 건강 회복: 버튼이 이미 이동 경로를 설명하므로 중복 안내 제거
repl(
    '<p class="muted" style="margin:-4px 0 11px">규칙적인 식사와 균형 잡힌 식사는 건강한 생활의 기본입니다. 앱에서는 식사 시간을 기존 생활 일정에서 정합니다.</p>',
    '<p class="muted" style="margin:-4px 0 11px">규칙적인 식사와 균형 잡힌 식사는 건강한 생활의 기본입니다.</p>'
)
repl(
    '<p class="muted" style="margin:-4px 0 11px">회복 초기에는 수면 패턴이 달라지고 적응에 시간이 걸릴 수 있습니다. 앱에서는 잠 시간을 생활 일정에서 정하고 몸 기록에서 흐름을 돌아봅니다.</p>',
    '<p class="muted" style="margin:-4px 0 11px">회복 초기에는 수면 패턴이 달라지고 적응에 시간이 걸릴 수 있습니다.</p>'
)
repl(
    '<p class="muted" style="margin:-4px 0 11px">SMART는 법적으로 처방된 정신과·중독 치료 약물과 전문적 치료의 사용을 지지합니다. 앱에서는 복약과 외래를 기존 치료 일정에서 관리합니다.</p>',
    '<p class="muted" style="margin:-4px 0 11px">SMART는 법적으로 처방된 정신과·중독 치료 약물과 전문적 치료의 사용을 지지합니다.</p>'
)
repl(
    "    ['건강 회복 · 생활 돌보기','식사 · 운동 · 수면 · 복약 · 미루기를 기존 기능으로 연결','smart-health','check']",
    "    ['건강 회복 · 생활 돌보기','식사 · 운동 · 수면 · 복약 · 미루기 점검','smart-health','check']"
)

# 습관 편집: Android 메뉴 경로 설명 제거
repl('<p class="tiny" style="margin:7px 0 0">Android 앱에서는 회복도구 → 일정·알림 → 알림 설정에서 예약 상태를 한 번에 확인할 수 있습니다.</p>', '')

# 12단계 작성 개인정보 안내: 내부 시스템 이름 제거
repl(
    '    작성 내용은 <b>이 기기에만 임시저장·보관</b>됩니다. 자원시트·의견서버·마음프로로 자동 전송되지 않습니다.',
    '    작성 내용은 <b>이 기기에 저장</b>되며 자동 전송되지 않습니다.'
)

# 가족 위기 안내: "기존"이라는 내부 참조 제거
repl('대화를 이어가기보다 기존 가족 위기 안내를 먼저 확인하세요.', '대화를 이어가기보다 가족 위기 안내를 먼저 확인하세요.')

# SMART 목표: "기존 습관" 내부 참조 제거
text = text.replace('저장 후 기록 보기에서 기존 습관으로 연결할 수 있습니다.', '저장 후 기록 보기에서 습관으로 연결할 수 있습니다.')

idx.write_text(text, encoding='utf-8')

# Service worker version/cache only; logic unchanged
s = sw.read_text(encoding='utf-8')
if s.count("const APP_VERSION = 'V8.2.39';") != 1:
    raise SystemExit('sw APP_VERSION mismatch')
s = s.replace("const APP_VERSION = 'V8.2.39';", "const APP_VERSION = 'V8.2.40';", 1)
if s.count("const V = 'ohg-v8239-usability-consolidation-2';") != 1:
    raise SystemExit('sw cache key mismatch')
s = s.replace("const V = 'ohg-v8239-usability-consolidation-2';", "const V = 'ohg-v8240-copy-cleanup';", 1)
sw.write_text(s, encoding='utf-8')

# README release note
r = readme.read_text(encoding='utf-8')
head = """# V8.2.40 — 사용자 문구 다이어트\n\n- 사용자에게 기능적 가치가 없는 내부 설계·화면 구현·기존 위치 설명을 제거합니다.\n- 가족도구의 기존 위치 안내문과 가족 자가점검의 모드 설명을 제거합니다.\n- `SMART 전체 도구 더 보기` 버튼을 앱의 강조색으로 분명하게 표시합니다.\n- `내 발자취 > 실천기록`의 `기존 저장방식` 설명은 대체 문구 없이 삭제합니다.\n- SMART 개별 도구는 목적·사용법 중심으로 간결하게 정리하고 반복되는 `앱에 맞게 재구성`, 저장 구현 설명을 걷어냅니다.\n- 임상적 경계, 위기·안전, 진단 아님, 개인정보·자동전송 관련 핵심 안내는 유지합니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, Android 정확알림·부팅 재예약·이완 TTS 로직은 변경하지 않습니다.\n\n"""
if r.startswith('# V8.2.40'):
    raise SystemExit('README already V8.2.40')
readme.write_text(head + r, encoding='utf-8')

print('V8.2.40 copy cleanup patch applied')
