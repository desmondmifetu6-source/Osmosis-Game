initModal();
const state = sharedState.load();
if (!state.selectedWords || state.selectedWords.length === 0) window.location.href = 'index.html';

// DOM Elements
const loadingContainer = document.getElementById('loading-container');
const revisionContainer = document.getElementById('revision-container');
const lap1Container = document.getElementById('lap1-container');
const transitionContainer = document.getElementById('transition-container');
const lap2Container = document.getElementById('lap2-container');

// State tracking
let testSequence = [];
let lap1Index = 0;
let lap1Score = 0;
let lap2Score = 0;
let lap2Identified = [];

// Timers
let globalTimerInt = null;

async function bootstrapStage() {
  if (!state.meanings) state.meanings = {};
  for (let w of state.selectedWords) {
    if (!state.meanings[w]) {
       state.meanings[w] = await DictionaryLogic.fetchMeaning(w);
    }
  }
  sharedState.save(state);
  testSequence = [...state.selectedWords].sort(() => 0.5 - Math.random());
  
  loadingContainer.style.display = 'none';
  startRevisionPhase();
}

/* =========================================
   REVISION PHASE
========================================= */
function startRevisionPhase() {
  revisionContainer.style.display = 'block';
  
  const listEl = document.getElementById('rev-list');
  state.selectedWords.forEach(w => {
    const item = document.createElement('div');
    item.className = 'revision-item';
    item.innerHTML = `<strong>${w}</strong><p>${state.meanings[w]}</p>`;
    listEl.appendChild(item);
  });
  
  // Calculate dynamic time: 8 seconds per word
  let timeLeft = state.selectedWords.length * 8;
  const timeEl = document.getElementById('rev-timer');
  
  const tick = () => {
    const min = String(Math.floor(timeLeft / 60)).padStart(2, '0');
    const sec = String(timeLeft % 60).padStart(2, '0');
    timeEl.textContent = `${min}:${sec}`;
    if (timeLeft <= 0) {
      clearInterval(globalTimerInt);
      endRevisionPhase();
    }
    timeLeft--;
  };
  tick();
  globalTimerInt = setInterval(tick, 1000);
  
  document.getElementById('start-test-early-btn').addEventListener('click', () => {
    clearInterval(globalTimerInt);
    endRevisionPhase();
  });
}

function endRevisionPhase() {
  revisionContainer.style.display = 'none';
  showModal('Attention', 'Your test starts now.');
  // Give them a moment to read the modal before UI shifts
  setTimeout(() => {
    startLap1Phase();
  }, 1500);
}

/* =========================================
   LAP 1 PHASE (Missing Letters)
========================================= */
function maskWord(word) {
  let arr = word.toUpperCase().split('');
  let numToMask = Math.max(1, Math.floor(word.length * 0.4)); // Mask 40%
  let indices = [];
  while(indices.length < numToMask) {
    let r = Math.floor(Math.random() * word.length);
    if(!indices.includes(r)) indices.push(r);
  }
  indices.forEach(i => arr[i] = '_');
  return arr.join(' ');
}

function startLap1Phase() {
  lap1Container.style.display = 'block';
  document.getElementById('scoreboard').style.display = 'block';
  renderLap1Current();
}

function renderLap1Current() {
  const currentWord = testSequence[lap1Index];
  document.getElementById('lap1-word-display').textContent = maskWord(currentWord);
  
  const inputEl = document.getElementById('lap1-input');
  const feedEl = document.getElementById('lap1-feedback');
  const btn = document.getElementById('lap1-submit');
  
  inputEl.value = '';
  inputEl.disabled = false;
  inputEl.focus();
  feedEl.textContent = '';
  feedEl.className = 'feedback';
  btn.textContent = "Submit Answer";
  
  document.getElementById('lap1-progress').textContent = `${lap1Index + 1} / ${testSequence.length}`;
}

document.getElementById('lap1-submit').addEventListener('click', processLap1Answer);
document.getElementById('lap1-input').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') processLap1Answer();
});

function processLap1Answer() {
  const btn = document.getElementById('lap1-submit');
  if (btn.textContent === "Next") {
    lap1Index++;
    if (lap1Index < testSequence.length) {
      renderLap1Current();
    } else {
      lap1Container.style.display = 'none';
      startTransitionPhase();
    }
    return;
  }
  
  const currentWord = testSequence[lap1Index];
  const inputEl = document.getElementById('lap1-input');
  const feedEl = document.getElementById('lap1-feedback');
  const userAns = inputEl.value.trim().toLowerCase();
  
  if (!userAns) return;
  inputEl.disabled = true;
  
  if (userAns === currentWord.toLowerCase()) {
    feedEl.textContent = "Correct!";
    feedEl.className = 'feedback success';
    AudioManager.play('success');
    
    spawnFloatingPoint(inputEl, 10);
    lap1Score += 10;
    updateScoreboard();
  } else {
    feedEl.textContent = `Incorrect. Word was "${currentWord}".`;
    feedEl.className = 'feedback error';
    AudioManager.play('error');
  }
  
  btn.textContent = "Next";
}

/* =========================================
   TRANSITION & LAP 2 PHASE
========================================= */
function startTransitionPhase() {
  transitionContainer.style.display = 'block';
}

document.getElementById('start-lap2-btn').addEventListener('click', () => {
  transitionContainer.style.display = 'none';
  startLap2Phase();
});

function startLap2Phase() {
  lap2Container.style.display = 'block';
  
  // Alarming timer: e.g. 5 sec per selected word
  let timeLeft = state.selectedWords.length * 6; // Max 60s for 10 words
  const timeEl = document.getElementById('lap2-timer');
  const inputEl = document.getElementById('lap2-input');
  const feedEl = document.getElementById('lap2-feedback');
  
  inputEl.focus();
  
  const tick = () => {
    const min = String(Math.floor(timeLeft / 60)).padStart(2, '0');
    const sec = String(timeLeft % 60).padStart(2, '0');
    timeEl.textContent = `${min}:${sec}`;
    
    if (timeLeft <= 0) {
      clearInterval(globalTimerInt);
      endLap2();
    } else if (timeLeft <= 10) {
      AudioManager.play('click'); // ticking sound
    }
    timeLeft--;
  };
  tick();
  globalTimerInt = setInterval(tick, 1000);
  
  inputEl.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const val = inputEl.value.trim().toLowerCase();
      inputEl.value = '';
      if (!val) return;
      
      if (lap2Identified.includes(val)) {
        feedEl.textContent = "Already appended!";
        feedEl.className = 'feedback error';
        return;
      }
      
      if (state.selectedWords.map(w => w.toLowerCase()).includes(val)) {
        lap2Identified.push(val);
        feedEl.textContent = "Match!";
        feedEl.className = 'feedback success';
        AudioManager.play('chip');
        
        spawnFloatingPoint(inputEl, 20);
        lap2Score += 20;
        updateScoreboard();
        
        // append tile
        const t = document.createElement('div');
        t.className = 'word-tile';
        t.textContent = val;
        document.getElementById('lap2-words-list').appendChild(t);
        
        // If they got all of them early
        if (lap2Identified.length === state.selectedWords.length) {
          clearInterval(globalTimerInt);
          setTimeout(endLap2, 1000);
        }
      } else {
        feedEl.textContent = "Not in your selection.";
        feedEl.className = 'feedback error';
        AudioManager.play('error');
      }
    }
  });
}

function spawnFloatingPoint(refElement, amount) {
  const rect = refElement.getBoundingClientRect();
  const floater = document.createElement('div');
  floater.className = 'floating-point';
  floater.textContent = `+${amount}`;
  floater.style.left = `${rect.left + rect.width / 2}px`;
  floater.style.top = `${rect.top - 20}px`;
  document.body.appendChild(floater);
  setTimeout(() => floater.remove(), 1000);
}

function updateScoreboard() {
  document.getElementById('current-score').textContent = lap1Score + lap2Score;
}

function endLap2() {
  lap2Container.style.display = 'none';
  document.getElementById('scoreboard').style.display = 'none';
  
  // Scoring Math
  state.score = lap1Score + lap2Score;
  sharedState.save(state);
  
  AudioManager.play('success');
  showModal("Assessment Concluded", `You remembered ${lap2Identified.length} out of ${state.selectedWords.length} words under pressure. Total Score: ${state.score}.`);
  
  setTimeout(() => {
    window.location.href = 'round5.html';
  }, 4000);
}

// Bootstrap
bootstrapStage();

// Developer Cheat
document.addEventListener('keydown', (e) => {
  if (e.key.toLowerCase() === 'p' && e.altKey) {
    e.preventDefault();
    if (revisionContainer.style.display !== 'none') {
      document.getElementById('start-test-early-btn').click();
    } else if (lap1Container.style.display !== 'none') {
      const input = document.getElementById('lap1-input');
      input.value = testSequence[lap1Index];
      document.getElementById('lap1-submit').click();
    } else if (transitionContainer.style.display !== 'none') {
      document.getElementById('start-lap2-btn').click();
    } else if (lap2Container.style.display !== 'none') {
      const input = document.getElementById('lap2-input');
      state.selectedWords.forEach(w => {
        if (!lap2Identified.includes(w.toLowerCase())) {
          input.value = w;
          input.dispatchEvent(new KeyboardEvent('keypress', { key: 'Enter' }));
        }
      });
    }
  }
});
