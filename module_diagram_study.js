// =====================================================================
// FILE: module_diagram_study.js (The Diagram Memorizer)
// =====================================================================
// Welcome to the Biology class! Imagine looking at a complicated drawing 
// of a cell (like an animal or plant cell). This mini-game challenges you 
// to remember all the parts of the cell.
// First, you find the parts in a word bank. Then, parts flash on the screen 
// and you type what you saw. Finally, you have to list as many as you can from pure memory!

initModal();
const state = sharedState.load();
if (!state.username) window.location.href = 'index.html';
sharedState.startTimer();
sharedState.updateTimerUI();

const urlParams = new URLSearchParams(window.location.search);
const diagramId = urlParams.get('id');

if (!diagramId || (diagramId !== 'animal' && diagramId !== 'plant')) {
  window.location.href = 'module_diagram_hub.html';
}

document.getElementById('current-score').textContent = state.score || 0;

const imgObj = document.getElementById('diagram-img');
const titleObj = document.getElementById('d-title');

const stageStartScore = state.score || 0;
let validLabels = [];
let labelAliases = {};

if (diagramId === 'animal') {
  imgObj.src = 'diagrams/animal_cell.jpeg';
  titleObj.textContent = 'Zoological Schema (Animal Cell)';
  validLabels = [
    "microtubules", "nucleus", "vacuole", "cytoplasm", "golgi complex",
    "vesicles", "lysosome", "centrioles", "mitochondrion",
    "plasma membrane", "ribosomes", "endoplasmic reticulum"
  ];
  labelAliases = {
    "golgi": "golgi complex",
    "mitochondria": "mitochondrion",
    "membrane": "plasma membrane",
    "ribosome": "ribosomes",
    "er": "endoplasmic reticulum"
  };
} else {
  imgObj.src = 'diagrams/plant_cell.jpeg';
  titleObj.textContent = 'Botanical Schema (Plant Cell)';
  validLabels = [
    "cell wall", "cell membrane", "ribosomes", "golgi apparatus",
    "plastids", "peroxisomes", "amyloplasts", "nucleus",
    "chloroplasts", "rough endoplasmic reticulum",
    "smooth endoplasmic reticulum", "mitochondrion"
  ];
  labelAliases = {
    "golgi": "golgi apparatus",
    "ribosome": "ribosomes",
    "plastid": "plastids",
    "peroxisome": "peroxisomes",
    "amyloplast": "amyloplasts",
    "chloroplast": "chloroplasts",
    "rough er": "rough endoplasmic reticulum",
    "smooth er": "smooth endoplasmic reticulum",
    "mitochondria": "mitochondrion"
  };
}

function normalizeLabel(input) {
  const cleaned = String(input || '').trim().toLowerCase();
  if (!cleaned) return '';
  return labelAliases[cleaned] || cleaned;
}

let r1Found = [];
let r2Parts = [];
let r2CurrentIdx = 0;
let r3Recalled = [];
let timerInterval;

const timerEl = document.getElementById('timer');
const instrText = document.getElementById('instruction-text');
const introView = document.getElementById('intro-view');
const imgView = document.getElementById('image-view');
const round1View = document.getElementById('round1-view');
const round2View = document.getElementById('round2-view');
const recallView = document.getElementById('recall-view');

// Utilities
function updateScore(pts) {
  state.score = (state.score || 0) + pts;
  sharedState.save(state);
  document.getElementById('current-score').textContent = state.score;
}

function spawnPoints(el, text) {
  const pt = document.createElement('div');
  pt.className = 'point-gained';
  pt.textContent = text;
  const rect = el.getBoundingClientRect();
  pt.style.left = (rect.left + rect.width / 2) + 'px';
  pt.style.top = rect.top + 'px';
  document.body.appendChild(pt);
  setTimeout(() => pt.remove(), 1000);
}

// Intro Phase
document.getElementById('begin-btn').addEventListener('click', startMemorizePhase);

function startMemorizePhase() {
  introView.style.display = 'none';
  imgView.style.display = 'block';
  timerEl.style.display = 'block';
  instrText.textContent = "Memorize the diagram! You have 10 seconds.";
  
  let timeLeft = 10;
  timerEl.textContent = timeLeft;
  
  timerInterval = setInterval(() => {
    timeLeft--;
    timerEl.textContent = timeLeft;
    if (timeLeft <= 3) timerEl.style.color = 'red';
    else timerEl.style.color = '';
    
    if (timeLeft <= 0) {
      clearInterval(timerInterval);
      timerEl.style.display = 'none';
      startRound1();
    }
  }, 1000);
}

// ROUND 1
// In this round, we show you all the cell parts in a word bank!
// You just need to type them out exactly as they appear so your fingers 
// get used to spelling these weird biology words.
function startRound1() {
  imgView.style.display = 'none';
  instrText.textContent = "Round 1: Type all words from the word bank to continue.";
  round1View.style.display = 'block';
  
  const bank = document.getElementById('r1-word-bank');
  bank.innerHTML = '';
  
  let scrambled = [...validLabels].sort(() => Math.random() - 0.5);
  scrambled.forEach((word) => {
    let div = document.createElement('div');
    div.className = 'word-bank-item';
    div.id = 'wb-' + word.replace(/\s+/g, '-');
    div.textContent = word;
    bank.appendChild(div);
  });
  
  document.getElementById('r1-input').focus();
}

document.getElementById('r1-input').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
     const val = normalizeLabel(e.target.value);
     if (!val) return;
     if (validLabels.includes(val) && !r1Found.includes(val)) {
        r1Found.push(val);
        const div = document.getElementById('wb-' + val.replace(/\s+/g, '-'));
        if (div) div.classList.add('found');
        e.target.value = '';
        AudioManager.play('success');
        updateScore(5);
        spawnPoints(e.target, "+5");
        
        if (r1Found.length === validLabels.length) {
           setTimeout(startRound2, 1000);
        }
     } else {
        AudioManager.play('error');
        e.target.style.animation = 'shake 0.4s ease';
        setTimeout(() => e.target.style.animation='', 400);
     }
  }
});

document.getElementById('r1-skip-btn').addEventListener('click', () => {
  startRound2();
});

// ROUND 2
// Now things get tricky! A word will blink quickly on the screen,
// then vanish. You have to type exactly what you just saw like a reflex!
function startRound2() {
  round1View.style.display = 'none';
  instrText.textContent = "Round 2: A labeled part will flash. Type it exactly as shown.";
  round2View.style.display = 'block';
  
  // Pick 8 random parts
  let scrambled = [...validLabels].sort(() => Math.random() - 0.5);
  r2Parts = scrambled.slice(0, 8);
  r2CurrentIdx = 0;
  
  flashNextR2();
}

const r2Word = document.getElementById('r2-flash-word');
const r2InputArea = document.getElementById('r2-input-area');
const r2Input = document.getElementById('r2-input');
const r2Prog = document.getElementById('r2-progress');

function flashNextR2() {
  r2InputArea.style.display = 'none';
  r2Input.value = '';
  
  if (r2CurrentIdx >= r2Parts.length) {
     setTimeout(startRound3, 1000);
     return;
  }
  r2Prog.textContent = `${r2CurrentIdx + 1} / 8`;
  const currentWord = r2Parts[r2CurrentIdx];
  r2Word.textContent = currentWord;

  // Dynamic font size adjustment for very long biology terms (e.g. "rough endoplasmic reticulum")
  if (currentWord.length > 20) {
    r2Word.style.fontSize = '1.8rem';
    r2Word.style.letterSpacing = '1px';
  } else if (currentWord.length > 12) {
    r2Word.style.fontSize = '2.5rem';
    r2Word.style.letterSpacing = '2px';
  } else {
    r2Word.style.fontSize = ''; // Use the clamp() defined in style
    r2Word.style.letterSpacing = '';
  }
  r2Word.style.opacity = '0';
  
  // Trigger animation
  r2Word.classList.remove('blink-twice');
  void r2Word.offsetWidth;
  r2Word.classList.add('blink-twice');
  
  AudioManager.play('chip');
  
  setTimeout(() => {
    r2InputArea.style.display = 'block';
    r2Input.focus();
  }, 700); // After animation finishes
}

r2Input.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
     const val = normalizeLabel(e.target.value);
     if (!val) return;
     if (val === r2Parts[r2CurrentIdx].toLowerCase()) {
        AudioManager.play('success');
        updateScore(10);
        spawnPoints(e.target, "+10");
        r2CurrentIdx++;
        flashNextR2();
     } else {
        AudioManager.play('error');
        e.target.style.animation = 'shake 0.4s ease';
        setTimeout(() => e.target.style.animation='', 400);
     }
  }
});

document.getElementById('r2-skip-btn').addEventListener('click', () => {
  r2CurrentIdx++;
  flashNextR2();
});

// ROUND 3
// The final exam! No hints, no blinking words. The screen is clear. 
// Dig deep inside your brain and type out all the cell parts from pure memory!
function startRound3() {
  round2View.style.display = 'none';
  instrText.textContent = "Round 3: Final test. Recall as many parts as possible from pure memory.";
  recallView.style.display = 'block';
  document.getElementById('recall-input').focus();
}

const r3Input = document.getElementById('recall-input');
r3Input.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    const val = normalizeLabel(e.target.value);
    if (!val) return;
    
    if (validLabels.includes(val)) {
      if (!r3Recalled.includes(val)) {
        r3Recalled.push(val);
        e.target.value = '';
        AudioManager.play('success');
        updateScore(20);
        spawnPoints(e.target, "+20");
        
        const pill = document.createElement('div');
        pill.className = 'recalled-pill';
        pill.textContent = val;
        document.getElementById('recalled-list').appendChild(pill);
      } else {
        AudioManager.play('error');
        e.target.style.animation = 'shake 0.4s ease';
        setTimeout(() => { e.target.style.animation = ''; }, 400);
      }
    } else {
      AudioManager.play('error');
      e.target.style.animation = 'shake 0.4s ease';
      setTimeout(() => e.target.style.animation='', 400);
    }
  }
});

document.getElementById('finish-btn').addEventListener('click', () => {
  const stageScore = Math.max(0, (state.score || 0) - stageStartScore);
  const stageKey = diagramId === 'animal' ? 'diagram_animal' : 'diagram_plant';
  const stageLabel = diagramId === 'animal' ? 'Diagram Animal Cell' : 'Diagram Plant Cell';
  sharedState.showStageScoreThen(stageKey, stageLabel, stageScore, () => {
    navigateWithTransition('module_diagram_hub.html');
  });
});
