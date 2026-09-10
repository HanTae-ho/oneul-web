/*
 * 오늘 한 걸음 V9.0.3 — 소셜 전용 Apps Script
 * 서버판: V9.0.3-social-1
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
 * ★ 앱에서 부를 때 주의
 *   Content-Type 은 반드시 'text/plain;charset=utf-8' 이어야 합니다.
 *   'application/json' 으로 보내면 브라우저가 먼저 OPTIONS 를 보내는데
 *   Apps Script 는 그것을 받지 못해 모든 요청이 통째로 실패합니다.
 */

const SOCIAL_VERSION = 'V9.0.3-social-1';
const SOCIAL_TIME_ZONE = 'Asia/Seoul';
const MAX_SOCIAL_REQUEST_CHARS = 8192;
const MAX_FEED_ITEMS = 60;
const MAX_COMMENT_ITEMS = 100;
const MAX_POSTS_PER_DAY = 20;
const MAX_COMMENTS_PER_DAY = 60;
const MIN_POST_INTERVAL_MS = 30000;
const MIN_COMMENT_INTERVAL_MS = 15000;
const REPORT_RETENTION_DAYS = 365;
const FEED_CACHE_SECONDS = 12;
const SCHEMA_CACHE_SECONDS = 300;
const MAX_PROFILE_ACTIVITY_ITEMS = 100;

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
    try { lock.waitLock(15000); }
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

function feedPublicSnapshot_(sort){
  const key='feed:'+SOCIAL_VERSION+':'+sort;
  let cache=null,raw='';
  try{cache=CacheService.getScriptCache();raw=cache.get(key)||'';}catch(ignore){}
  if(raw){try{const parsed=JSON.parse(raw);if(Array.isArray(parsed))return parsed;}catch(ignore){}}
  const posts=rows_(SOCIAL_SHEETS.posts).filter(function(r){return str_(r.status)==='active';});
  const comments=rows_(SOCIAL_SHEETS.comments).filter(function(r){return str_(r.status)==='active';});
  const counts={};
  comments.forEach(function(r){const id=str_(r.postId);counts[id]=(counts[id]||0)+1;});
  posts.sort(function(a,b){return sort==='support'?(num_(b.supportCount)-num_(a.supportCount)||num_(b.createdAt)-num_(a.createdAt)):num_(b.createdAt)-num_(a.createdAt);});
  const items=posts.slice(0,MAX_FEED_ITEMS).map(function(r){return {id:str_(r.postId),userId:str_(r.userId),nickname:str_(r.nickname),text:str_(r.text),createdAt:num_(r.createdAt),updatedAt:num_(r.updatedAt),supportCount:num_(r.supportCount),commentCount:num_(counts[str_(r.postId)]||0)};});
  if(cache){try{const text=JSON.stringify(items);if(text.length<95000)cache.put(key,text,FEED_CACHE_SECONDS);}catch(ignore){}}
  return items;
}

function userSupportSet_(userId){
  const key='sup:'+SOCIAL_VERSION+':'+userId;
  let cache=null,raw='';
  try{cache=CacheService.getScriptCache();raw=cache.get(key)||'';}catch(ignore){}
  if(raw){try{const parsed=JSON.parse(raw);if(Array.isArray(parsed))return new Set(parsed);}catch(ignore){}}
  const ids=rows_(SOCIAL_SHEETS.supports).filter(function(r){return str_(r.userId)===userId;}).map(function(r){return str_(r.postId);});
  if(cache){try{const text=JSON.stringify(ids);if(text.length<95000)cache.put(key,text,FEED_CACHE_SECONDS);}catch(ignore){}}
  return new Set(ids);
}

function invalidateFeedCache_(userId){
  try{
    const c=CacheService.getScriptCache();
    c.remove('feed:'+SOCIAL_VERSION+':latest');
    c.remove('feed:'+SOCIAL_VERSION+':support');
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
  sh.appendRow([userId,cellText_(nickname),hash,now,now,'active']);
  return {ok:true,userId:userId,nickname:nickname,createdAt:now};
}

function profileActivity_(b){
  ensureSheets_();
  const me=auth_(b.userId,b.token,true);if(!me.ok)return me;
  const profile=rows_(SOCIAL_SHEETS.profiles).find(function(r){return str_(r.userId)===me.userId&&str_(r.status)==='active';});
  if(!profile)return {ok:false,error:'AUTH'};
  const allPosts=rows_(SOCIAL_SHEETS.posts).filter(function(r){return str_(r.status)==='active';});
  const allComments=rows_(SOCIAL_SHEETS.comments).filter(function(r){return str_(r.status)==='active';});
  const supports=rows_(SOCIAL_SHEETS.supports),counts={};
  allComments.forEach(function(r){const id=str_(r.postId);counts[id]=(counts[id]||0)+1;});
  const myPosts=allPosts.filter(function(r){return str_(r.userId)===me.userId;}).sort(function(a,b){return num_(b.createdAt)-num_(a.createdAt);});
  const myIds=new Set(myPosts.map(function(r){return str_(r.postId);})),postById={};
  allPosts.forEach(function(r){postById[str_(r.postId)]=r;});
  const myComments=allComments.filter(function(r){return str_(r.userId)===me.userId;}).sort(function(a,b){return num_(b.createdAt)-num_(a.createdAt);});
  const posts=myPosts.slice(0,MAX_PROFILE_ACTIVITY_ITEMS).map(function(r){return {id:str_(r.postId),text:str_(r.text),createdAt:num_(r.createdAt),updatedAt:num_(r.updatedAt),supportCount:num_(r.supportCount),commentCount:num_(counts[str_(r.postId)]||0)};});
  const comments=myComments.slice(0,MAX_PROFILE_ACTIVITY_ITEMS).map(function(r){const post=postById[str_(r.postId)];return {id:str_(r.commentId),postId:str_(r.postId),text:str_(r.text),createdAt:num_(r.createdAt),updatedAt:num_(r.updatedAt),postText:post?str_(post.text).slice(0,160):'',postNickname:post?str_(post.nickname):''};});
  return {ok:true,version:SOCIAL_VERSION,profile:{nickname:me.nickname,createdAt:num_(profile.createdAt)},stats:{postCount:myPosts.length,commentCount:myComments.length,supportReceived:supports.filter(function(r){return myIds.has(str_(r.postId));}).length},posts:posts,comments:comments};
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
  sh.getRange(profile._row,1).setValue(''); sh.getRange(profile._row,2).setValue(''); sh.getRange(profile._row,3).setValue(''); sh.getRange(profile._row,5).setValue(now); sh.getRange(profile._row,6).setValue('deleted');
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
  const post=rows_(SOCIAL_SHEETS.posts).find(function(r){return str_(r.postId)===postId&&str_(r.status)==='active';}); if(!post)return {ok:false,error:'NOT_FOUND'};
  const all=rows_(SOCIAL_SHEETS.comments).filter(function(r){return str_(r.postId)===postId&&str_(r.status)==='active';}).sort(function(a,b){return num_(a.createdAt)-num_(b.createdAt);});
  const items=all.slice(-MAX_COMMENT_ITEMS).map(function(r){return {id:str_(r.commentId),postId:postId,userId:str_(r.userId),nickname:str_(r.nickname),text:str_(r.text),createdAt:num_(r.createdAt),updatedAt:num_(r.updatedAt),mine:str_(r.userId)===me.userId};}); return {ok:true,version:SOCIAL_VERSION,items:items,commentCount:all.length};
}

function commentCreate_(b){
  const me=auth_(b.userId,b.token); if(!me.ok)return me; const postId=cleanPostId_(b.postId),text=validCommentText_(b.text); if(!postId||!text)return {ok:false,error:'INVALID_COMMENT'};
  const post=rows_(SOCIAL_SHEETS.posts).find(function(r){return str_(r.postId)===postId&&str_(r.status)==='active';}); if(!post)return {ok:false,error:'NOT_FOUND'};
  const now=Date.now(); const mine=rows_(SOCIAL_SHEETS.comments).filter(function(r){return str_(r.userId)===me.userId;});
  if(mine.some(function(r){return now-num_(r.createdAt)<MIN_COMMENT_INTERVAL_MS;}))return {ok:false,error:'COMMENT_TOO_FAST',message:'댓글은 잠시 후 다시 남겨주세요.'};
  const day=Utilities.formatDate(new Date(now),SOCIAL_TIME_ZONE,'yyyy-MM-dd'); const todayCount=mine.filter(function(r){const ts=num_(r.createdAt);return ts>0&&Utilities.formatDate(new Date(ts),SOCIAL_TIME_ZONE,'yyyy-MM-dd')===day;}).length;
  if(todayCount>=MAX_COMMENTS_PER_DAY)return {ok:false,error:'COMMENT_DAILY_LIMIT',message:'오늘 남길 수 있는 댓글 수를 넘었습니다.'};
  const id='c_'+Utilities.getUuid().replace(/-/g,''); sheet_(SOCIAL_SHEETS.comments).appendRow([id,postId,me.userId,cellText_(me.nickname),cellText_(text),now,now,'active']);
  const count=rows_(SOCIAL_SHEETS.comments).filter(function(r){return str_(r.postId)===postId&&str_(r.status)==='active';}).length; return {ok:true,id:id,commentCount:count};
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
  const sh=sheet_(SOCIAL_SHEETS.supports),supportRows=rows_(SOCIAL_SHEETS.supports),old=supportRows.find(function(r){return str_(r.postId)===id&&str_(r.userId)===me.userId;}); let on=true;
  if(old){sh.deleteRow(old._row);on=false;}else sh.appendRow([id,me.userId,Date.now()]);
  const count=rows_(SOCIAL_SHEETS.supports).filter(function(r){return str_(r.postId)===id;}).length; sheet_(SOCIAL_SHEETS.posts).getRange(post._row,8).setValue(count); return {ok:true,supported:on,supportCount:count};
}

function report_(b){
  const me=auth_(b.userId,b.token); if(!me.ok)return me; cleanupReports_();
  const id=cleanPostId_(b.postId),reason=str_(b.reason).trim(); if(!id||REPORT_REASONS.indexOf(reason)<0)return {ok:false,error:'INVALID_REPORT'};
  const post=rows_(SOCIAL_SHEETS.posts).find(function(x){return str_(x.postId)===id&&str_(x.status)==='active';}); if(!post)return {ok:false,error:'NOT_FOUND'}; if(str_(post.userId)===me.userId)return {ok:false,error:'OWN_REPORT'};
  const old=rows_(SOCIAL_SHEETS.reports).find(function(r){return str_(r.postId)===id&&str_(r.reporterId)===me.userId;}); if(old)return {ok:true,duplicate:true};
  sheet_(SOCIAL_SHEETS.reports).appendRow(['r_'+Utilities.getUuid().replace(/-/g,''),id,me.userId,str_(post.userId),reason,Date.now()]); return {ok:true};
}

function auth_(userId,token,skipEnsure){
  if(!skipEnsure) ensureSheets_(); const uid=validUserId_(userId),tok=validToken_(token); if(!uid||!tok)return {ok:false,error:'AUTH'};
  const p=rows_(SOCIAL_SHEETS.profiles).find(function(r){return str_(r.userId)===uid&&str_(r.status)==='active';}); if(!p||str_(p.tokenHash)!==hash_(tok))return {ok:false,error:'AUTH'};
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
function sheet_(name){const sh=SpreadsheetApp.getActiveSpreadsheet().getSheetByName(name);if(!sh)throw new Error('MISSING_SHEET:'+name);return sh;}
function rows_(name){const sh=sheet_(name),last=sh.getLastRow(),heads=SOCIAL_HEADERS[name];if(last<2)return [];return sh.getRange(2,1,last-1,heads.length).getValues().map(function(a,i){const o={_row:i+2};heads.forEach(function(h,j){const v=a[j];o[h]=typeof v==='string'?uncellText_(v):v;});return o;});}
