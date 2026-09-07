from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old="const BUILD = 'V8.2.47';"
new="const BUILD = 'V8.2.48';"
assert old in s
s=s.replace(old,new,1)

old_start="""function startScreenNow(tool,sex){
  screenRun={id:tool.id,i:0,a:new Array((tool.questions||[]).length).fill(null),sex:sex,result:null};
  go('screen-test');
}
function drawScreenTest(){"""
new_start="""function startScreenNow(tool,sex){
  screenRun={id:tool.id,i:0,a:new Array((tool.questions||[]).length).fill(null),sex:sex,result:null,auditSkip:''};
  go('screen-test');
}
function screenAuditPrepareAnswer(tool,i,nextValue){
  if(!screenRun || tool.id!=='audit-k') return;
  if(screenRun.auditSkip==='q1' && i===0 && Number(nextValue)!==0){
    for(let k=1;k<=7;k++) screenRun.a[k]=null;
    screenRun.auditSkip='';
    return;
  }
  if(screenRun.auditSkip==='q23' && (i===1 || i===2)){
    const q2=i===1?Number(nextValue):screenRun.a[1];
    const q3=i===2?Number(nextValue):screenRun.a[2];
    if(q2!==0 || q3!==0){
      for(let k=3;k<=7;k++) screenRun.a[k]=null;
      screenRun.auditSkip='';
    }
  }
}
function screenNextQuestion(tool,i){
  if(tool.id==='audit-k'){
    if(i===0 && screenRun.a[0]===0){
      for(let k=1;k<=7;k++) screenRun.a[k]=0;
      screenRun.auditSkip='q1';
      return 8;
    }
    if(i===2 && screenRun.a[1]===0 && screenRun.a[2]===0){
      for(let k=3;k<=7;k++) screenRun.a[k]=0;
      screenRun.auditSkip='q23';
      return 8;
    }
  }
  return i+1;
}
function screenPrevQuestion(tool,i){
  if(tool.id==='audit-k' && i===8){
    if(screenRun.auditSkip==='q1') return 0;
    if(screenRun.auditSkip==='q23') return 2;
  }
  return Math.max(0,i-1);
}
function drawScreenTest(){"""
assert old_start in s
s=s.replace(old_start,new_start,1)

old_handlers="""  $$('[data-screen-v]').forEach(b=>b.onclick=()=>{ screenRun.a[i]=Number(b.dataset.screenV); drawScreenTest(); });
  $('#screen-prev').onclick=()=>{ if(screenRun.i>0){screenRun.i--;drawScreenTest();} };
  $('#screen-next').onclick=()=>{ if(screenRun.a[i]==null)return; if(i>=total-1) finishScreen(tool); else {screenRun.i++;drawScreenTest();} };"""
new_handlers="""  $$('[data-screen-v]').forEach(b=>b.onclick=()=>{
    const v=Number(b.dataset.screenV);
    screenAuditPrepareAnswer(tool,i,v);
    screenRun.a[i]=v;
    drawScreenTest();
  });
  $('#screen-prev').onclick=()=>{ if(screenRun.i>0){screenRun.i=screenPrevQuestion(tool,screenRun.i);drawScreenTest();} };
  $('#screen-next').onclick=()=>{ if(screenRun.a[i]==null)return; if(i>=total-1) finishScreen(tool); else {screenRun.i=screenNextQuestion(tool,i);drawScreenTest();} };"""
assert old_handlers in s
s=s.replace(old_handlers,new_handlers,1)

p.write_text(s,encoding='utf-8')

p=Path('sw.js')
s=p.read_text(encoding='utf-8')
assert "const APP_VERSION = 'V8.2.47';" in s
s=s.replace("const APP_VERSION = 'V8.2.47';","const APP_VERSION = 'V8.2.48';",1)
assert 'ohg-v8247-smart-direct-view' in s
s=s.replace('ohg-v8247-smart-direct-view','ohg-v8248-audit-skip',1)
p.write_text(s,encoding='utf-8')

p=Path('README.md')
s=p.read_text(encoding='utf-8')
s += """\n\n### V8.2.48 — AUDIT-K 표준 건너뛰기 흐름\n- AUDIT-K 1번에서 `전혀 안 마심` 선택 시 2~8번을 0점 처리하고 9번으로 이동합니다.\n- AUDIT-K 2번과 3번이 모두 0점이면 4~8번을 0점 처리하고 9번으로 이동합니다.\n- 건너뛴 뒤 `이전`을 누르면 각각 1번 또는 3번으로 돌아가며, 답을 바꿔 건너뛰기 조건이 사라지면 해당 문항들을 다시 응답하도록 초기화합니다.\n- 다른 자가점검 도구의 문항·채점·저장형식은 변경하지 않았습니다. DATA_SCHEMA=6 / ohg.v1 유지.\n"""
p.write_text(s,encoding='utf-8')
