const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');

const MIME = { '.html':'text/html', '.js':'text/javascript', '.json':'application/json', '.png':'image/png' };
const srv = http.createServer((req, res) => {
  let p = req.url.split('?')[0];
  if (p === '/') p = '/index.html';
  const f = path.join(__dirname, p);
  if (!fs.existsSync(f)) { console.error('TEST HTTP404:', p); res.writeHead(404); res.end('no'); return; }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'text/plain' });
  res.end(fs.readFileSync(f));
});

(async () => {
  await new Promise(r => srv.listen(8899, r));
  const launchOpts = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {};
  const b = await chromium.launch(launchOpts);
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2,
    locale: 'ko-KR', timezoneId: 'Asia/Seoul' });
  const pg = await ctx.newPage();

  const errs = [];
  pg.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  // 결정론적 회귀검사에서는 외부 서비스의 일시적 4xx를 JS 오류로 오인하지 않습니다.
  // 대신 localhost의 4xx/5xx는 별도로 실패 처리해 앱 자체의 누락 자원은 계속 잡습니다.
  pg.on('response', r => {
    try {
      const u = new URL(r.url());
      if ((u.hostname === 'localhost' || u.hostname === '127.0.0.1') && r.status() >= 400) {
        errs.push('LOCAL HTTP ' + r.status() + ': ' + u.pathname);
      }
    } catch (_) {}
  });
  pg.on('console', m => {
    if (m.type() !== 'error') return;
    const text = m.text();
    if (text.startsWith('Failed to load resource:')) return;
    errs.push('CONSOLE: ' + text);
  });

  const shot = async n => { await pg.screenshot({ path: `${__dirname}/shot-${n}.png`, fullPage: true }); };
  const seen = async () => await pg.$eval('.pg.on', e => e.id);
  // CI runner의 시스템 시간대(UTC)와 관계없이 앱과 같은 Asia/Seoul 날짜를 사용합니다.
  const kstYmd = d => {
    const parts = new Intl.DateTimeFormat('en-CA', {
      timeZone:'Asia/Seoul', year:'numeric', month:'2-digit', day:'2-digit'
    }).formatToParts(d);
    const v = Object.fromEntries(parts.map(x => [x.type, x.value]));
    return v.year + '-' + v.month + '-' + v.day;
  };
  const daysAgo = n => {
    const todayKst = kstYmd(new Date());
    const [y,m,d] = todayKst.split('-').map(Number);
    const x = new Date(Date.UTC(y, m-1, d));
    x.setUTCDate(x.getUTCDate() - n);
    const z = v => String(v).padStart(2, '0');
    return x.getUTCFullYear() + '-' + z(x.getUTCMonth()+1) + '-' + z(x.getUTCDate());
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
  const d40 = daysAgo(40), d12 = daysAgo(12);
  const ins = await pg.$$('#ob-dates input');
  await ins[0].fill(d40);
  await ins[1].fill(d12);
  assert(await pg.isChecked('#ob-recovery-home'), '최초 설정에서 홈 회복일 표시는 기본 ON');
  assert(await pg.isChecked('#ob-ai-use'), '최초 설정에서 마음프로 AI 사용은 기본 ON');
  await pg.check('#ob-privacy');
  await shot('2-onboard');
  await pg.click('#ob-go');
  await pg.waitForTimeout(300);
  console.log('2. 시작 후 =', await seen());
  const recoveryText = (await pg.$eval('#home-days', e => e.innerText)).replace(/\n/g, ' | ');
  console.log('   회복일 =', recoveryText);
  const recoveryCompact = recoveryText.replace(/\s*\|\s*/g, '').replace(/\s+/g, '');
  assert(recoveryCompact.includes('41일째'), '40일 전 시작은 오늘 41일째여야 함');
  assert(recoveryCompact.includes('13일째'), '12일 전 시작은 오늘 13일째여야 함');
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

  // 홈 오늘 일정 — 기본보기는 지금 확인할 것만, 전체보기에는 잠자리를 static 안내 행으로 포함
  const scheduleFocus = await pg.evaluate(() => {
    S.eats = [{s:'아침',t:'08:00'},{s:'점심',t:'12:30'},{s:'저녁',t:'18:30'}];
    const sample = [
      {kind:'habit',id:'done-habit',time:'08:00',done:true,action:1},
      {kind:'med',id:'아침',time:'08:00',done:false,action:1},
      {kind:'med',id:'점심',time:'12:30',done:true,action:1},
      {kind:'eat',id:'아침',time:'08:00',done:false,action:1},
      {kind:'eat',id:'점심',time:'12:30',done:false,action:1},
      {kind:'eat',id:'저녁',time:'18:30',done:false,action:1},
      {kind:'sleep',id:'bed',time:'23:00',done:false,action:0}
    ];
    return homeTodayFocusItems(sample, 13*60).map(x=>x.kind+':'+x.id);
  });
  console.log('   오늘 일정 기본 필터 =', scheduleFocus.join(', '));
  assert(!scheduleFocus.includes('eat:아침'), '점심 시간이 지나면 미완료 아침식사도 기본보기에서 접어야 함');
  assert(scheduleFocus.includes('med:아침'), '시간이 지난 미완료 복약은 기본보기에서 계속 보여야 함');
  assert(!scheduleFocus.includes('med:점심') && !scheduleFocus.includes('habit:done-habit'), '완료한 복약·습관은 기본보기에서 접어야 함');
  assert(scheduleFocus.includes('eat:점심') && scheduleFocus.includes('eat:저녁'), '현재·다음 끼니는 기본보기에서 보여야 함');
  assert(!scheduleFocus.includes('sleep:bed'), '잠자리는 기본보기에서 제외해야 함');

  await pg.evaluate(() => {
    S.eats = [{s:'아침',t:'08:00'},{s:'점심',t:'12:30'},{s:'저녁',t:'18:30'}];
    S.eatLog = [];
    S.sleep = {on:1,bed:'23:00',up:'07:00'};
    S.sleepLog = [{t:Date.now(),q:'good'}];
    homeTodayExpanded = true;
    drawTodayScheduleHome();
  });
  const fullScheduleText = await pg.$eval('#home-today', e => e.innerText);
  assert(fullScheduleText.includes('아침 식사') && fullScheduleText.includes('점심 식사') && fullScheduleText.includes('저녁 식사'), '전체보기에는 오늘 등록된 식사 일정이 보여야 함');
  assert(fullScheduleText.includes('잠자리'), '전체보기에는 오늘 잠자리 설정도 보여야 함');
  const fullSleepStatic = await pg.$eval('#home-today', e => [...e.querySelectorAll('.today-row')].some(r => r.innerText.includes('잠자리') && r.querySelector('.tcheck.static')));
  assert(fullSleepStatic, '전체보기의 잠자리는 체크 버튼이 없는 static 안내 행이어야 함');
  await pg.evaluate(() => {
    S.eats=[]; S.eatLog=[]; S.sleep={on:0,bed:'23:00',up:'07:00'}; S.sleepLog=[];
    homeTodayExpanded=false; save(); drawTodayScheduleHome();
  });

  // 선택형 회복일 + 별도 금연 실천 홈 표시
  await pg.evaluate(() => {
    S.recoveryHome = 1;
    S.smoking = { mode:'quit', start:today(), plan:'' };
    save(); drawHome();
  });
  const dual = await pg.$eval('#home-days', e => ({dual:e.classList.contains('dual'), text:e.innerText.replace(/\n/g,' | ')}));
  console.log('   회복+금연 2열 =', dual.text);
  assert(dual.dual, '회복일과 금연일이 모두 있으면 홈이 2열이어야 함');
  assert(dual.text.includes('금연') && dual.text.includes('1일째'), '금연 시작 당일은 금연 1일째로 보여야 함');

  const d5 = daysAgo(-5);
  await pg.evaluate(plan => {
    S.recoveryHome = 0;
    S.smoking = { mode:'plan', start:'', plan:plan };
    save(); drawHome();
  }, d5);
  const smokeOnly = await pg.$eval('#home-days', e => ({dual:e.classList.contains('dual'), text:e.innerText.replace(/\n/g,' | ')}));
  console.log('   금연예정 1열 =', smokeOnly.text);
  assert(!smokeOnly.dual && smokeOnly.text.includes('D-5'), '회복일을 숨기면 금연 예정만 기존 1열로 보여야 함');
  assert(!smokeOnly.text.includes('단주'), '홈 회복일 숨기기에서는 회복일 행이 보이면 안 됨');

  const recordStart = daysAgo(9);
  await pg.evaluate(recordStart => {
    S.recordStart = recordStart;
    S.dates.alcohol = '';
    S.dates.gambling = '';
    S.reclaim = { kind:'alcohol', timeOn:1, timePerDay:2, costOn:1, costPerDay:10000 };
    save(); drawReclaim();
  }, recordStart);
  const reclaimFallback = (await pg.$eval('#rec-reclaim', e => e.innerText)).replace(/\n/g,' | ');
  console.log('   시작일 미설정 되찾은 것 =', reclaimFallback.slice(0,180));
  assert(reclaimFallback.includes('기록 기간') && reclaimFallback.includes('10일'), '회복 시작일이 없으면 앱 기록 시작일부터 기록 기간을 계산해야 함');
  assert(reclaimFallback.includes('앱 기록 시작일부터'), '회복 시작일 미설정 계산 기준을 명확히 표시해야 함');

  await pg.evaluate(({d40,d12}) => {
    S.dates.alcohol = d40;
    S.dates.gambling = d12;
    S.recoveryHome = 1;
    S.smoking = { mode:'', start:'', plan:'' };
    S.reclaim = { kind:'', timeOn:0, timePerDay:0, costOn:0, costPerDay:0 };
    save(); drawHome(); drawReclaim();
  }, {d40,d12});

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
  await pg.click('#ni-save'); await pg.waitForTimeout(180);
  // 칭찬 항목을 고르지 않은 경우 현재 UI는 저장 전 확인 모달을 한 번 보여줍니다.
  if (await pg.isVisible('#ni-skip').catch(() => false)) {
    await pg.click('#ni-skip'); await pg.waitForTimeout(220);
  }
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
  const toolErrBefore = errs.length;
  await pg.click('#tabs button[data-t="tools"]'); await pg.waitForTimeout(250);
  assert(errs.length === toolErrBefore, '회복도구 진입 시 JavaScript 오류가 없어야 함');
  assert(await pg.isVisible('#tool-qa'), '하단 회복도구가 열려야 함');
  assert(await pg.isVisible('#tool-listen'), '회복도구에 듣는 글 메뉴가 보여야 함');
  assert((await pg.$eval('#tool-meaning-check-direct b', e => e.textContent.trim())) === '의미점검', '의미점검 메뉴 이름이 자가점검 기록과 구분되어야 함');
  assert((await pg.$eval('#tool-check-view b', e => e.textContent.trim())) === '자가점검 기록', '자가점검 결과 조회 메뉴 이름이 명확해야 함');

  const meaningDay = daysAgo(1), meaningCheckDay = daysAgo(2);
  await pg.evaluate(({meaningDay,meaningCheckDay}) => {
    S.wbDays = S.wbDays && typeof S.wbDays === 'object' && !Array.isArray(S.wbDays) ? S.wbDays : {};
    S.wbDays[meaningDay] = { hard:[], strength:[], action:[], request:'내가 지킬 한 걸음', ts:Date.now()-86400000 };
    S.meaningChecks = [{ d:meaningCheckDay, ts:Date.now()-172800000, answers:Array(10).fill(2), total:20, domains:{self:2,future:2,choice:2,relation:2} }];
    save(); recTab='work'; recPracticeFilter='meaning'; go('rec');
  }, {meaningDay,meaningCheckDay});
  await pg.waitForTimeout(180);
  const meaningTrailText = await pg.$eval('#rec-body', e => e.innerText);
  assert(meaningTrailText.includes('저장한 의미 기록 2건'), '내 발자취 의미 필터에 두 종류 의미 기록이 함께 보여야 함');
  assert(meaningTrailText.includes('의미 돌아보기') && meaningTrailText.includes('내가 지킬 한 걸음'), '의미 돌아보기 기존 기록을 내 발자취에서 읽어야 함');
  assert(meaningTrailText.includes('의미회복 간편점검') && meaningTrailText.includes('20/40'), '의미회복 간편점검 기존 결과를 내 발자취에서 읽어야 함');
  await pg.locator('#rec-body button.toolcard').filter({hasText:'의미회복 간편점검'}).click();
  await pg.waitForTimeout(100);
  assert((await pg.$eval('#modin h2', e => e.textContent.trim())) === '의미점검 결과', '내 발자취의 의미점검 기록은 기존 결과 상세를 재사용해야 함');
  await pg.evaluate(() => closeModal());
  await pg.evaluate(() => { S.role='family'; save(); recTab='work'; recPracticeFilter='all'; go('rec'); });
  await pg.waitForTimeout(150);
  const familyTrailText = await pg.$eval('#rec-body', e => e.innerText);
  assert(!familyTrailText.includes('의미 돌아보기') && !familyTrailText.includes('의미회복 간편점검'), '가족모드 내 발자취에는 당사자 의미기록이 노출되면 안 됨');
  await pg.evaluate(() => { S.role='self'; save(); go('tools'); });
  await pg.waitForTimeout(150);
  await pg.click('#tool-listen'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-listen', '회복도구의 듣는 글이 기존 듣는 글 화면을 열어야 함');
  assert(await pg.$eval('#tabs button[data-t="tools"]', e => e.classList.contains('on')), '회복도구에서 듣는 글을 열면 회복도구 탭 강조 유지');
  await pg.click('#ls-back'); await pg.waitForTimeout(120);
  assert((await seen()) === 'p-tools', '듣는 글에서 돌아가면 회복도구로 복귀');
  assert(!(await pg.$('#tool-share')), '회복도구에서 추천하기가 빠져야 함');
  assert(await pg.evaluate(() => Array.isArray(window.LEARNING_TOPICS) && window.LEARNING_TOPICS.length === 3), '회복학습은 3개 독립 주제를 learning-data.js에서 로드해야 함');
  await pg.click('#tool-learn'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-learn', '회복학습 목록 페이지가 열려야 함');
  assert((await pg.$$eval('#learn-list .help', a => a.length)) === 3, '회복학습 목록에는 12단계·회복의 기초 이해·SMART Recovery 3개가 있어야 함');
  const learnText = await pg.$eval('#learn-list', e => e.innerText);
  assert(learnText.includes('12단계'), '회복학습 목록에 12단계가 표시되어야 함');
  assert(learnText.includes('회복의 기초 이해'), '회복학습 목록에 심화 주제가 표시되어야 함');
  assert(learnText.includes('SMART Recovery'), '회복학습 목록에 SMART Recovery가 표시되어야 함');
  assert(!learnText.includes('12단계 점검'), '회복학습 목록에는 작성형 12단계 점검이 중복 표시되지 않아야 함');
  await pg.click('#learn-list .help'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-learn-topic', '12단계 선택 시 별도 주제 페이지가 열려야 함');
  assert((await pg.$eval('#learn-topic-title', e => e.innerText)) === '12단계', '주제 페이지 제목은 12단계');
  assert((await pg.$$eval('#learn-topic-sections .help', a => a.length)) === 14, '12단계 학습은 소개 + 기초 + 1~12단계 = 14개');
  assert((await pg.$eval('#learn-topic-sections', e => e.innerText)).includes('12단계의 기초'), '12단계의 기초가 추가되어야 함');
  await pg.evaluate(() => { S.role='self'; S.types=['alcohol']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)) === '우리는 알코올에 무력했으며, 우리의 삶을 수습할 수 없게 되었다는 것을 시인했다.', '알코올 영역 1단계 카드에 AA 단계문장 표시');
  await pg.evaluate(() => { S.types=['gambling']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)) === '우리는 도박에 무력하며 - 정상적으로 생활할 수 없게 되었음을 시인했습니다.', '도박 영역 1단계 카드에 GA 단계문장 표시');
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[5].innerText)).includes('도덕적, 재정적 목록'), '도박 영역 4단계 GA 재정적 목록 문장 표시');
  await pg.evaluate(() => { S.types=['drug']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)) === '우리는 중독에 무력했으며, 우리의 삶을 스스로 수습할 수 없게 되었다는 것을 시인했다.', '약물 영역 1단계 카드에 NA 단계문장 표시');
  await pg.evaluate(() => { S.types=['alcohol','drug']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)).startsWith('우리는 중독에 무력했으며'), '복수 회복영역은 중독 공통형 단계문장 표시');
  assert((await pg.$eval('#learn-topic-sections', e => e.innerText)).includes('공식 문안 자체가 아닙니다'), '복수 회복영역은 통합형 문안 안내 표시');
  await pg.evaluate(() => { S.role='family'; S.types=['alcohol']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)) === '우리는 알코올에 무력했으며, 우리의 삶을 수습할 수 없게 되었다는 것을 시인했다.', '가족모드도 같은 영역 단계문장 사용');
  await pg.evaluate(() => { S.types=['gambling']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)).startsWith('우리는 도박에 무력하며'), '가족모드 도박도 같은 GA 단계문장 사용');
  assert(await pg.evaluate(() => window.FAMILY_TWELVE_STEP_PERSPECTIVES && Object.keys(FAMILY_TWELVE_STEP_PERSPECTIVES).length===14), '가족 12단계 소개·기초·1~12단계 해설 오버레이 14개 로드');
  await pg.evaluate(() => { S.types=['alcohol']; drawLearnTopic(); });
  const familyStep1Text = await pg.evaluate(() => {
    const topic=LEARNING.find(x=>x.id===learnState.topic) || LEARNING[0];
    const sec=(topic.sections||[]).find(x=>x.id==='step-1');
    const view=learningSectionPerspective(sec);
    return ((view&&view.body)||[]).join(' ');
  });
  assert(familyStep1Text.includes('그 사람의 중독을 내가 대신 멈추게 할 수 없었다'), '가족 1단계 해설이 가족 관점으로 표시');
  assert(await pg.evaluate(() => window.FAMILY_STEP_WORKSHEETS && Object.keys(FAMILY_STEP_WORKSHEETS).length===7), '가족 단계별 점검 7종 로드');
  await pg.evaluate(() => { S.role='self'; S.types=['alcohol']; drawLearnTopic(); save(); });
  await pg.click('#learn-topic-sections .help'); await pg.waitForTimeout(100);
  assert(await pg.isVisible('#mod.on'), '12단계 소개 상세 모달이 열려야 함');
  assert((await pg.$eval('#modin', e => e.innerText)).includes('잠시 멈추어 생각해보기'), '학습 상세에 생각해보기 영역이 있어야 함');
  await pg.click('#learn-modal-close'); await pg.waitForTimeout(80);
  assert(!(await pg.$eval('#p-learn-topic', e => e.innerText)).includes('Q&A'), '12단계 학습 페이지가 Q&A로 되돌아가지 않아야 함');
  await pg.click('#learn-topic-back');
  const learnCards=await pg.$$('#learn-list .help');
  await learnCards[1].click();
  assert((await pg.$eval('#learn-topic-title', e => e.innerText)) === '회복의 기초 이해', '심화학습 주제 페이지 제목');
  assert((await pg.$$eval('#learn-topic-sections .help', a => a.length)) === 4, '심화학습은 4개 섹션');
  const deepText=await pg.$eval('#learn-topic-sections', e => e.innerText);
  assert(deepText.includes('영·마음·몸') && deepText.includes('욕구에서 탐욕까지') && deepText.includes('두려움을') && deepText.includes('의미와 자기초월'), '심화학습 4개 핵심 영역 표시');
  await pg.click('#learn-topic-back'); await pg.waitForTimeout(100);
  await pg.click('#p-learn .sp button'); await pg.waitForTimeout(120);
  assert((await seen()) === 'p-tools', '회복학습에서 회복도구로 돌아갈 수 있어야 함');

  // V7.6 1·4·8·9단계 검토 + 10·11·12단계 매일 실천 — 초안 + 내 발자취 저장
  assert(await pg.evaluate(() => window.STEP_WORKSHEETS && ['step1','step4','step8','step9','step10','step11','step12'].every(k => STEP_WORKSHEETS[k])), '1·4·8·9·10·11·12단계 검토·실천 데이터 로드');
  await pg.evaluate(() => openWorkbook('step1','rec')); await pg.waitForTimeout(120);
  assert((await seen()) === 'p-workbook', '1단계 검토 작성 화면이 열려야 함');
  assert((await pg.$$eval('#wb-body details.ws-sec', a => a.length)) === 3, '1단계 검토는 무력함·수습할 수 없는 삶·상실과 애도 3개 시트');
  await pg.fill('#wb-body textarea', '조절하려 했지만 뜻대로 되지 않았던 경험'); await pg.waitForTimeout(380);
  assert(await pg.evaluate(() => S.stepDrafts.step1.sections.powerless[0].event.includes('조절하려')), '검토 작성 중 초안이 상태에 자동 저장');
  await pg.click('#wb-save-record'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-rec' && await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===1 && S.stepWorks[0].kind==='step1'), '1단계 검토를 내 발자취 상태에 저장');
  await pg.evaluate(() => openWorkbook('step4','rec')); await pg.waitForTimeout(120);
  assert((await pg.$$eval('#wb-body details.ws-sec', a => a.length)) === 8, '4단계 검토는 어휘 + 핵심·심화 7개 시트');
  await pg.fill('#wb-body textarea', '내가 놓지 못한 원한'); await pg.waitForTimeout(380);
  await pg.click('#wb-save-record'); await pg.waitForTimeout(180);
  assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===2 && S.stepWorks.some(x=>x.kind==='step4')), '4단계 검토도 내 발자취 상태에 저장');

  for(const [btn,kind,sections,text] of [
    ['#rec-wb8','step8',3,'보상할 명단 첫 기록'],
    ['#rec-wb9','step9',3,'직접 보상 전 안전 검토'],
    ['#rec-wb10','step10',3,'오늘 남은 감정적 숙취'],
    ['#rec-wb11','step11',3,'오늘의 연결 방식'],
    ['#rec-wb12','step12',3,'오늘 살고 싶은 원칙']
  ]){
    await pg.evaluate(k => openWorkbook(k,'rec'), kind); await pg.waitForTimeout(100);
    assert((await seen()) === 'p-workbook', kind+' 작성 화면이 열려야 함');
    const detailCount=await pg.$$eval('#wb-body details.ws-sec', a => a.length);
    const refs=await pg.evaluate(k => (STEP_WORKSHEETS[k].references||[]).length, kind);
    assert(detailCount === sections + (refs ? 1 : 0), kind+' 섹션/어휘 렌더 수 일치');
    await pg.fill('#wb-body textarea', text); await pg.waitForTimeout(360);
    await pg.click('#wb-save-record'); await pg.waitForTimeout(120);
  }
  assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===7 && ['step1','step4','step8','step9','step10','step11','step12'].every(k=>S.stepWorks.some(x=>x.kind===k))), '1·4·8·9·10·11·12단계 기록 7건 상태 저장');
  assert(await pg.evaluate(() => STEP_WORKSHEETS.step11.safety.includes('특정 종교를 전제로 하지 않습니다')), '11단계 종교 강요 방지 문구');
  assert(await pg.evaluate(() => STEP_WORKSHEETS.step12.safety.includes('다른 사람을 치료하거나 책임지라는 뜻이 아닙니다')), '12단계 도움 역할 경계 문구');
  await pg.click('#tabs button[data-t="tools"]'); await pg.waitForTimeout(100);

  // V7.2 자가점검 — 선택 회복영역 + 공통 마음건강 + 행동연결/재점검 안내/최근기록
  // 앞의 영역별 12단계 문구 검증에서 유형을 바꿨으므로 여기서는 의도한 알코올+도박 프로필을 복원합니다.
  await pg.evaluate(() => { S.role='self'; S.types=['alcohol','gambling']; save(); });
  assert(await pg.evaluate(() => Array.isArray(window.SCREENING_TOOLS) && window.SCREENING_TOOLS.length === 9), '자가점검 도구는 9종이어야 함');
  await pg.click('#tool-check'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-screening', '자가점검 목록이 열려야 함');
  const selfScreens = await pg.$$eval('[data-screen]', a => a.map(x => x.dataset.screen));
  assert(JSON.stringify(selfScreens) === JSON.stringify(['audit-k','pgsi','nds-bv','nas-bv','nss-bv']), '알코올+도박 프로필에는 AUDIT-K·PGSI와 공통 3종만 보여야 함');

  // AUDIT-K 첫 검사: 남성 기준, 모두 0점
  await pg.click('[data-screen="audit-k"]'); await pg.waitForTimeout(100);
  assert(await pg.isVisible('#screen-sex-m') && await pg.isVisible('#screen-sex-f'), 'AUDIT-K는 원자료 성별 기준을 선택해야 함');
  await pg.click('#screen-sex-m'); await pg.waitForTimeout(100);
  assert((await pg.$$('[data-screen-v]')).length>0, 'AUDIT-K 첫 문항 선택지가 표시되어야 함');
  await pg.evaluate(() => { const t=screenTool('audit-k'); screenRun.a=Array(t.questions.length).fill(0); finishScreen(t); });
  await pg.waitForTimeout(80);
  assert((await pg.$eval('.screen-score .n', e => e.innerText)) === '0', 'AUDIT-K 0점 결과');
  assert((await pg.$eval('#screen-test-body', e => e.innerText)).includes('첫 기록'), '첫 자가점검은 첫 기록으로 표시');
  await pg.click('#screen-list-go'); await pg.waitForTimeout(100);

  // AUDIT-K 두 번째 검사: 첫 문항 1점, 나머지 0점 → 이전보다 1점 증가
  await pg.click('[data-screen="audit-k"]'); await pg.waitForTimeout(80);
  await pg.click('#screen-sex-m'); await pg.waitForTimeout(80);
  await pg.evaluate(() => { const t=screenTool('audit-k'); screenRun.a=Array(t.questions.length).fill(0); screenRun.a[0]=1; finishScreen(t); });
  await pg.waitForTimeout(80);
  const secondAudit = await pg.$eval('#screen-test-body', e => e.innerText);
  assert(secondAudit.includes('1점') && secondAudit.includes('1점 증가'), '두 번째 AUDIT-K는 이전 대비 1점 증가를 표시');
  assert(secondAudit.includes('약 4주 후') && secondAudit.includes('공식 재검사 주기'), '결과에 경과관찰용 재점검 안내 표시');
  assert(await pg.isVisible('#screen-log-go') && await pg.isVisible('#screen-help-go') && await pg.isVisible('#screen-ai-go'), '결과에서 기록·도움·마음프로 행동 연결 표시');
  await pg.click('#screen-stat-go'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-rec', '자가점검 결과에서 내 발자취 통계로 이동');
  const statTextV7 = await pg.$eval('#rec-body', e => e.innerText);
  assert(statTextV7.includes('자가점검 변화') && statTextV7.includes('AUDIT-K') && statTextV7.includes('이전보다 1점 증가'), '통계에 자가점검 최근점수와 이전 대비 변화 표시');
  assert((await pg.$$eval('#rec-body .trend-svg', a => a.length)) >= 1, '자가점검 통계에 검사별 꺾은선 그래프 표시');
  assert((await pg.$$eval('#rec-body .screen-record-row', a => a.length)) >= 2, '자가점검 통계에 최근 검사일·점수 목록 표시');
  await shot('10-screening-stat');

  // 다시 회복도구로 돌아와 Q&A 검증
  await pg.click('#tabs button[data-t="tools"]'); await pg.waitForTimeout(120);
  assert(await pg.evaluate(() => Array.isArray(window.QA_ITEMS) && window.QA_ITEMS.length === 224), 'Q&A가 224문답이어야 함');
  assert(await pg.evaluate(() => window.QA_ITEMS.every(x => { const n=String(x.a||'').split(/\n\s*\n/).filter(Boolean).length; return n>=2 && n<=3; })), 'Q&A 224개 답변이 모두 2~3문단이어야 함');
  await pg.click('#tool-qa'); await pg.waitForTimeout(250);
  assert((await pg.$eval('#qa-count', e => e.innerText)).includes('224'), 'Q&A 전체 224개 표시');
  await pg.fill('#qa-search', '갈망'); await pg.waitForTimeout(200);
  assert((await pg.$$eval('#qa-list .qaitem', a => a.length)) > 0, 'Q&A 갈망 검색 결과 존재');
  await pg.click('#qa-list .qaitem'); await pg.waitForTimeout(150);
  assert(await pg.isVisible('#qa-one .qadetail'), 'Q&A 상세 답변 표시');
  const qaVisible = await pg.$eval('#p-qa', e => e.innerText);
  assert(!qaVisible.includes('중독 200문답'), 'Q&A 사용자 화면에 원자료 제작 문구가 노출되지 않아야 함');
  assert(!qaVisible.includes('보완 문답'), 'Q&A 사용자 화면에 제작상 보완 구분이 노출되지 않아야 함');
  await shot('11-tools-qa');

  // 기록은 하단에서 내정보 → 내 발자취로 이동
  await pg.click('#tabs button[data-t="home"]'); await pg.waitForTimeout(150);
  await pg.click('#top-me'); await pg.waitForTimeout(250);
  assert((await seen()) === 'p-my' && await pg.isVisible('#my-trail') && await pg.isVisible('#my-settings'), '상단 나 아이콘은 개인 허브를 열어야 함');
  const myOrder = await pg.$$eval('#p-my > #my-settings, #p-my > #my-trail, #p-my > #rec-reclaim', els => els.map(e=>e.id));
  assert(myOrder.join('>') === 'my-settings>my-trail>rec-reclaim', '나 화면은 내 정보 · 설정 → 내 발자취 → 내가 되찾은 것 순서여야 함');
  await pg.click('#my-settings'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-me' && await pg.isVisible('#me-share'), '내 정보 · 설정에 독립 추천하기 항목 존재');
  assert(await pg.$('#me-feedback-send'), '내 정보 · 설정에 앱에 바라는 점 단일 입력 존재');
  await pg.evaluate(() => go('my')); await pg.waitForTimeout(80);
  await pg.click('#my-trail'); await pg.waitForTimeout(300);
  assert((await pg.$eval('#p-rec h1', e => e.innerText)) === '내 발자취', '기록 화면 명칭은 내 발자취');
  await shot('11-trail-mood');
  const rt = async i => { await pg.click(`#rec-tab button:nth-child(${i})`); await pg.waitForTimeout(300); };
  await rt(2); await shot('12-trail-urge');
  await rt(5); console.log('   다시시작 탭 =', (await pg.$eval('#rec-body', e => e.innerText)).replace(/\n+/g,' / ').slice(0,80));
  await rt(6); assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===7), '내 발자취 진입 후에도 12단계 검토 저장 기록 7건 유지');
  await rt(8);
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
  const afterResetCompact = afterReset.replace(/\s*\|\s*/g, '').replace(/\s+/g, '');
  assert(afterResetCompact.includes('1일째'), '다시 시작한 당일은 새 회복 1일째여야 함');

  // 다크 모드 — 나 → 내 정보 · 설정 → 앱 → 화면 설정
  await pg.click('#top-me'); await pg.waitForTimeout(250);
  assert((await seen()) === 'p-my', '상단 나 아이콘은 개인 허브를 열어야 함');
  await pg.click('#my-settings'); await pg.waitForTimeout(120);
  await pg.locator('#p-me .acc-h', {hasText:'앱'}).click(); await pg.waitForTimeout(150);
  assert(await pg.isVisible('#me-theme'), '앱 묶음에 화면 설정이 보여야 함');
  await pg.click('#me-theme [data-theme="dark"]'); await pg.waitForTimeout(300);
  await shot('17-dark');
  await pg.click('#me-theme [data-theme="light"]'); await pg.waitForTimeout(200);
  await pg.click('#tabs button[data-t="home"]'); await pg.waitForTimeout(200);

  // 새로고침 후에도 남아 있는지
  await pg.reload(); await pg.waitForTimeout(600);
  console.log('15. 새로고침 후 =', await seen(), '|', (await pg.$eval('#home-days', e => e.innerText)).replace(/\n/g, ' '));

  console.log('\n=== 오류 ===');
  console.log(errs.length ? errs.join('\n') : '없음');
  assert(errs.length === 0, '브라우저 회귀검사 중 로컬 HTTP·JavaScript 런타임 오류가 없어야 함');

  await b.close(); srv.close();
})();
