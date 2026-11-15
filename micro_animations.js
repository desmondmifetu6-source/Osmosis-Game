// =====================================================================
// FILE: micro_animations.js — Osmosis Micro-Animation & Game Juice Engine
// High-Octane Polish, Haptics, Physics-Based Micro-Interactions & Lottie
//
// Asset Matrix:
//   micro_animations/successfully-done.json  → Dynamic Correct Answer Burst
//   micro_animations/hatching-chick.json     → Final Graduation / Results Screen
//   micro_animations/Done.mp4                → Stage Clear HUD Portal
//   micro_animations/Success Loader.mp4      → Inter-stage Smooth Loader
//   micro_animations/Successfully Done.mp4   → Hall of Fame Grand Trophy Video
// =====================================================================

(function () {
  'use strict';

  const ANIM_PATH = './micro_animations/';

  // ── 1. Dynamic Lottie Engine Loader ────────────────────────────────
  function ensureLottieLibrary(callback) {
    if (window.lottie) {
      if (callback) callback();
      return;
    }
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js';
    script.async = true;
    script.onload = () => {
      if (callback) callback();
    };
    script.onerror = () => {
      // Fallback gracefully to SVG/CSS animation
      if (callback) callback();
    };
    document.head.appendChild(script);
  }

  // ── 2. Inject Master Juice Styles ──────────────────────────────────
  function injectStyles() {
    if (document.getElementById('osmosis-juice-styles')) return;
    const style = document.createElement('style');
    style.id = 'osmosis-juice-styles';
    style.textContent = `
      /* ── Correct Checkmark Burst (Clean, crisp, no glow) ── */
      #osmosis-correct-anim {
        position: fixed;
        top: 48%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0.6);
        width: 160px;
        height: 160px;
        z-index: 999999;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.12s cubic-bezier(0.16, 1, 0.3, 1), transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
      }
      #osmosis-correct-anim.anim-visible {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1);
      }
      #osmosis-correct-anim.anim-out {
        opacity: 0;
        transform: translate(-50%, -50%) scale(1.25);
        transition: opacity 0.2s ease, transform 0.2s ease;
      }

      /* ── Fallback SVG Checkmark when offline ── */
      .osmosis-fallback-svg {
        width: 100%;
        height: 100%;
        animation: osmosisSvgPop 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
      }
      @keyframes osmosisSvgPop {
        0%   { transform: scale(0.5); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
      }

      /* ── Floating Score Badge (Clean, flat, no neon glow) ── */
      .osmosis-score-floater {
        position: fixed;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-weight: 800;
        font-size: 1.45rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #10b981;
        background: #0f172a;
        padding: 6px 14px;
        border-radius: 999px;
        border: 1.5px solid #10b981;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
        pointer-events: none;
        z-index: 1000000;
        user-select: none;
        animation: osmosisFloatUp 0.85s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }
      .osmosis-score-floater.wrong {
        color: #ef4444;
        border-color: #ef4444;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
        animation: osmosisFloatUpWrong 0.85s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }
      @keyframes osmosisFloatUp {
        0%   { opacity: 0; transform: translateY(12px) scale(0.7); }
        25%  { opacity: 1; transform: translateY(-16px) scale(1.1); }
        60%  { opacity: 1; transform: translateY(-42px) scale(1.0); }
        100% { opacity: 0; transform: translateY(-75px) scale(0.85); }
      }
      @keyframes osmosisFloatUpWrong {
        0%   { opacity: 0; transform: translateY(8px) scale(0.8); }
        20%  { opacity: 1; transform: translateY(-8px) scale(1.05) rotate(-3deg); }
        60%  { opacity: 0.8; transform: translateY(-28px) scale(0.95) rotate(2deg); }
        100% { opacity: 0; transform: translateY(-50px) scale(0.8); }
      }

      /* ── Ripple Punch Effect ── */
      .osmosis-ripple {
        position: absolute;
        border-radius: 50%;
        transform: scale(0);
        background: radial-gradient(circle, rgba(16, 185, 129, 0.6) 0%, rgba(16, 185, 129, 0) 70%);
        animation: osmosisRipple 0.5s ease-out forwards;
        pointer-events: none;
        z-index: 10;
      }
      .osmosis-ripple.wrong-ripple {
        background: radial-gradient(circle, rgba(239, 68, 68, 0.5) 0%, rgba(239, 68, 68, 0) 70%);
      }
      @keyframes osmosisRipple {
        to { transform: scale(3.5); opacity: 0; }
      }

      /* ── Button Micro-Interactions ── */
      @keyframes osmosisBounce {
        0%   { transform: scale(1); }
        35%  { transform: scale(1.12); }
        65%  { transform: scale(0.96); }
        85%  { transform: scale(1.03); }
        100% { transform: scale(1); }
      }
      .osmosis-bounce {
        animation: osmosisBounce 0.42s cubic-bezier(0.34, 1.56, 0.64, 1) both !important;
      }

      @keyframes osmosisShake {
        0%, 100% { transform: translateX(0); }
        20%      { transform: translateX(-8px) rotate(-1deg); }
        40%      { transform: translateX(8px) rotate(1deg); }
        60%      { transform: translateX(-5px); }
        80%      { transform: translateX(5px); }
      }
      .osmosis-shake {
        animation: osmosisShake 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97) both !important;
      }

      /* ── Stage Transition Video Portal ── */
      #osmosis-transition-portal {
        position: fixed;
        inset: 0;
        background: rgba(10, 15, 30, 0.88);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        z-index: 999998;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      }
      #osmosis-transition-portal.active {
        opacity: 1;
        pointer-events: auto;
      }
      .osmosis-portal-video-box {
        position: relative;
        width: 190px;
        height: 190px;
        border-radius: 50%;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        border: 2.5px solid #6366f1;
        animation: osmosisPopIn 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
      }
      .osmosis-portal-video {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      .osmosis-portal-caption {
        margin-top: 1.25rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 800;
        font-size: 1.2rem;
        letter-spacing: 1px;
        color: #ffffff;
        text-transform: uppercase;
      }
      @keyframes osmosisPopIn {
        0%   { transform: scale(0.4); opacity: 0; }
        100% { transform: scale(1);   opacity: 1; }
      }

      /* ── Results Hatching Chick Display (Clean, no glow) ── */
      .osmosis-chick-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.75rem;
        position: relative;
      }
      .osmosis-chick-container {
        width: 140px;
        height: 140px;
        animation: osmosisPopIn 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) 0.15s both;
      }
      .osmosis-chick-caption {
        font-size: 0.85rem;
        font-weight: 800;
        color: #d97706;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: -6px;
      }
    `;
    document.head.appendChild(style);
  }

  // ── 3. Page Identity (declared early — used by preloader + observer guards) ──
  const pageName = window.location.pathname.split('/').pop().split('?')[0];

  // ── 4. Lottie Data Preloader ───────────────────────────────────────
  // ⚡ PERF FIX: Only preload Lottie assets on pages that actually use them.
  // Home menu and setup pages never show Lottie animations — skip the CDN fetch entirely.
  const LOTTIE_PAGES = /^(03_|04_|05_|06_|07_|08_|09_|10_|11_results|multiplayer_results|module_word_hunt)/i;
  const needsLottie = LOTTIE_PAGES.test(pageName);

  let lottieCorrectData = null;
  let lottieChickData = null;
  let correctAnimEl = null;
  let correctAnimInstance = null;
  let correctAnimTimer = null;

  function preloadAssets() {
    // ⚡ PERF FIX: Skip all network fetches + CDN script injection on non-game pages.
    if (!needsLottie) return;

    fetch(ANIM_PATH + 'successfully-done.json')
      .then(r => r.json())
      .then(d => { lottieCorrectData = d; })
      .catch(() => {});

    fetch(ANIM_PATH + 'hatching-chick.json')
      .then(r => r.json())
      .then(d => { lottieChickData = d; })
      .catch(() => {});

    // Ensure Lottie engine is ready
    ensureLottieLibrary();
  }

  // ── 4. Flash Correct Animation ─────────────────────────────────────
  let lastCorrectTime = 0;

  function ensureCorrectEl() {
    if (correctAnimEl) return;
    correctAnimEl = document.createElement('div');
    correctAnimEl.id = 'osmosis-correct-anim';
    document.body.appendChild(correctAnimEl);
  }

  function flashCorrect() {
    const now = Date.now();
    if (now - lastCorrectTime < 420) return; // Prevent double-trigger from both event & observer
    lastCorrectTime = now;

    ensureCorrectEl();
    if (correctAnimTimer) clearTimeout(correctAnimTimer);

    if (correctAnimInstance) {
      try { correctAnimInstance.destroy(); } catch (_) {}
      correctAnimInstance = null;
    }
    correctAnimEl.innerHTML = '';
    correctAnimEl.classList.remove('anim-visible', 'anim-out');

    if (lottieCorrectData && window.lottie) {
      try {
        correctAnimInstance = window.lottie.loadAnimation({
          container: correctAnimEl,
          renderer: 'svg',
          loop: false,
          autoplay: true,
          animationData: lottieCorrectData
        });
      } catch (_) {
        renderFallbackSvg(correctAnimEl);
      }
    } else {
      renderFallbackSvg(correctAnimEl);
    }

    requestAnimationFrame(() => {
      correctAnimEl.classList.add('anim-visible');
    });

    // Gentle tactile haptic punch on mobile
    if (navigator.vibrate) {
      try { navigator.vibrate([18, 25, 20]); } catch (_) {}
    }

    correctAnimTimer = setTimeout(() => {
      correctAnimEl.classList.add('anim-out');
      correctAnimEl.classList.remove('anim-visible');
      setTimeout(() => {
        correctAnimEl.innerHTML = '';
        correctAnimEl.classList.remove('anim-out');
        if (correctAnimInstance) {
          try { correctAnimInstance.destroy(); } catch (_) {}
          correctAnimInstance = null;
        }
      }, 250);
    }, 850);
  }

  function renderFallbackSvg(container) {
    container.innerHTML = `
      <svg class="osmosis-fallback-svg" viewBox="0 0 100 100" fill="none">
        <circle cx="50" cy="50" r="46" fill="#10B981" />
        <path d="M30 52 L44 66 L72 36" stroke="#ffffff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    `;
  }

  // ── 5. Floating Score Indicator ───────────────────────────────────
  let lastFloaterTime = 0;

  function spawnScoreFloater(points, x, y, isWrong = false) {
    const now = Date.now();
    if (now - lastFloaterTime < 280) return; // Debounce rapid triggers
    lastFloaterTime = now;

    const floater = document.createElement('div');
    floater.className = 'osmosis-score-floater' + (isWrong ? ' wrong' : '');
    floater.innerHTML = isWrong ? '<span>✕</span><span>Try again</span>' : `<span>⭐</span><span>+${points || 10}</span>`;

    const left = (x != null && x > 0 && x < window.innerWidth) ? x : (window.innerWidth / 2 - 50);
    const top  = (y != null && y > 0 && y < window.innerHeight) ? y : (window.innerHeight / 2);

    floater.style.left = `${left}px`;
    floater.style.top  = `${top}px`;
    document.body.appendChild(floater);

    setTimeout(() => floater.remove(), 900);
  }

  // ── 6. Button Effects: Ripple, Bounce & Shake ──────────────────────
  function addRipple(targetEl, isWrong = false) {
    if (!targetEl || typeof targetEl.getBoundingClientRect !== 'function') return;
    const rect = targetEl.getBoundingClientRect();
    const ripple = document.createElement('span');
    ripple.className = 'osmosis-ripple' + (isWrong ? ' wrong-ripple' : '');
    const size = Math.max(rect.width, rect.height) * 1.4;
    ripple.style.width = ripple.style.height = `${size}px`;
    ripple.style.left = `${rect.width / 2 - size / 2}px`;
    ripple.style.top  = `${rect.height / 2 - size / 2}px`;

    const currentPos = window.getComputedStyle(targetEl).position;
    if (currentPos === 'static') targetEl.style.position = 'relative';
    targetEl.style.overflow = 'hidden';

    targetEl.appendChild(ripple);
    setTimeout(() => ripple.remove(), 550);
  }

  function bounce(el) {
    if (!el) return;
    el.classList.remove('osmosis-bounce');
    void el.offsetWidth;
    el.classList.add('osmosis-bounce');
    setTimeout(() => el.classList.remove('osmosis-bounce'), 450);
  }

  function shake(el) {
    if (!el) return;
    el.classList.remove('osmosis-shake');
    void el.offsetWidth;
    el.classList.add('osmosis-shake');
    if (navigator.vibrate) {
      try { navigator.vibrate([35, 40, 35]); } catch (_) {}
    }
    setTimeout(() => el.classList.remove('osmosis-shake'), 420);
  }

  // ── 7. Stage Clear / Interstitial Video Portal ─────────────────────
  let portalEl = null;

  function ensurePortal() {
    if (portalEl) return;
    portalEl = document.createElement('div');
    portalEl.id = 'osmosis-transition-portal';
    portalEl.innerHTML = `
      <div class="osmosis-portal-video-box">
        <video id="osmosis-portal-video" class="osmosis-portal-video" autoplay muted playsinline></video>
      </div>
      <div class="osmosis-portal-caption" id="osmosis-portal-caption">Stage Completed!</div>
    `;
    document.body.appendChild(portalEl);
  }

  function playStagePortal(videoFile = 'Done.mp4', caption = 'Stage Complete!', duration = 1500) {
    ensurePortal();
    const vid = document.getElementById('osmosis-portal-video');
    const cap = document.getElementById('osmosis-portal-caption');
    if (vid) vid.src = ANIM_PATH + videoFile;
    if (cap) cap.textContent = caption;

    requestAnimationFrame(() => {
      portalEl.classList.add('active');
      if (vid) vid.play().catch(() => {});
    });

    setTimeout(() => {
      portalEl.classList.remove('active');
    }, duration);
  }

  // ── 8. Page Specific Embeds (Hall of Fame & Results) ────────────────
  function runPageSpecific() {
    // ── Hall of Fame (10b_stage8_complete.html) retains its original trophy without tick replacement ──

    // ── Final Results (11_results.html & multiplayer_results.html) ──
    if (pageName === '11_results.html' || pageName === 'multiplayer_results.html') {
      const scoreHost = document.getElementById('res-score');
      const avatarHost = document.getElementById('player-avatar-display');
      const host = avatarHost || scoreHost;

      if (host && !document.getElementById('osmosis-results-chick-wrap')) {
        const chickWrap = document.createElement('div');
        chickWrap.id = 'osmosis-results-chick-wrap';
        chickWrap.className = 'osmosis-chick-box';
        chickWrap.innerHTML = `
          <div class="osmosis-chick-container" id="osmosis-chick-lottie-container"></div>
          <div class="osmosis-chick-caption">🐣 Scholar Hatched!</div>
        `;
        host.parentNode.insertBefore(chickWrap, host);

        const targetContainer = document.getElementById('osmosis-chick-lottie-container');

        const loadChickAnim = () => {
          if (lottieChickData && window.lottie && targetContainer) {
            try {
              window.lottie.loadAnimation({
                container: targetContainer,
                renderer: 'svg',
                loop: true,
                autoplay: true,
                animationData: lottieChickData
              });
              return;
            } catch (_) {}
          }
          // If offline or data not ready, fallback to high-res video or emoji
          if (targetContainer) {
            targetContainer.innerHTML = `
              <video autoplay muted loop playsinline style="width:100%;height:100%;border-radius:50%;object-fit:cover;">
                <source src="${ANIM_PATH}Success Loader.mp4" type="video/mp4">
              </video>
            `;
          }
        };

        ensureLottieLibrary(loadChickAnim);
        setTimeout(loadChickAnim, 500);
      }
    }
  }

  // ── 9. Intercept Game Events (AudioManager + DOM Observer) ─────────
  function attachEventWatchers() {
    // Intercept AudioManager so any stage audio instantly triggers matching juice
    const hookAudio = () => {
      if (!window.AudioManager || window.AudioManager._juiceHooked) return;
      window.AudioManager._juiceHooked = true;

      const prevPlay = window.AudioManager.play.bind(window.AudioManager);
      window.AudioManager.play = function (sound, ...args) {
        prevPlay(sound, ...args);
        if (sound === 'success' || sound === 'correct' || sound === 'match') {
          flashCorrect();
          spawnScoreFloater(10, window.innerWidth / 2 - 50, window.innerHeight / 2 - 20, false);
        } else if (sound === 'wrong' || sound === 'error') {
          spawnScoreFloater(0, window.innerWidth / 2 - 50, window.innerHeight / 2 - 20, true);
        }
      };
    };

    hookAudio();
    // ⚡ PERF FIX: Only poll for AudioManager on game pages. Poll limit reduced: 15 × 150ms = 2.25s max.
    if (needsLottie) {
      let pollCount = 0;
      const pollInterval = setInterval(() => {
        hookAudio();
        if (window.AudioManager && window.AudioManager._juiceHooked) clearInterval(pollInterval);
        if (++pollCount > 15) clearInterval(pollInterval);
      }, 150);
    }

    // Dynamic DOM Mutation Observer for direct clicks, option selections, and classes
    // ⚡ PERF FIX: Only run on actual game stage pages — not on home/menu/results.
    const GAME_PAGES = /^(03_|04_|05_|06_|07_|08_|09_|10_|module_word_hunt|stage)/i;
    if (GAME_PAGES.test(pageName)) {
      let mutationScheduled = false;
      let pendingMutations = [];

      const observer = new MutationObserver((mutations) => {
        // ⚡ PERF FIX: Batch process via rAF instead of running synchronously on every mutation.
        pendingMutations.push(...mutations);
        if (!mutationScheduled) {
          mutationScheduled = true;
          requestAnimationFrame(() => {
            const batch = pendingMutations.splice(0);
            mutationScheduled = false;
            for (const m of batch) {
              const target = m.target;
              if (m.type === 'attributes' && m.attributeName === 'class' && target && target.nodeType === 1) {
                const cls = (typeof target.className === 'string')
                  ? target.className
                  : (target.className && target.className.baseVal ? target.className.baseVal : '');
                if (!cls) continue;

                if ((cls.includes('correct') || cls.includes('answered-correct')) && !target._juiceFired) {
                  target._juiceFired = true;
                  bounce(target);
                  addRipple(target, false);
                  flashCorrect();
                  const r = target.getBoundingClientRect();
                  spawnScoreFloater(10, r.left + r.width / 2 - 45, r.top - 20, false);
                  setTimeout(() => { target._juiceFired = false; }, 600);
                } else if ((cls.includes('wrong') || cls.includes('wrong-pick')) && !target._juiceWrongFired) {
                  target._juiceWrongFired = true;
                  shake(target);
                  addRipple(target, true);
                  const r = target.getBoundingClientRect();
                  spawnScoreFloater(0, r.left + r.width / 2 - 45, r.top - 20, true);
                  setTimeout(() => { target._juiceWrongFired = false; }, 600);
                }
              }
            }
          });
        }
      });

      observer.observe(document.body, {
        attributes: true,
        attributeFilter: ['class'],
        subtree: true
      });

      // Disconnect observer when page is hidden to save CPU while backgrounded
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) observer.disconnect();
        else observer.observe(document.body, { attributes: true, attributeFilter: ['class'], subtree: true });
      });
    }
  }

  // ── 10. Bootstrap ──────────────────────────────────────────────────
  function init() {
    injectStyles();
    preloadAssets();
    attachEventWatchers();
    runPageSpecific();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Public API
  window.OsmosisJuice = {
    flashCorrect,
    spawnScoreFloater,
    bounce,
    shake,
    addRipple,
    playStagePortal
  };
})();
