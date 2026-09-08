from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_rec = '''  <p class="muted" style="margin:0 0 14px">회복하면서 되찾은 것과 감정 · 하루 · 몸 · 실천기록 · 자가점검의 흐름을 한곳에서 돌아봅니다.</p>\n  <div id="rec-reclaim"></div>\n  <div class="opts" id="rec-tab" style="margin-bottom:14px"></div>'''
new_rec = '''  <p class="muted" style="margin:0 0 14px">감정 · 하루 · 몸 · 실천기록 · 자가점검과 회복 흐름을 한곳에서 돌아봅니다.</p>\n  <div class="opts" id="rec-tab" style="margin-bottom:14px"></div>'''
assert old_rec in s, '내 발자취 reclaim 원본을 찾지 못했습니다.'
s = s.replace(old_rec, new_rec, 1)

old_my = '''  <p class="muted" style="margin:0 0 14px">내 기록과 설정을 확인하고, 앱 안내와 의견 보내기를 이용합니다.</p>\n  <button class="toolcard" id="my-trail">'''
new_my = '''  <p class="muted" style="margin:0 0 14px">내 기록과 설정을 확인하고, 앱 안내와 의견 보내기를 이용합니다.</p>\n  <div id="rec-reclaim"></div>\n  <button class="toolcard" id="my-trail">'''
assert old_my in s, '나 화면 삽입 위치를 찾지 못했습니다.'
s = s.replace(old_my, new_my, 1)

assert "if(p === 'my'){ drawFeedbackStatus(); drawAdmin(); }" in s
s = s.replace("if(p === 'my'){ drawFeedbackStatus(); drawAdmin(); }", "if(p === 'my'){ drawReclaim(); drawFeedbackStatus(); drawAdmin(); }", 1)

assert '''function drawRec(){\n  drawReclaim();''' in s
s = s.replace('''function drawRec(){\n  drawReclaim();''', '''function drawRec(){''', 1)

assert "save(); closeModal(); drawRec(); toast('기준을 저장했습니다.');" in s
s = s.replace("save(); closeModal(); drawRec(); toast('기준을 저장했습니다.');", "save(); closeModal(); drawReclaim(); toast('기준을 저장했습니다.');", 1)

assert "const BUILD = 'V8.2.64';" in s
s = s.replace("const BUILD = 'V8.2.64';", "const BUILD = 'V8.2.65';", 1)
p.write_text(s, encoding='utf-8')

p = Path('sw.js')
sw = p.read_text(encoding='utf-8')
assert "const APP_VERSION = 'V8.2.64';" in sw
assert "const V = 'ohg-v8264-reclaimed-summary';" in sw
sw = sw.replace("const APP_VERSION = 'V8.2.64';", "const APP_VERSION = 'V8.2.65';", 1)
sw = sw.replace("const V = 'ohg-v8264-reclaimed-summary';", "const V = 'ohg-v8265-reclaim-to-my';", 1)
p.write_text(sw, encoding='utf-8')

p = Path('privacy.html')
pr = p.read_text(encoding='utf-8')
# 개인정보처리방침 내용은 그대로 두고 앱 기준 버전 표기만 현재 릴리즈에 맞춥니다.
assert pr.count('V8.2.63') >= 2
pr = pr.replace('V8.2.63', 'V8.2.65')
p.write_text(pr, encoding='utf-8')

p = Path('README.md')
rd = p.read_text(encoding='utf-8')
head = '''## V8.2.65 — 내가 되찾은 것 · 나 화면으로 이동\n- `내가 되찾은 것` 요약을 `내 발자취` 내부에서 빼고 `나` 화면의 `내 발자취` 카드 바로 위로 이동했습니다.\n- 회복일 · 되찾은 시간 · 지킨 비용 · 실천한 습관의 계산식, 기준 설정, 도박 비용 계산 차단, 직접 SVG 아이콘은 그대로 유지합니다.\n- `내 발자취`는 감정 · 충동 · 하루 · 몸 · 다시 시작 · 실천기록 · 자가점검 · 통계 기록을 돌아보는 공간으로 유지합니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, 관리자·마음프로·자원시트·Android 알림/TTS 엔진은 변경하지 않았습니다.\n\n'''
assert not rd.startswith('## V8.2.65')
p.write_text(head + rd, encoding='utf-8')
