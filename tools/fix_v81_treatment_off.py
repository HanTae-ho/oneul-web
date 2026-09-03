from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""  treatToggle($('#treat-on'),t.on,'사용함','사용하지 않음',v=>{ t.on=v; save(); drawTreatment(); drawHome(); });
  if(!t.on){ body.innerHTML=''; return; }
"""
new="""  treatToggle($('#treat-on'),t.on,'사용함','사용하지 않음',v=>{ t.on=v; save(); drawTreatment(); drawHome(); });
  if(!t.on){
    body.innerHTML='<div class=\"note\"><b>치료관리를 사용하지 않습니다.</b><br><span class=\"muted\">기존 복약·외래 설정과 기록은 보존됩니다.</span>' +
      (nativeAndroidApp() ? '<div style=\"height:9px\"></div><button class=\"btn sec sm\" id=\"treat-sync-off\">Android 예약알림에도 반영</button>' : '') + '</div>';
    const so=$('#treat-sync-off'); if(so) so.onclick=openNativeReminderSettings;
    return;
  }
"""
if s.count(old)!=1: raise SystemExit(f'off-sync anchor count={s.count(old)}')
s=s.replace(old,new,1)
# Static subtitle should match the post-V8.1 structure even before drawMe runs.
s=s.replace('<span class="acc-n"><b>챙기기</b><span id="acc-care-s">위험한 시간대 · 복약 · 식사 · 잠 · 알림</span></span>',
            '<span class="acc-n"><b>챙기기</b><span id="acc-care-s">위험한 시간대 · 식사 · 잠 · 알림</span></span>',1)
p.write_text(s,encoding='utf-8')
print('V8.1 treatment off-sync fix applied')
