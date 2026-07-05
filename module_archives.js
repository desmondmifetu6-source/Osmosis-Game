initModal();
sharedState.stopTimer();

const state = sharedState.load();
const grid = document.getElementById('ma-word-grid');
const stats = document.getElementById('ma-stats');
const timeEl = document.getElementById('ma-time');
const finishBtn = document.getElementById('ma-finish-btn');

// Calculate accuracy and total
const maxPts = (state.selectedWords ? state.selectedWords.length : 26) * 80;
const score = state.score || 0;
const acc = maxPts > 0 ? Math.round((score / maxPts) * 100) : 0;

stats.innerHTML = `<strong>Accuracy:</strong> ${acc}% <span style="margin: 0 10px;">|</span> <strong>Total Score:</strong> ${score} points`;
if (timeEl) {
  const start = sharedState.formatDateTime(state.sessionStartedAt);
  const end = sharedState.formatDateTime(state.sessionEndedAt);
  const total = sharedState.getFormattedTime(state.totalTime || 0);
  timeEl.innerHTML = `<strong>Started:</strong> ${start} <span style="margin: 0 8px;">|</span> <strong>Ended:</strong> ${end} <span style="margin: 0 8px;">|</span> <strong>Total Time:</strong> ${total}`;
}

// Populate word grid
if (state.selectedWords && state.selectedWords.length > 0) {
  state.selectedWords.forEach((w, index) => {
    const el = document.createElement('div');
    el.className = 'word-tile';
    el.textContent = w;
    // Stagger animation
    el.style.opacity = 0;
    el.style.animation = `fade_in_up 0.5s ease forwards`;
    el.style.animationDelay = `${index * 0.05}s`;
    grid.appendChild(el);
  });
} else {
  grid.innerHTML = "<p style='grid-column: 1 / -1; text-align: center; color: var(--text-secondary);'>No words tracked for this session.</p>";
}

// Inject standard keyframe if not in core_styles.css
const styleSheet = document.createElement("style");
styleSheet.innerText = `
  @keyframes fade_in_up {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
  }
`;
document.head.appendChild(styleSheet);

finishBtn.addEventListener('click', () => {
  AudioManager.init();
  AudioManager.play('click');
  // Clear the active game state to reset the loop while keeping user info
  if (typeof sharedState.clearGameSession === 'function') {
    sharedState.clearGameSession(true);
  } else {
    sessionStorage.removeItem('gameState');
  }
  setTimeout(() => {
    window.location.href = 'module_library.html';
  }, 300);
});
