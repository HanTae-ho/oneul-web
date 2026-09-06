from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="smartToolButton('이완 · 마음 가라앉히기','알아차림 → PMR · 심상화 · 명상 중 하나 사용하기','smart-relax','wave')"
new="smartToolButton('이완 · 마음 가라앉히기','알아차림 → PMR · 심상화 · 명상 중 하나 사용하기','smart-relax','sprout')"
if s.count(old)!=1: raise SystemExit(f'target count={s.count(old)}')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
