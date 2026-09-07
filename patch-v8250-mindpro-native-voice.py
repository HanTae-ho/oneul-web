from pathlib import Path

idx=Path('index.html')
native=Path('native.html')
sw=Path('sw.js')
readme=Path('README.md')
s=idx.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 marker, got {n}')
    s=s.replace(old,new,1)

def replace_function(name,newdef):
    global s
    marker=f'function {name}('
    start=s.find(marker)
    if start<0 or s.find(marker,start+1)>=0:
        raise SystemExit(f'{name}: function marker missing/duplicate')
    brace=s.find('{',start)
    if brace<0: raise SystemExit(f'{name}: opening brace missing')
    depth=0
    end=None
    for i in range(brace,len(s)):
        ch=s[i]
        if ch=='{': depth+=1
        elif ch=='}':
            depth-=1
            if depth==0:
                end=i+1
                break
    if end is None: raise SystemExit(f'{name}: closing brace missing')
    s=s[:start]+newdef+s[end:]

one("const BUILD = 'V8.2.49';","const BUILD = 'V8.2.50';",'BUILD')

replace_function('nativeAndroidApp',r'''function nativeAndroidApp(){
  try{
    if(sessionStorage.getItem('ohg.native.app') === '1') return true;
    const q=new URLSearchParams(location.search || '');
    const h=new URLSearchParams((location.hash || '').replace(/^#/, ''));
    const direct=q.get('native') === '1' || h.get('native') === '1';
    const twaRef=/^android-app:\/\/io\.github\.hantae_ho\.twa(?:\/|$)/i.test(String(document.referrer||''));
    if(direct || twaRef){
      try{ sessionStorage.setItem('ohg.native.app','1'); }catch(e){}
      if(q.get('native') === '1'){
        try{
          const u=new URL(location.href);
          u.searchParams.delete('native');
          history.replaceState(history.state,'',u.pathname+(u.search||'')+(u.hash||''));
        }catch(e){}
      }
      return true;
    }
    return false;
  }catch(e){ return false; }
}''')

one("},4500);","},1500);",'AI guide 1.5s')

replace_function('aiVoiceStop',r'''function aiVoiceStop(){
  if(!nativeAndroidApp()) return;
  aiNativeVoice('stop','');
}''')

replace_function('aiVoiceShouldRead',r'''function aiVoiceShouldRead(){
  if(!nativeAndroidApp()) return false;
  if(ai.voiceMode===1) return true;
  if(ai.voiceMode===-1) return false;
  return !!S.aiAutoRead;
}''')

replace_function('aiVoiceSpeak',r'''function aiVoiceSpeak(text){
  if(!aiVoiceShouldRead()) return;
  const msg=String(text||'').replace(/[*#_>`]/g,' ').replace(/\s+/g,' ').trim();
  if(!msg) return;
  aiNativeVoice('speak',msg);
}''')

replace_function('aiVoiceCommand',r'''function aiVoiceCommand(text){
  const x=String(text||'').replace(/\s+/g,'').replace(/[.!?~]/g,'');
  if(!x || x.length>60) return '';
  if(/그만읽|읽지마|읽지말|읽는거멈|음성멈|음성꺼|소리꺼|말하지마|그만말/.test(x)) return 'off';
  if(/계속읽|자동.*읽|이제부터.*읽|답변.*읽|소리내.*읽/.test(x) || /^(읽어줘|읽어주세요)$/.test(x)) return 'on';
  if(/(음성으로|음성|소리로|소리내서|말로).*(안내|설명|답|읽|말|해줘|해주세요)/.test(x)) return 'on';
  if(/말로(해줘|해주세요|설명해줘|안내해줘|답해줘|말해줘)/.test(x)) return 'on';
  return '';
}''')

# Insert the Android-native voice intent bridge immediately before aiVoiceStop.
bridge=r'''function aiNativeVoice(action,text){
  if(!nativeAndroidApp()) return false;
  try{
    const q=new URLSearchParams();
    q.set('action',action);
    if(text) q.set('text',text);
    const u='intent://mindpro-voice?'+q.toString()+
      '#Intent;scheme=oneul;package=io.github.hantae_ho.twa;end';
    location.href=u;
    return true;
  }catch(e){ return false; }
}
'''
marker='function aiVoiceStop(){'
if s.count(marker)!=1: raise SystemExit('aiVoiceStop insertion marker mismatch')
s=s.replace(marker,bridge+marker,1)

idx.write_text(s,encoding='utf-8')

n=native.read_text(encoding='utf-8')
old="location.replace('./index.html');"
if n.count(old)!=1: raise SystemExit('native redirect marker mismatch')
n=n.replace(old,"location.replace('./index.html?native=1');",1)
native.write_text(n,encoding='utf-8')

w=sw.read_text(encoding='utf-8')
for old,new,label in [
    ("const APP_VERSION = 'V8.2.49';","const APP_VERSION = 'V8.2.50';",'SW APP_VERSION'),
    ("const V = 'ohg-v8249-mindpro-guide-voice';","const V = 'ohg-v8250-mindpro-native-voice';",'SW cache')]:
    if w.count(old)!=1: raise SystemExit(f'{label} marker mismatch')
    w=w.replace(old,new,1)
sw.write_text(w,encoding='utf-8')

r=readme.read_text(encoding='utf-8')
entry='''\n## V8.2.50 — 마음프로 Android 네이티브 음성 연결 보정\n- 마음프로 안내 자동 접힘을 1.5초로 조정했습니다.\n- Android TWA 진입 표식을 보강해 설치 앱에서 마음프로 음성 설정이 안정적으로 표시되게 했습니다.\n- 마음프로 답변 읽기를 브라우저 speechSynthesis가 아닌 Android 네이티브 TTS 브리지로 전환했습니다.\n- “음성으로 안내해줘”, “말로 설명해줘”, “계속 읽어줘”, “자동으로 읽어줘”, “그만 읽어”를 AI 서버 전송 전에 로컬 음성명령으로 처리합니다.\n- 개인 회복기록 자동전송 금지, DATA_SCHEMA=6, ohg.v1, 기존 알림·이완 TTS 구조는 유지합니다.\n'''
if '## V8.2.50 — 마음프로 Android 네이티브 음성 연결 보정' not in r:
    r=entry+r
readme.write_text(r,encoding='utf-8')
