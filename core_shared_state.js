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

    // We create a new folder for the specific stage, saving your score and the time you finished it.
    state.stageScores[stageKey] = {
      label: stageLabel || stageKey,
      score: Number(score) || 0,
      at: Date.now()
    };
    this.save(state);

    // Multiplayer Reporting: If we are in a battle, tell the server!
    if (state.multiplayerMode && state.currentRoomId) {
      this.reportScoreToServer(state.currentRoomId, state.score || 0);
    }
  },

  reportScoreToServer: function(roomId, score) {
    // assumption: socket.io client is loaded in the page
    if (typeof io !== 'undefined') {
      if (!this.socket) this.socket = io();
      this.socket.emit('update_score', { 
        roomId: roomId, 
        score: score,
        username: localStorage.getItem('osmosis_user') || 'Guest'
      });
    }
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
    const state = this.load();
    if (!state.startTime) return;

    const el = elementId === 'global-game-timer' ? this.ensureGlobalTimer() : document.getElementById(elementId);
    if (!el) return;

    // This is a special loop that updates the clock super fast alongside the screen refresh rate,
    // so it looks incredibly smooth.
    const update = () => {
      const now = Date.now();
      const currentElapsed = state.totalTime + (now - state.startTime);
      el.textContent = this.getFormattedTime(currentElapsed); // Update the text on screen
      if (state.startTime) requestAnimationFrame(update); // Repeat forever until stopped!
    };
    update();
  },

  // Function: getLevel
  // This determines your overall Rank in the game based on your total persistent score.
  getLevel: function () {
    // Look for the absolute total score across all play sessions
    const score = parseInt(localStorage.getItem('osmosis_total_score')) || 0;

    // If you have a ton of points, you get higher ranks!
    if (score >= 3001) return { name: 'Titan', minLen: 12, maxLen: 30, next: Infinity };
    if (score >= 1501) return { name: 'Oak', minLen: 9, maxLen: 11, next: 3001 };
    if (score >= 501) return { name: 'Sprout', minLen: 6, maxLen: 8, next: 1501 };
    return { name: 'Seed', minLen: 4, maxLen: 5, next: 501 };
  }
};

// =====================================================================
// AudioManager: The Sound Effects Department
// =====================================================================
// This creates all those cool little bloops and bleeps you hear.
const AudioManager = {
  ctx: null,

  // Function: init
  // Starts up the "Sound Engine" inside the browser.
  init: function () {
    if (!this.ctx) {
      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioContext(); // We buy a brand new synthesizer
      } catch (err) { }
    }
  },

  // Function: play
  // Instead of using pre-recorded MP3 files, this ACTUALLY GENERATES SOUNDWAVES 
  // live using math! 
  play: function (type) {
    if (!this.ctx) return;
    // Sometimes browsers pause the sound engine to save battery. We wake it up.
    if (this.ctx.state === 'suspended') this.ctx.resume();

    const osc = this.ctx.createOscillator(); // Oscillator = The thing that vibrates to make sound
    const gain = this.ctx.createGain(); // Gain = The Volume Knob

    osc.connect(gain); // Connect the instrument to the volume knob
    gain.connect(this.ctx.destination); // Connect the volume knob to your computer speakers

    const now = this.ctx.currentTime;

    // Depending on what we want to hear, we change the shape of the soundwave!
    switch (type) {
      case 'click':
        // A simple smooth 'sine' wave that gently fades out.
        osc.type = 'sine'; osc.frequency.setValueAtTime(150, now); osc.frequency.exponentialRampToValueAtTime(40, now + 0.1);
        gain.gain.setValueAtTime(1, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
        osc.start(now); osc.stop(now + 0.1); break;
      case 'chip':
        // A sharp, jagged 'triangle' wave that sounds somewhat digital.
        osc.type = 'triangle'; osc.frequency.setValueAtTime(300, now); osc.frequency.exponentialRampToValueAtTime(100, now + 0.1);
        gain.gain.setValueAtTime(0.5, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
        osc.start(now); osc.stop(now + 0.1); break;
      case 'success':
        osc.type = 'sine'; osc.frequency.setValueAtTime(440, now); osc.frequency.setValueAtTime(554, now + 0.1);
        gain.gain.setValueAtTime(0, now); gain.gain.linearRampToValueAtTime(0.5, now + 0.05); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
        osc.start(now); osc.stop(now + 0.5); break;
      case 'error':
        // A buzzing 'sawtooth' wave that sounds a bit harsh and alerting.
        osc.type = 'sawtooth'; osc.frequency.setValueAtTime(100, now); osc.frequency.exponentialRampToValueAtTime(50, now + 0.2);
        gain.gain.setValueAtTime(0.5, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
        osc.start(now); osc.stop(now + 0.2); break;
    }
  }
};

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

  // Function: fetchWords
  // You hand the librarian a Letter and a Length, and it digs through 
  // the filing cabinet to bring you matched scientific words.
  fetchWords: function (letter, length) {
    if (typeof window.STEMDictionary === 'undefined') return [];
    const words = window.STEMDictionary.getWordsByLetter(letter);

    // We try to find words that match the exact target length first, AND have a valid definition!
    let matched = words.filter(w => w.definition && w.definition.trim() !== "")
      .filter(w => w.word.length === length)
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
  const overlay = document.createElement('div');
  overlay.id = 'modal-overlay';
  overlay.className = 'hidden';
  // Notice the backticks (` `). They let us write multi-line HTML string easily.
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
  document.body.appendChild(overlay); // Stick it onto the page

  // When you click close, we just hide it by putting the 'hidden' class back on.
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
  }
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
  if (document.body) document.body.classList.add('page-leave'); // Trigger the fade-out CSS animation!
  setTimeout(() => {
    window.location.href = url; // Actually move to the new page
  }, delayMs);
};

// Function: setupPageTransitions
// The opposite of the above! It handles the fade-IN animation when a new page first loads.
function setupPageTransitions() {
  if (!document.body) return;
  document.body.classList.add('page-preload');
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
    // If they were typing in a specific test box, we try to submit the answer.
    if (document.activeElement && (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA')) {
      if (document.activeElement.classList.contains('meaning-input')) {
        const submitBtn = document.getElementById('submit-btn');
        if (submitBtn && submitBtn.offsetParent !== null && !submitBtn.disabled) {
          submitBtn.click();
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
      's2-finish-btn', 'start-test-early-btn', 'lap1-submit', 'start-lap2-btn',
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
