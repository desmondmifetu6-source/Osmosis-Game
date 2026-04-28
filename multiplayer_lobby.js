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

  // 1. Mode Toggle Logic
  modeHost.addEventListener('click', () => {
    modeHost.classList.add('active');
    modeJoin.classList.remove('active');
    hostSection.style.display = 'block';
    joinSection.style.display = 'none';
  });

  modeJoin.addEventListener('click', () => {
    modeJoin.classList.add('active');
    modeHost.classList.remove('active');
    hostSection.style.display = 'none';
    joinSection.style.display = 'block';
  });

  // 2. Mock Room Code Generation
  function generateRoomCode() {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // No O, I, 0, 1 for clarity
    let result = '';
    for (let i = 0; i < 6; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  // Initialize Host Code
  const mockCode = generateRoomCode();
  roomIdEl.textContent = mockCode;

  // 3. Mock Join Logic
  document.getElementById('confirm-join-btn').addEventListener('click', () => {
    const code = document.getElementById('join-code-input').value.trim().toUpperCase();
    if (code.length < 6) {
      if (typeof window.showModal === 'function') {
        window.showModal("Invalid Link", "Please enter a valid 6-character room code.");
      } else {
        alert("Please enter a valid 6-character room code.");
      }
      return;
    }
    
    // For now, since we have no backend, we'll just mock a "Connecting..." state
    document.getElementById('confirm-join-btn').textContent = "Connecting...";
    document.getElementById('confirm-join-btn').disabled = true;
    
    setTimeout(() => {
      alert("Note: Real-time multiplayer requires a server backend. This is currently a visual preview.");
      document.getElementById('confirm-join-btn').textContent = "Establish Link";
      document.getElementById('confirm-join-btn').disabled = false;
    }, 1500);
  });
});
