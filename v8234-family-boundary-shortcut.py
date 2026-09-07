from pathlib import Path

idx=Path('index.html'); sw=Path('sw.js'); readme=Path('README.md')

def once(text, old, new, label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    return text.replace(old,new,1)

s=idx.read_text(encoding='utf-8')
s=once(s,"const BUILD = 'V8.2.33';","const BUILD = 'V8.2.34';",'BUILD')

# 1) Family self-care top shortcut: keep the original article entry too.
old='''  /* 위기 갈래는 읽을거리보다 전화가 먼저 나와야 합니다. 이것만 늘 위에 붙여둡니다. */\n  $('#fam-top').innerHTML = (famTab === 'sos')\n    ? '<div class="card">' +\n      '<h3 style="margin-top:0">지금 바로 걸 수 있는 곳</h3>' +\n      '<a class="btn danger" href="tel:119">119 · 몸이 위급할 때</a>' +\n      '<div style="height:9px"></div>' +\n      '<a class="btn sec" href="tel:109">109 · 죽고 싶다는 말이 나올 때</a>' +\n      '<div style="height:9px"></div>' +\n      '<a class="btn sec" href="tel:1577-0199">1577-0199 · 정신건강 상담전화</a>' +\n      '<div style="height:9px"></div>' +\n      '<a class="btn ghost" href="tel:112">112 · 폭력이 있을 때</a>' +\n      '<p class="tiny" style="margin:12px 0 0">가족이 대신 걸어도 됩니다. ' +\n      '"제가 당사자가 아닌데요" 라고 하셔도 상담해 줍니다.</p></div>'\n    : '';'''
new='''  /* 위기 갈래는 전화가 먼저, 나를 돌보기 갈래는 자주 쓰는 경계 실천도구를 먼저 둡니다. */\n  $('#fam-top').innerHTML = (famTab === 'sos')\n    ? '<div class="card">' +\n      '<h3 style="margin-top:0">지금 바로 걸 수 있는 곳</h3>' +\n      '<a class="btn danger" href="tel:119">119 · 몸이 위급할 때</a>' +\n      '<div style="height:9px"></div>' +\n      '<a class="btn sec" href="tel:109">109 · 죽고 싶다는 말이 나올 때</a>' +\n      '<div style="height:9px"></div>' +\n      '<a class="btn sec" href="tel:1577-0199">1577-0199 · 정신건강 상담전화</a>' +\n      '<div style="height:9px"></div>' +\n      '<a class="btn ghost" href="tel:112">112 · 폭력이 있을 때</a>' +\n      '<p class="tiny" style="margin:12px 0 0">가족이 대신 걸어도 됩니다. ' +\n      '"제가 당사자가 아닌데요" 라고 하셔도 상담해 줍니다.</p></div>'\n    : (famTab === 'self')\n      ? '<div class="card tight">' +\n        '<h3 style="margin:0 0 5px">바로 해보기</h3>' +\n        '<p class="muted" style="margin:0 0 10px">상대를 바꾸는 규칙이 아니라, 내가 지킬 기준과 행동을 정리합니다.</p>' +\n        '<button class="btn sec sm" id="fam-boundary-shortcut">내 경계 정리</button></div>'\n      : '';\n  const fbs=$('#fam-boundary-shortcut'); if(fbs) fbs.onclick=()=>go('family-boundary');'''
s=once(s,old,new,'family self-care shortcut')

# 2) Common route-aware back label for every SMART tool opened from Family Guide.
# This fixes ABC/CBA/Balance Pie/Health without changing self-mode or SMART-hub navigation.
s=once(s,"""  const labels={\n    'tools':'회복도구',""","""  const labels={\n    'tools':'회복도구',\n    'fam':'가족 안내',""",'family back label')
s=once(s,"""  const fallbacks={\n    'learn-topic':'learn-topic', 'capsule':'capsule', 'smart-tools':'smart-tools',""","""  const fallbacks={\n    'fam':'fam', 'learn-topic':'learn-topic', 'capsule':'capsule', 'smart-tools':'smart-tools',""",'family back fallback')
idx.write_text(s,encoding='utf-8')

w=sw.read_text(encoding='utf-8')
w=once(w,"const APP_VERSION = 'V8.2.33';","const APP_VERSION = 'V8.2.34';",'SW version')
w=once(w,"const V = 'ohg-v8233-family-boundary';","const V = 'ohg-v8234-family-navigation';",'SW cache')
sw.write_text(w,encoding='utf-8')

r=readme.read_text(encoding='utf-8')
intro='''# V8.2.34 — 가족 안내 접근성과 되돌아가기 정합성\n\n- 가족모드 `나를 돌보기` 화면 상단에 `내 경계 정리` 바로가기를 추가했습니다.\n- 기존 경계 안내 글 안의 `내 경계 정리하기` 버튼도 그대로 유지합니다.\n- 가족 안내에서 SMART 도구로 들어간 경우 공통 상단 되돌아가기를 `← 가족 안내`로 표시합니다.\n  - CBA\n  - ABC (`내 생각과 반응 살펴보기`)\n  - 밸런스 파이\n  - 건강 회복 · 생활 돌보기\n- SMART 실천도구/학습에서 직접 진입한 경우의 기존 되돌아가기는 변경하지 않습니다.\n- 별도 가족 메인메뉴나 새 저장구조는 추가하지 않습니다.\n- 기존 `family-boundary / family`, `DATA_SCHEMA=6`, 가족 충동·재발 비기록, Local-first를 유지합니다.\n- Android 이완 TTS·화면 OFF 재생·속도선택·정확알림 엔진은 변경하지 않습니다.\n\n'''
readme.write_text(intro+r,encoding='utf-8')
print('V8.2.34 family navigation patch applied')
