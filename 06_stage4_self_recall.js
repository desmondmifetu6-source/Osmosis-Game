// =====================================================================
// FILE: 06_stage4_self_recall.js
// =====================================================================

const Stage4Controller = {
  state: {
    gameData: null,
    domCache: {},
    lap2Score: 0,
    lap2Identified: [],
    lap2TimerInt: null
  },

  init() {
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
  },

  cacheDOM() {
    this.state.domCache = {
      scoreEl: document.getElementById('current-score'),
      transitionContainerLap2: document.getElementById('transition-container'),
      lap2Container: document.getElementById('lap2-container'),
      startLap2Btn: document.getElementById('start-lap2-btn'),
      lap2Timer: document.getElementById('lap2-timer'),
      lap2Input: document.getElementById('lap2-input'),
      lap2Feedback: document.getElementById('lap2-feedback'),
      lap2WordsList: document.getElementById('lap2-words-list')
    };
  },

  renderInitialUI() {
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score || 0;
    }
  },

  attachListeners() {
    const { domCache } = this.state;

    if (domCache.startLap2Btn) {
      domCache.startLap2Btn.addEventListener('click', () => {
        if (domCache.transitionContainerLap2) domCache.transitionContainerLap2.style.display = 'none';
        this.startFinalRecall();
      });
    }

    if (domCache.lap2Input) {
      domCache.lap2Input.addEventListener('keypress', (e) => this.handleLap2Keypress(e));
    }
  },

  startFinalRecall() {
    const { domCache, gameData } = this.state;
    if (domCache.lap2Container) domCache.lap2Container.style.display = 'block';

    let timeLeft = gameData.selectedWords.length * 6;

    if (domCache.lap2Input) domCache.lap2Input.focus();

    const tick = () => {
      const min = String(Math.floor(timeLeft / 60)).padStart(2, '0');
      const sec = String(timeLeft % 60).padStart(2, '0');
      if (domCache.lap2Timer) domCache.lap2Timer.textContent = `${min}:${sec}`;

      if (timeLeft <= 0) {
        this.clearLap2Timer();
        this.endFinalRecall();
      } else if (timeLeft <= 10) {
        if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      }
      timeLeft--;
    };

    tick();
    this.state.lap2TimerInt = setInterval(tick, 1000);
  },

  clearLap2Timer() {
    if (this.state.lap2TimerInt) {
      clearInterval(this.state.lap2TimerInt);
      this.state.lap2TimerInt = null;
    }
  },

  handleLap2Keypress(e) {
    if (e.key !== 'Enter') return;

    const { domCache, gameData } = this.state;
    const val = domCache.lap2Input.value.trim().toLowerCase();
    domCache.lap2Input.value = '';

    if (!val) return;

    if (this.state.lap2Identified.includes(val)) {
      this.triggerLap2Feedback("Already appended!", 'error');
      return;
    }

    const allCorrectWords = gameData.selectedWords.map(w => w.toLowerCase());

    if (allCorrectWords.includes(val)) {
      this.state.lap2Identified.push(val);
      this.triggerLap2Feedback("Match!", 'success');

      this.rewardLap2Points(20);

      const t = document.createElement('div');
      t.className = 'word-tile';
      t.textContent = val;
      if (domCache.lap2WordsList) domCache.lap2WordsList.appendChild(t);

      if (this.state.lap2Identified.length === gameData.selectedWords.length) {
        this.clearLap2Timer();
        setTimeout(() => this.endFinalRecall(), 1000);
      }
    } else {
      this.triggerLap2Feedback("Not in your selection.", 'error');
    }
  },

  triggerLap2Feedback(message, type) {
    if (this.state.domCache.lap2Feedback) {
      this.state.domCache.lap2Feedback.textContent = message;
      this.state.domCache.lap2Feedback.className = `feedback ${type}`;
    }
    const soundType = type === 'success' ? 'chip' : 'error';
    if (typeof AudioManager !== 'undefined') AudioManager.play(soundType);
  },

  rewardLap2Points(amount) {
    this.state.lap2Score += amount;
    this.state.gameData.score = (this.state.gameData.score || 0) + amount;

    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score;
    }

    const el = this.state.domCache.lap2Input;
    if (el) {
      const rect = el.getBoundingClientRect();
      const floater = document.createElement('div');
      floater.className = 'floating-point';
      floater.textContent = `+${amount}`;
      floater.style.left = `${rect.left + rect.width / 2}px`;
      floater.style.top = `${rect.top - 20}px`;
      document.body.appendChild(floater);
      setTimeout(() => floater.remove(), 1000);
    }
  },

  endFinalRecall() {
    const { domCache, gameData } = this.state;
    if (domCache.lap2Container) domCache.lap2Container.style.display = 'none';

    sharedState.save(gameData);
    if (typeof AudioManager !== 'undefined') AudioManager.play('success');

    this.showMissedWordsScreen();
  },

  showMissedWordsScreen() {
    const { gameData } = this.state;
    const allCorrectWords = gameData.selectedWords.map(w => w.toLowerCase());
    const missedWords = allCorrectWords.filter(w => !this.state.lap2Identified.includes(w));

    if (missedWords.length === 0) {
      this.finishStageTransition();
      return;
    }

    const missedWordsContainer = document.getElementById('missed-words-container');
    const missedWordsList = document.getElementById('missed-words-list');

    if (missedWordsContainer && missedWordsList) {
      missedWordsList.innerHTML = '';
      missedWords.forEach((w, index) => {
        const t = document.createElement('div');
        t.className = 'missed-word-tile';
        t.style.animationDelay = `${index * 0.1}s`;
        t.textContent = w;
        missedWordsList.appendChild(t);
      });
      missedWordsContainer.style.display = 'block';

      const continueBtn = document.getElementById('finish-stage-missed-btn');
      if (continueBtn) {
        continueBtn.onclick = () => {
          missedWordsContainer.style.display = 'none';
          this.finishStageTransition();
        };
      }
    } else {
      this.finishStageTransition();
    }
  },

  finishStageTransition() {
    sharedState.showStageScoreThen('06_stage4_self_recall', 'Stage 4: Self-Recall challenge', this.state.lap2Score, () => {
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('07_stage5_meaning_exposure.html');
      else window.location.href = '07_stage5_meaning_exposure.html';
    });
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => Stage4Controller.init());
} else {
  Stage4Controller.init();
}
