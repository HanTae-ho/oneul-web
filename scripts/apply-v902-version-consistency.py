from pathlib import Path

# 1) Legacy verify.js: stop accepting V8.0 as the current release.
p=Path('verify.js')
s=p.read_text(encoding='utf-8')
old="""ok(/const BUILD = 'V8\\.0';/.test(index),'index BUILD = V8.0');
ok(/const APP_VERSION = 'V8\\.0';/.test(sw),'sw APP_VERSION = V8.0');
ok(/const V = 'ohg-v800';/.test(sw),'sw cache = ohg-v800');"""
new="""const EXPECTED_APP_VERSION = 'V9.0.2';
ok(/const BUILD\\s*=\\s*'V9\\.0\\.2';/.test(index),'index BUILD = '+EXPECTED_APP_VERSION);
ok(/const APP_VERSION\\s*=\\s*'V9\\.0\\.2';/.test(sw),'sw APP_VERSION = '+EXPECTED_APP_VERSION);
ok(/const V\\s*=\\s*'ohg-v902[^']*';/.test(sw),'sw cache = V9.0.2 계열');"""
if old not in s:
    raise SystemExit('verify.js legacy V8.0 block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

# 2) Permanent CI: verify all three release markers together so this cannot regress silently.
p=Path('.github/workflows/check-web-runtime.yml')
s=p.read_text(encoding='utf-8')
old2="""      - name: Fixed invariants
        run: |
          grep -F \"const DATA_SCHEMA = 6;\" index.html
          grep -F \"const SOCIAL_KEY = 'ohg.social.v1';\" index.html
          ! grep -F 'HALTS.find' index.html
"""
new2="""      - name: Version and fixed invariants
        run: |
          set -euo pipefail
          grep -E \"const BUILD\\s*=\\s*'V9\\.0\\.2';\" index.html
          grep -E \"const APP_VERSION\\s*=\\s*'V9\\.0\\.2';\" sw.js
          grep -E \"const V\\s*=\\s*'ohg-v902[^']*';\" sw.js
          grep -F \"const EXPECTED_APP_VERSION = 'V9.0.2';\" verify.js
          grep -F \"const DATA_SCHEMA = 6;\" index.html
          grep -F \"const SOCIAL_KEY = 'ohg.social.v1';\" index.html
          ! grep -F 'HALTS.find' index.html
"""
if old2 not in s:
    raise SystemExit('runtime workflow invariant block not found')
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')

# 3) Local sanity assertions.
idx=Path('index.html').read_text(encoding='utf-8')
sw=Path('sw.js').read_text(encoding='utf-8')
vr=Path('verify.js').read_text(encoding='utf-8')
assert "const BUILD='V9.0.2';" in idx or "const BUILD = 'V9.0.2';" in idx
assert "const APP_VERSION = 'V9.0.2';" in sw
assert "ohg-v902" in sw
assert "EXPECTED_APP_VERSION = 'V9.0.2'" in vr
assert "V8\\.0" not in '\n'.join(vr.splitlines()[:20])
print('V9.0.2 version consistency patch PASS')
