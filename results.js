const state = sharedState.load();
if (!state.selectedWords || state.selectedWords.length === 0) window.location.href = 'index.html';

// Score Mechanics
const maxPossibleScore = state.selectedWords.length * 80; // (L1:10) + (L2:20) + (S4:30) + (S5:20)
const targetScore = state.score || 0;
let accuracy = 0;
if (maxPossibleScore > 0) accuracy = Math.round((targetScore / maxPossibleScore) * 100);

let intelligenceRank = "Novice Initiate";
if (accuracy >= 95) intelligenceRank = "Omniscient Polymath";
else if (accuracy >= 80) intelligenceRank = "Advanced Scholar";
else if (accuracy >= 60) intelligenceRank = "Adept Thinker";
else if (accuracy >= 40) intelligenceRank = "Apprentice";

// Score Animation
const scoreEl = document.getElementById('res-score');
let currentNumber = 0;
const duration = 2000;
const interval = 30;
const step = Math.max(1, Math.floor(targetScore / (duration / interval)));

const counterInt = setInterval(() => {
  currentNumber += step;
  if (currentNumber >= targetScore) {
    currentNumber = targetScore;
    clearInterval(counterInt);
    AudioManager.init();
    AudioManager.play('success'); // Chiming victory
    
    // Reveal Rank and Stats
    document.getElementById('res-rank').textContent = `Classification: ${intelligenceRank}`;
    document.getElementById('res-stats').textContent = `Accuracy: ${accuracy}%  (${targetScore} / ${maxPossibleScore} pts)`;
    document.getElementById('res-rank').style.opacity = 1;
    document.getElementById('res-stats').style.opacity = 1;
  }
  scoreEl.textContent = currentNumber;
}, interval);

const list = document.getElementById('res-words-list');
list.innerHTML = '';

state.selectedWords.forEach(word => {
  const item = document.createElement('div');
  item.className = 'word-item';
  const meaning = state.meanings && state.meanings[word] ? state.meanings[word] : "Definition captured strictly in memory.";
  
  item.innerHTML = `<strong>${word}</strong><p>${meaning}</p>`;
  list.appendChild(item);
});

// Update History locally
if (!sessionStorage.getItem('osmosis_saved_result')) {
  const history = JSON.parse(localStorage.getItem('osmosis_history')) || [];
  history.push({
    date: new Date().toLocaleDateString(),
    score: state.score,
    words: state.selectedWords
  });
  localStorage.setItem('osmosis_history', JSON.stringify(history));
  sessionStorage.setItem('osmosis_saved_result', 'true');
  
  // SEND TO GLOBAL DEVELOPER DATABASE!
  fetch('http://localhost:3000/api/score', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: state.username,
      score: targetScore,
      maxScore: maxPossibleScore,
      accuracy: accuracy,
      rank: intelligenceRank
    })
  }).catch(err => console.log('DB Offline'));
}

// Reset loop hooks
document.getElementById('play-again-btn').addEventListener('click', () => {
  sessionStorage.removeItem('osmosis_saved_result');
  // Retain just username, flush score and loop data
  sharedState.save({ username: state.username }); 
  AudioManager.play('click');
  setTimeout(() => window.location.href = 'setup.html', 200);
});

document.getElementById('go-home-btn').addEventListener('click', () => {
  sessionStorage.removeItem('osmosis_saved_result');
  AudioManager.play('click');
  setTimeout(() => window.location.href = 'library.html', 200);
});
