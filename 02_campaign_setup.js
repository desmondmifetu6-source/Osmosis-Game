// =====================================================================
// FILE: 02_campaign_setup.js (The Mission Dispenser)
// =====================================================================
// Imagine being a secret agent and getting your next top-secret mission envelope.
// This file looks at what alphabet letters you've already completed.
// It then rolls a dice to assign you a totally random Letter and Word Length 
// to hunt down next in the dictionary!

const CampaignSetupController = {
  // Contains mutable data state and element caching
  state: {
    gameData: null,
    domCache: {},
    cipherInterval: null
  },

  init() {
    this.state.gameData = sharedState.load();

    if (!this.state.gameData.username) {
      window.location.href = '00_login.html';
      return;
    }

    this.prepareData();
    this.cacheDOM();
    this.routeFlow();
  },

  prepareData() {
    const { gameData } = this.state;
    if (!gameData.usedLetters) gameData.usedLetters = [];
    if (!gameData.selectedWords) gameData.selectedWords = [];
    if (typeof gameData.score === 'undefined') gameData.score = 0;
  },

  cacheDOM() {
    this.state.domCache = {
      setupContinueBtn: document.getElementById('setup-continue-btn'),
      setupCodeEl: document.getElementById('setup-code'),
      setupDescEl: document.getElementById('setup-desc'),
      setupStatusText: document.getElementById('setup-status-text'),
      rulesScreen: document.getElementById('rules-screen'),
      generatorScreen: document.getElementById('generator-screen'),
      rulesContinueBtn: document.getElementById('rules-continue-btn')
    };
  },

  routeFlow() {
    const { domCache, gameData } = this.state;

    // If they have played before, skip rules
    if (gameData.usedLetters && gameData.usedLetters.length > 0) {
      if (domCache.rulesScreen) domCache.rulesScreen.style.display = 'none';
      if (domCache.generatorScreen) domCache.generatorScreen.style.display = 'block';
      this.runSelectionAlgorithm();
    } else {
      if (domCache.rulesContinueBtn) {
        domCache.rulesContinueBtn.addEventListener('click', () => {
          if (domCache.rulesScreen) domCache.rulesScreen.style.display = 'none';
          if (domCache.generatorScreen) domCache.generatorScreen.style.display = 'block';
          this.runSelectionAlgorithm();
        });
      } else {
        this.runSelectionAlgorithm(); // Fallback
      }
    }

    if (domCache.setupContinueBtn) {
      domCache.setupContinueBtn.addEventListener('click', () => {
        if (typeof window.navigateWithTransition === 'function') {
          navigateWithTransition('03_stage1_word_selection.html');
        } else {
          window.location.href = '03_stage1_word_selection.html';
        }
      });
    }
  },

  runSelectionAlgorithm() {
    const { domCache, gameData } = this.state;
    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const availableLetters = alphabet.split('').filter(l => !gameData.usedLetters.includes(l));

    // If we ran out of alphabet letters...
    if (availableLetters.length === 0) {
      if (typeof showModal === 'function') {
        showModal('Mission Complete', 'Every letter done — continuing to the next stage.');
        setTimeout(() => {
          if (typeof window.navigateWithTransition === 'function') navigateWithTransition('04_stage2_primary_recall.html');
          else window.location.href = '04_stage2_primary_recall.html';
        }, 1700);
      } else {
        if (typeof window.navigateWithTransition === 'function') navigateWithTransition('04_stage2_primary_recall.html');
        else window.location.href = '04_stage2_primary_recall.html';
      }
      return;
    }

    if (domCache.setupStatusText) domCache.setupStatusText.textContent = "Shuffling constraints...";

    let counter = 0;
    this.state.cipherInterval = setInterval(() => {
      let randChar = availableLetters[Math.floor(Math.random() * availableLetters.length)];
      let randLength = Math.floor(Math.random() * 8) + 4;

      if (domCache.setupCodeEl) domCache.setupCodeEl.textContent = `${randLength},${randChar}`;
      counter++;

      if (counter > 30) {
        clearInterval(this.state.cipherInterval);
        this.finalizeAssignment(availableLetters);
      }
    }, 50);
  },

  finalizeAssignment(availableLetters) {
    const { domCache, gameData } = this.state;

    gameData.letter = availableLetters[Math.floor(Math.random() * availableLetters.length)];
    gameData.usedLetters.push(gameData.letter);
    gameData.letters = [gameData.letter];

    let possibleWords = [];
    if (typeof window.STEMDictionary !== 'undefined') {
      possibleWords = window.STEMDictionary.getWordsByLetter(gameData.letter).map(w => w.word);
    } else {
      possibleWords = ["biology", "bacteria", "botany", "biodiversity"];
    }

    const globalUsedRaw = JSON.parse(localStorage.getItem('osmosis_global_used_words')) || [];
    const now = Date.now();
    const cooldownMs = 3 * 24 * 60 * 60 * 1000;

    const onCooldown = globalUsedRaw.map(item => typeof item === 'string' ? { word: item.toLowerCase(), time: now } : item)
      .filter(item => (now - item.time) < cooldownMs)
      .map(i => i.word);

    let freshWords = possibleWords.filter(w => !onCooldown.includes(w.toLowerCase()));
    if (freshWords.length === 0) freshWords = possibleWords;
    possibleWords = freshWords;

    if (possibleWords.length > 0) {
      let chosenWord = possibleWords[Math.floor(Math.random() * possibleWords.length)];
      gameData.length = chosenWord.length;
    } else {
      gameData.length = 7;
    }

    gameData.wordsPool = possibleWords;

    if (typeof AudioManager !== 'undefined') AudioManager.play('success');
    sharedState.save(gameData);

    if (domCache.setupStatusText) domCache.setupStatusText.textContent = "ASSIGNMENT GENERATOR";
    if (domCache.setupCodeEl) domCache.setupCodeEl.innerHTML = `<span style="animation: pulse 1s ease-in-out;">${gameData.length},${gameData.letter}</span>`;
    if (domCache.setupDescEl) domCache.setupDescEl.innerHTML = `implies.<br>Select one word starting with '<strong>${gameData.letter}</strong>' and exactly <strong>${gameData.length}</strong> letters long.`;

    if (domCache.setupContinueBtn) {
      domCache.setupContinueBtn.style.display = 'block';
      domCache.setupContinueBtn.textContent = 'Go Pick Word';
    }
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => CampaignSetupController.init());
} else {
  CampaignSetupController.init();
}
