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
    if (this.state.gameData.multiplayerMode && this.state.gameData.currentRoomId) {
      // Multiplayer players get their own dedicated results page
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('multiplayer_results.html');
      else window.location.href = 'multiplayer_results.html';
      return;
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
      leaderboardCard: document.getElementById('mp-leaderboard-card'),
      leaderboardBody: document.getElementById('mp-leaderboard-body'),
      insightsModal: document.getElementById('player-insights-modal'),
      insightsCloseBtn: document.getElementById('insights-close-btn'),
      insightsAvatar: document.getElementById('insights-avatar'),
      insightsName: document.getElementById('insights-name'),
      insightsWordsContainer: document.getElementById('insights-words-container'),
      playerAvatarDisplay: document.getElementById('player-avatar-display')
    };

    if (this.state.domCache.playerAvatarDisplay) {
      this.state.domCache.playerAvatarDisplay.textContent = this.state.gameData.avatar || '🤓';
    }

    // Close modal on button click or overlay click
    const { insightsModal, insightsCloseBtn } = this.state.domCache;
    if (insightsCloseBtn) {
      insightsCloseBtn.addEventListener('click', () => insightsModal.classList.remove('active'));
    }
    if (insightsModal) {
      insightsModal.addEventListener('click', (e) => {
        if (e.target === insightsModal) insightsModal.classList.remove('active');
      });
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
    const { domCache } = this.state;
    if (!domCache.leaderboardCard || !domCache.leaderboardBody) return;

    // Sort by score desc, then time asc
    const sorted = [...players].sort((a, b) => {
      if ((b.score || 0) !== (a.score || 0)) return (b.score || 0) - (a.score || 0);
      return (a.time || 0) - (b.time || 0);
    });

    // Show the leaderboard card
    domCache.leaderboardCard.hidden = false;
    domCache.leaderboardCard.style.display = 'block';

    // Rank medal emoji
    const medals = ['🥇', '🥈', '🥉'];
    const trophyIcons = ['🏆', '🏆', '🏆'];
    const rankColors = ['#d69e2e', '#a0aec0', '#9c4221'];

    domCache.leaderboardBody.innerHTML = '';
    sorted.forEach((player, i) => {
      const rank = i + 1;
      const isWinner = rank === 1;
      const hasScore = player.score !== undefined && player.score !== null;
      const scoreText = hasScore ? player.score.toLocaleString() : '...';
      const timeStr = hasScore && typeof sharedState !== 'undefined'
        ? sharedState.getFormattedTime(player.time || 0)
        : '—';
      const avatar = player.avatar || '🤓';
      const medal = medals[i] || '';
      const trophyColor = rankColors[i] || '#a0aec0';

      const tr = document.createElement('tr');
      if (isWinner) tr.classList.add('winner-row');
      if (rank === 2) tr.classList.add('rank-2');
      if (rank === 3) tr.classList.add('rank-3');
      tr.style.cursor = 'pointer';

      tr.innerHTML = `
        <td style="text-align: center;">
          <span class="mp-rank">${rank}</span>
          ${medal ? `<span class="mp-rank-medal">${medal}</span>` : ''}
        </td>
        <td>
          <div class="mp-player-col">
            <div class="mp-avatar">${avatar}</div>
            <div>
              <div class="mp-name">
                ${player.name}
                ${isWinner ? '<span class="mp-winner-tag">WINNER</span>' : ''}
              </div>
              <div style="font-size: 0.8rem; color: #a0aec0; margin-top: 2px;">Time: ${timeStr}</div>
            </div>
          </div>
        </td>
        <td class="right-align">
          <span class="mp-score">${scoreText}</span>
          ${rank <= 3 ? `<span class="mp-score-trophy" style="color: ${trophyColor};">🏆</span>` : ''}
        </td>
      `;

      // Click to open player insights
      tr.addEventListener('click', () => this.openPlayerInsights(player));
      domCache.leaderboardBody.appendChild(tr);
    });
  },

  openPlayerInsights(player) {
    const { domCache } = this.state;
    if (!domCache.insightsModal) return;

    // Populate header
    domCache.insightsAvatar.textContent = player.avatar || '🤓';
    domCache.insightsName.textContent = player.name;

    // Populate words list
    const words = player.words || [];
    const meanings = player.meanings || {};
    const container = domCache.insightsWordsContainer;
    container.innerHTML = '';

    if (words.length === 0) {
      container.innerHTML = '<p class="insights-empty">No words recorded for this player yet.</p>';
    } else {
      words.forEach(word => {
        const def = meanings[word] || 'Definition not available.';
        const item = document.createElement('div');
        item.className = 'insights-word-item';
        item.innerHTML = `
          <div class="insights-word-title">${word}</div>
          <p class="insights-word-def">${def}</p>
        `;
        container.appendChild(item);
      });
    }

    domCache.insightsModal.classList.add('active');
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
