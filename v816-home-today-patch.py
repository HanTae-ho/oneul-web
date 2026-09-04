from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

# Home gets one unified schedule container.
once('  <div id="home-habits"></div>\n  <div id="home-alert"></div>',
     '  <div id="home-today"></div>\n  <div id="home-alert"></div>', 'home container')

# V8.1.6 UI styles.
css_anchor='  .habit-home-row .time{font-size:11.5px;color:var(--faint);white-space:nowrap}\n'
css_add=css_anchor+'''  /* V8.1.6 — 홈의 습관·복약·식사·잠·외래를 한 장의 오늘 일정으로 모읍니다. */\n  .today-home{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:14px;margin-bottom:12px}\n  .today-home h3{margin:0}.today-summary{font-size:11.5px;color:var(--dim);margin-top:2px}\n  .today-row{display:flex;align-items:center;gap:9px;padding:9px 0;border-top:1px solid var(--line)}\n  .today-row.first{border-top:0}.today-row .tcheck{width:31px;height:31px;flex:none;border-radius:9px;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--acc);background:var(--bg)}\n  .today-row .tcheck.on{background:var(--acc);color:#fff;border-color:var(--acc)}.today-row .tcheck.static{border-color:transparent;background:var(--accbg)}\n  .today-row .txt{flex:1;min-width:0}.today-row .txt b{display:block;font-size:13.5px}.today-row .txt span{display:block;font-size:11.5px;color:var(--dim);margin-top:1px;line-height:1.45}\n  .today-row .time{font-size:11.5px;color:var(--faint);white-space:nowrap}.today-upcoming{margin-top:7px;padding-top:10px;border-top:1px dashed var(--line)}\n  .today-upcoming .k{display:block;font-size:11px;font-weight:700;color:var(--acc);margin-bottom:4px}.today-upcoming button{width:100%;text-align:left}\n  .today-sleepq{margin-top:8px;padding-top:11px;border-top:1px solid var(--line)}.today-sleepq p{margin:0 0 8px;font-size:12px;color:var(--dim)}\n'''
once(css_anchor,css_add,'today css')

# drawHome calls the unified card, not the separate habit card.
once('  drawDailyHome();\n  drawHabitHome();', '  drawDailyHome();\n  drawTodayScheduleHome();', 'home draw call')

# Remove duplicate medication/treatment/body cards from home. Their data/recording functions remain intact.
pat=r'''  /\* 복약 — 치료관리에서 사용할 때만 홈에 표시합니다\. \*/\n.*?  /\* 식사 · 잠 \*/\n  drawBodyHome\(a\);\n'''
s2,n=re.subn(pat,'  /* V8.1.6: 복약·외래·식사·잠은 위의 「오늘 일정」 카드에서 함께 표시합니다. */\n',s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'remove duplicate home cards: expected 1, got {n}')
s=s2

# Replace the V8.1.5 habit-only home renderer with a unified schedule renderer.
pat=r'''function drawHabitHome\(\)\{.*?\n\}\nfunction startHabitNew\(data\)\{'''
new=r'''function homeTimeKey(v){
  const m=String(v||'').match(/^(\d{2}):(\d{2})$/); return m?(+m[1]*60 + +m[2]):9999;
}
function drawTodayScheduleHome(){
  const box=$('#home-today'); if(!box) return;
  const fam=famMode(), d=today(), items=[];
  let actionable=0, completed=0;

  habitToday().forEach(h=>{
    const done=habitDoneOn(h,d); actionable++; if(done) completed++;
    items.push({kind:'habit',id:h.id,time:h.notify?(h.time||''):'',label:h.name,sub:(h.check||'오늘 실천했습니다')+' · '+habitProgressText(h),done:done,action:1});
  });

  if(!fam && treatmentMedOn() && (S.meds||[]).length){
    const ord=MEDSLOT.map(x=>x.k), done=todayRec(S.medLog||[]).map(x=>x.n);
    S.meds.slice().sort((a,b)=>ord.indexOf(a.s)-ord.indexOf(b.s)).forEach(m=>{
      const slot=MEDSLOT.find(x=>x.k===m.s)||{l:m.s}, ok=done.indexOf(m.s)>=0; actionable++; if(ok) completed++;
      items.push({kind:'med',id:m.s,time:m.t||'',label:slot.l+' 약',sub:'복약',done:ok,action:1});
    });
  }

  const eord=EATSLOT.map(x=>x.k), edone=todayRec(S.eatLog||[]).map(x=>x.n);
  (S.eats||[]).slice().sort((a,b)=>eord.indexOf(a.s)-eord.indexOf(b.s)).forEach(m=>{
    const slot=EATSLOT.find(x=>x.k===m.s)||{l:m.s}, ok=edone.indexOf(m.s)>=0; actionable++; if(ok) completed++;
    items.push({kind:'eat',id:m.s,time:m.t||'',label:slot.l,sub:'식사',done:ok,action:1});
  });

  const sp=S.sleep||{};
  if(sp.on && /^\d{2}:\d{2}$/.test(String(sp.bed||'')))
    items.push({kind:'sleep',id:'bed',time:sp.bed,label:'잠자리',sub:'잘 시간',done:false,action:0});

  items.sort((a,b)=>homeTimeKey(a.time)-homeTimeKey(b.time));

  let visitHtml='';
  if(!fam){
    const t=treatmentCfg();
    if(t.outpatientOn){
      const v=treatmentEffectiveVisit(), label=treatmentVisitLabel();
      if(v && label){
        const dd=diffYmd(d,v);
        if(dd===0){
          items.unshift({kind:'visit',id:'visit',time:'',label:'오늘 외래',sub:label,done:false,action:0});
        }else{
          visitHtml='<div class="today-upcoming"><span class="k">다가오는 일정</span><button id="home-today-visit"><b>외래</b><div class="muted" style="margin-top:2px">'+esc(label)+'</div></button></div>';
        }
      }
    }
  }

  const askSleep=!!sp.on && todayRec(S.sleepLog||[]).length===0;
  const configured=items.length || visitHtml || askSleep;
  if(!configured){ box.innerHTML=''; return; }

  let html='<div class="today-home"><div class="sp" style="align-items:flex-start"><div><h3>오늘 일정</h3>'+
    (actionable?'<div class="today-summary">'+completed+' / '+actionable+' 완료</div>':'')+
    '</div><button class="tiny link" id="home-today-manage">일정 관리</button></div>';
  items.forEach((x,i)=>{
    const icon=x.kind==='sleep'?'moon':x.kind==='visit'?'cal':(x.done?'check':'box');
    const btn=x.action?'<button class="tcheck'+(x.done?' on':'')+'" data-today-kind="'+x.kind+'" data-today-id="'+esc(x.id)+'">'+ico(icon)+'</button>':'<span class="tcheck static">'+ico(icon)+'</span>';
    html+='<div class="today-row'+(i===0?' first':'')+'">'+btn+'<div class="txt"><b>'+esc(x.label)+'</b><span>'+esc(x.sub)+'</span></div><span class="time">'+esc(x.time||'')+'</span></div>';
  });
  html+=visitHtml;
  if(askSleep){
    html+='<div class="today-sleepq"><p>어젯밤 잠은 어떠셨나요?</p><div class="opts">'+SLEEPQ.map(q=>'<button class="opt" data-today-sleep="'+q.k+'">'+q.l+'</button>').join('')+'</div></div>';
  }
  html+='</div>';
  box.innerHTML=html;

  const manage=$('#home-today-manage'); if(manage) manage.onclick=()=>go('schedule');
  const visit=$('#home-today-visit'); if(visit) visit.onclick=()=>go('treatment');
  box.querySelectorAll('[data-today-kind]').forEach(b=>b.onclick=()=>{
    if(b.dataset.todayKind==='habit'){
      const h=habitList().find(x=>x.id===b.dataset.todayId); if(h) habitToggle(h,d);
    }else if(b.dataset.todayKind==='med'){
      S.medLog=S.medLog||[]; if(todayRec(S.medLog).map(x=>x.n).indexOf(b.dataset.todayId)<0) S.medLog.push({t:Date.now(),n:b.dataset.todayId});
    }else if(b.dataset.todayKind==='eat'){
      S.eatLog=S.eatLog||[]; if(todayRec(S.eatLog).map(x=>x.n).indexOf(b.dataset.todayId)<0) S.eatLog.push({t:Date.now(),n:b.dataset.todayId});
    }
    save(); drawTodayScheduleHome(); drawTools();
  });
  box.querySelectorAll('[data-today-sleep]').forEach(b=>b.onclick=()=>{
    S.sleepLog=S.sleepLog||[]; S.sleepLog.push({t:Date.now(),q:b.dataset.todaySleep}); save(); drawTodayScheduleHome();
    toast(b.dataset.todaySleep==='bad'?'기록했습니다. 오늘은 무리하지 마세요.':'기록했습니다.');
  });
  refreshIcons();
}
/* V8.1.5 내부 호출과의 호환. 습관 체크 뒤에도 홈의 전체 일정이 갱신됩니다. */
function drawHabitHome(){ drawTodayScheduleHome(); }
function startHabitNew(data){'''
s2,n=re.subn(pat,new,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'unified home renderer: expected 1, got {n}')
s=s2

# Version bump.
once("const BUILD = 'V8.1.5';", "const BUILD = 'V8.1.6';", 'build version')
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
w=sw.read_text(encoding='utf-8')
w=w.replace("const APP_VERSION = 'V8.1.5';","const APP_VERSION = 'V8.1.6';",1)
w=w.replace("const V = 'ohg-v815-habits';","const V = 'ohg-v816-home-today';",1)
sw.write_text(w,encoding='utf-8')
print('V8.1.6 home today schedule patch PASS')
