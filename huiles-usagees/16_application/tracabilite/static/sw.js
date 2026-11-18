// Service worker : met en cache l'interface pour un fonctionnement hors ligne.
const CACHE = "tracabilite-v1";
const FICHIERS = ["/", "/static/app.js", "/static/style.css", "/static/manifest.json"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FICHIERS)));
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (url.pathname.startsWith("/api/")) return; // les donnees passent par l'application et sa file d'attente
  e.respondWith(caches.match(e.request).then((r) => r || fetch(e.request)));
});
