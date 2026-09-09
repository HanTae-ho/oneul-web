from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,name):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{name}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

once("const BUILD='V8.5';","const BUILD='V9.0';",'BUILD')

social_store=r'''

/* ══════════ V9.0 · 소셜은 개인 회복기록과 별도 저장 ══════════
   ohg.v1/S에는 닉네임·사용자ID·차단목록을 넣지 않습니다.
   소셜 공개 글 역시 전용 SOCIAL_URL 서버로만 보내고 회복기록은 절대 붙이지 않습니다. */
const SOCIAL_KEY = 'ohg.social.v1';
const SOCIAL_SCHEMA = 1;
const SOCIAL_URL_DEFAULT = '';
function socialBlank(){ return {schema:SOCIAL_SCHEMA,profile:null,blocks:[],hidden:[]}; }
function socialLoad(){
  try{
    const raw=localStorage.getItem(SOCIAL_KEY); if(!raw) return socialBlank();
    const x=Object.assign(socialBlank(),JSON.parse(raw));
    x.schema=SOCIAL_SCHEMA;
    if(!Array.isArray(x.blocks)) x.blocks=[];
    if(!Array.isArray(x.hidden)) x.hidden=[];
    if(x.profile && (typeof x.profile!=='object'||Array.isArray(x.profile))) x.profile=null;
    return x;
  }catch(_){ return socialBlank(); }
}
function socialSave(){ try{localStorage.setItem(SOCIAL_KEY,JSON.stringify(SO));}catch(_){toast('소셜 프로필을 기기에 저장하지 못했습니다.');} }
let SO=socialLoad();
'''
once("const DATA_SCHEMA = 6;","const DATA_SCHEMA = 6;"+social_store,'social store')

css=r'''

  /* ══════════ V9.0 · 소셜 1단계 ══════════ */
  #p-social{padding-bottom:34px}.social-top{display:flex;align-items:center;gap:10px;margin-bottom:13px}
  .social-top h1{margin:0;flex:1}.social-me{display:flex;align-items:center;gap:7px;max-width:52%;padding:8px 10px;border:1px solid var(--line);border-radius:999px;background:var(--panel);color:var(--dim)}
  .social-me b{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:12.5px;color:var(--tx)}
  .social-avatar{width:34px;height:34px;flex:none;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--accbg);color:var(--acc);font-weight:700;font-size:15px;border:1px solid var(--line)}
  .social-welcome{padding:20px 18px;text-align:center}.social-welcome .hero{width:66px;height:66px;margin:2px auto 14px;border-radius:21px;background:var(--accbg);display:flex;align-items:center;justify-content:center;color:var(--acc)}
  .social-welcome .hero svg{width:38px;height:38px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}.social-welcome h2{font-size:20px;color:var(--tx);margin:0 0 8px}.social-welcome p{margin:0;color:var(--dim);line-height:1.72}
  .social-compose{display:flex;align-items:center;gap:11px;width:100%;text-align:left;margin-bottom:12px}.social-compose .b{flex:1}.social-compose .b b{display:block}.social-compose .b span{display:block;color:var(--dim);font-size:12px;margin-top:2px}.social-plus{width:38px;height:38px;border-radius:50%;background:var(--acc);color:var(--panel);display:flex;align-items:center;justify-content:center;font-size:25px;line-height:1;font-weight:300}
  .social-sort{display:flex;gap:7px;margin-bottom:10px}.social-sort button{padding:8px 13px;border-radius:999px;border:1px solid var(--line);color:var(--dim);background:var(--panel);font-size:12.5px}.social-sort button.on{background:var(--accbg);border-color:var(--acc2);color:var(--acc);font-weight:700}
  .social-post{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:14px 15px;margin-bottom:10px}.social-post-head{display:flex;align-items:center;gap:9px}.social-post-head .who{flex:1;min-width:0}.social-post-head .who b{display:block;font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.social-post-head .who span{display:block;font-size:11.5px;color:var(--faint);margin-top:1px}.social-more{width:34px;height:34px;border-radius:50%;color:var(--dim);display:flex;align-items:center;justify-content:center}.social-more:active{background:var(--accbg)}
  .social-more svg,.social-act svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
  .social-text{margin:13px 0 12px;white-space:pre-wrap;word-break:break-word;font-size:15px;line-height:1.72}.social-actions{display:flex;align-items:center;gap:7px;border-top:1px solid var(--line);padding-top:9px}.social-act{display:flex;align-items:center;gap:5px;padding:7px 10px;border-radius:10px;color:var(--dim);font-size:12.5px}.social-act.on{color:var(--acc);background:var(--accbg);font-weight:700}.social-act[disabled]{opacity:.5}
  .social-status{font-size:12px;color:var(--dim);margin:7px 0 11px}.social-rule{font-size:12px;line-height:1.65;color:var(--dim)}.social-rule b{color:var(--tx)}
  .social-block-row{display:flex;align-items:center;gap:9px;padding:9px 0;border-bottom:1px solid var(--line)}.social-block-row:last-child{border-bottom:0}.social-block-row span{flex:1;font-size:13px}
  .social-char{font-size:11px;color:var(--faint);text-align:right;margin-top:5px}.social-error{background:var(--warnbg);color:var(--warn);border-radius:12px;padding:11px 12px;font-size:12.5px;line-height:1.6;margin-bottom:10px}
'''
once('</style>',css+'\n</style>','social css')

social_section=r'''

<!-- ══════════ V9.0 · 소셜 ══════════ -->
<section class="pg" id="p-social">
  <div class="social-top">
    <h1>소셜</h1>
    <button class="social-me hide" id="social-me" type="button"></button>
  </div>
  <div id="social-body"></div>
</section>

'''
once('<!-- ══════════ 헬프 ══════════ -->',social_section+'<!-- ══════════ 헬프 ══════════ -->','social page')

old_nav='''    <!-- 다섯 번째 자리는 소셜 기능을 만들 때 사용합니다. 기록은 내정보 → 내 발자취로 이동했습니다. -->\n    <button data-t="admin" id="tab-admin" class="hide"><svg viewBox="0 0 24 24"><rect x="4.5" y="10.5" width="15" height="10" rx="2"/><path d="M8.5 10.5V7.6a3.5 3.5 0 0 1 7 0v2.9"/></svg>관리자</button>'''
new_nav='''    <button data-t="social"><svg viewBox="0 0 24 24"><circle cx="8.2" cy="8.2" r="3.1"/><circle cx="16.8" cy="9.2" r="2.5"/><path d="M2.8 19.2a5.5 5.5 0 0 1 10.8 0M13.4 17.8a4.6 4.6 0 0 1 7.8 1.4"/></svg>소셜</button>\n    <button data-t="admin" id="tab-admin" class="hide"><svg viewBox="0 0 24 24"><rect x="4.5" y="10.5" width="15" height="10" rx="2"/><path d="M8.5 10.5V7.6a3.5 3.5 0 0 1 7 0v2.9"/></svg>관리자</button>'''
once(old_nav,new_nav,'social nav')
once("const TABBED = ['home','tools','help','ai'];","const TABBED = ['home','tools','help','ai','social'];",'tabbed social')
once("  if(p === 'ai')   drawAI();","  if(p === 'ai')   drawAI();\n  if(p === 'social') drawSocial();",'route social')

social_js=r'''

/* ═══════════════════════════════════════════════════════
   V9.0 · 소셜 1단계
   - 익명 닉네임 + 내부 ID
   - 오늘의 한 걸음 글 / 응원
   - 소유자 구분 · 수정/삭제 · 신고 · 기기 내 차단
   - 댓글/DM/친구/그룹/접속자수는 아직 만들지 않습니다.
   - S/ohg.v1의 회복기록은 이 코드에서 읽거나 전송하지 않습니다.
   ═══════════════════════════════════════════════════════ */
const SOCIAL_REPORT_REASONS=['개인정보 노출','비난·괴롭힘','광고·홍보','위험한 사용·도박 정보','기타'];
let socialState={sort:'latest',items:[],loading:false,loaded:false,error:'',registering:false};

function socialEndpoint(){
  const c=S.res&&S.res.config;
  const raw=c&&(c.socialUrl||c.SOCIAL_URL||c.social_url);
  const u=String(raw||SOCIAL_URL_DEFAULT||'').trim();
  return /^https:\/\/script\.google\.com\/macros\/s\//i.test(u)||/^https:\/\/script\.googleusercontent\.com\//i.test(u)?u:'';
}
function socialRandHex(bytes){
  const a=new Uint8Array(bytes);
  if(window.crypto&&crypto.getRandomValues) crypto.getRandomValues(a);
  else for(let i=0;i<a.length;i++) a[i]=Math.floor(Math.random()*256);
  return [...a].map(x=>x.toString(16).padStart(2,'0')).join('');
}
function socialNewId(){
  if(window.crypto&&typeof crypto.randomUUID==='function') return 'u_'+crypto.randomUUID();
  return 'u_'+Date.now().toString(36)+'-'+socialRandHex(12);
}
function socialNick(v){
  const n=String(v||'').replace(/\s+/g,' ').trim();
  if(n.length<2||n.length>12) return '';
  if(!/^[가-힣A-Za-z0-9 _-]+$/.test(n)) return '';
  const compact=n.replace(/\s/g,'');
  if(['관리자','운영자','오늘한걸음','마음프로'].includes(compact)) return '';
  return n;
}
function socialInitial(n){ const x=String(n||'').trim(); return esc(x?x.slice(0,1):'?'); }
function socialSvg(k){
  if(k==='more') return '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/></svg>';
  if(k==='cheer') return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.4S4.4 16 4.4 10.4A4.1 4.1 0 0 1 12 8.1a4.1 4.1 0 0 1 7.6 2.3c0 5.6-7.6 10-7.6 10z"/></svg>';
  return '';
}
function socialTime(t){
  const d=Math.max(0,Date.now()-Number(t||0));
  if(d<60000) return '방금';
  if(d<3600000) return Math.floor(d/60000)+'분 전';
  if(d<86400000) return Math.floor(d/3600000)+'시간 전';
  const x=new Date(Number(t||0));
  return (x.getMonth()+1)+'월 '+x.getDate()+'일';
}
function socialAuth(){ const p=SO.profile||{}; return {userId:p.userId||'',token:p.token||''}; }
function socialApiMessage(e){
  const code=e&&e.socialCode||'';
  if(code==='AUTH') return '소셜 프로필을 확인하지 못했습니다.';
  if(code==='TOO_FAST') return '잠시 후 다시 올려주세요.';
  if(code==='DAILY_LIMIT') return '오늘 올릴 수 있는 글 수를 넘었습니다.';
  if(code==='INVALID_TEXT') return '글 내용을 다시 확인해주세요.';
  if(code==='OWNER') return '내가 작성한 글만 수정할 수 있습니다.';
  return String(e&&e.message||'소셜 서버에 연결하지 못했습니다.');
}
async function socialWrite(action,data){
  const url=socialEndpoint();
  if(!url){ const e=new Error('소셜 서버가 아직 연결되지 않았습니다.'); e.socialCode='CONFIG'; throw e; }
  let r;
  try{
    r=await fetch(url,{method:'POST',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify(Object.assign({action:action},data||{})),cache:'no-store'});
  }catch(_){ throw new Error('소셜 서버에 연결하지 못했습니다.'); }
  if(!r.ok) throw new Error('소셜 서버 응답을 받지 못했습니다.');
  let j; try{j=await r.json();}catch(_){throw new Error('소셜 서버 응답 형식이 올바르지 않습니다.');}
  if(!j||!j.ok){ const e=new Error((j&&j.message)||'요청을 처리하지 못했습니다.'); e.socialCode=(j&&j.error)||''; throw e; }
  return j;
}
async function socialReadFeed(){
  const base=socialEndpoint(); if(!base) throw new Error('소셜 서버가 아직 연결되지 않았습니다.');
  const u=new URL(base); u.searchParams.set('action','feed'); u.searchParams.set('sort',socialState.sort); if(SO.profile&&SO.profile.userId) u.searchParams.set('userId',SO.profile.userId);
  let r; try{r=await fetch(u.href,{cache:'no-store'});}catch(_){throw new Error('소셜 서버에 연결하지 못했습니다.');}
  if(!r.ok) throw new Error('소셜 피드를 불러오지 못했습니다.');
  const j=await r.json(); if(!j||!j.ok) throw new Error('소셜 피드를 불러오지 못했습니다.'); return Array.isArray(j.items)?j.items:[];
}
async function socialRegister(){
  const p=SO.profile, url=socialEndpoint(); if(!p||!url) return false;
  if(p.registeredUrl===url) return true;
  if(socialState.registering) return false;
  socialState.registering=true;
  try{
    await socialWrite('profile',{userId:p.userId,token:p.token,nickname:p.nickname});
    p.registeredUrl=url; socialSave(); return true;
  } finally { socialState.registering=false; }
}
function socialVisibleItems(){
  const blocked=new Set((SO.blocks||[]).map(x=>String(x&&x.userId||x)));
  const hidden=new Set((SO.hidden||[]).map(String));
  return (socialState.items||[]).filter(x=>x&&!blocked.has(String(x.userId||''))&&!hidden.has(String(x.id||'')));
}
async function socialRefresh(force){
  if(!SO.profile||socialState.loading) return;
  if(!socialEndpoint()){ socialState.error=''; socialState.items=[]; socialState.loaded=true; drawSocial(); return; }
  socialState.loading=true; socialState.error=''; if(force) socialState.loaded=false; drawSocial();
  try{ await socialRegister(); socialState.items=await socialReadFeed(); socialState.loaded=true; }
  catch(e){ socialState.error=socialApiMessage(e); socialState.loaded=true; }
  finally{ socialState.loading=false; drawSocial(); }
}
function socialResetFeed(){ socialState.items=[]; socialState.loaded=false; socialState.error=''; }

function drawSocial(){
  const body=$('#social-body'), me=$('#social-me'); if(!body||!me) return;
  const p=SO.profile;
  me.classList.toggle('hide',!p);
  if(p){ me.innerHTML='<span class="social-avatar" style="width:25px;height:25px;font-size:11px">'+socialInitial(p.nickname)+'</span><b>'+esc(p.nickname)+'</b>'; me.onclick=socialProfileModal; }
  if(!p){
    body.innerHTML='<div class="card social-welcome"><div class="hero"><svg viewBox="0 0 24 24"><circle cx="8" cy="8.3" r="3"/><circle cx="16.5" cy="9" r="2.4"/><path d="M3 19a5.2 5.2 0 0 1 10.2 0M13.4 17.8a4.4 4.4 0 0 1 7.5 1.2"/><path d="M10.2 12.6l1.8 1.8 3.2-3.4"/></svg></div><h2>함께 회복하는 공간</h2><p>익명 닉네임으로 오늘의 한 걸음과 회복 경험을 나눌 수 있습니다.<br><b>충동·HALT·복약·자가점검 같은 내 회복기록은 소셜에 자동 공개되지 않습니다.</b></p><button class="btn" id="social-start" style="margin-top:17px">익명 프로필 만들기</button><button class="btn ghost sm" id="social-later" style="margin-top:8px">나중에 하기</button></div>';
    $('#social-start').onclick=socialProfileModal; $('#social-later').onclick=()=>go('home'); return;
  }
  const endpoint=socialEndpoint();
  let html='<button class="card social-compose" id="social-compose" type="button"><span class="social-avatar">'+socialInitial(p.nickname)+'</span><span class="b"><b>오늘의 한 걸음 나누기</b><span>오늘 한 회복 행동이나 마음을 짧게 남겨보세요</span></span><span class="social-plus">+</span></button>';
  html+='<div class="card tight social-rule"><b>소셜 이용 안내</b><br>실명·전화번호·주소·병원명처럼 나를 알아볼 수 있는 정보는 적지 않는 것을 권합니다. 개인 회복기록은 자동으로 붙지 않습니다. 생명이나 신체가 위급한 상황은 소셜보다 109·112·119 같은 즉시 도움을 먼저 이용하세요.</div>';
  if(!endpoint) html+='<div class="social-error"><b>소셜 서버 연결 준비 중</b><br>익명 프로필은 이 기기에 만들어졌습니다. 전용 SOCIAL_URL이 연결되면 같은 프로필로 공개 피드를 사용할 수 있습니다.</div>';
  else html+='<div class="social-sort"><button data-social-sort="latest" class="'+(socialState.sort==='latest'?'on':'')+'">최신</button><button data-social-sort="support" class="'+(socialState.sort==='support'?'on':'')+'">응원 많은 글</button><button id="social-refresh" style="margin-left:auto">새로고침</button></div>';
  if(socialState.error) html+='<div class="social-error">'+esc(socialState.error)+'</div>';
  if(endpoint){
    if(socialState.loading) html+='<div class="empty">소셜 피드를 불러오는 중입니다.</div>';
    else if(socialState.loaded){
      const rows=socialVisibleItems();
      html+=rows.length?'<div id="social-feed">'+rows.map(socialPostHtml).join('')+'</div>':'<div class="empty">아직 올라온 글이 없습니다.<br>첫 번째 오늘의 한 걸음을 남겨보세요.</div>';
    }else html+='<div class="empty">피드를 불러올 준비를 하고 있습니다.</div>';
  }
  body.innerHTML=html;
  $('#social-compose').onclick=()=>endpoint?socialCompose():toast('소셜 서버 연결 후 글을 올릴 수 있습니다.');
  $$('[data-social-sort]').forEach(b=>b.onclick=()=>{socialState.sort=b.dataset.socialSort;socialResetFeed();socialRefresh(true);});
  const rf=$('#social-refresh'); if(rf) rf.onclick=()=>socialRefresh(true);
  $$('[data-social-support]').forEach(b=>b.onclick=()=>socialSupport(b.dataset.socialSupport));
  $$('[data-social-menu]').forEach(b=>b.onclick=()=>socialMenu(b.dataset.socialMenu));
  if(endpoint&&!socialState.loaded&&!socialState.loading) setTimeout(()=>socialRefresh(false),0);
}
function socialPostHtml(x){
  const mine=!!x.mine||!!(SO.profile&&String(x.userId)===String(SO.profile.userId));
  const supportDisabled=mine?' disabled':'';
  return '<article class="social-post"><div class="social-post-head"><span class="social-avatar">'+socialInitial(x.nickname)+'</span><span class="who"><b>'+esc(x.nickname||'익명')+'</b><span>'+esc(socialTime(x.createdAt))+(Number(x.updatedAt)>Number(x.createdAt)+1000?' · 수정됨':'')+'</span></span><button class="social-more" type="button" data-social-menu="'+esc(x.id)+'" aria-label="게시물 메뉴">'+socialSvg('more')+'</button></div><div class="social-text">'+esc(x.text||'')+'</div><div class="social-actions"><button class="social-act'+(x.supported?' on':'')+'" type="button" data-social-support="'+esc(x.id)+'"'+supportDisabled+'>'+socialSvg('cheer')+'<span>'+(x.supported?'응원했어요':'응원')+' '+Number(x.supportCount||0)+'</span></button>'+(mine?'<span class="tiny" style="margin-left:auto">내 글</span>':'')+'</div></article>';
}
function socialProfileModal(){
  const p=SO.profile;
  const blocked=SO.blocks||[];
  modal('<h2>'+(p?'내 소셜 프로필':'익명 프로필 만들기')+'</h2><p class="muted" style="margin:5px 0 13px">실명 대신 소셜에서만 사용할 닉네임입니다. 회복영역·회복일·충동기록은 프로필에 붙지 않습니다.</p><label class="tiny">닉네임 · 2~12자</label><input id="social-nick" maxlength="12" value="'+esc(p&&p.nickname||'')+'" placeholder="닉네임을 입력하세요"><p class="tiny" style="margin:7px 0 13px">한글·영문·숫자·공백·-·_를 사용할 수 있습니다. 관리자·운영자·오늘한걸음·마음프로와 혼동되는 이름은 사용할 수 없습니다.</p><button class="btn" id="social-profile-save">'+(p?'닉네임 저장':'계속하기')+'</button>'+(p?'<div class="sep"></div><p class="tiny">내부 소셜 ID · …'+esc(String(p.userId||'').slice(-8))+'<br>게시물 소유자 확인에만 사용하며 피드 화면에는 표시하지 않습니다.</p><h3 style="margin-top:15px">차단한 사용자</h3><div id="social-block-list">'+(blocked.length?blocked.map((b,i)=>'<div class="social-block-row"><span>'+esc(b.nickname||'익명')+'</span><button class="btn ghost sm" style="width:auto" data-social-unblock="'+i+'">차단 해제</button></div>').join(''):'<p class="tiny">차단한 사용자가 없습니다.</p>')+'</div>':'')+'<div style="height:9px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
  $('#social-profile-save').onclick=()=>{
    const nick=socialNick($('#social-nick').value);
    if(!nick){toast('닉네임은 2~12자로 다시 확인해주세요.');return;}
    if(!SO.profile) SO.profile={userId:socialNewId(),token:socialRandHex(32),nickname:nick,registeredUrl:''};
    else {SO.profile.nickname=nick; SO.profile.registeredUrl='';}
    socialSave(); closeModal(); socialResetFeed(); drawSocial();
  };
  $$('[data-social-unblock]').forEach(b=>b.onclick=()=>{const i=Number(b.dataset.socialUnblock);if(i>=0){SO.blocks.splice(i,1);socialSave();socialProfileModal();if(cur==='social')drawSocial();}});
}
function socialCompose(post){
  const edit=!!post, text=edit?String(post.text||''):'';
  modal('<h2>'+(edit?'내 글 수정':'오늘의 한 걸음 나누기')+'</h2><p class="muted" style="margin:5px 0 11px">오늘 내가 한 회복 행동이나 지금의 마음을 나눠보세요. 개인 회복기록은 자동으로 가져오지 않습니다.</p><textarea id="social-post-text" maxlength="500" rows="6" placeholder="예: 오늘 모임에 다녀왔습니다. 가기 싫었지만 한 걸음은 했습니다.">'+esc(text)+'</textarea><div class="social-char" id="social-char">'+text.length+' / 500</div><div class="note w" style="margin-top:11px">실명·연락처·주소 같은 개인정보, 다른 사람을 알아볼 수 있는 정보, 술·약물 구매나 도박 실행을 돕는 정보는 올리지 마세요. 급하게 죽고 싶은 마음이나 신체 위험이 있다면 게시글보다 즉시 도움 연결이 먼저입니다.</div><button class="btn" id="social-post-send" style="margin-top:12px">'+(edit?'수정 저장':'게시하기')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">그만두기</button>');
  const ta=$('#social-post-text'), ch=$('#social-char'); ta.oninput=()=>ch.textContent=ta.value.length+' / 500';
  $('#social-post-send').onclick=()=>socialSubmitPost(String(ta.value||'').trim(),edit?post:null,false);
}
function socialCrisisText(t){ return /(죽고\s*싶|자살|극단적\s*선택|목숨을\s*끊)/.test(String(t||'')); }
async function socialSubmitPost(text,post,confirmed){
  if(!text||text.length>500){toast('글은 1~500자로 작성해주세요.');return;}
  if(socialCrisisText(text)&&!confirmed){
    modal('<h2>지금 안전이 먼저입니다</h2><div class="note b">이 글에는 죽고 싶은 마음과 관련된 표현이 있습니다. 지금 당장 위험하다면 게시글의 답을 기다리지 말고 <b>109</b>, <b>112</b>, <b>119</b> 또는 가까운 응급의료기관에 바로 연결하세요.</div><a class="btn danger" href="tel:109">109 자살예방상담전화</a><button class="btn sec" id="social-crisis-help" style="margin-top:8px">지금 위험해요 열기</button><button class="btn ghost" id="social-crisis-post" style="margin-top:8px">그래도 게시하기</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">그만두기</button>');
    $('#social-crisis-help').onclick=()=>{closeModal();go('panic');};
    $('#social-crisis-post').onclick=()=>socialSubmitPost(text,post,true); return;
  }
  try{
    const a=socialAuth();
    await socialWrite(post?'postEdit':'postCreate',Object.assign({},a,post?{postId:post.id,text:text}:{text:text}));
    closeModal(); socialResetFeed(); toast(post?'글을 수정했습니다.':'오늘의 한 걸음을 나눴습니다.'); socialRefresh(true);
  }catch(e){toast(socialApiMessage(e));}
}
function socialFind(id){ return (socialState.items||[]).find(x=>String(x.id)===String(id)); }
function socialMenu(id){
  const x=socialFind(id); if(!x)return;
  const mine=!!x.mine||!!(SO.profile&&String(x.userId)===String(SO.profile.userId));
  if(mine){
    modal('<h2>내 글</h2><button class="btn sec" id="social-edit">수정</button><button class="btn ghost" id="social-delete" style="margin-top:8px;color:var(--bad);border-color:var(--bad)">삭제</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">닫기</button>');
    $('#social-edit').onclick=()=>socialCompose(x); $('#social-delete').onclick=()=>socialDeleteConfirm(x); return;
  }
  modal('<h2>'+esc(x.nickname||'익명')+'님의 글</h2><button class="btn sec" id="social-report">신고</button><button class="btn ghost" id="social-block" style="margin-top:8px">이 사용자 차단</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">닫기</button>');
  $('#social-report').onclick=()=>socialReport(x); $('#social-block').onclick=()=>socialBlock(x);
}
function socialDeleteConfirm(x){
  modal('<h2>이 글을 삭제할까요?</h2><p class="muted">삭제하면 공개 글 내용이 서버에서 비워지고 되돌릴 수 없습니다.</p><button class="btn danger" id="social-delete-yes">삭제</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">그만두기</button>');
  $('#social-delete-yes').onclick=async()=>{try{await socialWrite('postDelete',Object.assign({},socialAuth(),{postId:x.id}));closeModal();socialResetFeed();toast('글을 삭제했습니다.');socialRefresh(true);}catch(e){toast(socialApiMessage(e));}};
}
function socialBlock(x){
  modal('<h2>이 사용자를 차단할까요?</h2><p class="muted">'+esc(x.nickname||'익명')+'님의 글을 이 기기에서 보이지 않게 합니다. 나중에 내 소셜 프로필에서 차단을 해제할 수 있습니다.</p><button class="btn" id="social-block-yes">차단</button><button class="btn ghost" onclick="closeModal()" style="margin-top:8px">그만두기</button>');
  $('#social-block-yes').onclick=()=>{if(!(SO.blocks||[]).some(b=>String(b.userId)===String(x.userId)))SO.blocks.push({userId:x.userId,nickname:x.nickname||'익명',t:Date.now()});socialSave();closeModal();drawSocial();toast('이 사용자의 글을 숨겼습니다.');};
}
function socialReport(x){
  modal('<h2>이 글을 신고하는 이유</h2><p class="muted" style="margin:5px 0 12px">신고 내용은 운영 확인용으로 소셜 서버에 저장됩니다. 신고 후 이 글은 이 기기에서 바로 숨깁니다.</p><div class="opts">'+SOCIAL_REPORT_REASONS.map((r,i)=>'<button class="opt" data-social-report-reason="'+i+'">'+esc(r)+'</button>').join('')+'</div><div style="height:10px"></div><button class="btn ghost" onclick="closeModal()">그만두기</button>');
  $$('[data-social-report-reason]').forEach(b=>b.onclick=async()=>{const reason=SOCIAL_REPORT_REASONS[Number(b.dataset.socialReportReason)];try{await socialWrite('report',Object.assign({},socialAuth(),{postId:x.id,reason:reason}));if(!SO.hidden.includes(x.id))SO.hidden.push(x.id);socialSave();closeModal();drawSocial();toast('신고했습니다. 이 글을 숨겼습니다.');}catch(e){toast(socialApiMessage(e));}});
}
async function socialSupport(id){
  const x=socialFind(id); if(!x||x.mine)return;
  try{
    const r=await socialWrite('supportToggle',Object.assign({},socialAuth(),{postId:id}));
    x.supported=!!r.supported; x.supportCount=Number(r.supportCount||0); drawSocial();
  }catch(e){toast(socialApiMessage(e));}
}
'''

anchor='/* ══════════ 모임 찾기 ══════════'
once(anchor,social_js+'\n\n'+anchor,'social js')

# 자원 설정이 앱을 연 뒤 갱신되는 경우 소셜도 즉시 연결 상태를 다시 그립니다.
once("      if(cur === 'me')   drawMe();","      if(cur === 'me')   drawMe();\n      if(cur === 'social'){ socialResetFeed(); drawSocial(); }",'resource social refresh')

# 도움말에 소셜 개인정보 원칙을 짧게 추가합니다.
manual_anchor='''    <details class="faq"><summary>13. Android 설치 앱 — 알림과 음성</summary>'''
social_faq='''    <details class="faq"><summary>13. 소셜 — 익명으로 오늘의 한 걸음 나누기</summary><div class="faq-a">\n      <p>소셜은 <b>익명 닉네임과 별도 내부 ID</b>를 사용합니다. 내 회복일·충동·HALT·복약·자가점검·다시 시작 기록은 게시글이나 프로필에 자동으로 붙지 않습니다.</p>\n      <p style="margin-top:8px">내 글은 수정·삭제할 수 있고, 다른 사용자의 글은 신고하거나 사용자를 차단할 수 있습니다. 차단목록은 이 기기의 소셜 전용 저장공간에만 보관합니다.</p>\n      <p style="margin-top:8px">V9.0에서는 댓글·개인메시지·친구·팔로우·그룹 기능을 제공하지 않습니다. 생명이나 신체가 위급한 상황은 소셜 답변을 기다리지 말고 109·112·119 등 즉시 도움을 이용하세요.</p>\n      <button class="btn ghost sm faq-go" type="button" onclick="go('social')">소셜 열기</button>\n    </div></details>\n\n    <details class="faq"><summary>14. Android 설치 앱 — 알림과 음성</summary>'''
once(manual_anchor,social_faq,'social faq')
once('''    <details class="faq"><summary>14. 기록을 안전하게 보관하는 방법</summary>''','''    <details class="faq"><summary>15. 기록을 안전하게 보관하는 방법</summary>''','faq renumber')

p.write_text(s,encoding='utf-8')

# service worker version/cache only. Android recommendation page remains verified V8.5 until device test.
swp=Path('sw.js'); sw=swp.read_text(encoding='utf-8')
for old,new,name in [
    ("const APP_VERSION = 'V8.5';","const APP_VERSION = 'V9.0';",'sw version'),
    ("const V = 'ohg-v850-summary-install';","const V = 'ohg-v900-social-stage1';",'sw cache')
]:
    if sw.count(old)!=1: raise SystemExit(f'{name}: expected 1, got {sw.count(old)}')
    sw=sw.replace(old,new,1)
swp.write_text(sw,encoding='utf-8')

# 개인정보처리방침: 소셜은 사용자가 선택한 공개정보만 별도 서버로 전송됨을 명시.
q=Path('privacy.html'); x=q.read_text(encoding='utf-8')
if x.count('<span class="ver">V8.5</span>')!=1: raise SystemExit('privacy version')
x=x.replace('<span class="ver">V8.5</span>','<span class="ver">V9.0</span>',1)
needle='<a class="legal-link" href="./legal.html">저작권 · 출처 · 라이선스 안내 보기 →</a>'
social_priv='''<div class="note"><b>소셜 기능 안내</b><br>소셜을 선택해 사용하는 경우 익명 내부 사용자 ID, 사용자가 정한 닉네임, 직접 작성한 게시글, 응원·신고 정보가 <b>소셜 전용 서버</b>에서 처리됩니다. 게시글과 닉네임은 다른 소셜 이용자에게 공개될 수 있습니다. 감정·충동·HALT·복약·자가점검·다시 시작 같은 기기 내 회복기록은 소셜에 자동 첨부하거나 전송하지 않습니다. 사용자 차단목록은 현재 기기의 소셜 전용 저장공간에 보관됩니다.</div>\n'''
if x.count(needle)!=1: raise SystemExit('privacy insert anchor')
x=x.replace(needle,social_priv+needle,1)
q.write_text(x,encoding='utf-8')

q=Path('legal.html'); x=q.read_text(encoding='utf-8')
if x.count('<span class="ver">V8.5</span>')!=1: raise SystemExit('legal version')
q.write_text(x.replace('<span class="ver">V8.5</span>','<span class="ver">V9.0</span>',1),encoding='utf-8')

readme=Path('README.md').read_text(encoding='utf-8')
note='''## V9.0 — 소셜 1단계 · 익명 오늘의 한 걸음\n- 하단의 예약된 다섯 번째 자리를 `소셜` 탭으로 열었습니다. 첫 진입에서는 익명 닉네임만 만들고, 내부 사용자 ID/인증토큰은 소셜 전용 `ohg.social.v1`에만 보관합니다. `ohg.v1`/`DATA_SCHEMA=6` 회복기록과 섞지 않습니다.\n- 전용 SOCIAL_URL이 연결되면 `오늘의 한 걸음` 글 작성, 최신/응원 많은 글 피드, 1종 응원, 내 글 수정·삭제, 다른 사용자 신고·기기 내 차단을 사용할 수 있습니다. 댓글·DM·친구/팔로우·그룹/하이브·접속자 수·전문가/기관 기능은 넣지 않았습니다.\n- 공개 게시글에는 회복일·충동·HALT·복약·자가점검·다시 시작 기록을 자동 첨부하지 않습니다. 소셜 글 작성 시 개인정보를 적지 않도록 안내하고, 자살 관련 명시적 표현이 감지되면 109/112/119 즉시 도움을 먼저 안내합니다.\n- `social-apps-script.gs`는 자원시트와 분리된 전용 Google Spreadsheet에 배포하는 서버 소스입니다. 익명 ID·닉네임·게시글·응원·신고만 처리하며 게시물 소유자 확인은 공개 userId가 아니라 기기 보유 토큰 해시로 검증합니다.\n- Android 정확알림·화면 OFF·부팅 재예약·복약/외래/생활/습관 알림·마음프로/이완 TTS 엔진은 변경하지 않습니다. 설치 안내의 검증 추천 APK는 V9.0 실기기 확인 전까지 V8.5를 유지합니다.\n\n'''
Path('README.md').write_text(note+readme,encoding='utf-8')
