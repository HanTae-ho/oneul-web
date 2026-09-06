from pathlib import Path

idx = Path('index.html')
s = idx.read_text(encoding='utf-8')

repls = []

def rep(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'MISSING: {label}')
    s = s.replace(old, new, 1)
    repls.append(label)

rep("const BUILD = 'V8.2.11';", "const BUILD = 'V8.2.12';", 'BUILD')

rep('''    <button class="btn ghost" onclick="go('urge-diary')">내 충동일기 열기</button>\n    <div id="smart-disarm-list" style="margin-top:12px"></div>''', '''    <button class="btn ghost" onclick="go('urge-diary')">내 충동일기 열기</button>\n    <div id="smart-disarm-capsule" style="margin-top:10px"></div>\n    <div id="smart-disarm-list" style="margin-top:12px"></div>''', 'DISARM capsule slot')

rep('''    <div id="capsule-manage">\n      <button class="btn sec" id="capsule-edit-btn">수정하기</button>''', '''    <div id="capsule-disarm-link" class="card" style="margin-top:12px">\n      <h3>이 초심을 충동 순간에 사용하기</h3>\n      <p class="muted" style="margin:-2px 0 11px">충동의 목소리와 내 선택을 분리하고, 내가 남긴 말 쪽으로 생각과 행동을 돌려봅니다.</p>\n      <button class="btn sec" id="capsule-disarm">이 초심으로 DISARM 해보기</button>\n    </div>\n    <div id="capsule-manage">\n      <button class="btn sec" id="capsule-edit-btn">수정하기</button>''', 'Future Self DISARM link')

rep("capsuleFrom=from==='panic'?'panic':'tools';", "capsuleFrom=from==='panic'?'panic':(from==='smart-disarm'?'smart-disarm':'tools');", 'capsule origin')

rep('''    back.textContent=capsuleFrom==='panic'?'← 위기 도움':'← 회복도구';\n    back.onclick=()=>capsuleFrom==='panic'?go('panic'):go('tools');''', '''    back.textContent=capsuleFrom==='panic'?'← 위기 도움':(capsuleFrom==='smart-disarm'?'← DISARM':'← 회복도구');\n    back.onclick=()=>capsuleFrom==='panic'?go('panic'):appBack(capsuleFrom==='smart-disarm'?'smart-disarm':'tools');''', 'capsule route-aware back')

rep('''  const manage=$('#capsule-manage'), pa=$('#capsule-panic-actions');\n  if(manage) manage.classList.toggle('hide',capsuleFrom==='panic');\n  if(pa) pa.classList.toggle('hide',capsuleFrom!=='panic');''', '''  const manage=$('#capsule-manage'), pa=$('#capsule-panic-actions'), dl=$('#capsule-disarm-link');\n  if(manage) manage.classList.toggle('hide',capsuleFrom==='panic');\n  if(pa) pa.classList.toggle('hide',capsuleFrom!=='panic');\n  if(dl) dl.classList.toggle('hide',capsuleFrom==='panic'||famMode()||!has||capsuleEditing);''', 'capsule bridge visibility')

rep('''    $('#capsule-edit-btn').onclick=()=>{ capsuleEditing=true; drawCapsule(); };\n    $('#capsule-delete').onclick=()=>{''', '''    $('#capsule-edit-btn').onclick=()=>{ capsuleEditing=true; drawCapsule(); };\n    const disarm=$('#capsule-disarm');\n    if(disarm) disarm.onclick=()=>go('smart-disarm');\n    $('#capsule-delete').onclick=()=>{''', 'capsule DISARM handler')

rep("save(); closeModal(); capsuleEditing=true; capsuleFrom='tools'; drawCapsule(); drawTools(); drawPanic(); toast('삭제했습니다.');", "save(); closeModal(); capsuleEditing=true; drawCapsule(); drawTools(); drawPanic(); toast('삭제했습니다.');", 'preserve capsule origin on delete')
rep("save(); capsuleEditing=false; capsuleFrom='tools'; drawCapsule(); drawTools(); drawPanic(); toast('미래의 나에게 남겨두었습니다.');", "save(); capsuleEditing=false; drawCapsule(); drawTools(); drawPanic(); toast('미래의 나에게 남겨두었습니다.');", 'preserve capsule origin on save')

rep('''  fam.innerHTML=''; tools.style.display='block';\n  const now=$('#smart-disarm-now'), add=$('#smart-disarm-new');\n  if(now) now.onclick=()=>openSmartDisarmNow();\n  if(add) add.onclick=()=>openSmartDisarmEditor(null);\n  if(!list) return;''', '''  fam.innerHTML=''; tools.style.display='block';\n  const now=$('#smart-disarm-now'), add=$('#smart-disarm-new'), cap=$('#smart-disarm-capsule');\n  if(now) now.onclick=()=>openSmartDisarmNow();\n  if(add) add.onclick=()=>openSmartDisarmEditor(null);\n  if(cap){\n    const hasCap=capsuleHas();\n    cap.innerHTML='<button class="btn sec" id="smart-disarm-capsule-open">'+(hasCap?'초심 다시 보기':'미래의 나에게 남기기')+'</button>'\n      +'<div class="tiny" style="margin:6px 2px 0">'+(hasCap?'내가 남겨둔 「미래의 나에게」 글로 돌아가 회복의 이유를 다시 확인합니다.':'충동이 덜할 때, 힘든 순간의 나에게 붙잡을 말을 미리 남겨둘 수 있습니다.')+'</div>';\n    const cb=$('#smart-disarm-capsule-open');\n    if(cb) cb.onclick=()=>openCapsule('smart-disarm',false);\n  }\n  if(!list) return;''', 'DISARM Future Self bridge')

idx.write_text(s, encoding='utf-8')

sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
if "const APP_VERSION = 'V8.2.11';" not in w or "const V = 'ohg-v8211-smart-tools-hub';" not in w:
    raise SystemExit('MISSING: sw version markers')
w = w.replace("const APP_VERSION = 'V8.2.11';", "const APP_VERSION = 'V8.2.12';", 1)
w = w.replace("const V = 'ohg-v8211-smart-tools-hub';", "const V = 'ohg-v8212-capsule-disarm-link';", 1)
sw.write_text(w, encoding='utf-8')

print('V8.2.12 patch PASS:', ', '.join(repls))
