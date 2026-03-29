const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');
const fs = require('fs');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

const server = http.createServer(app);
const io = new Server(server, { cors: { origin: '*' } });

// --- DATABASE LOGIC ---
const DB_FILE = 'database.json';
if (!fs.existsSync(DB_FILE)) {
  fs.writeFileSync(DB_FILE, JSON.stringify([]));
}

app.post('/api/score', (req, res) => {
  try {
    const newEntry = req.body;
    newEntry.timestamp = new Date().toISOString();
    
    const data = JSON.parse(fs.readFileSync(DB_FILE));
    data.push(newEntry);
    fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: 'Database Write Error' });
  }
});

app.get('/api/scores', (req, res) => {
  try {
    const data = JSON.parse(fs.readFileSync(DB_FILE));
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: 'Database Read Error' });
  }
});

const rooms = {};

io.on('connection', (socket) => {
  socket.on('create_room', ({ username, sessionId }, cb) => {
    const roomCode = Math.random().toString(36).substring(2, 6).toUpperCase();
    rooms[roomCode] = {
      players: { [sessionId]: { socketId: socket.id, username, score: 0, progress: 'Lobby', isWinner: false } },
      status: 'waiting',
      hostSessionId: sessionId
    };
    socket.join(roomCode);
    cb({ success: true, roomCode });
  });

  socket.on('join_room', ({ roomCode, username, sessionId }, cb) => {
    const code = roomCode.toUpperCase();
    const room = rooms[code];
    if (!room) return cb({ success: false, message: 'Room not found.' });
    
    // Reconnection logic
    if (room.players[sessionId]) {
      room.players[sessionId].socketId = socket.id;
      socket.join(code);
      return cb({ success: true, roomCode: code, hostUsername: room.players[room.hostSessionId].username, reconnected: true });
    }

    if (room.status !== 'waiting') return cb({ success: false, message: 'Game already started.' });
    if (Object.keys(room.players).length >= 2) return cb({ success: false, message: 'Room full.' });

    room.players[sessionId] = { socketId: socket.id, username, score: 0, progress: 'Lobby', isWinner: false };
    socket.join(code);
    
    io.to(code).emit('opponent_joined', { username });
    cb({ success: true, roomCode: code, hostUsername: room.players[room.hostSessionId].username });
  });

  socket.on('start_game_request', ({ roomCode, sessionId }) => {
    const room = rooms[roomCode];
    if (room && room.hostSessionId === sessionId && Object.keys(room.players).length === 2) {
      room.status = 'playing';
      const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
      const targetLetter = letters[Math.floor(Math.random() * letters.length)];
      const targetLength = Math.floor(Math.random() * (10 - 5 + 1)) + 5;
      
      io.to(roomCode).emit('game_started', { targetLetter, targetLength });
    }
  });

  socket.on('update_progress', ({ roomCode, sessionId, progress, score }) => {
    const room = rooms[roomCode];
    if (room && room.players[sessionId]) {
      room.players[sessionId].socketId = socket.id; // Update just in case
      if (progress) room.players[sessionId].progress = progress;
      if (score !== undefined) room.players[sessionId].score = score;
      
      // broadcast to others in room
      socket.to(roomCode).emit('opponent_update', room.players[sessionId]);
      
      if (progress === 'Finished') {
        const pKeys = Object.keys(room.players);
        const p1 = room.players[pKeys[0]];
        const p2 = room.players[pKeys[1]];
        if (p1 && p1.progress === 'Finished' && p2 && p2.progress === 'Finished') {
           let winnerSessionId = null;
           if (p1.score > p2.score) winnerSessionId = pKeys[0];
           else if (p2.score > p1.score) winnerSessionId = pKeys[1];
           else winnerSessionId = 'Tie';
           
           io.to(roomCode).emit('game_over', { winnerSessionId, p1, p2 });
           room.status = 'completed';
        }
      }
    }
  });

  socket.on('disconnect', () => {
    // We don't delete players immediately on disconnect because of MPA page changes.
    // Instead we rely on 'update_progress' or explicit 'leave_room' to manage state.
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Osmosis Live Server running on port ${PORT}`));
