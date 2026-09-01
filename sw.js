/* 오늘 한 걸음 — 서비스 워커
   앱 껍데기만 캐시합니다. 회복 기록은 브라우저 저장소가 따로 맡습니다.

   ★ index.html 을 고칠 때마다 아래 V 를 반드시 올리세요.
     index.html 안의 const BUILD 도 같이 올립니다. */
const V = 'ohg-v40';
const SHELL = ['./', './index.html', './manifest.json',
  './icon-180.png', './icon-192.png', './icon-512.png', './icon-32.png'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k))))
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
