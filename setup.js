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
  
  const levelInfo = sharedState.getLevel();

  document.getElementById('setup-status-text').textContent = "Drawing your assignment...";
  
  // Decipher Animation
  let cipherInterval = setInterval(() => {
    let randLen = Math.floor(Math.random() * (levelInfo.maxLen - levelInfo.minLen + 1)) + levelInfo.minLen;
    let randLet = alphabet[Math.floor(Math.random() * alphabet.length)];
    setupCodeEl.textContent = `${randLen},${randLet}`;
    AudioManager.play('chip');
  }, 100);

  // Intelligent word generation ensuring it can be played, constrained to level length bounds
<<<<<<< HEAD
  
  if (!state.usedLetters) state.usedLetters = [];
=======
>>>>>>> 9f63a988d5c66c2f5e88cbbd2d44101fe0e51b88
  
  while (!found && attempts < 10) {
    let availableLetters = alphabet.split('').filter(l => !state.usedLetters.includes(l));
    if (availableLetters.length === 0) {
      state.usedLetters = [];
      availableLetters = alphabet.split('');
    }
    
    if (Math.random() < 0.8) {
      // 80% chance to guarantee picking a length dynamically supported by Fallback
      await DictionaryLogic.initFallback();
      let fallbackWords = Object.keys(DictionaryLogic.fallback).filter(w => 
        w.length >= levelInfo.minLen && 
        w.length <= levelInfo.maxLen &&
        availableLetters.includes(w[0].toUpperCase())
      );
      if (fallbackWords.length === 0) fallbackWords = Object.keys(DictionaryLogic.fallback).filter(w => availableLetters.includes(w[0].toUpperCase()));
      if (fallbackWords.length === 0) fallbackWords = Object.keys(DictionaryLogic.fallback);
      
      const randomWord = fallbackWords[Math.floor(Math.random() * fallbackWords.length)];
      state.letter = randomWord[0].toUpperCase();
      state.length = randomWord.length;
    } else {
      // 20% random length within level limits
      state.letter = availableLetters[Math.floor(Math.random() * availableLetters.length)];
      state.length = Math.floor(Math.random() * (levelInfo.maxLen - levelInfo.minLen + 1)) + levelInfo.minLen;
    }
    
    state.wordsPool = await DictionaryLogic.fetchWords(state.letter, state.length);
    if (state.wordsPool.some(w => w.length === state.length)) {
      found = true;
    }
    attempts++;
  }
  
  // Failsafe Extreme Edge Case guarantee ensuring level compliance
  if (!found) {
    await DictionaryLogic.initFallback();
    let fallbackWords = Object.keys(DictionaryLogic.fallback).filter(w => w.length >= levelInfo.minLen && w.length <= levelInfo.maxLen);
    if (fallbackWords.length === 0) fallbackWords = Object.keys(DictionaryLogic.fallback);
    const safeWord = fallbackWords[0] || "biology";
    state.letter = safeWord[0].toUpperCase();
    state.length = safeWord.length;
    state.wordsPool = await DictionaryLogic.fetchWords(state.letter, state.length);
  }
  
  if (!state.usedLetters.includes(state.letter)) {
    state.usedLetters.push(state.letter);
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
