from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
assert 'hydrateIcons(box);' in s
assert 'function refreshIcons()' in s
s=s.replace('hydrateIcons(box);','refreshIcons();',1)
p.write_text(s,encoding='utf-8')
print('V8.2.11 SMART tools hub runtime icon refresh fixed')
