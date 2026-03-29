initModal();

const state = sharedState.load();
if (!state.username) window.location.href = 'index.html';

// Prepare Sync ID for persistent connections across the MPA
let sessionId = sessionStorage.getItem('mp_sessionId');
if (!sessionId) {
  sessionId = Math.random().toString(36).substring(2, 10);
  sessionStorage.setItem('mp_sessionId', sessionId);
}

// Connect to local Node.js server
const socket = io('http://localhost:3000');
socket.on('connect_error', () => {
    document.getElementById('join-error').textContent = "Multiplayer server is currently offline. Please ensure the Node server is running.";
    document.getElementById('join-error').style.display = 'block';
});

const modeSelection = document.getElementById('mode-selection');
const hostWaiting = document.getElementById('host-waiting');
const joinWaiting = document.getElementById('join-waiting');
const startMatchBtn = document.getElementById('start-match-btn');

let currentRoom = null;

document.getElementById('host-btn').addEventListener('click', () => {
  AudioManager.play('click');
  socket.emit('create_room', { username: state.username, sessionId }, (res) => {
    if (res.success) {
      currentRoom = res.roomCode;
      sessionStorage.setItem('mp_room', currentRoom);
      
      modeSelection.style.display = 'none';
      hostWaiting.style.display = 'block';
      document.getElementById('host-code-display').textContent = currentRoom;
      
    } else {
      alert("Failed to create room: " + res.message);
    }
  });
});

document.getElementById('join-btn').addEventListener('click', () => {
  AudioManager.play('click');
  const code = document.getElementById('join-input').value.toUpperCase().trim();
  if (code.length !== 4) return;
  
  socket.emit('join_room', { roomCode: code, username: state.username, sessionId }, (res) => {
    if (res.success) {
      currentRoom = res.roomCode;
      sessionStorage.setItem('mp_room', currentRoom);
      
      modeSelection.style.display = 'none';
      joinWaiting.style.display = 'block';
      document.getElementById('host-name-display').textContent = res.hostUsername;
    } else {
      document.getElementById('join-error').textContent = res.message;
      document.getElementById('join-error').style.display = 'block';
    }
  });
});

socket.on('opponent_joined', (data) => {
  const msg = document.getElementById('host-waiting-msg');
  msg.textContent = `${data.username} has entered the room.`;
  msg.style.color = 'var(--accent-green)';
  msg.style.fontWeight = 'bold';
  
  AudioManager.play('success');
  startMatchBtn.style.display = 'block';
});

startMatchBtn.addEventListener('click', () => {
  AudioManager.play('click');
  socket.emit('start_game_request', { roomCode: currentRoom, sessionId });
});

socket.on('game_started', (data) => {
  // Reset clean game state but keep username
  const cleanState = { username: state.username };
  cleanState.letter = data.targetLetter;
  cleanState.length = data.targetLength;
  cleanState.wordsPool = [];
  cleanState.selectedWords = [];
  cleanState.meanings = {};
  cleanState.score = 0;
  
  sharedState.save(cleanState);
  
  showModal("Match Commencing", `The constraints have been dictated (Letter: ${data.targetLetter}, Length: ${data.targetLength}). Proceed immediately.`);
  setTimeout(() => window.location.href = 'round1.html', 3000);
});
