from pathlib import Path
p=Path('v822-urge-diary.py')
s=p.read_text(encoding='utf-8')
s='\n'.join(line.rstrip() for line in s.splitlines())+'\n'
p.write_text(s,encoding='utf-8')
print('helper trailing whitespace removed')
