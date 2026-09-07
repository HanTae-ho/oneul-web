from pathlib import Path
import re

INDEX=Path('index.html')
s=INDEX.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'missing pattern ({n}/{count}): {old[:100]!r}')
    s=s.replace(old,new,count)

def sub(pattern,repl,count=1):
    global s
    s2,n=re.subn(pattern,repl,s,count=count,flags=re.S)
    if n != count:
        raise SystemExit(f'regex count {n}/{count}: {pattern[:100]}')
    s=s2

# V8.2.39 version + home role cleanup
rep("const BUILD = 'V8.2.38';", "const BUILD = 'V8.2.39';")
rep('<button id="top-me" aria-label="내 정보" title="내 정보">','<button id="top-me" aria-label="나" title="나">')
rep("$('#top-me').onclick = () => go('me');", "$('#top-me').onclick = () => go('my');")
rep('  <button class="btn sec" id="go-ai-home">마음프로와 이야기하기</button>\n  <div style="height:10px"></div>\n','')
rep("$('#go-ai-home').onclick = () => openAI('home');\n",'')
rep('<button class="tiny" style="color:var(--acc);font-weight:600" onclick="go(\'home\')">닫기</button>', '<button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack(\'home\')">← 돌아가기</button>')

# Recovery tools: four clear jobs — plan / learn / practice / check
TOOLS='''<!-- ══════════ 회복도구 V8.2.39 · 계획/배움/실천/점검 ══════════ -->
<section class="pg" id="p-tools">
  <h1>회복도구</h1>

  <div class="toolsec">
    <h2>내 계획</h2>
    <button class="toolcard" id="tool-schedule">
      <span class="ic" data-ico="cal"></span>
      <span class="b"><b>일정 · 알림</b><span>습관 · 생활 · 치료 일정을 한곳에서 관리</span></span><span class="go">열기</span>
    </button>
  </div>

  <div class="toolsec">
    <h2>배우기</h2>
    <div class="learnmini">
      <button class="minitool" id="tool-learn"><span class="ic" data-ico="sprout"></span><b>회복학습</b><span>회복을 더 잘 이해하기</span></button>
      <button class="minitool" id="tool-qa"><span class="ic" data-ico="speak"></span><b>중독 Q&A</b><span id="tool-qa-s">궁금한 내용을 질문하고 답변 보기</span></button>
      <button class="minitool" id="tool-listen"><span class="ic" data-ico="wave"></span><b>듣는 글</b><span>마음에 도움이 되는 이야기</span></button>
    </div>
  </div>

  <div class="toolsec">
    <h2>실천하기</h2>
    <button class="toolcard hide" id="tool-family-tools">
      <span class="ic" data-ico="family"></span><span class="b"><b>가족을 위한 도구</b><span>경계 · 대화 · 대응계획과 내 삶을 돌보는 연습</span></span><span class="go">열기</span>
    </button>
    <button class="toolcard" id="tool-workbook" style="margin-top:9px">
      <span class="ic" data-ico="check"></span><span class="b"><b>12단계 점검</b><span>1·4·8·9·10·11·12단계 기록</span></span><span class="go">열기</span>
    </button>
    <button class="toolcard" id="tool-smart-tools" style="margin-top:9px">
      <span class="ic" data-ico="check"></span><span class="b"><b>SMART 실천도구</b><span id="tool-smart-tools-s">4개 영역에서 지금 필요한 도구만 펼쳐보기</span></span><span class="go">열기</span>
    </button>
    <button class="toolcard" id="tool-urge-diary" style="margin-top:9px">
      <span class="ic" data-ico="wave"></span><span class="b"><b>충동일기</b><span id="tool-urge-diary-s">언제·무엇 때문에 힘들었는지 돌아보기</span></span><span class="go">열기</span>
    </button>
    <button class="toolcard" id="tool-capsule" style="margin-top:9px">
      <span class="ic" data-ico="speak"></span><span class="b"><b>미래의 나에게</b><span id="tool-capsule-s">회복을 시작한 마음을 남겨두기</span></span><span class="go">열기</span>
    </button>
  </div>

  <div class="toolsec">
    <h2>자가점검</h2>
    <div class="checkmini">
      <button class="minitool wide" id="tool-check"><span class="ic" data-ico="check"></span><b>자가점검</b><span>내 상태를 스스로 확인하기</span></button>
    </div>
  </div>
</section>

'''
sub(r'<!-- ══════════ 회복도구 V8\.1\.4 ══════════ -->\s*<section class="pg" id="p-tools">.*?</section>\s*(?=<!-- ══════════ 충동일기 V8\.2\.2)',TOOLS)

# Schedule becomes the one management hub; habit storage itself is unchanged
rep('<p class="muted" style="margin:0 0 14px">생활과 치료 일정을 나누어 정하고, 알림은 한곳에서 관리합니다.</p>', '<p class="muted" style="margin:0 0 14px">습관과 생활·치료 일정을 한곳에서 정하고, 알림까지 같은 흐름에서 관리합니다.</p>')
rep('''  <div class="schedulecards">\n    <button class="schedulecard" id="schedule-life">''','''  <div class="schedulecards">\n    <button class="schedulecard" id="schedule-habit">\n      <span class="ic" data-ico="sprout"></span>\n      <span class="b"><b>습관</b><span>추천 습관 · 내 습관 · 오늘 실천</span></span><span class="go">›</span>\n    </button>\n    <button class="schedulecard" id="schedule-life">''')
rep("onclick=\"appBack('tools')\">← 회복도구</button>\n  </div>\n  <p class=\"muted\" style=\"margin:0 0 14px\">작은 실천을 정하고 오늘 했는지만 체크합니다.", "onclick=\"appBack('schedule')\">← 일정·알림</button>\n  </div>\n  <p class=\"muted\" style=\"margin:0 0 14px\">작은 실천을 정하고 오늘 했는지만 체크합니다.")

# Family mode: curated family tools first, generic SMART only as secondary entry
rep('  <div class="note" style="margin-top:14px">가족 12단계 점검, 가족 모임, 긴급 도움은 각각 기존 <b>내 발자취 · 모임 · 헬프</b> 위치에서 그대로 사용합니다.</div>', '  <div class="note" style="margin-top:14px">가족 12단계 점검, 가족 모임, 긴급 도움은 각각 기존 <b>내 발자취 · 모임 · 헬프</b> 위치에서 그대로 사용합니다.</div>\n  <button class="btn ghost" id="family-smart-all" style="margin-top:9px">SMART 전체 도구 더 보기</button>')
rep('<button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack(\'tools\')">← 회복도구</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    SMART Recovery는', '<button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back data-back-default="tools" data-back-label="회복도구" onclick="appBack(\'tools\')">← 회복도구</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    SMART Recovery는')

# Personal hub: records and settings become peers, rather than records buried inside settings
MY='''<!-- ══════════ 나 · 개인 허브 V8.2.39 ══════════ -->
<section class="pg" id="p-my">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">나</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('home')">← 홈</button>
  </div>
  <p class="muted" style="margin:0 0 14px">내 기록을 돌아보거나, 내 정보와 앱 설정을 관리합니다.</p>
  <button class="toolcard" id="my-trail"><span class="ic" data-ico="check"></span><span class="b"><b>내 발자취</b><span>감정 · 충동 · 하루 · 몸 · 실천기록 · 통계</span></span><span class="go">열기</span></button>
  <button class="toolcard" id="my-settings" style="margin-top:9px"><span class="ic" data-ico="sprout"></span><span class="b"><b>내 정보 · 설정</b><span>역할 · 회복영역 · 화면 · 앱 · 기록 관리</span></span><span class="go">열기</span></button>
</section>

'''
rep('<!-- ══════════ 내 정보 ══════════ -->', MY+'<!-- ══════════ 내 정보 ══════════ -->')
rep('<section class="pg" id="p-me">\n  <h1>내 정보</h1>', '<section class="pg" id="p-me">\n  <div class="sp" style="margin-bottom:11px"><h1 style="margin:0">내 정보 · 설정</h1><button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack(\'my\')">← 나</button></div>')
rep('<span class="acc-n"><b>내 발자취</b><span>감정 · 충동 · 하루 · 몸 · 다시 시작 · 통계 · 기록 관리</span></span>', '<span class="acc-n"><b>기록 관리</b><span>내보내기 · 불러오기 · 전체 지우기</span></span>')
rep('      <p class="muted" style="margin:0 0 11px">지금까지의 회복 과정을 한곳에서 돌아봅니다.</p>\n      <button class="btn sec sm" id="me-trail-open">발자취 보기</button>\n      <div class="sep"></div>\n      <h3>기록 관리</h3>\n','      <h3>백업 · 복원</h3>\n')
rep("$('#me-trail-open').onclick = () => go('rec');", "$('#my-trail').onclick = () => go('rec');\n$('#my-settings').onclick = () => go('me');")

# Trail back path and unified practice tab
rep("onclick=\"appBack('me')\">← 내정보</button>", "onclick=\"appBack('my')\">← 나</button>")
rep('감정 · 충동 · 하루 · 몸 · 다시 시작 · 12단계 검토 · 통계를 돌아봅니다.', '감정 · 하루 · 몸 · 실천기록과 회복 흐름을 한곳에서 돌아봅니다.')
rep("{v:'work',l:'12단계 점검'}", "{v:'work',l:'실천기록'}")
rep("{v:'work',l:'12단계 검토'}", "{v:'work',l:'실천기록'}")
rep("if(recTab === 'work')    body.appendChild(recWorkbook());", "if(recTab === 'work')    body.appendChild(recPractice());")

PRACTICE=r'''function recPractice(){
  const w=el('div');
  w.appendChild(recWorkbook());
  const role=famMode()?'family':'self';
  const rows=(S.smartWorks||[]).filter(r=>r && (r.role||'self')===role)
    .slice().sort((a,b)=>Number(b.updatedAt||b.t||0)-Number(a.updatedAt||a.t||0));
  const labels={
    'family-boundary':'내 경계 정리','family-conversation':'대화 준비','family-return-plan':'다시 사용했을 때 내 대응계획',
    'importance-confidence':'중요성 · 자신감','hov':'가치의 계층 HOV','change-plan':'변화 계획','three-questions':'나의 3가지 질문',
    'cba':'비용-편익 분석 CBA','deads':'DEADS · 충동 대처','disarm':'DISARM','abc':'ABC 문제 해결','dibs':'DIBS · 생각 반박',
    'thinking-styles':'사고방식 점검','problem-solving':'문제 해결 · 5단계','balance-pie':'삶의 균형','vaci':'VACI','goal':'SMART 목표'
  };
  const pages={
    'family-boundary':'family-boundary','family-conversation':'family-conversation','family-return-plan':'family-return-plan',
    'importance-confidence':'smart-importance-confidence','hov':'smart-hov','change-plan':'smart-change-plan','three-questions':'smart-three-questions',
    'cba':'smart-cba','deads':'smart-deads','disarm':'smart-disarm','abc':'smart-abc','dibs':'smart-dibs','thinking-styles':'smart-thinking-styles',
    'problem-solving':'smart-problem-solving','balance-pie':'smart-balance-pie','vaci':'smart-vaci','goal':'smart-goal'
  };
  const c=el('div','card');
  c.appendChild(el('h3','',famMode()?'가족 실천 기록':'SMART 실천 기록'));
  if(!rows.length){ c.appendChild(el('p','muted','아직 저장된 실천 기록이 없습니다. 도구에서 작성하면 여기에 함께 모입니다.')); }
  else{
    c.appendChild(el('p','muted','기존 저장방식은 그대로 두고 최근 기록부터 한곳에서 보여줍니다. 기록을 누르면 해당 도구의 저장목록으로 이동합니다.'));
    rows.slice(0,30).forEach(r=>{
      const tool=String(r.tool||''), meta=labels[tool]||tool||'실천 기록';
      const d=new Date(Number(r.updatedAt||r.t||Date.now()));
      let ds=''; try{ds=d.toLocaleDateString('ko-KR',{year:'numeric',month:'short',day:'numeric'});}catch(_){ds=d.toLocaleDateString();}
      const b=el('button','toolcard','<span class="ic" data-ico="check"></span><span class="b"><b>'+esc(meta)+'</b><span>'+esc(ds)+'</span></span><span class="go">보기</span>');
      b.type='button'; b.onclick=()=>go(pages[tool]||'smart-tools'); c.appendChild(b);
    });
    if(rows.length>30) c.appendChild(el('p','tiny','최근 30건을 표시합니다. 각 도구 안의 기존 기록은 그대로 유지됩니다.'));
  }
  w.appendChild(c); return w;
}

'''
rep('function recWorkbook(){', PRACTICE+'function recWorkbook(){')

# Event and family visibility cleanup after removing the separate habit card
rep("  const habits=habitList(), ht=habitToday(), hd=ht.filter(h=>habitDoneOn(h,today())).length;\n  const hs=$('#tool-habit-s'); if(hs) hs.textContent=habits.length ? ('진행 '+habits.filter(h=>!habitEnded(h,today())).length+'개 · 오늘 '+hd+'/'+ht.length+'개') : '추천 습관과 내 습관 관리';\n",'')
rep("  const ft=$('#tool-family-tools'); if(ft) ft.classList.toggle('hide', !famMode());", "  const ft=$('#tool-family-tools'); if(ft) ft.classList.toggle('hide', !famMode());\n  const st=$('#tool-smart-tools'); if(st) st.classList.toggle('hide', famMode());")
rep("$('#tool-habit').onclick = () => go('habit');\n",'')
rep("$('#schedule-life').onclick = () => go('life-schedule');", "$('#schedule-habit').onclick = () => go('habit');\n$('#schedule-life').onclick = () => go('life-schedule');")
rep("$('#tool-family-tools').onclick = () => go('family-tools');", "$('#tool-family-tools').onclick = () => go('family-tools');\n$('#family-smart-all').onclick = () => go('smart-tools');")

# Safety invariants
checks=[
    "const DATA_SCHEMA = 6;", "const KEY = 'ohg.v1';", "const BUILD = 'V8.2.39';",
    'id="p-my"','id="schedule-habit"','<h2>내 계획</h2>','<h2>배우기</h2>','<h2>실천하기</h2>','<h2>자가점검</h2>',
    'function recPractice()','SMART 전체 도구 더 보기'
]
for x in checks:
    if x not in s: raise SystemExit('post-check missing: '+x)
if 'id="go-ai-home"' in s: raise SystemExit('home AI duplicate still exists')
if 'id="tool-habit"' in s: raise SystemExit('separate habit entry still exists')
INDEX.write_text(s,encoding='utf-8')

# Service worker version only; notification engine is untouched
sw=Path('sw.js').read_text(encoding='utf-8')
sw=sw.replace("const APP_VERSION = 'V8.2.38';", "const APP_VERSION = 'V8.2.39';",1)
sw=sw.replace("const V = 'ohg-v8238-usability-consolidation';", "const V = 'ohg-v8239-usability-consolidation-2';",1)
Path('sw.js').write_text(sw,encoding='utf-8')

# Release note
rd=Path('README.md'); r=rd.read_text(encoding='utf-8')
head='''# V8.2.39 — 정리 · 통합 · 사용성 2차\n\n- 홈은 오늘 실행, 회복도구는 계획·배움·실천·자가점검, 헬프는 사람·기관 연결, 마음프로는 대화, `나`는 기록·설정으로 역할을 분리합니다.\n- 회복도구를 `내 계획 / 배우기 / 실천하기 / 자가점검` 네 축으로 정리하고, 중독 Q&A를 학습 영역으로 이동합니다.\n- 습관 관리 진입을 `일정 · 알림` 허브로 통합합니다. 기존 습관 데이터와 알림 저장은 변경하지 않습니다.\n- 홈 우측 `나`에 `내 발자취 / 내 정보·설정` 개인 허브를 두어 기록 접근을 단축하고 설정과 기록조회를 분리합니다.\n- `내 발자취 > 실천기록`에서 기존 12단계 기록과 `S.smartWorks`의 SMART/가족 기록을 함께 조회합니다. 저장구조는 이동하지 않습니다.\n- 가족모드에서는 `가족을 위한 도구`를 주 진입으로 두고, 일반 SMART 전체도구는 2차 진입으로 내립니다.\n- 홈의 상시 마음프로 중복 버튼을 제거하고 하단 마음프로 탭과 상황별 연결은 유지합니다.\n- 가족 안내 상단 닫기를 History 기반 돌아가기로 보정합니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, 기존 SMART·12단계·가족 기록, Android 정확알림·부팅 재예약·이완 TTS는 변경하지 않습니다.\n\n'''
if not r.startswith('# V8.2.39'):
    rd.write_text(head+r,encoding='utf-8')
