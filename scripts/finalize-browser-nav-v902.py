from pathlib import Path
p=Path('test.js'); s=p.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    if s.count(old)!=1:
        raise SystemExit(f'{label}: expected 1 match, found {s.count(old)}')
    s=s.replace(old,new,1)

one("""  await pg.click('#tabs button[data-t=\"home\"]'); await pg.waitForTimeout(150);
  await pg.click('#top-me'); await pg.waitForTimeout(250);
  assert(await pg.isVisible('#me-share'), '내정보에 독립 추천하기 항목 존재');
  assert(await pg.$('#me-feedback-send'), '내정보에 앱에 바라는 점 단일 입력 존재');
  await pg.locator('#p-me .acc-h', {hasText:'내 발자취'}).click(); await pg.waitForTimeout(120);
  assert(await pg.isVisible('#me-trail-open'), '내정보에 내 발자취 진입 버튼 존재');
  await pg.click('#me-trail-open'); await pg.waitForTimeout(300);""",
"""  await pg.click('#tabs button[data-t=\"home\"]'); await pg.waitForTimeout(150);
  await pg.click('#top-me'); await pg.waitForTimeout(250);
  assert((await seen()) === 'p-my' && await pg.isVisible('#my-trail') && await pg.isVisible('#my-settings'), '상단 나 아이콘은 개인 허브를 열어야 함');
  await pg.click('#my-settings'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-me' && await pg.isVisible('#me-share'), '내 정보 · 설정에 독립 추천하기 항목 존재');
  assert(await pg.$('#me-feedback-send'), '내 정보 · 설정에 앱에 바라는 점 단일 입력 존재');
  await pg.evaluate(() => go('my')); await pg.waitForTimeout(80);
  await pg.click('#my-trail'); await pg.waitForTimeout(300);""", 'my hub/trail navigation')

one("""  await rt(7);
  console.log('12. 통계 =', (await pg.$eval('#rec-body', e => e.innerText)).replace(/\\n+/g, ' / ').slice(0, 200));""",
"""  await rt(8);
  console.log('12. 통계 =', (await pg.$eval('#rec-body', e => e.innerText)).replace(/\\n+/g, ' / ').slice(0, 200));""", 'statistics tab index')

one("""  // 다크 모드 — 내정보 → 앱 → 화면 설정
  await pg.click('#top-me'); await pg.waitForTimeout(250);
  const accs = await pg.$$('#p-me .acc');
  await accs[2].click('.acc-h'); await pg.waitForTimeout(150);
  await pg.click('#me-theme [data-theme=\"dark\"]'); await pg.waitForTimeout(300);""",
"""  // 다크 모드 — 나 → 내 정보 · 설정 → 앱 → 화면 설정
  await pg.click('#top-me'); await pg.waitForTimeout(250);
  assert((await seen()) === 'p-my', '상단 나 아이콘은 개인 허브를 열어야 함');
  await pg.click('#my-settings'); await pg.waitForTimeout(120);
  await pg.locator('#p-me .acc-h', {hasText:'앱'}).click(); await pg.waitForTimeout(150);
  assert(await pg.isVisible('#me-theme'), '앱 묶음에 화면 설정이 보여야 함');
  await pg.click('#me-theme [data-theme=\"dark\"]'); await pg.waitForTimeout(300);""", 'theme navigation')

p.write_text(s,encoding='utf-8')
print('browser test current My hub navigation PASS')
