// =====================================================================
// FILE: 08_stage6_meaning_fillin.js (The Missing Word Definition Test)
// =====================================================================
// Imagine you found an ancient scroll with a word's meaning written on it, 
// but moths ate holes through some of the words! 
// This file reads the word's meaning, picks a few words to turn into blank text boxes,
// and you have to fill in the missing pieces correctly like a puzzle detective!

const Stage6Controller = {
  state: {
    gameData: null,
    domCache: {},
    testSequence: [],
    testIndex: 0,
    stageScore: 0,
    globalTimerInt: null
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

    this.bootstrapStage();
  },

  cacheDOM() {
    this.state.domCache = {
      scoreEl: document.getElementById('current-score'),
      loadingContainer: document.getElementById('loading-container'),
      revisionContainer: document.getElementById('revision-container'),
      testContainer: document.getElementById('test-container'),
      scoreboard: document.getElementById('scoreboard'),
      revList: document.getElementById('rev-list'),
      revTimer: document.getElementById('rev-timer'),
      startTestBtn: document.getElementById('start-test-btn'),
      testWord: document.getElementById('test-word'),
      testProgress: document.getElementById('test-progress'),
      testMeaningContainer: document.getElementById('test-meaning-container'),
      submitBtn: document.getElementById('submit-btn'),
      skipBtn: document.getElementById('skip-btn'),
      testFeedback: document.getElementById('test-feedback')
    };
  },

  renderInitialUI() {
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score || 0;
    }
  },

  attachListeners() {
    const { domCache } = this.state;

    if (domCache.startTestBtn) {
      domCache.startTestBtn.addEventListener('click', () => {
        clearInterval(this.state.globalTimerInt);
        this.endRevisionPhase();
      });
    }

    if (domCache.submitBtn) {
      domCache.submitBtn.addEventListener('click', () => this.processValidation());
    }

    if (domCache.skipBtn) {
      domCache.skipBtn.addEventListener('click', () => this.skipWord());
    }

    // Developer Hack
    document.addEventListener('keydown', (e) => {
      if (e.key.toLowerCase() === 'p' && e.altKey) {
        e.preventDefault();
        if (domCache.testContainer && domCache.testContainer.style.display !== 'none') {
          const inputs = document.querySelectorAll('.meaning-input');
          inputs.forEach(inp => inp.value = inp.dataset.ans);
          if (domCache.submitBtn) domCache.submitBtn.click();
        }
      }
    });
  },

  bootstrapStage() {
    const { gameData, domCache } = this.state;

    if (!gameData.meanings) gameData.meanings = {};
    for (let w of gameData.selectedWords) {
      if (!gameData.meanings[w]) {
        gameData.meanings[w] = typeof DictionaryLogic !== 'undefined' ? DictionaryLogic.fetchMeaning(w) : "Definition unavailable";
      }
    }
    sharedState.save(gameData);

    this.state.testSequence = [...gameData.selectedWords].sort(() => 0.5 - Math.random());

    if (domCache.loadingContainer) domCache.loadingContainer.style.display = 'none';

    this.startTestPhase();
  },

  startTestPhase() {
    if (this.state.domCache.scoreboard) {
      this.state.domCache.scoreboard.style.display = 'block';
    }
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score || 0;
    }

    if (this.state.domCache.testContainer) {
      this.state.domCache.testContainer.style.display = 'block';
    }
    this.renderTestCurrent();
  },

  renderTestCurrent() {
    // This is where we punch holes in the scroll!
    // We look at the long meaning of the word, pick out some nice solid words, 
    // and replace them with empty text boxes for you to type in later.
    const { domCache, testSequence, testIndex, gameData } = this.state;

    if (testIndex >= testSequence.length) return;

    const currentWord = testSequence[testIndex];
    if (domCache.testWord) domCache.testWord.textContent = currentWord;
    if (domCache.testProgress) domCache.testProgress.textContent = `${testIndex + 1}/${testSequence.length}`;

    let rawMeaning = gameData.meanings[currentWord] || "";
    let plainMeaning = String(rawMeaning).replace(/<\/?[^>]+(>|$)/g, "");

    let stopWords = ["that", "with", "this", "have", "they", "their", "them", "what", "which", "when", "where", "who", "whom", "whose", "why", "how", "some", "such", "than", "very", "will", "just", "should", "also", "into", "only", "about", "many", "then", "would", "like", "these", "because", "could", "been", "much", "even", "from", "were", "there"];

    let tokens = plainMeaning.split(/(\b[\w'-]+\b)/);
    let validIndices = [];
    
    tokens.forEach((t, i) => {
      if (t.length > 3 && /^[a-zA-Z]+$/.test(t) && t.toLowerCase() !== currentWord.toLowerCase()) {
        if (!stopWords.includes(t.toLowerCase())) {
          validIndices.push(i);
        }
      }
    });

    if (validIndices.length === 0) {
      tokens.forEach((t, i) => {
        if (t.length > 3 && /^[a-zA-Z]+$/.test(t) && t.toLowerCase() !== currentWord.toLowerCase()) {
          validIndices.push(i);
        }
      });
    }

    let chosenIndices = [];
    if (validIndices.length > 0) {
      let longestIndex = validIndices[0];
      for (let i = 1; i < validIndices.length; i++) {
        if (tokens[validIndices[i]].length > tokens[longestIndex].length) {
          longestIndex = validIndices[i];
        } else if (tokens[validIndices[i]].length === tokens[longestIndex].length && Math.random() > 0.5) {
          longestIndex = validIndices[i];
        }
      }
      chosenIndices.push(longestIndex);
    }
    validIndices = chosenIndices;

    function escapeHTML(str) {
      return str.replace(/[&<>'"]/g, tag => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        "'": '&#39;',
        '"': '&quot;'
      }[tag] || tag));
    }

    let html = '';
    tokens.forEach((t, i) => {
      if (validIndices.includes(i)) {
        html += `<input type="text" class="meaning-input" data-ans="${escapeHTML(t.toLowerCase())}" autocomplete="off" style="width: ${Math.max(6, t.length * 1.2)}em;">`;
      } else {
        html += escapeHTML(t);
      }
    });

    if (domCache.testMeaningContainer) domCache.testMeaningContainer.innerHTML = html;

    if (domCache.submitBtn) {
      domCache.submitBtn.textContent = "Submit Findings";
      domCache.submitBtn.disabled = false;
    }
    if (domCache.skipBtn) domCache.skipBtn.disabled = false;

    if (domCache.testFeedback) {
      domCache.testFeedback.textContent = '';
      domCache.testFeedback.className = 'feedback';
    }

    const firstInput = document.querySelector('.meaning-input');
    if (firstInput) firstInput.focus();
  },

  processValidation() {
    // Here we check your homework! We look at every single blank you filled in,
    // and if you mapped them perfectly right, you get a 'Masterful interpretation!' sticker.
    // Otherwise, we tell you to review your errors and try again.
    const { domCache } = this.state;

    if (domCache.submitBtn && domCache.submitBtn.textContent === "Next Definition") {
      this.nextWord();
      return;
    }

    const inputs = document.querySelectorAll('.meaning-input');
    let allCorrect = true;
    let hasEmpty = false;

    inputs.forEach(inp => {
      const userVal = inp.value.trim().toLowerCase();
      const correctVal = inp.dataset.ans.toLowerCase();
      inp.classList.remove('wrong', 'correct');

      if (userVal === '') hasEmpty = true;

      if (userVal === correctVal) {
        inp.classList.add('correct');
        inp.disabled = true;
      } else if (userVal !== '') {
        inp.classList.add('wrong');
        allCorrect = false;
      } else {
        allCorrect = false;
      }
    });

    if (hasEmpty && !allCorrect) {
      this.triggerFeedback("Please fill in all blanks.", 'error');
      return;
    }

    if (allCorrect) {
      this.triggerFeedback("Excellent", 'success');
      this.state.stageScore += 5;
      this.updateScoreboard(5);

      if (domCache.skipBtn) domCache.skipBtn.disabled = true;
      if (domCache.submitBtn) domCache.submitBtn.textContent = "Next Definition";
    } else {
      this.triggerFeedback("Wrong. click skip/forfeit for answer", 'error');
    }
  },

  triggerFeedback(message, type) {
    if (this.state.domCache.testFeedback) {
      this.state.domCache.testFeedback.textContent = message;
      this.state.domCache.testFeedback.className = `feedback ${type}`;
    }
    if (typeof AudioManager !== 'undefined') AudioManager.play(type);
  },

  skipWord() {
    const inputs = document.querySelectorAll('.meaning-input');
    inputs.forEach(inp => {
      inp.value = inp.dataset.ans;
      inp.classList.add('wrong');
      inp.disabled = true;
    });

    this.triggerFeedback("", 'error');

    const { domCache } = this.state;
    if (domCache.skipBtn) domCache.skipBtn.disabled = true;
    if (domCache.submitBtn) domCache.submitBtn.textContent = "Next Definition";
  },

  nextWord() {
    this.state.testIndex++;
    if (this.state.testIndex < this.state.testSequence.length) {
      this.renderTestCurrent();
    } else {
      this.finishGame();
    }
  },

  updateScoreboard(amount) {
    this.state.gameData.score = (this.state.gameData.score || 0) + amount;
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score;
    }

    const btn = this.state.domCache.submitBtn;
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
    if (typeof AudioManager !== 'undefined') AudioManager.play('success');

    sharedState.showStageScoreThen('stage6', 'Stage 6: Filling-In Gaps In Definitions', this.state.stageScore, () => {
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('10_stage8_intro.html');
      else window.location.href = '10_stage8_intro.html';
    });
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => Stage6Controller.init());
} else {
  Stage6Controller.init();
}
