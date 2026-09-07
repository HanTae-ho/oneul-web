from pathlib import Path

root=Path('.')
idx=root/'index.html'
learn=root/'learning-data.js'
sw=root/'sw.js'
readme=root/'README.md'

def once(text, old, new, label):
    n=text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    return text.replace(old,new,1)

# ── index.html ──
s=idx.read_text(encoding='utf-8')
s=once(s,"const BUILD = 'V8.2.31';","const BUILD = 'V8.2.32';",'BUILD')

# Family guide -> existing tools. No new storage or worksheet.
links={
"    {h:'돕는 것과 대신 치워주는 것은 다릅니다',\n     b:":"    {h:'돕는 것과 대신 치워주는 것은 다릅니다', a:'smart-cba', al:'내 행동 CBA로 살펴보기',\n     b:",
"    {h:'말할 때는 그 사람이 아니라 일에 대해',\n     b:":"    {h:'말할 때는 그 사람이 아니라 일에 대해', a:'smart-abc', al:'내 반응을 ABC로 살펴보기',\n     b:",
"    {h:'가족도 아픕니다',\n     b:":"    {h:'가족도 아픕니다', a:'smart-health', al:'내 생활과 건강 돌보기',\n     b:",
"    {h:'가족 모임에는 혼자 가도 됩니다',\n     b:":"    {h:'가족 모임에는 혼자 가도 됩니다', a:'family-meet', al:'가족 모임 찾아보기',\n     b:",
"    {h:'감시가 삶의 전부가 되지 않게',\n     b:":"    {h:'감시가 삶의 전부가 되지 않게', a:'smart-balance-pie', al:'내 삶의 균형 살펴보기',\n     b:",
"    {h:'나의 기대를 내려놓고, 그의 눈으로 봐주세요',\n     b:":"    {h:'나의 기대를 내려놓고, 그의 눈으로 봐주세요', a:'smart-abc', al:'내 생각과 반응 살펴보기',\n     b:",
"    {h:'혼자 지고 계시면 상담을 받으세요',\n     b:":"    {h:'혼자 지고 계시면 상담을 받으세요', a:'help', al:'헬프에서 도움 찾기',\n     b:"
}
for old,new in links.items():
    s=once(s,old,new,'family guide link '+old.split("'")[1])

marker="""let famI = 0;\n\nfunction drawFam(){"""
helper="""let famI = 0;\n\n/* V8.2.32: 가족 안내는 새 워크시트를 늘리지 않고 이미 있는 도구로 이어집니다. */\nfunction familyGuideActionHTML(x){\n  if(!x || !x.a) return '';\n  return '<div style=\"height:14px\"></div><button class=\"btn sec sm\" id=\"fam-guide-action\">'+esc(x.al||'이어보기')+'</button>';\n}\nfunction familyGuideRun(action){\n  if(action==='family-meet'){\n    mt.target='fam'; mt.mode='today'; mt.q=''; mt.kind=''; mt.todayArea=''; go('meet'); return;\n  }\n  if(action==='help'){ go('help'); return; }\n  if(['smart-cba','smart-abc','smart-balance-pie','smart-health'].includes(action)){ go(action); return; }\n}\n\nfunction drawFam(){"""
s=once(s,marker,helper,'family guide helper')
old="""  $('#fam-body').innerHTML = x\n    ? '<div class=\"rdcard\"><h3>' + esc(x.h) + '</h3>' + para(x.b) + '</div>'\n    : '';\n\n  $('#fam-pos').textContent"""
new="""  $('#fam-body').innerHTML = x\n    ? '<div class=\"rdcard\"><h3>' + esc(x.h) + '</h3>' + para(x.b) + familyGuideActionHTML(x) + '</div>'\n    : '';\n  const ga=$('#fam-guide-action'); if(ga && x) ga.onclick=()=>familyGuideRun(x.a);\n\n  $('#fam-pos').textContent"""
s=once(s,old,new,'family guide action render')

old="""  const practice=$('#learn-topic-practice');\n  if(practice){\n    practice.innerHTML = topic.id==='smart-recovery' ? '<button class=\"btn sec\" id=\"learn-smart-tools\" style=\"margin-bottom:12px\">SMART 실천도구 열기</button>' : '';\n    const sb=$('#learn-smart-tools'); if(sb) sb.onclick=()=>go('smart-tools');\n  }"""
new="""  const practice=$('#learn-topic-practice');\n  if(practice){\n    const famSmart=topic.id==='smart-recovery' && famMode();\n    practice.innerHTML = topic.id==='smart-recovery'\n      ? (famSmart ? '<div class=\"note\" style=\"margin-bottom:12px\"><b>가족모드에서는 내 삶과 내 반응을 중심으로 사용합니다.</b><br>SMART 4-Point를 참고하되, Point 2의 충동대응·충동일지는 충동을 직접 경험하는 당사자의 도구입니다. 가족이 상대의 충동을 기록하거나 감시하는 데 사용하지 않습니다.</div>' : '')\n        + '<button class=\"btn sec\" id=\"learn-smart-tools\" style=\"margin-bottom:12px\">SMART 실천도구 열기</button>'\n      : '';\n    const sb=$('#learn-smart-tools'); if(sb) sb.onclick=()=>go('smart-tools');\n  }"""
s=once(s,old,new,'SMART family learning intro')
idx.write_text(s,encoding='utf-8')

# ── learning-data.js ──
l=learn.read_text(encoding='utf-8')
l=once(l,'/* 오늘 한 걸음 — 회복학습 데이터 V8.2.31','/* 오늘 한 걸음 — 회복학습 데이터 V8.2.32','learning header')

old='''        "practice": "네 가지 Point 가운데 지금 가장 필요한 하나를 고르고, 그 이유를 한 문장으로 생각해보세요."\n      },\n      {\n        "id": "smart-point1",'''
new='''        "practice": "네 가지 Point 가운데 지금 가장 필요한 하나를 고르고, 그 이유를 한 문장으로 생각해보세요.",\n        "perspectives": {\n          "family": {\n            "summary": "SMART 4-Point를 가족 자신의 생각·행동·생활을 돌아보는 참고 틀로 사용합니다.",\n            "body": [\n              "가족모드에서 SMART Recovery는 상대를 바꾸거나 회복을 관리하는 프로그램으로 사용하지 않습니다. 가족인 내가 어떤 생각과 반응을 하고 있는지, 무엇을 중요하게 여기며 어떻게 내 삶을 지킬지를 돌아보는 데 도움이 되는 도구만 골라 사용합니다.",\n              "Point 1의 가치와 변화, Point 3의 생각·감정·행동, Point 4의 삶의 균형 도구는 가족 자신의 문제에 적용할 수 있습니다. 반면 Point 2의 충동대응·충동일지는 충동을 직접 경험하는 당사자의 도구이므로 가족이 상대의 상태를 기록하거나 감시하는 데 사용하지 않습니다.",\n              "가족의 회복은 상대가 얼마나 빨리 달라지는지로 평가하지 않습니다. 내가 직접 선택할 수 있는 행동, 안전, 경계, 자기돌봄과 생활을 중심으로 필요한 도구를 골라 사용합니다."\n            ],\n            "reflection": [\n              "요즘 상대의 행동을 바꾸려는 데 내 시간과 마음이 얼마나 붙들려 있나요?",\n              "지금 내가 직접 선택하거나 바꿀 수 있는 것은 무엇인가요?",\n              "내 가치·생각과 반응·삶의 균형 가운데 지금 가장 먼저 돌보고 싶은 것은 무엇인가요?"\n            ],\n            "practice": "오늘 상대의 행동이 아니라 내가 직접 선택할 수 있는 작은 행동 한 가지를 정해보세요."\n          }\n        }\n      },\n      {\n        "id": "smart-point1",'''
l=once(l,old,new,'SMART intro family perspective')

old='''        "practice": "최근 충동 한 번을 떠올려 시간·장소·촉발요인·대처를 충동일기에 남겨보세요.",\n        "actions": [\n          {\n            "type": "urge-coping",\n            "label": "지금 충동 대처 시작하기"\n          },\n          {\n            "type": "smart-deads",\n            "label": "DEADS 대처계획·실행하기"\n          },\n          {\n            "type": "smart-disarm",\n            "label": "DISARM 충동의 목소리 다루기"\n          },\n          {\n            "type": "urge-diary",\n            "label": "내 충동일기 열기"\n          }\n        ]\n      },\n      {\n        "id": "smart-point3",'''
new='''        "practice": "최근 충동 한 번을 떠올려 시간·장소·촉발요인·대처를 충동일기에 남겨보세요.",\n        "actions": [\n          {\n            "type": "urge-coping",\n            "label": "지금 충동 대처 시작하기"\n          },\n          {\n            "type": "smart-deads",\n            "label": "DEADS 대처계획·실행하기"\n          },\n          {\n            "type": "smart-disarm",\n            "label": "DISARM 충동의 목소리 다루기"\n          },\n          {\n            "type": "urge-diary",\n            "label": "내 충동일기 열기"\n          }\n        ],\n        "perspectives": {\n          "family": {\n            "summary": "당사자의 충동을 이해하기 위한 참고 영역이며, 가족이 상대의 충동을 기록하거나 관리하지 않습니다.",\n            "body": [\n              "Point 2의 충동은 중독행동을 직접 경험하는 당사자의 회복 영역입니다. 가족이 상대의 충동 강도, 촉발상황, 대처를 대신 기록하거나 관리하는 것은 가족모드의 목적이 아닙니다.",\n              "가족에게 이 내용은 상대가 강한 충동을 경험할 수 있고 그 충동과 행동이 같은 것은 아니라는 점을 이해하는 참고가 될 수 있습니다. 그러나 상대가 지금 얼마나 충동적인지 확인하거나 DEADS·DISARM을 대신 적용하려고 하지는 않습니다.",\n              "상대의 행동 때문에 내가 불안·분노·두려움에 휩싸인다면, 가족인 나는 Point 3의 ABC·사고방식·문제해결처럼 내 생각과 반응을 다루는 도구를 사용하는 편이 맞습니다."\n            ],\n            "reflection": [\n              "상대의 상태를 계속 확인하거나 예측하려 할 때 나는 어떤 감정과 행동을 보이나요?",\n              "상대의 몫과 내가 직접 선택할 수 있는 내 몫을 어떻게 구분할 수 있을까요?",\n              "지금 내 반응을 돌아보기 위해 ABC나 문제해결이 도움이 될 상황이 있나요?"\n            ],\n            "practice": "상대의 충동을 기록하지 말고, 최근 힘들었던 상황에서 내가 느낀 감정과 내가 한 반응을 한 줄로 적어보세요.",\n            "actions": []\n          }\n        }\n      },\n      {\n        "id": "smart-point3",'''
l=once(l,old,new,'SMART Point2 family perspective')
learn.write_text(l,encoding='utf-8')

# ── sw.js ──
w=sw.read_text(encoding='utf-8')
w=once(w,"const APP_VERSION = 'V8.2.31';","const APP_VERSION = 'V8.2.32';",'SW version')
w=w.replace("const V = 'ohg-v8231-smart-integration';","const V = 'ohg-v8232-family-integration-links';",1)
if "ohg-v8232-family-integration-links" not in w: raise SystemExit('SW cache marker not patched')
sw.write_text(w,encoding='utf-8')

# ── README ──
r=readme.read_text(encoding='utf-8')
intro='''# V8.2.32 — 가족모드 통합 정합성 · 기존 도구 연결\n\n- 가족 SMART를 별도 Family & Friends 프로그램으로 재편하지 않고 `오늘 한 걸음`의 기존 가족 원칙을 유지합니다.\n- SMART 학습에서 가족모드 안내를 추가하고, Point 2는 당사자의 충동을 이해하기 위한 참고 영역으로 분리합니다. 가족에게 충동대응·DEADS·DISARM·충동일기 실행 버튼을 제공하지 않습니다.\n- 가족 안내 18편 중 실제 연결 가치가 높은 글만 기존 CBA·ABC·밸런스 파이·건강회복·가족모임·헬프로 연결합니다. 새 기록체계나 새 워크시트는 추가하지 않습니다.\n- 가족의 회복일·충동·재발 비기록, 가족 자신의 안전·경계·생활 중심 원칙을 그대로 유지합니다.\n- `DATA_SCHEMA=6`, 기존 SMART/12단계 가족 기록, Android 이완 TTS·속도선택, 정확알림 엔진은 변경하지 않습니다.\n\n'''
if r.startswith('# V8.2.32'): raise SystemExit('README already patched')
readme.write_text(intro+r,encoding='utf-8')
print('V8.2.32 family integration patch applied')