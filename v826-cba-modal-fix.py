from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="const root=document.querySelector('#modal .modal-sheet')||document.querySelector('#modal')||document.body;"
new="const root=document.querySelector('#modin')||document.body;"
if old not in s:
    raise SystemExit('CBA modal root anchor not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
