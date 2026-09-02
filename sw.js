/* 오늘 한 걸음 — 서비스 워커
   앱 껍데기만 캐시합니다. 회복 기록은 브라우저 저장소가 따로 맡습니다.

   ★ 배포할 때 APP_VERSION · 내부 캐시 V · index.html 의 BUILD 를 함께 갱신하세요. */
/* 사용자에게 보이는 앱 버전. index.html 의 BUILD 와 반드시 맞춥니다. */
const APP_VERSION = 'V7.1';
/* 내부 캐시 리비전. 기존 v46 클라이언트도 새 판을 감지하도록 숫자형 키를 유지합니다.
   V4.6 → 406, V4.7 → 407, V4.10 → 410, V5.0 → 500, V5.1 → 501, V5.2 → 502 */
const V = 'ohg-v701';
const SHELL = ['./', './index.html',
  './qa-data.js', './learning-data.js', './screening-data.js', './manifest.json',
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
