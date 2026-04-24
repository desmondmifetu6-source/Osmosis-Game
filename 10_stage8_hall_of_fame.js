// =====================================================================
// FILE: 09_stage7_boss_intro.js (The Chamber Doors)
// =====================================================================
// Imagine walking down a long, scary hallway toward the final boss room.
// This short file just handles the dramatic animations of the text pages 
// fading in and out to set a spooky mood before you actually face the king!

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
