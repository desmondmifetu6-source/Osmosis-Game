// =====================================================================
// FILE: multiplayer_results.js
// =====================================================================

document.addEventListener('DOMContentLoaded', () => {
  const gameData = sharedState.load();
  const cardsGrid = document.getElementById('cards-grid');
  const liveBadge = document.getElementById('live-badge');
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
    if (typeof sharedState !== 'undefined' && sharedState.getFormattedTime) {
      return sharedState.getFormattedTime(seconds);
    }
    const m = Math.floor((seconds || 0) / 60);
    const s = (seconds || 0) % 60;
    return `${m}m ${s}s`;
  }

  // ── Render cards ──
  const medals = ['🥇', '🥈', '🥉'];
  const rankClasses = ['rank-1', 'rank-2', 'rank-3'];

  function renderCards(players) {
    // Sort: score desc, then time asc
    const sorted = [...players].sort((a, b) => {
      if ((b.score || 0) !== (a.score || 0)) return (b.score || 0) - (a.score || 0);
      return (a.time || 0) - (b.time || 0);
    });

    cardsGrid.innerHTML = '';

    sorted.forEach((player, i) => {
      const rank = i + 1;
      const rankClass = rankClasses[i] || '';
      const medal = medals[i] || '';
      const hasScore = player.score !== undefined && player.score !== null;
      const avatar = player.avatar || '🤓';
      const isWinner = rank === 1;
      const scoreDisplay = hasScore ? player.score.toLocaleString() : '...';
      const timeStr = hasScore ? formatTime(player.time || 0) : '—';

      const card = document.createElement('div');
      card.className = `player-card ${rankClass}`;
      card.style.animationDelay = `${i * 0.1}s`;

      card.innerHTML = `
        <div class="rank-pill">${rank === 1 ? '👑 1st' : rank === 2 ? '🥈 2nd' : rank === 3 ? '🥉 3rd' : `#${rank}`}</div>
        <span class="card-medal">${medal}</span>
        <span class="card-avatar">${avatar}</span>
        <div class="card-name">${player.name}</div>
        ${isWinner ? '<div class="winner-crown">Winner</div>' : '<div style="margin-bottom:1rem;"></div>'}
        <div class="card-divider"></div>
        ${hasScore ? `
          <div class="card-score">${scoreDisplay}</div>
          <div class="card-pts">points</div>
          <div class="card-time">⏱ ${timeStr}</div>
          <button class="view-words-btn">📚 View Words Learned</button>
        ` : `
          <div class="card-time" style="margin-top:1rem;"><span class="pending-label">Awaiting results...</span></div>
        `}
      `;

      if (hasScore) {
        const wordsBtn = card.querySelector('.view-words-btn');
        wordsBtn.addEventListener('click', (e) => { e.stopPropagation(); openModal(player); });
        card.addEventListener('click', () => openModal(player));
      }

      cardsGrid.appendChild(card);
    });

    // Hide LIVE badge when all finished
    const allDone = sorted.every(p => p.score !== undefined && p.score !== null);
    if (allDone && liveBadge) liveBadge.style.display = 'none';
  }

  // ── Socket connection ──
  if (typeof io !== 'undefined' && gameData.currentRoomId) {
    const socket = io();

    // Rejoin room so the server knows we're here
    socket.emit('join_room', {
      roomId: gameData.currentRoomId,
      username: gameData.username || localStorage.getItem('osmosis_user') || 'Guest',
      avatar: gameData.avatar || '🤓'
    });

    // Push our final score to the room
    socket.emit('update_score', {
      roomId: gameData.currentRoomId,
      score: gameData.score || 0,
      username: gameData.username || localStorage.getItem('osmosis_user') || 'Guest',
      time: gameData.totalTime || 0,
      words: gameData.selectedWords || [],
      meanings: gameData.meanings || {}
    });

    socket.on('leaderboard_update', (data) => {
      renderCards(data.players);
    });
  } else {
    // Fallback: try sessionStorage data saved by 11_results.js
    const stored = sessionStorage.getItem('mp_final_results');
    if (stored) {
      try { renderCards(JSON.parse(stored)); } catch (e) { /* ignore */ }
    }
  }
});
