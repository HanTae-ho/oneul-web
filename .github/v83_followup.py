from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
anchor="""  if(urgeDays.size>=3&&halts.length){\n"""
insert=r'''  if(urges.length>=3&&(S.hours||[]).length){
    const riskHours=new Set((S.hours||[]).filter(h=>Number.isInteger(+h)).map(Number));
    const hit=urges.filter(r=>riskHours.has(new Date(+r.t).getHours())).length;
    if(hit>=2){
      add('설정한 위험시간과 충동', '최근 90일 충동 기록 '+urges.length+'건 중 '+hit+'건('+Math.round(hit/urges.length*100)+'%)이 내가 설정한 위험시간에 기록되었습니다.');
    }
  }

  const sinceDay=dayKey(since), todayDay=dayKey(Date.now());
  const habitDays=new Set();
  (Array.isArray(S.habits)?S.habits:[]).forEach(h=>{
    (Array.isArray(h&&h.done)?h.done:[]).forEach(d=>{
      const v=String(d||'');
      if(/^\d{4}-\d{2}-\d{2}$/.test(v)&&v>=sinceDay&&v<=todayDay) habitDays.add(v);
    });
  });
  if(habitDays.size>=3){
    let overlap=0; habitDays.forEach(d=>{ if(urgeDays.has(d)) overlap++; });
    add('회복 실천이 기록된 날', '최근 90일 회복 실천을 기록한 '+habitDays.size+'일 중 '+overlap+'일에 충동도 같은 날 기록되었습니다. 이 숫자는 실천의 효과를 평가하는 점수가 아니라 기록이 겹친 날만 보여줍니다.');
  }

'''
if s.count(anchor)!=1:
    raise SystemExit(f'anchor count {s.count(anchor)}')
s=s.replace(anchor,insert+anchor,1)
s=s.replace('cards.slice(0,6).forEach(x=>{','cards.forEach(x=>{',1)
p.write_text(s,encoding='utf-8')

r=Path('README.md').read_text(encoding='utf-8')
old='- `내 회복 패턴`은 최근 90일의 로컬 기록을 이용해 충동 시간대, 충동과 같은 날의 HALT·힘든 기분·수면, 반복해서 사용한 충동 대처를 사실 수준으로 보여줍니다. 다시 시작 기록이 2회 이상 쌓인 경우 직전 회복기간과 반복된 HALT도 참고합니다.'
new='- `내 회복 패턴`은 최근 90일의 로컬 기록을 이용해 충동 시간대, 사용자가 설정한 위험시간과 충동의 겹침, 충동과 같은 날의 HALT·힘든 기분·수면, 회복 실천이 기록된 날, 반복해서 사용한 충동 대처를 사실 수준으로 보여줍니다. 다시 시작 기록이 2회 이상 쌓인 경우 직전 회복기간과 반복된 HALT도 참고합니다.'
if r.count(old)!=1:
    raise SystemExit('README anchor')
Path('README.md').write_text(r.replace(old,new,1),encoding='utf-8')
print('V8.3 follow-up applied')
