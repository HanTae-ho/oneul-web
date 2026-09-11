const fs=require('fs'),path=require('path'),vm=require('vm');
const root=__dirname,read=f=>fs.readFileSync(path.join(root,f),'utf8');
const index=read('index.html'),feature=read('meaning-feature.js'),dataSrc=read('meaning-data.js'),workbook=read('workbook-data.js'),sw=read('sw.js');
const fail=m=>{throw new Error('VERIFY-MEANING: '+m)};
const ok=(c,m)=>{if(!c)fail(m);console.log('OK - '+m)};

let box={window:{}};vm.createContext(box);vm.runInContext(dataSrc,box);const md=box.window.MEANING_DATA;
ok(md&&md.ver===2,'의미 돌아보기 데이터 버전');
ok(Array.isArray(md.hard)&&md.hard.length===8,'오늘 아팠던 것 8개 칩');
ok(Array.isArray(md.strength)&&md.strength.length>=3,'남아 있던 힘 선택지');
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
ok(index.includes('id="mn-hard"')&&index.includes('id="mn-strength"')&&index.includes('id="mn-action"')&&index.includes('id="mn-request"')&&index.includes('id="mn-lines"'),'의미 문항 구조 통일');
ok(feature.includes('[0,1,2,3,4].forEach')&&!index.includes('id="mn-empty-r"'),'공허감 0~4 다섯 단계·슬라이더 없음');
ok(index.includes('컷오프나 판정은 없습니다.'),'공허감 컷오프·판정 없음 안내');
ok(index.includes('직접 적은 글은 앱이 자동 분류하거나 점수화하지 않습니다.'),'직접입력 자동분류 금지 안내');

ok(/p==='meaning' && famMode\(\)/.test(index),'라우터 가족모드 직접 진입 차단');
ok(/\$\('#ni-meaning'\)\.style\.display = fam \? 'none' : ''/.test(index),'가족모드 하루마무리 우회 버튼 숨김');
ok(/if\(famMode\(\)\)\{go\('tools',\{replace:true\}\);return;\}/.test(feature),'의미 화면 자체 가족모드 이중 차단');
ok(/function wbAllowedLines\(\)/.test(feature)&&/areas\.length===1/.test(feature)&&/scopes\.includes\('all'\)/.test(feature),'단일영역 추가문장·복수영역 공통문장 필터');

ok(!/남긴 기록 ['"+]?\+?[^\n]{0,30}일/.test(index+feature)&&!/(지난 기록 모두 보기 ·|지난 기록 보기 ·)/.test(index+feature),'기록일수 전면 표시 없음');
ok(/getFullYear\(\)\+'년 '/.test(feature),'지난 기록 날짜에 연도 표시');
ok(/const any=mnDraft\.hard\.length[\s\S]{0,500}mnDraft\.line/.test(feature)&&/if\(!any\)\{if\(st\[d\]\)\{delete st\[d\]/.test(feature),'빈 기록 미생성·기존 기록 모두 비우면 삭제');
ok(/st\[d\]=rec;save\(\)/.test(feature),'같은 날짜 키에 upsert 저장');
ok(!/toISOString\(/.test(feature)&&/function wbToday\(\)\{return ymd\(new Date\(\)\);\}/.test(feature),'로컬 ymd 날짜 사용·UTC 날짜 변환 없음');
ok(/hardNote/.test(feature)&&/strengthNote/.test(feature)&&/actionNote/.test(feature)&&/request/.test(feature),'직접입력은 별도 원문 필드로 저장');

console.log('\nV9.0.11 의미 돌아보기 회귀검증 통과');
