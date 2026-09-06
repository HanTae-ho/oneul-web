from pathlib import Path
idx=Path('index.html'); sw=Path('sw.js')
s=idx.read_text(encoding='utf-8'); w=sw.read_text(encoding='utf-8')
assert "const BUILD = 'V8.2.14';" in s
s=s.replace("const BUILD = 'V8.2.14';","const BUILD = 'V8.2.15';",1)
# page after ABC
anchor='''  <div id="smart-abc-list" style="margin-top:12px"></div>\n</section>\n'''
assert anchor in s
page='''\n<!-- ══════════ SMART Recovery · DIB/DIBS V8.2.15 ══════════ -->\n<section class="pg" id="p-smart-dibs">\n  <div class="sp" style="margin-bottom:11px">\n    <h1 style="margin:0">DIBS · 생각 반박하기</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back onclick="appBack('smart-tools')">← SMART 실천도구</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    도움이 되지 않는 신념을 알아차리고, 그것을 <b>질문으로 바꾸어 사실·논리·장기적 도움 여부를 점검</b>한 뒤 더 균형 잡힌 합리적 신념으로 바꿔봅니다. 내용은 <b>이 기기에만 저장</b>됩니다.\n  </div>\n  <div id="smart-dibs-role-note"></div>\n  <button class="btn sec" id="smart-dibs-new">+ DIBS 새로 작성하기</button>\n  <div id="smart-dibs-list" style="margin-top:12px"></div>\n</section>\n'''
s=s.replace(anchor,anchor+page,1)
# route tab + draw + labels/fallbacks/action
s=s.replace("p === 'smart-disarm' || p === 'smart-abc' || p === 'smart-tools'","p === 'smart-disarm' || p === 'smart-abc' || p === 'smart-dibs' || p === 'smart-tools'",1)
s=s.replace("  if(p === 'smart-abc') drawSmartAbc();\n","  if(p === 'smart-abc') drawSmartAbc();\n  if(p === 'smart-dibs') drawSmartDibs();\n",1)
s=s.replace("    'smart-abc':'ABC 문제 해결'\n","    'smart-abc':'ABC 문제 해결',\n    'smart-dibs':'DIBS 생각 반박하기'\n",1)
s=s.replace("    'smart-deads':'smart-deads', 'smart-disarm':'smart-disarm', 'smart-abc':'smart-abc'\n","    'smart-deads':'smart-deads', 'smart-disarm':'smart-disarm', 'smart-abc':'smart-abc', 'smart-dibs':'smart-dibs'\n",1)
s=s.replace("  if(type === 'smart-abc'){ go('smart-abc'); return; }\n","  if(type === 'smart-abc'){ go('smart-abc'); return; }\n  if(type === 'smart-dibs'){ go('smart-dibs'); return; }\n",1)
# smart tools Point 3
old="""smartToolButton('ABC 문제 해결','A 사건 → B 생각 → C 결과 → D 반박 → E 새로운 생각','smart-abc','speak')+'<div class=\"tiny\" style=\"margin-top:6px\">DIB/DIBS · 도움이 되지 않는 사고방식 · 문제해결 도구는 순차적으로 추가됩니다.</div>'"""
new="""smartToolButton('ABC 문제 해결','A 사건 → B 생각 → C 결과 → D 반박 → E 새로운 생각','smart-abc','speak')+smartToolButton('DIBS · 생각 반박하기','도움되지 않는 신념 → 질문·증거점검 → 균형 잡힌 합리적 신념','smart-dibs','speak')+'<div class=\"tiny\" style=\"margin-top:6px\">도움이 되지 않는 사고방식 · 문제해결 도구는 순차적으로 추가됩니다.</div>'"""
assert old in s
s=s.replace(old,new,1)
# Insert functions before learningAction
fn_anchor='function learningAction(type){\n'
assert fn_anchor in s
block=r'''/* ── SMART Recovery · DIB/DIBS V8.2.15 ── */
function smartDibsRecords(){
  return (Array.isArray(S.smartWorks)?S.smartWorks:[])
    .filter(r=>r&&r.kind==='dibs'&&(r.role||'self')===(famMode()?'family':'self'))
    .sort((a,b)=>(b.updatedAt||b.ts||0)-(a.updatedAt||a.ts||0));
}
function smartDibsDate(ts){ if(!ts)return ''; const d=new Date(ts); return d.getFullYear()+'. '+(d.getMonth()+1)+'. '+d.getDate()+'.'; }
function drawSmartDibs(){
  const list=$('#smart-dibs-list'),rn=$('#smart-dibs-role-note'),add=$('#smart-dibs-new'); if(!list||!add)return;
  if(rn) rn.innerHTML=famMode()?'<div class="note" style="margin-bottom:12px"><b>가족도 내 생각을 대상으로 사용합니다.</b><br>상대의 신념을 진단하거나 논박하는 도구가 아닙니다. 내가 상황을 해석하는 방식과 나의 반응을 더 균형 있게 점검합니다.</div>':'';
  add.onclick=()=>openSmartDibsEditor(null);
  const rows=smartDibsRecords();
  if(!rows.length){ list.innerHTML='<div class="card"><b>아직 저장한 DIBS 기록이 없습니다.</b><p class="muted" style="margin:5px 0 0">“절대”, “반드시”, “참을 수 없어”, “항상”, “나는 실패자야”처럼 나를 몰아붙이는 생각 하나부터 적어보세요.</p></div>'; return; }
  list.innerHTML='<div class="card"><h3>저장한 DIBS '+rows.length+'건</h3>'+rows.map(r=>'<div class="sp" style="gap:10px;padding:11px 0;border-top:1px solid var(--line)"><div style="min-width:0;flex:1"><div class="tiny">'+esc(smartDibsDate(r.updatedAt||r.ts))+'</div><b style="display:block;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(r.ib||'DIBS 기록')+'</b><div class="muted" style="margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(r.rb||'')+'</div></div><button class="tiny" style="color:var(--acc);font-weight:600" onclick="openSmartDibsView(\''+esc(r.id)+'\')">보기</button></div>').join('')+'</div>';
}
function smartDibsField(title,id,value,placeholder,help,max){
  return '<div class="card"><label>'+esc(title)+'</label>'+(help?'<div class="tiny" style="margin:4px 0 7px">'+esc(help)+'</div>':'')+'<textarea id="'+id+'" maxlength="'+(max||800)+'" placeholder="'+esc(placeholder)+'">'+esc(value||'')+'</textarea></div>';
}
function openSmartDibsEditor(record){
  const r=record||{};
  modal('<h2>'+(record?'DIBS 수정':'DIBS 생각 반박하기')+'</h2>'
    +'<p class="muted" style="margin:5px 0 14px">목표는 생각을 억지로 긍정적으로 만드는 것이 아니라, 부정확하고 경직된 신념을 더 사실적·논리적·도움이 되는 신념으로 바꾸는 것입니다.</p>'
    +smartDibsField('1 · 지금 떠오른 도움이 되지 않는 신념','dibs-ib',r.ib,'예: “이 충동은 절대 참을 수 없어.”','절대·반드시·항상·결코·참을 수 없어 같은 경직된 표현이 있는지 살펴봅니다.',700)
    +smartDibsField('2 · 이 생각을 믿으면 나에게 어떤 일이 생기나요?','dibs-impact',r.impact,'예: 불안이 커지고 술을 마셔야만 버틸 수 있다고 느낀다.','감정, 행동, 충동, 관계, 회복에 미치는 영향을 적습니다.',800)
    +smartDibsField('3 · 이 신념을 질문으로 바꾸기','dibs-q',r.q,'예: “정말 이 충동은 참을 수 없는가?”','단정문을 질문으로 바꾸면 생각과 한 걸음 거리를 둘 수 있습니다.',700)
    +smartDibsField('4 · 사실과 증거 점검','dibs-evidence',r.evidence,'이 생각을 뒷받침하는 증거와 반대되는 증거는 무엇인가요?','사실인가? 현실적인가? 실제 경험은 무엇을 보여주나?',900)
    +smartDibsField('5 · 논리와 장기적 도움 점검','dibs-test',r.test,'이 생각은 논리적인가? 이 생각대로 행동하면 장기적으로 내가 원하는 삶에 도움이 되는가?','SMART 자료의 핵심 기준인 사실성·논리성·장기적 도움 여부를 점검합니다.',900)
    +smartDibsField('6 · 더 균형 잡힌 합리적 신념','dibs-rb',r.rb,'예: “충동은 불쾌하지만 견딜 수 있다. 나는 사용하지 않기로 선택할 수 있다.”','현실적이고 유연하며, 장기적으로 내가 원하는 방향에 도움이 되는 문장으로 바꿉니다.',900)
    +'<button class="btn" id="dibs-save">'+(record?'수정 저장':'DIBS 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
  $('#dibs-save').onclick=()=>{
    const rec={id:record?record.id:('dibs-'+Date.now()+'-'+Math.random().toString(36).slice(2,7)),kind:'dibs',role:famMode()?'family':'self',ts:record?(record.ts||Date.now()):Date.now(),updatedAt:Date.now(),ib:$('#dibs-ib').value.trim(),impact:$('#dibs-impact').value.trim(),q:$('#dibs-q').value.trim(),evidence:$('#dibs-evidence').value.trim(),test:$('#dibs-test').value.trim(),rb:$('#dibs-rb').value.trim()};
    if(!rec.ib){toast('도움이 되지 않는 신념을 적어주세요.');return;} if(!rec.q){toast('그 신념을 질문으로 바꿔 적어주세요.');return;} if(!rec.rb){toast('더 균형 잡힌 합리적 신념을 적어주세요.');return;}
    if(!Array.isArray(S.smartWorks))S.smartWorks=[];
    if(record){const i=S.smartWorks.findIndex(x=>x&&x.id===record.id); if(i>=0)S.smartWorks[i]=rec; else S.smartWorks.push(rec);} else S.smartWorks.push(rec);
    save();closeModal();drawSmartDibs();toast(record?'DIBS 기록을 수정했습니다.':'DIBS 기록을 저장했습니다.');
  };
}
function openSmartDibsView(id){
  const r=(Array.isArray(S.smartWorks)?S.smartWorks:[]).find(x=>x&&x.id===id&&x.kind==='dibs'); if(!r)return;
  const sec=(t,v)=>'<div class="card"><h3>'+esc(t)+'</h3><div style="white-space:pre-wrap">'+(String(v||'').trim()?esc(v):'<span class="muted">작성하지 않음</span>')+'</div></div>';
  modal('<h2>DIBS 기록</h2><div class="muted" style="margin:-4px 0 12px">'+esc(smartDibsDate(r.updatedAt||r.ts))+'</div>'+sec('도움이 되지 않는 신념',r.ib)+sec('이 생각의 영향',r.impact)+sec('질문으로 바꾸기',r.q)+sec('사실과 증거 점검',r.evidence)+sec('논리와 장기적 도움 점검',r.test)+sec('균형 잡힌 합리적 신념',r.rb)+'<button class="btn sec" id="dibs-edit">수정</button><div style="height:8px"></div><button class="btn bad" id="dibs-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
  $('#dibs-edit').onclick=()=>openSmartDibsEditor(r);
  $('#dibs-delete').onclick=()=>{if(!confirm('이 DIBS 기록을 삭제할까요?'))return;S.smartWorks=(Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>!(x&&x.id===r.id));save();closeModal();drawSmartDibs();toast('기록을 삭제했습니다.');};
}

'''
s=s.replace(fn_anchor,block+fn_anchor,1)
assert "const APP_VERSION = 'V8.2.14';" in w and "const V = 'ohg-v8214-home-longpress-edit';" in w
w=w.replace("const APP_VERSION = 'V8.2.14';","const APP_VERSION = 'V8.2.15';",1).replace("const V = 'ohg-v8214-home-longpress-edit';","const V = 'ohg-v8215-smart-dibs';",1)
idx.write_text(s,encoding='utf-8'); sw.write_text(w,encoding='utf-8')
print('V8.2.15 DIBS patch applied')
