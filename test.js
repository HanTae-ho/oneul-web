const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');

const MIME = { '.html':'text/html', '.js':'text/javascript', '.json':'application/json', '.png':'image/png' };
const srv = http.createServer((req, res) => {
  let p = req.url.split('?')[0];
  if (p === '/') p = '/index.html';
  const f = path.join(__dirname, p);
  if (!fs.existsSync(f)) { console.error('TEST HTTP404:', p); res.writeHead(404); res.end('no'); return; }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'text/plain' });
  res.end(fs.readFileSync(f));
});

(async () => {
  await new Promise(r => srv.listen(8899, r));
  const launchOpts = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {};
  const b = await chromium.launch(launchOpts);
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2,
    locale: 'ko-KR', timezoneId: 'Asia/Seoul' });
  const pg = await ctx.newPage();

  const errs = [];
  pg.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  // 결정론적 회귀검사에서는 외부 서비스의 일시적 4xx를 JS 오류로 오인하지 않습니다.
  // 대신 localhost의 4xx/5xx는 별도로 실패 처리해 앱 자체의 누락 자원은 계속 잡습니다.
  pg.on('response', r => {
    try {
      const u = new URL(r.url());
      if ((u.hostname === 'localhost' || u.hostname === '127.0.0.1') && r.status() >= 400) {
        errs.push('LOCAL HTTP ' + r.status() + ': ' + u.pathname);
      }
    } catch (_) {}
  });
  pg.on('console', m => {
    if (m.type() !== 'error') return;
    const text = m.text();
    if (text.startsWith('Failed to load resource:')) return;
    errs.push('CONSOLE: ' + text);
  });

  const shot = async n => { await pg.screenshot({ path: `${__dirname}/shot-${n}.png`, fullPage: true }); };
  const seen = async () => await pg.$eval('.pg.on', e => e.id);
  // CI runner의 시스템 시간대(UTC)와 관계없이 앱과 같은 Asia/Seoul 날짜를 사용합니다.
  const kstYmd = d => {
    const parts = new Intl.DateTimeFormat('en-CA', {
      timeZone:'Asia/Seoul', year:'numeric', month:'2-digit', day:'2-digit'
    }).formatToParts(d);
    const v = Object.fromEntries(parts.map(x => [x.type, x.value]));
    return v.year + '-' + v.month + '-' + v.day;
  };
  const daysAgo = n => {
    const todayKst = kstYmd(new Date());
    const [y,m,d] = todayKst.split('-').map(Number);
    const x = new Date(Date.UTC(y, m-1, d));
    x.setUTCDate(x.getUTCDate() - n);
    const z = v => String(v).padStart(2, '0');
    return x.getUTCFullYear() + '-' + z(x.getUTCMonth()+1) + '-' + z(x.getUTCDate());
  };
  const assert = (ok, msg) => { if(!ok) throw new Error('ASSERT: ' + msg); };

  // V9.1.1 저장 복구 회귀 — V9.1.0 기존 데이터에는 recordStart가 없었습니다.
  // 초기 load()가 뒤쪽 today()/ymd() const를 참조해 BLANK로 떨어지던 회귀를 재현하고 차단합니다.
  {
    const oldCtx=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',timezoneId:'Asia/Seoul'});
    const oldPg=await oldCtx.newPage();
    const oldRecord={ver:1,dataSchema:6,started:true,role:'self',types:['alcohol'],dates:{alcohol:daysAgo(40)},cum:{alcohol:0},
      goal:'기존 목표',hours:[],meds:[],medLog:[],eats:[],eatLog:[],sleep:{on:0,bed:'23:00',up:'07:00'},sleepLog:[],
      moods:[{t:Date.now()-86400000,v:3}],halts:[],urges:[],nights:[],relapses:[],screenings:[],stepWorks:[],stepDrafts:{},
      wbDays:{},meaningChecks:[],smartWorks:[
        {id:'old-self-smart',kind:'abc',role:'self',ts:Date.now()-9000,updatedAt:Date.now()-9000},
        {id:'old-family-smart',kind:'abc',role:'family',ts:Date.now()-8000,updatedAt:Date.now()-8000}
      ],familyStepWorks:[],familyStepDrafts:{},aiChat:[],fired:[]};
    await oldCtx.addInitScript(raw=>localStorage.setItem('ohg.v1',raw),JSON.stringify(oldRecord));
    await oldPg.goto('http://localhost:8899/index.html'); await oldPg.waitForTimeout(500);
    assert(await oldPg.$eval('.pg.on',e=>e.id)==='p-home','recordStart 없는 V9.1.0 기존 데이터는 자동으로 홈에 복구되어야 함');
    const oldState=await oldPg.evaluate(()=>({
      dataSchema:S.dataSchema,moods:S.moods.length,goal:S.goal,recordStart:S.recordStart,blocked:!!(storageRecovery&&storageRecovery.blocking),
      familyWbDays:S.familyWbDays,familyMeaningChecks:S.familyMeaningChecks,familyMeaningCheckDraft:S.familyMeaningCheckDraft,
      familyMoods:S.familyMoods,familyHalts:S.familyHalts,familyNights:S.familyNights,familyScreenings:S.familyScreenings,
      familyHabits:S.familyHabits,familyEats:S.familyEats,familyEatLog:S.familyEatLog,familySleepLog:S.familySleepLog,
      smart:S.smartWorks.map(x=>x.id),familySmart:S.familySmartWorks.map(x=>x.id)
    }));
    assert(oldState.dataSchema===7&&oldState.moods===1&&oldState.goal==='기존 목표'&&/^\d{4}-\d{2}-\d{2}$/.test(oldState.recordStart),'스키마 6 기존 기록·목표를 보존하며 DATA_SCHEMA 7로 안전 마이그레이션');
    assert(oldState.familyWbDays&&Object.keys(oldState.familyWbDays).length===0&&Array.isArray(oldState.familyMeaningChecks)&&oldState.familyMeaningChecks.length===0&&oldState.familyMeaningCheckDraft===null,'기존 의미 데이터는 역할별 저장소를 그대로 유지');
    assert(oldState.familyMoods.length===0&&oldState.familyHalts.length===0&&oldState.familyNights.length===0&&oldState.familyScreenings.length===0&&oldState.familyHabits.length===0&&oldState.familyEats.length===0&&oldState.familyEatLog.length===0&&oldState.familySleepLog.length===0,'역할 정보가 없던 스키마 6 공용 기록은 가족으로 추정 이동하지 않고 가족 저장소를 빈 상태로 초기화');
    assert(oldState.smart.length===1&&oldState.smart[0]==='old-self-smart'&&oldState.familySmart.length===1&&oldState.familySmart[0]==='old-family-smart','스키마 6 SMART는 명시된 role만 이용해 당사자·가족 물리 저장소로 분리');
    assert(!oldState.blocked,'정상 기존 데이터에는 복구 선택창을 띄우지 않음');
    assert(await oldPg.evaluate(()=>S.viewMode===''&&!document.body.classList.contains('simple-view')),'viewMode 없는 기존 사용자는 전체 보기를 유지');
    await oldCtx.close();
  }

  // started=false인데 실제 개인기록이 있으면 자동 덮어쓰기 대신 복구 게이트에서 선택하게 합니다.
  {
    const gateCtx=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',timezoneId:'Asia/Seoul'});
    const gatePg=await gateCtx.newPage();
    const gateRecord={ver:1,dataSchema:6,started:false,role:'self',types:['alcohol'],dates:{alcohol:daysAgo(20)},cum:{alcohol:0},
      goal:'복구할 목표',moods:[{t:Date.now()-3600000,v:4}],halts:[],urges:[],nights:[],relapses:[],screenings:[],
      stepWorks:[],meaningChecks:[],smartWorks:[],familyStepWorks:[],medLog:[],eatLog:[],sleepLog:[]};
    const gateRaw=JSON.stringify(gateRecord);
    await gateCtx.addInitScript(raw=>localStorage.setItem('ohg.v1',raw),gateRaw);
    await gatePg.goto('http://localhost:8899/index.html'); await gatePg.waitForTimeout(500);
    assert(await gatePg.isVisible('#mod.on'),'started=false + 기존 기록은 복구 게이트를 표시');
    assert((await gatePg.$eval('#modin',e=>e.innerText)).includes('기존 데이터 사용'),'복구 게이트에 기존 데이터 사용 선택 제공');
    await gatePg.waitForTimeout(700);
    assert(await gatePg.evaluate(()=>localStorage.getItem('ohg.v1'))===gateRaw,'선택 전에는 기존 ohg.v1 원문을 덮어쓰지 않음');
    await gatePg.click('#recovery-use-primary'); await gatePg.waitForTimeout(350);
    assert(await gatePg.$eval('.pg.on',e=>e.id)==='p-home','기존 데이터 사용 선택 후 홈으로 복구');
    const gateAfter=await gatePg.evaluate(()=>({started:S.started,moods:S.moods.length,backup:localStorage.getItem('ohg.v1.recovery-backup')}));
    assert(gateAfter.started===true&&gateAfter.moods===1,'기존 기록을 유지하고 started만 복구');
    assert(gateAfter.backup===gateRaw,'복구 전 원문을 안전백업 키에 그대로 보존');
    await gateCtx.close();
  }

  // 파싱 불가 원문도 BLANK로 덮지 않고 그대로 보존합니다.
  {
    const badCtx=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',timezoneId:'Asia/Seoul'});
    const badPg=await badCtx.newPage();
    const badRaw='{"started":true,"moods":[';
    await badCtx.addInitScript(raw=>localStorage.setItem('ohg.v1',raw),badRaw);
    await badPg.goto('http://localhost:8899/index.html'); await badPg.waitForTimeout(700);
    assert(await badPg.isVisible('#mod.on'),'손상된 ohg.v1은 복구 게이트에서 멈춤');
    assert((await badPg.$eval('#modin',e=>e.innerText)).includes('정상적으로 읽지 못했습니다'),'손상 데이터 읽기 오류를 사용자에게 표시');
    assert(await badPg.evaluate(()=>localStorage.getItem('ohg.v1'))===badRaw,'손상된 기존 원문도 자동으로 덮어쓰지 않음');
    await badCtx.close();
  }

  // V9.1.2 기록관리 시뮬레이션 — 내보내기/불러오기/전체지우기/안전백업을 실제 브라우저에서 검증합니다.
  {
    const exCtx=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',timezoneId:'Asia/Seoul',acceptDownloads:true});
    const exPg=await exCtx.newPage();
    const base={ver:1,dataSchema:6,started:true,role:'self',types:['alcohol'],dates:{alcohol:daysAgo(30)},cum:{alcohol:0},
      goal:'내보내기 테스트',hours:[],meds:[],medLog:[],eats:[],eatLog:[],sleep:{on:0,bed:'23:00',up:'07:00'},sleepLog:[],
      moods:[{t:Date.now()-10000,v:4}],halts:[],urges:[],nights:[],relapses:[],screenings:[],stepWorks:[],stepDrafts:{},
      wbDays:{},meaningChecks:[],smartWorks:[],familyStepWorks:[],familyStepDrafts:{},aiChat:[],fired:[]};
    await exCtx.addInitScript(raw=>localStorage.setItem('ohg.v1',raw),JSON.stringify(base));
    await exPg.goto('http://localhost:8899/index.html'); await exPg.waitForTimeout(300);
    await exPg.evaluate(()=>{
      go('me');
      window.__exportNames=[];
      const orig=HTMLAnchorElement.prototype.click;
      HTMLAnchorElement.prototype.click=function(){
        if(this.download) window.__exportNames.push(this.download);
        return orig.call(this);
      };
    });
    await exPg.$eval('#me-export',el=>{
      const acc=el.closest('.acc'), head=acc&&acc.querySelector('.acc-h');
      if(head) head.click();
    });
    assert(await exPg.isVisible('#me-export'),'기록 관리 아코디언을 펼치면 내보내기 버튼이 보여야 함');
    await exPg.click('#me-export');
    await exPg.waitForTimeout(10);
    await exPg.click('#me-export');
    const names=await exPg.evaluate(()=>window.__exportNames.slice());
    assert(names.length===2,'연속 2회 내보내기는 각각 파일 생성을 요청');
    assert(/^오늘 한 걸음_백업_\d{8}-\d{6}-\d{3}\.json$/.test(names[0]),'내보내기 파일명은 날짜·시각·밀리초가 포함된 백업 이름');
    assert(names[0]!==names[1],'같은 날 연속 내보내기도 파일명이 겹치지 않음');
    assert((await exPg.$eval('#toast',e=>e.innerText)).includes('완료'),'내보내기 후 완료 안내를 표시');
    await exCtx.close();
  }

  // 기기 안전백업 관리 화면은 실제 버튼을 연결할 때도 오류 없이 열려야 합니다.
  {
    const mgrCtx=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',timezoneId:'Asia/Seoul',acceptDownloads:true});
    const mgrPg=await mgrCtx.newPage();
    const pageErrors=[];
    mgrPg.on('pageerror',e=>pageErrors.push(String(e&&e.message||e)));
    const current={ver:1,dataSchema:6,started:true,role:'self',types:['alcohol'],dates:{alcohol:daysAgo(10)},goal:'현재 기록',
      moods:[{t:Date.now(),v:3}],halts:[],urges:[],nights:[],relapses:[],screenings:[],stepWorks:[],meaningChecks:[],smartWorks:[],
      familyStepWorks:[],medLog:[],eatLog:[],sleepLog:[]};
    const backup={ver:1,dataSchema:6,started:true,role:'self',types:['alcohol'],dates:{alcohol:daysAgo(20)},goal:'안전백업1',
      moods:[{t:Date.now()-5000,v:4}],halts:[],urges:[],nights:[],relapses:[],screenings:[],stepWorks:[],meaningChecks:[],smartWorks:[],
      familyStepWorks:[],medLog:[],eatLog:[],sleepLog:[]};
    const quarantine={ver:1,dataSchema:6,started:true,role:'self',types:['alcohol'],dates:{alcohol:daysAgo(30)},goal:'안전백업2',
      moods:[{t:Date.now()-10000,v:2}],halts:[],urges:[],nights:[],relapses:[],screenings:[],stepWorks:[],meaningChecks:[],smartWorks:[],
      familyStepWorks:[],medLog:[],eatLog:[],sleepLog:[]};
    await mgrCtx.addInitScript(v=>{
      localStorage.setItem('ohg.v1',v.current);
      localStorage.setItem('ohg.v1.recovery-backup',v.backup);
      localStorage.setItem('ohg.v1.recovery-quarantine',v.quarantine);
    },{current:JSON.stringify(current),backup:JSON.stringify(backup),quarantine:JSON.stringify(quarantine)});
    await mgrPg.goto('http://localhost:8899/index.html'); await mgrPg.waitForTimeout(250);
    await mgrPg.evaluate(()=>{
      go('me');
      window.__backupExportClicks=0;
      HTMLAnchorElement.prototype.click=function(){ if(this.download) window.__backupExportClicks++; };
    });
    await mgrPg.$eval('#me-recovery-manage',el=>{
      const acc=el.closest('.acc'),head=acc&&acc.querySelector('.acc-h');
      if(head&&!acc.classList.contains('on')) head.click();
    });
    assert(await mgrPg.isVisible('#me-recovery-manage'),'기록 관리에서 기기 안전백업 확인 버튼 표시');
    await mgrPg.click('#me-recovery-manage'); await mgrPg.waitForTimeout(80);
    assert((await mgrPg.$eval('#modin',e=>e.innerText)).includes('안전백업 1')&&(await mgrPg.$eval('#modin',e=>e.innerText)).includes('안전백업 2'),'기기 안전백업 1·2를 함께 표시');
    assert(await mgrPg.evaluate(()=>document.querySelectorAll('[data-recovery-export]').length===2),'두 안전백업의 파일 내보내기 버튼 연결');
    assert(await mgrPg.evaluate(()=>document.querySelectorAll('[data-recovery-restore]').length===2),'두 안전백업의 복구 버튼 연결');
    await mgrPg.click('[data-recovery-export="backup"]'); await mgrPg.waitForTimeout(30);
    assert(await mgrPg.evaluate(()=>window.__backupExportClicks)===1,'안전백업 파일 내보내기 버튼이 실제로 동작');
    await mgrPg.click('[data-recovery-restore="backup"]'); await mgrPg.waitForTimeout(30);
    assert((await mgrPg.$eval('#modin',e=>e.innerText)).includes('이 안전백업을 복구할까요?'),'안전백업 복구 확인 화면 연결');
    assert(pageErrors.length===0,'기기 안전백업 관리 화면에서 JavaScript pageerror 없음');
    await mgrCtx.close();
  }

  // 전혀 다른 JSON은 백업으로 인정하지 않고 현재 기록을 보존합니다.
  {
    const imCtx=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',timezoneId:'Asia/Seoul'});
    const imPg=await imCtx.newPage();
    const current={ver:1,dataSchema:6,started:true,role:'self',types:['alcohol'],dates:{alcohol:daysAgo(12)},goal:'현재기록',
      moods:[{t:Date.now(),v:3}],halts:[],urges:[],nights:[],relapses:[],screenings:[],stepWorks:[],meaningChecks:[],smartWorks:[],
      familyStepWorks:[],medLog:[],eatLog:[],sleepLog:[]};
    const currentRaw=JSON.stringify(current);
    await imCtx.addInitScript(raw=>localStorage.setItem('ohg.v1',raw),currentRaw);
    await imPg.goto('http://localhost:8899/index.html'); await imPg.waitForTimeout(250);
    await imPg.setInputFiles('#me-file',{name:'not-oneul.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify({version:'V9.1.2',versionCode:918}))});
    await imPg.waitForTimeout(150);
    assert((await imPg.$eval('#toast',e=>e.innerText)).includes('오늘 한 걸음 백업 파일이 아니거나'),'다른 JSON을 명확히 거부');
    assert(await imPg.evaluate(()=>localStorage.getItem('ohg.v1'))===currentRaw,'잘못된 JSON 선택 후 기존 원문 불변');
    await imCtx.close();
  }

  // 정상 백업 불러오기는 현재 원문을 안전백업한 뒤 교체합니다.
  {
    const imCtx=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',timezoneId:'Asia/Seoul'});
    const imPg=await imCtx.newPage();
    const old={ver:1,dataSchema:6,started:true,role:'self',types:['alcohol'],dates:{alcohol:daysAgo(20)},goal:'교체 전',
      moods:[{t:Date.now()-5000,v:2}],halts:[],urges:[],nights:[],relapses:[],screenings:[],stepWorks:[],meaningChecks:[],smartWorks:[],
      familyStepWorks:[],medLog:[],eatLog:[],sleepLog:[]};
    const incoming={ver:1,dataSchema:7,started:true,role:'self',types:['alcohol'],dates:{alcohol:daysAgo(4)},goal:'불러온 기록',
      moods:[{t:Date.now()-3000,v:5},{t:Date.now()-2000,v:4}],halts:[],urges:[],nights:[],relapses:[],screenings:[],stepWorks:[],
      meaningChecks:[],smartWorks:[{id:'restore-self',kind:'abc',role:'self',ts:1,updatedAt:1}],familySmartWorks:[{id:'restore-family',kind:'abc',role:'family',ts:2,updatedAt:2}],
      familyMoods:[{t:Date.now()-1000,v:1}],familyHalts:[{t:Date.now()-900,v:['l']}],familyNights:[],familyScreenings:[{id:'nds-bv',t:Date.now()-800,score:1,level:'참고'}],
      habits:[{id:'self-h',name:'self',start:daysAgo(1),done:[daysAgo(0)]}],familyHabits:[{id:'fam-h',name:'family',start:daysAgo(1),done:[daysAgo(0)]}],
      eats:[],eatLog:[],sleep:{on:0,bed:'23:00',up:'07:00'},sleepLog:[],familyEats:[{s:'점심',t:'12:30'}],familyEatLog:[{t:Date.now()-700,n:'점심'}],familySleep:{on:1,bed:'22:30',up:'07:00'},familySleepLog:[{t:Date.now()-600,q:'good'}],
      familyStepWorks:[],medLog:[]};
    const oldRaw=JSON.stringify(old);
    await imCtx.addInitScript(raw=>localStorage.setItem('ohg.v1',raw),oldRaw);
    await imPg.goto('http://localhost:8899/index.html'); await imPg.waitForTimeout(250);
    await imPg.setInputFiles('#me-file',{name:'oneul-backup.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(incoming))});
    await imPg.waitForTimeout(80);
    assert(await imPg.isVisible('#import-yes'),'정상 백업은 교체 전 확인을 요청');
    await imPg.click('#import-yes'); await imPg.waitForTimeout(150);
    const result=await imPg.evaluate(()=>({
      goal:S.goal,moods:S.moods.length,familyMoods:S.familyMoods.length,familyScreenings:S.familyScreenings.length,
      selfHabits:S.habits.length,familyHabits:S.familyHabits.length,familyEats:S.familyEats.length,familySleepLog:S.familySleepLog.length,
      selfSmart:S.smartWorks.map(x=>x.id),familySmart:S.familySmartWorks.map(x=>x.id),
      backup:localStorage.getItem('ohg.v1.recovery-backup')
    }));
    assert(result.goal==='불러온 기록'&&result.moods===2,'정상 백업을 현재 상태로 복원');
    assert(result.familyMoods===1&&result.familyScreenings===1&&result.selfHabits===1&&result.familyHabits===1&&result.familyEats===1&&result.familySleepLog===1,'백업 복원 후 가족 역할별 생활·점검 저장소도 원위치에 복원');
    assert(result.selfSmart.join(',')==='restore-self'&&result.familySmart.join(',')==='restore-family','백업 복원 후 SMART 물리 저장소 분리 유지');
    assert(result.backup===oldRaw,'불러오기 전 현재 원문을 안전백업으로 보존');
    await imCtx.close();
  }

  // 저장 실패가 나면 메모리 S까지 새 백업으로 바뀌지 않고 기존 상태를 유지합니다.
  {
    const failCtx=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',timezoneId:'Asia/Seoul'});
    const failPg=await failCtx.newPage();
    const old={ver:1,dataSchema:6,started:true,role:'self',types:['alcohol'],dates:{alcohol:daysAgo(8)},goal:'롤백 원본',
      moods:[{t:Date.now(),v:3}],halts:[],urges:[],nights:[],relapses:[],screenings:[],stepWorks:[],meaningChecks:[],smartWorks:[],
      familyStepWorks:[],medLog:[],eatLog:[],sleepLog:[]};
    const incoming={ver:1,dataSchema:6,started:true,role:'self',types:['alcohol'],dates:{alcohol:daysAgo(2)},goal:'저장되면안됨',
      moods:[{t:Date.now(),v:5}],halts:[],urges:[],nights:[],relapses:[],screenings:[],stepWorks:[],meaningChecks:[],smartWorks:[],
      familyStepWorks:[],medLog:[],eatLog:[],sleepLog:[]};
    const oldRaw=JSON.stringify(old);
    await failCtx.addInitScript(raw=>localStorage.setItem('ohg.v1',raw),oldRaw);
    await failPg.goto('http://localhost:8899/index.html'); await failPg.waitForTimeout(250);
    await failPg.setInputFiles('#me-file',{name:'oneul-backup.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(incoming))});
    await failPg.waitForTimeout(80);
    await failPg.evaluate(()=>{
      const original=Storage.prototype.setItem;
      Storage.prototype.setItem=function(k,v){if(k==='ohg.v1')throw new DOMException('quota','QuotaExceededError');return original.call(this,k,v);};
    });
    await failPg.click('#import-yes'); await failPg.waitForTimeout(100);
    const state=await failPg.evaluate(()=>({goal:S.goal,raw:localStorage.getItem('ohg.v1')}));
    assert(state.goal==='롤백 원본'&&state.raw===JSON.stringify(old),'저장 실패 시 실행상태와 저장원문 모두 기존값 유지');
    assert((await failPg.$eval('#toast',e=>e.innerText)).includes('기존 기록은 그대로'),'저장 실패 롤백 안내');
    await failCtx.close();
  }

  // 현재 키가 없어도 두 번째 안전백업(quarantine)만 있으면 복구할 수 있습니다.
  {
    const qCtx=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',timezoneId:'Asia/Seoul'});
    const qPg=await qCtx.newPage();
    const q={ver:1,dataSchema:6,started:true,role:'self',types:['alcohol'],dates:{alcohol:daysAgo(15)},goal:'두번째 안전백업',
      moods:[{t:Date.now(),v:4}],halts:[],urges:[],nights:[],relapses:[],screenings:[],stepWorks:[],meaningChecks:[],smartWorks:[],
      familyStepWorks:[],medLog:[],eatLog:[],sleepLog:[]};
    await qCtx.addInitScript(raw=>localStorage.setItem('ohg.v1.recovery-quarantine',raw),JSON.stringify(q));
    await qPg.goto('http://localhost:8899/index.html'); await qPg.waitForTimeout(300);
    assert((await qPg.$eval('#modin',e=>e.innerText)).includes('두 번째 안전백업'),'quarantine-only 상태를 사용자에게 안내');
    assert(await qPg.isVisible('#recovery-use-quarantine'),'두 번째 안전백업 복구 버튼 표시');
    await qPg.click('#recovery-use-quarantine'); await qPg.waitForTimeout(150);
    assert(await qPg.evaluate(()=>S.goal)==='두번째 안전백업','두 번째 안전백업을 실제 개인 상태로 복구');
    assert(((await qPg.evaluate(()=>localStorage.getItem('ohg.v1')))||'').includes('두번째 안전백업'),'복구한 상태를 주 개인키에 저장');
    await qCtx.close();
  }

  // 전체 지우기는 현재 개인키와 두 안전백업만 지우고 커뮤니티 설정은 보존합니다.
  {
    const wCtx=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',timezoneId:'Asia/Seoul'});
    const wPg=await wCtx.newPage();
    const current={ver:1,dataSchema:6,started:true,role:'self',types:['alcohol'],dates:{},goal:'삭제대상',moods:[],halts:[],urges:[],
      nights:[],relapses:[],screenings:[],stepWorks:[],meaningChecks:[],smartWorks:[],familyStepWorks:[],medLog:[],eatLog:[],sleepLog:[]};
    await wCtx.addInitScript(raw=>{
      localStorage.setItem('ohg.v1',raw);
      localStorage.setItem('ohg.v1.recovery-backup',raw);
      localStorage.setItem('ohg.v1.recovery-quarantine',raw);
      localStorage.setItem('ohg.social.v1',JSON.stringify({schema:1,profile:{userId:'u1',nickname:'테스터'}}));
    },JSON.stringify(current));
    await wPg.goto('http://localhost:8899/index.html'); await wPg.waitForTimeout(250);
    await wPg.evaluate(()=>go('me'));
    await wPg.$eval('#me-wipe',el=>{
      const acc=el.closest('.acc'), head=acc&&acc.querySelector('.acc-h');
      if(head) head.click();
    });
    assert(await wPg.isVisible('#me-wipe'),'기록 관리 아코디언을 펼치면 전체 지우기 버튼이 보여야 함');
    await wPg.click('#me-wipe'); await wPg.click('#wipe-yes'); await wPg.waitForTimeout(100);
    const gone=await wPg.evaluate(()=>({
      p:localStorage.getItem('ohg.v1'),b:localStorage.getItem('ohg.v1.recovery-backup'),
      q:localStorage.getItem('ohg.v1.recovery-quarantine'),social:localStorage.getItem('ohg.social.v1'),
      familyEmpty:S.familyMoods.length===0&&S.familyHalts.length===0&&S.familyNights.length===0&&S.familyScreenings.length===0&&
        S.familyHabits.length===0&&S.familyEats.length===0&&S.familyEatLog.length===0&&S.familySleepLog.length===0&&S.familySmartWorks.length===0
    }));
    assert(gone.p===null&&gone.b===null&&gone.q===null,'전체 지우기는 개인 현재키와 안전백업 두 개를 모두 삭제');
    assert(gone.social!==null,'전체 지우기는 별도 커뮤니티 키를 삭제하지 않음');
    assert(gone.familyEmpty,'전체 지우기 후 메모리의 가족 역할별 저장소도 모두 빈 상태로 초기화');
    await wCtx.close();
  }

  // 자원시트 URL은 http/https만 화면 링크로 허용합니다.
  {
    const uCtx=await b.newContext({viewport:{width:390,height:844},locale:'ko-KR',timezoneId:'Asia/Seoul'});
    const uPg=await uCtx.newPage();
    await uPg.goto('http://localhost:8899/index.html'); await uPg.waitForTimeout(200);
    const urlGuard=await uPg.evaluate(()=>({
      bad:safeHttpUrl_('javascript:alert(1)'),
      data:safeHttpUrl_('data:text/html,x'),
      good:safeHttpUrl_('https://example.com/x'),
      card:card({n:'테스트',d:'설명',w:'javascript:alert(1)'},'center',false)
    }));
    assert(urlGuard.bad===''&&urlGuard.data===''&&urlGuard.good==='https://example.com/x','외부 링크 scheme은 http/https만 허용');
    assert(!urlGuard.card.includes('javascript:'),'자원 카드에 비허용 scheme 링크를 만들지 않음');
    await uCtx.close();
  }

  await pg.goto('http://localhost:8899/index.html');
  await pg.waitForTimeout(500);
  console.log('1. 첫 화면 =', await seen());
  await shot('1-intro');

  // 온보딩: 알코올 + 도박
  await pg.click('#ob-types button:nth-child(1)');
  await pg.click('#ob-types button:nth-child(2)');
  await pg.waitForTimeout(150);
  // 시작일을 40일 전으로
  const d40 = daysAgo(40), d12 = daysAgo(12);
  const ins = await pg.$$('#ob-dates input');
  await ins[0].fill(d40);
  await ins[1].fill(d12);
  assert(await pg.isChecked('#ob-recovery-home'), '최초 설정에서 홈 회복일 표시는 기본 ON');
  assert(await pg.isChecked('#ob-ai-use'), '최초 설정에서 마음프로 AI 사용은 기본 ON');
  await pg.check('#ob-privacy');
  await shot('2-onboard');
  await pg.click('#ob-go');
  await pg.waitForTimeout(300);
  console.log('2. 시작 후 =', await seen());
  assert(await pg.evaluate(()=>S.viewMode==='simple'&&document.body.classList.contains('simple-view')),'신규 설치는 간단히 보기로 시작');
  assert(await pg.$('#home-daily')&&await pg.$('#home-quote'),'간단히 보기에서도 숨김 대상 DOM은 유지');
  assert(await pg.$eval('#home-daily',e=>getComputedStyle(e).display==='none')&&await pg.$eval('#home-quote',e=>getComputedStyle(e).display==='none'),'간단히 보기에서는 매일의 명상·오늘의 문장만 숨김');
  const recoveryText = (await pg.$eval('#home-days', e => e.innerText)).replace(/\n/g, ' | ');
  console.log('   회복일 =', recoveryText);
  const recoveryCompact = recoveryText.replace(/\s*\|\s*/g, '').replace(/\s+/g, '');
  assert(recoveryCompact.includes('41일째'), '40일 전 시작은 오늘 41일째여야 함');
  assert(recoveryCompact.includes('13일째'), '12일 전 시작은 오늘 13일째여야 함');
  const dayRule = await pg.evaluate(() => ({
    start: recoveryDay(today(), today()),
    fixed: recoveryDay('2026-08-31', '2026-09-02'),
    before: ymd(new Date('2026-09-01T23:59:59+09:00')),
    after: ymd(new Date('2026-09-02T00:00:00+09:00'))
  }));
  console.log('   날짜 경계 =', dayRule);
  assert(dayRule.start === 1, '회복 시작 당일은 1일째');
  assert(dayRule.fixed === 3, '8/31 시작이면 9/2는 3일째');
  assert(dayRule.before === '2026-09-01' && dayRule.after === '2026-09-02', '한국시간 자정에서 날짜가 바뀌어야 함');
  console.log('   매일의 명상 =', (await pg.$eval('#home-daily-text', e => e.innerText)).slice(0, 80));

  // 홈 오늘 일정 — 기본보기는 지금 확인할 것만, 전체보기에는 잠자리를 static 안내 행으로 포함
  const scheduleFocus = await pg.evaluate(() => {
    S.eats = [{s:'아침',t:'08:00'},{s:'점심',t:'12:30'},{s:'저녁',t:'18:30'}];
    const sample = [
      {kind:'habit',id:'done-habit',time:'08:00',done:true,action:1},
      {kind:'med',id:'아침',time:'08:00',done:false,action:1},
      {kind:'med',id:'점심',time:'12:30',done:true,action:1},
      {kind:'eat',id:'아침',time:'08:00',done:false,action:1},
      {kind:'eat',id:'점심',time:'12:30',done:false,action:1},
      {kind:'eat',id:'저녁',time:'18:30',done:false,action:1},
      {kind:'sleep',id:'bed',time:'23:00',done:false,action:0}
    ];
    return homeTodayFocusItems(sample, 13*60).map(x=>x.kind+':'+x.id);
  });
  console.log('   오늘 일정 기본 필터 =', scheduleFocus.join(', '));
  assert(!scheduleFocus.includes('eat:아침'), '점심 시간이 지나면 미완료 아침식사도 기본보기에서 접어야 함');
  assert(scheduleFocus.includes('med:아침'), '시간이 지난 미완료 복약은 기본보기에서 계속 보여야 함');
  assert(!scheduleFocus.includes('med:점심') && !scheduleFocus.includes('habit:done-habit'), '완료한 복약·습관은 기본보기에서 접어야 함');
  assert(scheduleFocus.includes('eat:점심') && scheduleFocus.includes('eat:저녁'), '현재·다음 끼니는 기본보기에서 보여야 함');
  assert(!scheduleFocus.includes('sleep:bed'), '잠자리는 기본보기에서 제외해야 함');

  await pg.evaluate(() => {
    const t=treatmentCfg(); t.medOn=1; t.outpatientOn=0;
    S.meds=MEDSLOT.map(x=>({s:x.k,t:x.d})); S.medLog=[]; S.eats=[]; S.eatLog=[]; S.sleep={on:0,bed:'23:00',up:'07:00'};
    homeTodayExpanded=false; drawTodayScheduleHome();
  });
  assert((await pg['$$eval']('#home-today .today-row',a=>a.length))===3,'간단히 보기에서는 오늘 일정이 최대 3개만 먼저 보여야 함');
  assert(await pg.isVisible('#home-today-more'),'간단히 보기에서 숨은 일정은 펼쳐 볼 수 있어야 함');
  await pg.click('#home-today-more'); await pg.waitForTimeout(80);
  assert((await pg['$$eval']('#home-today .today-row',a=>a.length))>=4,'전체 펼치기에서는 등록된 일정을 모두 확인 가능');
  await pg.evaluate(()=>{ treatmentCfg().medOn=0; S.meds=[]; homeTodayExpanded=false; drawTodayScheduleHome(); });

  await pg.evaluate(() => {
    S.eats = [{s:'아침',t:'08:00'},{s:'점심',t:'12:30'},{s:'저녁',t:'18:30'}];
    S.eatLog = [];
    S.sleep = {on:1,bed:'23:00',up:'07:00'};
    S.sleepLog = [{t:Date.now(),q:'good'}];
    homeTodayExpanded = true;
    drawTodayScheduleHome();
  });
  const fullScheduleText = await pg.$eval('#home-today', e => e.innerText);
  assert(fullScheduleText.includes('아침 식사') && fullScheduleText.includes('점심 식사') && fullScheduleText.includes('저녁 식사'), '전체보기에는 오늘 등록된 식사 일정이 보여야 함');
  assert(fullScheduleText.includes('잠자리'), '전체보기에는 오늘 잠자리 설정도 보여야 함');
  const fullSleepStatic = await pg.$eval('#home-today', e => [...e.querySelectorAll('.today-row')].some(r => r.innerText.includes('잠자리') && r.querySelector('.tcheck.static')));
  assert(fullSleepStatic, '전체보기의 잠자리는 체크 버튼이 없는 static 안내 행이어야 함');
  await pg.evaluate(() => {
    S.eats=[]; S.eatLog=[]; S.sleep={on:0,bed:'23:00',up:'07:00'}; S.sleepLog=[];
    homeTodayExpanded=false; save(); drawTodayScheduleHome();
  });

  // 선택형 회복일 + 별도 금연 실천 홈 표시
  await pg.evaluate(() => {
    S.recoveryHome = 1;
    S.smoking = { mode:'quit', start:today(), plan:'' };
    save(); drawHome();
  });
  const dual = await pg.$eval('#home-days', e => ({dual:e.classList.contains('dual'), text:e.innerText.replace(/\n/g,' | ')}));
  console.log('   회복+금연 2열 =', dual.text);
  assert(dual.dual, '회복일과 금연일이 모두 있으면 홈이 2열이어야 함');
  assert(dual.text.includes('금연') && dual.text.includes('1일째'), '금연 시작 당일은 금연 1일째로 보여야 함');

  const d5 = daysAgo(-5);
  await pg.evaluate(plan => {
    S.recoveryHome = 0;
    S.smoking = { mode:'plan', start:'', plan:plan };
    save(); drawHome();
  }, d5);
  const smokeOnly = await pg.$eval('#home-days', e => ({dual:e.classList.contains('dual'), text:e.innerText.replace(/\n/g,' | ')}));
  console.log('   금연예정 1열 =', smokeOnly.text);
  assert(!smokeOnly.dual && smokeOnly.text.includes('D-5'), '회복일을 숨기면 금연 예정만 기존 1열로 보여야 함');
  assert(!smokeOnly.text.includes('단주'), '홈 회복일 숨기기에서는 회복일 행이 보이면 안 됨');

  const recordStart = daysAgo(9);
  await pg.evaluate(recordStart => {
    S.recordStart = recordStart;
    S.dates.alcohol = '';
    S.dates.gambling = '';
    S.reclaim = { kind:'alcohol', timeOn:1, timePerDay:2, costOn:1, costPerDay:10000 };
    save(); drawReclaim();
  }, recordStart);
  const reclaimFallback = (await pg.$eval('#rec-reclaim', e => e.innerText)).replace(/\n/g,' | ');
  console.log('   시작일 미설정 되찾은 것 =', reclaimFallback.slice(0,180));
  assert(reclaimFallback.includes('기록 기간') && reclaimFallback.includes('10일'), '회복 시작일이 없으면 앱 기록 시작일부터 기록 기간을 계산해야 함');
  assert(reclaimFallback.includes('앱 기록 시작일부터'), '회복 시작일 미설정 계산 기준을 명확히 표시해야 함');

  await pg.evaluate(({d40,d12}) => {
    S.dates.alcohol = d40;
    S.dates.gambling = d12;
    S.recoveryHome = 1;
    S.smoking = { mode:'', start:'', plan:'' };
    S.reclaim = { kind:'', timeOn:0, timePerDay:0, costOn:0, costPerDay:0 };
    save(); drawHome(); drawReclaim();
  }, {d40,d12});

  // HALT + 감정
  await pg.click('#home-halt button:nth-child(1)');
  await pg.click('#home-halt button:nth-child(3)');
  await pg.click('#home-mood button:nth-child(4)');
  await pg.waitForTimeout(200);
  console.log('3. HALT 팁 =', (await pg.$eval('#halt-tip', e => e.innerText)).slice(0, 40));
  assert((await pg.$eval('#toast',e=>e.textContent)).includes('저장했어요. 나중에 내 회복요약에서 다시 볼 수 있어요.'),'기분 저장 후 회복요약 안내 표시');
  await pg.click('#halt-act button'); await pg.waitForTimeout(80);
  assert((await pg.$eval('#toast',e=>e.textContent)).includes('저장했어요. 나중에 내 회복요약에서 다시 볼 수 있어요.'),'HALT 저장 후 같은 회복요약 안내 표시');
  assert(await pg.evaluate(()=>S.halts.length>0&&S.moods.length>0),'기분·HALT 기록은 정상 저장');
  assert(await pg.isVisible('#home-review'),'당사자 홈에는 작은 내 기록 돌아보기 링크 표시');
  const reviewLabels=await pg.evaluate(()=>{
    const t=treatmentCfg(); t.outpatientOn=1; t.intervalDays=0;
    t.nextVisit=addYmd(today(),1); drawHome(); const d1=$('#home-review').textContent;
    t.nextVisit=today(); drawHome(); const d0=$('#home-review').textContent;
    t.nextVisit=addYmd(today(),2); drawHome(); const d2=$('#home-review').textContent;
    t.outpatientOn=0; t.nextVisit=''; drawHome();
    return {d1,d0,d2};
  });
  assert(reviewLabels.d1.includes('내일 외래 일정이 있어요')&&reviewLabels.d0.includes('오늘 외래 일정이 있어요')&&reviewLabels.d2==='내 기록 돌아보기 →','외래 D-1/D-0에만 회복요약 링크 보조문구 변경');
  await pg.click('#home-review'); await pg.waitForTimeout(100);
  assert((await seen())==='p-recovery-summary','홈 링크는 내 회복요약으로 한 번에 진입');
  const summaryText=await pg.$eval('#p-recovery-summary',e=>e.innerText);
  assert(summaryText.includes('최근 4주 · 최근 상태'),'회복요약은 최근 4주를 최근 상태로 설명');
  assert(summaryText.includes('최근 90일 기록에서 함께 나타난 흐름'),'90일 반복 흐름을 함께 나타난 기록으로 설명');
  assert(summaryText.includes('함께 나타난 것일 뿐, 원인이나 위험 판정이 아닙니다.'),'90일 반복 흐름은 원인·위험 판정이 아님을 명시');
  assert(summaryText.includes('상담 때 보여주기')&&await pg.isVisible('#summary-consult'),'회복요약 안에 상담 때 보여주기 선택 카드 표시');
  const emptySummaryText=await pg.evaluate(()=>{
    const keep={
      urges:S.urges,halts:S.halts,moods:S.moods,sleepLog:S.sleepLog,relapses:S.relapses,habits:S.habits,hours:S.hours
    };
    S.urges=[]; S.halts=[]; S.moods=[]; S.sleepLog=[]; S.relapses=[]; S.habits=[]; S.hours=[];
    drawRecoverySummary();
    const txt=$('#summary-patterns').innerText;
    Object.assign(S,keep); drawRecoverySummary();
    return txt;
  });
  assert(emptySummaryText.includes('원할 때 홈에서 짧게 남겨보세요. 남긴 내용이 이곳에 모입니다.'),'반복 흐름 기록 부족 시 기록 초대 안내');
  await pg.click('#summary-consult'); await pg.waitForTimeout(80);
  assert(await pg.evaluate(()=>document.body.classList.contains('summary-consult')),'상담 보여주기는 눌렀을 때만 표시 모드');
  await pg.click('#summary-consult-exit'); await pg.waitForTimeout(50);
  await pg.evaluate(()=>{ S.role='family'; drawHome(); });
  assert(await pg.$eval('#home-review',e=>getComputedStyle(e).display==='none'),'가족모드에는 내 기록 돌아보기 링크를 두지 않음');
  await pg.evaluate(()=>{ S.role='self'; save(); go('home'); drawHome(); });
  await shot('3-home');

  // 위기 분기
  await pg.click('#panic');
  await pg.waitForTimeout(200);
  console.log('4. 위기 분기 =', await seen());
  assert(await pg.isVisible('#pk-mindrx'), '위기 화면에 마음 처방전 카드가 보여야 함');
  assert(await pg.isVisible('#go-read') && await pg.isVisible('#go-listen'), '마음 처방전에 도움글·듣는 글 버튼이 보여야 함');
  const panicOrder = await pg.$$eval('#p-panic > *', els => els.map(e => e.id).filter(Boolean));
  assert(panicOrder.indexOf('pk-urge') < panicOrder.indexOf('pk-mindrx') && panicOrder.indexOf('pk-mindrx') < panicOrder.indexOf('pk-with') && panicOrder.indexOf('pk-with') < panicOrder.indexOf('pk-life'), '위기 도움 순서가 충동→마음 처방전→몸 이상→죽고 싶어요여야 함');
  await shot('4-panic');

  // 금단 모달
  await pg.click('#pk-with');
  await pg.waitForTimeout(250);
  console.log('5. 금단 모달 tel =', await pg.$$eval('#modin a', a => a.map(x => x.getAttribute('href')).join(', ')));
  await shot('5-withdrawal');
  await pg.evaluate(() => closeModal()); await pg.waitForTimeout(200);

  // 자살위기 모달
  await pg.click('#pk-life'); await pg.waitForTimeout(250);
  console.log('6. 위기 모달 tel =', await pg.$$eval('#modin a', a => a.map(x => x.getAttribute('href')).join(', ')));
  await pg.evaluate(() => closeModal()); await pg.waitForTimeout(200);

  // 충동 대응
  await pg.click('#pk-urge'); await pg.waitForTimeout(250);
  console.log('7. 충동 화면 =', await seen());
  await pg.fill('#ur-r', '8');
  await pg.$eval('#ur-r', e => e.dispatchEvent(new Event('input', { bubbles: true })));
  await pg.click('#ur-th button:nth-child(1)');
  await pg.click('#ur-th button:nth-child(4)');
  await shot('6-urge');

  // 타이머 — 시간을 앞당겨 종료시킨다
  await pg.click('#ur-start'); await pg.waitForTimeout(400);
  console.log('8. 타이머 =', await seen(), '|', await pg.$eval('#tm-t', e => e.textContent));
  await pg.click('#tm-breath'); await pg.waitForTimeout(300);
  console.log('   호흡 =', await pg.$eval('#bc', e => e.textContent), await pg.$eval('#bc', e => e.className));
  await shot('7-timer');

  await pg.evaluate(() => { tm.end = Date.now() + 400; });
  await pg.waitForTimeout(1200);
  console.log('9. 종료 화면 =', await seen(), '|', await pg.$eval('#af-h', e => e.textContent));

  await pg.fill('#af-r', '3');
  await pg.$eval('#af-r', e => e.dispatchEvent(new Event('input', { bubbles: true })));
  await pg.waitForTimeout(150);
  console.log('   비교문 =', (await pg.$eval('#af-cmp', e => e.innerText)).slice(0, 46));
  await shot('8-after');
  await pg.click('#af-done'); await pg.waitForTimeout(300);
  console.log('10. 마친 후 =', await seen());

  // 자기 전
  await pg.click('#go-night'); await pg.waitForTimeout(250);
  await pg.click('#ni-mood button:nth-child(2)');
  await pg.click('#ni-urge button:nth-child(2)');
  await pg.click('#ni-kept button:nth-child(1)');
  await pg.fill('#ni-note', '오늘은 잘 넘겼다');
  await shot('9-night');
  await pg.click('#ni-save'); await pg.waitForTimeout(180);
  // 칭찬 항목을 고르지 않은 경우 현재 UI는 저장 전 확인 모달을 한 번 보여줍니다.
  if (await pg.isVisible('#ni-skip').catch(() => false)) {
    await pg.click('#ni-skip'); await pg.waitForTimeout(220);
  }
  console.log('11. 자기 전 저장 후 =', await seen());

  // 가짜 데이터 넣고 통계 확인
  await pg.evaluate(() => {
    const now = Date.now();
    for (let i = 0; i < 22; i++) {
      const t = now - Math.floor(Math.random() * 20) * 86400000;
      const d = new Date(t); d.setHours([19,20,21,20,22,15,20][i % 7], 30);
      const b = 4 + Math.floor(Math.random() * 6);
      S.urges.push({ t: d.getTime(), type: 'alcohol', b: b, a: Math.max(0, b - 1 - Math.floor(Math.random()*3)),
        sec: 300 + Math.floor(Math.random()*900),
        th: [['딱 한 잔만','이번 한 번만','괜찮을 것 같다','나는 조절할 수 있다'][i % 4]] });
      S.halts.push({ t: d.getTime(), v: [['h'],['l','t'],['a'],['l'],['t','l']][i % 5] });
      S.moods.push({ t: now - i * 86400000, v: 1 + (i * 3) % 5 });
      if (i % 5 === 0) S.nights.push({ t: now - i * 86400000, m: 3, u: 1, k: 1, n: '' });
    }
    S.relapses.push({ t: now - 12 * 86400000, type: 'gambling', halt: ['l','t'], n: '혼자 있는 밤에 무너졌다' });
    save();
  });

  // 회복도구 — Q&A 224문답은 AI 없이 로컬에서 검색
  const toolErrBefore = errs.length;
  await pg.click('#tabs button[data-t="tools"]'); await pg.waitForTimeout(250);
  assert(errs.length === toolErrBefore, '회복도구 진입 시 JavaScript 오류가 없어야 함');
  assert(await pg.isVisible('#tool-qa'), '하단 회복도구가 열려야 함');
  assert(await pg.isVisible('#tool-listen'), '회복도구에 듣는 글 메뉴가 보여야 함');
  assert((await pg.$eval('#tool-meaning-check-direct b', e => e.textContent.trim())) === '의미점검', '의미점검 메뉴 이름이 자가점검 기록과 구분되어야 함');
  assert((await pg.$eval('#tool-check-view b', e => e.textContent.trim())) === '자가점검 기록', '자가점검 결과 조회 메뉴 이름이 명확해야 함');

  const meaningDay = daysAgo(1), meaningCheckDay = daysAgo(2), familyMeaningDay = daysAgo(3), familyMeaningCheckDay = daysAgo(4);
  await pg.evaluate(({meaningDay,meaningCheckDay}) => {
    S.wbDays = S.wbDays && typeof S.wbDays === 'object' && !Array.isArray(S.wbDays) ? S.wbDays : {};
    S.wbDays[meaningDay] = { hard:[], strength:[], action:[], request:'내가 지킬 한 걸음', ts:Date.now()-86400000 };
    S.meaningChecks = [{ d:meaningCheckDay, ts:Date.now()-172800000, answers:Array(10).fill(2), total:20, domains:{self:2,future:2,choice:2,relation:2} }];
    save(); recTab='work'; recPracticeFilter='meaning'; go('rec');
  }, {meaningDay,meaningCheckDay});
  await pg.waitForTimeout(180);
  const meaningTrailText = await pg.$eval('#rec-body', e => e.innerText);
  assert(meaningTrailText.includes('저장한 의미 기록 2건'), '당사자 내 발자취 의미 필터에 두 종류 의미 기록이 함께 보여야 함');
  assert(meaningTrailText.includes('의미 돌아보기') && meaningTrailText.includes('내가 지킬 한 걸음'), '당사자 의미 돌아보기 기존 기록을 내 발자취에서 읽어야 함');
  assert(meaningTrailText.includes('의미회복 간편점검') && meaningTrailText.includes('20/40'), '당사자 의미회복 간편점검 기존 결과를 내 발자취에서 읽어야 함');
  await pg.locator('#rec-body button.toolcard').filter({hasText:'의미회복 간편점검'}).click();
  await pg.waitForTimeout(100);
  assert((await pg.$eval('#modin h2', e => e.textContent.trim())) === '의미점검 결과', '내 발자취의 의미점검 기록은 기존 결과 상세를 재사용해야 함');
  await pg.evaluate(() => closeModal());

  // 가족 의미영역 — UI 틀은 재사용하되 문항과 저장소는 당사자와 완전히 분리합니다.
  await pg.evaluate(() => { S.role='family'; save(); go('tools'); });
  await pg.waitForTimeout(150);
  assert(await pg.isVisible('#tool-meaning'), '가족모드 회복도구에도 의미 돌아보기가 보여야 함');
  assert(await pg.isVisible('#tool-meaning-check-direct'), '가족모드 회복도구에도 의미점검이 보여야 함');
  await pg.click('#tool-meaning'); await pg.waitForTimeout(120);
  assert((await seen()) === 'p-meaning', '가족모드에서 의미 돌아보기 화면이 열려야 함');
  const familyMeaningPage = await pg.$eval('#p-meaning', e => e.innerText);
  assert(familyMeaningPage.includes('오늘 내 마음, 경계, 자기돌봄'), '가족 의미 돌아보기는 가족 자신의 삶·경계 문구를 사용');
  assert(familyMeaningPage.includes('오늘의 부담감') && familyMeaningPage.includes('오늘 나를 힘들게 한 것은'), '가족용 오늘 돌아보기 문항이 표시');
  assert(!familyMeaningPage.includes('오늘 기록된 충동'), '가족 의미 돌아보기에는 당사자 충동기록을 참고자료로 노출하지 않음');
  await pg.fill('#mn-request','가족인 나의 삶을 지키기');
  await pg.click('#mn-save'); await pg.waitForTimeout(100);
  const familySaveState = await pg.evaluate(() => ({
    family:!!(S.familyWbDays&&S.familyWbDays[wbToday()]&&S.familyWbDays[wbToday()].request==='가족인 나의 삶을 지키기'),
    self:!!(S.wbDays&&S.wbDays[wbToday()]&&S.wbDays[wbToday()].request==='가족인 나의 삶을 지키기')
  }));
  assert(familySaveState.family&&!familySaveState.self, '가족 오늘 의미기록은 familyWbDays에만 저장');

  await pg.evaluate(({familyMeaningDay,familyMeaningCheckDay}) => {
    S.familyWbDays[familyMeaningDay] = { hard:['worry'], strength:['boundary'], action:['selfCare'], request:'가족 기록 전용 문장', ts:Date.now()-259200000 };
    S.familyMeaningChecks = [{ d:familyMeaningCheckDay, ts:Date.now()-345600000, answers:Array(10).fill(3), total:30, domains:{self:3,future:3,choice:3,relation:3} }];
    save(); recTab='work'; recPracticeFilter='meaning'; go('rec');
  }, {familyMeaningDay,familyMeaningCheckDay});
  await pg.waitForTimeout(150);
  const familyTrailText = await pg.$eval('#rec-body', e => e.innerText);
  assert(familyTrailText.includes('의미') && familyTrailText.includes('가족 기록 전용 문장') && familyTrailText.includes('30/40'), '가족 내 발자취 의미 필터가 가족 의미기록과 점검만 표시');
  assert(!familyTrailText.includes('내가 지킬 한 걸음') && !familyTrailText.includes('20/40'), '가족 내 발자취에 당사자 의미기록이 섞이지 않음');

  await pg.evaluate(() => openMeaningCheckDirect());
  await pg.waitForTimeout(80);
  assert((await pg.$eval('#mn-view-check', e => e.innerText)).includes('가족의 변화 여부가 아니라'), '가족 의미점검은 가족 자신의 상태·경계·자기돌봄을 안내');
  await pg.evaluate(() => { const d=mcNewDraft(); d.answers=Array(10).fill(2); mcCommitResult(d); });
  await pg.waitForTimeout(80);
  const familyCheckState = await pg.evaluate(() => ({family:S.familyMeaningChecks.length,self:S.meaningChecks.length,draft:S.familyMeaningCheckDraft}));
  assert(familyCheckState.family>=2 && familyCheckState.self===1 && familyCheckState.draft===null, '가족 의미점검 완료기록·초안은 가족 저장소에만 기록');

  await pg.evaluate(() => { S.role='self'; save(); recTab='work'; recPracticeFilter='meaning'; go('rec'); });
  await pg.waitForTimeout(120);
  const selfAgainText = await pg.$eval('#rec-body', e => e.innerText);
  assert(selfAgainText.includes('내가 지킬 한 걸음') && selfAgainText.includes('20/40'), '역할을 당사자로 돌리면 기존 당사자 의미기록을 그대로 다시 읽음');
  assert(!selfAgainText.includes('가족 기록 전용 문장') && !selfAgainText.includes('30/40'), '당사자 내 발자취에 가족 의미기록이 섞이지 않음');

  // DATA_SCHEMA 7 역할별 저장 완전 분리 — 자가점검 → 기분/HALT·하루마무리 → 습관·식사·수면 → SMART 순서로 검증
  await pg.evaluate(() => {
    S.screenings=[];S.familyScreenings=[];
    S.moods=[];S.familyMoods=[];S.halts=[];S.familyHalts=[];S.nights=[];S.familyNights=[];
    S.habits=[];S.familyHabits=[];
    S.eats=[];S.eatLog=[];S.sleep={on:0,bed:'23:00',up:'07:00'};S.sleepLog=[];
    S.familyEats=[];S.familyEatLog=[];S.familySleep={on:0,bed:'23:00',up:'07:00'};S.familySleepLog=[];
    S.smartWorks=[];S.familySmartWorks=[];S.role='self'; save(); go('home'); drawHome();
  });

  // ① 자가점검: 같은 도구를 두 역할에서 저장해도 서로의 이력에 섞이지 않아야 함
  await pg.evaluate(() => {
    screeningStore().push({id:'pgsi',t:Date.now()-2000,score:2,level:'당사자 전용'});
    S.role='family';
    screeningStore().push({id:'nds-bv',t:Date.now()-1000,score:1,level:'가족 전용'});
    save();
  });
  const screenSplit=await pg.evaluate(()=>({
    self:S.screenings.map(x=>x.id),family:S.familyScreenings.map(x=>x.id),
    familyHistory:screenHistory('nds-bv').length,selfPgsiHidden:screenHistory('pgsi').length
  }));
  assert(screenSplit.self.join(',')==='pgsi'&&screenSplit.family.join(',')==='nds-bv'&&screenSplit.familyHistory===1&&screenSplit.selfPgsiHidden===0,'① 자가점검 저장·이력 조회가 역할별 물리 저장소에서 완전 분리');

  // ② 기분/HALT: 실제 홈 버튼으로 각각 저장
  await pg.evaluate(()=>{S.role='self';save();go('home');drawHome();});
  await pg.click('#home-mood button:nth-child(5)');
  await pg.click('#home-halt button:nth-child(1)'); await pg.click('#halt-act button'); await pg.waitForTimeout(50);
  await pg.evaluate(()=>{drawNight();night={mood:1,urge:0,kept:1,praise:['hold']};$('#ni-note').value='SELF-NIGHT';$('#ni-save').click();});
  await pg.waitForTimeout(60);
  await pg.evaluate(()=>{S.role='family';save();go('home');drawHome();});
  assert((await pg.$eval('#mood-st',e=>e.innerText)).includes('아직 기록이 없습니다'),'② 가족모드 홈은 당사자 기분기록을 읽지 않음');
  await pg.click('#home-mood button:nth-child(1)');
  await pg.click('#home-halt button:nth-child(3)'); await pg.click('#halt-act button'); await pg.waitForTimeout(50);
  await pg.evaluate(()=>{drawNight();night={mood:5,urge:2,kept:1,praise:['hold']};$('#ni-note').value='FAMILY-NIGHT';$('#ni-save').click();});
  await pg.waitForTimeout(60);
  const emotionSplit=await pg.evaluate(()=>({
    selfMood:S.moods.map(x=>x.v),familyMood:S.familyMoods.map(x=>x.v),
    selfHalt:S.halts.map(x=>x.v.join('')),familyHalt:S.familyHalts.map(x=>x.v.join('')),
    selfNight:S.nights.map(x=>x.n),familyNight:S.familyNights.map(x=>x.n),
    familyUrge:S.familyNights.map(x=>x.u)
  }));
  assert(emotionSplit.selfMood.length===2&&emotionSplit.selfMood.every(v=>v===1)&&emotionSplit.familyMood.length===2&&emotionSplit.familyMood.every(v=>v===5),'② 당사자·가족 기분 저장 완전 분리');
  assert(emotionSplit.selfHalt.join(',')==='h'&&emotionSplit.familyHalt.join(',')==='l','② 당사자·가족 HALT 저장 완전 분리');
  assert(emotionSplit.selfNight.join(',')==='SELF-NIGHT'&&emotionSplit.familyNight.join(',')==='FAMILY-NIGHT'&&emotionSplit.familyUrge.every(v=>v==null),'② 하루마무리 저장 완전 분리 + 가족 충동값 비저장');

  // ③ 습관·식사·수면: 역할별 설정·체크 및 홈 일정 조회
  await pg.evaluate(()=>{
    S.role='self';S.habits=[];S.familyHabits=[];S.eats=[];S.eatLog=[];S.sleep={on:0,bed:'23:00',up:'07:00'};S.sleepLog=[];
    S.familyEats=[];S.familyEatLog=[];S.familySleep={on:0,bed:'23:00',up:'07:00'};S.familySleepLog=[];
    habitList().push({id:'self-h',name:'SELF-HABIT',days:0,freq:'daily',weekdays:[0,1,2,3,4,5,6],check:'SELF-CHECK',notify:0,time:'18:00',start:today(),done:[today()]});
    eatPlanStore().push({s:'아침',t:'08:00'});eatLogStore().push({t:Date.now(),n:'아침'});sleepStore().on=1;sleepLogStore().push({t:Date.now(),q:'good'});
    S.role='family';
    habitList().push({id:'family-h',name:'FAMILY-HABIT',days:0,freq:'daily',weekdays:[0,1,2,3,4,5,6],check:'FAMILY-CHECK',notify:0,time:'19:00',start:today(),done:[]});
    eatPlanStore().push({s:'점심',t:'12:30'});eatLogStore().push({t:Date.now(),n:'점심'});sleepStore().on=1;sleepStore().bed='22:30';sleepLogStore().push({t:Date.now(),q:'bad'});save();drawTodayScheduleHome();
  });
  const familySchedule=await pg.$eval('#home-today',e=>e.innerText);
  assert(familySchedule.includes('FAMILY-HABIT')&&!familySchedule.includes('SELF-HABIT')&&familySchedule.includes('점심 식사')&&!familySchedule.includes('아침 식사'),'③ 가족 홈 일정은 가족 습관·식사만 조회');
  const lifeSplit=await pg.evaluate(()=>({
    selfHabit:S.habits.map(x=>x.name),familyHabit:S.familyHabits.map(x=>x.name),
    selfEats:S.eats.map(x=>x.s),familyEats:S.familyEats.map(x=>x.s),
    selfEatLog:S.eatLog.map(x=>x.n),familyEatLog:S.familyEatLog.map(x=>x.n),
    selfSleep:S.sleepLog.map(x=>x.q),familySleep:S.familySleepLog.map(x=>x.q),
    payload:nativeReminderPayload()
  }));
  assert(lifeSplit.selfHabit.join(',')==='SELF-HABIT'&&lifeSplit.familyHabit.join(',')==='FAMILY-HABIT','③ 습관 저장소 완전 분리');
  assert(lifeSplit.selfEats.join(',')==='아침'&&lifeSplit.familyEats.join(',')==='점심'&&lifeSplit.selfEatLog.join(',')==='아침'&&lifeSplit.familyEatLog.join(',')==='점심','③ 식사 설정·체크 저장소 완전 분리');
  assert(lifeSplit.selfSleep.join(',')==='good'&&lifeSplit.familySleep.join(',')==='bad','③ 수면 기록 저장소 완전 분리');
  assert(lifeSplit.payload.eats.includes('noon@12:30')&&!lifeSplit.payload.eats.includes('am@08:00')&&lifeSplit.payload.bed==='22:30'&&lifeSplit.payload.habits.includes('family-h'),'③ Android 생활알림 payload도 현재 가족 역할의 습관·식사·수면만 사용');

  // ④ SMART: 한 배열 role 필터가 아니라 물리 저장소 자체를 분리
  await pg.evaluate(()=>{
    S.role='self';smartWorksStore().push({id:'self-smart',kind:'abc',role:'self',ts:Date.now()-100,updatedAt:Date.now()-100,a:'SELF-SMART'});
    S.role='family';smartWorksStore().push({id:'family-smart',kind:'abc',role:'family',ts:Date.now(),updatedAt:Date.now(),a:'FAMILY-SMART'});
    save();recTab='work';recPracticeFilter='smart';go('rec');
  });
  await pg.waitForTimeout(80);
  const familySmartTrail=await pg.$eval('#rec-body',e=>e.innerText);
  assert(familySmartTrail.includes('FAMILY-SMART')&&!familySmartTrail.includes('SELF-SMART'),'④ 가족 내 발자취는 familySmartWorks만 읽음');
  await pg.evaluate(()=>{S.role='self';save();recTab='work';recPracticeFilter='smart';go('rec');}); await pg.waitForTimeout(80);
  const selfSmartTrail=await pg.$eval('#rec-body',e=>e.innerText);
  assert(selfSmartTrail.includes('SELF-SMART')&&!selfSmartTrail.includes('FAMILY-SMART'),'④ 당사자 내 발자취는 smartWorks만 읽음');
  const physicalSmartSplit=await pg.evaluate(()=>({self:S.smartWorks.map(x=>x.id),family:S.familySmartWorks.map(x=>x.id)}));
  assert(physicalSmartSplit.self.join(',')==='self-smart'&&physicalSmartSplit.family.join(',')==='family-smart','④ SMART 기록이 두 물리 배열에 완전 분리');

  // 저장된 ohg.v1 자체에도 두 역할 저장소가 함께 존재하되 값은 섞이지 않아야 함
  const rawRoleSplit=await pg.evaluate(()=>JSON.parse(localStorage.getItem('ohg.v1')));
  assert(rawRoleSplit.dataSchema===7&&rawRoleSplit.screenings.length===1&&rawRoleSplit.familyScreenings.length===1&&rawRoleSplit.smartWorks.length===1&&rawRoleSplit.familySmartWorks.length===1,'역할별 저장소가 DATA_SCHEMA 7 백업 원본에 각각 독립 필드로 저장');

  // 앱 종료→재실행을 새 페이지로 시뮬레이션: 같은 브라우저 저장공간과 캐시에서 역할별 기록이 유지되어야 합니다.
  const coldRaw=await pg.evaluate(() => {
    const x=JSON.parse(JSON.stringify(S));
    x.role='family'; x.familyWbDays={}; x.familyMeaningChecks=[]; x.familyMeaningCheckDraft=null;
    return JSON.stringify(x);
  });
  const coldCtx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,locale:'ko-KR',timezoneId:'Asia/Seoul'});
  await coldCtx.addInitScript(raw=>{if(!localStorage.getItem('ohg.v1'))localStorage.setItem('ohg.v1',raw);},coldRaw);
  let coldPg=await coldCtx.newPage();
  const coldErrs=[]; coldPg.on('pageerror',e=>coldErrs.push(e.message));
  await coldPg.goto('http://localhost:8899/index.html'); await coldPg.waitForTimeout(650);
  assert(await coldPg.evaluate(()=>S.role==='family'),'cold-start 1차 실행에서 가족 역할 복구');
  await coldPg.evaluate(()=>go('meaning')); await coldPg.waitForTimeout(120);
  assert((await coldPg.$eval('.pg.on',e=>e.id))==='p-meaning','cold-start 1차 실행에서 가족 의미 돌아보기 진입');
  await coldPg.fill('#mn-request','재실행 뒤에도 남길 가족 의미기록');
  await coldPg.click('#mn-save'); await coldPg.waitForTimeout(120);
  assert(await coldPg.evaluate(()=>S.familyWbDays[wbToday()].request==='재실행 뒤에도 남길 가족 의미기록'),'cold-start 시뮬레이션용 가족 의미기록 저장');
  await coldPg.close();

  coldPg=await coldCtx.newPage();
  coldPg.on('pageerror',e=>coldErrs.push(e.message));
  await coldPg.goto('http://localhost:8899/index.html'); await coldPg.waitForTimeout(650);
  assert(await coldPg.evaluate(()=>S.role==='family'),'앱 종료 후 재실행에서도 가족 역할 유지');
  assert(await coldPg.evaluate(()=>S.familyWbDays[wbToday()]&&S.familyWbDays[wbToday()].request==='재실행 뒤에도 남길 가족 의미기록'),'앱 종료 후 재실행에서도 가족 의미기록 유지');
  const coldRoleSplit=await coldPg.evaluate(()=>({
    selfScreen:S.screenings.map(x=>x.id),familyScreen:S.familyScreenings.map(x=>x.id),
    selfMood:S.moods.map(x=>x.v),familyMood:S.familyMoods.map(x=>x.v),
    selfNight:S.nights.map(x=>x.n),familyNight:S.familyNights.map(x=>x.n),
    selfHabit:S.habits.map(x=>x.name),familyHabit:S.familyHabits.map(x=>x.name),
    selfEat:S.eats.map(x=>x.s),familyEat:S.familyEats.map(x=>x.s),
    selfSmart:S.smartWorks.map(x=>x.id),familySmart:S.familySmartWorks.map(x=>x.id)
  }));
  assert(coldRoleSplit.selfScreen.join(',')==='pgsi'&&coldRoleSplit.familyScreen.join(',')==='nds-bv','cold-start 후 자가점검 역할 분리 유지');
  assert(coldRoleSplit.selfNight.join(',')==='SELF-NIGHT'&&coldRoleSplit.familyNight.join(',')==='FAMILY-NIGHT','cold-start 후 기분/HALT·하루마무리 역할 분리 유지');
  assert(coldRoleSplit.selfHabit.join(',')==='SELF-HABIT'&&coldRoleSplit.familyHabit.join(',')==='FAMILY-HABIT'&&coldRoleSplit.selfEat.join(',')==='아침'&&coldRoleSplit.familyEat.join(',')==='점심','cold-start 후 습관·식사·수면 역할 분리 유지');
  assert(coldRoleSplit.selfSmart.join(',')==='self-smart'&&coldRoleSplit.familySmart.join(',')==='family-smart','cold-start 후 SMART 물리 분리 유지');
  await coldPg.evaluate(()=>go('tools')); await coldPg.waitForTimeout(100);
  await coldPg.click('#tool-meaning'); await coldPg.waitForTimeout(120);
  assert((await coldPg.$eval('.pg.on',e=>e.id))==='p-meaning','재실행 후 가족 의미 돌아보기 버튼이 정상 작동');
  if(await coldPg.isVisible('#mod.on').catch(()=>false)) await coldPg.evaluate(()=>closeModal());
  await coldPg.evaluate(()=>openMeaningCheckDirect()); await coldPg.waitForTimeout(100);
  assert((await coldPg.$eval('.pg.on',e=>e.id))==='p-meaning' && (await coldPg.$eval('#mn-view-check',e=>e.innerText)).includes('가족의 변화 여부가 아니라'),'재실행 후 가족 의미점검도 정상 작동');
  assert(coldErrs.length===0,'cold-start 재실행 시 JavaScript pageerror가 없어야 함');
  await coldCtx.close();

  await pg.evaluate(() => go('tools'));
  await pg.waitForTimeout(150);
  await pg.click('#tool-listen'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-listen', '회복도구의 듣는 글이 기존 듣는 글 화면을 열어야 함');
  assert(await pg.$eval('#tabs button[data-t="tools"]', e => e.classList.contains('on')), '회복도구에서 듣는 글을 열면 회복도구 탭 강조 유지');
  await pg.click('#ls-back'); await pg.waitForTimeout(120);
  assert((await seen()) === 'p-tools', '듣는 글에서 돌아가면 회복도구로 복귀');
  assert(!(await pg.$('#tool-share')), '회복도구에서 추천하기가 빠져야 함');
  assert(await pg.evaluate(() => Array.isArray(window.LEARNING_TOPICS) && window.LEARNING_TOPICS.length === 3), '회복학습은 3개 독립 주제를 learning-data.js에서 로드해야 함');
  await pg.click('#tool-learn'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-learn', '회복학습 목록 페이지가 열려야 함');
  assert((await pg.$$eval('#learn-list .help', a => a.length)) === 3, '회복학습 목록에는 12단계·회복의 기초 이해·SMART Recovery 3개가 있어야 함');
  const learnText = await pg.$eval('#learn-list', e => e.innerText);
  assert(learnText.includes('12단계'), '회복학습 목록에 12단계가 표시되어야 함');
  assert(learnText.includes('회복의 기초 이해'), '회복학습 목록에 심화 주제가 표시되어야 함');
  assert(learnText.includes('SMART Recovery'), '회복학습 목록에 SMART Recovery가 표시되어야 함');
  assert(!learnText.includes('12단계 점검'), '회복학습 목록에는 작성형 12단계 점검이 중복 표시되지 않아야 함');
  await pg.click('#learn-list .help'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-learn-topic', '12단계 선택 시 별도 주제 페이지가 열려야 함');
  assert((await pg.$eval('#learn-topic-title', e => e.innerText)) === '12단계', '주제 페이지 제목은 12단계');
  assert((await pg.$$eval('#learn-topic-sections .help', a => a.length)) === 14, '12단계 학습은 소개 + 기초 + 1~12단계 = 14개');
  assert((await pg.$eval('#learn-topic-sections', e => e.innerText)).includes('12단계의 기초'), '12단계의 기초가 추가되어야 함');
  await pg.evaluate(() => { S.role='self'; S.types=['alcohol']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)) === '우리는 알코올에 무력했으며, 우리의 삶을 수습할 수 없게 되었다는 것을 시인했다.', '알코올 영역 1단계 카드에 AA 단계문장 표시');
  await pg.evaluate(() => { S.types=['gambling']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)) === '우리는 도박에 무력하며 - 정상적으로 생활할 수 없게 되었음을 시인했습니다.', '도박 영역 1단계 카드에 GA 단계문장 표시');
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[5].innerText)).includes('도덕적, 재정적 목록'), '도박 영역 4단계 GA 재정적 목록 문장 표시');
  await pg.evaluate(() => { S.types=['drug']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)) === '우리는 중독에 무력했으며, 우리의 삶을 스스로 수습할 수 없게 되었다는 것을 시인했다.', '약물 영역 1단계 카드에 NA 단계문장 표시');
  await pg.evaluate(() => { S.types=['alcohol','drug']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)).startsWith('우리는 중독에 무력했으며'), '복수 회복영역은 중독 공통형 단계문장 표시');
  assert((await pg.$eval('#learn-topic-sections', e => e.innerText)).includes('공식 문안 자체가 아닙니다'), '복수 회복영역은 통합형 문안 안내 표시');
  await pg.evaluate(() => { S.role='family'; S.types=['alcohol']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)) === '우리는 알코올에 무력했으며, 우리의 삶을 수습할 수 없게 되었다는 것을 시인했다.', '가족모드도 같은 영역 단계문장 사용');
  await pg.evaluate(() => { S.types=['gambling']; drawLearnTopic(); });
  assert((await pg.$$eval('#learn-topic-sections .help .b span', a => a[2].innerText)).startsWith('우리는 도박에 무력하며'), '가족모드 도박도 같은 GA 단계문장 사용');
  assert(await pg.evaluate(() => window.FAMILY_TWELVE_STEP_PERSPECTIVES && Object.keys(FAMILY_TWELVE_STEP_PERSPECTIVES).length===14), '가족 12단계 소개·기초·1~12단계 해설 오버레이 14개 로드');
  await pg.evaluate(() => { S.types=['alcohol']; drawLearnTopic(); });
  const familyStep1Text = await pg.evaluate(() => {
    const topic=LEARNING.find(x=>x.id===learnState.topic) || LEARNING[0];
    const sec=(topic.sections||[]).find(x=>x.id==='step-1');
    const view=learningSectionPerspective(sec);
    return ((view&&view.body)||[]).join(' ');
  });
  assert(familyStep1Text.includes('그 사람의 중독을 내가 대신 멈추게 할 수 없었다'), '가족 1단계 해설이 가족 관점으로 표시');
  assert(await pg.evaluate(() => window.FAMILY_STEP_WORKSHEETS && Object.keys(FAMILY_STEP_WORKSHEETS).length===7), '가족 단계별 점검 7종 로드');
  await pg.evaluate(() => { S.role='self'; S.types=['alcohol']; drawLearnTopic(); save(); });
  await pg.click('#learn-topic-sections .help'); await pg.waitForTimeout(100);
  assert(await pg.isVisible('#mod.on'), '12단계 소개 상세 모달이 열려야 함');
  assert((await pg.$eval('#modin', e => e.innerText)).includes('잠시 멈추어 생각해보기'), '학습 상세에 생각해보기 영역이 있어야 함');
  await pg.click('#learn-modal-close'); await pg.waitForTimeout(80);
  assert(!(await pg.$eval('#p-learn-topic', e => e.innerText)).includes('Q&A'), '12단계 학습 페이지가 Q&A로 되돌아가지 않아야 함');
  await pg.click('#learn-topic-back');
  const learnCards=await pg.$$('#learn-list .help');
  await learnCards[1].click();
  assert((await pg.$eval('#learn-topic-title', e => e.innerText)) === '회복의 기초 이해', '심화학습 주제 페이지 제목');
  assert((await pg.$$eval('#learn-topic-sections .help', a => a.length)) === 4, '심화학습은 4개 섹션');
  const deepText=await pg.$eval('#learn-topic-sections', e => e.innerText);
  assert(deepText.includes('영·마음·몸') && deepText.includes('욕구에서 탐욕까지') && deepText.includes('두려움을') && deepText.includes('의미와 자기초월'), '심화학습 4개 핵심 영역 표시');
  await pg.click('#learn-topic-back'); await pg.waitForTimeout(100);
  await pg.click('#p-learn .sp button'); await pg.waitForTimeout(120);
  assert((await seen()) === 'p-tools', '회복학습에서 회복도구로 돌아갈 수 있어야 함');

  // V7.6 1·4·8·9단계 검토 + 10·11·12단계 매일 실천 — 초안 + 내 발자취 저장
  assert(await pg.evaluate(() => window.STEP_WORKSHEETS && ['step1','step4','step8','step9','step10','step11','step12'].every(k => STEP_WORKSHEETS[k])), '1·4·8·9·10·11·12단계 검토·실천 데이터 로드');
  await pg.evaluate(() => openWorkbook('step1','rec')); await pg.waitForTimeout(120);
  assert((await seen()) === 'p-workbook', '1단계 검토 작성 화면이 열려야 함');
  assert((await pg.$$eval('#wb-body details.ws-sec', a => a.length)) === 3, '1단계 검토는 무력함·수습할 수 없는 삶·상실과 애도 3개 시트');
  await pg.fill('#wb-body textarea', '조절하려 했지만 뜻대로 되지 않았던 경험'); await pg.waitForTimeout(380);
  assert(await pg.evaluate(() => S.stepDrafts.step1.sections.powerless[0].event.includes('조절하려')), '검토 작성 중 초안이 상태에 자동 저장');
  await pg.click('#wb-save-record'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-rec' && await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===1 && S.stepWorks[0].kind==='step1'), '1단계 검토를 내 발자취 상태에 저장');
  await pg.evaluate(() => openWorkbook('step4','rec')); await pg.waitForTimeout(120);
  assert((await pg.$$eval('#wb-body details.ws-sec', a => a.length)) === 8, '4단계 검토는 어휘 + 핵심·심화 7개 시트');
  await pg.fill('#wb-body textarea', '내가 놓지 못한 원한'); await pg.waitForTimeout(380);
  await pg.click('#wb-save-record'); await pg.waitForTimeout(180);
  assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===2 && S.stepWorks.some(x=>x.kind==='step4')), '4단계 검토도 내 발자취 상태에 저장');

  for(const [btn,kind,sections,text] of [
    ['#rec-wb8','step8',3,'보상할 명단 첫 기록'],
    ['#rec-wb9','step9',3,'직접 보상 전 안전 검토'],
    ['#rec-wb10','step10',3,'오늘 남은 감정적 숙취'],
    ['#rec-wb11','step11',3,'오늘의 연결 방식'],
    ['#rec-wb12','step12',3,'오늘 살고 싶은 원칙']
  ]){
    await pg.evaluate(k => openWorkbook(k,'rec'), kind); await pg.waitForTimeout(100);
    assert((await seen()) === 'p-workbook', kind+' 작성 화면이 열려야 함');
    const detailCount=await pg.$$eval('#wb-body details.ws-sec', a => a.length);
    const refs=await pg.evaluate(k => (STEP_WORKSHEETS[k].references||[]).length, kind);
    assert(detailCount === sections + (refs ? 1 : 0), kind+' 섹션/어휘 렌더 수 일치');
    await pg.fill('#wb-body textarea', text); await pg.waitForTimeout(360);
    await pg.click('#wb-save-record'); await pg.waitForTimeout(120);
  }
  assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===7 && ['step1','step4','step8','step9','step10','step11','step12'].every(k=>S.stepWorks.some(x=>x.kind===k))), '1·4·8·9·10·11·12단계 기록 7건 상태 저장');
  assert(await pg.evaluate(() => STEP_WORKSHEETS.step11.safety.includes('특정 종교를 전제로 하지 않습니다')), '11단계 종교 강요 방지 문구');
  assert(await pg.evaluate(() => STEP_WORKSHEETS.step12.safety.includes('다른 사람을 치료하거나 책임지라는 뜻이 아닙니다')), '12단계 도움 역할 경계 문구');
  await pg.click('#tabs button[data-t="tools"]'); await pg.waitForTimeout(100);

  // V7.2 자가점검 — 선택 회복영역 + 공통 마음건강 + 행동연결/재점검 안내/최근기록
  // 앞의 영역별 12단계 문구 검증에서 유형을 바꿨으므로 여기서는 의도한 알코올+도박 프로필을 복원합니다.
  await pg.evaluate(() => { S.role='self'; S.types=['alcohol','gambling']; save(); });
  assert(await pg.evaluate(() => Array.isArray(window.SCREENING_TOOLS) && window.SCREENING_TOOLS.length === 9), '자가점검 도구는 9종이어야 함');
  await pg.click('#tool-check'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-screening', '자가점검 목록이 열려야 함');
  const selfScreens = await pg.$$eval('[data-screen]', a => a.map(x => x.dataset.screen));
  assert(JSON.stringify(selfScreens) === JSON.stringify(['audit-k','pgsi','nds-bv','nas-bv','nss-bv']), '알코올+도박 프로필에는 AUDIT-K·PGSI와 공통 3종만 보여야 함');

  // AUDIT-K 첫 검사: 남성 기준, 모두 0점
  await pg.click('[data-screen="audit-k"]'); await pg.waitForTimeout(100);
  assert(await pg.isVisible('#screen-sex-m') && await pg.isVisible('#screen-sex-f'), 'AUDIT-K는 원자료 성별 기준을 선택해야 함');
  await pg.click('#screen-sex-m'); await pg.waitForTimeout(100);
  assert((await pg.$$('[data-screen-v]')).length>0, 'AUDIT-K 첫 문항 선택지가 표시되어야 함');
  await pg.evaluate(() => { const t=screenTool('audit-k'); screenRun.a=Array(t.questions.length).fill(0); finishScreen(t); });
  await pg.waitForTimeout(80);
  assert((await pg.$eval('.screen-score .n', e => e.innerText)) === '0', 'AUDIT-K 0점 결과');
  assert((await pg.$eval('#screen-test-body', e => e.innerText)).includes('첫 기록'), '첫 자가점검은 첫 기록으로 표시');
  await pg.click('#screen-list-go'); await pg.waitForTimeout(100);

  // AUDIT-K 두 번째 검사: 첫 문항 1점, 나머지 0점 → 이전보다 1점 증가
  await pg.click('[data-screen="audit-k"]'); await pg.waitForTimeout(80);
  await pg.click('#screen-sex-m'); await pg.waitForTimeout(80);
  await pg.evaluate(() => { const t=screenTool('audit-k'); screenRun.a=Array(t.questions.length).fill(0); screenRun.a[0]=1; finishScreen(t); });
  await pg.waitForTimeout(80);
  const secondAudit = await pg.$eval('#screen-test-body', e => e.innerText);
  assert(secondAudit.includes('1점') && secondAudit.includes('1점 증가'), '두 번째 AUDIT-K는 이전 대비 1점 증가를 표시');
  assert(secondAudit.includes('약 4주 후') && secondAudit.includes('공식 재검사 주기'), '결과에 경과관찰용 재점검 안내 표시');
  assert(await pg.isVisible('#screen-log-go') && await pg.isVisible('#screen-help-go') && await pg.isVisible('#screen-ai-go'), '결과에서 오늘 돌아보기·도움·마음프로 행동 연결 표시');
  assert((await pg.$eval('#screen-log-go',e=>e.textContent.trim()))==='오늘 돌아보기','자가점검 결과 첫 행동 이름은 오늘 돌아보기');
  await pg.evaluate(() => { window.__screenResultRouteTest=JSON.parse(JSON.stringify(screenRun)); });
  await pg.click('#screen-log-go'); await pg.waitForTimeout(150);
  assert((await seen()) === 'p-meaning', '당사자 자가점검 결과의 오늘 돌아보기는 의미 돌아보기로 이동');
  assert(await pg.$eval('[data-mn-view="today"]',e=>e.classList.contains('on')), '자가점검 결과에서는 의미 돌아보기의 오늘 돌아보기 탭이 열림');
  assert((await pg.$eval('#mn-intro-text',e=>e.textContent)).includes('오늘의 경험에서 아팠던 것'), '당사자는 당사자용 오늘 돌아보기 문항을 사용');
  assert(await pg.evaluate(()=>screenRun===null), '오늘 돌아보기로 이동하면 자가점검 실행 상태를 정리');
  await pg.evaluate(() => { screenRun=window.__screenResultRouteTest; go('screen-test'); drawScreenTest(); });
  await pg.waitForTimeout(120);
  await pg.click('#screen-stat-go'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-rec', '자가점검 결과에서 내 발자취 통계로 이동');
  const statTextV7 = await pg.$eval('#rec-body', e => e.innerText);
  assert(statTextV7.includes('자가점검 변화') && statTextV7.includes('AUDIT-K') && statTextV7.includes('이전보다 1점 증가'), '통계에 자가점검 최근점수와 이전 대비 변화 표시');
  assert((await pg.locator('#rec-body .trend-svg').count()) >= 1, '자가점검 통계에 검사별 꺾은선 그래프 표시');
  assert((await pg.locator('#rec-body .screen-record-row').count()) >= 2, '자가점검 통계에 최근 검사일·점수 목록 표시');
  await shot('10-screening-stat');

  // 가족도 같은 결과 행동을 쓰되 가족용 의미 돌아보기로 분기합니다.
  await pg.evaluate(() => {
    S.role='family';
    if(S.familyWbDays&&typeof S.familyWbDays==='object') delete S.familyWbDays[wbToday()];
    save();
    const t=screenTool('nds-bv');
    screenRun={id:t.id,i:0,a:Array(t.questions.length).fill(0),result:null};
    go('screen-test');
    finishScreen(t);
  });
  await pg.waitForTimeout(120);
  assert((await pg.$eval('#screen-log-go',e=>e.textContent.trim()))==='오늘 돌아보기','가족 자가점검 결과도 오늘 돌아보기 행동 표시');
  await pg.click('#screen-log-go'); await pg.waitForTimeout(150);
  assert((await seen()) === 'p-meaning', '가족 자가점검 결과의 오늘 돌아보기도 의미 돌아보기로 이동');
  const familyScreenMeaning=await pg.$eval('#p-meaning',e=>e.innerText);
  assert(familyScreenMeaning.includes('오늘 내 마음, 경계, 자기돌봄')&&familyScreenMeaning.includes('오늘의 부담감'),'가족 자가점검 결과는 가족용 오늘 돌아보기 문항으로 연결');
  assert(await pg.$eval('[data-mn-view="today"]',e=>e.classList.contains('on')), '가족 결과에서도 오늘 돌아보기 탭이 열림');
  await pg.evaluate(() => { S.role='self'; save(); go('tools'); });
  await pg.waitForTimeout(120);

  // 다시 회복도구로 돌아와 Q&A 검증
  await pg.click('#tabs button[data-t="tools"]'); await pg.waitForTimeout(120);
  assert(await pg.evaluate(() => Array.isArray(window.QA_ITEMS) && window.QA_ITEMS.length === 224), 'Q&A가 224문답이어야 함');
  assert(await pg.evaluate(() => window.QA_ITEMS.every(x => { const n=String(x.a||'').split(/\n\s*\n/).filter(Boolean).length; return n>=2 && n<=3; })), 'Q&A 224개 답변이 모두 2~3문단이어야 함');
  await pg.click('#tool-qa'); await pg.waitForTimeout(250);
  assert((await pg.$eval('#qa-count', e => e.innerText)).includes('224'), 'Q&A 전체 224개 표시');
  await pg.fill('#qa-search', '갈망'); await pg.waitForTimeout(200);
  assert((await pg.$$eval('#qa-list .qaitem', a => a.length)) > 0, 'Q&A 갈망 검색 결과 존재');
  await pg.click('#qa-list .qaitem'); await pg.waitForTimeout(150);
  assert(await pg.isVisible('#qa-one .qadetail'), 'Q&A 상세 답변 표시');
  const qaVisible = await pg.$eval('#p-qa', e => e.innerText);
  assert(!qaVisible.includes('중독 200문답'), 'Q&A 사용자 화면에 원자료 제작 문구가 노출되지 않아야 함');
  assert(!qaVisible.includes('보완 문답'), 'Q&A 사용자 화면에 제작상 보완 구분이 노출되지 않아야 함');
  await shot('11-tools-qa');

  // 기록은 하단에서 내정보 → 내 발자취로 이동
  await pg.click('#tabs button[data-t="home"]'); await pg.waitForTimeout(150);
  await pg.click('#top-me'); await pg.waitForTimeout(250);
  assert((await seen()) === 'p-my' && await pg.isVisible('#my-trail') && await pg.isVisible('#my-settings'), '상단 나 아이콘은 개인 허브를 열어야 함');
  const myOrder = await pg.$$eval('#p-my > #my-settings, #p-my > #my-trail, #p-my > #rec-reclaim', els => els.map(e=>e.id));
  assert(myOrder.join('>') === 'my-settings>my-trail>rec-reclaim', '나 화면은 내 정보 · 설정 → 내 발자취 → 내가 되찾은 것 순서여야 함');
  await pg.click('#my-settings'); await pg.waitForTimeout(180);
  assert((await seen()) === 'p-me' && await pg.isVisible('#me-share'), '내 정보 · 설정에 독립 추천하기 항목 존재');
  assert(await pg.$('#me-feedback-send'), '내 정보 · 설정에 앱에 바라는 점 단일 입력 존재');
  await pg.evaluate(() => go('my')); await pg.waitForTimeout(80);
  await pg.click('#my-trail'); await pg.waitForTimeout(300);
  assert((await pg.$eval('#p-rec h1', e => e.innerText)) === '내 발자취', '기록 화면 명칭은 내 발자취');
  await shot('11-trail-mood');
  const rt = async i => { await pg.click(`#rec-tab button:nth-child(${i})`); await pg.waitForTimeout(300); };
  await rt(2); await shot('12-trail-urge');
  await rt(5); console.log('   다시시작 탭 =', (await pg.$eval('#rec-body', e => e.innerText)).replace(/\n+/g,' / ').slice(0,80));
  await rt(6); assert(await pg.evaluate(() => Array.isArray(S.stepWorks) && S.stepWorks.length===7), '내 발자취 진입 후에도 12단계 검토 저장 기록 7건 유지');
  await rt(8);
  console.log('12. 통계 =', (await pg.$eval('#rec-body', e => e.innerText)).replace(/\n+/g, ' / ').slice(0, 200));
  await shot('13-trail-stat');

  // 도움
  await pg.click('#tabs button[data-t="help"]'); await pg.waitForTimeout(300);
  console.log('13. 핫라인 =', await pg.evaluate(() => [...document.querySelectorAll('#help-lines a')].map(x => x.getAttribute('href')).join(' ')));
  const helpTypesBefore=await pg.evaluate(()=>Array.isArray(S.types)?S.types.slice():[]);
  const fixedCalls=await pg.evaluate(() => [...document.querySelectorAll('#help-fixed-lines a')].map(x=>x.getAttribute('href')));
  assert(fixedCalls.includes('tel:119')&&fixedCalls.includes('tel:109'),'헬프 맨 위 119·109는 앱 내 고정 연결');
  assert(await pg.evaluate(()=>document.querySelectorAll('#help-fixed-lines .b span').length===0),'119·109 카드에는 설명문이 없어야 함');
  const helpCalls=async()=>await pg.evaluate(() => [...document.querySelectorAll('#help-lines a')].map(x=>x.getAttribute('href')));
  await pg.evaluate(()=>{ S.types=['alcohol']; drawHelp(); });
  assert(JSON.stringify(await helpCalls())===JSON.stringify(['tel:1577-0199','tel:129']),'알코올/기본 영역은 정신건강 1577-0199·보건복지 129만 표시');
  await pg.evaluate(()=>{ S.types=['gambling']; drawHelp(); });
  assert(JSON.stringify(await helpCalls())===JSON.stringify(['tel:1577-0199','tel:129','tel:1336']),'도박 영역은 기본 + 1336 표시');
  await pg.evaluate(()=>{ S.types=['drug']; drawHelp(); });
  assert(JSON.stringify(await helpCalls())===JSON.stringify(['tel:1577-0199','tel:129','tel:1342']),'약물 영역은 기본 + 1342 표시');
  await pg.evaluate(()=>{ S.types=['gambling','drug']; drawHelp(); });
  assert(JSON.stringify(await helpCalls())===JSON.stringify(['tel:1577-0199','tel:129','tel:1336','tel:1342']),'도박+약물은 기본 + 1336 + 1342를 중복 없이 표시');
  assert(await pg.evaluate(()=>[...document.querySelectorAll('#help-lines a')].every(x=>!['tel:119','tel:109'].includes(x.getAttribute('href')))),'헬프콜 목록에는 109·119 중복 없음');
  assert(!(await pg.$eval('#p-help',e=>e.innerText)).includes('지도 앱이 열리면서 지금 계신 곳 주변을 찾아줍니다.'),'내 주변에서 찾기 중복 설명문 없음');
  await pg.evaluate(types=>{ S.types=types; save(); drawHelp(); },helpTypesBefore);
  await shot('13-help');

  // 마음프로 Local-first — AI 서버 없이 앱 데이터 설명 + 위치 불일치 선택
  await ctx.grantPermissions(['geolocation'], { origin: 'http://localhost:8899' });
  await ctx.setGeolocation({ latitude: 35.1796, longitude: 129.0756 }); // 부산
  await pg.evaluate(() => {
    S.aiConsent = 1; S.area = '광주';
    S.res = S.res || {};
    S.res.groups = [{ n:'테스트 회복모임', y:DAYN[new Date().getDay()], h:'', a:'광주', d:'테스트 일정', t:'000-0000' }];
    save(); go('ai'); drawAI();
  });
  await pg.evaluate(() => aiSend('오늘 참여할 수 있는 모임 알려줘', 'meeting'));
  await pg.waitForTimeout(900);
  console.log('14. 마음프로 위치 비교 =', await pg.evaluate(() => ai.loc && ai.loc.state),
    '|', (await pg.$eval('#ai-resource', e => e.innerText)).replace(/\n+/g,' / ').slice(0,120));
  await pg.evaluate(() => aiSend('광주 오늘 참여할 수 있는 모임 알려줘', 'meeting'));
  await pg.waitForTimeout(500);
  console.log('    Local-first 설명 =', (await pg.$eval('#ai-thread', e => e.innerText)).replace(/\n+/g,' / ').slice(-220));
  console.log('    AI 전송 제외 =', await pg.evaluate(() => S.aiChat.filter(x => x.role === 'user').slice(-1)[0].local === 1));
  await shot('14-ai-local');

  // 내 정보 — 상단 내정보 아이콘은 홈에서 연다
  await pg.click('#tabs button[data-t="home"]'); await pg.waitForTimeout(150);
  await pg.click('#top-me'); await pg.waitForTimeout(300);
  await shot('15-me');

  // 다시 시작 흐름 — 누적 유지 확인
  await pg.click('#tabs button[data-t="home"]'); await pg.waitForTimeout(250);
  const before = await pg.$eval('#home-days', e => e.innerText.replace(/\n/g, ' | '));
  await pg.click('#go-relapse'); await pg.waitForTimeout(250);
  await pg.click('#rl-halt button:nth-child(3)');
  await pg.click('#rl-save'); await pg.waitForTimeout(300);
  console.log('14. 다시 시작 모달 =', (await pg.$eval('#modin', e => e.innerText)).slice(0, 60).replace(/\n/g,' '));
  await shot('16-relapse');
  await pg.evaluate(() => closeModal()); await pg.waitForTimeout(200);
  await pg.click('#tabs button[data-t="home"]'); await pg.waitForTimeout(250);
  console.log('    전 :', before);
  const afterReset = await pg.$eval('#home-days', e => e.innerText.replace(/\n/g, ' | '));
  console.log('    후 :', afterReset);
  const afterResetCompact = afterReset.replace(/\s*\|\s*/g, '').replace(/\s+/g, '');
  assert(afterResetCompact.includes('1일째'), '다시 시작한 당일은 새 회복 1일째여야 함');

  // 다크 모드 — 나 → 내 정보 · 설정 → 앱 → 화면 설정
  await pg.click('#top-me'); await pg.waitForTimeout(250);
  assert((await seen()) === 'p-my', '상단 나 아이콘은 개인 허브를 열어야 함');
  await pg.click('#my-settings'); await pg.waitForTimeout(120);
  await pg.locator('#p-me .acc-h', {hasText:'앱'}).click(); await pg.waitForTimeout(150);
  assert(await pg.isVisible('#me-theme'), '앱 묶음에 화면 설정이 보여야 함');
  assert(await pg.isVisible('#me-view-mode'),'앱 화면 설정에 홈 간단히 보기 선택이 보여야 함');
  await pg.click('#me-view-mode [data-view-mode=""]'); await pg.waitForTimeout(80);
  await pg.evaluate(()=>go('home')); await pg.waitForTimeout(80);
  assert(await pg.isVisible('#home-daily')&&await pg.isVisible('#home-quote'),'전체 보기에서는 숨긴 두 요소가 다시 보여야 함');
  await pg.evaluate(()=>go('me')); await pg.waitForTimeout(80);
  if(!(await pg.isVisible('#me-view-mode'))){
    await pg.locator('#p-me .acc-h', {hasText:'앱'}).click(); await pg.waitForTimeout(80);
  }
  await pg.click('#me-view-mode [data-view-mode="simple"]'); await pg.waitForTimeout(80);
  assert(await pg.evaluate(()=>S.viewMode==='simple'&&document.body.classList.contains('simple-view')),'간단히 보기 재선택이 즉시 저장·적용');
  await pg.click('#me-theme [data-theme="dark"]'); await pg.waitForTimeout(300);
  await shot('17-dark');
  await pg.click('#me-theme [data-theme="light"]'); await pg.waitForTimeout(200);
  await pg.click('#tabs button[data-t="home"]'); await pg.waitForTimeout(200);

  // 새로고침 후에도 남아 있는지
  await pg.reload(); await pg.waitForTimeout(600);
  console.log('15. 새로고침 후 =', await seen(), '|', (await pg.$eval('#home-days', e => e.innerText)).replace(/\n/g, ' '));

  console.log('\n=== 오류 ===');
  console.log(errs.length ? errs.join('\n') : '없음');
  assert(errs.length === 0, '브라우저 회귀검사 중 로컬 HTTP·JavaScript 런타임 오류가 없어야 함');

  await b.close(); srv.close();
})();
