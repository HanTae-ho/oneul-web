const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = __dirname;
const read = f => fs.readFileSync(path.join(root, f), 'utf8');
const index = read('index.html');
const sw = read('sw.js');
const test = read('test.js');
const qaSrc = read('qa-data.js');
const feedbackGs = read('오늘한걸음_의견_v1.0.gs');
const resourcePatch = read('자원시트_v1.7_to_v1.8_FEEDBACK_URL_패치.txt');
const fail = msg => { throw new Error('VERIFY: ' + msg); };
const ok = (cond, msg) => { if(!cond) fail(msg); console.log('OK - ' + msg); };

ok(/const BUILD = 'V6\.1';/.test(index), 'index BUILD = V6.1');
ok(/const APP_VERSION = 'V6\.1';/.test(sw), 'sw APP_VERSION = V6.1');
ok(/const V = 'ohg-v601';/.test(sw), 'sw cache = ohg-v601');
ok(/'\.\/qa-data\.js'/.test(sw), '서비스워커가 qa-data.js 오프라인 캐시');
ok(/<script src="\.\/qa-data\.js"><\/script>/.test(index), 'index가 qa-data.js 로드');
ok(/function recoveryDay\(from, to\)/.test(index), 'recoveryDay 함수 유지');
ok(/return from \? daysBetween\(from, to\) \+ 1 : 0;/.test(index), '회복 시작 당일 1일째 규칙 유지');
ok(!/\.toISOString\s*\(/.test(test), '자동테스트에서 toISOString() 미사용 유지');
ok(/timezoneId: 'Asia\/Seoul'/.test(test), '브라우저 회귀테스트 시간대 = Asia/Seoul 유지');

const sandbox={window:{}}; vm.createContext(sandbox); vm.runInContext(qaSrc,sandbox);
const qa=sandbox.window.QA_ITEMS;
ok(Array.isArray(qa) && qa.length===224, 'Q&A 총 224문답');
ok(qa.filter(x=>!x.supplement).length===200, '원본 기반 Q1~Q200 = 200문답');
ok(qa.filter(x=>x.supplement).length===24, '공식기관 보완 Q201~Q224 = 24문답');
ok(qa.every((x,i)=>x.id===i+1), 'Q&A ID 1~224 연속');
const counts=Object.fromEntries(['알코올','도박','마약','공통','가족'].map(c=>[c,qa.filter(x=>x.cat===c).length]));
ok(counts['알코올']===80 && counts['도박']===18 && counts['마약']===15 && counts['공통']===9 && counts['가족']===102, 'Q&A 분류 수량 일치');
ok(/data-t="tools"/.test(index) && !/data-t="rec"/.test(index), '하단 기록 제거 + 회복도구 추가');
ok(/<b>내 발자취<\/b>/.test(index) && /id="me-trail-open"/.test(index), '내정보 → 내 발자취 진입 존재');
ok(/id="p-tools"/.test(index) && /id="p-qa"/.test(index) && /id="p-learn"/.test(index), '회복도구/Q&A/회복학습 화면 존재');
ok(/id="tool-check"/.test(index) && /V7\.0/.test(index), '자가점검 V7.0 준비 진입 존재');
ok(/navigator\.share/.test(index), '앱 추천하기 Web Share 지원');
ok(/id="me-share"/.test(index) && !/id="tool-share"/.test(index), '추천하기가 회복도구에서 내정보 앱 아래로 이동');
ok(/id="me-feedback-text"/.test(index) && /id="me-feedback-send"/.test(index), '앱에 바라는 점 = 단일 자유입력 + 보내기');
ok(/function feedbackEndpoint\(\)/.test(index) && /FEEDBACK_URL/.test(index), '별도 의견 서버 연결 코드 존재');
ok(/id="fb-ad-list"/.test(index) && /반영완료/.test(index), '관리자 의견 전체조회/처리상태 UI 존재');
ok(/MAKE_NEW_FEEDBACK_SHEET/.test(feedbackGs) && /FEEDBACK_ADMIN_KEY/.test(feedbackGs), '별도 의견 Apps Script = 시트 자동생성 + 관리자 키 보호');
ok(/FEEDBACK_URL/.test(resourcePatch) && /feedbackUrl/.test(resourcePatch), '자원시트 v1.7→v1.8 FEEDBACK_URL 연결 패치 존재');

const panicStart = index.indexOf('<section class="pg" id="p-panic">');
const panicEnd = index.indexOf('</section>', panicStart);
const panic = index.slice(panicStart, panicEnd);
const urge = panic.indexOf('id="pk-urge"');
const rx = panic.indexOf('id="pk-mindrx"');
const withdr = panic.indexOf('id="pk-with"');
const life = panic.indexOf('id="pk-life"');
ok(panicStart >= 0 && panicEnd > panicStart, '위기 화면 존재');
ok(urge >= 0 && rx > urge && withdr > rx && life > withdr, '위기 순서 유지 = 충동 → 마음 처방전 → 몸 이상 → 죽고 싶어요');

console.log('\nV6.1 핵심 검증 통과');
