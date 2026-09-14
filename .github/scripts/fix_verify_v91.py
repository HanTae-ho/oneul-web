from pathlib import Path
p=Path('verify.js')
s=p.read_text(encoding='utf-8')
old="ok(/<b>의미점검 보기<\\/b>/.test(practiceSection)&&/<b>회복 실천도구<\\/b>/.test(practiceSection),'실천하기 압축 제목 반영');"
new="""ok(/<b>의미점검<\\/b>/.test(practiceSection)&&/<b>회복 실천도구<\\/b>/.test(practiceSection),'실천하기 압축 제목 반영');
ok(/id=\"tool-check-view\"[\\s\\S]{0,240}<b>자가점검 기록<\\/b>/.test(index),'자가점검 기록 명칭 반영');
ok(/\\{v:'meaning',l:'의미'\\}/.test(index),'내 발자취 실천기록 의미 필터');"""
if s.count(old)!=1:
    raise SystemExit(f'old invariant count={s.count(old)}')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
