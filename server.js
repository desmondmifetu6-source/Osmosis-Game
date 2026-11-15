// =====================================================================
// FILE: server.js (The Multiplayer Brain)
// =====================================================================
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*", // Allows anyone to connect for now
  }
});

// Server build / start timestamp for real-time version checking
const SERVER_START_TIME = Date.now();

// Serve the game files from the current directory
app.use(express.static(__dirname, {
  setHeaders: (res, filePath) => {
    if (filePath.endsWith('.html') || filePath.endsWith('.js') || filePath.endsWith('.css')) {
      res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
    }
  }
}));

app.get('/health', (_req, res) => {
  res.json({ ok: true, rooms: Object.keys(rooms).length });
});

app.get('/api/version', (_req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.json({ version: SERVER_START_TIME });
});

// Room Data Storage (in-memory)
const rooms = {};
const disconnectTimers = new Map(); // key: `${roomId}:${username}` -> timeoutId
const DISCONNECT_GRACE_MS = 25000;

function clearGraceTimer(roomId, username) {
  const key = `${roomId}:${username}`;
  if (disconnectTimers.has(key)) {
    clearTimeout(disconnectTimers.get(key));
    disconnectTimers.delete(key);
  }
}

io.on('connection', (socket) => {
  console.log('A player connected:', socket.id);

  // Broadcast current server version to client for instant update notification
  socket.emit('server_info', { version: SERVER_START_TIME });

  // 1. HOST: Create a Room
  socket.on('create_room', (data) => {
    const roomId = String(data?.roomId || '').trim().toUpperCase();
    const username = String(data?.username || 'Player').trim();
    if (!roomId) return;

    clearGraceTimer(roomId, username);
    rooms[roomId] = {
      players: [{
        id: socket.id,
        name: username,
        avatar: data?.avatar || '🤓',
        score: 0,
        time: 0,
        currentStage: 0,
        isFinished: false,
        connected: true
      }],
      status: 'waiting'
    };
    socket.join(roomId);
    socket.emit('room_created', { roomId, players: rooms[roomId].players });
    console.log(`[ROOM CREATED] ID: ${roomId} | Host: ${username} | Socket: ${socket.id}`);
  });

  // 2. GUEST / RECONNECT: Join a Room
  socket.on('join_room', (data) => {
    const roomId = String(data?.roomId || '').trim().toUpperCase();
    const username = String(data?.username || 'Guest').trim();
    console.log(`[JOIN ATTEMPT] ID: ${roomId} | User: ${username} | Socket: ${socket.id}`);

    const room = rooms[roomId];
    if (!room) {
      console.warn(`[JOIN FAILED] ID: ${roomId} not found. Active rooms:`, Object.keys(rooms));
      socket.emit('error_message', `Room not found (${roomId}). Check the code!`);
      return;
    }

    clearGraceTimer(roomId, username);

    // Check if player is already in the room by socket ID OR by name (for MPA page transitions)
    let player = room.players.find(p => p.id === socket.id || p.name === username);
    const isNewPlayer = !player;

    if (isNewPlayer) {
      if (room.players.length >= 10) {
        socket.emit('error_message', "Room is full! Max 10 players.");
        return;
      }
      player = {
        id: socket.id,
        name: username,
        avatar: data?.avatar || '🤓',
        score: 0,
        time: 0,
        currentStage: 1,
        isFinished: false,
        connected: true
      };
      room.players.push(player);
    } else {
      player.id = socket.id;
      player.connected = true;
      if (data?.avatar) player.avatar = data.avatar;
    }

    socket.join(roomId);

    if (isNewPlayer || room.status === 'waiting') {
      io.to(roomId).emit('player_joined', {
        players: room.players,
        message: `${username} joined the link!`
      });
    }

    // Always push latest leaderboard to everyone in the room on join/reconnect
    io.to(roomId).emit('leaderboard_update', {
      players: room.players
    });

    console.log(`[JOIN SUCCESS] ID: ${roomId} | User: ${username} | Reconnect: ${!isNewPlayer}`);
  });

  // 3. BATTLE: Update Score
  socket.on('update_score', (data) => {
    const roomId = String(data?.roomId || '').trim().toUpperCase();
    const room = rooms[roomId];
    if (!room) return;

    let player = room.players.find(p => p.id === socket.id);
    if (!player && data?.username) {
      player = room.players.find(p => p.name === data.username);
    }

    if (player) {
      clearGraceTimer(roomId, player.name);
      player.id = socket.id;
      player.connected = true;
      if (data.score !== undefined) player.score = Number(data.score) || 0;
      if (data.time !== undefined) player.time = Number(data.time) || 0;
      if (data.words) player.words = data.words;
      if (data.meanings) player.meanings = data.meanings;
      if (data.isFinished !== undefined) player.isFinished = !!data.isFinished;
      if (data.currentStage !== undefined) player.currentStage = data.currentStage;

      io.to(roomId).emit('leaderboard_update', {
        players: room.players
      });
    }
  });

  // 4. START GAME: Host starts for everyone
  socket.on('start_game', (roomId) => {
    const cleanRoomId = String(roomId || '').trim().toUpperCase();
    if (rooms[cleanRoomId]) {
      rooms[cleanRoomId].status = 'playing';
      io.to(cleanRoomId).emit('game_started');
      console.log(`[GAME STARTED] Room: ${cleanRoomId}`);
    }
  });

  // 5. EXPLICIT LEAVE: Player intentionally exits multiplayer
  socket.on('leave_room', (data) => {
    const roomId = String(data?.roomId || '').trim().toUpperCase();
    const room = rooms[roomId];
    if (!room) return;
    const idx = room.players.findIndex(p => p.id === socket.id || (data?.username && p.name === data.username));
    if (idx !== -1) {
      const removed = room.players.splice(idx, 1)[0];
      clearGraceTimer(roomId, removed.name);
      socket.leave(roomId);
      if (room.players.length === 0) {
        delete rooms[roomId];
      } else {
        io.to(roomId).emit('player_left', {
          players: room.players,
          message: `${removed.name} left the room.`
        });
        io.to(roomId).emit('leaderboard_update', { players: room.players });
      }
    }
  });

  socket.on('disconnect', () => {
    console.log(`[DISCONNECT] Socket: ${socket.id}`);

    for (const roomId of Object.keys(rooms)) {
      const room = rooms[roomId];
      const player = room.players.find(p => p.id === socket.id);
      if (player) {
        player.connected = false;
        const key = `${roomId}:${player.name}`;
        clearGraceTimer(roomId, player.name);

        // Grace window preserves rooms & scores during MPA HTML page transitions
        const timer = setTimeout(() => {
          disconnectTimers.delete(key);
          const activeRoom = rooms[roomId];
          if (!activeRoom) return;
          const idx = activeRoom.players.findIndex(p => p.name === player.name && !p.connected);
          if (idx === -1) return;

          const removedPlayer = activeRoom.players.splice(idx, 1)[0];
          console.log(`[GRACE EXPIRED] Removed player: ${removedPlayer.name} from Room: ${roomId}`);

          if (activeRoom.players.length === 0) {
            delete rooms[roomId];
            console.log(`[ROOM DELETED] Room ${roomId} is empty.`);
          } else {
            io.to(roomId).emit('player_left', {
              players: activeRoom.players,
              message: `${removedPlayer.name} disconnected.`
            });
            io.to(roomId).emit('leaderboard_update', {
              players: activeRoom.players
            });
          }
        }, DISCONNECT_GRACE_MS);

        disconnectTimers.set(key, timer);
      }
    }
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, '0.0.0.0', () => {
  console.log(`
  ==========================================
  🌟 OSMOSIS STEM MULTIPLAYER IS LIVE!
  👉 Local:   http://localhost:${PORT}
  👉 Network: http://0.0.0.0:${PORT}
  ==========================================
  `);
});
