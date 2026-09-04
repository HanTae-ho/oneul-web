from pathlib import Path

p=Path('v822-urge-diary.py')
s=p.read_text(encoding='utf-8')
start=s.index('# reading from urge/timer is also a coping strategy and must not erase draft')
end=s.index('# tools summary and entry', start)
block=r'''# reading from urge/timer is also a coping strategy and must not erase draft
pat_read=r"\$\('#tm-read'\)\.onclick\s*=\s*\(\)\s*=>\s*openRead\('timer'\);[^\n]*\n\$\('#ur-read'\)\.onclick\s*=\s*\(\)\s*=>\s*openRead\('urge'\);"
m_read=re.search(pat_read,s)
if not m_read:
    raise SystemExit('read-cope handlers not found')
read_new="$('#tm-read').onclick = () => { urgeUseCope('도움되는 글 읽기'); openRead('timer'); };   /* 타이머는 계속 돕습니다 */\n$('#ur-read').onclick = () => { urgeUseCope('도움되는 글 읽기'); openRead('urge'); };"
s=s[:m_read.start()]+read_new+s[m_read.end():]

'''
s=s[:start]+block+s[end:]
p.write_text(s,encoding='utf-8')
print('helper matcher fixed')
