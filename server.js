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
      players: [{ id: socket.id, name: data.username }],
      status: 'waiting'
    };
    socket.join(roomId);
    console.log(`Room created: ${roomId} by ${data.username}`);
  });

  // 2. GUEST: Join a Room
  socket.on('join_room', (data) => {
    const roomId = data.roomId;
    if (rooms[roomId]) {
      rooms[roomId].players.push({ id: socket.id, name: data.username });
      socket.join(roomId);
      
      // Tell everyone in the room that a new player arrived
      io.to(roomId).emit('player_joined', {
        players: rooms[roomId].players,
        message: `${data.username} joined the link!`
      });
      
      console.log(`${data.username} joined room: ${roomId}`);
    } else {
      socket.emit('error_message', 'Room not found. Check the code!');
    }
  });

  // 3. START GAME: Host starts for everyone
  socket.on('start_game', (roomId) => {
    if (rooms[roomId]) {
      rooms[roomId].status = 'playing';
      io.to(roomId).emit('game_started');
    }
  });

  socket.on('disconnect', () => {
    console.log('A player disconnected');
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
