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
      if (rooms[roomId].players.length >= 10 && !rooms[roomId].players.some(p => p.name === data.username)) {
        socket.emit('error_message', "Room is full! Max 10 players.");
        return;
      }

      // Check if player is already in the room by name OR socket ID (for stage transitions & reconnects)
      let player = rooms[roomId].players.find(p => p.name === data.username || p.id === socket.id);
      
      if (!player) {
        player = { 
          id: socket.id, 
          name: data.username, 
          avatar: data.avatar || '🤓',
          score: 0,
          time: 0,
          connected: true,
          isFinished: false
        };
        rooms[roomId].players.push(player);
      } else {
        // Reconnect existing player: update socket ID, mark connected
        player.id = socket.id;
        player.connected = true;
        if (data.avatar) player.avatar = data.avatar;
      }
      
      socket.join(roomId);
      
      // Send the current room leaderboard directly to the joining/reconnecting player immediately
      socket.emit('leaderboard_update', {
        players: rooms[roomId].players
      });

      // Tell everyone in the room that a player arrived / reconnected
      io.to(roomId).emit('player_joined', {
        players: rooms[roomId].players,
        message: `${data.username} connected!`
      });
      
      console.log(`[JOIN SUCCESS] ID: ${roomId} | User: ${data.username} | Total Players: ${rooms[roomId].players.length}`);
    } else {
      console.warn(`[JOIN FAILED] ID: ${roomId} not found. Active rooms:`, Object.keys(rooms));
      socket.emit('error_message', `Room not found (${roomId}). Check the code!`);
    }
  });

  // 3. BATTLE: Update Score
  socket.on('update_score', (data) => {
    const roomId = data.roomId;
    if (rooms[roomId]) {
      // Find by username first (rock-solid across page transitions), then by socket ID
      let player = rooms[roomId].players.find(p => p.name === data.username) ||
                   rooms[roomId].players.find(p => p.id === socket.id);
      
      if (player) {
        player.score = (data.score !== undefined) ? data.score : (player.score || 0);
        player.time = data.time || player.time || 0;
        if (data.words) player.words = data.words;
        if (data.meanings) player.meanings = data.meanings;
        if (data.isFinished !== undefined) player.isFinished = data.isFinished;
        if (data.currentStage !== undefined) player.currentStage = data.currentStage;
        player.connected = true;
        player.id = socket.id; // Sync latest socket ID

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
    
    for (const roomId in rooms) {
      const room = rooms[roomId];
      const player = room.players.find(p => p.id === socket.id);
      if (player) {
        player.connected = false;
        player.lastSeen = Date.now();
        console.log(`[DISCONNECT] Player ${player.name} went offline in Room: ${roomId} (game status: ${room.status})`);

        // If the game has already started or finished, DO NOT delete the player!
        // In a multi-page web app, players disconnect temporarily between stage navigation.
        // Keeping their records guarantees all final scores appear on the leaderboard!
        if (room.status === 'playing' || room.status === 'finished') {
          // Broadcast status without deleting their score or profile
          io.to(roomId).emit('leaderboard_update', {
            players: room.players
          });
        } else {
          // If still waiting in lobby, remove player after a 10s grace window
          setTimeout(() => {
            if (room.status === 'waiting' && !player.connected) {
              const idx = room.players.findIndex(p => p.name === player.name && !p.connected);
              if (idx !== -1) {
                room.players.splice(idx, 1);
                io.to(roomId).emit('player_left', {
                  players: room.players,
                  message: `${player.name} left the lobby.`
                });
                io.to(roomId).emit('leaderboard_update', {
                  players: room.players
                });
                if (room.players.length === 0) {
                  delete rooms[roomId];
                  console.log(`[ROOM DELETED] Lobby ${roomId} was empty.`);
                }
              }
            }
          }, 10000);
        }
      }
    }
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
