from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

# Version only; typography intentionally unchanged.
s=s.replace("const BUILD = 'V8.2.45';", "const BUILD = 'V8.2.46';", 1)

# Urge screen: inline, read-only time-capsule reveal immediately above helpful reading.
needle='  <button class="btn sec" id="ur-read">도움이 되는 글 읽기</button>'
insert='''  <button class="btn sec" id="ur-capsule-toggle" aria-expanded="false">미래의 나에게 바로보기</button>\n  <div id="ur-capsule-inline" class="hide" style="margin-top:9px"></div>\n  <div style="height:9px"></div>\n  <button class="btn sec" id="ur-read">도움이 되는 글 읽기</button>'''
assert s.count(needle)==1, f'ur-read target count={s.count(needle)}'
s=s.replace(needle, insert, 1)

old_pk="$('#pk-urge').onclick = () => go('urge');"
new_pk="$('#pk-urge').onclick = () => { drawUrgeCapsuleInline(false); go('urge'); };"
assert s.count(old_pk)==1, f'pk-urge target count={s.count(old_pk)}'
s=s.replace(old_pk,new_pk,1)

old_handlers="""$('#tm-read').onclick = () => { urgeUseCope('도움되는 글 읽기'); openRead('timer'); };   /* 타이머는 계속 돕습니다 */\n$('#ur-read').onclick = () => { urgeUseCope('도움되는 글 읽기'); openRead('urge'); };"""
new_handlers="""$('#tm-read').onclick = () => { urgeUseCope('도움되는 글 읽기'); openRead('timer'); };   /* 타이머는 계속 돕습니다 */\n\n/* V8.2.46 · 충동 대응 화면 안에서 저장해 둔 초심글을 이동 없이 바로 봅니다.\n   여기서는 읽기만 하며 timeCapsule 저장형식은 변경하지 않습니다. */\nfunction drawUrgeCapsuleInline(open){\n  const btn=$('#ur-capsule-toggle'), box=$('#ur-capsule-inline');\n  if(!btn||!box) return;\n  const show=!!open;\n  btn.setAttribute('aria-expanded',show?'true':'false');\n  btn.textContent=show?'미래의 나에게 접기':'미래의 나에게 바로보기';\n  if(!show){ box.classList.add('hide'); box.innerHTML=''; return; }\n  const c=capsuleData(), text=String(c.text||'').trim();\n  box.classList.remove('hide');\n  box.innerHTML=text\n    ? '<div class=\"card\" style=\"margin:0\"><h3>미래의 나에게</h3><div style=\"white-space:pre-wrap;font-size:16px;line-height:1.8\">'+esc(text)+'</div></div>'\n    : '<div class=\"note\" style=\"margin:0\">아직 남겨둔 글이 없습니다.</div>';\n}\nconst urCapsuleToggle=$('#ur-capsule-toggle');\nif(urCapsuleToggle) urCapsuleToggle.onclick=()=>drawUrgeCapsuleInline(urCapsuleToggle.getAttribute('aria-expanded')!=='true');\n$('#ur-read').onclick = () => { urgeUseCope('도움되는 글 읽기'); openRead('urge'); };"""
assert s.count(old_handlers)==1, f'urge handlers target count={s.count(old_handlers)}'
s=s.replace(old_handlers,new_handlers,1)

# Listening list: replace chip grid with vertical single accordion.
start=s.index("  if(!one){\n    /* V8.2.45 · 범주 칩은 단일 아코디언처럼 동작합니다.")
end_marker="    return;\n  }\n\n  if(ls.i < 0) ls.i = 0;"
end=s.index(end_marker,start)
new_block="""  if(!one){\n    /* V8.2.46 · 모바일에서는 범주를 세로형 단일 아코디언으로 보여줍니다.\n       한 범주를 열면 이전 범주는 닫히며, 한 화면에 필요한 글만 남깁니다. */\n    let h = '<p class=\"muted\" style=\"margin:-4px 0 12px\">' +\n      '지금 상태에 가까운 범주를 누르세요. 한 번에 한 범주의 글만 보여드립니다.</p>';\n    h += '<div id=\"ls-tags\">';\n    LTAG.forEach(t=>{\n      const list=LISTEN.filter(x=>x.g===t.k), on=ls.tag===t.k;\n      h += '<div class=\"acc'+(on?' on':'')+'\" data-ls-acc=\"'+esc(t.k)+'\">' +\n        '<button class=\"acc-h\" type=\"button\" data-ls-tag=\"'+esc(t.k)+'\" aria-expanded=\"'+(on?'true':'false')+'\">' +\n        '<span class=\"acc-n\"><b>'+esc(t.l)+'</b><span>'+list.length+'편</span></span>' +\n        '<span aria-hidden=\"true\" style=\"font-size:22px;line-height:1;color:var(--faint)\">'+(on?'−':'+')+'</span></button>' +\n        '<div class=\"acc-b\">';\n      if(on){\n        list.forEach(x=>{\n          h += '<button class=\"help\" style=\"width:100%;text-align:left\" data-ls=\"'+x.n+'\">' +\n            '<span class=\"b\"><b>'+esc(x.t)+'</b></span>' +\n            '<span class=\"acts\"><span class=\"go\">읽기</span></span></button>';\n        });\n      }\n      h += '</div></div>';\n    });\n    h += '</div>';\n    $('#ls-list').innerHTML=h;\n    $('#ls-list').querySelectorAll('[data-ls-tag]').forEach(b=>b.onclick=()=>{\n      const k=b.dataset.lsTag||'';\n      ls.tag=ls.tag===k?'':k;\n      drawListen();\n      if(ls.tag){\n        setTimeout(()=>{\n          const row=$('#ls-list').querySelector('[data-ls-acc=\"'+ls.tag+'\"]'), v=$('#view');\n          if(row&&v) v.scrollTo({top:Math.max(0,v.scrollTop+row.getBoundingClientRect().top-66),behavior:'smooth'});\n        },30);\n      }\n    });\n    $('#ls-list').querySelectorAll('[data-ls]').forEach(b=>b.onclick=()=>{\n      ls.i=LISTEN.findIndex(x=>x.n===+b.dataset.ls);\n      drawListen(); rdTop();\n    });\n    return;\n  }\n\n  if(ls.i < 0) ls.i = 0;"""
s=s[:start]+new_block+s[end+len(end_marker):]

assert "const BUILD = 'V8.2.46';" in s
assert 'data-ls-acc' in s and 'ur-capsule-toggle' in s
assert "font:15px/1.6" in s, 'base font unexpectedly changed'
assert '.rdcard p{margin:0;font-size:16.5px' in s, 'reading font unexpectedly changed'
p.write_text(s,encoding='utf-8')

# Service worker version/cache only.
sw=Path('sw.js')
t=sw.read_text(encoding='utf-8')
assert "const APP_VERSION = 'V8.2.45';" in t
assert "const V = 'ohg-v8245-mobile-scroll';" in t
t=t.replace("const APP_VERSION = 'V8.2.45';", "const APP_VERSION = 'V8.2.46';",1)
t=t.replace("const V = 'ohg-v8245-mobile-scroll';", "const V = 'ohg-v8246-listen-accordion-capsule';",1)
sw.write_text(t,encoding='utf-8')

# Changelog.
r=Path('README.md')
rt=r.read_text(encoding='utf-8')
head="""# V8.2.46 — 듣는 글 세로 아코디언 · 충동 초심글 바로보기\n\n- `듣는 글`의 범주 칩을 없애고 12단계 점검처럼 세로형 단일 아코디언으로 바꿉니다. 다른 범주를 열면 이전 범주는 자동으로 닫힙니다.\n- `지금 위험해요 → 충동이 올라와요 → 지금 충동이 얼마나 센가요?` 화면에서 `도움이 되는 글 읽기` 바로 위에 `미래의 나에게 바로보기`를 둡니다. 다른 화면으로 이동하지 않고 기기에 저장한 초심글을 그 자리에서 펼쳐 읽습니다.\n- V8.2.45와 V8.2.44의 글자 크기를 대조했으며 전역 본문 15px, 읽는 글 본문 16.5px 등 기존 값을 유지합니다. 이번 버전에서는 글자 크기를 변경하지 않습니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, timeCapsule 저장형식, Android 정확알림·화면 OFF·부팅 재예약·외래 반복예약·이완 TTS는 변경하지 않습니다.\n\n"""
assert not rt.startswith('# V8.2.46')
r.write_text(head+rt,encoding='utf-8')
print('V8.2.46 patch PASS')
