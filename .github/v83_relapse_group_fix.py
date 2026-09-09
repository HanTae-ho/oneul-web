from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old=r'''  const relapseDays=relapses.filter(r=>Number.isFinite(+r.days)&&+r.days>0);
  if(relapseDays.length>=2){
    const vals=relapseDays.map(r=>+r.days);
    const avg=Math.round(vals.reduce((a,b)=>a+b,0)/vals.length);
    const lo=Math.min.apply(null,vals), hi=Math.max.apply(null,vals);
    add('다시 시작 전 회복기간', '저장된 다시 시작 기록 '+relapseDays.length+'회에서 직전 회복기간은 평균 '+avg+'일이었고, 기록 범위는 '+lo+'~'+hi+'일이었습니다.');
  }

  if(relapses.length>=2){
    const counts={};
    relapses.forEach(r=>new Set(Array.isArray(r.halt)?r.halt:[]).forEach(k=>{ if(k) counts[k]=(counts[k]||0)+1; }));
    const ranked=Object.entries(counts).map(([k,n])=>({k,n})).sort((a,b)=>b.n-a.n);
    if(ranked.length&&ranked[0].n>=2){
      const top=ranked[0], meta=HALTS.find(x=>x.k===top.k);
      add('다시 시작 기록에서 반복된 상태', '다시 시작 기록 '+relapses.length+'회 중 '+top.n+'회에서 '+(meta?meta.l:top.k)+'을 함께 선택했습니다.');
    }
  }
'''
new=r'''  const relapseGroups={};
  relapses.forEach(r=>{
    const k=String(r.type||'etc');
    if(!relapseGroups[k]) relapseGroups[k]=[];
    relapseGroups[k].push(r);
  });
  Object.entries(relapseGroups).forEach(([type,rows])=>{
    const label=(typeOf(type)||{}).n||'회복';
    const withDays=rows.filter(r=>Number.isFinite(+r.days)&&+r.days>0);
    if(withDays.length>=2){
      const vals=withDays.map(r=>+r.days);
      const avg=Math.round(vals.reduce((a,b)=>a+b,0)/vals.length);
      const lo=Math.min.apply(null,vals), hi=Math.max.apply(null,vals);
      add(label+' · 다시 시작 전 회복기간', label+' 다시 시작 기록 '+withDays.length+'회에서 직전 회복기간은 평균 '+avg+'일이었고, 기록 범위는 '+lo+'~'+hi+'일이었습니다.');
    }
    if(rows.length>=2){
      const counts={};
      rows.forEach(r=>new Set(Array.isArray(r.halt)?r.halt:[]).forEach(k=>{ if(k) counts[k]=(counts[k]||0)+1; }));
      const ranked=Object.entries(counts).map(([k,n])=>({k,n})).sort((a,b)=>b.n-a.n);
      if(ranked.length&&ranked[0].n>=2){
        const top=ranked[0], meta=HALTS.find(x=>x.k===top.k);
        add(label+' · 다시 시작 때 반복된 상태', label+' 다시 시작 기록 '+rows.length+'회 중 '+top.n+'회에서 '+(meta?meta.l:top.k)+'을 함께 선택했습니다.');
      }
    }
  });
'''
if s.count(old)!=1:
    raise SystemExit(f'relapse block anchor count={s.count(old)}')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('V8.3 relapse grouping fix applied')
