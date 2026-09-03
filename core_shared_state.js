// =====================================================================
// FILE: core_shared_state.js (The World Builder)
// =====================================================================
// Imagine playing a video game where your score gets wiped out 
// every time you go to the next level. That would be terrible! 
// This file is responsible for remembering everything about you
// as you travel between the different web pages (stages) of Osmosis.

/**
 * sharedState: The Game's Backpack
 * We use something called 'sessionStorage' here. Think of sessionStorage 
 * as a temporary backpack that the browser wears. When you close the 
 * tab, the backpack gets thrown away. But while you are playing, 
 * we can put variables (like score) inside the backpack to carry them around!
 */
const sharedState = {

  // Function: load
  // When we need to look in the backpack to grab our stats, we call 'load()'.
  load: function () {
    // We open the backpack and look for 'gameState'.
    // If we find it, we read it. If it's completely empty (||), we create a brand new, empty save file!
    return JSON.parse(sessionStorage.getItem('gameState')) || {
      username: '', letters: [], length: 0, wordsPool: [],
      selectedWords: [], meanings: {}, score: 0, usedLetters: [],
      startTime: null, totalTime: 0, sessionStartedAt: null, sessionEndedAt: null, stageScores: {}
    };
  },

  // Function: save
  // When we earn points or learn new words, we need to put the new info back into the backpack.
  save: function (state) {
    // JSON.stringify is like squishing all your data into a flat piece of paper 
    // so it fits inside the backpack cleanly.
    sessionStorage.setItem('gameState', JSON.stringify(state));
  },

  // Function: clearGameSession
  // Wipes all game-specific progress (score, timers, word pools) from sessionStorage.
  // By default, preserves user profile information (username and avatar) so they stay logged in.
  clearGameSession: function (keepUserAndAvatar = true) {
    let username = '';
    let avatar = '🤓';
    let multiplayerMode = false;
    let currentRoomId = null;

    if (keepUserAndAvatar) {
      const state = this.load();
      username = state.username || localStorage.getItem('osmosis_user') || '';
      avatar = state.avatar || '🤓';
      multiplayerMode = state.multiplayerMode || false;
      currentRoomId = state.currentRoomId || null;
    }

    const cleanState = {
      username: username,
      avatar: avatar,
      letters: [],
      length: 0,
      wordsPool: [],
      selectedWords: [],
      meanings: {},
      score: 0,
      usedLetters: [],
      startTime: null,
      totalTime: 0,
      sessionStartedAt: null,
      sessionEndedAt: null,
      stageScores: {},
      multiplayerMode: multiplayerMode,
      currentRoomId: currentRoomId
    };

    this.save(cleanState);
    sessionStorage.removeItem('osmosis_saved_result');
  },

  // Function: startTimer
  // This is a stopwatch that starts ticking the moment a level begins.
  startTimer: function () {
    const state = this.load(); // Grab the backpack
    if (!state.sessionStartedAt) {
      state.sessionStartedAt = Date.now(); // Record exactly what time it is right now
    }
    state.sessionEndedAt = null;

    // If the stopwatch hasn't started yet...
    if (!state.startTime) {
      state.startTime = Date.now(); // Click the stopwatch button!
      this.save(state); // Put it back in the backpack
    }
  },

  // Function: stopTimer
  // Stops the stopwatch when you finish the stage to see how long you took.
  stopTimer: function () {
    const state = this.load();
    if (state.startTime) {
      const now = Date.now();
      // Add the time you just spent onto your total playtime.
      state.totalTime += (now - state.startTime);
      state.startTime = null; // Reset the current stage timer
      state.sessionEndedAt = now;
      this.save(state);
    }
  },

  // Function: getFormattedTime
  // Computers count time in milliseconds (thousands of a second). 
  // Humans don't read time like that. This converts "65000 milliseconds" into "1:05" (1 minute, 5 secs).
  getFormattedTime: function (ms) {
    const totalSeconds = Math.floor(ms / 1000); // Chop off the milliseconds
    const minutes = Math.floor(totalSeconds / 60); // Find out how many full minutes fit 
    const seconds = totalSeconds % 60; // Find the leftover seconds
    // The padStart(2, '0') makes sure it says "1:05" instead of "1:5".
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  },

  // Function: formatDateTime
  // Converts computer timestamp numbers into a human-readable calendar date.
  formatDateTime: function (ts) {
    if (!ts) return 'N/A';
    return new Date(ts).toLocaleString();
  },

  // Function: recordStageScore
  // Think of this like a report card. It records exactly how you did on a specific test.
  recordStageScore: function (stageKey, stageLabel, score) {
    const state = this.load();
    if (!state.stageScores || typeof state.stageScores !== 'object') state.stageScores = {};

    // Calculate elapsed time for this stage and add to totalTime
    if (state.startTime) {
      const now = Date.now();
      state.totalTime += (now - state.startTime);
      state.startTime = null; // Clear so it can be restarted by the next stage
    }

    // We create a new folder for the specific stage, saving your score and the time you finished it.
    state.stageScores[stageKey] = {
      label: stageLabel || stageKey,
      score: Number(score) || 0,
      at: Date.now()
    };
    this.save(state);

    // Multiplayer Reporting: If we are in a battle, tell the server!
    this.syncScore();
  },

  escapeHTML: function (str) {
    return String(str || '').replace(/[&<>'"]/g, tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag));
  },

  syncScore: function() {
    const state = this.load();
    if (state.multiplayerMode && state.currentRoomId) {
      this.reportScoreToServer(state.currentRoomId, state.score || 0);
    }
  },

  reportScoreToServer: function(roomId, score) {
    if (typeof io !== 'undefined') {
      const state = this.load();
      if (!this.socket) {
        this.socket = io();
      }
      this.socket.off('leaderboard_update');
      this.socket.on('leaderboard_update', (data) => this.renderLeaderboard(data.players));

      this.socket.emit('update_score', { 
        roomId: roomId, 
        score: score,
        username: localStorage.getItem('osmosis_user') || 'Guest',
        time: state.totalTime || 0
      });
    }
  },

  initMultiplayer: function() {
    const state = this.load();
    if (state.multiplayerMode && state.currentRoomId && typeof io !== 'undefined') {
      if (!this.socket) {
        this.socket = io();
      }
      
      // Re-join the room so server knows this socket is active in this room
      this.socket.emit('join_room', {
        roomId: state.currentRoomId,
        username: localStorage.getItem('osmosis_user') || 'Guest',
        avatar: state.avatar || '🤓'
      });

      // Listen for leaderboard updates from other players
      this.socket.off('leaderboard_update');
      this.socket.on('leaderboard_update', (data) => {
        this.renderLeaderboard(data.players);
      });

      // Listen for game end or other events
      this.socket.off('error_message');
      this.socket.on('error_message', (msg) => console.error("MP Error:", msg));
    }
  },

  renderLeaderboard: function(players) {
    // We don't want the floating scoreboard on the results page or the home menu
    const isResultsPage = window.location.pathname.includes('results.html');
    const isHome = window.location.pathname.includes('home_menu.html') || window.location.pathname.endsWith('/');
    
    if (isResultsPage || isHome) {
      const existing = document.getElementById('mp-leaderboard');
      if (existing) existing.remove();
      return;
    }

    let el = document.getElementById('mp-leaderboard');
    if (!el) {
      el = document.createElement('div');
      el.id = 'mp-leaderboard';
      el.style.cssText = `
        position: fixed; top: 1.5rem; left: 1.5rem; 
        background: rgba(255,255,255,0.7); backdrop-filter: blur(12px);
        padding: 8px 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.5);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15); z-index: 9998;
        min-width: 140px; font-family: var(--font-main); pointer-events: none;
      `;
      document.body.appendChild(el);
    }

    // Sort players by score
    const sorted = [...players].sort((a, b) => (b.score || 0) - (a.score || 0));
    
    el.innerHTML = `<h4 style="margin:0 0 8px 0; font-size: 0.6rem; font-weight: 800; letter-spacing:0.5px; color: var(--text-secondary); border-bottom: 1px solid rgba(0,0,0,0.05); padding-bottom: 4px; opacity: 0.7;">Score board</h4>`;
    sorted.forEach((p, i) => {
      const isMe = p.name === localStorage.getItem('osmosis_user');
      const div = document.createElement('div');
      div.style.cssText = `
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 4px; font-size: 0.75rem;
        ${isMe ? 'color: var(--accent-primary); font-weight: 700;' : ''}
      `;
      const escapedAvatar = this.escapeHTML(p.avatar || '🤓');
      const escapedName = this.escapeHTML(p.name || 'Guest');
      div.innerHTML = `
        <span>${i + 1}. ${escapedAvatar} ${escapedName}</span>
        <span style="font-family: monospace; font-weight: 800;">${Number(p.score) || 0}</span>
      `;
      el.appendChild(div);
    });
  },

  // Function: showStageScoreThen
  // When you beat a level, this magically teleports you to the next level seamlessly without a popup.
  showStageScoreThen: function (stageKey, stageLabel, score, onContinue) {
    this.recordStageScore(stageKey, stageLabel, score); // Update report card
    if (typeof onContinue === 'function') onContinue();
  },

  // Function: ensureGlobalTimer
  // If the screen doesn't have a clock visible, this physically builds a clock onto the webpage using code!
  ensureGlobalTimer: function () {
    let el = document.getElementById('global-game-timer');
    if (!el) {
      el = document.createElement('div'); // Create a new empty internet box (div)
      el.id = 'global-game-timer'; // Slap a nametag on it so we can find it later
      document.body.appendChild(el); // Stick it to the body of the webpage
    }
    return el;
  },

  // Function: updateTimerUI
  // This is the animated ticking clock you see on the screen.
  updateTimerUI: function (elementId = 'global-game-timer') {
    if (this._timerLoopId) {
      cancelAnimationFrame(this._timerLoopId);
      this._timerLoopId = null;
    }

    const el = elementId === 'global-game-timer' ? this.ensureGlobalTimer() : document.getElementById(elementId);
    if (!el) return;

    const update = () => {
      const state = this.load();
      if (!state.startTime) {
        this._timerLoopId = null;
        return;
      }
      const now = Date.now();
      const currentElapsed = state.totalTime + (now - state.startTime);
      el.textContent = this.getFormattedTime(currentElapsed); // Update the text on screen
      this._timerLoopId = requestAnimationFrame(update);
    };

    const state = this.load();
    if (state.startTime) {
      this._timerLoopId = requestAnimationFrame(update);
    }
  },
};

// Auto-init multiplayer if needed on page load
if (typeof window !== 'undefined') {
  window.addEventListener('load', () => sharedState.initMultiplayer());
}

// =====================================================================
// AudioManager: The Sound Effects Department
// =====================================================================
// Synthesizes rich audio live in-browser: fanfares, funny boings, page warps & gems!
const AudioManager = {
  ctx: null,

  init: function () {
    if (!this.ctx) {
      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioContext();
      } catch (err) { }
    }
  },

  vibrate: function (pattern) {
    // Telegram Mini App Haptics
    if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.HapticFeedback) {
      try {
        const haptic = window.Telegram.WebApp.HapticFeedback;
        if (pattern === 'error' || (Array.isArray(pattern) && pattern.length === 3)) {
          haptic.notificationOccurred('error');
        } else if (pattern === 'success' || pattern === 'levelup') {
          haptic.notificationOccurred('success');
        } else {
          haptic.impactOccurred('light');
        }
      } catch (e) { }
    }
    // Standard Web Vibration API
    if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
      try {
        navigator.vibrate(pattern);
      } catch (e) { }
    }
  },

  play: function (type) {
    try {
      this._playInternal(type);
    } catch (err) {
      // Never let audio glitches block Submit / Continue clicks
    }
  },

  _playInternal: function (type) {
    this.init(); // Guarantee audio context exists
    if (type === 'click') this.vibrate(10);
    else if (type === 'chip') this.vibrate(15);
    else if (type === 'success') this.vibrate([25, 35, 45, 35, 60]);
    else if (type === 'error') this.vibrate([50, 40, 50]);
    else if (type === 'levelup') this.vibrate([35, 50, 35, 50, 90]);
    else if (type === 'gem') this.vibrate([15, 25, 15]);
    else if (type === 'fanfare') this.vibrate([40, 50, 40, 50, 40, 60, 120]);

    if (!this.ctx) return;
    if (this.ctx.state === 'suspended') {
      try { this.ctx.resume(); } catch(e) {}
    }

    const now = this.ctx.currentTime;

    switch (type) {
      case 'fanfare': {
        // Triumphant "Pa-na-na-na-na-naaa!" Victory Trumpet Fanfare
        // Notes: G4 (392Hz), C5 (523.25Hz), E5 (659.25Hz), G5 (783.99Hz), E5 (659.25Hz), G5 (783.99Hz)
        const notes = [
          { freq: 392.00,  start: 0.00, duration: 0.09, vol: 0.25 }, // Pa
          { freq: 523.25,  start: 0.10, duration: 0.09, vol: 0.27 }, // Na
          { freq: 659.25,  start: 0.20, duration: 0.09, vol: 0.29 }, // Na
          { freq: 783.99,  start: 0.30, duration: 0.16, vol: 0.30 }, // Na
          { freq: 659.25,  start: 0.48, duration: 0.10, vol: 0.27 }, // Na
          { freq: 783.99,  start: 0.60, duration: 0.65, vol: 0.35 }  // NAAAA!
        ];

        notes.forEach(n => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          const filter = this.ctx.createBiquadFilter();

          osc.type = 'triangle';
          osc.frequency.setValueAtTime(n.freq, now + n.start);

          filter.type = 'lowpass';
          filter.frequency.setValueAtTime(2800, now + n.start);

          const tStart = now + n.start;
          const tEnd = tStart + n.duration;

          // Standard Web Audio gain envelope (0.0001 prevents WebKit exponential ramp DOM exceptions)
          gain.gain.setValueAtTime(0.0001, tStart);
          gain.gain.linearRampToValueAtTime(n.vol, tStart + 0.015);
          gain.gain.exponentialRampToValueAtTime(0.0001, tEnd);

          osc.connect(filter);
          filter.connect(gain);
          gain.connect(this.ctx.destination);

          osc.start(tStart);
          osc.stop(tEnd);
        });
        break;
      }
      case 'click': {
        // Soft futuristic glass tap (No more heavy drum thud!)
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain); gain.connect(this.ctx.destination);
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, now);
        osc.frequency.exponentialRampToValueAtTime(1100, now + 0.04);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
        osc.start(now); osc.stop(now + 0.04);
        break;
      }
      case 'chip': {
        // Soft dual-tone crystal tech harmony
        [659.25, 880].forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.connect(gain); gain.connect(this.ctx.destination);
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now + idx * 0.02);
          gain.gain.setValueAtTime(0.06, now + idx * 0.02);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.02 + 0.08);
          osc.start(now + idx * 0.02);
          osc.stop(now + idx * 0.02 + 0.08);
        });
        break;
      }
      case 'success': {
        // Glorious soft 3-note arpeggio chord (C5 - E5 - G5)
        [523.25, 659.25, 783.99].forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.connect(gain); gain.connect(this.ctx.destination);
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now + idx * 0.07);
          gain.gain.setValueAtTime(0, now + idx * 0.07);
          gain.gain.linearRampToValueAtTime(0.18, now + idx * 0.07 + 0.02);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.07 + 0.35);
          osc.start(now + idx * 0.07);
          osc.stop(now + idx * 0.07 + 0.35);
        });
        break;
      }
      case 'error': {
        // Soft, funny cartoon "boing / oopsie" sound (Gentle sine frequency bend, no harsh buzzing!)
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain); gain.connect(this.ctx.destination);
        osc.type = 'sine'; // Soft pure wave
        osc.frequency.setValueAtTime(320, now);
        osc.frequency.exponentialRampToValueAtTime(200, now + 0.12);
        osc.frequency.linearRampToValueAtTime(260, now + 0.22);
        osc.frequency.exponentialRampToValueAtTime(150, now + 0.38);

        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.38);
        osc.start(now); osc.stop(now + 0.38);
        break;
      }
      case 'warp': {
        // Soft futuristic ambient slide for stage transition
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain); gain.connect(this.ctx.destination);
        osc.type = 'sine';
        osc.frequency.setValueAtTime(300, now);
        osc.frequency.exponentialRampToValueAtTime(700, now + 0.25);
        gain.gain.setValueAtTime(0.01, now);
        gain.gain.linearRampToValueAtTime(0.12, now + 0.1);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
        osc.start(now); osc.stop(now + 0.25);
        break;
      }
      case 'gem': {
        // Sparkling high-pitched double chime
        [1046.50, 1567.98].forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.connect(gain); gain.connect(this.ctx.destination);
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now + idx * 0.08);
          gain.gain.setValueAtTime(0.15, now + idx * 0.08);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.08 + 0.25);
          osc.start(now + idx * 0.08);
          osc.stop(now + idx * 0.08 + 0.25);
        });
        break;
      }
      case 'levelup': {
        // Triumph victory trumpet fanfare
        [440, 554.37, 659.25, 880].forEach((freq, idx) => {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.connect(gain); gain.connect(this.ctx.destination);
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(freq, now + idx * 0.1);
          gain.gain.setValueAtTime(0, now + idx * 0.1);
          gain.gain.linearRampToValueAtTime(0.25, now + idx * 0.1 + 0.03);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.1 + 0.5);
          osc.start(now + idx * 0.1);
          osc.stop(now + idx * 0.1 + 0.5);
        });
        break;
      }
    }
  }
};

// =====================================================================
// VoiceManager: Educational Text-to-Speech Engine
// =====================================================================
const VoiceManager = {
  synth: typeof window !== 'undefined' ? window.speechSynthesis : null,
  enabledKey: 'osmosis_voice_enabled',
  selectedVoice: null,

  init: function () {
    if (!this.synth) return;
    if (this.selectedVoice) return;

    const findVoice = () => {
      const voices = this.synth.getVoices();
      if (!voices || voices.length === 0) return;
      // Preference: Natural, Google, British/US English voices
      this.selectedVoice = voices.find(v => (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Serena')) && v.lang.startsWith('en')) ||
                           voices.find(v => v.lang === 'en-GB') ||
                           voices.find(v => v.lang.startsWith('en')) ||
                           voices[0];
    };

    findVoice();
    if (this.synth.onvoiceschanged !== undefined) {
      this.synth.onvoiceschanged = findVoice;
    }
  },

  isEnabled: function () {
    const val = localStorage.getItem(this.enabledKey);
    return val === null ? true : val === 'true';
  },

  setEnabled: function (enabled) {
    localStorage.setItem(this.enabledKey, enabled ? 'true' : 'false');
    if (!enabled) this.stop();
  },

  toggle: function () {
    const nextState = !this.isEnabled();
    this.setEnabled(nextState);
    return nextState;
  },

  cleanTextForSpeech: function (text) {
    if (!text) return '';
    return text
      .replace(/\$\$\\frac\{([^}]+)\}\{([^}]+)\}\$\$/g, '$1 over $2')
      .replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, '$1 over $2')
      .replace(/\\sqrt\{([^}]+)\}/g, 'square root of $1')
      .replace(/\^2\b/g, ' squared')
      .replace(/\^3\b/g, ' cubed')
      .replace(/\\pm/g, ' plus or minus ')
      .replace(/\\times/g, ' times ')
      .replace(/\\cdot/g, ' dot ')
      .replace(/\\alpha/g, ' alpha ')
      .replace(/\\beta/g, ' beta ')
      .replace(/\\gamma/g, ' gamma ')
      .replace(/\\pi/g, ' pi ')
      .replace(/\$+/g, '')
      .replace(/\\[a-zA-Z]+/g, ' ')
      .replace(/[{}]/g, '')
      .replace(/\s+/g, ' ')
      .trim();
  },

  speak: function (text, options = {}) {
    if (!this.synth) return;
    if (!this.isEnabled() && !options.force) return;

    this.init();
    this.stop(); // Stop previous speech immediately

    const cleaned = this.cleanTextForSpeech(text);
    if (!cleaned) return;

    const utterance = new SpeechSynthesisUtterance(cleaned);
    if (this.selectedVoice) utterance.voice = this.selectedVoice;
    
    // Clear, comfortable educational pacing
    utterance.rate = options.rate || 0.92;
    utterance.pitch = options.pitch || 1.0;
    utterance.volume = options.volume || 1.0;

    if (options.onend) utterance.onend = options.onend;
    if (options.onerror) utterance.onerror = options.onerror;

    try {
      this.synth.speak(utterance);
    } catch (err) {
      console.warn('VoiceManager speak error:', err);
    }
  },

  stop: function () {
    if (this.synth) {
      try {
        this.synth.cancel();
      } catch (err) {}
    }
  }
};

if (typeof window !== 'undefined') {
  window.VoiceManager = VoiceManager;
}

// =====================================================================
// Global Event Listeners (The Lookouts)
// =====================================================================

// Look out for clicks. If someone clicks a button, we make the sound engine play a "click" noise.
document.addEventListener('click', (e) => {
  AudioManager.init(); // Make sure the sound engine is awake
  if (e.target.closest('.classic-btn')) AudioManager.play('click');
  else if (e.target.closest('.word-chip')) {
    setTimeout(() => {
      // If they clicked a bad word, buzzer! Otherwise, happy chip sound.
      if (e.target.closest('.word-chip').classList.contains('wrong')) AudioManager.play('error');
      else AudioManager.play('chip');
    }, 10);
  }
});

// =====================================================================
// DictionaryLogic (The Librarian)
// =====================================================================
// This is an assistant that talks strictly to our word library (core_dictionary.js).
const DictionaryLogic = {

  // Count only A–Z letters so spaces/hyphens in dictionary entries do not inflate length.
  // Example: "a fortiori" → 9 letters, not 10 characters.
  countLetters: function (word) {
    return String(word || '').replace(/[^a-zA-Z]/g, '').length;
  },

  // Function: fetchWords
  // You hand the librarian a Letter and a Length, and it digs through 
  // the filing cabinet to bring you matched scientific words.
  fetchWords: function (letter, length) {
    if (typeof window.STEMDictionary === 'undefined') return [];
    const words = window.STEMDictionary.getWordsByLetter(letter);
    const targetLen = Number(length);

    // We try to find words that match the exact target letter-count first, AND have a valid definition!
    let matched = words.filter(w => w.definition && w.definition.trim() !== "")
      .filter(w => this.countLetters(w.word) === targetLen)
      .map(w => w.word);

    // If the library has no words of that exact size, we just take any word under that letter with a definition.
    if (matched.length === 0) {
      matched = words.filter(w => w.definition && w.definition.trim() !== "").map(w => w.word);
    }

    // The "sort(() => 0.5 - Math.random())" is a fancy trick to shuffle the deck of words so they are in a random order!
    return [...new Set(matched)].sort(() => 0.5 - Math.random());
  },

  // Function: fetchMeaning
  // You give the librarian a word, and it hands you back the scientific definition.
  fetchMeaning: function (word) {
    if (!word || typeof window.STEMDictionary === 'undefined') return "Error: Dictionary offline.";
    const firstLetter = word.charAt(0).toUpperCase();
    const wordsArray = window.STEMDictionary.getWordsByLetter(firstLetter);
    const found = wordsArray.find(w => w.word.toLowerCase() === word.toLowerCase());
    return found ? found.definition : "Error: Definition not found in dictionary.";
  }
};

// =====================================================================
// UI Helpers (The Visual Magicians)
// =====================================================================

// Function: initModal
// Builds the pop-up box that tells you your score. It physically constructs HTML code inside JS.
function initModal() {
  // Never stack duplicate overlays — a leftover full-screen modal blocks every button.
  let overlay = document.getElementById('modal-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'modal-overlay';
    overlay.className = 'hidden';
    overlay.innerHTML = `
      <div class="card modal-card" style="max-width: 400px; margin: auto;">
        <h3 id="modal-title">Notice</h3>
        <p id="modal-text"></p>
        <div id="modal-btn-wrap" style="display:flex; gap:10px; margin-top:20px;">
          <button id="modal-forfeit-btn" class="classic-btn secondary" style="display:none; flex:1;">Forfeit</button>
          <button id="modal-close-btn" class="classic-btn" style="flex:1;">Continue</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    document.getElementById('modal-close-btn').addEventListener('click', () => {
      overlay.classList.add('hidden');
      if (typeof window.modalCallback === 'function') {
        const cb = window.modalCallback;
        window.modalCallback = null;
        cb();
      }
    });

    document.getElementById('modal-forfeit-btn').addEventListener('click', () => {
      overlay.classList.add('hidden');
      if (typeof window.modalForfeitCallback === 'function') {
        const cb = window.modalForfeitCallback;
        window.modalForfeitCallback = null;
        cb();
      }
    });
  } else {
    overlay.classList.add('hidden');
  }

  window.showModal = function (title, text, onContinue, onForfeit) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-text').textContent = text;
    window.modalCallback = onContinue;
    window.modalForfeitCallback = onForfeit;

    const forfeitBtn = document.getElementById('modal-forfeit-btn');
    if (onForfeit) {
      forfeitBtn.style.display = 'block';
    } else {
      forfeitBtn.style.display = 'none';
    }

    overlay.classList.remove('hidden');
  };
}


// Function: applyOsmosisFavicon
// A tiny magic spell that puts the neat little logo in your browser tab.
function applyOsmosisFavicon() {
  const href = 'assets/osmosis-favicon.svg';
  let link = document.querySelector("link[rel='icon']");
  if (!link) {
    link = document.createElement('link');
    link.setAttribute('rel', 'icon');
    document.head.appendChild(link);
  }
  link.setAttribute('type', 'image/svg+xml');
  link.setAttribute('href', href);
}

// Function: navigateWithTransition
// We don't want pages slamming into each other instantly. 
// This creates a tiny half-second delay to show a beautiful fading animation
// BEFORE we throw you into the next webpage (URL).
window.navigateWithTransition = function navigateWithTransition(url, delayMs = 220) {
  if (!url) return;
  const isResults = url.includes('results');
  const actualDelay = isResults ? 700 : delayMs;

  if (typeof AudioManager !== 'undefined') {
    AudioManager.init();
    if (isResults) {
      AudioManager.play('fanfare');
    } else {
      AudioManager.play('warp');
    }
  }
  if (document.body) document.body.classList.add('page-leave'); // Trigger the fade-out CSS animation!
  setTimeout(() => {
    window.location.href = url; // Actually move to the new page
  }, actualDelay);
};

// Function: setupPageTransitions
// The opposite of the above! It handles the fade-IN animation when a new page first loads.
function setupPageTransitions() {
  if (!document.body) return;
  document.body.classList.add('page-preload');
  
  // Background elements removed for maximum performance

  // Background formulas removed for maximum performance

  requestAnimationFrame(() => {
    requestAnimationFrame(() => document.body.classList.remove('page-preload'));
  });
}

// As soon as the browser brings up the page, apply the icon and start the in-fade animation.
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    applyOsmosisFavicon();
    setupPageTransitions();
  });
} else {
  applyOsmosisFavicon();
  setupPageTransitions();
}


// =====================================================================
// General Keyboard Shortcuts (Making things easy)
// =====================================================================

// Look out for people pressing keys on their keyboard...
document.addEventListener('keydown', (e) => {
  // If they smash the "Enter" key...
  if (e.key === 'Enter') {
    // If they were typing in a specific test box, submit that stage's answer.
    if (document.activeElement && (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA')) {
      const active = document.activeElement;
      const submitCandidates = [
        'submit-btn',
        'lap1-submit',
        'lap2-submit-btn'
      ];

      // Prefer stage-specific submit when typing in known answer fields
      if (
        active.classList.contains('meaning-input') ||
        active.classList.contains('s3-input') ||
        active.classList.contains('word-input') ||
        active.id === 'lap1-input' ||
        active.id === 'lap2-input'
      ) {
        for (const id of submitCandidates) {
          const submitBtn = document.getElementById(id);
          if (submitBtn && submitBtn.offsetParent !== null && submitBtn.style.display !== 'none' && !submitBtn.disabled) {
            e.preventDefault();
            submitBtn.click();
            return;
          }
        }
      }
      return;
    }

    // If there is a popup box waiting to be closed, Enter closes it instantly!
    const modalOverlay = document.getElementById('modal-overlay');
    if (modalOverlay && !modalOverlay.classList.contains('hidden')) {
      const closeBtn = document.getElementById('modal-close-btn');
      if (closeBtn) closeBtn.click();
      return;
    }

    // Otherwise, we look around for ANY big primary button on the screen and push it for them.
    const primaryButtons = [
      'login-btn', 'continue-saved-btn', 'play-solo-btn', 'setup-continue-btn',
      's2-finish-btn', 'start-test-early-btn', 'lap1-submit', 'lap2-submit-btn', 'start-lap2-btn',
      'start-test-btn', 'ready-btn', 'submit-btn', 'start-btn', 'next-btn',
      'play-again-btn', 'go-home-btn'
    ];

    for (const id of primaryButtons) {
      const btn = document.getElementById(id);
      if (btn && btn.offsetParent !== null && btn.style.display !== 'none' && !btn.disabled) {
        btn.click();
        break; // Only press one!
      }
    }
  }
});

// =====================================================================
// Developer Cheat Codes (Shhh!)
// =====================================================================
let cheatTapCount = 0;
let cheatTapTimeout = null;

// Look out for fingers tapping on mobile touchscreens...
document.addEventListener('touchstart', (e) => {
  const touch = e.touches[0];
  const screenWidth = window.innerWidth;

  // If they tap specifically in the top right corner (where it's empty)...
  if (touch.clientX > screenWidth - 100 && touch.clientY < 100) {

    // If they already unlocked Dev Mode, a single corner tap auto-completes the level!
    if (sessionStorage.getItem('devMode') === 'true') {
      // Simulate pushing "Alt + P"
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'p', altKey: true, bubbles: true }));

      // Floating text saying "HACK FIRED"
      const floater = document.createElement('div');
      floater.textContent = 'HACK FIRED';
      floater.style.cssText = 'position:fixed; top:80px; right:10px; color:var(--accent-primary); font-weight:bold; font-family:monospace; font-size:1rem; z-index:9999; text-shadow:1px 1px 3px #000; animation: floatUp 0.6s ease-out forwards; pointer-events:none;';
      document.body.appendChild(floater);
      setTimeout(() => floater.remove(), 600);
      return;
    }

    // Every tap we count it. If you tap 5 times fast... you unlock the cheat.
    cheatTapCount++;
    if (cheatTapTimeout) clearTimeout(cheatTapTimeout); // Stop the reset timer

    // Did they hit 5 times?
    if (cheatTapCount >= 5) {
      sessionStorage.setItem('devMode', 'true'); // Backpack updated: You are a god now.

      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'p', altKey: true, bubbles: true }));
      cheatTapCount = 0;

      AudioManager.play('success');
      const floater = document.createElement('div');
      floater.textContent = 'DEV MODE UNLOCKED';
      floater.style.cssText = 'position:fixed; top:50px; right:10px; color:#ff4d4d; font-weight:bold; font-family:monospace; font-size:1.2rem; z-index:9999; text-shadow:2px 2px 4px #000; animation: floatUp 1.5s ease-out forwards; pointer-events:none;';
      document.body.appendChild(floater);
      setTimeout(() => floater.remove(), 1500);
    } else {
      // If you are too slow (take longer than 1 second), the tap combo drops back to 0.
      cheatTapTimeout = setTimeout(() => { cheatTapCount = 0; }, 1000);
    }
  }
});
