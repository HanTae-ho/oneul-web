from pathlib import Path

P = Path('index.html')
s = P.read_text(encoding='utf-8')


def one(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {n}')
    s = s.replace(old, new, 1)

# Version.
one("const BUILD = 'V8.2.48';", "const BUILD = 'V8.2.49';", 'BUILD')

# Persistent Android-only MindPro auto-read preference. Top-level default means no schema bump is needed.
one("  aiChat: [], aiClient: '', aiConsent: 0,       /* AI 대화는 이 기기에만 저장 */\n",
    "  aiChat: [], aiClient: '', aiConsent: 0, aiAutoRead: 0, /* AI 대화·음성 기본설정은 이 기기에만 저장 */\n",
    'BLANK aiAutoRead')

# My settings: Android app only voice default.
old = '''      <div class="opts" id="me-theme">
        <button class="opt" data-theme="light">밝게</button>
        <button class="opt" data-theme="dark">어둡게</button>
      </div>

      <div class="sep"></div>
      <!-- 위의 [지금 새로 받기] 는 '목록' 만, 아래는 '앱 자체' 를 받습니다.'''
new = '''      <div class="opts" id="me-theme">
        <button class="opt" data-theme="light">밝게</button>
        <button class="opt" data-theme="dark">어둡게</button>
      </div>

      <div id="me-ai-voice" class="hide">
        <div class="sep"></div>
        <h3>마음프로 음성</h3>
        <p class="muted" style="margin:-4px 0 11px">
          Android 앱에서 마음프로의 새 답변을 자동으로 읽을지 정합니다. 대화 중 <b>“계속 읽어줘”</b> 또는 <b>“그만 읽어”</b>라고 하면 현재 대화에서는 이 설정보다 그 요청을 우선합니다.
        </p>
        <div class="opts" id="me-ai-auto-read">
          <button class="opt" data-ai-auto-read="0">텍스트만</button>
          <button class="opt" data-ai-auto-read="1">답변 자동 읽기</button>
        </div>
      </div>

      <div class="sep"></div>
      <!-- 위의 [지금 새로 받기] 는 '목록' 만, 아래는 '앱 자체' 를 받습니다.'''
one(old, new, 'My voice setting HTML')

# MindPro: remove blocking consent page. Keep a fixed, auto-folding information bar above the scrolling conversation.
old = '''  <div class="aiscroll" id="ai-scroll">
    <div class="note w" style="margin-bottom:12px">
      마음프로는 치료나 응급상담을 대신하지 않습니다. 생명이 위험하거나 경련·환각·심한 금단이 있으면
      대화보다 <b>119</b>가 먼저입니다. 죽고 싶은 마음이 급하면 <b>109</b>에 바로 연결하세요.
    </div>

    <div class="card" id="ai-consent">
      <h3>마음프로(AI)에서 처리되는 내용</h3>
      <p class="muted" style="margin:-4px 0 11px">
        이 대화창의 요청 중 <b>앱 내부 기능으로 처리할 수 없는 일반 대화만</b> AI 서버로 전송합니다.
        타이머·도움글·모임·센터·병원·헬프콜·기록 화면 같은 앱 기능은 AI에 보내지 않고 바로 처리합니다.
        회복 시작일·충동·재발·HALT·복약·기분 기록은 자동으로 보내지 않습니다.
      </p>
      <p class="tiny">대화 내용은 이 기기에 저장됩니다. 외부 AI API 처리 과정에서는 제공자의 데이터 처리 정책이 적용됩니다.</p>
      <button class="btn sec" id="ai-consent-go">확인하고 시작</button>
    </div>

    <div id="ai-main" class="hide">
      <div class="opts" id="ai-quick"></div>
      <div class="aithread" id="ai-thread"></div>
      <div class="aifollow" id="ai-resource"></div>
      <div style="height:10px"></div>
      <button class="btn ghost sm" id="ai-new">새 대화로 비우기</button>
    </div>
  </div>

  <div class="aidock hide" id="ai-dock">'''
new = '''  <div class="aiguide" id="ai-guide">
    <button class="aiguide-h" id="ai-guide-toggle" type="button" aria-expanded="false">
      <span><b>마음프로 안내</b><small>안전 · 개인정보 · 앱 기능 · 음성</small></span>
      <span class="aiguide-v" aria-hidden="true">+</span>
    </button>
    <div class="aiguide-b">
      <div class="note w" style="margin-bottom:10px">
        마음프로는 치료나 응급상담을 대신하지 않습니다. 생명이 위험하거나 경련·환각·심한 금단이 있으면 <b>119</b>가 먼저입니다. 죽고 싶은 마음이 급하면 <b>109</b>에 바로 연결하세요.
      </div>
      <p class="muted" style="margin:0 0 8px">
        타이머·도움글·모임·센터·병원·알림·앱 메뉴처럼 <b>앱이 직접 처리할 수 있는 요청은 기기에서 먼저 처리</b>합니다. 일반 대화가 필요할 때만 사용자가 직접 적은 문장을 AI 서버로 보냅니다.
      </p>
      <p class="tiny" style="margin:0">회복 시작일·충동·재발·HALT·복약·기분·자가점검 결과 같은 개인 회복기록은 자동 전송하지 않습니다. 대화 내용은 이 기기에 저장됩니다.</p>
      <p class="tiny hide" id="ai-guide-voice" style="margin:8px 0 0"></p>
    </div>
  </div>

  <div class="aiscroll" id="ai-scroll">
    <div id="ai-main">
      <div class="opts" id="ai-quick"></div>
      <div class="aithread" id="ai-thread"></div>
      <div class="aifollow" id="ai-resource"></div>
      <div style="height:10px"></div>
      <button class="btn ghost sm" id="ai-new">새 대화로 비우기</button>
    </div>
  </div>

  <div class="aidock" id="ai-dock">'''
one(old, new, 'MindPro HTML')

# MindPro fixed guide styles.
old = '''  .aihead .name span{display:block;font-size:11.5px;color:var(--dim);margin-top:2px}
  .aiscroll{flex:1;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;'''
new = '''  .aihead .name span{display:block;font-size:11.5px;color:var(--dim);margin-top:2px}
  .aiguide{flex:0 0 auto;margin:8px 3px 0;background:var(--panel);border:1px solid var(--line);border-radius:13px;overflow:hidden}
  .aiguide-h{display:flex;align-items:center;justify-content:space-between;gap:10px;width:100%;padding:9px 12px;text-align:left}
  .aiguide-h>span:first-child{min-width:0;flex:1}
  .aiguide-h b{display:block;font-size:13.5px;line-height:1.3}
  .aiguide-h small{display:block;color:var(--dim);font-size:10.8px;margin-top:2px}
  .aiguide-v{font-size:20px;line-height:1;color:var(--faint)}
  .aiguide-b{display:none;padding:2px 12px 11px}
  .aiguide.on{border-color:var(--acc2)}
  .aiguide.on .aiguide-h b{color:var(--acc)}
  .aiguide.on .aiguide-b{display:block}
  .aiguide.on .aiguide-v{color:var(--acc)}
  .aiscroll{flex:1;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;'''
one(old, new, 'MindPro guide CSS')

# Routing: first MindPro entry of an app session shows the guide briefly; leaving AI stops current speech only.
old = '''  if(prev === 'smart-relax' && p !== 'smart-relax' && typeof relaxTtsStop === 'function') relaxTtsStop(false);
  if(p === 'ai' && prev !== 'ai') ai.actionsOpen = false;
  cur = p;'''
new = '''  if(prev === 'smart-relax' && p !== 'smart-relax' && typeof relaxTtsStop === 'function') relaxTtsStop(false);
  if(prev === 'ai' && p !== 'ai' && typeof aiVoiceStop === 'function') aiVoiceStop();
  if(p === 'ai' && prev !== 'ai'){
    ai.actionsOpen = false;
    if(typeof aiGuideEnter === 'function') aiGuideEnter();
  }
  cur = p;'''
one(old, new, 'AI route entry/exit')

# My settings binding. nativeAndroidApp is a function declaration and can be called here before its textual definition.
old = '''function drawThemeSetting(){
  $$('#me-theme [data-theme]').forEach(b => {
    const k = b.dataset.theme;
    const on = (k === 'dark') ? S.theme === 'dark' : S.theme !== 'dark';
    b.classList.toggle('on', on);
  });
}
$('#me-theme').addEventListener('click', e => {
  const b = e.target.closest('[data-theme]');
  if(!b) return;
  S.theme = b.dataset.theme === 'dark' ? 'dark' : '';
  applyTheme(); save(); drawThemeSetting();
});'''
new = '''function drawThemeSetting(){
  $$('#me-theme [data-theme]').forEach(b => {
    const k = b.dataset.theme;
    const on = (k === 'dark') ? S.theme === 'dark' : S.theme !== 'dark';
    b.classList.toggle('on', on);
  });
}
function drawAiVoiceSetting(){
  const wrap=$('#me-ai-voice');
  if(!wrap) return;
  const android=nativeAndroidApp();
  wrap.classList.toggle('hide', !android);
  if(!android) return;
  $$('#me-ai-auto-read [data-ai-auto-read]').forEach(b=>b.classList.toggle('on', Number(b.dataset.aiAutoRead) === (S.aiAutoRead?1:0)));
}
$('#me-theme').addEventListener('click', e => {
  const b = e.target.closest('[data-theme]');
  if(!b) return;
  S.theme = b.dataset.theme === 'dark' ? 'dark' : '';
  applyTheme(); save(); drawThemeSetting();
});
$('#me-ai-auto-read').addEventListener('click', e=>{
  const b=e.target.closest('[data-ai-auto-read]');
  if(!b || !nativeAndroidApp()) return;
  S.aiAutoRead=Number(b.dataset.aiAutoRead)===1?1:0;
  save();
  if(!S.aiAutoRead && ai.voiceMode!==1) aiVoiceStop();
  drawAiVoiceSetting();
  toast(S.aiAutoRead?'마음프로 답변 자동 읽기를 켰습니다.':'마음프로 답변 자동 읽기를 껐습니다.');
});'''
one(old, new, 'AI voice settings JS')

# drawMe must refresh voice setting too.
one('''function drawMe(){
  const fam = famMode();
  drawThemeSetting();
  drawFeedbackStatus();''', '''function drawMe(){
  const fam = famMode();
  drawThemeSetting();
  drawAiVoiceSetting();
  drawFeedbackStatus();''', 'drawMe voice setting')

# MindPro session state.
one("let ai = { back:'help', busy:false, meetings:[], resources:[], actionsOpen:false, follow:'', timer:null, timerTick:0, read:null, loc:null, activeArea:'', activeAreaSource:'' };",
    "let ai = { back:'help', busy:false, meetings:[], resources:[], actionsOpen:false, follow:'', timer:null, timerTick:0, read:null, loc:null, activeArea:'', activeAreaSource:'', guideOpen:false, guideShown:false, guideTimer:0, voiceMode:0 };",
    'AI state')

# New assistant messages can be spoken only inside the Android package. Ordinary browser/PWA gets no TTS implementation.
old = '''function aiAdd(role, text, local){
  if(!Array.isArray(S.aiChat)) S.aiChat = [];
  const m = { role:role, text:String(text || '').slice(0, 1800), t:Date.now() };
  /* local=1 인 대화는 앱 내부 기능으로 끝난 내용입니다.
     나중에 일반 AI 대화를 보내더라도 이 문장들은 history에 섞어 보내지 않습니다. */
  if(local) m.local = 1;
  S.aiChat.push(m);
  if(S.aiChat.length > 24) S.aiChat = S.aiChat.slice(-24);
  save();
  return m;
}'''
new = '''function aiAdd(role, text, local){
  if(!Array.isArray(S.aiChat)) S.aiChat = [];
  const m = { role:role, text:String(text || '').slice(0, 1800), t:Date.now() };
  /* local=1 인 대화는 앱 내부 기능으로 끝난 내용입니다.
     나중에 일반 AI 대화를 보내더라도 이 문장들은 history에 섞어 보내지 않습니다. */
  if(local) m.local = 1;
  S.aiChat.push(m);
  if(S.aiChat.length > 24) S.aiChat = S.aiChat.slice(-24);
  save();
  if(role === 'assistant') aiVoiceSpeak(m.text);
  return m;
}'''
one(old, new, 'aiAdd voice')

# Guide + Android-only speech support. Keep existing native RelaxTtsActivity untouched.
old = "function openAI(back){ ai.back = back || 'help'; ai.meetings = []; ai.resources = []; ai.actionsOpen = false; ai.follow=''; ai.loc=null; ai.activeArea=''; ai.activeAreaSource=''; go('ai'); }\n\nfunction aiCrisisKind(text){"
new = '''function openAI(back){ ai.back = back || 'help'; ai.meetings = []; ai.resources = []; ai.actionsOpen = false; ai.follow=''; ai.loc=null; ai.activeArea=''; ai.activeAreaSource=''; go('ai'); }

function aiGuideEnter(){
  if(ai.guideTimer){ clearTimeout(ai.guideTimer); ai.guideTimer=0; }
  if(!ai.guideShown){
    ai.guideShown=true; ai.guideOpen=true;
    ai.guideTimer=setTimeout(()=>{ ai.guideTimer=0; ai.guideOpen=false; if(cur==='ai') drawAIGuide(); },4500);
  }else ai.guideOpen=false;
}
function aiVoiceStatusText(){
  if(!nativeAndroidApp()) return '';
  if(ai.voiceMode===1) return '현재 대화에서는 답변을 계속 읽습니다. “그만 읽어”라고 하면 바로 멈춥니다.';
  if(ai.voiceMode===-1) return '현재 대화에서는 답변을 읽지 않습니다. “계속 읽어줘”라고 하면 다시 읽습니다.';
  return S.aiAutoRead
    ? 'Android 자동 읽기가 켜져 있습니다. 현재 대화에서 “그만 읽어”라고 하면 이 대화만 멈춥니다.'
    : 'Android 자동 읽기는 꺼져 있습니다. 현재 대화에서 “계속 읽어줘”라고 하면 이 대화만 읽습니다.';
}
function drawAIGuide(){
  const g=$('#ai-guide'), b=$('#ai-guide-toggle'), v=$('#ai-guide-voice');
  if(!g||!b) return;
  g.classList.toggle('on', !!ai.guideOpen);
  b.setAttribute('aria-expanded', ai.guideOpen?'true':'false');
  const mark=b.querySelector('.aiguide-v'); if(mark) mark.textContent=ai.guideOpen?'−':'+';
  if(v){
    const android=nativeAndroidApp();
    v.classList.toggle('hide', !android);
    if(android) v.textContent=aiVoiceStatusText();
  }
}
function aiVoiceStop(){
  if(!nativeAndroidApp()) return;
  try{ if('speechSynthesis' in window) window.speechSynthesis.cancel(); }catch(e){}
}
function aiVoiceShouldRead(){
  if(!nativeAndroidApp() || !('speechSynthesis' in window) || typeof SpeechSynthesisUtterance==='undefined') return false;
  if(ai.voiceMode===1) return true;
  if(ai.voiceMode===-1) return false;
  return !!S.aiAutoRead;
}
function aiVoiceSpeak(text){
  if(!aiVoiceShouldRead()) return;
  const msg=String(text||'').replace(/[*#_>`]/g,' ').replace(/\\s+/g,' ').trim();
  if(!msg) return;
  try{
    window.speechSynthesis.cancel();
    const u=new SpeechSynthesisUtterance(msg);
    u.lang='ko-KR'; u.rate=0.82; u.pitch=1;
    const voices=window.speechSynthesis.getVoices?window.speechSynthesis.getVoices():[];
    const ko=voices.find(v=>/^ko(?:-|$)/i.test(v.lang||'')); if(ko) u.voice=ko;
    window.speechSynthesis.speak(u);
  }catch(e){}
}
function aiVoiceCommand(text){
  const x=String(text||'').replace(/\\s+/g,'').replace(/[.!?~]/g,'');
  if(!x || x.length>45) return '';
  if(/그만읽|읽지마|읽지말|읽는거멈|음성멈|음성꺼|소리꺼|말하지마/.test(x)) return 'off';
  if(/계속읽|자동.*읽|이제부터.*읽|답변.*읽|음성으로.*(답|말|읽)|소리내.*읽/.test(x) || /^(읽어줘|읽어주세요)$/.test(x)) return 'on';
  return '';
}

function aiCrisisKind(text){'''
one(old, new, 'AI guide and voice functions')

# Follow-up buttons: app menu/function help and SMART/12-step direct links.
old = '''    'nav-night':['하루 마무리 열기','night'], 'nav-me':['내정보 열기','me'],
    'nav-help':['헬프 열기','help'], 'nav-home':['홈 열기','home'],
    'nav-rec-mood':['기분 기록 열기','rec'], 'nav-rec-urge':['충동 기록 열기','rec'],
    'nav-rec-day':['하루 기록 열기','rec'], 'nav-rec-body':['몸 기록 열기','rec'],
    'nav-rec-relapse':['다시 시작 기록 열기','rec'], 'nav-rec-stat':['통계 열기','rec']'''
new = '''    'nav-night':['하루 마무리 열기','night'], 'nav-me':['내정보 열기','me'],
    'nav-help':['헬프 열기','help'], 'nav-home':['홈 열기','home'],
    'nav-treatment':['치료 일정 열기','treatment'], 'nav-notify':['알림 설정 열기','schedule'],
    'nav-schedule':['일정·알림 열기','schedule'], 'nav-life':['생활 일정 열기','life-schedule'],
    'nav-habit':['습관 열기','habit'], 'nav-screening':['자가점검 열기','screening'],
    'nav-tools':['회복도구 열기','tools'], 'nav-learn':['회복학습 열기','learn'],
    'nav-workbook':['12단계 점검 열기','workbook-list'], 'nav-smart-tools':['SMART 실천도구 열기','smart-tools'],
    'nav-capsule':['미래의 나에게 열기','capsule'], 'nav-learn-twelve':['12단계 학습 열기','learn-topic'],
    'nav-learn-smart':['SMART Recovery 학습 열기','learn-topic'],
    'nav-smart-hov':['HOV 열기','smart-hov'], 'nav-smart-cba':['CBA 열기','smart-cba'],
    'nav-smart-deads':['DEADS 열기','smart-deads'], 'nav-smart-disarm':['DISARM 열기','smart-disarm'],
    'nav-smart-abc':['ABC 열기','smart-abc'], 'nav-smart-dibs':['DIBS 열기','smart-dibs'],
    'nav-smart-thinking':['사고방식 점검 열기','smart-thinking-styles'], 'nav-smart-problem':['문제 해결 열기','smart-problem-solving'],
    'nav-smart-balance':['삶의 균형 열기','smart-balance-pie'], 'nav-smart-vaci':['VACI 열기','smart-vaci'],
    'nav-smart-goal':['SMART 목표 열기','smart-goal'], 'nav-smart-health':['건강 회복 열기','smart-health'],
    'nav-rec-mood':['기분 기록 열기','rec'], 'nav-rec-urge':['충동 기록 열기','rec'],
    'nav-rec-day':['하루 기록 열기','rec'], 'nav-rec-body':['몸 기록 열기','rec'],
    'nav-rec-relapse':['다시 시작 기록 열기','rec'], 'nav-rec-stat':['통계 열기','rec']'''
one(old, new, 'aiFollowHTML cfg')

old = '''  if(ai.follow==='nav-listen'){
    const b=$('#ai-follow-nav'); if(b) b.onclick=()=>{ ai.follow=''; openListen('ai'); };
    return;
  }
  const cfg={'''
new = '''  if(ai.follow==='nav-listen'){
    const b=$('#ai-follow-nav'); if(b) b.onclick=()=>{ ai.follow=''; openListen('ai'); };
    return;
  }
  if(ai.follow==='nav-notify'){
    const b=$('#ai-follow-nav'); if(b) b.onclick=()=>{ ai.follow=''; openScheduleReminderSettings(); };
    return;
  }
  if(ai.follow==='nav-learn-twelve' || ai.follow==='nav-learn-smart'){
    const b=$('#ai-follow-nav'); if(b) b.onclick=()=>{
      learnState.topic=ai.follow==='nav-learn-twelve'?'twelve-steps':'smart-recovery';
      ai.follow=''; go('learn-topic');
    };
    return;
  }
  const cfg={'''
one(old, new, 'aiBindFollow special')

old = '''    'nav-familyguide':['fam',''], 'nav-night':['night',''], 'nav-me':['me',''],
    'nav-help':['help',''], 'nav-home':['home',''],
    'nav-rec-mood':['rec','mood'], 'nav-rec-urge':['rec','urge'], 'nav-rec-day':['rec','day'],
    'nav-rec-body':['rec','body'], 'nav-rec-relapse':['rec','relapse'], 'nav-rec-stat':['rec','stat']'''
new = '''    'nav-familyguide':['fam',''], 'nav-night':['night',''], 'nav-me':['me',''],
    'nav-help':['help',''], 'nav-home':['home',''], 'nav-treatment':['treatment',''],
    'nav-schedule':['schedule',''], 'nav-life':['life-schedule',''], 'nav-habit':['habit',''],
    'nav-screening':['screening',''], 'nav-tools':['tools',''], 'nav-learn':['learn',''],
    'nav-workbook':['workbook-list',''], 'nav-smart-tools':['smart-tools',''], 'nav-capsule':['capsule',''],
    'nav-smart-hov':['smart-hov',''], 'nav-smart-cba':['smart-cba',''], 'nav-smart-deads':['smart-deads',''],
    'nav-smart-disarm':['smart-disarm',''], 'nav-smart-abc':['smart-abc',''], 'nav-smart-dibs':['smart-dibs',''],
    'nav-smart-thinking':['smart-thinking-styles',''], 'nav-smart-problem':['smart-problem-solving',''],
    'nav-smart-balance':['smart-balance-pie',''], 'nav-smart-vaci':['smart-vaci',''],
    'nav-smart-goal':['smart-goal',''], 'nav-smart-health':['smart-health',''],
    'nav-rec-mood':['rec','mood'], 'nav-rec-urge':['rec','urge'], 'nav-rec-day':['rec','day'],
    'nav-rec-body':['rec','body'], 'nav-rec-relapse':['rec','relapse'], 'nav-rec-stat':['rec','stat']'''
one(old, new, 'aiBindFollow cfg')

# drawAI is never blocked by a separate consent page now.
old = '''function drawAI(){
  const consent = !!S.aiConsent;
  $('#ai-profile').innerHTML = mindProAvatar(42);
  $('#ai-consent').classList.toggle('hide', consent);
  $('#ai-main').classList.toggle('hide', !consent);
  $('#ai-dock').classList.toggle('hide', !consent);
  if(!consent) return;

  const chat = Array.isArray(S.aiChat) ? S.aiChat : [];'''
new = '''function drawAI(){
  $('#ai-profile').innerHTML = mindProAvatar(42);
  drawAIGuide();
  $('#ai-main').classList.remove('hide');
  $('#ai-dock').classList.remove('hide');

  const chat = Array.isArray(S.aiChat) ? S.aiChat : [];'''
one(old, new, 'drawAI consent removal')

# App menu/function routing before generic body-record routing.
old = '''  /* 기록 화면은 세부 탭까지 기기에서 엽니다. */
  if(/(통계|분석)/.test(x) && /(기록|보여|열어|확인|봐)/.test(x)) return 'rec-stat';'''
new = '''  /* 앱 기능·메뉴 설명도 AI 서버로 보내지 않고 실제 화면으로 연결합니다. */
  if(/(복약|약).*(알림|시간|설정|예약|관리)|(?:알림|시간).*(복약|약)/.test(x)) return 'treatment';
  if(/(외래|처방).*(일정|알림|예약|설정|관리)|(?:일정|알림).*(외래|처방)/.test(x)) return 'treatment';
  if(/예약\s*알림|알림\s*설정|알림.*(켜|끄|관리|확인|어디)/.test(x)) return 'notify';
  if(/생활\s*일정|위험.*시간.*(설정|등록|관리)|(?:식사|잠|수면).*시간.*(설정|관리)/.test(x)) return 'life-schedule';
  if(/습관.*(만들|설정|알림|관리|메뉴|어디|열어)/.test(x)) return 'habit';
  if(/일정\s*·?\s*알림|일정.*(메뉴|어디|관리|열어)/.test(x)) return 'schedule';
  if(/자가\s*점검|AUDIT|PGSI|DAST|NDS-BV|NAS-BV|NSS-BV|(?:우울|불안|스트레스).*점검/i.test(x)) return 'screening';
  if(/12\s*단계.*(점검|작성|워크|기록)/.test(x)) return 'workbook';
  if(/SMART.*(도구|실천)|스마트.*(도구|실천)/i.test(x)) return 'smart-tools';
  if(/회복\s*학습.*(열|어디|메뉴|설명|보여)/.test(x)) return 'learn';
  if(/회복\s*도구.*(열|어디|메뉴|설명|뭐|보여)/.test(x)) return 'tools';
  if(/미래의\s*나|초심글|초심\s*글/.test(x) && /(열|보여|어디|메뉴|작성|수정)/.test(x)) return 'capsule';

  /* 기록 화면은 세부 탭까지 기기에서 엽니다. */
  if(/(통계|분석)/.test(x) && /(기록|보여|열어|확인|봐)/.test(x)) return 'rec-stat';'''
one(old, new, 'aiLocalIntent app menus')

# Static, app-owned 12-step / SMART knowledge layer. It uses learning-data.js and current app copy before external AI.
marker = '''function aiHelpCallReply(text){'''
knowledge = '''function aiKnowledgeReply(text){
  const x=String(text||'').trim();
  if(!x) return null;
  const twelve=LEARNING.find(t=>t&&t.id==='twelve-steps');
  const stepMatch=x.match(/(?:^|\\D)(1[0-2]|[1-9])\\s*단계/);
  const twelveAsked=!!stepMatch || /12\\s*단계|십이\\s*단계|AA.*단계|NA.*단계|GA.*단계/i.test(x);
  if(twelveAsked && !/(점검|작성|워크|기록)/.test(x)){
    if(stepMatch){
      const n=parseInt(stepMatch[1],10), set=twelveStepSet();
      const sentence=set&&Array.isArray(set.steps)?String(set.steps[n-1]||''):'';
      const sec=twelve&&Array.isArray(twelve.sections)?twelve.sections.find(v=>v&&v.id==='step-'+n):null;
      const view=sec?learningSectionPerspective(sec):null;
      const summary=view ? String(view.summary || (Array.isArray(view.body)&&view.body[0]) || '') : '';
      return {text:n+'단계 문장은 “'+sentence+'”입니다.'+(summary?'\\n\\n앱의 '+n+'단계 해설에서는 '+summary:'')+'\\n\\n회복학습에서 전체 설명과 생각해보기·오늘 해보기를 이어서 볼 수 있습니다.',follow:'nav-learn-twelve'};
    }
    const desc=twelve?String(twelve.longDescription||twelve.description||''):'';
    return {text:(desc||'12단계는 회복의 지도로 읽고, 생각하고, 오늘의 삶에 적용하도록 앱에 정리되어 있습니다.')+'\\n\\n회복학습에는 12단계의 기초와 1~12단계 해설이 있고, 12단계 점검에서는 실제 경험을 기록할 수 있습니다.',follow:'nav-learn-twelve'};
  }

  const smart=LEARNING.find(t=>t&&t.id==='smart-recovery');
  const smartTools=[
    {re:/\\bHOV\\b|가치의\\s*계층/i,name:'가치의 계층 HOV',desc:'내가 중요하게 여기는 가치를 정리하고 변화의 이유와 연결하는 도구입니다.',follow:'nav-smart-hov'},
    {re:/\\bCBA\\b|비용.?편익/i,name:'비용-편익 분석 CBA',desc:'사용·행동과 변화의 단기·장기 이점과 비용을 함께 비교하는 도구입니다.',follow:'nav-smart-cba'},
    {re:/\\bDEADS\\b/i,name:'DEADS',desc:'충동이 올라왔을 때 거부·지연, 벗어나기, 회피·수용·반박, 주의 돌리기, 대체하기 중 지금 쓸 전략을 고르는 도구입니다.',follow:'nav-smart-deads'},
    {re:/\\bDISARM\\b/i,name:'DISARM',desc:'충동을 부추기는 목소리와 나 자신을 분리하고, 그 생각을 알아차려 다른 선택으로 돌리는 도구입니다.',follow:'nav-smart-disarm'},
    {re:/\\bABC\\b/i,name:'ABC',desc:'사건(A), 생각·믿음(B), 감정·행동 결과(C)를 구분해 살펴보는 도구입니다.',follow:'nav-smart-abc'},
    {re:/\\bDIBS\\b/i,name:'DIBS',desc:'도움이 되지 않는 믿음이나 생각을 질문하고 더 균형 잡힌 생각으로 바꾸어보는 도구입니다.',follow:'nav-smart-dibs'},
    {re:/\\bVACI\\b/i,name:'VACI',desc:'삶에 활력과 관심을 되돌릴 수 있는 활동을 찾고 실제로 시도해보는 도구입니다.',follow:'nav-smart-vaci'},
    {re:/사고방식.*(점검|도구)|도움이\\s*되지\\s*않는\\s*사고/i,name:'사고방식 점검',desc:'반복되는 생각의 습관을 알아차리고 지금 도움이 되는 관점을 찾는 도구입니다.',follow:'nav-smart-thinking'},
    {re:/문제\\s*해결.*(5|다섯|도구|단계)/i,name:'문제 해결 5단계',desc:'문제를 구체적으로 정하고 가능한 선택을 비교한 뒤 실행계획을 세우는 도구입니다.',follow:'nav-smart-problem'},
    {re:/삶의\\s*균형/i,name:'삶의 균형',desc:'삶의 여러 영역이 한쪽으로 치우치지 않았는지 살펴보고 돌볼 영역을 정하는 도구입니다.',follow:'nav-smart-balance'},
    {re:/SMART\\s*목표|스마트\\s*목표/i,name:'SMART 목표',desc:'목표를 구체적·측정가능·동의가능·현실적·시간제한으로 점검하고 실행 행동을 정합니다.',follow:'nav-smart-goal'},
    {re:/건강\\s*회복|생활\\s*돌보기/i,name:'건강 회복',desc:'식사·운동·수면·복약 등 회복을 받쳐주는 생활을 살펴보는 SMART 도구입니다.',follow:'nav-smart-health'}
  ];
  for(const t of smartTools){
    if(t.re.test(x)) return {text:t.name+'는 '+t.desc+'\\n\\n앱에 이미 있는 실천도구를 바로 열어 사용할 수 있습니다.',follow:t.follow};
  }
  if(/SMART\\s*Recovery|SMART\\s*리커버리|스마트\\s*리커버리|SMART\\s*회복/i.test(x)){
    const desc=smart?String(smart.longDescription||smart.description||''):'';
    return {text:(desc||'SMART Recovery는 동기, 충동 대처, 생각·감정·행동 관리, 균형 잡힌 삶의 네 영역에서 필요한 도구를 반복해 사용하는 회복의 틀입니다.')+'\\n\\n앱의 회복학습과 SMART 실천도구에서 각 Point와 도구를 이어서 사용할 수 있습니다.',follow:'nav-learn-smart'};
  }
  return null;
}

'''
if s.count(marker) != 1:
    raise SystemExit('knowledge insertion marker missing')
s = s.replace(marker, knowledge + marker, 1)

# Local navigation replies for new app-function intents.
old = '''  if(intent === 'me'){
    aiAdd('assistant','내정보에서는 회복 영역·시작일·지역과 앱 설정, 내 발자취·기록 내보내기 등을 관리할 수 있어요. 일정과 알림은 [회복도구] → [일정·알림]에서 관리할 수 있어요.', true);
    ai.follow='nav-me'; drawAI(); return true;
  }'''
new = '''  if(intent === 'treatment'){
    aiAdd('assistant','복약 알림은 [회복도구 → 일정·알림 → 치료 일정]에서 하루 복약 횟수와 시간을 정한 뒤, [알림 설정]에서 Android 예약알림을 확인하면 됩니다. 약 이름이나 진단명은 입력하지 않습니다.', true);
    ai.follow='nav-treatment'; drawAI(); return true;
  }
  if(intent === 'notify'){
    aiAdd('assistant',nativeAndroidApp()?'알림 설정에서는 습관·생활·복약·외래 시간을 Android 예약알림으로 확인하고 저장합니다. 앱이 닫혀 있어도 Android가 예약시간에 알림을 보낼 수 있습니다.':'[회복도구 → 일정·알림 → 알림 설정]에서 습관·생활·치료 알림을 관리할 수 있습니다.', true);
    ai.follow='nav-notify'; drawAI(); return true;
  }
  if(intent === 'schedule'){
    aiAdd('assistant','[일정·알림]에는 습관, 생활 일정, 치료 일정, 알림 설정이 한곳에 모여 있습니다. 무엇을 챙기려는지에 따라 해당 메뉴로 들어가면 됩니다.', true);
    ai.follow='nav-schedule'; drawAI(); return true;
  }
  if(intent === 'life-schedule'){
    aiAdd('assistant','생활 일정에서는 위험한 시간대와 식사·잠 시간을 정합니다. 시간을 정한 뒤 알림 설정에서 실제 예약알림을 확인할 수 있습니다.', true);
    ai.follow='nav-life'; drawAI(); return true;
  }
  if(intent === 'habit'){
    aiAdd('assistant','습관에서는 작은 실천을 만들고 오늘 했는지 체크할 수 있습니다. 시간을 정했다면 알림 설정에서 실제 예약알림도 확인할 수 있습니다.', true);
    ai.follow='nav-habit'; drawAI(); return true;
  }
  if(intent === 'screening'){
    aiAdd('assistant','자가점검은 회복도구의 자가점검에서 할 수 있습니다. 결과는 진단이 아니라 현재 상태를 살펴보는 참고자료이며 점수와 결과구간만 이 기기에 저장됩니다.', true);
    ai.follow='nav-screening'; drawAI(); return true;
  }
  if(intent === 'tools'){
    aiAdd('assistant','회복도구는 내 계획, 배우기, 실천하기, 자가점검으로 나뉩니다. 새로 계획하거나 작성하는 기능은 여기에서 시작하고, 지나간 기록은 [나 → 내 발자취]에서 봅니다.', true);
    ai.follow='nav-tools'; drawAI(); return true;
  }
  if(intent === 'learn'){
    aiAdd('assistant','회복학습에는 12단계와 SMART Recovery처럼 앱에 미리 정리해 둔 회복 콘텐츠가 있습니다. 일반 AI 지식이 아니라 앱에 들어 있는 내용을 먼저 볼 수 있습니다.', true);
    ai.follow='nav-learn'; drawAI(); return true;
  }
  if(intent === 'workbook'){
    aiAdd('assistant','12단계 점검에서는 1·4·8·9·10·11·12단계의 검토와 실천을 직접 작성할 수 있고, 내용은 이 기기에만 저장됩니다.', true);
    ai.follow='nav-workbook'; drawAI(); return true;
  }
  if(intent === 'smart-tools'){
    aiAdd('assistant','SMART 실천도구는 4-Point를 순서대로 통과하는 방식이 아니라 지금 필요한 영역을 열어 HOV·CBA·DEADS·DISARM·ABC·DIBS·VACI 같은 도구를 반복해서 사용합니다.', true);
    ai.follow='nav-smart-tools'; drawAI(); return true;
  }
  if(intent === 'capsule'){
    aiAdd('assistant','[미래의 나에게]는 회복을 시작한 날의 마음과 힘든 날의 나에게 해주고 싶은 말을 남겨두는 곳입니다. 내용은 이 기기에만 저장됩니다.', true);
    ai.follow='nav-capsule'; drawAI(); return true;
  }
  if(intent === 'me'){
    aiAdd('assistant','내정보에서는 회복 영역·시작일·지역과 앱 설정, 내 발자취·기록 내보내기 등을 관리할 수 있어요. 일정과 알림은 [회복도구] → [일정·알림]에서 관리할 수 있어요.', true);
    ai.follow='nav-me'; drawAI(); return true;
  }'''
one(old, new, 'aiLocalNav app replies')

# Voice command and app-owned knowledge are local. Crisis keeps highest priority.
old = '''  const crisis = aiCrisisKind(text);
  const timerMin = aiTimerMinutes(text, topic);
  const wantsRead = aiReadWanted(text, topic);
  const localIntent = (!crisis && !timerMin && !wantsRead) ? aiLocalIntent(text, topic) : '';
  const isLocal = !!(crisis || timerMin || wantsRead || localIntent);'''
new = '''  const crisis = aiCrisisKind(text);
  const voiceCommand = !crisis ? aiVoiceCommand(text) : '';
  const timerMin = (!crisis && !voiceCommand) ? aiTimerMinutes(text, topic) : 0;
  const wantsRead = (!crisis && !voiceCommand && !timerMin) ? aiReadWanted(text, topic) : false;
  const knowledge = (!crisis && !voiceCommand && !timerMin && !wantsRead) ? aiKnowledgeReply(text) : null;
  const localIntent = (!crisis && !voiceCommand && !timerMin && !wantsRead && !knowledge) ? aiLocalIntent(text, topic) : '';
  const isLocal = !!(crisis || voiceCommand || timerMin || wantsRead || knowledge || localIntent);'''
one(old, new, 'aiSend local classification')

old = '''  const userMsg = aiAdd('user', text, isLocal);

  if(crisis){'''
new = '''  const userMsg = aiAdd('user', text, isLocal);

  if(voiceCommand){
    if(!nativeAndroidApp()){
      aiAdd('assistant','음성 자동 읽기는 Android 앱에서만 사용합니다. 일반 웹·PWA에서는 지금처럼 글자로 답변합니다.', true);
      drawAI(); return;
    }
    if(voiceCommand==='off'){
      ai.voiceMode=-1; aiVoiceStop();
      aiAdd('assistant','알겠습니다. 현재 대화에서는 답변을 읽지 않겠습니다. 다시 “계속 읽어줘”라고 하면 그때부터 읽습니다.', true);
    }else{
      ai.voiceMode=1;
      aiAdd('assistant','알겠습니다. 현재 대화에서는 설정과 상관없이 앞으로 오는 답변을 계속 읽겠습니다. “그만 읽어”라고 하면 바로 멈춥니다.', true);
    }
    drawAI(); return;
  }

  if(crisis){'''
one(old, new, 'aiSend voice command')

old = '''  /* 시간을 말로 요청하면 OpenAI에 맡기지 않고 실제 채팅 타이머를 엽니다. */
  if(timerMin){'''
new = '''  if(knowledge){
    aiAdd('assistant',knowledge.text,true);
    ai.follow=knowledge.follow||'';
    drawAI(); return;
  }

  /* 시간을 말로 요청하면 OpenAI에 맡기지 않고 실제 채팅 타이머를 엽니다. */
  if(timerMin){'''
one(old, new, 'aiSend knowledge')

# Any real conversation starts with the guide folded.
old = '''  ai.read = null;
  ai.actionsOpen = false;
  $('#ai-input').value = '';'''
new = '''  ai.read = null;
  ai.actionsOpen = false;
  ai.guideOpen = false;
  if(ai.guideTimer){ clearTimeout(ai.guideTimer); ai.guideTimer=0; }
  $('#ai-input').value = '';'''
one(old, new, 'aiSend fold guide')

# Replace old consent button handler with guide toggle.
one("$('#ai-consent-go').onclick = () => { S.aiConsent = 1; ai.actionsOpen = false; save(); drawAI(); };",
    "$('#ai-guide-toggle').onclick = () => { if(ai.guideTimer){ clearTimeout(ai.guideTimer); ai.guideTimer=0; } ai.guideOpen=!ai.guideOpen; drawAIGuide(); };",
    'guide toggle handler')

# New chat clears only session override and current speech, then returns to saved default.
old = "$('#ai-clear-go').onclick = () => { S.aiChat=[]; save(); ai.meetings=[]; ai.resources=[]; ai.actionsOpen=false; ai.follow=''; ai.loc=null; ai.activeArea=''; ai.activeAreaSource=''; ai.read=null; ai.timer=null; aiTimerClearTick(); closeModal(); drawAI(); };"
new = "$('#ai-clear-go').onclick = () => { S.aiChat=[]; save(); ai.meetings=[]; ai.resources=[]; ai.actionsOpen=false; ai.follow=''; ai.loc=null; ai.activeArea=''; ai.activeAreaSource=''; ai.read=null; ai.timer=null; ai.voiceMode=0; aiVoiceStop(); aiTimerClearTick(); closeModal(); drawAI(); };"
one(old, new, 'new chat voice reset')

# Update app accordion summary text so the Android voice setting is discoverable without adding another top-level section.
one("? '자원 목록 · 화면 설정 · 앱 새로고침 · 앱 설치<br><span class=\"flag\">새 판 ' +",
    "? '자원 목록 · 화면 설정 · 마음프로 음성 · 앱 새로고침 · 앱 설치<br><span class=\"flag\">새 판 ' +",
    'app accordion update text 1')
one(": '자원 목록 · 화면 설정 · 앱 새로고침 · 앱 설치';",
    ": '자원 목록 · 화면 설정 · 마음프로 음성 · 앱 새로고침 · 앱 설치';",
    'app accordion update text 2')

P.write_text(s, encoding='utf-8')

# Service worker version/cache.
sw = Path('sw.js').read_text(encoding='utf-8')
if sw.count("const APP_VERSION = 'V8.2.48';") != 1:
    raise SystemExit('sw APP_VERSION mismatch')
sw = sw.replace("const APP_VERSION = 'V8.2.48';", "const APP_VERSION = 'V8.2.49';", 1)
if sw.count("const V = 'ohg-v8248-audit-skip';") != 1:
    raise SystemExit('sw cache key mismatch')
sw = sw.replace("const V = 'ohg-v8248-audit-skip';", "const V = 'ohg-v8249-mindpro-guide-voice';", 1)
Path('sw.js').write_text(sw, encoding='utf-8')

# Release note at README top.
rp = Path('README.md')
r = rp.read_text(encoding='utf-8')
head = '''# V8.2.49 — 마음프로 안내 · 앱지식 · Android 음성\n\n- 마음프로 진입을 막던 `확인하고 시작` 화면을 없애고, 안전·개인정보 안내는 상단에서 잠깐 펼쳐진 뒤 자동으로 접히며 필요할 때 다시 열 수 있습니다.\n- 12단계와 SMART Recovery 질문은 `learning-data.js`와 앱의 기존 SMART 도구 설명을 먼저 사용해 기기에서 답하고 실제 학습·실천도구 화면으로 연결합니다.\n- 복약·외래 알림, 일정·알림, 습관, 자가점검, 회복도구 등 앱 기능과 메뉴 질문은 AI 서버보다 앱에서 먼저 설명하고 해당 화면으로 연결합니다.\n- Android 앱의 `내 정보 · 설정 → 앱`에 `마음프로 답변 자동 읽기` 기본설정을 둡니다. 일반 웹/PWA에는 음성 기능을 추가하지 않습니다.\n- 현재 대화에서 `계속 읽어줘`라고 하면 기본설정과 관계없이 이후 답변을 읽고, `그만 읽어`라고 하면 즉시 멈추며 새 대화를 시작하면 다시 기본설정을 따릅니다.\n- 개인 회복기록 자동전송 금지, `DATA_SCHEMA=6`, `ohg.v1`, Android 정확알림·부팅 재예약·기존 이완 TTS는 변경하지 않습니다.\n\n'''
if not r.startswith('# V8.2.49'):
    r = head + r
rp.write_text(r, encoding='utf-8')

print('V8.2.49 MindPro patch applied')
