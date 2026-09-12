from pathlib import Path
import json

root=Path('.')
idx=root/'index.html'
s=idx.read_text(encoding='utf-8')
assert "const BUILD='V9.0.17';" in s
s=s.replace("const BUILD='V9.0.17';","const BUILD='V9.0.18';",1)

start_marker='  <div class="toolsec">\n    <h2>실천하기</h2>'
start=s.index(start_marker)
end=s.index('\n\n  <div class="toolsec">',start+len(start_marker))
new='''  <div class="toolsec">
    <h2>실천하기</h2>
    <div class="learnmini practice-mini">
      <button class="minitool" id="tool-meaning">
        <span class="ic" data-ico="sprout"></span><b>의미 돌아보기</b><span id="tool-meaning-s">오늘 의미 돌아보기</span>
      </button>
      <button class="minitool" id="tool-meaning-check-direct" onclick="openMeaningCheckDirect()">
        <span class="ic" data-ico="check"></span><b>의미점검 바로하기</b><span id="tool-meaning-check-s">10문항 · 의미 흐름 점검</span>
      </button>
      <button class="minitool hide" id="tool-family-tools">
        <span class="ic" data-ico="family"></span><b>가족을 위한 도구</b><span>경계 · 대화 · 대응계획</span>
      </button>
      <button class="minitool" id="tool-workbook">
        <span class="ic" data-ico="check"></span><b>12단계 점검</b><span>1·4·8·9·10·11·12</span>
      </button>
      <button class="minitool" id="tool-smart-tools">
        <span class="ic" data-ico="check"></span><b>회복 실천도구</b><span id="tool-smart-tools-s">4개 영역 · 필요한 도구</span>
      </button>
      <button class="minitool" id="tool-urge-diary">
        <span class="ic" data-ico="wave"></span><b>충동일기</b><span id="tool-urge-diary-s">충동 기록하기</span>
      </button>
      <button class="minitool" id="tool-capsule">
        <span class="ic" data-ico="speak"></span><b>미래의 나에게</b><span id="tool-capsule-s">회복 마음 남기기</span>
      </button>
    </div>
  </div>'''
s=s[:start]+new+s[end:]

repls=[
("caps.textContent=capsuleHas()?'내가 남긴 메시지가 있습니다 · 힘들 때 다시 보기':'회복을 시작한 마음을 남겨두기';","caps.textContent=capsuleHas()?'메시지 있음 · 다시 보기':'회복 마음 남기기';"),
("if(uds) uds.textContent=(S.urges||[]).length ? ('저장된 충동 기록 '+S.urges.length+'건'+(S.urgeDraft?' · 작성 중 1건':'')) : (S.urgeDraft?'작성 중인 기록이 있습니다':'언제·무엇 때문에 힘들었는지 돌아보기');","if(uds) uds.textContent=(S.urges||[]).length ? ('충동 기록 '+S.urges.length+'건'+(S.urgeDraft?' · 작성 중':'')) : (S.urgeDraft?'작성 중 · 이어서':'충동 기록하기');"),
("mns.textContent=todayMeaning?'오늘 기록이 있습니다 · 다시 돌아보기':'오늘의 경험에서 나에게 중요한 것을 돌아보기';","mns.textContent=todayMeaning?'오늘 기록 있음 · 다시 보기':'오늘 의미 돌아보기';"),
("mcs.textContent=draft?('작성 중 '+done+'/10문항 · 이어서 하기'):(todayCheck?('오늘 결과 '+Number(todayCheck.total||0)+'/40 · 결과 보기'):(checks.length?'10문항 점검 · 이전 결과와 비교':'10문항으로 내 의미의 흐름을 짧게 점검하기'));","mcs.textContent=draft?('작성 중 '+done+'/10 · 이어서'):(todayCheck?('오늘 '+Number(todayCheck.total||0)+'/40 · 결과 보기'):(checks.length?'10문항 · 이전과 비교':'10문항 · 의미 흐름 점검'));"),
]
for old,new_text in repls:
    assert old in s, old
    s=s.replace(old,new_text,1)
idx.write_text(s,encoding='utf-8')

sw=root/'sw.js'; t=sw.read_text(encoding='utf-8')
assert "const APP_VERSION = 'V9.0.17';" in t and "const V = 'ohg-v9017-meaning-check-ux-r1';" in t
t=t.replace("const APP_VERSION = 'V9.0.17';","const APP_VERSION = 'V9.0.18';",1).replace("const V = 'ohg-v9017-meaning-check-ux-r1';","const V = 'ohg-v9018-practice-grid-r1';",1)
sw.write_text(t,encoding='utf-8')

latest={
  'version':'V9.0.18',
  'versionCode':913,
  'apk':'https://github.com/HanTae-ho/oneul-web/releases/download/v9.0.18-test/oneul-v9.0.18.apk',
  'release':'https://github.com/HanTae-ho/oneul-web/releases/tag/v9.0.18-test'
}
(root/'latest-release.json').write_text(json.dumps(latest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

v=root/'verify.js'; q=v.read_text(encoding='utf-8')
old="if(!index.includes(\"const BUILD='V9.0.17';\")) throw new Error('V9.0.17 BUILD 불일치');"
assert old in q
new="""const practiceSection=(index.match(/<h2>실천하기<\\/h2>([\\s\\S]*?)<div class=\"toolsec\">/)||[])[1]||'';
ok(/learnmini practice-mini/.test(practiceSection),'실천하기 배우기형 3열 그리드');
ok((practiceSection.match(/class=\"minitool/g)||[]).length===7,'실천하기 7개 카드 압축형');
ok(!/class=\"toolcard/.test(practiceSection)&&!/class=\"go\"/.test(practiceSection),'실천하기 목록형·열기 텍스트 제거');
if(!index.includes(\"const BUILD='V9.0.18';\")) throw new Error('V9.0.18 BUILD 불일치');"""
q=q.replace(old,new,1)
v.write_text(q,encoding='utf-8')

vm=root/'verify-meaning.js'; q=vm.read_text(encoding='utf-8')
q=q.replace('V9.0.17 의미 돌아보기·기록 다시보기·의미회복 간편점검 UX 회귀검증 통과','V9.0.18 의미 돌아보기·기록 다시보기·의미회복 간편점검 UX 회귀검증 통과')
vm.write_text(q,encoding='utf-8')
