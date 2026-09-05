from pathlib import Path
import json

idx = Path('index.html')
learn = Path('learning-data.js')
sw = Path('sw.js')

idx_text = idx.read_text(encoding='utf-8')
learn_text = learn.read_text(encoding='utf-8')
sw_text = sw.read_text(encoding='utf-8')

# Version only; no personal data schema change in this learning-only release.
idx_text = idx_text.replace("const BUILD = 'V8.2.2';", "const BUILD = 'V8.2.3';", 1)
sw_text = sw_text.replace("const APP_VERSION = 'V8.2.2';", "const APP_VERSION = 'V8.2.3';", 1)
sw_text = sw_text.replace("const V = 'ohg-v822-urge-diary';", "const V = 'ohg-v823-smart-learning';", 1)
learn_text = learn_text.replace('/* 오늘 한 걸음 — 회복학습 데이터 V7.11', '/* 오늘 한 걸음 — 회복학습 데이터 V8.2.3', 1)

# Point 2 can open the already-proven local urge diary directly from a learning section.
needle = "function learningAction(type){\n  closeModal();\n"
if "type === 'urge-diary'" not in idx_text:
    if needle not in idx_text:
        raise SystemExit('learningAction anchor not found')
    idx_text = idx_text.replace(
        needle,
        needle + "  if(type === 'urge-diary'){ go('urge-diary'); return; }\n",
        1
    )

smart_topic = {
    "id": "smart-recovery",
    "title": "SMART Recovery",
    "icon": "check",
    "description": "동기·충동·생각과 감정·삶의 균형을 실용적인 도구로 살펴봅니다.",
    "longDescription": "사용자가 번역한 SMART Recovery 핸드북의 4-Point Program과 도구 체계를 바탕으로 모바일 학습용으로 요약·재구성했습니다. 네 가지 Point는 순서대로 끝내는 단계가 아니라, 지금 필요한 영역의 도구를 골라 반복해서 사용하는 회복의 틀입니다.",
    "status": "content-ready",
    "sourceNote": "사용자 번역 SMART Recovery 핸드북 기반 — 앱용 요약·재구성",
    "sections": [
        {
            "id": "smart-intro",
            "title": "SMART Recovery란 무엇인가",
            "icon": "globe",
            "summary": "자기관리와 회복훈련, 그리고 4-Point Program의 기본 방향을 살펴봅니다.",
            "body": [
                "SMART Recovery는 Self-Management and Recovery Training의 약자로, 회복에서 자신의 선택과 자기관리 역할을 강조하는 과학 기반 상호지원 접근입니다.",
                "SMART에서 사용하는 여러 도구는 인지행동치료(CBT), 합리적 정서행동치료(REBT), 동기강화 접근의 원리를 회복에 적용합니다. 전문적인 치료를 대신하기보다 필요할 때 치료와 함께 사용할 수 있는 실용적인 보조도구로 볼 수 있습니다.",
                "4-Point Program은 순서대로 통과해야 하는 단계가 아닙니다. 어떤 사람은 먼저 충동을 다루고, 어떤 사람은 동기나 삶의 균형부터 살펴볼 수 있습니다. 회복에는 한 가지 방법만 있는 것이 아니라 자신에게 도움이 되는 길을 찾아갈 수 있습니다."
            ],
            "reflection": [
                "지금 나에게 가장 필요한 것은 동기, 충동 대처, 생각과 감정 관리, 삶의 균형 중 무엇인가요?",
                "지금까지 나에게 도움이 되었던 회복 방법은 무엇이었나요?",
                "도움이 잘 되지 않았던 방법이 있다면 다른 도구를 시도해볼 수 있을까요?"
            ],
            "practice": "네 가지 Point 가운데 지금 가장 필요한 하나를 고르고, 그 이유를 한 문장으로 생각해보세요."
        },
        {
            "id": "smart-point1",
            "title": "Point 1 · 동기 부여 및 유지",
            "icon": "sprout",
            "summary": "내가 왜 변화를 원하는지 분명히 하고, 그 이유를 계속 기억하는 영역입니다.",
            "body": [
                "변화를 시작하는 것과 변화를 계속 유지하는 것은 서로 다른 어려움이 있습니다. 시간이 지나면 처음 겪었던 문제의 고통은 흐려지고, 중독행동이 주었던 단기적인 이익만 다시 크게 보일 수 있습니다.",
                "SMART는 나에게 중요한 가치와 현재 행동이 얼마나 맞는지 살펴보고, 변화의 장점과 어려움을 함께 검토하도록 돕습니다. 이를 위해 가치의 계층(HOV), 세 가지 질문, 변화계획, 비용-편익 분석(CBA), 중요성·자신감 척도 같은 도구를 사용합니다.",
                "동기는 늘 높은 상태로 유지되는 감정이 아니라 다시 확인하고 보강할 수 있는 대상입니다. 내가 바꾸려는 이유와 이미 생긴 변화를 구체적으로 적어두면 흔들릴 때 방향을 다시 잡는 데 도움이 됩니다."
            ],
            "reflection": [
                "내가 처음 변화를 원했던 가장 중요한 이유는 무엇이었나요?",
                "내 삶에서 중독행동보다 더 중요하게 지키고 싶은 것은 무엇인가요?",
                "지금까지 달라진 작은 변화 하나는 무엇인가요?"
            ],
            "practice": "오늘 내가 지키고 싶은 가치 한 가지와, 그 가치를 위해 할 수 있는 작은 행동 한 가지를 정해보세요."
        },
        {
            "id": "smart-point2",
            "title": "Point 2 · 충동에 대처하기",
            "icon": "wave",
            "summary": "충동의 패턴을 알아차리고, 행동으로 옮기기 전 다른 선택을 연습합니다.",
            "body": [
                "충동은 강하게 느껴질 수 있지만 그 자체가 행동을 반드시 결정하는 것은 아닙니다. 시간, 장소, 사람, 감정, 사건 같은 촉발요인을 기록하면 나에게 반복되는 패턴을 더 일찍 알아차릴 수 있습니다.",
                "충동일지는 언제 충동이 왔는지, 얼마나 강했고 얼마나 지속됐는지, 무엇이 촉발했는지, 어디에 누구와 있었는지, 어떻게 대처했는지를 돌아보는 도구입니다. 기록이 쌓이면 피하거나 준비해야 할 상황과 실제로 도움이 되었던 대처가 보이기 시작합니다.",
                "SMART에서는 DEADS처럼 지연하기, 촉발상황에서 벗어나기, 충동을 지나가게 두기, 다른 활동으로 주의를 돌리기, 건강한 생각과 행동으로 대체하기를 활용합니다. DISARM과 ABC는 충동을 부추기는 자기대화와 믿음을 알아차리고 다른 방식으로 바라보는 데 사용합니다."
            ],
            "reflection": [
                "내 충동은 주로 어떤 시간이나 상황에서 반복되나요?",
                "충동을 행동으로 옮기지 않고 지나간 경험이 있었나요? 그때 무엇이 도움이 되었나요?",
                "다음 충동이 올 때 가장 먼저 해볼 수 있는 행동은 무엇인가요?"
            ],
            "practice": "최근 충동 한 번을 떠올려 시간·장소·촉발요인·대처를 충동일기에 남겨보세요.",
            "actions": [{"type": "urge-diary", "label": "내 충동일기 열기"}]
        },
        {
            "id": "smart-point3",
            "title": "Point 3 · 생각·감정·행동 관리하기",
            "icon": "speak",
            "summary": "사건 자체와 그 사건을 해석하는 생각을 구분하고, 더 도움이 되는 반응을 찾습니다.",
            "body": [
                "힘든 사건이 생겼을 때 감정과 행동은 사건 하나만으로 정해지지 않습니다. 그 사건에 대해 내가 어떤 믿음과 자기대화를 하고 있는지가 감정과 선택에 큰 영향을 줄 수 있습니다.",
                "ABC는 활성화 사건(A), 신념과 생각(B), 감정·행동의 결과(C)를 구분해서 살펴봅니다. 이어서 도움이 되지 않는 믿음에 질문을 던지고(D), 더 현실적이고 균형 잡힌 새로운 생각(E)을 만들어볼 수 있습니다.",
                "이 영역에서는 비합리적 신념에 이의제기하는 DIB/DIBS, 도움이 되지 않는 사고방식 알아차리기, 무조건적 자기·타인·삶의 수용, 문제 해결, 역할연습과 거절기술 같은 도구도 활용합니다. 목적은 감정을 없애는 것이 아니라 감정 속에서도 더 도움이 되는 선택을 할 수 있도록 연습하는 것입니다."
            ],
            "reflection": [
                "최근 나를 가장 힘들게 한 사건에서 머릿속에 어떤 말이 떠올랐나요?",
                "그 생각에는 반드시, 절대로, 견딜 수 없어 같은 강한 요구가 포함되어 있었나요?",
                "같은 상황을 조금 더 균형 있게 본다면 어떤 문장으로 바꿀 수 있을까요?"
            ],
            "practice": "오늘 힘들었던 상황 하나를 A-사건, B-생각, C-감정과 행동으로 나누어 살펴보세요."
        },
        {
            "id": "smart-point4",
            "title": "Point 4 · 균형 잡힌 삶 살기",
            "icon": "people",
            "summary": "중독행동이 차지하던 자리를 의미·관계·건강·즐거움이 있는 삶으로 다시 채웁니다.",
            "body": [
                "중독행동을 줄이거나 멈추면 이전에 그 행동이 차지하던 시간과 관계에 큰 빈자리가 생길 수 있습니다. 회복은 그 빈자리를 단순히 참는 것이 아니라 더 건강하고 만족스러운 생활로 다시 채워가는 과정입니다.",
                "라이프스타일 평가와 Balance Pie는 건강, 가족, 일, 친구, 여가, 성장, 재정, 영적 삶처럼 중요한 영역의 만족도를 돌아보게 합니다. VACI와 즐거운 활동 도구는 몰입할 수 있는 건강한 관심사와 새로운 즐거움을 찾도록 돕습니다.",
                "SMART 목표와 주간 플래너는 원하는 변화를 구체적인 행동으로 바꾸는 데 사용합니다. 수면, 영양, 운동, 이완과 같은 기본적인 생활관리도 균형 잡힌 회복의 일부입니다. 목표는 완벽한 균형이 아니라 부족한 영역을 알아차리고 조금씩 조정하는 것입니다."
            ],
            "reflection": [
                "중독행동이 줄어들면서 생긴 빈 시간이나 빈자리가 있나요?",
                "지금 내 삶에서 가장 만족도가 낮고 더 돌보고 싶은 영역은 무엇인가요?",
                "예전에 즐겼지만 중단했거나 새로 시도해보고 싶은 활동은 무엇인가요?"
            ],
            "practice": "이번 주에 삶의 균형을 위해 늘리고 싶은 활동 하나와 줄이고 싶은 활동 하나를 정해보세요."
        }
    ]
}

if "id: 'smart-recovery'" not in learn_text and '"id": "smart-recovery"' not in learn_text:
    end = learn_text.rfind('\n];')
    if end < 0:
        raise SystemExit('LEARNING_TOPICS end not found')
    payload = json.dumps(smart_topic, ensure_ascii=False, indent=2)
    learn_text = learn_text[:end] + ',\n  ' + payload.replace('\n', '\n  ') + learn_text[end:]

idx.write_text(idx_text, encoding='utf-8')
learn.write_text(learn_text, encoding='utf-8')
sw.write_text(sw_text, encoding='utf-8')

# Focused assertions
assert "const BUILD = 'V8.2.3';" in idx_text
assert "type === 'urge-diary'" in idx_text
assert '"id": "smart-recovery"' in learn_text
assert '"id": "smart-point1"' in learn_text
assert '"id": "smart-point2"' in learn_text
assert '"id": "smart-point3"' in learn_text
assert '"id": "smart-point4"' in learn_text
assert "const APP_VERSION = 'V8.2.3';" in sw_text
assert "ohg-v823-smart-learning" in sw_text
print('V8.2.3 SMART Recovery learning patch PASS')
