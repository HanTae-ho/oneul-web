from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,n=1,label='replace'):
    global s
    c=s.count(old)
    if c!=n:
        raise SystemExit(f'{label}: expected {n}, found {c}')
    s=s.replace(old,new,n)

def sub(pattern,repl,n=1,label='regex'):
    global s
    s2,c=re.subn(pattern,repl,s,count=n,flags=re.S)
    if c!=n:
        raise SystemExit(f'{label}: expected {n}, found {c}')
    s=s2

# Version only; storage schema/key are intentionally unchanged.
rep("const BUILD = 'V8.2.50';","const BUILD = 'V8.2.51';",label='BUILD')

# My Trail descriptions now expose self-assessment as its own history category.
rep('감정 · 하루 · 몸 · 실천기록과 회복 흐름을 한곳에서 돌아봅니다.',
    '감정 · 하루 · 몸 · 실천기록 · 자가점검과 회복 흐름을 한곳에서 돌아봅니다.',label='trail intro')
rep('<span>감정 · 충동 · 하루 · 몸 · 실천기록 · 통계</span>',
    '<span>감정 · 충동 · 하루 · 몸 · 실천기록 · 자가점검 · 통계</span>',label='my trail summary')

# Direct result access from the self-assessment list.
old='''  <div class="note w" style="margin-bottom:13px">자가점검은 진단이 아닙니다. 점수는 현재 상태를 살펴보고 상담이나 전문 평가가 필요한지 확인하는 참고자료입니다. 결과는 이 기기에만 저장됩니다.</div>\n  <div id="screening-list"></div>'''
new='''  <div class="note w" style="margin-bottom:13px">자가점검은 진단이 아닙니다. 점수는 현재 상태를 살펴보고 상담이나 전문 평가가 필요한지 확인하는 참고자료입니다. 결과는 이 기기에만 저장됩니다.</div>\n  <button class="btn sec" style="margin-bottom:13px" onclick="recTab='screen';go('rec')">내 점검 결과 보기</button>\n  <div id="screening-list"></div>'''
rep(old,new,label='screening history shortcut')

# Direct history shortcuts from the two practice hubs.
old='''  <p class="muted" style="margin:-2px 0 14px">12단계 내용을 읽은 뒤 실제 경험을 적어보는 공간입니다. 작성 내용은 이 기기에만 저장됩니다.</p>\n  <div class="learnlist" id="workbook-list"></div>'''
new='''  <p class="muted" style="margin:-2px 0 14px">12단계 내용을 읽은 뒤 실제 경험을 적어보는 공간입니다. 작성 내용은 이 기기에만 저장됩니다.</p>\n  <button class="btn sec sm" style="margin-bottom:12px" onclick="recTab='work';recPracticeFilter='step';go('rec')">내 12단계 기록 보기</button>\n  <div class="learnlist" id="workbook-list"></div>'''
rep(old,new,label='workbook history shortcut')

sub(r'''(<section class="pg" id="p-smart-tools">.*?<div class="note" style="margin-bottom:12px">\s*SMART Recovery의 4-Point는 순서대로 통과하는 단계가 아닙니다\. <b>지금 필요한 영역</b>을 골라 도구를 사용해보세요\.\s*</div>)''',
    r'''\1\n  <button class="btn sec sm" style="margin-bottom:12px" onclick="recTab='work';recPracticeFilter='smart';go('rec')">내 SMART 기록 보기</button>''',label='smart history shortcut')

# My Trail: self-assessment is a dedicated tab in both self and family modes.
old="""    ? [{v:'mood',l:'감정'},{v:'day',l:'하루'},{v:'body',l:'몸'},{v:'work',l:'실천기록'},{v:'stat',l:'통계'}]\n    : [{v:'mood',l:'감정'},{v:'urge',l:'충동'},{v:'day',l:'하루'},{v:'body',l:'몸'},\n       {v:'relapse',l:'다시 시작'},{v:'work',l:'실천기록'},{v:'stat',l:'통계'}];"""
new="""    ? [{v:'mood',l:'감정'},{v:'day',l:'하루'},{v:'body',l:'몸'},{v:'work',l:'실천기록'},{v:'screen',l:'자가점검'},{v:'stat',l:'통계'}]\n    : [{v:'mood',l:'감정'},{v:'urge',l:'충동'},{v:'day',l:'하루'},{v:'body',l:'몸'},\n       {v:'relapse',l:'다시 시작'},{v:'work',l:'실천기록'},{v:'screen',l:'자가점검'},{v:'stat',l:'통계'}];"""
rep(old,new,label='trail tabs')

rep("  if(recTab === 'work')    body.appendChild(recPractice());\n  if(recTab === 'stat')    body.appendChild(recStat());",
    "  if(recTab === 'work')    body.appendChild(recPractice());\n  if(recTab === 'screen')  body.appendChild(recScreening());\n  if(recTab === 'stat')    body.appendChild(recStat());",label='trail body')

marker='''}\n\n/* ── 하루 (자기 전 마무리) ──'''
insert='''}\n\nfunction recScreening(){\n  const w=el('div');\n  const stats=screeningStats();\n  if(stats) w.appendChild(stats);\n  else w.appendChild(emptyBox('아직 저장한 자가점검 결과가 없습니다.<br>회복도구 → 자가점검에서 지금 상태를 확인해보세요.'));\n  const b=el('button','btn sec','자가점검 하러 가기');\n  b.type='button'; b.style.marginTop='4px'; b.onclick=()=>go('screening');\n  w.appendChild(b);\n  return w;\n}\n\n/* ── 하루 (자기 전 마무리) ──'''
rep(marker,insert,label='recScreening function')

# A completed assessment now lands on the dedicated assessment-history tab.
rep("$('#screen-stat-go').onclick=()=>{ recTab='stat'; screenRun=null; go('rec'); };",
    "$('#screen-stat-go').onclick=()=>{ recTab='screen'; screenRun=null; go('rec'); };",label='result trail route')

# MindPro guide: keep the emergency warning verbatim, shorten everything below it.
old='''      <p class="muted" style="margin:0 0 8px">\n        타이머·도움글·모임·센터·병원·알림·앱 메뉴처럼 <b>앱이 직접 처리할 수 있는 요청은 기기에서 먼저 처리</b>합니다. 일반 대화가 필요할 때만 사용자가 직접 적은 문장을 AI 서버로 보냅니다.\n      </p>\n      <p class="tiny" style="margin:0">회복 시작일·충동·재발·HALT·복약·기분·자가점검 결과 같은 개인 회복기록은 자동 전송하지 않습니다. 대화 내용은 이 기기에 저장됩니다.</p>'''
new='''      <p class="muted" style="margin:0 0 6px">앱 기능은 가능한 경우 기기에서 바로 처리합니다. 일반 대화에 필요한 <b>내가 직접 적은 문장만</b> AI로 보냅니다.</p>\n      <p class="tiny" style="margin:0">개인 회복기록은 자동 전송하지 않습니다. Android 앱에서는 설정 또는 “음성으로”·“그만 읽어”로 답변 읽기를 조절할 수 있습니다.</p>'''
rep(old,new,label='mindpro guide summary')

# Single-word voice commands must stay local and turn on current-chat reading.
needle="""  if(/그만읽|읽지마|읽지말|읽는거멈|음성멈|음성꺼|소리꺼|말하지마|그만말/.test(x)) return 'off';\n  if(/계속읽|자동.*읽|이제부터.*읽|답변.*읽|소리내.*읽/.test(x) || /^(읽어줘|읽어주세요)$/.test(x)) return 'on';"""
repl="""  if(/그만읽|읽지마|읽지말|읽는거멈|음성멈|음성꺼|소리꺼|말하지마|그만말/.test(x)) return 'off';\n  if(/^(음성으로|말로|소리로)$/.test(x)) return 'on';\n  if(/계속읽|자동.*읽|이제부터.*읽|답변.*읽|소리내.*읽/.test(x) || /^(읽어줘|읽어주세요)$/.test(x)) return 'on';"""
rep(needle,repl,label='single voice command')

p.write_text(s,encoding='utf-8')

# Service worker cache/version.
sw=Path('sw.js').read_text(encoding='utf-8')
if sw.count("const APP_VERSION = 'V8.2.50';")!=1: raise SystemExit('sw APP_VERSION mismatch')
sw=sw.replace("const APP_VERSION = 'V8.2.50';","const APP_VERSION = 'V8.2.51';",1)
if sw.count("const V = 'ohg-v8250-mindpro-native-voice';")!=1: raise SystemExit('sw cache mismatch')
sw=sw.replace("const V = 'ohg-v8250-mindpro-native-voice';","const V = 'ohg-v8251-trail-screening-mindpro';",1)
Path('sw.js').write_text(sw,encoding='utf-8')

# Release note.
r=Path('README.md')
rd=r.read_text(encoding='utf-8')
head='''## V8.2.51 — 자가점검 기록 접근 · 실천기록 바로가기 · 마음프로 간결화\n- `내 발자취`에 `자가점검` 독립 탭을 추가하고 기존 검사별 변화 카드를 이 범주에서도 바로 확인할 수 있게 했습니다.\n- `회복도구 → 자가점검`에 `내 점검 결과 보기`, 12단계·SMART 실천도구에 각각 해당 실천기록 바로가기를 추가했습니다.\n- 자가점검 결과 화면의 `내 발자취에서 변화 보기`는 새 `자가점검` 탭으로 바로 이동합니다.\n- 마음프로 응급·안전 경고는 유지하고 그 아래 개인정보·앱기능·음성 설명은 짧게 정리했습니다.\n- `음성으로`·`말로`·`소리로` 단독 입력도 AI 서버로 보내지 않고 현재 대화 자동 읽기 ON 명령으로 처리합니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, Android 네이티브 TTS·정확알림·부팅 재예약·기존 저장형식은 변경하지 않습니다.\n\n'''
r.write_text(head+rd,encoding='utf-8')
