initModal();
const state = sharedState.load();
if (!state.selectedWords || state.selectedWords.length === 0) window.location.href = 'index.html';

const introContainer = document.getElementById('intro-container');
const quizContainer = document.getElementById('quiz-container');
const optionsContainer = document.getElementById('options-container');
const nextBtn = document.getElementById('next-btn');
const feedbackEl = document.getElementById('r5-feedback');

let testSequence = [];
let testIndex = 0;
let hasAnsweredRow = false;

function bootstrapStage() {
  testSequence = [...state.selectedWords].sort(() => 0.5 - Math.random());
  
  document.getElementById('start-btn').addEventListener('click', () => {
    introContainer.style.display = 'none';
    quizContainer.style.display = 'block';
    
    document.getElementById('scoreboard').style.display = 'block';
    document.getElementById('current-score').textContent = state.score || 0;
    
    renderQuizCurrent();
  });
}

function renderQuizCurrent() {
  hasAnsweredRow = false;
  nextBtn.style.display = 'none';
  feedbackEl.textContent = '';
  optionsContainer.innerHTML = '';
  
  const correctWord = testSequence[testIndex];
  document.getElementById('r5-meaning').textContent = state.meanings[correctWord];
  document.getElementById('quiz-progress').textContent = `${testIndex + 1} / ${testSequence.length}`;
  
  // Pick 3 distractors
  let allPossible = [];
  if (state.wordsPool && state.wordsPool.length > 4) {
    allPossible = [...state.wordsPool];
  } else {
    allPossible = Object.keys(DictionaryLogic.fallback);
  }
  
  // Filter out correct word
  allPossible = allPossible.filter(w => w.toLowerCase() !== correctWord.toLowerCase());
  
  // Randomize and take 3
  allPossible = allPossible.sort(() => 0.5 - Math.random());
  let distractors = allPossible.slice(0, 3);
  
  let options = [...distractors, correctWord].sort(() => 0.5 - Math.random());
  
  options.forEach(opt => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.textContent = opt;
    btn.dataset.word = opt.toLowerCase();
    
    btn.addEventListener('click', () => handleOptionClick(btn, opt, correctWord));
    
    optionsContainer.appendChild(btn);
  });
}

function handleOptionClick(clickedBtn, selectedWord, correctWord) {
  if (hasAnsweredRow) return;
  hasAnsweredRow = true;
  
  const allBtns = document.querySelectorAll('.option-btn');
  allBtns.forEach(btn => btn.disabled = true);
  
  if (selectedWord.toLowerCase() === correctWord.toLowerCase()) {
    // Correct logic
    clickedBtn.classList.add('correct');
    feedbackEl.textContent = "👍 Correct!";
    feedbackEl.className = 'feedback success';
    AudioManager.play('success');
    
    updateScoreboard(20, clickedBtn);
  } else {
    // Wrong logic
    clickedBtn.classList.add('wrong');
    feedbackEl.textContent = "Incorrect.";
    feedbackEl.className = 'feedback error';
    AudioManager.play('error');
    
    // Highlight correct response
    allBtns.forEach(btn => {
      if (btn.dataset.word === correctWord.toLowerCase()) {
        btn.classList.add('correct');
      }
    });
  }
  
  nextBtn.style.display = 'inline-block';
}

nextBtn.addEventListener('click', () => {
  testIndex++;
  if (testIndex < testSequence.length) {
    renderQuizCurrent();
  } else {
    finishGame();
  }
});

function updateScoreboard(amount, refElement) {
  state.score += amount;
  document.getElementById('current-score').textContent = state.score;
  
  const rect = refElement.getBoundingClientRect();
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
  window.location.href = 'round4.html';
}

// Bootstrap
bootstrapStage();

// Developer Cheat
document.addEventListener('keydown', (e) => {
  if (e.key.toLowerCase() === 'p' && e.altKey) {
    e.preventDefault();
    if (introContainer.style.display !== 'none') {
      document.getElementById('start-btn').click();
    } else if (quizContainer.style.display !== 'none') {
      const correct = testSequence[testIndex].toLowerCase();
      const btns = document.querySelectorAll('.option-btn');
      btns.forEach(b => { 
        if (b.dataset.word === correct && !b.disabled) b.click(); 
      });
      if (nextBtn.style.display !== 'none') nextBtn.click();
    }
  }
});
