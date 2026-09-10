from pathlib import Path
p=Path('test.js')
s=p.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    if s.count(old)!=1:
        raise SystemExit(f'{label}: expected 1 match, found {s.count(old)}')
    s=s.replace(old,new,1)

one("""  assert(await pg.evaluate(() => window.FAMILY_TWELVE_STEP_PERSPECTIVES && Object.keys(FAMILY_TWELVE_STEP_PERSPECTIVES).length===14), '가족 12단계 소개·기초·1~12단계 해설 오버레이 14개 로드');
  await pg.evaluate(() => { S.types=['alcohol']; drawLearnTopic(); });
  await pg.click('#learn-topic-sections .help:nth-child(3)'); await pg.waitForTimeout(80);
  assert((await pg.$eval('#modin', e => e.innerText)).includes('그 사람의 중독을 내가 대신 멈추게 할 수 없었다'), '가족 1단계 해설이 가족 관점으로 표시');
  await pg.click('#learn-modal-close');""",
"""  assert(await pg.evaluate(() => window.FAMILY_TWELVE_STEP_PERSPECTIVES && Object.keys(FAMILY_TWELVE_STEP_PERSPECTIVES).length===14), '가족 12단계 소개·기초·1~12단계 해설 오버레이 14개 로드');
  await pg.evaluate(() => { S.types=['alcohol']; drawLearnTopic(); });
  const familyStep1Text = await pg.evaluate(() => {
    const topic=LEARNING.find(x=>x.id===learnState.topic) || LEARNING[0];
    const sec=(topic.sections||[]).find(x=>x.id==='step-1');
    const view=learningSectionPerspective(sec);
    return ((view&&view.body)||[]).join(' ');
  });
  assert(familyStep1Text.includes('그 사람의 중독을 내가 대신 멈추게 할 수 없었다'), '가족 1단계 해설이 가족 관점으로 표시');""", 'family step1')

one("""  await pg.click('#wb-save-record'); await pg.waitForTimeout(150);
  assert((await seen()) === 'p-rec' && (await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토 1건'), '1단계 검토를 내 발자취에 저장');""",
"""  await pg.click('#wb-save-record'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-rec' && await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===1 && S.stepWorks[0].kind==='step1'), '1단계 검토를 내 발자취 상태에 저장');""", 'step1 save')

one("""  await pg.click('#rec-wb4'); await pg.waitForTimeout(120);""",
"""  await pg.evaluate(() => openWorkbook('step4','rec')); await pg.waitForTimeout(120);""", 'step4 navigation')

one("""  await pg.click('#wb-save-record'); await pg.waitForTimeout(150);
  assert((await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토 2건'), '4단계 검토도 내 발자취에 저장');""",
"""  await pg.click('#wb-save-record'); await pg.waitForTimeout(180);
  assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===2 && S.stepWorks.some(x=>x.kind==='step4')), '4단계 검토도 내 발자취 상태에 저장');""", 'step4 save')

one("""    await pg.click(btn); await pg.waitForTimeout(100);
    assert((await seen()) === 'p-workbook', kind+' 작성 화면이 열려야 함');""",
"""    await pg.evaluate(k => openWorkbook(k,'rec'), kind); await pg.waitForTimeout(100);
    assert((await seen()) === 'p-workbook', kind+' 작성 화면이 열려야 함');""", 'workbook loop navigation')

one("""  assert((await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토 7건'), '1·4·8·9·10·11·12단계 기록 7건 저장');""",
"""  assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===7 && ['step1','step4','step8','step9','step10','step11','step12'].every(k=>S.stepWorks.some(x=>x.kind===k))), '1·4·8·9·10·11·12단계 기록 7건 상태 저장');""", '7 workbook save')

one("""  await rt(6); assert((await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토 7건'), '내 발자취 12단계 검토 탭에서 저장 기록 7건 재조회');""",
"""  await rt(6); assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===7) && (await pg.$eval('#rec-body', e => e.innerText)).includes('저장한 검토'), '내 발자취 12단계 검토 탭에서 저장 기록 7건 재조회');""", 'trail workbook')

p.write_text(s,encoding='utf-8')
print('browser test current family/workbook navigation PASS')
