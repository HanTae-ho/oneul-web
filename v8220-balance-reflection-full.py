from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='<div class="note" style="margin-bottom:10px"><b>번역본의 돌아보기 질문</b><br>나는 균형 잡힌 삶을 살고 있나요?<br>나의 참된 가치와 우선순위가 반영되어 있나요?<br>더 많은 관심이 필요한 영역이나 계속 미뤄진 꿈·욕망이 있나요?<br>어떤 영역에 더 관심을 주고, 어떤 영역에는 덜 집중해야 할까요?</div>'
new='<details class="card tight" style="margin-bottom:10px"><summary style="cursor:pointer;font-weight:700">번역본 돌아보기 질문 전체 보기</summary><div class="muted" style="margin-top:10px;line-height:1.75">1. 저는 균형 잡힌 삶을 살고 있나요?<br>2. 여기에 나의 참된 가치와 우선순위가 반영되어 있나요?<br>3. 내가 살 날이 한 달 남았다면, 이것이 내가 시간을 보낼 방식인가요?<br>4. 너무 많은 활동에 참여하고 있나요? 해야 할 일이 너무 많은가요?<br>5. 내 시간의 얼마나 많은 부분이 다른 사람들을 돌보느라 사용되나요? 나를 위해서는?<br>6. 내 삶에서 더 많은 관심이 필요한 영역이 있습니까?<br>7. 계속 미뤄진 꿈이나 욕망이 있습니까? 그것에 집중하고 싶습니까?<br>8. 어떤 영역이 더 많은 관심을 필요로 합니까? 덜 집중해야 할 분야는 무엇인가요?<br>9. 내가 어떤 변화를 원하고 있습니까? 내 삶을 균형 잡힌 모양으로 살기 위해 무엇을 할 수 있나요?</div></details>'
if s.count(old)!=1: raise SystemExit(f'expected 1 old reflection block, found {s.count(old)}')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('full translated reflection prompts preserved')
