from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

repls=[
("<b>회복도구 → 실천하기 → 의미점검</b>로 들어가면", "<b>회복도구 → 실천하기 → 의미점검</b>으로 들어가면"),
("<b>나 → 내 발자취</b>에서 감정·충동·하루·몸·실천기록·자가점검·통계·회복 패턴을 다시 볼 수 있습니다.", "<b>나 → 내 발자취</b>에서 감정·충동·하루·몸·실천기록(의미·12단계·회복 실천도구)·자가점검·통계·회복 패턴을 다시 볼 수 있습니다."),
("의미점검의 작성 중 답변은 임시저장되고, 10문항 뒤 <b>결과 저장</b>을 눌러야 완료기록으로 저장됩니다. 모든 기록은 현재 기기에만 저장됩니다.", "의미점검의 작성 중 답변은 임시저장되고, 10문항 뒤 <b>결과 저장</b>을 눌러야 완료기록으로 저장됩니다. 저장한 의미기록과 의미점검 완료결과는 <b>나 → 내 발자취 → 실천기록 → 의미</b>에서도 함께 볼 수 있습니다. 모든 기록은 현재 기기에만 저장됩니다."),
("의미점검은 작성 중 답변과 완료결과를 구분하며, 완료결과는 점검 기록에서 다시 볼 수 있습니다. 가족·보호자 모드에서는 가족을 위한 도구 중심으로 구성이 달라집니다.", "의미점검은 작성 중 답변과 완료결과를 구분하며, 완료결과는 점검 기록에서 다시 볼 수 있습니다. 의미 돌아보기와 의미점검 완료기록은 <b>내 발자취 → 실천기록 → 의미</b>에서도 함께 확인합니다. 가족·보호자 모드에서는 가족을 위한 도구 중심으로 구성이 달라집니다."),
("12단계와 회복 실천도구의 저장기록도 실천기록에서 상세 내용을 다시 열 수 있습니다.", "의미 돌아보기와 의미회복 간편점검 완료기록은 실천기록의 <b>의미</b> 필터에서 함께 확인할 수 있고, 12단계와 회복 실천도구 저장기록도 같은 실천기록에서 다시 열 수 있습니다."),
("<b>내 발자취</b>에서는 감정·충동·하루·몸·실천기록·자가점검·통계·회복 패턴을 다시 보고,", "<b>내 발자취</b>에서는 감정·충동·하루·몸·실천기록(의미·12단계·회복 실천도구)·자가점검·통계·회복 패턴을 다시 보고,"),
("const empty={all:'저장된 실천 기록이 없습니다.',meaning:'저장된 의미 기록이 없습니다.',step:'저장된 12단계 기록이 없습니다.',smart:'저장된 실천도구 기록이 없습니다.',family:'저장된 가족도구 기록이 없습니다.'};", "const empty={all:'저장된 기록이 없습니다.',meaning:'저장된 의미 기록이 없습니다.',step:'저장된 12단계 기록이 없습니다.',smart:'저장된 실천도구 기록이 없습니다.',family:'저장된 가족도구 기록이 없습니다.'};"),
("c.appendChild(el('h3','', (recPracticeFilter==='meaning'?'저장한 의미 기록 ':'저장한 실천 기록 ')+shown.length+'건'));", "c.appendChild(el('h3','', (recPracticeFilter==='meaning'?'저장한 의미 기록 ':(recPracticeFilter==='all'?'저장한 기록 ':'저장한 실천 기록 '))+shown.length+'건'));"),
]
for old,new in repls:
    if old not in s:
        raise SystemExit('missing expected review text: '+old[:80])
    s=s.replace(old,new,1)

old="""    (Array.isArray(S.meaningChecks)?S.meaningChecks:[]).forEach(r=>{
      if(!r||!r.d||!Array.isArray(r.answers))return;
      const axes=(r.domains&&typeof r.domains==='object')?r.domains:(typeof mcAxes==='function'?mcAxes(r.answers):{});
      const axisText=['나를 보는 힘 '+Number(axes.self||0).toFixed(1)+'/4','앞으로 향하는 힘 '+Number(axes.future||0).toFixed(1)+'/4','책임·선택 '+Number(axes.choice||0).toFixed(1)+'/4','관계·넘어섬 '+Number(axes.relation||0).toFixed(1)+'/4'].join(' · ');
      const dt=(typeof ymdDate==='function')?ymdDate(r.d):null;
      rows.push({
        group:'meaning',ts:Number(r.ts||(dt?dt.getTime():0)),title:'의미회복 간편점검',summary:Number(r.total||0)+'/40 · '+axisText,record:{kind:'meaning-check',d:r.d},
        open:()=>{if(typeof mcShowResult==='function')mcShowResult(r.d);}
      });
    });
"""
new="""    (typeof mcRecords==='function'?mcRecords():[]).forEach(r=>{
      const axes=(r.domains&&typeof r.domains==='object')?r.domains:(typeof mcAxes==='function'?mcAxes(r.answers):{});
      const total=Number.isFinite(Number(r.total))?Number(r.total):(typeof mcScore==='function'?mcScore(r.answers):0);
      const axisText=['나를 보는 힘 '+Number(axes.self||0).toFixed(1)+'/4','앞으로 향하는 힘 '+Number(axes.future||0).toFixed(1)+'/4','책임·선택 '+Number(axes.choice||0).toFixed(1)+'/4','관계·넘어섬 '+Number(axes.relation||0).toFixed(1)+'/4'].join(' · ');
      const dt=(typeof ymdDate==='function')?ymdDate(r.d):null;
      rows.push({
        group:'meaning',ts:Number(r.ts||(dt?dt.getTime():0)),title:'의미회복 간편점검',summary:total+'/40 · '+axisText,record:{kind:'meaning-check',d:r.d},
        open:()=>{if(typeof mcShowResult==='function')mcShowResult(r.d);}
      });
    });
"""
if s.count(old)!=1:
    raise SystemExit(f'meaningChecks block count={s.count(old)}')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
