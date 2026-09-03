// =====================================================================
// FILE: 05_stage3_flash_recall.js (The Flash Memorization)
// =====================================================================

const Stage3Controller = {
  state: {
    gameData: null,
    domCache: {},
    sequence: [],
    currentIndex: 0,
    answerLocked: false,
    flashStageScore: 0
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
      introContainer: document.getElementById('intro-container'),
      quizContainer: document.getElementById('quiz-container'),
      startBtn: document.getElementById('start-btn'),
      flashWordEl: document.getElementById('flash-word'),
      hintEl: document.getElementById('flash-hint'),
      inputEl: document.getElementById('typed-word-input'),
      feedbackEl: document.getElementById('flash-feedback'),
      submitBtn: document.getElementById('submit-btn'),
      nextBtn: document.getElementById('next-btn'),
      progressEl: document.getElementById('quiz-progress'),
      voiceToggleBtn: document.getElementById('voice-toggle-btn'),
      voiceToggleIcon: document.getElementById('voice-toggle-icon'),
      voiceToggleLabel: document.getElementById('voice-toggle-label'),
      replayVoiceBtn: document.getElementById('replay-voice-btn')
    };
  },

  renderInitialUI() {
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score || 0;
    }
    this.updateVoiceToggleUI();
  },

  updateVoiceToggleUI() {
    const { domCache } = this.state;
    if (!domCache.voiceToggleBtn || typeof VoiceManager === 'undefined') return;
    const enabled = VoiceManager.isEnabled();
    if (enabled) {
      domCache.voiceToggleBtn.classList.remove('muted');
      if (domCache.voiceToggleIcon) domCache.voiceToggleIcon.textContent = '🔊';
      if (domCache.voiceToggleLabel) domCache.voiceToggleLabel.textContent = 'Voice: ON';
    } else {
      domCache.voiceToggleBtn.classList.add('muted');
      if (domCache.voiceToggleIcon) domCache.voiceToggleIcon.textContent = '🔇';
      if (domCache.voiceToggleLabel) domCache.voiceToggleLabel.textContent = 'Voice: OFF';
    }
  },

  attachListeners() {
    const { domCache } = this.state;

    if (domCache.startBtn) {
      domCache.startBtn.addEventListener('click', () => this.startFlashRecall());
    }

    if (domCache.voiceToggleBtn) {
      domCache.voiceToggleBtn.addEventListener('click', () => {
        if (typeof VoiceManager !== 'undefined') {
          VoiceManager.toggle();
          this.updateVoiceToggleUI();
        }
      });
    }

    if (domCache.replayVoiceBtn) {
      domCache.replayVoiceBtn.addEventListener('click', () => {
        const { sequence, currentIndex } = this.state;
        const currentWord = sequence[currentIndex];
        if (currentWord && typeof VoiceManager !== 'undefined') {
          VoiceManager.speak(currentWord, { force: true });
        }
      });
    }

    if (domCache.submitBtn) {
      domCache.submitBtn.addEventListener('click', () => this.submitFlashRow());
    }

    if (domCache.inputEl) {
      domCache.inputEl.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          if (!this.state.answerLocked) this.submitFlashRow();
          else if (domCache.nextBtn) domCache.nextBtn.click();
        }
      });
    }

    if (domCache.nextBtn) {
      domCache.nextBtn.addEventListener('click', () => this.advanceFlashRow());
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

  startFlashRecall() {
    const { domCache, gameData } = this.state;
    this.state.sequence = this.shuffle([...gameData.selectedWords]);
    this.state.currentIndex = 0;

    if (domCache.introContainer) domCache.introContainer.style.display = 'none';
    if (domCache.quizContainer) domCache.quizContainer.style.display = 'block';

    this.beginFlashRow();
  },

  beginFlashRow() {
    const { domCache, sequence, currentIndex } = this.state;
    this.state.answerLocked = false;

    if (domCache.inputEl) {
      domCache.inputEl.value = '';
      domCache.inputEl.disabled = true;
      domCache.inputEl.classList.remove('correct', 'wrong');
    }

    if (domCache.submitBtn) domCache.submitBtn.style.display = 'none';
    if (domCache.nextBtn) domCache.nextBtn.style.display = 'none';

    if (domCache.feedbackEl) {
      domCache.feedbackEl.textContent = '';
      domCache.feedbackEl.className = 'feedback';
    }

    if (domCache.progressEl) domCache.progressEl.textContent = `${currentIndex + 1} / ${sequence.length}`;

    const currentWord = sequence[currentIndex];
    if (domCache.flashWordEl) {
      // Dynamic font size adjustment based on word length to prevent overlap/overflow
      if (currentWord.length > 10) {
        domCache.flashWordEl.style.fontSize = '1.8rem';
        domCache.flashWordEl.style.letterSpacing = '1px';
      } else if (currentWord.length >= 7) {
        domCache.flashWordEl.style.fontSize = '2.2rem';
        domCache.flashWordEl.style.letterSpacing = '2px';
      } else {
        domCache.flashWordEl.style.fontSize = ''; // Reset to CSS default (3rem)
        domCache.flashWordEl.style.letterSpacing = ''; // Reset to CSS default (4px)
      }
      domCache.flashWordEl.textContent = currentWord;
      domCache.flashWordEl.classList.remove('hidden');
    }
    if (domCache.replayVoiceBtn) {
      domCache.replayVoiceBtn.style.display = 'flex';
    }
    if (domCache.hintEl) domCache.hintEl.textContent = 'Memorize it...';

    // Automatic voice reading as the word flashes!
    if (typeof VoiceManager !== 'undefined') {
      VoiceManager.speak(currentWord);
    }

    const baseFlashMs = 2000;
    const wordLengthExtra = Math.max(0, currentWord.length - 6) * 200;
    const totalFlashMs = baseFlashMs + wordLengthExtra;

    setTimeout(() => {
      if (domCache.flashWordEl) domCache.flashWordEl.classList.add('hidden');
      if (domCache.hintEl) domCache.hintEl.textContent = 'Now type the word you saw.';

      if (domCache.inputEl) {
        domCache.inputEl.disabled = false;
        domCache.inputEl.focus();
      }
      if (domCache.submitBtn) domCache.submitBtn.style.display = 'block';
    }, totalFlashMs);
  },

  submitFlashRow() {
    if (this.state.answerLocked) return;

    const { domCache, sequence, currentIndex } = this.state;
    const typed = domCache.inputEl ? domCache.inputEl.value.trim().toLowerCase() : '';
    if (!typed) return;

    this.state.answerLocked = true;
    if (domCache.inputEl) domCache.inputEl.disabled = true;
    if (domCache.submitBtn) domCache.submitBtn.style.display = 'none';

    const correct = sequence[currentIndex].toLowerCase();

    if (typed === correct) {
      if (domCache.inputEl) domCache.inputEl.classList.add('correct');
      this.triggerFlashFeedback('Correct.', 'success');
      this.rewardFlashPoints(10);
    } else {
      if (domCache.inputEl) domCache.inputEl.classList.add('wrong');
      this.triggerFlashFeedback(`Incorrect. It was "${correct.toUpperCase()}".`, 'error');
    }

    if (domCache.nextBtn) domCache.nextBtn.style.display = 'block';
  },

  advanceFlashRow() {
    if (typeof VoiceManager !== 'undefined') VoiceManager.stop();
    this.state.currentIndex++;
    if (this.state.currentIndex < this.state.sequence.length) {
      this.beginFlashRow();
    } else {
      this.finishFlashRecall();
    }
  },

  triggerFlashFeedback(message, type) {
    if (this.state.domCache.feedbackEl) {
      this.state.domCache.feedbackEl.textContent = message;
      this.state.domCache.feedbackEl.className = `feedback ${type}`;
    }
    if (typeof AudioManager !== 'undefined') AudioManager.play(type);
  },

  rewardFlashPoints(amount) {
    this.state.flashStageScore += amount;
    this.state.gameData.score = (this.state.gameData.score || 0) + amount;
    
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score;
    }
  },

  finishFlashRecall() {
    if (typeof VoiceManager !== 'undefined') VoiceManager.stop();
    sharedState.save(this.state.gameData);
    if (typeof AudioManager !== 'undefined') AudioManager.play('success');

    sharedState.showStageScoreThen('stage3', 'Stage 3: Flash Recall', this.state.flashStageScore, () => {
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('06_stage4_self_recall.html');
      else window.location.href = '06_stage4_self_recall.html';
    });
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => Stage3Controller.init());
} else {
  Stage3Controller.init();
}
