initModal();
const state = sharedState.load();
if (!state.username) window.location.href = 'index.html';

// If coming straight to this page without a letter, assign one.
if (!state.letter && typeof STEMDictionary !== 'undefined') {
  state.letter = STEMDictionary.getRandomLetter();
  state.length = 8;
  sharedState.save(state);
} else if (!state.letter) {
  state.letter = 'A';
}

const targetLetter = state.letter.toUpperCase();
document.getElementById('s1-target').textContent = targetLetter;

const columnEl = document.getElementById('letter-column');
const timerEl = document.getElementById('s1-timer');

let timeLeft = 10;
let timerInt;

function initStage1() {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
  
  alphabet.forEach(letter => {
    const plank = document.createElement('div');
    plank.className = 'wooden-plank';
    plank.textContent = letter; // Stacked A to Z
    
    plank.addEventListener('click', () => handlePlankClick(plank, letter));
    columnEl.appendChild(plank);
  });

  startTimer();
}

function startTimer() {
  timerEl.textContent = `${timeLeft}s`;
  timerInt = setInterval(() => {
    timeLeft--;
    timerEl.textContent = `${timeLeft}s`;
    
    if (timeLeft <= 0) {
      clearInterval(timerInt);
      showModal('Time\'s Up!', 'You failed to find the letter in time.');
      // Auto-fail or return to setup
      setTimeout(() => {
        window.location.href = 'setup.html';
      }, 3000);
    }
  }, 1000);
}

function handlePlankClick(plank, letter) {
  if (timeLeft <= 0) return;
  
  if (letter === targetLetter) {
    clearInterval(timerInt);
    AudioManager.play('success');
    plank.classList.add('plank-correct');
    
    // Smooth transition to stage 2 (round2.html)
    setTimeout(() => {
      window.location.href = 'round2.html';
    }, 1200);
  } else {
    AudioManager.play('error');
    plank.classList.add('plank-wrong');
    setTimeout(() => {
      plank.classList.remove('plank-wrong');
    }, 400); // Remove class to allow multiple shakes
  }
}

// Initializing the round
document.addEventListener('DOMContentLoaded', () => {
    initStage1();
});

// Developer Cheat
document.addEventListener('keydown', (e) => {
  if (e.key.toLowerCase() === 'p' && e.altKey) {
    e.preventDefault();
    const planks = document.querySelectorAll('.wooden-plank');
    for (let plank of planks) {
      if (plank.textContent === targetLetter) { plank.click(); break; }
    }
  }
});
