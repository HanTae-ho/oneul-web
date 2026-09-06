from pathlib import Path


def replace_one(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label} target count={n}')
    return text.replace(old, new, 1)

idx = Path('index.html')
s = idx.read_text(encoding='utf-8')

s = replace_one(s, "const BUILD = 'V8.2.25';", "const BUILD = 'V8.2.26';", 'build')

# Add one compact Point 4 relaxation page. No records or schema changes.
anchor = '''  <div id="smart-goal-list" style="margin-top:12px"></div>\n</section>\n\n<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->'''
page = '''  <div id="smart-goal-list" style="margin-top:12px"></div>\n</section>\n\n<!-- ══════════ SMART Recovery · Relaxation V8.2.26 ══════════ -->\n<section class="pg" id="p-smart-relax">\n  <div class="sp" style="margin-bottom:11px">\n    <h1 style="margin:0">이완 · 마음 가라앉히기</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back onclick="appBack('smart-tools')">← SMART 실천도구</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    강한 감정이 커질수록 생각과 행동의 균형을 잡기 어려워질 수 있습니다. 먼저 지금의 감정과 몸의 긴장을 알아차리고, <b>점진적 근육 이완(PMR) · 심상화 · 명상</b> 가운데 지금 맞는 방법 하나를 사용해보세요. 이 화면은 연습용이며 별도 기록을 저장하지 않습니다.\n  </div>\n  <div id="smart-relax-role-note"></div>\n  <div id="smart-relax-body">\n    <div class="acc on" data-relax-acc>\n      <button class="acc-h" type="button" data-relax-toggle aria-expanded="true">\n        <span class="acc-n"><b>1 · 먼저 알아차리기</b><span>감정 · 몸의 긴장 · 호흡을 잠깐 확인합니다.</span></span>\n        <svg class="acc-v" viewBox="0 0 24 24"><path d="M6.5 9.5l5.5 5.5 5.5-5.5"/></svg>\n      </button>\n      <div class="acc-b">\n        <p style="margin:0">감정을 바로 없애려 하기보다 <b>지금 감정이 얼마나 강한지</b>, 몸에서 어디가 긴장되어 있는지, 호흡이 어떤지 잠깐 알아차립니다. 강한 감정과 합리적인 사고 사이의 균형을 다시 찾기 위한 출발점입니다.</p>\n      </div>\n    </div>\n    <div class="acc" data-relax-acc>\n      <button class="acc-h" type="button" data-relax-toggle aria-expanded="false">\n        <span class="acc-n"><b>2 · 점진적 근육 이완(PMR)</b><span>각 근육군을 약 5초 긴장시킨 뒤 힘을 풉니다.</span></span>\n        <svg class="acc-v" viewBox="0 0 24 24"><path d="M6.5 9.5l5.5 5.5 5.5-5.5"/></svg>\n      </button>\n      <div class="acc-b">\n        <p class="muted" style="margin:0 0 10px">의자에 앉거나 누운 자세에서 합니다. 각 부위에 약 5초간 힘을 주었다가 풀면서 <b>긴장됐을 때와 이완됐을 때의 차이</b>를 느껴봅니다. 처음에는 변화가 크게 느껴지지 않을 수도 있습니다.</p>\n        <div class="card tight"><b>머리 · 얼굴</b><div class="muted">이마에 힘주기 → 눈을 꼭 감기 → 턱에 힘주기 → 모두 풀기</div></div>\n        <div class="card tight"><b>목 · 어깨</b><div class="muted">어깨를 귀 쪽으로 으쓱해 5초 → 천천히 내려 힘 풀기</div></div>\n        <div class="card tight"><b>팔 · 손</b><div class="muted">주먹과 팔에 힘주기 → 5초 뒤 손과 팔 전체 풀기</div></div>\n        <div class="card tight"><b>몸통</b><div class="muted">복부 · 등 · 엉덩이에 가볍게 힘주기 → 5초 뒤 풀기</div></div>\n        <div class="card tight"><b>다리 · 발</b><div class="muted">허벅지 · 종아리 · 발목 · 발가락에 힘주기 → 5초 뒤 풀기</div></div>\n        <p class="tiny" style="margin:8px 0 0">통증이나 불편함이 있는 부위는 억지로 힘주지 않고 건너뛰어도 됩니다.</p>\n      </div>\n    </div>\n    <div class="acc" data-relax-acc>\n      <button class="acc-h" type="button" data-relax-toggle aria-expanded="false">\n        <span class="acc-n"><b>3 · 심상화</b><span>약 15분 · 조용하고 안전하며 편안한 장소를 자세히 떠올립니다.</span></span>\n        <svg class="acc-v" viewBox="0 0 24 24"><path d="M6.5 9.5l5.5 5.5 5.5-5.5"/></svg>\n      </button>\n      <div class="acc-b">\n        <p class="muted" style="margin:0 0 10px">가능하면 약 15분의 여유를 두고 방해 요소가 적은 곳에 편하게 앉거나 눕습니다.</p>\n        <div class="card tight"><b>1</b><div class="muted">눈을 감고 혼자 조용하고 안전하며 편안한 장소에 있는 모습을 떠올립니다.</div></div>\n        <div class="card tight"><b>2</b><div class="muted">그곳에서 들리는 소리, 냄새, 앉거나 누워 있는 느낌을 상상합니다.</div></div>\n        <div class="card tight"><b>3</b><div class="muted">나를 편안하게 하는 세부 모습을 가능한 한 많이 채워봅니다.</div></div>\n        <div class="card tight"><b>4</b><div class="muted">어깨와 머리의 힘을 풀고 천천히 숨을 쉽니다.</div></div>\n      </div>\n    </div>\n    <div class="acc" data-relax-acc>\n      <button class="acc-h" type="button" data-relax-toggle aria-expanded="false">\n        <span class="acc-n"><b>4 · 명상</b><span>호흡과 숫자 세기로 지금 순간에 다시 주의를 둡니다.</span></span>\n        <svg class="acc-v" viewBox="0 0 24 24"><path d="M6.5 9.5l5.5 5.5 5.5-5.5"/></svg>\n      </button>\n      <div class="acc-b">\n        <p class="tiny" style="margin:0 0 10px">핸드북에서는 명상과 마음챙김이 SMART 모임의 일반적인 구성은 아니지만, 일부 사람에게 선택적으로 도움이 되는 연습으로 소개합니다.</p>\n        <div class="card tight"><b>자세와 호흡</b><div class="muted">등을 편안하게 곧게 펴고 앉습니다. 코로 천천히 숨을 쉬고, 깊고 긴 호흡을 세 번 하면서 몸의 느낌을 알아차립니다.</div></div>\n        <div class="card tight"><b>1부터 10까지</b><div class="muted">호흡이 자연스러운 리듬으로 돌아오면 숨을 내쉴 때마다 조용히 1, 2, 3… 10까지 셉니다. 10이 되면 다시 1부터 시작합니다.</div></div>\n        <div class="card tight"><b>생각이 들어오면</b><div class="muted">생각을 밀어내거나 없던 것처럼 하지 않습니다. 있다는 것을 알아차린 뒤 관여하지 않고 호흡과 숫자 세기로 천천히 돌아옵니다.</div></div>\n        <div class="card tight"><b>판단하지 않기</b><div class="muted">숫자를 잊거나 마음이 산만해져도 다시 1부터 시작합니다. 명상을 잘하고 못하고로 자신을 평가하지 않습니다.</div></div>\n      </div>\n    </div>\n  </div>\n  <div class="card" id="smart-relax-breath-wrap" style="margin-top:12px">\n    <h3>이미 있는 호흡 가이드</h3>\n    <p class="muted" style="margin:-3px 0 11px">앱의 충동 대응에는 이미 <b>4초 들이쉬기 · 6초 내쉬기</b> 호흡 가이드가 있습니다. 같은 기능을 하나 더 만들지 않고 기존 도구로 연결합니다.</p>\n    <button class="btn sec" id="smart-relax-breath">기존 호흡 가이드로 이동</button>\n  </div>\n</section>\n\n<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->'''
s = replace_one(s, anchor, page, 'relax page')

# Route, draw and context-aware back support.
s = replace_one(s,
"p === 'smart-vaci' || p === 'smart-goal' || p === 'smart-tools'",
"p === 'smart-vaci' || p === 'smart-goal' || p === 'smart-relax' || p === 'smart-tools'",
'route tab')
s = replace_one(s,
"  if(p === 'smart-goal') drawSmartGoal();\n  if(p === 'smart-tools') drawSmartTools();",
"  if(p === 'smart-goal') drawSmartGoal();\n  if(p === 'smart-relax') drawSmartRelax();\n  if(p === 'smart-tools') drawSmartTools();",
'draw route')
s = replace_one(s,
"    'smart-vaci':'VACI · 활력 넘치는 창의적 관심사',\n    'smart-goal':'SMART 목표 설정'",
"    'smart-vaci':'VACI · 활력 넘치는 창의적 관심사',\n    'smart-goal':'SMART 목표 설정',\n    'smart-relax':'이완 · 마음 가라앉히기'",
'back label')
s = replace_one(s,
"'smart-balance-pie':'smart-balance-pie', 'smart-vaci':'smart-vaci', 'smart-goal':'smart-goal'",
"'smart-balance-pie':'smart-balance-pie', 'smart-vaci':'smart-vaci', 'smart-goal':'smart-goal', 'smart-relax':'smart-relax'",
'back fallback')

# Point 4 hub: one additional tool only.
old_hub = "smartToolButton('라이프스타일 밸런스 파이','삶의 영역별 만족도 0~10 → 먼저 돌볼 영역과 작은 변화 찾기','smart-balance-pie','sprout')+smartToolButton('VACI · 활력 넘치는 창의적 관심사','새 활동 → 시도 전 점수 → 시도 후 점수와 생각 정리','smart-vaci','sprout')+smartToolButton('SMART 목표 설정','삶의 영역·가치 → 목표 → SMART 5기준 → 실행 행동','smart-goal','check')"
new_hub = old_hub + "+smartToolButton('이완 · 마음 가라앉히기','알아차림 → PMR · 심상화 · 명상 중 하나 사용하기','smart-relax','wave')"
s = replace_one(s, old_hub, new_hub, 'point4 hub')

# Learning action route.
s = replace_one(s,
"  if(type === 'smart-goal'){ go('smart-goal'); return; }\n  if(type === 'halt')",
"  if(type === 'smart-goal'){ go('smart-goal'); return; }\n  if(type === 'smart-relax'){ go('smart-relax'); return; }\n  if(type === 'halt')",
'learning route')

# Lightweight behavior only: one accordion open at a time and existing breath tool handoff.
relax_js = r'''/* ══════════ SMART Recovery · 이완 · 마음 가라앉히기 V8.2.26 ══════════
   핸드북 Point 4의 감정과 함께 살아가기, PMR, 심상화, 명상 내용을
   저장 없는 즉시 연습 화면으로 구성합니다. 기존 호흡 가이드는 충동 대응으로 연결합니다. */
function drawSmartRelax(){
 const box=$('#smart-relax-body'),rn=$('#smart-relax-role-note'),bw=$('#smart-relax-breath-wrap'),bb=$('#smart-relax-breath');if(!box)return;
 if(rn)rn.innerHTML=famMode()?'<div class="note" style="margin-bottom:12px"><b>가족도 자신의 긴장을 돌봅니다.</b><br>상대를 진정시키거나 바꾸기 위한 기술이 아니라, 가족인 내가 내 감정과 몸의 긴장을 알아차리고 가라앉히기 위한 연습으로 사용합니다.</div>':'';
 const setAcc=(node,on)=>{if(!node)return;node.classList.toggle('on',!!on);const h=node.querySelector('[data-relax-toggle]');if(h)h.setAttribute('aria-expanded',on?'true':'false');};
 box.querySelectorAll('[data-relax-toggle]').forEach(b=>b.onclick=()=>{const target=b.closest('[data-relax-acc]'),was=target&&target.classList.contains('on');box.querySelectorAll('[data-relax-acc]').forEach(x=>setAcc(x,false));if(target&&!was)setAcc(target,true);});
 if(bw)bw.classList.toggle('hide',famMode());
 if(bb)bb.onclick=()=>{go('urge');toast('충동 대응을 시작한 뒤 타이머에서 ‘호흡 같이 하기’를 사용할 수 있습니다.');};
}

'''
s = replace_one(s, "function learningAction(type,sectionId){", relax_js + "function learningAction(type,sectionId){", 'relax js')

idx.write_text(s, encoding='utf-8')

# Learning Point 4 action.
ld = Path('learning-data.js')
l = ld.read_text(encoding='utf-8')
l = l.replace('/* 오늘 한 걸음 — 회복학습 데이터 V8.2.22', '/* 오늘 한 걸음 — 회복학습 데이터 V8.2.26', 1)
old_action = '''          {\n            "type": "smart-goal",\n            "label": "SMART 목표 설정하기"\n          }'''
new_action = old_action + ''',\n          {\n            "type": "smart-relax",\n            "label": "이완 · 마음 가라앉히기"\n          }'''
if l.count(old_action) != 1:
    raise SystemExit(f'learning action target count={l.count(old_action)}')
l = l.replace(old_action, new_action, 1)
ld.write_text(l, encoding='utf-8')

# Service worker cache/version.
sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
w = replace_one(w, "const APP_VERSION = 'V8.2.25';", "const APP_VERSION = 'V8.2.26';", 'sw app version')
w = replace_one(w, "const V = 'ohg-v8225-smart-goals-habit-link';", "const V = 'ohg-v8226-relaxation';", 'sw cache')
sw.write_text(w, encoding='utf-8')
