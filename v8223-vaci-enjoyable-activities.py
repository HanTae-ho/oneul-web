from pathlib import Path

idx=Path('index.html')
s=idx.read_text(encoding='utf-8')

old="""const BUILD = 'V8.2.22';"""
new="""const BUILD = 'V8.2.23';"""
assert s.count(old)==1, s.count(old)
s=s.replace(old,new,1)

old="""<!-- ══════════ SMART Recovery · VACI V8.2.22 ══════════ -->"""
new="""<!-- ══════════ SMART Recovery · VACI V8.2.23 ══════════ -->"""
assert s.count(old)==1, s.count(old)
s=s.replace(old,new,1)

old="""    중독행동이 차지하던 시간과 즐거움의 자리에 <b>건강하게 몰입할 수 있는 관심사</b>를 다시 찾아봅니다. 해보고 싶은 활동을 적고 <b>시도 전 1~10점</b>으로 관심도를 표시한 뒤, 실제로 해본 후 <b>시도 후 점수와 생각</b>을 다시 기록합니다. 한 가지 활동이 또 다른 과도한 몰입이 되지 않도록 균형 있게 시도해보세요. 내용은 <b>이 기기에만 저장</b>됩니다."""
new="""    중독행동이 차지하던 시간과 즐거움의 자리에 <b>건강하게 몰입할 수 있는 관심사</b>를 다시 찾아봅니다. 활동이 잘 떠오르지 않으면 <b>즐거운 활동 아이디어</b>에서 몇 가지를 골라 VACI에 바로 추가할 수 있습니다. 해보고 싶은 활동을 <b>시도 전 1~10점</b>으로 표시한 뒤 실제로 해본 후 <b>시도 후 점수와 생각</b>을 다시 기록합니다. 한 가지 활동이 또 다른 과도한 몰입이 되지 않도록 균형 있게 시도해보세요. 내용은 <b>이 기기에만 저장</b>됩니다."""
assert s.count(old)==1, s.count(old)
s=s.replace(old,new,1)

needle="""function smartVaciScoreSelect(kind,value,optional){let h='<select data-vaci-'+kind+'><option value=\"\">'+(optional?'해본 뒤 선택':'점수 선택')+'</option>';for(let i=1;i<=10;i++)h+='<option value=\"'+i+'\"'+(Number(value)===i?' selected':'')+'>'+i+'</option>';return h+'</select>';}
"""
assert s.count(needle)==1, s.count(needle)
insert=r'''function smartVaciScoreSelect(kind,value,optional){let h='<select data-vaci-'+kind+'><option value="">'+(optional?'해본 뒤 선택':'점수 선택')+'</option>';for(let i=1;i<=10;i++)h+='<option value="'+i+'"'+(Number(value)===i?' selected':'')+'>'+i+'</option>';return h+'</select>';}
const SMART_VACI_IDEA_GROUPS=[
 {name:'사회적인',items:['친구에게 전화하기','커피를 마시러 나가기','외식하기','가족과 함께 시간 보내기','사교 모임·클럽 참여하기','친구를 식사에 초대하기']},
 {name:'창의적인',items:['글쓰기','그림 그리기','만화 그리기','식사 준비·요리하기','방 꾸미기','악기 배우기','바느질·뜨개질','사진 찍기']},
 {name:'교육적인',items:['박물관·미술관 방문하기','강좌에 등록하기','새로운 취미 시작하기','아쿠아리움 방문하기','외국어 배우기','십자말풀이·퍼즐 하기','도서관 방문하기']},
 {name:'하고 싶은대로 하기',items:['따뜻한 물에서 휴식하기','햇빛을 받으며 쉬기','마사지 받기','사우나·스파에서 휴식하기','미용실 가기','좋아하는 식사 준비하기','낮잠 자기']},
 {name:'레크리에이션',items:['책 읽기','산책하기','보드게임 하기','음악 듣기','영화 보기','조깅하기','정원 가꾸기','수영하기','운동하기','스포츠 경기 관람하기','댄스 배우기','관심 있는 장소 방문하기','해변·공원·시골 가기']}
];
function smartVaciIdeasHtml(){
 return '<details class="card tight" id="vaci-ideas" style="margin-bottom:12px"><summary style="cursor:pointer;font-weight:700">즐거운 활동 아이디어 보기</summary>'
  +'<p class="muted" style="margin:9px 0 12px">무엇을 해볼지 잘 떠오르지 않을 때 참고하세요. 마음이 가는 활동을 여러 개 고른 뒤 VACI에 추가할 수 있습니다.</p>'
  +SMART_VACI_IDEA_GROUPS.map((g,gi)=>'<div style="margin-top:'+(gi?'13':'4')+'px"><b>'+esc(g.name)+'</b><div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;margin-top:7px">'+g.items.map(name=>'<label class="card tight" style="display:flex;gap:8px;align-items:flex-start;margin:0;padding:9px;cursor:pointer"><input type="checkbox" data-vaci-idea value="'+esc(name)+'" style="width:auto;margin:3px 0 0;flex:0 0 auto"><span style="min-width:0">'+esc(name)+'</span></label>').join('')+'</div></div>').join('')
  +'<button class="btn sec" type="button" id="vaci-ideas-add" style="margin-top:14px">선택한 활동 VACI에 추가</button>'
  +'<p class="tiny" style="margin:8px 0 0">목록에 없는 활동은 아래의 ‘+ 관심사 추가’에서 직접 적을 수 있습니다.</p></details>';
}
'''
s=s.replace(needle,insert,1)

old=""" modal('<h2>'+(record?'VACI 목록 수정':'VACI 관심사 찾기')+'</h2><p class=\"muted\" style=\"margin:5px 0 10px\">어렸을 때 좋아했던 것, 미뤄둔 꿈, 예전에 즐겼지만 멈춘 활동, 새로 배우고 싶은 것을 떠올려보세요. <b>시도 전 점수만 먼저 저장</b>해두고 실제로 해본 뒤 다시 수정해도 됩니다.</p><div class=\"note\" style=\"margin-bottom:12px\">한 가지 활동으로 삶 전체를 채우기보다 여러 관심사를 탐색하고 균형 있게 시도합니다.</div><div id=\"vaci-items\"></div><button class=\"btn sec\" type=\"button\" id=\"vaci-add\">+ 관심사 추가</button><div style=\"height:10px\"></div><button class=\"btn\" id=\"vaci-save\">'+(record?'수정 저장':'VACI 목록 저장')+'</button><div style=\"height:8px\"></div><button class=\"btn ghost\" onclick=\"closeModal()\">취소</button>');"""
new=""" modal('<h2>'+(record?'VACI 목록 수정':'VACI 관심사 찾기')+'</h2><p class=\"muted\" style=\"margin:5px 0 10px\">어렸을 때 좋아했던 것, 미뤄둔 꿈, 예전에 즐겼지만 멈춘 활동, 새로 배우고 싶은 것을 떠올려보세요. <b>시도 전 점수만 먼저 저장</b>해두고 실제로 해본 뒤 다시 수정해도 됩니다.</p><div class=\"note\" style=\"margin-bottom:12px\">한 가지 활동으로 삶 전체를 채우기보다 여러 관심사를 탐색하고 균형 있게 시도합니다.</div>'+smartVaciIdeasHtml()+'<div id=\"vaci-items\"></div><button class=\"btn sec\" type=\"button\" id=\"vaci-add\">+ 관심사 추가</button><div style=\"height:10px\"></div><button class=\"btn\" id=\"vaci-save\">'+(record?'수정 저장':'VACI 목록 저장')+'</button><div style=\"height:8px\"></div><button class=\"btn ghost\" onclick=\"closeModal()\">취소</button>');"""
assert s.count(old)==1, s.count(old)
s=s.replace(old,new,1)

needle=""" render(0);
 $('#vaci-add').onclick=()=>{collect();if(items.length>=12){toast('관심사는 한 목록에 12개까지 추가할 수 있습니다.');return;}items.push({id:'vi-'+Date.now()+'-'+Math.random().toString(36).slice(2,6),name:'',before:null,after:null,note:''});render(items.length-1);setTimeout(()=>{const rows=$$('#vaci-items [data-vaci-item]');if(rows.length)rows[rows.length-1].scrollIntoView({behavior:'smooth',block:'center'});},30);};
"""
assert s.count(needle)==1, s.count(needle)
replace=""" render(0);
 const ideasAdd=$('#vaci-ideas-add');
 if(ideasAdd)ideasAdd.onclick=()=>{collect();const picked=$$('#vaci-ideas [data-vaci-idea]:checked').map(x=>String(x.value||'').trim()).filter(Boolean);if(!picked.length){toast('추가할 활동을 선택해주세요.');return;}items=items.filter(x=>x.name||x.before!=null||x.after!=null||x.note);const existing=new Set(items.map(x=>String(x.name||'').trim()).filter(Boolean));const fresh=picked.filter(n=>!existing.has(n));if(!fresh.length){toast('선택한 활동이 이미 VACI에 있습니다.');return;}const room=Math.max(0,12-items.length);if(!room){toast('관심사는 한 목록에 12개까지 추가할 수 있습니다.');return;}const added=fresh.slice(0,room);added.forEach(name=>items.push({id:'vi-'+Date.now()+'-'+Math.random().toString(36).slice(2,6),name,before:null,after:null,note:''}));$$('#vaci-ideas [data-vaci-idea]:checked').forEach(x=>x.checked=false);render(items.length-1);toast(added.length+'개 활동을 VACI에 추가했습니다.'+(fresh.length>added.length?' 나머지는 다음 목록에서 추가해주세요.':''));setTimeout(()=>{const rows=$$('#vaci-items [data-vaci-item]');if(rows.length)rows[rows.length-1].scrollIntoView({behavior:'smooth',block:'center'});},30);};
 $('#vaci-add').onclick=()=>{collect();if(items.length>=12){toast('관심사는 한 목록에 12개까지 추가할 수 있습니다.');return;}items.push({id:'vi-'+Date.now()+'-'+Math.random().toString(36).slice(2,6),name:'',before:null,after:null,note:''});render(items.length-1);setTimeout(()=>{const rows=$$('#vaci-items [data-vaci-item]');if(rows.length)rows[rows.length-1].scrollIntoView({behavior:'smooth',block:'center'});},30);};
"""
s=s.replace(needle,replace,1)

idx.write_text(s,encoding='utf-8')

sw=Path('sw.js')
w=sw.read_text(encoding='utf-8')
assert w.count("const APP_VERSION = 'V8.2.22';")==1
assert w.count("const V = 'ohg-v8222-smart-vaci';")==1
w=w.replace("const APP_VERSION = 'V8.2.22';","const APP_VERSION = 'V8.2.23';",1)
w=w.replace("const V = 'ohg-v8222-smart-vaci';","const V = 'ohg-v8223-vaci-enjoyable-activities';",1)
sw.write_text(w,encoding='utf-8')
