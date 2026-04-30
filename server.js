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

// Serve the game files from the current directory
app.use(express.static(__dirname));

// Room Data Storage (in-memory)
const rooms = {};

io.on('connection', (socket) => {
  console.log('A player connected:', socket.id);

  // 1. HOST: Create a Room
  socket.on('create_room', (data) => {
    const roomId = data.roomId;
    rooms[roomId] = {
      players: [{ id: socket.id, name: data.username, avatar: data.avatar || '🤓' }],
      status: 'waiting'
    };
    socket.join(roomId);
    console.log(`[ROOM CREATED] ID: ${roomId} | Host: ${data.username} | Socket: ${socket.id}`);
  });

  // 2. GUEST: Join a Room
  socket.on('join_room', (data) => {
    const roomId = data.roomId;
    console.log(`[JOIN ATTEMPT] ID: ${roomId} | User: ${data.username} | Socket: ${socket.id}`);
    
    if (rooms[roomId]) {
      // 10 Player Limit
      if (rooms[roomId].players.length >= 10) {
        socket.emit('error_message', "Room is full! Max 10 players.");
        return;
      }

      // Check if player is already in the room by socket ID OR by name (for page refreshes)
      let player = rooms[roomId].players.find(p => p.id === socket.id || p.name === data.username);
      
      if (!player) {
        player = { id: socket.id, name: data.username, avatar: data.avatar || '🤓' };
        rooms[roomId].players.push(player);
      } else {
        // Update socket ID and potentially avatar to the new one
        player.id = socket.id;
        if (data.avatar) player.avatar = data.avatar;
      }
      
      socket.join(roomId);
      
      // Tell everyone in the room that a new player arrived
      io.to(roomId).emit('player_joined', {
        players: rooms[roomId].players,
        message: `${data.username} joined the link!`
      });
      
      console.log(`[JOIN SUCCESS] ID: ${roomId} | User: ${data.username}`);
    } else {
      console.warn(`[JOIN FAILED] ID: ${roomId} not found. Active rooms:`, Object.keys(rooms));
      socket.emit('error_message', `Room not found (${roomId}). Check the code!`);
    }
  });

  // 3. BATTLE: Update Score
  socket.on('update_score', (data) => {
    const roomId = data.roomId;
    if (rooms[roomId]) {
      const player = rooms[roomId].players.find(p => p.id === socket.id);
      if (player) {
        player.score = data.score;
        io.to(roomId).emit('leaderboard_update', {
          players: rooms[roomId].players
        });
      }
    }
  });

  // 4. START GAME: Host starts for everyone
  socket.on('start_game', (roomId) => {
    if (rooms[roomId]) {
      rooms[roomId].status = 'playing';
      io.to(roomId).emit('game_started');
      console.log(`[GAME STARTED] Room: ${roomId}`);
    }
  });

  socket.on('disconnect', () => {
    console.log(`[DISCONNECT] Socket: ${socket.id}`);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`
  ==========================================
  OSMOSIS MULTIPLAYER SERVER IS LIVE!
  URL: http://localhost:${PORT}
  ==========================================
  `);
});
