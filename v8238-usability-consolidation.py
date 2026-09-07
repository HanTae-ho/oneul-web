from pathlib import Path
import re

idx=Path('index.html'); sw=Path('sw.js'); readme=Path('README.md')

def once(text, old, new, label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    return text.replace(old,new,1)

def replace_function(text, name, new_block):
    sig=f'function {name}('
    start=text.find(sig)
    if start<0: raise SystemExit(f'{name}: function start missing')
    brace=text.find('{', start)
    if brace<0: raise SystemExit(f'{name}: opening brace missing')
    depth=0; i=brace; quote=None; esc=False; line_comment=False; block_comment=False
    while i < len(text):
        c=text[i]; n=text[i+1] if i+1<len(text) else ''
        if line_comment:
            if c=='\n': line_comment=False
        elif block_comment:
            if c=='*' and n=='/': block_comment=False; i+=1
        elif quote:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c==quote: quote=None
        else:
            if c=='/' and n=='/': line_comment=True; i+=1
            elif c=='/' and n=='*': block_comment=True; i+=1
            elif c in "'\"`": quote=c
            elif c=='{': depth+=1
            elif c=='}':
                depth-=1
                if depth==0:
                    return text[:start]+new_block+text[i+1:]
        i+=1
    raise SystemExit(f'{name}: closing brace missing')

s=idx.read_text(encoding='utf-8')
s=once(s,"const BUILD = 'V8.2.37';","const BUILD = 'V8.2.38';",'BUILD')

# 회복도구 진입에서 12단계임을 바로 알 수 있게 명칭만 명확히 합니다.
s=s.replace('<b>단계별 점검</b><span>현재 상태를 단계별로 점검</span>', '<b>12단계 점검</b><span>1·4·8·9·10·11·12단계 기록</span>')
if '<b>12단계 점검</b><span>1·4·8·9·10·11·12단계 기록</span>' not in s:
    raise SystemExit('12-step tool label patch failed')
s=s.replace('<h1 style="margin:0">단계별 점검</h1>', '<h1 style="margin:0">12단계 점검</h1>')
s=s.replace('<span class="b"><b>단계별 점검</b><span>1·4·8·9·10·11·12단계의 검토와 실천 기록을 바로 작성합니다</span></span>', '<span class="b"><b>12단계 점검</b><span>1·4·8·9·10·11·12단계의 검토와 실천 기록을 바로 작성합니다</span></span>')

# SMART 허브 카드도 '긴 도구목록'이 아니라 4개 영역을 고르는 곳임을 먼저 보여줍니다.
s=once(s,'<span class="b"><b>SMART 실천도구</b><span id="tool-smart-tools-s">HOV · 변화계획 · CBA · DEADS · DISARM</span></span>', '<span class="b"><b>SMART 실천도구</b><span id="tool-smart-tools-s">4개 영역에서 지금 필요한 도구만 펼쳐보기</span></span>', 'SMART card subtitle')
old_note='''  <div class="note" style="margin-bottom:12px">\n    SMART Recovery의 4-Point는 순서대로 통과하는 단계가 아닙니다. <b>지금 필요한 영역</b>을 골라 배우고, 작성하고, 다시 사용할 수 있습니다. 작성 내용은 기존 원칙대로 <b>이 기기에만 저장</b>됩니다.\n  </div>'''
new_note='''  <div class="note" style="margin-bottom:12px">\n    SMART Recovery의 4-Point는 순서대로 통과하는 단계가 아닙니다. 아래 <b>4개 영역 중 지금 필요한 한 곳</b>을 눌러 도구를 펼쳐보세요. 한 번에 한 영역만 열리며, 작성 내용은 기존 원칙대로 <b>이 기기에만 저장</b>됩니다.\n  </div>'''
s=once(s,old_note,new_note,'SMART hub note')

# 가족 도구는 핵심 3개는 즉시 보이고, 공용 보조도구만 필요할 때 펼치도록 정리합니다.
start=s.find('<!-- ══════════ 가족을 위한 도구 V8.2.37 ══════════ -->')
end=s.find('<!-- ══════════ 가족 · 다시 사용했을 때 내 대응계획 V8.2.36 ══════════ -->', start)
if start<0 or end<0: raise SystemExit('family tools section markers missing')
family_section='''<!-- ══════════ 가족을 위한 도구 V8.2.38 · 핵심은 바로, 보조는 펼쳐보기 ══════════ -->
<section class="pg" id="p-family-tools">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">가족을 위한 도구</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('tools')">← 회복도구</button>
  </div>
  <div class="note" style="margin-bottom:14px">상대를 감시하거나 바꾸기 위한 도구가 아닙니다. 가족인 <b>내가 내 생각·행동·경계·생활을 돌보기 위해</b> 사용합니다. 가족 전용 도구 3개는 바로 보이고, 기존 보조도구는 필요할 때만 펼칩니다.</div>

  <h2 style="margin-top:0">관계와 안전 · 자주 쓰는 가족도구</h2>
  <button class="toolcard" data-family-tool="family-boundary"><span class="ic" data-ico="check"></span><span class="b"><b>내 경계 정리</b><span>내가 지킬 기준과 보호 행동을 정리합니다.</span></span><span class="go">열기</span></button>
  <button class="toolcard" data-family-tool="family-conversation" style="margin-top:9px"><span class="ic" data-ico="speak"></span><span class="b"><b>대화 준비</b><span>사실 · 내 느낌과 필요 · 구체적인 부탁을 정리합니다.</span></span><span class="go">열기</span></button>
  <button class="toolcard" data-family-tool="family-return-plan" style="margin-top:9px"><span class="ic" data-ico="check"></span><span class="b"><b>다시 사용했을 때 내 대응계획</b><span>안전 · 하지 않을 행동 · 내가 할 행동 · 도움 연결을 미리 정합니다.</span></span><span class="go">열기</span></button>

  <h2>필요할 때 더 살펴보기</h2>
  <div class="acc" data-family-tool-group>
    <button class="acc-h" type="button" aria-expanded="false" onclick="familyToolGroupToggle(this)">
      <div class="acc-n"><b>내 생각과 행동 살펴보기</b><span>ABC · CBA · 문제 해결 5단계</span></div>
      <svg class="acc-v" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg>
    </button>
    <div class="acc-b">
      <button class="toolcard" data-family-tool="smart-abc"><span class="ic" data-ico="speak"></span><span class="b"><b>내 생각과 반응 살펴보기</b><span>사건과 생각을 구분하고 감정·행동을 돌아봅니다.</span></span><span class="go">열기</span></button>
      <button class="toolcard" data-family-tool="smart-cba" style="margin-top:9px"><span class="ic" data-ico="check"></span><span class="b"><b>내 행동 CBA</b><span>내 행동의 단기·장기 이점과 비용을 살펴봅니다.</span></span><span class="go">열기</span></button>
      <button class="toolcard" data-family-tool="smart-problem-solving" style="margin-top:9px"><span class="ic" data-ico="check"></span><span class="b"><b>문제 해결 · 5단계</b><span>문제를 정의하고 선택 가능한 행동과 실행계획을 정리합니다.</span></span><span class="go">열기</span></button>
    </div>
  </div>
  <div class="acc" data-family-tool-group>
    <button class="acc-h" type="button" aria-expanded="false" onclick="familyToolGroupToggle(this)">
      <div class="acc-n"><b>내 생활 돌보기</b><span>삶의 균형 · VACI · 이완 · 건강 회복</span></div>
      <svg class="acc-v" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg>
    </button>
    <div class="acc-b">
      <button class="toolcard" data-family-tool="smart-balance-pie"><span class="ic" data-ico="sprout"></span><span class="b"><b>내 삶의 균형</b><span>한 사람의 문제에 삶 전체가 붙들리지 않도록 내 영역을 살펴봅니다.</span></span><span class="go">열기</span></button>
      <button class="toolcard" data-family-tool="smart-vaci" style="margin-top:9px"><span class="ic" data-ico="sprout"></span><span class="b"><b>VACI · 나를 살리는 활동</b><span>내 삶에 활력과 관심을 되돌리는 활동을 찾습니다.</span></span><span class="go">열기</span></button>
      <button class="toolcard" data-family-tool="smart-relax" style="margin-top:9px"><span class="ic" data-ico="wave"></span><span class="b"><b>이완 · 마음 가라앉히기</b><span>호흡·이완·명상으로 내 긴장을 낮춥니다.</span></span><span class="go">열기</span></button>
      <button class="toolcard" data-family-tool="smart-health" style="margin-top:9px"><span class="ic" data-ico="sprout"></span><span class="b"><b>건강 회복 · 생활 돌보기</b><span>식사·수면·운동 등 내 생활과 몸을 돌봅니다.</span></span><span class="go">열기</span></button>
    </div>
  </div>

  <div class="note" style="margin-top:14px">가족 12단계 점검, 가족 모임, 긴급 도움은 각각 기존 <b>내 발자취 · 모임 · 헬프</b> 위치에서 그대로 사용합니다.</div>
</section>

'''
s=s[:start]+family_section+s[end:]

# 기존 .acc UI를 재사용해 한 번에 하나만 펼칩니다. 데이터/저장은 건드리지 않습니다.
old_draw_family='''function drawFamilyTools(){
  if(!famMode()){ toast('가족모드에서 사용하는 도구입니다.'); go('tools'); return; }
  $$('[data-family-tool]').forEach(b=>{ b.onclick=()=>go(b.dataset.familyTool); });
}'''
new_draw_family='''function familyToolGroupToggle(btn){
  const acc=btn&&btn.closest?btn.closest('[data-family-tool-group]'):null; if(!acc)return;
  const open=!acc.classList.contains('on');
  $$('[data-family-tool-group]').forEach(x=>{x.classList.remove('on');const h=x.querySelector('.acc-h');if(h)h.setAttribute('aria-expanded','false');});
  if(open){acc.classList.add('on');btn.setAttribute('aria-expanded','true');}
}
function drawFamilyTools(){
  if(!famMode()){ toast('가족모드에서 사용하는 도구입니다.'); go('tools'); return; }
  $$('[data-family-tool]').forEach(b=>{ b.onclick=()=>go(b.dataset.familyTool); });
}'''
s=once(s,old_draw_family,new_draw_family,'family group toggle')

# SMART 18개 버튼을 4개 Point 요약으로 먼저 보여주고, 필요한 Point만 한 번에 하나 펼칩니다.
new_smart='''function smartPointToggle(btn){
  const acc=btn&&btn.closest?btn.closest('[data-smart-point]'):null; if(!acc)return;
  const open=!acc.classList.contains('on');
  $$('[data-smart-point]').forEach(x=>{x.classList.remove('on');const h=x.querySelector('.acc-h');if(h)h.setAttribute('aria-expanded','false');});
  if(open){acc.classList.add('on');btn.setAttribute('aria-expanded','true');}
}
function smartPointAccordion(title,summary,intro,body){
  return '<div class="acc" data-smart-point>'+
    '<button class="acc-h" type="button" aria-expanded="false" onclick="smartPointToggle(this)">'+
      '<div class="acc-n"><b>'+esc(title)+'</b><span>'+esc(summary)+'</span></div><svg class="acc-v" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg></button>'+
    '<div class="acc-b"><p class="muted" style="margin:0 0 11px">'+esc(intro)+'</p>'+body+'</div></div>';
}
function drawSmartTools(){
  const box=$('#smart-tools-body'), learn=$('#smart-tools-learn'); if(!box) return;
  if(learn) learn.onclick=()=>{ learnState.topic='smart-recovery'; go('learn-topic'); };
  const p1=[
    ['중요성 · 자신감 빠른 점검','변화 준비도·중요성·자신감을 따로 확인하고 다음 행동 찾기','smart-importance-confidence','check'],
    ['가치의 계층 HOV','내 삶에서 중요한 가치와 현재 행동의 방향을 확인','smart-hov','sprout'],
    ['나의 3가지 질문','원하는 미래와 현재 행동의 차이를 변화 동기로 연결','smart-three-questions','speak'],
    ['변화 계획 워크시트','변화 이유·단계·도움·진전의 신호·방해요인을 계획','smart-change-plan','cal'],
    ['비용-편익 분석 CBA','사용·중단의 좋은 점과 대가를 함께 비교','smart-cba','check']
  ];
  const p2=[
    ['지금 충동 대처하기','충동 강도 확인 → 버티기 타이머 → 호흡 → 전후 강도 확인','urge','wave'],
    ['DEADS · 충동 대처','충동 순간에 사용할 행동 전략을 미리 정하고 실행','smart-deads','wave'],
    ['DISARM · 충동의 목소리','충동을 부추기는 자기대화를 알아차리고 거부·대체','smart-disarm','speak'],
    ['내 충동일기','시간·상황·촉발요인·대처를 기록하고 패턴 확인','urge-diary','wave']
  ];
  const p3=[
    ['ABC 문제 해결','A 사건 → B 생각 → C 결과 → D 반박 → E 새로운 생각','smart-abc','speak'],
    ['DIBS · 생각 반박하기','도움되지 않는 신념 → 질문·증거점검 → 균형 잡힌 합리적 신념','smart-dibs','speak'],
    ['도움이 되지 않는 사고방식','내가 자주 쓰는 사고방식 찾기 → ABC 또는 DIBS로 이어보기','smart-thinking-styles','speak'],
    ['문제 해결 · 5단계','문제 정의 → 브레인스토밍 → 평가 → 선택 → 서면 계획','smart-problem-solving','check']
  ];
  const p4=[
    ['라이프스타일 밸런스 파이','삶의 영역별 만족도 0~10 → 먼저 돌볼 영역과 작은 변화 찾기','smart-balance-pie','sprout'],
    ['VACI · 활력 넘치는 창의적 관심사','새 활동 → 시도 전 점수 → 시도 후 점수와 생각 정리','smart-vaci','sprout'],
    ['SMART 목표 설정','삶의 영역·가치 → 목표 → SMART 5기준 → 실행 행동','smart-goal','check'],
    ['이완 · 마음 가라앉히기','알아차림 → PMR · 심상화 · 명상 중 하나 사용하기','smart-relax','sprout'],
    ['건강 회복 · 생활 돌보기','식사 · 운동 · 수면 · 복약 · 미루기를 기존 기능으로 연결','smart-health','check']
  ];
  const buttons=arr=>arr.map(x=>smartToolButton(x[0],x[1],x[2],x[3])).join('');
  let h='';
  h+=smartPointAccordion('Point 1 · 동기 부여 및 유지','가치 · 동기 · 변화계획 · 5개 도구','왜 바꾸려는지, 무엇을 지키려는지, 어떻게 바꿀지를 정리합니다.',buttons(p1));
  const p2body=famMode()?'<div class="note">DEADS·DISARM·충동일기는 충동을 직접 경험하는 당사자를 위한 도구입니다. 가족모드에서는 상대의 충동을 기록하거나 통제하는 기능으로 사용하지 않습니다.</div>':buttons(p2);
  h+=smartPointAccordion('Point 2 · 충동에 대처하기',famMode()?'당사자의 충동 대처를 이해하는 참고 영역':'즉시 대처 · DEADS · DISARM · 충동일기',''+(famMode()?'당사자가 충동을 알아차리고 대처하는 영역입니다. 가족은 상대의 충동을 기록하거나 관리하지 않고, 회복 과정을 이해하는 참고로 봅니다.':'충동을 알아차리고 지금 사용할 수 있는 대처를 준비합니다.'),p2body);
  h+=smartPointAccordion('Point 3 · 생각·감정·행동 관리하기','ABC · DIBS · 사고방식 · 문제해결','사건과 생각을 구분하고, 감정·행동에 도움이 되는 더 균형 잡힌 관점을 연습합니다.',buttons(p3));
  h+=smartPointAccordion('Point 4 · 균형 잡힌 삶 살기','삶의 균형 · VACI · 목표 · 이완 · 건강','삶의 여러 영역을 살펴보고, 가치에 맞는 활동과 목표로 균형을 만들어갑니다.',buttons(p4));
  box.innerHTML=h;
  box.querySelectorAll('[data-smart-page]').forEach(b=>b.onclick=()=>go(b.dataset.smartPage));
  refreshIcons();
}'''
s=replace_function(s,'drawSmartTools',new_smart)

# README / SW version
idx.write_text(s,encoding='utf-8')

w=sw.read_text(encoding='utf-8')
w=once(w,"const APP_VERSION = 'V8.2.37';","const APP_VERSION = 'V8.2.38';",'SW app version')
w=once(w,"const V = 'ohg-v8237-family-tools-hub';","const V = 'ohg-v8238-usability-consolidation';",'SW cache')
sw.write_text(w,encoding='utf-8')

r=readme.read_text(encoding='utf-8')
head='''# V8.2.38 — 정리 · 통합 · 사용성 1차\n\n- 새 기능을 추가하지 않고 V8.2.37의 기능을 더 쉽게 찾도록 정리합니다.\n- SMART 실천도구는 18개 버튼을 한꺼번에 보여주지 않고 4개 Point를 먼저 보여준 뒤, 필요한 Point 하나만 펼쳐 사용합니다. 기존 모든 도구와 저장은 그대로 유지합니다.\n- 가족을 위한 도구는 가족 전용 핵심 3개(내 경계 정리 / 대화 준비 / 다시 사용했을 때 내 대응계획)는 바로 보이고, ABC·CBA·문제해결·삶의 균형·VACI·이완·건강회복은 보조 묶음으로 접어둡니다.\n- `단계별 점검`은 SMART Point와 혼동되지 않도록 `12단계 점검`으로 명확히 표시합니다.\n- 홈·일정·알림·저장구조·DATA_SCHEMA=6·가족 충동/재발 비기록·SMART/12단계 내용·Android TTS/정확알림 엔진은 변경하지 않습니다.\n\n'''
readme.write_text(head+r,encoding='utf-8')
