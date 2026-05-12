// =====================================================================
// FILE: module_diagram_study.js (The Scalable Diagram Engine)
// =====================================================================
// Refactored by Uncle Chen: Using a centralized library. 
// No more hard-coding. No more junior logic. Just pure, scalable architecture.

initModal();
const state = sharedState.load();
if (!state.username) window.location.href = 'index.html';

sharedState.startTimer();
sharedState.updateTimerUI();

const urlParams = new URLSearchParams(window.location.search);
const diagramId = urlParams.get('id');

// Load Data from the Library
const diagramData = (typeof DiagramLibrary !== 'undefined') ? DiagramLibrary[diagramId] : null;

if (!diagramData) {
  window.location.href = 'module_diagram_hub.html';
}

document.getElementById('current-score').textContent = state.score || 0;

const imgObj = document.getElementById('diagram-img');
const titleObj = document.getElementById('d-title');

// Set up Diagram Specifics
const stageStartScore = state.score || 0;
const validLabels = diagramData.labels || [];
const labelAliases = diagramData.aliases || {};
imgObj.src = diagramData.image;
titleObj.textContent = diagramData.title;

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[array[j] ? j : i]] = [array[j], array[i]];
  }
  return array;
}

function normalizeLabel(input) {
  const cleaned = String(input || '').trim().toLowerCase();
  if (!cleaned) return '';
  return labelAliases[cleaned] || cleaned;
}

// Game State
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

// ── Score Logic ──────────────────────────────────────────────────────
function updateScore(pts) {
  state.score = (state.score || 0) + pts;
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

// ── Intro Phase ──────────────────────────────────────────────────────
document.getElementById('begin-btn').addEventListener('click', startMemorizePhase);

function startMemorizePhase() {
  introView.style.display = 'none';
  imgView.style.display = 'block';
  timerEl.style.display = 'block';
  instrText.textContent = "Memorize the diagram! You have 10 seconds.";
  
  let timeLeft = 10;
  timerEl.textContent = timeLeft;
  
  if (timerInterval) clearInterval(timerInterval);
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

// ── ROUND 1: Identification Familiarity ──────────────────────────────
function startRound1() {
  imgView.style.display = 'block'; 
  imgView.style.maxHeight = '300px'; 
  imgView.style.opacity = '0.7';

  instrText.textContent = "Round 1: Locate and type the parts shown in the diagram.";
  round1View.style.display = 'block';
  
  const bank = document.getElementById('r1-word-bank');
  bank.innerHTML = '';
  
  let scrambled = shuffleArray([...validLabels]);
  scrambled.forEach((word) => {
    let div = document.createElement('div');
    div.className = 'word-bank-item';
    div.id = 'wb-' + word.replace(/\s+/g, '-');
    div.textContent = word;
    bank.appendChild(div);
  });
  
  const input = document.getElementById('r1-input');
  input.value = '';
  input.focus();
}

document.getElementById('r1-input').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
     const val = normalizeLabel(e.target.value);
     if (!val) return;
     
     if (validLabels.includes(val) && !r1Found.includes(val)) {
        r1Found.push(val);
        const div = document.getElementById('wb-' + val.replace(/\s+/g, '-'));
        if (div) div.classList.add('found');
        e.target.value = '';
        if (typeof AudioManager !== 'undefined') AudioManager.play('success');
        updateScore(5);
        spawnPoints(e.target, "+5");
        
        if (r1Found.length === validLabels.length) {
           setTimeout(startRound2, 800);
        }
     } else {
        if (typeof AudioManager !== 'undefined') AudioManager.play('error');
        e.target.style.animation = 'shake 0.4s ease';
        setTimeout(() => e.target.style.animation='', 400);
     }
  }
});

document.getElementById('r1-skip-btn').addEventListener('click', () => startRound2());

// ── ROUND 2: Flash Reflex ────────────────────────────────────────────
function startRound2() {
  imgView.style.display = 'none';
  round1View.style.display = 'none';
  instrText.textContent = "Round 2: A labeled part will flash. Type it quickly from memory.";
  round2View.style.display = 'block';
  
  let scrambled = shuffleArray([...validLabels]);
  r2Parts = scrambled.slice(0, Math.min(8, validLabels.length));
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
     setTimeout(startRound3, 800);
     return;
  }
  r2Prog.textContent = `${r2CurrentIdx + 1} / ${r2Parts.length}`;
  const currentWord = r2Parts[r2CurrentIdx];
  r2Word.textContent = currentWord;

  if (currentWord.length > 20) r2Word.style.fontSize = '1.8rem';
  else if (currentWord.length > 12) r2Word.style.fontSize = '2.5rem';
  else r2Word.style.fontSize = ''; 
  
  r2Word.style.opacity = '0';
  r2Word.classList.remove('blink-twice');
  void r2Word.offsetWidth;
  r2Word.classList.add('blink-twice');
  
  if (typeof AudioManager !== 'undefined') AudioManager.play('chip');
  
  setTimeout(() => {
    r2InputArea.style.display = 'block';
    r2Input.focus();
  }, 650);
}

r2Input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
     const val = normalizeLabel(e.target.value);
     if (!val) return;
     if (val === r2Parts[r2CurrentIdx].toLowerCase()) {
        if (typeof AudioManager !== 'undefined') AudioManager.play('success');
        updateScore(10);
        spawnPoints(e.target, "+10");
        r2CurrentIdx++;
        flashNextR2();
     } else {
        if (typeof AudioManager !== 'undefined') AudioManager.play('error');
        e.target.style.animation = 'shake 0.4s ease';
        setTimeout(() => e.target.style.animation='', 400);
     }
  }
});

document.getElementById('r2-skip-btn').addEventListener('click', () => {
  r2CurrentIdx++;
  flashNextR2();
});

// ── ROUND 3: Pure Recall ─────────────────────────────────────────────
function startRound3() {
  round2View.style.display = 'none';
  instrText.textContent = "Round 3: Final test. Recall as many parts as possible from pure memory.";
  recallView.style.display = 'block';
  r3Input.value = '';
  r3Input.focus();
}

const r3Input = document.getElementById('recall-input');
r3Input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    const val = normalizeLabel(e.target.value);
    e.target.value = '';

    if (val && validLabels.includes(val)) {
      if (!r3Recalled.includes(val)) {
        r3Recalled.push(val);
        if (typeof AudioManager !== 'undefined') AudioManager.play('success');
        updateScore(20);
        spawnPoints(e.target, "+20");
        
        const pill = document.createElement('div');
        pill.className = 'recalled-pill';
        pill.textContent = val;
        document.getElementById('recalled-list').appendChild(pill);
      } else {
        if (typeof AudioManager !== 'undefined') AudioManager.play('error');
        e.target.style.animation = 'shake 0.4s ease';
        setTimeout(() => { e.target.style.animation = ''; }, 400);
      }
    } else if (val) {
      if (typeof AudioManager !== 'undefined') AudioManager.play('error');
      e.target.style.animation = 'shake 0.4s ease';
      setTimeout(() => e.target.style.animation='', 400);
    }
  }
});

// ── FINAL ASSIMILATION: Review Meanings ──────────────────────────────
document.getElementById('finish-btn').addEventListener('click', showAssimilation);

function showAssimilation() {
  recallView.style.display = 'none';
  instrText.textContent = "Assimilation: Review the scientific definitions of the schema.";
  
  const assimilationView = document.createElement('div');
  assimilationView.id = 'assimilation-view';
  assimilationView.style.cssText = "padding: 2rem; background: #fff; border-radius: 12px; border: 2px solid var(--accent-primary); max-height: 60vh; overflow-y: auto; text-align: left;";
  
  validLabels.forEach(word => {
    const item = document.createElement('div');
    item.style.marginBottom = '1.5rem';
    item.style.borderBottom = '1px solid #eee';
    item.style.paddingBottom = '1rem';
    
    const wasFound = r1Found.includes(word) || r2Parts.includes(word) || r3Recalled.includes(word);
    
    const meaning = (typeof DictionaryLogic !== 'undefined') ? DictionaryLogic.fetchMeaning(word) : "Definition stored in memory.";
    
    item.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
        <strong style="text-transform:uppercase; font-size:1.2rem; color:var(--text-main);">${word}</strong>
        ${wasFound ? '<span style="color:#4caf50; font-weight:bold;">[IDENTIFIED]</span>' : '<span style="color:#aaa;">[MISSED]</span>'}
      </div>
      <p style="font-style:italic; color:#555; line-height:1.4;">${meaning}</p>
    `;
    assimilationView.appendChild(item);
  });
  
  const concludeBtn = document.createElement('button');
  concludeBtn.className = "classic-btn primary";
  concludeBtn.style.marginTop = "2rem";
  concludeBtn.textContent = "Conclude Trial";
  concludeBtn.onclick = concludeTrial;
  
  const container = document.querySelector('.diagram-engine');
  container.appendChild(assimilationView);
  container.appendChild(concludeBtn);
  
  const oldBtnWrap = document.querySelector('#recall-view div[style*="margin-top: 3rem"]');
  if (oldBtnWrap) oldBtnWrap.style.display = 'none';
}

function concludeTrial() {
  sharedState.save(state);
  const stageScore = Math.max(0, (state.score || 0) - stageStartScore);
  const stageKey = diagramId === 'animal' ? 'diagram_animal' : 'diagram_plant';
  const stageLabel = diagramId === 'animal' ? 'Diagram Animal Cell' : 'Diagram Plant Cell';
  
  sharedState.showStageScoreThen(stageKey, stageLabel, stageScore, () => {
    navigateWithTransition('module_diagram_hub.html');
  });
}
