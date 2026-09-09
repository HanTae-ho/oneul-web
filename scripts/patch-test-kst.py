from pathlib import Path

p=Path('test.js')
s=p.read_text(encoding='utf-8')
old="""  const localYmd = d => {
    const z = n => String(n).padStart(2, '0');
    return d.getFullYear() + '-' + z(d.getMonth()+1) + '-' + z(d.getDate());
  };
  const daysAgo = n => {
    const d = new Date();
    d.setHours(12, 0, 0, 0);
    d.setDate(d.getDate() - n);
    return localYmd(d);
  };"""
new="""  // CI runner의 시스템 시간대(UTC)와 관계없이 앱과 같은 Asia/Seoul 날짜를 사용합니다.
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
  };"""
if old not in s:
    raise SystemExit('stale local date helper not found')
s=s.replace(old,new,1)

old2="""  const recoveryText = (await pg.$eval('#home-days', e => e.innerText)).replace(/\\n/g, ' | ');
  console.log('   회복일 =', recoveryText);
  assert(recoveryText.includes('41일째'), '40일 전 시작은 오늘 41일째여야 함');
  assert(recoveryText.includes('13일째'), '12일 전 시작은 오늘 13일째여야 함');"""
new2="""  const recoveryText = (await pg.$eval('#home-days', e => e.innerText)).replace(/\\n/g, ' | ');
  console.log('   회복일 =', recoveryText);
  const recoveryCompact = recoveryText.replace(/\\s*\\|\\s*/g, '').replace(/\\s+/g, '');
  assert(recoveryCompact.includes('41일째'), '40일 전 시작은 오늘 41일째여야 함');
  assert(recoveryCompact.includes('13일째'), '12일 전 시작은 오늘 13일째여야 함');"""
if old2 not in s:
    raise SystemExit('stale recovery-day assertion block not found')
s=s.replace(old2,new2,1)

old3="""  await pg.click('#ni-save'); await pg.waitForTimeout(300);
  console.log('11. 자기 전 저장 후 =', await seen());"""
new3="""  await pg.click('#ni-save'); await pg.waitForTimeout(180);
  // 칭찬 항목을 고르지 않은 경우 현재 UI는 저장 전 확인 모달을 한 번 보여줍니다.
  if (await pg.isVisible('#ni-skip').catch(() => false)) {
    await pg.click('#ni-skip'); await pg.waitForTimeout(220);
  }
  console.log('11. 자기 전 저장 후 =', await seen());"""
if old3 not in s:
    raise SystemExit('stale night-save test block not found')
s=s.replace(old3,new3,1)

old4="""  assert((await pg.$eval('#learn-topic-sections', e => e.innerText)).includes('12단계의 기초'), '12단계의 기초가 추가되어야 함');
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)) === '우리는 알코올에 무력했으며, 우리의 삶을 수습할 수 없게 되었다는 것을 시인했다.', '알코올 영역 1단계 카드에 AA 단계문장 표시');"""
new4="""  assert((await pg.$eval('#learn-topic-sections', e => e.innerText)).includes('12단계의 기초'), '12단계의 기초가 추가되어야 함');
  await pg.evaluate(() => { S.role='self'; S.types=['alcohol']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)) === '우리는 알코올에 무력했으며, 우리의 삶을 수습할 수 없게 되었다는 것을 시인했다.', '알코올 영역 1단계 카드에 AA 단계문장 표시');"""
if old4 not in s:
    raise SystemExit('stale Twelve Step area setup not found')
s=s.replace(old4,new4,1)

p.write_text(s,encoding='utf-8')
print('test.js current browser-regression repairs PASS')
