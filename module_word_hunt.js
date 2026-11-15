// =====================================================================
// FILE: module_word_hunt.js
// STEM Word Hunt 2.0 — Full Dictionary + Stage 7 Split-Sentence Engine
// Real-Time Sunlit Forest Backdrop, Procedural Melody & Flow Psychology
// =====================================================================

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  // ── DOM References ─────────────────────────────────────────────────
  const textLayer = document.getElementById('text-layer');
  const highlightsLayer = document.getElementById('highlights-layer');
  const wordsEl = document.getElementById('hunt-words');
  const scoreEl = document.getElementById('hunt-score');
  const lvlBadge = document.getElementById('hunt-lvl-badge');
  const comboBadge = document.getElementById('combo-badge');
  const poolLabel = document.getElementById('hunt-pool-label');
  const hintClueBanner = document.getElementById('hint-clue-banner');
  const huntArena = document.getElementById('hunt-arena');
  const wordsCard = document.querySelector('.words-card');
  const gridWrapper = document.getElementById('grid-wrapper');
  const fxCanvas = document.getElementById('fx-canvas');
  const fxCtx = fxCanvas ? fxCanvas.getContext('2d') : null;

  // Dock & Header Controls
  const backBtn = document.getElementById('back-home-btn');
  const bookBtn = document.getElementById('book-btn');
  const hintBtn = document.getElementById('hint-btn');
  const hintBtnLabel = document.getElementById('hint-btn-label');
  const musicToggleBtn = document.getElementById('music-toggle-btn');
  const musicToggleIcon = document.getElementById('music-toggle-icon');
  const musicToggleLabel = document.getElementById('music-toggle-label');
  const leagueBtn = document.getElementById('league-btn');
  const btnSettings = document.getElementById('settings-btn');
  const helpBtn = document.getElementById('help-btn');
  const statsHeaderTrigger = document.getElementById('stats-header-trigger');

  // Difficulty & Stats Modals
  const difficultyOverlay = document.getElementById('difficulty-overlay');
  const btnEasy = document.getElementById('diff-easy');
  const btnMedium = document.getElementById('diff-medium');
  const btnIntellect = document.getElementById('diff-intellect');
  const btnCancelDiff = document.getElementById('diff-cancel-btn');
  const xpBreakdownOverlay = document.getElementById('xp-breakdown-overlay');
  const xpBreakdownClose = document.getElementById('xp-breakdown-close');

  // Definition Study Overlay (Phase 1)
  const defOverlay = document.getElementById('def-popup-overlay');
  const defTitle = document.getElementById('def-popup-title');
  const defTag = document.getElementById('def-popup-tag');
  const defSpeakBtn = document.getElementById('def-speak-btn');
  const defDesc = document.getElementById('def-popup-desc');
  const defContinueBtn = document.getElementById('def-popup-continue');

  // Stage 7 Split-Sentence Overlay (Phase 2)
  const s7Overlay = document.getElementById('hunt-stage7-overlay');
  const s7WordEl = document.getElementById('s7-hunt-word');
  const s7ComboPill = document.getElementById('s7-combo-pill');
  const s7ProgressEl = document.getElementById('s7-hunt-progress');
  const s7StepDots = document.getElementById('s7-step-dots');
  const s7SentenceCard = document.getElementById('s7-sentence-card');
  const s7OptionsGrid = document.getElementById('s7-options-grid');
  const s7FeedbackEl = document.getElementById('s7-feedback');
  const s7SkipBtn = document.getElementById('s7-skip-btn');
  const s7NextBtn = document.getElementById('s7-next-btn');

  // Book & Win Overlays
  const bookOverlay = document.getElementById('book-popup-overlay');
  const bookList = document.getElementById('book-definitions-list');
  const bookContinueBtn = document.getElementById('book-popup-continue');
  const winOverlay = document.getElementById('win-overlay');
  const promoStar = document.getElementById('promotion-star');
  const overlayHomeBtn = document.getElementById('overlay-home-btn');
  const overlayContinueBtn = document.getElementById('overlay-continue-btn');

  // Wizard Overlay
  const wizardOverlay = document.getElementById('guiding-wizard-overlay');
  const wizardNextBtn = document.getElementById('wizard-next-btn');
  const wizardBackBtn = document.getElementById('wizard-back-btn');
  const wizardSteps = document.querySelectorAll('.wizard-step');
  const wizardDots = document.querySelectorAll('.wizard-progress-dots .dot');

  // ── Difficulty Configs ─────────────────────────────────────────────
  const DIFFICULTY_CONFIGS = {
    easy:      { key: 'easy',      lvl: 'Easy',      words: 3, maxLen: 5,  grid: 6,  freeHints: 1, dirs: [[0, 1], [1, 0]] },
    medium:    { key: 'medium',    lvl: 'Medium',    words: 5, maxLen: 7,  grid: 8,  freeHints: 1, dirs: [[0, 1], [1, 0], [1, 1]] },
    intellect: { key: 'intellect', lvl: 'Intellect', words: 7, maxLen: 10, grid: 10, freeHints: 2, dirs: [[0, 1], [1, 0], [1, 1], [-1, 1], [0, -1], [-1, 0], [-1, -1], [1, -1]] }
  };

  const STOP_WORDS = new Set([
    'that', 'with', 'this', 'have', 'they', 'their', 'them', 'what', 'which',
    'when', 'where', 'who', 'whom', 'whose', 'why', 'how', 'some', 'such',
    'than', 'very', 'will', 'just', 'should', 'also', 'into', 'only', 'about',
    'many', 'then', 'would', 'like', 'these', 'because', 'could', 'been',
    'much', 'even', 'from', 'were', 'there', 'used', 'part', 'made', 'each',
    'other', 'another', 'called', 'known', 'forms', 'type', 'types', 'form',
    'most', 'more', 'both', 'between', 'during', 'through', 'under', 'after',
    'before', 'while', 'since', 'still', 'often', 'found', 'using', 'make'
  ]);

  const PILL_COLORS = ['#34d399', '#38bdf8', '#fbbf24', '#a78bfa', '#fb7185', '#2dd4bf', '#60a5fa'];

  // ── Game State ─────────────────────────────────────────────────────
  let currentLevelObj = DIFFICULTY_CONFIGS.medium;
  let gridSize = 8;
  let numWords = 5;
  let grid = [];
  let targetWords = [];
  let foundWords = [];
  let wordCoordinates = {};
  let wordDefinitions = {};
  let wordMeta = {}; // { [WORD]: { source: 'Core' | 'Dictionary' | 'Review', category?: string } }
  let occupiedCells = new Set();

  let roundScore = 0;
  let flowStreak = 0; // consecutive clean actions -> scales multiplier 1x .. 3x
  let hintsRemaining = 1;
  let usedHintThisRound = false;
  let stageStartTime = null;
  let gameInProgress = false;
  let roundWon = false;

  let isSelecting = false;
  let startCell = null;
  let lastValidEndCell = null;
  let selectionPill = null;
  let colorIndex = 0;
  let activeHintCellEl = null;

  // Stage 7 Modal State
  let s7State = {
    word: '',
    sentences: [],
    sentenceIndex: 0,
    currentBlank: null,
    selectedOption: null,
    isAnswered: false,
    firstTryClean: true,
    advanceTimer: null
  };

  // Cached Unified Dictionary Corpus
  let cachedCorpus = null;

  function esc(str) {
    return String(str || '').replace(/[&<>'"]/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
    }[c] || c));
  }

  // ===================================================================
  // 1. REAL-TIME SUNLIT FOREST CANVAS ENGINE (God Rays, Fireflies, Ferns)
  // ===================================================================
  const ForestAtmosphere = (() => {
    const canvas = document.getElementById('forest-atmosphere-canvas');
    const ctx = canvas ? canvas.getContext('2d') : null;
    const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let width = 0;
    let height = 0;
    let fireflies = [];
    let leaves = [];
    let energyBoost = 0;
    let rafId = null;
    let lastTs = 0;

    function resize() {
      if (!canvas) return;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      if (ctx) ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function seedParticles() {
      fireflies = [];
      const count = width < 640 ? 24 : 42;
      for (let i = 0; i < count; i++) {
        fireflies.push({
          x: Math.random() * width,
          y: Math.random() * height,
          r: Math.random() * 2.2 + 1.1,
          vx: (Math.random() - 0.5) * 14,
          vy: -(Math.random() * 12 + 4),
          phase: Math.random() * Math.PI * 2,
          hue: Math.random() > 0.35 ? '110, 231, 183' : '253, 224, 71'
        });
      }

      leaves = [];
      const leafCount = width < 640 ? 6 : 12;
      for (let i = 0; i < leafCount; i++) {
        leaves.push({
          x: Math.random() * width,
          y: Math.random() * height,
          size: Math.random() * 5 + 4,
          vy: Math.random() * 14 + 10,
          vx: Math.random() * 12 - 6,
          sway: Math.random() * Math.PI * 2,
          rot: Math.random() * Math.PI
        });
      }
    }

    function pulse(amount = 1) {
      energyBoost = Math.min(2.5, energyBoost + amount);
    }

    function drawGodRays(t) {
      if (!ctx) return;
      const rays = 4;
      for (let i = 0; i < rays; i++) {
        const sway = Math.sin(t * 0.00025 + i * 1.4) * (width * 0.04);
        const topX = width * (0.18 + i * 0.22) + sway;
        const botX = topX + width * 0.16;
        const grad = ctx.createLinearGradient(topX, 0, botX, height * 0.85);
        const alpha = (0.045 + Math.sin(t * 0.0005 + i) * 0.015) * (1 + energyBoost * 0.45);
        grad.addColorStop(0, `rgba(254, 240, 138, ${alpha.toFixed(4)})`);
        grad.addColorStop(0.5, `rgba(110, 231, 183, ${(alpha * 0.55).toFixed(4)})`);
        grad.addColorStop(1, 'rgba(16, 185, 129, 0)');

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.moveTo(topX - 35, 0);
        ctx.lineTo(topX + 45, 0);
        ctx.lineTo(botX + 120, height);
        ctx.lineTo(botX - 80, height);
        ctx.closePath();
        ctx.fill();
      }
    }

    function drawFernFronds(t) {
      if (!ctx) return;
      const corners = [
        { x: -10, y: height + 10, dir: 1 },
        { x: width + 10, y: height + 10, dir: -1 }
      ];
      ctx.save();
      ctx.fillStyle = 'rgba(4, 20, 12, 0.45)';
      corners.forEach((c, idx) => {
        for (let b = 0; b < 4; b++) {
          const sway = Math.sin(t * 0.0011 + b + idx * 2) * 0.05;
          const angle = c.dir * (-0.35 - b * 0.24) + sway;
          const len = Math.min(width, height) * (0.22 - b * 0.025);
          ctx.save();
          ctx.translate(c.x, c.y);
          ctx.rotate(angle);
          ctx.beginPath();
          ctx.moveTo(0, 0);
          ctx.quadraticCurveTo(c.dir * len * 0.5, -len * 0.45, c.dir * len, -len * 0.9);
          ctx.quadraticCurveTo(c.dir * len * 0.35, -len * 0.2, 0, 0);
          ctx.fill();
          ctx.restore();
        }
      });
      ctx.restore();
    }

    function tick(ts) {
      if (!ctx) return;
      if (!lastTs) lastTs = ts;
      const dt = Math.min(0.05, (ts - lastTs) / 1000);
      lastTs = ts;

      if (energyBoost > 0) energyBoost = Math.max(0, energyBoost - dt * 0.9);

      ctx.clearRect(0, 0, width, height);
      drawGodRays(ts);

      // Floating glowing fireflies
      const speedMul = 1 + energyBoost * 1.4;
      for (let i = 0; i < fireflies.length; i++) {
        const f = fireflies[i];
        f.x += (f.vx + Math.sin(ts * 0.001 + f.phase) * 10) * dt * speedMul;
        f.y += f.vy * dt * speedMul;
        if (f.y < -15) {
          f.y = height + 15;
          f.x = Math.random() * width;
        }
        if (f.x < -15) f.x = width + 15;
        if (f.x > width + 15) f.x = -15;

        const pulseAlpha = 0.32 + 0.45 * (0.5 + 0.5 * Math.sin(ts * 0.0025 + f.phase));
        const alpha = Math.min(0.95, pulseAlpha + energyBoost * 0.22);

        const glow = ctx.createRadialGradient(f.x, f.y, 0, f.x, f.y, f.r * 5.2);
        glow.addColorStop(0, `rgba(${f.hue}, ${alpha})`);
        glow.addColorStop(0.45, `rgba(${f.hue}, ${(alpha * 0.35).toFixed(3)})`);
        glow.addColorStop(1, `rgba(${f.hue}, 0)`);
        ctx.fillStyle = glow;
        ctx.beginPath();
        ctx.arc(f.x, f.y, f.r * 5.2, 0, Math.PI * 2);
        ctx.fill();
      }

      // Drifting soft foliage motes
      ctx.save();
      for (let i = 0; i < leaves.length; i++) {
        const l = leaves[i];
        l.y += l.vy * dt;
        l.x += (l.vx + Math.sin(ts * 0.0012 + l.sway) * 18) * dt;
        l.rot += dt * 0.6;
        if (l.y > height + 20) {
          l.y = -20;
          l.x = Math.random() * width;
        }
        ctx.save();
        ctx.translate(l.x, l.y);
        ctx.rotate(l.rot);
        ctx.fillStyle = 'rgba(134, 239, 172, 0.22)';
        ctx.beginPath();
        ctx.ellipse(0, 0, l.size, l.size * 0.45, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
      ctx.restore();

      drawFernFronds(ts);
      rafId = requestAnimationFrame(tick);
    }

    function start() {
      if (!canvas || !ctx || reducedMotion) return;
      resize();
      seedParticles();
      if (!rafId) rafId = requestAnimationFrame(tick);
    }

    function stop() {
      if (rafId) {
        cancelAnimationFrame(rafId);
        rafId = null;
        lastTs = 0;
      }
    }

    window.addEventListener('resize', resize);
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) stop();
      else start();
    });

    return { start, pulse };
  })();

  // ===================================================================
  // 2. PROCEDURAL REAL-TIME FOREST MELODY ENGINE (Web Audio API)
  // ===================================================================
  const ForestAudioEngine = (() => {
    const PREF_KEY = 'osmosis_hunt_music';
    // Peaceful F-Major / D-Minor forest pentatonic notes (warm, calming, scholarly)
    const SCALE = [293.66, 329.63, 349.23, 440.00, 523.25, 587.33, 659.25];
    const CHORD_PADS = [
      [146.83, 220.00], // Dm
      [174.61, 261.63], // F
      [130.81, 196.00], // C
      [196.00, 293.66]  // Gm/D
    ];

    let isEnabled = localStorage.getItem(PREF_KEY) !== 'false';
    let isPlaying = false;
    let melodyTimer = null;
    let masterGain = null;
    let padStep = 0;
    let phrasePos = 0;

    function updateButtonUI() {
      if (!musicToggleBtn) return;
      if (isEnabled) {
        musicToggleBtn.classList.add('active-state');
        if (musicToggleIcon) musicToggleIcon.textContent = '🎵';
        if (musicToggleLabel) musicToggleLabel.textContent = 'Melody On';
      } else {
        musicToggleBtn.classList.remove('active-state');
        if (musicToggleIcon) musicToggleIcon.textContent = '🔇';
        if (musicToggleLabel) musicToggleLabel.textContent = 'Melody Off';
      }
    }

    function ensureMaster() {
      if (typeof AudioManager === 'undefined') return null;
      AudioManager.init();
      const ctx = AudioManager.ctx;
      if (!ctx) return null;
      if (ctx.state === 'suspended') {
        try { ctx.resume(); } catch (e) {}
      }
      if (!masterGain) {
        masterGain = ctx.createGain();
        masterGain.gain.setValueAtTime(0.85, ctx.currentTime);
        masterGain.connect(ctx.destination);
      }
      return ctx;
    }

    function playKalimbaNote(ctx, freq, gainPeak, durationSec) {
      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const overtone = ctx.createOscillator();
      const filter = ctx.createBiquadFilter();
      const gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now);

      overtone.type = 'triangle';
      overtone.frequency.setValueAtTime(freq * 2, now);

      const overtoneGain = ctx.createGain();
      overtoneGain.gain.setValueAtTime(0.18, now);

      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(1600, now);
      filter.frequency.exponentialRampToValueAtTime(420, now + durationSec);

      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.linearRampToValueAtTime(gainPeak, now + 0.04);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + durationSec);

      osc.connect(filter);
      overtone.connect(overtoneGain);
      overtoneGain.connect(filter);
      filter.connect(gain);
      gain.connect(masterGain);

      osc.start(now);
      overtone.start(now);
      osc.stop(now + durationSec + 0.05);
      overtone.stop(now + durationSec + 0.05);
    }

    function playWarmPad(ctx, freqs) {
      const now = ctx.currentTime;
      freqs.forEach(freq => {
        const osc = ctx.createOscillator();
        const filter = ctx.createBiquadFilter();
        const gain = ctx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now);

        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(520, now);

        gain.gain.setValueAtTime(0.0001, now);
        gain.gain.linearRampToValueAtTime(0.028, now + 1.2);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 4.8);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(masterGain);

        osc.start(now);
        osc.stop(now + 4.9);
      });
    }

    function scheduleNextNote() {
      if (!isPlaying || !isEnabled || document.hidden) return;
      const ctx = ensureMaster();
      if (!ctx) return;

      // Every 4th phrase note plays a gentle underlying forest pad chord
      if (phrasePos % 4 === 0) {
        playWarmPad(ctx, CHORD_PADS[padStep % CHORD_PADS.length]);
        padStep++;
      }

      // Gentle breathing melodic arpeggio with occasional soft rests
      if (Math.random() > 0.16) {
        const idx = (phrasePos % 2 === 0)
          ? Math.floor(Math.random() * 4)
          : Math.floor(Math.random() * SCALE.length);
        playKalimbaNote(ctx, SCALE[idx], 0.045, 2.2);
      }

      phrasePos++;
      const nextDelay = 1250 + Math.floor(Math.random() * 1100);
      melodyTimer = setTimeout(scheduleNextNote, nextDelay);
    }

    function startIfEnabled() {
      updateButtonUI();
      if (!isEnabled || isPlaying) return;
      const ctx = ensureMaster();
      if (!ctx) return;
      isPlaying = true;
      scheduleNextNote();
    }

    function stop() {
      isPlaying = false;
      if (melodyTimer) {
        clearTimeout(melodyTimer);
        melodyTimer = null;
      }
    }

    function toggle() {
      isEnabled = !isEnabled;
      localStorage.setItem(PREF_KEY, isEnabled ? 'true' : 'false');
      updateButtonUI();
      if (isEnabled) startIfEnabled();
      else stop();
    }

    function duck(ducked) {
      if (!masterGain || typeof AudioManager === 'undefined' || !AudioManager.ctx) return;
      const ctx = AudioManager.ctx;
      const target = ducked ? 0.22 : 0.85;
      masterGain.gain.setTargetAtTime(target, ctx.currentTime, 0.25);
    }

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) stop();
      else if (isEnabled) startIfEnabled();
    });

    updateButtonUI();
    return { startIfEnabled, stop, toggle, duck, isEnabled: () => isEnabled };
  })();

  // ===================================================================
  // 3. GRID CANVAS PARTICLE BURSTS & FLOATING XP
  // ===================================================================
  let particles = [];
  let particleLoopRunning = false;

  function resizeFxCanvas() {
    if (!fxCanvas || !textLayer) return;
    fxCanvas.width = textLayer.clientWidth || 300;
    fxCanvas.height = textLayer.clientHeight || 300;
  }

  function triggerParticleExplosion(start, end) {
    if (!fxCtx || !textLayer) return;
    resizeFxCanvas();
    const cw = textLayer.clientWidth / gridSize;
    const ch = textLayer.clientHeight / gridSize;
    const startX = (start.c + 0.5) * cw;
    const startY = (start.r + 0.5) * ch;
    const endX = (end.c + 0.5) * cw;
    const endY = (end.r + 0.5) * ch;
    const colors = ['#10b981', '#34d399', '#fbbf24', '#38bdf8', '#f472b6'];

    for (let i = 0; i < 38; i++) {
      const t = Math.random();
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 5 + 2;
      particles.push({
        x: startX + (endX - startX) * t,
        y: startY + (endY - startY) * t,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        radius: Math.random() * 4.5 + 2.5,
        color: colors[Math.floor(Math.random() * colors.length)],
        life: 1
      });
    }

    if (!particleLoopRunning) {
      particleLoopRunning = true;
      requestAnimationFrame(runParticleLoop);
    }
  }

  function runParticleLoop() {
    if (!fxCtx) return;
    fxCtx.clearRect(0, 0, fxCanvas.width, fxCanvas.height);
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.14;
      p.life -= 0.026;
      ctxDrawParticle(p);
      if (p.life <= 0) particles.splice(i, 1);
    }
    if (particles.length > 0) requestAnimationFrame(runParticleLoop);
    else particleLoopRunning = false;
  }

  function ctxDrawParticle(p) {
    fxCtx.save();
    fxCtx.globalAlpha = Math.max(0, p.life);
    fxCtx.fillStyle = p.color;
    fxCtx.beginPath();
    fxCtx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    fxCtx.fill();
    fxCtx.restore();
  }

  function triggerFloatingXPBadge(endCell, text) {
    if (!textLayer || !gridWrapper) return;
    const cw = textLayer.clientWidth / gridSize;
    const ch = textLayer.clientHeight / gridSize;
    const posX = Math.max(10, Math.min(textLayer.clientWidth - 95, (endCell.c + 0.5) * cw - 40));
    const posY = Math.max(8, (endCell.r + 0.5) * ch - 18);

    const badge = document.createElement('div');
    badge.className = 'xp-float-badge';
    badge.textContent = text;
    badge.style.left = `${posX}px`;
    badge.style.top = `${posY}px`;
    gridWrapper.appendChild(badge);
    setTimeout(() => badge.remove(), 980);
  }

  // ===================================================================
  // 4. RESPONSIVE FIT-TO-SCREEN VIEWPORT SIZING
  // ===================================================================
  function fitGridToViewport() {
    if (!huntArena || !wordsCard || !gridWrapper) return;
    const arenaRect = huntArena.getBoundingClientRect();
    const wordsRect = wordsCard.getBoundingClientRect();
    const gridCard = gridWrapper.closest('.grid-card');

    let cardPadW = 20;
    let cardPadH = 20;
    if (gridCard) {
      const cardStyle = window.getComputedStyle(gridCard);
      cardPadW = (parseFloat(cardStyle.paddingLeft) || 6) + (parseFloat(cardStyle.paddingRight) || 6) +
                 (parseFloat(cardStyle.borderLeftWidth) || 1.5) + (parseFloat(cardStyle.borderRightWidth) || 1.5);
      cardPadH = (parseFloat(cardStyle.paddingTop) || 6) + (parseFloat(cardStyle.paddingBottom) || 6) +
                 (parseFloat(cardStyle.borderTopWidth) || 1.5) + (parseFloat(cardStyle.borderBottomWidth) || 1.5);
    }

    const availW = Math.max(160, arenaRect.width - cardPadW - 6);
    const availH = Math.max(160, arenaRect.height - wordsRect.height - cardPadH - 8);
    const squarePx = Math.max(170, Math.min(540, Math.floor(Math.min(availW, availH))));

    document.documentElement.style.setProperty('--grid-size-px', `${squarePx}px`);
    const cellPx = squarePx / Math.max(gridSize, 6);
    const fontPx = Math.max(12, Math.min(30, Math.floor(cellPx * 0.54)));
    document.documentElement.style.setProperty('--cell-font-px', `${fontPx}px`);

    requestAnimationFrame(() => {
      resizeFxCanvas();
      realignFoundPills();
    });
  }

  if (typeof ResizeObserver !== 'undefined' && huntArena) {
    const ro = new ResizeObserver(() => fitGridToViewport());
    ro.observe(huntArena);
  }
  window.addEventListener('resize', fitGridToViewport);

  // ===================================================================
  // 5. STAGE 7 SENTENCE SEGMENTER & FULL DICTIONARY CORPUS
  // ===================================================================
  function segmentDefinition(text) {
    if (!text) return [];
    const clean = String(text)
      .replace(/<\/?[^>]+(>|$)/g, ' ')
      .replace(/^\s*\d+\.\s*/, '')
      .replace(/\b(e\.g\.|i\.e\.|etc\.|vs\.|Fig\.|Dr\.|approx\.)/gi, m => m.replace(/\./g, '§DOT§'))
      .replace(/(\d)\.(\d)/g, '$1§DOT§$2')
      .replace(/\s+/g, ' ')
      .trim();

    const parts = clean.split(/(?<=[.!?])\s+(?=[A-Z0-9])/);
    let sentences = parts
      .map(p => p.replace(/§DOT§/g, '.').replace(/\s+\d+\.?$/, '').trim())
      .filter(p => p.length >= 16 && !p.includes('$$'));

    if (sentences.length === 0) {
      clean.replace(/§DOT§/g, '.').split(/;\s+/).forEach(sp => {
        const s = sp.trim();
        if (s.length >= 16 && !s.includes('$$')) sentences.push(s);
      });
    }

    if (sentences.length === 0) {
      const strippedMath = clean.replace(/§DOT§/g, '.').replace(/\$\$[^$]+\$\$/g, '').replace(/\$[^$]+\$/g, 'formula').trim();
      if (strippedMath.length >= 12) sentences.push(strippedMath);
    }

    return sentences.slice(0, 3);
  }

  function pickBlankCandidate(sentence, targetWord) {
    const tokens = sentence.split(/(\b[a-zA-Z]{3,}\b)/);
    const targetLower = String(targetWord || '').toLowerCase();
    const candidates = [];

    tokens.forEach((t, i) => {
      if (/^[a-zA-Z]{4,}$/.test(t)) {
        const lower = t.toLowerCase();
        if (!STOP_WORDS.has(lower) && lower !== targetLower) {
          candidates.push({ index: i, word: t, length: t.length });
        }
      }
    });

    if (candidates.length === 0) {
      tokens.forEach((t, i) => {
        if (/^[a-zA-Z]{4,}$/.test(t) && t.toLowerCase() !== targetLower) {
          candidates.push({ index: i, word: t, length: t.length });
        }
      });
    }

    if (candidates.length === 0) return null;
    candidates.sort((a, b) => b.length - a.length);
    return { tokens, chosen: candidates[0] };
  }

  function isCleanScientificEntry(rawWord, rawDef) {
    const cleanWord = String(rawWord || '').trim();
    if (!/^[a-zA-Z]{3,10}$/.test(cleanWord)) return false;
    if (/^(.)\1{2,}$/i.test(cleanWord)) return false; // filter noisy AAA/XXX stubs

    const def = String(rawDef || '').replace(/\s+/g, ' ').trim();
    if (def.length < 28) return false;
    if (/^(see |abbreviation for |plural of |alternate spelling|archaic )/i.test(def)) return false;

    const segs = segmentDefinition(def);
    if (segs.length === 0) return false;
    return segs.some(s => pickBlankCandidate(s, cleanWord) !== null);
  }

  function getUnifiedCorpus() {
    if (cachedCorpus) return cachedCorpus;

    const map = new Map();

    // 1. Add all curated HuntDictionary words first
    if (window.HuntDictionary && Array.isArray(window.HuntDictionary.words)) {
      window.HuntDictionary.words.forEach(item => {
        const clean = String(item.word || '').trim().toUpperCase();
        if (isCleanScientificEntry(clean, item.definition)) {
          map.set(clean, {
            word: clean,
            definition: item.definition.trim(),
            category: item.category || 'STEM Core',
            source: 'Core'
          });
        }
      });
    }

    // 2. Integrate ALL clean words from main STEMDictionary (~8,600+ clean 3-10 char entries)
    if (window.STEMDictionary && typeof window.STEMDictionary.getAllWords === 'function') {
      const all = window.STEMDictionary.getAllWords();
      for (let i = 0; i < all.length; i++) {
        const entry = all[i];
        if (!entry || !entry.word) continue;
        const clean = String(entry.word).trim().toUpperCase();
        if (!map.has(clean) && isCleanScientificEntry(clean, entry.definition)) {
          map.set(clean, {
            word: clean,
            definition: entry.definition.replace(/\s+/g, ' ').trim(),
            category: 'STEM Dictionary',
            source: 'Dictionary'
          });
        }
      }
    }

    if (map.size === 0) {
      [
        { word: 'ATOM', definition: 'The smallest unit of ordinary matter that forms a chemical element.', category: 'Chemistry', source: 'Core' },
        { word: 'CELL', definition: 'The basic structural and functional membrane-bound unit of all living organisms.', category: 'Biology', source: 'Core' },
        { word: 'GENE', definition: 'A functional unit of heredity made of DNA instructions that build proteins.', category: 'Biology', source: 'Core' }
      ].forEach(f => map.set(f.word, f));
    }

    cachedCorpus = Array.from(map.values());
    return cachedCorpus;
  }

  function getFlowMultiplier() {
    if (flowStreak >= 6) return 3.0;
    if (flowStreak >= 4) return 2.0;
    if (flowStreak >= 2) return 1.5;
    return 1.0;
  }

  // ===================================================================
  // 6. REWARDS, STREAKS, MASTERY & PERSISTENCE (BUG-FREE ATOMIC SYNC)
  // ===================================================================
  function updateProgressionHeader() {
    const streak = parseInt(localStorage.getItem('osmosis_hunt_streak'), 10) || 0;
    const totalXP = parseInt(localStorage.getItem('osmosis_total_score'), 10) || 0;
    const gems = Math.floor(totalXP / 100);
    const level = Math.floor(totalXP / 500) + 1;
    const currentLevelXP = totalXP % 500;
    const xpPercent = Math.min(100, Math.floor((currentLevelXP / 500) * 100));

    const streakEl = document.getElementById('header-streak-count');
    const lvlTitleEl = document.getElementById('header-level-title');
    const xpTextEl = document.getElementById('header-xp-text');
    const xpFillEl = document.getElementById('header-xp-fill');
    const gemsEl = document.getElementById('header-gems-count');

    if (streakEl) streakEl.textContent = streak;
    if (lvlTitleEl) lvlTitleEl.textContent = `LVL ${level}`;
    if (xpTextEl) xpTextEl.textContent = `${currentLevelXP} / 500 XP`;
    if (xpFillEl) xpFillEl.style.width = `${xpPercent}%`;
    if (gemsEl) gemsEl.textContent = gems;
  }

  function updateScoreAndComboUI() {
    if (scoreEl) scoreEl.textContent = `${roundScore} pts`;
    if (comboBadge) {
      const mul = getFlowMultiplier();
      comboBadge.textContent = `${mul}x`;
      if (mul > 1) comboBadge.classList.add('hot');
      else comboBadge.classList.remove('hot');
    }
    if (s7ComboPill) {
      s7ComboPill.textContent = `🔥 ${getFlowMultiplier()}x`;
    }
  }

  function awardXP(basePoints) {
    const earned = Math.max(0, Math.round(basePoints * getFlowMultiplier()));
    roundScore += earned;

    const currentTotal = parseInt(localStorage.getItem('osmosis_total_score'), 10) || 0;
    localStorage.setItem('osmosis_total_score', String(currentTotal + earned));

    updateScoreAndComboUI();
    updateProgressionHeader();
    return earned;
  }

  function recordMasteredHuntWord(word) {
    try {
      const upper = String(word || '').toUpperCase();
      if (!upper) return;
      const list = JSON.parse(localStorage.getItem('osmosis_hunt_mastered_words') || '[]');
      if (!list.includes(upper)) {
        list.push(upper);
        localStorage.setItem('osmosis_hunt_mastered_words', JSON.stringify(list));
      }
    } catch (e) {}
  }

  function populateStatsModal() {
    const streak = parseInt(localStorage.getItem('osmosis_hunt_streak'), 10) || 0;
    const totalXP = parseInt(localStorage.getItem('osmosis_total_score'), 10) || 0;
    const gems = Math.floor(totalXP / 100);
    const level = Math.floor(totalXP / 500) + 1;
    const leagues = ['Bronze League', 'Silver League', 'Gold League', 'Sapphire League', 'Ruby League', 'Diamond League'];
    const leagueRank = leagues[Math.min(leagues.length - 1, Math.floor((level - 1) / 2))];

    const corpusTotal = getUnifiedCorpus().length;
    let huntMasteredCount = 0;
    try {
      huntMasteredCount = (JSON.parse(localStorage.getItem('osmosis_hunt_mastered_words') || '[]')).length;
    } catch (e) {}
    const srsStats = (typeof sharedState !== 'undefined' && sharedState.getMasteryStats)
      ? sharedState.getMasteryStats()
      : { totalTerms: 0 };

    const uniqueDiscovered = Math.max(huntMasteredCount, srsStats.totalTerms || 0);

    const rankEl = document.getElementById('modal-league-rank');
    const streakEl = document.getElementById('breakdown-streak');
    const xpEl = document.getElementById('breakdown-xp');
    const gemsEl = document.getElementById('breakdown-gems');
    const masteredEl = document.getElementById('breakdown-mastered');

    if (rankEl) rankEl.textContent = leagueRank;
    if (streakEl) streakEl.textContent = `${streak} Rounds`;
    if (xpEl) xpEl.textContent = `${totalXP.toLocaleString()} XP`;
    if (gemsEl) gemsEl.textContent = `${gems} Gems`;
    if (masteredEl) masteredEl.textContent = `${uniqueDiscovered} / ${corpusTotal.toLocaleString()}`;
  }

  // ===================================================================
  // 7. GAME INITIALIZATION & SMART WORD PICKING
  // ===================================================================
  function shuffleArray(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function initGame() {
    gameInProgress = true;
    roundWon = false;
    roundScore = 0;
    flowStreak = 0;
    usedHintThisRound = false;
    stageStartTime = Date.now();
    if (typeof initModal === 'function') initModal();

    gridSize = currentLevelObj.grid;
    numWords = currentLevelObj.words;
    hintsRemaining = currentLevelObj.freeHints;

    const streak = parseInt(localStorage.getItem('osmosis_hunt_streak'), 10) || 0;
    textLayer.style.setProperty('--grid-size', gridSize);
    lvlBadge.textContent = `${currentLevelObj.lvl} · Streak ${streak}`;
    if (hintClueBanner) {
      hintClueBanner.textContent = '';
      hintClueBanner.classList.remove('visible');
    }
    updateHintButtonUI();
    updateProgressionHeader();
    updateScoreAndComboUI();

    foundWords = [];
    wordCoordinates = {};
    wordDefinitions = {};
    wordMeta = {};
    isSelecting = false;
    startCell = null;
    lastValidEndCell = null;
    selectionPill = null;
    activeHintCellEl = null;
    highlightsLayer.innerHTML = '';
    winOverlay.classList.remove('active');

    const fullCorpus = getUnifiedCorpus();
    if (poolLabel) {
      poolLabel.textContent = `Active Dictionary: ${fullCorpus.length.toLocaleString()} verified STEM terms`;
    }

    const eligible = fullCorpus.filter(item => item.word.length <= currentLevelObj.maxLen);

    let usedWords = [];
    try {
      usedWords = JSON.parse(localStorage.getItem('wordHuntUsedWords') || '[]');
    } catch (e) { usedWords = []; }
    const usedSet = new Set(usedWords);

    let freshPool = eligible.filter(item => !usedSet.has(item.word));
    if (freshPool.length < numWords * 2) {
      // Soft-rotate oldest half instead of wiping history completely
      usedWords = usedWords.slice(Math.floor(usedWords.length / 2));
      const trimmedSet = new Set(usedWords);
      freshPool = eligible.filter(item => !trimmedSet.has(item.word));
      if (freshPool.length < numWords) {
        usedWords = [];
        freshPool = eligible.slice();
      }
    }

    shuffleArray(freshPool);

    // Optional Spaced Repetition weave: include at most 1 due review term that fits grid
    let chosenObjs = [];
    if (typeof sharedState !== 'undefined' && typeof sharedState.getDueReviewWords === 'function') {
      const due = sharedState.getDueReviewWords(12);
      for (const item of due) {
        const up = String(item.word || '').trim().toUpperCase();
        const matchObj = eligible.find(e => e.word === up);
        if (matchObj && !usedWords.slice(-15).includes(up)) {
          chosenObjs.push({ ...matchObj, source: 'Due Review' });
          break;
        }
      }
    }

    for (const candidate of freshPool) {
      if (chosenObjs.length >= numWords + 4) break; // extra reserve candidates in case placement needs fallback
      if (!chosenObjs.some(c => c.word === candidate.word)) {
        chosenObjs.push(candidate);
      }
    }

    const successBoard = buildReliableGrid(chosenObjs, numWords);
    targetWords = successBoard.placedWords;
    grid = successBoard.grid;
    wordCoordinates = successBoard.coords;
    occupiedCells = successBoard.occupied;

    targetWords.forEach(w => {
      const metaObj = chosenObjs.find(c => c.word === w);
      wordDefinitions[w] = metaObj ? metaObj.definition : 'A scientific term.';
      wordMeta[w] = metaObj || { source: 'Dictionary', category: 'STEM' };
    });

    usedWords.push(...targetWords);
    if (usedWords.length > 2500) usedWords = usedWords.slice(-2500);
    localStorage.setItem('wordHuntUsedWords', JSON.stringify(usedWords));

    renderGrid();
    renderWords();
    fitGridToViewport();
    ForestAtmosphere.start();
  }

  function buildReliableGrid(candidateObjs, desiredCount) {
    const dirs = currentLevelObj.dirs;
    let bestResult = null;

    for (let attempt = 0; attempt < 6; attempt++) {
      const workingGrid = Array(gridSize).fill(null).map(() => Array(gridSize).fill(''));
      const occupied = new Set();
      const coords = {};
      const placedWords = [];

      // Try placing longer words first for maximum grid packing success
      const batch = candidateObjs.slice(0, desiredCount + 3).sort((a, b) => b.word.length - a.word.length);

      for (const item of batch) {
        if (placedWords.length >= desiredCount) break;
        const word = item.word;
        let placed = false;

        for (let tries = 0; tries < 220; tries++) {
          const d = dirs[Math.floor(Math.random() * dirs.length)];
          const r = Math.floor(Math.random() * gridSize);
          const c = Math.floor(Math.random() * gridSize);

          if (canPlaceOnGrid(workingGrid, word, r, c, d[0], d[1])) {
            for (let i = 0; i < word.length; i++) {
              const nr = r + i * d[0];
              const nc = c + i * d[1];
              workingGrid[nr][nc] = word[i];
              occupied.add(`${nr},${nc}`);
            }
            coords[word] = {
              start: { r, c },
              end: { r: r + (word.length - 1) * d[0], c: c + (word.length - 1) * d[1] },
              dir: d
            };
            placedWords.push(word);
            placed = true;
            break;
          }
        }
        if (!placed) continue;
      }

      if (!bestResult || placedWords.length > bestResult.placedWords.length) {
        bestResult = { grid: workingGrid, occupied, coords, placedWords };
      }
      if (placedWords.length >= desiredCount) break;
    }

    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    for (let i = 0; i < gridSize; i++) {
      for (let j = 0; j < gridSize; j++) {
        if (bestResult.grid[i][j] === '') {
          bestResult.grid[i][j] = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
        }
      }
    }

    removeAccidentalWordsFromGrid(bestResult.grid, bestResult.placedWords, bestResult.coords, bestResult.occupied);
    return bestResult;
  }

  function canPlaceOnGrid(targetGrid, word, r, c, dr, dc) {
    for (let i = 0; i < word.length; i++) {
      const nr = r + i * dr;
      const nc = c + i * dc;
      if (nr < 0 || nr >= gridSize || nc < 0 || nc >= gridSize) return false;
      if (targetGrid[nr][nc] !== '' && targetGrid[nr][nc] !== word[i]) return false;
    }
    return true;
  }

  function removeAccidentalWordsFromGrid(targetGrid, words, coords, occupied) {
    const dirs = [[0, 1], [1, 0], [1, 1], [-1, 1], [0, -1], [-1, 0], [-1, -1], [1, -1]];
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let foundAccidental = true;
    let iterations = 0;

    while (foundAccidental && iterations < 60) {
      foundAccidental = false;
      iterations++;

      for (const word of words) {
        const len = word.length;
        const coord = coords[word];
        if (!coord) continue;

        for (let r = 0; r < gridSize; r++) {
          for (let c = 0; c < gridSize; c++) {
            for (const [dr, dc] of dirs) {
              const endR = r + (len - 1) * dr;
              const endC = c + (len - 1) * dc;
              if (endR < 0 || endR >= gridSize || endC < 0 || endC >= gridSize) continue;

              let match = true;
              for (let i = 0; i < len; i++) {
                if (targetGrid[r + i * dr][c + i * dc] !== word[i]) {
                  match = false;
                  break;
                }
              }

              if (match) {
                const isDesignated = (
                  (r === coord.start.r && c === coord.start.c && endR === coord.end.r && endC === coord.end.c) ||
                  (r === coord.end.r && c === coord.end.c && endR === coord.start.r && endC === coord.start.c)
                );
                if (!isDesignated) {
                  for (let i = 0; i < len; i++) {
                    const mr = r + i * dr;
                    const mc = c + i * dc;
                    if (!occupied.has(`${mr},${mc}`)) {
                      let nextChar;
                      do {
                        nextChar = alphabet.charAt(Math.floor(Math.random() * 26));
                      } while (nextChar === targetGrid[mr][mc]);
                      targetGrid[mr][mc] = nextChar;
                      foundAccidental = true;
                      break;
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  function renderGrid() {
    textLayer.innerHTML = '';
    for (let r = 0; r < gridSize; r++) {
      for (let c = 0; c < gridSize; c++) {
        const cell = document.createElement('div');
        cell.className = 'hunt-cell';
        cell.dataset.r = r;
        cell.dataset.c = c;
        cell.textContent = grid[r][c];
        textLayer.appendChild(cell);
      }
    }
  }

  function renderWords() {
    wordsEl.innerHTML = '';
    targetWords.forEach(w => {
      const span = document.createElement('span');
      span.className = 'hunt-word';
      span.textContent = w;
      span.id = 'word-' + w;
      wordsEl.appendChild(span);
    });
  }

  // ===================================================================
  // 8. GRID INTERACTION & HARMONIC DRAG AUDIO (ATTACHED ONCE!)
  // ===================================================================
  const pianoScale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25, 587.33, 659.25, 698.46, 783.99];
  let activeHarmonies = [];

  function playDragNote(steps) {
    if (typeof AudioManager === 'undefined') return;
    AudioManager.init();
    const ctx = AudioManager.ctx;
    if (!ctx) return;
    if (ctx.state === 'suspended') {
      try { ctx.resume(); } catch (e) {}
    }

    activeHarmonies.forEach(node => {
      try { node.osc.stop(); } catch (e) {}
    });
    activeHarmonies = [];

    const rootFreq = pianoScale[Math.min(steps, pianoScale.length - 1)];
    const playVoice = (freq, volume, delay = 0, type = 'sine') => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const filter = ctx.createBiquadFilter();
      const now = ctx.currentTime;

      osc.type = type;
      osc.frequency.setValueAtTime(freq, now);
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(1900, now);
      filter.frequency.exponentialRampToValueAtTime(120, now + 0.35);

      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.linearRampToValueAtTime(volume, now + 0.025 + delay);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.42 + delay);

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.5);
      activeHarmonies.push({ osc, gain });
    };

    const thirdRatio = steps % 2 === 0 ? 1.25 : 1.2;
    playVoice(rootFreq, 0.14, 0, 'sine');
    playVoice(rootFreq * thirdRatio, 0.08, 0.015, 'sine');
    playVoice(rootFreq * 1.5, 0.06, 0.03, 'sine');
  }

  function getCellFromEvent(e) {
    let clientX;
    let clientY;
    if (e.touches && e.touches.length > 0) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    } else if (e.changedTouches && e.changedTouches.length > 0) {
      clientX = e.changedTouches[0].clientX;
      clientY = e.changedTouches[0].clientY;
    } else {
      clientX = e.clientX;
      clientY = e.clientY;
    }

    const rect = textLayer.getBoundingClientRect();
    const x = clientX - rect.left;
    const y = clientY - rect.top;
    if (x < 0 || x > rect.width || y < 0 || y > rect.height) return null;

    const c = Math.floor(x / (rect.width / gridSize));
    const r = Math.floor(y / (rect.height / gridSize));
    if (r >= 0 && r < gridSize && c >= 0 && c < gridSize) return { r, c };
    return null;
  }

  function updatePillTransform(pill, start, end, color) {
    const cw = textLayer.clientWidth / gridSize;
    const ch = textLayer.clientHeight / gridSize;
    const x1 = start.c * cw + cw / 2;
    const y1 = start.r * ch + ch / 2;
    const x2 = end.c * cw + cw / 2;
    const y2 = end.r * ch + ch / 2;
    const distance = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
    const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
    const thickness = Math.min(cw, ch) * 0.78;

    pill.style.width = `${distance + thickness}px`;
    pill.style.height = `${thickness}px`;
    pill.style.backgroundColor = color;
    pill.style.left = `${(x1 + x2) / 2}px`;
    pill.style.top = `${(y1 + y2) / 2}px`;
    pill.style.transform = `translate(-50%, -50%) rotate(${angle}deg)`;
  }

  function realignFoundPills() {
    const pills = highlightsLayer.querySelectorAll('.highlight-pill[data-sr]');
    pills.forEach(p => {
      const start = { r: Number(p.dataset.sr), c: Number(p.dataset.sc) };
      const end = { r: Number(p.dataset.er), c: Number(p.dataset.ec) };
      updatePillTransform(p, start, end, p.style.backgroundColor);
    });
  }

  function highlightMatrixCellsInSelection() {
    if (!startCell || !lastValidEndCell) return;
    const cells = textLayer.querySelectorAll('.hunt-cell');
    cells.forEach(c => {
      c.style.transform = '';
      c.style.color = '#0f172a';
    });

    const dr = lastValidEndCell.r - startCell.r;
    const dc = lastValidEndCell.c - startCell.c;
    const steps = Math.max(Math.abs(dr), Math.abs(dc));
    const stepR = steps === 0 ? 0 : dr / steps;
    const stepC = steps === 0 ? 0 : dc / steps;

    for (let i = 0; i <= steps; i++) {
      const r = Math.round(startCell.r + stepR * i);
      const c = Math.round(startCell.c + stepC * i);
      const cellNode = cells[r * gridSize + c];
      if (cellNode) {
        cellNode.style.transform = 'scale(1.22)';
        cellNode.style.color = '#047857';
      }
    }
  }

  function handlePointerDown(e) {
    ForestAudioEngine.startIfEnabled();
    if (e.type === 'mousedown' && e.button !== 0) return;
    if (e.type === 'touchstart') e.preventDefault();

    const cellPos = getCellFromEvent(e);
    if (!cellPos) return;

    isSelecting = true;
    startCell = cellPos;
    lastValidEndCell = cellPos;

    selectionPill = document.createElement('div');
    selectionPill.className = 'highlight-pill';
    highlightsLayer.appendChild(selectionPill);

    const color = PILL_COLORS[colorIndex % PILL_COLORS.length];
    updatePillTransform(selectionPill, startCell, startCell, color);

    playDragNote(0);
    highlightMatrixCellsInSelection();
  }

  function handlePointerMove(e) {
    if (!isSelecting) return;
    if (e.type === 'touchmove') e.preventDefault();

    const cellPos = getCellFromEvent(e);
    if (!cellPos) return;

    const dr = cellPos.r - startCell.r;
    const dc = cellPos.c - startCell.c;
    if (dr === 0 || dc === 0 || Math.abs(dr) === Math.abs(dc)) {
      if (lastValidEndCell.r !== cellPos.r || lastValidEndCell.c !== cellPos.c) {
        lastValidEndCell = cellPos;
        const color = PILL_COLORS[colorIndex % PILL_COLORS.length];
        updatePillTransform(selectionPill, startCell, lastValidEndCell, color);
        playDragNote(Math.max(Math.abs(dr), Math.abs(dc)));
        highlightMatrixCellsInSelection();
      }
    }
  }

  function handlePointerUp() {
    if (!isSelecting) return;
    isSelecting = false;

    const cells = textLayer.querySelectorAll('.hunt-cell');
    cells.forEach(c => {
      c.style.transform = '';
      c.style.color = '#0f172a';
    });

    const dr = lastValidEndCell.r - startCell.r;
    const dc = lastValidEndCell.c - startCell.c;
    const steps = Math.max(Math.abs(dr), Math.abs(dc));
    const stepR = steps === 0 ? 0 : dr / steps;
    const stepC = steps === 0 ? 0 : dc / steps;

    let wordStr = '';
    for (let i = 0; i <= steps; i++) {
      const r = startCell.r + stepR * i;
      const c = startCell.c + stepC * i;
      wordStr += grid[r][c];
    }

    const wordStrRev = wordStr.split('').reverse().join('');
    const match = targetWords.find(w => w === wordStr || w === wordStrRev);

    if (match && !foundWords.includes(match)) {
      foundWords.push(match);
      flowStreak++;
      if (typeof AudioManager !== 'undefined') AudioManager.play('success');
      ForestAtmosphere.pulse(1.6);

      // Clear active hint beacon if found word matches
      if (activeHintCellEl) {
        activeHintCellEl.classList.remove('hint-pulse');
        activeHintCellEl = null;
      }
      if (hintClueBanner) hintClueBanner.classList.remove('visible');

      const notebookEl = document.querySelector('.grid-card');
      if (notebookEl) {
        notebookEl.classList.remove('impact-shake');
        void notebookEl.offsetWidth;
        notebookEl.classList.add('impact-shake');
      }

      if (selectionPill) {
        selectionPill.dataset.sr = startCell.r;
        selectionPill.dataset.sc = startCell.c;
        selectionPill.dataset.er = lastValidEndCell.r;
        selectionPill.dataset.ec = lastValidEndCell.c;
      }

      const earned = awardXP(100);
      triggerParticleExplosion(startCell, lastValidEndCell);
      triggerFloatingXPBadge(lastValidEndCell, `+${earned} XP`);

      const chip = document.getElementById('word-' + match);
      if (chip) {
        chip.classList.remove('hinted');
        chip.classList.add('found');
      }

      colorIndex++;
      selectionPill = null;

      setTimeout(() => showDefinitionPopup(match), 280);
    } else {
      if (steps > 0) {
        if (typeof AudioManager !== 'undefined') AudioManager.play('error');
      }
      if (selectionPill) {
        selectionPill.remove();
        selectionPill = null;
      }
    }

    startCell = null;
    lastValidEndCell = null;
  }

  // Attach pointer listeners ONCE cleanly
  textLayer.addEventListener('mousedown', handlePointerDown);
  document.addEventListener('mousemove', handlePointerMove);
  document.addEventListener('mouseup', handlePointerUp);
  textLayer.addEventListener('touchstart', handlePointerDown, { passive: false });
  document.addEventListener('touchmove', handlePointerMove, { passive: false });
  document.addEventListener('touchend', handlePointerUp);

  // ===================================================================
  // 9. TACTICAL HINT COMPASS (Anti-Frustration Flow Support)
  // ===================================================================
  function updateHintButtonUI() {
    if (hintBtnLabel) {
      hintBtnLabel.textContent = hintsRemaining > 0 ? `Hint (${hintsRemaining})` : 'Clue';
    }
  }

  function describeDirection(dir) {
    if (!dir) return 'Straight';
    const [dr, dc] = dir;
    if (dr === 0) return 'Horizontal';
    if (dc === 0) return 'Vertical';
    return 'Diagonal';
  }

  if (hintBtn) {
    hintBtn.addEventListener('click', () => {
      ForestAudioEngine.startIfEnabled();
      if (typeof AudioManager !== 'undefined') AudioManager.play('chip');
      const unfound = targetWords.find(w => !foundWords.includes(w));
      if (!unfound || !wordCoordinates[unfound]) return;

      usedHintThisRound = true;
      const info = wordCoordinates[unfound];
      const chip = document.getElementById('word-' + unfound);
      if (chip) chip.classList.add('hinted');

      if (activeHintCellEl) activeHintCellEl.classList.remove('hint-pulse');

      const cells = textLayer.querySelectorAll('.hunt-cell');
      const targetCell = cells[info.start.r * gridSize + info.start.c];
      if (targetCell) {
        targetCell.classList.add('hint-pulse');
        activeHintCellEl = targetCell;
      }

      if (hintsRemaining > 0) hintsRemaining--;
      updateHintButtonUI();

      if (hintClueBanner) {
        hintClueBanner.textContent = `💡 ${unfound.slice(0, 2)}… at Row ${info.start.r + 1}, Col ${info.start.c + 1} (${describeDirection(info.dir)})`;
        hintClueBanner.classList.add('visible');
      }
    });
  }

  // ===================================================================
  // 10. PHASE 1: STUDY DEFINITION + PHASE 2: STAGE 7 SPLIT-SENTENCE TEST
  // ===================================================================
  function showDefinitionPopup(word) {
    const defText = wordDefinitions[word] || 'A scientific term.';
    const meta = wordMeta[word] || { source: 'STEM Dictionary', category: 'STEM' };

    defTitle.textContent = word;
    if (defTag) {
      defTag.textContent = meta.source === 'Due Review' ? 'Spaced Review Term' : (meta.category || 'STEM Discovery');
      defTag.className = meta.source === 'Due Review' ? 'meta-tag review' : 'meta-tag';
    }

    if (typeof window.renderScienceText === 'function') {
      defDesc.removeAttribute('data-raw-content');
      defDesc.setAttribute('data-raw-content', defText);
      window.renderScienceText(defDesc);
    } else {
      defDesc.textContent = defText;
    }

    defOverlay.classList.add('active');
  }

  if (defSpeakBtn) {
    defSpeakBtn.addEventListener('click', () => {
      const word = defTitle.textContent;
      const def = wordDefinitions[word] || '';
      if (typeof VoiceManager !== 'undefined') {
        ForestAudioEngine.duck(true);
        VoiceManager.speak(`${word}. ${def}`, {
          force: true,
          onend: () => ForestAudioEngine.duck(false),
          onerror: () => ForestAudioEngine.duck(false)
        });
      }
    });
  }

  if (defContinueBtn) {
    defContinueBtn.addEventListener('click', () => {
      if (typeof VoiceManager !== 'undefined') {
        VoiceManager.stop();
        ForestAudioEngine.duck(false);
      }
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      defOverlay.classList.remove('active');

      const word = defTitle.textContent;
      const def = wordDefinitions[word] || 'A scientific term.';
      startStage7MeaningTest(word, def);
    });
  }

  function startStage7MeaningTest(word, definition) {
    if (s7State.advanceTimer) {
      clearTimeout(s7State.advanceTimer);
      s7State.advanceTimer = null;
    }

    const sentences = segmentDefinition(definition);
    const validSentences = sentences.filter(s => pickBlankCandidate(s, word) !== null);

    if (validSentences.length === 0) {
      recordMasteredHuntWord(word);
      if (typeof sharedState !== 'undefined' && sharedState.recordWordMastery) {
        sharedState.recordWordMastery(word, true);
      }
      finishStage7WordTest();
      return;
    }

    s7State.word = word;
    s7State.sentences = validSentences;
    s7State.sentenceIndex = 0;
    s7State.firstTryClean = true;
    s7State.isAnswered = false;
    s7State.selectedOption = null;

    s7WordEl.textContent = word;
    s7Overlay.classList.add('active');
    renderStage7Sentence();
  }

  function renderStage7Sentence() {
    const { word, sentences, sentenceIndex } = s7State;
    if (sentenceIndex >= sentences.length) {
      finishStage7WordTest();
      return;
    }

    s7State.isAnswered = false;
    s7State.selectedOption = null;

    if (s7ProgressEl) s7ProgressEl.textContent = `Sentence ${sentenceIndex + 1} of ${sentences.length}`;
    updateScoreAndComboUI();

    if (s7StepDots) {
      s7StepDots.innerHTML = '';
      sentences.forEach((_, idx) => {
        const dot = document.createElement('span');
        dot.className = 's7-step-dot' + (idx < sentenceIndex ? ' done' : idx === sentenceIndex ? ' current' : '');
        s7StepDots.appendChild(dot);
      });
    }

    const sentence = sentences[sentenceIndex];
    const picked = pickBlankCandidate(sentence, word);
    if (!picked) {
      s7State.sentenceIndex++;
      renderStage7Sentence();
      return;
    }

    const expected = picked.chosen.word;
    let options = [];
    if (typeof window.DistractorEngine !== 'undefined') {
      options = window.DistractorEngine.getOptionsWithAnswer(expected, 4, {
        exclude: [word],
        preserveCase: false
      });
    } else {
      options = shuffleArray([expected, 'energy', 'system', 'matter'].slice(0, 4));
    }

    s7State.currentBlank = { expected, options };

    let cardHtml = '';
    picked.tokens.forEach((t, i) => {
      if (i === picked.chosen.index) {
        cardHtml += `<span class="s7-slot" id="hunt-s7-blank"><span class="slot-icon">🧩</span> <span class="slot-text">Select word</span></span>`;
      } else {
        cardHtml += esc(t);
      }
    });
    s7SentenceCard.innerHTML = cardHtml;

    s7OptionsGrid.innerHTML = '';
    options.forEach(opt => {
      const lower = String(opt).toLowerCase();
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 's7-option-btn';
      btn.textContent = lower;
      btn.addEventListener('click', () => onStage7OptionClick(lower, btn));
      s7OptionsGrid.appendChild(btn);
    });

    if (s7FeedbackEl) {
      s7FeedbackEl.textContent = '';
      s7FeedbackEl.className = 's7-feedback';
    }
    if (s7SkipBtn) {
      s7SkipBtn.style.display = '';
      s7SkipBtn.disabled = false;
    }
    if (s7NextBtn) s7NextBtn.style.display = 'none';
  }

  function onStage7OptionClick(opt, btnEl) {
    if (s7State.isAnswered) return;
    s7State.selectedOption = opt;

    const slot = document.getElementById('hunt-s7-blank');
    const expected = s7State.currentBlank.expected.toLowerCase();
    const isCorrect = opt === expected;
    const allBtns = s7OptionsGrid.querySelectorAll('.s7-option-btn');

    if (isCorrect) {
      s7State.isAnswered = true;
      flowStreak++;
      const earned = awardXP(25);
      if (typeof AudioManager !== 'undefined') AudioManager.play('success');
      ForestAtmosphere.pulse(1.2);

      if (slot) {
        slot.innerHTML = `<span class="slot-icon">✅</span> <span class="slot-text">${esc(opt)}</span>`;
        slot.classList.add('filled', 'correct');
      }

      allBtns.forEach(b => {
        if (b.textContent.trim().toLowerCase() === opt) b.classList.add('correct');
        else b.classList.add('dimmed');
      });

      if (s7FeedbackEl) {
        s7FeedbackEl.textContent = `Sharp deduction! +${earned} XP${getFlowMultiplier() > 1 ? ` (${getFlowMultiplier()}x Flow)` : ''}`;
        s7FeedbackEl.className = 's7-feedback ok';
      }
      if (s7SkipBtn) s7SkipBtn.style.display = 'none';

      // Record Spaced Repetition Mastery on completion of this word's sentences
      const isLastSentence = s7State.sentenceIndex >= s7State.sentences.length - 1;
      if (isLastSentence) {
        recordMasteredHuntWord(s7State.word);
        if (typeof sharedState !== 'undefined' && sharedState.recordWordMastery) {
          sharedState.recordWordMastery(s7State.word, s7State.firstTryClean);
        }
      }

      s7State.advanceTimer = setTimeout(() => {
        s7State.sentenceIndex++;
        renderStage7Sentence();
      }, 820);
    } else {
      s7State.firstTryClean = false;
      flowStreak = 0; // Gentle reset of Flow multiplier without taking points away!
      updateScoreAndComboUI();
      if (typeof AudioManager !== 'undefined') AudioManager.play('error');

      btnEl.classList.add('wrong-pick');
      btnEl.disabled = true;

      if (slot) {
        slot.innerHTML = `<span class="slot-icon">🧩</span> <span class="slot-text">Try again</span>`;
        slot.classList.add('wrong');
        setTimeout(() => {
          slot.classList.remove('wrong');
          if (!s7State.isAnswered) {
            slot.innerHTML = `<span class="slot-icon">🧩</span> <span class="slot-text">Select word</span>`;
          }
        }, 550);
      }

      if (s7FeedbackEl) {
        s7FeedbackEl.textContent = 'Not quite — check the context clue and pick another option.';
        s7FeedbackEl.className = 's7-feedback err';
      }
    }
  }

  if (s7SkipBtn) {
    s7SkipBtn.addEventListener('click', () => {
      if (s7State.isAnswered) return;
      s7State.isAnswered = true;
      s7State.firstTryClean = false;
      flowStreak = 0;
      updateScoreAndComboUI();

      const expected = s7State.currentBlank.expected.toLowerCase();
      const slot = document.getElementById('hunt-s7-blank');
      if (slot) {
        slot.innerHTML = `<span class="slot-icon">💡</span> <span class="slot-text">${esc(expected)}</span>`;
        slot.classList.add('filled', 'correct');
      }

      s7OptionsGrid.querySelectorAll('.s7-option-btn').forEach(b => {
        if (b.textContent.trim().toLowerCase() === expected) b.classList.add('correct');
        else b.classList.add('dimmed');
      });

      if (s7FeedbackEl) {
        s7FeedbackEl.textContent = 'Term revealed (+0 pts) — lock it into memory!';
        s7FeedbackEl.className = 's7-feedback err';
      }

      const isLast = s7State.sentenceIndex >= s7State.sentences.length - 1;
      if (isLast && typeof sharedState !== 'undefined' && sharedState.recordWordMastery) {
        sharedState.recordWordMastery(s7State.word, false);
      }

      s7SkipBtn.disabled = true;
      if (s7NextBtn) {
        s7NextBtn.textContent = isLast ? 'Finish Word ✓' : 'Next Sentence →';
        s7NextBtn.style.display = 'block';
      }
    });
  }

  if (s7NextBtn) {
    s7NextBtn.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      s7State.sentenceIndex++;
      renderStage7Sentence();
    });
  }

  function finishStage7WordTest() {
    s7Overlay.classList.remove('active');
    if (typeof confetti === 'function') {
      confetti({
        particleCount: 36,
        spread: 55,
        origin: { y: 0.65 },
        colors: ['#10b981', '#fbbf24', '#38bdf8', '#ffffff']
      });
    }
    if (foundWords.length >= targetWords.length && !roundWon) {
      handleWin();
    }
  }

  // ===================================================================
  // 11. ROUND WIN, HISTORY LOGGING & CELEBRATION
  // ===================================================================
  function handleWin() {
    if (roundWon) return;
    roundWon = true;

    setTimeout(() => {
      const timeDiff = stageStartTime ? Math.floor((Date.now() - stageStartTime) / 1000) : 0;
      const formattedTime = `${Math.floor(timeDiff / 60).toString().padStart(2, '0')}:${(timeDiff % 60).toString().padStart(2, '0')}`;

      // Difficulty completion bonus + No-Hint Clean Clear bonus
      let bonus = 100;
      if (currentLevelObj.key === 'easy') bonus = 50;
      if (currentLevelObj.key === 'intellect') bonus = 200;
      if (!usedHintThisRound) bonus += 50;

      awardXP(bonus);

      // Immediately increment persistent Hunt Streak upon board victory
      const prevStreak = parseInt(localStorage.getItem('osmosis_hunt_streak'), 10) || 0;
      localStorage.setItem('osmosis_hunt_streak', String(prevStreak + 1));

      // Log into Osmosis Archive History so Profile page displays Word Hunt sessions too
      try {
        const history = JSON.parse(localStorage.getItem('osmosis_history') || '[]');
        history.push({
          date: new Date().toLocaleDateString(),
          score: roundScore,
          words: foundWords.slice(),
          mode: 'word-hunt'
        });
        localStorage.setItem('osmosis_history', JSON.stringify(history));
      } catch (e) {}

      updateProgressionHeader();

      const wordsFoundEl = document.getElementById('result-words-found');
      const timeSpentEl = document.getElementById('result-time-spent');
      const totalScoreEl = document.getElementById('result-total-score');
      const winSubMsg = document.getElementById('win-sub-msg');
      const wordListHost = document.getElementById('result-words-list');

      if (wordsFoundEl) wordsFoundEl.textContent = `${foundWords.length}/${targetWords.length}`;
      if (timeSpentEl) timeSpentEl.textContent = formattedTime;
      if (totalScoreEl) totalScoreEl.textContent = roundScore;
      if (winSubMsg) {
        winSubMsg.textContent = !usedHintThisRound
          ? 'No-Hint Forest Mastery Bonus (+50 base XP) unlocked!'
          : 'Meanings & recall synced to your Mastery Archive.';
      }

      if (wordListHost) {
        wordListHost.innerHTML = '';
        foundWords.forEach(w => {
          const chip = document.createElement('span');
          chip.className = 'duo-word-chip';
          chip.textContent = w;
          wordListHost.appendChild(chip);
        });
      }

      if (promoStar) promoStar.classList.add('active');
      winOverlay.classList.add('active');

      if (typeof confetti === 'function') {
        confetti({ particleCount: 90, spread: 80, origin: { y: 0.6 }, colors: ['#10b981', '#fbbf24', '#38bdf8', '#ffffff'] });
      }
      if (typeof AudioManager !== 'undefined') {
        AudioManager.init();
        AudioManager.play('fanfare');
      }
    }, 550);
  }

  // ===================================================================
  // 12. NAVIGATION, MODALS, WIZARD & BOOTSTRAP
  // ===================================================================
  function goHome() {
    ForestAudioEngine.stop();
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');
    if (typeof window.navigateWithTransition === 'function') window.navigateWithTransition('01_home_menu.html');
    else window.location.href = '01_home_menu.html';
  }

  if (backBtn) backBtn.addEventListener('click', goHome);
  if (overlayHomeBtn) overlayHomeBtn.addEventListener('click', goHome);

  if (overlayContinueBtn) {
    overlayContinueBtn.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      winOverlay.classList.remove('active');
      initGame();
    });
  }

  if (musicToggleBtn) {
    musicToggleBtn.addEventListener('click', () => ForestAudioEngine.toggle());
  }

  if (bookBtn) {
    bookBtn.addEventListener('click', () => {
      ForestAudioEngine.startIfEnabled();
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      bookList.innerHTML = '';
      targetWords.forEach(word => {
        const item = document.createElement('div');
        item.className = 'book-item';
        const wordEl = document.createElement('div');
        wordEl.className = 'book-item-word';
        wordEl.textContent = word;
        const descEl = document.createElement('div');
        descEl.className = 'book-item-desc';
        const defText = wordDefinitions[word] || 'A scientific term.';
        if (typeof window.renderScienceText === 'function') {
          descEl.setAttribute('data-raw-content', defText);
          window.renderScienceText(descEl);
        } else {
          descEl.textContent = defText;
        }
        item.appendChild(wordEl);
        item.appendChild(descEl);
        bookList.appendChild(item);
      });
      bookOverlay.classList.add('active');
    });
  }

  if (bookContinueBtn) {
    bookContinueBtn.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      bookOverlay.classList.remove('active');
    });
  }

  const openLeagueModal = () => {
    ForestAudioEngine.startIfEnabled();
    if (typeof AudioManager !== 'undefined') AudioManager.play('gem');
    populateStatsModal();
    xpBreakdownOverlay.style.display = 'flex';
  };
  if (statsHeaderTrigger) statsHeaderTrigger.addEventListener('click', openLeagueModal);
  if (leagueBtn) leagueBtn.addEventListener('click', openLeagueModal);
  if (xpBreakdownClose) {
    xpBreakdownClose.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      xpBreakdownOverlay.style.display = 'none';
    });
  }

  function setDifficulty(level) {
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');
    currentLevelObj = DIFFICULTY_CONFIGS[level] || DIFFICULTY_CONFIGS.medium;
    localStorage.setItem('osmosis_hunt_diff', level);
    difficultyOverlay.style.display = 'none';
    initGame();
  }

  if (btnEasy) btnEasy.addEventListener('click', () => setDifficulty('easy'));
  if (btnMedium) btnMedium.addEventListener('click', () => setDifficulty('medium'));
  if (btnIntellect) btnIntellect.addEventListener('click', () => setDifficulty('intellect'));
  if (btnSettings) {
    btnSettings.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      btnCancelDiff.style.display = gameInProgress ? 'block' : 'none';
      difficultyOverlay.style.display = 'flex';
    });
  }
  if (btnCancelDiff) {
    btnCancelDiff.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      difficultyOverlay.style.display = 'none';
    });
  }

  // Guiding Wizard
  let wizardCurrentStep = 1;
  function updateWizardUI() {
    wizardSteps.forEach(step => {
      step.style.display = (parseInt(step.dataset.step, 10) === wizardCurrentStep) ? 'block' : 'none';
    });
    wizardDots.forEach((dot, idx) => {
      dot.classList.toggle('active', idx + 1 === wizardCurrentStep);
    });
    if (wizardBackBtn) wizardBackBtn.style.display = wizardCurrentStep === 1 ? 'none' : 'block';
    if (wizardNextBtn) wizardNextBtn.textContent = wizardCurrentStep === 3 ? 'Start Hunting →' : 'Next';
  }

  if (wizardNextBtn && wizardBackBtn) {
    wizardNextBtn.addEventListener('click', () => {
      ForestAudioEngine.startIfEnabled();
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      if (wizardCurrentStep < 3) {
        wizardCurrentStep++;
        updateWizardUI();
      } else {
        localStorage.setItem('wordHuntWizardShown', 'true');
        if (wizardOverlay) wizardOverlay.style.display = 'none';
        const savedDiff = localStorage.getItem('osmosis_hunt_diff');
        if (savedDiff && DIFFICULTY_CONFIGS[savedDiff]) {
          currentLevelObj = DIFFICULTY_CONFIGS[savedDiff];
          difficultyOverlay.style.display = 'none';
          initGame();
        } else {
          difficultyOverlay.style.display = 'flex';
        }
      }
    });

    wizardBackBtn.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      if (wizardCurrentStep > 1) {
        wizardCurrentStep--;
        updateWizardUI();
      }
    });
  }

  if (helpBtn) {
    helpBtn.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      wizardCurrentStep = 1;
      updateWizardUI();
      if (wizardOverlay) wizardOverlay.style.display = 'flex';
    });
  }

  // Bootstrap Entry
  ForestAtmosphere.start();
  updateProgressionHeader();

  const savedDiffPref = localStorage.getItem('osmosis_hunt_diff');
  if (savedDiffPref && DIFFICULTY_CONFIGS[savedDiffPref]) {
    currentLevelObj = DIFFICULTY_CONFIGS[savedDiffPref];
  }

  if (!localStorage.getItem('wordHuntWizardShown')) {
    if (wizardOverlay) wizardOverlay.style.display = 'flex';
    if (difficultyOverlay) difficultyOverlay.style.display = 'none';
    updateWizardUI();
  } else if (savedDiffPref && DIFFICULTY_CONFIGS[savedDiffPref]) {
    if (difficultyOverlay) difficultyOverlay.style.display = 'none';
    initGame();
  } else {
    if (difficultyOverlay) difficultyOverlay.style.display = 'flex';
  }

  if (window.location.search.includes('celebration=true')) {
    if (typeof confetti === 'function') {
      confetti({ particleCount: 95, spread: 80, origin: { y: 0.6 }, colors: ['#10b981', '#fbbf24', '#38bdf8', '#ffffff'] });
    }
    if (typeof AudioManager !== 'undefined') {
      AudioManager.init();
      AudioManager.play('fanfare');
    }
  }
});
