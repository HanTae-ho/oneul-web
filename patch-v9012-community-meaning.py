from pathlib import Path
import json


def once(s, old, new, label):
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 anchor, found {n}')
    return s.replace(old,new,1)

# index.html
p=Path('index.html'); s=p.read_text(encoding='utf-8')
s=once(s,"const BUILD='V9.0.11';","const BUILD='V9.0.12';",'BUILD')
# 사용자에게 보이는 명칭만 한국어 수준에서 통일합니다. social route/상수/함수명은 변경하지 않습니다.
s=s.replace('소셜','커뮤니티')

css_anchor="  .mn-empty{display:grid;grid-template-columns:repeat(5,1fr);gap:7px}"
css_new="""  .mn-view-tabs{display:flex;gap:7px;margin:0 0 12px}
  .mn-view-tabs button{flex:1;border:1px solid var(--line);border-radius:11px;padding:10px 7px;color:var(--dim);background:var(--panel)}
  .mn-view-tabs button.on{border-color:var(--acc);color:var(--acc);background:var(--accbg);font-weight:600}
  .mn-empty{display:grid;grid-template-columns:repeat(5,1fr);gap:7px}"""
s=once(s,css_anchor,css_new,'meaning tabs css')

open_anchor="""  </div>
  <div class=\"note\" style=\"margin-bottom:12px\">오늘의 경험에서 아팠던 것, 남아 있던 힘, 내가 지킨 것을 짧게 돌아봅니다.<br><b id=\"mn-date\"></b></div>"""
open_new="""  </div>
  <div class=\"mn-view-tabs\" id=\"mn-view-tabs\">
    <button type=\"button\" class=\"on\" data-mn-view=\"today\">오늘 돌아보기</button>
    <button type=\"button\" data-mn-view=\"history\">지난 기록</button>
  </div>
  <div id=\"mn-view-today\">
  <div class=\"note\" style=\"margin-bottom:12px\">오늘의 경험에서 아팠던 것, 남아 있던 힘, 내가 지킨 것을 짧게 돌아봅니다.<br><b id=\"mn-date\"></b></div>"""
s=once(s,open_anchor,open_new,'meaning today tab open')

history_old="""  <button class=\"btn\" id=\"mn-save\">저장하기</button><div style=\"height:9px\"></div><button class=\"btn ghost\" id=\"mn-clear\" style=\"display:none;color:var(--bad);border-color:var(--bad)\">오늘 기록 지우기</button>
  <div class=\"sep\"></div><h2 style=\"font-size:15px;margin:0 0 9px\">지난 기록</h2><div class=\"card\" style=\"padding-top:4px;padding-bottom:4px\"><div id=\"mn-list\"></div></div><button class=\"btn ghost sm\" id=\"mn-more\" style=\"display:none\"></button>
  <p class=\"tiny\" style=\"margin:12px 0 0\">이 기록은 이 기기 안에만 남습니다. 서버나 마음프로로 자동 전송하지 않습니다.</p>"""
history_new="""  <button class=\"btn\" id=\"mn-save\">저장하기</button><div style=\"height:9px\"></div><button class=\"btn ghost\" id=\"mn-clear\" style=\"display:none;color:var(--bad);border-color:var(--bad)\">오늘 기록 지우기</button>
  </div>
  <div id=\"mn-view-history\" class=\"hide\">
    <div class=\"card\" style=\"padding-top:4px;padding-bottom:4px\"><div id=\"mn-list\"></div></div><button class=\"btn ghost sm\" id=\"mn-more\" style=\"display:none\"></button>
  </div>
  <p class=\"tiny\" style=\"margin:12px 0 0\">이 기록은 이 기기 안에만 남습니다. 서버나 마음프로로 자동 전송하지 않습니다.</p>"""
s=once(s,history_old,history_new,'meaning history tab split')
p.write_text(s,encoding='utf-8')

# meaning-data.js: 기존 key를 보존해 V9.0.11 저장기록 호환
p=Path('meaning-data.js'); s=p.read_text(encoding='utf-8')
s=once(s,'/* 오늘 한 걸음 V9.0.11 — 의미 돌아보기 기본 자료','/* 오늘 한 걸음 V9.0.12 — 의미 돌아보기 기본 자료','meaning data version comment')
s=once(s,'  ver: 2,','  ver: 3,','meaning data ver')
old="""  strength: [
    {k:'hold', l:'버티기'},
    {k:'family', l:'가족'},
    {k:'help', l:'도움요청'}
  ],"""
new="""  strength: [
    {k:'hold', l:'버티기'},
    {k:'recoveryWill', l:'회복하려는 마음'},
    {k:'hope', l:'희망'},
    {k:'selfProtect', l:'나를 지키려는 마음'},
    {k:'family', l:'가족'},
    {k:'help', l:'도움받을 사람'},
    {k:'learning', l:'회복에서 배운 것'},
    {k:'restart', l:'다시 시작할 마음'}
  ],"""
s=once(s,old,new,'strength chips')
p.write_text(s,encoding='utf-8')

# meaning-feature.js
p=Path('meaning-feature.js'); s=p.read_text(encoding='utf-8')
s=once(s,'   V9.0.11 · 의미 돌아보기 — 하루 한 장','   V9.0.12 · 의미 돌아보기 — 하루 한 장','feature version comment')
old="let mnDraft={d:'',hard:[],hardNote:'',strength:[],strengthNote:'',action:[],actionNote:'',empty:null,request:'',line:''},mnListAll=false,mnLineOffset=0;"
new="""let mnDraft={d:'',hard:[],hardNote:'',strength:[],strengthNote:'',action:[],actionNote:'',empty:null,request:'',line:''},mnListAll=false,mnLineOffset=0,mnView='today';
function setMeaningView(v){mnView=v==='history'?'history':'today';const today=$('#mn-view-today'),history=$('#mn-view-history');if(today)today.classList.toggle('hide',mnView!=='today');if(history)history.classList.toggle('hide',mnView!=='history');$$('[data-mn-view]').forEach(b=>b.classList.toggle('on',b.dataset.mnView===mnView));if(mnView==='history')drawMeaningList();const view=$('#view');if(view)view.scrollTop=0;}"""
s=once(s,old,new,'meaning view state')
old="$('#mn-clear').style.display=r?'':'none';drawMeaningChips();drawMeaningEmpty();drawMeaningLines();drawMeaningList();}"
new="$('#mn-clear').style.display=r?'':'none';drawMeaningChips();drawMeaningEmpty();drawMeaningLines();drawMeaningList();setMeaningView('today');}"
s=once(s,old,new,'default today tab')
old="$('#mn-empty-skip').onclick=()=>{mnDraft.empty=null;drawMeaningEmpty();};$('#mn-lines-more').onclick=()=>{mnLineOffset+=3;drawMeaningLines();};$('#mn-more').onclick=()=>{mnListAll=!mnListAll;drawMeaningList();};"
new="$('#mn-empty-skip').onclick=()=>{mnDraft.empty=null;drawMeaningEmpty();};$('#mn-lines-more').onclick=()=>{mnLineOffset+=3;drawMeaningLines();};$('#mn-more').onclick=()=>{mnListAll=!mnListAll;drawMeaningList();};$$('[data-mn-view]').forEach(b=>b.onclick=()=>setMeaningView(b.dataset.mnView));"
s=once(s,old,new,'meaning tab handlers')
p.write_text(s,encoding='utf-8')

# verify-meaning.js
p=Path('verify-meaning.js'); s=p.read_text(encoding='utf-8')
s=once(s,"ok(md&&md.ver===2,'의미 돌아보기 데이터 버전');","ok(md&&md.ver===3,'의미 돌아보기 데이터 버전');",'verify data ver')
s=once(s,"ok(Array.isArray(md.strength)&&md.strength.length>=3,'남아 있던 힘 선택지');","ok(Array.isArray(md.strength)&&md.strength.length===8&&['hold','recoveryWill','hope','selfProtect','family','help','learning','restart'].every(k=>md.strength.some(x=>x.k===k)),'남아 있던 힘 8개 선택지·기존 키 보존');",'verify strength chips')
anchor="ok(index.includes('id=\"p-meaning\"')&&index.includes('id=\"tool-meaning\"')&&index.includes('id=\"ni-meaning\"'),'회복도구·하루마무리 두 진입점');"
addition=anchor+"\nok(index.includes('id=\"mn-view-tabs\"')&&index.includes('data-mn-view=\"today\"')&&index.includes('data-mn-view=\"history\"')&&index.includes('id=\"mn-view-history\" class=\"hide\"'),'의미 돌아보기 오늘·지난 기록 2탭');\nok(/function setMeaningView\(v\)/.test(feature)&&/setMeaningView\('today'\)/.test(feature),'의미 돌아보기 기본 오늘 탭·탭 전환 로직');"
s=once(s,anchor,addition,'verify meaning tabs')
s=s.replace('V9.0.11 의미 돌아보기 회귀검증 통과','V9.0.12 의미 돌아보기 회귀검증 통과')
p.write_text(s,encoding='utf-8')

# verify.js: 사용자 명칭 및 빌드 검증 현행화
p=Path('verify.js'); s=p.read_text(encoding='utf-8')
s=s.replace('소셜','커뮤니티')
s=once(s,"const BUILD='V9.0.11';","const BUILD='V9.0.12';",'verify build literal')
# 위 replace로 에러문구만 바뀌고 실제 fixed BUILD 검사 문자열은 위 once가 처리함
anchor="ok(/SOCIAL_FEED_CACHE_KEY='ohg\\.social\\.feed\\.v1'/.test(index)&&/function socialFeedCacheLoad\\(sort\\)/.test(index)&&/function socialFeedCacheSave\\(sort,items\\)/.test(index),'커뮤니티 피드 기기 캐시 선표시');"
add=anchor+"\nok(/data-t=\"social\"[\\s\\S]{0,400}>커뮤니티<\\/button>/.test(index)&&/<section class=\"pg\" id=\"p-social\">[\\s\\S]{0,200}<h1>커뮤니티<\\/h1>/.test(index),'하단 탭·페이지 사용자 명칭 커뮤니티');\nok(index.includes(\"const SOCIAL_KEY = 'ohg.social.v1';\")&&/const TABBED = \\['home','tools','help','ai','social'\\]/.test(index),'커뮤니티 명칭 변경 후 social 내부 route·저장키 유지');"
s=once(s,anchor,add,'verify community label')
p.write_text(s,encoding='utf-8')

# sw.js
p=Path('sw.js'); s=p.read_text(encoding='utf-8')
s=once(s,"const APP_VERSION = 'V9.0.11';","const APP_VERSION = 'V9.0.12';",'sw app version')
s=once(s,"const V = 'ohg-v9011-meaning-r1';","const V = 'ohg-v9012-community-meaning-ui-r1';",'sw cache')
p.write_text(s,encoding='utf-8')

# latest-release.json
p=Path('latest-release.json'); obj=json.loads(p.read_text(encoding='utf-8'))
obj.update({
  'version':'V9.0.12',
  'versionCode':907,
  'apk':'https://github.com/HanTae-ho/oneul-web/releases/download/v9.0.12-test/oneul-v9.0.12.apk',
  'release':'https://github.com/HanTae-ho/oneul-web/releases/tag/v9.0.12-test'
})
p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
