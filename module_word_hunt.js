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
  const winMessage = document.getElementById('win-message');
  const xpFluid = document.getElementById('xp-fluid');
  const xpText = document.getElementById('xp-text');
  const overlayHomeBtn = document.getElementById('overlay-home-btn');
  const overlayContinueBtn = document.getElementById('overlay-continue-btn');

  // Definition Popup Elements
  const defOverlay = document.getElementById('def-popup-overlay');
  const defTitle = document.getElementById('def-popup-title');
  const defDesc = document.getElementById('def-popup-desc');
  const defContinueBtn = document.getElementById('def-popup-continue');

  // Book Popup Elements
  const bookOverlay = document.getElementById('book-popup-overlay');
  const bookList = document.getElementById('book-definitions-list');
  const bookContinueBtn = document.getElementById('book-popup-continue');

  // Progression Data
  const LEVELS = [
    { lvl: 1, words: 3, maxLen: 5, grid: 6, xpNeeded: 2 },
    { lvl: 2, words: 4, maxLen: 6, grid: 7, xpNeeded: 5 },
    { lvl: 3, words: 5, maxLen: 7, grid: 8, xpNeeded: 9 },
    { lvl: 4, words: 6, maxLen: 8, grid: 9, xpNeeded: 14 },
    { lvl: 5, words: 7, maxLen: 10, grid: 10, xpNeeded: 9999 } // Max level
  ];

  let currentLevelObj = null;
  let gridSize = 6;
  let numWords = 3;

  let grid = [];
  let targetWords = [];
  let foundWords = [];
  let wordCoordinates = {}; // Stores {start, end} for hints
  let wordDefinitions = {}; // Stores {word: definition}
  let currentScore = 0;

  let isSelecting = false;
  let startCell = null;
  let lastValidEndCell = null;
  let selectionPill = null;
  
  const pillColors = ["#818cf8", "#34d399", "#f472b6", "#fb7185", "#38bdf8", "#fbbf24", "#a78bfa"];
  let colorIndex = 0;

  initGame();

  function getCurrentLevelIndex(xp) {
    for (let i = 0; i < LEVELS.length; i++) {
      if (xp < LEVELS[i].xpNeeded) return i;
    }
    return LEVELS.length - 1;
  }

  function initGame() {
    if (typeof initModal === 'function') initModal();
    
    // Load XP and set difficulty
    let xp = parseInt(localStorage.getItem('wordHuntXP')) || 0;
    const lvlIndex = getCurrentLevelIndex(xp);
    currentLevelObj = LEVELS[lvlIndex];
    gridSize = currentLevelObj.grid;
    numWords = currentLevelObj.words;
    
    // Update UI for level
    textLayer.style.setProperty('--grid-size', gridSize);
    lvlBadge.textContent = `Lvl ${currentLevelObj.lvl}`;

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
    winMessage.textContent = "Great job!";
    
    let allWords = [];
    if (typeof window.STEMDictionary !== 'undefined') {
      // Use wordBank (the correct property name) to get all letters
      const bank = window.STEMDictionary.wordBank || {};
      const letters = Object.keys(bank);
      letters.forEach(l => {
        // getWordsByLetter returns [{word, definition}, ...] directly
        allWords.push(...window.STEMDictionary.getWordsByLetter(l));
      });
    }
    
    if (allWords.length === 0) {
      // Fallback only if dictionary truly failed to load
      const fallbacks = [
        {word:"ATOM", definition:"Smallest unit of matter"},
        {word:"CELL", definition:"Basic unit of life"},
        {word:"GENE", definition:"A unit of heredity"},
        {word:"LENS", definition:"A curved piece of glass that focuses light"},
        {word:"BOND", definition:"A force holding atoms together"},
        {word:"MASS", definition:"The amount of matter in an object"},
        {word:"WAVE", definition:"A disturbance that transfers energy"},
        {word:"ACID", definition:"A substance with a pH below 7"},
        {word:"VEIN", definition:"A blood vessel carrying blood to the heart"},
        {word:"CORE", definition:"The central part of the Earth"}
      ];
      allWords = fallbacks;
    }

    let uniqueMap = new Map();
    allWords.forEach(w => {
       const clean = w.word.toUpperCase().replace(/[^A-Z]/g, '');
       if (clean.length >= 3 && clean.length <= currentLevelObj.maxLen) {
           if(!uniqueMap.has(clean)) {
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
    const dirs = [[0,1], [1,0], [1,1], [-1,1], [0,-1], [-1,0], [-1,-1], [1,-1]];
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
            start: {r, c},
            end: {r: r + (word.length - 1)*d[0], c: c + (word.length - 1)*d[1]}
          };
          placed = true;
          successfullyPlaced.push(word);
        }
      }
    });

    targetWords = successfullyPlaced; // Drop any words that couldn't fit

    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for(let i=0; i<gridSize; i++) {
       for(let j=0; j<gridSize; j++) {
          if(grid[i][j] === '') {
             grid[i][j] = letters.charAt(Math.floor(Math.random() * letters.length));
          }
       }
    }
  }

  function canPlace(word, r, c, dr, dc) {
    for(let i=0; i<word.length; i++) {
       const nr = r + i*dr;
       const nc = c + i*dc;
       if(nr < 0 || nr >= gridSize || nc < 0 || nc >= gridSize) return false;
       if(grid[nr][nc] !== '' && grid[nr][nc] !== word[i]) return false;
    }
    return true;
  }

  function placeWord(word, r, c, dr, dc) {
    for(let i=0; i<word.length; i++) {
       const nr = r + i*dr;
       const nc = c + i*dc;
       grid[nr][nc] = word[i];
    }
  }

  function renderGrid() {
    textLayer.innerHTML = '';
    
    for(let r=0; r<gridSize; r++) {
      for(let c=0; c<gridSize; c++) {
        const cell = document.createElement('div');
        cell.className = 'hunt-cell';
        cell.textContent = grid[r][c];
        textLayer.appendChild(cell);
      }
    }

    textLayer.addEventListener('mousedown', handlePointerDown);
    document.addEventListener('mousemove', handlePointerMove);
    document.addEventListener('mouseup', handlePointerUp);

    textLayer.addEventListener('touchstart', handlePointerDown, {passive: false});
    document.addEventListener('touchmove', handlePointerMove, {passive: false});
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
    if(e.touches && e.touches.length > 0) {
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

    if(r >= 0 && r < gridSize && c >= 0 && c < gridSize) {
        return {r, c};
    }
    return null;
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
      lastValidEndCell = cellPos;
      const color = pillColors[colorIndex % pillColors.length];
      updatePillTransform(selectionPill, startCell, lastValidEndCell, color);
    }
  }

  function handlePointerUp(e) {
    if (!isSelecting) return;
    isSelecting = false;

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

    const distance = Math.sqrt((x2 - x1)**2 + (y2 - y1)**2);
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
      
      if (foundWords.length === targetWords.length) {
        handleWin();
      }
    });
  }

  function handleWin() {
    setTimeout(() => {
      // Add standard score
      const totalScore = parseInt(localStorage.getItem('osmosis_total_score')) || 0;
      localStorage.setItem('osmosis_total_score', totalScore + currentScore);

      // Handle Progression
      let xp = parseInt(localStorage.getItem('wordHuntXP')) || 0;
      const oldLvlIndex = getCurrentLevelIndex(xp);
      
      xp++; // Earn 1 session point
      localStorage.setItem('wordHuntXP', xp);
      
      const newLvlIndex = getCurrentLevelIndex(xp);
      const isPromoted = (newLvlIndex > oldLvlIndex);
      const oldLevelObj = LEVELS[oldLvlIndex];

      // Setup overlay UI
      winOverlay.classList.add('active');
      levelText.textContent = `Level ${oldLevelObj.lvl} Clear!`;
      
      const previousTierXp = oldLvlIndex === 0 ? 0 : LEVELS[oldLvlIndex - 1].xpNeeded;
      const pointsInThisTier = xp - previousTierXp;
      const totalPointsInThisTier = oldLevelObj.xpNeeded - previousTierXp;
      
      const startPct = ((pointsInThisTier - 1) / totalPointsInThisTier) * 100;
      xpFluid.style.width = `${Math.max(0, startPct)}%`;
      xpText.textContent = `${pointsInThisTier - 1} / ${totalPointsInThisTier}`;

      setTimeout(() => {
        if (typeof AudioManager !== 'undefined') AudioManager.play('chip');
        const endPct = (pointsInThisTier / totalPointsInThisTier) * 100;
        xpFluid.style.width = `${Math.min(100, endPct)}%`;
        xpText.textContent = `${pointsInThisTier} / ${totalPointsInThisTier}`;

        if (isPromoted) {
          setTimeout(() => {
            if (typeof AudioManager !== 'undefined') AudioManager.play('success');
            promoStar.classList.add('active');
            levelText.textContent = `PROMOTED TO LVL ${LEVELS[newLvlIndex].lvl}!`;
            winMessage.textContent = "Grid expanded. New words unlocked.";
          }, 1000);
        }
      }, 500);

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
    initGame();
  });
});
