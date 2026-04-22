// =====================================================================
// FILE: 10_results.js (The Report Card)
// =====================================================================

const ResultsController = {
  state: {
    gameData: null,
    domCache: {},
    counterInt: null,
    targetScore: 0,
    currentNumber: 0
  },

  init() {
    if (typeof initModal === 'function') initModal();
    sharedState.stopTimer();

    const globalTimer = document.getElementById('global-game-timer');
    if (globalTimer) globalTimer.style.display = 'none';

    this.state.gameData = sharedState.load();
    if (!this.state.gameData.selectedWords || this.state.gameData.selectedWords.length === 0) {
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('00_login.html');
      else window.location.href = '00_login.html';
      return;
    }

    this.cacheDOM();
    this.renderTimes();
    this.renderStageScores();
    this.processFinalScore();
    this.renderWordsList();
    this.updateGlobalHistory();
    this.attachListeners();
  },

  cacheDOM() {
    this.state.domCache = {
      totalTimeEl: document.getElementById('res-total-time'),
      startTimeEl: document.getElementById('res-start-time'),
      endTimeEl: document.getElementById('res-end-time'),
      stageScoresHost: document.getElementById('res-stage-scores'),
      scoreEl: document.getElementById('res-score'),
      statsEl: document.getElementById('res-stats'),
      lifetimeScoreEl: document.getElementById('res-lifetime-score'),
      wordsList: document.getElementById('res-words-list'),
      playAgainBtn: document.getElementById('play-again-btn'),
      goHomeBtn: document.getElementById('go-home-btn')
    };
  },

  renderTimes() {
    const { domCache, gameData } = this.state;
    if (domCache.totalTimeEl) domCache.totalTimeEl.textContent = `Total Session Time: ${sharedState.getFormattedTime(gameData.totalTime)}`;
    if (domCache.startTimeEl) domCache.startTimeEl.textContent = `Started: ${sharedState.formatDateTime(gameData.sessionStartedAt)}`;
    if (domCache.endTimeEl) domCache.endTimeEl.textContent = `Ended: ${sharedState.formatDateTime(gameData.sessionEndedAt)}`;
  },

  renderStageScores() {
    const { domCache, gameData } = this.state;
    if (!domCache.stageScoresHost) return;

    const stageScores = gameData.stageScores || {};
    const stageItems = Object.entries(stageScores).sort((a, b) => (a[1].at || 0) - (b[1].at || 0));
    
    if (stageItems.length === 0) {
      domCache.stageScoresHost.innerHTML = `<p style="font-style: italic; color: var(--text-secondary);">No stage scores recorded.</p>`;
    } else {
      domCache.stageScoresHost.innerHTML = '';
      stageItems.forEach(([, item]) => {
        const row = document.createElement('div');
        row.className = 'word-item';
        row.innerHTML = `<strong>${item.label}</strong><p>${item.score} pts</p>`;
        domCache.stageScoresHost.appendChild(row);
      });
    }
  },

  processFinalScore() {
    const { gameData, domCache } = this.state;
    
    const maxPossibleScore = gameData.selectedWords.length * 56;
    this.state.targetScore = gameData.score || 0;
    
    let accuracy = 0;
    if (maxPossibleScore > 0) accuracy = Math.round((this.state.targetScore / maxPossibleScore) * 100);

    this.state.currentNumber = 0;
    const duration = 2000;
    const interval = 30;
    const step = Math.max(1, Math.floor(this.state.targetScore / (duration / interval)));

    this.state.counterInt = setInterval(() => {
      this.state.currentNumber += step;
      
      if (this.state.currentNumber >= this.state.targetScore) {
        this.state.currentNumber = this.state.targetScore;
        clearInterval(this.state.counterInt);
        
        if (typeof AudioManager !== 'undefined') {
          AudioManager.init();
          AudioManager.play('success'); 
        }
        
        if (domCache.statsEl) {
          domCache.statsEl.textContent = `Accuracy: ${accuracy}%  (${this.state.targetScore} / ${maxPossibleScore} pts)`;
          domCache.statsEl.style.opacity = 1;
        }

        const currentTotal = parseInt(localStorage.getItem('osmosis_total_score')) || 0;
        const isSaved = sessionStorage.getItem('osmosis_saved_result');
        const finalTotal = isSaved ? currentTotal : currentTotal + this.state.targetScore;
        
        let nextLimit = 501;
        if (finalTotal >= 3001) nextLimit = 'MAX';
        else if (finalTotal >= 1501) nextLimit = 3001;
        else if (finalTotal >= 501) nextLimit = 1501;
        
        if (domCache.lifetimeScoreEl) {
          const progressText = nextLimit === 'MAX' ? `Titan Tier Maxed` : `Next Rank at ${nextLimit}`;
          domCache.lifetimeScoreEl.textContent = `Lifetime Accumulation: ${finalTotal} pts (${progressText})`;
          domCache.lifetimeScoreEl.style.opacity = 1;
        }

        let bonusShown = false;
        const showBonus = () => {
          if (bonusShown) return;
          bonusShown = true;
          if (typeof showModal === 'function') {
            showModal('Run Complete', 'Full run complete.');
          }
        };
        setTimeout(showBonus, 900);
      }

      if (domCache.scoreEl) {
        domCache.scoreEl.textContent = this.state.currentNumber;
      }
    }, interval);
  },

  renderWordsList() {
    const { domCache, gameData } = this.state;
    if (!domCache.wordsList) return;

    domCache.wordsList.innerHTML = '';
    gameData.selectedWords.forEach(word => {
      const item = document.createElement('div');
      item.className = 'word-item';
      const meaning = gameData.meanings && gameData.meanings[word] ? gameData.meanings[word] : "Definition captured strictly in memory.";
      
      item.innerHTML = `<strong>${word}</strong><p>${meaning}</p>`;
      domCache.wordsList.appendChild(item);
    });
  },

  updateGlobalHistory() {
    if (!sessionStorage.getItem('osmosis_saved_result')) {
      const previousLevel = sharedState.getLevel().name;
      const currentTotal = parseInt(localStorage.getItem('osmosis_total_score')) || 0;
      localStorage.setItem('osmosis_total_score', currentTotal + this.state.targetScore);
      const newLevel = sharedState.getLevel().name;
      
      if (newLevel !== previousLevel) {
        setTimeout(() => {
          if (typeof showModal === 'function') {
            showModal('Rank Promoted!', `You have transcended to the [${newLevel}] tier! Prepare for vastly expanded lexicon constraints. Mifetu wishes you well.`);
          }
        }, 2500);
      }

      const history = JSON.parse(localStorage.getItem('osmosis_history')) || [];
      history.push({
        date: new Date().toLocaleDateString(),
        score: this.state.gameData.score,
        words: this.state.gameData.selectedWords
      });
      localStorage.setItem('osmosis_history', JSON.stringify(history));
      sessionStorage.setItem('osmosis_saved_result', 'true');
    }
  },

  attachListeners() {
    const { domCache, gameData } = this.state;

    if (domCache.playAgainBtn) {
      domCache.playAgainBtn.addEventListener('click', () => {
        sessionStorage.removeItem('osmosis_saved_result');
        if (typeof AudioManager !== 'undefined') AudioManager.play('click');
        
        if (gameData.usedLetters && gameData.usedLetters.length >= 26) {
           if (typeof showModal === 'function') {
             showModal('Alphabet Mastery Achieved!', 'You have dominated all 26 letters of the alphabet in a single continuous session! You are a true titan. Initiating the total score.');
           }
           setTimeout(() => {
             if (typeof window.navigateWithTransition === 'function') navigateWithTransition('module_archives.html');
             else window.location.href = 'module_archives.html';
           }, 4000);
        } else {
           gameData.score = 0;
           gameData.usedLetters = [];
           gameData.selectedWords = [];
           gameData.stageScores = {};
           gameData.meanings = {};
           gameData.lastLength = null;
           gameData.totalTime = 0;
           gameData.sessionStartedAt = null;
           sharedState.save(gameData);
           
           setTimeout(() => {
             if (typeof window.navigateWithTransition === 'function') navigateWithTransition('02_campaign_setup.html');
             else window.location.href = '02_campaign_setup.html';
           }, 200);
        }
      });
    }

    if (domCache.goHomeBtn) {
      domCache.goHomeBtn.addEventListener('click', () => {
        sessionStorage.removeItem('osmosis_saved_result');
        if (typeof AudioManager !== 'undefined') AudioManager.play('click');
        setTimeout(() => {
          if (typeof window.navigateWithTransition === 'function') navigateWithTransition('01_home_menu.html');
          else window.location.href = '01_home_menu.html';
        }, 200);
      });
    }
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => ResultsController.init());
} else {
  ResultsController.init();
}
