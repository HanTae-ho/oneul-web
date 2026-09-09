/*
 * 오늘 한 걸음 V9.0 — 소셜 전용 Apps Script
 *
 * 중요:
 * - 이 프로젝트는 자원시트/회복기록과 분리한 전용 Google Spreadsheet에 연결합니다.
 * - 감정·충동·HALT·다시 시작·복약·자가점검 등 ohg.v1 회복기록을 받지 않습니다.
 * - 공개 소셜에 필요한 익명 ID·닉네임·게시글·응원·신고만 저장합니다.
 *
 * 처음 한 번:
 * 1) 빈 Google Spreadsheet를 새로 만들고 확장 프로그램 → Apps Script
 * 2) 이 파일 전체를 붙여넣고 SOCIAL_SETUP 실행
 * 3) 배포 → 새 배포 → 웹 앱 / 실행 사용자: 나 / 액세스: 모든 사용자
 * 4) /exec 주소를 오늘 한 걸음 자원시트 [설정]의 SOCIAL_URL 값으로 넣고
 *    기존 자원시트 배포를 '새 버전'으로 갱신합니다.
 */

const SOCIAL_VERSION = 'V9.0-social-1';
const SOCIAL_SHEETS = {
  profiles: 'Profiles',
  posts: 'Posts',
  supports: 'Supports',
  reports: 'Reports'
};
const SOCIAL_HEADERS = {
  Profiles: ['userId','nickname','tokenHash','createdAt','updatedAt','status'],
  Posts: ['postId','userId','nickname','text','createdAt','updatedAt','status','supportCount'],
  Supports: ['postId','userId','createdAt'],
  Reports: ['reportId','postId','reporterId','reportedUserId','reason','createdAt']
};
const REPORT_REASONS = ['개인정보 노출','비난·괴롭힘','광고·홍보','위험한 사용·도박 정보','기타'];
const RESERVED_NICKS = ['관리자','운영자','오늘한걸음','오늘 한 걸음','마음프로'];

function SOCIAL_SETUP(){
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if(!ss) throw new Error('전용 Google Spreadsheet에 연결된 Apps Script에서 실행해주세요.');
  Object.keys(SOCIAL_HEADERS).forEach(name => {
    let sh = ss.getSheetByName(name);
    if(!sh) sh = ss.insertSheet(name);
    const heads = SOCIAL_HEADERS[name];
    if(sh.getLastRow() === 0) sh.getRange(1,1,1,heads.length).setValues([heads]);
    else {
      const cur = sh.getRange(1,1,1,heads.length).getValues()[0].map(String);
      if(cur.join('|') !== heads.join('|')) throw new Error(name+' 시트 1행 헤더가 예상 형식과 다릅니다.');
    }
    sh.setFrozenRows(1);
  });
  return 'SOCIAL_SETUP 완료 · '+SOCIAL_VERSION;
}

function SOCIAL_CHECK(){
  SOCIAL_SETUP();
  return JSON.stringify({ok:true,version:SOCIAL_VERSION,spreadsheet:SpreadsheetApp.getActiveSpreadsheet().getName()});
}

function doGet(e){
  try{
    const a = str_((e && e.parameter && e.parameter.action) || 'health');
    if(a === 'health') return json_({ok:true,version:SOCIAL_VERSION});
    if(a === 'feed') return json_(feed_(e.parameter || {}));
    return json_({ok:false,error:'UNKNOWN_ACTION'});
  }catch(err){
    return json_({ok:false,error:'SERVER_ERROR',message:String(err && err.message || err)});
  }
}

function doPost(e){
  try{
    const body = parseBody_(e);
    const action = str_(body.action);
    if(!action) return json_({ok:false,error:'ACTION_REQUIRED'});
    const lock = LockService.getScriptLock();
    lock.waitLock(15000);
    try{
      if(action === 'profile') return json_(profile_(body));
      if(action === 'postCreate') return json_(postCreate_(body));
      if(action === 'postEdit') return json_(postEdit_(body));
      if(action === 'postDelete') return json_(postDelete_(body));
      if(action === 'supportToggle') return json_(supportToggle_(body));
      if(action === 'report') return json_(report_(body));
      return json_({ok:false,error:'UNKNOWN_ACTION'});
    } finally { lock.releaseLock(); }
  }catch(err){
    return json_({ok:false,error:'SERVER_ERROR',message:String(err && err.message || err)});
  }
}

function feed_(p){
  SOCIAL_SETUP();
  const requester = cleanId_(p.userId || '');
  const sort = str_(p.sort) === 'support' ? 'support' : 'latest';
  const posts = rows_(SOCIAL_SHEETS.posts).filter(r => str_(r.status) === 'active');
  const supports = rows_(SOCIAL_SHEETS.supports);
  const supported = new Set(supports.filter(r => str_(r.userId) === requester).map(r => str_(r.postId)));
  posts.sort((a,b) => sort === 'support'
    ? (num_(b.supportCount)-num_(a.supportCount) || num_(b.createdAt)-num_(a.createdAt))
    : num_(b.createdAt)-num_(a.createdAt));
  const items = posts.slice(0,60).map(r => ({
    id:str_(r.postId),
    userId:str_(r.userId),
    nickname:str_(r.nickname),
    text:str_(r.text),
    createdAt:num_(r.createdAt),
    updatedAt:num_(r.updatedAt),
    supportCount:num_(r.supportCount),
    mine:requester && str_(r.userId) === requester,
    supported:supported.has(str_(r.postId))
  }));
  return {ok:true,version:SOCIAL_VERSION,items:items};
}

function profile_(b){
  SOCIAL_SETUP();
  const userId = validUserId_(b.userId);
  const token = validToken_(b.token);
  const nickname = validNick_(b.nickname);
  if(!userId || !token) return {ok:false,error:'INVALID_PROFILE'};
  if(!nickname) return {ok:false,error:'INVALID_NICKNAME'};
  const sh = sheet_(SOCIAL_SHEETS.profiles), data = rows_(SOCIAL_SHEETS.profiles);
  const found = data.find(r => str_(r.userId) === userId);
  const now = Date.now(), hash = hash_(token);
  if(found){
    if(str_(found.tokenHash) !== hash) return {ok:false,error:'AUTH'};
    const row = found._row;
    sh.getRange(row,2).setValue(nickname);
    sh.getRange(row,5).setValue(now);
    sh.getRange(row,6).setValue('active');
    // 기존 게시물의 표시 닉네임도 함께 갱신합니다.
    const ps = rows_(SOCIAL_SHEETS.posts).filter(r => str_(r.userId) === userId && str_(r.status) === 'active');
    const psh = sheet_(SOCIAL_SHEETS.posts);
    ps.forEach(r => psh.getRange(r._row,3).setValue(nickname));
    return {ok:true,userId:userId,nickname:nickname};
  }
  sh.appendRow([userId,nickname,hash,now,now,'active']);
  return {ok:true,userId:userId,nickname:nickname};
}

function postCreate_(b){
  const me = auth_(b.userId,b.token); if(!me.ok) return me;
  const text = validPostText_(b.text); if(!text) return {ok:false,error:'INVALID_TEXT'};
  const now = Date.now();
  const mine = rows_(SOCIAL_SHEETS.posts).filter(r => str_(r.userId)===me.userId && str_(r.status)==='active');
  if(mine.some(r => now-num_(r.createdAt)<30000)) return {ok:false,error:'TOO_FAST',message:'잠시 후 다시 올려주세요.'};
  const day = Utilities.formatDate(new Date(now), Session.getScriptTimeZone() || 'Asia/Seoul', 'yyyy-MM-dd');
  const todayCount = mine.filter(r => Utilities.formatDate(new Date(num_(r.createdAt)), Session.getScriptTimeZone() || 'Asia/Seoul', 'yyyy-MM-dd')===day).length;
  if(todayCount>=20) return {ok:false,error:'DAILY_LIMIT',message:'오늘 올릴 수 있는 글 수를 넘었습니다.'};
  const id='p_'+Utilities.getUuid().replace(/-/g,'');
  sheet_(SOCIAL_SHEETS.posts).appendRow([id,me.userId,me.nickname,text,now,now,'active',0]);
  return {ok:true,id:id};
}

function postEdit_(b){
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
  const id=cleanPostId_(b.postId), text=validPostText_(b.text);
  if(!id || !text) return {ok:false,error:'INVALID_TEXT'};
  const r=rows_(SOCIAL_SHEETS.posts).find(x=>str_(x.postId)===id && str_(x.status)==='active');
  if(!r) return {ok:false,error:'NOT_FOUND'};
  if(str_(r.userId)!==me.userId) return {ok:false,error:'OWNER'};
  const sh=sheet_(SOCIAL_SHEETS.posts);
  sh.getRange(r._row,4).setValue(text);
  sh.getRange(r._row,6).setValue(Date.now());
  return {ok:true};
}

function postDelete_(b){
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
  const id=cleanPostId_(b.postId); if(!id) return {ok:false,error:'INVALID_ID'};
  const r=rows_(SOCIAL_SHEETS.posts).find(x=>str_(x.postId)===id && str_(x.status)==='active');
  if(!r) return {ok:false,error:'NOT_FOUND'};
  if(str_(r.userId)!==me.userId) return {ok:false,error:'OWNER'};
  const sh=sheet_(SOCIAL_SHEETS.posts);
  sh.getRange(r._row,4).setValue('');
  sh.getRange(r._row,6).setValue(Date.now());
  sh.getRange(r._row,7).setValue('deleted');
  return {ok:true};
}

function supportToggle_(b){
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
  const id=cleanPostId_(b.postId); if(!id) return {ok:false,error:'INVALID_ID'};
  const post=rows_(SOCIAL_SHEETS.posts).find(x=>str_(x.postId)===id && str_(x.status)==='active');
  if(!post) return {ok:false,error:'NOT_FOUND'};
  if(str_(post.userId)===me.userId) return {ok:false,error:'OWN_SUPPORT'};
  const sh=sheet_(SOCIAL_SHEETS.supports), rows=rows_(SOCIAL_SHEETS.supports);
  const old=rows.find(r=>str_(r.postId)===id && str_(r.userId)===me.userId);
  let on=true;
  if(old){ sh.deleteRow(old._row); on=false; }
  else sh.appendRow([id,me.userId,Date.now()]);
  const count=rows_(SOCIAL_SHEETS.supports).filter(r=>str_(r.postId)===id).length;
  sheet_(SOCIAL_SHEETS.posts).getRange(post._row,8).setValue(count);
  return {ok:true,supported:on,supportCount:count};
}

function report_(b){
  const me=auth_(b.userId,b.token); if(!me.ok) return me;
  const id=cleanPostId_(b.postId), reason=str_(b.reason).trim();
  if(!id || REPORT_REASONS.indexOf(reason)<0) return {ok:false,error:'INVALID_REPORT'};
  const post=rows_(SOCIAL_SHEETS.posts).find(x=>str_(x.postId)===id && str_(x.status)==='active');
  if(!post) return {ok:false,error:'NOT_FOUND'};
  if(str_(post.userId)===me.userId) return {ok:false,error:'OWN_REPORT'};
  const old=rows_(SOCIAL_SHEETS.reports).find(r=>str_(r.postId)===id && str_(r.reporterId)===me.userId);
  if(old) return {ok:true,duplicate:true};
  sheet_(SOCIAL_SHEETS.reports).appendRow(['r_'+Utilities.getUuid().replace(/-/g,''),id,me.userId,str_(post.userId),reason,Date.now()]);
  return {ok:true};
}

function auth_(userId,token){
  const uid=validUserId_(userId), tok=validToken_(token);
  if(!uid||!tok) return {ok:false,error:'AUTH'};
  const p=rows_(SOCIAL_SHEETS.profiles).find(r=>str_(r.userId)===uid && str_(r.status)==='active');
  if(!p || str_(p.tokenHash)!==hash_(tok)) return {ok:false,error:'AUTH'};
  return {ok:true,userId:uid,nickname:str_(p.nickname)};
}

function validNick_(v){
  const n=str_(v).replace(/\s+/g,' ').trim();
  if(n.length<2 || n.length>12) return '';
  if(!/^[가-힣A-Za-z0-9 _-]+$/.test(n)) return '';
  if(RESERVED_NICKS.some(x=>x.replace(/\s/g,'')===n.replace(/\s/g,''))) return '';
  return n;
}
function validPostText_(v){ const s=str_(v).trim(); return s && s.length<=500 ? s : ''; }
function validUserId_(v){ const s=str_(v); return /^u_[A-Za-z0-9-]{16,80}$/.test(s)?s:''; }
function validToken_(v){ const s=str_(v); return /^[A-Fa-f0-9]{48,160}$/.test(s)?s:''; }
function cleanPostId_(v){ const s=str_(v); return /^p_[A-Za-z0-9]{20,80}$/.test(s)?s:''; }
function cleanId_(v){ const s=str_(v); return /^u_[A-Za-z0-9-]{16,80}$/.test(s)?s:''; }
function str_(v){ return v==null?'':String(v); }
function num_(v){ const n=Number(v); return isFinite(n)?n:0; }
function hash_(v){ return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,str_(v),Utilities.Charset.UTF_8).map(b=>('0'+((b<0?b+256:b).toString(16))).slice(-2)).join(''); }
function parseBody_(e){ try{return JSON.parse((e&&e.postData&&e.postData.contents)||'{}');}catch(_){return {};} }
function json_(o){ return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function sheet_(name){ const sh=SpreadsheetApp.getActiveSpreadsheet().getSheetByName(name); if(!sh) throw new Error(name+' 시트가 없습니다. SOCIAL_SETUP을 실행하세요.'); return sh; }
function rows_(name){
  const sh=sheet_(name), last=sh.getLastRow(), heads=SOCIAL_HEADERS[name];
  if(last<2) return [];
  return sh.getRange(2,1,last-1,heads.length).getValues().map((a,i)=>{
    const o={_row:i+2}; heads.forEach((h,j)=>o[h]=a[j]); return o;
  });
}
