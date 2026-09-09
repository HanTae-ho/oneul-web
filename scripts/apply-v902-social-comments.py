from pathlib import Path
import re


def one(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    return text.replace(old, new, 1)


def sub_one(text, pattern, repl, label, flags=0):
    out, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    return out

# ── index.html ──────────────────────────────────────────────
p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = one(s, "const BUILD='V9.0.1';", "const BUILD='V9.0.2';", 'BUILD')
s = one(
    s,
    "<p style=\"margin-top:8px\">V9.0에서는 댓글·개인메시지·친구·팔로우·그룹 기능을 제공하지 않습니다. 생명이나 신체가 위급한 상황은 소셜 답변을 기다리지 말고 109·112·119 등 즉시 도움을 이용하세요.</p>",
    "<p style=\"margin-top:8px\">V9.0.2에서는 게시물에 댓글을 남기고, 내 댓글을 삭제하며, 다른 사용자의 댓글을 신고하거나 작성자를 차단할 수 있습니다. 신고된 게시물·댓글은 운영 검토용 소셜 시트에서 확인합니다. 개인메시지·친구·팔로우·답글·그룹·하이브 기능은 제공하지 않습니다. 생명이나 신체가 위급한 상황은 소셜 답변을 기다리지 말고 109·112·119 등 즉시 도움을 이용하세요.</p>",
    'social FAQ'
)
s = one(
    s,
    "   - 댓글/DM/친구/그룹/접속자수는 아직 만들지 않습니다.\n",
    "   - V9.0.2: 댓글 작성·내 댓글 삭제·댓글 신고·작성자 차단·운영 검토를 추가합니다.\n   - DM/친구/팔로우/답글/그룹/하이브/접속자수는 만들지 않습니다.\n",
    'social code comment'
)

css = r'''
  /* ══════════ V9.0.2 · 소셜 댓글/프로필 요약 ══════════ */
  .social-profile-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin:0 0 13px}
  .social-profile-stats>div{border:1px solid var(--line);border-radius:12px;padding:9px 6px;text-align:center;background:var(--bg)}
  .social-profile-stats b{display:block;font-size:17px;color:var(--tx);line-height:1.2}.social-profile-stats span{display:block;margin-top:4px;font-size:10.5px;color:var(--dim)}
  .social-comments-head{margin-bottom:10px}.social-comments-post{padding:11px 12px;border:1px solid var(--line);border-radius:12px;background:var(--bg);margin-bottom:11px}
  .social-comments-post b{font-size:12.5px}.social-comments-post p{margin:4px 0 0;white-space:pre-wrap;word-break:break-word;font-size:13.5px;line-height:1.55;color:var(--tx)}
  .social-comment{display:flex;gap:9px;padding:11px 0;border-bottom:1px solid var(--line)}.social-comment:last-child{border-bottom:0}
  .social-comment-main{flex:1;min-width:0}.social-comment-head{display:flex;align-items:center;gap:7px}.social-comment-head b{font-size:12.5px;max-width:65%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.social-comment-head span{font-size:10.5px;color:var(--faint)}
  .social-comment-text{margin-top:4px;white-space:pre-wrap;word-break:break-word;font-size:13.5px;line-height:1.58}.social-comment-more{margin-left:auto;width:28px;height:28px;border-radius:50%;color:var(--dim)}
  .social-comment-compose{margin-top:12px;padding-top:12px;border-top:1px solid var(--line)}.social-comment-compose textarea{min-height:66px}.social-comment-compose .btn{margin-top:8px}
'''
idx = s.rfind('</style>')
if idx < 0: raise SystemExit('style end not found')
s = s[:idx] + css + '\n' + s[idx:]

js = r'''

/* ═══════════════════════════════════════════════════════
   V9.0.2 · 소셜 2단계 — 댓글 / 신고 / 작성자 차단 / 운영 검토
   - 회복기록 ohg.v1 / DATA_SCHEMA=6 은 읽거나 전송하지 않습니다.
   - 댓글도 기존 소셜 프로필의 userId/token만 사용합니다.
   - DM·친구·팔로우·답글·그룹·하이브는 추가하지 않습니다.
   ═══════════════════════════════════════════════════════ */
socialState.stats = socialState.stats || {postCount:0,commentCount:0,supportReceived:0};
let socialCommentState={postId:'',items:[],loading:false,error:''};

const socialSvgV901=socialSvg;
socialSvg=function(k){
  if(k==='comment') return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5h16v10.2H10l-4.8 3.1v-3.1H4z"/></svg>';
  return socialSvgV901(k);
};

async function socialReadFeed(){
  const j=await socialWrite('feed',Object.assign({sort:socialState.sort},socialAuth()));
  socialState.stats=(j&&j.stats)||{postCount:0,commentCount:0,supportReceived:0};
  return Array.isArray(j.items)?j.items:[];
}

function socialPostHtml(x){
  const mine=!!x.mine||!!(SO.profile&&String(x.userId)===String(SO.profile.userId));
  const supportDisabled=mine?' disabled':'';
  return '<article class="social-post"><div class="social-post-head"><span class="social-avatar">'+socialInitial(x.nickname)+'</span><span class="who"><b>'+esc(x.nickname||'익명')+'</b><span>'+esc(socialTime(x.createdAt))+(Number(x.updatedAt)>Number(x.createdAt)+1000?' · 수정됨':'')+'</span></span><button class="social-more" type="button" data-social-menu="'+esc(x.id)+'" aria-label="게시물 메뉴">'+socialSvg('more')+'</button></div><div class="social-text">'+esc(x.text||'')+'</div><div class="social-actions"><button class="social-act'+(x.supported?' on':'')+'" type="button" data-social-support="'+esc(x.id)+'"'+supportDisabled+'>'+socialSvg('cheer')+'<span>'+(x.supported?'응원했어요':'응원')+' '+Number(x.supportCount||0)+'</span></button><button class="social-act" type="button" data-social-comments="'+esc(x.id)+'">'+socialSvg('comment')+'<span>댓글 '+Number(x.commentCount||0)+'</span></button>'+(mine?'<span class="tiny" style="margin-left:auto">내 글</span>':'')+'</div></article>';
}

const socialProfileModalV901=socialProfileModal;
socialProfileModal=function(){
  socialProfileModalV901();
  const p=SO.profile, input=$('#social-nick');
  if(!p||!input) return;
  const st=socialState.stats||{};
  input.insertAdjacentHTML('beforebegin','<div class="social-profile-stats"><div><b>'+Number(st.supportReceived||0)+'</b><span>받은 응원</span></div><div><b>'+Number(st.postCount||0)+'</b><span>게시물</span></div><div><b>'+Number(st.commentCount||0)+'</b><span>댓글</span></div></div>');
};

function socialCommentApiMessage(e){
  const c=e&&e.socialCode||'';
  if(c==='INVALID_COMMENT') return '댓글은 1~300자로 작성해주세요.';
  if(c==='COMMENT_TOO_FAST') return '댓글은 잠시 후 다시 남겨주세요.';
  if(c==='COMMENT_DAILY_LIMIT') return '오늘 남길 수 있는 댓글 수를 넘었습니다.';
  if(c==='OWNER') return '내가 작성한 댓글만 삭제할 수 있습니다.';
  return socialApiMessage(e);
}
function socialCommentVisible(){
  const blocked=new Set((SO.blocks||[]).map(x=>String(x&&x.userId||x)));
  const hidden=new Set((SO.hidden||[]).map(String));
  return (socialCommentState.items||[]).filter(x=>x&&!blocked.has(String(x.userId||''))&&!hidden.has(String(x.id||'')));
}
function socialCommentHtml(c){
  const mine=!!c.mine||!!(SO.profile&&String(c.userId)===String(SO.profile.userId));
  return '<div class="social-comment"><span class="social-avatar" style="width:30px;height:30px;font-size:12px">'+socialInitial(c.nickname)+'</span><div class="social-comment-main"><div class="social-comment-head"><b>'+esc(c.nickname||'익명')+'</b><span>'+esc(socialTime(c.createdAt))+'</span>'+(mine?'<span>· 내 댓글</span>':'')+'<button class="social-comment-more" type="button" data-social-comment-menu="'+esc(c.id)+'" aria-label="댓글 메뉴">'+socialSvg('more')+'</button></div><div class="social-comment-text">'+esc(c.text||'')+'</div></div></div>';
}
function socialCommentFind(id){return (socialCommentState.items||[]).find(x=>String(x.id)===String(id));}

async function socialComments(postId){
  const x=socialFind(postId); if(!x)return;
  socialCommentState={postId:String(postId),items:[],loading:true,error:''};
  modal('<h2>댓글</h2><div class="social-comments-post"><b>'+esc(x.nickname||'익명')+'</b><p>'+esc(x.text||'')+'</p></div><div id="social-comment-list"><div class="empty">댓글을 불러오는 중입니다.</div></div><div class="social-comment-compose"><textarea id="social-comment-text" maxlength="300" rows="3" placeholder="회복을 돕는 말을 남겨보세요."></textarea><div class="social-char" id="social-comment-char">0 / 300</div><button class="btn" id="social-comment-send">댓글 남기기</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">닫기</button></div>');
  const ta=$('#social-comment-text'), ch=$('#social-comment-char'); if(ta)ta.oninput=()=>ch.textContent=ta.value.length+' / 300';
  const send=$('#social-comment-send'); if(send)send.onclick=()=>socialCommentSubmit(postId,String(ta&&ta.value||'').trim(),false);
  await socialCommentsRefresh(postId);
}
async function socialCommentsRefresh(postId){
  try{
    const r=await socialWrite('commentList',Object.assign({},socialAuth(),{postId:postId}));
    socialCommentState.items=Array.isArray(r.items)?r.items:[]; socialCommentState.loading=false; socialCommentState.error='';
    const x=socialFind(postId); if(x)x.commentCount=Number(r.commentCount||socialCommentState.items.length);
    socialRenderComments(); drawSocial();
  }catch(e){socialCommentState.loading=false;socialCommentState.error=socialCommentApiMessage(e);socialRenderComments();}
}
function socialRenderComments(){
  const box=$('#social-comment-list'); if(!box)return;
  if(socialCommentState.error){box.innerHTML='<div class="social-error">'+esc(socialCommentState.error)+'</div>';return;}
  const rows=socialCommentVisible();
  box.innerHTML=rows.length?rows.map(socialCommentHtml).join(''):'<div class="empty">아직 댓글이 없습니다.<br>첫 댓글을 남겨보세요.</div>';
}
async function socialCommentSubmit(postId,text,confirmed){
  if(!text||text.length>300){toast('댓글은 1~300자로 작성해주세요.');return;}
  if(socialCrisisText(text)&&!confirmed){
    modal('<h2>지금 안전이 먼저입니다</h2><div class="note b">댓글에 죽고 싶은 마음과 관련된 표현이 있습니다. 지금 당장 위험하다면 댓글의 답을 기다리지 말고 <b>109</b>, <b>112</b>, <b>119</b> 또는 가까운 응급의료기관에 바로 연결하세요.</div><a class="btn danger" href="tel:109">109 자살예방상담전화</a><button class="btn sec" id="social-comment-crisis-help" style="margin-top:8px">지금 위험해요 열기</button><button class="btn ghost" id="social-comment-crisis-send" style="margin-top:8px">그래도 댓글 남기기</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">그만두기</button>');
    $('#social-comment-crisis-help').onclick=()=>{closeModal();go('panic');};
    $('#social-comment-crisis-send').onclick=()=>socialCommentSubmit(postId,text,true); return;
  }
  try{
    const r=await socialWrite('commentCreate',Object.assign({},socialAuth(),{postId:postId,text:text}));
    const x=socialFind(postId); if(x)x.commentCount=Number(r.commentCount||Number(x.commentCount||0)+1);
    toast('댓글을 남겼습니다.'); await socialComments(postId);
  }catch(e){toast(socialCommentApiMessage(e));}
}
function socialCommentMenu(id){
  const c=socialCommentFind(id); if(!c)return;
  const mine=!!c.mine||!!(SO.profile&&String(c.userId)===String(SO.profile.userId));
  if(mine){
    modal('<h2>내 댓글</h2><button class="btn ghost" id="social-comment-delete" style="color:var(--bad);border-color:var(--bad)">댓글 삭제</button><button class="btn ghost" onclick="socialComments(\''+esc(socialCommentState.postId)+'\')" style="margin-top:8px">돌아가기</button>');
    $('#social-comment-delete').onclick=()=>socialCommentDelete(c); return;
  }
  modal('<h2>'+esc(c.nickname||'익명')+'님의 댓글</h2><button class="btn sec" id="social-comment-report">댓글 신고</button><button class="btn ghost" id="social-comment-block" style="margin-top:8px">이 작성자 차단</button><button class="btn ghost" onclick="socialComments(\''+esc(socialCommentState.postId)+'\')" style="margin-top:8px">돌아가기</button>');
  $('#social-comment-report').onclick=()=>socialCommentReport(c); $('#social-comment-block').onclick=()=>socialCommentBlock(c);
}
async function socialCommentDelete(c){
  const postId=socialCommentState.postId;
  try{const r=await socialWrite('commentDelete',Object.assign({},socialAuth(),{commentId:c.id}));const x=socialFind(postId);if(x)x.commentCount=Number(r.commentCount||Math.max(0,Number(x.commentCount||1)-1));toast('댓글을 삭제했습니다.');await socialComments(postId);}catch(e){toast(socialCommentApiMessage(e));}
}
function socialCommentReport(c){
  const postId=socialCommentState.postId;
  modal('<h2>댓글을 신고하는 이유</h2><p class="muted" style="margin:5px 0 12px">신고 내용은 운영 검토용으로 소셜 서버에 저장됩니다. 신고 후 이 댓글은 이 기기에서 바로 숨깁니다.</p><div class="opts">'+SOCIAL_REPORT_REASONS.map((r,i)=>'<button class="opt" data-social-comment-report-reason="'+i+'">'+esc(r)+'</button>').join('')+'</div><div style="height:10px"></div><button class="btn ghost" onclick="socialComments(\''+esc(postId)+'\')">그만두기</button>');
  $$('[data-social-comment-report-reason]').forEach(b=>b.onclick=async()=>{const reason=SOCIAL_REPORT_REASONS[Number(b.dataset.socialCommentReportReason)];try{await socialWrite('commentReport',Object.assign({},socialAuth(),{commentId:c.id,reason:reason}));if(!SO.hidden.includes(c.id))SO.hidden.push(c.id);socialSave();toast('댓글을 신고하고 숨겼습니다.');await socialComments(postId);}catch(e){toast(socialCommentApiMessage(e));}});
}
function socialCommentBlock(c){
  const postId=socialCommentState.postId;
  modal('<h2>이 작성자를 차단할까요?</h2><p class="muted">'+esc(c.nickname||'익명')+'님의 게시물과 댓글을 이 기기에서 보이지 않게 합니다. 내 소셜 프로필에서 차단을 해제할 수 있습니다.</p><button class="btn" id="social-comment-block-yes">차단</button><button class="btn ghost" onclick="socialComments(\''+esc(postId)+'\')" style="margin-top:8px">그만두기</button>');
  $('#social-comment-block-yes').onclick=async()=>{if(!(SO.blocks||[]).some(b=>String(b.userId)===String(c.userId)))SO.blocks.push({userId:c.userId,nickname:c.nickname||'익명',t:Date.now()});socialSave();drawSocial();toast('이 작성자의 게시물과 댓글을 숨겼습니다.');await socialComments(postId);};
}

document.addEventListener('click',function(e){
  const cb=e.target&&e.target.closest&&e.target.closest('[data-social-comments]');
  if(cb){e.preventDefault();socialComments(cb.dataset.socialComments);return;}
  const cm=e.target&&e.target.closest&&e.target.closest('[data-social-comment-menu]');
  if(cm){e.preventDefault();socialCommentMenu(cm.dataset.socialCommentMenu);}
});
'''
idx = s.rfind('</script>')
if idx < 0: raise SystemExit('script end not found')
s = s[:idx] + js + '\n' + s[idx:]
p.write_text(s, encoding='utf-8')

# ── service worker ─────────────────────────────────────────
p = Path('sw.js'); s = p.read_text(encoding='utf-8')
s = one(s, "const APP_VERSION = 'V9.0.1';", "const APP_VERSION = 'V9.0.2';", 'SW version')
s = one(s, "const V = 'ohg-v901-ai-role-meeting-social';", "const V = 'ohg-v902-social-comments';", 'SW cache')
p.write_text(s, encoding='utf-8')

# ── social Apps Script ─────────────────────────────────────
p = Path('social-apps-script.gs'); g = p.read_text(encoding='utf-8')
g = g.replace('오늘 한 걸음 V9.0 — 소셜 전용 Apps Script', '오늘 한 걸음 V9.0.2 — 소셜 전용 Apps Script', 1)
g = g.replace('익명 ID·닉네임·게시글·응원·신고만 저장합니다.', '익명 ID·닉네임·게시글·댓글·응원·신고만 저장합니다.', 1)
g = one(g, "const SOCIAL_VERSION = 'V9.0.1-social-1';", "const SOCIAL_VERSION = 'V9.0.2-social-1';", 'social server version')
g = one(g,
"const SOCIAL_SHEETS = {\n  profiles: 'Profiles',\n  posts: 'Posts',\n  supports: 'Supports',\n  reports: 'Reports'\n};",
"const SOCIAL_SHEETS = {\n  profiles: 'Profiles',\n  posts: 'Posts',\n  comments: 'Comments',\n  supports: 'Supports',\n  reports: 'Reports',\n  commentReports: 'CommentReports'\n};", 'SOCIAL_SHEETS')
g = one(g,
"const SOCIAL_HEADERS = {\n  Profiles: ['userId','nickname','tokenHash','createdAt','updatedAt','status'],\n  Posts: ['postId','userId','nickname','text','createdAt','updatedAt','status','supportCount'],\n  Supports: ['postId','userId','createdAt'],\n  Reports: ['reportId','postId','reporterId','reportedUserId','reason','createdAt']\n};",
"const SOCIAL_HEADERS = {\n  Profiles: ['userId','nickname','tokenHash','createdAt','updatedAt','status'],\n  Posts: ['postId','userId','nickname','text','createdAt','updatedAt','status','supportCount'],\n  Comments: ['commentId','postId','userId','nickname','text','createdAt','updatedAt','status'],\n  Supports: ['postId','userId','createdAt'],\n  Reports: ['reportId','postId','reporterId','reportedUserId','reason','createdAt'],\n  CommentReports: ['reportId','commentId','postId','reporterId','reportedUserId','reason','createdAt','status','reviewedAt','reviewNote']\n};", 'SOCIAL_HEADERS')

g = sub_one(g, r"function SOCIAL_CHECK\(\)\{.*?\n\}", """function SOCIAL_CHECK(){
  SOCIAL_SETUP();
  const ss=SpreadsheetApp.getActiveSpreadsheet();
  return JSON.stringify({ok:true,version:SOCIAL_VERSION,spreadsheet:ss.getName(),timeZone:ss.getSpreadsheetTimeZone(),sheets:Object.keys(SOCIAL_HEADERS)});
}

function SOCIAL_REVIEW_CHECK(){
  SOCIAL_SETUP();
  const postReports=rows_(SOCIAL_SHEETS.reports);
  const commentReports=rows_(SOCIAL_SHEETS.commentReports);
  const pendingComments=commentReports.filter(r=>!str_(r.status)||str_(r.status)==='pending');
  return JSON.stringify({ok:true,version:SOCIAL_VERSION,postReports:postReports.length,commentReports:commentReports.length,pendingCommentReports:pendingComments.length,lastPostReports:postReports.slice(-20).reverse(),lastCommentReports:pendingComments.slice(-20).reverse()});
}""", 'SOCIAL_CHECK', flags=re.S)

g = one(g,
"      if(action === 'postDelete') return json_(postDelete_(body));\n      if(action === 'supportToggle') return json_(supportToggle_(body));",
"      if(action === 'postDelete') return json_(postDelete_(body));\n      if(action === 'commentList') return json_(commentList_(body));\n      if(action === 'commentCreate') return json_(commentCreate_(body));\n      if(action === 'commentDelete') return json_(commentDelete_(body));\n      if(action === 'commentReport') return json_(commentReport_(body));\n      if(action === 'supportToggle') return json_(supportToggle_(body));", 'comment routes')

feed = r'''function feed_(p){
  SOCIAL_SETUP();
  const me = auth_(p.userId,p.token); if(!me.ok) return me;
  const requester = me.userId;
  const sort = str_(p.sort) === 'support' ? 'support' : 'latest';
  const posts = rows_(SOCIAL_SHEETS.posts).filter(r => str_(r.status) === 'active');
  const comments = rows_(SOCIAL_SHEETS.comments).filter(r => str_(r.status) === 'active');
  const supports = rows_(SOCIAL_SHEETS.supports);
  const supported = new Set(supports.filter(r => str_(r.userId) === requester).map(r => str_(r.postId)));
  const commentCounts={};
  comments.forEach(r=>{const id=str_(r.postId);commentCounts[id]=(commentCounts[id]||0)+1;});
  posts.sort((a,b) => sort === 'support'
    ? (num_(b.supportCount)-num_(a.supportCount) || num_(b.createdAt)-num_(a.createdAt))
    : num_(b.createdAt)-num_(a.createdAt));
  const items = posts.slice(0,60).map(r => ({
    id:str_(r.postId), userId:str_(r.userId), nickname:str_(r.nickname), text:str_(r.text),
    createdAt:num_(r.createdAt), updatedAt:num_(r.updatedAt), supportCount:num_(r.supportCount),
    commentCount:num_(commentCounts[str_(r.postId)]||0),
    mine:requester && str_(r.userId) === requester,
    supported:supported.has(str_(r.postId))
  }));
  const myPosts=posts.filter(r=>str_(r.userId)===requester);
  const myPostIds=new Set(myPosts.map(r=>str_(r.postId)));
  const stats={
    postCount:myPosts.length,
    commentCount:comments.filter(r=>str_(r.userId)===requester).length,
    supportReceived:supports.filter(r=>myPostIds.has(str_(r.postId))).length
  };
  return {ok:true,version:SOCIAL_VERSION,items:items,stats:stats};
}'''
g = sub_one(g, r"function feed_\(p\)\{.*?\n\}\n\nfunction profile_", feed + "\n\nfunction profile_", 'feed_', flags=re.S)

# nickname changes propagate to comments too
g = one(g,
"    ps.forEach(r => psh.getRange(r._row,3).setValue(nickname));\n    return {ok:true,userId:userId,nickname:nickname};",
"    ps.forEach(r => psh.getRange(r._row,3).setValue(nickname));\n    const cs = rows_(SOCIAL_SHEETS.comments).filter(r => str_(r.userId) === userId && str_(r.status) === 'active');\n    const csh = sheet_(SOCIAL_SHEETS.comments);\n    cs.forEach(r => csh.getRange(r._row,4).setValue(nickname));\n    return {ok:true,userId:userId,nickname:nickname};", 'profile nickname comments')

profile_delete = r'''function profileDelete_(b){
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
  const now=Date.now();
  const profiles=rows_(SOCIAL_SHEETS.profiles);
  const profile=profiles.find(r=>str_(r.userId)===me.userId);
  if(!profile) return {ok:false,error:'NOT_FOUND'};

  const posts=rows_(SOCIAL_SHEETS.posts).filter(r=>str_(r.userId)===me.userId);
  const postIds=new Set(posts.map(r=>str_(r.postId)));
  const psh=sheet_(SOCIAL_SHEETS.posts);
  posts.forEach(r=>{
    psh.getRange(r._row,2).setValue(''); psh.getRange(r._row,3).setValue(''); psh.getRange(r._row,4).setValue('');
    psh.getRange(r._row,6).setValue(now); psh.getRange(r._row,7).setValue('deleted'); psh.getRange(r._row,8).setValue(0);
  });

  const comments=rows_(SOCIAL_SHEETS.comments).filter(r=>str_(r.userId)===me.userId || postIds.has(str_(r.postId)));
  const csh=sheet_(SOCIAL_SHEETS.comments);
  comments.forEach(r=>{
    csh.getRange(r._row,3).setValue(''); csh.getRange(r._row,4).setValue(''); csh.getRange(r._row,5).setValue('');
    csh.getRange(r._row,7).setValue(now); csh.getRange(r._row,8).setValue('deleted');
  });

  const supports=rows_(SOCIAL_SHEETS.supports)
    .filter(r=>str_(r.userId)===me.userId || postIds.has(str_(r.postId)))
    .map(r=>r._row).sort((a,b)=>b-a);
  const ssh=sheet_(SOCIAL_SHEETS.supports); supports.forEach(row=>ssh.deleteRow(row));

  const reports=rows_(SOCIAL_SHEETS.reports), rsh=sheet_(SOCIAL_SHEETS.reports);
  reports.forEach(r=>{
    let changed=false;
    if(str_(r.reporterId)===me.userId){ r.reporterId=''; changed=true; }
    if(str_(r.reportedUserId)===me.userId){ r.reportedUserId=''; changed=true; }
    if(changed) rsh.getRange(r._row,1,1,SOCIAL_HEADERS.Reports.length).setValues([[r.reportId,r.postId,r.reporterId,r.reportedUserId,r.reason,r.createdAt]]);
  });
  const creports=rows_(SOCIAL_SHEETS.commentReports), crsh=sheet_(SOCIAL_SHEETS.commentReports);
  creports.forEach(r=>{
    let changed=false;
    if(str_(r.reporterId)===me.userId){r.reporterId='';changed=true;}
    if(str_(r.reportedUserId)===me.userId){r.reportedUserId='';changed=true;}
    if(changed) crsh.getRange(r._row,1,1,SOCIAL_HEADERS.CommentReports.length).setValues([[r.reportId,r.commentId,r.postId,r.reporterId,r.reportedUserId,r.reason,r.createdAt,r.status,r.reviewedAt,r.reviewNote]]);
  });
  const sh=sheet_(SOCIAL_SHEETS.profiles);
  sh.getRange(profile._row,1).setValue(''); sh.getRange(profile._row,2).setValue(''); sh.getRange(profile._row,3).setValue('');
  sh.getRange(profile._row,5).setValue(now); sh.getRange(profile._row,6).setValue('deleted');
  return {ok:true};
}'''
g = sub_one(g, r"function profileDelete_\(b\)\{.*?\n\}\n\nfunction postCreate_", profile_delete + "\n\nfunction postCreate_", 'profileDelete_', flags=re.S)

post_delete = r'''function postDelete_(b){
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
  const id=cleanPostId_(b.postId); if(!id) return {ok:false,error:'INVALID_ID'};
  const r=rows_(SOCIAL_SHEETS.posts).find(x=>str_(x.postId)===id && str_(x.status)==='active');
  if(!r) return {ok:false,error:'NOT_FOUND'};
  if(str_(r.userId)!==me.userId) return {ok:false,error:'OWNER'};
  const now=Date.now(), sh=sheet_(SOCIAL_SHEETS.posts);
  sh.getRange(r._row,4).setValue(''); sh.getRange(r._row,6).setValue(now); sh.getRange(r._row,7).setValue('deleted'); sh.getRange(r._row,8).setValue(0);
  const supportRows=rows_(SOCIAL_SHEETS.supports).filter(s=>str_(s.postId)===id).map(s=>s._row).sort((a,b)=>b-a);
  const supportSheet=sheet_(SOCIAL_SHEETS.supports); supportRows.forEach(row=>supportSheet.deleteRow(row));
  const comments=rows_(SOCIAL_SHEETS.comments).filter(c=>str_(c.postId)===id && str_(c.status)==='active');
  const csh=sheet_(SOCIAL_SHEETS.comments);
  comments.forEach(c=>{csh.getRange(c._row,3).setValue('');csh.getRange(c._row,4).setValue('');csh.getRange(c._row,5).setValue('');csh.getRange(c._row,7).setValue(now);csh.getRange(c._row,8).setValue('deleted');});
  return {ok:true};
}'''
g = sub_one(g, r"function postDelete_\(b\)\{.*?\n\}\n\nfunction supportToggle_", post_delete + "\n\nfunction supportToggle_", 'postDelete_', flags=re.S)

comment_funcs = r'''
function commentList_(b){
  SOCIAL_SETUP();
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
  const postId=cleanPostId_(b.postId); if(!postId) return {ok:false,error:'INVALID_ID'};
  const post=rows_(SOCIAL_SHEETS.posts).find(r=>str_(r.postId)===postId && str_(r.status)==='active');
  if(!post) return {ok:false,error:'NOT_FOUND'};
  const rows=rows_(SOCIAL_SHEETS.comments).filter(r=>str_(r.postId)===postId && str_(r.status)==='active').sort((a,b)=>num_(a.createdAt)-num_(b.createdAt));
  const items=rows.slice(-100).map(r=>({id:str_(r.commentId),postId:postId,userId:str_(r.userId),nickname:str_(r.nickname),text:str_(r.text),createdAt:num_(r.createdAt),updatedAt:num_(r.updatedAt),mine:str_(r.userId)===me.userId}));
  return {ok:true,items:items,commentCount:rows.length};
}
function commentCreate_(b){
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
  const postId=cleanPostId_(b.postId), text=validCommentText_(b.text);
  if(!postId||!text) return {ok:false,error:'INVALID_COMMENT'};
  const post=rows_(SOCIAL_SHEETS.posts).find(r=>str_(r.postId)===postId && str_(r.status)==='active');
  if(!post) return {ok:false,error:'NOT_FOUND'};
  const now=Date.now();
  const mine=rows_(SOCIAL_SHEETS.comments).filter(r=>str_(r.userId)===me.userId && str_(r.status)==='active');
  if(mine.some(r=>now-num_(r.createdAt)<15000)) return {ok:false,error:'COMMENT_TOO_FAST',message:'댓글은 잠시 후 다시 남겨주세요.'};
  const day=Utilities.formatDate(new Date(now),Session.getScriptTimeZone()||'Asia/Seoul','yyyy-MM-dd');
  const todayCount=mine.filter(r=>Utilities.formatDate(new Date(num_(r.createdAt)),Session.getScriptTimeZone()||'Asia/Seoul','yyyy-MM-dd')===day).length;
  if(todayCount>=60) return {ok:false,error:'COMMENT_DAILY_LIMIT',message:'오늘 남길 수 있는 댓글 수를 넘었습니다.'};
  const id='c_'+Utilities.getUuid().replace(/-/g,'');
  sheet_(SOCIAL_SHEETS.comments).appendRow([id,postId,me.userId,me.nickname,text,now,now,'active']);
  const count=rows_(SOCIAL_SHEETS.comments).filter(r=>str_(r.postId)===postId && str_(r.status)==='active').length;
  return {ok:true,id:id,commentCount:count};
}
function commentDelete_(b){
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
  const id=cleanCommentId_(b.commentId); if(!id) return {ok:false,error:'INVALID_ID'};
  const r=rows_(SOCIAL_SHEETS.comments).find(x=>str_(x.commentId)===id && str_(x.status)==='active');
  if(!r) return {ok:false,error:'NOT_FOUND'};
  if(str_(r.userId)!==me.userId) return {ok:false,error:'OWNER'};
  const now=Date.now(), sh=sheet_(SOCIAL_SHEETS.comments);
  sh.getRange(r._row,3).setValue('');sh.getRange(r._row,4).setValue('');sh.getRange(r._row,5).setValue('');sh.getRange(r._row,7).setValue(now);sh.getRange(r._row,8).setValue('deleted');
  const count=rows_(SOCIAL_SHEETS.comments).filter(x=>str_(x.postId)===str_(r.postId) && str_(x.status)==='active').length;
  return {ok:true,commentCount:count};
}
function commentReport_(b){
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
  const id=cleanCommentId_(b.commentId), reason=str_(b.reason).trim();
  if(!id||REPORT_REASONS.indexOf(reason)<0) return {ok:false,error:'INVALID_REPORT'};
  const c=rows_(SOCIAL_SHEETS.comments).find(x=>str_(x.commentId)===id && str_(x.status)==='active');
  if(!c) return {ok:false,error:'NOT_FOUND'};
  if(str_(c.userId)===me.userId) return {ok:false,error:'OWN_REPORT'};
  const old=rows_(SOCIAL_SHEETS.commentReports).find(r=>str_(r.commentId)===id && str_(r.reporterId)===me.userId);
  if(old) return {ok:true,duplicate:true};
  sheet_(SOCIAL_SHEETS.commentReports).appendRow(['cr_'+Utilities.getUuid().replace(/-/g,''),id,str_(c.postId),me.userId,str_(c.userId),reason,Date.now(),'pending','','']);
  return {ok:true};
}
'''
g = one(g, "\nfunction supportToggle_(b){", comment_funcs + "\nfunction supportToggle_(b){", 'insert comment functions')
g = one(g,
"function validPostText_(v){ const s=str_(v).trim(); return s && s.length<=500 ? s : ''; }\nfunction validUserId_",
"function validPostText_(v){ const s=str_(v).trim(); return s && s.length<=500 ? s : ''; }\nfunction validCommentText_(v){ const s=str_(v).trim(); return s && s.length<=300 ? s : ''; }\nfunction cleanCommentId_(v){ const s=str_(v); return /^c_[A-Za-z0-9]{20,80}$/.test(s)?s:''; }\nfunction validUserId_", 'comment helpers')
p.write_text(g, encoding='utf-8')

# ── docs ───────────────────────────────────────────────────
p=Path('README.md'); r=p.read_text(encoding='utf-8')
head="""## V9.0.2 — 소셜 2단계 · 댓글과 운영 검토
- 게시물에 댓글을 작성하고 댓글 수를 확인할 수 있습니다. 내 댓글은 삭제할 수 있으며, 다른 사용자의 댓글은 신고하거나 작성자를 기기 내 차단할 수 있습니다.
- 소셜 프로필에는 받은 응원·게시물·댓글 요약을 표시합니다. 참고 UI의 프로필/활동 구조만 반영하며 Message·답글·하이브·친구/팔로우 기능은 추가하지 않습니다.
- 소셜 서버는 `Comments`와 `CommentReports` 시트를 추가합니다. `SOCIAL_REVIEW_CHECK()`로 게시물/댓글 신고 현황을 운영자가 확인할 수 있습니다.
- 댓글은 `ohg.social.v1`의 익명 userId/token만 사용하고 `ohg.v1` 회복기록을 읽거나 전송하지 않습니다. `DATA_SCHEMA=6`, `ohg.v1`, `ohg.social.v1`은 유지합니다.
- 실제 댓글 E2E는 `social-apps-script.gs` V9.0.2-social-1 배포와 자원서버 `config.SOCIAL_URL` 연결 후 확인합니다.

"""
if not r.startswith('## V9.0.2'):
    r=head+r
p.write_text(r,encoding='utf-8')

p=Path('SOCIAL_SETUP.md'); d=p.read_text(encoding='utf-8')
notice="""# V9.0.2 댓글 확장 배포 메모

V9.0.2에서는 기존 소셜 전용 스프레드시트에 `Comments`, `CommentReports` 두 시트가 추가됩니다. `social-apps-script.gs`를 교체한 뒤 **SOCIAL_SETUP을 한 번 실행**하면 기존 Profiles/Posts/Supports/Reports는 유지하고 새 시트만 준비합니다. 이어서 **기존 웹 앱 배포를 새 버전으로 갱신**합니다. `/exec` 주소는 바꾸지 않습니다.

운영 검토는 Apps Script의 `SOCIAL_REVIEW_CHECK()`를 실행하거나 `Reports` / `CommentReports` 시트를 확인합니다. 댓글 신고는 `CommentReports`에 `pending` 상태로 저장됩니다.

> 자원서버가 `config.SOCIAL_URL`을 앱에 내려주는 작업은 별도 보류 항목입니다. 이 연결이 완료되기 전에는 앱이 소셜 서버 준비 중으로 표시됩니다.

---

"""
if not d.startswith('# V9.0.2'):
    d=notice+d
p.write_text(d,encoding='utf-8')

# ── invariants ─────────────────────────────────────────────
idx=Path('index.html').read_text(encoding='utf-8')
assert "const BUILD='V9.0.2';" in idx
assert "const DATA_SCHEMA = 6;" in idx
assert "const SOCIAL_KEY = 'ohg.social.v1';" in idx
assert 'data-social-comments' in idx and 'commentReport' in idx
assert "const APP_VERSION = 'V9.0.2';" in Path('sw.js').read_text(encoding='utf-8')
server=Path('social-apps-script.gs').read_text(encoding='utf-8')
for token in ["V9.0.2-social-1","Comments:","CommentReports:","function commentCreate_","function commentReport_","function SOCIAL_REVIEW_CHECK"]:
    assert token in server, token
print('V9.0.2 patch invariants PASS')
