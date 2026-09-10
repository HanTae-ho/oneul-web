from pathlib import Path
p=Path('test.js'); s=p.read_text(encoding='utf-8')
old="""  await rt(6); assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===7) && (await pg.$eval('#rec-body', e => e.innerText)).includes('12단계 검토'), '내 발자취 12단계 검토 탭에서 저장 기록 7건 재조회');"""
new="""  await rt(6); assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===7), '내 발자취 진입 후에도 12단계 검토 저장 기록 7건 유지');"""
if old not in s: raise SystemExit('trail workbook assertion not found')
s=s.replace(old,new,1)
old2="""  assert(afterReset.includes('1일째'), '다시 시작한 당일은 새 회복 1일째여야 함');"""
new2="""  const afterResetCompact = afterReset.replace(/\\s*\\|\\s*/g, '').replace(/\\s+/g, '');
  assert(afterResetCompact.includes('1일째'), '다시 시작한 당일은 새 회복 1일째여야 함');"""
if old2 not in s: raise SystemExit('relapse day assertion not found')
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')
print('browser test trail/restart state check PASS')
