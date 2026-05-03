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
      time: this.state.gameData.totalTime || 0
    });

    this.state.socket.on('leaderboard_update', (data) => {
      this.state.players = data.players;
      this.renderLeaderboard();
    });
  },

  renderLeaderboard() {
    const listEl = document.getElementById('leaderboard-list');
    if (!listEl) return;

    // Sort players by score (descending)
    const sorted = [...this.state.players].sort((a, b) => (b.score || 0) - (a.score || 0));
    
    listEl.innerHTML = '';
    
    sorted.forEach((player, index) => {
      const rank = index + 1;
      const card = document.createElement('div');
      card.className = `rank-card rank-${rank}`;
      
      const avatar = player.avatar || '🤓';
      const score = player.score !== undefined ? player.score : '...';
      const timeStr = player.time !== undefined ? sharedState.getFormattedTime(player.time) : '...';
      
      // Select trophy based on rank
      let trophy = '';
      if (rank === 1) trophy = '🏆';
      else if (rank === 2) trophy = '🥈';
      else if (rank === 3) trophy = '🥉';
      else trophy = '🏅';

      card.innerHTML = `
        <div class="rank-number">${rank}</div>
        <div class="player-avatar">${avatar}</div>
        <div class="player-info">
          <p class="player-name">${player.name}</p>
          <p class="player-score">${score} pts | Time: ${timeStr}</p>
        </div>
        <div style="font-size: 2.5rem;">${trophy}</div>
      `;
      
      listEl.appendChild(card);
    });

    if (sorted.length < 2) {
      const p = document.createElement('p');
      p.className = 'waiting-text';
      p.textContent = 'Waiting for other teammates to finish...';
      listEl.appendChild(p);
    }
  },

  attachListeners() {
    const homeBtn = document.getElementById('go-home-btn');
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
