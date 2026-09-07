from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''  s.innerHTML = updReady
    ? '자원 목록 · 화면 설정 · 마음프로 음성 · 앱 새로고침 · 앱 설치<br><span class="flag">새 판 ' +
      esc(updReady) + ' 이 나와 있습니다</span>'
    : '자원 목록 · 화면 설정 · 마음프로 음성 · 앱 새로고침 · 앱 설치';'''
new='''  const voice = nativeAndroidApp() ? ' · 마음프로 음성' : '';
  s.innerHTML = updReady
    ? '자원 목록 · 화면 설정' + voice + ' · 앱 새로고침 · 앱 설치<br><span class="flag">새 판 ' +
      esc(updReady) + ' 이 나와 있습니다</span>'
    : '자원 목록 · 화면 설정' + voice + ' · 앱 새로고침 · 앱 설치';'''
if s.count(old)!=1: raise SystemExit('markAppAcc target mismatch')
p.write_text(s.replace(old,new,1),encoding='utf-8')
