// =====================================================================
// FILE: 10_stage8_recall_test.js (The Final Recall Test)
// =====================================================================
// Welcome to the final battle! This is like standing before a great king who 
// wants you to interpret his dreams.
// For every word you've collected, we show it to you along with its meaning 
// for just 5 short seconds. Then, poof! It vanishes! 
// You have to type back the exact word and meaning entirely from memory. 
// Get it right, and the king rewards you. Get it wrong, and you lose points!

const Stage8Controller = {
  state: {
    gameData: null,
    domCache: {},
    sequence: [],
    idx: -1,
    phase: 'intro',
    stageStartScore: 0,
    isFinishing: false,
    isSecondChance: false
  },

  CONFIG: {
    FLASH_MS: 5000
  },

  init() {
    if (typeof initModal === 'function') initModal();
    sharedState.startTimer();
    this.state.gameData = sharedState.load();
    sharedState.updateTimerUI();

    if (!this.state.gameData.selectedWords || this.state.gameData.selectedWords.length === 0) {
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('index.html');
      else window.location.href = 'index.html';
      return;
    }

    this.state.stageStartScore = this.state.gameData.score || 0;
    this.state.sequence = [...(this.state.gameData.selectedWords || [])].sort(() => Math.random() - 0.5);

    this.cacheDOM();
    this.renderInitialUI();
    this.attachListeners();
    this.advanceToNextCard(); // Auto-start — no need for a "Continue" click
  },

  cacheDOM() {
    this.state.domCache = {
      scoreEl: document.getElementById('current-score'),
      progressEl: document.getElementById('nd-progress'),
      memoryBoxEl: document.getElementById('nd-memory-box'),
      inputWrapEl: document.getElementById('nd-input-wrap'),
      wordInput: document.getElementById('nd-word-input'),
      meaningInput: document.getElementById('nd-meaning-input'),
      feedbackEl: document.getElementById('nd-feedback'),
      revealEl: document.getElementById('nd-reveal'),
      revealWordEl: document.getElementById('nd-reveal-word'),
      revealMeaningEl: document.getElementById('nd-reveal-meaning'),
      mainBtn: document.getElementById('nd-main-btn')
    };
  },

  renderInitialUI() {
    if (this.state.domCache.scoreEl) {
      this.state.domCache.scoreEl.textContent = this.state.gameData.score || 0;
    }
  },

  attachListeners() {
    const { domCache } = this.state;

    if (domCache.mainBtn) {
      domCache.mainBtn.addEventListener('click', () => this.handleMainAction());
    }
  },

  escapeHTML(str) {
    return String(str || '').replace(/[&<>'"]/g, tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag));
  },

  extractKeywords(text) {
    // This is a special word-filter. It throws away small, boring words 
    // like "the" or "and", and keeps only the big, juicy words (keywords) 
    // so we can see if you *actually* understood the meaning!
    const stopwords = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'of', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'it', 'this', 'that', 'which', 'who', 'whom', 'whose', 'some', 'any', 'such', 'into'];
    const words = String(text || '').toLowerCase().replace(/[^\w\s]/g, '').split(/\s+/);
    return [...new Set(words.filter(w => w.length > 2 && !stopwords.includes(w)))];
  },

  gradeAttempt(userWord, userMeaning, trueWord, trueMeaning) {
    // Here we grade your answer like a strict but fair teacher.
    // It checks if you spelled your word perfectly, and counts how many 
    // "juicy" keywords you got right in the meaning.
    const wOk = userWord.trim().toLowerCase() === String(trueWord || '').toLowerCase();
    const trueK = this.extractKeywords(trueMeaning);
    const userK = this.extractKeywords(userMeaning);
    let mRatio = 0;

    if (trueK.length > 0) {
      const hit = trueK.filter(k => userK.includes(k)).length;
      mRatio = hit / trueK.length;
    } else if (String(userMeaning || '').trim().length > 15) {
      mRatio = 0.35;
    }

    let pts = 0;
    if (wOk) pts += 10;
    pts += Math.round(mRatio * 10);
    pts = Math.max(0, pts); // Safety guard — score can never decrease here

    return { wOk, mRatio, pts };
  },

  setProgress() {
    const { domCache, sequence, idx } = this.state;
    if (!domCache.progressEl) return;

    if (idx < 0) {
      domCache.progressEl.textContent = `0 / ${sequence.length}`;
    } else {
      domCache.progressEl.textContent = `${idx + 1} / ${sequence.length}`;
    }
  },

  finishStage() {
    if (this.state.isFinishing) return;
    this.state.isFinishing = true;

    sharedState.save(this.state.gameData);
    const stageScore = Math.max(0, (this.state.gameData.score || 0) - this.state.stageStartScore);

    if (typeof AudioManager !== 'undefined') AudioManager.play('success');

    sharedState.showStageScoreThen('stage7', "Stage 7: Hall of fame", stageScore, () => {
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('10b_stage8_complete.html');
      else window.location.href = '10b_stage8_complete.html';
    });
  },

  showFlashCard() {
    // This is the magical "Flash!" moment. We bring up the flashcard, 
    // show you the word and its meaning, and start our 5-second countdown timer!
    // Stare at it and memorize it before it disappears!
    const { domCache, sequence, idx, gameData } = this.state;

    const word = sequence[idx];
    const meaning = (gameData.meanings && gameData.meanings[word]) ? gameData.meanings[word] : '';

    this.setProgress();

    if (domCache.feedbackEl) {
      domCache.feedbackEl.textContent = '';
      domCache.feedbackEl.className = 'nd-feedback';
    }

    if (domCache.revealEl) domCache.revealEl.style.display = 'none';
    if (domCache.inputWrapEl) domCache.inputWrapEl.style.display = 'none';
    if (domCache.wordInput) domCache.wordInput.value = '';
    if (domCache.meaningInput) domCache.meaningInput.value = '';

    if (domCache.memoryBoxEl) {
      domCache.memoryBoxEl.style.display = 'flex';
      domCache.memoryBoxEl.innerHTML = `<div class="nd-word">${this.escapeHTML(word)}</div><div class="nd-meaning">${this.escapeHTML(meaning)}</div>`;
    }

    if (domCache.mainBtn) {
      domCache.mainBtn.style.flex = '1';
      domCache.mainBtn.disabled = true;
      domCache.mainBtn.textContent = 'Memorize...';
    }
    this.state.phase = 'flash';

    setTimeout(() => {
      if (domCache.memoryBoxEl) {
        domCache.memoryBoxEl.innerHTML = `<div class="nd-hidden-note">Now type the word and meaning you saw.</div>`;
      }
      if (domCache.inputWrapEl) domCache.inputWrapEl.style.display = 'block';
      if (domCache.wordInput) domCache.wordInput.focus();

      if (domCache.mainBtn) {
        domCache.mainBtn.disabled = false;
        domCache.mainBtn.textContent = (idx === sequence.length - 1) ? 'Check & Finish' : 'Check';
      }
      this.state.phase = 'answer';
    }, this.CONFIG.FLASH_MS);
  },

  advanceToNextCard() {
    this.state.isSecondChance = false;
    this.state.idx += 1;
    if (this.state.idx >= this.state.sequence.length) {
      this.finishStage();
      return;
    }
    this.showFlashCard();
  },

  handleMainAction() {
    const { sequence, phase } = this.state;

    if (sequence.length === 0) {
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('10b_stage8_complete.html');
      else window.location.href = '10b_stage8_complete.html';
      return;
    }

    if (phase === 'intro' || phase === 'next') {
      this.advanceToNextCard();
      return;
    }

    if (phase !== 'answer') return;

    this.submitAnswer();
  },

  triggerFlashSequence(word, meaning) {
    const { domCache, idx, sequence } = this.state;

    // Flash logic
    if (domCache.inputWrapEl) domCache.inputWrapEl.style.display = 'none';
    if (domCache.memoryBoxEl) {
      domCache.memoryBoxEl.style.display = 'flex';
      domCache.memoryBoxEl.innerHTML = `<div class="nd-word">${this.escapeHTML(word)}</div><div class="nd-meaning">${this.escapeHTML(meaning)}</div>`;
    }
    if (domCache.mainBtn) {
      domCache.mainBtn.disabled = true;
      domCache.mainBtn.textContent = 'Memorize...';
    }

    setTimeout(() => {
      if (domCache.memoryBoxEl) {
        domCache.memoryBoxEl.innerHTML = `<div class="nd-hidden-note">Try again! (Half points available)</div>`;
      }
      if (domCache.inputWrapEl) domCache.inputWrapEl.style.display = 'block';
      if (domCache.wordInput) domCache.wordInput.focus();
      if (domCache.mainBtn) {
        domCache.mainBtn.disabled = false;
        domCache.mainBtn.textContent = (idx === sequence.length - 1) ? 'Check & Finish' : 'Check';
      }
    }, 2500);
  },

  submitAnswer() {
    const { domCache, sequence, idx, gameData, isSecondChance } = this.state;
    const word = sequence[idx];
    const meaning = (gameData.meanings && gameData.meanings[word]) ? gameData.meanings[word] : '';
    const userWord = domCache.wordInput ? domCache.wordInput.value : '';
    const userMeaning = domCache.meaningInput ? domCache.meaningInput.value : '';

    const g = this.gradeAttempt(userWord, userMeaning, word, meaning);
    const isBad = (!g.wOk && g.mRatio < 0.50);
    const isPerfect = (g.wOk && g.mRatio >= 0.8);

    if (isBad && !isSecondChance) {
      // Trigger Second Chance via Popup only if they totally failed
      this.state.isSecondChance = true;

      const promptText = "Incorrect. You have a second chance for half points. Prepare to read carefully...";

      if (typeof window.showModal === 'function') {
        window.showModal(
          "Second Chance",
          promptText,
          () => {
            this.triggerFlashSequence(word, meaning);
          },
          () => {
            // Forfeit Logic: Show answer, no points, move to next
            if (domCache.feedbackEl) {
              domCache.feedbackEl.className = 'nd-feedback bad';
              domCache.feedbackEl.textContent = "Forfeited. Look at the answer and click next.";
            }
            if (domCache.revealWordEl) domCache.revealWordEl.textContent = word;
            if (domCache.revealMeaningEl) domCache.revealMeaningEl.textContent = meaning;
            if (domCache.revealEl) domCache.revealEl.style.display = 'block';
            this.state.phase = 'next';
            if (domCache.mainBtn) {
              domCache.mainBtn.textContent = (idx === sequence.length - 1) ? 'Finish to Results' : 'Next';
            }
          }
        );
      } else {
        // Fallback if modal system is somehow missing
        if (domCache.feedbackEl) {
          domCache.feedbackEl.className = 'nd-feedback partial';
          domCache.feedbackEl.textContent = promptText;
        }
        setTimeout(() => this.triggerFlashSequence(word, meaning), 1000);
      }

      if (typeof AudioManager !== 'undefined') AudioManager.play('error');
      return;
    }

    // Final grading (either perfect on first try, or any result on second try)
    let finalPts = g.pts;
    if (isSecondChance) finalPts = Math.round(finalPts / 2);

    gameData.score = (gameData.score || 0) + finalPts;
    if (domCache.scoreEl) domCache.scoreEl.textContent = gameData.score;
    sharedState.save(gameData);

    const pct = Math.round(g.mRatio * 100);

    if (domCache.feedbackEl) {
      if (isPerfect) {
        domCache.feedbackEl.className = 'nd-feedback ok';
        domCache.feedbackEl.textContent = `Excellent! You remembered it perfectly! +${finalPts} pts`;
        if (typeof AudioManager !== 'undefined') AudioManager.play('success');
      } else if (g.wOk || g.mRatio >= 0.50) {
        domCache.feedbackEl.className = 'nd-feedback partial';
        domCache.feedbackEl.textContent = `You have partially remembered +${finalPts} pts (${pct}% match)`;
        if (typeof AudioManager !== 'undefined') AudioManager.play('chip');
      } else {
        domCache.feedbackEl.className = 'nd-feedback bad';
        domCache.feedbackEl.textContent = `Keep going, The correct answer is shown below. (${pct}% match)`;
        if (typeof AudioManager !== 'undefined') AudioManager.play('error');
      }
    }

    if (domCache.revealWordEl) domCache.revealWordEl.textContent = word;
    if (domCache.revealMeaningEl) domCache.revealMeaningEl.textContent = meaning;
    if (domCache.revealEl) domCache.revealEl.style.display = 'block';

    this.state.phase = 'next';
    if (domCache.mainBtn) {
      domCache.mainBtn.textContent = (idx === sequence.length - 1) ? 'Finish to Results' : 'Next';
    }
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => Stage8Controller.init());
} else {
  Stage8Controller.init();
}
