from pathlib import Path


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    return text.replace(old, new, 1)

idxp = Path('index.html')
idx = idxp.read_text(encoding='utf-8')
idx = replace_once(idx, "const BUILD = 'V8.2.65';", "const BUILD = 'V8.2.66';", 'BUILD')
idx = replace_once(idx,
    "card('sprout','실천한 습관',habits+'회','내 습관에서 직접 체크한 횟수','habit',false)+",
    "card('sprout','회복 실천',habits+'회','내가 실천하고 기록한 회복 행동','habit',false)+",
    'reclaim label')
idx = replace_once(idx,
    "도박 회복영역에서는 손실복구 사고를 자극하지 않도록 금액 누적 계산을 제공하지 않습니다. 회복일·시간·실천한 습관은 그대로 볼 수 있습니다.",
    "도박 회복영역에서는 손실복구 사고를 자극하지 않도록 금액 누적 계산을 제공하지 않습니다. 회복일·시간·회복 실천은 그대로 볼 수 있습니다.",
    'gambling note')

old_help = '''    <details class="faq"><summary>지나간 기록은 어디에서 볼 수 있나요?</summary><div class="faq-a"><p><b>나 → 내 발자취</b>에서 감정·충동·하루·몸·실천기록·자가점검·통계를 다시 볼 수 있습니다.</p><button class="btn ghost sm faq-go" type="button" onclick="go('rec')">내 발자취 열기</button></div></details>'''
new_help = old_help + '''\n    <details class="faq"><summary>내가 되찾은 것은 어디에서 보나요?</summary><div class="faq-a"><p>당사자 모드에서는 <b>나</b> 화면 상단의 <b>내가 되찾은 것</b>에서 회복일·되찾은 시간·지킨 비용·회복 실천을 한눈에 볼 수 있습니다. 되찾은 시간과 지킨 비용은 <b>기준 설정</b>에서 원할 때만 켜며, 도박 회복영역은 손실복구 사고를 자극하지 않도록 금액 누적 계산을 제공하지 않습니다.</p><button class="btn ghost sm faq-go" type="button" onclick="go('my')">나 열기</button></div></details>'''
idx = replace_once(idx, old_help, new_help, 'help reclaim faq')

idx = replace_once(idx,
    '''      <p style="margin-top:8px"><b>⑤ 기록 돌아보기</b> — 나 → 내 발자취에서 저장한 기록과 변화 흐름을 확인합니다.</p>''',
    '''      <p style="margin-top:8px"><b>⑤ 변화와 기록 돌아보기</b> — 당사자 모드에서는 나 화면 상단의 <b>내가 되찾은 것</b>에서 회복일·되찾은 시간·지킨 비용·회복 실천을 확인하고, <b>나 → 내 발자취</b>에서 저장한 기록과 변화 흐름을 확인합니다.</p>''',
    'manual first steps')
idx = replace_once(idx,
    '''      <p>하단 메뉴는 <b>홈 · 회복도구 · 헬프 · 마음프로</b>를 중심으로 사용합니다. 홈 오른쪽 위의 사람 모양 버튼을 누르면 <b>나</b>로 들어가 내 발자취와 내 정보·설정을 관리할 수 있습니다.</p>\n      <p style="margin-top:8px">관리자 기능은 일반 사용 메뉴와 분리되어 있으며, 관리자 상태일 때만 별도 메뉴가 표시됩니다.</p>''',
    '''      <p>하단 메뉴는 <b>홈 · 회복도구 · 헬프 · 마음프로</b>를 중심으로 사용합니다. 홈 오른쪽 위의 사람 모양 버튼을 누르면 <b>나</b>로 들어갑니다.</p>\n      <p style="margin-top:8px">당사자 모드의 <b>나</b> 화면에는 위에서부터 <b>내가 되찾은 것 → 내 발자취 → 내 정보 · 설정 → 앱에 바라는 점 → 지원 및 안내 → 관리자</b>가 배치됩니다. 가족·보호자 모드에서는 당사자의 회복성과를 대신 계산하지 않도록 <b>내가 되찾은 것</b>은 표시하지 않습니다.</p>\n      <p style="margin-top:8px">관리자는 일반 사용 기능과 분리되어 있으며 기존 관리자 접근 방식은 그대로 유지됩니다.</p>''',
    'manual menu structure')

old_sec12 = '''    <details class="faq"><summary>12. 나 · 내 정보 · 설정 — 기록, 설정, 안내</summary><div class="faq-a">\n      <p><b>나</b>에서는 역할, 회복 영역·시작일·목표·지역 등 기본 정보를 관리합니다.</p>\n      <p style="margin-top:8px"><b>앱</b>에서는 자원 목록 새로 받기, 화면 밝기, 마음프로 AI 사용 여부, 앱 새로고침·설치와 Android 마음프로 음성 설정을 관리합니다.</p>\n      <p style="margin-top:8px"><b>기록 관리</b>에서는 JSON 파일로 내보내기·불러오기와 전체 지우기를 할 수 있습니다. 다른 기기로 옮기거나 앱을 삭제하기 전에는 내보내기를 먼저 권합니다.</p>\n      <p style="margin-top:8px"><b>앱에 바라는 점·지원 및 안내·관리자</b>는 <b>나</b> 화면에서 바로 이용합니다. 관리자 기능의 기존 접근 방식은 그대로 유지됩니다.</p>\n      <button class="btn ghost sm faq-go" type="button" onclick="go('my')">나 열기</button>\n    </div></details>'''
new_sec12 = '''    <details class="faq"><summary>12. 나 — 회복 요약 · 기록 · 설정 · 안내</summary><div class="faq-a">\n      <p>당사자 모드의 <b>나</b> 화면 상단에는 <b>내가 되찾은 것</b>이 표시됩니다. 회복일은 설정한 회복 시작일에서 계산하고, <b>회복 실천</b>은 내 습관에서 직접 체크해 기록한 회복 행동 횟수를 보여줍니다.</p>\n      <p style="margin-top:8px"><b>되찾은 시간</b>과 <b>지킨 비용</b>은 선택 기능입니다. <b>기준 설정</b>에서 회복 전 하루 평균 시간·실제 사용비용을 입력한 경우에만 추정치를 표시합니다. 도박 회복영역은 손실복구 사고를 자극하지 않도록 금액 누적 계산을 제공하지 않습니다.</p>\n      <p style="margin-top:8px"><b>내 발자취</b>에서는 감정·충동·하루·몸·실천기록·자가점검·통계를 다시 보고, <b>내 정보 · 설정</b>에서는 역할·회복영역·화면·앱·추천하기·기록 관리를 관리합니다.</p>\n      <p style="margin-top:8px"><b>앱에 바라는 점 · 지원 및 안내 · 관리자</b>는 <b>내 정보 · 설정</b> 안이 아니라 <b>나</b> 화면에서 바로 이용합니다. 관리자 기능의 기존 접근 방식은 그대로 유지됩니다.</p>\n      <button class="btn ghost sm faq-go" type="button" onclick="go('my')">나 열기</button>\n    </div></details>'''
idx = replace_once(idx, old_sec12, new_sec12, 'manual section 12')
idxp.write_text(idx, encoding='utf-8')

swp = Path('sw.js')
sw = swp.read_text(encoding='utf-8')
sw = replace_once(sw, "const APP_VERSION = 'V8.2.65';", "const APP_VERSION = 'V8.2.66';", 'sw version')
sw = replace_once(sw, "const V = 'ohg-v8265-reclaim-to-my';", "const V = 'ohg-v8266-manual-reclaim-label';", 'sw cache')
swp.write_text(sw, encoding='utf-8')

pp = Path('privacy.html')
pr = pp.read_text(encoding='utf-8')
if 'V8.2.65' not in pr:
    raise SystemExit('privacy version missing')
pr = pr.replace('V8.2.65', 'V8.2.66')
pp.write_text(pr, encoding='utf-8')

rp = Path('README.md')
r = rp.read_text(encoding='utf-8')
head = '''## V8.2.66 — 사용설명서 현행화 · 회복 실천 명칭\n- 현재 `나` 메뉴 구조에 맞춰 도움말·사용설명서의 메뉴 경로와 설명을 현행화했습니다.\n- `나` 화면의 `내가 되찾은 것` 사용법과 회복일·되찾은 시간·지킨 비용·회복 실천의 의미를 안내합니다.\n- `실천한 습관` 명칭을 `회복 실천`으로 바꾸고 설명을 `내가 실천하고 기록한 회복 행동`으로 정리했습니다.\n- 도박 회복영역의 금액 누적 계산 차단, 계산식, 직접 SVG 아이콘, `DATA_SCHEMA=6`, `ohg.v1`은 그대로 유지합니다.\n- 관리자·마음프로·자원시트·Android 알림/TTS 엔진은 변경하지 않았습니다.\n\n'''
if r.startswith('## V8.2.66'):
    raise SystemExit('README already patched')
rp.write_text(head + r, encoding='utf-8')
