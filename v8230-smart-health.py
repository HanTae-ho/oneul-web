from pathlib import Path


def replace_one(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    return text.replace(old, new, 1)

# index.html
p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = replace_one(s, "const BUILD = 'V8.2.29';", "const BUILD = 'V8.2.30';", 'BUILD')

health_page = r'''<!-- ══════════ SMART Recovery · 건강 회복 · 생활 돌보기 V8.2.30 ══════════ -->
<section class="pg" id="p-smart-health">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">건강 회복 · 생활 돌보기</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back onclick="appBack('smart-tools')">← SMART 실천도구</button>
  </div>
  <div class="note" style="margin-bottom:12px">
    건강을 돌보는 일을 새 기록으로 하나 더 만들지 않습니다. <b>식사 · 운동 · 수면 · 복약과 치료 · 미루기</b>를 살펴보고, 이미 있는 생활 일정·습관·치료 일정·SMART 목표로 바로 이어갑니다.
  </div>
  <div id="smart-health-role-note"></div>

  <div class="card tight">
    <h3>식사</h3>
    <p class="muted" style="margin:-4px 0 11px">규칙적인 식사와 균형 잡힌 식사는 건강한 생활의 기본입니다. 앱에서는 식사 시간을 기존 생활 일정에서 정합니다.</p>
    <button class="btn sec sm" id="smart-health-food">식사 · 생활 일정으로</button>
  </div>

  <div class="card tight">
    <h3>운동</h3>
    <p class="muted" style="margin:-4px 0 11px">운동은 꼭 격렬할 필요가 없습니다. 걷기처럼 지속할 수 있는 움직임부터 시작하고, 오래 쉬었다면 서서히 늘려갑니다.</p>
    <button class="btn sec sm" id="smart-health-exercise">운동을 습관으로</button>
  </div>

  <div class="card tight">
    <h3>수면</h3>
    <p class="muted" style="margin:-4px 0 11px">회복 초기에는 수면 패턴이 달라지고 적응에 시간이 걸릴 수 있습니다. 앱에서는 잠 시간을 생활 일정에서 정하고 몸 기록에서 흐름을 돌아봅니다.</p>
    <button class="btn sec sm" id="smart-health-sleep">잠 · 생활 일정으로</button>
  </div>

  <div class="card tight" id="smart-health-treatment-card">
    <h3>복약 · 치료</h3>
    <p class="muted" style="margin:-4px 0 11px">SMART는 법적으로 처방된 정신과·중독 치료 약물과 전문적 치료의 사용을 지지합니다. 앱에서는 복약과 외래를 기존 치료 일정에서 관리합니다.</p>
    <button class="btn sec sm" id="smart-health-treatment">복약 · 치료 일정 관리</button>
  </div>

  <div class="card tight">
    <h3>미루기</h3>
    <p class="muted" style="margin:-4px 0 11px">미루기는 누구에게나 있지만, 과해지면 생활을 방해하는 습관이 될 수 있습니다. 해야 할 일을 작게 나누어 실행 가능한 SMART 목표로 바꿔봅니다.</p>
    <button class="btn sec sm" id="smart-health-procrastination">SMART 목표로 정리하기</button>
  </div>

  <button class="btn ghost" id="smart-health-bodylog">내 몸 기록 보기</button>
</section>

'''
marker = '<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->'
s = replace_one(s, marker, health_page + marker, 'health page insertion')

old_tab = "|| p === 'smart-goal' || p === 'smart-relax' || p === 'smart-tools') ? 'tools' : p;"
new_tab = "|| p === 'smart-goal' || p === 'smart-relax' || p === 'smart-health' || p === 'smart-tools') ? 'tools' : p;"
s = replace_one(s, old_tab, new_tab, 'tab route')

old_draw = "  if(p === 'smart-relax') drawSmartRelax();\n  if(p === 'smart-tools') drawSmartTools();"
new_draw = "  if(p === 'smart-relax') drawSmartRelax();\n  if(p === 'smart-health') drawSmartHealth();\n  if(p === 'smart-tools') drawSmartTools();"
s = replace_one(s, old_draw, new_draw, 'draw route')

old_label = "    'smart-goal':'SMART 목표 설정',\n    'smart-relax':'이완 · 마음 가라앉히기'"
new_label = "    'smart-goal':'SMART 목표 설정',\n    'smart-relax':'이완 · 마음 가라앉히기',\n    'smart-health':'건강 회복 · 생활 돌보기'"
s = replace_one(s, old_label, new_label, 'back label')

old_fallback = "'smart-balance-pie':'smart-balance-pie', 'smart-vaci':'smart-vaci', 'smart-goal':'smart-goal', 'smart-relax':'smart-relax'"
new_fallback = "'smart-balance-pie':'smart-balance-pie', 'smart-vaci':'smart-vaci', 'smart-goal':'smart-goal', 'smart-relax':'smart-relax', 'smart-health':'smart-health'"
s = replace_one(s, old_fallback, new_fallback, 'back fallback')

old_menu = "smartToolButton('SMART 목표 설정','삶의 영역·가치 → 목표 → SMART 5기준 → 실행 행동','smart-goal','check')+smartToolButton('이완 · 마음 가라앉히기','알아차림 → PMR · 심상화 · 명상 중 하나 사용하기','smart-relax','sprout')+'</div>';"
new_menu = "smartToolButton('SMART 목표 설정','삶의 영역·가치 → 목표 → SMART 5기준 → 실행 행동','smart-goal','check')+smartToolButton('이완 · 마음 가라앉히기','알아차림 → PMR · 심상화 · 명상 중 하나 사용하기','smart-relax','sprout')+smartToolButton('건강 회복 · 생활 돌보기','식사 · 운동 · 수면 · 복약 · 미루기를 기존 기능으로 연결','smart-health','check')+'</div>';"
s = replace_one(s, old_menu, new_menu, 'Point 4 menu')

health_js = r'''function drawSmartHealth(){
 const rn=$('#smart-health-role-note'),food=$('#smart-health-food'),ex=$('#smart-health-exercise'),sleep=$('#smart-health-sleep'),tc=$('#smart-health-treatment-card'),tr=$('#smart-health-treatment'),pro=$('#smart-health-procrastination'),body=$('#smart-health-bodylog');
 if(rn)rn.innerHTML=famMode()?'<div class="note" style="margin-bottom:12px"><b>가족도 자신의 생활과 건강을 돌봅니다.</b><br>상대의 식사·수면·복약을 확인하거나 관리하는 화면이 아니라, 가족인 내가 내 몸과 생활을 챙기는 데 사용합니다.</div>':'';
 if(tc)tc.classList.toggle('hide',famMode());
 if(food)food.onclick=()=>go('life-schedule');
 if(ex)ex.onclick=()=>go('habit');
 if(sleep)sleep.onclick=()=>go('life-schedule');
 if(tr)tr.onclick=()=>go('treatment');
 if(pro)pro.onclick=()=>go('smart-goal');
 if(body)body.onclick=()=>{recTab='body';go('rec');};
}

'''
s = replace_one(s, 'function learningAction(type,sectionId){', health_js + 'function learningAction(type,sectionId){', 'health draw function')

old_action = "  if(type === 'smart-relax'){ go('smart-relax'); return; }"
new_action = "  if(type === 'smart-relax'){ go('smart-relax'); return; }\n  if(type === 'smart-health'){ go('smart-health'); return; }"
s = replace_one(s, old_action, new_action, 'learning action')

p.write_text(s, encoding='utf-8')

# learning-data.js
p = Path('learning-data.js')
s = p.read_text(encoding='utf-8')
s = replace_one(s, '/* 오늘 한 걸음 — 회복학습 데이터 V8.2.26', '/* 오늘 한 걸음 — 회복학습 데이터 V8.2.30', 'learning header')
old_learning = '''          {
            "type": "smart-relax",
            "label": "이완 · 마음 가라앉히기"
          }
        ]'''
new_learning = '''          {
            "type": "smart-relax",
            "label": "이완 · 마음 가라앉히기"
          },
          {
            "type": "smart-health",
            "label": "건강 회복 · 생활 돌보기"
          }
        ]'''
s = replace_one(s, old_learning, new_learning, 'learning Point 4 action')
p.write_text(s, encoding='utf-8')

# sw.js
p = Path('sw.js')
s = p.read_text(encoding='utf-8')
s = replace_one(s, "const APP_VERSION = 'V8.2.29';", "const APP_VERSION = 'V8.2.30';", 'SW version')
s = replace_one(s, "const V = 'ohg-v8229-relax-rate';", "const V = 'ohg-v8230-smart-health';", 'SW cache')
p.write_text(s, encoding='utf-8')

print('V8.2.30 SMART health hub patch applied')
