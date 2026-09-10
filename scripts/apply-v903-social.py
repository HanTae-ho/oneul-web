from pathlib import Path

p=Path('social-apps-script.gs')
s=p.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1, found {n}')
    s=s.replace(old,new,1)

def replace_between(start_marker,end_marker,new_text,label):
    global s
    a=s.find(start_marker)
    if a<0: raise SystemExit(f'{label}: start not found')
    b=s.find(end_marker,a+len(start_marker))
    if b<0: raise SystemExit(f'{label}: end not found')
    s=s[:a]+new_text.rstrip()+"\n\n"+s[b:]

one('오늘 한 걸음 V9.0.2 — 소셜 전용 Apps Script','오늘 한 걸음 V9.0.3 — 소셜 전용 Apps Script','header')
one('서버판: V9.0.2-social-4','서버판: V9.0.3-social-1','server header')
one("const SOCIAL_VERSION = 'V9.0.2-social-4';","const SOCIAL_VERSION = 'V9.0.3-social-1';",'version')
one('const REPORT_RETENTION_DAYS = 365;','const REPORT_RETENTION_DAYS = 365;\nconst FEED_CACHE_SECONDS = 12;\nconst SCHEMA_CACHE_SECONDS = 300;\nconst MAX_PROFILE_ACTIVITY_ITEMS = 100;','cache constants')
one(' * ★ 앱에서 부를 때 주의',' * V9.0.3-social-1\n * - 가입 뒤 닉네임은 고정합니다. 변경하려면 소셜 탈퇴 후 새 프로필을 만듭니다.\n * - 내 프로필 페이지용 profileActivity 읽기 API를 추가합니다.\n * - 피드 공개 스냅샷과 내 응원목록을 짧게 캐시하고, 시트 헤더 검증도 캐시해 반복 읽기를 줄입니다.\n * - 쓰기 작업 뒤 관련 피드 캐시를 즉시 무효화합니다.\n *\n * ★ 앱에서 부를 때 주의','changelog')
one("    if(action === 'commentList') return json_(commentList_(body));","    if(action === 'commentList') return json_(commentList_(body));\n    if(action === 'profileActivity') return json_(profileActivity_(body));",'profileActivity route')

# Write routes: centralize cache invalidation after successful mutations.
old_routes="""      if(action === 'profile') return json_(profile_(body));
      if(action === 'profileDelete') return json_(profileDelete_(body));
      if(action === 'postCreate') return json_(postCreate_(body));
      if(action === 'postEdit') return json_(postEdit_(body));
      if(action === 'postDelete') return json_(postDelete_(body));
      if(action === 'commentCreate') return json_(commentCreate_(body));
      if(action === 'commentDelete') return json_(commentDelete_(body));
      if(action === 'commentReport') return json_(commentReport_(body));
      if(action === 'supportToggle') return json_(supportToggle_(body));
      if(action === 'report') return json_(report_(body));
      return json_({ok:false,error:'UNKNOWN_ACTION'});"""
new_routes="""      let result = null;
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
      return json_(result);"""
one(old_routes,new_routes,'write routes')

feed=r'''function feed_(p){
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
}'''
replace_between('function feed_(p){','function profile_(b){',feed,'feed')

profile=r'''function profile_(b){
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
}'''
replace_between('function profile_(b){','function profileDelete_(b){',profile,'profile')

one('function auth_(userId,token){\n  ensureSheets_();','function auth_(userId,token,skipEnsure){\n  if(!skipEnsure) ensureSheets_();','auth skip ensure')
one('function commentList_(b){\n  ensureSheets_(); const me=auth_(b.userId,b.token);','function commentList_(b){\n  ensureSheets_(); const me=auth_(b.userId,b.token,true);','commentList ensure')

old_ensure="function ensureSheets_(){const ss=SpreadsheetApp.getActiveSpreadsheet();if(!ss)throw new Error('NO_SPREADSHEET');Object.keys(SOCIAL_HEADERS).forEach(function(name){const sh=ss.getSheetByName(name);if(!sh)throw new Error('MISSING_SHEET:'+name);const heads=SOCIAL_HEADERS[name];const cur=sh.getRange(1,1,1,heads.length).getValues()[0].map(String);if(cur.join('|')!==heads.join('|'))throw new Error('BAD_HEADER:'+name);});}"
new_ensure="function schemaCacheKey_(){return 'schema:'+SOCIAL_VERSION;}\nfunction ensureSheets_(){const ss=SpreadsheetApp.getActiveSpreadsheet();if(!ss)throw new Error('NO_SPREADSHEET');let cache=null;try{cache=CacheService.getScriptCache();if(cache.get(schemaCacheKey_())==='1')return;}catch(ignore){cache=null;}Object.keys(SOCIAL_HEADERS).forEach(function(name){const sh=ss.getSheetByName(name);if(!sh)throw new Error('MISSING_SHEET:'+name);const heads=SOCIAL_HEADERS[name];const cur=sh.getRange(1,1,1,heads.length).getValues()[0].map(String);if(cur.join('|')!==heads.join('|'))throw new Error('BAD_HEADER:'+name);});if(cache){try{cache.put(schemaCacheKey_(),'1',SCHEMA_CACHE_SECONDS);}catch(ignore){}}}"
one(old_ensure,new_ensure,'ensure cache')
one("  return 'SOCIAL_SETUP 완료 · ' + SOCIAL_VERSION;","  try { CacheService.getScriptCache().put(schemaCacheKey_(),'1',SCHEMA_CACHE_SECONDS); } catch(ignore) {}\n  return 'SOCIAL_SETUP 완료 · ' + SOCIAL_VERSION;",'setup cache')
one("  if(typeof recountSupports_ !== 'function') throw new Error('recountSupports_ 없음');","  if(typeof recountSupports_ !== 'function') throw new Error('recountSupports_ 없음');\n  if(typeof feedPublicSnapshot_ !== 'function') throw new Error('feedPublicSnapshot_ 없음');\n  if(typeof profileActivity_ !== 'function') throw new Error('profileActivity_ 없음');\n  if(typeof invalidateFeedCache_ !== 'function') throw new Error('invalidateFeedCache_ 없음');",'selftest')

p.write_text(s,encoding='utf-8')
print('social V9.0.3 patch PASS')
