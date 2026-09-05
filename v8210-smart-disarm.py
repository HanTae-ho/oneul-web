from pathlib import Path

idx=Path('index.html'); learn=Path('learning-data.js'); sw=Path('sw.js')
s=idx.read_text(encoding='utf-8'); ld=learn.read_text(encoding='utf-8'); st=sw.read_text(encoding='utf-8')

assert "const BUILD = 'V8.2.9';" in s
assert "const DATA_SCHEMA = 6;" in s
s=s.replace("const BUILD = 'V8.2.9';","const BUILD = 'V8.2.10';",1)

# Add DISARM page after DEADS, before Future Self.
page_anchor='<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->'
assert page_anchor in s
page=r'''<!-- ══════════ SMART Recovery · DISARM V8.2.10 ══════════ -->
<section class="pg" id="p-smart-disarm">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">DISARM · 충동의 목소리 분리하기</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="go('learn-topic')">← SMART Recovery</button>
  </div>
  <div class="note" style="margin-bottom:12px">
    <b>DISARM(Destructive Images and Self-talk Awareness and Refusal Method)</b>은 충동을 부추기는 파괴적인 이미지·자기대화를 알아차리고, 현실적이고 건설적인 생각으로 거부·대체하는 도구입니다. 충동이나 그 목소리에 이름을 붙이는 것은 <b>선택</b>이며, 내 계획은 <b>이 기기에만 저장</b>됩니다.
  </div>
  <div id="smart-disarm-family-note"></div>
  <div id="smart-disarm-self-tools">
    <button class="btn" id="smart-disarm-now">지금 DISARM 사용하기</button>
    <div style="height:8px"></div>
    <button class="btn sec" id="smart-disarm-new">+ 내 DISARM 대처문장 만들기</button>
    <div style="height:8px"></div>
    <button class="btn ghost" onclick="go('urge-diary')">내 충동일기 열기</button>
    <div id="smart-disarm-list" style="margin-top:12px"></div>
  </div>
</section>

'''
s=s.replace(page_anchor,page+page_anchor,1)

# Keep Recovery Tools tab active for DISARM.
nav="|| p === 'smart-deads') ? 'tools'"
assert nav in s
s=s.replace(nav,"|| p === 'smart-deads' || p === 'smart-disarm') ? 'tools'",1)

draw="  if(p === 'smart-deads') drawSmartDeads();"
assert draw in s
s=s.replace(draw,draw+"\n  if(p === 'smart-disarm') drawSmartDisarm();",1)

# Add DISARM implementation immediately before learningAction.
fn_anchor='function learningAction(type){'
assert fn_anchor in s
block=r'''/* ── SMART Recovery · DISARM V8.2.10 ── */
function smartDisarmRecords(){
  return (Array.isArray(S.smartWorks)?S.smartWorks:[])
    .filter(r=>r && r.kind==='disarm' && (r.role||'self')==='self')
    .sort((a,b)=>(b.updatedAt||b.ts||0)-(a.updatedAt||a.ts||0));
}
function smartDisarmDate(ts){
  if(!ts) return '';
  const d=new Date(ts); return d.getFullYear()+'. '+(d.getMonth()+1)+'. '+d.getDate()+'.';
}
function drawSmartDisarm(){
  const fam=$('#smart-disarm-family-note'), tools=$('#smart-disarm-self-tools'), list=$('#smart-disarm-list');
  if(!fam||!tools) return;
  if(famMode()){
    fam.innerHTML='<div class="note"><b>가족을 위한 안내</b><br>DISARM은 충동을 직접 경험하는 사람이 자신의 파괴적 이미지·자기대화를 알아차리고 거부하는 도구입니다. 가족이 상대의 생각을 분석하거나 논박하고, 충동을 감시·통제하는 용도로 사용하지 않습니다.<div style="height:10px"></div><button class="btn ghost" onclick="go(\'learn-topic\')">SMART Recovery로 돌아가기</button></div>';
    tools.style.display='none'; return;
  }
  fam.innerHTML=''; tools.style.display='block';
  const now=$('#smart-disarm-now'), add=$('#smart-disarm-new');
  if(now) now.onclick=()=>openSmartDisarmNow();
  if(add) add.onclick=()=>openSmartDisarmEditor(null);
  if(!list) return;
  const rows=smartDisarmRecords();
  if(!rows.length){
    list.innerHTML='<div class="card"><b>아직 저장한 DISARM 대처문장이 없습니다.</b><p class="muted" style="margin:5px 0 0">평소에 반복되는 충동의 자기대화와 내가 할 현실적인 대답을 적어두면, 충동이 왔을 때 더 빨리 알아차리고 대응할 수 있습니다.</p></div>';
    return;
  }
  list.innerHTML='<div class="card"><h3>저장한 DISARM 대처문장 '+rows.length+'건</h3>'+rows.map(r=>'<div class="sp" style="gap:10px;padding:11px 0;border-top:1px solid var(--line)"><div style="min-width:0;flex:1"><div class="tiny">'+esc(smartDisarmDate(r.updatedAt||r.ts))+'</div><b style="display:block;margin-top:2px">'+esc(r.voiceName||'내 충동의 목소리')+'</b><div class="muted" style="margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(r.destructive||'')+'</div></div><button class="tiny" style="color:var(--acc);font-weight:600" onclick="openSmartDisarmView(\''+esc(r.id)+'\')">보기</button></div>').join('')+'</div>';
}
function smartDisarmField(title,id,value,placeholder,help){
  return '<div class="card"><label>'+esc(title)+'</label>'+(help?'<div class="tiny" style="margin:4px 0 7px">'+esc(help)+'</div>':'')+'<textarea id="'+id+'" maxlength="600" placeholder="'+esc(placeholder)+'">'+esc(value||'')+'</textarea></div>';
}
function openSmartDisarmEditor(record){
  if(famMode()) return;
  const r=record||{};
  modal('<h2>'+(record?'DISARM 대처문장 수정':'내 DISARM 대처문장 만들기')+'</h2>'
    +'<p class="muted" style="margin:5px 0 14px">핵심은 “나에게 어떤 생각·이미지가 나타나는가”를 알아차리고, 그것을 사실이나 명령처럼 따르지 않도록 현실적인 대답을 준비하는 것입니다. 이름 붙이기는 원할 때만 사용하세요.</p>'
    +smartDisarmField('충동의 목소리 이름 · 선택','disarm-name',r.voiceName,'예: 로비스트, 징징이, 유혹의 목소리','충동을 나 자신과 분리해서 빨리 알아차리는 데 도움이 된다면 이름을 붙일 수 있습니다. 꼭 필요하지는 않습니다.')
    +smartDisarmField('나를 끌어당기는 생각·이미지','disarm-destructive',r.destructive,'예: “오늘만 마시면 긴장이 풀릴 거야.”','반복해서 나타나는 말, 장면, 기대, 핑계를 가능한 그대로 적습니다.')
    +smartDisarmField('그 생각이 약속하는 것','disarm-promise',r.promise,'예: 편안함, 재미, 탈출, 외로움이 줄어듦','그 생각이 무엇을 얻을 수 있다고 유혹하는지 적습니다.')
    +smartDisarmField('현실 확인','disarm-reality',r.reality,'예: 잠깐 편해져도 다음 날 후회·갈등·몸 상태 악화가 반복됐다.','과거 경험과 실제 결과를 기준으로 그 약속을 현실적으로 점검합니다.')
    +smartDisarmField('단호한 거부 문장','disarm-refusal',r.refusal,'예: “아니. 이건 충동의 목소리일 뿐이고 나는 따르지 않는다.”','처음 속삭임을 알아차렸을 때 짧고 분명하게 거부할 말을 정합니다.')
    +smartDisarmField('현실적인 대체 생각·이미지','disarm-replacement',r.replacement,'예: “이 충동은 지나간다. 나는 5분만 다른 행동을 선택한다.”','파괴적인 자기대화를 더 건설적이고 현실적인 생각이나 이미지로 바꿉니다.')
    +'<button class="btn" id="disarm-save">'+(record?'수정 저장':'DISARM 대처문장 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
  $('#disarm-save').onclick=()=>{
    const rec={
      id:record?record.id:('disarm-'+Date.now()+'-'+Math.random().toString(36).slice(2,7)), kind:'disarm', role:'self',
      ts:record?(record.ts||Date.now()):Date.now(), updatedAt:Date.now(),
      voiceName:$('#disarm-name').value.trim(), destructive:$('#disarm-destructive').value.trim(), promise:$('#disarm-promise').value.trim(),
      reality:$('#disarm-reality').value.trim(), refusal:$('#disarm-refusal').value.trim(), replacement:$('#disarm-replacement').value.trim()
    };
    if(!rec.destructive){ toast('반복해서 나타나는 생각이나 이미지를 적어주세요.'); return; }
    if(!rec.refusal && !rec.replacement){ toast('거부 문장이나 현실적인 대체 생각을 하나 이상 적어주세요.'); return; }
    if(!Array.isArray(S.smartWorks)) S.smartWorks=[];
    if(record){ const i=S.smartWorks.findIndex(x=>x&&x.id===record.id); if(i>=0) S.smartWorks[i]=rec; else S.smartWorks.push(rec); }
    else S.smartWorks.push(rec);
    save(); closeModal(); drawSmartDisarm(); toast(record?'DISARM 대처문장을 수정했습니다.':'DISARM 대처문장을 저장했습니다.');
  };
}
function smartDisarmSection(title,text){
  return '<div class="card"><h3>'+esc(title)+'</h3><div style="white-space:pre-wrap">'+(String(text||'').trim()?esc(text):'<span class="muted">작성하지 않음</span>')+'</div></div>';
}
function openSmartDisarmView(id){
  const r=smartDisarmRecords().find(x=>x.id===id); if(!r) return;
  modal('<h2>'+esc(r.voiceName||'내 DISARM 대처문장')+'</h2><div class="muted" style="margin:-4px 0 12px">'+esc(smartDisarmDate(r.updatedAt||r.ts))+'</div>'
    +smartDisarmSection('나를 끌어당기는 생각·이미지',r.destructive)+smartDisarmSection('그 생각이 약속하는 것',r.promise)
    +smartDisarmSection('현실 확인',r.reality)+smartDisarmSection('단호한 거부 문장',r.refusal)+smartDisarmSection('현실적인 대체 생각·이미지',r.replacement)
    +'<button class="btn" id="disarm-use">지금 이 대처문장 사용하기</button><div style="height:8px"></div><button class="btn sec" id="disarm-edit">수정</button><div style="height:8px"></div><button class="btn bad" id="disarm-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
  $('#disarm-use').onclick=()=>openSmartDisarmNow(r);
  $('#disarm-edit').onclick=()=>openSmartDisarmEditor(r);
  $('#disarm-delete').onclick=()=>{
    if(!confirm('이 DISARM 대처문장을 삭제할까요?')) return;
    S.smartWorks=(Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>!(x&&x.id===r.id)); save(); closeModal(); drawSmartDisarm(); toast('기록을 삭제했습니다.');
  };
}
function openSmartDisarmNow(plan){
  if(famMode()) return;
  const r=plan||smartDisarmRecords()[0]||null;
  if(!r){
    modal('<h2>지금 DISARM 사용하기</h2><div class="card"><h3>1 · 알아차리기</h3><p>지금 떠오르는 이미지나 자기대화가 나를 중독행동 쪽으로 끌고 가는지 알아차립니다.</p></div><div class="card"><h3>2 · 거부하고 대체하기</h3><p>그 생각을 사실이나 명령으로 따르지 않고, 짧게 거부한 뒤 현실적이고 건설적인 생각으로 바꿉니다.</p></div><div class="note">저장한 대처문장이 아직 없습니다. 지금 바로 5분 버티기를 시작할 수도 있고, 반복되는 자기대화를 먼저 적어둘 수도 있습니다.</div><button class="btn" id="disarm-generic-urge">DISARM으로 5분 버티기</button><div style="height:8px"></div><button class="btn sec" id="disarm-generic-new">내 대처문장 만들기</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
    $('#disarm-generic-urge').onclick=()=>startSmartDisarmUrge();
    $('#disarm-generic-new').onclick=()=>openSmartDisarmEditor(null);
    return;
  }
  const name=r.voiceName||'충동의 목소리';
  modal('<h2>지금 DISARM 사용하기</h2>'
    +'<div class="card"><h3>1 · 알아차리기</h3><div class="tiny" style="margin-bottom:6px">'+esc(name)+'</div><div style="white-space:pre-wrap"><b>'+esc(r.destructive)+'</b></div>'+(r.promise?'<p class="muted" style="margin:8px 0 0">이 생각이 약속하는 것: '+esc(r.promise)+'</p>':'')+'</div>'
    +'<div class="card"><h3>2 · 거부하고 현실로 돌아오기</h3>'+(r.reality?'<p style="white-space:pre-wrap"><b>현실 확인</b><br>'+esc(r.reality)+'</p>':'')+(r.refusal?'<p style="white-space:pre-wrap"><b>내 거부 문장</b><br>'+esc(r.refusal)+'</p>':'')+(r.replacement?'<p style="white-space:pre-wrap"><b>내 대체 생각·이미지</b><br>'+esc(r.replacement)+'</p>':'')+'</div>'
    +'<div class="note">이 생각은 내가 경험하는 생각·이미지일 뿐, 곧바로 따라야 하는 명령은 아닙니다. 이름을 붙였다면 처음 알아차리는 순간 그 이름을 부르고, 단호하게 거부한 뒤 약해져 사라지는 모습을 떠올려 볼 수 있습니다.</div>'
    +'<button class="btn" id="disarm-now-urge">이 대답으로 5분 버티기</button><div style="height:8px"></div><button class="btn sec" id="disarm-now-edit">대처문장 수정</button><div style="height:8px"></div><button class="btn ghost" id="disarm-now-other">다른 DISARM 기록 보기</button>');
  $('#disarm-now-urge').onclick=()=>startSmartDisarmUrge();
  $('#disarm-now-edit').onclick=()=>openSmartDisarmEditor(r);
  $('#disarm-now-other').onclick=()=>{ closeModal(); go('smart-disarm'); };
}
function startSmartDisarmUrge(){
  closeModal(); go('urge'); setTimeout(()=>urgeUseCope('DISARM · 자기대화 거부·대체'),80);
}

'''
s=s.replace(fn_anchor,block+fn_anchor,1)

# Route learning action.
act="  if(type === 'smart-deads'){ go('smart-deads'); return; }"
assert act in s
s=s.replace(act,act+"\n  if(type === 'smart-disarm'){ go('smart-disarm'); return; }",1)

# Add DISARM action to Point 2 after DEADS and before urge diary.
old='''        "actions": [
          {
            "type": "smart-deads",
            "label": "DEADS 대처계획·실행하기"
          },
          {
            "type": "urge-diary",
            "label": "내 충동일기 열기"
          }
        ]'''
new='''        "actions": [
          {
            "type": "smart-deads",
            "label": "DEADS 대처계획·실행하기"
          },
          {
            "type": "smart-disarm",
            "label": "DISARM 충동의 목소리 다루기"
          },
          {
            "type": "urge-diary",
            "label": "내 충동일기 열기"
          }
        ]'''
assert old in ld
ld=ld.replace(old,new,1)
assert '회복학습 데이터 V8.2.9' in ld
ld=ld.replace('회복학습 데이터 V8.2.9','회복학습 데이터 V8.2.10',1)

assert "const APP_VERSION = 'V8.2.9';" in st
assert "const V = 'ohg-v829-smart-deads';" in st
st=st.replace("const APP_VERSION = 'V8.2.9';","const APP_VERSION = 'V8.2.10';",1)
st=st.replace("const V = 'ohg-v829-smart-deads';","const V = 'ohg-v8210-smart-disarm';",1)

idx.write_text(s,encoding='utf-8'); learn.write_text(ld,encoding='utf-8'); sw.write_text(st,encoding='utf-8')
print('V8.2.10 SMART DISARM patch applied')
