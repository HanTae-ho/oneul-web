from pathlib import Path
import json

def rep(path, old, new, count=None):
    p=Path(path); s=p.read_text(encoding='utf-8')
    n=s.count(old)
    if n == 0:
        raise SystemExit(f'{path}: target not found: {old!r}')
    if count is not None and n != count:
        raise SystemExit(f'{path}: expected {count} matches, got {n}: {old!r}')
    p.write_text(s.replace(old,new),encoding='utf-8')
    print(path, old, '->', new, 'matches', n)

rep('index.html', "const BUILD='V9.0.20';", "const BUILD='V9.1.0';", 1)
rep('sw.js', "const APP_VERSION = 'V9.0.20';", "const APP_VERSION = 'V9.1.0';", 1)
rep('sw.js', "const V = 'ohg-v9020-practice-label-r1';", "const V = 'ohg-v910-ux-consolidation-r1';", 1)

latest=Path('latest-release.json')
data=json.loads(latest.read_text(encoding='utf-8'))
if data.get('version')!='V9.0.20' or int(data.get('versionCode',0))!=915:
    raise SystemExit('latest-release.json unexpected baseline')
data={
  'version':'V9.1.0',
  'versionCode':916,
  'apk':'https://github.com/HanTae-ho/oneul-web/releases/download/v9.1.0/oneul-v9.1.0.apk',
  'release':'https://github.com/HanTae-ho/oneul-web/releases/tag/v9.1.0'
}
latest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

rep('install.html', "verifiedVersion:'V9.0.20'", "verifiedVersion:'V9.1.0'", 1)
rep('install.html', "releases/download/v9.0.20-test/oneul-v9.0.20.apk", "releases/download/v9.1.0/oneul-v9.1.0.apk", 1)
rep('install.html', "releases/tag/v9.0.20-test", "releases/tag/v9.1.0", 1)
rep('privacy.html', '<span class="ver">V9.0</span>', '<span class="ver">V9.1.0</span>', 1)
rep('verify.js', "const BUILD='V9.0.20';", "const BUILD='V9.1.0';", 1)
rep('verify.js', "V9.0.20 BUILD 불일치", "V9.1.0 BUILD 불일치", 1)

p=Path('README.md'); s=p.read_text(encoding='utf-8')
if not s.startswith('## V9.0.20'):
    raise SystemExit('README baseline header unexpected')
entry="""## V9.1.0 — UX 통합 · 의미기록 내 발자취 연결\n- 회복도구의 `의미점검`과 `자가점검 기록` 명칭을 구분하고 FAQ·사용설명서를 현재 흐름에 맞게 동기화했습니다.\n- `나 → 내 발자취 → 실천기록`에 `의미` 필터를 추가해 기존 의미 돌아보기와 의미회복 간편점검 결과를 새 저장 없이 함께 확인할 수 있습니다.\n- 개인정보처리방침의 사용자 명칭을 `커뮤니티`로 통일하고 화면 문구 조사 오류를 정리했습니다.\n- `meaning-check-feature.js`를 정적 no-undef 검사에 포함하고 README/용어 불변식까지 CI에서 확인합니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, `ohg.social.v1` 및 Android 알림/TTS 엔진은 유지합니다.\n\n"""
p.write_text(entry+s,encoding='utf-8')
print('README V9.1.0 entry added')

# hard safety invariants
idx=Path('index.html').read_text(encoding='utf-8')
assert "const DATA_SCHEMA = 6;" in idx
assert "const KEY = 'ohg.v1';" in idx
assert "const SOCIAL_KEY = 'ohg.social.v1';" in idx
assert "const BUILD='V9.1.0';" in idx
assert "const APP_VERSION = 'V9.1.0';" in Path('sw.js').read_text(encoding='utf-8')
print('V9.1.0 promotion patch complete')
