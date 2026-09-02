const fs = require('fs');
const path = require('path');
const vm = require('vm');
const root=__dirname;
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const index=read('index.html'), sw=read('sw.js'), test=read('test.js');
const qaSrc=read('qa-data.js'), learningSrc=read('learning-data.js'), screeningSrc=read('screening-data.js');
const feedbackGs=read('오늘한걸음_의견_v1.0.gs'), resourceGs=read('오늘한걸음_자원시트_v1.8.gs');
const fail=m=>{throw new Error('VERIFY: '+m)}; const ok=(c,m)=>{if(!c)fail(m);console.log('OK - '+m)};

ok(/const BUILD = 'V7\.1';/.test(index),'index BUILD = V7.1');
ok(/const APP_VERSION = 'V7\.1';/.test(sw),'sw APP_VERSION = V7.1');
ok(/const V = 'ohg-v701';/.test(sw),'sw cache = ohg-v701');
['qa-data.js','learning-data.js','screening-data.js'].forEach(f=>{
  ok(sw.includes("'./"+f+"'"),'서비스워커가 '+f+' 오프라인 캐시');
  ok(index.includes('<script src="./'+f+'"></script>'),'index가 '+f+' 로드');
});
ok(/function recoveryDay\(from, to\)/.test(index) && /daysBetween\(from, to\) \+ 1/.test(index),'회복 시작 당일 1일째 규칙 유지');
ok(!/\.toISOString\s*\(/.test(test),'자동테스트에서 toISOString() 미사용 유지');
ok(/timezoneId: 'Asia\/Seoul'/.test(test),'기존 브라우저 회귀테스트 시간대 Asia/Seoul 유지');

let box={window:{}};vm.createContext(box);vm.runInContext(qaSrc,box);const qa=box.window.QA_ITEMS;
ok(Array.isArray(qa)&&qa.length===224,'Q&A 224문답 유지');
ok(qa.every(x=>{const n=x.a.split(/\n\s*\n/).filter(Boolean).length;return n>=2&&n<=3;}),'Q&A 답변 2~3문단 유지');
ok(/\.qadetail \.answer\{[^}]*font-size:16px;[^}]*line-height:1\.85/.test(index),'Q&A 상세 16px / 1.85 유지');

box={window:{}};vm.createContext(box);vm.runInContext(learningSrc,box);const learning=box.window.LEARNING_TOPICS;
ok(Array.isArray(learning)&&learning.length===1&&learning[0].id==='twelve-steps','회복학습 12단계 독립 구조 유지');
ok(learning[0].sections.length===13,'12단계 소개 + 1~12단계 13개 유지');

box={window:{}};vm.createContext(box);vm.runInContext(screeningSrc,box);const sc=box.window.SCREENING_TOOLS;
ok(Array.isArray(sc)&&sc.length===9,'자가점검 9개 도구 등록');
const qcount=Object.fromEntries(sc.map(x=>[x.id,x.questions.length]));
const expected={'audit-k':10,'pgsi':9,'dast-k10':10,'nds-bv':3,'nas-bv':3,'nss-bv':3,'internet-habit':28,'game-habit':30,'smartphone-habit':28};
ok(Object.entries(expected).every(([k,n])=>qcount[k]===n),'자가점검 도구별 문항 수 일치');
ok(sc.reduce((a,x)=>a+x.questions.length,0)===124,'자가점검 총 문항 데이터 124개');
const audit=sc.find(x=>x.id==='audit-k');
ok(audit.sexCutoff && audit.levelsMale[0].max===9 && audit.levelsFemale[0].max===5,'AUDIT-K 남/여 결과기준 분리');
const pgsi=sc.find(x=>x.id==='pgsi');
ok(pgsi.levels.map(x=>x.max).join(',')==='0,2,7,27','PGSI 0 / 1~2 / 3~7 / 8~27 구간');
const dast=sc.find(x=>x.id==='dast-k10');
ok(dast.levels.map(x=>x.max).join(',')==='0,2,5,8,10','DAST-Korean 0 / 1~2 / 3~5 / 6~8 / 9~10 구간');
ok(dast.options.length===2 && dast.options[0].l==='예' && dast.options[0].v===1 && dast.options[1].l==='아니오' && dast.options[1].v===0,'DAST-Korean 예=1 / 아니오=0 채점 방향');
const dastExact=[
  '의료상 필요한 경우 이외에 약물을 사용했습니까?',
  '한번에 두 가지 이상의 약물을 남용합니까?',
  '중단하기를 원할 때 약물 사용을 중단할 수 없습니까?',
  '약물 사용으로 인해 일시적 기억상실 또는 환각을 경험한 적이 있습니까?',
  '약물 사용에 대하여 나쁘다고 생각하거나 죄책감을 느낍니까?',
  '귀하의 약물 사용에 대해 배우자(또는 부모)가 불평한 적이 있습니까?',
  '약물 사용을 이유로 가족을 소홀히 한 적이 있습니까?',
  '약물을 입수하기 위해 불법적인 활동에 관여한 적이 있습니까?',
  '약물 복용을 중단했을 때 금단증상을 경험한 적이 있습니까?',
  '약물 사용으로 인해 의학적 문제(예: 기억상실, 간염, 경련, 출혈)를 겪은 적이 있습니까?'
];
ok(dast.questions.map(x=>x.q).join('\n')===dastExact.join('\n'),'DAST-Korean 10문항 2020 표준지침과 1:1 일치');
ok(['nds-bv','nas-bv','nss-bv'].every(id=>{const x=sc.find(y=>y.id===id);return x.min===0&&x.max===9&&x.levels[0].max===2;}),'우울·불안·스트레스 단축형 3문항·3점 절단 기준');
ok(sc.find(x=>x.id==='internet-habit').levels[0].max===40,'인터넷 고위험 기준: 정수점수 41점 이상');
ok(sc.find(x=>x.id==='game-habit').levels[0].max===38,'게임 고위험 기준: 정수점수 39점 이상');
ok(sc.find(x=>x.id==='smartphone-habit').levels[0].max===48,'스마트폰 고위험 기준: 49점 이상');

ok(/id="p-screening"/.test(index)&&/id="p-screen-test"/.test(index),'자가점검 목록/검사 화면 존재');
ok(/function drawScreening\(\)/.test(index)&&/function drawScreenTest\(\)/.test(index),'자가점검 실행 UI 함수 존재');
ok(/screenings: \[\]/.test(index)&&/답변 하나하나는 저장하지 않고/.test(index),'자가점검 결과 로컬 저장 + 문항응답 미저장');
ok(/function screeningStats\(\)/.test(index)&&/trendSvg\(tool,h\)/.test(index),'통계 점수 변화 + 꺾은선 그래프 존재');
ok(/function screenRetestText\(last\)/.test(index)&&/약 4주 후 다시 점검해볼 수 있습니다/.test(index),'최근 검사일·경과관찰 재점검 안내 존재');
ok(/id="screen-log-go"/.test(index)&&/id="screen-help-go"/.test(index)&&/id="screen-ai-go"/.test(index),'검사결과에서 기록·도움·마음프로 행동 연결');
ok(/검사 점수와 결과는 마음프로에 자동으로 전달되지 않습니다/.test(index),'마음프로 자동전송 방지 안내');
ok(/function screenRecentRows\(rows\)/.test(index)&&/screen-record-row/.test(index),'통계 최근 검사일·점수·결과구간 목록 존재');
ok(/이전보다/.test(index)&&/점수의 증가·감소/.test(index),'이전 점수 차이와 과잉해석 방지 문구 존재');
ok(/types\.includes\('etc'\)/.test(index),'기타 회복영역에서 인터넷·게임·스마트폰 점검 노출');
ok(/가족·보호자 모드에서는 당사자 대신/.test(index),'가족 모드에서 중독검사 대리응답 방지');
ok(/#top-me\{[^}]*width:40px;[^}]*border-radius:50%/.test(index),'사용자 아이콘 원형 40px 아바타 기반');
ok(/#top-me img\{[^}]*object-fit:cover/.test(index),'향후 프로필 이미지 삽입 가능한 아바타 CSS');

ok(/navigator\.share/.test(index),'추천하기 Web Share 유지');
ok(/id="me-feedback-text"/.test(index)&&/id="me-feedback-send"/.test(index),'앱에 바라는 점 유지');
ok(/MAKE_NEW_FEEDBACK_SHEET/.test(feedbackGs)&&/FEEDBACK_ADMIN_KEY/.test(feedbackGs),'의견 Apps Script 유지');
ok(/GS_VER\s*=\s*'v1\.8'/.test(resourceGs)&&/FEEDBACK_URL/.test(resourceGs),'자원시트 v1.8 유지');

console.log('\nV7.1 핵심 검증 통과');
