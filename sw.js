/* 오늘 한 걸음 — 서비스 워커
   앱 껍데기만 캐시합니다. 회복 기록은 브라우저 저장소가 따로 맡습니다.

   ★ 배포할 때 APP_VERSION · 내부 캐시 V · index.html 의 BUILD 를 함께 갱신하세요. */
/* 사용자에게 보이는 앱 버전. index.html 의 BUILD 와 반드시 맞춥니다. */
const APP_VERSION = 'V8.0.5';
/* 내부 캐시 리비전. 기존 v46 클라이언트도 새 판을 감지하도록 숫자형 키를 유지합니다.
   V4.6 → 406, V4.7 → 407, V4.10 → 410, V5.0 → 500, V5.1 → 501, V5.2 → 502 */
const V = 'ohg-v805';
const SHELL = ['./', './index.html', './native.html',
  './qa-data.js', './learning-data.js', './screening-data.js', './workbook-data.js', './manifest.json',
  './icon-180.png', './icon-192.png', './icon-512.png', './icon-32.png'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k.startsWith('ohg-') && k !== V).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);

  /* 자원 목록(Apps Script)은 절대 캐시하지 않습니다 */
  if (u.hostname.endsWith('google.com') ||
      u.hostname.endsWith('googleusercontent.com') ||
      u.hostname.endsWith('googleapis.com')) return;

  if (e.request.method !== 'GET') return;
  if (u.origin !== location.origin) return;

  /* ★ 캐시 우선이 아니라 '네트워크 우선' 입니다.
       캐시 우선으로 두었더니 고친 화면이 안 보여서 여러 번 헤맸습니다.
       인터넷이 없을 때만 캐시로 버팁니다 — 충동 타이머와 기록은
       index.html 안에 다 들어 있으므로 비행기 모드에서도 그대로 돌아갑니다. */
  e.respondWith(
    fetch(e.request).then(res => {
      const copy = res.clone();
      caches.open(V).then(c => c.put(e.request, copy)).catch(() => {});
      return res;
    }).catch(() => caches.match(e.request).then(hit => hit || caches.match('./index.html')))
  );
});


/* V8.0 — 브라우저 알림 호환 경로. Android 패키지는 네이티브 예약알림을 주 경로로 씁니다. */
self.addEventListener('notificationclick', e => {
  e.notification.close();
  const target = (e.notification.data && e.notification.data.url) || './index.html';
  const scope = self.registration && self.registration.scope ? self.registration.scope : '';
  e.waitUntil(
    self.clients.matchAll({ type:'window', includeUncontrolled:true }).then(list => {
      for(const c of list){
        /* 같은 github.io origin의 다른 프로젝트 창을 잘못 앞으로 가져오지 않습니다. */
        if((!scope || String(c.url || '').startsWith(scope)) && 'focus' in c) return c.focus();
      }
      return self.clients.openWindow ? self.clients.openWindow(target) : undefined;
    })
  );
});
