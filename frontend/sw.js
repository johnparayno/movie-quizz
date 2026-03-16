/**
 * Service worker for quiz PWA — offline caching
 * Works when deployed to root or subfolder (FTP-friendly).
 * When bumping version in index.html, update CACHE_NAME here too.
 */
const CACHE_NAME = 'quiz-v2.0.6';
const BASE = self.location.pathname.replace(/sw\.js$/, '') || '/';
const ASSETS = [
  BASE || '/',
  BASE + 'index.html',
  BASE + 'styles.css?v=2.0.6',
  BASE + 'app.js?v=2.0.6',
  BASE + 'manifest.json',
  BASE + 'movie_quizz_500_updated.json',
  BASE + 'icons/icon.svg',
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      Promise.allSettled(ASSETS.map((url) => cache.add(url).catch(() => {})))
    )
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  const { request } = e;
  const url = new URL(request.url);
  if (url.origin !== location.origin) return;
  if (!url.pathname.startsWith('/')) return;

  // Network-first for HTML so users get latest version on load/refresh
  if (request.mode === 'navigate' || url.pathname.endsWith('/') || url.pathname.endsWith('/index.html')) {
    e.respondWith(
      fetch(request).catch(() => caches.match(request))
    );
    return;
  }

  // Network-first for movie_quizz_500_updated.json so we get fresh data when online
  if (url.pathname.endsWith('/movie_quizz_500_updated.json')) {
    e.respondWith(
      fetch(request)
        .then((res) => {
          if (res.ok) {
            const clone = res.clone();
            caches.open(CACHE_NAME).then((c) => c.put(request, clone));
          }
          return res;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  e.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;
      return fetch(request).then((res) => {
        const clone = res.clone();
        if (res.ok && request.method === 'GET')
          caches.open(CACHE_NAME).then((c) => c.put(request, clone));
        return res;
      });
    })
  );
});
