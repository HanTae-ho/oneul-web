const fs = require('fs');
const path = require('path');

const root = __dirname;
const read = f => fs.readFileSync(path.join(root, f), 'utf8');
const index = read('index.html');
const sw = read('sw.js');
const test = read('test.js');
const fail = msg => { throw new Error('VERIFY: ' + msg); };
const ok = (cond, msg) => { if(!cond) fail(msg); console.log('OK - ' + msg); };

ok(/const BUILD = 'V5\.2';/.test(index), 'index BUILD = V5.2');
ok(/const APP_VERSION = 'V5\.2';/.test(sw), 'sw APP_VERSION = V5.2');
ok(/const V = 'ohg-v502';/.test(sw), 'sw cache = ohg-v502');
ok(/function recoveryDay\(from, to\)/.test(index), 'recoveryDay 함수 존재');
ok(/return from \? daysBetween\(from, to\) \+ 1 : 0;/.test(index), '회복 시작 당일을 1일째로 계산');
ok(/const t = typeOf\(k\), n = recoveryDay\(S\.dates\[k\]\);/.test(index), '홈 회복일 표시가 recoveryDay 사용');
ok(!/\.toISOString\s*\(/.test(test), '자동테스트에서 toISOString() 미사용');
ok(/timezoneId: 'Asia\/Seoul'/.test(test), '브라우저 회귀테스트 시간대 = Asia/Seoul');
ok(/recoveryDay\('2026-08-31', '2026-09-02'\)/.test(test), '8/31→9/2 = 3일째 테스트 포함');
ok(/2026-09-01T23:59:59\+09:00/.test(test) && /2026-09-02T00:00:00\+09:00/.test(test), '한국시간 자정 경계 테스트 포함');
ok(/다시 시작한 당일은 새 회복 1일째/.test(test), '다시 시작 당일 1일째 테스트 포함');

// 날짜 수학 자체도 독립 검증
const daySerial = v => {
  const m = String(v || '').match(/^(\d{4})-(\d{2})-(\d{2})$/);
  return m ? Math.floor(Date.UTC(+m[1], +m[2]-1, +m[3]) / 86400000) : NaN;
};
const daysBetween = (a,b) => Math.max(0, daySerial(b)-daySerial(a));
const recoveryDay = (a,b) => a ? daysBetween(a,b)+1 : 0;
ok(recoveryDay('2026-08-31','2026-08-31') === 1, '시작 당일 = 1일째');
ok(recoveryDay('2026-08-31','2026-09-01') === 2, '다음 날 = 2일째');
ok(recoveryDay('2026-08-31','2026-09-02') === 3, '8/31 시작, 9/2 = 3일째');

console.log('\nV5.2 핵심 검증 통과');
