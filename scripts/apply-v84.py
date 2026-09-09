#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
idx = root / 'index.html'
s = idx.read_text(encoding='utf-8')


def rep(old, new, count=1, label='replace'):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f'{label}: expected {count}, found {n}')
    s = s.replace(old, new, count)


def sub(pattern, repl, count=1, label='regex'):
    global s
    s2, n = re.subn(pattern, repl, s, count=count, flags=re.S)
    if n != count:
        raise SystemExit(f'{label}: expected {count}, found {n}')
    s = s2

# Version
rep("const BUILD='V8.3';", "const BUILD='V8.4';", label='BUILD')

# Relationship vocabulary shared by urge, urge diary, relapse, and pattern analysis.
rep(
    "const URGE_COMPANY = ['혼자','가족과','친구·동료와','회복 동료와','그 밖의 사람과'];",
    "const URGE_COMPANY = ['혼자','배우자·연인','가족','친구','직장·학교 사람','과거 중독 관련 관계','회복 동료·자조모임 사람','그 밖의 사람'];\n"
    "function relationLabel(v){\n"
    "  const x=String(v||'');\n"
    "  const old={'가족과':'가족','친구·동료와':'친구','회복 동료와':'회복 동료·자조모임 사람','그 밖의 사람과':'그 밖의 사람','사람들과 함께':'그 밖의 사람'};\n"
    "  return old[x]||x;\n"
    "}",
    label='URGE_COMPANY'
)

# Keep the current urge flow: strength -> thoughts -> 5-minute delay -> optional context.
rep(
    '<button class="btn ghost" id="ur-track-toggle" aria-expanded="false">상황·촉발 기록 (선택) · 눌러서 기록</button>',
    '<button class="btn ghost" id="ur-track-toggle" aria-expanded="false">지금 상황 남기기 (선택) · 관계·장소·촉발</button>',
    label='urge context toggle'
)
rep(
    '<h3>누구와 있었나요? <span class="tiny" style="font-weight:400">(선택)</span></h3>\n      <div class="opts" id="ur-with"></div>',
    '<h3>그때 누구와 관련이 있었나요? <span class="tiny" style="font-weight:400">(선택)</span></h3>\n      <p class="muted" style="margin:-4px 0 11px">함께 있지 않았어도 갈등·연락·기억 등으로 관련된 사람을 고를 수 있습니다. 이름은 저장하지 않습니다.</p>\n      <div class="opts" id="ur-with"></div>',
    label='urge relationship question'
)
rep(
    "btn.textContent=urgeTrackOpen?'상황·촉발 기록 접기':('상황·촉발 기록 (선택)'+(n?' · '+n+'개 임시저장됨':' · 눌러서 기록'));",
    "btn.textContent=urgeTrackOpen?'지금 상황 남기기 접기':('지금 상황 남기기 (선택)'+(n?' · '+n+'개 임시저장됨':' · 관계·장소·촉발'));",
    label='urge toggle JS'
)
rep("company:String(d.with||'')", "company:relationLabel(String(d.with||''))", label='draft relation normalize')

# Urge diary uses the same relationship classification.
rep(
    "function urgeDiaryWith(u){ return String((u&&u.with)||urgeLegacyWith(u)||''); }",
    "function urgeDiaryWith(u){ return relationLabel(String((u&&u.with)||urgeLegacyWith(u)||'')); }",
    label='urgeDiaryWith'
)
rep(
    "if(loc) parts.push(loc); if(who) parts.push(who); if(trg.length) parts.push(trg.slice(0,2).join('·'));",
    "if(who) parts.push(who); if(loc) parts.push(loc); if(trg.length) parts.push(trg.slice(0,2).join('·'));",
    label='urge diary summary order'
)
rep(
    "if(who) rows.push('<div class=\"sp\" style=\"padding:5px 0\"><span>함께</span><b>'+esc(who)+'</b></div>');",
    "if(who) rows.push('<div class=\"sp\" style=\"padding:5px 0\"><span>관계</span><b>'+esc(who)+'</b></div>');",
    label='urge diary record relationship label'
)
rep(
    "<div class=\"sep\"></div><h3>누구와 있었나요?</h3><div class=\"opts\" id=\"ud-with\">'+urgeEditorChips(URGE_COMPANY,st.with,'data-ud-with',false)+'</div><div class=\"sep\"></div><h3>무엇이 촉발했나요?</h3>",
    "<div class=\"sep\"></div><h3>그때 누구와 관련이 있었나요? <span class=\"tiny\" style=\"font-weight:400\">(선택)</span></h3><p class=\"muted\" style=\"margin:-4px 0 11px\">함께 있지 않았어도 갈등·연락·기억 등으로 관련된 사람을 고를 수 있습니다. 이름은 저장하지 않습니다.</p><div class=\"opts\" id=\"ud-with\">'+urgeEditorChips(URGE_COMPANY,st.with,'data-ud-with',false)+'</div><div class=\"sep\"></div><h3>무엇이 촉발했나요?</h3>",
    label='urge diary editor relationship question'
)

# Relapse UI: add the same optional single-select relationship field.
rep(
    "  <div class=\"card\">\n    <h3>그때 어떤 상태였나요?</h3>\n    <div class=\"halt\" id=\"rl-halt\"></div>\n  </div>\n\n  <!-- 재발 뒤의 감정.",
    "  <div class=\"card\">\n    <h3>그때 어떤 상태였나요?</h3>\n    <div class=\"halt\" id=\"rl-halt\"></div>\n  </div>\n\n  <div class=\"card\">\n    <h3>그때 누구와 관련이 있었나요? <span class=\"tiny\" style=\"font-weight:400\">(선택)</span></h3>\n    <p class=\"muted\" style=\"margin:-4px 0 11px\">함께 있지 않았어도 갈등·연락·기억 등으로 관련된 사람을 고를 수 있습니다. 이름은 저장하지 않습니다.</p>\n    <div class=\"opts\" id=\"rl-with\"></div>\n  </div>\n\n  <!-- 재발 뒤의 감정.",
    label='relapse relationship card'
)
rep("let rl = { type: null, halt: [], when: 'today' };", "let rl = { type: null, halt: [], with: '', when: 'today' };", label='rl state')
rep("rl = { type: S.types[0] || 'etc', halt: [], feel: [], when: 'today' };", "rl = { type: S.types[0] || 'etc', halt: [], feel: [], with: '', when: 'today' };", label='rl reset')

# Insert relationship button binding after HALT controls and before feeling rendering helper.
sub(
    r"(function drawRelapse\(\)\{.*?const hb = \$\('#rl-halt'\); hb\.innerHTML = '';.*?HALT\.forEach\(x => \{.*?\n  \}\);)(\n  drawRlFeel\(\);)",
    r"\1\n  const rw = $('#rl-with'); rw.innerHTML = '';\n  URGE_COMPANY.forEach(x => {\n    const b = el('button', 'opt' + (rl.with === x ? ' on' : ''), x);\n    b.onclick = () => { rl.with = rl.with === x ? '' : x; [...rw.children].forEach(c => c.classList.remove('on')); if(rl.with) b.classList.add('on'); };\n    rw.appendChild(b);\n  });\2",
    label='relapse relationship binding'
)

rep(
    "S.relapses.push({ t: Date.now(), type: k, halt: rl.halt.slice(),\n                    f: rl.feel.slice(),",
    "S.relapses.push({ t: Date.now(), type: k, halt: rl.halt.slice(),\n                    f: rl.feel.slice(), with: rl.with || '',",
    label='relapse save relationship'
)

# Show relationship in both trail lists.
rep(
    "(u.th && u.th.length ? '<p>\"' + u.th.map(esc).join('\", \"') + '\"</p>' : '') +\n      '</div>';",
    "(u.th && u.th.length ? '<p>\"' + u.th.map(esc).join('\", \"') + '\"</p>' : '') +\n      (urgeDiaryWith(u) ? '<p>관계: ' + esc(urgeDiaryWith(u)) + '</p>' : '') +\n      '</div>';",
    label='recUrge relationship'
)
rep(
    "const fs = (r.f || []).map(k => (RFEEL.find(x => x.k === k) || {}).l).filter(Boolean).join(' · ');\n    const i = el('div', 'item');",
    "const fs = (r.f || []).map(k => (RFEEL.find(x => x.k === k) || {}).l).filter(Boolean).join(' · ');\n    const rel = relationLabel(r.with);\n    const i = el('div', 'item');",
    label='recRelapse rel var'
)
rep(
    "(fs ? '<p>그때 마음: ' + esc(fs) + '</p>' : '') +\n      (r.days != null ? '<p>' + r.days + '일 지키신 뒤였습니다</p>' : '') +",
    "(fs ? '<p>그때 마음: ' + esc(fs) + '</p>' : '') +\n      (rel ? '<p>관계: ' + esc(rel) + '</p>' : '') +\n      (r.days != null ? '<p>' + r.days + '일 지키신 뒤였습니다</p>' : '') +",
    label='recRelapse relationship display'
)

# Pattern analysis: use relationship as a non-causal context axis.
rep(
    "  const relapses=(S.relapses||[]).filter(r=>r&&Number.isFinite(+r.t));\n  const urgeDays=",
    "  const relapses=(S.relapses||[]).filter(r=>r&&Number.isFinite(+r.t));\n  const recentRelapses=(S.relapses||[]).filter(timed);\n  const urgeDays=",
    label='recent relapses'
)

relationship_block = r'''  const urgeRelRows=urges.filter(r=>relationLabel(r.with));
  if(urgeRelRows.length>=3){
    const relCounts={};
    urgeRelRows.forEach(r=>{ const rel=relationLabel(r.with); relCounts[rel]=(relCounts[rel]||0)+1; });
    const relRank=Object.entries(relCounts).map(([k,n])=>({k,n})).sort((a,b)=>b.n-a.n);
    if(relRank.length&&relRank[0].n>=2&&relRank[0].n/urgeRelRows.length>=0.4){
      const top=relRank[0];
      add('관계 · 충동에서 반복된 맥락', '최근 90일 관계를 기록한 충동 '+urgeRelRows.length+'건 중 '+top.n+'건('+Math.round(top.n/urgeRelRows.length*100)+'%)에서 '+top.k+'을 선택했습니다.');
    }

    const pairCounts={};
    urgeRelRows.forEach(r=>{
      const rel=relationLabel(r.with);
      new Set(Array.isArray(r.trg)?r.trg:[]).forEach(trg=>{ if(trg) pairCounts[rel+'\u0001'+trg]=(pairCounts[rel+'\u0001'+trg]||0)+1; });
    });
    const pairRank=Object.entries(pairCounts).map(([k,n])=>{ const [rel,trg]=k.split('\u0001'); return {rel,trg,n}; }).sort((a,b)=>b.n-a.n);
    if(pairRank.length&&pairRank[0].n>=2){
      const top=pairRank[0], total=relCounts[top.rel]||0;
      if(total>=2&&top.n/total>=0.5) add('관계 · 함께 기록된 촉발', top.rel+'이 선택된 충동 '+total+'건 중 '+top.n+'건에서 '+top.trg+'도 함께 선택했습니다.');
    }

    const feelCounts={};
    urgeRelRows.forEach(r=>{
      const rel=relationLabel(r.with);
      new Set(Array.isArray(r.feel)?r.feel:[]).forEach(feel=>{ if(feel) feelCounts[rel+'\u0001'+feel]=(feelCounts[rel+'\u0001'+feel]||0)+1; });
    });
    const feelRank=Object.entries(feelCounts).map(([k,n])=>{ const [rel,feel]=k.split('\u0001'); return {rel,feel,n}; }).sort((a,b)=>b.n-a.n);
    if(feelRank.length&&feelRank[0].n>=2){
      const top=feelRank[0], total=relCounts[top.rel]||0;
      if(total>=2&&top.n/total>=0.5) add('관계 · 함께 기록된 감정', top.rel+'이 선택된 충동 '+total+'건 중 '+top.n+'건에서 '+top.feel+'도 함께 기록되었습니다.');
    }

    const haltByDay={};
    halts.forEach(r=>{ const d=dayKey(r.t); if(!d) return; if(!haltByDay[d]) haltByDay[d]=new Set(); (Array.isArray(r.v)?r.v:[]).forEach(k=>haltByDay[d].add(k)); });
    const relHaltDays={};
    urgeRelRows.forEach(r=>{
      const rel=relationLabel(r.with), d=dayKey(r.t); if(!rel||!d||!haltByDay[d]) return;
      haltByDay[d].forEach(k=>{ const key=rel+'\u0001'+k; if(!relHaltDays[key]) relHaltDays[key]=new Set(); relHaltDays[key].add(d); });
    });
    const haltRank=Object.entries(relHaltDays).map(([k,set])=>{ const [rel,halt]=k.split('\u0001'); return {rel,halt,n:set.size}; }).sort((a,b)=>b.n-a.n);
    if(haltRank.length&&haltRank[0].n>=2){
      const top=haltRank[0], meta=HALTS.find(x=>x.k===top.halt);
      add('관계 · 같은 날 반복된 HALT', top.rel+'이 선택된 충동이 있었던 날 중 '+top.n+'일에서 '+(meta?meta.l:top.halt)+'도 같은 날 기록되었습니다.');
    }
  }

  const recentRelCounts={};
  recentRelapses.forEach(r=>{ const rel=relationLabel(r.with); if(rel) recentRelCounts[rel]=(recentRelCounts[rel]||0)+1; });
  if(urgeRelRows.length>=2&&Object.keys(recentRelCounts).length){
    const urgeCounts={}; urgeRelRows.forEach(r=>{ const rel=relationLabel(r.with); urgeCounts[rel]=(urgeCounts[rel]||0)+1; });
    const shared=Object.keys(urgeCounts).filter(rel=>urgeCounts[rel]>=2&&(recentRelCounts[rel]||0)>=2).sort((a,b)=>(urgeCounts[b]+recentRelCounts[b])-(urgeCounts[a]+recentRelCounts[a]));
    if(shared.length){
      const rel=shared[0];
      add('관계 · 충동과 다시 시작에 함께 나타난 맥락', '최근 90일 기록에서 '+rel+'이 충동 '+urgeCounts[rel]+'건과 다시 시작 '+recentRelCounts[rel]+'회에 모두 반복해서 선택되었습니다. 특정 사람이 원인이라는 뜻은 아닙니다.');
    }
  }

'''
rep("  const relapseGroups={};\n", relationship_block + "  const relapseGroups={};\n", label='relationship pattern block')

# Per recovery area, report repeated relationship on recent relapse records only.
rep(
    "  Object.entries(relapseGroups).forEach(([type,rows])=>{\n    const label=(typeOf(type)||{}).n||'회복';\n    const withDays=",
    "  Object.entries(relapseGroups).forEach(([type,rows])=>{\n    const label=(typeOf(type)||{}).n||'회복';\n    const recentRows=rows.filter(timed), relationRows=recentRows.filter(r=>relationLabel(r.with));\n    if(relationRows.length>=2){\n      const counts={}; relationRows.forEach(r=>{ const rel=relationLabel(r.with); counts[rel]=(counts[rel]||0)+1; });\n      const ranked=Object.entries(counts).map(([k,n])=>({k,n})).sort((a,b)=>b.n-a.n);\n      if(ranked.length&&ranked[0].n>=2){ const top=ranked[0]; add(label+' · 다시 시작 때 반복된 관계', '최근 90일 '+label+' 다시 시작 중 관계를 기록한 '+relationRows.length+'회 가운데 '+top.n+'회에서 '+top.k+'을 선택했습니다.'); }\n    }\n    const withDays=",
    label='relapse area relationship pattern'
)

rep(
    "최근 90일의 기기 내 기록을 서로 연결해 반복된 사실만 보여드립니다. 진단·위험도 점수·재발 예측이 아니며, 자가점검 점수는 이 계산에 섞지 않습니다. 다시 시작 전 회복기간은 저장된 전체 다시 시작 기록을 참고합니다.",
    "최근 90일의 기기 내 기록을 서로 연결해 반복된 사실만 보여드립니다. 관계 항목도 함께 기록되었다는 맥락만 보여주며 특정 사람이 원인이라고 판단하지 않습니다. 진단·위험도 점수·재발 예측이 아니며, 자가점검 점수는 이 계산에 섞지 않습니다. 다시 시작 전 회복기간은 저장된 전체 다시 시작 기록을 참고합니다.",
    label='pattern safety note'
)

# Help text: mention relationship patterns without changing the menu structure.
rep(
    "내 회복 패턴은 최근 90일 기기 기록에서 반복된 사실을 설명할 뿐 진단·재발예측이 아니며, 자가점검 점수를 다른 기록과 합쳐 위험점수로 만들지 않습니다.",
    "내 회복 패턴은 최근 90일 기기 기록에서 시간·HALT·감정·수면·회복 실천·관계처럼 반복된 사실을 설명할 뿐 진단·재발예측이 아니며, 특정 사람을 원인으로 판단하거나 자가점검 점수를 다른 기록과 합쳐 위험점수로 만들지 않습니다.",
    count=1,
    label='FAQ pattern relationship'
)

idx.write_text(s, encoding='utf-8')

# Other visible version surfaces.
sw = root / 'sw.js'
t = sw.read_text(encoding='utf-8')
if t.count("const APP_VERSION = 'V8.3';") != 1 or t.count("const V = 'ohg-v830-recovery-patterns';") != 1:
    raise SystemExit('sw version anchors not found')
t = t.replace("const APP_VERSION = 'V8.3';", "const APP_VERSION = 'V8.4';", 1)
t = t.replace("const V = 'ohg-v830-recovery-patterns';", "const V = 'ohg-v840-relationship-context';", 1)
sw.write_text(t, encoding='utf-8')

for name in ('privacy.html','legal.html'):
    p=root/name; t=p.read_text(encoding='utf-8')
    if t.count('>V8.3</span>') != 1:
        raise SystemExit(f'{name}: version badge anchor not found')
    p.write_text(t.replace('>V8.3</span>','>V8.4</span>',1),encoding='utf-8')

readme=root/'README.md'
r=readme.read_text(encoding='utf-8')
notes="""## V8.4 — 관계 맥락 · 회복 패턴 연결
- 충동 대응의 기존 순서 `충동 강도 → 어떤 생각이 드나요? → 5분만 같이 버텨보기 → 지금 상황 남기기`는 유지하고, 선택 기록의 관계 항목을 `그때 누구와 관련이 있었나요?`로 명확히 했습니다.
- 관계 분류를 `혼자 / 배우자·연인 / 가족 / 친구 / 직장·학교 사람 / 과거 중독 관련 관계 / 회복 동료·자조모임 사람 / 그 밖의 사람` 8종으로 통일하고 충동일기와 다시 시작에서 같은 단일선택을 사용합니다. 실명은 저장하지 않습니다.
- `내 회복 패턴`은 관계 자체의 반복, 관계와 촉발·감정·같은 날 HALT, 회복영역별 다시 시작 관계를 사실 수준에서 보여줍니다. 관계가 함께 기록되었다는 뜻일 뿐 특정 사람이 재발의 원인이라고 판단하지 않습니다.
- `DATA_SCHEMA=6`, 저장키 `ohg.v1`, 자가점검 채점과 Android 정확알림·화면 OFF·부팅 재예약·복약/외래/생활/습관 알림·마음프로 TTS·이완 TTS 엔진은 변경하지 않습니다.

"""
if r.startswith('## V8.4 —'):
    raise SystemExit('README already V8.4')
readme.write_text(notes+r,encoding='utf-8')

print('V8.4 relationship context patch applied')
