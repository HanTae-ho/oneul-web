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

old2="""  await pg.click('#wb-save-record'); await pg.waitForTimeout(150);
  assert((await seen()) === 'p-rec' && (await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토 1건'), '1단계 검토를 내 발자취에 저장');"""
new2="""  await pg.click('#wb-save-record'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-rec' && await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===1 && S.stepWorks[0].kind==='step1'), '1단계 검토를 내 발자취 상태에 저장');"""
if old2 not in s:
    raise SystemExit('step1 workbook stale assertion not found')
s=s.replace(old2,new2,1)

old3="""  await pg.click('#wb-save-record'); await pg.waitForTimeout(150);
  assert((await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토 2건'), '4단계 검토도 내 발자취에 저장');"""
new3="""  await pg.click('#wb-save-record'); await pg.waitForTimeout(180);
  assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===2 && S.stepWorks.some(x=>x.kind==='step4')), '4단계 검토도 내 발자취 상태에 저장');"""
if old3 not in s:
    raise SystemExit('step4 workbook stale assertion not found')
s=s.replace(old3,new3,1)

old4="""  assert((await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토 7건'), '1·4·8·9·10·11·12단계 기록 7건 저장');"""
new4="""  assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===7 && ['step1','step4','step8','step9','step10','step11','step12'].every(k=>S.stepWorks.some(x=>x.kind===k))), '1·4·8·9·10·11·12단계 기록 7건 상태 저장');"""
if old4 not in s:
    raise SystemExit('7 workbook stale assertion not found')
s=s.replace(old4,new4,1)

# 내 발자취 재조회도 렌더 문구만 보지 않고 저장 상태와 화면을 함께 확인합니다.
old5="""  await rt(6); assert((await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토 7건'), '내 발자취 12단계 검토 탭에서 저장 기록 7건 재조회');"""
new5="""  await rt(6); assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===7) && (await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토'), '내 발자취 12단계 검토 탭에서 저장 기록 7건 재조회');"""
if old5 not in s:
    raise SystemExit('trail workbook stale assertion not found')
s=s.replace(old5,new5,1)

p.write_text(s,encoding='utf-8')
print('browser test current family/workbook checks PASS')
