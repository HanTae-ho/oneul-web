const fs = require('fs');
const path = require('path');
const vm = require('vm');
const root=__dirname;
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const index=read('index.html'), sw=read('sw.js'), test=read('test.js'), manifest=read('manifest.json');
const qaSrc=read('qa-data.js'), learningSrc=read('learning-data.js'), screeningSrc=read('screening-data.js'), workbookSrc=read('workbook-data.js');
const feedbackGs=read('오늘한걸음_의견_v1.0.gs'), resourceGs=read('오늘한걸음_자원시트_v1.8.gs');
const fail=m=>{throw new Error('VERIFY: '+m)}; const ok=(c,m)=>{if(!c)fail(m);console.log('OK - '+m)};

ok(/const BUILD = 'V7\.14';/.test(index),'index BUILD = V7.14');
ok(/const APP_VERSION = 'V7\.14';/.test(sw),'sw APP_VERSION = V7.14');
ok(/const V = 'ohg-v714';/.test(sw),'sw cache = ohg-v714');
['qa-data.js','learning-data.js','screening-data.js','workbook-data.js'].forEach(f=>{
  ok(sw.includes("'./"+f+"'"),'서비스워커가 '+f+' 오프라인 캐시');
  ok(index.includes('<script src="./'+f+'"></script>'),'index가 '+f+' 로드');
});
ok(/function recoveryDay\(from, to\)/.test(index) && /daysBetween\(from, to\) \+ 1/.test(index),'회복 시작 당일 1일째 규칙 유지');
ok(/도박문제 헬프라인', t:'1336', d:'365일 09:00~22:00/.test(index) && /가족 상담도 받습니다 · 365일 09:00~22:00/.test(index),'1336 운영시간 최신 표기 365일 09:00~22:00');
ok(!/user-scalable=no/.test(index),'접근성: 사용자 화면 확대 차단 없음');
ok(/ks\.filter\(k => k\.startsWith\('ohg-'\)\)/.test(index),'앱 새로고침은 오늘 한 걸음 캐시만 삭제');
ok(/getRegistration\('\.\/'\)/.test(index) && !/getRegistrations\(\)/.test(index),'앱 새로고침은 현재 앱 서비스워커만 갱신');
ok(/k\.startsWith\('ohg-'\) && k !== V/.test(sw),'서비스워커 활성화 시 다른 앱 캐시를 삭제하지 않음');
ok(/registration\.showNotification|reg\.showNotification/.test(index),'Android/TWA 시스템 알림은 서비스워커 showNotification 우선');
ok(/function testNotify\(\)/.test(index)&&/시험 알림 보내기/.test(index),'시험 알림 기능 존재');
ok(/function notifyWanted\(\)/.test(index)&&/const wanted = notifyWanted\(\)/.test(index),'알림 사용자 설정과 실제 권한 상태를 분리 표시');
ok(/휴대폰 설정 → 앱 → 오늘 한 걸음 → 알림/.test(index),'TWA/Android 알림 차단 시 앱 알림 설정 안내');
ok(/self\.addEventListener\('notificationclick'/.test(sw),'서비스워커 알림 클릭 시 앱 복귀 처리');

ok(/id="tool-listen"/.test(index),'회복도구에 듣는 글 메뉴 존재');
ok(/\$\('#tool-listen'\)\.onclick = \(\) => openListen\('tools'\)/.test(index),'회복도구 듣는 글이 기존 듣는 글 화면으로 연결');
ok(/p === 'listen' && ls\.back === 'tools'/.test(index),'회복도구에서 듣는 글 진입 시 회복도구 탭 강조 유지');
ok(/마음 처방전.*회복도구/.test(index),'마음프로 듣는 글 안내가 두 진입경로를 반영');
ok(/id="p-workbook-list"/.test(index)&&/id="workbook-list"/.test(index),'회복학습 안에 단계별 점검 화면 존재');
ok(/<b>단계별 점검<\/b>/.test(index)&&/go\('workbook-list'\)/.test(index),'회복학습 목록에서 단계별 점검 직접 진입');
ok(/const order=\['step1','step4','step8','step9','step10','step11','step12'\]/.test(index),'단계별 점검 1·4·8·9·10·11·12단계 순서');
ok(!/if\(topic\.sourceNote\) h\+=/.test(index),'회복학습 사용자 화면에서 내부 sourceNote 미표시');
ok(/#modbox'\); if\(mb\) mb\.scrollTop=0/.test(index),'학습 모달을 새로 열 때 스크롤 맨 위 초기화');
ok(/id="learn-modal-prev"/.test(index)&&/id="learn-modal-next"/.test(index),'회복학습 글 이전·다음 탐색 존재');
ok(/btn help-alert sm/.test(index)&&/\.btn\.help-alert\{[^}]*var\(--badbg\)[^}]*var\(--bad\)/.test(index),'긴급 Q&A 헬프 버튼 붉은 계열 강조');
ok(/history\.pushState/.test(index)&&/history\.replaceState/.test(index)&&/addEventListener\('popstate'/.test(index),'Android 시스템 뒤로가기용 History API 연결');
ok(/function appBack\(fallback\)/.test(index),'앱 내부 뒤로가기 헬퍼 존재');
ok(!/\.toISOString\s*\(/.test(test),'자동테스트에서 toISOString() 미사용 유지');
ok(/timezoneId: 'Asia\/Seoul'/.test(test),'기존 브라우저 회귀테스트 시간대 Asia/Seoul 유지');
ok(!/\/opt\/pw-browsers\/chromium/.test(test),'자동테스트 Chromium 경로 하드코딩 제거');
ok(/process\.env\.CHROMIUM_PATH/.test(test),'필요 시 CHROMIUM_PATH 사용자 지정 지원');
ok(/회복학습 목록에는 12단계·회복의 기초 이해·단계별 점검 3개/.test(test),'test.js 회복학습 3메뉴 기준으로 갱신');
ok(/알코올 영역 1단계 카드에 AA 단계문장 표시/.test(test)&&/도박 영역 1단계 카드에 GA 단계문장 표시/.test(test)&&/약물 영역 1단계 카드에 NA 단계문장 표시/.test(test),'test.js AA·GA·NA 영역별 단계문장 회귀검사');

let box={window:{}};vm.createContext(box);vm.runInContext(qaSrc,box);const qa=box.window.QA_ITEMS;
ok(Array.isArray(qa)&&qa.length===224,'Q&A 224문답 유지');
ok(qa.every(x=>{const n=x.a.split(/\n\s*\n/).filter(Boolean).length;return n>=2&&n<=3;}),'Q&A 답변 2~3문단 유지');
ok(/\.qadetail \.answer\{[^}]*font-size:16px;[^}]*line-height:1\.85/.test(index),'Q&A 상세 16px / 1.85 유지');

box={window:{}};vm.createContext(box);vm.runInContext(learningSrc,box);const learning=box.window.LEARNING_TOPICS; const stepWords=box.window.TWELVE_STEP_WORDINGS; const famLearn=box.window.FAMILY_TWELVE_STEP_PERSPECTIVES;
ok(stepWords&&stepWords.version==='V7.10'&&stepWords.sets,'AA·GA·NA 영역별 단계문장 데이터 유지');
ok(famLearn&&Object.keys(famLearn).length===14,'가족 12단계 소개·기초·1~12단계 오버레이 14개 등록');
ok(['step-1','step-4','step-8','step-9','step-10','step-11','step-12'].every(k=>famLearn[k]&&Array.isArray(famLearn[k].reflection)&&famLearn[k].reflection.length>=4),'가족 핵심단계 성찰질문 4문항 이상');
ok(famLearn.intro&&famLearn.intro.body.join(' ').includes('상대의 회복을 위해 바라는 것')===false&&famLearn.intro.body.join(' ').includes('가족이 자신의 삶·관계·경계·안전을 다시 돌아보는 회복의 지도'),'가족용 12단계 소개가 상대 변화가 아닌 가족 자신의 회복에 초점');
ok(famLearn.foundation&&famLearn.foundation.body.join(' ').includes('무조건 참는 것이 아닙니다')&&famLearn.foundation.body.join(' ').includes('반드시 화해·재결합·직접 접촉'),'가족용 12단계 기초에서 겸손·용서와 자기희생·화해를 구분');
ok(!learningSrc.includes('중독행동의 선택과 중단은 결국 그 사람의 몫')&&learningSrc.includes('치료와 회복을 선택하고 실천하는 책임까지 가족이 대신 맡을 수는 없습니다'),'중독 자체를 단순한 선택으로 오해하지 않도록 가족 1단계 문구 정제');
ok(famLearn['step-1'].body.join(' ').includes('대신 멈추게 할 수 없었다')&&famLearn['step-4'].body.join(' ').includes('가족의 탓')&&famLearn['step-9'].body.join(' ').includes('통제의 수단'),'가족 1·4·9단계 핵심 안전 관점 반영');
ok(['alcohol','gambling','drug','addiction'].every(k=>stepWords.sets[k]&&stepWords.sets[k].steps.length===12),'AA·GA·NA·중독 통합형 각각 12개 단계문장');
ok(stepWords.sets.gambling.official===true&&stepWords.sets.gambling.verified===true,'GA 공식 문안 독립 세트 등록');
ok(stepWords.sets.gambling.steps[0]==='우리는 도박에 무력하며 - 정상적으로 생활할 수 없게 되었음을 시인했습니다.','GA 1단계 비교표 문안 정확히 등록');
ok(stepWords.sets.gambling.steps[3].includes('도덕적, 재정적 목록'),'GA 4단계 재정적 목록 핵심 표현 유지');
ok(stepWords.sets.gambling.steps[11].includes('다른 도박중독자들에게 이 메시지를 전하려고 노력했습니다.'),'GA 12단계 도박 영역어 유지');
ok(['alcohol','gambling','drug'].every(k=>stepWords.sets[k].official===true&&stepWords.sets[k].verified===true),'AA·GA·NA 공식/검증 세트 표시');
ok(stepWords.sets.alcohol.steps[0]==='우리는 알코올에 무력했으며, 우리의 삶을 수습할 수 없게 되었다는 것을 시인했다.','AA 1단계 문안 정확히 등록');
ok(stepWords.sets.alcohol.steps[1]==='우리보다 위대하신 힘이 우리를 본정신으로 돌아오게 해 주실 수 있다는 것을 믿게 되었다.','AA 2단계 비교표 문안 등록');
ok(stepWords.sets.alcohol.steps[11].includes('알코올중독자들에게 이 메시지를 전하려고 노력했으며'),'AA 12단계 영역어 유지');
ok(stepWords.sets.drug.steps[0]==='우리는 중독에 무력했으며, 우리의 삶을 스스로 수습할 수 없게 되었다는 것을 시인했다.','NA 1단계 문안 정확히 등록');
ok(stepWords.sets.drug.steps[11].includes('약물 중독자들에게 이 메시지를 전하려고 노력했으며'),'NA 12단계 비교표 영역어 유지');
ok(stepWords.sets.addiction.adapted===true&&stepWords.sets.addiction.official===false&&stepWords.sets.addiction.label==='통합형(중독)'&&stepWords.sets.addiction.steps[0].includes('중독에 무력했으며')&&stepWords.sets.addiction.steps[11].includes('중독자들에게'),'복수/기타 영역 중독 통합형을 공식 문안과 명확히 구분');
ok(/function twelveStepDomain\(\)/.test(index)&&/function twelveStepSentence\(section\)/.test(index)&&/function learningCardText\(topic, section, ready\)/.test(index),'영역별 단계문장 선택 함수 존재');
ok(/if\(types\[0\]==='alcohol'\) return 'alcohol'/.test(index)&&/if\(types\[0\]==='drug'\) return 'drug'/.test(index),'알코올·약물 단일영역 분기');
ok(/types\[0\]==='gambling'.*sets\.gambling/.test(index),'도박 단일영역 GA 세트 분기');
ok(!/function twelveStepDomain\(\)[\s\S]{0,500}S\.role/.test(index),'단계문장 선택은 self/family 역할과 독립');
ok(/FAMILY_TWELVE_STEP_PERSPECTIVES/.test(index)&&/function learningSectionPerspective\(section\)/.test(index),'가족 12단계 해설 오버레이 연결');
ok(/learningCardText\(topic,s,ready\)/.test(index),'12단계 카드 작은글씨가 동적 단계문장 함수 사용');
ok(/function twelveStepWordingNotice\(\)/.test(index)&&/set\.adapted/.test(index),'복수영역 통합형 안내를 공식 문안과 구분해 표시');
ok(Array.isArray(learning)&&learning.length===2&&learning[0].id==='twelve-steps'&&learning[1].id==='recovery-foundations','회복학습 2개 독립 주제 등록');
ok(learning[0].sections.length===14,'12단계 소개 + 기초 + 1~12단계 14개');
ok(learning[0].status==='content-ready','12단계 학습 콘텐츠 준비 완료 상태');
ok(learning[0].sections.every(x=>Array.isArray(x.body)&&x.body.length>=3),'12단계 14개 섹션 모두 본문 3문단 이상');
ok(learning[0].sections.every(x=>Array.isArray(x.reflection)&&x.reflection.length>=4),'12단계 14개 섹션 모두 생각해보기 4문항 이상');
ok(learning[0].sections.some(x=>x.id==='foundation'),'12단계의 기초(믿음·겸손·용서) 추가');
ok(/function openLearnSection\(topic,s\)/.test(index)&&/function learningAction\(type\)/.test(index),'회복학습 모바일 상세/행동연결 UI 존재');
ok(/type:'halt'/.test(learningSrc)&&/type:'night'/.test(learningSrc),'10단계 HALT·하루 돌아보기 연결');
ok(/type:'meditation'/.test(learningSrc)&&/type:'breath'/.test(learningSrc),'11단계 명상·호흡 연결');
ok(/type:'meet'/.test(learningSrc)&&/type:'help'/.test(learningSrc),'12단계 자조모임·헬프 연결');
const deep=learning.find(x=>x.id==='recovery-foundations');
ok(deep&&deep.status==='content-ready'&&deep.sections.length===4,'회복의 기초 심화학습 4개 섹션');
ok(deep.sections.map(x=>x.id).join(',')==='whole-person,need-greed,fear,meaning-transcendence','심화학습 순서: 영·마음·몸 / 욕구와 탐욕 / 두려움 / 의미와 자기초월');
ok(deep.sections.every(x=>Array.isArray(x.body)&&x.body.length>=4&&Array.isArray(x.reflection)&&x.reflection.length>=4&&x.practice),'심화학습 4개 모두 본문·성찰·오늘 해보기 구성');
ok(/철학적·영적 해석 틀이며/.test(learningSrc)&&/의학적 진단/.test(learningSrc),'심화학습 해석 관점과 의학적 진단 구분');
ok(/type:'rec-mood'/.test(learningSrc)&&/type:'halt'/.test(learningSrc)&&/type:'meditation'/.test(learningSrc),'심화학습 감정기록·HALT·명상 연결');

box={window:{}};vm.createContext(box);vm.runInContext(workbookSrc,box);const wb=box.window.STEP_WORKSHEETS; const fwb=box.window.FAMILY_STEP_WORKSHEETS;
ok(wb&&['step1','step4','step8','step9','step10','step11','step12'].every(k=>wb[k]),'1·4·8·9·10·11·12단계 검토·실천 데이터 등록');
ok(Object.keys(wb).join(',')==='step1,step4,step8,step9,step10,step11,step12','검토·실천 workbook 7종만 등록');
ok(wb.step1.sections.map(x=>x.id).join(',')==='powerless,unmanageable,loss','1단계 검토: 무력함 / 수습할 수 없는 삶 / 상실과 애도');
ok(wb.step4.sections.map(x=>x.id).join(',')==='resentment,fear,harm,strength,desire,emotion,meaning','4단계 검토: 핵심 4개 + 욕망·감정·공허/의미 심화');
ok(wb.step4.sections.find(x=>x.id==='desire').fixedLabels.length===4,'4단계 네 가지 욕망 고정 항목');
ok(wb.step8.sections.map(x=>x.id).join(',')==='amendsList,selfHarm,forgive','8단계: 보상 명단 / 자기 보상 / 용서 방해요인');
ok(wb.step9.sections.map(x=>x.id).join(',')==='plan,words,selfAmends','9단계: 직접 보상 계획 / 태도 / 자기 보상');
ok(wb.step10.sections.map(x=>x.id).join(',')==='inventory,admit,tomorrow','10단계: 오늘 검토 / 즉시 시인 / 내일 한 걸음');
ok(wb.step11.sections.map(x=>x.id).join(',')==='connect,prayer,practice','11단계: 연결 / 기도·의도 / 행동 실천');
ok(wb.step12.sections.map(x=>x.id).join(',')==='principle,message,share','12단계: 원칙 / 삶의 메시지 / 나눔');
ok(/특정 종교를 전제로 하지 않습니다/.test(workbookSrc),'11단계 비종교 사용자 안전 문구');
ok(/다른 사람을 치료하거나 책임지라는 뜻이 아닙니다/.test(workbookSrc),'12단계 과도한 도움 역할 방지 문구');
ok(fwb&&['step1','step4','step8','step9','step10','step11','step12'].every(k=>fwb[k]),'가족 1·4·8·9·10·11·12단계 점검 7종 등록');
ok(Object.keys(fwb).join(',')==='step1,step4,step8,step9,step10,step11,step12','가족 workbook 7종만 등록');
ok(fwb.step1.sections.map(x=>x.id).join(',')==='control,rescue,life','가족 1단계: 통제 / 대신 수습 / 내 삶 회복');
ok(fwb.step4.sections.map(x=>x.id).join(',')==='resentment,fear,overresponsibility,strength','가족 4단계: 원한 / 두려움 / 과잉책임 / 강점');
ok(fwb.step8.sections.map(x=>x.id).join(',')==='people,self,notmine','가족 8단계: 보상대상 / 자기보상 / 책임 구분');
ok(fwb.step9.sections.map(x=>x.id).join(',')==='plan,attitude,self','가족 9단계: 보상계획 / 태도 / 자기보상');
ok(fwb.step10.sections.map(x=>x.id).join(',')==='review,boundary','가족 10단계: 오늘 점검 / 경계·자기돌봄');
ok(fwb.step11.sections.map(x=>x.id).join(',')==='pause,direction','가족 11단계: 멈춤 / 오늘의 방향');
ok(fwb.step12.sections.map(x=>x.id).join(',')==='principle,share,life','가족 12단계: 원칙 / 나눔 / 나의 삶');
ok(fwb.step4.safety.includes('폭력·학대 등 위해 행동의 책임은 행위자에게')&&fwb.step4.safety.includes('중독이 생긴 원인을 가족의 탓으로 돌리지 않습니다'),'가족 4단계가 위해행동 책임과 중독 원인에 대한 가족 죄책감을 분리');
ok(!workbookSrc.includes('구원자 역할')&&fwb.step12.subtitle.includes('다른 사람의 문제를 대신 책임지는 역할'),'가족 12단계 나눔을 구원자 역할이 아닌 책임 경계 언어로 정제');
ok(/familyStepWorks: \[\], familyStepDrafts: \{\}/.test(index),'가족 12단계 기록·초안 별도 로컬 저장소');
ok(/function workbookDefs\(scope\)/.test(index)&&/FAMILY_WORKSHEETS/.test(index),'역할별 workbook 정의 선택 엔진');
ok(/workbookState = \{kind:'step1', from:'learn-topic', scope:'self'\}/.test(index),'workbook 역할 scope 상태 분리');
ok(/mt\.target=famMode\(\)\?'fam':'me'/.test(index),'가족 12단계 모임 action이 가족모임으로 분기');
ok(/\{v:'work',l:'12단계 점검'\}/.test(index),'가족 내 발자취 12단계 점검 탭');

ok(/stepWorks: \[\], stepDrafts: \{\}/.test(index),'당사자 검토 저장기록·자동저장 초안 localStorage 상태 유지');
ok(/function drawWorkbook\(\)/.test(index)&&/function saveWorkbookRecord\(kind\)/.test(index),'검토시트 작성·저장 UI 존재');
ok(/function recWorkbook\(\)/.test(index)&&/12단계 검토/.test(index),'내 발자취 12단계 검토 재조회 탭 존재');
ok(/자원시트·의견서버·마음프로로 자동 전송되지 않습니다/.test(index),'검토 내용 서버·AI 자동전송 방지 안내');
ok(['step1','step4','step8','step9','step10','step11','step12'].every(k=>new RegExp("type:'"+k+"-workbook'").test(learningSrc)),'1·4·8·9·10·11·12단계 학습에서 검토·실천 직접 연결');
ok(/workbookDraftStore\(scope\)\[kind\]=workbookEmptyData/.test(index)&&/workbookQueueSave/.test(index),'역할별 검토 작성 중 기기내 초안 자동저장');
ok(/wb-record-delete/.test(index),'저장한 개별 검토 기록 삭제 기능');

box={window:{}};vm.createContext(box);vm.runInContext(screeningSrc,box);const sc=box.window.SCREENING_TOOLS;
ok(Array.isArray(sc)&&sc.length===9,'자가점검 9개 도구 등록');
const qcount=Object.fromEntries(sc.map(x=>[x.id,x.questions.length]));
const expected={'audit-k':10,'pgsi':9,'dast-k10':10,'nds-bv':3,'nas-bv':3,'nss-bv':3,'internet-habit':28,'game-habit':30,'smartphone-habit':28};
ok(Object.entries(expected).every(([k,n])=>qcount[k]===n),'자가점검 도구별 문항 수 일치');
ok(sc.reduce((a,x)=>a+x.questions.length,0)===124,'자가점검 총 문항 데이터 124개');
const audit=sc.find(x=>x.id==='audit-k');
ok(audit.sexCutoff && audit.levelsMale[0].max===9 && audit.levelsFemale[0].max===5,'AUDIT-K 남/여 결과기준 분리');
const pgsi=sc.find(x=>x.id==='pgsi');
ok(pgsi.levels.map(x=>x.max).join(',')==='0,2,7,27','PGSI 0 / 1~2 / 3~7 / 8~27 구간');
const dast=sc.find(x=>x.id==='dast-k10');
ok(dast.levels.map(x=>x.max).join(',')==='0,2,5,8,10','DAST-Korean 0 / 1~2 / 3~5 / 6~8 / 9~10 구간');
ok(dast.options.length===2 && dast.options[0].l==='예' && dast.options[0].v===1 && dast.options[1].l==='아니오' && dast.options[1].v===0,'DAST-Korean 예=1 / 아니오=0 채점 방향');
const dastExact=[
  '의료상 필요한 경우 이외에 약물을 사용했습니까?',
  '한번에 두 가지 이상의 약물을 남용합니까?',
  '중단하기를 원할 때 약물 사용을 중단할 수 없습니까?',
  '약물 사용으로 인해 일시적 기억상실 또는 환각을 경험한 적이 있습니까?',
  '약물 사용에 대하여 나쁘다고 생각하거나 죄책감을 느낍니까?',
  '귀하의 약물 사용에 대해 배우자(또는 부모)가 불평한 적이 있습니까?',
  '약물 사용을 이유로 가족을 소홀히 한 적이 있습니까?',
  '약물을 입수하기 위해 불법적인 활동에 관여한 적이 있습니까?',
  '약물 복용을 중단했을 때 금단증상을 경험한 적이 있습니까?',
  '약물 사용으로 인해 의학적 문제(예: 기억상실, 간염, 경련, 출혈)를 겪은 적이 있습니까?'
];
ok(dast.questions.map(x=>x.q).join('\n')===dastExact.join('\n'),'DAST-Korean 10문항 2020 표준지침과 1:1 일치');
ok(['nds-bv','nas-bv','nss-bv'].every(id=>{const x=sc.find(y=>y.id===id);return x.min===0&&x.max===9&&x.levels[0].max===2;}),'우울·불안·스트레스 단축형 3문항·3점 절단 기준');
ok(sc.find(x=>x.id==='internet-habit').levels[0].max===40,'인터넷 고위험 기준: 정수점수 41점 이상');
ok(sc.find(x=>x.id==='game-habit').levels[0].max===38,'게임 고위험 기준: 정수점수 39점 이상');
ok(sc.find(x=>x.id==='smartphone-habit').levels[0].max===48,'스마트폰 고위험 기준: 49점 이상');

ok(/id="p-screening"/.test(index)&&/id="p-screen-test"/.test(index),'자가점검 목록/검사 화면 존재');
ok(/function drawScreening\(\)/.test(index)&&/function drawScreenTest\(\)/.test(index),'자가점검 실행 UI 함수 존재');
ok(/screenings: \[\]/.test(index)&&/답변 하나하나는 저장하지 않고/.test(index),'자가점검 결과 로컬 저장 + 문항응답 미저장');
ok(/function screeningStats\(\)/.test(index)&&/trendSvg\(tool,h\)/.test(index),'통계 점수 변화 + 꺾은선 그래프 존재');
ok(/function screenRetestText\(last\)/.test(index)&&/약 4주 후 다시 점검해볼 수 있습니다/.test(index),'최근 검사일·경과관찰 재점검 안내 존재');
ok(/id="screen-log-go"/.test(index)&&/id="screen-help-go"/.test(index)&&/id="screen-ai-go"/.test(index),'검사결과에서 기록·도움·마음프로 행동 연결');
ok(/검사 점수와 결과는 마음프로에 자동으로 전달되지 않습니다/.test(index),'마음프로 자동전송 방지 안내');
ok(/function screenRecentRows\(rows\)/.test(index)&&/screen-record-row/.test(index),'통계 최근 검사일·점수·결과구간 목록 존재');
ok(/이전보다/.test(index)&&/점수의 증가·감소/.test(index),'이전 점수 차이와 과잉해석 방지 문구 존재');
ok(/types\.includes\('etc'\)/.test(index),'기타 회복영역에서 인터넷·게임·스마트폰 점검 노출');
ok(/가족·보호자 모드에서는 당사자 대신/.test(index),'가족 모드에서 중독검사 대리응답 방지');
ok(/#top-me\{[^}]*width:40px;[^}]*border-radius:50%/.test(index),'사용자 아이콘 원형 40px 아바타 기반');
ok(/#top-me img\{[^}]*object-fit:cover/.test(index),'향후 프로필 이미지 삽입 가능한 아바타 CSS');

ok(/navigator\.share/.test(index),'추천하기 Web Share 유지');
ok(/id="me-feedback-text"/.test(index)&&/id="me-feedback-send"/.test(index),'앱에 바라는 점 유지');
ok(/MAKE_NEW_FEEDBACK_SHEET/.test(feedbackGs)&&/FEEDBACK_ADMIN_KEY/.test(feedbackGs),'의견 Apps Script 유지');
ok(/GS_VER\s*=\s*'v1\.8'/.test(resourceGs)&&/FEEDBACK_URL/.test(resourceGs),'자원시트 v1.8 유지');


ok(/const isSamsung = \/SamsungBrowser\/i.test\(navigator.userAgent\)/.test(index),'Samsung Internet 감지');
ok(index.includes('삼성 인터넷 권장 방법'),'Samsung Internet 전용 설치 안내');
ok(index.includes('앱스 화면에 설치'),'Samsung Internet 앱스 화면 설치 안내');
ok(index.indexOf('if(isSamsung){') < index.indexOf('} else if(isIOS){'),'Samsung 설치 분기를 표준 prompt보다 우선');
ok(manifest.includes('\"id\": \"./index.html\"'),'manifest 안정적 app id');

console.log('\nV7.14 알림 안정화 검증 통과');
