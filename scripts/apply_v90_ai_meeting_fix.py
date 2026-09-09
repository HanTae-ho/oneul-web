from pathlib import Path
import re


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, got {count}')
    return text.replace(old, new, 1)

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Keep AA/NA/GA family together; SMART Recovery is a separate recovery approach.
old_groups = """  {n:'NA 익명의 약물중독자들', d:'약물 · 지역별 모임 일정',
   w:'https://nakr.org/'},
  {n:'한국 SMART Recovery', d:'CBT 접근과 자기관리 기술을 활용하는 회복 자조모임',
   w:'https://smartkr.org/'},
  /* 도박 자조모임은 두 단체다. 이름이 비슷하지만 별개 조직이고 모임도 겹치지 않는다. */
  {n:'한국GA 단도박모임', d:'도박 · 서울·부산·대구·경남 중심',
   w:'http://www.dandobak.co.kr/'},
  {n:'한국단도박모임', d:'도박 · 전국 지역모임',
   w:'http://www.dandobak.or.kr/'}
"""
new_groups = """  {n:'NA 익명의 약물중독자들', d:'약물 · 지역별 모임 일정',
   w:'https://nakr.org/'},
  /* 도박 자조모임은 두 단체다. 이름이 비슷하지만 별개 조직이고 모임도 겹치지 않는다. */
  {n:'한국GA 단도박모임', d:'도박 · 서울·부산·대구·경남 중심',
   w:'http://www.dandobak.co.kr/'},
  {n:'한국단도박모임', d:'도박 · 전국 지역모임',
   w:'http://www.dandobak.or.kr/'},
  /* SMART Recovery는 AA·NA·GA와 별도의 회복 접근체계이므로 공식 자조모임 묶음 뒤에 둔다. */
  {n:'한국 SMART Recovery', d:'CBT 접근과 자기관리 기술을 활용하는 회복 자조모임',
   w:'https://smartkr.org/'}
"""
s = replace_once(s, old_groups, new_groups, 'GROUPS order')

# 2) Preserve the user's exact meeting query through location-permission decisions.
s = replace_once(
    s,
    "let ai = { back:'help', busy:false, meetings:[], resources:[], actionsOpen:false, follow:'', timer:null, timerTick:0, read:null, loc:null, activeArea:'', activeAreaSource:'', guideOpen:false, guideShown:false, guideTimer:0, voiceMode:0 };",
    "let ai = { back:'help', busy:false, meetings:[], resources:[], actionsOpen:false, follow:'', timer:null, timerTick:0, read:null, loc:null, activeArea:'', activeAreaSource:'', meetingQueryText:'', guideOpen:false, guideShown:false, guideTimer:0, voiceMode:0 };",
    'ai state'
)
s = replace_once(
    s,
    "function openAI(back){ ai.back = back || 'help'; ai.meetings = []; ai.resources = []; ai.actionsOpen = false; ai.follow=''; ai.loc=null; ai.activeArea=''; ai.activeAreaSource=''; go('ai'); }",
    "function openAI(back){ ai.back = back || 'help'; ai.meetings = []; ai.resources = []; ai.actionsOpen = false; ai.follow=''; ai.loc=null; ai.activeArea=''; ai.activeAreaSource=''; ai.meetingQueryText=''; go('ai'); }",
    'openAI reset'
)

# 3) Replace today's-only meeting engine with date/day/kind aware local matching.
start = s.index('/* 오늘 실제 등록된 모임. S.area·S.types는 이 기기에서 필터링할 때만 쓰고 AI 서버에는 보내지 않는다. */')
end = s.index('/* 가까운 센터·병원 — 정확한 거리 계산이 아니라 이 기기에 설정된 지역을 우선한다.', start)
new_meeting = r'''/* 모임 날짜·요일·종류는 기기에서 결정합니다. S.area·S.types는 AI 서버로 보내지 않습니다. */
function aiAddLocalDays(base, days){
  const d = new Date(base == null ? Date.now() : base);
  d.setDate(d.getDate() + Number(days || 0));
  return d;
}
function aiDateLabel(d){
  return (d.getMonth()+1)+'월 '+d.getDate()+'일 '+DAYN[d.getDay()]+'요일';
}
function aiMeetingDateTarget(text, baseDate){
  const x=String(text||'');
  const now=new Date(baseDate == null ? Date.now() : baseDate);
  let target=new Date(now.getTime()), explicit=false;
  const md=x.match(/(?:(\d{4})\s*년\s*)?(\d{1,2})\s*월\s*(\d{1,2})\s*일/);
  if(md){
    const y=md[1]?parseInt(md[1],10):now.getFullYear();
    target=new Date(y,parseInt(md[2],10)-1,parseInt(md[3],10),now.getHours(),now.getMinutes(),0,0);
    explicit=true;
  }else if(/모레/.test(x)){ target=aiAddLocalDays(now,2); explicit=true; }
  else if(/내일/.test(x)){ target=aiAddLocalDays(now,1); explicit=true; }
  else if(/오늘/.test(x)){ target=new Date(now.getTime()); explicit=true; }
  else {
    const m=x.match(/([월화수목금토일])요일/);
    if(m){
      const want=DAYN.indexOf(m[1]);
      let delta=(want-now.getDay()+7)%7;
      if(/다음\s*주/.test(x)) delta+=7;
      target=aiAddLocalDays(now,delta); explicit=true;
    }
  }
  return {
    date:target, day:DAYN[target.getDay()], label:aiDateLabel(target),
    ymd:ymd(target), isToday:ymd(target)===ymd(now), explicit:explicit,
    hm:pad(now.getHours())+':'+pad(now.getMinutes()), now:now
  };
}
function aiCurrentTimeContext(baseDate){
  const d=new Date(baseDate == null ? Date.now() : baseDate);
  let tz='';
  try{ tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''; }catch(e){}
  return {
    localDate:ymd(d), day:DAYN[d.getDay()]+'요일', time:pad(d.getHours())+':'+pad(d.getMinutes()),
    timeZone:tz||'device-local',
    label:d.getFullYear()+'년 '+(d.getMonth()+1)+'월 '+d.getDate()+'일 '+DAYN[d.getDay()]+'요일 '+pad(d.getHours())+':'+pad(d.getMinutes())
  };
}
function aiCalendarReply(text, baseDate){
  const x=String(text||'').trim();
  if(!x || /(모임|센터|병원|기관|예약|일정)/.test(x)) return '';
  const asksDate=/(오늘|내일|모레|어제|현재)/.test(x) && /(몇\s*월|몇\s*일|며칠|요일|날짜)/.test(x);
  const asksTime=/(지금|현재|오늘)/.test(x) && /(몇\s*시|현재\s*시간|지금\s*시간)/.test(x);
  if(!asksDate && !asksTime) return '';
  const now=new Date(baseDate == null ? Date.now() : baseDate);
  if(asksTime){
    const hh=now.getHours(), ap=hh<12?'오전':'오후', h12=hh%12||12;
    return '현재 기기 시각은 '+now.getFullYear()+'년 '+(now.getMonth()+1)+'월 '+now.getDate()+'일 '+DAYN[now.getDay()]+'요일 '+ap+' '+h12+'시 '+pad(now.getMinutes())+'분입니다.';
  }
  let offset=0, word='오늘';
  if(/어제/.test(x)){ offset=-1; word='어제'; }
  else if(/모레/.test(x)){ offset=2; word='모레'; }
  else if(/내일/.test(x)){ offset=1; word='내일'; }
  const d=aiAddLocalDays(now,offset);
  return word+'은 '+d.getFullYear()+'년 '+(d.getMonth()+1)+'월 '+d.getDate()+'일 '+DAYN[d.getDay()]+'요일입니다.';
}
function aiMeetingKindQuery(text){
  const x=String(text||'');
  if(/SMART\s*Recovery|SMART\s*(모임|회복)|스마트\s*(리커버리|모임|회복)/i.test(x)) return 'SMART';
  if(/\bAA\b|알코올\s*(?:자조)?모임|술\s*모임/i.test(x)) return '알코올';
  if(/\bGA\b|단도박|도박\s*(?:자조)?모임/i.test(x)) return '도박';
  if(/\bNA\b|약물\s*(?:자조)?모임|마약\s*(?:자조)?모임/i.test(x)) return '약물';
  return '';
}
function aiMeetingKindOK(r, kind){
  if(!kind) return true;
  const txt=[r&&r.k,r&&r.n,r&&r.d].filter(Boolean).join(' ');
  if(kind==='SMART') return /SMART|스마트/i.test(txt);
  const rk=rowKind(r);
  if(rk) return rk===kind;
  if(kind==='알코올') return /(^|\s)AA(?:\s|$)|알코올/i.test(txt);
  if(kind==='도박') return /(^|\s)GA(?:\s|$)|단도박|도박/i.test(txt);
  if(kind==='약물') return /(^|\s)NA(?:\s|$)|약물|마약/i.test(txt);
  return false;
}
function aiMeetingInfo(area,text,baseDate){
  const R=S.res||{};
  const src=famMode()
    ? ((R.family&&R.family.length)?R.family:FAMILY)
    : ((R.groups&&R.groups.length)?R.groups:GROUPS);
  const target=aiMeetingDateTarget(text,baseDate), kind=aiMeetingKindQuery(text), mine=myKinds();
  let rows=src.filter(r=>r.y===target.day);
  if(kind) rows=rows.filter(r=>aiMeetingKindOK(r,kind));
  else rows=rows.filter(r=>{ const k=rowKind(r); return !k||!mine.length||mine.indexOf(k)>=0; });
  if(area) rows=rows.filter(r=>{
    const a=areasOf(r);
    return a.length&&a.indexOf(area)>=0;
  });
  rows.sort((a,b)=>String(a.h||'99:99').localeCompare(String(b.h||'99:99')));
  const upcoming=target.isToday?rows.filter(r=>!r.h||String(r.h)>=target.hm):rows.slice();
  const started=target.isToday?rows.filter(r=>r.h&&String(r.h)<=target.hm):[];
  const nowIntent=target.isToday && /(?:지금|현재).{0,12}모임|모임.{0,12}(?:지금|현재)|하고\s*있는\s*.*모임/.test(String(text||''));
  return {all:rows,upcoming:upcoming,started:started,target:target,kind:kind,nowIntent:nowIntent,mine:mine};
}
function aiMeetingRows(area,text,baseDate){
  const info=aiMeetingInfo(area == null ? (S.area||'') : area,text||'',baseDate);
  let rows;
  if(info.nowIntent) rows=info.started.slice().reverse();
  else rows=info.upcoming.length?info.upcoming:info.all;
  return rows.slice(0,6);
}
function aiKoTime(h){
  const m=String(h||'').match(/^(\d{1,2}):(\d{2})/); if(!m) return String(h||'');
  let hh=parseInt(m[1],10), mm=parseInt(m[2],10); const ap=hh<12?'오전':'오후';
  let k=hh%12; if(!k) k=12;
  return ap+' '+k+'시'+(mm ? ' '+mm+'분' : '');
}
function aiMeetingExample(rows){
  return rows.slice(0,3).map(r=>{
    const bits=[r.n||'모임'];
    if(r.h) bits.push(aiKoTime(r.h));
    if(r.a) bits.push(r.a);
    return bits.join(' · ');
  }).join('\n');
}
function aiMeetingSummary(area,source,note,text,baseDate){
  const info=aiMeetingInfo(area,text||'',baseDate), target=info.target;
  const where=area?area+' 지역':'등록된 전체 지역';
  const prefix=note?note+'\n':'';
  const via=source?source+'으로 ':'';
  const kind=info.kind?info.kind+' ':'';
  const personal=!info.kind && /나에게\s*맞|내게\s*맞|추천/.test(String(text||'')) && info.mine.length
    ? '내 정보의 회복 영역('+info.mine.join('·')+')을 기준으로 ' : '';
  if(info.nowIntent){
    if(info.started.length){
      return prefix+via+personal+'오늘 '+where+'에서 현재 시각 이전에 시작한 등록 '+kind+'모임은 '+info.started.length+'개 확인됩니다.\n'+
        aiMeetingExample(info.started.slice().reverse())+'\n종료시간 정보는 없어 지금 실제로 진행 중인지는 확정할 수 없습니다. 참여 전 전화나 안내 페이지에서 확인해주세요.';
    }
    return prefix+via+'오늘 '+where+'에서 현재 시각 이전에 시작한 등록 '+kind+'모임은 확인되지 않습니다. 종료시간 정보가 없는 일정은 현재 진행 여부를 앱이 확정하지 않습니다.';
  }
  if(target.isToday){
    if(info.upcoming.length){
      return prefix+via+personal+'오늘 '+where+'에서 지금부터 시작 예정인 등록 '+kind+'모임을 확인했어요. 현재 시각 이후 '+info.upcoming.length+'개 일정이 있습니다.\n'+
        aiMeetingExample(info.upcoming)+'\n일정이 바뀌었을 수 있으니 참여 전 전화나 안내 페이지에서 한 번 확인해주세요.';
    }
    if(info.all.length){
      return prefix+via+'오늘 '+where+'에 등록된 '+kind+'모임은 '+info.all.length+'개 있지만 현재 시각 이후 시작 예정인 일정은 확인되지 않습니다. 다른 요일이나 지역도 확인할 수 있습니다.';
    }
    return prefix+via+'오늘 '+where+'에서 확인되는 등록 '+kind+'모임이 없습니다. 지역이나 모임 종류를 넓혀 확인해볼 수 있습니다.';
  }
  if(info.all.length){
    return prefix+via+personal+target.label+' '+where+'에서 등록 '+kind+'모임 '+info.all.length+'개를 확인했어요.\n'+
      aiMeetingExample(info.all)+'\n일정이 바뀌었을 수 있으니 참여 전 전화나 안내 페이지에서 한 번 확인해주세요.';
  }
  return prefix+via+target.label+' '+where+'에서 확인되는 등록 '+kind+'모임이 없습니다. 지역이나 모임 종류를 넓혀 확인해볼 수 있습니다.';
}
function aiMeetingPayload(rows){
  return (rows || []).map(r => ({
    name:String(r.n || '').slice(0,100), day:String(r.y || ''), time:String(r.h || ''),
    area:String(r.a || '').slice(0,80), desc:String(r.d || '').slice(0,220),
    phone:String(r.t || '').slice(0,40), url:String(r.w || '').slice(0,300)
  }));
}
function aiMeetingCards(rows){
  if(!rows || !rows.length) return '<div class="note">요청한 조건에 맞는 등록 모임이 없습니다. ' +
    '모임 찾기에서 지역이나 종류를 넓혀 확인해보세요.</div>' +
    '<div style="height:9px"></div><button class="btn sec sm" id="ai-all-meet">모임 찾기 열기</button>';
  let h = '<div class="note" style="margin-bottom:9px">아래 일정은 자원시트에 등록된 공개 정보입니다. 변경될 수 있으니 가기 전에 한 번 더 확인해주세요.</div>';
  rows.forEach(r => {
    h += '<div class="help"><span class="ic">' + ico(famMode() ? 'family' : 'people') + '</span>' +
      '<span class="b"><b>' + esc(r.n) + '</b><span>' + esc([r.y ? r.y + '요일' : '', r.h || '', r.a || '', r.d || ''].filter(Boolean).join(' · ')) + '</span></span>' +
      '<span class="acts">' +
      (r.t ? '<a class="go" href="tel:' + esc(String(r.t).replace(/[^0-9+\-]/g,'')) + '">전화</a>' : '') +
      (r.w ? '<a class="go" href="' + esc(r.w) + '" target="_blank" rel="noopener">열기</a>' : '') +
      '</span></div>';
  });
  h += '<button class="btn ghost sm" id="ai-all-meet">전체 모임 찾기</button>';
  return h;
}
function aiBindMeetingButton(){
  const b=$('#ai-all-meet');
  if(b) b.onclick=()=>{
    const q=String(ai.meetingQueryText||''), target=aiMeetingDateTarget(q), kind=aiMeetingKindQuery(q);
    mt.target=famMode()?'fam':'me'; mt.mode=target.isToday?'today':'area'; mt.todayArea=target.isToday?(ai.activeArea||''):'';
    mt.area=target.isToday?'':(ai.activeArea||''); mt.q=''; mt.kind=kind==='SMART'?'전체':kind;
    go('meet');
  };
}

'''
s = s[:start] + new_meeting + s[end:]

# 4) Apply saved meeting query after location selection and preserve it through the permission flow.
old_apply = """function aiApplyArea(kind,area,source,note){
  ai.loc=null; ai.activeArea=area || ''; ai.activeAreaSource=source || '';
  if(kind==='meeting'){
    ai.meetings=aiTodayMeetings(area || ''); ai.resources=[];
    aiAdd('assistant',aiMeetingSummary(area || '',source || '',note || ''),true);
    ai.follow='meeting';
  }else{
"""
new_apply = """function aiApplyArea(kind,area,source,note){
  ai.loc=null; ai.activeArea=area || ''; ai.activeAreaSource=source || '';
  if(kind==='meeting'){
    const q=String(ai.meetingQueryText||'');
    ai.meetings=aiMeetingRows(area || '',q); ai.resources=[];
    aiAdd('assistant',aiMeetingSummary(area || '',source || '',note || '',q),true);
    ai.follow='meeting';
  }else{
"""
s = replace_once(s, old_apply, new_apply, 'aiApplyArea')
s = replace_once(
    s,
    "async function aiHandleAreaRequest(kind,text){\n  ai.busy=true; drawAI();",
    "async function aiHandleAreaRequest(kind,text){\n  if(kind==='meeting') ai.meetingQueryText=String(text||'');\n  ai.busy=true; drawAI();",
    'aiHandleAreaRequest query preserve'
)

# 5) A meeting follow-up should not always force the Today screen.
s = replace_once(
    s,
    "if(ai.follow==='meeting') return '<button class=\"btn sec sm\" id=\"ai-follow-meet\">오늘 모임 전체 보기</button>';",
    "if(ai.follow==='meeting') return '<button class=\"btn sec sm\" id=\"ai-follow-meet\">모임 전체 보기</button>';",
    'meeting follow label'
)
old_bind = """  if(ai.follow==='meeting'){
    const b=$('#ai-follow-meet'); if(b) b.onclick=()=>{
      const area=ai.activeArea || '';
      ai.follow=''; mt.target=famMode()?'fam':'me'; mt.mode='today'; mt.todayArea=area; mt.q=''; mt.kind=''; go('meet');
    };
    return;
  }
"""
new_bind = """  if(ai.follow==='meeting'){
    const b=$('#ai-follow-meet'); if(b) b.onclick=()=>{
      const area=ai.activeArea||'', q=String(ai.meetingQueryText||''), target=aiMeetingDateTarget(q), kind=aiMeetingKindQuery(q);
      ai.follow=''; mt.target=famMode()?'fam':'me'; mt.mode=target.isToday?'today':'area'; mt.todayArea=target.isToday?area:'';
      mt.area=target.isToday?'':area; mt.q=''; mt.kind=kind==='SMART'?'전체':kind; go('meet');
    };
    return;
  }
"""
s = replace_once(s, old_bind, new_bind, 'meeting follow action')\n
# 6) Broaden only explicit meeting lookup language; counselling sentences like "모임이 싫다" remain AI conversation.
s = replace_once(
    s,
    "  if(/\\b(AA|GA|NA)\\b/i.test(x) && /(모임|있|찾|시간|언제|어디|보여|알려|참여)/.test(x)) return 'meeting';\n  if(/(모임|알아넌|겜아넌|나란온)/i.test(x) && /(있어|있나|찾|시간|언제|어디|보여|알려|목록|참여할\\s*수|열려|열리)/.test(x)) return 'meeting';",
    "  if(/\\b(AA|GA|NA)\\b|SMART\\s*Recovery|스마트\\s*리커버리/i.test(x) && /(모임|있|찾|시간|언제|어디|보여|알려|참여|열려|열리|추천)/.test(x)) return 'meeting';\n  if(/(모임|알아넌|겜아넌|나란온)/i.test(x) && /(있어|있나|찾|시간|언제|어디|보여|알려|목록|참여할\\s*수|열려|열리|맞는|추천|어떤)/.test(x)) return 'meeting';",
    'meeting intent regex'
)

# 7) Resolve pure date/day questions locally before AI, then provide current device time context to general AI calls.
old_chain = """  const wantsRead = (!crisis && !voiceCommand && !timerMin) ? aiReadWanted(text, topic) : false;
  const knowledge = (!crisis && !voiceCommand && !timerMin && !wantsRead) ? aiKnowledgeReply(text) : null;
  const localIntent = (!crisis && !voiceCommand && !timerMin && !wantsRead && !knowledge) ? aiLocalIntent(text, topic) : '';
  const isLocal = !!(crisis || voiceCommand || timerMin || wantsRead || knowledge || localIntent);
"""
new_chain = """  const wantsRead = (!crisis && !voiceCommand && !timerMin) ? aiReadWanted(text, topic) : false;
  const calendarReply = (!crisis && !voiceCommand && !timerMin && !wantsRead) ? aiCalendarReply(text) : '';
  const knowledge = (!crisis && !voiceCommand && !timerMin && !wantsRead && !calendarReply) ? aiKnowledgeReply(text) : null;
  const localIntent = (!crisis && !voiceCommand && !timerMin && !wantsRead && !calendarReply && !knowledge) ? aiLocalIntent(text, topic) : '';
  const isLocal = !!(crisis || voiceCommand || timerMin || wantsRead || calendarReply || knowledge || localIntent);
"""
s = replace_once(s, old_chain, new_chain, 'aiSend local chain')

s = replace_once(
    s,
    """  if(knowledge){
    aiAdd('assistant',knowledge.text,true);
    ai.follow=knowledge.follow||'';
    drawAI(); return;
  }

  /* 시간을 말로 요청하면 OpenAI에 맡기지 않고 실제 채팅 타이머를 엽니다. */
""",
    """  if(calendarReply){
    aiAdd('assistant',calendarReply,true);
    drawAI(); return;
  }

  if(knowledge){
    aiAdd('assistant',knowledge.text,true);
    ai.follow=knowledge.follow||'';
    drawAI(); return;
  }

  /* 시간을 말로 요청하면 OpenAI에 맡기지 않고 실제 채팅 타이머를 엽니다. */
""",
    'calendar response branch'
)

old_body = """    const body = {
      clientId: aiClientId(), message:text, topic:topic || '', build:BUILD,
      history: prior.map(m => ({ role:m.role, text:String(m.text || '').slice(0,1200) })),
      meetings: [], resources: []
    };
"""
new_body = """    const nowCtx=aiCurrentTimeContext();
    const body = {
      clientId: aiClientId(),
      /* AI 서버 v1.3도 현재 문장으로 읽을 수 있도록 기준시각을 메시지 앞에 함께 보냅니다. */
      message:'[앱 기준 현재시각: '+nowCtx.label+' · '+nowCtx.timeZone+']\\n'+text,
      topic:topic || '', build:BUILD, currentTime:nowCtx,
      history: prior.map(m => ({ role:m.role, text:String(m.text || '').slice(0,1200) })),
      meetings: [], resources: []
    };
"""
s = replace_once(s, old_body, new_body, 'AI current time context')

p.write_text(s, encoding='utf-8')

# Service worker cache revision; visible app version remains V9.0.
sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
w = replace_once(w, "const V = 'ohg-v900-social-stage1';", "const V = 'ohg-v900-social-ai-meeting-fix';", 'sw cache')
sw.write_text(w, encoding='utf-8')

# Privacy: device-local date/time/timezone is now supplied to AI for relative-date correctness.
pp = Path('privacy.html')
pr = pp.read_text(encoding='utf-8')
pr = replace_once(
    pr,
    '<li>사용자가 마음프로에 입력한 현재 메시지</li>\n<li>대화 주제와 앱 버전</li>',
    '<li>사용자가 마음프로에 입력한 현재 메시지</li>\n<li>상대 날짜·요일 표현을 정확히 해석하기 위한 기기의 현재 날짜·시간·시간대</li>\n<li>대화 주제와 앱 버전</li>',
    'privacy AI transmitted fields'
)
pp.write_text(pr, encoding='utf-8')

# Keep an audit note in README without changing product semantics.
rp = Path('README.md')
r = rp.read_text(encoding='utf-8')
note = """

### V9.0 마음프로 날짜·모임 보정

- `오늘/내일/모레/특정 요일` 모임 질문은 기기 날짜를 기준으로 로컬에서 계산합니다.
- AA·GA·NA·SMART Recovery를 질문에 명시하면 해당 종류를 우선 필터링합니다.
- `지금 하고 있는 모임`은 종료시간 자료가 없으므로 현재 진행 중이라고 단정하지 않고, 현재시각 이전 시작 일정과 확인 필요를 안내합니다.
- 순수 날짜·요일 질문은 AI에 보내지 않고 기기에서 답합니다.
- 일반 AI 상담에는 기기의 현재 날짜·시간·시간대를 기준시각으로 함께 보내 상대 날짜 표현의 오류를 줄입니다. GPS나 회복기록은 함께 보내지 않습니다.
- 단체 공식 안내는 AA → NA → GA 2개 단체 → SMART Recovery 순서로 표시합니다.
"""
if '### V9.0 마음프로 날짜·모임 보정' not in r:
    r += note
rp.write_text(r, encoding='utf-8')

print('V9.0 AI/meeting patch applied')
