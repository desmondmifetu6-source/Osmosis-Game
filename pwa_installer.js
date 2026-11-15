// =====================================================================
// FILE: pwa_installer.js (Osmosis Realtime Update & PWA Engine)
// =====================================================================

(function () {
  'use strict';

  let waitingWorker = null;
  let swRegistration = null;
  let refreshing = false;
  let bannerElement = null;

  // 1. Controller Change Handler (Smooth reload once new worker activates)
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (!refreshing) {
        refreshing = true;
        window.location.reload();
      }
    });
  }

  // 2. Inject CSS for the Floating Update Banner
  function injectStyles() {
    if (document.getElementById('osmosis-update-styles')) return;
    const style = document.createElement('style');
    style.id = 'osmosis-update-styles';
    style.textContent = `
      @keyframes osmosisSlideUp {
        0% { transform: translate(-50%, 80px); opacity: 0; }
        100% { transform: translate(-50%, 0); opacity: 1; }
      }
      @keyframes osmosisPulseGlow {
        0%, 100% { box-shadow: 0 0 12px rgba(168, 85, 247, 0.4), 0 14px 34px rgba(0, 0, 0, 0.55); }
        50% { box-shadow: 0 0 24px rgba(168, 85, 247, 0.8), 0 16px 40px rgba(0, 0, 0, 0.65); }
      }
      .osmosis-update-banner {
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translate(-50%, 0);
        z-index: 9999999;
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 10px 18px;
        background: linear-gradient(135deg, rgba(24, 16, 47, 0.96), rgba(15, 23, 42, 0.96));
        border: 1.5px solid rgba(168, 85, 247, 0.55);
        border-radius: 999px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        animation: osmosisSlideUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards, osmosisPulseGlow 3s infinite ease-in-out;
        color: #fff;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        user-select: none;
        max-width: 94vw;
        box-sizing: border-box;
      }
      .osmosis-update-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #a855f7, #6366f1);
        box-shadow: 0 0 12px rgba(168, 85, 247, 0.6);
        font-size: 19px;
        flex-shrink: 0;
      }
      .osmosis-update-text {
        display: flex;
        flex-direction: column;
        line-height: 1.25;
        text-align: left;
      }
      .osmosis-update-title {
        color: #ffffff;
        font-weight: 800;
        font-size: 0.92rem;
        letter-spacing: 0.3px;
      }
      .osmosis-update-sub {
        color: rgba(226, 232, 240, 0.82);
        font-size: 0.76rem;
      }
      .osmosis-update-btn {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        border: none;
        font-weight: 700;
        font-size: 0.86rem;
        padding: 8px 18px;
        border-radius: 999px;
        cursor: pointer;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        white-space: nowrap;
        flex-shrink: 0;
      }
      .osmosis-update-btn:hover {
        transform: scale(1.04);
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.6);
      }
      .osmosis-update-btn:active {
        transform: scale(0.97);
      }
      .osmosis-update-dismiss {
        background: transparent;
        border: none;
        color: rgba(255, 255, 255, 0.55);
        font-size: 1.25rem;
        line-height: 1;
        cursor: pointer;
        padding: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: color 0.2s;
        flex-shrink: 0;
      }
      .osmosis-update-dismiss:hover {
        color: #ffffff;
      }
      @media (max-width: 600px) {
        .osmosis-update-banner {
          bottom: 16px;
          padding: 8px 12px;
          gap: 10px;
          border-radius: 18px;
        }
        .osmosis-update-sub {
          display: none;
        }
      }
    `;
    document.head.appendChild(style);
  }

  // 3. Show the Floating Update Banner
  function showUpdateBanner(worker) {
    if (worker) waitingWorker = worker;
    if (bannerElement || document.querySelector('.osmosis-update-banner')) return;

    injectStyles();

    const banner = document.createElement('div');
    banner.className = 'osmosis-update-banner';
    banner.setAttribute('role', 'alert');
    banner.setAttribute('aria-live', 'assertive');

    banner.innerHTML = `
      <div class="osmosis-update-icon">⚡</div>
      <div class="osmosis-update-text">
        <span class="osmosis-update-title">Update Ready!</span>
        <span class="osmosis-update-sub">Tap to get the latest features</span>
      </div>
      <button class="osmosis-update-btn" id="osmosis-apply-update-btn">
        <span>🔄</span>
        <span>Update</span>
      </button>
      <button class="osmosis-update-dismiss" id="osmosis-dismiss-update-btn" title="Dismiss">&times;</button>
    `;

    document.body.appendChild(banner);
    bannerElement = banner;

    const updateBtn = document.getElementById('osmosis-apply-update-btn');
    if (updateBtn) {
      updateBtn.addEventListener('click', () => applyUpdate());
    }

    const dismissBtn = document.getElementById('osmosis-dismiss-update-btn');
    if (dismissBtn) {
      dismissBtn.addEventListener('click', () => {
        banner.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
        banner.style.transform = 'translate(-50%, 100px)';
        banner.style.opacity = '0';
        setTimeout(() => {
          banner.remove();
          bannerElement = null;
        }, 300);
      });
    }
  }

  // 4. Trigger Update Application
  async function applyUpdate() {
    const updateBtn = document.getElementById('osmosis-apply-update-btn');
    if (updateBtn) {
      updateBtn.innerHTML = '<span>⏳</span><span>Updating...</span>';
      updateBtn.style.pointerEvents = 'none';
    }

    // 1. Tell waiting service worker to skipWaiting
    if (waitingWorker) {
      waitingWorker.postMessage({ action: 'skipWaiting' });
    } else if (navigator.serviceWorker && navigator.serviceWorker.controller) {
      navigator.serviceWorker.controller.postMessage({ action: 'skipWaiting' });
    }

    // 2. Clear stale cache storage to guarantee brand new code
    if ('caches' in window) {
      try {
        const keys = await caches.keys();
        await Promise.all(keys.map((k) => caches.delete(k)));
      } catch (err) {
        console.warn('[PWA] Cache purge error:', err);
      }
    }

    // 3. Mark version updated in localStorage
    if (window._latestServerVersion) {
      localStorage.setItem('osmosis_active_version', String(window._latestServerVersion));
    }

    // 4. Force reload
    setTimeout(() => {
      window.location.reload(true);
    }, 350);
  }

  // 5. Register Service Worker & Attach Listeners
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register('./sw.js')
        .then((reg) => {
          swRegistration = reg;
          console.log('[PWA] Service Worker registered with scope:', reg.scope);

          // If a worker is already waiting in background, prompt immediately
          if (reg.waiting) {
            console.log('[PWA] Found a waiting Service Worker update.');
            showUpdateBanner(reg.waiting);
          }

          // Listen for new worker installation
          reg.onupdatefound = () => {
            const installingWorker = reg.installing;
            if (!installingWorker) return;
            installingWorker.onstatechange = () => {
              if (installingWorker.state === 'installed') {
                if (navigator.serviceWorker.controller) {
                  console.log('[PWA] New version of Osmosis detected!');
                  showUpdateBanner(installingWorker);
                } else {
                  console.log('[PWA] Osmosis cached for offline play.');
                }
              }
            };
          };
        })
        .catch((err) => {
          console.warn('[PWA] Service Worker registration failed:', err);
        });
    });
  }

  // 6. Realtime Polling & Focus Checking via /api/version
  async function checkServerVersion() {
    try {
      const res = await fetch(`/api/version?t=${Date.now()}`, { cache: 'no-store' });
      if (!res.ok) return;
      const data = await res.json();
      if (!data || !data.version) return;

      window._latestServerVersion = data.version;
      const savedVersion = localStorage.getItem('osmosis_active_version');

      if (!savedVersion) {
        localStorage.setItem('osmosis_active_version', String(data.version));
      } else if (String(savedVersion) !== String(data.version)) {
        console.log('[PWA] Server update detected! Current:', savedVersion, 'New:', data.version);
        showUpdateBanner(waitingWorker);
      }
    } catch (_) {
      // Offline or network error - fail silently
    }
  }

  // Check on tab focus and periodically every 45s
  window.addEventListener('focus', () => {
    if (swRegistration) swRegistration.update().catch(() => {});
    checkServerVersion();
  });
  setInterval(() => {
    if (swRegistration) swRegistration.update().catch(() => {});
    checkServerVersion();
  }, 45000);

  // Initial version check after page settles
  setTimeout(checkServerVersion, 2500);

  // 7. Realtime Socket.IO Listeners (If Socket is present on the page)
  function attachSocketUpdateListener(socket) {
    if (!socket || socket._hasOsmosisUpdateListener) return;
    socket._hasOsmosisUpdateListener = true;
    socket.on('server_info', (data) => {
      if (data && data.version) {
        window._latestServerVersion = data.version;
        const current = localStorage.getItem('osmosis_active_version');
        if (!current) {
          localStorage.setItem('osmosis_active_version', String(data.version));
        } else if (String(current) !== String(data.version)) {
          showUpdateBanner(waitingWorker);
        }
      }
    });
  }

  // Hook into global socket if already present or when created
  if (window.socket) attachSocketUpdateListener(window.socket);
  const origIo = window.io;
  if (typeof origIo === 'function') {
    window.io = function (...args) {
      const sock = origIo(...args);
      attachSocketUpdateListener(sock);
      return sock;
    };
    Object.assign(window.io, origIo);
  }

  // 8. Handle PWA "Add to Home Screen"
  let deferredPrompt = null;
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    console.log('[PWA] Install prompt detected and deferred.');

    const installBtn = document.getElementById('pwa-install-btn');
    if (installBtn) {
      installBtn.style.display = 'inline-flex';
      installBtn.addEventListener('click', promptInstall);
    }
  });

  function promptInstall() {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('[PWA] User accepted install prompt');
      }
      deferredPrompt = null;
      const installBtn = document.getElementById('pwa-install-btn');
      if (installBtn) installBtn.style.display = 'none';
    });
  }

  window.addEventListener('appinstalled', () => {
    console.log('[PWA] Osmosis App was successfully installed!');
    const installBtn = document.getElementById('pwa-install-btn');
    if (installBtn) installBtn.style.display = 'none';
  });

  // 9. Expose Global Updater API
  window.OsmosisUpdater = {
    showBanner: () => showUpdateBanner(waitingWorker),
    applyUpdate: () => applyUpdate(),
    checkUpdate: () => {
      if (swRegistration) swRegistration.update().catch(() => {});
      return checkServerVersion();
    }
  };
  window.triggerOsmosisInstall = promptInstall;
  window.triggerOsmosisUpdate = () => showUpdateBanner(waitingWorker);
})();
