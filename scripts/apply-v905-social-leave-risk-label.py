from pathlib import Path
import re


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, got {n}')
    return text.replace(old, new, 1)

# index.html
p = Path('index.html')
s = p.read_text(encoding='utf-8')

s, n = re.subn(r"const BUILD\s*=\s*'V9\.0\.4';", "const BUILD='V9.0.5';", s, count=1)
if n != 1:
    raise SystemExit(f'BUILD: expected 1 occurrence, got {n}')

s = replace_once(s, '미래의 나에게 바로보기', '초심 보기', 'urge capsule label')

old_faq = '탈퇴는 두 번 확인하며, 사용하던 닉네임은 탈퇴 후 <b>30일 동안 재사용할 수 없습니다.</b>'
new_faq = '탈퇴 확인창에서 삭제되는 범위를 확인한 뒤 바로 탈퇴할 수 있으며, 사용하던 닉네임은 탈퇴 후 <b>30일 동안 재사용할 수 없습니다.</b>'
s = replace_once(s, old_faq, new_faq, 'social FAQ leave flow')

start = s.rfind('socialProfileDeleteConfirm=function(){')
end = s.find('\n\n</script>', start)
if start < 0 or end < 0:
    raise SystemExit('socialProfileDeleteConfirm block not found')
old_block = s[start:end]
for required in ['탈퇴 계속', '정말 탈퇴할까요?', 'social-leave-word', 'social-leave-next']:
    if required not in old_block:
        raise SystemExit(f'expected old leave flow marker missing: {required}')

new_block = """socialProfileDeleteConfirm=function(){
  const p=SO.profile;if(!p)return;
  modal('<h2>소셜 탈퇴</h2><p class=\"muted\">탈퇴하면 익명 프로필과 내가 작성한 공개 게시물·댓글·응원 관계가 삭제됩니다. 차단·숨김 목록도 이 기기에서 지워집니다.<br><br>사용하던 닉네임은 탈퇴 후 <b>30일 동안 재사용할 수 없으며</b>, 개인 회복기록은 삭제되지 않습니다.</p><button class=\"btn danger\" id=\"social-leave-confirm\">소셜 탈퇴</button><button class=\"btn ghost\" onclick=\"closeModal()\" style=\"margin-top:8px\">취소</button>');
  const yes=$('#social-leave-confirm');
  yes.onclick=async()=>{try{if(p.registeredUrl){if(!socialEndpoint()){toast('소셜 서버에 연결된 뒤 다시 탈퇴해주세요.');return;}await socialWrite('profileDelete',socialAuth());}SO=socialBlank();socialSave();socialResetFeed();socialProfileState={tab:'posts',loading:false,data:null,error:''};closeModal();go('social',{replace:true});toast('소셜에서 탈퇴했습니다.');}catch(e){toast(socialApiMessage(e));}};
};"""
s = s[:start] + new_block + s[end:]

for forbidden in ['social-leave-word', 'social-leave-next', '정말 탈퇴할까요?', '탈퇴 계속']:
    if forbidden in s:
        raise SystemExit(f'stale leave flow marker remains: {forbidden}')
if 'id="ur-capsule-toggle" aria-expanded="false">초심 보기</button>' not in s:
    raise SystemExit('초심 보기 button not found after patch')

p.write_text(s, encoding='utf-8')

# sw.js
p = Path('sw.js')
s = p.read_text(encoding='utf-8')
s = replace_once(s, "const APP_VERSION = 'V9.0.4';", "const APP_VERSION = 'V9.0.5';", 'sw APP_VERSION')
s = replace_once(s, "const V = 'ohg-v904-social-manage-r1';", "const V = 'ohg-v905-social-leave-r1';", 'sw cache')
p.write_text(s, encoding='utf-8')

# README.md
p = Path('README.md')
s = p.read_text(encoding='utf-8')
head = """## V9.0.5 — 소셜 탈퇴 단순화 · 충동 화면 문구 정리
- `⋮ → 소셜 탈퇴`는 확인창 1회에서 삭제 범위와 닉네임 30일 보호를 안내하고, `소셜 탈퇴`를 누르면 바로 처리하도록 단순화했습니다. `탈퇴 계속`, 두 번째 확인, `탈퇴` 직접 입력 단계는 제거했습니다.
- `지금 위험해요 → 충동`의 `미래의 나에게 바로보기` 버튼 문구를 `초심 보기`로 단순화했습니다. 연결 기능과 저장 데이터는 그대로 유지합니다.
- 소셜 서버는 이미 배포된 `V9.0.4-social-1`을 그대로 사용하며 30일 닉네임 보호 로직은 변경하지 않습니다.
- `DATA_SCHEMA=6`, `ohg.v1`, `ohg.social.v1`, Android 네이티브 알림/TTS 엔진과 하단 메뉴 구조는 변경하지 않습니다.

"""
if not s.startswith('## V9.0.4'):
    raise SystemExit('README top baseline unexpected')
p.write_text(head + s, encoding='utf-8')

# verify.js
p = Path('verify.js')
s = p.read_text(encoding='utf-8')
anchor = "ok(/NICK_COOLDOWN/.test(index)&&/NICK_COOLDOWN/.test(read('social-apps-script.gs')),'앱·서버 닉네임 보호 오류 계약 일치');\n"
extra = """ok(/id=\"social-leave-confirm\"/.test(index)&&!/social-leave-word|social-leave-next|정말 탈퇴할까요\?|탈퇴 계속/.test(index),'소셜 탈퇴 확인 1회로 단순화');
ok(/id=\"ur-capsule-toggle\" aria-expanded=\"false\">초심 보기<\/button>/.test(index),'충동 화면 초심 보기 문구 적용');
"""
if anchor not in s:
    raise SystemExit('verify anchor not found')
s = s.replace(anchor, anchor + extra, 1)
p.write_text(s, encoding='utf-8')

print('V9.0.5 minimal patch applied')
