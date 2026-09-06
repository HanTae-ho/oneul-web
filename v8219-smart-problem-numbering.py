from pathlib import Path

idx = Path('index.html')
sw = Path('sw.js')
s = idx.read_text(encoding='utf-8')
w = sw.read_text(encoding='utf-8')

repls = [
    ("const BUILD = 'V8.2.18';", "const BUILD = 'V8.2.19';"),
    ("smartProblemField('문제는 일반적으로 언제 발생합니까? 언제 일어날 가능성이 있습니까?'", "smartProblemField('1-1 · 문제는 일반적으로 언제 발생합니까? 언제 일어날 가능성이 있습니까?'"),
    ("smartProblemField('누가 관련되어 있나요? 또 누가 참여할 가능성이 있나요?'", "smartProblemField('1-2 · 누가 관련되어 있나요? 또 누가 참여할 가능성이 있나요?'"),
    ("smartProblemField('보통 무슨 일이 일어나나요? 무슨 일이 일어날 것 같나요?'", "smartProblemField('1-3 · 보통 무슨 일이 일어나나요? 무슨 일이 일어날 것 같나요?'"),
    ("smartProblemField('이 상황에 대한 나의 일반적인 생각과 감정은 무엇입니까?'", "smartProblemField('1-4 · 이 상황에 대한 나의 일반적인 생각과 감정은 무엇입니까?'"),
    ("smartProblemSection('1 · 언제 발생하나요?',r.when)", "smartProblemSection('1-1 · 언제 발생하나요?',r.when)"),
    ("smartProblemSection('1 · 누가 관련되어 있나요?',r.who)", "smartProblemSection('1-2 · 누가 관련되어 있나요?',r.who)"),
    ("smartProblemSection('1 · 무슨 일이 일어나나요?',r.what)", "smartProblemSection('1-3 · 무슨 일이 일어나나요?',r.what)"),
    ("smartProblemSection('1 · 생각과 감정',r.thoughts)", "smartProblemSection('1-4 · 생각과 감정',r.thoughts)"),
]
for old, new in repls:
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'expected exactly one match for {old!r}, found {count}')
    s = s.replace(old, new, 1)

sw_repls = [
    ("const APP_VERSION = 'V8.2.18';", "const APP_VERSION = 'V8.2.19';"),
    ("const V = 'ohg-v8218-smart-accordion';", "const V = 'ohg-v8219-smart-problem-numbering';"),
]
for old, new in sw_repls:
    count = w.count(old)
    if count != 1:
        raise SystemExit(f'expected exactly one SW match for {old!r}, found {count}')
    w = w.replace(old, new, 1)

if "const DATA_SCHEMA = 6;" not in s:
    raise SystemExit('DATA_SCHEMA changed unexpectedly')

idx.write_text(s, encoding='utf-8')
sw.write_text(w, encoding='utf-8')
print('V8.2.19 numbering patch PASS')
