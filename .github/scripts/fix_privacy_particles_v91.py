from pathlib import Path
p=Path('privacy.html')
s=p.read_text(encoding='utf-8')
count=s.count('커뮤니티을')
if count < 1:
    raise SystemExit('privacy: 커뮤니티을 not found')
s=s.replace('커뮤니티을','커뮤니티를')
if '소셜' in s or '커뮤니티은' in s or '커뮤니티을' in s:
    raise SystemExit('privacy terminology/particle cleanup incomplete')
p.write_text(s,encoding='utf-8')
print('privacy particle replacements',count)
