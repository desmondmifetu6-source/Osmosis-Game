// =====================================================================
// FILE: sw.js (Osmosis Service Worker - Offline & PWA Engine)
// =====================================================================
const CACHE_NAME = 'osmosis-core-v5';

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
  './micro_animations.js',
  './micro_animations/successfully-done.json',
  './micro_animations/hatching-chick.json',
  './micro_animations/Done.mp4',
  './micro_animations/Success Loader.mp4',
  './micro_animations/Successfully Done.mp4',
  './core_dictionary.js',
  './hunt_dictionary.js',
  './core_dictionary_diagrams.js',
  './core_formula_renderer.js',
  './core_distractor_engine.js',
  './core_diagram_data.js',
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/osmosis-favicon.svg',
  './assets/forest_canopy_backdrop.jpg',
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
  './10_stage8_hall_of_fame_intro.html',
  './10_stage8_recall_test.html',
  './10_stage8_recall_test.js',
  './10b_stage8_complete.html',
  './11_results.html',
  './11_results.js',
  './multiplayer_lobby.html',
  './multiplayer_lobby.js',
  './multiplayer_results.html',
  './multiplayer_results.js',
  './module_word_hunt.html',
  './module_word_hunt.js',
  './module_library.html',
  './module_library.js',
  './module_archives.html',
  './module_archives.js',
  './module_profile.html',
  './module_profile.js',
  './module_about.html'
];

// Listen for skipWaiting messages from client
self.addEventListener('message', (event) => {
  if (event.data && (event.data.action === 'skipWaiting' || event.data === 'skipWaiting')) {
    self.skipWaiting();
  }
});

// 1. INSTALL: Pre-cache the shell cleanly
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      for (const asset of PRECACHE_ASSETS) {
        try {
          await cache.add(new Request(asset, { cache: 'reload' }));
        } catch (err) {
          console.warn('[Service Worker] Could not pre-cache:', asset, err.message);
        }
      }
      return self.skipWaiting();
    })
  );
});

// 2. ACTIVATE: Purge obsolete caches & take immediate control
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. FETCH: Network-First for HTML/JS/CSS so updates ship immediately;
//           Stale-While-Revalidate for heavy static media assets.
// 3. FETCH: Instant Stale-While-Revalidate (0ms Cache Response with background refresh)
self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);

  // Skip socket.io and non-GET requests
  if (request.method !== 'GET' || url.pathname.includes('/socket.io/')) {
    return;
  }

  // Cross-origin requests (e.g. external CDNs): let browser handle
  if (url.origin !== self.location.origin) {
    return;
  }

  // Stale-While-Revalidate Strategy for ALL Same-Origin Assets (HTML, JS, CSS, Media)
  // 1. Return cached copy immediately (0ms instant page transitions)
  // 2. Fetch fresh copy in background and update the cache silently
  event.respondWith(
    caches.match(request, { ignoreSearch: true }).then((cachedResponse) => {
      const fetchPromise = fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          }
          return networkResponse;
        })
        .catch(() => null);

      // Return cached version immediately if available (Instantaneous Transition!)
      if (cachedResponse) {
        return cachedResponse;
      }

      // If not in cache, wait for network response
      return fetchPromise.then((networkResponse) => {
        if (networkResponse) return networkResponse;

        // Offline Fallback for navigation requests
        if (request.mode === 'navigate' || (request.headers.get('accept') && request.headers.get('accept').includes('text/html'))) {
          return caches.match('./01_home_menu.html') || caches.match('./index.html');
        }
      });
    })
  );
});
