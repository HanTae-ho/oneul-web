from pathlib import Path

root=Path('.')
idx=root/'index.html'
s=idx.read_text(encoding='utf-8')

def repl(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

repl("const BUILD = 'V8.2.51';","const BUILD = 'V8.2.52';",'BUILD')

old_tools='''  <div class="toolsec">\n    <h2>자가점검</h2>\n    <div class="checkmini">\n      <button class="minitool wide" id="tool-check"><span class="ic" data-ico="check"></span><b>자가점검</b><span>내 상태를 스스로 확인하기</span></button>\n    </div>\n  </div>'''
new_tools='''  <div class="toolsec">\n    <h2>자가점검</h2>\n    <div class="checkmini">\n      <button class="minitool wide" id="tool-check"><span class="ic" data-ico="check"></span><b>자가점검</b><span>내 상태를 스스로 확인하기</span></button>\n      <button class="minitool wide" id="tool-check-view" onclick="recTab='screen';go('rec')"><span class="ic" data-ico="check"></span><b>점검 보기</b><span>지난 점검 결과와 변화 확인</span></button>\n    </div>\n  </div>'''
repl(old_tools,new_tools,'tools selfcheck pair')

old_screen='''  <div class="note w" style="margin-bottom:13px">자가점검은 진단이 아닙니다. 점수는 현재 상태를 살펴보고 상담이나 전문 평가가 필요한지 확인하는 참고자료입니다. 결과는 이 기기에만 저장됩니다.</div>\n  <button class="btn sec" style="margin-bottom:13px" onclick="recTab='screen';go('rec')">내 점검 결과 보기</button>\n  <div id="screening-list"></div>'''
new_screen='''  <div class="note w" style="margin-bottom:13px">자가점검은 진단이 아닙니다. 점수는 현재 상태를 살펴보고 상담이나 전문 평가가 필요한지 확인하는 참고자료입니다. 결과는 이 기기에만 저장됩니다.</div>\n  <div id="screening-list"></div>'''
repl(old_screen,new_screen,'remove duplicate result button')

repl('<span><b>마음프로 안내</b><small>안전 · 개인정보 · 앱 기능 · 음성</small></span>','<span><b>마음프로 안내</b><small>안전 · 개인정보 · 앱 기능</small></span>','AI guide subtitle')

old_guide='''      <p class="muted" style="margin:0 0 6px">앱 기능은 가능한 경우 기기에서 바로 처리합니다. 일반 대화에 필요한 <b>내가 직접 적은 문장만</b> AI로 보냅니다.</p>\n      <p class="tiny" style="margin:0">개인 회복기록은 자동 전송하지 않습니다. Android 앱에서는 설정 또는 “음성으로”·“그만 읽어”로 답변 읽기를 조절할 수 있습니다.</p>\n      <p class="tiny hide" id="ai-guide-voice" style="margin:8px 0 0"></p>'''
new_guide='''      <p class="muted" style="margin:0">앱 기능은 기기에서 먼저 처리하고, <b>내가 직접 적은 일반 대화만</b> AI로 보냅니다. 개인 회복기록은 자동 전송하지 않습니다.</p>'''
repl(old_guide,new_guide,'AI guide compact copy')

idx.write_text(s,encoding='utf-8')

sw=root/'sw.js'
w=sw.read_text(encoding='utf-8')
for old,new,label in [
    ("const APP_VERSION = 'V8.2.51';","const APP_VERSION = 'V8.2.52';",'sw version'),
    ("const V = 'ohg-v8251-trail-screening-mindpro';","const V = 'ohg-v8252-selfcheck-card-guide';",'sw cache'),
]:
    n=w.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 match, got {n}')
    w=w.replace(old,new,1)
sw.write_text(w,encoding='utf-8')

readme=root/'README.md'
r=readme.read_text(encoding='utf-8')
head='''## V8.2.52 — 자가점검 결과 바로보기 · 마음프로 안내 축약\n- `회복도구 → 자가점검` 영역을 두 카드로 정리해 `자가점검` 오른쪽에 `점검 보기`를 배치하고, 누르면 `내 발자취 → 자가점검`으로 바로 이동합니다.\n- 자가점검 화면 안에 있던 중복 `내 점검 결과 보기` 큰 버튼은 제거합니다. `내 발자취 → 자가점검` 탭과 검사별 변화 기록은 그대로 유지합니다.\n- 마음프로 안내는 응급·안전 경고를 그대로 유지하고, 그 아래 설명을 일반 대화 전송·개인 회복기록 비전송을 설명하는 1~2줄로 축약합니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, 기존 검사·통계 저장형식, Android 네이티브 TTS·정확알림 엔진은 변경하지 않습니다.\n\n'''
if r.startswith('## V8.2.52'):
    raise SystemExit('README already V8.2.52')
readme.write_text(head+r,encoding='utf-8')
