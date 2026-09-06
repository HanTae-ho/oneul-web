from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="const bad=used.findIndex(x=>!x.name||x.before==null);if(bad>=0){render(bad);toast(!used[bad].name?'활동 이름을 적어주세요.':'시도 전 관심도 1~10점을 선택해주세요.');return;}"
new="const bad=items.findIndex(x=>(x.name||x.before!=null||x.after!=null||x.note)&&(!x.name||x.before==null));if(bad>=0){render(bad);toast(!items[bad].name?'활동 이름을 적어주세요.':'시도 전 관심도 1~10점을 선택해주세요.');return;}"
if s.count(old)!=1:
    raise SystemExit(f'expected 1 validation block, found {s.count(old)}')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
