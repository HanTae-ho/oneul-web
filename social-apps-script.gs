/*
 * 오늘 한 걸음 V9.0.7 — 소셜 전용 Apps Script
 * 서버판: V9.0.7-social-1
 *
 * 목적
 * - 자원시트·개인 회복기록(ohg.v1)과 완전히 분리한 익명 소셜 전용 서버입니다.
 * - 저장 대상: 익명 내부 ID, 닉네임, 게시글, 댓글, 응원, 신고.
 * - 감정·충동·HALT·다시 시작·복약·자가점검 등 개인 회복기록은 받지 않습니다.
 *
 * 설치
 * 1) 소셜 전용 빈 Google Spreadsheet를 새로 만듭니다.
 * 2) 확장 프로그램 → Apps Script에서 이 파일 전체를 붙여넣습니다.
 * 3) SOCIAL_SETUP()을 한 번 실행합니다.
 * 4) 배포 → 새 배포 → 웹 앱
 *    - 실행 사용자: 나
 *    - 액세스 권한: 모든 사용자
 * 5) 발급된 /exec 주소를 오늘 한 걸음 자원시트 [설정]의 SOCIAL_URL에 넣고
 *    자원시트 Apps Script를 새 버전으로 배포합니다.
 *
 * V9.0.1-social-2 보완을 그대로 유지합니다.
 * - feed/commentList 조회는 전역 쓰기 lock 밖에서 처리합니다.
 * - POST 원문 크기 제한, 공개 오류 최소화, Asia/Seoul 기준일을 유지합니다.
 * - 게시글·댓글·닉네임이 =,+,-,@ 로 시작해도 Google Sheets 수식이 되지 않게 보호합니다.
 *
 * V9.0.2-social-3 추가
 * - Comments / CommentReports 시트를 추가합니다.
 * - 댓글 작성·조회·내 댓글 삭제·댓글 신고를 지원합니다.
 * - 피드에 댓글 수, 내 프로필 요약에 게시물·댓글·받은 응원 수를 제공합니다.
 * - SOCIAL_REVIEW_CHECK()로 게시글/댓글 신고 현황을 운영자가 점검할 수 있습니다.
 * - 기존 V9.0.1-social-2의 안전장치와 프런트엔드 기존 action/response 계약을 유지합니다.
 *
 * V9.0.2-social-4 고침
 * - 탈퇴한 사람이 남에게 눌러준 응원이 사라져도 그 글의 응원 수가 그대로 남던 것을 고칩니다.
 * - 글·댓글을 지우면 하루 제한과 30초 간격 제한이 되돌아가던 것을 막습니다.
 * - 신고 요청의 오래된 기록 청소를 인증 뒤로 옮깁니다.
 * - 닉네임을 바꿀 때 글·댓글 수만큼 시트를 두드리던 것을 한 번에 씁니다.
 * - 서버가 붐빌 때 SERVER_ERROR 대신 BUSY 로 알려줍니다.
 * - 닉네임 거절 사유에 안내 문구를 붙입니다.
 * - 탈퇴로 함께 삭제되는 타인의 댓글은 userId를 유지해 댓글 제한 우회를 막습니다.
 * - 운영 점검 Logger에는 익명 사용자 ID를 남기지 않습니다.
 *
 * V9.0.3-social-1
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
 * V9.0.7-social-1
 * - 인증 결과(userId/tokenHash/nickname)를 120초 캐시하고 탈퇴 시 즉시 폐기합니다.
 * - 최신 피드는 끝 400행만 읽고, 댓글 수는 postId/status 두 열만 읽습니다.
 * - 내 응원 목록은 두 열만 읽어 10분 캐시하며 응원 변경 시 즉시 무효화합니다.
 * - profileActivity 결과를 사용자별로 캐시하고 쓰기 작업 뒤 세대키를 바꿔 오래된 결과를 사용하지 않습니다.
 * - 기존 action/response 계약과 익명 소셜 전용 저장 원칙은 유지합니다.
 *
 * ★ 앱에서 부를 때 주의
 *   Content-Type 은 반드시 'text/plain;charset=utf-8' 이어야 합니다.
 *   'application/json' 으로 보내면 브라우저가 먼저 OPTIONS 를 보내는데
 *   Apps Script 는 그것을 받지 못해 모든 요청이 통째로 실패합니다.
 */

const SOCIAL_VERSION = 'V9.0.7-social-1';
const SOCIAL_TIME_ZONE = 'Asia/Seoul';
const MAX_SOCIAL_REQUEST_CHARS = 8192;
const MAX_FEED_ITEMS = 60;
const MAX_COMMENT_ITEMS = 100;
const MAX_POSTS_PER_DAY = 20;
const MAX_COMMENTS_PER_DAY = 60;
const MIN_POST_INTERVAL_MS = 30000;
const MIN_COMMENT_INTERVAL_MS = 15000;
const REPORT_RETENTION_DAYS = 365;
const FEED_CACHE_SECONDS = 30;
const SCHEMA_CACHE_SECONDS = 300;
const AUTH_CACHE_SECONDS = 120;      /* 로그인 확인 결과를 짧게 들고 있습니다 */
const FEED_TAIL_ROWS = 400;          /* 최신순 피드는 시트 끝에서 이만큼만 읽습니다 */
const SUPPORT_CACHE_SECONDS = 600;   /* 내 응원 목록은 내가 누를 때만 바뀝니다 */
const MAX_PROFILE_ACTIVITY_ITEMS = 100;
const NICK_REUSE_COOLDOWN_MS = 30 * 24 * 60 * 60 * 1000;

const SOCIAL_SHEETS = {
  profiles: 'Profiles',
  posts: 'Posts',
  comments: 'Comments',
  supports: 'Supports',
  reports: 'Reports',
  commentReports: 'CommentReports'
};

const SOCIAL_HEADERS = {
  Profiles: ['userId','nickname','tokenHash','createdAt','updatedAt','status'],
  Posts: ['postId','userId','nickname','text','createdAt','updatedAt','status','supportCount'],
  Comments: ['commentId','postId','userId','nickname','text','createdAt','updatedAt','status'],
  Supports: ['postId','userId','createdAt'],
  Reports: ['reportId','postId','reporterId','reportedUserId','reason','createdAt'],
  CommentReports: ['reportId','commentId','postId','reporterId','reportedUserId','reason','createdAt','status','reviewedAt','reviewNote']
};

const REPORT_REASONS = [
  '개인정보 노출',
  '비난·괴롭힘',
  '광고·홍보',
  '위험한 사용·도박 정보',
  '기타'
];

const RESERVED_NICKS = [
  '관리자','운영자','오늘한걸음','오늘 한 걸음','마음프로'
];

function SOCIAL_SETUP(){
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if(!ss) throw new Error('소셜 전용 Google Spreadsheet에 연결된 Apps Script에서 실행해주세요.');
  try { ss.setSpreadsheetTimeZone(SOCIAL_TIME_ZONE); } catch(e) {}
  Object.keys(SOCIAL_HEADERS).forEach(function(name){
    let sh = ss.getSheetByName(name);
    if(!sh) sh = ss.insertSheet(name);
    const heads = SOCIAL_HEADERS[name];
    if(sh.getLastRow() === 0){
      sh.getRange(1,1,1,heads.length).setValues([heads]);
    } else {
      const cur = sh.getRange(1,1,1,heads.length).getValues()[0].map(String);
      if(cur.join('|') !== heads.join('|')) throw new Error(name + ' 시트 1행 헤더가 예상 형식과 다릅니다.');
    }
    sh.setFrozenRows(1);
  });
  try { CacheService.getScriptCache().put(schemaCacheKey_(),'1',SCHEMA_CACHE_SECONDS); } catch(ignore) {}
  return 'SOCIAL_SETUP 완료 · ' + SOCIAL_VERSION;
}

function SOCIAL_CHECK(){
  SOCIAL_SETUP();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const out = {ok:true,version:SOCIAL_VERSION,spreadsheet:ss.getName(),timeZone:SOCIAL_TIME_ZONE,sheets:Object.keys(SOCIAL_HEADERS)};
  Logger.log(JSON.stringify(out));
  return JSON.stringify(out);
}

function SOCIAL_REVIEW_CHECK(){
  ensureSheets_();
  const postReports = rows_(SOCIAL_SHEETS.reports);
  const commentReports = rows_(SOCIAL_SHEETS.commentReports);
  const pendingComments = commentReports.filter(function(r){
    const st = str_(r.status).trim(); return !st || st === 'pending';
  });
  const out = {
    ok:true,version:SOCIAL_VERSION,
    postReports:postReports.length,
    commentReports:commentReports.length,
    pendingCommentReports:pendingComments.length,
    lastPostReports:postReports.slice(-20).reverse(),
    lastCommentReports:pendingComments.slice(-20).reverse()
  };
  Logger.log(JSON.stringify({ok:true,version:SOCIAL_VERSION,postReports:out.postReports,commentReports:out.commentReports,pendingCommentReports:out.pendingCommentReports}));
  return JSON.stringify(out);
}

function SOCIAL_TEST_VALIDATION(){
  if(!validUserId_('u_1234567890abcdef')) throw new Error('userId validator 실패');
  if(!validToken_('a'.repeat(64))) throw new Error('token validator 실패');
  if(!validNick_('회복한걸음')) throw new Error('nickname validator 실패');
  if(validNick_('오늘한걸음관리자')) throw new Error('reserved nickname validator 실패');
  if(validNick_('나는관리자')) throw new Error('reserved nickname substring validator 실패');
  if(validNick_('staff회복')) throw new Error('reserved nickname staff validator 실패');
  if(!validPostText_('오늘 모임에 다녀왔습니다.')) throw new Error('post validator 실패');
  if(!validCommentText_('응원합니다.')) throw new Error('comment validator 실패');
  if(!cleanCommentId_('c_' + 'a'.repeat(32))) throw new Error('commentId validator 실패');
  const dangerous = '=IMPORTXML("https://example.com","//x")';
  const stored = cellText_(dangerous);
  if(stored === dangerous || uncellText_(stored) !== dangerous) throw new Error('sheet text guard 실패');
  if(cellText_('평범한 글') !== '평범한 글') throw new Error('평범한 글까지 손대고 있습니다');
  if(typeof setColumnValues_ !== 'function') throw new Error('setColumnValues_ 없음');
  if(typeof recountSupports_ !== 'function') throw new Error('recountSupports_ 없음');
  if(typeof feedPublicSnapshot_ !== 'function') throw new Error('feedPublicSnapshot_ 없음');
  if(typeof profileActivity_ !== 'function') throw new Error('profileActivity_ 없음');
  if(typeof invalidateFeedCache_ !== 'function') throw new Error('invalidateFeedCache_ 없음');
  if(typeof tailRows_ !== 'function') throw new Error('tailRows_ 없음');
  if(typeof commentCounts_ !== 'function') throw new Error('commentCounts_ 없음');
  if(typeof authCacheKey_ !== 'function') throw new Error('authCacheKey_ 없음');
  if(typeof bumpFeedGen_ !== 'function') throw new Error('bumpFeedGen_ 없음');
  if(typeof findPostRow_ !== 'function') throw new Error('findPostRow_ 없음');
  if(typeof commentRowsFor_ !== 'function') throw new Error('commentRowsFor_ 없음');
  if(typeof supportRowsLite_ !== 'function') throw new Error('supportRowsLite_ 없음');
  Logger.log('SOCIAL_TEST_VALIDATION 정상 · ' + SOCIAL_VERSION);
}

function doGet(e){
  try{
    const action = str_((e && e.parameter && e.parameter.action) || 'health');
    if(action === 'health') return json_({ok:true,version:SOCIAL_VERSION});
    return json_({ok:false,error:'UNKNOWN_ACTION'});
  }catch(err){ console.error('social doGet error: ' + safeErrorLog_(err)); return json_({ok:false,error:'SERVER_ERROR'}); }
}

function doPost(e){
  try{
    const raw = e && e.postData ? String(e.postData.contents || '') : '';
    if(!raw) return json_({ok:false,error:'ACTION_REQUIRED'});
    if(raw.length > MAX_SOCIAL_REQUEST_CHARS) return json_({ok:false,error:'REQUEST_TOO_LARGE'});
    let body; try { body = JSON.parse(raw); } catch(parseErr){ return json_({ok:false,error:'BAD_REQUEST'}); }
    const action = str_(body && body.action).trim();
    if(!action) return json_({ok:false,error:'ACTION_REQUIRED'});
    if(action === 'feed') return json_(feed_(body));
    if(action === 'commentList') return json_(commentList_(body));
    if(action === 'profileActivity') return json_(profileActivity_(body));
    const lock = LockService.getScriptLock();
    try { lock.waitLock(5000); }
    catch(lockErr){ return json_({ok:false,error:'BUSY',message:'지금 서버가 붐빕니다. 잠시 후 다시 시도해주세요.'}); }
    try{
      let result = null;
      if(action === 'profile') result = profile_(body);
      else if(action === 'profileDelete') result = profileDelete_(body);
      else if(action === 'postCreate') result = postCreate_(body);
      else if(action === 'postEdit') result = postEdit_(body);
      else if(action === 'postDelete') result = postDelete_(body);
      else if(action === 'commentCreate') result = commentCreate_(body);
      else if(action === 'commentDelete') result = commentDelete_(body);
      else if(action === 'commentReport') result = commentReport_(body);
      else if(action === 'supportToggle') result = supportToggle_(body);
      else if(action === 'report') result = report_(body);
      else return json_({ok:false,error:'UNKNOWN_ACTION'});
      if(result && result.ok && ['profileDelete','postCreate','postEdit','postDelete','commentCreate','commentDelete','supportToggle'].indexOf(action) >= 0){
        invalidateFeedCache_(validUserId_(body.userId));
      }
      return json_(result);
    } finally { try { if(lock.hasLock()) lock.releaseLock(); } catch(ignore) {} }
  }catch(err){ console.error('social doPost error: ' + safeErrorLog_(err)); return json_({ok:false,error:'SERVER_ERROR'}); }
}

function feed_(p){
  ensureSheets_();
  const me = auth_(p.userId,p.token,true);
  if(!me.ok) return me;
  const requester = me.userId;
  const sort = str_(p.sort) === 'support' ? 'support' : 'latest';
  const baseItems = feedPublicSnapshot_(sort);
  const supported = userSupportSet_(requester);
  const items = baseItems.map(function(r){
    return {id:r.id,userId:r.userId,nickname:r.nickname,text:r.text,createdAt:r.createdAt,updatedAt:r.updatedAt,supportCount:r.supportCount,commentCount:r.commentCount,mine:requester && r.userId === requester,supported:supported.has(r.id)};
  });
  return {ok:true,version:SOCIAL_VERSION,items:items};
}

/* ★ 세대(gen)를 키에 넣습니다.
   전에는 이런 일이 있었습니다 —
     ① B가 피드를 요청해 시트를 읽기 시작
     ② 그 사이 A가 글을 올리고 캐시를 지움
     ③ B가 '②보다 먼저 읽은' 옛 목록을 캐시에 넣음
   그러면 A의 글이 30초 동안 아무에게도 안 보입니다.
   세대가 바뀌면 옛 목록은 옛 키에 남아 아무도 읽지 않습니다. */
function feedGen_(){
  try{ return CacheService.getScriptCache().get('gen:'+SOCIAL_VERSION)||'0'; }
  catch(ignore){ return '0'; }
}
function bumpFeedGen_(){
  try{ CacheService.getScriptCache().put('gen:'+SOCIAL_VERSION,String(Date.now()),21600); }
  catch(ignore){}
}

function feedPublicSnapshot_(sort){
  const key='feed:'+SOCIAL_VERSION+':'+feedGen_()+':'+sort;
  let cache=null,raw='';
  try{cache=CacheService.getScriptCache();raw=cache.get(key)||'';}catch(ignore){}
  if(raw){try{const parsed=JSON.parse(raw);if(Array.isArray(parsed))return parsed;}catch(ignore){}}
  /* ★ 최신순은 시트 끝에서만 읽습니다.
     appendRow 로만 쌓이므로 행 순서가 곧 createdAt 순서입니다.
     지운 글이 섞여 있으니 60개를 채우려고 넉넉히 400행을 봅니다.
     '응원 많은 순'은 전부 봐야 하므로 그대로 둡니다. */
  const posts=(sort==='support'
      ? rows_(SOCIAL_SHEETS.posts)
      : tailRows_(SOCIAL_SHEETS.posts,FEED_TAIL_ROWS)
    ).filter(function(r){return str_(r.status)==='active';});

  const wanted={};
  posts.forEach(function(r){wanted[str_(r.postId)]=0;});
  const counts=commentCounts_(wanted);
  posts.sort(function(a,b){return sort==='support'?(num_(b.supportCount)-num_(a.supportCount)||num_(b.createdAt)-num_(a.createdAt)):num_(b.createdAt)-num_(a.createdAt);});
  const items=posts.slice(0,MAX_FEED_ITEMS).map(function(r){return {id:str_(r.postId),userId:str_(r.userId),nickname:str_(r.nickname),text:str_(r.text),createdAt:num_(r.createdAt),updatedAt:num_(r.updatedAt),supportCount:num_(r.supportCount),commentCount:num_(counts[str_(r.postId)]||0)};});
  if(cache){try{const text=JSON.stringify(items);if(text.length<95000)cache.put(key,text,FEED_CACHE_SECONDS);}catch(ignore){}}
  return items;
}

/* 내가 응원한 글 목록.
   ★ 전에는 Supports 시트를 통째로(세 열) 읽었습니다. 응원이 3,000개면 9,000칸입니다.
      필요한 것은 postId·userId 두 열뿐이라 3분의 2가 헛읽기였습니다.
   ★ 캐시도 30초에서 10분으로 늘립니다. 이 목록은 '내가 응원을 누를 때'만 바뀌고
      그때 supportToggle_ 이 캐시를 지웁니다. 짧게 잡을 이유가 없었습니다. */
function userSupportSet_(userId){
  const key='sup:'+SOCIAL_VERSION+':'+userId;
  let cache=null,raw='';
  try{cache=CacheService.getScriptCache();raw=cache.get(key)||'';}catch(ignore){}
  if(raw){try{const parsed=JSON.parse(raw);if(Array.isArray(parsed))return new Set(parsed);}catch(ignore){}}

  const sh=sheet_(SOCIAL_SHEETS.supports),last=sh.getLastRow(),ids=[];
  if(last>=2){
    const v=sh.getRange(2,1,last-1,2).getValues();      /* postId · userId 두 열만 */
    for(let i=0;i<v.length;i++) if(String(v[i][1])===userId) ids.push(uncellText_(String(v[i][0])));
  }
  if(cache){try{const text=JSON.stringify(ids);if(text.length<95000)cache.put(key,text,SUPPORT_CACHE_SECONDS);}catch(ignore){}}
  return new Set(ids);
}

function invalidateFeedCache_(userId){
  try{
    bumpFeedGen_();                       /* 옛 세대 목록은 이제 아무도 안 읽습니다 */
    const c=CacheService.getScriptCache();
    if(userId)c.remove('sup:'+SOCIAL_VERSION+':'+userId);
  }catch(ignore){}
}

function profile_(b){
  ensureSheets_();
  const userId=validUserId_(b.userId),token=validToken_(b.token),nickname=validNick_(b.nickname);
  if(!userId||!token)return {ok:false,error:'INVALID_PROFILE'};
  if(!nickname)return {ok:false,error:'INVALID_NICKNAME',message:'닉네임은 2~12자의 한글·영문·숫자로 지어주세요. 관리자·운영자·오늘한걸음 같은 말은 쓸 수 없습니다.'};
  const sh=sheet_(SOCIAL_SHEETS.profiles),data=rows_(SOCIAL_SHEETS.profiles),found=data.find(function(r){return str_(r.userId)===userId;}),now=Date.now(),hash=hash_(token);
  if(found){
    if(str_(found.tokenHash)!==hash||str_(found.status)!=='active')return {ok:false,error:'AUTH'};
    const current=str_(found.nickname);
    if(current!==nickname)return {ok:false,error:'NICK_LOCKED',message:'가입한 닉네임은 변경할 수 없습니다. 다른 닉네임을 사용하려면 소셜 탈퇴 후 새 프로필을 만들어주세요.'};
    sh.getRange(found._row,5).setValue(now);
    return {ok:true,userId:userId,nickname:current,createdAt:num_(found.createdAt)};
  }
  const same=data.find(function(r){return str_(r.status)==='active'&&nickKey_(r.nickname)===nickKey_(nickname);});
  if(same)return {ok:false,error:'NICK_TAKEN',message:'이미 사용 중인 닉네임입니다.'};
  const reserved=data.find(function(r){return str_(r.status)==='deleted'&&nickKey_(r.nickname)===nickKey_(nickname)&&now-num_(r.updatedAt)<NICK_REUSE_COOLDOWN_MS;});
  if(reserved)return {ok:false,error:'NICK_COOLDOWN',message:'최근 탈퇴한 닉네임입니다. 탈퇴 후 30일이 지나면 다시 사용할 수 있습니다.',availableAt:num_(reserved.updatedAt)+NICK_REUSE_COOLDOWN_MS};
  data.filter(function(r){return str_(r.status)==='deleted'&&nickKey_(r.nickname)===nickKey_(nickname)&&now-num_(r.updatedAt)>=NICK_REUSE_COOLDOWN_MS;}).forEach(function(r){sh.getRange(r._row,2).setValue('');});
  sh.appendRow([userId,cellText_(nickname),hash,now,now,'active']);
  return {ok:true,userId:userId,nickname:nickname,createdAt:now};
}

function profileActivity_(b){
  ensureSheets_();
  const me=auth_(b.userId,b.token,true);if(!me.ok)return me;
  const akey='act:'+SOCIAL_VERSION+':'+feedGen_()+':'+me.userId;
  try{
    const raw=CacheService.getScriptCache().get(akey);
    if(raw)return JSON.parse(raw);
  }catch(ignore){}
  const profile=rows_(SOCIAL_SHEETS.profiles).find(function(r){return str_(r.userId)===me.userId&&str_(r.status)==='active';});
  if(!profile)return {ok:false,error:'AUTH'};   /* 가입일이 필요해 여기만 프로필을 읽습니다 */
  /* ★ 여기는 시트를 훑는 것 말고 줄일 방법이 없습니다.
     한 사람의 글·댓글은 시트 전체에 흩어져 있어서 '내 행만 골라 읽기'가 오히려 손해였습니다.
     대신 결과를 통째로 캐시합니다 — 이 화면은 그 사람이 글·댓글을 쓰거나 지울 때만 바뀌고,
     그때 invalidateFeedCache_ 가 함께 지웁니다. */
  const allPosts=rows_(SOCIAL_SHEETS.posts).filter(function(r){return str_(r.status)==='active';});
  const allComments=rows_(SOCIAL_SHEETS.comments).filter(function(r){return str_(r.status)==='active';});
  const supports=supportRowsLite_(),counts={};
  allComments.forEach(function(r){const id=str_(r.postId);counts[id]=(counts[id]||0)+1;});
  const myPosts=allPosts.filter(function(r){return str_(r.userId)===me.userId;}).sort(function(a,b){return num_(b.createdAt)-num_(a.createdAt);});
  const myIds=new Set(myPosts.map(function(r){return str_(r.postId);})),postById={};
  allPosts.forEach(function(r){postById[str_(r.postId)]=r;});
  const myComments=allComments.filter(function(r){return str_(r.userId)===me.userId;}).sort(function(a,b){return num_(b.createdAt)-num_(a.createdAt);});
  const posts=myPosts.slice(0,MAX_PROFILE_ACTIVITY_ITEMS).map(function(r){return {id:str_(r.postId),text:str_(r.text),createdAt:num_(r.createdAt),updatedAt:num_(r.updatedAt),supportCount:num_(r.supportCount),commentCount:num_(counts[str_(r.postId)]||0)};});
  const comments=myComments.slice(0,MAX_PROFILE_ACTIVITY_ITEMS).map(function(r){const post=postById[str_(r.postId)];return {id:str_(r.commentId),postId:str_(r.postId),text:str_(r.text),createdAt:num_(r.createdAt),updatedAt:num_(r.updatedAt),postText:post?str_(post.text).slice(0,160):'',postNickname:post?str_(post.nickname):''};});
  const out={ok:true,version:SOCIAL_VERSION,profile:{nickname:me.nickname,createdAt:num_(profile.createdAt)},stats:{postCount:myPosts.length,commentCount:myComments.length,supportReceived:supports.filter(function(id){return myIds.has(id);}).length},posts:posts,comments:comments};
  try{const text=JSON.stringify(out);if(text.length<95000)CacheService.getScriptCache().put(akey,text,SUPPORT_CACHE_SECONDS);}catch(ignore){}
  return out;
}

function profileDelete_(b){
  const me = auth_(b.userId,b.token); if(!me.ok) return me;
  const now = Date.now();
  const profiles = rows_(SOCIAL_SHEETS.profiles);
  const profile = profiles.find(function(r){ return str_(r.userId) === me.userId; });
  if(!profile) return {ok:false,error:'NOT_FOUND'};
  const posts = rows_(SOCIAL_SHEETS.posts).filter(function(r){ return str_(r.userId) === me.userId; });
  const postIds = new Set(posts.map(function(r){ return str_(r.postId); }));
  const psh = sheet_(SOCIAL_SHEETS.posts);
  posts.forEach(function(r){ psh.getRange(r._row,2,1,3).setValues([['','','']]); psh.getRange(r._row,6,1,3).setValues([[now,'deleted',0]]); });
  const comments = rows_(SOCIAL_SHEETS.comments).filter(function(r){ return str_(r.userId) === me.userId || postIds.has(str_(r.postId)); });
  const csh = sheet_(SOCIAL_SHEETS.comments);
  comments.forEach(function(r){
    const mine = str_(r.userId) === me.userId;
    if(mine) csh.getRange(r._row,3,1,3).setValues([['','','']]);
    else csh.getRange(r._row,4,1,2).setValues([['','']]);
    csh.getRange(r._row,7,1,2).setValues([[now,'deleted']]);
  });
  const allSupports = rows_(SOCIAL_SHEETS.supports);
  const othersSupported = [];
  allSupports.forEach(function(r){ if(str_(r.userId) === me.userId && !postIds.has(str_(r.postId))) othersSupported.push(str_(r.postId)); });
  const supportRows = allSupports.filter(function(r){ return str_(r.userId) === me.userId || postIds.has(str_(r.postId)); }).map(function(r){ return r._row; }).sort(function(a,b){ return b-a; });
  const ssh = sheet_(SOCIAL_SHEETS.supports); supportRows.forEach(function(row){ ssh.deleteRow(row); });
  recountSupports_(othersSupported);
  const reports = rows_(SOCIAL_SHEETS.reports); const rsh = sheet_(SOCIAL_SHEETS.reports);
  reports.forEach(function(r){ let changed=false; if(str_(r.reporterId)===me.userId){r.reporterId='';changed=true;} if(str_(r.reportedUserId)===me.userId){r.reportedUserId='';changed=true;} if(changed) rsh.getRange(r._row,1,1,SOCIAL_HEADERS.Reports.length).setValues([[r.reportId,r.postId,r.reporterId,r.reportedUserId,r.reason,r.createdAt]]); });
  const commentReports=rows_(SOCIAL_SHEETS.commentReports); const crsh=sheet_(SOCIAL_SHEETS.commentReports);
  commentReports.forEach(function(r){ let changed=false; if(str_(r.reporterId)===me.userId){r.reporterId='';changed=true;} if(str_(r.reportedUserId)===me.userId){r.reportedUserId='';changed=true;} if(changed) crsh.getRange(r._row,1,1,SOCIAL_HEADERS.CommentReports.length).setValues([[r.reportId,r.commentId,r.postId,r.reporterId,r.reportedUserId,r.reason,r.createdAt,r.status,r.reviewedAt,r.reviewNote]]); });
  const sh=sheet_(SOCIAL_SHEETS.profiles);
  sh.getRange(profile._row,1).setValue(''); sh.getRange(profile._row,2).setValue(cellText_(me.nickname)); sh.getRange(profile._row,3).setValue(''); sh.getRange(profile._row,5).setValue(now); sh.getRange(profile._row,6).setValue('deleted');
  /* 탈퇴는 즉시 반영해야 합니다. 캐시가 남아 있으면 탈퇴한 토큰이 잠시 통합니다. */
  try{ CacheService.getScriptCache().remove(authCacheKey_(me.userId)); }catch(ignore){}
  return {ok:true};
}

function postCreate_(b){
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
  const text=validPostText_(b.text); if(!text) return {ok:false,error:'INVALID_TEXT'};
  const now=Date.now();
  const mine=rows_(SOCIAL_SHEETS.posts).filter(function(r){ return str_(r.userId)===me.userId; });
  if(mine.some(function(r){return now-num_(r.createdAt)<MIN_POST_INTERVAL_MS;})) return {ok:false,error:'TOO_FAST',message:'잠시 후 다시 올려주세요.'};
  const day=Utilities.formatDate(new Date(now),SOCIAL_TIME_ZONE,'yyyy-MM-dd');
  const todayCount=mine.filter(function(r){const ts=num_(r.createdAt);return ts>0&&Utilities.formatDate(new Date(ts),SOCIAL_TIME_ZONE,'yyyy-MM-dd')===day;}).length;
  if(todayCount>=MAX_POSTS_PER_DAY) return {ok:false,error:'DAILY_LIMIT',message:'오늘 올릴 수 있는 글 수를 넘었습니다.'};
  const id='p_'+Utilities.getUuid().replace(/-/g,'');
  sheet_(SOCIAL_SHEETS.posts).appendRow([id,me.userId,cellText_(me.nickname),cellText_(text),now,now,'active',0]);
  return {ok:true,id:id};
}

function postEdit_(b){
  const me=auth_(b.userId,b.token); if(!me.ok)return me;
  const id=cleanPostId_(b.postId),text=validPostText_(b.text); if(!id||!text)return {ok:false,error:'INVALID_TEXT'};
  const r=rows_(SOCIAL_SHEETS.posts).find(function(x){return str_(x.postId)===id&&str_(x.status)==='active';});
  if(!r)return {ok:false,error:'NOT_FOUND'}; if(str_(r.userId)!==me.userId)return {ok:false,error:'OWNER'};
  const sh=sheet_(SOCIAL_SHEETS.posts); sh.getRange(r._row,4).setValue(cellText_(text)); sh.getRange(r._row,6).setValue(Date.now()); return {ok:true};
}

function postDelete_(b){
  const me=auth_(b.userId,b.token); if(!me.ok)return me;
  const id=cleanPostId_(b.postId); if(!id)return {ok:false,error:'INVALID_ID'};
  const r=rows_(SOCIAL_SHEETS.posts).find(function(x){return str_(x.postId)===id&&str_(x.status)==='active';}); if(!r)return {ok:false,error:'NOT_FOUND'}; if(str_(r.userId)!==me.userId)return {ok:false,error:'OWNER'};
  const now=Date.now(),sh=sheet_(SOCIAL_SHEETS.posts); sh.getRange(r._row,3,1,2).setValues([['','']]); sh.getRange(r._row,6,1,3).setValues([[now,'deleted',0]]);
  const supportRows=rows_(SOCIAL_SHEETS.supports).filter(function(s){return str_(s.postId)===id;}).map(function(s){return s._row;}).sort(function(a,b){return b-a;}); const supportSheet=sheet_(SOCIAL_SHEETS.supports); supportRows.forEach(function(row){supportSheet.deleteRow(row);});
  const comments=rows_(SOCIAL_SHEETS.comments).filter(function(c){return str_(c.postId)===id&&str_(c.status)==='active';}); const csh=sheet_(SOCIAL_SHEETS.comments); comments.forEach(function(c){csh.getRange(c._row,4,1,2).setValues([['','']]);csh.getRange(c._row,7,1,2).setValues([[now,'deleted']]);}); return {ok:true};
}

function commentList_(b){
  ensureSheets_(); const me=auth_(b.userId,b.token,true); if(!me.ok)return me; const postId=cleanPostId_(b.postId); if(!postId)return {ok:false,error:'INVALID_ID'};
  const post=findPostRow_(postId); if(!post||str_(post.status)!=='active')return {ok:false,error:'NOT_FOUND'};
  const all=commentRowsFor_(postId).filter(function(r){return str_(r.status)==='active';}).sort(function(a,b){return num_(a.createdAt)-num_(b.createdAt);});
  const items=all.slice(-MAX_COMMENT_ITEMS).map(function(r){return {id:str_(r.commentId),postId:postId,userId:str_(r.userId),nickname:str_(r.nickname),text:str_(r.text),createdAt:num_(r.createdAt),updatedAt:num_(r.updatedAt),mine:str_(r.userId)===me.userId};}); return {ok:true,version:SOCIAL_VERSION,items:items,commentCount:all.length};
}

function commentCreate_(b){
  const me=auth_(b.userId,b.token); if(!me.ok)return me; const postId=cleanPostId_(b.postId),text=validCommentText_(b.text); if(!postId||!text)return {ok:false,error:'INVALID_COMMENT'};
  const post=rows_(SOCIAL_SHEETS.posts).find(function(r){return str_(r.postId)===postId&&str_(r.status)==='active';}); if(!post)return {ok:false,error:'NOT_FOUND'};
  const now=Date.now(),commentRows=rows_(SOCIAL_SHEETS.comments),mine=commentRows.filter(function(r){return str_(r.userId)===me.userId;});
  if(mine.some(function(r){return now-num_(r.createdAt)<MIN_COMMENT_INTERVAL_MS;}))return {ok:false,error:'COMMENT_TOO_FAST',message:'댓글은 잠시 후 다시 남겨주세요.'};
  const day=Utilities.formatDate(new Date(now),SOCIAL_TIME_ZONE,'yyyy-MM-dd'); const todayCount=mine.filter(function(r){const ts=num_(r.createdAt);return ts>0&&Utilities.formatDate(new Date(ts),SOCIAL_TIME_ZONE,'yyyy-MM-dd')===day;}).length;
  if(todayCount>=MAX_COMMENTS_PER_DAY)return {ok:false,error:'COMMENT_DAILY_LIMIT',message:'오늘 남길 수 있는 댓글 수를 넘었습니다.'};
  const id='c_'+Utilities.getUuid().replace(/-/g,''),count=commentRows.filter(function(r){return str_(r.postId)===postId&&str_(r.status)==='active';}).length+1; sheet_(SOCIAL_SHEETS.comments).appendRow([id,postId,me.userId,cellText_(me.nickname),cellText_(text),now,now,'active']);
  return {ok:true,id:id,commentCount:count};
}

function commentDelete_(b){
  const me=auth_(b.userId,b.token); if(!me.ok)return me; const id=cleanCommentId_(b.commentId); if(!id)return {ok:false,error:'INVALID_ID'};
  const r=rows_(SOCIAL_SHEETS.comments).find(function(x){return str_(x.commentId)===id&&str_(x.status)==='active';}); if(!r)return {ok:false,error:'NOT_FOUND'}; if(str_(r.userId)!==me.userId)return {ok:false,error:'OWNER'};
  const now=Date.now(),sh=sheet_(SOCIAL_SHEETS.comments); sh.getRange(r._row,4,1,2).setValues([['','']]); sh.getRange(r._row,7,1,2).setValues([[now,'deleted']]);
  const count=rows_(SOCIAL_SHEETS.comments).filter(function(x){return str_(x.postId)===str_(r.postId)&&str_(x.status)==='active';}).length; return {ok:true,commentCount:count};
}

function commentReport_(b){
  const me=auth_(b.userId,b.token); if(!me.ok)return me; cleanupCommentReports_();
  const id=cleanCommentId_(b.commentId),reason=str_(b.reason).trim(); if(!id||REPORT_REASONS.indexOf(reason)<0)return {ok:false,error:'INVALID_REPORT'};
  const c=rows_(SOCIAL_SHEETS.comments).find(function(x){return str_(x.commentId)===id&&str_(x.status)==='active';}); if(!c)return {ok:false,error:'NOT_FOUND'}; if(str_(c.userId)===me.userId)return {ok:false,error:'OWN_REPORT'};
  const old=rows_(SOCIAL_SHEETS.commentReports).find(function(r){return str_(r.commentId)===id&&str_(r.reporterId)===me.userId;}); if(old)return {ok:true,duplicate:true};
  sheet_(SOCIAL_SHEETS.commentReports).appendRow(['cr_'+Utilities.getUuid().replace(/-/g,''),id,str_(c.postId),me.userId,str_(c.userId),reason,Date.now(),'pending','','']); return {ok:true};
}

function supportToggle_(b){
  const me=auth_(b.userId,b.token); if(!me.ok)return me; const id=cleanPostId_(b.postId); if(!id)return {ok:false,error:'INVALID_ID'};
  const post=rows_(SOCIAL_SHEETS.posts).find(function(x){return str_(x.postId)===id&&str_(x.status)==='active';}); if(!post)return {ok:false,error:'NOT_FOUND'}; if(str_(post.userId)===me.userId)return {ok:false,error:'OWN_SUPPORT'};
  const sh=sheet_(SOCIAL_SHEETS.supports),supportRows=rows_(SOCIAL_SHEETS.supports),old=supportRows.find(function(r){return str_(r.postId)===id&&str_(r.userId)===me.userId;}),before=supportRows.filter(function(r){return str_(r.postId)===id;}).length; let on=true,count=before+1;
  if(old){sh.deleteRow(old._row);on=false;count=Math.max(0,before-1);}else sh.appendRow([id,me.userId,Date.now()]);
  sheet_(SOCIAL_SHEETS.posts).getRange(post._row,8).setValue(count); return {ok:true,supported:on,supportCount:count};
}

function report_(b){
  const me=auth_(b.userId,b.token); if(!me.ok)return me; cleanupReports_();
  const id=cleanPostId_(b.postId),reason=str_(b.reason).trim(); if(!id||REPORT_REASONS.indexOf(reason)<0)return {ok:false,error:'INVALID_REPORT'};
  const post=rows_(SOCIAL_SHEETS.posts).find(function(x){return str_(x.postId)===id&&str_(x.status)==='active';}); if(!post)return {ok:false,error:'NOT_FOUND'}; if(str_(post.userId)===me.userId)return {ok:false,error:'OWN_REPORT'};
  const old=rows_(SOCIAL_SHEETS.reports).find(function(r){return str_(r.postId)===id&&str_(r.reporterId)===me.userId;}); if(old)return {ok:true,duplicate:true};
  sheet_(SOCIAL_SHEETS.reports).appendRow(['r_'+Utilities.getUuid().replace(/-/g,''),id,me.userId,str_(post.userId),reason,Date.now()]); return {ok:true};
}

/* ★ 여기가 모든 요청이 지나는 길목입니다.
   고치기 전에는 요청 하나마다 Profiles 시트를 통째로 읽었습니다.
   사람이 300명이면 1,800칸, 3,000명이면 18,000칸을 매번 읽습니다.
   토큰 해시와 닉네임만 짧게 들고 있으면 그 읽기가 통째로 사라집니다. */
function authCacheKey_(uid){ return 'auth:'+SOCIAL_VERSION+':'+uid; }

function auth_(userId,token,skipEnsure){
  if(!skipEnsure) ensureSheets_();
  const uid=validUserId_(userId),tok=validToken_(token);
  if(!uid||!tok)return {ok:false,error:'AUTH'};
  const want=hash_(tok);

  let cache=null;
  try{
    cache=CacheService.getScriptCache();
    const raw=cache.get(authCacheKey_(uid));
    if(raw){
      const c=JSON.parse(raw);
      /* 토큰이 맞을 때만 캐시를 믿습니다. 틀리면 시트를 봐야
         '토큰이 바뀐 것'과 '탈퇴한 것'을 구분할 수 있습니다. */
      if(c&&c.h===want) return {ok:true,userId:uid,nickname:str_(c.n)};
    }
  }catch(ignore){ cache=null; }

  const p=rows_(SOCIAL_SHEETS.profiles).find(function(r){return str_(r.userId)===uid&&str_(r.status)==='active';});
  if(!p||str_(p.tokenHash)!==want)return {ok:false,error:'AUTH'};

  if(cache){try{cache.put(authCacheKey_(uid),JSON.stringify({h:want,n:str_(p.nickname)}),AUTH_CACHE_SECONDS);}catch(ignore){}}
  return {ok:true,userId:uid,nickname:str_(p.nickname)};
}

function cleanupReports_(){
  const cutoff=Date.now()-REPORT_RETENTION_DAYS*24*60*60*1000; const old=rows_(SOCIAL_SHEETS.reports).filter(function(r){return num_(r.createdAt)>0&&num_(r.createdAt)<cutoff;}).map(function(r){return r._row;}).sort(function(a,b){return b-a;}); if(!old.length)return; const sh=sheet_(SOCIAL_SHEETS.reports); old.forEach(function(row){sh.deleteRow(row);});
}
function cleanupCommentReports_(){
  const cutoff=Date.now()-REPORT_RETENTION_DAYS*24*60*60*1000; const old=rows_(SOCIAL_SHEETS.commentReports).filter(function(r){return num_(r.createdAt)>0&&num_(r.createdAt)<cutoff;}).map(function(r){return r._row;}).sort(function(a,b){return b-a;}); if(!old.length)return; const sh=sheet_(SOCIAL_SHEETS.commentReports); old.forEach(function(row){sh.deleteRow(row);});
}

function validNick_(v){
  const n=str_(v).replace(/\s+/g,' ').trim(); if(n.length<2||n.length>12)return ''; if(!/^[가-힣A-Za-z0-9 _-]+$/.test(n))return '';
  const nk=nickKey_(n); if(RESERVED_NICKS.some(function(x){return nickKey_(x)===nk;}))return ''; if(/관리자|운영자|오늘한걸음|마음프로|admin|official|staff/i.test(nk))return ''; return n;
}
function nickKey_(v){return str_(v).replace(/\s+/g,'').toLowerCase();}
function validPostText_(v){const s=str_(v).replace(/\u0000/g,'').trim();return s&&s.length<=500?s:'';}
function validCommentText_(v){const s=str_(v).replace(/\u0000/g,'').trim();return s&&s.length<=300?s:'';}
function validUserId_(v){const s=str_(v);return /^u_[A-Za-z0-9-]{16,80}$/.test(s)?s:'';}
function validToken_(v){const s=str_(v);return /^[A-Fa-f0-9]{48,160}$/.test(s)?s:'';}
function cleanPostId_(v){const s=str_(v);return /^p_[A-Za-z0-9]{20,80}$/.test(s)?s:'';}
function cleanCommentId_(v){const s=str_(v);return /^c_[A-Za-z0-9]{20,80}$/.test(s)?s:'';}
function cellText_(v){const s=str_(v);return /^[=+\-@]/.test(s)?'\u200B'+s:s;}
function uncellText_(v){const s=str_(v);return s.charAt(0)==='\u200B'?s.slice(1):s;}
function str_(v){return v==null?'':String(v);}
function num_(v){const n=Number(v);return isFinite(n)?n:0;}
function hash_(v){return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,str_(v),Utilities.Charset.UTF_8).map(function(b){return ('0'+((b<0?b+256:b).toString(16))).slice(-2);}).join('');}
function json_(o){return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);}
function safeErrorLog_(err){const name=err&&err.name?String(err.name):'Error';const msg=err&&err.message?String(err.message):String(err||'');return (name+': '+msg).slice(0,500);}
function schemaCacheKey_(){return 'schema:'+SOCIAL_VERSION;}
function ensureSheets_(){const ss=SpreadsheetApp.getActiveSpreadsheet();if(!ss)throw new Error('NO_SPREADSHEET');let cache=null;try{cache=CacheService.getScriptCache();if(cache.get(schemaCacheKey_())==='1')return;}catch(ignore){cache=null;}Object.keys(SOCIAL_HEADERS).forEach(function(name){const sh=ss.getSheetByName(name);if(!sh)throw new Error('MISSING_SHEET:'+name);const heads=SOCIAL_HEADERS[name];const cur=sh.getRange(1,1,1,heads.length).getValues()[0].map(String);if(cur.join('|')!==heads.join('|'))throw new Error('BAD_HEADER:'+name);});if(cache){try{cache.put(schemaCacheKey_(),'1',SCHEMA_CACHE_SECONDS);}catch(ignore){}}}
function setColumnValues_(name,col,changes){const keys=Object.keys(changes);if(!keys.length)return;const sh=sheet_(name),last=sh.getLastRow();if(last<2)return;const rng=sh.getRange(2,col,last-1,1),cur=rng.getValues();let touched=false;keys.forEach(function(k){const i=Number(k)-2;if(i>=0&&i<cur.length){cur[i][0]=changes[k];touched=true;}});if(touched)rng.setValues(cur);}
function recountSupports_(postIds){const ids=[];(postIds||[]).forEach(function(id){if(id&&ids.indexOf(id)<0)ids.push(id);});if(!ids.length)return;const counts={};ids.forEach(function(id){counts[id]=0;});rows_(SOCIAL_SHEETS.supports).forEach(function(r){const id=str_(r.postId);if(counts.hasOwnProperty(id))counts[id]++;});const changes={};rows_(SOCIAL_SHEETS.posts).forEach(function(r){const id=str_(r.postId);if(counts.hasOwnProperty(id))changes[r._row]=counts[id];});setColumnValues_(SOCIAL_SHEETS.posts,8,changes);}
/* 시트 끝에서 n행만 읽습니다. 전체를 읽지 않습니다. */
/* 응원은 postId 열만 있으면 셀 수 있습니다. */
function supportRowsLite_(){
  const sh=sheet_(SOCIAL_SHEETS.supports),last=sh.getLastRow();
  if(last<2)return [];
  return sh.getRange(2,1,last-1,1).getValues().map(function(a){return uncellText_(String(a[0]));});
}

function tailRows_(name,n){
  const sh=sheet_(name),last=sh.getLastRow(),heads=SOCIAL_HEADERS[name];
  if(last<2)return [];
  const start=Math.max(2,last-n+1);
  return sh.getRange(start,1,last-start+1,heads.length).getValues().map(function(a,i){
    const o={_row:start+i};
    heads.forEach(function(h,j){const v=a[j];o[h]=typeof v==='string'?uncellText_(v):v;});
    return o;
  });
}

/* 댓글 수만 필요할 때 본문·닉네임까지 읽지 않습니다.
   Comments 는 postId(2열)와 status(8열) 두 열만 봅니다. */
function commentCounts_(wanted){
  const sh=sheet_(SOCIAL_SHEETS.comments),last=sh.getLastRow();
  const counts={};
  if(last<2)return counts;
  const ids=sh.getRange(2,2,last-1,1).getValues();
  const sts=sh.getRange(2,8,last-1,1).getValues();
  for(let i=0;i<ids.length;i++){
    if(String(sts[i][0])!=='active')continue;
    const id=uncellText_(String(ids[i][0]));
    if(wanted&&!wanted.hasOwnProperty(id))continue;
    counts[id]=(counts[id]||0)+1;
  }
  return counts;
}

/* 글 하나가 살아 있는지만 볼 때 Posts 를 통째로 읽지 않습니다.
   postId·status 두 열만 훑어 행 번호를 찾고, 그 한 줄만 읽습니다. */
function findPostRow_(postId){
  const sh=sheet_(SOCIAL_SHEETS.posts),last=sh.getLastRow();
  if(last<2)return null;
  const ids=sh.getRange(2,1,last-1,1).getValues();
  for(let i=ids.length-1;i>=0;i--){                       /* 최근 글이 뒤에 있으니 뒤에서부터 */
    if(uncellText_(String(ids[i][0]))===postId){
      const row=i+2;
      const v=sh.getRange(row,1,1,SOCIAL_HEADERS.Posts.length).getValues()[0];
      const o={_row:row};
      SOCIAL_HEADERS.Posts.forEach(function(h,j){const x=v[j];o[h]=typeof x==='string'?uncellText_(x):x;});
      return o;
    }
  }
  return null;
}

/* 한 글의 댓글만 읽습니다.
   postId 열만 훑어 해당 행의 처음~끝 구간을 정하고 그 구간만 한 번에 읽습니다.
   같은 글의 댓글은 대개 시간이 몰려 있어 구간이 좁습니다. */
function commentRowsFor_(postId){
  const sh=sheet_(SOCIAL_SHEETS.comments),last=sh.getLastRow(),heads=SOCIAL_HEADERS.Comments;
  if(last<2)return [];
  const ids=sh.getRange(2,2,last-1,1).getValues();
  let lo=-1,hi=-1;
  for(let i=0;i<ids.length;i++){
    if(uncellText_(String(ids[i][0]))!==postId)continue;
    if(lo<0)lo=i; hi=i;
  }
  if(lo<0)return [];
  const start=lo+2,cnt=hi-lo+1;
  return sh.getRange(start,1,cnt,heads.length).getValues().map(function(a,i){
    const o={_row:start+i};
    heads.forEach(function(h,j){const v=a[j];o[h]=typeof v==='string'?uncellText_(v):v;});
    return o;
  }).filter(function(r){return str_(r.postId)===postId;});
}

function sheet_(name){const sh=SpreadsheetApp.getActiveSpreadsheet().getSheetByName(name);if(!sh)throw new Error('MISSING_SHEET:'+name);return sh;}
function rows_(name){const sh=sheet_(name),last=sh.getLastRow(),heads=SOCIAL_HEADERS[name];if(last<2)return [];return sh.getRange(2,1,last-1,heads.length).getValues().map(function(a,i){const o={_row:i+2};heads.forEach(function(h,j){const v=a[j];o[h]=typeof v==='string'?uncellText_(v):v;});return o;});}
