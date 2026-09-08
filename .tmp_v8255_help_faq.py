from pathlib import Path

idx = Path('index.html')
sw = Path('sw.js')
readme = Path('README.md')

s = idx.read_text(encoding='utf-8')
orig = s

# Version bump
old = "const BUILD = 'V8.2.54';"
new = "const BUILD = 'V8.2.55';"
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new, 1)

# FAQ styles
css_old = """  .acc-b{display:none;padding:2px 16px 16px}\n  .acc.on .acc-b{display:block}\n  @media (prefers-reduced-motion:reduce){ .acc-v{transition:none} }"""
css_new = """  .acc-b{display:none;padding:2px 16px 16px}\n  .acc.on .acc-b{display:block}\n\n  /* ── 도움말 · 자주 묻는 질문 ── */\n  .faq-list{display:flex;flex-direction:column;gap:9px}\n  .faq{background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden}\n  .faq summary{list-style:none;display:flex;align-items:center;gap:10px;padding:15px 16px;\n    font-weight:600;line-height:1.45;cursor:pointer;word-break:keep-all}\n  .faq summary::-webkit-details-marker{display:none}\n  .faq summary::after{content:'⌄';margin-left:auto;flex:none;color:var(--faint);font-size:20px;line-height:1;transition:transform .16s ease}\n  .faq[open]{border-color:var(--acc2)}\n  .faq[open] summary{color:var(--acc)}\n  .faq[open] summary::after{transform:rotate(180deg);color:var(--acc)}\n  .faq-a{padding:0 16px 16px;line-height:1.72;word-break:keep-all}\n  .faq-a p{margin:0;color:var(--tx)}\n  .faq-a .tiny{margin-top:7px}\n  .faq-go{margin-top:11px;width:100%}\n  @media (prefers-reduced-motion:reduce){ .acc-v,.faq summary::after{transition:none} }"""
assert s.count(css_old) == 1, s.count(css_old)
s = s.replace(css_old, css_new, 1)

# Add support/help entry before administrator accordion
admin_marker = """  <div class=\"acc\">\n    <button class=\"acc-h\">\n      <span class=\"acc-n\"><b>관리자</b><span>자원 목록 관리 · 앱에 바라는 점 전체보기</span></span>"""
support_block = """  <div class=\"acc\">\n    <button class=\"acc-h\">\n      <span class=\"acc-n\"><b>지원 및 안내</b><span>도움말 · 자주 묻는 질문</span></span>\n      <svg class=\"acc-v\" viewBox=\"0 0 24 24\"><path d=\"M6.5 9.5l5.5 5.5 5.5-5.5\"/></svg>\n    </button>\n    <div class=\"acc-b\">\n      <button class=\"toolcard\" type=\"button\" onclick=\"go('guide')\"><span class=\"ic\" data-ico=\"check\"></span><span class=\"b\"><b>도움말 · 자주 묻는 질문</b><span>설정 · 기록 · 알림 · 회복도구 · 마음프로 사용법</span></span><span class=\"go\">열기</span></button>\n    </div>\n  </div>\n\n""" + admin_marker
assert s.count(admin_marker) == 1, s.count(admin_marker)
s = s.replace(admin_marker, support_block, 1)

# Add static FAQ page after settings page
end_me = """  <div class=\"note w\" style=\"margin-top:16px\">\n    이 앱은 치료를 대신하지 않습니다. 회복을 돕는 도구입니다.\n    필요할 때는 반드시 전문가와 연결되세요.\n  </div>\n  <p class=\"tiny cen\" style=\"margin-top:14px\" id=\"me-ver\"></p>\n</section>"""
faq_page = end_me + """\n\n<!-- ══════════ 도움말 · 자주 묻는 질문 ══════════ -->\n<section class=\"pg\" id=\"p-guide\">\n  <div class=\"sp\" style=\"margin-bottom:11px\"><h1 style=\"margin:0\">도움말</h1><button class=\"tiny\" style=\"color:var(--acc);font-weight:600\" onclick=\"appBack('me')\">← 내 정보 · 설정</button></div>\n  <p class=\"muted\" style=\"margin:0 0 16px\">궁금한 항목을 눌러 짧게 확인할 수 있습니다. 필요한 곳은 바로 열 수 있습니다.</p>\n\n  <h2>시작 · 기록</h2>\n  <div class=\"faq-list\">\n    <details class=\"faq\"><summary>처음에는 무엇부터 하면 되나요?</summary><div class=\"faq-a\"><p>처음 설정에서 역할, 회복 영역, 시작일과 지역을 정한 뒤 홈에서 오늘 할 일과 상태를 확인하면 됩니다. 새 계획이나 연습은 <b>회복도구</b>에서 시작합니다.</p></div></details>\n    <details class=\"faq\"><summary>내 기록은 어디에 저장되나요?</summary><div class=\"faq-a\"><p>감정, 충동, 하루, 몸, 12단계, 회복 실천도구, 자가점검 결과 같은 개인 회복기록은 기본적으로 <b>현재 기기 안</b>에 저장됩니다. 자동으로 다른 사람이나 마음프로에 전달되지 않습니다.</p></div></details>\n    <details class=\"faq\"><summary>지나간 기록은 어디에서 볼 수 있나요?</summary><div class=\"faq-a\"><p><b>나 → 내 발자취</b>에서 감정·충동·하루·몸·실천기록·자가점검·통계를 다시 볼 수 있습니다.</p><button class=\"btn ghost sm faq-go\" type=\"button\" onclick=\"go('rec')\">내 발자취 열기</button></div></details>\n    <details class=\"faq\"><summary>기록을 백업하거나 다른 기기로 옮길 수 있나요?</summary><div class=\"faq-a\"><p><b>나 → 내 정보 · 설정 → 기록 관리</b>에서 기록을 내보내고 다시 불러올 수 있습니다. 앱 삭제나 기기 변경 전에는 먼저 내보내기를 권합니다.</p><button class=\"btn ghost sm faq-go\" type=\"button\" onclick=\"go('me')\">기록 관리 열기</button></div></details>\n    <details class=\"faq\"><summary>앱을 업데이트하거나 다시 설치하면 기록은 어떻게 되나요?</summary><div class=\"faq-a\"><p>기존 앱 위에 업데이트하는 경우에는 같은 앱 데이터가 유지되도록 설계되어 있습니다. 다만 <b>앱 삭제, 앱 데이터 삭제, 기기 초기화</b>를 하면 기기 안 기록이 사라질 수 있으므로 먼저 기록을 내보내세요.</p></div></details>\n  </div>\n\n  <h2>일정 · 알림</h2>\n  <div class=\"faq-list\">\n    <details class=\"faq\"><summary>복약·외래·식사·잠·습관 일정은 어디에서 관리하나요?</summary><div class=\"faq-a\"><p><b>회복도구 → 내 계획 → 일정·알림</b>에서 습관, 생활 일정, 치료 일정을 한 흐름으로 관리합니다.</p><button class=\"btn ghost sm faq-go\" type=\"button\" onclick=\"go('schedule')\">일정·알림 열기</button></div></details>\n    <details class=\"faq\"><summary>화면을 꺼도 알림이 오나요?</summary><div class=\"faq-a\"><p>Android 설치 앱에서는 정확 알림을 사용해 화면이 꺼진 상태에서도 예약 시각에 알림이 오도록 구성되어 있습니다. 처음 사용할 때 알림 권한과 정확 알림 허용 상태를 확인해주세요.</p></div></details>\n    <details class=\"faq\"><summary>알림이 늦거나 오지 않으면 무엇을 확인하나요?</summary><div class=\"faq-a\"><p><b>일정·알림 → 알림 설정</b>에서 Android 알림 권한과 예약 상태를 확인하세요. 기기의 절전·배터리 제한이 강한 경우에는 오늘 한 걸음의 백그라운드 실행 제한도 확인하는 것이 좋습니다.</p></div></details>\n  </div>\n\n  <h2>회복도구</h2>\n  <div class=\"faq-list\">\n    <details class=\"faq\"><summary>12단계 기록은 어디에서 작성하나요?</summary><div class=\"faq-a\"><p><b>회복도구 → 실천하기 → 12단계 점검</b>에서 작성합니다. 저장한 기록은 <b>내 발자취 → 실천기록</b>에서 다시 볼 수 있습니다.</p></div></details>\n    <details class=\"faq\"><summary>회복 실천도구는 어떻게 사용하나요?</summary><div class=\"faq-a\"><p>SMART Recovery의 4-Point 학습 구조를 바탕으로 가치 우선순위 정하기, 의사결정 저울, 충동 다루기, 중독 생각과 거리두기, 상황·생각·감정 돌아보기, 삶의 균형 살펴보기 같은 도구를 필요할 때 골라 사용할 수 있습니다.</p><button class=\"btn ghost sm faq-go\" type=\"button\" onclick=\"go('smart-tools')\">회복 실천도구 열기</button></div></details>\n    <details class=\"faq\"><summary>자가점검은 진단인가요?</summary><div class=\"faq-a\"><p>아닙니다. 자가점검은 현재 상태와 변화를 살펴보기 위한 <b>선별·참고 도구</b>입니다. 결과가 걱정되거나 일상 기능에 어려움이 있다면 전문가와 상담하세요.</p><button class=\"btn ghost sm faq-go\" type=\"button\" onclick=\"go('screening')\">자가점검 열기</button></div></details>\n    <details class=\"faq\"><summary>자가점검 결과는 어디에서 다시 보나요?</summary><div class=\"faq-a\"><p><b>내 발자취 → 자가점검</b>에서 검사별 저장 결과와 이전 기록의 변화 흐름을 확인할 수 있습니다.</p><button class=\"btn ghost sm faq-go\" type=\"button\" onclick=\"go('rec')\">내 발자취 열기</button></div></details>\n    <details class=\"faq\"><summary>가족·보호자 모드는 무엇인가요?</summary><div class=\"faq-a\"><p>당사자가 아니라 가족이나 보호자의 자리에서 사용할 수 있도록 문구와 일부 도구를 바꾸는 모드입니다. <b>나 → 내 정보 · 설정 → 나</b>에서 역할을 변경할 수 있습니다.</p><button class=\"btn ghost sm faq-go\" type=\"button\" onclick=\"go('me')\">역할 설정 열기</button></div></details>\n  </div>\n\n  <h2>마음프로 · 안전</h2>\n  <div class=\"faq-list\">\n    <details class=\"faq\"><summary>마음프로는 어떤 기능인가요?</summary><div class=\"faq-a\"><p>회복학습과 앱 사용법을 안내하고, 사용자가 직접 보낸 문장에 답하는 대화 기능입니다. 치료자나 응급서비스를 대신하지 않으며 위급한 상황의 판단을 맡기는 용도로 사용하지 않습니다.</p><button class=\"btn ghost sm faq-go\" type=\"button\" onclick=\"go('ai')\">마음프로 열기</button></div></details>\n    <details class=\"faq\"><summary>마음프로에 내 회복기록이 자동으로 전송되나요?</summary><div class=\"faq-a\"><p><b>자동으로 전송되지 않습니다.</b> 내 발자취, 자가점검 점수, 12단계·회복 실천도구 기록을 마음프로가 자동 첨부하지 않습니다. 마음프로에서 사용자가 직접 전송한 문장은 답변 생성을 위해 AI 서버로 전송됩니다.</p></div></details>\n    <details class=\"faq\"><summary>마음프로 답변을 음성으로 들을 수 있나요?</summary><div class=\"faq-a\"><p>Android 설치 앱에서는 <b>나 → 내 정보 · 설정 → 앱</b>의 마음프로 답변 자동 읽기를 사용할 수 있습니다. 대화에서 “계속 읽어줘”, “그만 읽어”라고 입력해 현재 대화의 읽기 상태를 바꿀 수도 있습니다.</p></div></details>\n    <details class=\"faq\"><summary>지금 위험하거나 스스로를 다치게 할 것 같으면 어떻게 하나요?</summary><div class=\"faq-a\"><p>앱의 <b>지금 위험해요</b>를 열어 즉시 도움 연결을 확인하세요. 자신이나 다른 사람의 생명·신체에 즉각적인 위험이 있다면 앱에 머물지 말고 <b>112 또는 119</b>, 가까운 응급의료기관 등 즉시 연결 가능한 도움을 이용하세요.</p><button class=\"btn danger sm faq-go\" type=\"button\" onclick=\"go('panic')\">지금 위험해요 열기</button></div></details>\n  </div>\n\n  <div class=\"note\" style=\"margin-top:18px\">도움말에 없는 기능은 다음 단계의 <b>사용설명서</b>에서 메뉴별로 더 자세히 안내합니다.</div>\n</section>"""
assert s.count(end_me) == 1, s.count(end_me)
s = s.replace(end_me, faq_page, 1)

# Guards: storage and native behavior identifiers must remain unchanged
assert "const KEY = 'ohg.v1';" in s
assert "const DATA_SCHEMA = 6;" in s
assert "setExactAndAllowWhileIdle" not in s  # native Android code is not embedded here
assert s.count("id=\"p-guide\"") == 1
assert s.count("<summary>") >= 16
idx.write_text(s, encoding='utf-8')

# Service worker version/cache only
w = sw.read_text(encoding='utf-8')
assert w.count("const APP_VERSION = 'V8.2.54';") == 1
assert w.count("const V = 'ohg-v8254-smart-copy-completion';") == 1
w = w.replace("const APP_VERSION = 'V8.2.54';", "const APP_VERSION = 'V8.2.55';", 1)
w = w.replace("const V = 'ohg-v8254-smart-copy-completion';", "const V = 'ohg-v8255-help-faq';", 1)
sw.write_text(w, encoding='utf-8')

# README release note
r = readme.read_text(encoding='utf-8')
head = """## V8.2.55 — 도움말 · 자주 묻는 질문\n- `내 정보 · 설정`에 `지원 및 안내` 묶음을 추가하고 `도움말 · 자주 묻는 질문`으로 진입할 수 있게 했습니다.\n- FAQ는 시작·기록, 일정·알림, 회복도구, 마음프로·안전으로 나누고 실제 V8.2.54 메뉴 경로에 맞춘 짧은 답변과 필요한 바로가기를 제공합니다.\n- 개인 회복기록은 기본적으로 기기 내부 저장이며, 마음프로에는 저장된 기록이 자동 전송되지 않고 사용자가 직접 전송한 문장만 AI 답변 생성을 위해 서버로 전송된다는 점을 도움말에 명확히 안내합니다.\n- 사용설명서와 개인정보처리방침은 별도 다음 단계로 작성하며 이번 버전에서는 본문을 추가하지 않습니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, 기존 기록형식, Android 정확알림·화면 OFF 알림·부팅 재예약·복약/외래/생활/습관 알림·네이티브 TTS·이완 TTS는 변경하지 않습니다.\n\n"""
assert r.startswith("## V8.2.54")
readme.write_text(head + r, encoding='utf-8')

print('V8.2.55 help FAQ patch applied')
