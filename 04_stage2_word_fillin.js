// =====================================================================
// FILE: 04_stage2_primary_recall.js (The Fill-in-the-Blanks Test)
// =====================================================================
// Welcome to Stage 2! The player has collected all 26 of their words.
// Now, we hide a few letters from each word, and they must remember how to spell them!

const CONFIG = {
  TIME_PER_WORD: 8,       
  MASK_PERCENTAGE: 0.4,   
  POINTS_PER_CORRECT: 5   
};

const Stage2Controller = {
  state: {
    gameData: null,
    domCache: {},
    meanings: {},
    sequence: [],
    currentIndex: 0,
    roundScore: 0,
    timerInt: null
  },

  async init() {
    if (typeof initModal === 'function') initModal();
    sharedState.startTimer();
    this.state.gameData = sharedState.load();
    sharedState.updateTimerUI();

    if (!this.state.gameData.selectedWords || this.state.gameData.selectedWords.length === 0) {
      window.location.href = 'index.html';
      return;
    }

    this.cacheDOM();
    this.renderInitialUI();
    this.attachListeners();

    await this.loadMeanings();
    this.startRevisionPhase();
  },

  cacheDOM() {
    this.state.domCache = {
      scoreEl: document.getElementById('current-score'),
      loadingContainer: document.getElementById('loading-container'),
      revisionContainer: document.getElementById('revision-container'),
      lap1Container: document.getElementById('lap1-container'),
      revList: document.getElementById('rev-list'),
      revTimer: document.getElementById('rev-timer'),
      startEarlyBtn: document.getElementById('start-test-early-btn'),
      lap1Input: document.getElementById('lap1-input'),
      lap1Submit: document.getElementById('lap1-submit'),
      lap1Feedback: document.getElementById('lap1-feedback'),
      lap1Display: document.getElementById('lap1-word-display'),
      lap1Progress: document.getElementById('lap1-progress')
    };
  },

  renderInitialUI() {
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score || 0;
    }
  },

  attachListeners() {
    const { domCache } = this.state;
    if (domCache.startEarlyBtn) {
      domCache.startEarlyBtn.addEventListener('click', () => {
        this.clearTimer();
        this.startTestPhase();
      });
    }

    if (domCache.lap1Submit) {
      domCache.lap1Submit.addEventListener('click', () => this.handleValidation());
    }

    if (domCache.lap1Input) {
      domCache.lap1Input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') this.handleValidation();
      });
    }
  },

  async loadMeanings() {
    if (!this.state.meanings) this.state.meanings = {};
    for (let w of this.state.gameData.selectedWords) {
      if (!this.state.meanings[w]) {
        try {
          this.state.meanings[w] = typeof DictionaryLogic !== 'undefined' ? DictionaryLogic.fetchMeaning(w) : "Definition unavailable";
        } catch(e) {
          this.state.meanings[w] = "Definition unavailable";
        }
      }
    }
    this.state.gameData.meanings = this.state.meanings;
    sharedState.save(this.state.gameData);
  },

  shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  },

  maskWord(word) {
    let arr = word.toUpperCase().split('');
    let len = word.length;
    let numToMask = Math.min(2, Math.max(1, Math.floor(len * CONFIG.MASK_PERCENTAGE)));
    let validIndices = [];

    for (let i = 1; i < len; i++) {
        validIndices.push(i);
    }
    
    let chosen = [];
    if (validIndices.length > 0) {
      if (numToMask === 1 || validIndices.length < 3) {
          chosen.push(validIndices[Math.floor(Math.random() * validIndices.length)]);
      } else {
          let found = false;
          let shuffled = this.shuffle([...validIndices]);
          for (let i = 0; i < shuffled.length; i++) {
              for (let j = i + 1; j < shuffled.length; j++) {
                  if (Math.abs(shuffled[i] - shuffled[j]) > 1) {
                      chosen.push(shuffled[i], shuffled[j]);
                      found = true;
                      break;
                  }
              }
              if (found) break;
          }
          if (!found) chosen.push(shuffled[0]);
      }
    }
    
    chosen.forEach(i => arr[i] = '_');
    return arr.join(' ');
  },

  formatTime(sec) {
    const min = String(Math.floor(sec / 60)).padStart(2, '0');
    const s = String(sec % 60).padStart(2, '0');
    return `${min}:${s}`;
  },

  startRevisionPhase() {
    const { domCache, gameData, meanings } = this.state;
    if (domCache.loadingContainer) domCache.loadingContainer.style.display = 'none';
    if (domCache.revisionContainer) domCache.revisionContainer.style.display = 'block';
    if (domCache.revList) domCache.revList.innerHTML = '';

    gameData.selectedWords.forEach(w => {
      const item = document.createElement('div');
      item.className = 'revision-item';
      item.innerHTML = `<strong>${w}</strong><p>${meanings[w]}</p>`;
      if (domCache.revList) domCache.revList.appendChild(item);
    });

    let timeLeft = gameData.selectedWords.length * CONFIG.TIME_PER_WORD;

    this.state.timerInt = setInterval(() => {
      if (domCache.revTimer) domCache.revTimer.textContent = this.formatTime(timeLeft);
      if (timeLeft-- <= 0) {
        this.clearTimer();
        this.startTestPhase();
      }
    }, 1000);
  },

  clearTimer() {
    if (this.state.timerInt) {
      clearInterval(this.state.timerInt);
      this.state.timerInt = null;
    }
  },

  startTestPhase() {
    const { domCache, gameData } = this.state;
    if (domCache.revisionContainer) domCache.revisionContainer.style.display = 'none';
    if (domCache.lap1Container) domCache.lap1Container.style.display = 'block';

    this.state.sequence = this.shuffle([...gameData.selectedWords]);
    this.state.currentIndex = 0;
    this.renderCurrentQuestion();
  },

  renderCurrentQuestion() {
    const { domCache, sequence, currentIndex } = this.state;
    if (currentIndex >= sequence.length) return;

    const word = sequence[currentIndex];

    if (domCache.lap1Display) domCache.lap1Display.textContent = this.maskWord(word);
    if (domCache.lap1Progress) domCache.lap1Progress.textContent = `${currentIndex + 1} / ${sequence.length}`;

    if (domCache.lap1Input) {
      domCache.lap1Input.value = '';
      domCache.lap1Input.disabled = false;
      domCache.lap1Input.focus();
    }

    if (domCache.lap1Feedback) {
      domCache.lap1Feedback.textContent = '';
      domCache.lap1Feedback.className = 'feedback';
    }

    if (domCache.lap1Submit) domCache.lap1Submit.textContent = "Submit";
  },

  handleValidation() {
    const { domCache, sequence, currentIndex } = this.state;
    
    if (domCache.lap1Submit && domCache.lap1Submit.textContent === "Next") {
      this.state.currentIndex++;
      if (this.state.currentIndex < sequence.length) {
        this.renderCurrentQuestion();
      } else {
        this.finishGame();
      }
      return;
    }

    const inputVal = domCache.lap1Input ? domCache.lap1Input.value.trim().toLowerCase() : '';
    if (!inputVal) return;

    const correctWord = sequence[currentIndex].toLowerCase();
    const isCorrect = inputVal === correctWord;

    if (domCache.lap1Input) domCache.lap1Input.disabled = true;

    if (isCorrect) {
      this.triggerFeedback("Correct!", 'success');
      this.rewardPoints(CONFIG.POINTS_PER_CORRECT);
    } else {
      this.triggerFeedback(`Incorrect. Word was "${correctWord.toUpperCase()}"`, 'error');
    }

    if (domCache.lap1Submit) domCache.lap1Submit.textContent = "Next";
  },

  triggerFeedback(message, type) {
    const { domCache } = this.state;
    if (domCache.lap1Feedback) {
      domCache.lap1Feedback.textContent = message;
      domCache.lap1Feedback.className = `feedback ${type}`;
    }
    if (typeof AudioManager !== 'undefined') AudioManager.play(type);
  },

  rewardPoints(amount) {
    this.state.roundScore += amount;
    this.state.gameData.score = (this.state.gameData.score || 0) + amount;
    
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score;
    }

    const btn = this.state.domCache.lap1Submit;
    if (btn) {
      const rect = btn.getBoundingClientRect();
      const floater = document.createElement('div');
      floater.className = 'floating-point';
      floater.textContent = `+${amount}`;
      floater.style.left = `${rect.left + rect.width / 2}px`;
      floater.style.top = `${rect.top - 20}px`;
      document.body.appendChild(floater);
      setTimeout(() => floater.remove(), 1000);
    }
  },

  finishGame() {
    sharedState.save(this.state.gameData);
    
    sharedState.showStageScoreThen(
      'stage2',
      'Stage 2: Word Fill-in',
      this.state.roundScore,
      () => {
        if (typeof window.navigateWithTransition === 'function') navigateWithTransition('05_stage3_flash_recall.html');
        else window.location.href = '05_stage3_flash_recall.html';
      }
    );
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => Stage2Controller.init());
} else {
  Stage2Controller.init();
}
