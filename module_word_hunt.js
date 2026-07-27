// =====================================================================
// FILE: module_word_hunt.js (The Mini-Game)
// =====================================================================

document.addEventListener('DOMContentLoaded', () => {
  const textLayer = document.getElementById('text-layer');
  const highlightsLayer = document.getElementById('highlights-layer');
  const wordsEl = document.getElementById('hunt-words');
  const scoreEl = document.getElementById('hunt-score');
  const backBtn = document.getElementById('back-home-btn');
  const bookBtn = document.getElementById('book-btn');
  const lvlBadge = document.getElementById('hunt-lvl-badge');

  // Overlay Elements
  const winOverlay = document.getElementById('win-overlay');
  const promoStar = document.getElementById('promotion-star');
  const levelText = document.getElementById('level-text');
  // Note: win-message, xp-fluid, xp-text are no longer in the HTML (replaced by results card)
  const overlayHomeBtn = document.getElementById('overlay-home-btn');
  const overlayContinueBtn = document.getElementById('overlay-continue-btn');

  // Definition Popup Elements
  const defOverlay = document.getElementById('def-popup-overlay');
  const defTitle = document.getElementById('def-popup-title');
  const defDesc = document.getElementById('def-popup-desc');
  const defContinueBtn = document.getElementById('def-popup-continue');

  // Dropdown Test Popup Elements
  const huntDropdownOverlay = document.getElementById('hunt-dropdown-overlay');
  const huntDropdownTitle = document.getElementById('hunt-dropdown-title');
  const huntDropdownMeaning = document.getElementById('hunt-dropdown-meaning');
  const huntDropdownFeedback = document.getElementById('hunt-dropdown-feedback');
  const huntDropdownSubmit = document.getElementById('hunt-dropdown-submit');
  const huntDropdownSkip = document.getElementById('hunt-dropdown-skip');

  // Success Banner Elements
  const successBanner = document.getElementById('success-banner-overlay');
  const successThanksBtn = document.getElementById('success-banner-thanks');

  // Book Popup Elements
  const bookOverlay = document.getElementById('book-popup-overlay');
  const bookList = document.getElementById('book-definitions-list');
  const bookContinueBtn = document.getElementById('book-popup-continue');

  // Difficulty Selection Elements
  const difficultyOverlay = document.getElementById('difficulty-overlay');
  const btnEasy = document.getElementById('diff-easy');
  const btnMedium = document.getElementById('diff-medium');
  const btnIntellect = document.getElementById('diff-intellect');
  const btnSettings = document.getElementById('settings-btn');
  const btnCancelDiff = document.getElementById('diff-cancel-btn');

  // Progression Data (Difficulty configs)
  const DIFFICULTY_CONFIGS = {
    easy: { lvl: 'Easy', words: 3, maxLen: 5, grid: 6, dirs: [[0, 1], [1, 0]] },
    medium: { lvl: 'Medium', words: 5, maxLen: 7, grid: 8, dirs: [[0, 1], [1, 0], [1, 1]] },
    intellect: { lvl: 'Intellect', words: 7, maxLen: 10, grid: 10, dirs: [[0, 1], [1, 0], [1, 1], [-1, 1], [0, -1], [-1, 0], [-1, -1], [1, -1]] }
  };

  let currentLevelObj = DIFFICULTY_CONFIGS.medium;
  let gridSize = 8;
  let numWords = 5;

  let grid = [];
  let targetWords = [];
  let foundWords = [];
  let wordCoordinates = {}; // Stores {start, end} for hints
  let wordDefinitions = {}; // Stores {word: definition}
  let currentScore = 0;
  let stageStartTime = null;
  let occupiedCells = new Set();

  let isSelecting = false;
  let startCell = null;
  let lastValidEndCell = null;
  let selectionPill = null;
  let gameInProgress = false;

  const pillColors = ["#818cf8", "#34d399", "#f472b6", "#fb7185", "#38bdf8", "#fbbf24", "#a78bfa"];
  let colorIndex = 0;

  // Visual FX Canvas Engine
  const fxCanvas = document.getElementById('fx-canvas');
  const fxCtx = fxCanvas ? fxCanvas.getContext('2d') : null;
  let particles = [];

  function resizeFxCanvas() {
    if (!fxCanvas || !textLayer) return;
    fxCanvas.width = textLayer.clientWidth;
    fxCanvas.height = textLayer.clientHeight;
  }
  window.addEventListener('resize', resizeFxCanvas);
  setTimeout(resizeFxCanvas, 100);

  function triggerParticleExplosion(start, end) {
    if (!fxCtx || !textLayer) return;
    resizeFxCanvas();

    const cw = textLayer.clientWidth / gridSize;
    const ch = textLayer.clientHeight / gridSize;

    const startX = (start.c + 0.5) * cw;
    const startY = (start.r + 0.5) * ch;
    const endX = (end.c + 0.5) * cw;
    const endY = (end.r + 0.5) * ch;

    const colors = ["#38bdf8", "#818cf8", "#34d399", "#fb7185", "#fbbf24"];

    // Spawn 40 vivid physics particles along the word vector
    for (let i = 0; i < 40; i++) {
      const t = Math.random();
      const px = startX + (endX - startX) * t;
      const py = startY + (endY - startY) * t;

      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 6 + 2;

      particles.push({
        x: px,
        y: py,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        radius: Math.random() * 5 + 3,
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: 1,
        life: 1
      });
    }

    if (!window.particleAnimLoopRunning) {
      window.particleAnimLoopRunning = true;
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
      p.vy += 0.15; // Gravity pull
      p.life -= 0.025;
      p.alpha = Math.max(0, p.life);

      fxCtx.save();
      fxCtx.globalAlpha = p.alpha;
      fxCtx.fillStyle = p.color;
      fxCtx.beginPath();
      fxCtx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      fxCtx.fill();
      fxCtx.restore();

      if (p.life <= 0) particles.splice(i, 1);
    }

    if (particles.length > 0) {
      requestAnimationFrame(runParticleLoop);
    } else {
      window.particleAnimLoopRunning = false;
    }
  }

  function triggerFloatingXPBadge(endCell) {
    if (!textLayer) return;
    const cw = textLayer.clientWidth / gridSize;
    const ch = textLayer.clientHeight / gridSize;

    const posX = (endCell.c + 0.5) * cw;
    const posY = (endCell.r + 0.5) * ch;

    const badge = document.createElement('div');
    badge.className = 'xp-float-badge';
    badge.textContent = '+100 XP!';
    badge.style.left = `${posX - 40}px`;
    badge.style.top = `${posY - 20}px`;

    const wrapper = document.getElementById('grid-wrapper');
    if (wrapper) wrapper.appendChild(badge);

    setTimeout(() => badge.remove(), 1000);
  }

  // Event Listeners for Difficulty
  btnEasy.addEventListener('click', () => setDifficulty('easy'));
  btnMedium.addEventListener('click', () => setDifficulty('medium'));
  btnIntellect.addEventListener('click', () => setDifficulty('intellect'));

  // // 3D Parallax Card Tilt Effect on Mouse Movement . commented becaus it was affecting ios browser
  // const notebookCard = document.querySelector('.notebook');
  // if (notebookCard) {
  //   document.addEventListener('mousemove', (e) => {
  //     const cx = window.innerWidth / 2;
  //     const cy = window.innerHeight / 2;
  //     const dx = (e.clientX - cx) / cx;
  //     const dy = (e.clientY - cy) / cy;

  //     const tiltX = (dy * -8).toFixed(2);
  //     const tiltY = (dx * 8).toFixed(2);

  //     notebookCard.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
  //     notebookCard.style.transition = 'transform 0.1s ease-out';
  //   });

  //   document.addEventListener('mouseleave', () => {
  //     notebookCard.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
  //     notebookCard.style.transition = 'transform 0.5s ease';
  //   });
  // }

  btnSettings.addEventListener('click', () => {
    btnCancelDiff.style.display = gameInProgress ? 'inline-block' : 'none';
    difficultyOverlay.style.display = 'flex';
  });

  btnCancelDiff.addEventListener('click', () => {
    difficultyOverlay.style.display = 'none';
  });

  const statsHeaderTrigger = document.getElementById('stats-header-trigger');
  const leagueBtn = document.getElementById('league-btn');
  const xpBreakdownOverlay = document.getElementById('xp-breakdown-overlay');
  const xpBreakdownClose = document.getElementById('xp-breakdown-close');

  const openLeagueModal = () => {
    if (typeof AudioManager !== 'undefined') {
      AudioManager.init();
      AudioManager.play('gem');
    }
    populateStatsModal();
    xpBreakdownOverlay.style.display = 'flex';
  };

  if (statsHeaderTrigger && xpBreakdownOverlay) {
    statsHeaderTrigger.addEventListener('click', openLeagueModal);
  }

  if (leagueBtn && xpBreakdownOverlay) {
    leagueBtn.addEventListener('click', openLeagueModal);
  }

  if (xpBreakdownClose && xpBreakdownOverlay) {
    xpBreakdownClose.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      xpBreakdownOverlay.style.display = 'none';
    });
  }

  function populateStatsModal() {
    const streak = parseInt(localStorage.getItem('osmosis_hunt_streak')) || 0;
    const totalXP = parseInt(localStorage.getItem('osmosis_total_score')) || 0;
    const gems = Math.floor(totalXP / 100);

    const level = Math.floor(totalXP / 500) + 1;
    const leagues = ["Bronze League", "Silver League", "Gold League", "Sapphire League", "Ruby League", "Diamond League"];
    const leagueRank = leagues[Math.min(leagues.length - 1, Math.floor((level - 1) / 2))];

    const rankEl = document.getElementById('modal-league-rank');
    const streakEl = document.getElementById('breakdown-streak');
    const xpEl = document.getElementById('breakdown-xp');
    const gemsEl = document.getElementById('breakdown-gems');

    if (rankEl) rankEl.textContent = leagueRank;
    if (streakEl) streakEl.textContent = `${streak} Sessions`;
    if (xpEl) xpEl.textContent = `${totalXP} XP`;
    if (gemsEl) gemsEl.textContent = `${gems} Gems`;
  }

  function updateProgressionHeader() {
    const streak = parseInt(localStorage.getItem('osmosis_hunt_streak')) || 0;
    const totalXP = parseInt(localStorage.getItem('osmosis_total_score')) || 0;
    const gems = Math.floor(totalXP / 100);

    // Calculate level progression (Every level requires 500 XP)
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

  function setDifficulty(level) {
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');
    currentLevelObj = DIFFICULTY_CONFIGS[level];
    localStorage.setItem('osmosis_hunt_diff', level);
    difficultyOverlay.style.display = 'none';
    initGame();
  }

  function initGame() {
    gameInProgress = true;
    stageStartTime = Date.now();
    if (typeof initModal === 'function') initModal();

    // Set parameters based on chosen difficulty
    gridSize = currentLevelObj.grid;
    numWords = currentLevelObj.words;

    // Update UI for level with persistent streak progress
    const streak = parseInt(localStorage.getItem('osmosis_hunt_streak')) || 0;
    textLayer.style.setProperty('--grid-size', gridSize);
    lvlBadge.textContent = `${currentLevelObj.lvl} (Streak: ${streak})`;

    updateProgressionHeader();

    // Reset game vars
    foundWords = [];
    wordCoordinates = {};
    wordDefinitions = {};
    isSelecting = false;
    startCell = null;
    lastValidEndCell = null;
    selectionPill = null;
    highlightsLayer.innerHTML = '';
    winOverlay.classList.remove('active');
    promoStar.classList.remove('active');

    // Use the curated Hunt Dictionary (200 STEM words, short definitions, grid-friendly)
    let allWords = [];
    if (typeof window.HuntDictionary !== 'undefined') {
      allWords = window.HuntDictionary.getWordsByMaxLength(currentLevelObj.maxLen);
    } else if (typeof window.STEMDictionary !== 'undefined') {
      // Fallback to main dictionary if hunt dictionary not loaded
      const bank = window.STEMDictionary.wordBank || {};
      Object.keys(bank).forEach(l => {
        allWords.push(...window.STEMDictionary.getWordsByLetter(l));
      });
    }

    if (allWords.length === 0) {
      // Last-resort fallback
      allWords = [
        { word: "ATOM", definition: "Smallest unit of matter that retains element properties." },
        { word: "CELL", definition: "The basic structural unit of all living organisms." },
        { word: "GENE", definition: "A segment of DNA that codes for a specific trait." },
        { word: "WAVE", definition: "A disturbance that transfers energy from place to place." },
        { word: "ACID", definition: "A substance with a pH below 7 that releases H+ ions." }
      ];
    }

    let uniqueMap = new Map();
    allWords.forEach(w => {
      const clean = (w.word || '').toUpperCase().replace(/[^A-Z]/g, '');
      if (clean.length >= 3 && clean.length <= currentLevelObj.maxLen) {
        if (!uniqueMap.has(clean)) {
          uniqueMap.set(clean, { word: clean, definition: w.definition || "A scientific term." });
        }
      }
    });
    let validWords = Array.from(uniqueMap.values());

    let usedWords = JSON.parse(localStorage.getItem('wordHuntUsedWords')) || [];
    let availableWords = validWords.filter(w => !usedWords.includes(w.word));

    if (availableWords.length < numWords) {
      usedWords = [];
      availableWords = validWords;
    }

    // Proper Fisher-Yates shuffle
    for (let i = availableWords.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [availableWords[i], availableWords[j]] = [availableWords[j], availableWords[i]];
    }

    const pickedObjs = availableWords.slice(0, numWords);
    targetWords = pickedObjs.map(obj => obj.word);

    pickedObjs.forEach(obj => {
      wordDefinitions[obj.word] = obj.definition;
    });

    usedWords.push(...targetWords);
    localStorage.setItem('wordHuntUsedWords', JSON.stringify(usedWords));

    generateGrid();
    renderGrid();
    renderWords();
    scoreEl.textContent = `${currentScore} pts`;
  }

  function generateGrid() {
    grid = Array(gridSize).fill(null).map(() => Array(gridSize).fill(''));
    occupiedCells.clear();
    // Use directions restricted by current difficulty level
    const dirs = currentLevelObj.dirs;
    wordCoordinates = {};
    let successfullyPlaced = [];

    targetWords.forEach(word => {
      let placed = false;
      let attempts = 0;
      while (!placed && attempts < 200) {
        attempts++;
        const d = dirs[Math.floor(Math.random() * dirs.length)];
        const r = Math.floor(Math.random() * gridSize);
        const c = Math.floor(Math.random() * gridSize);

        if (canPlace(word, r, c, d[0], d[1])) {
          placeWord(word, r, c, d[0], d[1]);
          // Save coordinates for the Magic Hint system
          wordCoordinates[word] = {
            start: { r, c },
            end: { r: r + (word.length - 1) * d[0], c: c + (word.length - 1) * d[1] }
          };
          placed = true;
          successfullyPlaced.push(word);
        }
      }
    });

    targetWords = successfullyPlaced; // Drop any words that couldn't fit

    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (let i = 0; i < gridSize; i++) {
      for (let j = 0; j < gridSize; j++) {
        if (grid[i][j] === '') {
          grid[i][j] = letters.charAt(Math.floor(Math.random() * letters.length));
        }
      }
    }

    removeAccidentalWords();
  }

  function canPlace(word, r, c, dr, dc) {
    for (let i = 0; i < word.length; i++) {
      const nr = r + i * dr;
      const nc = c + i * dc;
      if (nr < 0 || nr >= gridSize || nc < 0 || nc >= gridSize) return false;
      if (grid[nr][nc] !== '' && grid[nr][nc] !== word[i]) return false;
    }
    return true;
  }

  function placeWord(word, r, c, dr, dc) {
    for (let i = 0; i < word.length; i++) {
      const nr = r + i * dr;
      const nc = c + i * dc;
      grid[nr][nc] = word[i];
      occupiedCells.add(`${nr},${nc}`);
    }
  }

  function removeAccidentalWords() {
    const dirs = [[0, 1], [1, 0], [1, 1], [-1, 1], [0, -1], [-1, 0], [-1, -1], [1, -1]];
    let foundAccidental = true;
    let iterations = 0;

    while (foundAccidental && iterations < 100) {
      foundAccidental = false;
      iterations++;

      for (let word of targetWords) {
        const len = word.length;
        const coord = wordCoordinates[word];
        if (!coord) continue;

        for (let r = 0; r < gridSize; r++) {
          for (let c = 0; c < gridSize; c++) {
            for (let [dr, dc] of dirs) {
              const endR = r + (len - 1) * dr;
              const endC = c + (len - 1) * dc;
              if (endR < 0 || endR >= gridSize || endC < 0 || endC >= gridSize) continue;

              let match = true;
              for (let i = 0; i < len; i++) {
                if (grid[r + i * dr][c + i * dc] !== word[i]) {
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
                  let changed = false;
                  for (let i = 0; i < len; i++) {
                    const mr = r + i * dr;
                    const mc = c + i * dc;
                    if (!occupiedCells.has(`${mr},${mc}`)) {
                      let newLetter;
                      do {
                        newLetter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".charAt(Math.floor(Math.random() * 26));
                      } while (newLetter === grid[mr][mc]);
                      grid[mr][mc] = newLetter;
                      changed = true;
                      foundAccidental = true;
                      break;
                    }
                  }

                  if (!changed) {
                    // Overlap is entirely on occupied cells, which is extremely rare.
                    // We change one letter anyway to break the accidental word.
                    const randomIdx = Math.floor(Math.random() * len);
                    const mr = r + randomIdx * dr;
                    const mc = c + randomIdx * dc;
                    let newLetter;
                    do {
                      newLetter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".charAt(Math.floor(Math.random() * 26));
                    } while (newLetter === grid[mr][mc]);
                    grid[mr][mc] = newLetter;
                    foundAccidental = true;
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
        cell.textContent = grid[r][c];
        textLayer.appendChild(cell);
      }
    }

    textLayer.addEventListener('mousedown', handlePointerDown);
    document.addEventListener('mousemove', handlePointerMove);
    document.addEventListener('mouseup', handlePointerUp);

    textLayer.addEventListener('touchstart', handlePointerDown, { passive: false });
    document.addEventListener('touchmove', handlePointerMove, { passive: false });
    document.addEventListener('touchend', handlePointerUp);
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

  // --- Book Button (View All Definitions) ---
  bookBtn.addEventListener('click', () => {
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
      descEl.textContent = wordDefinitions[word] || 'A scientific term.';
      item.appendChild(wordEl);
      item.appendChild(descEl);
      bookList.appendChild(item);
    });
    bookOverlay.classList.add('active');
  });

  if (bookContinueBtn) {
    bookContinueBtn.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      bookOverlay.classList.remove('active');
    });
  }

  // --- Interaction Logic ---

  function getCellFromEvent(e) {
    let clientX, clientY;
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

    const cw = rect.width / gridSize;
    const ch = rect.height / gridSize;

    const c = Math.floor(x / cw);
    const r = Math.floor(y / ch);

    if (r >= 0 && r < gridSize && c >= 0 && c < gridSize) {
      return { r, c };
    }
    return null;
  }

  const pianoScale = [
    261.63, // C4 (Do)
    293.66, // D4 (Re)
    329.63, // E4 (Mi)
    349.23, // F4 (Fa)
    392.00, // G4 (Sol)
    440.00, // A4 (La)
    493.88, // B4 (Ti)
    523.25, // C5 (Do)
    587.33, // D5 (Re)
    659.25, // E5 (Mi)
    698.46, // F5 (Fa)
    783.99  // G5 (Sol)
  ];

  // We keep a registry of active audio nodes to play harmonized chord layers
  let activeHarmonies = [];

  function playDragNote(steps) {
    if (typeof AudioManager === 'undefined') return;
    AudioManager.init();
    const ctx = AudioManager.ctx;
    if (!ctx) return;
    if (ctx.state === 'suspended') ctx.resume();

    // Clean up old active notes to prevent frequency clutter
    activeHarmonies.forEach(node => {
      try { node.osc.stop(); } catch (e) { }
    });
    activeHarmonies = [];

    // Scale index bounded to range
    const rootIndex = Math.min(steps, pianoScale.length - 1);
    const rootFreq = pianoScale[rootIndex];

    // Define helper to create a warm synthesized piano voice
    const playHarmonicVoice = (frequency, volume, delay = 0, type = 'sine') => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const filter = ctx.createBiquadFilter();

      osc.type = type;
      osc.frequency.setValueAtTime(frequency, ctx.currentTime);

      // Lowpass filter simulates the warm damper resonance of a piano string
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(2000, ctx.currentTime);
      filter.frequency.exponentialRampToValueAtTime(100, ctx.currentTime + 0.4);

      const now = ctx.currentTime;
      gain.gain.setValueAtTime(0, now);
      gain.gain.linearRampToValueAtTime(volume, now + 0.03 + delay);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5 + delay); // decay

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);

      osc.start(now);
      osc.stop(now + 0.6);

      activeHarmonies.push({ osc, gain });
    };

    // Play a beautiful chord progression harmony based on step length
    // Ratios: Root (1.0), Major Third (1.25) or Minor Third (1.2), Perfect Fifth (1.5), Octave (2.0)
    const isEven = (steps % 2 === 0);
    const thirdRatio = isEven ? 1.25 : 1.20; // Alternates between major/minor steps for organic coloring
    const fifthRatio = 1.50;
    const octaveRatio = 2.00;

    // 1. Root Note (deep warm resonance)
    playHarmonicVoice(rootFreq, 0.20, 0, 'sine');

    // 2. Harmonic Third (adds emotional coloring)
    playHarmonicVoice(rootFreq * thirdRatio, 0.12, 0.02, 'sine');

    // 3. Harmonic Fifth (provides stability)
    playHarmonicVoice(rootFreq * fifthRatio, 0.10, 0.04, 'sine');

    // 4. Sparkling Octave (adds bell-like high clarity)
    if (steps > 2) {
      playHarmonicVoice(rootFreq * octaveRatio, 0.08, 0.06, 'triangle');
    }
  }

  // Helper to animate matrix cells selected in the path
  function highlightMatrixCellsInSelection() {
    if (!startCell || !lastValidEndCell) return;
    const cells = textLayer.querySelectorAll('.hunt-cell');

    // Reset all cells from temporary scale/glow effects
    cells.forEach(c => {
      c.style.transform = '';
      c.style.textShadow = '';
      c.style.color = '#0f172a';
    });

    const dr = lastValidEndCell.r - startCell.r;
    const dc = lastValidEndCell.c - startCell.c;
    const steps = Math.max(Math.abs(dr), Math.abs(dc));

    const stepR = steps === 0 ? 0 : dr / steps;
    const stepC = steps === 0 ? 0 : dc / steps;

    for (let i = 0; i <= steps; i++) {
      const r = Math.round(startCell.r + (stepR * i));
      const c = Math.round(startCell.c + (stepC * i));
      const idx = r * gridSize + c;
      const cellNode = cells[idx];
      if (cellNode) {
        // Dynamic scale expansion & color shift to reflect live selection
        cellNode.style.transform = 'scale(1.25)';
        cellNode.style.color = '#4f46e5';
        cellNode.style.textShadow = '0 0 12px rgba(79, 70, 229, 0.8)';
        cellNode.style.transition = 'transform 0.1s cubic-bezier(0.175, 0.885, 0.32, 1.275), color 0.1s';
      }
    }
  }

  function handlePointerDown(e) {
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

    const color = pillColors[colorIndex % pillColors.length];
    updatePillTransform(selectionPill, startCell, startCell, color);

    playDragNote(0);
    highlightMatrixCellsInSelection();
  }

  function handlePointerMove(e) {
    if (!isSelecting) return;
    if (e.type === 'touchmove') e.preventDefault();

    const cellPos = getCellFromEvent(e);
    if (!cellPos) return;

    // Check if it forms a valid straight line
    const dr = cellPos.r - startCell.r;
    const dc = cellPos.c - startCell.c;

    if (dr === 0 || dc === 0 || Math.abs(dr) === Math.abs(dc)) {
      if (lastValidEndCell.r !== cellPos.r || lastValidEndCell.c !== cellPos.c) {
        lastValidEndCell = cellPos;
        const color = pillColors[colorIndex % pillColors.length];
        updatePillTransform(selectionPill, startCell, lastValidEndCell, color);

        const steps = Math.max(Math.abs(dr), Math.abs(dc));
        playDragNote(steps);
        highlightMatrixCellsInSelection();
      }
    }
  }

  function handlePointerUp(e) {
    if (!isSelecting) return;
    isSelecting = false;

    // Reset temporary styles on all cells from the dynamic highlighting
    const cells = textLayer.querySelectorAll('.hunt-cell');
    cells.forEach(c => {
      c.style.transform = '';
      c.style.textShadow = '';
      c.style.color = '#0f172a';
    });

    // Evaluate selection
    const dr = lastValidEndCell.r - startCell.r;
    const dc = lastValidEndCell.c - startCell.c;
    const steps = Math.max(Math.abs(dr), Math.abs(dc));

    let wordStr = '';
    const stepR = steps === 0 ? 0 : dr / steps;
    const stepC = steps === 0 ? 0 : dc / steps;

    for (let i = 0; i <= steps; i++) {
      const r = startCell.r + (stepR * i);
      const c = startCell.c + (stepC * i);
      wordStr += grid[r][c];
    }

    const wordStrReverse = wordStr.split('').reverse().join('');
    const match = targetWords.find(w => w === wordStr || w === wordStrReverse);

    if (match && !foundWords.includes(match)) {
      // Correct!
      if (typeof AudioManager !== 'undefined') AudioManager.play('success');
      foundWords.push(match);

      // 1. Trigger Screen Impact Shake
      const notebookEl = document.querySelector('.notebook');
      if (notebookEl) {
        notebookEl.classList.remove('impact-shake');
        void notebookEl.offsetWidth; // Force DOM reflow
        notebookEl.classList.add('impact-shake');
      }

      // 2. Trigger Canvas Particle Explosion along the word path
      triggerParticleExplosion(startCell, lastValidEndCell);

      // 3. Trigger Floating "+100 XP" Badge Animation
      triggerFloatingXPBadge(lastValidEndCell);

      const chip = document.getElementById('word-' + match);
      if (chip) chip.classList.add('found');

      currentScore += 100;
      scoreEl.textContent = `${currentScore} pts`;

      showDefinitionPopup(match);

      // Keep pill
      colorIndex++;
      selectionPill = null;
    } else {
      // Wrong selection
      if (typeof AudioManager !== 'undefined' && steps > 0) AudioManager.play('error');
      if (selectionPill) {
        selectionPill.remove();
        selectionPill = null;
      }
    }

    startCell = null;
    lastValidEndCell = null;
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

    const centerX = (x1 + x2) / 2;
    const centerY = (y1 + y2) / 2;

    const pillThickness = Math.min(cw, ch) * 0.8;

    pill.style.width = `${distance + pillThickness}px`;
    pill.style.height = `${pillThickness}px`;
    pill.style.backgroundColor = color;
    pill.style.left = `${centerX}px`;
    pill.style.top = `${centerY}px`;
    pill.style.transform = `translate(-50%, -50%) rotate(${angle}deg)`;
  }

  function showDefinitionPopup(word) {
    defTitle.textContent = word;
    defDesc.textContent = wordDefinitions[word] || "A scientific term.";
    defOverlay.classList.add('active');
  }

  if (defContinueBtn) {
    defContinueBtn.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      defOverlay.classList.remove('active');

      // Start the definition test
      const currentWord = defTitle.textContent;
      const currentDef = wordDefinitions[currentWord] || "A scientific term.";
      startDropdownTest(currentWord, currentDef);
    });
  }

  let activeDropdownTestAnswers = [];

  function startDropdownTest(word, definition) {
    huntDropdownTitle.textContent = word;
    huntDropdownFeedback.textContent = '';
    huntDropdownFeedback.className = 'feedback';
    huntDropdownSubmit.textContent = 'Submit';
    huntDropdownSubmit.disabled = false;
    huntDropdownSkip.style.display = 'block';

    const stopWords = ['a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 'on', 'at', 'to', 'from', 'by', 'of', 'in', 'is', 'are', 'was', 'were', 'it', 'that', 'this', 'with'];

    // simple tokenization keeping punctuation separate
    const tokens = definition.match(/([a-zA-Z]+|[^a-zA-Z]+)/g) || [];

    // find valid words to blank
    let validIndices = [];
    tokens.forEach((t, i) => {
      if (/^[a-zA-Z]+$/.test(t) && t.length > 3 && !stopWords.includes(t.toLowerCase())) {
        validIndices.push(i);
      }
    });

    // pick 1 to 2 blanks
    let numBlanks = Math.min(validIndices.length, Math.floor(Math.random() * 2) + 1);
    // shuffle validIndices
    for (let i = validIndices.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [validIndices[i], validIndices[j]] = [validIndices[j], validIndices[i]];
    }

    let chosenIndices = validIndices.slice(0, numBlanks);
    activeDropdownTestAnswers = [];

    let html = '';
    let blankCounter = 0;

    tokens.forEach((t, i) => {
      if (chosenIndices.includes(i)) {
        let correctWord = t;
        let trickWords = getRandomTrickWords(correctWord, 3);
        let options = [correctWord, ...trickWords];
        // shuffle options
        for (let k = options.length - 1; k > 0; k--) {
          const j = Math.floor(Math.random() * (k + 1));
          [options[k], options[j]] = [options[j], options[k]];
        }

        let id = `hunt-blank-${blankCounter}`;
        activeDropdownTestAnswers.push({ id, correct: correctWord });

        let optionsHtml = options.map(opt => `<div class="custom-option" data-val="${opt}">${opt}</div>`).join('');

        html += `
              <div class="custom-dropdown-container" id="${id}">
                <div class="custom-dropdown-btn" onclick="toggleDropdown(this)">
                  <span class="btn-text">Select</span>
                  <span class="dropdown-arrow">▼</span>
                </div>
                <div class="custom-dropdown-menu">
                  ${optionsHtml}
                </div>
              </div>
            `;
        blankCounter++;
      } else {
        html += t;
      }
    });

    if (blankCounter === 0) {
      // Fallback if no valid blanks found (e.g. very short definition)
      huntDropdownMeaning.innerHTML = definition;
    } else {
      huntDropdownMeaning.innerHTML = html;

      // Add option click listeners
      const optionElements = huntDropdownMeaning.querySelectorAll('.custom-option');
      optionElements.forEach(opt => {
        opt.addEventListener('click', (e) => {
          const container = opt.closest('.custom-dropdown-container');
          const btn = container.querySelector('.custom-dropdown-btn');
          const btnText = btn.querySelector('.btn-text');
          btnText.textContent = opt.dataset.val;
          btn.dataset.selected = opt.dataset.val;
          btn.classList.add('filled');
          container.classList.remove('open');
          if (typeof AudioManager !== 'undefined') AudioManager.play('click');
          e.stopPropagation();
        });
      });
    }

    huntDropdownOverlay.classList.add('active');
  }

  // Make toggleDropdown global for onclick attribute
  window.toggleDropdown = function (btn) {
    const container = btn.closest('.custom-dropdown-container');
    // close others
    document.querySelectorAll('.custom-dropdown-container.open').forEach(c => {
      if (c !== container) c.classList.remove('open');
    });
    container.classList.toggle('open');
  };

  // close dropdowns when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.custom-dropdown-container')) {
      document.querySelectorAll('.custom-dropdown-container.open').forEach(c => {
        c.classList.remove('open');
      });
    }
  });

  huntDropdownSubmit.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (huntDropdownSubmit.disabled) return;
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');

    // Close any open dropdown menus so they can't sit on top of the button
    document.querySelectorAll('.custom-dropdown-container.open').forEach(c => {
      c.classList.remove('open');
    });

    if (activeDropdownTestAnswers.length === 0) {
      closeTestAndCheckWin();
      return;
    }

    let allCorrect = true;
    let hasEmpty = false;

    activeDropdownTestAnswers.forEach(ans => {
      const container = document.getElementById(ans.id);
      if (!container) {
        allCorrect = false;
        return;
      }
      const btn = container.querySelector('.custom-dropdown-btn');
      if (!btn) {
        allCorrect = false;
        return;
      }
      const selected = (btn.dataset.selected || '').trim();

      btn.classList.remove('wrong', 'correct');

      if (!selected) {
        hasEmpty = true;
        allCorrect = false;
        btn.classList.add('wrong');
        setTimeout(() => {
          if (btn.classList.contains('wrong') && !(btn.dataset.selected || '').trim()) {
            btn.classList.remove('wrong');
          }
        }, 400);
        return;
      }

      if (selected.toLowerCase() === String(ans.correct).toLowerCase()) {
        btn.classList.add('correct');
      } else {
        btn.classList.add('wrong');
        allCorrect = false;
        setTimeout(() => {
          if (btn.classList.contains('wrong')) btn.classList.remove('wrong');
        }, 400);
      }
    });

    if (hasEmpty) {
      if (typeof AudioManager !== 'undefined') AudioManager.play('error');
      huntDropdownFeedback.textContent = 'Please select a word for every blank.';
      huntDropdownFeedback.className = 'feedback error';
      return;
    }

    if (allCorrect) {
      if (typeof AudioManager !== 'undefined') AudioManager.play('success');

      huntDropdownFeedback.textContent = '';
      huntDropdownFeedback.className = 'feedback';
      huntDropdownSubmit.disabled = true;
      huntDropdownSkip.style.display = 'none';

      // Show the grand success banner ABOVE the dropdown overlay
      successBanner.style.display = 'flex';
      successBanner.style.zIndex = '26000';

      // Start continuous confetti
      startContinuousConfetti();
    } else {
      if (typeof AudioManager !== 'undefined') AudioManager.play('error');
      huntDropdownFeedback.textContent = 'Some answers are incorrect. Try again!';
      huntDropdownFeedback.className = 'feedback error';
    }
  });

  huntDropdownSkip.addEventListener('click', () => {
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');

    // Deduct the points gained for finding the word since they skipped the definition test
    currentScore = Math.max(0, currentScore - 100);
    scoreEl.textContent = `${currentScore} pts`;

    activeDropdownTestAnswers.forEach(ans => {
      const container = document.getElementById(ans.id);
      const btn = container.querySelector('.custom-dropdown-btn');
      const btnText = btn.querySelector('.btn-text');
      btnText.textContent = ans.correct;
      btn.dataset.selected = ans.correct;
      btn.classList.remove('wrong');
      btn.classList.add('correct');
    });

    huntDropdownFeedback.textContent = 'Skipped. Showing correct answers.';
    huntDropdownFeedback.className = 'feedback';
    huntDropdownSubmit.disabled = true;
    huntDropdownSkip.style.display = 'none';

    setTimeout(() => {
      closeTestAndCheckWin();
    }, 2000);
  });

  function closeTestAndCheckWin() {
    huntDropdownOverlay.classList.remove('active');
    if (foundWords.length === targetWords.length) {
      handleWin();
    }
  }

  let confettiInterval;
  function startContinuousConfetti() {
    if (typeof confetti === 'function') {
      const defaults = {
        spread: 60,
        ticks: 100,
        gravity: 0.9,
        decay: 0.92,
        startVelocity: 45,
        zIndex: 10002, // Ensure it is above the new banner
        scalar: 1.5,
        shapes: ['star', 'circle', 'square'],
        colors: ['#F5C842', '#D4AF37', '#C9A96E', '#E8B4B8', '#ffffff', '#B8860B', '#E8D5B7']
      };

      function shoot() {
        // Left corner
        confetti({
          ...defaults,
          particleCount: 60,
          angle: 60,
          origin: { x: 0, y: 1 }
        });

        // Right corner
        confetti({
          ...defaults,
          particleCount: 60,
          angle: 120,
          origin: { x: 1, y: 1 }
        });
      }

      shoot();
      confettiInterval = setInterval(shoot, 800);
    }
  }

  function stopContinuousConfetti() {
    if (confettiInterval) {
      clearInterval(confettiInterval);
      confettiInterval = null;
    }
  }

  if (successThanksBtn) {
    successThanksBtn.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      successBanner.style.display = 'none';
      stopContinuousConfetti();
      closeTestAndCheckWin();
    });
  }

  function getRandomTrickWords(correctWord, num = 3) {
    let all = [];
    if (typeof window.STEMDictionary !== 'undefined') {
      if (typeof window.STEMDictionary.getAllWords === 'function') {
        all = window.STEMDictionary.getAllWords().map(w => w.word);
      } else if (window.STEMDictionary.wordBank) {
        const bank = window.STEMDictionary.wordBank;
        for (let letter in bank) {
          all.push(...bank[letter].map(w => w.word));
        }
      }
    }
    if (all.length < 5) {
      all = ['Energy', 'Matter', 'Cell', 'Force', 'Space', 'Gene', 'Atom', 'Bond', 'Mass', 'Acid'];
    }

    let tricks = [];
    let attempts = 0;
    while (tricks.length < num && attempts < 100) {
      attempts++;
      let word = all[Math.floor(Math.random() * all.length)];
      word = String(word).split(' ')[0]; // Take only first word to keep dropdown options short
      if (!word) continue;
      word = word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();

      if (word.toLowerCase() !== String(correctWord).toLowerCase() && !tricks.includes(word)) {
        tricks.push(word);
      }
    }
    return tricks;
  }

  function handleWin() {
    setTimeout(() => {
      // Calculate time spent
      const endTime = Date.now();
      const timeDiff = stageStartTime ? Math.floor((endTime - stageStartTime) / 1000) : 0;
      const min = Math.floor(timeDiff / 60);
      const sec = timeDiff % 60;
      const formattedTime = `${min.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;

      // Calculate difficulty bonus
      let bonus = 100;
      if (currentLevelObj.lvl === 'Easy') bonus = 50;
      if (currentLevelObj.lvl === 'Intellect') bonus = 200;

      // Add bonus to score
      currentScore += bonus;

      // Update total score in localStorage
      const totalScore = parseInt(localStorage.getItem('osmosis_total_score')) || 0;
      localStorage.setItem('osmosis_total_score', totalScore + currentScore);

      // Save to shared state as well so it propagates
      let gameData = sharedState.load() || {};
      gameData.score = (gameData.score || 0) + currentScore;
      sharedState.save(gameData);

      // Refresh top header stats (XP bar animation & Gem earnings)
      updateProgressionHeader();

      // Populate results details
      const wordsFoundEl = document.getElementById('result-words-found');
      if (wordsFoundEl) wordsFoundEl.textContent = `${foundWords.length}/${targetWords.length}`;

      const timeSpentEl = document.getElementById('result-time-spent');
      if (timeSpentEl) timeSpentEl.textContent = formattedTime;

      const totalScoreEl = document.getElementById('result-total-score');
      if (totalScoreEl) totalScoreEl.textContent = currentScore;

      // Render words mastered list with new duo chip style
      const wordListHost = document.getElementById('result-words-list');
      if (wordListHost) {
        wordListHost.innerHTML = '';
        foundWords.forEach(w => {
          const chip = document.createElement('span');
          chip.className = 'duo-word-chip';
          chip.textContent = w;
          wordListHost.appendChild(chip);
        });
      }

      // Show win overlay
      winOverlay.classList.add('active');

      setTimeout(() => {
        if (typeof AudioManager !== 'undefined') {
          AudioManager.init();
          AudioManager.play('fanfare');
        }
      }, 300);

    }, 800);
  }

  // Navigation Buttons
  overlayHomeBtn.addEventListener('click', goHome);
  backBtn.addEventListener('click', goHome);

  function goHome() {
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');
    if (typeof window.navigateWithTransition === 'function') navigateWithTransition('01_home_menu.html');
    else window.location.href = '01_home_menu.html';
  }

  overlayContinueBtn.addEventListener('click', () => {
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');
    winOverlay.classList.remove('active');

    // Increment a "Streak / Game Level" count to show progress going up
    const currentStreak = parseInt(localStorage.getItem('osmosis_hunt_streak')) || 0;
    localStorage.setItem('osmosis_hunt_streak', currentStreak + 1);

    // Re-initialize a brand new game with a fresh set of words
    initGame();
  });

  // --- Guiding Wizard Logic ---
  let wizardCurrentStep = 1;
  const wizardOverlay = document.getElementById('guiding-wizard-overlay');
  const wizardNextBtn = document.getElementById('wizard-next-btn');
  const wizardBackBtn = document.getElementById('wizard-back-btn');
  const wizardSteps = document.querySelectorAll('.wizard-step');
  const wizardDots = document.querySelectorAll('.wizard-progress-dots .dot');

  function updateWizardUI() {
    wizardSteps.forEach((step) => {
      if (parseInt(step.dataset.step) === wizardCurrentStep) {
        step.style.display = 'block';
      } else {
        step.style.display = 'none';
      }
    });

    wizardDots.forEach((dot, index) => {
      if (index + 1 === wizardCurrentStep) {
        dot.classList.add('active');
      } else {
        dot.classList.remove('active');
      }
    });

    if (wizardCurrentStep === 1) {
      wizardBackBtn.style.display = 'none';
      wizardNextBtn.textContent = 'Next';
    } else if (wizardCurrentStep === 3) {
      wizardBackBtn.style.display = 'block';
      wizardNextBtn.textContent = 'Got It!';
    } else {
      wizardBackBtn.style.display = 'block';
      wizardNextBtn.textContent = 'Next';
    }
  }

  if (wizardNextBtn && wizardBackBtn) {
    wizardNextBtn.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      if (wizardCurrentStep < 3) {
        wizardCurrentStep++;
        updateWizardUI();
      } else {
        localStorage.setItem('wordHuntWizardShown', 'true');
        if (wizardOverlay) wizardOverlay.style.display = 'none';
        const diffOverlay = document.getElementById('difficulty-overlay');
        const savedDiff = localStorage.getItem('osmosis_hunt_diff');
        if (savedDiff && DIFFICULTY_CONFIGS[savedDiff]) {
          currentLevelObj = DIFFICULTY_CONFIGS[savedDiff];
          if (diffOverlay) diffOverlay.style.display = 'none';
          initGame();
        } else {
          if (diffOverlay) diffOverlay.style.display = 'flex';
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

  const helpBtn = document.getElementById('help-btn');
  if (helpBtn) {
    helpBtn.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      wizardCurrentStep = 1;
      updateWizardUI();
      if (wizardOverlay) wizardOverlay.style.display = 'flex';
    });
  }

  // Load saved difficulty preference if present
  const savedDiffPref = localStorage.getItem('osmosis_hunt_diff');
  if (savedDiffPref && DIFFICULTY_CONFIGS[savedDiffPref]) {
    currentLevelObj = DIFFICULTY_CONFIGS[savedDiffPref];
  }

  // Check if wizard or difficulty overlay needs to be shown
  if (!localStorage.getItem('wordHuntWizardShown')) {
    if (wizardOverlay) wizardOverlay.style.display = 'flex';
    const diffOverlay = document.getElementById('difficulty-overlay');
    if (diffOverlay) diffOverlay.style.display = 'none';
  } else {
    const diffOverlay = document.getElementById('difficulty-overlay');
    if (savedDiffPref && DIFFICULTY_CONFIGS[savedDiffPref]) {
      if (diffOverlay) diffOverlay.style.display = 'none';
      initGame();
    } else {
      if (diffOverlay) diffOverlay.style.display = 'flex';
    }
  }

  if (window.location.search.includes('celebration=true')) {
    launchGrandCelebration();
  }
});
