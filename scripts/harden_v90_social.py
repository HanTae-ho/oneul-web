from pathlib import Path

# ---------- backend ----------
p=Path('social-apps-script.gs')
s=p.read_text(encoding='utf-8')

def one(txt,old,new,name):
    n=txt.count(old)
    if n!=1: raise SystemExit(f'{name}: expected 1 match, got {n}')
    return txt.replace(old,new,1)

s=one(s,"    if(a === 'feed') return json_(feed_(e.parameter || {}));\n",'', 'remove unauth GET feed')
s=one(s,"      if(action === 'profile') return json_(profile_(body));\n","      if(action === 'feed') return json_(feed_(body));\n      if(action === 'profile') return json_(profile_(body));\n      if(action === 'profileDelete') return json_(profileDelete_(body));\n",'post feed/delete routes')
s=one(s,"  const requester = cleanId_(p.userId || '');\n","  const me = auth_(p.userId,p.token); if(!me.ok) return me;\n  const requester = me.userId;\n",'authenticate feed')

anchor="""function postCreate_(b){
"""
profile_delete=r'''function profileDelete_(b){
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
  const now=Date.now();
  const profiles=rows_(SOCIAL_SHEETS.profiles);
  const profile=profiles.find(r=>str_(r.userId)===me.userId);
  if(!profile) return {ok:false,error:'NOT_FOUND'};

  // 작성글은 본문과 표시 닉네임을 비우고 삭제 상태로 전환합니다.
  const posts=rows_(SOCIAL_SHEETS.posts).filter(r=>str_(r.userId)===me.userId);
  const postIds=new Set(posts.map(r=>str_(r.postId)));
  const psh=sheet_(SOCIAL_SHEETS.posts);
  posts.forEach(r=>{
    psh.getRange(r._row,3).setValue('');
    psh.getRange(r._row,4).setValue('');
    psh.getRange(r._row,6).setValue(now);
    psh.getRange(r._row,7).setValue('deleted');
    psh.getRange(r._row,8).setValue(0);
  });

  // 내가 누른 응원과 내 글에 달린 응원 관계를 함께 정리합니다.
  const supports=rows_(SOCIAL_SHEETS.supports)
    .filter(r=>str_(r.userId)===me.userId || postIds.has(str_(r.postId)))
    .map(r=>r._row).sort((a,b)=>b-a);
  const ssh=sheet_(SOCIAL_SHEETS.supports);
  supports.forEach(row=>ssh.deleteRow(row));

  const sh=sheet_(SOCIAL_SHEETS.profiles);
  sh.getRange(profile._row,2).setValue('');
  sh.getRange(profile._row,3).setValue('');
  sh.getRange(profile._row,5).setValue(now);
  sh.getRange(profile._row,6).setValue('deleted');
  return {ok:true};
}

'''
s=one(s,anchor,profile_delete+anchor,'profile delete function')

old="""function report_(b){
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
"""
new="""function report_(b){
  cleanupReports_();
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
"""
s=one(s,old,new,'report cleanup call')

helper=r'''
function cleanupReports_(){
  const cutoff=Date.now()-365*24*60*60*1000;
  const old=rows_(SOCIAL_SHEETS.reports).filter(r=>num_(r.createdAt)>0 && num_(r.createdAt)<cutoff).map(r=>r._row).sort((a,b)=>b-a);
  if(!old.length) return;
  const sh=sheet_(SOCIAL_SHEETS.reports);
  old.forEach(row=>sh.deleteRow(row));
}
'''
s=one(s,"function validNick_(v){",helper+"\nfunction validNick_(v){",'report cleanup helper')
p.write_text(s,encoding='utf-8')

# ---------- frontend ----------
p=Path('index.html')
s=p.read_text(encoding='utf-8')

old=r'''async function socialReadFeed(){
  const base=socialEndpoint(); if(!base) throw new Error('소셜 서버가 아직 연결되지 않았습니다.');
  const u=new URL(base); u.searchParams.set('action','feed'); u.searchParams.set('sort',socialState.sort); if(SO.profile&&SO.profile.userId) u.searchParams.set('userId',SO.profile.userId);
  let r; try{r=await fetch(u.href,{cache:'no-store'});}catch(_){throw new Error('소셜 서버에 연결하지 못했습니다.');}
  if(!r.ok) throw new Error('소셜 피드를 불러오지 못했습니다.');
  const j=await r.json(); if(!j||!j.ok) throw new Error('소셜 피드를 불러오지 못했습니다.'); return Array.isArray(j.items)?j.items:[];
}'''
new=r'''async function socialReadFeed(){
  const j=await socialWrite('feed',Object.assign({sort:socialState.sort},socialAuth()));
  return Array.isArray(j.items)?j.items:[];
}'''
s=one(s,old,new,'authenticated frontend feed')

s=one(s,"  if(code==='OWNER') return '내가 작성한 글만 수정할 수 있습니다.';\n","  if(code==='OWNER') return '내가 작성한 글만 수정할 수 있습니다.';\n  if(code==='NICK_TAKEN') return '이미 사용 중인 닉네임입니다.';\n",'nickname error')

old="""+'</div>':'')+'<div style=\"height:9px\"></div><button class=\"btn ghost\" onclick=\"closeModal()\">닫기</button>');
"""
new="""+'</div><button class=\"btn ghost sm\" id=\"social-profile-delete\" style=\"margin-top:12px;color:var(--bad);border-color:var(--bad)\">소셜 프로필 삭제</button>':'')+'<div style=\"height:9px\"></div><button class=\"btn ghost\" onclick=\"closeModal()\">닫기</button>');
"""
s=one(s,old,new,'profile delete button')

old="""  $$('[data-social-unblock]').forEach(b=>b.onclick=()=>{const i=Number(b.dataset.socialUnblock);if(i>=0){SO.blocks.splice(i,1);socialSave();socialProfileModal();if(cur==='social')drawSocial();}});
}
function socialCompose(post){
"""
new="""  $$('[data-social-unblock]').forEach(b=>b.onclick=()=>{const i=Number(b.dataset.socialUnblock);if(i>=0){SO.blocks.splice(i,1);socialSave();socialProfileModal();if(cur==='social')drawSocial();}});
  const del=$('#social-profile-delete'); if(del) del.onclick=socialProfileDeleteConfirm;
}
function socialProfileDeleteConfirm(){
  const p=SO.profile; if(!p) return;
  modal('<h2>소셜 프로필을 삭제할까요?</h2><p class=\"muted\">서버에 등록된 익명 프로필과 내가 작성한 공개 글·응원 관계를 삭제합니다. 이 기기의 차단·숨김 목록도 함께 지웁니다. 되돌릴 수 없습니다.</p><button class=\"btn danger\" id=\"social-profile-delete-yes\">소셜 프로필 삭제</button><button class=\"btn ghost\" onclick=\"closeModal()\" style=\"margin-top:8px\">그만두기</button>');
  $('#social-profile-delete-yes').onclick=async()=>{
    try{
      if(p.registeredUrl){
        if(!socialEndpoint()){toast('소셜 서버에 연결된 뒤 다시 삭제해주세요.');return;}
        await socialWrite('profileDelete',socialAuth());
      }
      SO=socialBlank(); socialSave(); socialResetFeed(); closeModal(); drawSocial(); toast('소셜 프로필을 삭제했습니다.');
    }catch(e){toast(socialApiMessage(e));}
  };
}
function socialCompose(post){
"""
s=one(s,old,new,'profile delete frontend')
p.write_text(s,encoding='utf-8')

# ---------- privacy ----------
p=Path('privacy.html')
s=p.read_text(encoding='utf-8')
s=one(s,
"<p>오늘 한 걸음은 회복일 확인, 기록·통계, 일정·알림, 12단계·회복 실천도구, 자가점검, 지역 자원 안내, 마음프로 AI 답변, 이용자 의견 접수 등 앱 기능을 제공하기 위해 필요한 정보를 처리합니다.</p>",
"<p>오늘 한 걸음은 회복일 확인, 기록·통계, 일정·알림, 12단계·회복 실천도구, 자가점검, 지역 자원 안내, 마음프로 AI 답변, 이용자 의견 접수와 선택형 익명 소셜 기능을 제공하기 위해 필요한 정보를 처리합니다.</p>",
'privacy purpose')
s=one(s,
"<li>기기 기록은 사용자가 직접 내보내지 않는 한 별도 운영 서버로 자동 백업하지 않습니다.</li>",
"<li>기기 기록은 사용자가 직접 내보내지 않는 한 별도 운영 서버로 자동 백업하지 않습니다.</li>\n<li><b>소셜을 선택해 사용할 때:</b> 별도 소셜 저장공간에 익명 내부 사용자 ID·인증토큰·차단/숨김 목록이 저장되고, 소셜 전용 서버에는 익명 ID의 해시 인증정보·닉네임·직접 작성한 게시글·응원·신고 정보가 처리됩니다. 회복기록은 자동 첨부하지 않습니다.</li>",
'privacy social data')
s=one(s,
"<tr><td>Google Apps Script / Google Sheets</td><td>자원목록 제공, 의견 접수, 마음프로 API 중계</td><td>자원 요청, 이용자가 작성한 의견과 앱 버전, 마음프로 AI 요청 데이터</td></tr>",
"<tr><td>Google Apps Script / Google Sheets</td><td>자원목록 제공, 의견 접수, 마음프로 API 중계</td><td>자원 요청, 이용자가 작성한 의견과 앱 버전, 마음프로 AI 요청 데이터</td></tr>\n<tr><td>Google Apps Script / Google Sheets (소셜 전용)</td><td>익명 소셜 프로필·피드·응원·신고 처리</td><td>익명 내부 사용자 ID, 토큰 해시, 닉네임, 직접 작성한 게시글, 응원·신고 정보</td></tr>",
'privacy external social')
s=one(s,
"<li><b>앱에 바라는 점:</b> 운영 목적 달성 후 삭제하며 장기 보관이 필요하지 않은 경우 1년 이내 정리합니다.</li>",
"<li><b>앱에 바라는 점:</b> 운영 목적 달성 후 삭제하며 장기 보관이 필요하지 않은 경우 1년 이내 정리합니다.</li>\n<li><b>소셜 프로필·게시글·응원:</b> 사용자가 소셜 프로필 화면에서 프로필을 삭제하면 서버의 익명 프로필과 작성글·응원 관계를 삭제 상태로 정리하며, 개별 게시글도 직접 삭제할 수 있습니다. 기기 내 소셜 프로필·차단·숨김 목록도 함께 지울 수 있습니다.</li>\n<li><b>소셜 신고:</b> 안전·운영 확인을 위해 최대 1년 보관한 뒤 소셜 서버에서 정리합니다.</li>",
'privacy retention social')
s=one(s,
"<p class=\"small\">일반 사용자 계정이 없으므로 별도의 회원탈퇴 절차는 없습니다.</p>",
"<p class=\"small\">일반 앱 계정·로그인은 없습니다. 선택해서 만든 익명 소셜 프로필은 소셜 프로필 화면에서 별도로 삭제할 수 있습니다.</p>",
'privacy account deletion')
s=one(s,
"<li>‘앱에 바라는 점’은 이용자가 직접 작성·전송하는 선택 기능입니다.</li>",
"<li>‘앱에 바라는 점’은 이용자가 직접 작성·전송하는 선택 기능입니다.</li>\n<li>소셜은 선택 기능이며 익명 닉네임을 만들거나 변경할 수 있고, 내 게시글을 수정·삭제하거나 소셜 프로필 전체를 삭제할 수 있습니다. 다른 사용자의 글은 신고하거나 기기에서 차단할 수 있습니다.</li>",
'privacy choices social')
# Footer was stale from an old pre-V8.5 version; align it now.
import re
s2,n=re.subn(r'<footer>오늘 한 걸음 개인정보처리방침 · 시행일 2026-09-09 · 앱 기준 V[^<]+</footer>', '<footer>오늘 한 걸음 개인정보처리방침 · 시행일 2026-09-09 · 앱 기준 V9.0</footer>', s, count=1)
if n!=1: raise SystemExit(f'privacy footer: expected 1, got {n}')
p.write_text(s2,encoding='utf-8')

# ---------- docs ----------
p=Path('SOCIAL_SETUP.md'); s=p.read_text(encoding='utf-8')
s=one(s,
"- 내 글 수정·삭제\n- 다른 사용자 신고",
"- 내 글 수정·삭제\n- 소셜 프로필 삭제(작성글·응원 정리)\n- 다른 사용자 신고",
'setup scope delete')
s=one(s,
"- 신고 기록은 운영 확인용으로 저장됨.\n- 사용자가 앱 데이터/브라우저 데이터를 삭제해 소셜 토큰을 잃으면 기존 게시글의 소유자 권한을 복구할 계정 로그인 기능은 V9.0에 없음.",
"- 신고 기록은 운영 확인용으로 최대 1년 저장되고 이후 정리됨.\n- 소셜 프로필 삭제는 서버의 프로필·작성글·응원 관계를 정리하고 기기의 소셜 전용 데이터도 비움.\n- 사용자가 앱 데이터/브라우저 데이터를 먼저 삭제해 소셜 토큰을 잃으면 기존 게시글의 소유자 권한을 복구할 계정 로그인 기능은 V9.0에 없음. 따라서 서버 프로필 삭제가 필요하면 앱 데이터 삭제 전에 소셜 프로필 삭제를 먼저 실행해야 함.",
'setup privacy')
p.write_text(s,encoding='utf-8')

p=Path('README.md'); s=p.read_text(encoding='utf-8')
s=one(s,
"- 전용 SOCIAL_URL이 연결되면 `오늘의 한 걸음` 글 작성, 최신/응원 많은 글 피드, 1종 응원, 내 글 수정·삭제, 다른 사용자 신고·기기 내 차단을 사용할 수 있습니다.",
"- 전용 SOCIAL_URL이 연결되면 `오늘의 한 걸음` 글 작성, 최신/응원 많은 글 피드, 1종 응원, 내 글 수정·삭제, 소셜 프로필 삭제, 다른 사용자 신고·기기 내 차단을 사용할 수 있습니다. 피드 조회와 쓰기는 기기 보유 토큰으로 인증합니다.",
'readme social auth/delete')
p.write_text(s,encoding='utf-8')
