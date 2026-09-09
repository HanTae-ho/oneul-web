from pathlib import Path


def replace_one(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 anchor, found {count}')
    return text.replace(old, new, 1)

p = Path('index.html')
s = p.read_text(encoding='utf-8')

s = replace_one(s, "const BUILD='V8.2.69';", "const BUILD='V8.3';", 'BUILD')
s = replace_one(
    s,
    "let recTab = 'mood';\nlet recPracticeFilter = 'all';",
    "let recTab = 'mood';\nlet recStatView = 'stat';\nlet recPracticeFilter = 'all';",
    'recStatView state'
)

old_tabs = """  const tabs = famMode()\n    ? [{v:'mood',l:'감정'},{v:'day',l:'하루'},{v:'body',l:'몸'},{v:'work',l:'실천기록'},{v:'screen',l:'자가점검'},{v:'stat',l:'통계'}]\n    : [{v:'mood',l:'감정'},{v:'urge',l:'충동'},{v:'day',l:'하루'},{v:'body',l:'몸'},\n       {v:'relapse',l:'다시 시작'},{v:'work',l:'실천기록'},{v:'screen',l:'자가점검'},{v:'stat',l:'통계'}];"""
new_tabs = """  const tabs = famMode()\n    ? [{v:'mood',l:'감정'},{v:'day',l:'하루'},{v:'body',l:'몸'},{v:'work',l:'실천기록'},{v:'screen',l:'자가점검'},{v:'stat',l:'통계'}]\n    : [{v:'mood',l:'감정'},{v:'urge',l:'충동'},{v:'day',l:'하루'},{v:'body',l:'몸'},\n       {v:'relapse',l:'다시 시작'},{v:'work',l:'실천기록'},{v:'screen',l:'자가점검'},{v:'stat',l:'통계 · 패턴'}];"""
s = replace_one(s, old_tabs, new_tabs, 'record tabs')

pattern_code = r'''function recStat(){
  if(famMode()) return recStatCore();
  const w=el('div');
  const nav=el('div','opts');
  nav.style.marginBottom='12px';
  [{v:'stat',l:'기록 통계'},{v:'pattern',l:'내 회복 패턴'}].forEach(o=>{
    const b=el('button','opt'+(recStatView===o.v?' on':''),o.l);
    b.onclick=()=>{ recStatView=o.v; drawRec(); };
    nav.appendChild(b);
  });
  w.appendChild(nav);
  w.appendChild(recStatView==='pattern'?recPattern():recStatCore());
  return w;
}

function recPattern(){
  const w=el('div');
  const DAY=86400000, since=Date.now()-90*DAY;
  const timed=r=>r&&Number.isFinite(+r.t)&&+r.t>=since;
  const dayKey=t=>{
    const d=new Date(+t);
    if(!Number.isFinite(d.getTime())) return '';
    return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
  };
  const urges=(S.urges||[]).filter(timed);
  const halts=(S.halts||[]).filter(timed);
  const moods=(S.moods||[]).filter(timed);
  const sleeps=(S.sleepLog||[]).filter(timed);
  const relapses=(S.relapses||[]).filter(r=>r&&Number.isFinite(+r.t));
  const urgeDays=new Set(urges.map(r=>dayKey(r.t)).filter(Boolean));
  const cards=[];
  const add=(title,text)=>cards.push({title,text});

  if(urges.length>=3){
    const buckets=[
      {a:0,b:6,l:'새벽 0~6시',n:0},
      {a:6,b:12,l:'오전 6~12시',n:0},
      {a:12,b:18,l:'오후 12~18시',n:0},
      {a:18,b:24,l:'저녁 18~24시',n:0}
    ];
    urges.forEach(r=>{
      const h=new Date(+r.t).getHours();
      const x=buckets.find(v=>h>=v.a&&h<v.b); if(x) x.n++;
    });
    buckets.sort((a,b)=>b.n-a.n);
    const top=buckets[0], share=top.n/urges.length;
    if(top.n>=2&&share>=0.4){
      add('충동이 많이 기록된 시간', '최근 90일 충동 기록 '+urges.length+'건 중 '+top.n+'건('+Math.round(share*100)+'%)이 '+top.l+'에 기록되었습니다.');
    }
  }

  if(urgeDays.size>=3&&halts.length){
    const codeDays={};
    halts.forEach(r=>{
      const d=dayKey(r.t); if(!urgeDays.has(d)) return;
      new Set(Array.isArray(r.v)?r.v:[]).forEach(k=>{
        if(!codeDays[k]) codeDays[k]=new Set();
        codeDays[k].add(d);
      });
    });
    const ranked=Object.entries(codeDays).map(([k,set])=>({k,n:set.size})).sort((a,b)=>b.n-a.n);
    if(ranked.length&&ranked[0].n>=2){
      const top=ranked[0], meta=HALTS.find(x=>x.k===top.k);
      add('충동과 같은 날 반복된 HALT', '충동이 기록된 '+urgeDays.size+'일 중 '+top.n+'일에 '+(meta?meta.l:top.k)+'도 같은 날 기록되었습니다.');
    }
  }

  if(urgeDays.size>=3&&moods.length){
    const lowDays=new Set(moods.filter(r=>+r.v<=2).map(r=>dayKey(r.t)).filter(Boolean));
    let overlap=0; lowDays.forEach(d=>{ if(urgeDays.has(d)) overlap++; });
    if(lowDays.size>=2&&overlap>=2){
      add('힘든 기분과 충동이 겹친 날', '기분을 힘듦 또는 많이힘듦으로 기록한 '+lowDays.size+'일 중 '+overlap+'일에 충동도 같은 날 기록되었습니다.');
    }
  }

  if(urgeDays.size>=3&&sleeps.length){
    const badDays=new Set(sleeps.filter(r=>r.q==='bad').map(r=>dayKey(r.t)).filter(Boolean));
    let overlap=0; badDays.forEach(d=>{ if(urgeDays.has(d)) overlap++; });
    if(badDays.size>=2&&overlap>=2){
      add('잠을 못 잔 날과 충동', '잠을 못 잤다고 기록한 '+badDays.size+'일 중 '+overlap+'일에 충동도 같은 날 기록되었습니다.');
    }
  }

  if(urges.length>=3){
    const counts={};
    urges.forEach(r=>new Set(Array.isArray(r.cope)?r.cope:[]).forEach(x=>{ if(x) counts[x]=(counts[x]||0)+1; }));
    const ranked=Object.entries(counts).map(([k,n])=>({k,n})).sort((a,b)=>b.n-a.n);
    if(ranked.length&&ranked[0].n>=2){
      add('자주 사용한 충동 대처', '최근 충동 기록에서 '+ranked[0].k+'을 '+ranked[0].n+'회 사용했다고 남겼습니다. 효과를 단정하지 않고, 내가 반복해서 선택한 대처로만 표시합니다.');
    }
  }

  const relapseDays=relapses.filter(r=>Number.isFinite(+r.days)&&+r.days>0);
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

  w.appendChild(el('div','note','<b>내 기록에서 보이는 흐름</b><br>최근 90일의 기기 내 기록을 서로 연결해 반복된 사실만 보여드립니다. 진단·위험도 점수·재발 예측이 아니며, 자가점검 점수는 이 계산에 섞지 않습니다. 다시 시작 전 회복기간은 저장된 전체 다시 시작 기록을 참고합니다.'));

  if(!cards.length){
    w.appendChild(emptyBox('아직 반복되는 흐름을 말하기에 기록이 충분하지 않습니다. 같은 종류의 기록이 2~3번 이상 더 쌓이면 확인할 수 있습니다.'));
  }else{
    cards.slice(0,6).forEach(x=>{
      const c=el('div','card tight');
      c.innerHTML='<h3>'+esc(x.title)+'</h3><p style="margin:0;line-height:1.72">'+esc(x.text)+'</p>';
      w.appendChild(c);
    });
  }
  w.appendChild(el('p','tiny','기록이 늘어나면 보이는 흐름도 달라질 수 있습니다. 중요한 결정이나 치료 판단은 이 화면만으로 하지 마세요.'));
  return w;
}

'''
s = replace_one(s, 'function recStat(){', pattern_code + 'function recStatCore(){', 'recStat wrapper')
s = replace_one(s, "return emptyBox('기록이 쌓이면 여기에 나의 회복 패턴이 보입니다.');", "return emptyBox('기록이 쌓이면 여기에 통계가 보입니다.');", 'stats empty text')

s = s.replace('감정 · 충동 · 하루 · 몸 · 실천기록 · 자가점검 · 통계</span>', '감정 · 충동 · 하루 · 몸 · 실천기록 · 자가점검 · 통계 · 회복 패턴</span>')
s = s.replace('<b>나 → 내 발자취</b>에서 감정·충동·하루·몸·실천기록·자가점검·통계를 다시 볼 수 있습니다.', '<b>나 → 내 발자취</b>에서 감정·충동·하루·몸·실천기록·자가점검·통계·회복 패턴을 다시 볼 수 있습니다.')
s = s.replace('<b>감정 · 충동 · 하루 · 몸 · 다시 시작 · 실천기록 · 자가점검 · 통계</b>를 한곳에서 돌아봅니다.', '<b>감정 · 충동 · 하루 · 몸 · 다시 시작 · 실천기록 · 자가점검 · 통계 · 회복 패턴</b>을 한곳에서 돌아봅니다.')
s = s.replace('<p style="margin-top:8px">12단계와 회복 실천도구의 저장기록도 실천기록에서 상세 내용을 다시 열 수 있습니다.</p>', '<p style="margin-top:8px">12단계와 회복 실천도구의 저장기록도 실천기록에서 상세 내용을 다시 열 수 있습니다.</p>\n      <p style="margin-top:8px"><b>통계 · 패턴</b>에서는 기존 기록 통계와 <b>내 회복 패턴</b>을 전환해 볼 수 있습니다. 내 회복 패턴은 최근 90일 기기 기록에서 반복된 사실을 설명할 뿐 진단·재발예측이 아니며, 자가점검 점수를 다른 기록과 합쳐 위험점수로 만들지 않습니다.</p>')
s = s.replace('<b>내 발자취</b>에서는 감정·충동·하루·몸·실천기록·자가점검·통계를 다시 보고,', '<b>내 발자취</b>에서는 감정·충동·하루·몸·실천기록·자가점검·통계·회복 패턴을 다시 보고,')

p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
t = sw.read_text(encoding='utf-8')
t = replace_one(t, "const APP_VERSION = 'V8.2.69';", "const APP_VERSION = 'V8.3';", 'SW version')
t = replace_one(t, "const V = 'ohg-v8269-me-smart';", "const V = 'ohg-v830-recovery-patterns';", 'SW cache')
sw.write_text(t, encoding='utf-8')

for name in ('privacy.html','legal.html'):
    q=Path(name)
    u=q.read_text(encoding='utf-8')
    old='<span class="ver">V8.2.69</span>'
    if old in u:
        u=u.replace(old,'<span class="ver">V8.3</span>',1)
    q.write_text(u,encoding='utf-8')

readme=Path('README.md')
r=readme.read_text(encoding='utf-8')
entry="""## V8.3 — 내 회복 패턴\n- `나 → 내 발자취 → 통계 · 패턴` 안을 `기록 통계 | 내 회복 패턴`으로 나눴습니다. 기존 통계는 그대로 유지합니다.\n- `내 회복 패턴`은 최근 90일의 로컬 기록을 이용해 충동 시간대, 충동과 같은 날의 HALT·힘든 기분·수면, 반복해서 사용한 충동 대처를 사실 수준으로 보여줍니다. 다시 시작 기록이 2회 이상 쌓인 경우 직전 회복기간과 반복된 HALT도 참고합니다.\n- 진단·위험도 점수·재발예측을 만들지 않으며, 자가점검 점수도 다른 기록과 합산하지 않습니다. 기록은 외부 서버나 마음프로로 전송하지 않습니다.\n- `DATA_SCHEMA=6`, 저장키 `ohg.v1`, 기존 기록형식, Android 정확알림·화면 OFF·부팅 재예약·복약/외래/생활/습관 알림·마음프로 TTS·이완 TTS 엔진은 변경하지 않습니다.\n\n"""
if not r.startswith('## V8.3 — 내 회복 패턴'):
    r=entry+r
readme.write_text(r,encoding='utf-8')

print('V8.3 recovery pattern patch applied')
