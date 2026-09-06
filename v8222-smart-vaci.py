from pathlib import Path

idx=Path('index.html')
learn=Path('learning-data.js')
sw=Path('sw.js')
s=idx.read_text(encoding='utf-8')
l=learn.read_text(encoding='utf-8')
w=sw.read_text(encoding='utf-8')

def once(text, old, new, label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    return text.replace(old,new,1)

# Version
s=once(s,"const BUILD = 'V8.2.21';","const BUILD = 'V8.2.22';",'index BUILD')
w=once(w,"const APP_VERSION = 'V8.2.21';","const APP_VERSION = 'V8.2.22';",'sw APP_VERSION')
w=once(w,"const V = 'ohg-v8221-smart-return-path';","const V = 'ohg-v8222-smart-vaci';",'sw cache')
l=once(l,'/* 오늘 한 걸음 — 회복학습 데이터 V8.2.21','/* 오늘 한 걸음 — 회복학습 데이터 V8.2.22','learning version')

# Page
page='''<!-- ══════════ SMART Recovery · VACI V8.2.22 ══════════ -->
<section class="pg" id="p-smart-vaci">
  <div class="sp" style="margin-bottom:11px">
    <h1 style="margin:0">VACI · 활력 넘치는 창의적 관심사</h1>
    <button class="tiny" style="color:var(--acc);font-weight:600" data-smart-back onclick="appBack('smart-tools')">← SMART 실천도구</button>
  </div>
  <div class="note" style="margin-bottom:12px">
    중독행동이 차지하던 시간과 즐거움의 자리에 <b>건강하게 몰입할 수 있는 관심사</b>를 다시 찾아봅니다. 해보고 싶은 활동을 적고 <b>시도 전 1~10점</b>으로 관심도를 표시한 뒤, 실제로 해본 후 <b>시도 후 점수와 생각</b>을 다시 기록합니다. 한 가지 활동이 또 다른 과도한 몰입이 되지 않도록 균형 있게 시도해보세요. 내용은 <b>이 기기에만 저장</b>됩니다.
  </div>
  <div id="smart-vaci-role-note"></div>
  <button class="btn sec" id="smart-vaci-new">+ VACI 목록 새로 작성하기</button>
  <div id="smart-vaci-list" style="margin-top:12px"></div>
</section>

'''
s=once(s,'<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->',page+'<!-- ══════════ 미래의 나에게 V8.2.0 ══════════ -->','VACI page')

# Routing
s=once(s,"p === 'smart-problem-solving' || p === 'smart-balance-pie' || p === 'smart-tools'","p === 'smart-problem-solving' || p === 'smart-balance-pie' || p === 'smart-vaci' || p === 'smart-tools'",'tab route')
s=once(s,"  if(p === 'smart-balance-pie') drawSmartBalancePie();\n  if(p === 'smart-tools') drawSmartTools();","  if(p === 'smart-balance-pie') drawSmartBalancePie();\n  if(p === 'smart-vaci') drawSmartVaci();\n  if(p === 'smart-tools') drawSmartTools();",'draw route')

# Back labels
s=once(s,"    'smart-balance-pie':'라이프스타일 밸런스 파이'","    'smart-balance-pie':'라이프스타일 밸런스 파이',\n    'smart-vaci':'VACI · 활력 넘치는 창의적 관심사'",'back label')
s=once(s,"'smart-problem-solving':'smart-problem-solving', 'smart-balance-pie':'smart-balance-pie'","'smart-problem-solving':'smart-problem-solving', 'smart-balance-pie':'smart-balance-pie', 'smart-vaci':'smart-vaci'",'back fallback')

# Point 4 hub
old="h+='<div class=\"card\"><h3>Point 4 · 균형 잡힌 삶 살기</h3><p class=\"muted\" style=\"margin:-4px 0 11px\">삶의 여러 영역을 살펴보고, 가치에 맞는 활동과 목표로 균형을 만들어갑니다.</p>'+smartToolButton('라이프스타일 밸런스 파이','삶의 영역별 만족도 0~10 → 먼저 돌볼 영역과 작은 변화 찾기','smart-balance-pie','sprout')+'</div>';"
new="h+='<div class=\"card\"><h3>Point 4 · 균형 잡힌 삶 살기</h3><p class=\"muted\" style=\"margin:-4px 0 11px\">삶의 여러 영역을 살펴보고, 가치에 맞는 활동과 목표로 균형을 만들어갑니다.</p>'+smartToolButton('라이프스타일 밸런스 파이','삶의 영역별 만족도 0~10 → 먼저 돌볼 영역과 작은 변화 찾기','smart-balance-pie','sprout')+smartToolButton('VACI · 활력 넘치는 창의적 관심사','새 활동 → 시도 전 점수 → 시도 후 점수와 생각 정리','smart-vaci','sprout')+'</div>';"
s=once(s,old,new,'Point 4 hub')

# VACI implementation
impl=r'''/* ── SMART Recovery · VACI V8.2.22 ──
   Point 4의 Vital Absorbing Creative Interests: 관심 있는 새 활동을 목록으로 만들고
   시도 전 1~10점, 시도 후 1~10점, 활동 후 생각을 비교해 봅니다. */
function smartVaciRecords(){return (Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(r=>r&&r.kind==='vaci'&&(r.role||'self')===(famMode()?'family':'self')).sort((a,b)=>(b.updatedAt||b.ts||0)-(a.updatedAt||a.ts||0));}
function smartVaciDate(ts){return smartProblemDate(ts);}
function smartVaciScore(v){if(v===''||v==null)return null;v=parseInt(v,10);return Number.isFinite(v)?Math.max(1,Math.min(10,v)):null;}
function smartVaciScoreSelect(kind,value,optional){let h='<select data-vaci-'+kind+'><option value="">'+(optional?'해본 뒤 선택':'점수 선택')+'</option>';for(let i=1;i<=10;i++)h+='<option value="'+i+'"'+(Number(value)===i?' selected':'')+'>'+i+'</option>';return h+'</select>';}
function smartVaciItemHtml(it,i,open,total){
 const title=String(it.name||'').trim()||('관심사 '+(i+1));
 const score=(it.after!=null?(' · '+(it.before||'-')+' → '+it.after):(it.before!=null?(' · 시도 전 '+it.before):''));
 return '<div class="acc'+(open?' on':'')+'" data-vaci-item data-vaci-id="'+esc(it.id||('vi-'+Date.now()+'-'+i))+'">'
  +'<button class="acc-h" type="button" data-vaci-toggle aria-expanded="'+(open?'true':'false')+'"><div class="acc-n"><b>'+(i+1)+' · '+esc(title)+'</b><span>'+esc(score||'새로 해보고 싶은 활동을 적어보세요.')+'</span></div><svg class="acc-v" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg></button>'
  +'<div class="acc-b"><div class="field"><label>새로 시도하거나 다시 시작해보고 싶은 활동</label><input data-vaci-name maxlength="80" placeholder="예: 주말 아침 자전거 타기" value="'+esc(it.name||'')+'"></div>'
  +'<div class="field"><label>시도 전 관심도 <span class="tiny">1~10</span></label>'+smartVaciScoreSelect('before',it.before,false)+'</div>'
  +'<div class="field"><label>시도 후 점수 <span class="tiny">(해본 뒤, 선택)</span></label>'+smartVaciScoreSelect('after',it.after,true)+'</div>'
  +'<div class="field"><label>활동 후 평가 · 생각 정리 <span class="tiny">(선택)</span></label><textarea data-vaci-note maxlength="700" placeholder="실제로 해보니 어땠나요? 다시 하고 싶은가요? 무엇이 달랐나요?">'+esc(it.note||'')+'</textarea></div>'
  +(total>1?'<button class="btn ghost sm" type="button" data-vaci-remove style="margin-top:4px">이 관심사 삭제</button>':'')+'</div></div>';
}
function drawSmartVaci(){
 const list=$('#smart-vaci-list'),rn=$('#smart-vaci-role-note'),add=$('#smart-vaci-new');if(!list||!add)return;
 if(rn)rn.innerHTML=famMode()?'<div class="note" style="margin-bottom:12px"><b>가족도 내 삶의 관심사를 찾습니다.</b><br>상대에게 하게 만들 활동이나 상대를 감시하는 계획이 아니라, 가족 자신의 회복·자기돌봄·관계 밖의 삶을 다시 넓혀가는 관심사를 적습니다.</div>':'';
 add.onclick=()=>openSmartVaciEditor(null);
 const rows=smartVaciRecords();
 if(!rows.length){list.innerHTML='<div class="card"><b>아직 저장한 VACI 목록이 없습니다.</b><p class="muted" style="margin:5px 0 0">어릴 때 좋아했던 것, 미뤄둔 관심사, 새로 해보고 싶었던 활동 하나부터 떠올려보세요.</p></div>';return;}
 list.innerHTML='<div class="card"><h3>저장한 VACI 목록 '+rows.length+'건</h3>'+rows.map(r=>{const items=Array.isArray(r.items)?r.items:[],done=items.filter(x=>x&&x.after!=null).length;return '<div class="sp" style="gap:10px;padding:11px 0;border-top:1px solid var(--line)"><div style="min-width:0;flex:1"><div class="tiny">'+esc(smartVaciDate(r.updatedAt||r.ts))+' · '+items.length+'개 관심사 · 시도 후 기록 '+done+'개</div><b style="display:block;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc((items[0]&&items[0].name)||'VACI 목록')+'</b><div class="muted" style="margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(items.slice(1,4).map(x=>x.name).filter(Boolean).join(' · '))+'</div></div><button class="tiny" style="color:var(--acc);font-weight:600" onclick="openSmartVaciView(\''+esc(r.id)+'\')">보기</button></div>';}).join('')+'</div>';
}
function openSmartVaciEditor(record){
 const r=record||{};let items=Array.isArray(r.items)&&r.items.length?r.items.map(x=>({id:x.id||('vi-'+Date.now()+'-'+Math.random().toString(36).slice(2,6)),name:x.name||'',before:x.before==null?null:smartVaciScore(x.before),after:x.after==null?null:smartVaciScore(x.after),note:x.note||''})):[{id:'vi-'+Date.now(),name:'',before:null,after:null,note:''}];
 modal('<h2>'+(record?'VACI 목록 수정':'VACI 관심사 찾기')+'</h2><p class="muted" style="margin:5px 0 10px">어렸을 때 좋아했던 것, 미뤄둔 꿈, 예전에 즐겼지만 멈춘 활동, 새로 배우고 싶은 것을 떠올려보세요. <b>시도 전 점수만 먼저 저장</b>해두고 실제로 해본 뒤 다시 수정해도 됩니다.</p><div class="note" style="margin-bottom:12px">한 가지 활동으로 삶 전체를 채우기보다 여러 관심사를 탐색하고 균형 있게 시도합니다.</div><div id="vaci-items"></div><button class="btn sec" type="button" id="vaci-add">+ 관심사 추가</button><div style="height:10px"></div><button class="btn" id="vaci-save">'+(record?'수정 저장':'VACI 목록 저장')+'</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">취소</button>');
 const collect=()=>{items=$$('#vaci-items [data-vaci-item]').map(row=>({id:row.dataset.vaciId||('vi-'+Date.now()+'-'+Math.random().toString(36).slice(2,6)),name:(row.querySelector('[data-vaci-name]')?.value||'').trim(),before:smartVaciScore(row.querySelector('[data-vaci-before]')?.value||''),after:smartVaciScore(row.querySelector('[data-vaci-after]')?.value||''),note:(row.querySelector('[data-vaci-note]')?.value||'').trim()}));};
 const render=(openIndex)=>{const box=$('#vaci-items');if(!box)return;box.innerHTML=items.map((x,i)=>smartVaciItemHtml(x,i,i===openIndex,items.length)).join('');box.querySelectorAll('[data-vaci-toggle]').forEach(b=>b.onclick=()=>{const target=b.closest('[data-vaci-item]'),was=target.classList.contains('on');box.querySelectorAll('[data-vaci-item]').forEach(a=>setAcc(a,false));if(!was)setAcc(target,true);});box.querySelectorAll('[data-vaci-remove]').forEach((b,i)=>b.onclick=()=>{collect();if(items.length<=1)return;items.splice(i,1);render(Math.max(0,Math.min(i,items.length-1)));});};
 render(0);
 $('#vaci-add').onclick=()=>{collect();if(items.length>=12){toast('관심사는 한 목록에 12개까지 추가할 수 있습니다.');return;}items.push({id:'vi-'+Date.now()+'-'+Math.random().toString(36).slice(2,6),name:'',before:null,after:null,note:''});render(items.length-1);setTimeout(()=>{const rows=$$('#vaci-items [data-vaci-item]');if(rows.length)rows[rows.length-1].scrollIntoView({behavior:'smooth',block:'center'});},30);};
 $('#vaci-save').onclick=()=>{collect();const used=items.filter(x=>x.name||x.before!=null||x.after!=null||x.note);if(!used.length){toast('관심사를 하나 이상 적어주세요.');return;}const bad=used.findIndex(x=>!x.name||x.before==null);if(bad>=0){render(bad);toast(!used[bad].name?'활동 이름을 적어주세요.':'시도 전 관심도 1~10점을 선택해주세요.');return;}const rec={id:record?record.id:('vaci-'+Date.now()+'-'+Math.random().toString(36).slice(2,7)),kind:'vaci',role:famMode()?'family':'self',ts:record?(record.ts||Date.now()):Date.now(),updatedAt:Date.now(),items:used};if(!Array.isArray(S.smartWorks))S.smartWorks=[];if(record){const i=S.smartWorks.findIndex(x=>x&&x.id===record.id);if(i>=0)S.smartWorks[i]=rec;else S.smartWorks.push(rec);}else S.smartWorks.push(rec);save();closeModal();drawSmartVaci();toast(record?'VACI 목록을 수정했습니다.':'VACI 목록을 저장했습니다.');};
}
function openSmartVaciView(id){
 const r=smartVaciRecords().find(x=>x.id===id);if(!r)return;const items=Array.isArray(r.items)?r.items:[];
 const h=items.map((x,i)=>'<details class="card tight"><summary style="cursor:pointer;font-weight:700">'+(i+1)+' · '+esc(x.name||'관심사')+' <span class="tiny" style="font-weight:400">'+(x.before!=null?('시도 전 '+x.before):'')+(x.after!=null?(' → 시도 후 '+x.after):'')+'</span></summary><div style="margin-top:10px"><div><b>시도 전 관심도</b><br>'+(x.before==null?'<span class="muted">작성하지 않음</span>':esc(String(x.before))+' / 10')+'</div><div style="margin-top:9px"><b>시도 후 점수</b><br>'+(x.after==null?'<span class="muted">아직 기록하지 않음</span>':esc(String(x.after))+' / 10')+'</div><div style="margin-top:9px"><b>활동 후 평가 · 생각 정리</b><br>'+(String(x.note||'').trim()?'<span style="white-space:pre-wrap">'+esc(x.note)+'</span>':'<span class="muted">아직 기록하지 않음</span>')+'</div></div></details>').join('');
 modal('<h2>VACI · 활력 넘치는 창의적 관심사</h2><div class="muted" style="margin:-4px 0 12px">'+esc(smartVaciDate(r.updatedAt||r.ts))+'</div>'+h+'<button class="btn sec" id="vaci-edit">수정 · 시도 후 기록 추가</button><div style="height:8px"></div><button class="btn bad" id="vaci-delete">이 VACI 목록 삭제</button><div style="height:8px"></div><button class="btn ghost" onclick="closeModal()">닫기</button>');
 $('#vaci-edit').onclick=()=>openSmartVaciEditor(r);$('#vaci-delete').onclick=()=>{if(!confirm('이 VACI 목록을 삭제할까요?'))return;S.smartWorks=(Array.isArray(S.smartWorks)?S.smartWorks:[]).filter(x=>!(x&&x.id===r.id));save();closeModal();drawSmartVaci();toast('VACI 목록을 삭제했습니다.');};
}

'''
s=once(s,'function learningAction(type,sectionId){',impl+'function learningAction(type,sectionId){','VACI implementation')
s=once(s,"  if(type === 'smart-balance-pie'){ go('smart-balance-pie'); return; }","  if(type === 'smart-balance-pie'){ go('smart-balance-pie'); return; }\n  if(type === 'smart-vaci'){ go('smart-vaci'); return; }",'learning route')

# Point 4 learning action
old='''          {
            "type": "smart-balance-pie",
            "label": "라이프스타일 밸런스 파이 작성하기"
          }
        ]'''
new='''          {
            "type": "smart-balance-pie",
            "label": "라이프스타일 밸런스 파이 작성하기"
          },
          {
            "type": "smart-vaci",
            "label": "VACI 관심사 목록 작성하기"
          }
        ]'''
l=once(l,old,new,'Point 4 learning VACI action')

# User-facing wording policy safeguard
if '번역본' in s or '번역본' in l:
    raise SystemExit('user-facing files contain forbidden wording: 번역본')
if "const DATA_SCHEMA = 6;" not in s:
    raise SystemExit('DATA_SCHEMA changed')

idx.write_text(s,encoding='utf-8')
learn.write_text(l,encoding='utf-8')
sw.write_text(w,encoding='utf-8')
