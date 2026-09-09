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

old_gs="""ok(/MAKE_NEW_FEEDBACK_SHEET/.test(feedbackGs)&&/FEEDBACK_ADMIN_KEY/.test(feedbackGs),'의견 Apps Script 유지');
ok(/GS_VER\\s*=\\s*'v1\\.8'/.test(resourceGs)&&/FEEDBACK_URL/.test(resourceGs),'자원시트 v1.8 유지');"""
new_gs="""if(feedbackGs) ok(/MAKE_NEW_FEEDBACK_SHEET/.test(feedbackGs)&&/FEEDBACK_ADMIN_KEY/.test(feedbackGs),'의견 Apps Script 유지');
else console.log('SKIP - 의견 Apps Script 파일은 저장소 외부 배포 자원');
if(resourceGs) ok(/GS_VER\\s*=\\s*'v1\\.8'/.test(resourceGs)&&/FEEDBACK_URL/.test(resourceGs),'자원시트 v1.8 유지');
else console.log('SKIP - 자원시트 Apps Script 파일은 저장소 외부 배포 자원');"""
if old_gs not in s:
    raise SystemExit('verify.js Apps Script assertion block not found')
s=s.replace(old_gs,new_gs,1)

p.write_text(s,encoding='utf-8')

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
assert "V8\\.0" not in '\n'.join(vr.splitlines()[:30])
print('V9.0.2 verify consistency repair PASS')
