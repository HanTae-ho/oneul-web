from pathlib import Path
import re, json

root=Path('.')
idx=root/'index.html'
s=idx.read_text(encoding='utf-8')

if "const BUILD='V9.0.18';" not in s:
    raise SystemExit('expected V9.0.18 baseline not found')

# Keep the three-column layout, but make learning/practice cards icon+title only and shorter.
needle="  .minitool.wide{min-height:126px}\n"
insert="""  .minitool.wide{min-height:126px}\n  /* V9.0.19 — 배우기·실천하기 3열 카드는 아이콘+제목만 남겨 빠르게 찾습니다. */\n  .learnmini .minitool{min-height:100px;padding:10px 6px;justify-content:center}\n  .learnmini .minitool .ic{width:38px;height:38px;margin:0 0 7px}\n  .learnmini .minitool b{font-size:13.5px;line-height:1.35;word-break:keep-all}\n"""
if needle not in s:
    raise SystemExit('minitool css anchor not found')
s=s.replace(needle,insert,1)

old_media="@media(max-width:350px){.learnmini{grid-template-columns:1fr}.minitool{min-height:0;flex-direction:row;text-align:left;gap:10px;padding:12px}.minitool .ic{margin:0;flex:none}.minitool b{min-width:70px}.minitool span{margin:0;flex:1}.practicegrid,.checkmini{grid-template-columns:1fr}.practicecard{min-height:0}}"
new_media="@media(max-width:350px){.learnmini{grid-template-columns:repeat(3,minmax(0,1fr))}.learnmini .minitool{min-height:96px;padding:9px 4px}.learnmini .minitool b{font-size:12.5px}.practicegrid,.checkmini{grid-template-columns:1fr}.practicecard{min-height:0}}"
if old_media not in s:
    raise SystemExit('small-width minitool media rule not found')
s=s.replace(old_media,new_media,1)

ids=['tool-learn','tool-qa','tool-listen','tool-meaning','tool-meaning-check-direct','tool-family-tools','tool-workbook','tool-smart-tools','tool-urge-diary','tool-capsule']
for bid in ids:
    pat=re.compile(r'(<button[^>]*\bid="'+re.escape(bid)+r'"[^>]*>)([\s\S]*?)(</button>)')
    m=pat.search(s)
    if not m:
        raise SystemExit(f'button not found: {bid}')
    body=m.group(2)
    # Description/status spans have no class; preserve the icon span (.ic).
    body2=re.sub(r'<span(?:\s+id="[^"]+")?>[\s\S]*?</span>','',body)
    if body2==body:
        raise SystemExit(f'description span not removed: {bid}')
    s=s[:m.start()]+m.group(1)+body2+m.group(3)+s[m.end():]

# Shorter card names approved for the compact 3-column layout.
s=s.replace('<b>의미점검 바로하기</b>','<b>의미점검 보기</b>',1)
s=s.replace('<b>회복 실천도구</b>','<b>필요한 도구</b>',1)

# Keep help/manual naming aligned with visible card names without renaming the underlying route.
s=s.replace('회복도구 → 실천하기 → 의미점검 바로하기','회복도구 → 실천하기 → 의미점검 보기')
s=s.replace('>의미점검 바로하기</button>','>의미점검 보기</button>')
s=s.replace('의미점검 바로하기(점검하기 · 점검 기록)','의미점검 보기(점검하기 · 점검 기록)')
s=s.replace('<summary>회복 실천도구는 어떻게 사용하나요?</summary>','<summary>필요한 도구는 어떻게 사용하나요?</summary>')
s=s.replace('>회복 실천도구 열기</button>','>필요한 도구 열기</button>')
s=s.replace(', 회복 실천도구, 충동일기, 미래의 나에게',', 필요한 도구, 충동일기, 미래의 나에게')

s=s.replace("const BUILD='V9.0.18';","const BUILD='V9.0.19';",1)
idx.write_text(s,encoding='utf-8')

# Service worker/version metadata.
sw=root/'sw.js'
t=sw.read_text(encoding='utf-8')
t=t.replace("const APP_VERSION = 'V9.0.18';","const APP_VERSION = 'V9.0.19';",1)
t=t.replace("const V = 'ohg-v9018-practice-grid-r1';","const V = 'ohg-v9019-compact-grid-r1';",1)
sw.write_text(t,encoding='utf-8')

lr=root/'latest-release.json'
data=json.loads(lr.read_text(encoding='utf-8'))
data.update({
    'version':'V9.0.19',
    'versionCode':914,
    'apk':'https://github.com/HanTae-ho/oneul-web/releases/download/v9.0.19-test/oneul-v9.0.19.apk',
    'release':'https://github.com/HanTae-ho/oneul-web/releases/tag/v9.0.19-test'
})
lr.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Fixed regression checks: keep old coverage and add compact-card invariants.
vf=root/'verify.js'
v=vf.read_text(encoding='utf-8')
v=v.replace("const BUILD='V9.0.18';","const BUILD='V9.0.19';")
v=v.replace("throw new Error('V9.0.18 BUILD 불일치')","throw new Error('V9.0.19 BUILD 불일치')")
anchor="ok(!/class=\"toolcard/.test(practiceSection)&&!/class=\"go\"/.test(practiceSection),'실천하기 목록형·열기 텍스트 제거');\n"
extra="""ok(!/class=\"toolcard/.test(practiceSection)&&!/class=\"go\"/.test(practiceSection),'실천하기 목록형·열기 텍스트 제거');\nconst learnSection=(index.match(/<h2>배우기<\\/h2>([\\s\\S]*?)<div class=\"toolsec\">/)||[])[1]||'';\nok(!/<span(?! class=\"ic\")/.test(learnSection+practiceSection),'배우기·실천하기 3열 카드 설명글 제거');\nok(/<b>의미점검 보기<\\/b>/.test(practiceSection)&&/<b>필요한 도구<\\/b>/.test(practiceSection),'실천하기 압축 제목 반영');\nok(/\\.learnmini \\.minitool\\{min-height:100px/.test(index),'배우기·실천하기 카드 높이 축소');\n"""
if anchor not in v:
    raise SystemExit('verify practice anchor not found')
v=v.replace(anchor,extra,1)
vf.write_text(v,encoding='utf-8')

vm=root/'verify-meaning.js'
m=vm.read_text(encoding='utf-8')
m=m.replace("index.includes('의미점검 바로하기(점검하기 · 점검 기록)')","index.includes('의미점검 보기(점검하기 · 점검 기록)')")
m=m.replace('V9.0.18 의미 돌아보기·기록 다시보기·의미회복 간편점검 UX 회귀검증 통과','V9.0.19 의미 돌아보기·기록 다시보기·의미회복 간편점검 UX 회귀검증 통과')
vm.write_text(m,encoding='utf-8')

# Guard rails.
final=idx.read_text(encoding='utf-8')
for must in ["const DATA_SCHEMA = 6;","const KEY = 'ohg.v1';","const SOCIAL_KEY = 'ohg.social.v1';",'<b>의미점검 보기</b>','<b>필요한 도구</b>']:
    if must not in final: raise SystemExit('missing invariant: '+must)
if 'tool-meaning-s' in re.search(r'<h2>실천하기</h2>([\s\S]*?)<div class="toolsec">',final).group(1):
    raise SystemExit('practice descriptions still present')
print('V9.0.19 compact grid patch applied')
