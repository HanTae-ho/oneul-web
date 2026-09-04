from pathlib import Path
import re


def replace_once(text, old, new, label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    return text.replace(old,new,1)

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# version/schema
s=replace_once(s,"const BUILD = 'V8.2.1';","const BUILD = 'V8.2.2';",'build')
s=replace_once(s,'const DATA_SCHEMA = 4;','const DATA_SCHEMA = 5;','schema')

# urgent card copy: keep meaning, prevent orphan final character on narrow Android widths
s=replace_once(s,'손떨림·식은땀·경련·환각은 응급상황일 수 있습니다','심한 떨림·경련·환각은 응급 신호일 수 있습니다','urgent-copy')

# tool entry
old='''      <button class="minitool wide" id="tool-qa">\n        <span class="ic" data-ico="speak"></span><b>중독 Q&A</b><span id="tool-qa-s">궁금한 내용을 질문하고 답변 보기</span>\n      </button>\n    </div>\n  </div>\n</section>'''
new='''      <button class="minitool wide" id="tool-qa">\n        <span class="ic" data-ico="speak"></span><b>중독 Q&A</b><span id="tool-qa-s">궁금한 내용을 질문하고 답변 보기</span>\n      </button>\n    </div>\n    <button class="toolcard" id="tool-urge-diary" style="margin-top:9px">\n      <span class="ic" data-ico="wave"></span>\n      <span class="b"><b>충동일기</b><span id="tool-urge-diary-s">언제·무엇 때문에 힘들었는지 돌아보기</span></span>\n      <span class="go">열기</span>\n    </button>\n  </div>\n</section>'''
s=replace_once(s,old,new,'tool-entry')

# dedicated urge diary page before future-self page
anchor='<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->'
page='''<!-- ══════════ 충동일기 V8.2.2 ══════════ -->\n<section class="pg" id="p-urge-diary">\n  <div class="sp" style="margin-bottom:11px">\n    <h1 style="margin:0">충동일기</h1>\n    <button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack('tools')">← 회복도구</button>\n  </div>\n  <div class="note" style="margin-bottom:12px">\n    충동은 특정 시간·상황·촉발요인에서 반복될 수 있습니다. 기록을 모아 내 패턴과 나에게 도움이 된 대처를 찾아봅니다. SMART Recovery의 충동일지 구조를 참고해 앱에 맞게 재구성했으며, <b>내용은 이 기기에만 저장</b>됩니다.\n  </div>\n  <button class="btn sec" id="urge-diary-new">+ 충동 기록하기</button>\n  <div id="urge-diary-draft" style="margin-top:12px"></div>\n  <div id="urge-diary-summary" style="margin-top:12px"></div>\n  <div id="urge-diary-list" style="margin-top:12px"></div>\n</section>\n\n'''
s=replace_once(s,anchor,page+anchor,'urge-diary-page')

# crisis optional tracking: separate place and company, explain autosave
old='''  <button class="btn ghost" id="ur-track-toggle" aria-expanded="false">상황·촉발 기록 (선택) · 눌러서 기록</button>\n  <div id="ur-track" class="hide" style="margin-top:9px">\n    <div class="card">\n      <h3>지금 어떤 상황인가요? <span class="tiny" style="font-weight:400">(선택)</span></h3>\n      <p class="muted" style="margin:-4px 0 11px">해당하는 것을 골라주세요. 정확한 위치는 저장하지 않습니다.</p>\n      <div class="opts" id="ur-ctx"></div>\n      <div class="sep"></div>\n      <h3>무엇이 촉발했나요? <span class="tiny" style="font-weight:400">(선택)</span></h3>\n      <p class="muted" style="margin:-4px 0 11px">여러 개를 골라도 되고, 건너뛰어도 됩니다.</p>\n      <div class="opts" id="ur-trg"></div>\n    </div>\n  </div>'''
new='''  <button class="btn ghost" id="ur-track-toggle" aria-expanded="false">상황·촉발 기록 (선택) · 눌러서 기록</button>\n  <div id="ur-track" class="hide" style="margin-top:9px">\n    <div class="card">\n      <h3>어디에 있었나요? <span class="tiny" style="font-weight:400">(선택)</span></h3>\n      <p class="muted" style="margin:-4px 0 11px">정확한 위치가 아니라 상황 범주만 저장합니다.</p>\n      <div class="opts" id="ur-loc"></div>\n      <div class="sep"></div>\n      <h3>누구와 있었나요? <span class="tiny" style="font-weight:400">(선택)</span></h3>\n      <div class="opts" id="ur-with"></div>\n      <div class="sep"></div>\n      <h3>무엇이 촉발했나요? <span class="tiny" style="font-weight:400">(선택)</span></h3>\n      <p class="muted" style="margin:-4px 0 11px">여러 개를 골라도 되고, 건너뛰어도 됩니다.</p>\n      <div class="opts" id="ur-trg"></div>\n      <p class="tiny" style="margin:11px 0 0">선택 내용은 자동으로 임시저장되며, 충동 대응을 마치면 충동일기에 남습니다.</p>\n    </div>\n  </div>'''
s=replace_once(s,old,new,'crisis-track-ui')

# route: diary stays under Recovery Tools and gets draw function
s=replace_once(s,"p === 'treatment' || p === 'capsule') ? 'tools' : p;","p === 'treatment' || p === 'capsule' || p === 'urge-diary') ? 'tools' : p;",'route-tab')
s=replace_once(s,"  if(p === 'capsule') drawCapsule();\n  if(p === 'schedule') drawScheduleHub();","  if(p === 'capsule') drawCapsule();\n  if(p === 'urge-diary') drawUrgeDiary();\n  if(p === 'schedule') drawScheduleHub();",'route-draw')

# storage: persistent draft is separate from completed urge records
s=replace_once(s,'moods: [], halts: [], urges: [], nights: [], relapses: [], screenings: [],','moods: [], halts: [], urges: [], urgeDraft: null, nights: [], relapses: [], screenings: [],','blank-draft')
s=replace_once(s,'  if(!Array.isArray(s.screenings)) s.screenings = [];','  if(!Array.isArray(s.screenings)) s.screenings = [];\n  if(s.urgeDraft && (typeof s.urgeDraft !== \'object\' || Array.isArray(s.urgeDraft))) s.urgeDraft = null;','migrate-draft')

# replace Trigger Tracking V2 block wholesale, preserving timer marker
pat=r"/\* ══════════ 충동 대응 ══════════ \*/.*?/\* ══════════ 타이머 ══════════ \*/"
m=re.search(pat,s,re.S)
if not m:
    raise SystemExit('urge-block not found')
new_block=r'''/* ══════════ 충동 대응 · 충동일기 V8.2.2 ══════════ */
/* SMART Recovery의 충동일지에서 강조하는 시간·강도·지속·촉발·대처를 기본축으로 두고,
   앱에서는 장소 범주와 동행 상태를 분리했습니다. 정확한 위치정보는 저장하지 않습니다. */
const URGE_LOCATIONS = ['집','직장·학교','이동 중','모임·약속 중','기타'];
const URGE_COMPANY = ['혼자','가족과','친구·동료와','회복 동료와','그 밖의 사람과'];
const URGE_TRIGGERS = ['갈등','외로움','지루함','스트레스','돈 문제','과거 기억','중독 관련 노출','특정 사람'];
const URGE_FEELS = ['불안','외로움','화','슬픔','압박감','지루함','죄책감·수치심','무기력'];
/* DEADs의 지연·벗어나기·수용·주의분산·대체를 사용자 언어로 풀고 기존 앱 대처를 함께 둡니다. */
const URGE_COPES = ['조금 미루기','자리를 벗어나기','충동을 지나가게 두기','주의 돌리기','건강한 행동으로 바꾸기','사람에게 연락하기','호흡하기','도움되는 글 읽기'];
let urgeTrackOpen = false;
let urgeDraftTimer = 0;
let urge = { before:5, after:null, thoughts:[], loc:'', company:'', triggers:[], copes:[], start:0, draftT:0, type:null };

function urgeNewId(){ return 'u'+Date.now().toString(36)+Math.random().toString(36).slice(2,7); }
function urgeLegacyLoc(u){
  if(u && u.loc) return String(u.loc);
  const a=(u && Array.isArray(u.ctx))?u.ctx:[];
  return a.find(x=>['집','직장·학교','이동 중','모임·약속 중'].includes(x)) || '';
}
function urgeLegacyWith(u){
  if(u && u.with) return String(u.with);
  const a=(u && Array.isArray(u.ctx))?u.ctx:[];
  if(a.includes('혼자')) return '혼자';
  if(a.includes('사람들과 함께')) return '사람들과 함께';
  return '';
}
function urgeDraftRecent(){
  const d=S.urgeDraft;
  if(!d || typeof d!=='object') return null;
  const at=Number(d.savedAt||d.t||0);
  if(at && Date.now()-at > 12*60*60*1000){ S.urgeDraft=null; save(); return null; }
  return d;
}
function queueUrgeDraft(){
  clearTimeout(urgeDraftTimer);
  urgeDraftTimer=setTimeout(()=>{
    if(!urge.touched && !urge.start) return;
    S.urgeDraft={
      t:urge.draftT||Date.now(), savedAt:Date.now(), type:urge.type,
      b:urge.before, a:urge.after, start:urge.start||0,
      th:urge.thoughts.slice(), loc:urge.loc||'', with:urge.company||'',
      trg:urge.triggers.slice(), cope:urge.copes.slice()
    };
    save();
    if(cur==='tools') drawTools();
  },180);
}
function clearUrgeDraft(){ clearTimeout(urgeDraftTimer); urgeDraftTimer=0; S.urgeDraft=null; }
function urgeUseCope(x){ if(urge.copes.indexOf(x)<0) urge.copes.push(x); urge.touched=true; queueUrgeDraft(); }

function drawUrgeTrack(){
  const loc=$('#ur-loc'), who=$('#ur-with'), trg=$('#ur-trg');
  if(!loc || !who || !trg) return;
  loc.innerHTML=''; who.innerHTML=''; trg.innerHTML='';
  URGE_LOCATIONS.forEach(x=>{
    const b=el('button','opt'+(urge.loc===x?' on':''),x);
    b.onclick=()=>{ urge.touched=true; urge.loc=urge.loc===x?'':x; queueUrgeDraft(); drawUrgeTrack(); };
    loc.appendChild(b);
  });
  URGE_COMPANY.forEach(x=>{
    const b=el('button','opt'+(urge.company===x?' on':''),x);
    b.onclick=()=>{ urge.touched=true; urge.company=urge.company===x?'':x; queueUrgeDraft(); drawUrgeTrack(); };
    who.appendChild(b);
  });
  URGE_TRIGGERS.forEach(x=>{
    const b=el('button','opt'+(urge.triggers.indexOf(x)>=0?' on':''),x);
    b.onclick=()=>{ urge.touched=true; const i=urge.triggers.indexOf(x); if(i<0) urge.triggers.push(x); else urge.triggers.splice(i,1); queueUrgeDraft(); drawUrgeTrack(); };
    trg.appendChild(b);
  });
}
function setUrgeTrackOpen(open){
  urgeTrackOpen=!!open;
  const box=$('#ur-track'), btn=$('#ur-track-toggle');
  if(box) box.classList.toggle('hide',!urgeTrackOpen);
  if(btn){
    const n=(urge.loc?1:0)+(urge.company?1:0)+urge.triggers.length;
    btn.setAttribute('aria-expanded',urgeTrackOpen?'true':'false');
    btn.textContent=urgeTrackOpen?'상황·촉발 기록 접기':('상황·촉발 기록 (선택)'+(n?' · '+n+'개 임시저장됨':' · 눌러서 기록'));
  }
  if(urgeTrackOpen) drawUrgeTrack();
}

function drawUrge(){
  const d=urgeDraftRecent();
  urge=d ? {
    before:Number(d.b==null?5:d.b), after:d.a==null?null:Number(d.a), thoughts:Array.isArray(d.th)?d.th.slice():[],
    loc:String(d.loc||''), company:String(d.with||''), triggers:Array.isArray(d.trg)?d.trg.slice():[],
    copes:Array.isArray(d.cope)?d.cope.slice():[], start:Number(d.start||0), draftT:Number(d.t||Date.now()),
    touched:true, saved:false, type:d.type || S.types[0] || 'etc'
  } : { before:5, after:null, thoughts:[], loc:'', company:'', triggers:[], copes:[], start:0,
        draftT:Date.now(), touched:false, saved:false, type:S.types[0] || 'etc' };
  $('#ur-r').value=urge.before;
  $('#ur-n').textContent=urge.before;
  const box=$('#ur-th'); box.innerHTML='';
  THOUGHTS.forEach(t=>{
    const b=el('button','opt'+(urge.thoughts.indexOf(t)>=0?' on':''),'"'+t+'"');
    b.onclick=()=>{ urge.touched=true; const i=urge.thoughts.indexOf(t); if(i<0) urge.thoughts.push(t); else urge.thoughts.splice(i,1); queueUrgeDraft(); drawUrge(); };
    box.appendChild(b);
  });
  setUrgeTrackOpen(!!(urge.loc||urge.company||urge.triggers.length));
}
$('#ur-r').oninput=e=>{ urge.before=+e.target.value; urge.touched=true; $('#ur-n').textContent=e.target.value; queueUrgeDraft(); };
$('#ur-start').onclick=()=>{ urge.touched=true; urgeUseCope('조금 미루기'); startTimer(0); };
$('#ur-track-toggle').onclick=()=>setUrgeTrackOpen(!urgeTrackOpen);
$('#ur-help').onclick=()=>{ urgeUseCope('사람에게 연락하기'); saveUrge(); go('help'); };
$('#ur-ok').onclick=()=>{
  const had=urge.touched&&!urge.saved; urge.ok=true; saveUrge();
  if(had) toast('충동일기에 기록했습니다. 잘 넘기셨습니다.');
  go('home');
};

/* ══════════ 타이머 ══════════ */'''
s=s[:m.start()]+new_block+s[m.end():]

# timer interactions also keep the draft current and record helpful strategies
s=replace_once(s,'  if(!urge.start) urge.start = Date.now();\n  $(\'#tm-s\').textContent = st.n;',"  if(!urge.start) urge.start = Date.now();\n  queueUrgeDraft();\n  $('#tm-s').textContent = st.n;",'timer-draft')
s=replace_once(s,"  if(b.classList.contains('hide')){ b.classList.remove('hide'); startBreath(); $('#tm-breath').textContent = '호흡 멈추기'; }","  if(b.classList.contains('hide')){ b.classList.remove('hide'); urgeUseCope('호흡하기'); startBreath(); $('#tm-breath').textContent = '호흡 멈추기'; }",'breath-cope')
s=replace_once(s,"  urge.after = +e.target.value;\n  $('#af-n').textContent = e.target.value;\n  afCmp();","  urge.after = +e.target.value;\n  $('#af-n').textContent = e.target.value;\n  queueUrgeDraft();\n  afCmp();",'after-draft')

# final completed-record save: same S.urges, richer fields, then clear draft
pat=r"function saveUrge\(\)\{.*?\n\}\n\n/\* ══════════ 자기 전 ══════════ \*/"
m=re.search(pat,s,re.S)
if not m:
    raise SystemExit('saveUrge block not found')
new_save=r'''function saveUrge(){
  if(urge.saved) return;
  if(!urge.touched && !urge.start) return;
  urge.saved=true;
  const rec={
    rid:urgeNewId(), t:urge.draftT||urge.start||Date.now(), type:urge.type,
    b:urge.before, a:urge.after==null?urge.before:urge.after,
    sec:urge.start?Math.round((Date.now()-urge.start)/1000):0,
    th:urge.thoughts.slice(), loc:urge.loc||'', with:urge.company||'', trg:urge.triggers.slice(),
    cope:urge.copes.slice(), ok:urge.ok?1:0, src:'crisis'
  };
  S.urges.push(rec);
  clearUrgeDraft();
  save();
  urge.start=0;
}

/* ══════════ 자기 전 ══════════ */'''
s=s[:m.start()]+new_save+s[m.end():]

# reading from urge/timer is also a coping strategy and must not erase draft
s=replace_once(s,"$('#tm-read').onclick = () => openRead('timer');   /* 타이머는 계속 돕습니다 */\n$('#ur-read').onclick = () => openRead('urge');","$('#tm-read').onclick = () => { urgeUseCope('도움되는 글 읽기'); openRead('timer'); };   /* 타이머는 계속 돕습니다 */\n$('#ur-read').onclick = () => { urgeUseCope('도움되는 글 읽기'); openRead('urge'); };",'read-cope')

# tools summary and entry
s=replace_once(s,"  if(caps) caps.textContent=capsuleHas()?'내가 남긴 메시지가 있습니다 · 힘들 때 다시 보기':'회복을 시작한 마음을 남겨두기';","  if(caps) caps.textContent=capsuleHas()?'내가 남긴 메시지가 있습니다 · 힘들 때 다시 보기':'회복을 시작한 마음을 남겨두기';\n  const uds=$('#tool-urge-diary-s'), ud=$('#tool-urge-diary');\n  if(ud) ud.style.display=famMode()?'none':'flex';\n  if(uds) uds.textContent=(S.urges||[]).length ? ('저장된 충동 기록 '+S.urges.length+'건'+(S.urgeDraft?' · 작성 중 1건':'')) : (S.urgeDraft?'작성 중인 기록이 있습니다':'언제·무엇 때문에 힘들었는지 돌아보기');",'tools-summary')

# insert diary renderer/editor after drawTools() and before schedule hub
anchor='''  refreshIcons();\n}\n\nfunction drawScheduleHub(){'''
if s.count(anchor)!=1:
    raise SystemExit(f'drawTools anchor count {s.count(anchor)}')
code=r'''  refreshIcons();
}

$('#tool-urge-diary').onclick=()=>go('urge-diary');

function urgeDiaryTimeInput(ts){
  const d=new Date(ts||Date.now());
  return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate())+'T'+pad(d.getHours())+':'+pad(d.getMinutes());
}
function urgeDiaryDuration(sec){
  sec=Math.max(0,Number(sec||0));
  if(!sec) return '';
  if(sec<60) return Math.round(sec)+'초';
  return Math.round(sec/60)+'분';
}
function urgeDiaryTags(a){ return (Array.isArray(a)?a:[]).filter(Boolean); }
function urgeDiaryLoc(u){ return String((u&&u.loc)||urgeLegacyLoc(u)||''); }
function urgeDiaryWith(u){ return String((u&&u.with)||urgeLegacyWith(u)||''); }
function urgeDiaryRows(){ return (S.urges||[]).slice().sort((a,b)=>Number(b.t||0)-Number(a.t||0)); }
function urgeDiaryTop(rows,getter){
  const c={}; rows.forEach(r=>{ const a=getter(r)||[]; (Array.isArray(a)?a:[a]).filter(Boolean).forEach(x=>c[x]=(c[x]||0)+1); });
  return Object.entries(c).sort((a,b)=>b[1]-a[1])[0]||null;
}
function urgeDiarySummaryText(r){
  const parts=[];
  const loc=urgeDiaryLoc(r), who=urgeDiaryWith(r), trg=urgeDiaryTags(r.trg);
  if(loc) parts.push(loc); if(who) parts.push(who); if(trg.length) parts.push(trg.slice(0,2).join('·'));
  if(r.sec) parts.push(urgeDiaryDuration(r.sec));
  return parts.join(' · ') || '상황 기록 없음';
}
function drawUrgeDiary(){
  if(famMode()){ go('tools'); return; }
  const rows=urgeDiaryRows(), db=$('#urge-diary-draft'), sm=$('#urge-diary-summary'), list=$('#urge-diary-list');
  if(!db||!sm||!list) return;
  const d=urgeDraftRecent();
  if(d){
    const bits=[d.loc,d.with].filter(Boolean).concat(urgeDiaryTags(d.trg).slice(0,2));
    db.innerHTML='<div class="card"><div class="sp"><div><h3 style="margin:0 0 4px">작성 중인 충동 기록</h3><p class="tiny" style="margin:0">'+esc(bits.join(' · ')||'상황을 기록하는 중입니다')+' · 자동 임시저장</p></div><span class="badge">작성 중</span></div><div style="height:10px"></div><button class="btn sec sm" id="urge-diary-resume">이어쓰기</button><div style="height:7px"></div><button class="btn ghost sm" id="urge-diary-discard">임시기록 삭제</button></div>';
    $('#urge-diary-resume').onclick=()=>go('urge');
    $('#urge-diary-discard').onclick=()=>{ S.urgeDraft=null; save(); drawUrgeDiary(); drawTools(); toast('임시기록을 삭제했습니다.'); };
  }else db.innerHTML='';

  if(rows.length>=2){
    const hour=urgeDiaryTop(rows,r=>[new Date(r.t).getHours()+'시 무렵']);
    const trg=urgeDiaryTop(rows,r=>urgeDiaryTags(r.trg));
    const loc=urgeDiaryTop(rows,r=>{const x=urgeDiaryLoc(r);return x?[x]:[];});
    const p=[]; if(hour)p.push('시간 '+hour[0]); if(loc)p.push('장소 '+loc[0]); if(trg)p.push('촉발 '+trg[0]);
    sm.innerHTML='<div class="note"><b>내 패턴 한눈에</b><br>'+esc(p.join(' · '))+'<div class="tiny" style="margin-top:6px">기록이 쌓이면 반복되는 시간·상황·촉발요인이 더 분명해집니다.</div></div>';
  }else sm.innerHTML='';

  if(!rows.length){ list.innerHTML='<div class="empty">아직 저장된 충동 기록이 없습니다.<br>위기 대응을 마치거나 [+ 충동 기록하기]로 남긴 기록이 여기에 모입니다.</div>'; }
  else{
    let h='<div class="card"><h3>저장한 충동 기록 '+rows.length+'건</h3>';
    rows.forEach(r=>{
      const typ=typeOf(r.type||'etc');
      const b=Number(r.b==null?0:r.b), a=Number(r.a==null?b:r.a);
      h+='<button class="ws-saved" style="width:100%;text-align:left" data-urge-rid="'+esc(r.rid||String(r.t))+'"><span class="date">'+esc(ymd(r.t))+'<br>'+esc(new Date(r.t).toLocaleTimeString('ko-KR',{hour:'2-digit',minute:'2-digit'}))+'</span><span class="body"><b>'+esc(typ.n)+' · 강도 '+b+(r.a!=null?' → '+a:'')+'</b><span>'+esc(urgeDiarySummaryText(r))+'</span></span><span class="go">보기</span></button>';
    });
    h+='</div>'; list.innerHTML=h;
    list.querySelectorAll('[data-urge-rid]').forEach(b=>b.onclick=()=>{
      const r=rows.find(x=>(x.rid||String(x.t))===b.dataset.urgeRid); if(r) openUrgeDiaryRecord(r);
    });
  }
  $('#urge-diary-new').onclick=()=>openUrgeDiaryEditor();
  refreshIcons();
}
function openUrgeDiaryRecord(r){
  const typ=typeOf(r.type||'etc'), loc=urgeDiaryLoc(r), who=urgeDiaryWith(r), trg=urgeDiaryTags(r.trg), feel=urgeDiaryTags(r.feel), cope=urgeDiaryTags(r.cope);
  const b=Number(r.b==null?0:r.b), a=Number(r.a==null?b:r.a);
  const rows=[];
  rows.push('<div class="sp" style="padding:5px 0"><span>강도</span><b>'+b+(r.a!=null?' → '+a:'')+'</b></div>');
  if(r.sec) rows.push('<div class="sp" style="padding:5px 0"><span>지속</span><b>'+esc(urgeDiaryDuration(r.sec))+'</b></div>');
  if(loc) rows.push('<div class="sp" style="padding:5px 0"><span>장소</span><b>'+esc(loc)+'</b></div>');
  if(who) rows.push('<div class="sp" style="padding:5px 0"><span>함께</span><b>'+esc(who)+'</b></div>');
  if(trg.length) rows.push('<div class="sp" style="padding:5px 0"><span>촉발</span><b>'+esc(trg.join(' · '))+'</b></div>');
  if((r.th||[]).length || r.thought) rows.push('<div class="sp" style="padding:5px 0;align-items:flex-start"><span>생각</span><b style="max-width:68%;text-align:right">'+esc(r.thought || (r.th||[]).join(' · '))+'</b></div>');
  if(feel.length) rows.push('<div class="sp" style="padding:5px 0"><span>감정</span><b>'+esc(feel.join(' · '))+'</b></div>');
  if(cope.length) rows.push('<div class="sp" style="padding:5px 0;align-items:flex-start"><span>대처</span><b style="max-width:68%;text-align:right">'+esc(cope.join(' · '))+'</b></div>');
  if(r.alt) rows.push('<div class="sp" style="padding:5px 0;align-items:flex-start"><span>대신 한 행동</span><b style="max-width:68%;text-align:right">'+esc(r.alt)+'</b></div>');
  if(r.note) rows.push('<div class="note" style="margin-top:10px">'+esc(r.note)+'</div>');
  modal('<h2>'+esc(typ.n)+' 충동 기록</h2><p class="tiny" style="margin:4px 0 11px">'+esc(new Date(r.t).toLocaleString('ko-KR'))+(r.src==='diary'?' · 직접 작성':' · 위기 대응에서 저장')+'</p><div class="card tight">'+rows.join('')+'</div>'+(r.src==='diary'?'<button class="btn sec" id="urge-diary-edit">수정</button><div style="height:8px"></div>':'')+'<button class="btn danger" id="urge-diary-delete">이 기록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
  const e=$('#urge-diary-edit'); if(e) e.onclick=()=>openUrgeDiaryEditor(r);
  $('#urge-diary-delete').onclick=()=>{
    const key=r.rid||String(r.t);
    modal('<h2>이 충동 기록을 삭제할까요?</h2><p class="muted" style="margin:6px 0 14px">이 기록 한 건만 기기에서 삭제하며 되돌릴 수 없습니다.</p><button class="btn danger" id="urge-delete-yes">삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
    $('#urge-delete-yes').onclick=()=>{ S.urges=(S.urges||[]).filter(x=>(x.rid||String(x.t))!==key); save(); closeModal(); drawUrgeDiary(); drawTools(); toast('삭제했습니다.'); };
  };
}
function urgeEditorChips(items,selected,attr,multi){
  const arr=Array.isArray(selected)?selected:[];
  return items.map(x=>'<button class="opt'+((multi?arr.indexOf(x)>=0:selected===x)?' on':'')+'" '+attr+'="'+esc(x)+'">'+esc(x)+'</button>').join('');
}
function openUrgeDiaryEditor(record){
  const edit=!!record;
  const st={
    rid:edit?(record.rid||urgeNewId()):urgeNewId(), t:edit?Number(record.t||Date.now()):Date.now(),
    type:edit?(record.type||S.types[0]||'etc'):(S.types[0]||'etc'), b:edit?Number(record.b==null?5:record.b):5,
    loc:edit?urgeDiaryLoc(record):'', with:edit?urgeDiaryWith(record):'', trg:edit?urgeDiaryTags(record.trg).slice():[],
    feel:edit?urgeDiaryTags(record.feel).slice():[], cope:edit?urgeDiaryTags(record.cope).slice():[]
  };
  const types=(S.types&&S.types.length?S.types:['etc']);
  modal('<h2>'+(edit?'충동일기 수정':'충동 기록하기')+'</h2><p class="muted" style="margin:5px 0 14px">강도·지속시간·촉발요인과 어떻게 대처했는지 남겨두면 반복되는 패턴을 찾는 데 도움이 됩니다.</p>'+ 
    '<div class="card"><div class="field"><label>일시</label><input id="ud-time" type="datetime-local" value="'+urgeDiaryTimeInput(st.t)+'"></div>'+ 
    '<div class="field"><label>회복영역</label><div class="opts" id="ud-type">'+types.map(k=>{const t=typeOf(k);return '<button class="opt'+(st.type===k?' on':'')+'" data-ud-type="'+esc(k)+'">'+esc(t.n)+'</button>';}).join('')+'</div></div>'+ 
    '<div class="field"><label>충동 강도 <b id="ud-b-n">'+st.b+'</b> / 10</label><input id="ud-b" type="range" min="1" max="10" value="'+st.b+'"></div>'+ 
    '<div class="field"><label>나중 강도 <span class="tiny">(선택)</span></label><input id="ud-a" type="number" min="0" max="10" placeholder="0~10" value="'+(edit&&record.a!=null?Number(record.a):'')+'"></div>'+ 
    '<div class="field"><label>얼마나 지속됐나요? <span class="tiny">(선택)</span></label><input id="ud-min" type="number" min="0" max="1440" placeholder="분" value="'+(edit&&record.sec?Math.round(Number(record.sec)/60):'')+'"></div></div>'+ 
    '<div class="card"><h3>어디에 있었나요?</h3><div class="opts" id="ud-loc">'+urgeEditorChips(URGE_LOCATIONS,st.loc,'data-ud-loc',false)+'</div><div class="sep"></div><h3>누구와 있었나요?</h3><div class="opts" id="ud-with">'+urgeEditorChips(URGE_COMPANY,st.with,'data-ud-with',false)+'</div><div class="sep"></div><h3>무엇이 촉발했나요?</h3><div class="opts" id="ud-trg">'+urgeEditorChips(URGE_TRIGGERS,st.trg,'data-ud-trg',true)+'</div></div>'+ 
    '<div class="card"><h3>그때 어떤 생각이 들었나요? <span class="tiny" style="font-weight:400">(선택)</span></h3><textarea id="ud-thought" maxlength="180" placeholder="예: 오늘은 한 번쯤 괜찮을 것 같았다">'+esc(edit?(record.thought||((record.th||[]).join(' · '))):'')+'</textarea><div class="sep"></div><h3>어떤 감정이 있었나요? <span class="tiny" style="font-weight:400">(여러 개)</span></h3><div class="opts" id="ud-feel">'+urgeEditorChips(URGE_FEELS,st.feel,'data-ud-feel',true)+'</div></div>'+ 
    '<div class="card"><h3>어떻게 대처했나요? <span class="tiny" style="font-weight:400">(여러 개)</span></h3><div class="opts" id="ud-cope">'+urgeEditorChips(URGE_COPES,st.cope,'data-ud-cope',true)+'</div><p class="tiny" style="margin:9px 0 0">미루기·자리 벗어나기·충동을 지나가게 두기·주의 돌리기·건강한 행동으로 바꾸기 등 SMART Recovery의 DEADs 원리를 앱 언어로 풀었습니다.</p><div class="sep"></div><label>대신 무엇을 했나요? <span class="tiny">(선택)</span></label><textarea id="ud-alt" maxlength="180" placeholder="예: 산책을 하고 회복 동료에게 전화했다">'+esc(edit?(record.alt||''):'')+'</textarea><div class="field" style="margin-top:11px"><label>한 줄 메모 <span class="tiny">(선택)</span></label><textarea id="ud-note" maxlength="300" placeholder="다음에 기억하고 싶은 점">'+esc(edit?(record.note||''):'')+'</textarea></div></div>'+ 
    '<button class="btn" id="ud-save">'+(edit?'수정 저장':'충동일기에 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
  $('#ud-b').oninput=e=>{st.b=+e.target.value;$('#ud-b-n').textContent=e.target.value;};
  $$('[data-ud-type]').forEach(b=>b.onclick=()=>{st.type=b.dataset.udType;$$('[data-ud-type]').forEach(x=>x.classList.toggle('on',x===b));});
  $$('[data-ud-loc]').forEach(b=>b.onclick=()=>{st.loc=st.loc===b.dataset.udLoc?'':b.dataset.udLoc;$$('[data-ud-loc]').forEach(x=>x.classList.toggle('on',x.dataset.udLoc===st.loc));});
  $$('[data-ud-with]').forEach(b=>b.onclick=()=>{st.with=st.with===b.dataset.udWith?'':b.dataset.udWith;$$('[data-ud-with]').forEach(x=>x.classList.toggle('on',x.dataset.udWith===st.with));});
  const toggle=(sel,key,data)=>{$$(sel).forEach(b=>b.onclick=()=>{const v=b.dataset[data],i=st[key].indexOf(v);if(i<0)st[key].push(v);else st[key].splice(i,1);b.classList.toggle('on',st[key].indexOf(v)>=0);});};
  toggle('[data-ud-trg]','trg','udTrg'); toggle('[data-ud-feel]','feel','udFeel'); toggle('[data-ud-cope]','cope','udCope');
  $('#ud-save').onclick=()=>{
    const dt=new Date($('#ud-time').value); const t=Number.isFinite(dt.getTime())?dt.getTime():Date.now();
    const av=$('#ud-a').value.trim(), a=av===''?null:Math.max(0,Math.min(10,parseInt(av,10)||0));
    const mins=Math.max(0,Math.min(1440,parseInt($('#ud-min').value||0,10)||0));
    const rec={rid:st.rid,t:t,type:st.type,b:st.b,a:a,sec:mins*60,loc:st.loc,with:st.with,trg:st.trg.slice(),feel:st.feel.slice(),cope:st.cope.slice(),thought:$('#ud-thought').value.trim(),alt:$('#ud-alt').value.trim(),note:$('#ud-note').value.trim(),src:'diary',ok:0};
    const rows=S.urges||[]; const i=edit?rows.findIndex(x=>(x.rid||String(x.t))===(record.rid||String(record.t))):-1;
    if(i>=0) rows[i]=rec; else rows.push(rec); S.urges=rows; save(); closeModal(); drawUrgeDiary(); drawTools(); toast(edit?'수정했습니다.':'충동일기에 저장했습니다.');
  };
}

function drawScheduleHub(){'''
s=replace_once(s,anchor,code,'diary-functions')

# broader diary changes the old KPI semantics; manual entries are not timer trials
s=s.replace('<span>충동을 넘긴 횟수</span>','<span>충동 기록</span>')
s=replace_once(s,'const withT = S.urges.filter(u => u.sec > 60);',"const withT = S.urges.filter(u => u.sec > 60 && u.src !== 'diary');",'timer-stat-filter')

p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
w=sw.read_text(encoding='utf-8')
w=replace_once(w,"const APP_VERSION = 'V8.2.1';","const APP_VERSION = 'V8.2.2';",'sw-version')
w=replace_once(w,"const V = 'ohg-v821-trigger-tracking';","const V = 'ohg-v822-urge-diary';",'sw-cache')
sw.write_text(w,encoding='utf-8')
print('V8.2.2 urge diary patch applied')
