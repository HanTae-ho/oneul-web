from pathlib import Path
import json

p=Path('index.html'); s=p.read_text(encoding='utf-8')
old="const BUILD='V9.0.14';"; new="const BUILD='V9.0.15';"
assert s.count(old)==1, f'BUILD anchor {s.count(old)}'
s=s.replace(old,new,1); p.write_text(s,encoding='utf-8')

p=Path('meaning-feature.js'); s=p.read_text(encoding='utf-8')
s=s.replace('V9.0.14 · 의미 돌아보기','V9.0.15 · 의미 돌아보기',1)
old="function wbTodayUrges(d){return (Array.isArray(S.urges)?S.urges:[]).filter(x=>x&&x.t&&ymd(Number(x.t))===d).sort((a,b)=>Number(b.t||0)-Number(a.t||0));}"
new="function wbUrgesForDate(d){return (Array.isArray(S.urges)?S.urges:[]).filter(x=>x&&x.t&&ymd(Number(x.t))===d).sort((a,b)=>Number(b.t||0)-Number(a.t||0));}\nfunction wbTodayUrges(d){return wbUrgesForDate(d);}"
assert s.count(old)==1, f'urge helper anchor {s.count(old)}'; s=s.replace(old,new,1)
anchor="function meaningTopKeys(counts,limit){return Object.keys(counts).sort((a,b)=>counts[b]-counts[a]||String(a).localeCompare(String(b),'ko')).slice(0,limit);}"
add="function showMeaningUrgesForDate(d){const rows=wbUrgesForDate(d);if(!rows.length){toast('이날의 충동기록이 없습니다.');return;}modal('<h2>'+esc(wbDateLabel(d))+' 충동기록</h2><p class=\"muted\" style=\"margin:6px 0 10px\">의미기록과 합치지 않고 같은 날짜의 충동일기를 연결해 보여줍니다.</p><div>'+rows.map(meaningUrgeLine).join('')+'</div><button class=\"btn ghost\" id=\"mn-date-urge-diary\" style=\"margin-top:10px\">충동일기 전체 보기</button>');const b=$('#mn-date-urge-diary');if(b)b.onclick=()=>{closeModal();go('urge-diary');};}\nfunction openMeaningHistoryDay(d){closeModal();setMeaningView('history');setTimeout(()=>{const card=document.querySelector('[data-mn-day=\"'+d+'\"]');if(card&&card.scrollIntoView)card.scrollIntoView({behavior:'smooth',block:'start'});},60);}"
assert s.count(anchor)==1, f'meaningTopKeys anchor {s.count(anchor)}'; s=s.replace(anchor,anchor+'\n'+add,1)
s=s.replace('기록이 쌓이면 자주 보인 힘과 지킨 가치를 여기에서 확인할 수 있습니다.','기록이 쌓이면 기록에서 보인 힘과 지킨 가치를 여기에서 확인할 수 있습니다.',1)
s=s.replace('>자주 보인 힘<','>기록에서 보인 힘<',1)
s=s.replace('>자주 지킨 가치<','>기록에서 지킨 가치<',1)
start=s.find('function showMeaningExistingChoice(d,r){'); end=s.find('function drawMeaning(opts){',start)
assert start>=0 and end>start, 'showMeaningExistingChoice anchors missing'
new_choice="function showMeaningExistingChoice(d,r){modal('<h2>오늘 작성한 기록이 있습니다</h2><p class=\"muted\" style=\"margin:6px 0 14px\">오늘 기록을 먼저 확인하거나, 기존 기록을 이어서 수정하거나, 빈 화면에서 처음부터 다시 작성할 수 있습니다.<br><b>처음부터 다시 작성해도 새 내용을 저장하기 전까지 기존 기록은 지워지지 않습니다.</b></p><button class=\"btn ghost\" id=\"mn-view-existing\">오늘 기록 보기</button><button class=\"btn\" id=\"mn-edit-existing\" style=\"margin-top:8px\">기존 기록 수정하기</button><button class=\"btn ghost\" id=\"mn-restart-existing\" style=\"margin-top:8px\">처음부터 다시 작성</button>');$('#mn-view-existing').onclick=()=>openMeaningHistoryDay(d);$('#mn-edit-existing').onclick=()=>{mnReplaceExisting=false;closeModal();renderMeaningDraft(d,r,false);};$('#mn-restart-existing').onclick=()=>{mnReplaceExisting=true;closeModal();renderMeaningDraft(d,null,true);setMeaningView('today');};}\n"
s=s[:start]+new_choice+s[end:]
start=s.find('function drawMeaningList(){'); end=s.find('function meaningCollected(){',start)
assert start>=0 and end>start, 'drawMeaningList anchors missing'; old_fn=s[start:end]
old_piece="const line=wbLineById(r.line);if(line)parts.push('<div class=\"mn-record-line\"><span class=\"mn-record-label\">오늘의 문장</span><span class=\"mn-record-value\">'+esc(line.text)+'</span></div>');return '<div class=\"mn-day\"><div class=\"d\">'+esc(wbDateLabel(k))+'</div><div class=\"c\">'+(parts.length?parts.join(''):'<div class=\"mn-record-row\"><span class=\"mn-record-label\">기록</span><span class=\"mn-record-value\">비어 있음</span></div>')+'</div></div>';}).join('');more.style.display=keys.length>14?'':'none';more.textContent=mnListAll?'최근 기록만 보기':'지난 기록 모두 보기';}"
new_piece="const line=wbLineById(r.line);if(line)parts.push('<div class=\"mn-record-line\"><span class=\"mn-record-label\">오늘의 문장</span><span class=\"mn-record-value\">'+esc(line.text)+'</span></div>');const urges=wbUrgesForDate(k),urgeLink=urges.length?'<button class=\"btn ghost sm mn-day-urge-btn\" type=\"button\" data-d=\"'+esc(k)+'\" style=\"margin-top:10px\">이날의 충동기록 '+urges.length+'건 보기</button>':'';return '<div class=\"mn-day\" data-mn-day=\"'+esc(k)+'\"><div class=\"d\">'+esc(wbDateLabel(k))+'</div><div class=\"c\">'+(parts.length?parts.join(''):'<div class=\"mn-record-row\"><span class=\"mn-record-label\">기록</span><span class=\"mn-record-value\">비어 있음</span></div>')+urgeLink+'</div></div>';}).join('');box.querySelectorAll('.mn-day-urge-btn').forEach(b=>b.onclick=()=>showMeaningUrgesForDate(b.dataset.d));more.style.display=keys.length>14?'':'none';more.textContent=mnListAll?'최근 기록만 보기':'지난 기록 모두 보기';}"
assert old_piece in old_fn, 'drawMeaningList replacement segment missing'; s=s[:start]+old_fn.replace(old_piece,new_piece,1)+s[end:]
p.write_text(s,encoding='utf-8')

p=Path('verify-meaning.js'); s=p.read_text(encoding='utf-8')
old="ok(/function wbTodayUrges\\(d\\)/.test(feature)&&/Array\\.isArray\\(S\\.urges\\)/.test(feature)&&/ymd\\(Number\\(x\\.t\\)\\)===d/.test(feature),'오늘 충동기록만 로컬 날짜 기준 참고 조회');"
new="ok(/function wbUrgesForDate\\(d\\)/.test(feature)&&/function wbTodayUrges\\(d\\)\\{return wbUrgesForDate\\(d\\);\\}/.test(feature)&&/Array\\.isArray\\(S\\.urges\\)/.test(feature)&&/ymd\\(Number\\(x\\.t\\)\\)===d/.test(feature),'날짜별 충동기록을 로컬 날짜 기준 동적 조회');"
assert s.count(old)==1; s=s.replace(old,new,1)
old="ok(/function showMeaningExistingChoice\\(d,r\\)/.test(feature)&&/기존 기록 수정하기/.test(feature)&&/처음부터 다시 작성/.test(feature),'오늘 기존 의미기록 진입 시 수정·처음부터 다시 작성 선택');"
new="ok(/function showMeaningExistingChoice\\(d,r\\)/.test(feature)&&/오늘 기록 보기/.test(feature)&&/기존 기록 수정하기/.test(feature)&&/처음부터 다시 작성/.test(feature),'오늘 기존 의미기록 진입 시 보기·수정·처음부터 다시 작성 선택');"
assert s.count(old)==1; s=s.replace(old,new,1)
old="ok(/function drawMeaningHistorySummary\\(\\)/.test(feature)&&/자주 보인 힘/.test(feature)&&/자주 지킨 가치/.test(feature),'2단계 기록 다시보기: 힘·가치 흐름');"
new="ok(/function drawMeaningHistorySummary\\(\\)/.test(feature)&&/기록에서 보인 힘/.test(feature)&&/기록에서 지킨 가치/.test(feature)&&!/자주 보인 힘/.test(feature)&&!/자주 지킨 가치/.test(feature),'2단계 기록 다시보기: 중립적 힘·가치 제목');"
assert s.count(old)==1; s=s.replace(old,new,1)
marker="ok(index.includes('.mn-day{display:block')&&index.includes('.mn-record-row{display:grid')&&feature.includes('mn-record-line')&&feature.includes('<div class=\\\"d\\\">'),'지난 기록 모바일: 날짜 상단·내용 전체폭·오늘의 문장 별도 블록');"
add="\nok(/function showMeaningUrgesForDate\\(d\\)/.test(feature)&&/이날의 충동기록/.test(feature)&&/mn-day-urge-btn/.test(feature)&&/data-mn-day/.test(feature),'지난 의미기록에 같은 날짜 충동기록 동적 연결');\nok(/function openMeaningHistoryDay\\(d\\)/.test(feature)&&/mn-view-existing/.test(feature)&&/setMeaningView\\('history'\\)/.test(feature),'오늘 기록 보기에서 지난 기록의 오늘 카드로 이동');"
assert s.count(marker)==1; s=s.replace(marker,marker+add,1)
s=s.replace('V9.0.14 의미 돌아보기·기록 다시보기 회귀검증 통과','V9.0.15 의미 돌아보기·기록 다시보기 회귀검증 통과')
p.write_text(s,encoding='utf-8')

p=Path('verify.js'); s=p.read_text(encoding='utf-8')
assert "const BUILD='V9.0.14';" in s; s=s.replace("const BUILD='V9.0.14';","const BUILD='V9.0.15';"); s=s.replace('V9.0.14 BUILD 불일치','V9.0.15 BUILD 불일치'); p.write_text(s,encoding='utf-8')

p=Path('sw.js'); s=p.read_text(encoding='utf-8')
for old,new in [("const APP_VERSION = 'V9.0.14';","const APP_VERSION = 'V9.0.15';"),("const V = 'ohg-v9014-meaning-history-mobile-r1';","const V = 'ohg-v9015-meaning-linked-urge-view-r1';")]: assert s.count(old)==1; s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

p=Path('latest-release.json'); d=json.loads(p.read_text(encoding='utf-8')); d.update({'version':'V9.0.15','versionCode':910,'apk':'https://github.com/HanTae-ho/oneul-web/releases/download/v9.0.15-test/oneul-v9.0.15.apk','release':'https://github.com/HanTae-ho/oneul-web/releases/tag/v9.0.15-test'}); p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
