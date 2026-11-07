// =====================================================================
// FILE: 09_stage7_meaning_fillin.js
// Architect: Desmond Mifetu & Co-Chief Developer
// Design: Pixel-perfect match to Osmosis reference screenshot
// =====================================================================

const Stage7Controller = {

  state: {
    gameData:       null,
    domCache:       {},
    testSequence:   [],
    testIndex:      0,
    sentences:      [],
    sentenceIndex:  0,
    currentBlank:   null,
    selectedOption: null,
    isAnswered:     false,
    stageScore:     0,
    isAdvancing:    false
  },

  // Words we never blank out — they're too generic to test
  STOP_WORDS: new Set([
    'that','with','this','have','they','their','them','what','which',
    'when','where','who','whom','whose','why','how','some','such',
    'than','very','will','just','should','also','into','only','about',
    'many','then','would','like','these','because','could','been',
    'much','even','from','were','there','used','part','made','each',
    'other','another','called','known','forms','type','types','form',
    'most','more','both','between','during','through','under','after',
    'before','while','since','still','often','found','using','make'
  ]),

  // ── Bootstrap ───────────────────────────────────────────────────

  init() {
    if (typeof initModal === 'function') initModal();
    sharedState.startTimer();
    this.state.gameData = sharedState.load();
    sharedState.updateTimerUI('timer-display');

    if (!this.state.gameData.selectedWords || this.state.gameData.selectedWords.length === 0) {
      this.navigate('index.html');
      return;
    }

    this.cacheDOM();
    this.renderInitialScore();
    this.attachListeners();
    this.bootstrapStage();
  },

  cacheDOM() {
    this.state.domCache = {
      scoreEl:       document.getElementById('current-score'),
      testContainer: document.getElementById('test-container'),
      testWord:      document.getElementById('test-word'),
      testProgress:  document.getElementById('test-progress'),
      sentenceCard:  document.getElementById('sentence-card'),
      optionsGrid:   document.getElementById('options-grid'),
      submitBtn:     document.getElementById('submit-btn'),
      skipBtn:       document.getElementById('skip-btn'),
      feedback:      document.getElementById('test-feedback')
    };
  },

  renderInitialScore() {
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score || 0;
    }
  },

  attachListeners() {
    const { domCache } = this.state;

    domCache.submitBtn?.addEventListener('click', e => {
      e.preventDefault();
      this.onSubmitClick();
    });

    domCache.skipBtn?.addEventListener('click', e => {
      e.preventDefault();
      this.skipSentence();
    });

    // Dev shortcut: Alt+P = auto-pick correct answer
    document.addEventListener('keydown', e => {
      if (e.key.toLowerCase() === 'p' && e.altKey) {
        e.preventDefault();
        if (this.state.isAnswered) {
          this.advance();
        } else if (this.state.currentBlank) {
          const target = this.state.currentBlank.expected.toLowerCase();
          document.querySelectorAll('.s7-option-btn').forEach(btn => {
            if (btn.textContent.trim().toLowerCase() === target) btn.click();
          });
          setTimeout(() => domCache.submitBtn?.click(), 80);
        }
      }
    });
  },

  bootstrapStage() {
    const { gameData, domCache } = this.state;

    // Ensure meanings are loaded for every selected word
    if (!gameData.meanings) gameData.meanings = {};
    for (const w of gameData.selectedWords) {
      if (!gameData.meanings[w]) {
        gameData.meanings[w] =
          typeof DictionaryLogic !== 'undefined'
            ? DictionaryLogic.fetchMeaning(w)
            : (typeof STEMDictionary !== 'undefined'
                ? (STEMDictionary.getMeaning ? STEMDictionary.getMeaning(w) : 'Definition unavailable')
                : 'Definition unavailable');
      }
    }
    sharedState.save(gameData);

    // Shuffle word order for variety
    this.state.testSequence = [...gameData.selectedWords].sort(() => 0.5 - Math.random());
    this.state.testIndex    = 0;

    if (domCache.testContainer) {
      domCache.testContainer.style.display = 'flex';
    }

    this.loadWordTest();
  },

  // ── Word / Sentence Loading ──────────────────────────────────────

  loadWordTest() {
    const { testSequence, testIndex, gameData } = this.state;

    if (testIndex >= testSequence.length) {
      this.finishStage();
      return;
    }

    const word        = testSequence[testIndex];
    const rawMeaning  = gameData.meanings[word] || '';
    this.state.sentences     = this.segmentDefinition(rawMeaning);
    this.state.sentenceIndex = 0;

    this.renderSentence();
  },

  /**
   * Splits a definition into clean scientific sentences.
   * Protects abbreviations, decimals, and chemical formulas.
   * Max 4 sentences per word to keep the pace snappy.
   */
  segmentDefinition(text) {
    if (!text) return [];
    let clean = String(text)
      .replace(/<\/?[^>]+(>|$)/g, ' ')   // strip HTML tags
      .replace(/^\s*\d+\.\s*/, '')         // strip leading "1."
      .replace(/\s+/g, ' ')
      .trim();

    // Split at sentence boundaries — only when next char is uppercase/digit
    const parts = clean.split(/(?<=[.!?])\s+(?=[A-Z0-9])/);
    const sentences = parts
      .map(p => p.replace(/\s+\d+\.?$/, '').trim())
      .filter(p => p.length >= 15);

    // Fallback: split on semicolons
    if (sentences.length === 0) {
      clean.split(/;\s+/).forEach(sp => {
        if (sp.trim().length >= 15) sentences.push(sp.trim());
      });
    }

    // Last fallback: use entire definition as one sentence
    if (sentences.length === 0 && clean.length > 0) sentences.push(clean);

    return sentences.slice(0, 4);
  },

  // ── Rendering ───────────────────────────────────────────────────

  /**
   * Renders the hero sentence card + 2×2 option grid.
   * Picks the longest non-stop word in the sentence as the blank.
   */
  renderSentence() {
    const { domCache, sentences, sentenceIndex, testSequence, testIndex } = this.state;
    const currentWord = testSequence[testIndex];

    // Advance to next word if we've exhausted all sentences for this one
    if (sentenceIndex >= sentences.length) {
      this.state.testIndex++;
      this.loadWordTest();
      return;
    }

    this.state.isAnswered    = false;
    this.state.selectedOption = null;

    const sentence = sentences[sentenceIndex];

    // Tokenise — keeping non-word chars (spaces, commas, etc.) as separate tokens
    const tokens     = sentence.split(/(\b[a-zA-Z]{3,}\b)/);
    const candidates = [];

    tokens.forEach((t, i) => {
      if (/^[a-zA-Z]{4,}$/.test(t)) {
        const lower = t.toLowerCase();
        if (!this.STOP_WORDS.has(lower) && lower !== currentWord.toLowerCase()) {
          candidates.push({ index: i, word: t, length: t.length });
        }
      }
    });

    // If stop-word filter leaves nothing, allow any long word
    if (candidates.length === 0) {
      tokens.forEach((t, i) => {
        if (/^[a-zA-Z]{4,}$/.test(t) && t.toLowerCase() !== currentWord.toLowerCase()) {
          candidates.push({ index: i, word: t, length: t.length });
        }
      });
    }

    // Emergency fallback
    if (candidates.length === 0) {
      candidates.push({ index: 1, word: tokens[1] || 'scientific', length: 10 });
    }

    // Blank out the longest / most significant word
    candidates.sort((a, b) => b.length - a.length);
    const chosen     = candidates[0];
    const targetWord = chosen.word;

    // ── Generate 4 same-length / same-POS options ──
    let options = [];
    if (typeof window.DistractorEngine !== 'undefined') {
      options = window.DistractorEngine.getOptionsWithAnswer(targetWord, 4, {
        exclude:      [currentWord],
        preserveCase: false
      });
    } else {
      // Graceful fallback when engine not loaded
      options = [targetWord, 'system', 'element', 'process'].sort(() => 0.5 - Math.random());
    }

    this.state.currentBlank = { expected: targetWord, options };

    // ── Build sentence HTML with inline puzzle slot ──
    let cardHtml = '';
    tokens.forEach((t, i) => {
      if (i === chosen.index) {
        cardHtml += `<span class="s7-slot" id="active-blank" data-expected="${this.esc(targetWord.toLowerCase())}">` +
                    `<span class="slot-icon">🧩</span> <span class="slot-text">Select word</span></span>`;
      } else {
        cardHtml += this.esc(t);
      }
    });

    if (domCache.sentenceCard) domCache.sentenceCard.innerHTML = cardHtml;

    // ── Build 2×2 option buttons ──
    if (domCache.optionsGrid) {
      domCache.optionsGrid.innerHTML = '';
      options.forEach(opt => {
        const btn = document.createElement('button');
        btn.type      = 'button';
        btn.className = 's7-option-btn';
        btn.textContent = opt.toLowerCase();
        btn.addEventListener('click', e => {
          e.preventDefault();
          this.onOptionClick(opt.toLowerCase(), btn);
        });
        domCache.optionsGrid.appendChild(btn);
      });
    }

    // ── Update subtle meta labels ──
    if (domCache.testWord)     domCache.testWord.textContent     = currentWord.toUpperCase();
    if (domCache.testProgress) domCache.testProgress.textContent = `Sentence ${sentenceIndex + 1} of ${sentences.length}`;

    // ── Reset action bar ──
    this.resetActionBar();
  },

  resetActionBar() {
    const { submitBtn, skipBtn, feedback } = this.state.domCache;
    if (submitBtn) {
      submitBtn.textContent = 'Submit Findings';
      submitBtn.className   = 's7-btn s7-btn-submit';
      submitBtn.disabled    = false;
    }
    if (skipBtn) {
      skipBtn.disabled    = false;
      skipBtn.style.display = '';
    }
    if (feedback) {
      feedback.textContent = '';
      feedback.className   = 's7-feedback';
    }
  },

  // ── Interaction Handlers ─────────────────────────────────────────

  onOptionClick(opt, btnEl) {
    if (this.state.isAnswered) return;

    this.state.selectedOption = opt;

    // Highlight selected, clear others
    document.querySelectorAll('.s7-option-btn').forEach(b => b.classList.remove('selected'));
    btnEl.classList.add('selected');

    // Update inline slot with chosen word
    const slot = document.getElementById('active-blank');
    if (slot) {
      slot.innerHTML = `<span class="slot-icon">🧩</span> <span class="slot-text">${this.esc(opt)}</span>`;
      slot.classList.add('filled');
      slot.classList.remove('wrong');
    }

    // Clear any error feedback
    const fb = this.state.domCache.feedback;
    if (fb?.classList.contains('err')) {
      fb.textContent = '';
      fb.className   = 's7-feedback';
    }
  },

  onSubmitClick() {
    // If already answered → advance to next sentence/word
    if (this.state.isAnswered) {
      this.advance();
      return;
    }

    // No option chosen yet
    if (!this.state.selectedOption) {
      this.showFeedback('Please select a word from the options below.', 'err');
      const slot = document.getElementById('active-blank');
      if (slot) slot.classList.add('wrong');
      return;
    }

    this.validate();
  },

  validate() {
    const { selectedOption, currentBlank, domCache } = this.state;
    const isCorrect = selectedOption === currentBlank.expected.toLowerCase();
    const slot      = document.getElementById('active-blank');
    const allBtns   = document.querySelectorAll('.s7-option-btn');

    this.state.isAnswered = true;

    if (isCorrect) {
      this.showFeedback('Brilliant deduction! (+10 pts)', 'ok');
      slot?.classList.add('correct');

      allBtns.forEach(btn => {
        if (btn.textContent.trim() === selectedOption) btn.classList.add('correct');
        else                                             btn.classList.add('dimmed');
      });

      this.addScore(10);
      if (domCache.skipBtn) domCache.skipBtn.disabled = true;

    } else {
      this.showFeedback('Incorrect — try another option or skip.', 'err');
      slot?.classList.add('wrong');

      // Un-select the wrong pick so player can try again
      allBtns.forEach(btn => {
        if (btn.textContent.trim() === selectedOption) {
          btn.classList.remove('selected');
          btn.classList.add('wrong-pick');
          setTimeout(() => btn.classList.remove('wrong-pick'), 600);
        }
      });

      this.state.isAnswered    = false; // allow retry
      this.state.selectedOption = null;
      return; // don't advance button yet
    }

    this.updateAdvanceButton();
  },

  skipSentence() {
    if (this.state.isAnswered) return;
    this.state.isAnswered = true;

    const expected = this.state.currentBlank.expected.toLowerCase();
    const slot     = document.getElementById('active-blank');
    if (slot) {
      slot.innerHTML =
        `<span class="slot-icon">💡</span> <span class="slot-text">${this.esc(expected)}</span>`;
      slot.classList.add('filled');
      slot.style.cssText += ';border-color:#f59e0b;color:#b45309;background:#fffbeb;';
    }

    document.querySelectorAll('.s7-option-btn').forEach(btn => {
      if (btn.textContent.trim() === expected) btn.classList.add('correct');
      else                                      btn.classList.add('dimmed');
    });

    this.showFeedback('Term revealed — no points awarded.', 'err');
    if (this.state.domCache.skipBtn) this.state.domCache.skipBtn.disabled = true;
    this.updateAdvanceButton();
  },

  // ── Progression ─────────────────────────────────────────────────

  updateAdvanceButton() {
    const { domCache, testSequence, testIndex, sentenceIndex, sentences } = this.state;
    if (!domCache.submitBtn) return;

    const lastSentence = sentenceIndex >= sentences.length - 1;
    const lastWord     = testIndex >= testSequence.length - 1;

    if (lastSentence && lastWord) {
      domCache.submitBtn.textContent = 'Proceed to Final Stage 🏆 →';
      domCache.submitBtn.className   = 's7-btn s7-btn-submit gold';
    } else if (lastSentence) {
      domCache.submitBtn.textContent = 'Next Word →';
      domCache.submitBtn.className   = 's7-btn s7-btn-submit';
    } else {
      domCache.submitBtn.textContent = 'Next Sentence →';
      domCache.submitBtn.className   = 's7-btn s7-btn-submit';
    }

    domCache.submitBtn.disabled = false;
    domCache.submitBtn.focus();
  },

  advance() {
    const { sentenceIndex, sentences, testIndex, testSequence } = this.state;
    const lastSentence = sentenceIndex >= sentences.length - 1;
    const lastWord     = testIndex >= testSequence.length - 1;

    if (lastSentence && lastWord) {
      this.finishStage();
      return;
    }
    if (lastSentence) {
      this.state.testIndex++;
      this.loadWordTest();
    } else {
      this.state.sentenceIndex++;
      this.renderSentence();
    }
  },

  finishStage() {
    if (this.state.isAdvancing) return;
    this.state.isAdvancing = true;

    sharedState.save(this.state.gameData);
    if (typeof sharedState.recordStageScore === 'function') {
      sharedState.recordStageScore('stage7', 'Stage 7: Definition Completion', this.state.stageScore);
    }

    this.navigate('10_stage8_hall_of_fame_intro.html');
  },

  // ── Helpers ─────────────────────────────────────────────────────

  navigate(url) {
    if (typeof window.navigateWithTransition === 'function') {
      window.navigateWithTransition(url);
    } else {
      window.location.href = url;
    }
  },

  showFeedback(msg, type) {
    const fb = this.state.domCache.feedback;
    if (fb) {
      fb.textContent = msg;
      fb.className   = `s7-feedback ${type}`;
    }
    if (typeof AudioManager !== 'undefined') AudioManager.play(type);
  },

  addScore(pts) {
    this.state.stageScore       += pts;
    this.state.gameData.score    = (this.state.gameData.score || 0) + pts;
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score;
    }

    // Floating +10 effect
    const submitBtn = this.state.domCache.submitBtn;
    if (submitBtn) {
      const rect    = submitBtn.getBoundingClientRect();
      const floater = document.createElement('div');
      floater.className   = 'floating-point';
      floater.textContent = `+${pts}`;
      floater.style.left  = `${rect.left + rect.width / 2}px`;
      floater.style.top   = `${rect.top - 24}px`;
      document.body.appendChild(floater);
      setTimeout(() => floater.remove(), 1000);
    }
  },

  esc(str) {
    return String(str || '').replace(/[&<>'"]/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
    }[c] || c));
  }
};

// Node.js export (for unit testing), browser auto-init
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Stage7Controller;
} else if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => Stage7Controller.init());
  } else {
    Stage7Controller.init();
  }
}
