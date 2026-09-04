from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""    b.onclick=()=>{ urge.touched=true; const i=urge.thoughts.indexOf(t); if(i<0) urge.thoughts.push(t); else urge.thoughts.splice(i,1); queueUrgeDraft(); drawUrge(); };"""
new="""    b.onclick=()=>{ urge.touched=true; const i=urge.thoughts.indexOf(t); if(i<0) urge.thoughts.push(t); else urge.thoughts.splice(i,1); queueUrgeDraft(); b.classList.toggle('on',urge.thoughts.indexOf(t)>=0); };"""
if s.count(old)!=1: raise SystemExit(f'expected thought handler once, found {s.count(old)}')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('V8.2.2 thought state fix applied')
