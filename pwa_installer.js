// =====================================================================
// FILE: pwa_installer.js (Osmosis PWA Registration & Install Handler)
// =====================================================================

(function () {
  'use strict';

  // 1. Register the Service Worker
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register('./sw.js')
        .then((reg) => {
          console.log('[PWA] Service Worker registered with scope:', reg.scope);

          // Listen for updates
          reg.onupdatefound = () => {
            const installingWorker = reg.installing;
            installingWorker.onstatechange = () => {
              if (installingWorker.state === 'installed') {
                if (navigator.serviceWorker.controller) {
                  console.log('[PWA] New version of Osmosis is available!');
                } else {
                  console.log('[PWA] Osmosis is cached for offline play!');
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

  // 2. Handle the "Add to Home Screen" Install Prompt
  let deferredPrompt = null;

  window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the mini-infobar from appearing automatically on mobile
    e.preventDefault();
    deferredPrompt = e;
    console.log('[PWA] Install prompt detected and deferred.');

    // Reveal install UI if present on page
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
        console.log('[PWA] User accepted the Osmosis install prompt!');
      } else {
        console.log('[PWA] User dismissed the Osmosis install prompt.');
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

  // Expose global trigger for any button to call
  window.triggerOsmosisInstall = promptInstall;
})();
