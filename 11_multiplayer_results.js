// =====================================================================
// FILE: 11_multiplayer_results.js (The Battle Arena Controller)
// =====================================================================

const MultiplayerResults = {
  state: {
    gameData: null,
    players: [],
    socket: null,
    roomId: null
  },

  init() {
    this.state.gameData = sharedState.load();
    this.state.roomId = this.state.gameData.currentRoomId;

    if (!this.state.roomId) {
      window.location.href = '01_home_menu.html';
      return;
    }

    sharedState.stopTimer();
    this.initSocket();
    this.attachListeners();
  },

  initSocket() {
    if (typeof io === 'undefined') return;
    
    this.state.socket = io();
    const myName = localStorage.getItem('osmosis_user') || 'Guest';
    const myAvatar = this.state.gameData.avatar || '🤓';

    this.state.socket.emit('join_room', { 
      roomId: this.state.roomId, 
      username: myName,
      avatar: myAvatar
    });

    // Send final score
    this.state.socket.emit('update_score', {
      roomId: this.state.roomId,
      score: this.state.gameData.score || 0,
      username: myName,
      time: this.state.gameData.totalTime || 0,
      words: this.state.gameData.selectedWords || [],
      meanings: this.state.gameData.meanings || {}
    });

    this.state.socket.on('leaderboard_update', (data) => {
      this.state.players = data.players;
      this.renderLeaderboard();
    });
  },

  getOrdinal(n) {
    const s = ["th", "st", "nd", "rd"], v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  },

  renderLeaderboard() {
    const listEl = document.getElementById('leaderboard-list');
    if (!listEl) return;

    // Sort players by score (descending), then by time (ascending) to break ties
    const sorted = [...this.state.players].sort((a, b) => {
      if ((b.score || 0) !== (a.score || 0)) {
        return (b.score || 0) - (a.score || 0);
      }
      return (a.time || 0) - (b.time || 0); // Lower time wins tie
    });
    
    listEl.innerHTML = '';
    
    sorted.forEach((player, index) => {
      const rank = index + 1;
      const rankOrdinal = this.getOrdinal(rank);
      const card = document.createElement('div');
      card.className = `rank-card rank-${rank}`;
      
      const avatar = player.avatar || '🤓';
      const score = player.score !== undefined ? player.score : '...';
      const timeStr = player.time !== undefined ? sharedState.getFormattedTime(player.time) : '...';
      
      let trophy = '';
      if (rank === 1) trophy = '🏆';
      else if (rank === 2) trophy = '🥈';
      else if (rank === 3) trophy = '🥉';
      else trophy = '🏅';

      card.innerHTML = `
        <div class="rank-number">${rankOrdinal}</div>
        <div class="player-avatar">${avatar}</div>
        <div class="player-info">
          <p class="player-name">${player.name}</p>
          <p class="player-score">${score} pts | Time: ${timeStr}</p>
          <p style="font-size: 0.7rem; color: rgba(255,255,255,0.6); margin-top: 2px;">View Learning</p>
        </div>
        <div style="font-size: 1.8rem;">${trophy}</div>
      `;

      card.addEventListener('click', () => this.showPlayerWords(player));
      
      listEl.appendChild(card);
    });

    if (sorted.length < 2) {
      const p = document.createElement('p');
      p.className = 'waiting-text';
      p.textContent = 'Waiting for other teammates to finish...';
      listEl.appendChild(p);
    }
  },

  showPlayerWords(player) {
    const modal = document.getElementById('word-modal');
    const nameEl = document.getElementById('modal-player-name');
    const listEl = document.getElementById('modal-word-list');
    
    if (!modal || !nameEl || !listEl) return;
    if (typeof AudioManager !== 'undefined') AudioManager.play('chip');

    nameEl.textContent = `${player.name}'s Learning Achieved`;
    listEl.innerHTML = '';

    const words = player.words || [];
    const meanings = player.meanings || {};

    if (words.length === 0) {
      listEl.innerHTML = '<p style="text-align:center; font-style:italic; padding: 2rem;">No words collected yet.</p>';
    } else {
      words.forEach(word => {
        const item = document.createElement('div');
        item.className = 'word-item';
        const m = meanings[word] || 'Definition stored in memory.';
        item.innerHTML = `<h4>${word}</h4><p>${m}</p>`;
        listEl.appendChild(item);
      });
    }

    modal.classList.add('active');
  },

  attachListeners() {
    const homeBtn = document.getElementById('go-home-btn');
    const playAgainBtn = document.getElementById('play-again-btn');

    if (playAgainBtn) {
      playAgainBtn.addEventListener('click', () => {
        if (typeof AudioManager !== 'undefined') AudioManager.play('click');
        
        // Reset game stats but keep multiplayer active
        const data = sharedState.load();
        data.score = 0;
        data.usedLetters = [];
        data.selectedWords = [];
        data.stageScores = {};
        data.meanings = {};
        data.lastLength = null;
        data.totalTime = 0;
        data.sessionStartedAt = null;
        sharedState.save(data);
        
        if (typeof window.navigateWithTransition === 'function') navigateWithTransition('02_campaign_setup.html');
        else window.location.href = '02_campaign_setup.html';
      });
    }

    if (homeBtn) {
      homeBtn.addEventListener('click', () => {
        if (typeof AudioManager !== 'undefined') AudioManager.play('click');
        
        // Reset multiplayer state before returning
        const data = sharedState.load();
        data.multiplayerMode = false;
        data.currentRoomId = null;
        sharedState.save(data);
        
        window.location.href = '01_home_menu.html';
      });
    }
  }
};

document.addEventListener('DOMContentLoaded', () => MultiplayerResults.init());
