// =====================================================================
// FILE: multiplayer_results.js
// =====================================================================

document.addEventListener('DOMContentLoaded', () => {
  const gameData = sharedState.load();
  const cardsList = document.getElementById('cards-list');
  const modalOverlay = document.getElementById('modal-overlay');
  const modalX = document.getElementById('modal-x');
  const modalAvatar = document.getElementById('modal-avatar');
  const modalName = document.getElementById('modal-name');
  const modalBody = document.getElementById('modal-body');
  const homeBtn = document.getElementById('mp-home-btn');
  const playBtn = document.getElementById('mp-play-btn');

  // ── Navigation ──
  homeBtn.addEventListener('click', () => {
    if (typeof window.navigateWithTransition === 'function') navigateWithTransition('01_home_menu.html');
    else window.location.href = '01_home_menu.html';
  });

  playBtn.addEventListener('click', () => {
    if (typeof window.navigateWithTransition === 'function') navigateWithTransition('multiplayer_lobby.html');
    else window.location.href = 'multiplayer_lobby.html';
  });

  // ── Play Victory Fanfare ──
  if (typeof AudioManager !== 'undefined') {
    AudioManager.init();
    AudioManager.play('fanfare');
  }

  // ── Modal ──
  function closeModal() { modalOverlay.classList.remove('active'); }
  modalX.addEventListener('click', closeModal);
  modalOverlay.addEventListener('click', (e) => { if (e.target === modalOverlay) closeModal(); });

  function openModal(player) {
    modalAvatar.textContent = player.avatar || '🤓';
    modalName.textContent = player.name;
    modalBody.innerHTML = '';

    const words = player.words || [];
    const meanings = player.meanings || {};

    if (words.length === 0) {
      modalBody.innerHTML = '<p class="modal-empty">No words recorded yet for this player.</p>';
    } else {
      words.forEach(word => {
        const def = meanings[word] || 'Definition not available.';
        const row = document.createElement('div');
        row.className = 'modal-word-row';
        row.innerHTML = `<div class="modal-word-name">${word}</div><div class="modal-word-def">${def}</div>`;
        modalBody.appendChild(row);
      });
    }
    modalOverlay.classList.add('active');
  }

  // ── Time helper ──
  function formatTime(seconds) {
    if (!seconds && seconds !== 0) return '—';
    if (typeof sharedState !== 'undefined' && sharedState.getFormattedTime) {
      return sharedState.getFormattedTime(seconds);
    }
    const m = Math.floor((seconds || 0) / 60);
    const s = (seconds || 0) % 60;
    return `${m}m ${s}s`;
  }

  // ── Render slim player cards ──
  const medals = ['🥇', '🥈', '🥉'];
  const rankClasses = ['rank-1', 'rank-2', 'rank-3'];

  function renderCards(players) {
    // Sort: score desc, then time asc
    const sorted = [...players].sort((a, b) => {
      const scoreA = a.score || 0;
      const scoreB = b.score || 0;
      if (scoreB !== scoreA) return scoreB - scoreA;
      return (a.time || 0) - (b.time || 0);
    });

    cardsList.innerHTML = '';

    sorted.forEach((player, i) => {
      const rank = i + 1;
      const rankClass = rankClasses[i] || '';
      const medal = medals[i] || '';
      const isFinished = player.isFinished || player.finished || (player.score !== undefined && player.score !== null && player.time > 0);
      const currentScore = player.score || 0;
      const timeStr = formatTime(player.time || 0);
      const avatar = player.avatar || '🤓';
      const isWinner = rank === 1;

      const card = document.createElement('div');
      card.className = `player-card ${rankClass}`;
      card.style.animationDelay = `${i * 0.08}s`;

      card.innerHTML = `
        <div class="rank-badge">
          ${medal ? `<span class="rank-medal">${medal}</span>` : `<span class="rank-num">#${rank}</span>`}
        </div>

        <div class="card-avatar">${avatar}</div>

        <div class="card-info">
          <div class="card-name">
            ${player.name}
            ${isWinner ? '<span class="winner-tag">Winner</span>' : ''}
          </div>
          <div class="card-meta">
            ${isFinished ? `
              <span class="meta-item">⏱ ${timeStr}</span>
              <span class="meta-item">📚 ${player.words ? player.words.length : 0} words</span>
            ` : `
              <span class="in-progress-dot">Playing Stage ${(player.currentStage || 1)}</span>
            `}
          </div>
        </div>

        <div class="card-score-block">
          <div class="card-score-val">${currentScore.toLocaleString()}</div>
          <div class="card-score-label">PTS</div>
        </div>

        <div class="card-chevron">❯</div>
      `;

      // Click card to open words modal
      card.addEventListener('click', () => openModal(player));

      cardsList.appendChild(card);
    });
  }

  // ── Socket connection ──
  if (typeof io !== 'undefined' && gameData.currentRoomId) {
    const socket = io();

    // Rejoin room
    socket.emit('join_room', {
      roomId: gameData.currentRoomId,
      username: gameData.username || localStorage.getItem('osmosis_user') || 'Guest',
      avatar: gameData.avatar || '🤓'
    });

    // Send updated score
    socket.emit('update_score', {
      roomId: gameData.currentRoomId,
      score: gameData.score || 0,
      username: gameData.username || localStorage.getItem('osmosis_user') || 'Guest',
      time: gameData.totalTime || 0,
      words: gameData.selectedWords || [],
      meanings: gameData.meanings || {},
      isFinished: true
    });

    socket.on('leaderboard_update', (data) => {
      renderCards(data.players);
    });
  } else {
    // Fallback: local session storage
    const stored = sessionStorage.getItem('mp_final_results');
    if (stored) {
      try { renderCards(JSON.parse(stored)); } catch (e) {}
    } else {
      // Demo preview if standalone
      renderCards([
        { name: gameData.username || 'You', score: gameData.score || 1250, time: gameData.totalTime || 145, avatar: gameData.avatar || '⚡', words: gameData.selectedWords || ['osmosis', 'mitosis'], isFinished: true },
        { name: 'Alex', score: 980, time: 180, avatar: '🔥', words: ['nucleus', 'ribosome'], isFinished: true },
        { name: 'Chen', score: 620, time: 90, avatar: '🧪', currentStage: 5, isFinished: false }
      ]);
    }
  }
});
