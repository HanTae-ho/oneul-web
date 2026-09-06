from pathlib import Path

idx=Path('index.html')
s=idx.read_text(encoding='utf-8')

s=s.replace("const BUILD = 'V8.2.23';","const BUILD = 'V8.2.24';",1)

old=""" list.innerHTML='<div class=\"card\"><h3>저장한 VACI 목록 '+rows.length+'건</h3>'+rows.map(r=>{const items=Array.isArray(r.items)?r.items:[],done=items.filter(x=>x&&x.after!=null).length;return '<div class=\"sp\" style=\"gap:10px;padding:11px 0;border-top:1px solid var(--line)\"><div style=\"min-width:0;flex:1\"><div class=\"tiny\">'+esc(smartVaciDate(r.updatedAt||r.ts))+' · '+items.length+'개 관심사 · 시도 후 기록 '+done+'개</div><b style=\"display:block;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis\">'+esc((items[0]&&items[0].name)||'VACI 목록')+'</b><div class=\"muted\" style=\"margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis\">'+esc(items.slice(1,4).map(x=>x.name).filter(Boolean).join(' · '))+'</div></div><button class=\"tiny\" style=\"color:var(--acc);font-weight:600\" onclick=\"openSmartVaciView(\\''+esc(r.id)+'\\')\">보기</button></div>';}).join('')+'</div>';"""
new=""" list.innerHTML='<div class=\"card\"><h3>저장한 VACI 목록 '+rows.length+'건</h3>'+rows.map(r=>{const items=Array.isArray(r.items)?r.items:[],done=items.filter(x=>x&&x.after!=null).length,names=items.map(x=>String((x&&x.name)||'').trim()).filter(Boolean);const chips=names.length?'<div style=\"display:flex;flex-wrap:wrap;gap:6px;margin-top:7px\">'+names.map(name=>'<span style=\"display:inline-flex;align-items:center;max-width:100%;padding:4px 9px;border-radius:999px;background:var(--accbg);color:var(--acc);font-size:12px;line-height:1.35\">'+esc(name)+'</span>').join('')+'</div>':'<div class=\"muted\" style=\"margin-top:5px\">관심사 이름 없음</div>';return '<div class=\"sp\" style=\"gap:10px;padding:11px 0;border-top:1px solid var(--line);align-items:flex-start\"><div style=\"min-width:0;flex:1\"><div class=\"tiny\">'+esc(smartVaciDate(r.updatedAt||r.ts))+' · '+items.length+'개 관심사 · 시도 후 기록 '+done+'개</div><div class=\"tiny\" style=\"margin-top:5px;font-weight:600;color:var(--dim)\">선택한 관심사</div>'+chips+'</div><button class=\"tiny\" style=\"color:var(--acc);font-weight:600;flex:0 0 auto\" onclick=\"openSmartVaciView(\\''+esc(r.id)+'\\')\">보기</button></div>';}).join('')+'</div>';"""
if old not in s:
    raise SystemExit('drawSmartVaci target not found')
s=s.replace(old,new,1)

old2="""function openSmartVaciEditor(record){
 const r=record||{};let items=Array.isArray(r.items)&&r.items.length?r.items.map(x=>({id:x.id||('vi-'+Date.now()+'-'+Math.random().toString(36).slice(2,6)),name:x.name||'',before:x.before==null?null:smartVaciScore(x.before),after:x.after==null?null:smartVaciScore(x.after),note:x.note||''})):[{id:'vi-'+Date.now(),name:'',before:null,after:null,note:''}];
"""
new2="""function openSmartVaciEditor(record){
 const r=record||{};let items=Array.isArray(r.items)&&r.items.length?r.items.map(x=>({id:x.id||('vi-'+Date.now()+'-'+Math.random().toString(36).slice(2,6)),name:x.name||'',before:x.before==null?null:smartVaciScore(x.before),after:x.after==null?null:smartVaciScore(x.after),note:x.note||''})):[{id:'vi-'+Date.now(),name:'',before:null,after:null,note:''}];
 const setAcc=(node,on)=>{if(!node)return;node.classList.toggle('on',!!on);const b=Array.from(node.children).find(x=>x.classList&&x.classList.contains('acc-h'));if(b)b.setAttribute('aria-expanded',on?'true':'false');};
"""
if old2 not in s:
    raise SystemExit('VACI editor target not found')
s=s.replace(old2,new2,1)
idx.write_text(s,encoding='utf-8')

sw=Path('sw.js')
t=sw.read_text(encoding='utf-8')
t=t.replace("const APP_VERSION = 'V8.2.23';","const APP_VERSION = 'V8.2.24';",1)
t=t.replace("const V = 'ohg-v8223-vaci-enjoyable-activities';","const V = 'ohg-v8224-vaci-fix-chips';",1)
sw.write_text(t,encoding='utf-8')
