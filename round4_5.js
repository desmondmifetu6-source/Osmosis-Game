/**
 * ROUND 4.5: Absolute Recall
 * The user is shown the full definition and must type out the exact word without choices.
 */
initModal();
const state = sharedState.load();
if (!state.selectedWords || state.selectedWords.length === 0) window.location.href = 'index.html';

const introContainer = document.getElementById('intro-container');
const quizContainer = document.getElementById('quiz-container');
const submitBtn = document.getElementById('submit-btn');
const nextBtn = document.getElementById('next-btn');
const feedbackEl = document.getElementById('r45-feedback');
const wordInput = document.getElementById('target-word-input');

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
  submitBtn.style.display = 'inline-block';
  nextBtn.style.display = 'none';
  feedbackEl.textContent = '';
  wordInput.value = '';
  wordInput.disabled = false;
  wordInput.classList.remove('correct', 'wrong');
  wordInput.focus();
  
  const correctWord = testSequence[testIndex];
  document.getElementById('r45-meaning').textContent = state.meanings[correctWord];
  document.getElementById('quiz-progress').textContent = `${testIndex + 1} / ${testSequence.length}`;
}

submitBtn.addEventListener('click', () => {
  if (hasAnsweredRow) return;
  const userText = wordInput.value.trim().toLowerCase();
  if (!userText) return;

  hasAnsweredRow = true;
  wordInput.disabled = true;
  submitBtn.style.display = 'none';
  
  const correctWord = testSequence[testIndex].toLowerCase();
  
  if (userText === correctWord) {
    wordInput.classList.add('correct');
    feedbackEl.textContent = "👍 Correct!";
    feedbackEl.className = 'feedback success';
    AudioManager.play('success');
    
    updateScoreboard(30, wordInput);
  } else {
    wordInput.classList.add('wrong');
    feedbackEl.textContent = `Incorrect. The word was "${correctWord.toUpperCase()}".`;
    feedbackEl.className = 'feedback error';
    AudioManager.play('error');
  }
  
  nextBtn.style.display = 'inline-block';
});

wordInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    if (!hasAnsweredRow) submitBtn.click();
    else nextBtn.click();
  }
});

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
  window.location.href = 'round4.html'; // Move to Stage 5
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
      if (nextBtn.style.display !== 'none') nextBtn.click();
      else {
        wordInput.value = testSequence[testIndex];
        submitBtn.click();
      }
    }
  }
});
