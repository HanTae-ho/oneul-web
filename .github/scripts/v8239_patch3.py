from pathlib import Path
import re

idx=Path('index.html')
s=idx.read_text(encoding='utf-8')

def patch_section(section_id, end_marker, old, new):
    global s
    a=s.find(f'<section class="pg" id="{section_id}">')
    if a<0: raise SystemExit('section not found: '+section_id)
    b=s.find(end_marker,a)
    if b<0: raise SystemExit('section end not found: '+section_id)
    part=s[a:b]
    if old not in part: raise SystemExit('button not found in '+section_id)
    part=part.replace(old,new,1)
    s=s[:a]+part+s[b:]

patch_section(
    'p-habit','<section class="pg" id="p-habit-edit">',
    "onclick=\"appBack('tools')\">← 회복도구</button>",
    "onclick=\"appBack('schedule')\">← 일정·알림</button>"
)
patch_section(
    'p-smart-tools','<!-- ══════════ SMART Recovery · 중요성',
    "class=\"tiny\" style=\"color:var(--acc);font-weight:600\" onclick=\"appBack('tools')\">← 회복도구</button>",
    "class=\"tiny\" style=\"color:var(--acc);font-weight:600\" data-smart-back data-back-default=\"tools\" data-back-label=\"회복도구\" onclick=\"appBack('tools')\">← 회복도구</button>"
)
idx.write_text(s,encoding='utf-8')

# Reuse the reviewed main patch, but remove the two strict lines already handled above.
p=Path('.github/scripts/v8239_patch.py')
src=p.read_text(encoding='utf-8')
src,n1=re.subn(r'^rep\("onclick=.*작은 실천을 정하고 오늘 했는지만 체크합니다\..*\)\n','',src,count=1,flags=re.M)
src,n2=re.subn(r"^rep\('<button class=.*SMART Recovery는.*\)\n",'',src,count=1,flags=re.M)
if n1!=1 or n2!=1:
    raise SystemExit(f'could not neutralize strict patch lines: habit={n1}, smart={n2}')
exec(compile(src,'v8239_patch.py','exec'),{'__name__':'__main__'})
