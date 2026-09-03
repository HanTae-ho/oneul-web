from pathlib import Path

# index.html: build marker + Android native marker detection.
p = Path('index.html')
s = p.read_text(encoding='utf-8')
if "const BUILD = 'V8.0.4';" not in s:
    if s.count("const BUILD = 'V8.0';") != 1:
        raise SystemExit('Unexpected BUILD marker')
    s = s.replace("const BUILD = 'V8.0';", "const BUILD = 'V8.0.4';", 1)

hash_probe = "new URLSearchParams((location.hash || '').replace(/^#/, ''))"
if hash_probe not in s:
    old_fn = """function nativeAndroidApp(){
  try{ return new URLSearchParams(location.search || '').get('native') === '1'; }
  catch(e){ return false; }
}"""
    new_fn = """function nativeAndroidApp(){
  try{
    if(new URLSearchParams(location.search || '').get('native') === '1') return true;
    return new URLSearchParams((location.hash || '').replace(/^#/, '')).get('native') === '1';
  }catch(e){ return false; }
}"""
    if s.count(old_fn) != 1:
        raise SystemExit(f'Actual nativeAndroidApp match count={s.count(old_fn)}')
    s = s.replace(old_fn, new_fn, 1)
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
