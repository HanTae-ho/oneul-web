from pathlib import Path

idx=Path('index.html')
sw=Path('sw.js')
s=idx.read_text(encoding='utf-8')
w=sw.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    s=s.replace(old,new,1)

once("const BUILD = 'V8.2.20';","const BUILD = 'V8.2.21';",'BUILD')
once("SMART Recovery 번역본의 <b>문제 해결을 위한 5단계</b>와 문제 해결 워크시트를 앱에 맞게 옮겼으며", "SMART Recovery의 <b>문제 해결을 위한 5단계</b>와 문제 해결 워크시트를 바탕으로 앱에 맞게 구성했으며", 'problem solving user text')
once("SMART Recovery 번역본의 <b>Lifestyle Balance Pie</b>를 모바일에 맞게 옮겼으며", "SMART Recovery의 <b>Lifestyle Balance Pie</b>를 바탕으로 모바일에 맞게 구성했으며", 'balance pie user text')
once("번역본 돌아보기 질문 전체 보기", "삶을 돌아보는 질문 전체 보기", 'balance prompt toggle')
once("   번역본 Point 3의 '삶의 문제 해결 / 문제 해결을 위한 5단계'와", "   SMART Recovery Point 3의 '삶의 문제 해결 / 문제 해결을 위한 5단계'와", 'problem solving comment')
once("   번역본 Point 4의 Lifestyle Balance Pie: 삶의 영역을 정하고 0~10 만족도를 표시한 뒤", "   SMART Recovery Point 4의 Lifestyle Balance Pie: 삶의 영역을 정하고 0~10 만족도를 표시한 뒤", 'balance pie comment')

if '번역본' in s:
    raise SystemExit('index.html still contains forbidden user-facing/source-process term: 번역본')

w=w.replace("const APP_VERSION = 'V8.2.20';","const APP_VERSION = 'V8.2.21';",1)
w=w.replace("const V = 'ohg-v8220-smart-balance-pie';","const V = 'ohg-v8221-user-wording-cleanup';",1)
if "V8.2.21" not in w or "ohg-v8221-user-wording-cleanup" not in w:
    raise SystemExit('sw.js version/cache update failed')

idx.write_text(s,encoding='utf-8')
sw.write_text(w,encoding='utf-8')
