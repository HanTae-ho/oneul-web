from pathlib import Path
import re

idx=Path('index.html'); sw=Path('sw.js'); readme=Path('README.md')

def once(text, old, new, label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    return text.replace(old,new,1)

s=idx.read_text(encoding='utf-8')
s=once(s,"const BUILD = 'V8.2.36';","const BUILD = 'V8.2.37';",'BUILD')

# 1) 회복도구 > 배우고 연습하기에 가족모드 전용 허브 진입카드를 둡니다.
smart_card='''    <button class="toolcard" id="tool-smart-tools" style="margin-top:9px">\n      <span class="ic" data-ico="check"></span>\n      <span class="b"><b>SMART 실천도구</b><span id="tool-smart-tools-s">HOV · 변화계획 · CBA · DEADS · DISARM</span></span>\n      <span class="go">열기</span>\n    </button>'''
family_card='''    <button class="toolcard hide" id="tool-family-tools" style="margin-top:9px">\n      <span class="ic" data-ico="family"></span>\n      <span class="b"><b>가족을 위한 도구</b><span>경계 · 대화 · 대응계획과 내 삶을 돌보는 연습</span></span>\n      <span class="go">열기</span>\n    </button>\n'''
s=once(s,smart_card,family_card+smart_card,'family tools entry card')

# 2) 가족을 위한 도구 허브. 기존 기능의 바로가기만 제공하며 새 저장체계를 만들지 않습니다.
page_marker='<!-- ══════════ 가족 · 다시 사용했을 때 내 대응계획 V8.2.36 ══════════ -->'
page='''<!-- ══════════ 가족을 위한 도구 V8.2.37 ══════════ -->
<section class="pg" id="p-family-tools">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">가족을 위한 도구</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('tools')">← 회복도구</button>
  </div>
  <div class="note" style="margin-bottom:14px">상대를 감시하거나 바꾸기 위한 도구가 아닙니다. 가족인 <b>내가 내 생각·행동·경계·생활을 돌보기 위해</b> 필요한 도구를 골라 사용합니다.</div>

  <h2 style="margin-top:0">관계와 안전</h2>
  <button class="toolcard" data-family-tool="family-boundary"><span class="ic" data-ico="shield"></span><span class="b"><b>내 경계 정리</b><span>내가 지킬 기준과 보호 행동을 정리합니다.</span></span><span class="go">열기</span></button>
  <button class="toolcard" data-family-tool="family-conversation" style="margin-top:9px"><span class="ic" data-ico="speak"></span><span class="b"><b>대화 준비</b><span>사실 · 내 느낌과 필요 · 구체적인 부탁을 정리합니다.</span></span><span class="go">열기</span></button>
  <button class="toolcard" data-family-tool="family-return-plan" style="margin-top:9px"><span class="ic" data-ico="check"></span><span class="b"><b>다시 사용했을 때 내 대응계획</b><span>안전 · 하지 않을 행동 · 내가 할 행동 · 도움 연결을 미리 정합니다.</span></span><span class="go">열기</span></button>

  <h2>내 생각과 행동 살펴보기</h2>
  <button class="toolcard" data-family-tool="smart-abc"><span class="ic" data-ico="speak"></span><span class="b"><b>내 생각과 반응 살펴보기</b><span>사건과 생각을 구분하고 감정·행동을 돌아봅니다.</span></span><span class="go">열기</span></button>
  <button class="toolcard" data-family-tool="smart-cba" style="margin-top:9px"><span class="ic" data-ico="check"></span><span class="b"><b>내 행동 CBA</b><span>내 행동의 단기·장기 이점과 비용을 살펴봅니다.</span></span><span class="go">열기</span></button>
  <button class="toolcard" data-family-tool="smart-problem-solving" style="margin-top:9px"><span class="ic" data-ico="check"></span><span class="b"><b>문제 해결 · 5단계</b><span>문제를 정의하고 선택 가능한 행동과 실행계획을 정리합니다.</span></span><span class="go">열기</span></button>

  <h2>내 생활 돌보기</h2>
  <button class="toolcard" data-family-tool="smart-balance-pie"><span class="ic" data-ico="sprout"></span><span class="b"><b>내 삶의 균형</b><span>한 사람의 문제에 삶 전체가 붙들리지 않도록 내 영역을 살펴봅니다.</span></span><span class="go">열기</span></button>
  <button class="toolcard" data-family-tool="smart-vaci" style="margin-top:9px"><span class="ic" data-ico="sprout"></span><span class="b"><b>VACI · 나를 살리는 활동</b><span>내 삶에 활력과 관심을 되돌리는 활동을 찾습니다.</span></span><span class="go">열기</span></button>
  <button class="toolcard" data-family-tool="smart-relax" style="margin-top:9px"><span class="ic" data-ico="wave"></span><span class="b"><b>이완 · 마음 가라앉히기</b><span>호흡·이완·명상으로 내 긴장을 낮춥니다.</span></span><span class="go">열기</span></button>
  <button class="toolcard" data-family-tool="smart-health" style="margin-top:9px"><span class="ic" data-ico="sprout"></span><span class="b"><b>건강 회복 · 생활 돌보기</b><span>식사·수면·운동 등 내 생활과 몸을 돌봅니다.</span></span><span class="go">열기</span></button>

  <div class="note" style="margin-top:14px">가족 12단계 점검, 가족 모임, 긴급 도움은 각각 기존 <b>내 발자취 · 모임 · 헬프</b> 위치에서 그대로 사용합니다.</div>
</section>

'''
s=once(s,page_marker,page+page_marker,'family tools page')

# 3) 가족 전용 세 도구의 돌아가기도 실제 진입경로를 반영하게 합니다.
for page_id in ['family-return-plan','family-conversation','family-boundary']:
    start=s.index(f'id="p-{page_id}"')
    end=s.find('</section>',start)
    block=s[start:end]
    old='onclick="appBack(\'fam\')">← 가족 안내</button>'
    if old not in block:
        raise SystemExit(f'{page_id} back marker missing')
    block=block.replace(old,'data-smart-back data-back-label="가족 안내" data-back-default="fam" onclick="appBack(\'fam\')">← 가족 안내</button>',1)
    s=s[:start]+block+s[end:]

# 4) 공통 route-aware back에 가족도구 허브를 추가합니다.
s=once(s,"    'fam':'가족 안내',","    'fam':'가족 안내',\n    'family-tools':'가족을 위한 도구',",'family tools back label')
s=once(s,"    'fam':'fam', 'learn-topic':'learn-topic', 'capsule':'capsule', 'smart-tools':'smart-tools',","    'fam':'fam', 'family-tools':'family-tools', 'learn-topic':'learn-topic', 'capsule':'capsule', 'smart-tools':'smart-tools',",'family tools fallback')

# 5) 허브 표시/동작. 가족모드가 아니면 회복도구에 카드가 나타나지 않습니다.
s=once(s,"function drawTools(){\n","function drawTools(){\n  const ft=$('#tool-family-tools'); if(ft) ft.classList.toggle('hide', !famMode());\n",'draw tools family card')
func_marker='/* ══════════ 가족 · 내 경계 정리 V8.2.33 ══════════'
func='''function drawFamilyTools(){
  if(!famMode()){ toast('가족모드에서 사용하는 도구입니다.'); go('tools'); return; }
  $$('[data-family-tool]').forEach(b=>{ b.onclick=()=>go(b.dataset.familyTool); });
}

'''
s=once(s,func_marker,func+func_marker,'family tools draw')
s=once(s,"$('#tool-smart-tools').onclick = () => go('smart-tools');","$('#tool-family-tools').onclick = () => go('family-tools');\n$('#tool-smart-tools').onclick = () => go('smart-tools');",'family tools click')

# 6) go() 렌더링 및 하단 회복도구 탭 정합성. V8.2.35~36 가족 페이지 누락도 함께 보정합니다.
s=once(s,"  if(p === 'family-return-plan') drawFamilyReturnPlan();","  if(p === 'family-tools') drawFamilyTools();\n  if(p === 'family-return-plan') drawFamilyReturnPlan();",'family tools dispatch')
old_tab=" || p === 'smart-health' || p === 'family-boundary' || p === 'smart-tools') ? 'tools' : p;"
new_tab=" || p === 'smart-health' || p === 'family-tools' || p === 'family-return-plan' || p === 'family-conversation' || p === 'family-boundary' || p === 'smart-tools') ? 'tools' : p;"
s=once(s,old_tab,new_tab,'family pages tool tab')

# 7) 가족 안내 임상 문구 보정: 단일 뇌회로/만성질환 비유/재발 단정 대신 더 넓고 중립적인 표현.
pat=r"    \{h:'의지의 문제가 아닙니다',\n     b:.*?\},\n    \{h:'당신 탓이 아닙니다'"
rep="""    {h:'의지의 문제가 아닙니다',
     b:'중독은 단순한 의지의 문제가 아닙니다. 반복된 사용이나 행동은 뇌의 보상·학습 체계와 습관, 감정, 생활환경에 영향을 주어 의지만으로 바꾸기 어려울 수 있습니다.\\
' +
       '\"정신 차려\"라는 말만으로 해결되지 않는 데에는 이런 여러 요인이 함께 작용합니다.'},
    {h:'당신 탓이 아닙니다'"""
s,n=re.subn(pat,rep,s,count=1,flags=re.S)
if n!=1: raise SystemExit(f'willpower wording: {n}')

pat=r"    \{h:'회복은 완치가 아니라 관리입니다',\n     b:.*?\},\n    \{h:'재발은 흔한 일입니다', a:'family-return-plan', al:'내 대응계획 정리하기',\n     b:.*?\},"
rep="""    {h:'회복은 삶을 다시 돌보는 과정입니다',
     b:'회복은 사용이나 행동을 멈추는 데서 끝나지 않습니다. 몸·마음·생활·관계를 계속 돌보며 안정된 삶을 만들어가는 과정입니다.\\
' +
       '\"이제 다 나았지?\"처럼 회복을 한 번에 끝나는 일로 보는 질문은 당사자에게 부담이 될 수 있습니다.'},
    {h:'다시 사용하는 일이 생겼을 때', a:'family-return-plan', al:'내 대응계획 정리하기',
     b:'다시 사용했다고 지금까지의 회복이 모두 사라지는 것은 아닙니다. 먼저 안전을 확인하고, 있었던 일을 없던 일처럼 넘기지 않으면서 다음 행동을 정리할 수 있습니다.\\
' +
       '가족은 추궁이나 감시에 매달리기보다 그 상황에서 내가 할 행동과 도움받을 곳을 미리 준비할 수 있습니다.'},"""
s,n=re.subn(pat,rep,s,count=1,flags=re.S)
if n!=1: raise SystemExit(f'recovery/reuse wording: {n}')

# 8) SMART Point 2의 소개문도 가족/당사자에 따라 다르게 보입니다.
old="  h+='<div class=\"card\"><h3>Point 2 · 충동에 대처하기</h3><p class=\"muted\" style=\"margin:-4px 0 11px\">충동을 기록하고, 지금 사용할 수 있는 대처를 준비합니다.</p>';\n  if(famMode()){"
new="  h+='<div class=\"card\"><h3>Point 2 · 충동에 대처하기</h3><p class=\"muted\" style=\"margin:-4px 0 11px\">'+(famMode()?'당사자가 충동을 알아차리고 대처하는 영역입니다. 가족은 상대의 충동을 기록하거나 관리하지 않고, 회복 과정을 이해하는 참고로 봅니다.':'충동을 기록하고, 지금 사용할 수 있는 대처를 준비합니다.')+'</p>';\n  if(famMode()){"
s=once(s,old,new,'SMART point2 family wording')

idx.write_text(s,encoding='utf-8')

w=sw.read_text(encoding='utf-8')
w=once(w,"const APP_VERSION = 'V8.2.36';","const APP_VERSION = 'V8.2.37';",'sw version')
w=once(w,"const V = 'ohg-v8236-family-return-plan';","const V = 'ohg-v8237-family-tools-hub';",'sw cache')
sw.write_text(w,encoding='utf-8')

r=readme.read_text(encoding='utf-8')
head='''# V8.2.37 — 가족모드 최종 정리 · 가족을 위한 도구 허브

- 가족모드 `회복도구 → 배우고 연습하기`에 `가족을 위한 도구` 허브를 추가합니다. 당사자모드에서는 이 카드가 보이지 않습니다.
- 허브는 새 저장체계가 아니라 기존 실천도구의 바로가기입니다.
  - 가족 전용: 내 경계 정리 / 대화 준비 / 다시 사용했을 때 내 대응계획
  - 보조: ABC / CBA / 문제 해결 5단계 / 삶의 균형 / VACI / 이완 / 건강 회복
- 가족 12단계·가족모임·헬프는 기존 위치를 유지해 또 하나의 가족 전체 메뉴로 확장하지 않습니다.
- 가족 안내 글 안의 기존 문맥형 실행버튼도 그대로 유지합니다.
- 가족 안내의 중독·회복·다시 사용 관련 문구를 단정적 설명보다 임상적으로 폭넓고 중립적인 표현으로 보정합니다.
- SMART Point 2는 가족모드에서 상대의 충동을 기록·관리하는 영역이 아니라 당사자의 충동 대처를 이해하는 참고 영역임을 처음부터 명시합니다.
- 가족 안내 또는 가족도구 허브에서 기존 도구로 들어갈 때 상단 되돌아가기가 실제 진입경로에 맞게 표시됩니다.
- V8.2.35~36 가족 전용 페이지에서도 하단 `회복도구` 탭 강조가 유지되도록 누락된 라우팅을 보정합니다.
- `S.smartWorks`, `DATA_SCHEMA=6`, 가족 충동·재발 비기록, Local-first, 기존 SMART/12단계 저장구조는 유지합니다.
- Android 이완 TTS·화면 OFF 재생·속도선택·정확알림 엔진·부팅 후 재예약은 변경하지 않습니다.

'''
readme.write_text(head+r,encoding='utf-8')
