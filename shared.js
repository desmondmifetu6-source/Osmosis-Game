const sharedState = {
  load: function() {
    return JSON.parse(sessionStorage.getItem('gameState')) || {
      username: '', letter: '', length: 0, wordsPool: [],
      selectedWords: [], meanings: {}, score: 0
    };
  },
  save: function(state) {
    sessionStorage.setItem('gameState', JSON.stringify(state));
  },
  getLevel: function() {
    const score = parseInt(localStorage.getItem('osmosis_total_score')) || 0;
    if (score >= 3001) return { name: 'Titan', minLen: 12, maxLen: 30, next: Infinity };
    if (score >= 1501) return { name: 'Oak', minLen: 9, maxLen: 11, next: 3001 };
    if (score >= 501) return { name: 'Sprout', minLen: 6, maxLen: 8, next: 1501 };
    return { name: 'Seed', minLen: 4, maxLen: 5, next: 501 };
  }
};

const AudioManager = {
  ctx: null,
  init: function() {
    if (!this.ctx) {
      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioContext();
      } catch (err) {}
    }
  },
  play: function(type) {
    if (!this.ctx) return;
    if (this.ctx.state === 'suspended') this.ctx.resume();
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    const now = this.ctx.currentTime;
    
    switch(type) {
      case 'click':
        osc.type = 'sine'; osc.frequency.setValueAtTime(150, now); osc.frequency.exponentialRampToValueAtTime(40, now + 0.1);
        gain.gain.setValueAtTime(1, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
        osc.start(now); osc.stop(now + 0.1); break;
      case 'chip':
        osc.type = 'triangle'; osc.frequency.setValueAtTime(300, now); osc.frequency.exponentialRampToValueAtTime(100, now + 0.1);
        gain.gain.setValueAtTime(0.5, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
        osc.start(now); osc.stop(now + 0.1); break;
      case 'success':
        osc.type = 'sine'; osc.frequency.setValueAtTime(440, now); osc.frequency.setValueAtTime(554, now + 0.1);
        gain.gain.setValueAtTime(0, now); gain.gain.linearRampToValueAtTime(0.5, now + 0.05); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
        osc.start(now); osc.stop(now + 0.5); break;
      case 'error':
        osc.type = 'sawtooth'; osc.frequency.setValueAtTime(100, now); osc.frequency.exponentialRampToValueAtTime(50, now + 0.2);
        gain.gain.setValueAtTime(0.5, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
        osc.start(now); osc.stop(now + 0.2); break;
    }
  }
};

document.addEventListener('click', (e) => {
  AudioManager.init();
  if (e.target.closest('.classic-btn')) AudioManager.play('click');
  else if (e.target.closest('.word-chip')) {
    setTimeout(() => {
      if (e.target.closest('.word-chip').classList.contains('wrong')) AudioManager.play('error');
      else AudioManager.play('chip');
    }, 10);
  }
});

const DictionaryLogic = {
  fallback: {},
  _loaded: false,
  initFallback: async function() {
    if (this._loaded) return;
    try {
      const res = await fetch('dictionary.json');
      this.fallback = await res.json();
      this._loaded = true;
    } catch {
      this.fallback = { "abyssal": "Ocean depths", "osmosis": "diffusion", "biology": "study of life" }; // simple ultimate failsafe
    }
  },
  fetchWords: async function(letter, length) {
    await this.initFallback();
    try {
      const pattern = letter.toLowerCase() + "?".repeat(length - 1);
      const res = await fetch(`https://api.datamuse.com/words?sp=${pattern}&topics=science&max=100`);
      let words = await res.json();
      words = words.filter(w => /^[a-zA-Z]+$/.test(w.word)).sort(() => 0.5 - Math.random());
      
      if(words.length > 0) return words.slice(0, 20).map(w => w.word);
      throw new Error("No words");
    } catch {
      let matched = Object.keys(this.fallback).filter(w => w.startsWith(letter.toLowerCase()) && w.length === length);
      if(matched.length < 5) matched = matched.concat(Object.keys(this.fallback).filter(w => w.startsWith(letter.toLowerCase())));
      if(matched.length < 15) matched = matched.concat(Object.keys(this.fallback));
      return [...new Set(matched)].slice(0, 20).sort(() => 0.5 - Math.random());
    }
  },
  fetchMeaning: async function(word) {
    await this.initFallback();
    try {
      if(this.fallback[word.toLowerCase()]) return this.fallback[word.toLowerCase()];
      const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
      const data = await res.json();
      for(let entry of data) for(let meaning of entry.meanings) for(let def of meaning.definitions) if(def.definition) return def.definition;
      throw new Error("No meaning");
    } catch {
      return "A highly specialized scientific term or biological construct heavily studied in standard academic fields.";
    }
  }
};

function initModal() {
  const overlay = document.createElement('div');
  overlay.id = 'modal-overlay';
  overlay.className = 'hidden';
  overlay.innerHTML = `
    <div class="card modal-card" style="max-width: 400px; margin: auto;">
      <h3 id="modal-title">Notice</h3>
      <p id="modal-text"></p>
      <button id="modal-close-btn" class="classic-btn" style="margin-top:20px;">Close</button>
    </div>
  `;
  document.body.appendChild(overlay);
  
  document.getElementById('modal-close-btn').addEventListener('click', () => {
    overlay.classList.add('hidden');
  });
  
  window.showModal = function(title, text) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-text').textContent = text;
    overlay.classList.remove('hidden');
  }
}


// Global Enter Key Navigation
document.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    // Let specific pages handle Enter inside inputs, except for round4's meaning input
    if (document.activeElement && (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA')) {
      if (document.activeElement.classList.contains('meaning-input')) {
        const submitBtn = document.getElementById('submit-btn');
        if (submitBtn && submitBtn.offsetParent !== null && !submitBtn.disabled) {
          submitBtn.click();
        }
      }
      return; 
    }

    // Modal takes highest priority
    const modalOverlay = document.getElementById('modal-overlay');
    if (modalOverlay && !modalOverlay.classList.contains('hidden')) {
      const closeBtn = document.getElementById('modal-close-btn');
      if (closeBtn) closeBtn.click();
      return;
    }

    // Sequence of priority buttons for progression
    const primaryButtons = [
      'login-btn',
      'continue-saved-btn',
      'play-solo-btn',
      'setup-continue-btn',
      's2-finish-btn',
      'start-test-early-btn',
      'lap1-submit',
      'start-lap2-btn',
      'start-test-btn',
      'ready-btn',
      'submit-btn',
      'start-btn',
      'next-btn',
      'play-again-btn',
      'go-home-btn'
    ];

    for (const id of primaryButtons) {
      const btn = document.getElementById(id);
      // Check if button exists, is visible, and is not disabled
      if (btn && btn.offsetParent !== null && btn.style.display !== 'none' && !btn.disabled) {
        btn.click();
        break;
      }
    }
  }
});

// Mobile Developer Cheat (5 rapid taps unlocks Dev Mode)
let cheatTapCount = 0;
let cheatTapTimeout = null;

document.addEventListener('touchstart', (e) => {
  const touch = e.touches[0];
  const screenWidth = window.innerWidth;
  
  // Check if tap is in the top-right corner (approx 100x100 box)
  if (touch.clientX > screenWidth - 100 && touch.clientY < 100) {
    // If Dev Mode is already unlocked for this session, just 1 tap fires the cheat!
    if (sessionStorage.getItem('devMode') === 'true') {
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'p', altKey: true, bubbles: true }));
      const floater = document.createElement('div');
      floater.textContent = 'HACK FIRED';
      floater.style.cssText = 'position:fixed; top:80px; right:10px; color:var(--accent-primary); font-weight:bold; font-family:monospace; font-size:1rem; z-index:9999; text-shadow:1px 1px 3px #000; animation: floatUp 0.6s ease-out forwards; pointer-events:none;';
      document.body.appendChild(floater);
      setTimeout(() => floater.remove(), 600);
      return;
    }

    cheatTapCount++;
    if (cheatTapTimeout) clearTimeout(cheatTapTimeout);
    
    if (cheatTapCount >= 5) {
      // Unlock Dev Mode securely in the background
      sessionStorage.setItem('devMode', 'true');
      
      // Trigger the existing Alt+P developer hack natively
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'p', altKey: true, bubbles: true }));
      cheatTapCount = 0;
      
      // Visual & Audio confirmation
      AudioManager.play('success');
      const floater = document.createElement('div');
      floater.textContent = 'DEV MODE UNLOCKED';
      floater.style.cssText = 'position:fixed; top:50px; right:10px; color:#ff4d4d; font-weight:bold; font-family:monospace; font-size:1.2rem; z-index:9999; text-shadow:2px 2px 4px #000; animation: floatUp 1.5s ease-out forwards; pointer-events:none;';
      document.body.appendChild(floater);
      setTimeout(() => floater.remove(), 1500);
    } else {
      cheatTapTimeout = setTimeout(() => { cheatTapCount = 0; }, 1000);
    }
  }
});
