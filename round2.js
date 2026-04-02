/**
 * ROUND 2: Word Collection
 * The player must collect exactly 10 words that start with the previously assigned letter 
 * and match the designated character length. Words spawn dynamically based on difficulty.
 */
initModal();
const state = sharedState.load();
if (!state.letter || !state.length || !state.wordsPool) {
  window.location.href = 'index.html';
}

document.getElementById('s2-letter').textContent = state.letter.toUpperCase();
document.getElementById('s2-length').textContent = state.length;

const poolContainer = document.getElementById('word-pool');
const boardContainer = document.getElementById('pasted-words');
const countEl = document.getElementById('s2-count');
const finishBtn = document.getElementById('s2-finish-btn');

state.selectedWords = [];

let spawnIntervalId = null;

function initRound() {
  const level = sharedState.getLevel().name;
  
  if (level === 'Titan') {
    state.wordsPool.forEach(word => {
      spawnStaticWord(word);
    });
  } else {
    // Falling mode for Seed, Sprout, Oak
    let spawnRate = 2000;
    let fallSpeed = 8; // seconds
    
    if (level === 'Sprout') {
      spawnRate = 1200;
      fallSpeed = 5;
    } else if (level === 'Oak') {
      spawnRate = 600;
      fallSpeed = 3;
    }
    
    let poolIndex = 0;
    // Spawn initial word
    spawnFallingWord(state.wordsPool[0], fallSpeed);
    poolIndex++;
    
    spawnIntervalId = setInterval(() => {
      if (state.selectedWords.length >= 10) {
        clearInterval(spawnIntervalId);
        return;
      }
      
      const word = state.wordsPool[poolIndex];
      spawnFallingWord(word, fallSpeed);
      
      poolIndex = (poolIndex + 1) % state.wordsPool.length;
    }, spawnRate);
  }
}

function spawnStaticWord(word) {
  const tile = document.createElement('div');
  tile.className = 'word-tile';
<<<<<<< HEAD
  if (word.length === state.length) tile.classList.add('correct-length');
=======
>>>>>>> 9f63a988d5c66c2f5e88cbbd2d44101fe0e51b88
  tile.textContent = word;
  tile.addEventListener('click', () => handleWordClick(tile, word));
  poolContainer.appendChild(tile);
}

function spawnFallingWord(word, duration) {
  const tile = document.createElement('div');
  tile.className = 'word-tile falling-word';
<<<<<<< HEAD
  if (word.length === state.length) tile.classList.add('correct-length');
=======
>>>>>>> 9f63a988d5c66c2f5e88cbbd2d44101fe0e51b88
  tile.textContent = word;
  
  // Random horizontal position (5% to 85% to keep within container)
  const randomX = Math.floor(Math.random() * 80) + 5;
  tile.style.left = `${randomX}%`;
  tile.style.animationDuration = `${duration}s`;
  
  tile.addEventListener('click', () => handleWordClick(tile, word));
  
  // Remove if it reaches the bottom
  tile.addEventListener('animationend', () => {
    if (tile.parentNode === poolContainer) {
      tile.remove();
    }
  });
  
  poolContainer.appendChild(tile);
}

function handleWordClick(tile, word) {
  // Prevent double collection
  if (state.selectedWords.includes(word)) return;
  
  // Validation against designated length
  const isValidLength = word.length === state.length || !state.wordsPool.some(w => w.length === state.length);
  
  if (isValidLength) {
    if (state.selectedWords.length >= 10) {
      showModal('Limit Reached', 'You can only collect a maximum of 10 words.');
      return;
    }
    
    // Paste animation sequence
    state.selectedWords.push(word);
    AudioManager.play('success');
    
    // Stop fall animation to apply static transition
    tile.style.animation = 'none';
    
    // Force reflow so transition works from current position, or simply override
    tile.style.transform = 'scale(0)';
    tile.style.opacity = '0';
    
    setTimeout(() => {
      if (tile.parentNode) tile.remove(); // Remove from top
      
      const pastedNode = document.createElement('div');
      pastedNode.className = 'word-tile pasted-word';
      pastedNode.textContent = word;
      
      // Random rotation for manual aesthetic
      const rot = Math.floor(Math.random() * 8) - 4; // -4 to 4 degrees
      pastedNode.style.animation = `pasteIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards`;
      pastedNode.style.transform = `rotate(${rot}deg)`;
      
      boardContainer.appendChild(pastedNode);
      updateCount();
    }, 200);
    
  } else {
    // Wrong length glow constraint
    AudioManager.play('error');
    tile.classList.add('wrong');
    setTimeout(() => tile.classList.remove('wrong'), 500);
  }
}

function updateCount() {
  const len = state.selectedWords.length;
  countEl.textContent = len;
  finishBtn.disabled = false;
}

finishBtn.addEventListener('click', () => {
    if (spawnIntervalId) clearInterval(spawnIntervalId);
    sharedState.save(state);
    window.location.href = 'round3.html'; // Move to Meaning Exposure phase
});

initRound();

// Developer Cheat
document.addEventListener('keydown', (e) => {
  if (e.key.toLowerCase() === 'p' && e.altKey) {
    e.preventDefault();
    if (spawnIntervalId) clearInterval(spawnIntervalId);
    const validWords = state.wordsPool.filter(w => w.length === state.length);
    state.selectedWords = validWords.slice(0, 10);
<<<<<<< HEAD
=======
    if (state.selectedWords.length < 3) state.selectedWords = state.wordsPool.slice(0, 10);
>>>>>>> 9f63a988d5c66c2f5e88cbbd2d44101fe0e51b88
    sharedState.save(state);
    finishBtn.disabled = false;
    finishBtn.click();
  }
});
