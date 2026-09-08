from pathlib import Path

idx=Path('index.html')
sw=Path('sw.js')
readme=Path('README.md')

s=idx.read_text(encoding='utf-8')
assert "const BUILD = 'V8.2.58';" in s
assert 'function enableSingleAccordion(' not in s
s=s.replace("const BUILD = 'V8.2.58';", "const BUILD = 'V8.2.59';", 1)
anchor="const DATA_SCHEMA = 6;\n"
insert="""const DATA_SCHEMA = 6;\n\n/* V8.2.59 — 도움말·사용설명서 단일 아코디언. 새 항목을 열면 이전 항목은 자동으로 접습니다. */\nfunction enableSingleAccordion(rootSelector){\n  const root = document.querySelector(rootSelector);\n  if(!root) return;\n  root.querySelectorAll('details.faq').forEach(item => {\n    item.addEventListener('toggle', () => {\n      if(!item.open) return;\n      root.querySelectorAll('details.faq[open]').forEach(other => {\n        if(other !== item) other.open = false;\n      });\n    });\n  });\n}\nenableSingleAccordion('#p-guide');\nenableSingleAccordion('#p-manual');\n"""
assert s.count(anchor)==1
s=s.replace(anchor,insert,1)
idx.write_text(s,encoding='utf-8')

w=sw.read_text(encoding='utf-8')
assert "const APP_VERSION = 'V8.2.58';" in w
assert "const V = 'ohg-v8258-privacy-concise';" in w
w=w.replace("const APP_VERSION = 'V8.2.58';", "const APP_VERSION = 'V8.2.59';", 1)
w=w.replace("const V = 'ohg-v8258-privacy-concise';", "const V = 'ohg-v8259-single-accordion';", 1)
sw.write_text(w,encoding='utf-8')

r=readme.read_text(encoding='utf-8')
assert not r.startswith('## V8.2.59')
entry='''## V8.2.59 — 안내문 단일 아코디언 · 자동 폴딩\n- 도움말 · 자주 묻는 질문, 사용설명서, 개인정보처리방침을 단일 아코디언 방식으로 통일했습니다.\n- 같은 안내 화면에서 새 항목을 열면 이전에 열려 있던 항목은 자동으로 접히며, 열린 항목을 다시 누르면 닫힙니다.\n- 도움말은 기존 주제 구분과 바로가기, 사용설명서는 14개 안내 항목, 개인정보처리방침은 간결화된 6개 항목의 내용은 변경하지 않고 표시 방식만 정리했습니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, 기존 기록형식, 자가점검·12단계·회복 실천도구 저장, Android 정확알림·화면 OFF 알림·부팅 재예약·네이티브 TTS·이완 TTS는 변경하지 않습니다.\n\n'''
readme.write_text(entry+r,encoding='utf-8')
