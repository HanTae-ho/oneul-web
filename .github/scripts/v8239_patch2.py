from pathlib import Path

p=Path('.github/scripts/v8239_patch.py')
src=p.read_text(encoding='utf-8')
old1="rep(\"onclick=\\\"appBack('tools')\\\">← 회복도구</button>\\n  </div>\\n  <p class=\\\"muted\\\" style=\\\"margin:0 0 14px\\\">작은 실천을 정하고 오늘 했는지만 체크합니다.\", \"onclick=\\\"appBack('schedule')\\\">← 일정·알림</button>\\n  </div>\\n  <p class=\\\"muted\\\" style=\\\"margin:0 0 14px\\\">작은 실천을 정하고 오늘 했는지만 체크합니다.\")"
new1="sub(r'(<section class=\\\"pg\\\" id=\\\"p-habit\\\">.*?<button class=\\\"tiny\\\"[^>]*onclick=\\\")appBack\\\(\\\'tools\\\'\\\)(\\\"[^>]*>)← 회복도구</button>', r'\\1appBack(\\\'schedule\\\')\\2← 일정·알림</button>')"
old2="rep('<button class=\"tiny\" style=\"color:var(--acc);font-weight:600\" onclick=\"appBack(\\'tools\\')\">← 회복도구</button>\\n  </div>\\n  <div class=\"note\" style=\"margin-bottom:12px\">\\n    SMART Recovery는', '<button class=\"tiny\" style=\"color:var(--acc);font-weight:600\" data-smart-back data-back-default=\"tools\" data-back-label=\"회복도구\" onclick=\"appBack(\\'tools\\')\">← 회복도구</button>\\n  </div>\\n  <div class=\"note\" style=\"margin-bottom:12px\">\\n    SMART Recovery는')"
new2="sub(r'(<section class=\\\"pg\\\" id=\\\"p-smart-tools\\\">.*?<button class=\\\"tiny\\\")([^>]*)(onclick=\\\"appBack\\\(\\\'tools\\\'\\\)\\\"[^>]*>)← 회복도구</button>', r'\\1\\2data-smart-back data-back-default=\\\"tools\\\" data-back-label=\\\"회복도구\\\" \\3← 회복도구</button>')"
if old1 not in src:
    raise SystemExit('habit patch source line not found')
if old2 not in src:
    raise SystemExit('SMART back patch source line not found')
src=src.replace(old1,new1,1).replace(old2,new2,1)
exec(compile(src,'v8239_patch.py','exec'),{'__name__':'__main__'})
