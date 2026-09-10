from pathlib import Path
import re


def one(text,old,new,label):
    n=text.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1, found {n}')
    return text.replace(old,new,1)

def sub_one(text,pattern,repl,label,flags=0):
    out,n=re.subn(pattern,repl,text,count=1,flags=flags)
    if n!=1: raise SystemExit(f'{label}: expected 1, found {n}')
    return out

p=Path('index.html');s=p.read_text(encoding='utf-8')
s=one(s,"const BUILD='V9.0.2';","const BUILD='V9.0.3';",'BUILD')

old='''<section class="pg" id="p-social">
  <div class="social-top">
    <h1>소셜</h1>
    <button class="social-me hide" id="social-me" type="button"></button>
  </div>
  <div id="social-body"></div>
</section>'''
new=old+'''\n\n<section class="pg" id="p-social-profile">
  <div class="sp" style="margin-bottom:11px">
    <button class="tiny" style="color:var(--acc);font-weight:600" id="social-profile-back">← 소셜</button>
    <h1 style="margin:0">내 소셜 프로필</h1>
    <span style="width:34px"></span>
  </div>
  <div id="social-profile-body"></div>
</section>'''
s=one(s,old,new,'profile section')

s=one(s,"  if(p === 'listen' && ls.back === 'tools') tabP = 'tools';\n  $$('#tabs button').forEach(b => b.classList.toggle('on', b.dataset.t === tabP));","  if(p === 'listen' && ls.back === 'tools') tabP = 'tools';\n  if(p === 'social-profile') tabP = 'social';\n  $$('#tabs button').forEach(b => b.classList.toggle('on', b.dataset.t === tabP));",'profile tab mapping')
s=one(s,"  if(p === 'social') drawSocial();\n  if(p === 'me')   drawMe();","  if(p === 'social') drawSocial();\n  if(p === 'social-profile') drawSocialProfile();\n  if(p === 'me')   drawMe();",'profile draw')

pat=r"\n  /\* 12단계를 읽는 곳과 직접 작성하는 곳을 회복학습 안에서 나란히 둡니다\. \*/\n  const w=el\('button','help'\);.*?\n  box\.appendChild\(w\);\n  refreshIcons\(\);"
s=sub_one(s,pat,"\n  refreshIcons();",'remove learning workbook',re.S)

s=s.replace('한글·영문·숫자·공백·-·_를 사용할 수 있습니다. 관리자·운영자·오늘한걸음·마음프로와 혼동되는 이름은 사용할 수 없습니다.','한글·영문·숫자·공백·-·_를 사용할 수 있습니다. 관리자·운영자·오늘한걸음·마음프로와 혼동되는 이름은 사용할 수 없습니다. 가입 후에는 닉네임을 변경할 수 없습니다.',1)
s=s.replace("else {SO.profile.nickname=nick; SO.profile.registeredUrl='';}","else {toast('가입 후 닉네임은 변경할 수 없습니다. 다른 닉네임을 사용하려면 소셜 탈퇴 후 새 프로필을 만들어주세요.');return;}",1)

faq_pat=r'    <details class="faq"><summary>13\. 소셜 — 익명으로 오늘의 한 걸음 나누기</summary><div class="faq-a">.*?    </div></details>'
faq='''    <details class="faq"><summary>13. 소셜 — 익명으로 오늘의 한 걸음 나누기</summary><div class="faq-a">
      <p>소셜은 <b>익명 닉네임</b>으로 사용합니다. 내 회복일·충동·HALT·복약·자가점검·다시 시작 기록은 게시글이나 프로필에 자동으로 붙지 않습니다.</p>
      <p style="margin-top:8px">상단의 내 닉네임을 누르면 <b>내 소셜 프로필</b>에서 내가 작성한 게시물과 댓글을 따로 보고, 게시물은 수정·삭제하고 댓글은 삭제할 수 있습니다. 내부 인증용 ID는 화면에 표시하지 않습니다.</p>
      <p style="margin-top:8px">닉네임은 가입할 때 정하며 <b>가입 후에는 변경할 수 없습니다.</b> 다른 닉네임을 쓰려면 프로필의 탈퇴 영역에서 소셜 탈퇴 후 새 프로필을 만들어야 합니다. 탈퇴는 실수를 줄이기 위해 두 번 확인합니다.</p>
      <p style="margin-top:8px">다른 사용자의 게시물·댓글은 신고하거나 작성자를 차단할 수 있습니다. 개인메시지·친구·팔로우·답글·그룹·하이브 기능은 제공하지 않습니다. 생명이나 신체가 위급한 상황은 소셜 답변을 기다리지 말고 109·112·119 등 즉시 도움을 이용하세요.</p>
      <button class="btn ghost sm faq-go" type="button" onclick="go('social')">소셜 열기</button>
    </div></details>'''
s=sub_one(s,faq_pat,faq,'social FAQ',re.S)

css=r'''
  /* ══════════ V9.0.3 · 내 소셜 프로필 ══════════ */
  .social-profile-head{display:flex;align-items:center;gap:13px;margin-bottom:12px}
  .social-profile-head .social-avatar{width:54px;height:54px;font-size:21px;flex:none}
  .social-profile-head .name{min-width:0;flex:1}.social-profile-head .name b{display:block;font-size:19px;line-height:1.3}
  .social-profile-head .name span{display:block;margin-top:3px;font-size:12px;color:var(--dim)}
  .social-profile-tabs{display:flex;gap:7px;margin:12px 0}.social-profile-tabs button{flex:1;border:1px solid var(--line);border-radius:11px;padding:9px 6px;color:var(--dim);background:var(--panel)}
  .social-profile-tabs button.on{border-color:var(--acc);color:var(--acc);background:var(--accbg);font-weight:600}
  .social-profile-item{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:13px 14px;margin-bottom:9px}
  .social-profile-item .meta{display:flex;align-items:center;gap:7px;color:var(--faint);font-size:11px}.social-profile-item .meta .grow{flex:1}
  .social-profile-item .text{white-space:pre-wrap;word-break:break-word;line-height:1.62;margin:7px 0}
  .social-profile-item .parent{margin-top:8px;padding:9px 10px;border-radius:10px;background:var(--bg);font-size:12px;color:var(--dim);line-height:1.5}
  .social-profile-item .row-actions{display:flex;gap:7px;justify-content:flex-end;margin-top:9px}.social-profile-item .row-actions button{border:1px solid var(--line);border-radius:9px;padding:6px 10px;font-size:12px;color:var(--dim)}
  .social-profile-fixed{padding:11px 12px;border-radius:11px;background:var(--bg);margin-bottom:12px}.social-profile-fixed b{display:block;font-size:13px}.social-profile-fixed span{display:block;font-size:11.5px;color:var(--dim);margin-top:3px;line-height:1.55}
  .social-profile-danger{border-color:#e5b4b0}.social-profile-danger h3{color:var(--bad)}
'''
i=s.rfind('</style>')
if i<0:raise SystemExit('style end not found')
s=s[:i]+css+'\n'+s[i:]

js=r'''
/* ═══════════════════════════════════════════════════════
   V9.0.3 · 내 소셜 프로필 / 닉네임 고정
   ═══════════════════════════════════════════════════════ */
let socialProfileState={tab:'posts',loading:false,data:null,error:''};
const socialProfileCreateV902=socialProfileModal;
socialProfileModal=function(){if(SO.profile){go('social-profile');return;}return socialProfileCreateV902();};
const socialApiMessageV902=socialApiMessage;
socialApiMessage=function(e){const c=e&&e.socialCode||'';if(c==='NICK_LOCKED')return '가입한 닉네임은 변경할 수 없습니다. 다른 닉네임을 사용하려면 소셜 탈퇴 후 새 프로필을 만들어주세요.';if(c==='UNKNOWN_ACTION')return '소셜 서버가 현재 앱보다 이전 버전입니다. V9.0.3 소셜 서버로 업데이트해주세요.';return socialApiMessageV902(e);};
function socialProfileDate(t){if(!t)return '';try{return new Intl.DateTimeFormat('ko-KR',{year:'numeric',month:'long'}).format(new Date(Number(t)))+' 가입';}catch(_){return '';}}
function socialProfilePostById(id){const d=socialProfileState.data;return d&&Array.isArray(d.posts)?d.posts.find(x=>String(x.id)===String(id)):null;}
function socialProfileCommentById(id){const d=socialProfileState.data;return d&&Array.isArray(d.comments)?d.comments.find(x=>String(x.id)===String(id)):null;}
async function socialProfileLoad(force){
  if(!SO.profile||socialProfileState.loading)return;
  if(!force&&socialProfileState.data){drawSocialProfile();return;}
  if(!socialEndpoint()){socialProfileState.error='소셜 서버에 연결되지 않았습니다.';drawSocialProfile();return;}
  socialProfileState.loading=true;socialProfileState.error='';drawSocialProfile();
  try{await socialRegister();const r=await socialWrite('profileActivity',socialAuth());socialProfileState.data=r;socialProfileState.error='';}
  catch(e){socialProfileState.error=socialApiMessage(e);}finally{socialProfileState.loading=false;drawSocialProfile();}
}
function socialProfilePostHtml(x){return '<article class="social-profile-item"><div class="meta"><span>'+esc(socialTime(x.createdAt))+'</span>'+(Number(x.updatedAt)>Number(x.createdAt)+1000?'<span>· 수정됨</span>':'')+'<span class="grow"></span><span>응원 '+Number(x.supportCount||0)+' · 댓글 '+Number(x.commentCount||0)+'</span></div><div class="text">'+esc(x.text||'')+'</div><div class="row-actions"><button type="button" data-social-profile-edit="'+esc(x.id)+'">수정</button><button type="button" data-social-profile-post-delete="'+esc(x.id)+'" style="color:var(--bad)">삭제</button></div></article>';}
function socialProfileCommentHtml(x){const parent=x.postText?'<div class="parent">'+(x.postNickname?'<b>'+esc(x.postNickname)+'님의 게시물</b><br>':'')+esc(x.postText)+'</div>':'';return '<article class="social-profile-item"><div class="meta"><span>'+esc(socialTime(x.createdAt))+'</span><span class="grow"></span></div><div class="text">'+esc(x.text||'')+'</div>'+parent+'<div class="row-actions"><button type="button" data-social-profile-comment-delete="'+esc(x.id)+'" style="color:var(--bad)">댓글 삭제</button></div></article>';}
function drawSocialProfile(){
  const body=$('#social-profile-body'),back=$('#social-profile-back');if(!body)return;if(back)back.onclick=()=>appBack('social');const p=SO.profile;
  if(!p){body.innerHTML='<div class="empty">소셜 프로필이 없습니다.</div>';setTimeout(()=>go('social',{replace:true}),0);return;}
  const d=socialProfileState.data||{},st=d.stats||{postCount:0,commentCount:0,supportReceived:0},prof=d.profile||{};
  let html='<div class="card"><div class="social-profile-head"><span class="social-avatar">'+socialInitial(p.nickname)+'</span><span class="name"><b>'+esc(p.nickname)+'</b><span>'+esc(socialProfileDate(prof.createdAt))+'</span></span></div><div class="social-profile-stats"><div><b>'+Number(st.supportReceived||0)+'</b><span>받은 응원</span></div><div><b>'+Number(st.postCount||0)+'</b><span>게시물</span></div><div><b>'+Number(st.commentCount||0)+'</b><span>댓글</span></div></div><div class="social-profile-fixed"><b>닉네임은 가입 후 고정됩니다</b><span>잦은 이름 변경으로 다른 사람과 혼동되는 일을 줄이기 위한 기준입니다. 다른 닉네임을 사용하려면 소셜 탈퇴 후 새 프로필을 만들어주세요.</span></div></div>';
  if(socialProfileState.loading)html+='<div class="empty">내 활동을 불러오는 중입니다.</div>';else if(socialProfileState.error)html+='<div class="social-error">'+esc(socialProfileState.error)+'</div><button class="btn ghost sm" id="social-profile-retry">다시 불러오기</button>';else if(d&&d.ok){html+='<div class="social-profile-tabs"><button type="button" data-social-profile-tab="posts" class="'+(socialProfileState.tab==='posts'?'on':'')+'">게시물 '+Number(st.postCount||0)+'</button><button type="button" data-social-profile-tab="comments" class="'+(socialProfileState.tab==='comments'?'on':'')+'">댓글 '+Number(st.commentCount||0)+'</button></div>';const rows=socialProfileState.tab==='comments'?(d.comments||[]):(d.posts||[]);html+=rows.length?rows.map(socialProfileState.tab==='comments'?socialProfileCommentHtml:socialProfilePostHtml).join(''):'<div class="empty">'+(socialProfileState.tab==='comments'?'아직 작성한 댓글이 없습니다.':'아직 작성한 게시물이 없습니다.')+'</div>';}
  const blocked=SO.blocks||[];html+='<div class="card" style="margin-top:16px"><h3>차단한 사용자</h3>'+(blocked.length?blocked.map((b,i)=>'<div class="social-block-row"><span>'+esc(b.nickname||'익명')+'</span><button class="btn ghost sm" style="width:auto" data-social-profile-unblock="'+i+'">차단 해제</button></div>').join(''):'<p class="tiny">차단한 사용자가 없습니다.</p>')+'</div><div class="card social-profile-danger"><h3>탈퇴</h3><p class="muted">소셜 탈퇴는 닉네임 변경과 구분되는 별도 절차입니다. 탈퇴하면 내 공개 게시물·댓글·응원 관계와 익명 프로필을 삭제하며 되돌릴 수 없습니다.</p><button class="btn ghost" id="social-profile-leave" style="color:var(--bad);border-color:var(--bad)">소셜 탈퇴</button></div>';body.innerHTML=html;
  const retry=$('#social-profile-retry');if(retry)retry.onclick=()=>socialProfileLoad(true);$$('[data-social-profile-tab]').forEach(b=>b.onclick=()=>{socialProfileState.tab=b.dataset.socialProfileTab;drawSocialProfile();});$$('[data-social-profile-edit]').forEach(b=>b.onclick=()=>{const x=socialProfilePostById(b.dataset.socialProfileEdit);if(x)socialCompose(x);});$$('[data-social-profile-post-delete]').forEach(b=>b.onclick=()=>{const x=socialProfilePostById(b.dataset.socialProfilePostDelete);if(x)socialProfileDeletePost(x);});$$('[data-social-profile-comment-delete]').forEach(b=>b.onclick=()=>{const x=socialProfileCommentById(b.dataset.socialProfileCommentDelete);if(x)socialProfileDeleteComment(x);});$$('[data-social-profile-unblock]').forEach(b=>b.onclick=()=>{const i=Number(b.dataset.socialProfileUnblock);if(i>=0&&i<SO.blocks.length){SO.blocks.splice(i,1);socialSave();drawSocialProfile();if(socialState.loaded)drawSocial();}});const leave=$('#social-profile-leave');if(leave)leave.onclick=socialProfileDeleteConfirm;if(!socialProfileState.data&&!socialProfileState.loading&&!socialProfileState.error)setTimeout(()=>socialProfileLoad(false),0);
}
function socialProfileDeletePost(x){modal('<h2>이 게시물을 삭제할까요?</h2><p class="muted">삭제하면 공개 글 내용과 해당 글의 댓글이 서버에서 삭제 처리되며 되돌릴 수 없습니다.</p><button class="btn danger" id="social-profile-post-delete-yes">삭제</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">그만두기</button>');$('#social-profile-post-delete-yes').onclick=async()=>{try{await socialWrite('postDelete',Object.assign({},socialAuth(),{postId:x.id}));closeModal();socialResetFeed();socialProfileState.data=null;toast('게시물을 삭제했습니다.');socialProfileLoad(true);}catch(e){toast(socialApiMessage(e));}};}
function socialProfileDeleteComment(x){modal('<h2>이 댓글을 삭제할까요?</h2><p class="muted">삭제한 댓글은 되돌릴 수 없습니다.</p><button class="btn danger" id="social-profile-comment-delete-yes">댓글 삭제</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">그만두기</button>');$('#social-profile-comment-delete-yes').onclick=async()=>{try{await socialWrite('commentDelete',Object.assign({},socialAuth(),{commentId:x.id}));closeModal();socialResetFeed();socialProfileState.data=null;toast('댓글을 삭제했습니다.');socialProfileLoad(true);}catch(e){toast(socialCommentApiMessage(e));}};}
const socialSubmitPostV902=socialSubmitPost;
socialSubmitPost=async function(text,post,confirmed){const fromProfile=cur==='social-profile',actual=!socialCrisisText(text)||confirmed;await socialSubmitPostV902(text,post,confirmed);if(fromProfile&&post&&actual){socialProfileState.data=null;setTimeout(()=>socialProfileLoad(true),180);}};
socialProfileDeleteConfirm=function(){const p=SO.profile;if(!p)return;modal('<h2>소셜 탈퇴</h2><p class="muted">탈퇴하면 익명 프로필과 내가 작성한 공개 게시물·댓글·응원 관계가 삭제됩니다. 차단·숨김 목록도 이 기기에서 지워집니다.<br><br><b>닉네임만 바꾸는 기능은 제공하지 않습니다.</b> 다른 닉네임을 쓰려는 경우에도 현재 프로필을 탈퇴한 뒤 새로 만들어야 합니다.</p><button class="btn danger" id="social-leave-next">탈퇴 계속</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">취소</button>');$('#social-leave-next').onclick=()=>{modal('<h2>정말 탈퇴할까요?</h2><p class="muted">실수로 탈퇴하지 않도록 아래에 <b>탈퇴</b>라고 입력해주세요.</p><input id="social-leave-word" autocomplete="off" placeholder="탈퇴"><button class="btn danger" id="social-leave-confirm" disabled style="margin-top:10px">소셜 탈퇴</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">취소</button>');const input=$('#social-leave-word'),yes=$('#social-leave-confirm');input.oninput=()=>{yes.disabled=String(input.value||'').trim()!=='탈퇴';};yes.onclick=async()=>{if(String(input.value||'').trim()!=='탈퇴')return;try{if(p.registeredUrl){if(!socialEndpoint()){toast('소셜 서버에 연결된 뒤 다시 탈퇴해주세요.');return;}await socialWrite('profileDelete',socialAuth());}SO=socialBlank();socialSave();socialResetFeed();socialProfileState={tab:'posts',loading:false,data:null,error:''};closeModal();go('social',{replace:true});toast('소셜에서 탈퇴했습니다.');}catch(e){toast(socialApiMessage(e));}};};};
'''
i=s.rfind('</script>')
if i<0:raise SystemExit('script end not found')
s=s[:i]+js+'\n'+s[i:]
p.write_text(s,encoding='utf-8')

p=Path('sw.js');w=p.read_text(encoding='utf-8')
w=one(w,"const APP_VERSION = 'V9.0.2';","const APP_VERSION = 'V9.0.3';",'APP_VERSION')
w=sub_one(w,r"const V = 'ohg-v902-[^']+';","const V = 'ohg-v903-social-profile-r1';",'cache')
p.write_text(w,encoding='utf-8')

p=Path('test.js');t=p.read_text(encoding='utf-8')
t=one(t,"if (!fs.existsSync(f)) { res.writeHead(404); res.end('no'); return; }","if (!fs.existsSync(f)) { console.error('TEST HTTP404:', p); res.writeHead(404); res.end('no'); return; }",'test 404 trace')
t=one(t,"assert((await pg.$$eval('#learn-list .help', a => a.length)) === 4, '회복학습 목록에는 12단계·회복의 기초 이해·SMART Recovery·12단계 점검 4개가 있어야 함');","assert((await pg.$$eval('#learn-list .help', a => a.length)) === 3, '회복학습 목록에는 12단계·회복의 기초 이해·SMART Recovery 3개가 있어야 함');",'test count')
t=one(t,"  assert(learnText.includes('12단계 점검'), '회복학습 목록에 12단계 점검이 표시되어야 함');\n","  assert(!learnText.includes('12단계 점검'), '회복학습 목록에는 작성형 12단계 점검이 중복 표시되지 않아야 함');\n",'test duplicate')
p.write_text(t,encoding='utf-8')

p=Path('verify.js');v=p.read_text(encoding='utf-8')
v=v.replace("'회복학습 안에 단계별 점검 화면 존재'","'12단계 점검 작성 화면 존재'",1)
line="ok(/<b>12단계 점검<\\/b>/.test(index)&&/w\\.onclick=\\(\\)=>go\\('workbook-list'\\)/.test(index),'회복학습 목록에서 12단계 점검 직접 진입');\n"
if line not in v:raise SystemExit('old learning verifier missing')
v=v.replace(line,'',1)
v=one(v,"ok(/회복학습 목록에는 12단계·회복의 기초 이해·SMART Recovery·12단계 점검 4개/.test(test),'test.js 회복학습 4메뉴 기준으로 갱신');","ok(/회복학습 목록에는 12단계·회복의 기초 이해·SMART Recovery 3개/.test(test)&&/작성형 12단계 점검이 중복 표시되지 않아야 함/.test(test),'test.js 회복학습 3개 학습주제·12단계 점검 실천하기 일원화');",'verify test')
p.write_text(v,encoding='utf-8')

p=Path('README.md');r=p.read_text(encoding='utf-8')
head='''## V9.0.3 — 내 소셜 프로필 · 피드 속도 · 12단계 점검 일원화
- 상단 소셜 닉네임을 누르면 별도 **내 소셜 프로필** 페이지에서 내가 작성한 게시물·댓글과 받은 응원 요약을 확인합니다. 내 게시물은 수정·삭제, 내 댓글은 삭제할 수 있습니다.
- 내부 소셜 ID는 UI에서 숨기고, 닉네임은 가입 후 고정합니다. 다른 닉네임은 소셜 탈퇴 후 새 프로필을 만드는 방식으로만 사용합니다.
- 소셜 탈퇴를 프로필의 별도 영역으로 분리하고 `탈퇴` 입력까지 두 번 확인합니다.
- 소셜 서버 `V9.0.3-social-1`은 내 활동 조회와 짧은 피드/응원/시트검증 캐시를 추가합니다.
- `회복도구 → 회복학습`의 중복 **12단계 점검** 카드를 제거하고 작성은 `회복도구 → 실천하기 → 12단계 점검`으로 일원화했습니다.
- `DATA_SCHEMA=6`, `ohg.v1`, `ohg.social.v1` 및 Android 네이티브 알림/TTS 엔진은 변경하지 않습니다.

'''
if not r.startswith('## V9.0.3'):r=head+r
p.write_text(r,encoding='utf-8')

p=Path('SOCIAL_SETUP.md');d=p.read_text(encoding='utf-8')
head='''# V9.0.3 소셜 서버 배포 메모

`social-apps-script.gs` 서버판은 **V9.0.3-social-1**입니다. 시트 구조는 그대로 유지하므로 `SOCIAL_SETUP()`을 한 번 실행해 헤더를 확인한 뒤 기존 웹 앱 배포를 새 버전으로 갱신합니다. `/exec` 주소는 바꾸지 않습니다.

V9.0.3은 닉네임 변경을 서버에서도 거부하고 `profileActivity`를 추가합니다. 피드 공개 목록·내 응원목록·시트 헤더 검증은 짧게 캐시하며 쓰기 직후 관련 캐시를 무효화합니다.

---

'''
if not d.startswith('# V9.0.3'):d=head+d
p.write_text(d,encoding='utf-8')

idx=Path('index.html').read_text(encoding='utf-8')
assert "const BUILD='V9.0.3';" in idx
assert 'const DATA_SCHEMA = 6;' in idx
assert "const SOCIAL_KEY = 'ohg.social.v1';" in idx
assert 'id="p-social-profile"' in idx
assert "if(p === 'social-profile') tabP = 'social';" in idx
assert "if(p === 'social-profile') drawSocialProfile();" in idx
assert "w.onclick=()=>go('workbook-list');" not in idx
assert "const APP_VERSION = 'V9.0.3';" in Path('sw.js').read_text(encoding='utf-8')
print('app V9.0.3 patch PASS')
