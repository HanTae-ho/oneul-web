from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    s=s.replace(old,new,1)

one("const BUILD = 'V8.2.28';","const BUILD = 'V8.2.29';",'BUILD')
one('''  <div class="note hide" id="smart-relax-native-note" style="margin-bottom:12px"><b>Android 앱에서는 화면이 꺼져도 이어집니다.</b><br>가이드 듣기를 누르면 전용 음성 가이드가 열립니다. 한국어 음성 선택과 미리듣기는 그 화면에서 설정하며, 화면은 자연스럽게 꺼져도 안내와 쉼 시간이 계속 진행됩니다.</div>\n''','', 'remove duplicate Android note')
one("const native=relaxNativeApp(),supported=relaxTtsAvailable(),vc=$('#smart-relax-voice-card'),nn=$('#smart-relax-native-note'),un=$('#smart-relax-tts-unsupported'),sel=$('#smart-relax-voice'),pv=$('#smart-relax-voice-preview'),pp=$('#smart-relax-player-pause'),ps=$('#smart-relax-player-stop');","const native=relaxNativeApp(),supported=relaxTtsAvailable(),vc=$('#smart-relax-voice-card'),un=$('#smart-relax-tts-unsupported'),sel=$('#smart-relax-voice'),pv=$('#smart-relax-voice-preview'),pp=$('#smart-relax-player-pause'),ps=$('#smart-relax-player-stop');",'remove note reference')
one("if(vc)vc.classList.toggle('hide',native||!supported);if(nn)nn.classList.toggle('hide',!native);if(un)un.classList.toggle('hide',native||supported);box.querySelectorAll('[data-relax-guide]').forEach(b=>{b.disabled=!native&&!supported;b.onclick=()=>native?relaxNativeOpen(b.dataset.relaxGuide):relaxTtsStart(b.dataset.relaxGuide);});","if(vc)vc.classList.toggle('hide',native||!supported);if(un)un.classList.toggle('hide',native||supported);box.querySelectorAll('[data-relax-guide]').forEach(b=>{b.disabled=!native&&!supported;b.onclick=()=>native?relaxNativeOpen(b.dataset.relaxGuide):relaxTtsStart(b.dataset.relaxGuide);});",'remove note toggle')
p.write_text(s,encoding='utf-8')

p=Path('sw.js')
s=p.read_text(encoding='utf-8')
if s.count("const APP_VERSION = 'V8.2.28';")!=1: raise SystemExit('SW version marker')
s=s.replace("const APP_VERSION = 'V8.2.28';","const APP_VERSION = 'V8.2.29';",1)
if s.count("const V = 'ohg-v8228-native-relax-tts';")!=1: raise SystemExit('SW cache marker')
s=s.replace("const V = 'ohg-v8228-native-relax-tts';","const V = 'ohg-v8229-relax-rate';",1)
p.write_text(s,encoding='utf-8')
print('V8.2.29 web patch applied')
