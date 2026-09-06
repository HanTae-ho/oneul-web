from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="DIB/DIBS · 도움이 되지 않는 사고방식 · 문제해결 도구는 순차적으로 추가됩니다.</div></div>';"
new="DIB/DIBS · 도움이 되지 않는 사고방식 · 문제해결 도구는 순차적으로 추가됩니다.</div>'+'</div>';"
assert old in s
p.write_text(s.replace(old,new,1),encoding='utf-8')
print('Prepared Point 3 string for V8.2.15 patch')
