from pathlib import Path


def one(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    return text.replace(old, new, 1)

p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = one(s, "const BUILD='V9.0.5';", "const BUILD='V9.0.6';", 'BUILD')
s = one(s,
"btn.textContent=show?'미래의 나에게 접기':'미래의 나에게 바로보기';",
"btn.textContent=show?'초심 접기':'초심 보기';",
'urge runtime label')

s = one(s,
".social-status{font-size:12px;color:var(--dim);margin:7px 0 11px}.social-rule{font-size:12px;line-height:1.65;color:var(--dim)}.social-rule b{color:var(--tx)}",
".social-status{font-size:12px;color:var(--dim);margin:7px 0 11px}.social-rule{font-size:12px;line-height:1.65;color:var(--dim)}.social-rule b{color:var(--tx)}.social-fold summary{cursor:pointer;list-style:none;font-weight:700;color:var(--tx);outline:none}.social-fold summary::-webkit-details-marker{display:none}.social-fold summary::after{content:'⌄';float:right;color:var(--faint);font-size:16px;line-height:1.2}.social-fold[open] summary::after{content:'⌃'}.social-fold-body{margin-top:7px}.social-safety-fold:not([open]){background:var(--panel);color:var(--dim);border:1px solid var(--line)}",
'social fold css')

old_refresh = """async function socialRefresh(force){
  if(!SO.profile||socialState.loading) return;
  if(!socialEndpoint()){ socialState.error=''; socialState.items=[]; socialState.loaded=true; drawSocial(); return; }
  socialState.loading=true; socialState.error=''; if(force) socialState.loaded=false; drawSocial();
  try{ await socialRegister(); socialState.items=await socialReadFeed(); socialState.loaded=true; }
  catch(e){ socialState.error=socialApiMessage(e); socialState.loaded=true; }
  finally{ socialState.loading=false; drawSocial(); }
}
function socialResetFeed(){ socialState.items=[]; socialState.loaded=false; socialState.error=''; }
"""
new_refresh = """async function socialRefresh(force,quiet){
  if(!SO.profile||socialState.loading) return;
  if(!socialEndpoint()){ socialState.error=''; socialState.items=[]; socialState.loaded=true; drawSocial(); return; }
  socialState.loading=true; if(!quiet) socialState.error=''; if(force&&!socialState.items.length) socialState.loaded=false; drawSocial();
  try{ await socialRegister(); socialState.items=await socialReadFeed(); socialState.loaded=true; }
  catch(e){ if(!quiet) socialState.error=socialApiMessage(e); socialState.loaded=true; }
  finally{ socialState.loading=false; drawSocial(); }
}
function socialResetFeed(){ socialState.items=[]; socialState.loaded=false; socialState.error=''; }
let socialGuideAutoUntil=0;
function socialGuideAutoOpen(){
  if(socialGuideAutoUntil>Date.now()) return true;
  try{
    if(!sessionStorage.getItem('ohg.social.guide.v1')){
      sessionStorage.setItem('ohg.social.guide.v1','1');
      socialGuideAutoUntil=Date.now()+2800;
      return true;
    }
  }catch(_){ }
  return false;
}
function socialAutoFold(id,delay){
  setTimeout(()=>{const x=$('#'+id);if(x&&x.open)x.open=false;},Number(delay||2400));
}
"""
s = one(s, old_refresh, new_refresh, 'social refresh')

s = one(s,
"  const endpoint=socialEndpoint();\n  let html='<button class=\"card social-compose\" id=\"social-compose\" type=\"button\"><span class=\"social-avatar\">'+socialInitial(p.nickname)+'</span><span class=\"b\"><b>오늘의 한 걸음 나누기</b><span>오늘 한 회복 행동이나 마음을 짧게 남겨보세요</span></span><span class=\"social-plus\">+</span></button>';\n  html+='<div class=\"card tight social-rule\"><b>소셜 이용 안내</b><br>실명·전화번호·주소·병원명처럼 나를 알아볼 수 있는 정보는 적지 않는 것을 권합니다. 개인 회복기록은 자동으로 붙지 않습니다. 생명이나 신체가 위급한 상황은 소셜보다 109·112·119 같은 즉시 도움을 먼저 이용하세요.</div>';",
"  const endpoint=socialEndpoint(),guideOpen=socialGuideAutoOpen();\n  let html='<button class=\"card social-compose\" id=\"social-compose\" type=\"button\"><span class=\"social-avatar\">'+socialInitial(p.nickname)+'</span><span class=\"b\"><b>오늘의 한 걸음 나누기</b><span>오늘 한 회복 행동이나 마음을 짧게 남겨보세요</span></span><span class=\"social-plus\">+</span></button>';\n  html+='<details class=\"card tight social-rule social-fold\" id=\"social-rule-fold\" '+(guideOpen?'open':'')+'><summary>소셜 이용 안내</summary><div class=\"social-fold-body\">실명·전화번호·주소·병원명처럼 나를 알아볼 수 있는 정보는 적지 않는 것을 권합니다. 개인 회복기록은 자동으로 붙지 않습니다. 생명이나 신체가 위급한 상황은 소셜보다 109·112·119 같은 즉시 도움을 먼저 이용하세요.</div></details>';",
'social guide fold')

old_load = """  if(endpoint){
    if(socialState.loading) html+='<div class=\"empty\">소셜 피드를 불러오는 중입니다.</div>';
    else if(socialState.loaded){
      const rows=socialVisibleItems();
      html+=rows.length?'<div id=\"social-feed\">'+rows.map(socialPostHtml).join('')+'</div>':'<div class=\"empty\">아직 올라온 글이 없습니다.<br>첫 번째 오늘의 한 걸음을 남겨보세요.</div>';
    }else html+='<div class=\"empty\">피드를 불러올 준비를 하고 있습니다.</div>';
  }
  body.innerHTML=html;
"""
new_load = """  if(endpoint){
    if(socialState.loaded){
      const rows=socialVisibleItems();
      html+=rows.length?'<div id=\"social-feed\">'+rows.map(socialPostHtml).join('')+'</div>':'<div class=\"empty\">아직 올라온 글이 없습니다.<br>첫 번째 오늘의 한 걸음을 남겨보세요.</div>';
      if(socialState.loading) html+='<div class=\"social-status cen\">새 글을 확인하는 중입니다.</div>';
    }else if(socialState.loading) html+='<div class=\"empty\">소셜 피드를 불러오는 중입니다.</div>';
    else html+='<div class=\"empty\">피드를 불러올 준비를 하고 있습니다.</div>';
  }
  body.innerHTML=html;
  if(guideOpen) socialAutoFold('social-rule-fold',2800);
"""
s = one(s, old_load, new_load, 'social loading preserve')

old_compose = """  modal('<h2>'+(edit?'내 글 수정':'오늘의 한 걸음 나누기')+'</h2><p class=\"muted\" style=\"margin:5px 0 11px\">오늘 내가 한 회복 행동이나 지금의 마음을 나눠보세요. 개인 회복기록은 자동으로 가져오지 않습니다.</p><textarea id=\"social-post-text\" maxlength=\"500\" rows=\"6\" placeholder=\"예: 오늘 모임에 다녀왔습니다. 가기 싫었지만 한 걸음은 했습니다.\">'+esc(text)+'</textarea><div class=\"social-char\" id=\"social-char\">'+text.length+' / 500</div><div class=\"note w\" style=\"margin-top:11px\">실명·연락처·주소 같은 개인정보, 다른 사람을 알아볼 수 있는 정보, 술·약물 구매나 도박 실행을 돕는 정보는 올리지 마세요. 급하게 죽고 싶은 마음이나 신체 위험이 있다면 게시글보다 즉시 도움 연결이 먼저입니다.</div><button class=\"btn\" id=\"social-post-send\" style=\"margin-top:12px\">'+(edit?'수정 저장':'게시하기')+'</button><div style=\"height:8px\"></div><button class=\"btn ghost\" onclick=\"closeModal()\">그만두기</button>');
  const ta=$('#social-post-text'), ch=$('#social-char'); ta.oninput=()=>ch.textContent=ta.value.length+' / 500';
"""
new_compose = """  modal('<h2>'+(edit?'내 글 수정':'오늘의 한 걸음 나누기')+'</h2><p class=\"muted\" style=\"margin:5px 0 11px\">오늘 내가 한 회복 행동이나 지금의 마음을 나눠보세요. 개인 회복기록은 자동으로 가져오지 않습니다.</p><textarea id=\"social-post-text\" maxlength=\"500\" rows=\"6\" placeholder=\"예: 오늘 모임에 다녀왔습니다. 가기 싫었지만 한 걸음은 했습니다.\">'+esc(text)+'</textarea><div class=\"social-char\" id=\"social-char\">'+text.length+' / 500</div><details class=\"note w social-fold social-safety-fold\" id=\"social-compose-safety\" style=\"margin-top:11px\" open><summary>안전하게 나누기</summary><div class=\"social-fold-body\">실명·연락처·주소 같은 개인정보, 다른 사람을 알아볼 수 있는 정보, 술·약물 구매나 도박 실행을 돕는 정보는 올리지 마세요. 급하게 죽고 싶은 마음이나 신체 위험이 있다면 게시글보다 즉시 도움 연결이 먼저입니다.</div></details><button class=\"btn\" id=\"social-post-send\" style=\"margin-top:12px\">'+(edit?'수정 저장':'게시하기')+'</button><div style=\"height:8px\"></div><button class=\"btn ghost\" onclick=\"closeModal()\">그만두기</button>');
  socialAutoFold('social-compose-safety',2200);
  const ta=$('#social-post-text'), ch=$('#social-char'); ta.oninput=()=>ch.textContent=ta.value.length+' / 500';
"""
s = one(s, old_compose, new_compose, 'compose safety fold')

old_submit = """  try{
    const a=socialAuth();
    await socialWrite(post?'postEdit':'postCreate',Object.assign({},a,post?{postId:post.id,text:text}:{text:text}));
    closeModal(); socialResetFeed(); toast(post?'글을 수정했습니다.':'오늘의 한 걸음을 나눴습니다.'); socialRefresh(true);
  }catch(e){toast(socialApiMessage(e));}
"""
new_submit = """  const send=$('#social-post-send');
  if(send){send.disabled=true;send.textContent=post?'저장 중…':'게시 중…';}
  try{
    const a=socialAuth(),r=await socialWrite(post?'postEdit':'postCreate',Object.assign({},a,post?{postId:post.id,text:text}:{text:text}));
    const now=Date.now();
    if(post){const x=socialFind(post.id);if(x){x.text=text;x.updatedAt=now;}}
    else if(r&&r.id){socialState.items.unshift({id:r.id,userId:a.userId,nickname:(SO.profile&&SO.profile.nickname)||'익명',text:text,createdAt:now,updatedAt:now,supportCount:0,commentCount:0,mine:true,supported:false});}
    socialState.loaded=true;socialState.error='';closeModal();drawSocial();toast(post?'글을 수정했습니다.':'오늘의 한 걸음을 나눴습니다.');setTimeout(()=>socialRefresh(false,true),250);
  }catch(e){if(send){send.disabled=false;send.textContent=post?'수정 저장':'게시하기';}toast(socialApiMessage(e));}
"""
s = one(s, old_submit, new_submit, 'post immediate reflect')

old_comment = """  try{
    const r=await socialWrite('commentCreate',Object.assign({},socialAuth(),{postId:postId,text:text}));
    const x=socialFind(postId); if(x)x.commentCount=Number(r.commentCount||Number(x.commentCount||0)+1);
    toast('댓글을 남겼습니다.'); await socialComments(postId);
  }catch(e){toast(socialCommentApiMessage(e));}
"""
new_comment = """  try{
    const a=socialAuth(),r=await socialWrite('commentCreate',Object.assign({},a,{postId:postId,text:text}));
    const x=socialFind(postId); if(x)x.commentCount=Number(r.commentCount||Number(x.commentCount||0)+1);
    socialCommentState.items.push({id:r.id||('local_'+Date.now()),postId:String(postId),userId:a.userId,nickname:(SO.profile&&SO.profile.nickname)||'익명',text:text,createdAt:Date.now(),updatedAt:Date.now(),mine:true});
    socialCommentState.loading=false;socialCommentState.error='';const ta=$('#social-comment-text');if(ta)ta.value='';const ch=$('#social-comment-char');if(ch)ch.textContent='0 / 300';socialRenderComments();drawSocial();toast('댓글을 남겼습니다.');setTimeout(()=>socialCommentsRefresh(postId,true),250);
  }catch(e){toast(socialCommentApiMessage(e));}
"""
s = one(s, old_comment, new_comment, 'comment immediate reflect')

s = one(s, "async function socialCommentsRefresh(postId){", "async function socialCommentsRefresh(postId,quiet){", 'comment refresh signature')
s = one(s,
"  }catch(e){socialCommentState.loading=false;socialCommentState.error=socialCommentApiMessage(e);socialRenderComments();}\n}\nfunction socialRenderComments(){",
"  }catch(e){socialCommentState.loading=false;if(!quiet){socialCommentState.error=socialCommentApiMessage(e);socialRenderComments();}}\n}\nfunction socialRenderComments(){",
'comment quiet refresh')

old_support = """async function socialSupport(id){
  const x=socialFind(id); if(!x||x.mine)return;
  try{
    const r=await socialWrite('supportToggle',Object.assign({},socialAuth(),{postId:id}));
    x.supported=!!r.supported; x.supportCount=Number(r.supportCount||0); drawSocial();
  }catch(e){toast(socialApiMessage(e));}
}
"""
new_support = """async function socialSupport(id){
  const x=socialFind(id); if(!x||x.mine)return;
  const was=!!x.supported,oldCount=Number(x.supportCount||0);x.supported=!was;x.supportCount=Math.max(0,oldCount+(x.supported?1:-1));drawSocial();
  try{
    const r=await socialWrite('supportToggle',Object.assign({},socialAuth(),{postId:id}));
    x.supported=!!r.supported; x.supportCount=Number(r.supportCount||0); drawSocial();
  }catch(e){x.supported=was;x.supportCount=oldCount;drawSocial();toast(socialApiMessage(e));}
}
"""
s = one(s, old_support, new_support, 'optimistic support')

p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
w=sw.read_text(encoding='utf-8')
w=one(w,"const APP_VERSION = 'V9.0.5';","const APP_VERSION = 'V9.0.6';",'SW version')
w=one(w,"const V = 'ohg-v905-update-flow-r1';","const V = 'ohg-v906-social-speed-r1';",'SW cache')
sw.write_text(w,encoding='utf-8')

srv=Path('social-apps-script.gs')
g=srv.read_text(encoding='utf-8')
g=one(g,"오늘 한 걸음 V9.0.4 — 소셜 전용 Apps Script","오늘 한 걸음 V9.0.6 — 소셜 전용 Apps Script",'social header')
g=one(g,"서버판: V9.0.4-social-1","서버판: V9.0.6-social-1",'social header version')
g=one(g,"const SOCIAL_VERSION = 'V9.0.4-social-1';","const SOCIAL_VERSION = 'V9.0.6-social-1';",'social version')
g=one(g,"const FEED_CACHE_SECONDS = 12;","const FEED_CACHE_SECONDS = 30;",'feed cache ttl')
g=one(g,"try { lock.waitLock(15000); }","try { lock.waitLock(5000); }",'lock wait')
old_c="""  const now=Date.now(); const mine=rows_(SOCIAL_SHEETS.comments).filter(function(r){return str_(r.userId)===me.userId;});
  if(mine.some(function(r){return now-num_(r.createdAt)<MIN_COMMENT_INTERVAL_MS;}))return {ok:false,error:'COMMENT_TOO_FAST',message:'댓글은 잠시 후 다시 남겨주세요.'};
  const day=Utilities.formatDate(new Date(now),SOCIAL_TIME_ZONE,'yyyy-MM-dd'); const todayCount=mine.filter(function(r){const ts=num_(r.createdAt);return ts>0&&Utilities.formatDate(new Date(ts),SOCIAL_TIME_ZONE,'yyyy-MM-dd')===day;}).length;
  if(todayCount>=MAX_COMMENTS_PER_DAY)return {ok:false,error:'COMMENT_DAILY_LIMIT',message:'오늘 남길 수 있는 댓글 수를 넘었습니다.'};
  const id='c_'+Utilities.getUuid().replace(/-/g,''); sheet_(SOCIAL_SHEETS.comments).appendRow([id,postId,me.userId,cellText_(me.nickname),cellText_(text),now,now,'active']);
  const count=rows_(SOCIAL_SHEETS.comments).filter(function(r){return str_(r.postId)===postId&&str_(r.status)==='active';}).length; return {ok:true,id:id,commentCount:count};
"""
new_c="""  const now=Date.now(),commentRows=rows_(SOCIAL_SHEETS.comments),mine=commentRows.filter(function(r){return str_(r.userId)===me.userId;});
  if(mine.some(function(r){return now-num_(r.createdAt)<MIN_COMMENT_INTERVAL_MS;}))return {ok:false,error:'COMMENT_TOO_FAST',message:'댓글은 잠시 후 다시 남겨주세요.'};
  const day=Utilities.formatDate(new Date(now),SOCIAL_TIME_ZONE,'yyyy-MM-dd'); const todayCount=mine.filter(function(r){const ts=num_(r.createdAt);return ts>0&&Utilities.formatDate(new Date(ts),SOCIAL_TIME_ZONE,'yyyy-MM-dd')===day;}).length;
  if(todayCount>=MAX_COMMENTS_PER_DAY)return {ok:false,error:'COMMENT_DAILY_LIMIT',message:'오늘 남길 수 있는 댓글 수를 넘었습니다.'};
  const id='c_'+Utilities.getUuid().replace(/-/g,''),count=commentRows.filter(function(r){return str_(r.postId)===postId&&str_(r.status)==='active';}).length+1; sheet_(SOCIAL_SHEETS.comments).appendRow([id,postId,me.userId,cellText_(me.nickname),cellText_(text),now,now,'active']);
  return {ok:true,id:id,commentCount:count};
"""
g=one(g,old_c,new_c,'comment create scan')
old_sup="""  const sh=sheet_(SOCIAL_SHEETS.supports),supportRows=rows_(SOCIAL_SHEETS.supports),old=supportRows.find(function(r){return str_(r.postId)===id&&str_(r.userId)===me.userId;}); let on=true;
  if(old){sh.deleteRow(old._row);on=false;}else sh.appendRow([id,me.userId,Date.now()]);
  const count=rows_(SOCIAL_SHEETS.supports).filter(function(r){return str_(r.postId)===id;}).length; sheet_(SOCIAL_SHEETS.posts).getRange(post._row,8).setValue(count); return {ok:true,supported:on,supportCount:count};
"""
new_sup="""  const sh=sheet_(SOCIAL_SHEETS.supports),supportRows=rows_(SOCIAL_SHEETS.supports),old=supportRows.find(function(r){return str_(r.postId)===id&&str_(r.userId)===me.userId;}),before=supportRows.filter(function(r){return str_(r.postId)===id;}).length; let on=true,count=before+1;
  if(old){sh.deleteRow(old._row);on=false;count=Math.max(0,before-1);}else sh.appendRow([id,me.userId,Date.now()]);
  sheet_(SOCIAL_SHEETS.posts).getRange(post._row,8).setValue(count); return {ok:true,supported:on,supportCount:count};
"""
g=one(g,old_sup,new_sup,'support scan')
srv.write_text(g,encoding='utf-8')

readme=Path('README.md')
r=readme.read_text(encoding='utf-8')
needle='## V9.0.5 — 탈퇴 단순화 · 초심 보기 · APK 업데이트 안내\n'
block=("## V9.0.6 — 초심 보기 런타임 수정 · 소셜 반응속도 개선\n"
"- `지금 위험해요 → 충동`에서 런타임이 버튼 문구를 다시 덮어쓰던 문제를 고쳐 실제 화면에서도 `초심 보기 / 초심 접기`로 표시합니다.\n"
"- 소셜 이용안내와 글쓰기 안전안내는 처음 잠깐 펼쳐진 뒤 자동으로 접히며, 필요할 때 다시 펼쳐 볼 수 있습니다.\n"
"- 글·댓글은 서버 성공 직후 현재 화면에 즉시 반영하고 전체 피드 재조회는 백그라운드로 돌립니다. 응원은 낙관적 UI로 즉시 반응한 뒤 서버 결과와 맞춥니다.\n"
"- 피드 갱신 중 기존 글을 지우지 않고 유지합니다. 소셜 서버는 피드 캐시를 30초로 늘리고 댓글/응원 쓰기의 중복 시트 읽기를 줄이며 쓰기 lock 대기를 5초로 낮춥니다.\n"
"- `DATA_SCHEMA=6`, `ohg.v1`, `ohg.social.v1`, 닉네임 30일 보호, Android 네이티브 알림/TTS 엔진은 유지합니다.\n\n")
if needle not in r: raise SystemExit('README V9.0.5 heading not found')
r=r.replace(needle,block+needle,1)
readme.write_text(r,encoding='utf-8')

ver=Path('verify.js')
v=ver.read_text(encoding='utf-8')
marker="console.log('V9.0.2 웹 회귀검증 통과');"
checks="""if(!html.includes("btn.textContent=show?'초심 접기':'초심 보기';")) throw new Error('V9.0.6 초심 보기 런타임 문구 누락');
if(!html.includes('id=\\"social-compose-safety\\"')) throw new Error('V9.0.6 소셜 안전안내 폴딩 누락');
if(!html.includes("socialRefresh(false,true)")) throw new Error('V9.0.6 소셜 백그라운드 동기화 누락');
if(!html.includes("const BUILD='V9.0.6';")) throw new Error('V9.0.6 BUILD 불일치');
"""
if checks not in v:
    if marker in v: v=v.replace(marker,checks+marker,1)
    else: v += '\n'+checks
ver.write_text(v,encoding='utf-8')
