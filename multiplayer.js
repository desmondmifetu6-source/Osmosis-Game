// multiplayer.js
// Dynamically loaded on all game rounds if multiplayer room exists
const mpSessionId = sessionStorage.getItem('mp_sessionId');
const currentRoom = sessionStorage.getItem('mp_room');
const localState = sharedState.load();

const socket = io('http://localhost:3000');

// Inject HUD
const hud = document.createElement('div');
hud.id = 'mp-hud';
hud.style.cssText = `
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  background: rgba(43, 29, 20, 0.95);
  color: var(--gold);
  padding: 1rem 1.5rem;
  border-radius: 8px;
  border: 2px solid var(--gold);
  z-index: 9999;
  text-align: right;
  box-shadow: 0 5px 15px rgba(0,0,0,0.5);
  transition: all 0.3s ease;
`;

hud.innerHTML = `
  <div style="font-size:0.9rem; color:var(--parchment); opacity:0.8; letter-spacing:1px; text-transform:uppercase;">Opponent</div>
  <div id="mp-opp-name" style="font-size:1.2rem; font-weight:bold; color:#fff; margin-bottom:0.5rem;">Connecting...</div>
  <div style="font-size:1.5rem; font-family:monospace;">Points: <span id="mp-opp-score" style="color:#4caf50;">0</span></div>
  <div id="mp-opp-prog" style="font-size:1rem; margin-top:0.5rem; font-style:italic; color:var(--ink-light);">Standby</div>
`;
document.body.appendChild(hud);

// Rejoin logic to maintain connection across pages
socket.emit('join_room', { roomCode: currentRoom, username: localState.username, sessionId: mpSessionId }, (res) => {
  if (res.success) {
    const pg = window.location.pathname.split('/').pop().replace('.html', '');
    socket.emit('update_progress', { 
      roomCode: currentRoom, 
      sessionId: mpSessionId, 
      progress: pg === 'results' ? 'Finished' : pg.toUpperCase(),
      score: localState.score || 0
    });
  }
});

socket.on('opponent_update', (data) => {
  document.getElementById('mp-opp-name').textContent = data.username;
  document.getElementById('mp-opp-score').textContent = data.score;
  
  const progNames = {
    'ROUND1': 'Stage 1: Search',
    'ROUND2': 'Stage 2: Collection',
    'ROUND3': 'Stage 3: Memory Lab',
    'ROUND4': 'Stage 5: Final Revision',
    'ROUND5': 'Stage 4: Multiple Choice',
    'ROUND6': 'Stage 6: Ultimate Test',
    'Finished': 'Awaiting Results...'
  };
  document.getElementById('mp-opp-prog').textContent = progNames[data.progress] || data.progress;
});

// Handling the End Game on results.html
if (window.location.pathname.includes('results.html')) {
  // Alter UI to wait for opponent if they haven't finished
  document.querySelector('.res-header h2').textContent = "Awaiting Opponent...";
  document.querySelector('.res-subtitle').textContent = "Your score is locked. Waiting for your rival to finish.";
  
  socket.on('game_over', (data) => {
    AudioManager.play('success');
    const header = document.querySelector('.res-header h2');
    const subtitle = document.querySelector('.res-subtitle');
    
    if (data.winnerSessionId === 'Tie') {
      header.textContent = "It is a Draw!";
      subtitle.textContent = "A rare display of equal intellect.";
    } else if (data.winnerSessionId === mpSessionId) {
      header.textContent = "Victory!";
      header.style.color = "#4caf50";
      subtitle.textContent = `You outsmarted ${data.p1.id === mpSessionId ? data.p2.username : data.p1.username}.`;
    } else {
      header.textContent = "Defeat.";
      header.style.color = "#c62828";
      const winner = data.p1.id === data.winnerSessionId ? data.p1.username : data.p2.username;
      subtitle.textContent = `${winner} proved to be the superior scholar.`;
    }
    
    // Disconnect safely after results
    setTimeout(() => {
      sessionStorage.removeItem('mp_room');
      sessionStorage.removeItem('mp_sessionId');
    }, 5000);
  });
}
