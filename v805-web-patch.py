from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
index = root / 'index.html'
sw = root / 'sw.js'
native = root / 'native.html'

# 1) App build marker.
s = index.read_text(encoding='utf-8')
old_build = "const BUILD = 'V8.0.4';"
new_build = "const BUILD = 'V8.0.5';"
if new_build not in s:
    if s.count(old_build) != 1:
        raise SystemExit(f'Unexpected BUILD marker count: {s.count(old_build)}')
    s = s.replace(old_build, new_build, 1)

# 2) Robust native-app detection: native.html sets a session-only marker.
old_fn = """function nativeAndroidApp(){
  try{
    if(new URLSearchParams(location.search || '').get('native') === '1') return true;
    return new URLSearchParams((location.hash || '').replace(/^#/, '')).get('native') === '1';
  }catch(e){ return false; }
}"""
new_fn = """function nativeAndroidApp(){
  try{
    if(sessionStorage.getItem('ohg.native.app') === '1') return true;
    if(new URLSearchParams(location.search || '').get('native') === '1') return true;
    return new URLSearchParams((location.hash || '').replace(/^#/, '')).get('native') === '1';
  }catch(e){ return false; }
}"""
if "sessionStorage.getItem('ohg.native.app')" not in s:
    if s.count(old_fn) != 1:
        raise SystemExit(f'Unexpected nativeAndroidApp shape/count: {s.count(old_fn)}')
    s = s.replace(old_fn, new_fn, 1)

# 3) Visible diagnostic while native branch is active.
old_status = "st.textContent = '앱이 완전히 닫혀 있어도 Android가 예약알림을 보낼 수 있습니다. 현재 설정된 시간 ' + n + '개. ' +"
new_status = "st.textContent = 'Android 앱 연결 확인됨 · ' + BUILD + ' · 앱이 완전히 닫혀 있어도 Android가 예약알림을 보낼 수 있습니다. 현재 설정된 시간 ' + n + '개. ' +"
if 'Android 앱 연결 확인됨 · ' not in s:
    if s.count(old_status) != 1:
        raise SystemExit(f'Unexpected native status anchor count: {s.count(old_status)}')
    s = s.replace(old_status, new_status, 1)

index.write_text(s, encoding='utf-8')

# 4) Service worker version/cache and offline native entry.
s = sw.read_text(encoding='utf-8')
repls = [
    ("const APP_VERSION = 'V8.0.4';", "const APP_VERSION = 'V8.0.5';"),
    ("const V = 'ohg-v804';", "const V = 'ohg-v805';"),
]
for old, new in repls:
    if new not in s:
        if s.count(old) != 1:
            raise SystemExit(f'Unexpected SW marker {old!r}: {s.count(old)}')
        s = s.replace(old, new, 1)
if "'./native.html'" not in s:
    anchor = "const SHELL = ['./', './index.html',"
    if s.count(anchor) != 1:
        raise SystemExit('Unexpected SHELL anchor')
    s = s.replace(anchor, "const SHELL = ['./', './index.html', './native.html',", 1)
sw.write_text(s, encoding='utf-8')

# 5) Dedicated native entry. sessionStorage is tab/session scoped, so a normal Chrome tab is not marked native.
native.write_text("""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <meta name="theme-color" content="#1f6f8a">
  <title>오늘 한 걸음</title>
</head>
<body>
<script>
(function(){
  try { sessionStorage.setItem('ohg.native.app', '1'); } catch(e) {}
  location.replace('./index.html');
})();
</script>
<noscript><a href="./index.html">오늘 한 걸음 열기</a></noscript>
</body>
</html>
""", encoding='utf-8')

# 6) Guardrails.
i = index.read_text(encoding='utf-8')
w = sw.read_text(encoding='utf-8')
n = native.read_text(encoding='utf-8')
assert "const BUILD = 'V8.0.5';" in i
assert "sessionStorage.getItem('ohg.native.app') === '1'" in i
assert 'Android 앱 연결 확인됨 · ' in i
assert "const APP_VERSION = 'V8.0.5';" in w
assert "const V = 'ohg-v805';" in w
assert "'./native.html'" in w
assert "sessionStorage.setItem('ohg.native.app', '1')" in n
assert "location.replace('./index.html')" in n
print('V8.0.5 web native-entry patch: PASS')
