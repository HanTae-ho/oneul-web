from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="const b=el('button','btn sec sm',f.l); b.type='button';"
new="const b=el('button','btn sec sm',f.l); b.type='button'; b.style.width='auto'; b.style.padding='9px 13px'; b.style.flex='0 0 auto';"
if old not in s: raise SystemExit('filter button marker not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
