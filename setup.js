const state = sharedState.load();
if (!state.username) window.location.href = 'index.html';

const setupContinueBtn = document.getElementById('setup-continue-btn');
const setupCodeEl = document.getElementById('setup-code');
const setupDescEl = document.getElementById('setup-desc');

// Reset game state for fresh play
state.score = 0;
state.selectedWords = [];
state.meanings = {};
state.wordsPool = [];

async function generateTarget() {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let found = false;
  let attempts = 0;
  
  document.getElementById('setup-status-text').textContent = "Drawing your assignment...";
  
  // Decipher Animation
  let cipherInterval = setInterval(() => {
    let randLen = Math.floor(Math.random() * 27) + 4; // Lengths 4-30
    let randLet = alphabet[Math.floor(Math.random() * alphabet.length)];
    setupCodeEl.textContent = `${randLen},${randLet}`;
    AudioManager.play('chip');
  }, 100);

  // Intelligent word generation ensuring it can be played, constrained to max length 30
  while (!found && attempts < 10) {
    if (Math.random() < 0.8) {
      // 80% chance to guarantee picking a length dynamically supported by Fallback
      const fallbackWords = Object.keys(DictionaryLogic.fallback).filter(w => w.length <= 30);
      const randomWord = fallbackWords[Math.floor(Math.random() * fallbackWords.length)];
      state.letter = randomWord[0].toUpperCase();
      state.length = randomWord.length;
    } else {
      // 20% random length
      state.letter = alphabet[Math.floor(Math.random() * alphabet.length)];
      state.length = Math.floor(Math.random() * (30 - 4 + 1)) + 4;
    }
    
    state.wordsPool = await DictionaryLogic.fetchWords(state.letter, state.length);
    if (state.wordsPool.some(w => w.length === state.length)) {
      found = true;
    }
    attempts++;
  }
  
  // Failsafe Extreme Edge Case guarantee (Max 30)
  if (!found) {
    state.letter = "A";
    state.length = 7;
    state.wordsPool = await DictionaryLogic.fetchWords(state.letter, state.length);
  }
  
  clearInterval(cipherInterval);
  AudioManager.play('success');
  
  sharedState.save(state);
  
  document.getElementById('setup-status-text').textContent = "Assignment Confirmed.";
  setupCodeEl.innerHTML = `<span style="animation: pulse 1s ease-in-out;">${state.length},${state.letter}</span>`;
  setupDescEl.innerHTML = `Target Acquired.<br>Find words starting with '<strong>${state.letter}</strong>' that are exactly <strong>${state.length}</strong> letters long.`;
  setupContinueBtn.style.display = 'block';
}

setupContinueBtn.addEventListener('click', () => {
  window.location.href = 'round1.html';
});

generateTarget();
