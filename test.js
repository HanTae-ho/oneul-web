const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');

const MIME = { '.html':'text/html', '.js':'text/javascript', '.json':'application/json', '.png':'image/png' };
const srv = http.createServer((req, res) => {
  let p = req.url.split('?')[0];
  if (p === '/') p = '/index.html';
  const f = path.join(__dirname, p);
  if (!fs.existsSync(f)) { res.writeHead(404); res.end('no'); return; }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'text/plain' });
  res.end(fs.readFileSync(f));
});

(async () => {
  await new Promise(r => srv.listen(8899, r));
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2,
    locale: 'ko-KR', timezoneId: 'Asia/Seoul' });
  const pg = await ctx.newPage();

  const errs = [];
  pg.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  pg.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });

  const shot = async n => { await pg.screenshot({ path: `${__dirname}/shot-${n}.png`, fullPage: true }); };
  const seen = async () => await pg.$eval('.pg.on', e => e.id);
  const localYmd = d => {
    const z = n => String(n).padStart(2, '0');
    return d.getFullYear() + '-' + z(d.getMonth()+1) + '-' + z(d.getDate());
  };
  const daysAgo = n => {
    const d = new Date();
    d.setHours(12, 0, 0, 0);
    d.setDate(d.getDate() - n);
    return localYmd(d);
  };
  const assert = (ok, msg) => { if(!ok) throw new Error('ASSERT: ' + msg); };

  await pg.goto('http://localhost:8899/index.html');
  await pg.waitForTimeout(500);
  console.log('1. 첫 화면 =', await seen());
  await shot('1-intro');

  // 온보딩: 알코올 + 도박
  await pg.click('#ob-types button:nth-child(1)');
  await pg.click('#ob-types button:nth-child(2)');
  await pg.waitForTimeout(150);
  // 시작일을 40일 전으로
  const d40 = daysAgo(40);
  const ins = await pg.$$('#ob-dates input');
  await ins[0].fill(d40);
  await ins[1].fill(daysAgo(12));
  await shot('2-onboard');
  await pg.click('#ob-go');
  await pg.waitForTimeout(300);
  console.log('2. 시작 후 =', await seen());
  const recoveryText = (await pg.$eval('#home-days', e => e.innerText)).replace(/\n/g, ' | ');
  console.log('   회복일 =', recoveryText);
  assert(recoveryText.includes('41일째'), '40일 전 시작은 오늘 41일째여야 함');
  assert(recoveryText.includes('13일째'), '12일 전 시작은 오늘 13일째여야 함');
  const dayRule = await pg.evaluate(() => ({
    start: recoveryDay(today(), today()),
    fixed: recoveryDay('2026-08-31', '2026-09-02'),
    before: ymd(new Date('2026-09-01T23:59:59+09:00')),
    after: ymd(new Date('2026-09-02T00:00:00+09:00'))
  }));
  console.log('   날짜 경계 =', dayRule);
  assert(dayRule.start === 1, '회복 시작 당일은 1일째');
  assert(dayRule.fixed === 3, '8/31 시작이면 9/2는 3일째');
  assert(dayRule.before === '2026-09-01' && dayRule.after === '2026-09-02', '한국시간 자정에서 날짜가 바뀌어야 함');
  console.log('   매일의 명상 =', (await pg.$eval('#home-daily-text', e => e.innerText)).slice(0, 80));

  // HALT + 감정
  await pg.click('#home-halt button:nth-child(1)');
  await pg.click('#home-halt button:nth-child(3)');
  await pg.click('#home-mood button:nth-child(4)');
  await pg.waitForTimeout(200);
  console.log('3. HALT 팁 =', (await pg.$eval('#halt-tip', e => e.innerText)).slice(0, 40));
  await shot('3-home');

  // 위기 분기
  await pg.click('#panic');
  await pg.waitForTimeout(200);
  console.log('4. 위기 분기 =', await seen());
  assert(await pg.isVisible('#pk-mindrx'), '위기 화면에 마음 처방전 카드가 보여야 함');
  assert(await pg.isVisible('#go-read') && await pg.isVisible('#go-listen'), '마음 처방전에 도움글·듣는 글 버튼이 보여야 함');
  const panicOrder = await pg.$$eval('#p-panic > *', els => els.map(e => e.id).filter(Boolean));
  assert(panicOrder.indexOf('pk-urge') < panicOrder.indexOf('pk-mindrx') && panicOrder.indexOf('pk-mindrx') < panicOrder.indexOf('pk-with') && panicOrder.indexOf('pk-with') < panicOrder.indexOf('pk-life'), '위기 도움 순서가 충동→마음 처방전→몸 이상→죽고 싶어요여야 함');
  await shot('4-panic');

  // 금단 모달
  await pg.click('#pk-with');
  await pg.waitForTimeout(250);
  console.log('5. 금단 모달 tel =', await pg.$$eval('#modin a', a => a.map(x => x.getAttribute('href')).join(', ')));
  await shot('5-withdrawal');
  await pg.evaluate(() => closeModal()); await pg.waitForTimeout(200);

  // 자살위기 모달
  await pg.click('#pk-life'); await pg.waitForTimeout(250);
  console.log('6. 위기 모달 tel =', await pg.$$eval('#modin a', a => a.map(x => x.getAttribute('href')).join(', ')));
  await pg.evaluate(() => closeModal()); await pg.waitForTimeout(200);

  // 충동 대응
  await pg.click('#pk-urge'); await pg.waitForTimeout(250);
  console.log('7. 충동 화면 =', await seen());
  await pg.fill('#ur-r', '8');
  await pg.$eval('#ur-r', e => e.dispatchEvent(new Event('input', { bubbles: true })));
  await pg.click('#ur-th button:nth-child(1)');
  await pg.click('#ur-th button:nth-child(4)');
  await shot('6-urge');

  // 타이머 — 시간을 앞당겨 종료시킨다
  await pg.click('#ur-start'); await pg.waitForTimeout(400);
  console.log('8. 타이머 =', await seen(), '|', await pg.$eval('#tm-t', e => e.textContent));
  await pg.click('#tm-breath'); await pg.waitForTimeout(300);
  console.log('   호흡 =', await pg.$eval('#bc', e => e.textContent), await pg.$eval('#bc', e => e.className));
  await shot('7-timer');

  await pg.evaluate(() => { tm.end = Date.now() + 400; });
  await pg.waitForTimeout(1200);
  console.log('9. 종료 화면 =', await seen(), '|', await pg.$eval('#af-h', e => e.textContent));

  await pg.fill('#af-r', '3');
  await pg.$eval('#af-r', e => e.dispatchEvent(new Event('input', { bubbles: true })));
  await pg.waitForTimeout(150);
  console.log('   비교문 =', (await pg.$eval('#af-cmp', e => e.innerText)).slice(0, 46));
  await shot('8-after');
  await pg.click('#af-done'); await pg.waitForTimeout(300);
  console.log('10. 마친 후 =', await seen());

  // 자기 전
  await pg.click('#go-night'); await pg.waitForTimeout(250);
  await pg.click('#ni-mood button:nth-child(2)');
  await pg.click('#ni-urge button:nth-child(2)');
  await pg.click('#ni-kept button:nth-child(1)');
  await pg.fill('#ni-note', '오늘은 잘 넘겼다');
  await shot('9-night');
  await pg.click('#ni-save'); await pg.waitForTimeout(300);
  console.log('11. 자기 전 저장 후 =', await seen());

  // 가짜 데이터 넣고 통계 확인
  await pg.evaluate(() => {
    const now = Date.now();
    for (let i = 0; i < 22; i++) {
      const t = now - Math.floor(Math.random() * 20) * 86400000;
      const d = new Date(t); d.setHours([19,20,21,20,22,15,20][i % 7], 30);
      const b = 4 + Math.floor(Math.random() * 6);
      S.urges.push({ t: d.getTime(), type: 'alcohol', b: b, a: Math.max(0, b - 1 - Math.floor(Math.random()*3)),
        sec: 300 + Math.floor(Math.random()*900),
        th: [['딱 한 잔만','이번 한 번만','괜찮을 것 같다','나는 조절할 수 있다'][i % 4]] });
      S.halts.push({ t: d.getTime(), v: [['h'],['l','t'],['a'],['l'],['t','l']][i % 5] });
      S.moods.push({ t: now - i * 86400000, v: 1 + (i * 3) % 5 });
      if (i % 5 === 0) S.nights.push({ t: now - i * 86400000, m: 3, u: 1, k: 1, n: '' });
    }
    S.relapses.push({ t: now - 12 * 86400000, type: 'gambling', halt: ['l','t'], n: '혼자 있는 밤에 무너졌다' });
    save();
  });

  // 회복도구 — Q&A 224문답은 AI 없이 로컬에서 검색
  await pg.click('#tabs button[data-t="tools"]'); await pg.waitForTimeout(250);
  assert(await pg.isVisible('#tool-qa'), '하단 회복도구가 열려야 함');
  assert(!(await pg.$('#tool-share')), '회복도구에서 추천하기가 빠져야 함');
  assert(await pg.evaluate(() => Array.isArray(window.QA_ITEMS) && window.QA_ITEMS.length === 224), 'Q&A가 224문답이어야 함');
  await pg.click('#tool-qa'); await pg.waitForTimeout(250);
  assert((await pg.$eval('#qa-count', e => e.innerText)).includes('224'), 'Q&A 전체 224개 표시');
  await pg.fill('#qa-search', '갈망'); await pg.waitForTimeout(200);
  assert((await pg.$$eval('#qa-list .qaitem', a => a.length)) > 0, 'Q&A 갈망 검색 결과 존재');
  await pg.click('#qa-list .qaitem'); await pg.waitForTimeout(150);
  assert(await pg.isVisible('#qa-one .qadetail'), 'Q&A 상세 답변 표시');
  await shot('10-tools-qa');

  // 기록은 하단에서 내정보 → 내 발자취로 이동
  await pg.click('#tabs button[data-t="home"]'); await pg.waitForTimeout(150);
  await pg.click('#top-me'); await pg.waitForTimeout(250);
  assert(await pg.isVisible('#me-share'), '내정보에 독립 추천하기 항목 존재');
  assert(await pg.$('#me-feedback-send'), '내정보에 앱에 바라는 점 단일 입력 존재');
  await pg.locator('#p-me .acc-h', {hasText:'내 발자취'}).click(); await pg.waitForTimeout(120);
  assert(await pg.isVisible('#me-trail-open'), '내정보에 내 발자취 진입 버튼 존재');
  await pg.click('#me-trail-open'); await pg.waitForTimeout(300);
  assert((await pg.$eval('#p-rec h1', e => e.innerText)) === '내 발자취', '기록 화면 명칭은 내 발자취');
  await shot('11-trail-mood');
  const rt = async i => { await pg.click(`#rec-tab button:nth-child(${i})`); await pg.waitForTimeout(300); };
  await rt(2); await shot('12-trail-urge');
  await rt(5); console.log('   다시시작 탭 =', (await pg.$eval('#rec-body', e => e.innerText)).replace(/\n+/g,' / ').slice(0,80));
  await rt(6);
  console.log('12. 통계 =', (await pg.$eval('#rec-body', e => e.innerText)).replace(/\n+/g, ' / ').slice(0, 200));
  await shot('13-trail-stat');

  // 도움
  await pg.click('#tabs button[data-t="help"]'); await pg.waitForTimeout(300);
  console.log('13. 핫라인 =', await pg.$$eval('#help-lines a', a => a.map(x => x.getAttribute('href')).join(' ')));
  await shot('13-help');

  // 마음프로 Local-first — AI 서버 없이 앱 데이터 설명 + 위치 불일치 선택
  await ctx.grantPermissions(['geolocation'], { origin: 'http://localhost:8899' });
  await ctx.setGeolocation({ latitude: 35.1796, longitude: 129.0756 }); // 부산
  await pg.evaluate(() => {
    S.aiConsent = 1; S.area = '광주';
    S.res = S.res || {};
    S.res.groups = [{ n:'테스트 회복모임', y:DAYN[new Date().getDay()], h:'', a:'광주', d:'테스트 일정', t:'000-0000' }];
    save(); go('ai'); drawAI();
  });
  await pg.evaluate(() => aiSend('오늘 참여할 수 있는 모임 알려줘', 'meeting'));
  await pg.waitForTimeout(900);
  console.log('14. 마음프로 위치 비교 =', await pg.evaluate(() => ai.loc && ai.loc.state),
    '|', (await pg.$eval('#ai-resource', e => e.innerText)).replace(/\n+/g,' / ').slice(0,120));
  await pg.evaluate(() => aiSend('광주 오늘 참여할 수 있는 모임 알려줘', 'meeting'));
  await pg.waitForTimeout(500);
  console.log('    Local-first 설명 =', (await pg.$eval('#ai-thread', e => e.innerText)).replace(/\n+/g,' / ').slice(-220));
  console.log('    AI 전송 제외 =', await pg.evaluate(() => S.aiChat.filter(x => x.role === 'user').slice(-1)[0].local === 1));
  await shot('14-ai-local');

  // 내 정보 — 상단 내정보 아이콘은 홈에서 연다
  await pg.click('#tabs button[data-t="home"]'); await pg.waitForTimeout(150);
  await pg.click('#top-me'); await pg.waitForTimeout(300);
  await shot('15-me');

  // 다시 시작 흐름 — 누적 유지 확인
  await pg.click('#tabs button[data-t="home"]'); await pg.waitForTimeout(250);
  const before = await pg.$eval('#home-days', e => e.innerText.replace(/\n/g, ' | '));
  await pg.click('#go-relapse'); await pg.waitForTimeout(250);
  await pg.click('#rl-halt button:nth-child(3)');
  await pg.click('#rl-save'); await pg.waitForTimeout(300);
  console.log('14. 다시 시작 모달 =', (await pg.$eval('#modin', e => e.innerText)).slice(0, 60).replace(/\n/g,' '));
  await shot('16-relapse');
  await pg.evaluate(() => closeModal()); await pg.waitForTimeout(200);
  await pg.click('#tabs button[data-t="home"]'); await pg.waitForTimeout(250);
  console.log('    전 :', before);
  const afterReset = await pg.$eval('#home-days', e => e.innerText.replace(/\n/g, ' | '));
  console.log('    후 :', afterReset);
  assert(afterReset.includes('1일째'), '다시 시작한 당일은 새 회복 1일째여야 함');

  // 다크 모드 — 내정보 → 앱 → 화면 설정
  await pg.click('#top-me'); await pg.waitForTimeout(250);
  const accs = await pg.$$('#p-me .acc');
  await accs[2].click('.acc-h'); await pg.waitForTimeout(150);
  await pg.click('#me-theme [data-theme="dark"]'); await pg.waitForTimeout(300);
  await shot('17-dark');
  await pg.click('#me-theme [data-theme="light"]'); await pg.waitForTimeout(200);
  await pg.click('#tabs button[data-t="home"]'); await pg.waitForTimeout(200);

  // 새로고침 후에도 남아 있는지
  await pg.reload(); await pg.waitForTimeout(600);
  console.log('15. 새로고침 후 =', await seen(), '|', (await pg.$eval('#home-days', e => e.innerText)).replace(/\n/g, ' '));

  console.log('\n=== 오류 ===');
  console.log(errs.length ? errs.join('\n') : '없음');

  await b.close(); srv.close();
})();
