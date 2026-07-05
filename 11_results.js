// =====================================================================
// FILE: 11_results.js (The Report Card - Hall of Fame)
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
    // Add socket.io client dynamically if in multiplayer
    this.state.gameData = sharedState.load();
    if (this.state.gameData.multiplayerMode) {
      this.initMultiplayer();
    }

    if (typeof initModal === 'function') initModal();
    sharedState.stopTimer();

    const globalTimer = document.getElementById('global-game-timer');
    if (globalTimer) globalTimer.style.display = 'none';

    this.state.gameData = sharedState.load();
    if (!this.state.gameData.selectedWords || this.state.gameData.selectedWords.length === 0) {
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('index.html');
      else window.location.href = 'index.html';
      return;
    }

    this.cacheDOM();
    this.renderStageScores();
    this.processFinalScore();
    this.renderWordsList();
    this.updateGlobalHistory();
    this.attachListeners();
  },

  cacheDOM() {
    this.state.domCache = {
      scoreEl: document.getElementById('res-score'),
      assimilationEl: document.getElementById('res-assimilation'),
      stageScoresHost: document.getElementById('res-stage-scores'),
      wordsList: document.getElementById('res-words-list'),
      playAgainBtn: document.getElementById('play-again-btn'),
      goHomeBtn: document.getElementById('go-home-btn'),
      battleContainer: document.getElementById('battle-verdict-container'),
      battleOutcome: document.getElementById('battle-outcome'),
      opponentName: document.getElementById('opponent-name'),
      opponentPoints: document.getElementById('opponent-points'),
      playerAvatarDisplay: document.getElementById('player-avatar-display')
    };

    if (this.state.domCache.playerAvatarDisplay) {
      this.state.domCache.playerAvatarDisplay.textContent = this.state.gameData.avatar || '🤓';
    }
  },

  initMultiplayer() {
    const { gameData } = this.state;
    if (typeof io === 'undefined') return;
    
    this.socket = io();
    this.socket.emit('join_room', { 
      roomId: gameData.currentRoomId, 
      username: localStorage.getItem('osmosis_user') || 'Guest' 
    });

    // Send final score immediately
    this.socket.emit('update_score', {
      roomId: gameData.currentRoomId,
      score: gameData.score || 0,
      username: localStorage.getItem('osmosis_user') || 'Guest',
      time: gameData.totalTime || 0,
      words: gameData.selectedWords || [],
      meanings: gameData.meanings || {}
    });

    this.socket.on('leaderboard_update', (data) => {
      this.updateBattleVerdict(data.players);
    });
  },

  updateBattleVerdict(players) {
    const { domCache, gameData } = this.state;
    if (!domCache.battleContainer) return;

    const myName = localStorage.getItem('osmosis_user') || 'Guest';
    const otherPlayers = players.filter(p => p.name !== myName);

    if (otherPlayers.length > 0) {
      domCache.battleContainer.style.display = 'block';
      
      // Check if everyone has a score submitted
      const allFinished = players.every(p => p.score !== undefined && p.score !== null);
      
      if (!allFinished) {
        domCache.battleOutcome.textContent = "WAITING FOR OTHERS...";
        domCache.battleOutcome.style.color = "var(--text-secondary)";
        domCache.opponentName.textContent = "Multiplayer Battle";
        domCache.opponentPoints.textContent = "Calculating...";
        return;
      }

      // If everyone finished, find the winner using tie-breaking (Faster time wins)
      const myScore = gameData.score || 0;
      const myTime = gameData.totalTime || 0;

      const sortedPlayers = [...players].sort((a, b) => {
        if ((b.score || 0) !== (a.score || 0)) return (b.score || 0) - (a.score || 0);
        return (a.time || 0) - (b.time || 0);
      });

      const winner = sortedPlayers[0];

      // UI Polish for the verdict
      if (winner.name === myName) {
        domCache.battleOutcome.textContent = "VICTORY";
        domCache.battleOutcome.style.color = "#4caf50";
      } else {
        domCache.battleOutcome.textContent = "DEFEAT";
        domCache.battleOutcome.style.color = "#f44336";
      }

      // Show the top opponent's score and time in the sub-box
      const topOpponent = otherPlayers.sort((a, b) => {
        if ((b.score || 0) !== (a.score || 0)) return (b.score || 0) - (a.score || 0);
        return (a.time || 0) - (b.time || 0);
      })[0];
      
      const oppTimeStr = typeof sharedState !== 'undefined' ? sharedState.getFormattedTime(topOpponent.time || 0) : '...';
      domCache.opponentName.textContent = `Top Opponent: ${topOpponent.name}`;
      domCache.opponentPoints.textContent = `${topOpponent.score} pts (Time: ${oppTimeStr})`;
    }
  },

  renderStageScores() {
    const { domCache, gameData } = this.state;
    if (!domCache.stageScoresHost) return;

    const stageScores = gameData.stageScores || {};
    const stageItems = Object.entries(stageScores).sort((a, b) => (a[1].at || 0) - (b[1].at || 0));

    if (stageItems.length === 0) {
      domCache.stageScoresHost.innerHTML = `<p style="font-style: italic; color: #aaa; text-align: center;">No stage scores recorded.</p>`;
    } else {
      domCache.stageScoresHost.innerHTML = '';
      stageItems.forEach(([, item]) => {
        const row = document.createElement('div');
        row.className = 'stage-row';
        row.innerHTML = `<span class="stage-name">${item.label}</span><span class="stage-score">${item.score} pts</span>`;
        domCache.stageScoresHost.appendChild(row);
      });
    }
  },

  processFinalScore() {
    const { gameData, domCache } = this.state;

    this.state.targetScore = gameData.score || 0;
    
    // Rate of Assimilation = Total Score / Total Time
    let totalTimeSecs = (gameData.totalTime || 0) / 1000;
    let rateOfAssimilation = 0;
    if (totalTimeSecs > 0) {
        rateOfAssimilation = (this.state.targetScore / totalTimeSecs).toFixed(2);
    } else if (this.state.targetScore > 0) {
        rateOfAssimilation = this.state.targetScore.toFixed(2);
    }
    
    if (domCache.assimilationEl) {
        domCache.assimilationEl.textContent = `Rate of Assimilation: ${rateOfAssimilation} pts/sec`;
    }

    // Format total time as Xm Ys
    const totalMins = Math.floor(totalTimeSecs / 60);
    const totalSecs = Math.floor(totalTimeSecs % 60);
    const totalTimeFormatted = totalMins > 0
      ? `${totalMins}m ${totalSecs}s`
      : `${totalSecs}s`;

    this.state.currentNumber = 0;
    const duration = 2000;
    const interval = 30;
    const step = Math.max(1, Math.floor(this.state.targetScore / (duration / interval)));

    // Show total time spent immediately
    if (domCache.scoreEl) {
      domCache.scoreEl.innerHTML = `Total Score: 0<br><span class="time-spent-text" style="color:#ffd700; letter-spacing:2px; font-size:1.5rem;">time spent: ${totalTimeFormatted}</span>`;
    }

    this.state.counterInt = setInterval(() => {
      this.state.currentNumber += step;

      if (this.state.currentNumber >= this.state.targetScore) {
        this.state.currentNumber = this.state.targetScore;
        clearInterval(this.state.counterInt);

        if (typeof AudioManager !== 'undefined') {
          AudioManager.init();
          AudioManager.play('success');
        }

        // Final Score display with time
        if (domCache.scoreEl) {
          domCache.scoreEl.innerHTML = `Total Score: ${this.state.currentNumber}<br><span class="time-spent-text" style="color:#ffd700; letter-spacing:2px; font-size:1.5rem;">time spent: ${totalTimeFormatted}</span>`;
        }

        let bonusShown = false;
        const showBonus = () => {
          if (bonusShown) return;
          bonusShown = true;
        };
        setTimeout(showBonus, 900);
        return;
      }

      if (domCache.scoreEl) {
        domCache.scoreEl.innerHTML = `Total Score: ${this.state.currentNumber}<br><span class="time-spent-text" style="color:#ffd700; letter-spacing:2px; font-size:1.5rem;">time spent: ${totalTimeFormatted}</span>`;
      }
    }, interval);
  },

  renderWordsList() {
    const { domCache, gameData } = this.state;
    if (!domCache.wordsList) return;

    domCache.wordsList.innerHTML = '';
    gameData.selectedWords.forEach(word => {
      const item = document.createElement('div');
      item.className = 'word-card';
      const meaning = gameData.meanings && gameData.meanings[word] ? gameData.meanings[word] : "Definition captured strictly in memory.";

      item.innerHTML = `<h4>${word}</h4><p>${meaning}</p>`;
      domCache.wordsList.appendChild(item);
    });
  },

  updateGlobalHistory() {
    if (!sessionStorage.getItem('osmosis_saved_result')) {
      const currentTotal = parseInt(localStorage.getItem('osmosis_total_score')) || 0;
      localStorage.setItem('osmosis_total_score', currentTotal + this.state.targetScore);

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
        if (typeof AudioManager !== 'undefined') AudioManager.play('click');

        if (typeof sharedState.clearGameSession === 'function') {
          sharedState.clearGameSession(true);
        }

        setTimeout(() => {
          if (typeof window.navigateWithTransition === 'function') navigateWithTransition('02_campaign_setup.html');
          else window.location.href = '02_campaign_setup.html';
        }, 200);
      });
    }

    if (domCache.goHomeBtn) {
      domCache.goHomeBtn.addEventListener('click', () => {
        if (typeof AudioManager !== 'undefined') AudioManager.play('click');

        if (typeof sharedState.clearGameSession === 'function') {
          sharedState.clearGameSession(true);
        }

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
