// =====================================================================
// FILE: main.js (The Desktop Commander)
// =====================================================================
// This is the Electron "brain" for the desktop app.
// It does three important jobs:
//   1. Spawns the Node.js server (server.js) as a background child process
//      so that Socket.io and multiplayer work inside the app.
//   2. Waits until the server is ready, then opens the game window.
//   3. Kills the server child process when the app is closed — no orphan processes.

const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

let mainWindow = null;
let serverProcess = null;
const SERVER_PORT = 3000;
const SERVER_URL = `http://localhost:${SERVER_PORT}`;

// -----------------------------------------------------------------------
// 1. SPAWN THE SERVER
// -----------------------------------------------------------------------
function startServer() {
  // Use the same Node.js executable that is running this script
  const nodePath = process.execPath;
  const serverScript = path.join(__dirname, 'server.js');

  serverProcess = spawn(nodePath, [serverScript], {
    // Inherit environment so server can find its own node_modules
    env: { ...process.env, PORT: SERVER_PORT },
    stdio: ['ignore', 'pipe', 'pipe']
  });

  serverProcess.stdout.on('data', (data) => {
    console.log(`[SERVER]: ${data.toString().trim()}`);
  });

  serverProcess.stderr.on('data', (data) => {
    console.error(`[SERVER ERR]: ${data.toString().trim()}`);
  });

  serverProcess.on('close', (code) => {
    console.log(`[SERVER]: Process exited with code ${code}`);
    serverProcess = null;
  });

  serverProcess.on('error', (err) => {
    console.error('[SERVER]: Failed to start:', err.message);
    dialog.showErrorBox('Server Error', `Could not start the game server:\n${err.message}`);
  });
}

// -----------------------------------------------------------------------
// 2. WAIT FOR SERVER TO BE READY, THEN OPEN WINDOW
// -----------------------------------------------------------------------
function waitForServer(retries = 30, delay = 500) {
  return new Promise((resolve, reject) => {
    let attempts = 0;

    function checkServer() {
      attempts++;
      const req = http.get(SERVER_URL, (res) => {
        // Server responded — it's ready!
        res.destroy();
        resolve();
      });

      req.on('error', () => {
        if (attempts < retries) {
          setTimeout(checkServer, delay);
        } else {
          reject(new Error(`Server did not respond after ${retries} attempts.`));
        }
      });

      req.setTimeout(300, () => {
        req.destroy();
        if (attempts < retries) {
          setTimeout(checkServer, delay);
        } else {
          reject(new Error('Server connection timed out.'));
        }
      });
    }

    checkServer();
  });
}

// -----------------------------------------------------------------------
// 3. CREATE THE MAIN WINDOW
// -----------------------------------------------------------------------
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    show: false, // Don't show until page is loaded
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    },
    // Aesthetic desktop features
    backgroundColor: '#f5f3ee', // Matches the web app background
    title: 'Osmosis — STEM Learning Game'
  });

  // Remove the default menu bar for a cleaner app feel
  mainWindow.setMenuBarVisibility(false);

  // Load the game from the local server
  mainWindow.loadURL(SERVER_URL);

  // Show the window once it's ready (smooth, no white flash)
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// -----------------------------------------------------------------------
// 4. APP LIFECYCLE
// -----------------------------------------------------------------------
app.whenReady().then(async () => {
  // Start the server first
  startServer();

  try {
    // Wait for it to be ready (up to 15 seconds)
    await waitForServer(30, 500);
    console.log('[ELECTRON]: Server is ready. Opening window...');
    createWindow();
  } catch (err) {
    console.error('[ELECTRON]: Server failed to start:', err.message);
    dialog.showErrorBox(
      'Osmosis — Startup Error',
      'Could not connect to the game server. Please try restarting the app.\n\n' + err.message
    );
    app.quit();
  }

  app.on('activate', () => {
    // On macOS: re-create window when dock icon is clicked
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Kill the server when ALL windows are closed
app.on('window-all-closed', () => {
  killServer();
  if (process.platform !== 'darwin') app.quit();
});

// Also kill when explicitly quitting (catches Cmd+Q on Mac, etc.)
app.on('before-quit', () => {
  killServer();
});

// -----------------------------------------------------------------------
// 5. CLEAN SHUTDOWN — no orphan server processes
// -----------------------------------------------------------------------
function killServer() {
  if (serverProcess) {
    console.log('[ELECTRON]: Shutting down embedded server...');
    serverProcess.kill('SIGTERM');
    serverProcess = null;
  }
}
