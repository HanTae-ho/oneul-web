from pathlib import Path
import subprocess

s = Path('index.html').read_text(encoding='utf-8')

def part(a, b):
    return s[s.index(a):s.index(b, s.index(a))]

blocks = [
    part('function aiCrisisKind', 'function aiCrisisBox'),
    part('function aiAddLocalDays', 'function aiMeetingPayload'),
    part('function aiTimerMinutes', 'function aiTimerClearTick'),
    part('function aiVoiceCommand', 'function aiCrisisKind'),
    part('function aiCanRetry', 'async function aiRequestOnce'),
    part('function aiLocalIntent', 'function aiKnowledgeReply'),
]

pre = r'''
const DAYN=['일','월','화','수','목','금','토'];
const pad=n=>String(n).padStart(2,'0');
const ymd=v=>{const d=new Date(v);return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate());};
let S={res:{groups:[
  {n:'AA 수요일 저녁',y:'수',h:'19:00',a:'광주',k:'알코올',d:'AA'},
  {n:'AA 수요일 밤',y:'수',h:'21:00',a:'광주',k:'알코올',d:'AA'},
  {n:'AA 목요일',y:'목',h:'19:00',a:'광주',k:'알코올',d:'AA'},
  {n:'GA 목요일',y:'목',h:'20:00',a:'광주',k:'도박',d:'GA'},
  {n:'NA 목요일',y:'목',h:'18:00',a:'광주',k:'약물',d:'NA'},
  {n:'SMART 목요일',y:'목',h:'17:00',a:'광주',k:'',d:'SMART Recovery'}
]},area:'광주',types:['alcohol']};
const FAMILY=[], GROUPS=[];
const famMode=()=>false;
const rowKind=r=>r.k||'';
const myKinds=()=>['알코올'];
const areasOf=r=>r.a?[r.a]:[];
'''

regression = r'''
let N=0;
function ok(v,msg){N++;if(!v)throw new Error(msg);}
function eq(a,b,msg){ok(a===b,msg+' | got='+a+' expected='+b);}
const wed=new Date(2026,8,9,20,0,0,0);
const fri=new Date(2026,8,11,20,0,0,0);

ok(aiCalendarReply('오늘은 며칠이야',wed).includes('2026년 9월 9일 수요일'),'today');
ok(aiCalendarReply('내일이 무슨 요일이야',wed).includes('2026년 9월 10일 목요일'),'tomorrow');
ok(aiCalendarReply('어제 날짜가 뭐야',wed).startsWith('어제는 2026년 9월 8일 화요일'),'yesterday particle');
ok(aiCalendarReply('모레 날짜 알려줘',wed).startsWith('모레는 2026년 9월 11일 금요일'),'day-after particle');
eq(aiMeetingDateTarget('어제 모임 보여줘',wed).ymd,'2026-09-08','yesterday meeting');
eq(aiMeetingDateTarget('이번 주 목요일 모임',fri).ymd,'2026-09-10','this-week past weekday');
eq(aiMeetingDateTarget('다음 주 목요일 모임',fri).ymd,'2026-09-17','next-week weekday');
eq(aiMeetingDateTarget('지난 주 목요일 모임',fri).ymd,'2026-09-03','last-week weekday');
eq(aiMeetingDateTarget('목요일 모임',fri).ymd,'2026-09-17','bare next weekday');
eq(aiMeetingDateTarget('1월 1일 모임',wed).ymd,'2027-01-01','omitted year rolls forward');
ok(aiMeetingDateTarget('2월 30일 모임',wed).invalid,'invalid Feb 30');
ok(aiMeetingDateTarget('13월 1일 모임',wed).invalid,'invalid month 13');
ok(aiMeetingSummary('광주','','','2월 30일 모임',wed).includes('존재하지 않습니다'),'invalid date answer');

eq(aiMeetingKindQuery('AA 모임 어디야'),'알코올','AA');
eq(aiMeetingKindQuery('GA 모임'),'도박','GA');
eq(aiMeetingKindQuery('NA 모임'),'약물','NA');
eq(aiMeetingKindQuery('SMART Recovery 모임'),'SMART','SMART');
let rows=aiMeetingRows('광주','내일 AA 모임',wed); ok(rows.length===1&&rows[0].n==='AA 목요일','tomorrow AA only');
rows=aiMeetingRows('광주','내일 GA 모임',wed); ok(rows.length===1&&rows[0].n==='GA 목요일','tomorrow GA only');
rows=aiMeetingRows('광주','내일 SMART Recovery 모임',wed); ok(rows.length===1&&rows[0].n==='SMART 목요일','tomorrow SMART only');
eq(aiMeetingRows('광주','오늘 모임',new Date(2026,8,9,23,0,0,0)).length,0,'no past fallback');
ok(aiMeetingSummary('광주','','','지금 하고 있는 AA 모임이 어디야',wed).includes('종료시간 정보는 없어'),'current meeting uncertainty');

['AA 모임이 싫어요','AA 모임이 부담스러워요','GA 모임에서 싸웠어요','NA 모임을 그만 가고 싶어요','SMART Recovery 모임이 나랑 안 맞는 것 같아','어제 AA 모임에서 속상했어','GA 모임 사람 때문에 화가 나요'].forEach(x=>eq(aiLocalIntent(x,''),'','counselling: '+x));
['AA 모임 있어?','AA 모임 어디야','GA 모임 시간 알려줘','NA 모임 찾고 싶어','SMART Recovery 모임 추천해줘','목요일에 열리는 모임 있어?','내일 모임 보여줘','나에게 맞는 모임은 뭐야','어떤 모임이 좋을까','모임 몇 시에 있어?'].forEach(x=>eq(aiLocalIntent(x,''),'meeting','search: '+x));

eq(aiTimerMinutes('5분 같이 버텨줘',''),5,'5m'); eq(aiTimerMinutes('10분만 견뎌보자',''),10,'10m'); eq(aiTimerMinutes('3분 같이 있어줘',''),3,'3m'); eq(aiTimerMinutes('20분 타이머',''),20,'20m'); eq(aiTimerMinutes('30분 기다려',''),30,'30m'); eq(aiTimerMinutes('31분 같이 버텨줘',''),0,'over max'); eq(aiTimerMinutes('5분 후 약 알림',''),0,'not timer'); eq(aiTimerMinutes('같이 버텨줘','timer'),5,'topic default');

eq(aiCrisisKind('죽고 싶어요'),'life','life'); eq(aiCrisisKind('자해하고 싶다'),'life','self harm'); eq(aiCrisisKind('경련이 와요'),'withdrawal','withdrawal'); eq(aiCrisisKind('환각이 보여'),'withdrawal','hallucination'); eq(aiCrisisKind('칼로 죽이겠어'),'violence','violence'); eq(aiCrisisKind('그냥 힘들어요'),'','distress');

eq(aiVoiceCommand('그만 읽어'),'off','voice off'); eq(aiVoiceCommand('계속 읽어줘'),'on','voice on'); eq(aiVoiceCommand('오늘 모임 읽어줘'),'','content not voice mode');
['NETWORK_ERROR','INVALID_JSON','TEMPORARY','UPSTREAM_BUSY'].forEach(c=>ok(aiCanRetry(c),'retry '+c));
['AUTH','CONFIG','BAD_REQUEST','RATE_LIMIT','SERVER_ERROR','QUOTA'].forEach(c=>ok(!aiCanRetry(c),'no retry '+c));
ok(!aiErrorMessage('SERVER_ERROR').includes('한 번 자동으로 다시 시도'),'retry wording');
console.log('REGRESSION_SCENARIOS_PASS',N);
'''

adversarial = r'''
let N=0; function ok(v,msg){N++;if(!v)throw new Error(msg);}
const names=['AA','GA','NA','SMART Recovery'];
const feelings=['모임이 싫어요','모임이 부담돼요','모임에서 싸웠어요','모임 사람 때문에 속상해요','모임을 그만 가고 싶어요','모임이 나랑 안 맞아요','모임에서 외로웠어요','모임 생각만 해도 긴장돼요'];
names.forEach(n=>feelings.forEach(f=>ok(aiLocalIntent(n+' '+f,'')!=='meeting','false positive '+n+' '+f)));
const asks=['모임 있어?','모임 어디야?','모임 시간 알려줘','모임 찾아줘','모임 몇 시야?','모임 추천해줘','모임 열려 있어?','모임 목록 보여줘'];
names.forEach(n=>asks.forEach(a=>ok(aiLocalIntent(n+' '+a,'')==='meeting','search miss '+n+' '+a)));
const monday=new Date(2026,8,7,12,0,0,0);
for(let cur=0;cur<7;cur++){
  const base=new Date(monday); base.setDate(monday.getDate()+cur);
  for(let target=0;target<7;target++){
    const jsDay=(target+1)%7, ko=DAYN[jsDay];
    const thisT=aiMeetingDateTarget('이번 주 '+ko+'요일 모임',base);
    const nextT=aiMeetingDateTarget('다음 주 '+ko+'요일 모임',base);
    const curMon=(base.getDay()+6)%7;
    const expectedThis=new Date(base); expectedThis.setDate(base.getDate()+(target-curMon));
    const expectedNext=new Date(base); expectedNext.setDate(base.getDate()+((7-curMon)+target));
    ok(thisT.ymd===ymd(expectedThis),'this week '+ymd(base)+' '+ko);
    ok(nextT.ymd===ymd(expectedNext),'next week '+ymd(base)+' '+ko);
  }
}
['2월 30일','2월 31일','4월 31일','6월 31일','9월 31일','11월 31일','0월 1일','13월 1일','1월 0일','1월 32일','2025년 2월 29일','2026년 2월 29일','2026년 13월 2일','2026년 4월 31일'].forEach(x=>ok(aiMeetingDateTarget(x+' 모임',new Date(2026,8,9)).invalid,'invalid accepted '+x));
['2024년 2월 29일','2028년 2월 29일','2026년 1월 31일','2026년 4월 30일','2026년 6월 30일','2026년 9월 30일','2026년 11월 30일','2026년 12월 31일'].forEach(x=>ok(!aiMeetingDateTarget(x+' 모임',new Date(2026,8,9)).invalid,'valid rejected '+x));
const timerWords=['버텨줘','버텨보자','버틸래','견뎌줘','견딜게','타이머','기다려','같이 있어줘','같이 버텨줘','같이 견뎌보자'];
timerWords.forEach((w,i)=>{const m=(i%10)+1;ok(aiTimerMinutes(m+'분 '+w,'')===m,'timer '+w);ok(aiTimerMinutes('약 '+m+'분 후 알림','')===0,'non timer '+i);});
console.log('ADVERSARIAL_SIMULATION_PASS',N);
'''

Path('/tmp/regression.js').write_text(pre + '\n' + '\n'.join(blocks) + '\n' + regression, encoding='utf-8')
Path('/tmp/adversarial.js').write_text(pre + '\n' + '\n'.join(blocks) + '\n' + adversarial, encoding='utf-8')
subprocess.run(['node', '/tmp/regression.js'], check=True)
subprocess.run(['node', '/tmp/adversarial.js'], check=True)
