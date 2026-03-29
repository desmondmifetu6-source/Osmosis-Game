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

function initRound() {
  state.wordsPool.forEach(word => {
    const tile = document.createElement('div');
    tile.className = 'word-tile';
    tile.textContent = word;
    tile.addEventListener('click', () => handleWordClick(tile, word));
    poolContainer.appendChild(tile);
  });
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
    
    tile.style.transform = 'scale(0)';
    tile.style.opacity = '0';
    
    setTimeout(() => {
      tile.remove(); // Remove from top
      
      const pastedNode = document.createElement('div');
      pastedNode.className = 'word-tile pasted-word';
      pastedNode.textContent = word;
      
      // Random rotation for manual aesthetic
      const rot = Math.floor(Math.random() * 8) - 4; // -4 to 4 degrees
      pastedNode.style.animation = `pasteIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards`;
      // We set rotation dynamically inside a wrapper or just trust the transform inheritance.
      // Easiest is to set CSS var or inline
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
  finishBtn.disabled = len < 3;
}

finishBtn.addEventListener('click', () => {
    sharedState.save(state);
    window.location.href = 'round3.html'; // Move to Meaning Exposure phase
});

initRound();
