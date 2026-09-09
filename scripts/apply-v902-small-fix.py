from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
count=s.count('HALTS.find')
if count != 3:
    raise SystemExit(f'HALTS.find expected 3, found {count}')
s=s.replace('HALTS.find','HALT.find')
if "const DATA_SCHEMA = 6;" not in s or "const SOCIAL_KEY = 'ohg.social.v1';" not in s:
    raise SystemExit('storage invariants missing')
p.write_text(s,encoding='utf-8')

p=Path('sw.js')
s=p.read_text(encoding='utf-8')
old="const V = 'ohg-v902-social-comments';"
new="const V = 'ohg-v902-social-comments-r2';"
if old not in s:
    raise SystemExit('sw cache key not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

p=Path('README.md')
s=p.read_text(encoding='utf-8')
needle='## V9.0.2 — 소셜 2단계 · 댓글과 운영 검토\n'
extra='- 런타임 점검에서 `통계 · 패턴`의 `HALTS` 오타 3곳을 확인해 실제 상수명 `HALT`로 수정했습니다. 같은 유형의 참조 오류를 막기 위해 브라우저 JS `no-undef` CI 검사를 추가했습니다.\n- 소셜 서버는 실제 운영 기준본 `V9.0.1-social-2`의 요청 크기 제한·읽기 lock 분리·Asia/Seoul 기준·수식주입 방어·내부 오류 비노출을 유지한 `V9.0.2-social-3`으로 다시 병합했습니다.\n'
if extra not in s:
    if needle not in s:
        raise SystemExit('README V9.0.2 heading not found')
    s=s.replace(needle,needle+extra,1)
s=s.replace('V9.0.2-social-1','V9.0.2-social-3')
p.write_text(s,encoding='utf-8')

p=Path('SOCIAL_SETUP.md')
s=p.read_text(encoding='utf-8')
head='# V9.0.2 댓글 확장 배포 메모\n'
intro='\n현재 저장소의 소셜 서버 기준본은 **V9.0.2-social-3**입니다. 실제 운영 중이던 `V9.0.1-social-2`를 기준으로 댓글 기능만 병합했으며, social-2의 요청 크기 제한·feed/commentList 읽기 lock 분리·Asia/Seoul 기준·Google Sheets 수식주입 방어·내부 오류 비노출을 유지합니다.\n'
if intro not in s:
    if head not in s:
        raise SystemExit('SOCIAL_SETUP heading not found')
    s=s.replace(head,head+intro,1)
s=s.replace('`Profiles / Posts / Supports / Reports` 네 시트가 만들어지는지 확인합니다.','`Profiles / Posts / Comments / Supports / Reports / CommentReports` 여섯 시트가 만들어지는지 확인합니다.')
s=s.replace('이 스프레드시트에는 익명 사용자 ID·닉네임·공개 게시글·응원·신고만 저장합니다.','이 스프레드시트에는 익명 사용자 ID·닉네임·공개 게시글·댓글·응원·신고만 저장합니다.')
s=s.replace('아직 하지 않음: 댓글, 개인 메시지, 친구/팔로우, 그룹/하이브, 접속자 수, 전문가/기관 계정.','V9.0 당시에는 댓글이 없었고 V9.0.2에서 댓글·댓글 신고가 추가되었습니다. 아직 하지 않음: 개인 메시지, 친구/팔로우, 답글, 그룹/하이브, 접속자 수, 전문가/기관 계정.')
s=s.replace('> 자원서버가 `config.SOCIAL_URL`을 앱에 내려주는 작업은 별도 보류 항목입니다. 이 연결이 완료되기 전에는 앱이 소셜 서버 준비 중으로 표시됩니다.','> 자원서버 **v1.8.1**에서 `[설정] SOCIAL_URL`을 `config.socialUrl`로 내려주는 최소 보정본을 준비했습니다. 실제 연결은 자원 Apps Script를 v1.8.1로 기존 웹앱 배포의 새 버전으로 갱신한 뒤 확인합니다.')
p.write_text(s,encoding='utf-8')

idx=Path('index.html').read_text(encoding='utf-8')
server=Path('social-apps-script.gs').read_text(encoding='utf-8')
sw=Path('sw.js').read_text(encoding='utf-8')
assert 'HALTS.find' not in idx
assert idx.count('HALT.find') >= 3
assert "const DATA_SCHEMA = 6;" in idx
assert "const SOCIAL_KEY = 'ohg.social.v1';" in idx
for token in ["V9.0.2-social-3",'MAX_SOCIAL_REQUEST_CHARS','SOCIAL_TIME_ZONE','function commentList_','function commentCreate_','function commentDelete_','function commentReport_','function SOCIAL_REVIEW_CHECK','cellText_(text)']:
    assert token in server, token
assert 'ohg-v902-social-comments-r2' in sw
print('V9.0.2 runtime/social patch invariants PASS')
