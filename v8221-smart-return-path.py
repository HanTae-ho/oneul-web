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

# Only change the back button inside the urge-diary page; other recovery-tool back buttons stay untouched.
sec_start=s.find('<section class="pg" id="p-urge-diary">')
if sec_start<0:
    raise SystemExit('urge diary section not found')
sec_end=s.find('</section>',sec_start)
if sec_end<0:
    raise SystemExit('urge diary section end not found')
segment=s[sec_start:sec_end]
old_btn='<button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack(\'tools\')">← 회복도구</button>'
new_btn='<button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back data-back-default="tools" data-back-label="회복도구" onclick="appBack(\'tools\')">← 회복도구</button>'
if segment.count(old_btn)!=1:
    raise SystemExit(f'urge diary scoped back button: expected 1 match, found {segment.count(old_btn)}')
segment=segment.replace(old_btn,new_btn,1)
s=s[:sec_start]+segment+s[sec_end:]

once("    'smart-tools':'SMART 실천도구',", "    'tools':'회복도구',\n    'smart-tools':'SMART 실천도구',", 'route back tools label')
once("  b.textContent='← '+(labels[from]||'SMART 실천도구');\n  b.onclick=()=>appBack(fallbacks[from]||'smart-tools');", "  const defaultLabel=b.dataset.backLabel||'SMART 실천도구';\n  const defaultBack=b.dataset.backDefault||'smart-tools';\n  b.textContent='← '+(labels[from]||defaultLabel);\n  b.onclick=()=>appBack(fallbacks[from]||defaultBack);", 'route back default')
once("let learnState = { topic:'' };", "let learnState = { topic:'', returnSection:'' };", 'learn state return section')
once("function learningAction(type){\n  closeModal();", "function learningAction(type,sectionId){\n  if(sectionId && learnState.topic==='smart-recovery') learnState.returnSection=String(sectionId);\n  closeModal();", 'learning action return section')
once("data-learn-act=\"'+esc(a.type)+'\">", "data-learn-act=\"'+esc(a.type)+'\" data-learn-section=\"'+esc(s.id||'')+'\">", 'learning action button section')
once("  $$('#modin [data-learn-act]').forEach(b=>{ b.onclick=()=>learningAction(b.dataset.learnAct); });", "  $$('#modin [data-learn-act]').forEach(b=>{ b.onclick=()=>learningAction(b.dataset.learnAct,b.dataset.learnSection); });", 'learning action handler')
once("  if(p === 'learn-topic') drawLearnTopic();", "  if(p === 'learn-topic') drawLearnTopic(!!opt.fromHistory);", 'history-aware learn draw')
once("function drawLearnTopic(){", "function drawLearnTopic(fromHistory){", 'draw learn signature')
once("  if(!(topic.sections || []).length) box.innerHTML='<div class=\"note\">학습 내용을 준비 중입니다.</div>';\n  refreshIcons();\n}", "  if(!(topic.sections || []).length) box.innerHTML='<div class=\"note\">학습 내용을 준비 중입니다.</div>';\n  refreshIcons();\n  const returnId=fromHistory?String(learnState.returnSection||''):'';\n  if(returnId){\n    const target=(topic.sections||[]).find(x=>x&&x.id===returnId);\n    learnState.returnSection='';\n    if(target) setTimeout(()=>openLearnSection(topic,target),0);\n  }\n}", 'restore exact learning section')

# Keep visible V8.2.21; bump only cache revision so this fix reaches clients already on V8.2.21.
if "const APP_VERSION = 'V8.2.21';" not in w:
    raise SystemExit('unexpected APP_VERSION')
old_cache="const V = 'ohg-v8221-user-wording-cleanup';"
if w.count(old_cache)!=1:
    raise SystemExit(f'unexpected cache key count: {w.count(old_cache)}')
w=w.replace(old_cache,"const V = 'ohg-v8221-smart-return-path';",1)

idx.write_text(s,encoding='utf-8')
sw.write_text(w,encoding='utf-8')
