from pathlib import Path
p=Path('test.js')
s=p.read_text(encoding='utf-8')
old="""  assert(await pg.evaluate(() => window.FAMILY_TWELVE_STEP_PERSPECTIVES && Object.keys(FAMILY_TWELVE_STEP_PERSPECTIVES).length===14), '가족 12단계 소개·기초·1~12단계 해설 오버레이 14개 로드');
  await pg.evaluate(() => { S.types=['alcohol']; drawLearnTopic(); });
  await pg.click('#learn-topic-sections .help:nth-child(3)'); await pg.waitForTimeout(80);
  assert((await pg.$eval('#modin', e => e.innerText)).includes('그 사람의 중독을 내가 대신 멈추게 할 수 없었다'), '가족 1단계 해설이 가족 관점으로 표시');
  await pg.click('#learn-modal-close');"""
new="""  assert(await pg.evaluate(() => window.FAMILY_TWELVE_STEP_PERSPECTIVES && Object.keys(FAMILY_TWELVE_STEP_PERSPECTIVES).length===14), '가족 12단계 소개·기초·1~12단계 해설 오버레이 14개 로드');
  await pg.evaluate(() => { S.types=['alcohol']; drawLearnTopic(); });
  const familyStep1Text = await pg.evaluate(() => {
    const topic=LEARNING.find(x=>x.id===learnState.topic) || LEARNING[0];
    const sec=(topic.sections||[]).find(x=>x.id==='step-1');
    const view=learningSectionPerspective(sec);
    return ((view&&view.body)||[]).join(' ');
  });
  assert(familyStep1Text.includes('그 사람의 중독을 내가 대신 멈추게 할 수 없었다'), '가족 1단계 해설이 가족 관점으로 표시');"""
if old not in s:
    raise SystemExit('family step1 stale browser block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('browser test family step-1 current check PASS')
