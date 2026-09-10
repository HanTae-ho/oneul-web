from pathlib import Path
import json


def one(s, old, new, label):
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1, found {n}')
    return s.replace(old, new, 1)

idx = Path('index.html')
s = idx.read_text(encoding='utf-8')

s = one(s, "const BUILD='V9.0.4';", "const BUILD='V9.0.5';", 'BUILD')
s = one(s, '>미래의 나에게 바로보기</button>', '>초심 보기</button>', 'urge capsule label')

# 소셜 탈퇴: 설명 1회 + 바로 탈퇴. 직접 입력/두 번째 확인은 제거.
start = s.find('socialProfileDeleteConfirm=function(){')
end = s.find('\n\n</script>', start)
if start < 0 or end < 0:
    raise SystemExit('socialProfileDeleteConfirm block not found')
new_leave = r'''socialProfileDeleteConfirm=function(){const p=SO.profile;if(!p)return;modal('<h2>소셜 탈퇴</h2><p class="muted">탈퇴하면 익명 프로필과 내가 작성한 공개 게시물·댓글·응원 관계가 삭제됩니다. 차단·숨김 목록도 이 기기에서 지워집니다.<br><br>사용하던 닉네임은 탈퇴 시점부터 <b>30일 동안 누구도 사용할 수 없으며</b>, 30일이 지난 뒤 다시 사용할 수 있습니다. <b>개인 회복기록은 삭제되지 않습니다.</b></p><button class="btn danger" id="social-leave-confirm">소셜 탈퇴</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">취소</button>');$('#social-leave-confirm').onclick=async()=>{try{if(p.registeredUrl){if(!socialEndpoint()){toast('소셜 서버에 연결된 뒤 다시 탈퇴해주세요.');return;}await socialWrite('profileDelete',socialAuth());}SO=socialBlank();socialSave();socialResetFeed();socialProfileState={tab:'posts',loading:false,data:null,error:''};closeModal();go('social',{replace:true});toast('소셜에서 탈퇴했습니다. 닉네임은 30일 동안 보호됩니다.');}catch(e){toast(socialApiMessage(e));}};};'''
s = s[:start] + new_leave + s[end:]

# FAQ: 탈퇴 절차와 Android 업데이트 안내 현행화.
s = one(s,
    '탈퇴는 두 번 확인하며, 사용하던 닉네임은 탈퇴 후 <b>30일 동안 재사용할 수 없습니다.</b>',
    '탈퇴 전 안내를 한 번 확인한 뒤 <b>소셜 탈퇴</b>를 누르면 바로 처리되며, 사용하던 닉네임은 탈퇴 후 <b>30일 동안 재사용할 수 없습니다.</b>',
    'social FAQ leave')
s = one(s,
    '<p style="margin-top:8px">마음프로 답변 자동 읽기와 이완 가이드는 Android 네이티브 TTS를 사용합니다. 일반 웹/PWA에서는 Android 전용 음성 기능이 표시되지 않을 수 있습니다.</p>',
    '<p style="margin-top:8px">마음프로 답변 자동 읽기와 이완 가이드는 Android 네이티브 TTS를 사용합니다. 일반 웹/PWA에서는 Android 전용 음성 기능이 표시되지 않을 수 있습니다.</p>\n      <p style="margin-top:8px">새 APK가 배포되면 <b>나 → 설정 → 앱</b>에 새 버전 안내와 <b>최신 버전 받기</b> 버튼이 표시됩니다. 앱 새로고침은 화면·콘텐츠 캐시만 다시 받는 기능이며 APK 업데이트와는 다릅니다. 업데이트 설치 시 개인 회복기록은 그대로 유지됩니다.</p>',
    'android FAQ update')

# 앱 설정: APK 업데이트 영역을 앱 새로고침과 분리.
marker = '''      <!-- 위의 [지금 새로 받기] 는 '목록' 만, 아래는 '앱 자체' 를 받습니다.
           둘이 다르다는 것을 설명에서 분명히 해야 엉뚱한 것을 안 누릅니다. -->
      <h3>앱 새로고침</h3>'''
replacement = '''      <div id="me-package-update" class="hide">
        <h3>앱 업데이트</h3>
        <p class="muted" id="me-package-update-m" style="margin:-4px 0 11px"></p>
        <button class="btn sm" id="me-package-update-go">최신 버전 받기</button>
        <div class="sep"></div>
      </div>

      <!-- 위의 [지금 새로 받기] 는 자원 목록, 앱 업데이트는 APK 설치,
           아래 새로고침은 화면·콘텐츠 캐시만 다시 받습니다. -->
      <h3>앱 새로고침</h3>'''
s = one(s, marker, replacement, 'app update UI')
s = one(s,
    '''      <p class="muted" style="margin:-4px 0 11px">
        고친 것이 안 보이거나 화면이 이상할 때 눌러주세요.
        앱을 새로 받아 다시 엽니다. <b>기록은 지워지지 않습니다.</b>
      </p>''',
    '''      <p class="muted" style="margin:-4px 0 11px">
        화면이나 콘텐츠가 정상적으로 갱신되지 않을 때 사용합니다.
        캐시를 비우고 화면 파일을 다시 불러옵니다. <b>기록은 지워지지 않습니다.</b>
      </p>''',
    'reload copy')

# 앱 설정 요약 문구에 업데이트 역할을 명시.
s = s.replace('자원 목록 · 화면 설정 · 마음프로 AI · 앱 새로고침 · 앱 설치',
              '자원 목록 · 화면 설정 · 마음프로 AI · 앱 업데이트 · 앱 새로고침 · 앱 설치')

# 버전 비교를 3자리까지 정확히 처리하고 설치 APK 버전/릴리즈 피드 지원.
vs = s.find('function appVersionParts(v){')
ve = s.find('/* 서버의 sw.js 를 캐시 없이 읽어 판을 봅니다.', vs)
if vs < 0 or ve < 0:
    raise SystemExit('version helper block not found')
version_block = r'''function appVersionParts(v){
  const m=String(v||'').trim().match(/^[vV]?(\d+)(?:\.(\d+))?(?:\.(\d+))?$/);
  return m?[Number(m[1]),Number(m[2]||0),Number(m[3]||0)]:null;
}
function isNewerAppVersion(remote,current){
  const r=appVersionParts(remote),c=appVersionParts(current);if(!r||!c)return false;
  for(let i=0;i<3;i++){if(r[i]!==c[i])return r[i]>c[i];}return false;
}
let pkgRelease=null;
let pkgReady='';
function nativeInstalledVersion(){
  if(!nativeAndroidApp())return '';
  try{const v=String(sessionStorage.getItem('ohg.native.version')||'').toUpperCase();return appVersionParts(v)?v:'';}catch(e){return '';}
}
async function checkPackageRelease(){
  if(!nativeAndroidApp()||location.protocol==='file:')return null;
  try{
    const r=await fetch('latest-release.json?_='+Date.now(),{cache:'no-store'});if(!r.ok)return null;
    const x=await r.json(),v=String(x&&x.version||'').toUpperCase(),apk=String(x&&x.apk||'');
    if(!appVersionParts(v)||!/^https:\/\/github\.com\/HanTae-ho\/oneul-web\/releases\/download\//.test(apk))return null;
    return {version:v,versionCode:Number(x.versionCode||0),apk:apk,release:String(x.release||'')};
  }catch(e){return null;}
}
async function drawPackageUpdate(){
  const box=$('#me-package-update'),msg=$('#me-package-update-m'),goBtn=$('#me-package-update-go');
  if(!box||!msg||!goBtn)return;
  if(!nativeAndroidApp()){box.classList.add('hide');pkgReady='';return;}
  const x=await checkPackageRelease();pkgRelease=x;
  const installed=nativeInstalledVersion();
  pkgReady=x&&(!installed||isNewerAppVersion(x.version,installed))?x.version:'';
  if(!pkgReady){box.classList.add('hide');markAppAcc();return;}
  box.classList.remove('hide');
  msg.innerHTML='<b>새 버전 '+esc(pkgReady)+'가 있습니다.</b><br>최신 기능과 수정사항을 적용하려면 앱을 업데이트해주세요. 개인 회복기록은 그대로 유지됩니다.'+(installed?'<br><span class="tiny">현재 설치 '+esc(installed)+'</span>':'');
  goBtn.onclick=()=>{if(pkgRelease&&pkgRelease.apk)location.href=pkgRelease.apk;};
  markAppAcc();
}
'''
s = s[:vs] + version_block + s[ve:]

# 설정 접기 요약: APK 업데이트를 우선 표시.
ms = s.find('function markAppAcc(){')
me = s.find('function drawReload(){', ms)
if ms < 0 or me < 0:
    raise SystemExit('markAppAcc block not found')
new_mark = r'''function markAppAcc(){
  const s=$('#acc-app-s');if(!s)return;
  const voice=nativeAndroidApp()?' · 마음프로 음성':'';
  const base='자원 목록 · 화면 설정 · 마음프로 AI'+voice+' · 앱 업데이트 · 앱 새로고침 · 앱 설치';
  if(pkgReady)s.innerHTML=base+'<br><span class="flag">새 앱 '+esc(pkgReady)+' 업데이트 가능</span>';
  else if(updReady)s.innerHTML=base+'<br><span class="flag">새 화면 버전 '+esc(updReady)+' 사용 가능</span>';
  else s.textContent=base;
}

'''
s = s[:ms] + new_mark + s[me:]

# drawReload 진입 때 APK 업데이트도 확인. 웹 캐시 상태는 '화면 버전'으로 명확히 표기.
s = one(s, 'function drawReload(){\n  markAppAcc();', 'function drawReload(){\n  markAppAcc();\n  drawPackageUpdate();', 'draw package update')
s = s.replace("st.textContent = '지금 판 ' + BUILD + ' · 확인하는 중…';", "st.textContent = '화면 버전 ' + BUILD + ' · 확인하는 중…';")
s = s.replace("st.innerHTML = '지금 판 ' + BUILD + ' · <b>새 판 '", "st.innerHTML = '화면 버전 ' + BUILD + ' · <b>새 화면 버전 '")
s = s.replace("st.textContent = '지금 판 ' + BUILD + ' · 최신입니다.';", "st.textContent = '화면 버전 ' + BUILD + ' · 최신입니다.';")

idx.write_text(s, encoding='utf-8')

# native.html: Android 패키지가 전달한 설치 버전을 세션에 보관.
native = Path('native.html')
n = native.read_text(encoding='utf-8')
n = one(n,
'''(function(){
  try { sessionStorage.setItem('ohg.native.app', '1'); } catch(e) {}
  location.replace('./index.html?native=1');
})();''',
'''(function(){
  try {
    sessionStorage.setItem('ohg.native.app', '1');
    const q=new URLSearchParams(location.search||'');
    const raw=String(q.get('appv')||'').trim();
    if(/^\\d+\\.\\d+\\.\\d+$/.test(raw)) sessionStorage.setItem('ohg.native.version','V'+raw);
  } catch(e) {}
  location.replace('./index.html?native=1');
})();''',
'native version marker')
native.write_text(n, encoding='utf-8')

# 서비스워커 버전 + 릴리즈 피드는 SW 캐시 대상에서 제외.
sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
w = one(w, "const APP_VERSION = 'V9.0.4';", "const APP_VERSION = 'V9.0.5';", 'sw version')
w = one(w, "const V = 'ohg-v904-social-manage-r1';", "const V = 'ohg-v905-update-flow-r1';", 'sw cache')
w = one(w, "  /* 자원 목록(Apps Script)은 절대 캐시하지 않습니다 */", "  /* 릴리즈 정보와 자원 목록은 서비스워커 캐시를 사용하지 않습니다 */\n  if (u.pathname.endsWith('/latest-release.json')) return;\n\n  /* 자원 목록(Apps Script)은 절대 캐시하지 않습니다 */", 'release feed bypass')
sw.write_text(w, encoding='utf-8')

# 최신 릴리즈 포인터는 V9.0.5 APK가 실제 게시되기 전까지 현재 V9.0.4를 가리킨다.
Path('latest-release.json').write_text(json.dumps({
    'version':'V9.0.4',
    'versionCode':899,
    'apk':'https://github.com/HanTae-ho/oneul-web/releases/download/v9.0.4-test/oneul-v9.0.4.apk',
    'release':'https://github.com/HanTae-ho/oneul-web/releases/tag/v9.0.4-test'
}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

# README
rd = Path('README.md')
r = rd.read_text(encoding='utf-8')
head = '''## V9.0.5 — 탈퇴 단순화 · 초심 보기 · APK 업데이트 안내
- 소셜 탈퇴는 안내를 한 번 확인한 뒤 `소셜 탈퇴`를 누르면 바로 처리합니다. `탈퇴 계속`, 두 번째 확인, `탈퇴` 직접 입력 단계는 제거했습니다. 서버의 탈퇴 닉네임 30일 보호는 그대로 유지합니다.
- `지금 위험해요 → 충동`의 `미래의 나에게 바로보기` 버튼을 짧은 `초심 보기`로 변경하며 연결 기능과 저장 데이터는 바꾸지 않습니다.
- Android 설치 앱의 새 APK가 배포되면 `나 → 설정 → 앱`에 `새 버전 Vx.x.x가 있습니다`와 `최신 버전 받기`를 표시합니다. `앱 새로고침`은 화면·콘텐츠 캐시 갱신 기능으로 분리합니다.
- `latest-release.json`을 배포 포인터로 사용하고 Android 패키지가 자신의 설치 버전을 `native.html?appv=`로 전달해, 웹 화면 버전이 먼저 갱신되어도 설치 APK 버전과 최신 릴리즈를 정확히 비교할 수 있게 합니다.
- `DATA_SCHEMA=6`, `ohg.v1`, `ohg.social.v1`, 소셜 서버 `V9.0.4-social-1`, Android 알림/TTS 엔진은 유지합니다.

'''
if r.startswith('## V9.0.5'):
    raise SystemExit('README already V9.0.5')
r = head + r
rd.write_text(r, encoding='utf-8')

# 검증 규칙
vp = Path('verify.js')
v = vp.read_text(encoding='utf-8')
anchor = "ok(!!build && cacheVersion.startsWith(expectedCachePrefix),'sw cache = '+expectedCachePrefix+' 계열');\n"
extra = """ok(/id=\"social-leave-confirm\"/.test(index)&&!/social-leave-next/.test(index)&&!/social-leave-word/.test(index),'소셜 탈퇴 1회 확인 후 바로 처리');
ok(/id=\"ur-capsule-toggle\"[^>]*>초심 보기<\\/button>/.test(index),'충동 화면 초심 보기 문구');
ok(/id=\"me-package-update\"/.test(index)&&/latest-release\\.json/.test(index)&&/function nativeInstalledVersion\\(\\)/.test(index),'Android APK 업데이트 안내/버전 비교');
ok(/ohg\\.native\\.version/.test(read('native.html'))&&/appv/.test(read('native.html')),'native.html 설치 APK 버전 마커');
ok(!/탈퇴는 두 번 확인하며/.test(index),'도움말 탈퇴 1회 확인 현행화');
"""
if anchor not in v:
    raise SystemExit('verify anchor missing')
v = v.replace(anchor, anchor+extra, 1)
vp.write_text(v, encoding='utf-8')

# 고정 불변조건
final = idx.read_text(encoding='utf-8')
assert "const DATA_SCHEMA = 6;" in final
assert "const SOCIAL_KEY = 'ohg.social.v1';" in final
assert "const BUILD='V9.0.5';" in final
assert 'social-leave-next' not in final
assert 'social-leave-word' not in final
assert '>초심 보기</button>' in final
assert "const SOCIAL_VERSION = 'V9.0.4-social-1';" in Path('social-apps-script.gs').read_text(encoding='utf-8')
print('V9.0.5 combined patch applied')
