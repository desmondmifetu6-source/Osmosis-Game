// =====================================================================
// FILE: 06_stage4_meaning_exposure.js (The Library Reading Room)
// =====================================================================
// Stage 4 is simple: It's just a reading room. 
// We give the player 5 massive minutes to stare at a clean list of all 26 words 
// and their definitions, trying to memorize them before the hard tests begin.

initModal(); // Wake up the popup system
sharedState.startTimer();
const state = sharedState.load(); // Open the backpack
sharedState.updateTimerUI();

// Built-in Security: No backpack? Back to the lobby!
if (!state.selectedWords || state.selectedWords.length === 0) window.location.href = 'index.html';

const transitionContainer = document.getElementById('transition-container'); // The big red curtain
const revisionContainer = document.getElementById('revision-container'); // The study desk empty paper

let globalTimerInt = null; // A slot for our ticking study clock

// When they click 'Start' on the red curtain...
document.getElementById('start-btn').addEventListener('click', () => {
  transitionContainer.style.display = 'none'; // Rip away the curtain
  document.getElementById('current-score').textContent = state.score || 0; // Show their current score
  startRevisionPhase(); // Start studying!
});

// Function: startRevisionPhase
// Prints the definitions on the page and starts a 5-minute countdown clock.
function startRevisionPhase() {
  revisionContainer.style.display = 'block'; // Make the study desk visible
  
  const listEl = document.getElementById('rev-list'); // The blank piece of paper
  
  // For every single word the player collected...
  state.selectedWords.forEach(w => {
    const item = document.createElement('div'); // Make a nice box
    item.className = 'revision-item';
    // Write the bold Word and then its scientific meaning directly from the backpack
    item.innerHTML = `<strong>${w}</strong><p>${state.meanings[w]}</p>`;
    listEl.appendChild(item); // Tape the box to the piece of paper
  });
  
  // The clock! 300 seconds = exactly 5 minutes.
  let timeLeft = 300; 
  const timeEl = document.getElementById('rev-timer'); // The visual ticking clock on screen
  
  // The metronome tick function
  const tick = () => {
    const min = String(Math.floor(timeLeft / 60)).padStart(2, '0');
    const sec = String(timeLeft % 60).padStart(2, '0');
    timeEl.textContent = `${min}:${sec}`;
    
    // If 5 minutes pass and they are still staring at the screen...
    if (timeLeft <= 0) {
      clearInterval(globalTimerInt); // Smash the metronome
      endRevisionPhase(); // Rip the paper away!
    }
    timeLeft--; // Subtract 1 second
  };
  
  tick(); // Tick once manually
  globalTimerInt = setInterval(tick, 1000); // Tick automatically every 1 second
  
  // What if the player is super smart, finishes reading in 30 seconds, and clicks the button?
  document.getElementById('start-test-btn').addEventListener('click', () => {
    clearInterval(globalTimerInt); // Smash the clock early
    endRevisionPhase(); // Move on
  });
}

// Function: endRevisionPhase
// Throws the player out of the reading room and right into Stage 5!
function endRevisionPhase() {
  navigateWithTransition('08_stage6_definition_selection.html');
}

// Developer Cheat Code (Alt + P)
// If I'm building the game and don't want to wait 5 minutes to test the next page, I press Alt+P to skip it!
document.addEventListener('keydown', (e) => {
  if (e.key.toLowerCase() === 'p' && e.altKey) {
    e.preventDefault();
    if (transitionContainer.style.display !== 'none') {
      document.getElementById('start-btn').click(); // Auto-clicks start
    } else {
      document.getElementById('start-test-btn').click(); // Auto-clicks skip!
    }
  }
});
