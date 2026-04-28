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
  
  if (gameData.username) {
    hostPlayerName.textContent = gameData.username;
  }

  // 1. Initialize Connection
  const socket = io(); // Connects to the server we just built
  let currentRoomId = null;

  // 2. Mode Toggle Logic
  modeHost.addEventListener('click', () => {
    modeHost.classList.add('active');
    modeJoin.classList.remove('active');
    hostSection.style.display = 'block';
    joinSection.style.display = 'none';
    
    // Generate and register room
    currentRoomId = generateRoomCode();
    roomIdEl.textContent = currentRoomId;
    socket.emit('create_room', { roomId: currentRoomId, username: gameData.username || 'Player' });
  });

  modeJoin.addEventListener('click', () => {
    modeJoin.classList.add('active');
    modeHost.classList.remove('active');
    hostSection.style.display = 'none';
    joinSection.style.display = 'block';
  });

  // 3. Mock Room Code Generation
  function generateRoomCode() {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    let result = '';
    for (let i = 0; i < 6; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  // Auto-host on load
  currentRoomId = generateRoomCode();
  roomIdEl.textContent = currentRoomId;
  socket.emit('create_room', { roomId: currentRoomId, username: gameData.username || 'Player' });

  // 4. Real Join Logic
  document.getElementById('confirm-join-btn').addEventListener('click', () => {
    const code = document.getElementById('join-code-input').value.trim().toUpperCase();
    if (code.length < 6) return alert("Enter a valid 6-char code.");
    
    currentRoomId = code;
    socket.emit('join_room', { roomId: code, username: gameData.username || 'Guest' });
  });

  // 5. Server Listeners
  socket.on('player_joined', (data) => {
    const extraPlayers = document.getElementById('extra-players');
    extraPlayers.innerHTML = ''; // Clear "Waiting..."
    
    data.players.forEach(p => {
      if (p.name !== gameData.username) {
        const div = document.createElement('div');
        div.className = 'player-entry';
        div.innerHTML = `<span class="player-name">${p.name}</span><span class="player-status">Connected</span>`;
        extraPlayers.appendChild(div);
      }
    });

    // Enable Start button if someone joined
    const startBtn = document.getElementById('start-multi-btn');
    startBtn.disabled = false;
    startBtn.textContent = "Ignite Game!";
  });

  socket.on('error_message', (msg) => {
    alert(msg);
  });

  socket.on('game_started', () => {
    window.location.href = '02_campaign_setup.html'; // Or a specific multiplayer stage
  });

  document.getElementById('start-multi-btn').addEventListener('click', () => {
    socket.emit('start_game', currentRoomId);
  });
});
