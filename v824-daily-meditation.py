from pathlib import Path

idx = Path('index.html')
sw = Path('sw.js')

idx_text = idx.read_text(encoding='utf-8')
sw_text = sw.read_text(encoding='utf-8')

idx_text = idx_text.replace("const BUILD = 'V8.2.3';", "const BUILD = 'V8.2.4';", 1)
sw_text = sw_text.replace("const APP_VERSION = 'V8.2.3';", "const APP_VERSION = 'V8.2.4';", 1)
sw_text = sw_text.replace("const V = 'ohg-v823-smart-learning';", "const V = 'ohg-v824-daily-meditation';", 1)

old = """  const a = DAILY_HOME_A[serial % DAILY_HOME_A.length];\n  const b = DAILY_HOME_B[Math.floor(serial / DAILY_HOME_A.length) % DAILY_HOME_B.length];\n  return a + ' ' + b;\n"""
new = """  const aLen = DAILY_HOME_A.length;\n  const bLen = DAILY_HOME_B.length;\n  const aIdx = serial % aLen;\n  const cycle = Math.floor(serial / aLen);\n  /* 두 문장 모두 매일 바뀌되, (A,B) 24×24 조합은 576일 동안 중복 없이 순환합니다. */\n  const bIdx = (cycle + aIdx) % bLen;\n  const a = DAILY_HOME_A[aIdx];\n  const b = DAILY_HOME_B[bIdx];\n  return a + ' ' + b;\n"""
if old not in idx_text:
    raise SystemExit('daily meditation formula anchor not found')
idx_text = idx_text.replace(old, new, 1)

idx.write_text(idx_text, encoding='utf-8')
sw.write_text(sw_text, encoding='utf-8')
