from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    s=s.replace(old,new,1)

one("const BUILD = 'V8.2.27';","const BUILD = 'V8.2.28';",'BUILD')
one("const RELAX_TTS_RATE=.88;","const RELAX_TTS_RATE=.80;",'TTS rate')

one('''  <div class="note w hide" id="smart-relax-tts-unsupported" style="margin-bottom:12px">이 기기에서는 음성 안내 기능을 사용할 수 없습니다. 아래 글을 보며 연습할 수 있습니다.</div>''','''  <div class="note hide" id="smart-relax-native-note" style="margin-bottom:12px"><b>Android 앱에서는 화면이 꺼져도 이어집니다.</b><br>가이드 듣기를 누르면 전용 음성 가이드가 열립니다. 한국어 음성 선택과 미리듣기는 그 화면에서 설정하며, 화면은 자연스럽게 꺼져도 안내와 쉼 시간이 계속 진행됩니다.</div>\n  <div class="note w hide" id="smart-relax-tts-unsupported" style="margin-bottom:12px">이 기기에서는 음성 안내 기능을 사용할 수 없습니다. 아래 글을 보며 연습할 수 있습니다.</div>''','native note')

one('''let relaxTts={guide:'',index:0,token:0,timer:0,speaking:false,waiting:false,paused:false,voiceBound:false};\nfunction relaxTtsAvailable(){return !!(window.speechSynthesis&&window.SpeechSynthesisUtterance);}''','''let relaxTts={guide:'',index:0,token:0,timer:0,speaking:false,waiting:false,paused:false,voiceBound:false};\nfunction relaxNativeApp(){try{return sessionStorage.getItem('ohg.native.app')==='1';}catch(e){return false;}}\nfunction relaxNativeOpen(kind){if(!['pmr','visual','meditation'].includes(kind))return;relaxTtsStop(false);location.href='oneul://relax/'+kind;}\nfunction relaxTtsAvailable(){return !!(window.speechSynthesis&&window.SpeechSynthesisUtterance);}''','native helpers')

old=''' const supported=relaxTtsAvailable(),vc=$('#smart-relax-voice-card'),un=$('#smart-relax-tts-unsupported'),sel=$('#smart-relax-voice'),pv=$('#smart-relax-voice-preview'),pp=$('#smart-relax-player-pause'),ps=$('#smart-relax-player-stop');\n if(vc)vc.classList.toggle('hide',!supported);if(un)un.classList.toggle('hide',supported);box.querySelectorAll('[data-relax-guide]').forEach(b=>{b.disabled=!supported;b.onclick=()=>relaxTtsStart(b.dataset.relaxGuide);});\n if(supported){relaxTtsBindVoiceEvent();relaxTtsRenderVoices();if(sel)sel.onchange=()=>{relaxTtsStop(false);relaxTtsSaveVoice(sel.value);relaxTtsRenderVoices();toast('가이드 음성을 저장했습니다.');};if(pv)pv.onclick=relaxTtsPreview;if(pp)pp.onclick=relaxTtsTogglePause;if(ps)ps.onclick=()=>relaxTtsStop(true);}\n if(!relaxTts.guide)relaxTtsPlayer(false,'','');'''
new=''' const native=relaxNativeApp(),supported=relaxTtsAvailable(),vc=$('#smart-relax-voice-card'),nn=$('#smart-relax-native-note'),un=$('#smart-relax-tts-unsupported'),sel=$('#smart-relax-voice'),pv=$('#smart-relax-voice-preview'),pp=$('#smart-relax-player-pause'),ps=$('#smart-relax-player-stop');\n if(vc)vc.classList.toggle('hide',native||!supported);if(nn)nn.classList.toggle('hide',!native);if(un)un.classList.toggle('hide',native||supported);box.querySelectorAll('[data-relax-guide]').forEach(b=>{b.disabled=!native&&!supported;b.onclick=()=>native?relaxNativeOpen(b.dataset.relaxGuide):relaxTtsStart(b.dataset.relaxGuide);});\n if(!native&&supported){relaxTtsBindVoiceEvent();relaxTtsRenderVoices();if(sel)sel.onchange=()=>{relaxTtsStop(false);relaxTtsSaveVoice(sel.value);relaxTtsRenderVoices();toast('가이드 음성을 저장했습니다.');};if(pv)pv.onclick=relaxTtsPreview;if(pp)pp.onclick=relaxTtsTogglePause;if(ps)ps.onclick=()=>relaxTtsStop(true);}\n if(native)relaxTtsStop(false);else if(!relaxTts.guide)relaxTtsPlayer(false,'','');'''
one(old,new,'drawSmartRelax native routing')

p.write_text(s,encoding='utf-8')

p=Path('sw.js')
s=p.read_text(encoding='utf-8')
if s.count("const APP_VERSION = 'V8.2.27';")!=1: raise SystemExit('SW version marker')
s=s.replace("const APP_VERSION = 'V8.2.27';","const APP_VERSION = 'V8.2.28';",1)
if s.count("const V = 'ohg-v8227-relax-tts';")!=1: raise SystemExit('SW cache marker')
s=s.replace("const V = 'ohg-v8227-relax-tts';","const V = 'ohg-v8228-native-relax-tts';",1)
p.write_text(s,encoding='utf-8')
print('V8.2.28 web patch applied')
