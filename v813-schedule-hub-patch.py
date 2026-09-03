from pathlib import Path


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    return text.replace(old, new, 1)

p = Path('index.html')
s = p.read_text(encoding='utf-8')

s = replace_once(s,
'''<!-- ══════════ 치료관리 V8.1 ══════════ -->
<section class="pg" id="p-treatment">
  <div class="sp" style="margin-bottom:8px">
    <h1 style="margin:0">치료관리</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('me')">← 돌아가기</button>
  </div>
  <p class="muted" style="margin:0 0 14px">
    복약과 외래 일정을 한곳에서 관리합니다. 약 이름이나 진단명은 묻지 않습니다. 기록은 이 기기에만 저장됩니다.
  </p>
  <div id="treat-master"></div>
  <div id="treat-body"></div>
</section>''',
'''<!-- ══════════ 일정·알림 · 치료 일정 V8.1.3 ══════════ -->
<section class="pg" id="p-treatment">
  <div class="sp" style="margin-bottom:8px">
    <h1 style="margin:0">치료 일정</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('me')">← 일정·알림</button>
  </div>
  <p class="muted" style="margin:0 0 14px">
    복약과 외래 일정을 관리합니다. 약 이름이나 진단명은 묻지 않습니다. 기록은 이 기기에만 저장됩니다.
  </p>
  <div id="treat-master"></div>
  <div id="treat-body"></div>
</section>''', 'treatment page')

s = replace_once(s,
'''  <!-- 위험시간·식사·잠은 일상 챙기기입니다. 복약·외래는 V8.1부터 별도 치료관리로 분리합니다. -->
  <div class="acc">
    <button class="acc-h">
      <span class="acc-n"><b>챙기기</b><span id="acc-care-s">위험한 시간대 · 식사 · 잠 · 알림</span></span>''',
'''  <!-- V8.1.3: 생활·치료·알림의 진입점을 하나로 합칩니다. 내부 저장·예약 엔진은 그대로 유지합니다. -->
  <div class="acc">
    <button class="acc-h">
      <span class="acc-n"><b>일정·알림</b><span id="acc-care-s">생활 일정 · 치료 일정 · 알림</span></span>''', 'schedule hub heading')

s = replace_once(s,
'''      <div class="me-self">
        <h3>복약 · 외래</h3>
        <p class="muted" style="margin:-4px 0 11px">
          복약 시간, 처방일수와 다음 외래일은 별도의 치료관리에서 설정합니다.
        </p>
        <button class="btn sec sm" onclick="go('treatment')">치료관리 열기</button>
        <div class="sep"></div>
      </div>''',
'''      <div class="me-self">
        <h3>치료 일정</h3>
        <p class="muted" style="margin:-4px 0 11px">
          복약 시간, 처방일수와 다음 외래일을 관리합니다.
        </p>
        <button class="btn sec sm" onclick="go('treatment')">복약·외래 일정 설정</button>
        <div class="sep"></div>
      </div>''', 'treatment link inside hub')

s = replace_once(s,
'''      <div class="sep"></div>
      <h3>알림</h3>
      <p class="muted" style="margin:-4px 0 11px">
        위험한 시간대 · 복약 · 식사 · 잘 시간에 알려드립니다.
      </p>''',
'''      <div class="sep"></div>
      <h3>알림 설정</h3>
      <p class="muted" style="margin:-4px 0 11px">
        위험한 시간대 · 복약 · 식사 · 잘 시간 · 외래 일정을 한곳에서 알려드립니다.
      </p>''', 'notification heading')

s = replace_once(s,
'''  <div class="acc me-self">
    <button class="acc-h">
      <span class="acc-n"><b>치료관리</b><span>복약 · 처방일수 · 외래 일정 · 치료 알림</span></span>
      <svg class="acc-v" viewBox="0 0 24 24"><path d="M6.5 9.5l5.5 5.5 5.5-5.5"/></svg>
    </button>
    <div class="acc-b">
      <p class="muted" style="margin:0 0 11px">
        필요한 경우에만 켜서 사용합니다. 끄더라도 기존 복약·외래 설정과 기록은 지우지 않습니다.
      </p>
      <button class="btn sec sm" onclick="go('treatment')">치료관리 설정</button>
    </div>
  </div>

''', '', 'duplicate treatment accordion')

s = replace_once(s,
'''  $('#acc-care-s').textContent = fam
    ? '식사 · 잠 · 알림'
    : '위험한 시간대 · 식사 · 잠 · 알림';''',
'''  $('#acc-care-s').textContent = fam
    ? '생활 일정 · 알림'
    : '생활 일정 · 치료 일정 · 알림';''', 'dynamic schedule hub subtitle')

s = replace_once(s,
'''    aiAdd('assistant','내정보에서는 회복 영역·시작일·지역·챙기기 설정과 앱 설정, 기록 내보내기 등을 관리할 수 있어요.', true);''',
'''    aiAdd('assistant','내정보에서는 회복 영역·시작일·지역·일정·알림 설정과 앱 설정, 기록 내보내기 등을 관리할 수 있어요.', true);''', 'AI me help text')

s = replace_once(s,
'''    '<div class="sp"><div><b>'+esc(d===0?'오늘 외래':'치료관리')+'</b><div class="muted" style="margin-top:3px">'+esc(label)+'</div></div>'+''',
'''    '<div class="sp"><div><b>'+esc(d===0?'오늘 외래':'치료 일정')+'</b><div class="muted" style="margin-top:3px">'+esc(label)+'</div></div>'+''', 'home treatment card label')

s = replace_once(s,
'''    master.innerHTML='<div class="note w">치료관리는 현재 본인 회복모드에서만 사용합니다. 가족의 복약·진료를 대신 관리하는 기능은 별도로 설계합니다.</div>';''',
'''    master.innerHTML='<div class="note w">치료 일정은 현재 본인 회복모드에서만 사용합니다. 가족의 복약·진료를 대신 관리하는 기능은 별도로 설계합니다.</div>';''', 'family treatment wording')

s = replace_once(s,
'''  master.innerHTML='<div class="card"><h3>치료관리 사용</h3><p class="muted" style="margin:-4px 0 11px">필요한 경우에만 켜세요. 끄더라도 기존 설정과 기록은 삭제하지 않습니다.</p><div class="opts" id="treat-on"></div></div>';''',
'''  master.innerHTML='<div class="card"><h3>치료 일정 사용</h3><p class="muted" style="margin:-4px 0 11px">필요한 경우에만 켜세요. 끄더라도 기존 설정과 기록은 삭제하지 않습니다.</p><div class="opts" id="treat-on"></div></div>';''', 'treatment master wording')

s = replace_once(s,
'''    body.innerHTML='<div class="note"><b>치료관리를 사용하지 않습니다.</b><br><span class="muted">기존 복약·외래 설정과 기록은 보존됩니다.</span>' +''',
'''    body.innerHTML='<div class="note"><b>치료 일정을 사용하지 않습니다.</b><br><span class="muted">기존 복약·외래 설정과 기록은 보존됩니다.</span>' +''', 'treatment off wording')

s = replace_once(s, "const BUILD = 'V8.1.2';", "const BUILD = 'V8.1.3';", 'BUILD')

# Guardrails: only presentation/labels and web build marker change here.
if '<b>치료관리</b><span>복약 · 처방일수 · 외래 일정 · 치료 알림</span>' in s:
    raise SystemExit('duplicate treatment accordion still present')
if '<b>일정·알림</b>' not in s or '복약·외래 일정 설정' not in s:
    raise SystemExit('schedule hub UI missing')
if "const BUILD = 'V8.1.3';" not in s:
    raise SystemExit('BUILD not updated')
p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
w = replace_once(w, "const APP_VERSION = 'V8.1.2';", "const APP_VERSION = 'V8.1.3';", 'sw APP_VERSION')
w = replace_once(w, "const V = 'ohg-v812-treatment';", "const V = 'ohg-v813-schedulehub';", 'sw cache key')
sw.write_text(w, encoding='utf-8')

readme = Path('README.md')
r = readme.read_text(encoding='utf-8')
if not r.startswith('# V8.1.3 — 일정·알림 허브'):
    note = '''# V8.1.3 — 일정·알림 허브\n\n- `내 정보`의 `챙기기`와 별도 `치료관리` 진입을 `일정·알림` 한 묶음으로 통합했습니다.\n- 생활 일정(위험시간·식사·잠), 치료 일정(복약·외래), 알림 설정을 같은 흐름에서 관리합니다.\n- 기존 `S.treat`, 복약·식사·잠 데이터와 Android V8.1.2 네이티브 예약 엔진은 변경하지 않습니다.\n- 향후 AA·GA·NA 등 모임 일정도 같은 `일정·알림` 허브에 붙일 수 있는 메뉴 원칙을 확정했습니다.\n\n'''
    r = note + r
readme.write_text(r, encoding='utf-8')

print('V8.1.3 schedule hub patch PASS')
