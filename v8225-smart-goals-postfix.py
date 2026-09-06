from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="const r=smartGoalRecords().find(x=>x.id===id);if(!r)return,c=r.checks||{};"
new="const r=smartGoalRecords().find(x=>x.id===id);if(!r)return;const c=r.checks||{};"
if old not in s:
    raise SystemExit('SMART goal view syntax target not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
