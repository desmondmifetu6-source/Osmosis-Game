// =====================================================================
// FILE: 03_stage1_word_selection.js (The Scavenger Hunt)
// =====================================================================
// Welcome to Stage 1! The Mission Dispenser just told us what Letter and Length 
// we need to find. Now, we spawn a big pool of words on the screen, and the 
// player has to click the ONE word that perfectly matches their mission.

const Stage1Controller = {
  state: {
    gameData: null,
    domCache: {},
    featuredWordThisRound: null,
    localSelectedWord: null
  },

  init() {
    if (typeof initModal === 'function') initModal();
    sharedState.startTimer();
    this.state.gameData = sharedState.load();
    sharedState.updateTimerUI();

    // Security Check
    if (!this.state.gameData.letter || typeof this.state.gameData.length === 'undefined') {
      window.location.href = 'index.html';
      return;
    }

    if (!this.state.gameData.selectedWords) this.state.gameData.selectedWords = [];

    this.cacheDOM();
    this.renderInitialUI();
    this.attachListeners();
    this.generateLengthAndWords();
    this.updateCount();
  },

  cacheDOM() {
    this.state.domCache = {
      scoreEl: document.getElementById('current-score'),
      poolContainer: document.getElementById('word-pool'),
      boardContainer: document.getElementById('pasted-words'),
      countEl: document.getElementById('s2-count'),
      finishBtn: document.getElementById('s2-finish-btn'),
      progressEl: document.getElementById('s2-progress'),
      transitionContainer: document.getElementById('transition-container'),
      mainContainer: document.getElementById('main-container'),
      startBtn: document.getElementById('start-btn'),
      targetLetterEl: document.getElementById('s2-letter'),
      targetLengthEl: document.getElementById('s2-length'),
      sb: document.getElementById('scoreboard'),
      skipBtn: document.getElementById('s2-skip-btn')
    };
  },

  renderInitialUI() {
    const { domCache, gameData } = this.state;
    
    if (domCache.scoreEl) domCache.scoreEl.textContent = gameData.score || 0;
    
    const currentLetter = gameData.letter.toUpperCase();
    if (domCache.targetLetterEl) domCache.targetLetterEl.textContent = currentLetter;
    if (domCache.progressEl) domCache.progressEl.textContent = (gameData.selectedWords ? gameData.selectedWords.length : 0) + 1;
  },

  attachListeners() {
    const { domCache } = this.state;

    if (domCache.startBtn && domCache.transitionContainer && domCache.mainContainer) {
      domCache.startBtn.addEventListener('click', () => {
        domCache.transitionContainer.style.display = 'none';
        domCache.mainContainer.style.display = 'block';
      });
    }

    if (domCache.finishBtn) {
      domCache.finishBtn.addEventListener('click', () => this.handleProceed());
    }

    if (domCache.skipBtn) {
      domCache.skipBtn.addEventListener('click', () => this.handleSkip());
    }
  },

  shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  },

  // Function: generateLengthAndWords
  // This is the heart of the scavenger hunt! It builds a massive random pool of words,
  // making sure at least ONE word exactly matches your target letter and length.
  generateLengthAndWords() {
    const { gameData, domCache } = this.state;
    const currentLetter = gameData.letter.toUpperCase();

    let allWordsForLetter = []; // We removed the fake fallback words!
    if (typeof window.STEMDictionary !== 'undefined') {
      const rawWords = window.STEMDictionary.getWordsByLetter(currentLetter);
      // ONLY accept words that actually have a definition in the dictionary!
      if (rawWords.length > 0) {
        allWordsForLetter = rawWords.filter(w => w.definition && w.definition.trim() !== "").map(w => w.word);
      }
    }

    if (domCache.targetLengthEl) domCache.targetLengthEl.textContent = gameData.length;

    // Cooldown System
    const globalUsedRaw = JSON.parse(localStorage.getItem('osmosis_global_used_words')) || [];
    const now = Date.now();
    const cooldownMs = 3 * 24 * 60 * 60 * 1000;

    const onCooldown = globalUsedRaw.map(item => typeof item === 'string' ? { word: item.toLowerCase(), time: now } : item)
      .filter(item => (now - item.time) < cooldownMs)
      .map(i => i.word);

    let freshWords = allWordsForLetter.filter(w => !onCooldown.includes(w.toLowerCase()));

    if (freshWords.filter(w => w.length === gameData.length).length === 0) {
      freshWords = allWordsForLetter;
    }

    const correctWords = this.shuffle(freshWords.filter(w => w.length === gameData.length));

    let workingCorrect = correctWords;
    if (workingCorrect.length === 0) {
      workingCorrect = [String(currentLetter).repeat(Math.max(3, gameData.length))];
    }

    this.state.featuredWordThisRound = workingCorrect[Math.floor(Math.random() * workingCorrect.length)];

    let finalPool = [];
    const maxPoolSize = 20;

    let uniqueSelected = this.shuffle(workingCorrect).slice(0, maxPoolSize);
    uniqueSelected.forEach(w => finalPool.push(w));

    finalPool = this.shuffle(finalPool);

    if (!finalPool.includes(this.state.featuredWordThisRound)) {
      finalPool[Math.floor(Math.random() * finalPool.length)] = this.state.featuredWordThisRound;
    }

    let targetSpawned = false;

    // Paste old words
    gameData.selectedWords.forEach(w => this.spawnPastedWord(w, true));

    // Spawn new pool
    finalPool.forEach(word => {
      let isFeatured = false;
      if (!targetSpawned && word.toLowerCase() === this.state.featuredWordThisRound.toLowerCase()) {
        isFeatured = true;
        targetSpawned = true;
      }
      this.spawnStaticWord(word, isFeatured);
    });
  },

  // Function: spawnStaticWord
  // This builds a single 'word tile' floating in the pool. It also secretly tags 
  // the tile if it's the exact target word we are hunting for!
  spawnStaticWord(word, isFeatured = false) {
    const { domCache, gameData } = this.state;
    if (!domCache.poolContainer) return;

    const tile = document.createElement('div');
    tile.className = 'word-tile';

    if (word.length === gameData.length) tile.classList.add('correct-length');
    if (isFeatured) tile.classList.add('highlighted-target');

    tile.textContent = word;
    tile.dataset.isTarget = isFeatured ? "true" : "false";

    tile.addEventListener('click', () => this.handleWordClick(tile, word));
    domCache.poolContainer.appendChild(tile);
  },

  // Function: spawnPastedWord
  // Once you select a word, we remove it from the pool and "paste" it onto your
  // permanent player board like a sticker, rotating it randomly for a cool effect.
  spawnPastedWord(word, isOld = false) {
    const { domCache } = this.state;
    if (!domCache.boardContainer) return;

    const pastedNode = document.createElement('div');
    pastedNode.className = 'word-tile pasted-word';
    pastedNode.textContent = word;

    if (isOld) {
      pastedNode.style.animation = 'none';
      pastedNode.style.opacity = '0.6';
      pastedNode.style.transform = `scale(0.85) rotate(${Math.floor(Math.random() * 8) - 4}deg)`;
    } else {
      const rot = Math.floor(Math.random() * 8) - 4;
      pastedNode.style.animation = `pasteIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards`;
      pastedNode.style.transform = `rotate(${rot}deg)`;
    }

    domCache.boardContainer.appendChild(pastedNode);
  },

  // Function: handleWordClick
  // What happens when you tap a word tile? This checks your backpack to see if 
  // you collected it yet. If it's the right word, you get 5 points!
  handleWordClick(tile, word) {
    if (tile.dataset.collected === "true") return;

    if (this.state.localSelectedWord !== null) {
      if (typeof showModal === 'function') showModal('Limit', 'Only 1 word per letter.');
      return;
    }

    const isTarget = tile.dataset.isTarget === "true";

    if (isTarget) {
      this.state.localSelectedWord = word;
      tile.dataset.collected = "true";
      if (typeof AudioManager !== 'undefined') AudioManager.play('success');

      this.rewardPoints(5, tile);

      tile.style.animation = 'none';
      tile.style.transform = 'scale(0)';
      tile.style.opacity = '0';

      setTimeout(() => {
        if (tile.parentNode) tile.remove();
        this.spawnPastedWord(word, false);
        this.updateCount();
      }, 200);
    }
  },

  rewardPoints(amount, originElement) {
    const { domCache, gameData } = this.state;
    
    gameData.score = (gameData.score || 0) + amount;
    
    if (domCache.scoreEl) domCache.scoreEl.textContent = gameData.score;
    if (domCache.sb) {
      domCache.sb.style.animation = 'none';
      domCache.sb.offsetHeight; // trigger reflow
      domCache.sb.style.animation = 'scorePop 0.3s ease-out forwards';
    }

    if (originElement) {
      const rect = originElement.getBoundingClientRect();
      const floater = document.createElement('div');
      floater.className = 'floating-point';
      floater.textContent = `+${amount}`;
      floater.style.left = `${rect.left + rect.width / 2}px`;
      floater.style.top = `${rect.top - 20}px`;
      document.body.appendChild(floater);
      setTimeout(() => floater.remove(), 1000);
    }
  },

  updateCount() {
    const { domCache, gameData, localSelectedWord } = this.state;
    
    if (domCache.countEl) domCache.countEl.textContent = localSelectedWord ? '1' : '0';
    if (domCache.finishBtn) {
      domCache.finishBtn.disabled = localSelectedWord === null;
      
      let usedCount = gameData.usedLetters ? gameData.usedLetters.length : 1;
      if (usedCount >= 26) {
        domCache.finishBtn.textContent = "Finalize Board & Proceed";
      } else {
        domCache.finishBtn.textContent = "Next Alphabet";
      }
    }
  },

  // Function: handleProceed
  // You clicked finish! We save your new word to the global save file (cooldown memory)
  // so you don't get the same word again for 3 days. Then we move you along!
  handleProceed() {
    const { gameData, localSelectedWord } = this.state;

    if (localSelectedWord) {
      gameData.selectedWords.push(localSelectedWord);

      // Save to global cooldown
      const gl = JSON.parse(localStorage.getItem('osmosis_global_used_words')) || [];
      const wordToLower = localSelectedWord.toLowerCase();
      const now = Date.now();
      let upgradedGl = gl.map(item => {
        if (typeof item === 'string') return { word: item.toLowerCase(), time: now - (4 * 24 * 60 * 60 * 1000) };
        return item;
      });
      upgradedGl = upgradedGl.filter(item => item.word !== wordToLower);
      upgradedGl.push({ word: wordToLower, time: now });
      localStorage.setItem('osmosis_global_used_words', JSON.stringify(upgradedGl));
    }

    let usedCount = gameData.usedLetters ? gameData.usedLetters.length : 1;
    sharedState.save(gameData);

    // If we've completed all letters...
    if (usedCount >= 26) {
      sharedState.recordStageScore('03_stage1', 'Stage 1: Word Selection', gameData.selectedWords.length * 5);
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('04_stage2_word_fillin.html');
      else window.location.href = '04_stage2_word_fillin.html';
    } else {
      // Otherwise, keep hunting for the next letter!
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('02_campaign_setup.html');
      else window.location.href = '02_campaign_setup.html';
    }
  },

  handleSkip() {
    const { gameData, localSelectedWord } = this.state;
    if (localSelectedWord && !gameData.selectedWords.includes(localSelectedWord)) {
      gameData.selectedWords.push(localSelectedWord);
    }
    if (gameData.selectedWords.length === 0) {
      if (typeof showModal === 'function') showModal('Wait', 'Select at least 1 word before skipping.');
      return;
    }
    
    sharedState.save(gameData);
    sharedState.recordStageScore('03_stage1', 'Stage 1: Word Selection', gameData.selectedWords.length * 5);
    if (typeof window.navigateWithTransition === 'function') navigateWithTransition('04_stage2_word_fillin.html');
    else window.location.href = '04_stage2_word_fillin.html';
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => Stage1Controller.init());
} else {
  Stage1Controller.init();
}
