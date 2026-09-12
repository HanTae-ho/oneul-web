from pathlib import Path
p=Path('meaning-check-feature.js')
s=p.read_text(encoding='utf-8')
old='최근의 나를 기준으로 답해보세요. 0은 전혀 아니다, 4는 매우 그렇다입니다.<br><span class="tiny">답을 고를 때마다 <b>작성 중 답변만 임시저장</b>됩니다.'
new='최근의 나를 기준으로 답해보세요. 0은 전혀 아니다, 4는 매우 그렇다입니다.<br><span class="tiny">MIL-II의 구성개념을 참고한 오늘 한 걸음 자체 자기점검이며, 진단검사가 아닙니다.</span><br><span class="tiny">답을 고를 때마다 <b>작성 중 답변만 임시저장</b>됩니다.'
if s.count(old)!=1: raise SystemExit(f'non-diagnostic copy anchor count={s.count(old)}')
p.write_text(s.replace(old,new,1),encoding='utf-8')
