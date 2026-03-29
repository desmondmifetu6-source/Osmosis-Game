initModal();
const state = sharedState.load();
if (!state.selectedWords || state.selectedWords.length === 0) window.location.href = 'index.html';

// DOM Elements
const loadingContainer = document.getElementById('loading-container');
const revisionContainer = document.getElementById('revision-container');
const testContainer = document.getElementById('test-container');

// State tracking
let testSequence = [];
let testIndex = 0;
let round4Score = 0;

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

function startRevisionPhase() {
  revisionContainer.style.display = 'block';
  document.getElementById('scoreboard').style.display = 'block'; // Ensure score is visible
  document.getElementById('current-score').textContent = state.score || 0;
  
  const listEl = document.getElementById('rev-list');
  state.selectedWords.forEach(w => {
    const item = document.createElement('div');
    item.className = 'revision-item';
    item.innerHTML = `<strong>${w}</strong><p>${state.meanings[w]}</p>`;
    listEl.appendChild(item);
  });
  
  // Dynamic time: 10 seconds per word (more forgiving for reading meanings)
  let timeLeft = state.selectedWords.length * 10; 
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
  
  document.getElementById('start-test-btn').addEventListener('click', () => {
    clearInterval(globalTimerInt);
    endRevisionPhase();
  });
}

function endRevisionPhase() {
  revisionContainer.style.display = 'none';
  showModal('Attention', 'The final Mastery Test begins now.');
  setTimeout(() => {
    startTestPhase();
  }, 1500);
}

function startTestPhase() {
  testContainer.style.display = 'block';
  renderTestCurrent();
}

function renderTestCurrent() {
  const currentWord = testSequence[testIndex];
  document.getElementById('test-word').textContent = currentWord;
  document.getElementById('test-progress').textContent = `${testIndex + 1}/${testSequence.length}`;
  
  const meaning = state.meanings[currentWord];
  
  // Masking Algorithm for definitions
  // Splits by boundaries but keeps punctuation
  let tokens = meaning.split(/(\b[\w'-]+\b)/); 
  
  let validIndices = [];
  tokens.forEach((t, i) => {
    // We only mask words > 3 letters that are alphabetical, and ignore perfectly matched words with the target word itself
    if (t.length > 3 && /^[a-zA-Z]+$/.test(t) && t.toLowerCase() !== currentWord.toLowerCase()) {
      validIndices.push(i);
    }
  });
  
  // Pick roughly 30% of eligible words, min 2, max 4.
  let targetMasks = Math.min(4, Math.max(2, Math.floor(validIndices.length * 0.3)));
  validIndices = validIndices.sort(() => 0.5 - Math.random()).slice(0, targetMasks);
  
  let html = '';
  tokens.forEach((t, i) => {
    if (validIndices.includes(i)) {
      html += `<input type="text" class="meaning-input" data-ans="${t.toLowerCase()}" autocomplete="off" style="width: ${t.length * 0.8}em;">`;
    } else {
      html += t;
    }
  });
  
  document.getElementById('test-meaning-container').innerHTML = html;
  
  const btn = document.getElementById('submit-btn');
  btn.textContent = "Submit Findings";
  btn.disabled = false;
  document.getElementById('skip-btn').disabled = false;
  
  document.getElementById('test-feedback').textContent = '';
  document.getElementById('test-feedback').className = 'feedback';
  
  // Autofocus first input if exists
  const firstInput = document.querySelector('.meaning-input');
  if (firstInput) firstInput.focus();
}

document.getElementById('submit-btn').addEventListener('click', processValidation);
document.getElementById('skip-btn').addEventListener('click', skipWord);

function processValidation() {
  const btn = document.getElementById('submit-btn');
  if (btn.textContent === "Next Definition") {
    nextWord();
    return;
  }
  
  const inputs = document.querySelectorAll('.meaning-input');
  let allCorrect = true;
  let hasEmpty = false;
  
  inputs.forEach(inp => {
    const userVal = inp.value.trim().toLowerCase();
    const correctVal = inp.dataset.ans.toLowerCase();
    inp.classList.remove('wrong', 'correct');
    
    if (userVal === '') hasEmpty = true;
    
    if (userVal === correctVal) {
      inp.classList.add('correct');
      inp.disabled = true;
    } else if (userVal !== '') {
      inp.classList.add('wrong');
      allCorrect = false;
    } else {
      allCorrect = false;
    }
  });
  
  const feedEl = document.getElementById('test-feedback');
  
  if (hasEmpty && !allCorrect) {
    feedEl.textContent = "Please fill in all blanks.";
    feedEl.className = 'feedback error';
    AudioManager.play('error');
    return;
  }
  
  if (allCorrect) {
    feedEl.textContent = "Masterful interpretation!";
    feedEl.className = 'feedback success';
    AudioManager.play('success');
    
    round4Score += 30; // 30 points per perfectly restored definition
    updateScoreboard(30);
    
    document.getElementById('skip-btn').disabled = true;
    btn.textContent = "Next Definition";
  } else {
    feedEl.textContent = "There are errors in your transcription. Review and try again.";
    feedEl.className = 'feedback error';
    AudioManager.play('error');
  }
}

function skipWord() {
  // Show answers before skipping
  const inputs = document.querySelectorAll('.meaning-input');
  inputs.forEach(inp => {
    inp.value = inp.dataset.ans;
    inp.classList.add('wrong');
    inp.disabled = true;
  });
  
  document.getElementById('test-feedback').textContent = "Skipped. Revealing transcription.";
  document.getElementById('test-feedback').className = 'feedback error';
  AudioManager.play('error');
  
  document.getElementById('skip-btn').disabled = true;
  document.getElementById('submit-btn').textContent = "Next Definition";
}

function nextWord() {
  testIndex++;
  if (testIndex < testSequence.length) {
    renderTestCurrent();
  } else {
    finishGame();
  }
}

function updateScoreboard(amount) {
  state.score += amount;
  document.getElementById('current-score').textContent = state.score;
  
  const btn = document.getElementById('submit-btn');
  const rect = btn.getBoundingClientRect();
  const floater = document.createElement('div');
  floater.className = 'floating-point';
  floater.textContent = `+${amount}`;
  floater.style.left = `${rect.left + rect.width / 2}px`;
  floater.style.top = `${rect.top - 20}px`;
  document.body.appendChild(floater);
  setTimeout(() => floater.remove(), 1000);
}

function finishGame() {
  sharedState.save(state);
  AudioManager.play('success');
  window.location.href = 'round5.html';
}

// Bootstrap
bootstrapStage();
