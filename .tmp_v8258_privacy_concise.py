from pathlib import Path

idx=Path('index.html')
sw=Path('sw.js')
readme=Path('README.md')

s=idx.read_text(encoding='utf-8')
pairs=[
("const BUILD = 'V8.2.57';","const BUILD = 'V8.2.58';"),
('기기 저장 · 위치 · 마음프로 · 외부 서비스 데이터 처리 안내','기기 저장 · 마음프로 · 외부 전송 안내')
]
for old,new in pairs:
    n=s.count(old)
    assert n==1,(old,n)
    s=s.replace(old,new,1)
idx.write_text(s,encoding='utf-8')

w=sw.read_text(encoding='utf-8')
for old,new in [
("const APP_VERSION = 'V8.2.57';","const APP_VERSION = 'V8.2.58';"),
("const V = 'ohg-v8257-privacy-policy';","const V = 'ohg-v8258-privacy-concise';")
]:
    n=w.count(old)
    assert n==1,(old,n)
    w=w.replace(old,new,1)
sw.write_text(w,encoding='utf-8')

r=readme.read_text(encoding='utf-8')
entry='''## V8.2.58 — 개인정보처리방침 간결화\n- V8.2.57의 실제 데이터 흐름은 유지하면서 개인정보처리방침을 핵심 6개 항목으로 줄여 읽기 쉽게 정리했습니다.\n- 기기 내부 기록, 마음프로·의견의 외부 전송, 위치·Android 권한, 보유·삭제, 외부 서비스, 이용자 선택·문의만 남기고 반복 설명과 세부 표를 제거했습니다.\n- 개인정보 관련 문의 이메일을 `admin@maumpro.com`으로 변경했습니다.\n- 마음프로 일반 AI 대화는 익명형 clientId·현재 메시지·주제·앱 버전·최근 일반 AI 대화 최대 8개가 Apps Script 중계 후 OpenAI API로 전송되는 실제 동작을 그대로 공개합니다. 저장된 회복기록은 자동 첨부하지 않습니다.\n- `DATA_SCHEMA=6`, `ohg.v1`, 기존 기록형식과 Android 정확알림·화면 OFF 알림·부팅 재예약·복약/외래/생활/습관 알림·네이티브 TTS·이완 TTS는 변경하지 않습니다.\n\n'''
assert not r.startswith('## V8.2.58')
readme.write_text(entry+r,encoding='utf-8')
