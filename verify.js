const fs = require('fs');
const path = require('path');

const root = __dirname;
const read = f => fs.readFileSync(path.join(root, f), 'utf8');
const index = read('index.html');
const sw = read('sw.js');
const test = read('test.js');
const fail = msg => { throw new Error('VERIFY: ' + msg); };
const ok = (cond, msg) => { if(!cond) fail(msg); console.log('OK - ' + msg); };

ok(/const BUILD = 'V5\.3';/.test(index), 'index BUILD = V5.3');
ok(/const APP_VERSION = 'V5\.3';/.test(sw), 'sw APP_VERSION = V5.3');
ok(/const V = 'ohg-v503';/.test(sw), 'sw cache = ohg-v503');
ok(/function recoveryDay\(from, to\)/.test(index), 'recoveryDay 함수 유지');
ok(/return from \? daysBetween\(from, to\) \+ 1 : 0;/.test(index), '회복 시작 당일 1일째 규칙 유지');
ok(!/\.toISOString\s*\(/.test(test), '자동테스트에서 toISOString() 미사용 유지');
ok(/timezoneId: 'Asia\/Seoul'/.test(test), '브라우저 회귀테스트 시간대 = Asia/Seoul 유지');

const panicStart = index.indexOf('<section class="pg" id="p-panic">');
const panicEnd = index.indexOf('</section>', panicStart);
const panic = index.slice(panicStart, panicEnd);
const urge = panic.indexOf('id="pk-urge"');
const rx = panic.indexOf('id="pk-mindrx"');
const withdr = panic.indexOf('id="pk-with"');
const life = panic.indexOf('id="pk-life"');
ok(panicStart >= 0 && panicEnd > panicStart, '위기 화면 존재');
ok(/지금 어떤 도움이 필요한가요\?/.test(panic), '위기 화면 제목 변경');
ok(urge >= 0 && rx > urge && withdr > rx && life > withdr, '순서 = 충동 → 마음 처방전 → 몸 이상 → 죽고 싶어요');
ok(/id="go-read"/.test(panic) && /id="go-listen"/.test(panic), '마음 처방전에 도움글·듣는 글 버튼 존재');

const helpStart = index.indexOf('<section class="pg" id="p-help">');
const helpEnd = index.indexOf('</section>', helpStart);
const help = index.slice(helpStart, helpEnd);
ok(!/읽고 듣기/.test(help), '헬프 일반 목록에서 읽고 듣기 섹션 제거');
ok(!/id="go-read"/.test(help) && !/id="go-listen"/.test(help), '헬프에서 도움글·듣는 글 버튼 제거');
ok(/openRead\('panic'\)/.test(index) && /openListen\('panic'\)/.test(index), '마음 처방전에서 돌아가기는 위기 화면으로');
ok(/pk-mindrx/.test(test), '브라우저 회귀테스트에 마음 처방전 검증 포함');

console.log('\nV5.3 핵심 검증 통과');
