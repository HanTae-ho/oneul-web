from pathlib import Path

idx=Path('index.html')
sw=Path('sw.js')
readme=Path('README.md')

s=idx.read_text(encoding='utf-8')

pairs=[
("const BUILD = 'V8.2.56';", "const BUILD = 'V8.2.57';"),
('<span class="acc-n"><b>지원 및 안내</b><span>도움말 · 자주 묻는 질문 · 사용설명서</span></span>', '<span class="acc-n"><b>지원 및 안내</b><span>도움말 · 사용설명서 · 개인정보처리방침</span></span>'),
('''      <button class="toolcard" type="button" style="margin-top:9px" onclick="go('manual')"><span class="ic" data-ico="sprout"></span><span class="b"><b>사용설명서</b><span>처음 시작부터 기록 · 알림 · 안전한 사용까지 메뉴별 안내</span></span><span class="go">열기</span></button>''', '''      <button class="toolcard" type="button" style="margin-top:9px" onclick="go('manual')"><span class="ic" data-ico="sprout"></span><span class="b"><b>사용설명서</b><span>처음 시작부터 기록 · 알림 · 안전한 사용까지 메뉴별 안내</span></span><span class="go">열기</span></button>\n      <a class="toolcard" style="margin-top:9px" href="./privacy.html"><span class="ic" data-ico="check"></span><span class="b"><b>개인정보처리방침</b><span>기기 저장 · 위치 · 마음프로 · 외부 서비스 데이터 처리 안내</span></span><span class="go">열기</span></a>'''),
('''   기록은 이 기기 안에만 저장됩니다. 서버로 가지 않습니다.''', '''   개인 회복기록은 기본적으로 이 기기 안에 저장되며 서버로 자동 전송하지 않습니다.'''),
('''     ★ 개인 회복기록은 자동 전송하지 않고, 사용자가 직접 보낸 문장만 AI 서버로 전송합니다. */''', '''     ★ 개인 회복기록은 자동 전송하지 않고, 일반 AI 대화에서 현재 문장과 최근 일반 대화 문맥만 AI 서버로 전송합니다. */''')
]
for old,new in pairs:
    n=s.count(old)
    assert n==1,(old[:80],n)
    s=s.replace(old,new,1)
idx.write_text(s,encoding='utf-8')

w=sw.read_text(encoding='utf-8')
for old,new in [
("const APP_VERSION = 'V8.2.56';","const APP_VERSION = 'V8.2.57';"),
("const V = 'ohg-v8256-user-manual';","const V = 'ohg-v8257-privacy-policy';"),
("'./qa-data.js', './learning-data.js', './screening-data.js', './workbook-data.js', './manifest.json',","'./qa-data.js', './learning-data.js', './screening-data.js', './workbook-data.js', './privacy.html', './manifest.json',")
]:
    n=w.count(old); assert n==1,(old,n); w=w.replace(old,new,1)
sw.write_text(w,encoding='utf-8')

r=readme.read_text(encoding='utf-8')
entry='''## V8.2.57 — 개인정보처리방침 · 데이터 흐름 공개\n- V8.2.56 기준 실제 데이터 흐름을 다시 점검하고 `privacy.html` 공개 개인정보처리방침을 추가했습니다.\n- `내 정보 · 설정 → 지원 및 안내`에서 도움말·사용설명서와 함께 개인정보처리방침을 바로 열 수 있습니다.\n- 개인 회복기록은 `ohg.v1`의 기기 내부 저장을 유지하고, 현재 위치는 사용자가 선택할 때 좌표를 시·도 수준으로만 변환하며 원래 GPS 좌표는 저장·AI 전송하지 않음을 명시했습니다.\n- 앱에 바라는 점은 사용자가 작성한 의견+앱 버전만 전송하며, 마음프로 일반 AI 대화는 익명형 clientId·현재 메시지·주제·앱 버전·최근 일반 AI 대화 최대 8개를 Apps Script 중계 후 OpenAI API로 보냅니다. 저장된 회복기록·자가점검·12단계·회복 실천도구 기록은 자동 첨부하지 않습니다.\n- 자원목록은 Google Apps Script에서 공개 자료를 GET으로 받으며 회복기록을 전송하지 않습니다. 광고·행동분석 추적 SDK는 사용하지 않습니다.\n- 개인정보보호위원회 2026.4 처리방침 작성지침과 Google Play User Data/AI 연동 정책을 참고해 기기 저장, 외부 처리, 보유·삭제, Android 권한, 문의 경로를 구분했습니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, 기존 기록형식, Android 정확알림·화면 OFF 알림·부팅 재예약·복약/외래/생활/습관 알림·네이티브 TTS·이완 TTS는 변경하지 않습니다.\n\n'''
assert not r.startswith('## V8.2.57')
readme.write_text(entry+r,encoding='utf-8')
