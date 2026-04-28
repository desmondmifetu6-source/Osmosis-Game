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
    hostPlayerName.textContent = gameData.username;
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

  // 2. Initialize Connection (with safety)
  let socket;
  try {
    if (typeof io !== 'undefined') {
      socket = io(); 
      
      // Auto-host on load
      socket.emit('create_room', { 
        roomId: currentRoomId, 
        username: gameData.username || 'Player',
        avatar: gameData.avatar || '👦'
      });

      // Server Listeners
      socket.on('player_joined', (data) => {
        const extraPlayers = document.getElementById('extra-players');
        if (extraPlayers) {
          extraPlayers.innerHTML = ''; // Clear "Waiting..."
          data.players.forEach(p => {
            if (p.name !== gameData.username) {
              const div = document.createElement('div');
              div.className = 'player-entry';
              const pAvatar = p.avatar || '👦';
              div.innerHTML = `<span class="player-name">${pAvatar} ${p.name}</span><span class="player-status">Connected</span>`;
              extraPlayers.appendChild(div);
            }
          });
        }

        // Enable Start button if someone joined
        if (startBtn) {
          startBtn.disabled = false;
          startBtn.textContent = "Ignite Game!";
        }
      });

      socket.on('error_message', (msg) => {
        alert(msg);
      });

      socket.on('game_started', () => {
        gameData.multiplayerMode = true;
        gameData.currentRoomId = currentRoomId;
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
      if (confirmJoinBtn) {
        confirmJoinBtn.addEventListener('click', () => {
          const code = document.getElementById('join-code-input').value.trim().toUpperCase();
          if (code.length < 6) return alert("Enter a valid 6-char code.");
          
          currentRoomId = code;
          socket.emit('join_room', { 
            roomId: code, 
            username: gameData.username || 'Guest',
            avatar: gameData.avatar || '👦'
          });
        });
      }
    } else {
      console.warn("Socket.io not loaded. Multiplayer features disabled.");
      if (startBtn) startBtn.textContent = "Offline Mode (No Server)";
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
        avatar: gameData.avatar || '👦'
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
