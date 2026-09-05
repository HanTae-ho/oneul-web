from pathlib import Path

idx=Path('index.html'); sw=Path('sw.js')
s=idx.read_text(encoding='utf-8'); st=sw.read_text(encoding='utf-8')

assert "const BUILD = 'V8.2.10';" in s
s=s.replace("const BUILD = 'V8.2.10';","const BUILD = 'V8.2.11';",1)

anchor='''    <button class="toolcard" id="tool-capsule" style="margin-top:9px">\n      <span class="ic" data-ico="speak"></span>\n      <span class="b"><b>미래의 나에게</b><span id="tool-capsule-s">회복을 시작한 마음을 남겨두기</span></span>\n      <span class="go">열기</span>\n    </button>'''
assert anchor in s
insert='''    <button class="toolcard" id="tool-smart-tools" style="margin-top:9px">\n      <span class="ic" data-ico="check"></span>\n      <span class="b"><b>SMART 실천도구</b><span id="tool-smart-tools-s">HOV · 변화계획 · CBA · DEADS · DISARM</span></span>\n      <span class="go">열기</span>\n    </button>\n'''
s=s.replace(anchor,insert+anchor,1)

page_anchor='''<!-- ══════════ SMART Recovery · HOV V8.2.5 ══════════ -->'''
assert page_anchor in s
page='''<!-- ══════════ SMART Recovery · 실천도구 허브 V8.2.11 ══════════ -->\n<section class="pg" id="p-smart-tools">\n  <div class="sp" style="margin-bottom:11px">\n    <h1 style="margin:0">SMART 실천도구</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('tools')">← 회복도구</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    SMART Recovery의 4-Point는 순서대로 통과하는 단계가 아닙니다. <b>지금 필요한 영역</b>을 골라 배우고, 작성하고, 다시 사용할 수 있습니다. 작성 내용은 기존 원칙대로 <b>이 기기에만 저장</b>됩니다.\n  </div>\n  <button class="btn sec" id="smart-tools-learn">SMART Recovery 설명 보기</button>\n  <div id="smart-tools-body" style="margin-top:14px"></div>\n</section>\n\n'''
s=s.replace(page_anchor,page+page_anchor,1)

# Back buttons return to the actual previous context when possible.
s=s.replace("onclick=\"go('learn-topic')\">← SMART Recovery</button>","onclick=\"appBack('smart-tools')\">← SMART Recovery</button>")

learn_desc='<p class="muted" style="margin:-2px 0 14px" id="learn-topic-desc"></p>\n  <div class="learnlist" id="learn-topic-sections"></div>'
assert learn_desc in s
s=s.replace(learn_desc,'<p class="muted" style="margin:-2px 0 14px" id="learn-topic-desc"></p>\n  <div id="learn-topic-practice"></div>\n  <div class="learnlist" id="learn-topic-sections"></div>',1)

old="|| p === 'smart-deads' || p === 'smart-disarm') ? 'tools' : p;"
assert old in s
s=s.replace(old,"|| p === 'smart-deads' || p === 'smart-disarm' || p === 'smart-tools') ? 'tools' : p;",1)
route="  if(p === 'smart-disarm') drawSmartDisarm();\n"
assert route in s
s=s.replace(route,route+"  if(p === 'smart-tools') drawSmartTools();\n",1)

fn_anchor='''/* ══════════ SMART Recovery · 가치의 계층(HOV) V8.2.5 ══════════'''
assert fn_anchor in s
block=r'''/* ══════════ SMART Recovery · 실천도구 허브 V8.2.11 ══════════ */
function smartToolButton(title,desc,page,icon){
  return '<button class="schedulecard" style="margin-bottom:8px" data-smart-page="'+esc(page)+'">'
    +'<span class="ic" data-ico="'+esc(icon||'check')+'"></span>'
    +'<span class="b"><b>'+esc(title)+'</b><span>'+esc(desc)+'</span></span><span class="go">›</span></button>';
}
function drawSmartTools(){
  const box=$('#smart-tools-body'), learn=$('#smart-tools-learn'); if(!box) return;
  if(learn) learn.onclick=()=>{ learnState.topic='smart-recovery'; go('learn-topic'); };
  const p1=[
    ['가치의 계층 HOV','내 삶에서 중요한 가치와 현재 행동의 방향을 확인','smart-hov','sprout'],
    ['나의 3가지 질문','원하는 미래와 현재 행동의 차이를 변화 동기로 연결','smart-three-questions','speak'],
    ['변화 계획 워크시트','변화 이유·단계·도움·진전의 신호·방해요인을 계획','smart-change-plan','cal'],
    ['비용-편익 분석 CBA','사용·중단의 좋은 점과 대가를 함께 비교','smart-cba','check']
  ];
  const p2=[
    ['DEADS · 충동 대처','충동 순간에 사용할 행동 전략을 미리 정하고 실행','smart-deads','wave'],
    ['DISARM · 충동의 목소리','충동을 부추기는 자기대화를 알아차리고 거부·대체','smart-disarm','speak'],
    ['내 충동일기','시간·상황·촉발요인·대처를 기록하고 패턴 확인','urge-diary','wave']
  ];
  let h='<div class="card"><h3>Point 1 · 동기 부여 및 유지</h3><p class="muted" style="margin:-4px 0 11px">왜 바꾸려는지, 무엇을 지키려는지, 어떻게 바꿀지를 정리합니다.</p>';
  h+=p1.map(x=>smartToolButton(x[0],x[1],x[2],x[3])).join('')+'</div>';
  h+='<div class="card"><h3>Point 2 · 충동에 대처하기</h3><p class="muted" style="margin:-4px 0 11px">충동을 기록하고, 지금 사용할 수 있는 대처를 준비합니다.</p>';
  if(famMode()){
    h+='<div class="note">DEADS·DISARM·충동일기는 충동을 직접 경험하는 당사자를 위한 도구입니다. 가족모드에서는 상대의 충동을 감시하거나 통제하는 기능으로 사용하지 않습니다.</div>';
  }else{
    h+=p2.map(x=>smartToolButton(x[0],x[1],x[2],x[3])).join('');
  }
  h+='</div>';
  h+='<div class="card"><h3>Point 3 · 생각·감정·행동 관리하기</h3><p class="muted" style="margin:-4px 0 0">ABC · DIB/DIBS 등 작성형 도구를 순차적으로 추가할 예정입니다.</p><div class="tiny" style="margin-top:8px">준비 중</div></div>';
  h+='<div class="card"><h3>Point 4 · 균형 잡힌 삶 살기</h3><p class="muted" style="margin:-4px 0 0">생활 균형 · 가치에 맞는 활동 · 목표와 주간계획 도구를 순차적으로 추가할 예정입니다.</p><div class="tiny" style="margin-top:8px">준비 중</div></div>';
  box.innerHTML=h;
  box.querySelectorAll('[data-smart-page]').forEach(b=>b.onclick=()=>go(b.dataset.smartPage));
  hydrateIcons(box);
}

'''
s=s.replace(fn_anchor,block+fn_anchor,1)

draw_anchor="  $('#learn-topic-desc').textContent=topic.longDescription || topic.description || '';\n  const box=$('#learn-topic-sections'); box.innerHTML='';"
assert draw_anchor in s
s=s.replace(draw_anchor,"  $('#learn-topic-desc').textContent=topic.longDescription || topic.description || '';\n  const practice=$('#learn-topic-practice');\n  if(practice){\n    practice.innerHTML = topic.id==='smart-recovery' ? '<button class=\"btn sec\" id=\"learn-smart-tools\" style=\"margin-bottom:12px\">SMART 실천도구 열기</button>' : '';\n    const sb=$('#learn-smart-tools'); if(sb) sb.onclick=()=>go('smart-tools');\n  }\n  const box=$('#learn-topic-sections'); box.innerHTML='';",1)

event="$('#tool-learn').onclick = () => go('learn');\n"
assert event in s
s=s.replace(event,event+"$('#tool-smart-tools').onclick = () => go('smart-tools');\n",1)

assert "const APP_VERSION = 'V8.2.10';" in st
assert "const V = 'ohg-v8210-smart-disarm';" in st
st=st.replace("const APP_VERSION = 'V8.2.10';","const APP_VERSION = 'V8.2.11';",1)
st=st.replace("const V = 'ohg-v8210-smart-disarm';","const V = 'ohg-v8211-smart-tools-hub';",1)

idx.write_text(s,encoding='utf-8'); sw.write_text(st,encoding='utf-8')
print('V8.2.11 SMART tools hub patch applied')
