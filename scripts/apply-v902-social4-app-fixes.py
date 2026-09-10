from pathlib import Path


def one(text, old, new, label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    return text.replace(old,new,1)

# index.html — 서버와 닉네임 규칙·오류 메시지를 일치시킵니다.
p=Path('index.html'); s=p.read_text(encoding='utf-8')
s=one(s,
"""  const compact=n.replace(/\\s/g,'');
  if(['관리자','운영자','오늘한걸음','마음프로'].includes(compact)) return '';
  return n;""",
"""  const compact=n.replace(/\\s/g,'').toLowerCase();
  if(/관리자|운영자|오늘한걸음|마음프로|admin|official|staff/i.test(compact)) return '';
  return n;""",
'socialNick reserved rule')
s=one(s,
"""  if(code==='AUTH') return '소셜 프로필을 확인하지 못했습니다.';
  if(code==='TOO_FAST') return '잠시 후 다시 올려주세요.';""",
"""  if(code==='AUTH') return '소셜 프로필을 확인하지 못했습니다.';
  if(code==='INVALID_NICKNAME') return '닉네임은 2~12자의 한글·영문·숫자로 지어주세요. 관리자·운영자·오늘한걸음 같은 말은 사용할 수 없습니다.';
  if(code==='BUSY') return '지금 소셜 서버가 붐빕니다. 잠시 후 다시 시도해주세요.';
  if(code==='TOO_FAST') return '잠시 후 다시 올려주세요.';""",
'social API messages')
s=one(s,
"""    if(!nick){toast('닉네임은 2~12자로 다시 확인해주세요.');return;}""",
"""    if(!nick){toast('닉네임은 2~12자로 입력하고 관리자·운영자·오늘한걸음·마음프로·admin·official·staff와 혼동되는 이름은 피해주세요.');return;}""",
'local nickname message')
p.write_text(s,encoding='utf-8')

# sw.js — 같은 V9.0.2 패치라도 새 웹 자산을 확실히 받도록 캐시 리비전만 올립니다.
p=Path('sw.js'); s=p.read_text(encoding='utf-8')
s=one(s,"const V = 'ohg-v902-social-comments-r2';","const V = 'ohg-v902-social4-r3';",'service-worker cache revision')
p.write_text(s,encoding='utf-8')

# README — 같은 버전의 안정화 변경을 기존 V9.0.2 절에 누적합니다.
p=Path('README.md'); s=p.read_text(encoding='utf-8')
anchor="## V9.0.2 — 소셜 2단계 · 댓글과 운영 검토\n"
insert=(
"- social-4 안정화: 탈퇴 후 남의 글 응원 수 재계산, 삭제한 글·댓글도 하루/간격 제한에 포함, 미인증 신고의 신고시트 청소 방지, 닉네임 갱신 쓰기 횟수 고정, BUSY/INVALID_NICKNAME 안내, 운영 로그의 익명 ID 비노출을 반영했습니다.\n"
"- 앱의 닉네임 검증을 서버와 맞춰 관리자·운영자·오늘한걸음·마음프로·admin·official·staff가 포함된 혼동 가능 이름을 앱 단계에서도 막습니다. 같은 V9.0.2 패치가 즉시 반영되도록 서비스워커 캐시 리비전을 `ohg-v902-social4-r3`로 갱신했습니다.\n")
if insert not in s:
    s=one(s,anchor,anchor+insert,'README V9.0.2 anchor')
s=s.replace('`V9.0.2-social-3`으로 다시 병합했습니다.','`V9.0.2-social-4`로 안정화했습니다.',1)
s=s.replace('`social-apps-script.gs` V9.0.2-social-3 배포','`social-apps-script.gs` V9.0.2-social-4 배포',1)
p.write_text(s,encoding='utf-8')

# SOCIAL_SETUP — 배포 기준본 표기 현행화.
p=Path('SOCIAL_SETUP.md'); s=p.read_text(encoding='utf-8')
s=s.replace('현재 저장소의 소셜 서버 기준본은 **V9.0.2-social-3**입니다.','현재 저장소의 소셜 서버 기준본은 **V9.0.2-social-4**입니다.',1)
marker='실제 운영 중이던 `V9.0.1-social-2`를 기준으로 댓글 기능만 병합했으며, social-2의 요청 크기 제한·feed/commentList 읽기 lock 분리·Asia/Seoul 기준·Google Sheets 수식주입 방어·내부 오류 비노출을 유지합니다.\n'
extra='social-4는 탈퇴 후 응원 수 정합성, 글·댓글 삭제를 이용한 작성 제한 우회, 신고 전 인증 순서, 닉네임 갱신 쓰기 횟수, BUSY/닉네임 오류 안내를 보정합니다. 탈퇴로 함께 삭제되는 다른 사용자의 댓글은 그 사용자의 userId를 유지해 작성 제한 집계에서 빠지지 않게 하며, 운영 점검 Logger에는 익명 ID를 남기지 않습니다.\n'
if extra not in s:
    s=one(s,marker,marker+'\n'+extra,'SOCIAL_SETUP social-4 note')
p.write_text(s,encoding='utf-8')

# 불변 조건
idx=Path('index.html').read_text(encoding='utf-8')
sw=Path('sw.js').read_text(encoding='utf-8')
assert "const BUILD='V9.0.2';" in idx
assert 'const DATA_SCHEMA = 6;' in idx
assert "const SOCIAL_KEY = 'ohg.social.v1';" in idx
assert "const APP_VERSION = 'V9.0.2';" in sw
assert "const V = 'ohg-v902-social4-r3';" in sw
assert 'HALTS.find' not in idx
assert '/관리자|운영자|오늘한걸음|마음프로|admin|official|staff/i.test(compact)' in idx
assert "if(code==='BUSY')" in idx and "if(code==='INVALID_NICKNAME')" in idx
print('V9.0.2 social-4 app patch invariants PASS')
