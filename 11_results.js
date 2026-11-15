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
    if (typeof initModal === 'function') initModal();
    sharedState.stopTimer();

    const globalTimer = document.getElementById('global-game-timer');
    if (globalTimer) globalTimer.style.display = 'none';

    this.state.gameData = sharedState.load();
    this.state.targetScore = this.state.gameData.score || 0;
    if (this.state.gameData.selectedWords && this.state.gameData.selectedWords.length > 0) {
      this.updateGlobalHistory();
    }

    if (this.state.gameData.multiplayerMode && this.state.gameData.currentRoomId) {
      // Multiplayer players get their own dedicated results page
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('multiplayer_results.html');
      else window.location.href = 'multiplayer_results.html';
      return;
    }

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

    // Play Victory Trumpet Fanfare!
    if (typeof AudioManager !== 'undefined') {
      AudioManager.init();
      AudioManager.play('fanfare');
    }
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

  _activeSpeechIndex: -1,
  _readAllPlaylist: [],
  _playlistCurrentIndex: 0,
  _isReadingAll: false,

  stopAnySpeech() {
    this._isReadingAll = false;
    this._readAllPlaylist = [];
    if (window.VoiceManager && typeof window.VoiceManager.stop === 'function') {
      window.VoiceManager.stop();
    } else if (typeof window !== 'undefined' && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    this.clearSpeakingHighlights();
    this.updateToolbarState(false);
  },

  clearSpeakingHighlights() {
    document.querySelectorAll('.word-card.speaking').forEach(c => c.classList.remove('speaking'));
    document.querySelectorAll('.word-action-btn.active-speaking').forEach(b => {
      b.classList.remove('active-speaking');
      if (b.dataset.origHtml) b.innerHTML = b.dataset.origHtml;
    });
    this._activeSpeechIndex = -1;
  },

  setCardSpeaking(idx, activeBtn) {
    this.clearSpeakingHighlights();
    const card = document.getElementById(`hof-word-card-${idx}`);
    if (card) {
      card.classList.add('speaking');
      try {
        card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } catch (_) {}
    }
    if (activeBtn) {
      activeBtn.classList.add('active-speaking');
      if (!activeBtn.dataset.origHtml) activeBtn.dataset.origHtml = activeBtn.innerHTML;
      activeBtn.innerHTML = '<span>⏹️</span> Stop';
    }
    this._activeSpeechIndex = idx;
    this.updateToolbarState(true);
  },

  speakWordOnly(word, idx) {
    const btn = document.getElementById(`pronounce-btn-${idx}`);
    if (this._activeSpeechIndex === idx && btn && btn.classList.contains('active-speaking')) {
      this.stopAnySpeech();
      return;
    }

    this.stopAnySpeech();
    this.setCardSpeaking(idx, btn);

    this.executeSpeech(word, () => {
      this.clearSpeakingHighlights();
      this.updateToolbarState(false);
    });
  },

  speakWordAndMeaning(word, meaning, idx) {
    const btn = document.getElementById(`meaning-btn-${idx}`);
    if (this._activeSpeechIndex === idx && btn && btn.classList.contains('active-speaking')) {
      this.stopAnySpeech();
      return;
    }

    this.stopAnySpeech();
    this.setCardSpeaking(idx, btn);

    const speechText = `${word}. Definition: ${meaning}`;
    this.executeSpeech(speechText, () => {
      this.clearSpeakingHighlights();
      this.updateToolbarState(false);
    });
  },

  executeSpeech(text, onComplete) {
    // If background audio is playing, duck/pause it gently
    if (typeof AudioManager !== 'undefined' && typeof AudioManager.pauseBackground === 'function') {
      try { AudioManager.pauseBackground(); } catch (_) {}
    }

    const finish = () => {
      if (typeof AudioManager !== 'undefined' && typeof AudioManager.resumeBackground === 'function') {
        try { AudioManager.resumeBackground(); } catch (_) {}
      }
      if (onComplete) onComplete();
    };

    if (window.VoiceManager && typeof window.VoiceManager.speak === 'function') {
      window.VoiceManager.speak(text, {
        force: true,
        rate: 0.90,
        pitch: 1.0,
        onend: finish,
        onerror: finish
      });
    } else if (typeof window !== 'undefined' && window.speechSynthesis) {
      try {
        window.speechSynthesis.cancel();
        setTimeout(() => {
          const u = new SpeechSynthesisUtterance(text);
          u.rate = 0.90;
          u.onend = finish;
          u.onerror = finish;
          window.speechSynthesis.speak(u);
        }, 35);
      } catch (_) {
        finish();
      }
    } else {
      finish();
    }
  },

  setupSpeechToolbar(words, meanings) {
    const readAllBtn = document.getElementById('read-all-btn');
    const stopBtn = document.getElementById('stop-speech-btn');

    if (readAllBtn) {
      readAllBtn.onclick = () => {
        if (this._isReadingAll) {
          this.stopAnySpeech();
          return;
        }
        this.startReadAllPlaylist(words, meanings);
      };
    }

    if (stopBtn) {
      stopBtn.onclick = () => {
        this.stopAnySpeech();
      };
    }
  },

  startReadAllPlaylist(words, meanings) {
    this.stopAnySpeech();
    if (!words || words.length === 0) return;

    this._isReadingAll = true;
    this._readAllPlaylist = words.map((w, idx) => ({
      word: w,
      meaning: (meanings && meanings[w]) ? meanings[w] : "Definition captured strictly in memory.",
      idx: idx
    }));
    this._playlistCurrentIndex = 0;
    this.updateToolbarState(true);
    this.playNextInPlaylist();
  },

  playNextInPlaylist() {
    if (!this._isReadingAll || this._playlistCurrentIndex >= this._readAllPlaylist.length) {
      this.stopAnySpeech();
      return;
    }

    const item = this._readAllPlaylist[this._playlistCurrentIndex];
    const meaningBtn = document.getElementById(`meaning-btn-${item.idx}`);
    this.setCardSpeaking(item.idx, meaningBtn);

    const speechText = `${item.word}. ${item.meaning}`;
    this.executeSpeech(speechText, () => {
      this._playlistCurrentIndex++;
      if (this._isReadingAll) {
        setTimeout(() => this.playNextInPlaylist(), 500);
      }
    });
  },

  updateToolbarState(isPlaying) {
    const readAllBtn = document.getElementById('read-all-btn');
    const stopBtn = document.getElementById('stop-speech-btn');
    if (!readAllBtn || !stopBtn) return;

    if (isPlaying) {
      stopBtn.style.display = 'inline-flex';
      if (this._isReadingAll) {
        readAllBtn.innerHTML = '<span class="audio-icon">⏸️</span><span class="audio-text">Reading All...</span>';
      }
    } else {
      stopBtn.style.display = 'none';
      readAllBtn.innerHTML = '<span class="audio-icon">🔊</span><span class="audio-text">Read All Words & Meanings</span>';
    }
  },

  renderWordsList() {
    const { domCache, gameData } = this.state;
    if (!domCache.wordsList) return;

    domCache.wordsList.innerHTML = '';
    const words = gameData.selectedWords || [];

    if (words.length === 0) {
      domCache.wordsList.innerHTML = '<p style="text-align:center; color:#aaa; font-style:italic;">No words recorded in this session.</p>';
      return;
    }

    words.forEach((word, idx) => {
      const item = document.createElement('div');
      item.className = 'word-card';
      item.id = `hof-word-card-${idx}`;
      const meaning = (gameData.meanings && gameData.meanings[word]) ? gameData.meanings[word] : "Definition captured strictly in memory.";

      item.innerHTML = `
        <div class="word-card-top">
          <h4>${word}</h4>
          <div class="word-audio-actions">
            <button class="word-action-btn pronounce-btn" id="pronounce-btn-${idx}" title="Pronounce '${word}'">
              <span class="action-icon">🔊</span> Pronounce
            </button>
            <button class="word-action-btn meaning-btn" id="meaning-btn-${idx}" title="Read meaning of '${word}'">
              <span class="action-icon">📖</span> Read Meaning
            </button>
          </div>
        </div>
        <p>${meaning}</p>
      `;

      // Pronounce word only
      const pronounceBtn = item.querySelector(`#pronounce-btn-${idx}`);
      if (pronounceBtn) {
        pronounceBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.speakWordOnly(word, idx);
        });
      }

      // Read word + meaning
      const meaningBtn = item.querySelector(`#meaning-btn-${idx}`);
      if (meaningBtn) {
        meaningBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.speakWordAndMeaning(word, meaning, idx);
        });
      }

      domCache.wordsList.appendChild(item);
    });

    this.setupSpeechToolbar(words, gameData.meanings || {});

    // Ensure speech stops on page departure
    window.addEventListener('beforeunload', () => this.stopAnySpeech());
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) this.stopAnySpeech();
    });
  },

  updateGlobalHistory() {
    if (typeof sharedState.recordSessionResult === 'function') {
      sharedState.recordSessionResult(this.state.gameData);
      return;
    }
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

  
  openShareModal() {
    const modal = document.getElementById('share-card-modal');
    if (!modal) return;

    const { gameData } = this.state;
    const username = gameData.username || localStorage.getItem('osmosis_user') || 'Scholar';
    const avatar = gameData.avatar || '🤓';
    const score = gameData.score || 0;
    const words = gameData.selectedWords || [];
    const wordsCount = words.length || 8;

    let totalTimeSecs = (gameData.totalTime || 0) / 1000;
    let rateOfAssimilation = 0;
    if (totalTimeSecs > 0) rateOfAssimilation = (score / totalTimeSecs).toFixed(1);
    else if (score > 0) rateOfAssimilation = score.toFixed(1);

    const totalMins = Math.floor(totalTimeSecs / 60);
    const totalSecs = Math.floor(totalTimeSecs % 60);
    const timeFormatted = totalMins > 0 ? `${totalMins}m ${totalSecs}s` : `${totalSecs}s`;

    // Populate Modal Elements
    const scoreEl = document.getElementById('cert-score');
    const wordsEl = document.getElementById('cert-words-count');
    const accuracyEl = document.getElementById('cert-accuracy');

    if (scoreEl) scoreEl.textContent = typeof score === 'number' ? score.toLocaleString() : score;
    if (wordsEl) wordsEl.textContent = wordsCount;
    if (accuracyEl) accuracyEl.textContent = '100%';

    modal.classList.add('active');

    // Close logic
    const closeBtn = document.getElementById('share-modal-close');
    if (closeBtn) closeBtn.onclick = () => modal.classList.remove('active');
    modal.onclick = (e) => {
      if (e.target === modal) modal.classList.remove('active');
    };

    const shareDataPayload = {
      username, avatar, score, rate: rateOfAssimilation, timeStr: timeFormatted, words, wordsCount
    };

    // Ivory "Share Score" button on the card
    const cardTrigger = document.getElementById('card-share-trigger-btn');
    if (cardTrigger) {
      cardTrigger.onclick = async () => {
        if (navigator.share) {
          try {
            await navigator.share({
              title: 'Osmosis STEM Game Score',
              text: `⭐ I scored ${score.toLocaleString()} points in Osmosis STEM! Words Mastered: ${words.join(', ')}. Can you beat my score?`,
              url: 'https://osmosis-game.web.app'
            });
            return;
          } catch (_) {}
        }
        this.generateAndDownloadShareCard(shareDataPayload, cardTrigger);
      };
    }

    // Download Image Button
    const downloadBtn = document.getElementById('download-cert-btn');
    if (downloadBtn) {
      downloadBtn.onclick = () => this.generateAndDownloadShareCard(shareDataPayload, downloadBtn);
    }

    // WhatsApp Button
    const waBtn = document.getElementById('whatsapp-share-btn');
    if (waBtn) {
      waBtn.onclick = () => {
        const wordsList = words.join(', ');
        const waText = `🏆 OSMOSIS STEM LEARNING ACHIEVEMENT 🏆\n\n⭐ Score: ${score.toLocaleString()} points\n📖 Words Treated: ${wordsCount}\n✅ Accuracy: 100%\nConcepts: ${wordsList}\n\nPlay Osmosis STEM Game here:\nhttps://osmosis-game.web.app`;
        window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(waText)}`, '_blank');
      };
    }

    // Copy Summary Button
    const copyBtn = document.getElementById('copy-summary-btn');
    if (copyBtn) {
      copyBtn.onclick = async () => {
        const wordsList = words.join(', ');
        const summary = `⭐ Osmosis Score: ${score.toLocaleString()} pts | 📖 Words Treated: ${wordsCount} | ✅ Accuracy: 100% | Concepts: ${wordsList} | https://osmosis-game.web.app`;
        try {
          if (navigator.clipboard) await navigator.clipboard.writeText(summary);
          copyBtn.innerHTML = '<span>✓</span> Copied!';
          setTimeout(() => { copyBtn.innerHTML = '<span>📋</span> Copy Text'; }, 2000);
        } catch (_) {}
      };
    }
  },

  generateAndDownloadShareCard(data, triggerBtn) {
    const origHtml = triggerBtn.innerHTML;
    triggerBtn.innerHTML = '<span>⏳</span> Rendering...';
    triggerBtn.style.pointerEvents = 'none';

    try {
      // 1000 x 1150 High-Res Square-format Social Card
      const W = 1000;
      const H = 1150;
      const canvas = document.createElement('canvas');
      canvas.width = W;
      canvas.height = H;
      const ctx = canvas.getContext('2d');

      // ── 1. Room Ambient Background (Cozy Study Room Vibe) ──
      const bgGrad = ctx.createRadialGradient(W / 2, H * 0.35, 100, W / 2, H / 2, 750);
      bgGrad.addColorStop(0, '#1d2a54');
      bgGrad.addColorStop(0.5, '#121a36');
      bgGrad.addColorStop(1, '#090d1c');
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, W, H);

      // Subtle Atom Orbits in Top-Right
      ctx.save();
      ctx.strokeStyle = 'rgba(147, 197, 253, 0.12)';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.ellipse(820, 200, 110, 42, Math.PI / 4, 0, Math.PI * 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.ellipse(820, 200, 110, 42, -Math.PI / 4, 0, Math.PI * 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.ellipse(820, 200, 110, 42, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();

      // ── 2. Top Golden Trophy Glow & Floating Trophy ──
      const trophyY = 165;
      const haloGrad = ctx.createRadialGradient(W / 2, trophyY, 20, W / 2, trophyY, 170);
      haloGrad.addColorStop(0, 'rgba(251, 191, 36, 0.45)');
      haloGrad.addColorStop(0.6, 'rgba(251, 191, 36, 0.12)');
      haloGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = haloGrad;
      ctx.fillRect(W / 2 - 200, trophyY - 180, 400, 360);

      // Sparkles around trophy
      ctx.font = '32px serif';
      ctx.fillStyle = '#fbbf24';
      ctx.fillText('✦', W / 2 - 130, trophyY - 10);
      ctx.font = '28px serif';
      ctx.fillText('★', W / 2 + 115, trophyY - 35);
      ctx.font = '20px serif';
      ctx.fillText('✦', W / 2 + 130, trophyY + 25);

      // Trophy Emoji Icon
      ctx.font = '100px serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('🏆', W / 2, trophyY);

      // ── 3. Frosted Acrylic Card Body ──
      const cX = 90, cY = 245, cW = W - 180, cH = 800, cR = 56;
      ctx.save();
      ctx.beginPath();
      ctx.roundRect(cX, cY, cW, cH, cR);

      // Translucent frosted glass fill
      const glassGrad = ctx.createLinearGradient(cX, cY, cX + cW, cY + cH);
      glassGrad.addColorStop(0, 'rgba(255, 255, 255, 0.18)');
      glassGrad.addColorStop(0.5, 'rgba(255, 255, 255, 0.08)');
      glassGrad.addColorStop(1, 'rgba(255, 255, 255, 0.04)');
      ctx.fillStyle = glassGrad;
      ctx.fill();

      // Crisp glass border highlight
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.45)';
      ctx.lineWidth = 3.5;
      ctx.stroke();
      ctx.restore();

      // ── 4. Pill Header: —— Your Score —— ──
      const pillY = cY + 68;
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.35)';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(cX + 55, pillY);
      ctx.lineTo(W / 2 - 165, pillY);
      ctx.moveTo(W / 2 + 165, pillY);
      ctx.lineTo(cX + cW - 55, pillY);
      ctx.stroke();

      // "Your Score" pill
      ctx.save();
      const pW = 300, pH = 56, pR = 28;
      ctx.beginPath();
      ctx.roundRect(W / 2 - pW / 2, pillY - pH / 2, pW, pH, pR);
      const pillGrad = ctx.createLinearGradient(0, pillY - pH / 2, 0, pillY + pH / 2);
      pillGrad.addColorStop(0, '#3957b0');
      pillGrad.addColorStop(1, '#20326d');
      ctx.fillStyle = pillGrad;
      ctx.fill();
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.restore();

      ctx.font = 'bold 26px -apple-system, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('Your Score', W / 2, pillY);

      // ── 5. Star + Giant Score + points ──
      const scoreY = pillY + 115;
      ctx.font = '64px serif';
      ctx.textAlign = 'right';
      ctx.textBaseline = 'middle';
      ctx.fillText('⭐', W / 2 - 120, scoreY);

      ctx.font = '900 96px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      const scoreStr = typeof data.score === 'number' ? data.score.toLocaleString() : (data.score || '860');
      ctx.fillText(scoreStr, W / 2, scoreY);

      ctx.font = '600 30px -apple-system, sans-serif';
      ctx.fillStyle = '#cbd5e1';
      ctx.textAlign = 'left';
      ctx.fillText('points', W / 2 + 125, scoreY + 18);

      // ── 6. Two Metric Cards: Words Treated & Accuracy ──
      const cardGridY = scoreY + 95;
      const cardW = 370, cardH = 175, cardR = 32;
      const leftCardX = cX + 35;
      const rightCardX = cX + cW - 35 - cardW;

      // Left Box: Words Treated
      ctx.save();
      ctx.beginPath();
      ctx.roundRect(leftCardX, cardGridY, cardW, cardH, cardR);
      ctx.fillStyle = 'rgba(20, 32, 68, 0.42)';
      ctx.fill();
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.25)';
      ctx.lineWidth = 2.5;
      ctx.stroke();
      ctx.restore();

      ctx.font = '44px serif';
      ctx.textAlign = 'center';
      ctx.fillText('📖', leftCardX + cardW / 2, cardGridY + 48);
      ctx.font = 'bold 44px -apple-system, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.fillText(String(data.wordsCount || 8), leftCardX + cardW / 2, cardGridY + 106);
      ctx.font = '600 18px -apple-system, sans-serif';
      ctx.fillStyle = '#cbd5e1';
      ctx.fillText('Words Treated', leftCardX + cardW / 2, cardGridY + 144);

      // Right Box: Accuracy
      ctx.save();
      ctx.beginPath();
      ctx.roundRect(rightCardX, cardGridY, cardW, cardH, cardR);
      ctx.fillStyle = 'rgba(20, 32, 68, 0.42)';
      ctx.fill();
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.25)';
      ctx.lineWidth = 2.5;
      ctx.stroke();
      ctx.restore();

      ctx.font = '44px serif';
      ctx.textAlign = 'center';
      ctx.fillText('✅', rightCardX + cardW / 2, cardGridY + 48);
      ctx.font = 'bold 44px -apple-system, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.fillText('100%', rightCardX + cardW / 2, cardGridY + 106);
      ctx.font = '600 18px -apple-system, sans-serif';
      ctx.fillStyle = '#cbd5e1';
      ctx.fillText('Accuracy', rightCardX + cardW / 2, cardGridY + 144);

      // ── 7. Motivational Lines ──
      const motivY = cardGridY + cardH + 75;
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.35)';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(W / 2 - 180, motivY - 14);
      ctx.lineTo(W / 2 - 95, motivY - 14);
      ctx.moveTo(W / 2 + 95, motivY - 14);
      ctx.lineTo(W / 2 + 180, motivY - 14);
      ctx.stroke();

      ctx.font = 'bold 28px -apple-system, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.fillText('Great job!', W / 2, motivY - 14);

      ctx.font = 'italic 21px -apple-system, sans-serif';
      ctx.fillStyle = '#cbd5e1';
      ctx.fillText('Keep learning, keep growing.', W / 2, motivY + 22);

      // ── 8. Ivory Pill Button: Share Score ──
      const btnY = motivY + 75;
      const bW = cW - 80, bH = 76, bR = 38;
      const btnX = cX + 40;

      ctx.save();
      ctx.beginPath();
      ctx.roundRect(btnX, btnY, bW, bH, bR);
      ctx.fillStyle = '#fef3c7';
      ctx.fill();
      ctx.restore();

      ctx.font = 'bold 28px -apple-system, sans-serif';
      ctx.fillStyle = '#1e293b';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('🔗  |  Share Score', W / 2, btnY + bH / 2);

      // ── 9. Watermark Footer ──
      ctx.font = '14px -apple-system, sans-serif';
      ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
      ctx.textAlign = 'center';
      ctx.fillText('OSMOSIS STEM RAPID LEARNING GAME • NaCCA • CSIR • GAST ENDORSED', W / 2, H - 42);

      // ── 10. Trigger PNG Download ──
      const url = canvas.toDataURL('image/png');
      const a = document.createElement('a');
      a.href = url;
      a.download = `Osmosis_Score_${scoreStr}.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      triggerBtn.innerHTML = '<span>✅</span> Downloaded!';
      setTimeout(() => { triggerBtn.innerHTML = origHtml; triggerBtn.style.pointerEvents = 'auto'; }, 2000);
    } catch (err) {
      console.warn('Canvas export failed:', err);
      triggerBtn.innerHTML = origHtml;
      triggerBtn.style.pointerEvents = 'auto';
    }
  },

  attachListeners() {
    const { domCache, gameData } = this.state;

    if (domCache.playAgainBtn) {
      domCache.playAgainBtn.addEventListener('click', () => {
        this.stopAnySpeech();
        if (typeof AudioManager !== 'undefined') AudioManager.play('click');

        const isPersonalStudy = gameData.personalStudyMode;

        if (typeof sharedState.clearGameSession === 'function') {
          sharedState.clearGameSession(true);
        }

        const targetUrl = isPersonalStudy ? '02b_personal_study_setup.html' : '02_campaign_setup.html';

        setTimeout(() => {
          if (typeof window.navigateWithTransition === 'function') navigateWithTransition(targetUrl);
          else window.location.href = targetUrl;
        }, 100);
      });
    }

    const shareBtn = document.getElementById('share-score-btn');
    if (shareBtn) {
      shareBtn.addEventListener('click', async () => {
        const wordsCount = (gameData.selectedWords || []).length;
        const text = `I just scored ${gameData.score || 0} pts mastering ${wordsCount} STEM terms on Osmosis! Can you beat my score?`;
        const url = window.location.href.replace(/11_results\.html.*$/i, 'index.html');
        try {
          if (navigator.share) {
            await navigator.share({ title: 'Osmosis STEM Score', text, url });
          } else if (navigator.clipboard && navigator.clipboard.writeText) {
            await navigator.clipboard.writeText(`${text} ${url}`);
            shareBtn.textContent = '✓ Copied!';
            setTimeout(() => { shareBtn.textContent = '📤 Share Score'; }, 2000);
          }
        } catch (e) {}
      });
    }

    if (domCache.goHomeBtn) {
      domCache.goHomeBtn.addEventListener('click', () => {
        this.stopAnySpeech();
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
