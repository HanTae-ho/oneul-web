const fs=require('fs'),path=require('path'),vm=require('vm');
const root=__dirname,read=f=>fs.readFileSync(path.join(root,f),'utf8');
const index=read('index.html'),feature=read('meaning-feature.js'),dataSrc=read('meaning-data.js'),workbook=read('workbook-data.js'),sw=read('sw.js');
const fail=m=>{throw new Error('VERIFY-MEANING: '+m)};
const ok=(c,m)=>{if(!c)fail(m);console.log('OK - '+m)};

let box={window:{}};vm.createContext(box);vm.runInContext(dataSrc,box);const md=box.window.MEANING_DATA;
ok(md&&md.ver===3,'의미 돌아보기 데이터 버전');
ok(Array.isArray(md.hard)&&md.hard.length===8,'오늘 아팠던 것 8개 칩');
ok(Array.isArray(md.strength)&&md.strength.length===8&&['hold','recoveryWill','hope','selfProtect','family','help','learning','restart'].every(k=>md.strength.some(x=>x.k===k)),'남아 있던 힘 8개 선택지·기존 키 보존');
ok(Array.isArray(md.action)&&md.action.length===8&&md.action.every(x=>x.value),'선택·행동 8개와 가치 매핑');
ok(md.values&&md.values.create==='창조'&&md.values.exp==='경험'&&md.values.att==='태도','창조·경험·태도 가치 매핑');
ok(Array.isArray(md.lines)&&md.lines.length===22&&md.lines.every(x=>x.id&&x.text&&Array.isArray(x.scope)&&x.scope.length),'오늘의 문장 22개·scope 계약');
const common=md.lines.filter(x=>x.scope.includes('all'));
ok(!common.some(x=>/(술|알코올|단주)/.test(x.text)),'공통 문장에 알코올 전용 표현 없음');
const allowed=types=>{const single=types.length===1?types[0]:'';return md.lines.filter(x=>x.scope.includes('all')||(single&&x.scope.includes(single)));};
ok(!allowed(['gambling']).some(x=>/(술|알코올|단주)/.test(x.text)),'도박 단일영역에 술·단주 문장 없음');
ok(!allowed(['drug']).some(x=>/(술|알코올|단주)/.test(x.text)),'약물 단일영역에 술·단주 문장 없음');
ok(allowed(['alcohol','gambling']).every(x=>x.scope.includes('all')),'복수 회복영역은 공통 문장만 사용');

ok(index.includes("const DATA_SCHEMA = 6;")&&index.includes("const KEY = 'ohg.v1';"),'DATA_SCHEMA 6·ohg.v1 유지');
ok(/wbDays: \{\}/.test(index)&&/if\(!s\.wbDays \|\| typeof s\.wbDays !== 'object'/.test(index),'wbDays 기본값·마이그레이션');
ok(!/window\.WB_BASE/.test(workbook),'12단계 workbook-data와 의미 데이터 분리');
ok(index.includes('<script src="./meaning-data.js"></script>')&&index.includes('<script src="./meaning-feature.js"></script>'),'의미 데이터·실행 로직 로드');
ok(sw.includes("'./meaning-data.js'")&&sw.includes("'./meaning-feature.js'"),'의미 파일 오프라인 캐시');

ok(index.includes('id="p-meaning"')&&index.includes('id="tool-meaning"')&&index.includes('id="ni-meaning"'),'회복도구·하루마무리 두 진입점');
ok(index.includes('id="mn-view-tabs"')&&index.includes('data-mn-view="today"')&&index.includes('data-mn-view="history"')&&index.includes('id="mn-view-history" class="hide"'),'의미 돌아보기 오늘·지난 기록 2탭');
ok(/function setMeaningView\(v\)/.test(feature)&&/setMeaningView\('today'\)/.test(feature),'의미 돌아보기 기본 오늘 탭·탭 전환 로직');
ok(index.includes('id="mn-hard"')&&index.includes('id="mn-strength"')&&index.includes('id="mn-action"')&&index.includes('id="mn-request"')&&index.includes('id="mn-lines"'),'의미 문항 구조 통일');
ok(feature.includes('[0,1,2,3,4].forEach')&&!index.includes('id="mn-empty-r"'),'공허감 0~4 다섯 단계·슬라이더 없음');
ok(index.includes('컷오프나 판정은 없습니다.'),'공허감 컷오프·판정 없음 안내');
ok(index.includes('직접 적은 글은 앱이 자동 분류하거나 점수화하지 않습니다.'),'직접입력 자동분류 금지 안내');

ok(/p==='meaning' && famMode\(\)/.test(index),'라우터 가족모드 직접 진입 차단');
ok(/\$\('#ni-meaning'\)\.style\.display = fam \? 'none' : ''/.test(index),'가족모드 하루마무리 우회 버튼 숨김');
ok(/night\.kept === 0 && niAfter !== 'meaning'/.test(index),'당사자가 의미 돌아보기를 선택하면 재발 안내보다 해당 진입을 우선');
ok(/if\(famMode\(\)\)\{go\('tools',\{replace:true\}\);return;\}/.test(feature),'의미 화면 자체 가족모드 이중 차단');
ok(/function wbAllowedLines\(\)/.test(feature)&&/areas\.length===1/.test(feature)&&/scopes\.includes\('all'\)/.test(feature),'단일영역 추가문장·복수영역 공통문장 필터');

ok(/function wbTodayUrges\(d\)/.test(feature)&&/Array\.isArray\(S\.urges\)/.test(feature)&&/ymd\(Number\(x\.t\)\)===d/.test(feature),'오늘 충동기록만 로컬 날짜 기준 참고 조회');
ok(/오늘 기록된 충동/.test(feature)&&/참고용/.test(feature)&&/의미기록에 복사 저장하지 않습니다/.test(feature)&&/go\('urge-diary'\)/.test(feature),'의미 화면에서 오늘 충동 요약·충동일기 이동');
const collected=(feature.match(/function meaningCollected\(\)\{([\s\S]*?)return \{any:/)||[])[1]||'';
ok(collected.includes("rec={hard:mnDraft.hard.slice(),strength:mnDraft.strength.slice(),action:mnDraft.action.slice(),ts:Date.now()}")&&!/rec\.urges|rec\.urge|urges\s*:|urge\s*:/.test(collected),'충동기록을 wbDays 의미기록에 중복 저장하지 않음');

ok(/function showMeaningExistingChoice\(d,r\)/.test(feature)&&/기존 기록 수정하기/.test(feature)&&/처음부터 다시 작성/.test(feature),'오늘 기존 의미기록 진입 시 수정·처음부터 다시 작성 선택');
ok(/mnReplaceExisting=true/.test(feature)&&/renderMeaningDraft\(d,null,true\)/.test(feature),'처음부터 다시 작성은 빈 초안으로 시작');
ok(/새 내용을 저장하기 전까지 기존 기록은 지워지지 않습니다/.test(feature)&&/새로 작성할 내용이 없습니다\. 기존 기록은 그대로 유지됩니다/.test(feature),'처음부터 다시 작성 중 기존 기록 선삭제 방지');
ok(/기존 오늘 기록을 바꿀까요/.test(feature)&&/saveMeaningRecord\(true\)/.test(feature),'새 내용 저장 직전에 기존 오늘 기록 교체 확인');

ok(/function drawMeaningHistorySummary\(\)/.test(feature)&&/자주 보인 힘/.test(feature)&&/자주 지킨 가치/.test(feature),'2단계 기록 다시보기: 힘·가치 흐름');
ok(/strengthCount/.test(feature)&&/valueCount/.test(feature)&&/a\.value/.test(feature),'2단계 집계는 선택형 힘·행동 가치 키 기반');
ok(/직접 적은 글은 분류하거나 점수화하지 않습니다/.test(feature),'2단계 자유입력 비분류 원칙 표시');
ok(!/남긴 기록 ['"+]?\+?[^\n]{0,30}일/.test(index+feature)&&!/(지난 기록 모두 보기 ·|지난 기록 보기 ·)/.test(index+feature),'기록일수 전면 표시 없음');
ok(!/streak|연속\s*\d+\s*일|Day\s*\d+/i.test(feature),'2단계 streak·Day 숫자 없음');
ok(/getFullYear\(\)\+'년 '/.test(feature),'지난 기록 날짜에 연도 표시');

ok(/function meaningCollected\(\)/.test(feature)&&/if\(!x\.any\)/.test(feature),'빈 기록 저장 방지');
ok(/st\[d\]=x\.rec;save\(\)/.test(feature),'같은 날짜 키에 upsert 저장');
ok(!/toISOString\(/.test(feature)&&/function wbToday\(\)\{return ymd\(new Date\(\)\);\}/.test(feature),'로컬 ymd 날짜 사용·UTC 날짜 변환 없음');
ok(/hardNote/.test(feature)&&/strengthNote/.test(feature)&&/actionNote/.test(feature)&&/request/.test(feature),'직접입력은 별도 원문 필드로 저장');

console.log('\nV9.0.13 의미 돌아보기·기록 다시보기 회귀검증 통과');
