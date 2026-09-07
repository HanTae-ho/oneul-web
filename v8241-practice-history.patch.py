from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if "const BUILD = 'V8.2.40';" not in s:
    raise SystemExit('Expected V8.2.40 BUILD not found')
s = s.replace("const BUILD = 'V8.2.40';", "const BUILD = 'V8.2.41';", 1)

marker = "let recTab = 'mood';"
if marker not in s:
    raise SystemExit('recTab marker not found')
if "let recPracticeFilter = 'all';" not in s:
    s = s.replace(marker, marker + "\nlet recPracticeFilter = 'all';", 1)

start = s.find('function recPractice(){')
end = s.find('\nfunction recWorkbook(){', start)
if start < 0 or end < 0:
    raise SystemExit('recPractice boundaries not found')

new_func = r'''function recPractice(){
  const w=el('div');
  const scope=famMode()?'family':'self';
  const role=scope;
  const labels={
    'family-boundary':'내 경계 정리','family-conversation':'대화 준비','family-return-plan':'다시 사용했을 때 내 대응계획',
    'importance-confidence':'중요성 · 자신감','hov':'가치의 계층 HOV','change-plan':'변화 계획','three-questions':'나의 3가지 질문',
    'cba':'비용-편익 분석 CBA','deads':'DEADS · 충동 대처','disarm':'DISARM','abc':'ABC · 생각과 행동 살펴보기','dibs':'DIBS · 생각 반박',
    'thinking-styles':'사고방식 점검','problem-solving':'문제 해결 · 5단계','balance-pie':'삶의 균형','vaci':'VACI','goal':'SMART 목표'
  };
  const pages={
    'family-boundary':'family-boundary','family-conversation':'family-conversation','family-return-plan':'family-return-plan',
    'importance-confidence':'smart-importance-confidence','hov':'smart-hov','change-plan':'smart-change-plan','three-questions':'smart-three-questions',
    'cba':'smart-cba','deads':'smart-deads','disarm':'smart-disarm','abc':'smart-abc','dibs':'smart-dibs','thinking-styles':'smart-thinking-styles',
    'problem-solving':'smart-problem-solving','balance-pie':'smart-balance-pie','vaci':'smart-vaci','goal':'smart-goal'
  };
  const cleanText=v=>String(v==null?'':v).replace(/\s+/g,' ').trim();
  const smartPreview=r=>{
    const keys=['sentence','change','future','subject','destructive','thought','ib','problem','goal','topic','situation','protect','request','action','nextStep','reasons','current','replacement','rb','support','next','avoid','reality','feeling','impact'];
    for(const k of keys){
      const v=r&&r[k];
      let text='';
      if(Array.isArray(v)) text=v.map(x=>typeof x==='string'?x:(x&&typeof x==='object'?(x.text||x.value||x.label||''):'')).filter(Boolean).join(' · ');
      else if(typeof v==='string'||typeof v==='number') text=String(v);
      text=cleanText(text);
      if(text) return text.length>72?text.slice(0,72)+'…':text;
    }
    if(r&&Array.isArray(r.values)){
      const text=cleanText(r.values.join(' · '));
      if(text) return text.length>72?text.slice(0,72)+'…':text;
    }
    return '';
  };
  const whenText=t=>{
    const d=new Date(Number(t||Date.now()));
    try{return d.toLocaleString('ko-KR',{year:'numeric',month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'});}
    catch(_){return d.toLocaleString();}
  };

  const rows=[];
  workbookRecordStore(scope).forEach(r=>{
    const def=workbookDef(r.kind,scope); if(!def) return;
    rows.push({
      group:'step', ts:Number(r.updatedAt||r.t||0), title:def.title,
      summary:cleanText(workbookRecordSummary(r)), record:r,
      open:()=>openWorkbookRecord(r.rid)
    });
  });
  (S.smartWorks||[]).filter(r=>r&&(r.role||'self')===role).forEach(r=>{
    const key=String(r.tool||r.kind||'');
    if(!key) return;
    const family=key.startsWith('family-');
    rows.push({
      group:family?'family':'smart', ts:Number(r.updatedAt||r.t||r.ts||0),
      title:labels[key]||key, summary:smartPreview(r), record:r,
      open:()=>go(pages[key]||'smart-tools')
    });
  });
  rows.sort((a,b)=>b.ts-a.ts);

  const filters=scope==='family'
    ? [{v:'all',l:'전체'},{v:'step',l:'12단계'},{v:'smart',l:'SMART'},{v:'family',l:'가족도구'}]
    : [{v:'all',l:'전체'},{v:'step',l:'12단계'},{v:'smart',l:'SMART'}];
  if(!filters.some(x=>x.v===recPracticeFilter)) recPracticeFilter='all';
  const bar=el('div','row wrap'); bar.style.marginBottom='12px';
  filters.forEach(f=>{
    const b=el('button','btn sec sm',f.l); b.type='button';
    if(f.v===recPracticeFilter){ b.style.borderColor='var(--acc)'; b.style.background='var(--accbg)'; b.style.color='var(--acc)'; }
    b.onclick=()=>{ recPracticeFilter=f.v; drawRec(); };
    bar.appendChild(b);
  });
  w.appendChild(bar);

  const shown=(recPracticeFilter==='all'?rows:rows.filter(x=>x.group===recPracticeFilter));
  if(!shown.length){
    const empty={all:'저장된 실천 기록이 없습니다.',step:'저장된 12단계 기록이 없습니다.',smart:'저장된 SMART 기록이 없습니다.',family:'저장된 가족도구 기록이 없습니다.'};
    w.appendChild(emptyBox(empty[recPracticeFilter]||empty.all));
    return w;
  }

  const c=el('div','card');
  c.appendChild(el('h3','', '저장한 실천 기록 '+shown.length+'건'));
  shown.slice(0,30).forEach(row=>{
    const badge=row.group==='step'?'12':row.group==='family'?'가':'S';
    const date=whenText(row.ts);
    const summary=row.summary?'<span>'+esc(row.summary)+'</span>':'';
    const b=el('button','toolcard','<span class="ic"><b style="font-size:13px">'+badge+'</b></span><span class="b"><b>'+esc(row.title)+'</b><span>'+esc(date)+'</span>'+summary+'</span><span class="go">보기</span>');
    b.type='button'; b.onclick=row.open; c.appendChild(b);
  });
  if(shown.length>30) c.appendChild(el('p','tiny','최근 30건을 표시합니다.'));
  w.appendChild(c); return w;
}
'''

s = s[:start] + new_func + s[end:]
p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
t = sw.read_text(encoding='utf-8')
if "const APP_VERSION = 'V8.2.40';" not in t:
    raise SystemExit('Expected V8.2.40 service worker version not found')
t = t.replace("const APP_VERSION = 'V8.2.40';", "const APP_VERSION = 'V8.2.41';", 1)
t = t.replace("const V = 'ohg-v8240-copy-cleanup';", "const V = 'ohg-v8241-practice-history';", 1)
sw.write_text(t, encoding='utf-8')

readme = Path('README.md')
r = readme.read_text(encoding='utf-8')
section = '''\n## V8.2.41 · 내 발자취 실천기록 정리\n\n- `내 발자취 > 실천기록`은 새 기록을 작성하는 메뉴가 아니라 저장된 과거 기록만 보여주도록 정리했습니다.\n- 12단계의 1·4·8·9·10·11·12단계 새 작성 버튼을 실천기록 화면에서 제거했습니다. 새 작성은 기존 `회복도구 > 12단계 점검`에서 합니다.\n- `전체 / 12단계 / SMART / 가족도구` 필터로 저장 기록을 구분합니다(당사자 모드에서는 가족도구 필터 제외).\n- SMART 기록의 식별값을 `tool`뿐 아니라 `kind`에서도 읽어 ABC, DIBS, 변화 계획 등이 더 이상 모두 `실천 기록`으로 표시되지 않습니다.\n- SMART/가족 실천 기록은 실제 도구명, 작성·수정 시각, 가능한 경우 저장내용 1줄 미리보기를 표시합니다.\n- 12단계 저장기록은 기존 제목과 요약을 그대로 사용하며 `보기`에서 해당 저장기록을 엽니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, 기존 저장자료 형식, Android 정확알림·부팅 재예약·이완 TTS는 변경하지 않았습니다.\n\n'''
if '## V8.2.41 · 내 발자취 실천기록 정리' not in r:
    first_nl=r.find('\n')
    if first_nl>=0: r=r[:first_nl+1]+section+r[first_nl+1:]
    else: r=section+r
readme.write_text(r, encoding='utf-8')
