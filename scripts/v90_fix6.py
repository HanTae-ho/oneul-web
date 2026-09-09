from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')


def block(start, end, new, label):
    global s
    a = s.index(start)
    b = s.index(end, a)
    s = s[:a] + new + s[b:]
    print('patched', label)


def once(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, got {n}')
    s = s.replace(old, new, 1)
    print('patched', label)


# 1. Named fellowship mentions alone must not turn counselling into meeting search.
old = """  if(/\\b(AA|GA|NA)\\b|SMART\\s*Recovery|스마트\\s*리커버리/i.test(x) && /(모임|있|찾|시간|언제|어디|보여|알려|참여|열려|열리|추천)/.test(x)) return 'meeting';
  if(/(모임|알아넌|겜아넌|나란온)/i.test(x) && /(있어|있나|찾|시간|언제|어디|보여|알려|목록|참여할\\s*수|열려|열리|맞는|추천|어떤)/.test(x)) return 'meeting';"""
new = """  if(/\\b(AA|GA|NA)\\b|SMART\\s*Recovery|스마트\\s*리커버리/i.test(x) && /(있어|있나|있는|있을|찾|시간|언제|어디|보여|알려|참여할\\s*수|열려|열리|추천|몇\\s*시|몇\\s*개)/.test(x)) return 'meeting';
  if(/(?:나에게|내게).{0,12}맞는.{0,12}모임|(?:어떤|무슨|맞는).{0,10}모임/.test(x)) return 'meeting';
  if(/(모임|알아넌|겜아넌|나란온)/i.test(x) && /(있어|있나|있는|있을|찾|시간|언제|어디|보여|알려|목록|참여할\\s*수|열려|열리|추천|몇\\s*시|몇\\s*개)/.test(x)) return 'meeting';"""
once(old, new, 'meeting intent boundary')

# 2. Natural Korean timer requests such as "5분 같이 버텨줘".
block(
    'function aiTimerMinutes(text, topic){',
    'function aiTimerClearTick()',
    """function aiTimerMinutes(text, topic){
  const x = String(text || '');
  if(topic === 'timer' && !/(\\d{1,2})\\s*분/.test(x)) return 5;
  if(!/(버티|버텨|버틸|견디|견뎌|견딜|타이머|기다려|같이\\s*(?:있|버티|버텨|견디|견뎌))/.test(x)) return 0;
  const m = x.match(/(\\d{1,2})\\s*분/);
  if(!m) return topic === 'timer' ? 5 : 0;
  const n = parseInt(m[1], 10);
  return n >= 1 && n <= 30 ? n : 0;
}
""",
    'timer natural language',
)

# 3. Retry temporary upstream failures once; avoid false retry claims.
block(
    'function aiCanRetry(code){',
    'function aiErrorMessage(code){',
    """function aiCanRetry(code){
  return ['NETWORK_ERROR','INVALID_JSON','TEMPORARY','UPSTREAM_BUSY'].includes(String(code || ''));
}

""",
    'retry transient errors',
)
once(
    "  return '마음프로 연결이 잠시 불안정했습니다. 한 번 자동으로 다시 시도했지만 연결되지 않았습니다. 잠시 후 다시 보내주세요. 급한 도움이 필요하면 헬프의 헬프콜을 이용해주세요.';",
    "  return '마음프로 연결이 잠시 불안정했습니다. 잠시 후 다시 보내주세요. 급한 도움이 필요하면 헬프의 헬프콜을 이용해주세요.';",
    'retry wording',
)

# 4 + 6. Date boundary conditions and Korean particles.
block(
    'function aiMeetingDateTarget(text, baseDate){',
    'function aiCurrentTimeContext(baseDate){',
    """function aiValidLocalDate(year,month,day,now){
  if(!Number.isInteger(year)||!Number.isInteger(month)||!Number.isInteger(day)||month<1||month>12||day<1||day>31) return null;
  const d=new Date(year,month-1,day,now.getHours(),now.getMinutes(),0,0);
  if(d.getFullYear()!==year||d.getMonth()!==month-1||d.getDate()!==day) return null;
  return d;
}
function aiMondayIndex(day){ return (Number(day)+6)%7; }
function aiMeetingDateTarget(text, baseDate){
  const x=String(text||'');
  const now=new Date(baseDate == null ? Date.now() : baseDate);
  let target=new Date(now.getTime()), explicit=false, invalid=false, error='';
  const md=x.match(/(?:(\\d{4})\\s*년\\s*)?(\\d{1,2})\\s*월\\s*(\\d{1,2})\\s*일/);
  if(md){
    let year=md[1]?parseInt(md[1],10):now.getFullYear();
    const month=parseInt(md[2],10), day=parseInt(md[3],10), yearExplicit=!!md[1];
    target=aiValidLocalDate(year,month,day,now);
    if(target && !yearExplicit){
      const today0=new Date(now.getFullYear(),now.getMonth(),now.getDate());
      const target0=new Date(target.getFullYear(),target.getMonth(),target.getDate());
      if(target0<today0){ year+=1; target=aiValidLocalDate(year,month,day,now); }
    }
    explicit=true;
    if(!target){ invalid=true; error='입력한 날짜가 존재하지 않습니다. 월과 일을 다시 확인해주세요.'; target=new Date(now.getTime()); }
  }else if(/어제/.test(x)){ target=aiAddLocalDays(now,-1); explicit=true; }
  else if(/모레/.test(x)){ target=aiAddLocalDays(now,2); explicit=true; }
  else if(/내일/.test(x)){ target=aiAddLocalDays(now,1); explicit=true; }
  else if(/오늘/.test(x)){ target=new Date(now.getTime()); explicit=true; }
  else {
    const m=x.match(/([월화수목금토일])요일/);
    if(m){
      const want=DAYN.indexOf(m[1]);
      const curMon=aiMondayIndex(now.getDay()), wantMon=aiMondayIndex(want);
      let delta;
      if(/다음\\s*주/.test(x)) delta=(7-curMon)+wantMon;
      else if(/지난\\s*주/.test(x)) delta=wantMon-curMon-7;
      else if(/이번\\s*주/.test(x)) delta=wantMon-curMon;
      else delta=(want-now.getDay()+7)%7;
      target=aiAddLocalDays(now,delta); explicit=true;
    }
  }
  return {
    date:target, day:invalid?'':DAYN[target.getDay()], label:invalid?'':aiDateLabel(target),
    ymd:invalid?'':ymd(target), isToday:!invalid&&ymd(target)===ymd(now), explicit:explicit,
    invalid:invalid, error:error, hm:pad(now.getHours())+':'+pad(now.getMinutes()), now:now
  };
}
""",
    'date target boundaries',
)

block(
    'function aiCalendarReply(text, baseDate){',
    'function aiMeetingKindQuery(text){',
    """function aiCalendarReply(text, baseDate){
  const x=String(text||'').trim();
  if(!x || /(모임|센터|병원|기관|예약|일정)/.test(x)) return '';
  const asksDate=/(오늘|내일|모레|어제|현재)/.test(x) && /(몇\\s*월|몇\\s*일|며칠|요일|날짜)/.test(x);
  const asksTime=/(지금|현재|오늘)/.test(x) && /(몇\\s*시|현재\\s*시간|지금\\s*시간)/.test(x);
  if(!asksDate && !asksTime) return '';
  const now=new Date(baseDate == null ? Date.now() : baseDate);
  if(asksTime){
    const hh=now.getHours(), ap=hh<12?'오전':'오후', h12=hh%12||12;
    return '현재 기기 시각은 '+now.getFullYear()+'년 '+(now.getMonth()+1)+'월 '+now.getDate()+'일 '+DAYN[now.getDay()]+'요일 '+ap+' '+h12+'시 '+pad(now.getMinutes())+'분입니다.';
  }
  let offset=0, lead='오늘은';
  if(/어제/.test(x)){ offset=-1; lead='어제는'; }
  else if(/모레/.test(x)){ offset=2; lead='모레는'; }
  else if(/내일/.test(x)){ offset=1; lead='내일은'; }
  const d=aiAddLocalDays(now,offset);
  return lead+' '+d.getFullYear()+'년 '+(d.getMonth()+1)+'월 '+d.getDate()+'일 '+DAYN[d.getDay()]+'요일입니다.';
}
""",
    'calendar grammar',
)

# 4 + 5. Invalid-date short circuit and no fallback to already-past cards.
block(
    'function aiMeetingInfo(area,text,baseDate){',
    'function aiMeetingRows(area,text,baseDate){',
    """function aiMeetingInfo(area,text,baseDate){
  const R=S.res||{};
  const src=famMode()
    ? ((R.family&&R.family.length)?R.family:FAMILY)
    : ((R.groups&&R.groups.length)?R.groups:GROUPS);
  const target=aiMeetingDateTarget(text,baseDate), kind=aiMeetingKindQuery(text), mine=myKinds();
  const nowIntent=target.isToday && /(?:지금|현재).{0,12}모임|모임.{0,12}(?:지금|현재)|하고\\s*있는\\s*.*모임/.test(String(text||''));
  if(target.invalid) return {all:[],upcoming:[],started:[],target:target,kind:kind,nowIntent:false,mine:mine};
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
  return {all:rows,upcoming:upcoming,started:started,target:target,kind:kind,nowIntent:nowIntent,mine:mine};
}
""",
    'meeting invalid handling',
)

block(
    'function aiMeetingRows(area,text,baseDate){',
    'function aiKoTime(h){',
    """function aiMeetingRows(area,text,baseDate){
  const info=aiMeetingInfo(area == null ? (S.area||'') : area,text||'',baseDate);
  if(info.target.invalid) return [];
  let rows;
  if(info.nowIntent) rows=info.started.slice().reverse();
  else if(info.target.isToday) rows=info.upcoming.slice();
  else rows=info.all.slice();
  return rows.slice(0,6);
}
""",
    'past meeting cards',
)

old = """function aiMeetingSummary(area,source,note,text,baseDate){
  const info=aiMeetingInfo(area,text||'',baseDate), target=info.target;
  const where=area?area+' 지역':'등록된 전체 지역';
  const prefix=note?note+'\\n':'';
  const via=source?source+'으로 ':'';
  const kind=info.kind?info.kind+' ':'';"""
new = """function aiMeetingSummary(area,source,note,text,baseDate){
  const info=aiMeetingInfo(area,text||'',baseDate), target=info.target;
  const where=area?area+' 지역':'등록된 전체 지역';
  const prefix=note?note+'\\n':'';
  const via=source?source+'으로 ':'';
  const kind=info.kind?info.kind+' ':'';
  if(target.invalid) return prefix+(target.error||'입력한 날짜를 확인해주세요.');"""
once(old, new, 'invalid meeting reply')

p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
old_cache = "const V = 'ohg-v900-social-ai-meeting-fix';"
if old_cache not in w:
    raise SystemExit('service worker baseline cache not found')
w = w.replace(old_cache, "const V = 'ohg-v900-ai-simulation-fixes';", 1)
sw.write_text(w, encoding='utf-8')
print('six fixes applied')
