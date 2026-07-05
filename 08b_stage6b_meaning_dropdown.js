// =====================================================================
// FILE: 08b_stage6b_meaning_dropdown.js (The Missing Word Trick Test)
// =====================================================================

const Stage6bController = {
  state: {
    gameData: null,
    domCache: {},
    testSequence: [],
    testIndex: 0,
    stageScore: 0,
    activeDropdown: null
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
      testContainer: document.getElementById('test-container'),
      scoreboard: document.getElementById('scoreboard'),
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

    if (domCache.submitBtn) {
      domCache.submitBtn.addEventListener('click', () => this.processValidation());
    }

    if (domCache.skipBtn) {
      domCache.skipBtn.addEventListener('click', () => this.skipWord());
    }

    // Close open dropdowns when clicking outside
    document.addEventListener('click', (e) => {
      if (this.state.activeDropdown && !e.target.closest('.custom-dropdown-container')) {
        this.closeActiveDropdown();
      }
    });

    // Developer Hack
    document.addEventListener('keydown', (e) => {
      if (e.key.toLowerCase() === 'p' && e.altKey) {
        e.preventDefault();
        if (domCache.testContainer && domCache.testContainer.style.display !== 'none') {
          const dropdowns = document.querySelectorAll('.custom-dropdown-container');
          dropdowns.forEach(dd => {
            const correctAns = dd.dataset.ans;
            const btnText = dd.querySelector('.dropdown-text');
            btnText.textContent = correctAns;
            dd.dataset.selected = correctAns;
            dd.querySelector('.custom-dropdown-btn').classList.add('filled');
          });
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

  closeActiveDropdown() {
    if (this.state.activeDropdown) {
      this.state.activeDropdown.classList.remove('open');
      this.state.activeDropdown = null;
    }
  },

  toggleDropdown(container) {
    if (this.state.activeDropdown === container) {
      this.closeActiveDropdown();
    } else {
      this.closeActiveDropdown();
      container.classList.add('open');
      this.state.activeDropdown = container;
    }
  },

  selectOption(container, optionText) {
    const btn = container.querySelector('.custom-dropdown-btn');
    const textSpan = btn.querySelector('.dropdown-text');
    textSpan.textContent = optionText;
    btn.classList.add('filled');
    container.dataset.selected = optionText;
    this.closeActiveDropdown();
  },

  renderTestCurrent() {
    const { domCache, testSequence, testIndex, gameData } = this.state;

    if (testIndex >= testSequence.length) return;

    const currentWord = testSequence[testIndex];
    if (domCache.testWord) domCache.testWord.textContent = currentWord;
    if (domCache.testProgress) domCache.testProgress.textContent = `${testIndex + 1}/${testSequence.length}`;

    let rawMeaning = gameData.meanings[currentWord] || "";
    let plainMeaning = String(rawMeaning).replace(/<\/?[^>]+(>|$)/g, "");

    let stopWords = ["that", "with", "this", "have", "they", "their", "them", "what", "which", "when", "where", "who", "whom", "whose", "why", "how", "some", "such", "than", "very", "will", "just", "should", "also", "into", "only", "about", "many", "then", "would", "like", "these", "because", "could", "been", "much", "even", "from", "were", "there", "used", "part", "made"];

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
      // Pick 1 to 3 words randomly based on how many valid ones exist
      let numToPick = Math.min(validIndices.length, Math.floor(Math.random() * 3) + 1);
      
      // Shuffle validIndices to pick random
      let shuffled = [...validIndices].sort(() => 0.5 - Math.random());
      chosenIndices = shuffled.slice(0, numToPick).sort((a,b) => a - b);
    }
    validIndices = chosenIndices;

    function escapeHTML(str) {
      return str.replace(/[&<>'"]/g, tag => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
      }[tag] || tag));
    }

    // Prepare trick words pool globally from STEMDictionary
    let globalTricks = [];
    if (typeof window.STEMDictionary !== 'undefined') {
      let attempts = 0;
      while (globalTricks.length < 20 && attempts < 100) {
        const randLetter = window.STEMDictionary.getRandomLetter();
        const words = window.STEMDictionary.getWordsByLetter(randLetter);
        if (words && words.length > 0) {
          const wObj = words[Math.floor(Math.random() * words.length)];
          const parts = wObj.definition.split(/(\b[\w'-]+\b)/).filter(t => t.length > 4 && /^[a-zA-Z]+$/.test(t) && !stopWords.includes(t.toLowerCase()));
          if (parts.length > 0) {
            let trk = parts[Math.floor(Math.random() * parts.length)].toLowerCase();
            if (!globalTricks.includes(trk)) globalTricks.push(trk);
          }
        }
        attempts++;
      }
    }
    
    let defaultTricks = ["process", "system", "cell", "energy", "force", "matter", "reaction", "structure", "function", "development"];
    if (globalTricks.length < 10) globalTricks = [...globalTricks, ...defaultTricks];

    // Build HTML
    if (domCache.testMeaningContainer) domCache.testMeaningContainer.innerHTML = '';
    
    tokens.forEach((t, i) => {
      if (validIndices.includes(i)) {
        const correctAns = t.toLowerCase();
        
        // Pick 3 trick words for this dropdown
        let trickOptions = [];
        let pool = [...globalTricks].sort(() => 0.5 - Math.random());
        for (let w of pool) {
          if (w !== correctAns && trickOptions.length < 3) {
            trickOptions.push(w);
          }
        }
        
        let allOptions = [correctAns, ...trickOptions].sort(() => 0.5 - Math.random());
        
        // Build Custom Dropdown UI
        const container = document.createElement('div');
        container.className = 'custom-dropdown-container';
        container.dataset.ans = correctAns;
        container.dataset.selected = "";
        
        const btn = document.createElement('div');
        btn.className = 'custom-dropdown-btn';
        btn.innerHTML = `<span class="dropdown-text">______</span><span class="dropdown-arrow">▼</span>`;
        btn.onclick = (e) => {
          e.stopPropagation();
          if (btn.classList.contains('correct') || btn.disabled) return;
          this.toggleDropdown(container);
        };
        
        const menu = document.createElement('div');
        menu.className = 'custom-dropdown-menu';
        
        allOptions.forEach(opt => {
          const item = document.createElement('div');
          item.className = 'custom-option';
          item.textContent = opt;
          item.onclick = (e) => {
            e.stopPropagation();
            this.selectOption(container, opt);
          };
          menu.appendChild(item);
        });
        
        container.appendChild(btn);
        container.appendChild(menu);
        
        domCache.testMeaningContainer.appendChild(container);
      } else {
        const textNode = document.createTextNode(t);
        domCache.testMeaningContainer.appendChild(textNode);
      }
    });

    if (domCache.submitBtn) {
      domCache.submitBtn.textContent = "Submit Findings";
      domCache.submitBtn.disabled = false;
    }
    if (domCache.skipBtn) domCache.skipBtn.disabled = false;

    if (domCache.testFeedback) {
      domCache.testFeedback.textContent = '';
      domCache.testFeedback.className = 'feedback';
    }
  },

  processValidation() {
    const { domCache } = this.state;
    this.closeActiveDropdown();

    if (domCache.submitBtn && domCache.submitBtn.textContent !== "Submit Findings") {
      this.nextWord();
      return;
    }

    const dropdowns = document.querySelectorAll('.custom-dropdown-container');
    let allCorrect = true;
    let hasEmpty = false;

    dropdowns.forEach(dd => {
      const userVal = dd.dataset.selected.toLowerCase();
      const correctVal = dd.dataset.ans.toLowerCase();
      const btn = dd.querySelector('.custom-dropdown-btn');
      
      btn.classList.remove('wrong', 'correct');

      if (userVal === '') hasEmpty = true;

      if (userVal === correctVal) {
        btn.classList.add('correct');
      } else if (userVal !== '') {
        btn.classList.add('wrong');
        allCorrect = false;
      } else {
        allCorrect = false;
      }
    });

    if (hasEmpty && !allCorrect) {
      this.triggerFeedback("Please select a word for all blanks.", 'error');
      return;
    }

    if (allCorrect) {
      this.triggerFeedback("Correct!", 'success');
      const pts = 10;
      this.state.stageScore += pts;
      this.updateScoreboard(pts);

      if (domCache.skipBtn) domCache.skipBtn.disabled = true;
      if (domCache.submitBtn) domCache.submitBtn.textContent = (this.state.testIndex < this.state.testSequence.length - 1) ? "Next Word" : "Proceed";
    } else {
      this.triggerFeedback("Incorrect interpretation. Try again or skip.", 'error');
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
    this.closeActiveDropdown();
    const dropdowns = document.querySelectorAll('.custom-dropdown-container');
    dropdowns.forEach(dd => {
      const correctVal = dd.dataset.ans;
      const btn = dd.querySelector('.custom-dropdown-btn');
      const textSpan = btn.querySelector('.dropdown-text');
      textSpan.textContent = correctVal;
      btn.classList.add('wrong', 'filled');
      btn.style.pointerEvents = 'none'; // Disable clicks
    });

    this.triggerFeedback("", 'error');

    const { domCache } = this.state;
    if (domCache.skipBtn) domCache.skipBtn.disabled = true;
    if (domCache.submitBtn) domCache.submitBtn.textContent = (this.state.testIndex < this.state.testSequence.length - 1) ? "Next Definition" : "Proceed";
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

    sharedState.showStageScoreThen('stage6b', 'Stage 6b: Missing Word Analysis', this.state.stageScore, () => {
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('09_stage7_meaning_fillin.html');
      else window.location.href = '09_stage7_meaning_fillin.html';
    });
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => Stage6bController.init());
} else {
  Stage6bController.init();
}
