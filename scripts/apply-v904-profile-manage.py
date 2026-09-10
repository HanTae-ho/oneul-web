from pathlib import Path


def one(s, old, new, label):
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    return s.replace(old,new,1)

# index.html
p=Path('index.html'); s=p.read_text(encoding='utf-8')
s=one(s,"const BUILD='V9.0.3';","const BUILD='V9.0.4';",'BUILD')

s=one(s,
'''<section class="pg" id="p-social-profile">
  <div class="sp" style="margin-bottom:11px">
    <button class="tiny" style="color:var(--acc);font-weight:600" id="social-profile-back">← 소셜</button>
    <h1 style="margin:0">내 소셜 프로필</h1>
    <span style="width:34px"></span>
  </div>
  <div id="social-profile-body"></div>
</section>''',
'''<section class="pg" id="p-social-profile">
  <div class="sp social-profile-titlebar" style="margin-bottom:11px">
    <button class="tiny" style="color:var(--acc);font-weight:600" id="social-profile-back">← 소셜</button>
    <h1 style="margin:0">내 소셜 프로필</h1>
    <button class="social-profile-manage" id="social-profile-manage" type="button" aria-label="소셜 관리">⋮</button>
  </div>
  <div id="social-profile-body"></div>
</section>''','profile header')

s=one(s,
'''  .social-profile-head .name span{display:block;margin-top:3px;font-size:12px;color:var(--dim)}
  .social-profile-tabs{display:flex;gap:7px;margin:12px 0}.social-profile-tabs button{flex:1;border:1px solid var(--line);border-radius:11px;padding:9px 6px;color:var(--dim);background:var(--panel)}''',
'''  .social-profile-head .name span{display:block;margin-top:3px;font-size:12px;color:var(--dim)}
  .social-profile-titlebar{position:relative}.social-profile-titlebar>h1{flex:1;text-align:center}
  .social-profile-manage{width:34px;height:34px;flex:none;border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--dim);font-size:24px;line-height:1}
  .social-profile-manage:active{background:var(--accbg);color:var(--acc)}
  .social-profile-support{margin-top:8px;font-size:12.5px;color:var(--dim)}.social-profile-support b{color:var(--tx);font-size:14px}
  .social-profile-tabs{display:flex;gap:7px;margin:12px 0}.social-profile-tabs button{flex:1;border:1px solid var(--line);border-radius:11px;padding:9px 6px;color:var(--dim);background:var(--panel)}''','profile css')

old_draw='''function drawSocialProfile(){
  const body=$('#social-profile-body'),back=$('#social-profile-back');if(!body)return;if(back)back.onclick=()=>appBack('social');const p=SO.profile;
  if(!p){body.innerHTML='<div class="empty">소셜 프로필이 없습니다.</div>';setTimeout(()=>go('social',{replace:true}),0);return;}
  const d=socialProfileState.data||{},st=d.stats||{postCount:0,commentCount:0,supportReceived:0},prof=d.profile||{};
  let html='<div class="card"><div class="social-profile-head"><span class="social-avatar">'+socialInitial(p.nickname)+'</span><span class="name"><b>'+esc(p.nickname)+'</b><span>'+esc(socialProfileDate(prof.createdAt))+'</span></span></div><div class="social-profile-stats"><div><b>'+Number(st.supportReceived||0)+'</b><span>받은 응원</span></div><div><b>'+Number(st.postCount||0)+'</b><span>게시물</span></div><div><b>'+Number(st.commentCount||0)+'</b><span>댓글</span></div></div><div class="social-profile-fixed"><b>닉네임은 가입 후 고정됩니다</b><span>잦은 이름 변경으로 다른 사람과 혼동되는 일을 줄이기 위한 기준입니다. 다른 닉네임을 사용하려면 소셜 탈퇴 후 새 프로필을 만들어주세요.</span></div></div>';
  if(socialProfileState.loading)html+='<div class="empty">내 활동을 불러오는 중입니다.</div>';else if(socialProfileState.error)html+='<div class="social-error">'+esc(socialProfileState.error)+'</div><button class="btn ghost sm" id="social-profile-retry">다시 불러오기</button>';else if(d&&d.ok){html+='<div class="social-profile-tabs"><button type="button" data-social-profile-tab="posts" class="'+(socialProfileState.tab==='posts'?'on':'')+'">게시물 '+Number(st.postCount||0)+'</button><button type="button" data-social-profile-tab="comments" class="'+(socialProfileState.tab==='comments'?'on':'')+'">댓글 '+Number(st.commentCount||0)+'</button></div>';const rows=socialProfileState.tab==='comments'?(d.comments||[]):(d.posts||[]);html+=rows.length?rows.map(socialProfileState.tab==='comments'?socialProfileCommentHtml:socialProfilePostHtml).join(''):'<div class="empty">'+(socialProfileState.tab==='comments'?'아직 작성한 댓글이 없습니다.':'아직 작성한 게시물이 없습니다.')+'</div>';}
  const blocked=SO.blocks||[];html+='<div class="card" style="margin-top:16px"><h3>차단한 사용자</h3>'+(blocked.length?blocked.map((b,i)=>'<div class="social-block-row"><span>'+esc(b.nickname||'익명')+'</span><button class="btn ghost sm" style="width:auto" data-social-profile-unblock="'+i+'">차단 해제</button></div>').join(''):'<p class="tiny">차단한 사용자가 없습니다.</p>')+'</div><div class="card social-profile-danger"><h3>탈퇴</h3><p class="muted">소셜 탈퇴는 닉네임 변경과 구분되는 별도 절차입니다. 탈퇴하면 내 공개 게시물·댓글·응원 관계와 익명 프로필을 삭제하며 되돌릴 수 없습니다.</p><button class="btn ghost" id="social-profile-leave" style="color:var(--bad);border-color:var(--bad)">소셜 탈퇴</button></div>';body.innerHTML=html;
  const retry=$('#social-profile-retry');if(retry)retry.onclick=()=>socialProfileLoad(true);$$('[data-social-profile-tab]').forEach(b=>b.onclick=()=>{socialProfileState.tab=b.dataset.socialProfileTab;drawSocialProfile();});$$('[data-social-profile-edit]').forEach(b=>b.onclick=()=>{const x=socialProfilePostById(b.dataset.socialProfileEdit);if(x)socialCompose(x);});$$('[data-social-profile-post-delete]').forEach(b=>b.onclick=()=>{const x=socialProfilePostById(b.dataset.socialProfilePostDelete);if(x)socialProfileDeletePost(x);});$$('[data-social-profile-comment-delete]').forEach(b=>b.onclick=()=>{const x=socialProfileCommentById(b.dataset.socialProfileCommentDelete);if(x)socialProfileDeleteComment(x);});$$('[data-social-profile-unblock]').forEach(b=>b.onclick=()=>{const i=Number(b.dataset.socialProfileUnblock);if(i>=0&&i<SO.blocks.length){SO.blocks.splice(i,1);socialSave();drawSocialProfile();if(socialState.loaded)drawSocial();}});const leave=$('#social-profile-leave');if(leave)leave.onclick=socialProfileDeleteConfirm;if(!socialProfileState.data&&!socialProfileState.loading&&!socialProfileState.error)setTimeout(()=>socialProfileLoad(false),0);
}'''
new_draw='''function drawSocialProfile(){
  const body=$('#social-profile-body'),back=$('#social-profile-back'),manage=$('#social-profile-manage');if(!body)return;if(back)back.onclick=()=>appBack('social');if(manage)manage.onclick=socialProfileManageMenu;const p=SO.profile;
  if(!p){if(manage)manage.style.display='none';body.innerHTML='<div class="empty">소셜 프로필이 없습니다.</div>';setTimeout(()=>go('social',{replace:true}),0);return;}if(manage)manage.style.display='flex';
  const d=socialProfileState.data||{},st=d.stats||{postCount:0,commentCount:0,supportReceived:0},prof=d.profile||{};
  let html='<div class="card"><div class="social-profile-head"><span class="social-avatar">'+socialInitial(p.nickname)+'</span><span class="name"><b>'+esc(p.nickname)+'</b><span>'+esc(socialProfileDate(prof.createdAt))+'</span><span class="social-profile-support">받은 응원 <b>'+Number(st.supportReceived||0)+'</b></span></span></div></div>';
  if(socialProfileState.loading)html+='<div class="empty">내 활동을 불러오는 중입니다.</div>';else if(socialProfileState.error)html+='<div class="social-error">'+esc(socialProfileState.error)+'</div><button class="btn ghost sm" id="social-profile-retry">다시 불러오기</button>';else if(d&&d.ok){html+='<div class="social-profile-tabs"><button type="button" data-social-profile-tab="posts" class="'+(socialProfileState.tab==='posts'?'on':'')+'">게시물 '+Number(st.postCount||0)+'</button><button type="button" data-social-profile-tab="comments" class="'+(socialProfileState.tab==='comments'?'on':'')+'">댓글 '+Number(st.commentCount||0)+'</button></div>';const rows=socialProfileState.tab==='comments'?(d.comments||[]):(d.posts||[]);html+=rows.length?rows.map(socialProfileState.tab==='comments'?socialProfileCommentHtml:socialProfilePostHtml).join(''):'<div class="empty">'+(socialProfileState.tab==='comments'?'아직 작성한 댓글이 없습니다.':'아직 작성한 게시물이 없습니다.')+'</div>';}
  body.innerHTML=html;
  const retry=$('#social-profile-retry');if(retry)retry.onclick=()=>socialProfileLoad(true);$$('[data-social-profile-tab]').forEach(b=>b.onclick=()=>{socialProfileState.tab=b.dataset.socialProfileTab;drawSocialProfile();});$$('[data-social-profile-edit]').forEach(b=>b.onclick=()=>{const x=socialProfilePostById(b.dataset.socialProfileEdit);if(x)socialCompose(x);});$$('[data-social-profile-post-delete]').forEach(b=>b.onclick=()=>{const x=socialProfilePostById(b.dataset.socialProfilePostDelete);if(x)socialProfileDeletePost(x);});$$('[data-social-profile-comment-delete]').forEach(b=>b.onclick=()=>{const x=socialProfileCommentById(b.dataset.socialProfileCommentDelete);if(x)socialProfileDeleteComment(x);});if(!socialProfileState.data&&!socialProfileState.loading&&!socialProfileState.error)setTimeout(()=>socialProfileLoad(false),0);
}
function socialProfileManageMenu(){
  if(!SO.profile)return;const blocked=SO.blocks||[];
  modal('<h2>소셜 관리</h2><h3 style="margin:4px 0 8px">차단한 사용자</h3><div id="social-manage-blocks">'+(blocked.length?blocked.map((b,i)=>'<div class="social-block-row"><span>'+esc(b.nickname||'익명')+'</span><button class="btn ghost sm" style="width:auto" data-social-manage-unblock="'+i+'">차단 해제</button></div>').join(''):'<p class="tiny">차단한 사용자가 없습니다.</p>')+'</div><div class="sep"></div><button class="btn ghost" id="social-manage-leave" style="color:var(--bad);border-color:var(--bad)">소셜 탈퇴</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">닫기</button>');
  $$('[data-social-manage-unblock]').forEach(b=>b.onclick=()=>{const i=Number(b.dataset.socialManageUnblock);if(i>=0&&i<SO.blocks.length){SO.blocks.splice(i,1);socialSave();socialProfileManageMenu();if(socialState.loaded)drawSocial();}});const leave=$('#social-manage-leave');if(leave)leave.onclick=socialProfileDeleteConfirm;
}'''
s=one(s,old_draw,new_draw,'drawSocialProfile')

old_delete="""socialProfileDeleteConfirm=function(){const p=SO.profile;if(!p)return;modal('<h2>소셜 탈퇴</h2><p class=\"muted\">탈퇴하면 익명 프로필과 내가 작성한 공개 게시물·댓글·응원 관계가 삭제됩니다. 차단·숨김 목록도 이 기기에서 지워집니다.<br><br><b>닉네임만 바꾸는 기능은 제공하지 않습니다.</b> 다른 닉네임을 쓰려는 경우에도 현재 프로필을 탈퇴한 뒤 새로 만들어야 합니다.</p><button class=\"btn danger\" id=\"social-leave-next\">탈퇴 계속</button><button class=\"btn ghost\" onclick=\"closeModal()\" style=\"margin-top:8px\">취소</button>');$('#social-leave-next').onclick=()=>{modal('<h2>정말 탈퇴할까요?</h2><p class=\"muted\">실수로 탈퇴하지 않도록 아래에 <b>탈퇴</b>라고 입력해주세요.</p><input id=\"social-leave-word\" autocomplete=\"off\" placeholder=\"탈퇴\"><button class=\"btn danger\" id=\"social-leave-confirm\" disabled style=\"margin-top:10px\">소셜 탈퇴</button><button class=\"btn ghost\" onclick=\"closeModal()\" style=\"margin-top:8px\">취소</button>');const input=$('#social-leave-word'),yes=$('#social-leave-confirm');input.oninput=()=>{yes.disabled=String(input.value||'').trim()!=='탈퇴';};yes.onclick=async()=>{if(String(input.value||'').trim()!=='탈퇴')return;try{if(p.registeredUrl){if(!socialEndpoint()){toast('소셜 서버에 연결된 뒤 다시 탈퇴해주세요.');return;}await socialWrite('profileDelete',socialAuth());}SO=socialBlank();socialSave();socialResetFeed();socialProfileState={tab:'posts',loading:false,data:null,error:''};closeModal();go('social',{replace:true});toast('소셜에서 탈퇴했습니다.');}catch(e){toast(socialApiMessage(e));}};};};"""
new_delete="""socialProfileDeleteConfirm=function(){const p=SO.profile;if(!p)return;modal('<h2>소셜 탈퇴</h2><p class=\"muted\">탈퇴하면 익명 프로필과 내가 작성한 공개 게시물·댓글·응원 관계가 삭제됩니다. 차단·숨김 목록도 이 기기에서 지워집니다.<br><br>사용하던 닉네임은 탈퇴 시점부터 <b>30일 동안 누구도 사용할 수 없으며</b>, 30일이 지난 뒤 다시 사용할 수 있습니다. 개인 회복기록은 삭제되지 않습니다.</p><button class=\"btn danger\" id=\"social-leave-next\">탈퇴 계속</button><button class=\"btn ghost\" onclick=\"closeModal()\" style=\"margin-top:8px\">취소</button>');$('#social-leave-next').onclick=()=>{modal('<h2>정말 탈퇴할까요?</h2><p class=\"muted\">실수로 탈퇴하지 않도록 아래에 <b>탈퇴</b>라고 입력해주세요.<br>이 닉네임은 30일 동안 재사용할 수 없습니다.</p><input id=\"social-leave-word\" autocomplete=\"off\" placeholder=\"탈퇴\"><button class=\"btn danger\" id=\"social-leave-confirm\" disabled style=\"margin-top:10px\">소셜 탈퇴</button><button class=\"btn ghost\" onclick=\"closeModal()\" style=\"margin-top:8px\">취소</button>');const input=$('#social-leave-word'),yes=$('#social-leave-confirm');input.oninput=()=>{yes.disabled=String(input.value||'').trim()!=='탈퇴';};yes.onclick=async()=>{if(String(input.value||'').trim()!=='탈퇴')return;try{if(p.registeredUrl){if(!socialEndpoint()){toast('소셜 서버에 연결된 뒤 다시 탈퇴해주세요.');return;}await socialWrite('profileDelete',socialAuth());}SO=socialBlank();socialSave();socialResetFeed();socialProfileState={tab:'posts',loading:false,data:null,error:''};closeModal();go('social',{replace:true});toast('소셜에서 탈퇴했습니다. 닉네임은 30일 동안 보호됩니다.');}catch(e){toast(socialApiMessage(e));}};};};"""
s=one(s,old_delete,new_delete,'leave confirm')

s=one(s,
"  if(code==='NICK_TAKEN') return '이미 사용 중인 닉네임입니다.';",
"  if(code==='NICK_TAKEN') return '이미 사용 중인 닉네임입니다.';\n  if(code==='NICK_COOLDOWN') return '최근 탈퇴한 닉네임입니다. 탈퇴 후 30일이 지나면 다시 사용할 수 있습니다.';",
'nick cooldown api message')

s=one(s,
'''      <p style="margin-top:8px">닉네임은 가입할 때 정하며 <b>가입 후에는 변경할 수 없습니다.</b> 다른 닉네임을 쓰려면 프로필의 탈퇴 영역에서 소셜 탈퇴 후 새 프로필을 만들어야 합니다. 탈퇴는 실수를 줄이기 위해 두 번 확인합니다.</p>
      <p style="margin-top:8px">다른 사용자의 게시물·댓글은 신고하거나 작성자를 차단할 수 있습니다. 개인메시지·친구·팔로우·답글·그룹·하이브 기능은 제공하지 않습니다. 생명이나 신체가 위급한 상황은 소셜 답변을 기다리지 말고 109·112·119 등 즉시 도움을 이용하세요.</p>''',
'''      <p style="margin-top:8px">닉네임은 가입할 때 정하며 가입 후에는 변경할 수 없습니다. <b>내 소셜 프로필 제목 오른쪽의 ⋮</b>에서 차단한 사용자를 관리하거나 소셜에서 탈퇴할 수 있습니다. 탈퇴는 두 번 확인하며, 사용하던 닉네임은 탈퇴 후 <b>30일 동안 재사용할 수 없습니다.</b></p>
      <p style="margin-top:8px">다른 사용자의 게시물·댓글은 신고하거나 작성자를 차단할 수 있습니다. 차단 목록은 평상시 프로필 화면에 노출하지 않고 ⋮의 소셜 관리에서만 확인합니다. 개인메시지·친구·팔로우·답글·그룹·하이브 기능은 제공하지 않습니다. 생명이나 신체가 위급한 상황은 소셜 답변을 기다리지 말고 109·112·119 등 즉시 도움을 이용하세요.</p>''','FAQ social')

p.write_text(s,encoding='utf-8')

# sw.js
p=Path('sw.js'); s=p.read_text(encoding='utf-8')
s=one(s,"const APP_VERSION = 'V9.0.3';","const APP_VERSION = 'V9.0.4';",'APP_VERSION')
s=one(s,"const V = 'ohg-v903-social-profile-r1';","const V = 'ohg-v904-social-manage-r1';",'SW cache')
p.write_text(s,encoding='utf-8')

# social server
p=Path('social-apps-script.gs'); g=p.read_text(encoding='utf-8')
g=one(g," * 오늘 한 걸음 V9.0.3 — 소셜 전용 Apps Script"," * 오늘 한 걸음 V9.0.4 — 소셜 전용 Apps Script",'social header')
g=one(g," * 서버판: V9.0.3-social-1"," * 서버판: V9.0.4-social-1",'social header version')
g=one(g,"const SOCIAL_VERSION = 'V9.0.3-social-1';","const SOCIAL_VERSION = 'V9.0.4-social-1';",'SOCIAL_VERSION')
g=one(g,"const MAX_PROFILE_ACTIVITY_ITEMS = 100;","const MAX_PROFILE_ACTIVITY_ITEMS = 100;\nconst NICK_REUSE_COOLDOWN_MS = 30 * 24 * 60 * 60 * 1000;",'cooldown const')

needle=""" * V9.0.3-social-1
 * - 가입 뒤 닉네임은 고정합니다. 변경하려면 소셜 탈퇴 후 새 프로필을 만듭니다.
 * - 내 프로필 페이지용 profileActivity 읽기 API를 추가합니다.
 * - 피드 공개 스냅샷과 내 응원목록을 짧게 캐시하고, 시트 헤더 검증도 캐시해 반복 읽기를 줄입니다.
 * - 쓰기 작업 뒤 관련 피드 캐시를 즉시 무효화합니다.
 *
 * ★ 앱에서 부를 때 주의"""
repl=""" * V9.0.3-social-1
 * - 가입 뒤 닉네임은 고정합니다. 변경하려면 소셜 탈퇴 후 새 프로필을 만듭니다.
 * - 내 프로필 페이지용 profileActivity 읽기 API를 추가합니다.
 * - 피드 공개 스냅샷과 내 응원목록을 짧게 캐시하고, 시트 헤더 검증도 캐시해 반복 읽기를 줄입니다.
 * - 쓰기 작업 뒤 관련 피드 캐시를 즉시 무효화합니다.
 *
 * V9.0.4-social-1
 * - 탈퇴한 닉네임은 30일 동안 누구도 다시 사용할 수 없도록 보호합니다.
 * - 탈퇴 시 익명 ID와 인증 토큰은 즉시 비우고 닉네임만 보호기간 판정을 위해 보관합니다.
 * - 보호기간이 지난 같은 닉네임이 다시 가입되면 이전 삭제행의 닉네임을 비웁니다.
 *
 * ★ 앱에서 부를 때 주의"""
g=one(g,needle,repl,'social changelog')

old_profile="""  const same=data.find(function(r){return str_(r.status)==='active'&&nickKey_(r.nickname)===nickKey_(nickname);});
  if(same)return {ok:false,error:'NICK_TAKEN',message:'이미 사용 중인 닉네임입니다.'};
  sh.appendRow([userId,cellText_(nickname),hash,now,now,'active']);
  return {ok:true,userId:userId,nickname:nickname,createdAt:now};"""
new_profile="""  const same=data.find(function(r){return str_(r.status)==='active'&&nickKey_(r.nickname)===nickKey_(nickname);});
  if(same)return {ok:false,error:'NICK_TAKEN',message:'이미 사용 중인 닉네임입니다.'};
  const reserved=data.find(function(r){return str_(r.status)==='deleted'&&nickKey_(r.nickname)===nickKey_(nickname)&&now-num_(r.updatedAt)<NICK_REUSE_COOLDOWN_MS;});
  if(reserved)return {ok:false,error:'NICK_COOLDOWN',message:'최근 탈퇴한 닉네임입니다. 탈퇴 후 30일이 지나면 다시 사용할 수 있습니다.',availableAt:num_(reserved.updatedAt)+NICK_REUSE_COOLDOWN_MS};
  data.filter(function(r){return str_(r.status)==='deleted'&&nickKey_(r.nickname)===nickKey_(nickname)&&now-num_(r.updatedAt)>=NICK_REUSE_COOLDOWN_MS;}).forEach(function(r){sh.getRange(r._row,2).setValue('');});
  sh.appendRow([userId,cellText_(nickname),hash,now,now,'active']);
  return {ok:true,userId:userId,nickname:nickname,createdAt:now};"""
g=one(g,old_profile,new_profile,'profile cooldown')

g=one(g,
"  sh.getRange(profile._row,1).setValue(''); sh.getRange(profile._row,2).setValue(''); sh.getRange(profile._row,3).setValue(''); sh.getRange(profile._row,5).setValue(now); sh.getRange(profile._row,6).setValue('deleted');",
"  sh.getRange(profile._row,1).setValue(''); sh.getRange(profile._row,2).setValue(cellText_(me.nickname)); sh.getRange(profile._row,3).setValue(''); sh.getRange(profile._row,5).setValue(now); sh.getRange(profile._row,6).setValue('deleted');",
'preserve nickname 30d')

p.write_text(g,encoding='utf-8')

# README
p=Path('README.md'); r=p.read_text(encoding='utf-8')
head="""## V9.0.4 — 소셜 프로필 관리 단순화 · 닉네임 30일 보호
- `내 소셜 프로필` 제목 오른쪽 `⋮`에 소셜 관리 기능을 모았습니다. 평상시 화면의 닉네임 고정 안내, 차단 사용자 카드, 큰 탈퇴 카드를 제거해 활동 목록 중심으로 단순화했습니다.
- `⋮ → 소셜 관리`에서 차단한 사용자를 확인·해제하고, 같은 화면에서 소셜 탈퇴를 시작할 수 있습니다.
- 탈퇴한 닉네임은 30일 동안 본인과 다른 사용자 모두 재사용할 수 없습니다. 30일 이후에는 다시 사용할 수 있습니다.
- 탈퇴 시 개인 회복기록은 삭제하지 않으며 `DATA_SCHEMA=6`, `ohg.v1`, `ohg.social.v1`은 유지합니다.
- Android 네이티브 알림/TTS 엔진과 하단 메뉴 구조는 변경하지 않습니다.

"""
if not r.startswith('## V9.0.4'):
    r=head+r
p.write_text(r,encoding='utf-8')

# SOCIAL_SETUP
p=Path('SOCIAL_SETUP.md'); d=p.read_text(encoding='utf-8')
notice="""# V9.0.4 소셜 프로필 관리 · 닉네임 보호

소셜 서버 `V9.0.4-social-1`은 탈퇴한 닉네임을 30일 동안 재사용하지 못하게 보호합니다. 기존 `Profiles` 시트 구조는 바꾸지 않으며, 탈퇴 행의 `nickname`과 `updatedAt`을 30일 보호 판정에 사용합니다. 익명 `userId`와 `tokenHash`는 탈퇴 즉시 비웁니다.

앱에서는 `내 소셜 프로필` 제목 오른쪽 `⋮`에서 차단 사용자 관리와 소셜 탈퇴를 엽니다. 평상시 프로필 화면에는 차단 목록과 탈퇴 카드가 표시되지 않습니다.

---

"""
if not d.startswith('# V9.0.4'):
    d=notice+d
p.write_text(d,encoding='utf-8')

# verify.js
p=Path('verify.js'); v=p.read_text(encoding='utf-8')
marker="ok(!!build && cacheVersion.startsWith(expectedCachePrefix),'sw cache = '+expectedCachePrefix+' 계열');\n"
insert="""ok(!!build && cacheVersion.startsWith(expectedCachePrefix),'sw cache = '+expectedCachePrefix+' 계열');
ok(/id=\"social-profile-manage\"/.test(index)&&/function socialProfileManageMenu\(\)/.test(index),'내 소셜 프로필 제목 오른쪽 관리 메뉴 존재');
ok(!/social-profile-fixed><b>닉네임은 가입 후 고정됩니다/.test(index),'프로필 본문 닉네임 고정 안내 제거');
ok(!/card social-profile-danger/.test(index),'프로필 본문 큰 탈퇴 카드 제거');
ok(/NICK_REUSE_COOLDOWN_MS\s*=\s*30 \* 24 \* 60 \* 60 \* 1000/.test(read('social-apps-script.gs')),'탈퇴 닉네임 30일 보호');
ok(/NICK_COOLDOWN/.test(index)&&/NICK_COOLDOWN/.test(read('social-apps-script.gs')),'앱·서버 닉네임 보호 오류 계약 일치');
"""
v=one(v,marker,insert,'verify invariants')
p.write_text(v,encoding='utf-8')

idx=Path('index.html').read_text(encoding='utf-8'); server=Path('social-apps-script.gs').read_text(encoding='utf-8'); sw=Path('sw.js').read_text(encoding='utf-8')
assert "const BUILD='V9.0.4';" in idx
assert "const APP_VERSION = 'V9.0.4';" in sw and "ohg-v904-" in sw
assert "const DATA_SCHEMA = 6;" in idx
assert "const SOCIAL_KEY = 'ohg.social.v1';" in idx
assert 'id="social-profile-manage"' in idx and 'function socialProfileManageMenu()' in idx
assert 'card social-profile-danger' not in idx
assert "V9.0.4-social-1" in server and 'NICK_REUSE_COOLDOWN_MS' in server and 'NICK_COOLDOWN' in server
print('V9.0.4 patch invariants PASS')
