// =====================================================================
// FILE: 07_stage5_definition_selection.js (The Multiple Choice Test)
// =====================================================================

const Stage5Controller = {
  state: {
    gameData: null,
    domCache: {},
    testSequence: [],
    testIndex: 0,
    stageScore: 0,
    answerLocked: false
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

    this.state.testSequence = this.shuffle([...this.state.gameData.selectedWords]);
    this.state.testIndex = 0;
    this.renderQuestion();
  },

  cacheDOM() {
    this.state.domCache = {
      scoreEl: document.getElementById('current-score'),
      targetWordEl: document.getElementById('target-word'),
      progressEl: document.getElementById('test-progress'),
      optionsContainer: document.getElementById('options-container'),
      feedbackEl: document.getElementById('test-feedback'),
      nextBtn: document.getElementById('next-btn')
    };
  },

  renderInitialUI() {
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score || 0;
    }
  },

  attachListeners() {
    const { domCache } = this.state;
    
    if (domCache.nextBtn) {
      domCache.nextBtn.addEventListener('click', () => {
        this.state.testIndex++;
        if (this.state.testIndex < this.state.testSequence.length) {
          this.renderQuestion();
        } else {
          this.finishStage();
        }
      });
    }

    // Developer Hack (Alt + P)
    document.addEventListener('keydown', (e) => {
      if (e.key.toLowerCase() === 'p' && e.altKey) {
        e.preventDefault();
        if (!this.state.answerLocked) {
          const allBtns = document.querySelectorAll('.option-btn');
          const correctWord = this.state.testSequence[this.state.testIndex];
          allBtns.forEach(b => {
            if (b.textContent === correctWord) b.click();
          });
        } else {
          if (domCache.nextBtn) domCache.nextBtn.click();
        }
      }
    });
  },

  shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  },

  renderQuestion() {
    const { domCache, testSequence, testIndex, gameData } = this.state;
    
    this.state.answerLocked = false;
    if (domCache.nextBtn) domCache.nextBtn.style.display = 'none';
    if (domCache.feedbackEl) {
      domCache.feedbackEl.textContent = '';
      domCache.feedbackEl.className = 'feedback';
    }

    const currentWord = testSequence[testIndex];
    if (!gameData.meanings) gameData.meanings = {};
    const correctMeaning = gameData.meanings[currentWord] || "Definition not found.";

    if (domCache.targetWordEl) domCache.targetWordEl.textContent = correctMeaning;
    if (domCache.progressEl) domCache.progressEl.textContent = `${testIndex + 1}/${testSequence.length}`;

    const otherWords = Object.keys(gameData.meanings).filter(w => w !== currentWord);
    const pool = this.shuffle(otherWords);

    let options = [currentWord];
    for (let w of pool) {
      if (options.length < 4) options.push(w);
    }

    if (options.length < 4 && typeof window.STEMDictionary !== 'undefined') {
      const all = window.STEMDictionary.getWordsByLetter('B'); 
      for (let w of all) {
         if (options.length < 4 && !options.includes(w.word)) {
            options.push(w.word);
         }
      }
    }

    while(options.length < 4) {
      options.push("Anomaly");
    }

    options = this.shuffle(options);

    if (domCache.optionsContainer) {
      domCache.optionsContainer.innerHTML = '';
      options.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.textContent = opt;
        btn.onclick = () => this.handleSelection(btn, opt === currentWord);
        domCache.optionsContainer.appendChild(btn);
      });
    }
  },

  handleSelection(btn, isCorrect) {
    if (this.state.answerLocked) return;
    this.state.answerLocked = true;

    const allBtns = document.querySelectorAll('.option-btn');
    allBtns.forEach(b => b.style.pointerEvents = 'none');

    const { domCache, testSequence, testIndex } = this.state;

    if (isCorrect) {
      btn.classList.add('correct');
      if (domCache.feedbackEl) {
        domCache.feedbackEl.textContent = 'Precise.';
        domCache.feedbackEl.className = 'feedback success';
      }
      if (typeof AudioManager !== 'undefined') AudioManager.play('success');
      
      this.state.stageScore += 5;
      this.updateScoreboard(5, btn);
    } else {
      btn.classList.add('wrong');
      if (domCache.feedbackEl) {
        domCache.feedbackEl.textContent = 'Incorrect word.';
        domCache.feedbackEl.className = 'feedback error';
      }
      if (typeof AudioManager !== 'undefined') AudioManager.play('error');

      allBtns.forEach(b => {
        if (b.textContent === testSequence[testIndex]) {
          b.classList.add('correct');
        }
      });
    }

    if (domCache.nextBtn) {
      domCache.nextBtn.style.display = 'block';
      domCache.nextBtn.textContent = (testIndex < testSequence.length - 1) ? 'Next Word' : 'Complete Stage';
    }
  },

  updateScoreboard(amount, refElement) {
    this.state.gameData.score = (this.state.gameData.score || 0) + amount;
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score;
    }

    const rect = refElement.getBoundingClientRect();
    const floater = document.createElement('div');
    floater.className = 'floating-point';
    floater.textContent = `+${amount}`;
    floater.style.left = `${rect.left + rect.width / 2}px`;
    floater.style.top = `${rect.top - 20}px`;
    document.body.appendChild(floater);
    setTimeout(() => floater.remove(), 1000);
  },

  finishStage() {
    sharedState.save(this.state.gameData);
    if (typeof AudioManager !== 'undefined') AudioManager.play('success');
    
    sharedState.showStageScoreThen('07_stage5', 'Stage 5: Definition Selection', this.state.stageScore, () => {
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('09_stage7_meaning_fillin.html');
      else window.location.href = '09_stage7_meaning_fillin.html';
    });
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => Stage5Controller.init());
} else {
  Stage5Controller.init();
}
