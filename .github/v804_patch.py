from pathlib import Path
import re

# index.html: build marker + Android native marker detection.
p = Path('index.html')
s = p.read_text(encoding='utf-8')
if "const BUILD = 'V8.0.4';" not in s:
    if s.count("const BUILD = 'V8.0';") != 1:
        raise SystemExit('Unexpected BUILD marker')
    s = s.replace("const BUILD = 'V8.0';", "const BUILD = 'V8.0.4';", 1)

if "new URLSearchParams((location.hash||'').replace(/^#/,''))" not in s:
    pattern = re.compile(
        r"function\s+nativeAndroidApp\(\)\s*\{\s*"
        r"const\s+p\s*=\s*new\s+URLSearchParams\(location\.search\);\s*"
        r"return\s+p\.get\('native'\)\s*===\s*'1';\s*\}",
        re.S,
    )
    replacement = """function nativeAndroidApp(){
    const p=new URLSearchParams(location.search);
    if(p.get('native')==='1') return true;
    const h=new URLSearchParams((location.hash||'').replace(/^#/,''));
    return h.get('native')==='1';
  }"""
    s, n = pattern.subn(replacement, s, count=1)
    if n != 1:
        raise SystemExit(f'Legacy nativeAndroidApp match count={n}')
p.write_text(s, encoding='utf-8')

# sw.js: advance service-worker version/cache with app build.
p = Path('sw.js')
s = p.read_text(encoding='utf-8')
if "const APP_VERSION = 'V8.0.4';" not in s:
    if s.count("const APP_VERSION = 'V8.0';") != 1:
        raise SystemExit('Unexpected APP_VERSION marker')
    s = s.replace("const APP_VERSION = 'V8.0';", "const APP_VERSION = 'V8.0.4';", 1)
if "const V = 'ohg-v804';" not in s:
    if s.count("const V = 'ohg-v800';") != 1:
        raise SystemExit('Unexpected service-worker cache marker')
    s = s.replace("const V = 'ohg-v800';", "const V = 'ohg-v804';", 1)
p.write_text(s, encoding='utf-8')
