from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

assert "const BUILD = 'V8.2.46';" in s
s=s.replace("const BUILD = 'V8.2.46';", "const BUILD = 'V8.2.47';", 1)

pages="""  const pages={
    'family-boundary':'family-boundary','family-conversation':'family-conversation','family-return-plan':'family-return-plan',
    'importance-confidence':'smart-importance-confidence','hov':'smart-hov','change-plan':'smart-change-plan','three-questions':'smart-three-questions',
    'cba':'smart-cba','deads':'smart-deads','disarm':'smart-disarm','abc':'smart-abc','dibs':'smart-dibs','thinking-styles':'smart-thinking-styles',
    'problem-solving':'smart-problem-solving','balance-pie':'smart-balance-pie','vaci':'smart-vaci','goal':'smart-goal'
  };
"""
assert s.count(pages)==1
insert=pages+"""  /* V8.2.47 · 내 발자취의 SMART 기록은 도구 목록을 거치지 않고 저장기록을 바로 엽니다. */
  const smartRecordKey=r=>{
    const raw=String((r&&(r.tool||r.kind))||'');
    if(raw==='lifestyle-balance-pie') return 'balance-pie';
    if(raw==='smart-goal') return 'goal';
    return raw;
  };
  const openSmartRecord=(key,r)=>{
    if(key==='hov' && typeof openSmartHovRecord==='function'){ openSmartHovRecord(r); return; }
    if(key==='cba' && typeof openSmartCbaRecord==='function'){ openSmartCbaRecord(r); return; }
    const id=String((r&&(r.id||r.rid))||'');
    const views={
      'change-plan':'openSmartChangePlanView','three-questions':'openSmartThreeView',
      'deads':'openSmartDeadsView','disarm':'openSmartDisarmView','abc':'openSmartAbcView','dibs':'openSmartDibsView',
      'thinking-styles':'openSmartThinkingView','problem-solving':'openSmartProblemView',
      'balance-pie':'openSmartBalanceView','vaci':'openSmartVaciView','goal':'openSmartGoalView'
    };
    const fn=views[key]&&window[views[key]];
    if(id&&typeof fn==='function'){ fn(id); return; }
    go(pages[key]||'smart-tools');
  };
"""
s=s.replace(pages,insert,1)

old="const key=String((r&&(r.tool||r.kind))||'');"
assert s.count(old)==1
s=s.replace(old,"const key=smartRecordKey(r);",1)

old="""  (S.smartWorks||[]).filter(r=>r&&(r.role||'self')===role).forEach(r=>{
    const key=String(r.tool||r.kind||'');
    if(!key) return;
    const family=key.startsWith('family-');
    rows.push({
      group:family?'family':'smart', ts:Number(r.updatedAt||r.t||r.ts||0),
      title:labels[key]||key, summary:smartPreview(r), record:r,
      open:()=>go(pages[key]||'smart-tools')
    });
  });
"""
new="""  (S.smartWorks||[]).filter(r=>r&&(r.role||'self')===role).forEach(r=>{
    const key=smartRecordKey(r);
    if(!key) return;
    const family=key.startsWith('family-');
    rows.push({
      group:family?'family':'smart', ts:Number(r.updatedAt||r.t||r.ts||0),
      title:labels[key]||key, summary:smartPreview(r), record:r,
      open:()=>family?go(pages[key]||'smart-tools'):openSmartRecord(key,r)
    });
  });
"""
assert s.count(old)==1
s=s.replace(old,new,1)

assert "const DATA_SCHEMA = 6;" in s
assert "const KEY = 'ohg.v1';" in s
assert "open:()=>family?go(pages[key]||'smart-tools'):openSmartRecord(key,r)" in s
assert "if(key==='hov' && typeof openSmartHovRecord==='function')" in s
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
t=sw.read_text(encoding='utf-8')
assert "const APP_VERSION = 'V8.2.46';" in t
assert "const V = 'ohg-v8246-listen-accordion-capsule';" in t
t=t.replace("const APP_VERSION = 'V8.2.46';", "const APP_VERSION = 'V8.2.47';",1)
t=t.replace("const V = 'ohg-v8246-listen-accordion-capsule';", "const V = 'ohg-v8247-smart-record-direct-view';",1)
sw.write_text(t,encoding='utf-8')

r=Path('README.md')
rt=r.read_text(encoding='utf-8')
head="""# V8.2.47 — 내 발자취 SMART 기록 바로보기\n\n- `내 발자취 → 실천기록`의 SMART `보기`는 SMART 실천도구 화면을 거치지 않고 해당 저장기록 상세를 바로 엽니다.\n- HOV·CBA와 변화 계획·3가지 질문·DEADS·DISARM·ABC·DIBS·사고방식·문제 해결·삶의 균형·VACI·SMART 목표의 기존 상세보기 함수를 그대로 재사용합니다.\n- 12단계 보기, SMART 작성·수정·삭제 기능과 `smartWorks` 저장형식은 변경하지 않습니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, Android 정확알림·화면 OFF·부팅 재예약·외래 반복예약·이완 TTS는 변경하지 않습니다.\n\n"""
assert not rt.startswith('# V8.2.47')
r.write_text(head+rt,encoding='utf-8')
print('V8.2.47 focused patch PASS')
