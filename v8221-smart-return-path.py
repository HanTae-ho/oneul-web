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

once('<button class="tiny" style="color:var(--acc);font-weight:600" onclick="appBack(\'tools\')">← 회복도구</button>', '<button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back data-back-default="tools" data-back-label="회복도구" onclick="appBack(\'tools\')">← 회복도구</button>', 'urge diary back button')
once("    'smart-tools':'SMART 실천도구',", "    'tools':'회복도구',\n    'smart-tools':'SMART 실천도구',", 'route back tools label')
once("  b.textContent='← '+(labels[from]||'SMART 실천도구');\n  b.onclick=()=>appBack(fallbacks[from]||'smart-tools');", "  const defaultLabel=b.dataset.backLabel||'SMART 실천도구';\n  const defaultBack=b.dataset.backDefault||'smart-tools';\n  b.textContent='← '+(labels[from]||defaultLabel);\n  b.onclick=()=>appBack(fallbacks[from]||defaultBack);", 'route back default')
once("let learnState = { topic:'' };", "let learnState = { topic:'', returnSection:'' };", 'learn state return section')
once("function learningAction(type){\n  closeModal();", "function learningAction(type,sectionId){\n  if(sectionId && learnState.topic==='smart-recovery') learnState.returnSection=String(sectionId);\n  closeModal();", 'learning action return section')
once("h+='<div class=\"learn-actions\">'+v.actions.map((a,i)=>'<button class=\"btn '+(i?'ghost':'sec')+'\" data-learn-act=\"'+esc(a.type)+'\">'+esc(a.label)+'</button>').join('')+'</div>';", "h+='<div class=\"learn-actions\">'+v.actions.map((a,i)=>'<button class=\"btn '+(i?'ghost':'sec')+'\" data-learn-act=\"'+esc(a.type)+'\" data-learn-section=\"'+esc(s.id||'')+'\">'+esc(a.label)+'</button>').join('')+'</div>';", 'learning action button section')
once("  $$('#modin [data-learn-act]').forEach(b=>{ b.onclick=()=>learningAction(b.dataset.learnAct); });", "  $$('#modin [data-learn-act]').forEach(b=>{ b.onclick=()=>learningAction(b.dataset.learnAct,b.dataset.learnSection); });", 'learning action handler')
once("  if(p === 'learn-topic') drawLearnTopic();", "  if(p === 'learn-topic') drawLearnTopic(!!opt.fromHistory);", 'history-aware learn draw')
once("function drawLearnTopic(){", "function drawLearnTopic(fromHistory){", 'draw learn signature')
once("  if(!(topic.sections || []).length) box.innerHTML='<div class=\"note\">학습 내용을 준비 중입니다.</div>';\n  refreshIcons();\n}", "  if(!(topic.sections || []).length) box.innerHTML='<div class=\"note\">학습 내용을 준비 중입니다.</div>';\n  refreshIcons();\n  const returnId=fromHistory?String(learnState.returnSection||''):'';\n  if(returnId){\n    const target=(topic.sections||[]).find(x=>x&&x.id===returnId);\n    learnState.returnSection='';\n    if(target) setTimeout(()=>openLearnSection(topic,target),0);\n  }\n}", 'restore exact learning section')

# Preserve visible app version; change cache revision so the return-path fix reaches existing V8.2.21 clients.
if "const APP_VERSION = 'V8.2.21';" not in w:
    raise SystemExit('unexpected APP_VERSION')
w=w.replace("const V = 'ohg-v8221-user-wording-cleanup';","const V = 'ohg-v8221-smart-return-path';",1)
if "ohg-v8221-smart-return-path" not in w:
    raise SystemExit('cache revision update failed')

idx.write_text(s,encoding='utf-8')
sw.write_text(w,encoding='utf-8')
