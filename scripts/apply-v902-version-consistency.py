from pathlib import Path

p=Path('verify.js')
s=p.read_text(encoding='utf-8')

old_reads="""const feedbackGs=read('오늘한걸음_의견_v1.0.gs'), resourceGs=read('오늘한걸음_자원시트_v1.8.gs');"""
new_reads="""const readIf=f=>fs.existsSync(path.join(root,f))?read(f):'';
const feedbackGs=readIf('오늘한걸음_의견_v1.0.gs'), resourceGs=readIf('오늘한걸음_자원시트_v1.8.gs');"""
if old_reads not in s:
    raise SystemExit('verify.js Apps Script read block not found')
s=s.replace(old_reads,new_reads,1)

old_versions="""ok(/const BUILD = 'V8\\.0';/.test(index),'index BUILD = V8.0');
ok(/const APP_VERSION = 'V8\\.0';/.test(sw),'sw APP_VERSION = V8.0');
ok(/const V = 'ohg-v800';/.test(sw),'sw cache = ohg-v800');"""
new_versions="""const build=(index.match(/const BUILD\\s*=\\s*'([^']+)'/)||[])[1]||'';
const appVersion=(sw.match(/const APP_VERSION\\s*=\\s*'([^']+)'/)||[])[1]||'';
const cacheVersion=(sw.match(/const V\\s*=\\s*'([^']+)'/)||[])[1]||'';
const expectedCachePrefix='ohg-v'+build.replace(/^V/,'').replace(/\\./g,'');
ok(/^V\\d+\\.\\d+(?:\\.\\d+)?$/.test(build),'index BUILD 형식 정상: '+build);
ok(appVersion===build,'sw APP_VERSION = index BUILD ('+build+')');
ok(!!build && cacheVersion.startsWith(expectedCachePrefix),'sw cache = '+expectedCachePrefix+' 계열');"""
if old_versions not in s:
    raise SystemExit('verify.js legacy V8.0 version block not found')
s=s.replace(old_versions,new_versions,1)

old_workbook="""ok(/<b>단계별 점검<\\/b>/.test(index)&&/go\\('workbook-list'\\)/.test(index),'회복학습 목록에서 단계별 점검 직접 진입');"""
new_workbook="""ok(/<b>12단계 점검<\\/b>/.test(index)&&/w\\.onclick=\\(\\)=>go\\('workbook-list'\\)/.test(index),'회복학습 목록에서 12단계 점검 직접 진입');"""
if old_workbook not in s:
    raise SystemExit('verify.js stale workbook assertion not found')
s=s.replace(old_workbook,new_workbook,1)

old_learning="""ok(Array.isArray(learning)&&learning.length===2&&learning[0].id==='twelve-steps'&&learning[1].id==='recovery-foundations','회복학습 2개 독립 주제 등록');"""
new_learning="""ok(Array.isArray(learning)&&learning.length===3&&learning.map(x=>x.id).join(',')==='twelve-steps,recovery-foundations,smart-recovery','회복학습 3개 독립 주제 등록');"""
if old_learning not in s:
    raise SystemExit('verify.js stale learning-topic assertion not found')
s=s.replace(old_learning,new_learning,1)

old_action="""ok(/function openLearnSection\\(topic,s\\)/.test(index)&&/function learningAction\\(type\\)/.test(index),'회복학습 모바일 상세/행동연결 UI 존재');"""
new_action="""ok(/function openLearnSection\\(topic,s\\)/.test(index)&&/function learningAction\\(type,sectionId\\)/.test(index),'회복학습 모바일 상세/행동연결 UI 존재');"""
if old_action not in s:
    raise SystemExit('verify.js stale learningAction assertion not found')
s=s.replace(old_action,new_action,1)

old_family_tab="""ok(/\\{v:'work',l:'12단계 점검'\\}/.test(index),'가족 내 발자취 12단계 점검 탭');"""
new_family_tab="""ok(/\\{v:'work',l:'실천기록'\\}/.test(index),'가족 내 발자취 실천기록 탭');"""
if old_family_tab not in s:
    raise SystemExit('verify.js stale family work-tab assertion not found')
s=s.replace(old_family_tab,new_family_tab,1)

old_privacy="""ok(/자원시트·의견서버·마음프로로 자동 전송되지 않습니다/.test(index),'검토 내용 서버·AI 자동전송 방지 안내');"""
new_privacy="""ok(/작성 내용은 <b>이 기기에 저장<\\/b>되며 자동 전송되지 않습니다/.test(index)&&/작성 중 초안과 저장 기록 모두 S 안에만 두며 서버로 자동 전송하지 않습니다/.test(index),'검토 내용 서버·AI 자동전송 방지 안내');"""
if old_privacy not in s:
    raise SystemExit('verify.js stale workbook privacy assertion not found')
s=s.replace(old_privacy,new_privacy,1)

old_family_screen="""ok(/가족·보호자 모드에서는 당사자 대신/.test(index),'가족 모드에서 중독검사 대리응답 방지');"""
new_family_screen="""ok(/function drawScreening\\(\\)[\\s\\S]{0,600}if\\(!famMode\\(\\)\\)/.test(index),'가족 모드에서 중독검사 대리응답 방지');"""
if old_family_screen not in s:
    raise SystemExit('verify.js stale family screening assertion not found')
s=s.replace(old_family_screen,new_family_screen,1)

old_test_check="""ok(/회복학습 목록에는 12단계·회복의 기초 이해·단계별 점검 3개/.test(test),'test.js 회복학습 3메뉴 기준으로 갱신');"""
new_test_check="""ok(/회복학습 목록에는 12단계·회복의 기초 이해·SMART Recovery·12단계 점검 4개/.test(test),'test.js 회복학습 4메뉴 기준으로 갱신');"""
if old_test_check not in s:
    raise SystemExit('verify.js stale test.js learning-menu assertion not found')
s=s.replace(old_test_check,new_test_check,1)

old_gs="""ok(/MAKE_NEW_FEEDBACK_SHEET/.test(feedbackGs)&&/FEEDBACK_ADMIN_KEY/.test(feedbackGs),'의견 Apps Script 유지');
ok(/GS_VER\\s*=\\s*'v1\\.8'/.test(resourceGs)&&/FEEDBACK_URL/.test(resourceGs),'자원시트 v1.8 유지');"""
new_gs="""if(feedbackGs) ok(/MAKE_NEW_FEEDBACK_SHEET/.test(feedbackGs)&&/FEEDBACK_ADMIN_KEY/.test(feedbackGs),'의견 Apps Script 유지');
else console.log('SKIP - 의견 Apps Script 파일은 저장소 외부 배포 자원');
if(resourceGs) ok(/GS_VER\\s*=\\s*'v1\\.8'/.test(resourceGs)&&/FEEDBACK_URL/.test(resourceGs),'자원시트 v1.8 유지');
else console.log('SKIP - 자원시트 Apps Script 파일은 저장소 외부 배포 자원');"""
if old_gs not in s:
    raise SystemExit('verify.js Apps Script assertion block not found')
s=s.replace(old_gs,new_gs,1)

s=s.replace("console.log('\\nV8.0 네이티브 예약알림 웹 회귀검증 통과');", "console.log('\\n'+build+' 웹 회귀검증 통과');", 1)

p.write_text(s,encoding='utf-8')

p=Path('test.js')
t=p.read_text(encoding='utf-8')
old="""  assert(await pg.evaluate(() => Array.isArray(window.LEARNING_TOPICS) && window.LEARNING_TOPICS.length === 2), '회복학습은 2개 독립 주제를 learning-data.js에서 로드해야 함');
  await pg.click('#tool-learn'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-learn', '회복학습 목록 페이지가 열려야 함');
  assert((await pg.$$eval('#learn-list .help', a => a.length)) === 3, '회복학습 목록에는 12단계·회복의 기초 이해·단계별 점검 3개가 있어야 함');
  assert((await pg.$eval('#learn-list', e => e.innerText)).includes('12단계'), '회복학습 목록에 12단계가 표시되어야 함');
  assert((await pg.$eval('#learn-list', e => e.innerText)).includes('회복의 기초 이해'), '회복학습 목록에 심화 주제가 표시되어야 함');
  assert((await pg.$eval('#learn-list', e => e.innerText)).includes('단계별 점검'), '회복학습 목록에 단계별 점검이 표시되어야 함');"""
new="""  assert(await pg.evaluate(() => Array.isArray(window.LEARNING_TOPICS) && window.LEARNING_TOPICS.length === 3), '회복학습은 3개 독립 주제를 learning-data.js에서 로드해야 함');
  await pg.click('#tool-learn'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-learn', '회복학습 목록 페이지가 열려야 함');
  assert((await pg.$$eval('#learn-list .help', a => a.length)) === 4, '회복학습 목록에는 12단계·회복의 기초 이해·SMART Recovery·12단계 점검 4개가 있어야 함');
  const learnText = await pg.$eval('#learn-list', e => e.innerText);
  assert(learnText.includes('12단계'), '회복학습 목록에 12단계가 표시되어야 함');
  assert(learnText.includes('회복의 기초 이해'), '회복학습 목록에 심화 주제가 표시되어야 함');
  assert(learnText.includes('SMART Recovery'), '회복학습 목록에 SMART Recovery가 표시되어야 함');
  assert(learnText.includes('12단계 점검'), '회복학습 목록에 12단계 점검이 표시되어야 함');"""
if old not in t:
    raise SystemExit('test.js stale learning-menu block not found')
t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8')

idx=Path('index.html').read_text(encoding='utf-8')
sw=Path('sw.js').read_text(encoding='utf-8')
vr=Path('verify.js').read_text(encoding='utf-8')
assert "const BUILD='V9.0.2';" in idx or "const BUILD = 'V9.0.2';" in idx
assert "const APP_VERSION = 'V9.0.2';" in sw
assert "ohg-v902" in sw
assert "const build=(index.match" in vr
assert "readIf=f=>fs.existsSync" in vr
assert "<b>12단계 점검" in vr
assert "회복학습 3개 독립 주제 등록" in vr
assert "learningAction\\(type,sectionId" in vr
assert "실천기록" in vr
assert "작성 내용은 <b>이 기기에 저장" in vr
assert "function drawScreening" in vr
assert "SMART Recovery·12단계 점검 4개" in Path('test.js').read_text(encoding='utf-8')
assert "V8\\.0" not in '\n'.join(vr.splitlines()[:30])
print('V9.0.2 verify consistency repair PASS')
