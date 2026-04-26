// =====================================================================
// FILE: 10_stage8_hall_of_fame.js (Boss Stage Intro — The Chamber Doors)
// =====================================================================
// This file controls the dramatic two-page intro sequence that plays
// immediately before the final boss stage (Stage 8).
//
// Responsibilities:
//   1. Loads the player's current score from sharedState and displays it.
//   2. Manages a two-screen narrative transition:
//        - Page 1 fades out when the player clicks the first "Next" button.
//        - Page 2 fades in, building suspense before the hall of fame encounter.
//   3. On the second "Next" click, navigates the player to the boss phase
//      (10_stage8_boss_phase.html) using an animated page transition.

document.addEventListener('DOMContentLoaded', () => {
  const gameData = sharedState.load();
  const scoreEl = document.getElementById('current-score');
  if (scoreEl) scoreEl.textContent = gameData.score || 0;

  const page1 = document.getElementById('page-1');
  const page2 = document.getElementById('page-2');

  document.getElementById('nd-next-1')?.addEventListener('click', () => {
    if (page1 && page2) {
      page1.classList.add('fade-out');
      setTimeout(() => {
        page1.style.display = 'none';
        page2.style.display = 'block';
        page2.classList.add('fade-in');
      }, 400); // Wait for fade-out animation to finish
    }
  });

  document.getElementById('nd-next-2')?.addEventListener('click', () => {
    if (typeof window.navigateWithTransition === 'function') navigateWithTransition('10_stage8_boss_phase.html');
    else window.location.href = '10_stage8_boss_phase.html';
  });
});
