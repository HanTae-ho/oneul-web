from pathlib import Path
import re


def must_replace(text, old, new, count=1, label='replace'):
    found = text.count(old)
    if found != count:
        raise SystemExit(f'{label}: expected {count}, found {found}')
    return text.replace(old, new, count)


def cut_top_acc(text, marker):
    idx = text.find(marker)
    if idx < 0:
        raise SystemExit(f'marker not found: {marker}')
    start = text.rfind('<div class="acc">', 0, idx)
    if start < 0:
        raise SystemExit(f'acc start not found: {marker}')
    depth = 0
    end = None
    for m in re.finditer(r'<div\b[^>]*>|</div>', text[start:], re.I):
        tag = m.group(0).lower()
        if tag.startswith('<div'):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = start + m.end()
                break
    if end is None:
        raise SystemExit(f'acc end not found: {marker}')
    block = text[start:end]
    return text[:start] + text[end:], block

# ── index.html ──
p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = must_replace(s, "const BUILD = 'V8.2.61';", "const BUILD = 'V8.2.62';", label='BUILD')

s, feedback = cut_top_acc(s, '<b>앱에 바라는 점</b>')
s, support = cut_top_acc(s, '<b>지원 및 안내</b>')
s, admin = cut_top_acc(s, '<b>관리자</b><span>자원 목록 관리 · 앱에 바라는 점 전체보기</span>')

# 관리자 카드 앞의 오래된 소스 주석도 현재 위치에 맞게 제거합니다.
s = re.sub(r'\n\s*<!-- 목록을 고치는 사람\(팀장님\)만 들어갑니다\..*?구글 계정입니다\. -->\s*', '\n', s, count=1, flags=re.S)

old_intro = '<p class="muted" style="margin:0 0 14px">내 기록을 돌아보거나, 내 정보와 앱 설정을 관리합니다.</p>'
new_intro = '<p class="muted" style="margin:0 0 14px">내 기록과 설정을 확인하고, 앱 안내와 의견 보내기를 이용합니다.</p>'
s = must_replace(s, old_intro, new_intro, label='my intro')

my_start = s.find('<section class="pg" id="p-my">')
if my_start < 0:
    raise SystemExit('p-my not found')
my_end = s.find('</section>', my_start)
if my_end < 0:
    raise SystemExit('p-my end not found')
insert = '\n  <div style="height:12px"></div>\n' + feedback + '\n\n' + support + '\n\n  <!-- 관리자 기능과 접근 방식은 그대로 두고 위치만 나 화면으로 옮깁니다. -->\n' + admin + '\n'
s = s[:my_end] + insert + s[my_end:]

# 내 정보·설정과 나 화면의 아코디언을 같은 방식으로 동작시킵니다.
s = must_replace(s, "$$('#p-me .acc-h').forEach(h => {", "$$('#p-me .acc-h, #p-my .acc-h').forEach(h => {", label='accordion bind')
s = must_replace(s, "$$('#p-me .acc').forEach(x => x.classList.remove('on'));", "(h.closest('.pg') || document).querySelectorAll('.acc').forEach(x => x.classList.remove('on'));", label='accordion scope')

# 지원·안내 화면은 이제 나에서 들어오므로 뒤로가기도 나로 맞춥니다.
old_back = "onclick=\"appBack('me')\">← 내 정보 · 설정</button>"
if s.count(old_back) != 2:
    raise SystemExit(f'guide/manual back expected 2, found {s.count(old_back)}')
s = s.replace(old_back, "onclick=\"appBack('my')\">← 나</button>")

s = s.replace('지원 및 안내 → 도움말 · 자주 묻는 질문', '나 → 지원 및 안내 → 도움말 · 자주 묻는 질문')

s = must_replace(
    s,
    '<details class="faq"><summary>12. 내 정보 · 설정 — 설정, 백업, 앱 관리</summary><div class="faq-a">',
    '<details class="faq"><summary>12. 나 · 내 정보 · 설정 — 기록, 설정, 안내</summary><div class="faq-a">',
    label='manual item 12 title'
)
s = must_replace(
    s,
    '<p style="margin-top:8px"><b>앱에 바라는 점</b>은 불편한 점이나 제안을 보내는 기능입니다. 작성 내용과 앱 버전만 전송되며 민감한 개인정보는 직접 적지 않는 것이 좋습니다.</p>',
    '<p style="margin-top:8px"><b>앱에 바라는 점·지원 및 안내·관리자</b>는 <b>나</b> 화면에서 바로 이용합니다. 관리자 기능의 기존 접근 방식은 그대로 유지됩니다.</p>',
    label='manual moved items'
)
# 위 항목 안의 버튼 하나만 나 화면으로 연결합니다.
item12 = s.find('<details class="faq"><summary>12. 나 · 내 정보 · 설정 — 기록, 설정, 안내</summary>')
item13 = s.find('<details class="faq"><summary>13. Android 설치 앱', item12)
if item12 < 0 or item13 < 0:
    raise SystemExit('manual item 12/13 bounds not found')
chunk = s[item12:item13]
old_btn = '<button class="btn ghost sm faq-go" type="button" onclick="go(\'me\')">내 정보 · 설정 열기</button>'
if chunk.count(old_btn) != 1:
    raise SystemExit(f'manual item12 button expected 1, found {chunk.count(old_btn)}')
chunk = chunk.replace(old_btn, '<button class="btn ghost sm faq-go" type="button" onclick="go(\'my\')">나 열기</button>', 1)
s = s[:item12] + chunk + s[item13:]

p.write_text(s, encoding='utf-8')

# ── privacy.html ──
p = Path('privacy.html')
s = p.read_text(encoding='utf-8')
s = must_replace(
    s,
    '<a class="back" href="./index.html">← 오늘 한 걸음으로 돌아가기</a>',
    '<a class="back" href="./index.html" onclick="if(history.length>1){event.preventDefault();history.back();}">← 이전 화면으로</a>',
    label='privacy back'
)
s = s.replace('V8.2.61', 'V8.2.62')
p.write_text(s, encoding='utf-8')

# ── sw.js ──
p = Path('sw.js')
s = p.read_text(encoding='utf-8')
s = must_replace(s, "const APP_VERSION = 'V8.2.61';", "const APP_VERSION = 'V8.2.62';", label='sw app version')
s = must_replace(s, "const V = 'ohg-v8261-onboarding-ai';", "const V = 'ohg-v8262-me-menu-back';", label='sw cache')
p.write_text(s, encoding='utf-8')

# ── README.md ──
p = Path('README.md')
s = p.read_text(encoding='utf-8')
if '## V8.2.62 — 나 메뉴 정리 · 개인정보처리방침 이전 화면 복귀' in s:
    raise SystemExit('README V8.2.62 already exists')
entry = '''## V8.2.62 — 나 메뉴 정리 · 개인정보처리방침 이전 화면 복귀
- `앱에 바라는 점`, `지원 및 안내`, `관리자`를 `내 정보 · 설정`에서 `나` 화면으로 이동했습니다. 기능과 관리자 접근 방식은 변경하지 않았습니다.
- `내 정보 · 설정`에는 `나`, `앱`, `추천하기`, `기록 관리`처럼 실제 정보·설정 성격의 항목만 남겼습니다.
- 도움말·사용설명서의 뒤로가기는 새 위치에 맞춰 `나`로 연결하고 관련 안내 문구도 갱신했습니다.
- 개인정보처리방침 상단의 `← 오늘 한 걸음으로 돌아가기`를 `← 이전 화면으로`로 바꾸고, 방문 이력이 있으면 실제 이전 화면으로 돌아가며 없으면 앱 시작화면으로 연결됩니다.
- `DATA_SCHEMA=6`, `ohg.v1`, 마음프로 Local-first/AI 전송 구조, 자원시트, 회복기록, Android 정확알림·화면 OFF 알림·부팅 재예약·TTS는 변경하지 않습니다.

'''
p.write_text(entry + s, encoding='utf-8')

# ── 최종 정적 검증 ──
idx = Path('index.html').read_text(encoding='utf-8')
my = idx[idx.index('<section class="pg" id="p-my">'):idx.index('</section>', idx.index('<section class="pg" id="p-my">'))]
me = idx[idx.index('<section class="pg" id="p-me">'):idx.index('</section>', idx.index('<section class="pg" id="p-me">'))]
for label in ('앱에 바라는 점', '지원 및 안내', '관리자'):
    if label not in my:
        raise SystemExit(f'{label} missing from p-my')
    if label in me:
        raise SystemExit(f'{label} still present in p-me')
for label in ('<b>나</b>', '<b>앱</b>', '<b>추천하기</b>', '<b>기록 관리</b>'):
    if label not in me:
        raise SystemExit(f'settings item missing: {label}')
for iid in ('me-feedback-send','me-admin','me-admin-m'):
    if idx.count(f'id="{iid}"') != 1:
        raise SystemExit(f'id {iid} count != 1')
if "const KEY = 'ohg.v1';" not in idx or 'const DATA_SCHEMA = 6;' not in idx:
    raise SystemExit('storage/schema changed')
priv = Path('privacy.html').read_text(encoding='utf-8')
if priv.count('<details class="pacc">') != 6:
    raise SystemExit('privacy accordion count changed')
if '← 이전 화면으로' not in priv or 'history.back()' not in priv:
    raise SystemExit('privacy back behavior missing')
print('V8.2.62 patch static verification: PASS')
