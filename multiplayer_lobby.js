// =====================================================================
// FILE: multiplayer_lobby.js (The Connection Hub)
// =====================================================================

document.addEventListener('DOMContentLoaded', () => {
  const gameData = sharedState.load();

  // UI Elements
  const modeHost = document.getElementById('mode-host');
  const modeJoin = document.getElementById('mode-join');
  const hostSection = document.getElementById('host-section');
  const joinSection = document.getElementById('join-section');
  const roomIdEl = document.getElementById('room-id');
  const hostPlayerName = document.getElementById('host-player-name');
  const startBtn = document.getElementById('start-multi-btn');

  if (gameData.username) {
    const avatar = gameData.avatar || '🤓';
    hostPlayerName.textContent = `${avatar} ${gameData.username}`;
  }

  // 1. Generate Room Code Immediately (Before Socket)
  function generateRoomCode() {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    let result = '';
    for (let i = 0; i < 6; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  let currentRoomId = generateRoomCode();
  if (roomIdEl) roomIdEl.textContent = currentRoomId;

  const urlParams = new URLSearchParams(window.location.search);
  const invitedRoom = (urlParams.get('room') || sessionStorage.getItem('osmosis_pending_room') || '').trim().toUpperCase();
  if (invitedRoom) sessionStorage.removeItem('osmosis_pending_room');

  // Copy Challenge Link button
  const copyInviteBtn = document.getElementById('copy-invite-btn');
  const inviteStatus = document.getElementById('invite-status');
  if (copyInviteBtn) {
    copyInviteBtn.addEventListener('click', async () => {
      const basePath = window.location.href.replace(/multiplayer_lobby\.html.*$/i, '');
      const inviteUrl = `${basePath}index.html?room=${encodeURIComponent(currentRoomId)}`;
      try {
        if (navigator.share) {
          await navigator.share({
            title: 'Osmosis STEM Battle',
            text: `Join my Osmosis STEM battle! Room: ${currentRoomId}`,
            url: inviteUrl
          });
        } else if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(inviteUrl);
          if (inviteStatus) inviteStatus.textContent = `Copied invite link for ${currentRoomId}!`;
          copyInviteBtn.textContent = '✓ Link Copied!';
          setTimeout(() => { copyInviteBtn.textContent = '🔗 Copy Challenge Link'; }, 2000);
        }
      } catch (e) {
        if (inviteStatus) inviteStatus.textContent = `Room Code: ${currentRoomId}`;
      }
    });
  }

  // 2. Initialize Connection (with safety)
  let socket;
  try {
    if (typeof io !== 'undefined') {
      const serverUrl = (typeof sharedState.getSocketServerUrl === 'function') ? sharedState.getSocketServerUrl() : undefined;
      socket = serverUrl ? io(serverUrl) : io();

      // Auto-host unless joining via ?room= invite link
      if (!invitedRoom) {
        socket.emit('create_room', {
          roomId: currentRoomId,
          username: gameData.username || 'Player',
          avatar: gameData.avatar || '🤓'
        });
      }

      // Server Listeners
      socket.on('player_joined', (data) => {
        const extraPlayers = document.getElementById('extra-players');
        const guestPlayerList = document.getElementById('guest-player-list');
        const guestStatus = document.getElementById('guest-status-container');
        const confirmJoinBtn = document.getElementById('confirm-join-btn');
        const joinInput = document.getElementById('join-code-input');

        // Update Host UI
        if (extraPlayers && Array.isArray(data.players)) {
          extraPlayers.innerHTML = '';
          data.players.forEach(p => {
            if (p.name !== gameData.username) {
              const div = document.createElement('div');
              div.className = 'player-entry';
              const pAvatar = sharedState.escapeHTML(p.avatar || '🤓');
              const pName = sharedState.escapeHTML(p.name || 'Player');
              div.innerHTML = `<span class="player-name">${pAvatar} ${pName}</span><span class="player-status">Connected</span>`;
              extraPlayers.appendChild(div);
            }
          });
        }

        // Update Guest UI (if they are in join mode and this is their room)
        if (modeJoin && modeJoin.classList.contains('active')) {
          if (confirmJoinBtn) confirmJoinBtn.style.display = 'none';
          if (joinInput) joinInput.style.display = 'none';
          if (guestStatus) guestStatus.style.display = 'block';

          if (guestPlayerList && Array.isArray(data.players)) {
            guestPlayerList.innerHTML = '';
            data.players.forEach(p => {
              const div = document.createElement('div');
              div.className = 'player-entry';
              const pAvatar = sharedState.escapeHTML(p.avatar || '🤓');
              const pName = sharedState.escapeHTML(p.name || 'Player');
              const isMe = p.name === gameData.username;
              div.innerHTML = `<span class="player-name">${pAvatar} ${pName} ${isMe ? '(You)' : ''}</span><span class="player-status">Connected</span>`;
              guestPlayerList.appendChild(div);
            });
          }
        }

        // Enable Start button if someone joined
        if (startBtn) {
          startBtn.disabled = false;
          startBtn.textContent = "Start";
        }
      });

      socket.on('error_message', (msg) => {
        if (typeof showModal === 'function') showModal('Room Notice', msg);
        else console.warn('Room Notice:', msg);
        const confirmJoinBtn = document.getElementById('confirm-join-btn');
        if (confirmJoinBtn) {
          confirmJoinBtn.textContent = "Establish Link";
          confirmJoinBtn.disabled = false;
          confirmJoinBtn.style.display = '';
        }
        const joinInput = document.getElementById('join-code-input');
        if (joinInput) joinInput.style.display = '';
      });

      socket.on('game_started', () => {
        gameData.multiplayerMode = true;
        gameData.currentRoomId = currentRoomId;
        gameData.score = 0;
        gameData.usedLetters = [];
        gameData.selectedWords = [];
        gameData.stageScores = {};
        gameData.meanings = {};
        gameData.lastLength = null;
        gameData.totalTime = 0;
        gameData.sessionStartedAt = null;
        sharedState.save(gameData);
        window.location.href = '02_campaign_setup.html';
      });

      // Handle Host Start
      if (startBtn) {
        startBtn.addEventListener('click', () => {
          socket.emit('start_game', currentRoomId);
        });
      }

      // Handle Join Confirmation
      const confirmJoinBtn = document.getElementById('confirm-join-btn');
      function attemptJoin(code) {
        const clean = String(code || '').trim().toUpperCase();
        if (clean.length < 6) {
          if (typeof showModal === 'function') showModal('Invalid Code', 'Enter a valid 6-character room code.');
          return;
        }
        if (confirmJoinBtn) {
          confirmJoinBtn.textContent = "Connecting...";
          confirmJoinBtn.disabled = true;
        }
        currentRoomId = clean;
        socket.emit('join_room', {
          roomId: clean,
          username: gameData.username || 'Guest',
          avatar: gameData.avatar || '🤓'
        });
      }

      if (confirmJoinBtn) {
        confirmJoinBtn.addEventListener('click', () => {
          attemptJoin(document.getElementById('join-code-input').value);
        });
      }

      // Auto-join if invited via ?room=CODE
      if (invitedRoom && invitedRoom.length >= 6 && modeJoin && modeHost && hostSection && joinSection) {
        modeJoin.classList.add('active');
        modeHost.classList.remove('active');
        hostSection.style.display = 'none';
        joinSection.style.display = 'block';
        const joinInput = document.getElementById('join-code-input');
        if (joinInput) joinInput.value = invitedRoom;
        attemptJoin(invitedRoom);
      }
    } else {
      console.warn("Socket.io not loaded. Multiplayer features disabled.");
      if (startBtn) {
        startBtn.textContent = "Server Offline";
        startBtn.disabled = true;
      }
      if (inviteStatus) {
        inviteStatus.textContent = "Live multiplayer server offline on static hosting. Run Node server for live rooms.";
      }
    }
  } catch (err) {
    console.error("Socket initialization failed:", err);
  }

  // 3. Mode Toggle Logic
  if (modeHost && modeJoin && hostSection && joinSection) {
    modeHost.addEventListener('click', () => {
      if (modeHost.classList.contains('active')) return;

      modeHost.classList.add('active');
      modeJoin.classList.remove('active');
      hostSection.style.display = 'block';
      joinSection.style.display = 'none';

      // Re-generate if hosting a new session
      currentRoomId = generateRoomCode();
      if (roomIdEl) roomIdEl.textContent = currentRoomId;
      if (socket) socket.emit('create_room', {
        roomId: currentRoomId,
        username: gameData.username || 'Player',
        avatar: gameData.avatar || '🤓'
      });
    });

    modeJoin.addEventListener('click', () => {
      modeJoin.classList.add('active');
      modeHost.classList.remove('active');
      hostSection.style.display = 'none';
      joinSection.style.display = 'block';
    });
  }
});
