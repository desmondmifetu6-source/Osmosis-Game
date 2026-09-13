// =====================================================================
// FILE: sw.js (Osmosis Service Worker - Offline & PWA Engine)
// =====================================================================
const CACHE_NAME = 'osmosis-core-v1';

// Core Application Shell: essential files for full offline play
const PRECACHE_ASSETS = [
  './',
  './index.html',
  './index.js',
  './01_home_menu.html',
  './01_home_menu.js',
  './manifest.json',
  './core_styles.css',
  './core_shared_state.js',
  './core_dictionary.js',
  './core_dictionary_diagrams.js',
  './core_formula_renderer.js',
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/osmosis-favicon.svg',
  './02_campaign_setup.html',
  './02_campaign_setup.js',
  './02b_personal_study_setup.html',
  './02b_personal_study_setup.js',
  './03_stage1_word_selection.html',
  './03_stage1_word_selection.js',
  './04_stage2_word_fillin.html',
  './04_stage2_word_fillin.js',
  './05_stage3_flash_recall.html',
  './05_stage3_flash_recall.js',
  './06_stage4_self_recall.html',
  './06_stage4_self_recall.js',
  './07_stage5_meaning_exposure.html',
  './07_stage5_meaning_exposure.js',
  './08_stage6_definition_selection.html',
  './08_stage6_definition_selection.js',
  './08b_stage6b_meaning_dropdown.html',
  './08b_stage6b_meaning_dropdown.js',
  './09_stage7_meaning_fillin.html',
  './09_stage7_meaning_fillin.js',
  './10_stage8_recall_test.html',
  './10_stage8_recall_test.js',
  './11_results.html',
  './11_results.js',
  './module_diagram_hub.html',
  './module_diagram_hub.js',
  './module_diagram_study.html',
  './module_diagram_study.js',
  './module_word_hunt.html',
  './module_word_hunt.js',
  './module_library.html',
  './module_library.js',
  './module_about.html'
];

// 1. INSTALL: Pre-cache the shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      console.log('[Service Worker] Pre-caching Osmosis Application Shell...');
      // Use individual adds so a single missing asset does not abort the entire precache
      for (const asset of PRECACHE_ASSETS) {
        try {
          await cache.add(asset);
        } catch (err) {
          console.warn('[Service Worker] Could not pre-cache:', asset, err.message);
        }
      }
      return self.skipWaiting();
    })
  );
});

// 2. ACTIVATE: Clean up obsolete caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[Service Worker] Purging legacy cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. FETCH: Smart caching strategy (Stale-While-Revalidate with offline fallback)
self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);

  // Bypass Socket.io and POST/PUT/DELETE requests for real-time multiplayer integrity
  if (request.method !== 'GET' || url.pathname.includes('/socket.io/')) {
    return;
  }

  // Handle same-origin requests & Google fonts
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        // Return cached immediately, fetch fresh copy in the background (Stale-While-Revalidate)
        fetch(request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, networkResponse.clone());
            });
          }
        }).catch(() => {/* Silent offline catch */});
        return cachedResponse;
      }

      // If not in cache, fetch from network and cache dynamically (e.g. diagrams, audio)
      return fetch(request).then((networkResponse) => {
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type === 'opaque') {
          return networkResponse;
        }

        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(request, responseToCache);
        });

        return networkResponse;
      }).catch(() => {
        // Fallback for HTML navigation when offline
        if (request.headers.get('accept') && request.headers.get('accept').includes('text/html')) {
          return caches.match('./01_home_menu.html') || caches.match('./index.html');
        }
      });
    })
  );
});
