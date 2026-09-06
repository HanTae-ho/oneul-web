from pathlib import Path

root=Path('.')
idx=root/'index.html'
learn=root/'learning-data.js'
sw=root/'sw.js'
readme=root/'README.md'

def replace_once(text, old, new, label):
    n=text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    return text.replace(old,new,1)

# ── index.html ──
s=idx.read_text(encoding='utf-8')
s=replace_once(s,"const BUILD = 'V8.2.30';","const BUILD = 'V8.2.31';",'BUILD')

marker='''  <button class="btn sec" id="smart-tools-learn">SMART Recovery 설명 보기</button>\n  <div id="smart-tools-body" style="margin-top:14px"></div>\n</section>\n\n<!-- ══════════ SMART Recovery · HOV V8.2.5 ══════════ -->'''
page='''  <button class="btn sec" id="smart-tools-learn">SMART Recovery 설명 보기</button>\n  <div id="smart-tools-body" style="margin-top:14px"></div>\n</section>\n\n<!-- ══════════ SMART Recovery · 중요성 · 자신감 빠른 점검 V8.2.31 ══════════ -->\n<section class="pg" id="p-smart-importance-confidence">\n  <div class="sp" style="margin-bottom:11px">\n    <h1 style="margin:0">중요성 · 자신감 빠른 점검</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back onclick="appBack('smart-tools')">← SMART 실천도구</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    변화를 얼마나 중요하게 느끼는지와 <b>해낼 수 있다는 자신감</b>을 따로 살펴봅니다. 점수는 평가나 진단이 아니며, <b>이 빠른 점검은 저장하지 않습니다.</b>\n  </div>\n  <div id="smart-ic-role-note"></div>\n  <div class="card">\n    <div class="field">\n      <label>변화를 시작하거나 이어갈 준비가 얼마나 되어 있나요? <b id="smart-ic-ready-n">5</b> / 10</label>\n      <input id="smart-ic-ready" type="range" min="1" max="10" value="5">\n    </div>\n    <div class="field">\n      <label>이 변화를 실행하는 것이 얼마나 중요한가요? <b id="smart-ic-important-n">5</b> / 10</label>\n      <input id="smart-ic-important" type="range" min="0" max="10" value="5">\n    </div>\n    <div class="field">\n      <label>이 변화를 해낼 수 있다고 얼마나 느끼나요? <b id="smart-ic-confidence-n">5</b> / 10</label>\n      <input id="smart-ic-confidence" type="range" min="0" max="10" value="5">\n    </div>\n  </div>\n  <div class="card">\n    <label>앞으로 나아가는 데 무엇이 도움이 될까요?</label>\n    <textarea id="smart-ic-help" maxlength="400" placeholder="예: 작은 행동부터 시작하기, 믿을 수 있는 사람에게 도움을 요청하기"></textarea>\n  </div>\n  <div class="card">\n    <h3>다음에 이어보기</h3>\n    <p class="muted" style="margin:-4px 0 11px">점수의 정답을 찾기보다, 지금 나에게 필요한 도구를 골라 이어가세요.</p>\n    <button class="btn sec sm" id="smart-ic-hov">HOV 가치의 계층</button>\n    <div style="height:8px"></div>\n    <button class="btn ghost sm" id="smart-ic-cba">CBA 비용-편익 분석</button>\n    <div style="height:8px"></div>\n    <button class="btn ghost sm" id="smart-ic-plan">변화 계획 워크시트</button>\n  </div>\n</section>\n\n<!-- ══════════ SMART Recovery · HOV V8.2.5 ══════════ -->'''
s=replace_once(s,marker,page,'importance page insertion')

old='''  const p1=[\n    ['가치의 계층 HOV','내 삶에서 중요한 가치와 현재 행동의 방향을 확인','smart-hov','sprout'],'''
new='''  const p1=[\n    ['중요성 · 자신감 빠른 점검','변화 준비도·중요성·자신감을 따로 확인하고 다음 행동 찾기','smart-importance-confidence','check'],\n    ['가치의 계층 HOV','내 삶에서 중요한 가치와 현재 행동의 방향을 확인','smart-hov','sprout'],'''
s=replace_once(s,old,new,'Point1 hub link')

old='''  const p2=[\n    ['DEADS · 충동 대처','충동 순간에 사용할 행동 전략을 미리 정하고 실행','smart-deads','wave'],'''
new='''  const p2=[\n    ['지금 충동 대처하기','충동 강도 확인 → 버티기 타이머 → 호흡 → 전후 강도 확인','urge','wave'],\n    ['DEADS · 충동 대처','충동 순간에 사용할 행동 전략을 미리 정하고 실행','smart-deads','wave'],'''
s=replace_once(s,old,new,'Point2 urge link')

old="p === 'capsule' || p === 'urge-diary' || p === 'smart-hov'"
new="p === 'capsule' || p === 'urge-diary' || p === 'smart-importance-confidence' || p === 'smart-hov'"
s=replace_once(s,old,new,'tool tab route')

old="""  if(p === 'capsule') drawCapsule();\n  if(p === 'urge-diary') drawUrgeDiary();\n  if(p === 'smart-hov') drawSmartHov();"""
new="""  if(p === 'capsule') drawCapsule();\n  if(p === 'urge-diary') drawUrgeDiary();\n  if(p === 'smart-importance-confidence') drawSmartImportanceConfidence();\n  if(p === 'smart-hov') drawSmartHov();"""
s=replace_once(s,old,new,'draw dispatch')

old="""    'capsule':'미래의 나에게',\n    'smart-hov':'가치의 계층 HOV',"""
new="""    'capsule':'미래의 나에게',\n    'smart-importance-confidence':'중요성 · 자신감 빠른 점검',\n    'smart-hov':'가치의 계층 HOV',"""
s=replace_once(s,old,new,'back label')
old="""    'learn-topic':'learn-topic', 'capsule':'capsule', 'smart-tools':'smart-tools',\n    'smart-hov':'smart-hov',"""
new="""    'learn-topic':'learn-topic', 'capsule':'capsule', 'smart-tools':'smart-tools',\n    'smart-importance-confidence':'smart-importance-confidence', 'smart-hov':'smart-hov',"""
s=replace_once(s,old,new,'back fallback')

fn="""/* ══════════ SMART Recovery · 중요성 · 자신감 빠른 점검 V8.2.31 ══════════ */\nfunction drawSmartImportanceConfidence(){\n  const rn=$('#smart-ic-role-note');\n  if(rn) rn.innerHTML=famMode()\n    ? '<div class=\"note\" style=\"margin-bottom:12px\"><b>가족은 내 변화를 점검합니다.</b><br>상대가 얼마나 변하고 싶어 하는지 평가하는 척도가 아니라, 가족인 내가 바꾸고 싶은 내 행동·생활·경계를 대상으로 사용합니다.</div>'\n    : '';\n  [\n    ['#smart-ic-ready','#smart-ic-ready-n'],\n    ['#smart-ic-important','#smart-ic-important-n'],\n    ['#smart-ic-confidence','#smart-ic-confidence-n']\n  ].forEach(pair=>{\n    const x=$(pair[0]), n=$(pair[1]);\n    if(!x||!n) return;\n    const sync=()=>{ n.textContent=x.value; };\n    sync(); x.oninput=sync;\n  });\n  const hov=$('#smart-ic-hov'), cba=$('#smart-ic-cba'), plan=$('#smart-ic-plan');\n  if(hov) hov.onclick=()=>go('smart-hov');\n  if(cba) cba.onclick=()=>go('smart-cba');\n  if(plan) plan.onclick=()=>go('smart-change-plan');\n}\n\nfunction smartHovValues"""
s=replace_once(s,'function smartHovValues',fn,'importance draw function')

old="""  if(type === 'urge-diary'){ go('urge-diary'); return; }\n  if(type === 'smart-hov'){ go('smart-hov'); return; }"""
new="""  if(type === 'urge-coping'){ go('urge'); return; }\n  if(type === 'urge-diary'){ go('urge-diary'); return; }\n  if(type === 'smart-importance-confidence'){ go('smart-importance-confidence'); return; }\n  if(type === 'smart-hov'){ go('smart-hov'); return; }"""
s=replace_once(s,old,new,'learning action routes')
idx.write_text(s,encoding='utf-8')

l=learn.read_text(encoding='utf-8')
l=replace_once(l,'/* 오늘 한 걸음 — 회복학습 데이터 V8.2.30','/* 오늘 한 걸음 — 회복학습 데이터 V8.2.31','learning header')
old='''        "actions": [\n          {\n            "type": "smart-hov",\n            "label": "HOV 가치의 계층 작성하기"\n          },'''
new='''        "actions": [\n          {\n            "type": "smart-importance-confidence",\n            "label": "중요성 · 자신감 빠른 점검"\n          },\n          {\n            "type": "smart-hov",\n            "label": "HOV 가치의 계층 작성하기"\n          },'''
l=replace_once(l,old,new,'Point1 learning action')
old='''        "actions": [\n          {\n            "type": "smart-deads",\n            "label": "DEADS 대처계획·실행하기"\n          },'''
new='''        "actions": [\n          {\n            "type": "urge-coping",\n            "label": "지금 충동 대처 시작하기"\n          },\n          {\n            "type": "smart-deads",\n            "label": "DEADS 대처계획·실행하기"\n          },'''
l=replace_once(l,old,new,'Point2 learning action')
learn.write_text(l,encoding='utf-8')

w=sw.read_text(encoding='utf-8')
w=replace_once(w,"const APP_VERSION = 'V8.2.30';","const APP_VERSION = 'V8.2.31';",'SW app version')
w=replace_once(w,"const V = 'ohg-v8230-smart-health';","const V = 'ohg-v8231-smart-integration';",'SW cache')
sw.write_text(w,encoding='utf-8')

r=readme.read_text(encoding='utf-8')
intro='''# V8.2.31 — SMART Recovery 전체 앱 통합\n\n- SMART Recovery 4-Point 학습과 실천도구를 핸드북 본문·부록 D 기준으로 다시 대조했습니다.\n- Point 1의 학습에만 있고 실천도구에 빠져 있던 `중요성 · 자신감 빠른 점검`을 연결했습니다.\n- Point 2의 `충동에 대처하기`는 새 도구를 중복 생성하지 않고 기존 충동 강도·버티기 타이머·호흡·전후 강도 흐름으로 연결합니다.\n- `주간 플래너`는 기존 생활 일정·습관, `브레인스토밍`은 문제 해결 5단계, `즐거운 활동 체크리스트`는 VACI 안의 기존 기능을 계속 사용합니다.\n- 역할극·거절기술·자기수용·동기유지 등 부록의 독립 후보는 필요성 검토 후 별도 버전에서 다룹니다.\n- `DATA_SCHEMA=6`, 개인 회복기록 Local-first, Android 이완 TTS·속도선택, 정확알림 엔진은 변경하지 않습니다.\n\n'''
if r.startswith('# V8.2.31'):
    raise SystemExit('README already patched')
r=intro+r
readme.write_text(r,encoding='utf-8')

print('V8.2.31 SMART integration patch applied')