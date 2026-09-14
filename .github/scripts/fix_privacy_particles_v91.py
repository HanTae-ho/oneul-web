from pathlib import Path
p=Path('privacy.html')
s=p.read_text(encoding='utf-8')
obj=s.count('커뮤니티을')
topic=s.count('커뮤니티은')
if obj + topic < 1:
    raise SystemExit('privacy: malformed community particles not found')
s=s.replace('커뮤니티을','커뮤니티를').replace('커뮤니티은','커뮤니티는')
for bad in ('소셜','커뮤니티은','커뮤니티을','커뮤니티이','커뮤니티과'):
    if bad in s:
        raise SystemExit('privacy terminology/particle cleanup incomplete: '+bad)
p.write_text(s,encoding='utf-8')
print('privacy particle replacements','object=',obj,'topic=',topic)
