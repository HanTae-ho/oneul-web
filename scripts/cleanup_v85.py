from pathlib import Path
for fn in ['index.html','install.html','sw.js','privacy.html','legal.html','README.md']:
    p=Path(fn)
    if not p.exists():
        continue
    text=p.read_text(encoding='utf-8')
    had_nl=text.endswith('\n')
    cleaned='\n'.join(line.rstrip() for line in text.splitlines())
    if had_nl:
        cleaned+='\n'
    p.write_text(cleaned,encoding='utf-8')
