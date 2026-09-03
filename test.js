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
  const launchOpts = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {};
  const b = await chromium.launch(launchOpts);
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
  const toolErrBefore = errs.length;
  await pg.click('#tabs button[data-t="tools"]'); await pg.waitForTimeout(250);
  assert(errs.length === toolErrBefore, '회복도구 진입 시 JavaScript 오류가 없어야 함');
  assert(await pg.isVisible('#tool-qa'), '하단 회복도구가 열려야 함');
  assert(await pg.isVisible('#tool-listen'), '회복도구에 듣는 글 메뉴가 보여야 함');
  await pg.click('#tool-listen'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-listen', '회복도구의 듣는 글이 기존 듣는 글 화면을 열어야 함');
  assert(await pg.$eval('#tabs button[data-t="tools"]', e => e.classList.contains('on')), '회복도구에서 듣는 글을 열면 회복도구 탭 강조 유지');
  await pg.click('#ls-back'); await pg.waitForTimeout(120);
  assert((await seen()) === 'p-tools', '듣는 글에서 돌아가면 회복도구로 복귀');
  assert(!(await pg.$('#tool-share')), '회복도구에서 추천하기가 빠져야 함');
  assert(await pg.evaluate(() => Array.isArray(window.LEARNING_TOPICS) && window.LEARNING_TOPICS.length === 2), '회복학습은 2개 독립 주제를 learning-data.js에서 로드해야 함');
  await pg.click('#tool-learn'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-learn', '회복학습 목록 페이지가 열려야 함');
  assert((await pg.$$eval('#learn-list .help', a => a.length)) === 3, '회복학습 목록에는 12단계·회복의 기초 이해·단계별 점검 3개가 있어야 함');
  assert((await pg.$eval('#learn-list', e => e.innerText)).includes('12단계'), '회복학습 목록에 12단계가 표시되어야 함');
  assert((await pg.$eval('#learn-list', e => e.innerText)).includes('회복의 기초 이해'), '회복학습 목록에 심화 주제가 표시되어야 함');
  assert((await pg.$eval('#learn-list', e => e.innerText)).includes('단계별 점검'), '회복학습 목록에 단계별 점검이 표시되어야 함');
  await pg.click('#learn-list .help'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-learn-topic', '12단계 선택 시 별도 주제 페이지가 열려야 함');
  assert((await pg.$eval('#learn-topic-title', e => e.innerText)) === '12단계', '주제 페이지 제목은 12단계');
  assert((await pg.$$eval('#learn-topic-sections .help', a => a.length)) === 14, '12단계 학습은 소개 + 기초 + 1~12단계 = 14개');
  assert((await pg.$eval('#learn-topic-sections', e => e.innerText)).includes('12단계의 기초'), '12단계의 기초가 추가되어야 함');
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
  assert(await pg.evaluate(() => window.FAMILY_TWELVE_STEP_PERSPECTIVES && Object.keys(FAMILY_TWELVE_STEP_PERSPECTIVES).length===12), '가족 12단계 해설 오버레이 12개 로드');
  await pg.evaluate(() => { S.types=['alcohol']; drawLearnTopic(); });
  await pg.click('#learn-topic-sections .help:nth-child(4)'); await pg.waitForTimeout(80);
  assert((await pg.$eval('#modin', e => e.innerText)).includes('그 사람의 중독을 내가 대신 멈추게 할 수 없었다'), '가족 1단계 해설이 가족 관점으로 표시');
  await pg.click('#learn-modal-close');
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
  await pg.click('#wb-save-record'); await pg.waitForTimeout(150);
  assert((await seen()) === 'p-rec' && (await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토 1건'), '1단계 검토를 내 발자취에 저장');
  await pg.click('#rec-wb4'); await pg.waitForTimeout(120);
  assert((await pg.$$eval('#wb-body details.ws-sec', a => a.length)) === 8, '4단계 검토는 어휘 + 핵심·심화 7개 시트');
  await pg.fill('#wb-body textarea', '내가 놓지 못한 원한'); await pg.waitForTimeout(380);
  await pg.click('#wb-save-record'); await pg.waitForTimeout(150);
  assert((await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토 2건'), '4단계 검토도 내 발자취에 저장');

  for(const [btn,kind,sections,text] of [
    ['#rec-wb8','step8',3,'보상할 명단 첫 기록'],
    ['#rec-wb9','step9',3,'직접 보상 전 안전 검토'],
    ['#rec-wb10','step10',3,'오늘 남은 감정적 숙취'],
    ['#rec-wb11','step11',3,'오늘의 연결 방식'],
    ['#rec-wb12','step12',3,'오늘 살고 싶은 원칙']
  ]){
    await pg.click(btn); await pg.waitForTimeout(100);
    assert((await seen()) === 'p-workbook', kind+' 작성 화면이 열려야 함');
    const detailCount=await pg.$$eval('#wb-body details.ws-sec', a => a.length);
    const refs=await pg.evaluate(k => (STEP_WORKSHEETS[k].references||[]).length, kind);
    assert(detailCount === sections + (refs ? 1 : 0), kind+' 섹션/어휘 렌더 수 일치');
    await pg.fill('#wb-body textarea', text); await pg.waitForTimeout(360);
    await pg.click('#wb-save-record'); await pg.waitForTimeout(120);
  }
  assert((await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토 7건'), '1·4·8·9·10·11·12단계 기록 7건 저장');
  assert(await pg.evaluate(() => STEP_WORKSHEETS.step11.safety.includes('특정 종교를 전제로 하지 않습니다')), '11단계 종교 강요 방지 문구');
  assert(await pg.evaluate(() => STEP_WORKSHEETS.step12.safety.includes('다른 사람을 치료하거나 책임지라는 뜻이 아닙니다')), '12단계 도움 역할 경계 문구');
  await pg.click('#tabs button[data-t="tools"]'); await pg.waitForTimeout(100);

  // V7.2 자가점검 — 선택 회복영역 + 공통 마음건강 + 행동연결/재점검 안내/최근기록
  assert(await pg.evaluate(() => Array.isArray(window.SCREENING_TOOLS) && window.SCREENING_TOOLS.length === 9), '자가점검 도구는 9종이어야 함');
  await pg.click('#tool-check'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-screening', '자가점검 목록이 열려야 함');
  const selfScreens = await pg.$$eval('[data-screen]', a => a.map(x => x.dataset.screen));
  assert(JSON.stringify(selfScreens) === JSON.stringify(['audit-k','pgsi','nds-bv','nas-bv','nss-bv']), '알코올+도박 프로필에는 AUDIT-K·PGSI와 공통 3종만 보여야 함');

  // AUDIT-K 첫 검사: 남성 기준, 모두 0점
  await pg.click('[data-screen="audit-k"]'); await pg.waitForTimeout(100);
  assert(await pg.isVisible('#screen-sex-m') && await pg.isVisible('#screen-sex-f'), 'AUDIT-K는 원자료 성별 기준을 선택해야 함');
  await pg.click('#screen-sex-m'); await pg.waitForTimeout(100);
  for(let i=0;i<10;i++){
    await pg.click('[data-screen-v="0"]');
    await pg.click('#screen-next');
    await pg.waitForTimeout(35);
  }
  assert((await pg.$eval('.screen-score .n', e => e.innerText)) === '0', 'AUDIT-K 0점 결과');
  assert((await pg.$eval('#screen-test-body', e => e.innerText)).includes('첫 기록'), '첫 자가점검은 첫 기록으로 표시');
  await pg.click('#screen-list-go'); await pg.waitForTimeout(100);

  // AUDIT-K 두 번째 검사: 첫 문항 1점, 나머지 0점 → 이전보다 1점 증가
  await pg.click('[data-screen="audit-k"]'); await pg.waitForTimeout(80);
  await pg.click('#screen-sex-m'); await pg.waitForTimeout(80);
  for(let i=0;i<10;i++){
    await pg.click(i===0 ? '[data-screen-v="1"]' : '[data-screen-v="0"]');
    await pg.click('#screen-next');
    await pg.waitForTimeout(35);
  }
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
  await rt(6); assert((await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토 7건'), '내 발자취 12단계 검토 탭에서 저장 기록 7건 재조회');
  await rt(7);
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
