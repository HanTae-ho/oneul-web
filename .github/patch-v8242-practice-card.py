from pathlib import Path
import re

root = Path('.')
index = root / 'index.html'
sw = root / 'sw.js'
readme = root / 'README.md'

s = index.read_text(encoding='utf-8')
assert "const BUILD = 'V8.2.41';" in s
s = s.replace("const BUILD = 'V8.2.41';", "const BUILD = 'V8.2.42';", 1)

start = s.index('  const cleanText=v=>', s.index('function recPractice(){'))
end = s.index('  const whenText=t=>', start)
new_preview = r'''  const cleanText=v=>String(v==null?'':v).replace(/\s+/g,' ').trim();
  const previewText=v=>{
    let text='';
    if(Array.isArray(v)) text=v.map(x=>typeof x==='string'?x:(x&&typeof x==='object'?(x.text||x.value||x.label||''):'')).filter(Boolean).join(' · ');
    else if(v&&typeof v==='object') text=String(v.text||v.value||v.label||'');
    else if(typeof v==='string'||typeof v==='number') text=String(v);
    text=cleanText(text);
    return text.length>72?text.slice(0,72)+'…':text;
  };
  const smartPreview=r=>{
    const key=String((r&&(r.tool||r.kind))||'');
    const labeled=(label,...vals)=>{
      for(const v of vals){ const text=previewText(v); if(text) return label+' · '+text; }
      return '';
    };
    let fixed='';
    if(key==='hov') fixed=labeled('우선 가치',r.protect,Array.isArray(r.values)?r.values[0]:'');
    else if(key==='abc') fixed=labeled('떠오른 생각',r.b,r.a);
    else if(key==='change-plan') fixed=labeled('변화 목표',r.change);
    else if(key==='dibs') fixed=labeled('균형 잡힌 생각',r.rb,r.ib);
    else if(key==='thinking-styles') fixed=labeled('떠오른 생각',r.thought);
    else if(key==='three-questions') fixed=labeled('원하는 미래',r.future);
    else if(key==='cba') fixed=labeled('살펴본 행동',r.subject);
    else if(key==='disarm') fixed=labeled('대체 생각',r.replacement,r.reality);
    else if(key==='problem-solving') fixed=labeled('해결할 문제',r.problem);
    else if(key==='goal') fixed=labeled('목표',r.goal);
    else if(key==='family-boundary') fixed=labeled('내가 지킬 경계',r.protect,r.action);
    else if(key==='family-conversation') fixed=labeled('말할 한 문장',r.sentence,r.request);
    else if(key==='family-return-plan') fixed=labeled('내가 할 행동',r.action,r.next);
    if(fixed) return fixed;
    const keys=['sentence','change','future','subject','destructive','thought','ib','problem','goal','topic','situation','protect','request','action','nextStep','reasons','current','replacement','rb','support','next','avoid','reality','feeling','impact'];
    for(const k of keys){ const text=previewText(r&&r[k]); if(text) return text; }
    if(r&&Array.isArray(r.values)) return previewText(r.values);
    return '';
  };
'''
s = s[:start] + new_preview + s[end:]

old_filter = """  filters.forEach(f=>{\n    const b=el('button','btn sec sm',f.l); b.type='button'; b.style.width='auto'; b.style.padding='9px 13px'; b.style.flex='0 0 auto';\n    if(f.v===recPracticeFilter){ b.style.borderColor='var(--acc)'; b.style.background='var(--accbg)'; b.style.color='var(--acc)'; }\n    b.onclick=()=>{ recPracticeFilter=f.v; drawRec(); };\n    bar.appendChild(b);\n  });"""
new_filter = """  filters.forEach(f=>{\n    const selected=f.v===recPracticeFilter;\n    const b=el('button','btn ghost sm',f.l); b.type='button'; b.style.width='auto'; b.style.padding='9px 13px'; b.style.flex='0 0 auto';\n    b.style.background=selected?'var(--acc)':'var(--panel)'; b.style.color=selected?'var(--panel)':'var(--dim)'; b.style.borderColor=selected?'var(--acc)':'var(--line)'; b.style.fontWeight=selected?'700':'600';\n    b.setAttribute('aria-pressed',selected?'true':'false');\n    b.onclick=()=>{ recPracticeFilter=f.v; drawRec(); };\n    bar.appendChild(b);\n  });"""
assert old_filter in s
s = s.replace(old_filter, new_filter, 1)
index.write_text(s, encoding='utf-8')

w = sw.read_text(encoding='utf-8')
assert "const APP_VERSION = 'V8.2.41';" in w
assert "const V = 'ohg-v8241-practice-history';" in w
w = w.replace("const APP_VERSION = 'V8.2.41';", "const APP_VERSION = 'V8.2.42';", 1)
w = w.replace("const V = 'ohg-v8241-practice-history';", "const V = 'ohg-v8242-practice-card-polish';", 1)
sw.write_text(w, encoding='utf-8')

r = readme.read_text(encoding='utf-8')
section = '''# V8.2.42 — 실천기록 카드 표시 개선\n\n- `내 발자취 > 실천기록`의 SMART/가족 기록 미리보기를 도구별 의미가 드러나는 문구로 표시합니다.\n- 예: HOV `우선 가치 · …`, ABC `떠오른 생각 · …`, 변화 계획 `변화 목표 · …`, DIBS `균형 잡힌 생각 · …`, 가족 경계 `내가 지킬 경계 · …`.\n- `전체 / 12단계 / SMART / 가족도구` 필터는 선택된 항목을 강조색 채움으로 분명하게 구분합니다.\n- 기록 저장형식, `DATA_SCHEMA=6`, `ohg.v1`, 회복도구 작성 기능, Android 정확알림·부팅 재예약·이완 TTS는 변경하지 않습니다.\n\n'''
if not r.startswith('# V8.2.42'):
    readme.write_text(section + r, encoding='utf-8')
