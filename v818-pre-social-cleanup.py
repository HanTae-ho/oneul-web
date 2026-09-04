from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,n=1):
    global s
    c=s.count(old)
    assert c==n, f'expected {n} occurrences, got {c}: {old[:80]}'
    s=s.replace(old,new)

rep("const BUILD = 'V8.1.7';\nconst KEY = 'ohg.v1';", "const BUILD = 'V8.1.8';\n/* 개인 회복기록 S의 저장 키와 데이터 스키마입니다.\n   향후 소셜의 닉네임·게시글·댓글·인증정보는 이 KEY/S에 넣지 않고 별도 서버 영역으로 분리합니다.\n   따라서 현재의 회복기록 백업(JSON)에도 소셜 데이터는 포함되지 않습니다. */\nconst KEY = 'ohg.v1';\nconst DATA_SCHEMA = 2;")
rep("  ver: 1, started: false,", "  ver: 1, dataSchema: DATA_SCHEMA, started: false,")
rep("function migrate(s){\n", "function migrate(s){\n  /* 앱 버전과 개인 기록 형식의 버전은 별도로 관리합니다. 기존 백업도 불러오면 현재 스키마로 올립니다. */\n  s.dataSchema = DATA_SCHEMA;\n")
rep("return emptyBox('내 정보에서 복약과 식사·잠을 정해두면 여기에 쌓입니다.');", "return emptyBox('회복도구 → 일정·알림에서 복약과 식사·잠을 정해두면 여기에 쌓입니다.');")
rep("'시 무렵</b>입니다. 내 정보에서 이 시간을 위험 시간대로 등록해두면 미리 챙겨드립니다.</div>'", "'시 무렵</b>입니다. 회복도구 → 일정·알림 → 생활 일정에서 이 시간을 위험 시간대로 등록해두면 미리 챙겨드립니다.</div>'")
rep("aiAdd('assistant','내정보에서는 회복 영역·시작일·지역·일정·알림 설정과 앱 설정, 기록 내보내기 등을 관리할 수 있어요.', true);", "aiAdd('assistant','내정보에서는 회복 영역·시작일·지역과 앱 설정, 내 발자취·기록 내보내기 등을 관리할 수 있어요. 일정과 알림은 [회복도구] → [일정·알림]에서 관리할 수 있어요.', true);")
p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
w=sw.read_text(encoding='utf-8')
assert "const APP_VERSION = 'V8.1.7';" in w
assert "const V = 'ohg-v817-home-polish';" in w
w=w.replace("const APP_VERSION = 'V8.1.7';","const APP_VERSION = 'V8.1.8';")
w=w.replace("const V = 'ohg-v817-home-polish';","const V = 'ohg-v818-pre-social';")
sw.write_text(w,encoding='utf-8')
print('V8.1.8 pre-social cleanup patch PASS')
