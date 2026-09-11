from pathlib import Path
import json

# index.html: version + mobile history layout
p=Path('index.html'); s=p.read_text(encoding='utf-8')
old="const BUILD='V9.0.13';"; new="const BUILD='V9.0.14';"
assert s.count(old)==1, f'BUILD anchor {s.count(old)}'
s=s.replace(old,new,1)
old_css="""  .mn-day{display:flex;gap:10px;padding:11px 0;border-top:1px solid var(--line)}
  .mn-day:first-child{border-top:none}
  .mn-day .d{flex:0 0 128px;font-size:12px;color:var(--dim);line-height:1.6;white-space:nowrap}
  .mn-day .c{flex:1;min-width:0;font-size:13.5px;line-height:1.6;word-break:break-word}
  .mn-day .c em{font-style:normal;color:var(--faint);font-size:12px;margin-right:4px}
"""
new_css="""  .mn-day{display:block;padding:14px 0;border-top:1px solid var(--line)}
  .mn-day:first-child{border-top:none}
  .mn-day .d{display:block;font-size:13px;color:var(--dim);font-weight:600;line-height:1.45;margin-bottom:9px;white-space:normal}
  .mn-day .c{display:block;min-width:0}
  .mn-record-row{display:grid;grid-template-columns:88px minmax(0,1fr);gap:8px;align-items:start;margin:5px 0}
  .mn-record-label{font-size:12px;line-height:1.6;color:var(--faint)}
  .mn-record-value{min-width:0;font-size:13.5px;line-height:1.6;word-break:break-word}
  .mn-record-line{margin-top:10px;padding:10px 12px;border-radius:11px;background:var(--bg)}
  .mn-record-line .mn-record-label{display:block;margin-bottom:4px}
  .mn-record-line .mn-record-value{display:block}
  @media(max-width:380px){.mn-record-row{grid-template-columns:80px minmax(0,1fr)}}
"""
assert s.count(old_css)==1, f'mn-day CSS anchor {s.count(old_css)}'
s=s.replace(old_css,new_css,1)
p.write_text(s,encoding='utf-8')

# meaning-data.js: user-facing value names only; internal keys stay create/exp/att
p=Path('meaning-data.js'); s=p.read_text(encoding='utf-8')
s=s.replace('오늘 한 걸음 V9.0.12','오늘 한 걸음 V9.0.14',1)
old="values: {create:'창조', exp:'경험', att:'태도'},"
new="values: {create:'기여·해냄', exp:'관계·경험', att:'태도·선택'},"
assert s.count(old)==1, f'value anchor {s.count(old)}'
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

# meaning-feature.js: only history card renderer
p=Path('meaning-feature.js'); s=p.read_text(encoding='utf-8')
s=s.replace('V9.0.13 · 의미 돌아보기','V9.0.14 · 의미 돌아보기',1)
start=s.find('function drawMeaningList(){')
end=s.find('function meaningCollected(){',start)
assert start>=0 and end>start, 'drawMeaningList anchors missing'
new_fn="""function drawMeaningList(){const st=wbStore(),keys=Object.keys(st).filter(k=>wbGet(k)).sort().reverse(),box=$('#mn-list'),more=$('#mn-more');if(!keys.length){box.innerHTML='<div class=\"empty\" style=\"margin:8px 0\">아직 남긴 기록이 없습니다.</div>';more.style.display='none';return;}const show=mnListAll?keys:keys.slice(0,14),row=(label,value)=>'<div class=\"mn-record-row\"><span class=\"mn-record-label\">'+esc(label)+'</span><span class=\"mn-record-value\">'+value+'</span></div>';box.innerHTML=show.map(k=>{const r=st[k],parts=[],h=(r.hard||[]).map(x=>(mnItem(MN_HARD,x)||{}).l).filter(Boolean),stg=(r.strength||[]).map(x=>(mnItem(MN_STRENGTH,x)||{}).l).filter(Boolean),act=(r.action||r.did||[]).map(x=>(mnItem(MN_ACTION,x)||{}).l).filter(Boolean);if(typeof r.empty==='number')parts.push(row('공허감',String(Number(r.empty))));if(h.length)parts.push(row('아팠던 것',esc(h.join(' · '))));if(r.hardNote||r.note)parts.push(row('직접 기록',esc(String(r.hardNote||r.note))));if(stg.length)parts.push(row('남아 있던 힘',esc(stg.join(' · '))));if(r.strengthNote)parts.push(row('힘 · 직접',esc(String(r.strengthNote))));if(act.length)parts.push(row('선택·지킨 것',esc(act.join(' · '))));if(r.actionNote)parts.push(row('선택 · 직접',esc(String(r.actionNote))));if(r.request)parts.push(row('삶의 요청',esc(String(r.request))));const line=wbLineById(r.line);if(line)parts.push('<div class=\"mn-record-line\"><span class=\"mn-record-label\">오늘의 문장</span><span class=\"mn-record-value\">'+esc(line.text)+'</span></div>');return '<div class=\"mn-day\"><div class=\"d\">'+esc(wbDateLabel(k))+'</div><div class=\"c\">'+(parts.length?parts.join(''):'<div class=\"mn-record-row\"><span class=\"mn-record-label\">기록</span><span class=\"mn-record-value\">비어 있음</span></div>')+'</div></div>';}).join('');more.style.display=keys.length>14?'':'none';more.textContent=mnListAll?'최근 기록만 보기':'지난 기록 모두 보기';}\n"""
s=s[:start]+new_fn+s[end:]
p.write_text(s,encoding='utf-8')

# verify-meaning.js: update value labels + add layout regression
p=Path('verify-meaning.js'); s=p.read_text(encoding='utf-8')
old="ok(md.values&&md.values.create==='창조'&&md.values.exp==='경험'&&md.values.att==='태도','창조·경험·태도 가치 매핑');"
new="ok(md.values&&md.values.create==='기여·해냄'&&md.values.exp==='관계·경험'&&md.values.att==='태도·선택','사용자용 가치명: 기여·해냄·관계·경험·태도·선택');"
assert s.count(old)==1, f'verify value anchor {s.count(old)}'
s=s.replace(old,new,1)
marker="ok(/getFullYear\\(\\)\\+'년 '/.test(feature),'지난 기록 날짜에 연도 표시');"
add="\nok(index.includes('.mn-day{display:block')&&index.includes('.mn-record-row{display:grid')&&feature.includes('mn-record-line')&&feature.includes('<div class=\\\"d\\\">'),'지난 기록 모바일: 날짜 상단·내용 전체폭·오늘의 문장 별도 블록');"
assert s.count(marker)==1, f'history marker {s.count(marker)}'
s=s.replace(marker,marker+add,1)
s=s.replace('V9.0.13 의미 돌아보기·기록 다시보기 회귀검증 통과','V9.0.14 의미 돌아보기·기록 다시보기 회귀검증 통과')
p.write_text(s,encoding='utf-8')

# verify.js BUILD assertion only
p=Path('verify.js'); s=p.read_text(encoding='utf-8')
assert "const BUILD='V9.0.13';" in s, 'verify BUILD anchor missing'
s=s.replace("const BUILD='V9.0.13';","const BUILD='V9.0.14';")
s=s.replace('V9.0.13 BUILD 불일치','V9.0.14 BUILD 불일치')
p.write_text(s,encoding='utf-8')

# sw.js
p=Path('sw.js'); s=p.read_text(encoding='utf-8')
for old,new in [
    ("const APP_VERSION = 'V9.0.13';","const APP_VERSION = 'V9.0.14';"),
    ("const V = 'ohg-v9013-meaning-urge-review-r1';","const V = 'ohg-v9014-meaning-history-mobile-r1';")]:
    assert s.count(old)==1, f'sw anchor {old} count={s.count(old)}'
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

# latest-release.json
p=Path('latest-release.json'); d=json.loads(p.read_text(encoding='utf-8'))
d.update({
    'version':'V9.0.14',
    'versionCode':909,
    'apk':'https://github.com/HanTae-ho/oneul-web/releases/download/v9.0.14-test/oneul-v9.0.14.apk',
    'release':'https://github.com/HanTae-ho/oneul-web/releases/tag/v9.0.14-test'
})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
