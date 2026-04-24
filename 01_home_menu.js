// =====================================================================
// FILE: 01_home_menu.js (The Crossroad)
// =====================================================================
// This is the Main Menu lobby. From here, you pick which hallway to walk down.

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize & Security Check
  if (typeof initModal === 'function') initModal();
  
  const gameData = sharedState.load();
  if (!gameData.username) {
    navigate('index.html');
    return;
  }

  // 2. Display Username
  const usernameEl = document.getElementById('home-username');
  if (usernameEl) usernameEl.textContent = gameData.username;

  // 3. Navigation Helper
  function navigate(url) {
    if (typeof window.navigateWithTransition === 'function') navigateWithTransition(url);
    else window.location.href = url;
  }

  // 4. Standard Navigation Buttons
  const routes = {
    'diagram-btn': 'module_diagram_hub.html',
    'profile-btn': 'module_profile.html',
    'library-btn': 'module_library.html',
    'about-btn': 'module_about.html'
  };

  for (const [id, url] of Object.entries(routes)) {
    const btn = document.getElementById(id);
    if (btn) btn.addEventListener('click', () => navigate(url));
  }

  // 5. Play Solo Logic
  const playSoloBtn = document.getElementById('play-solo-btn');
  if (playSoloBtn) {
    playSoloBtn.addEventListener('click', () => {
      // Wipe session data for a fresh run
      Object.assign(gameData, {
        score: 0, usedLetters: [], selectedWords: [], stageScores: {},
        meanings: {}, lastLength: null, totalTime: 0, sessionStartedAt: null
      });
      sharedState.save(gameData);

      // Navigate instantly without restrictive popups
      navigate('02_campaign_setup.html');
    });
  }

  // 6. Play Friends Logic
  const playFriendsBtn = document.getElementById('play-friends-btn');
  if (playFriendsBtn) {
    playFriendsBtn.addEventListener('click', () => {
      if (typeof showModal === 'function') {
        showModal('Tip', 'This mode can be played manually in groups by each player acquiring the dictionary. In this case the hard-copy is the tool for playing the game not the computer or phone.');
      }
    });
  }

  // 7. Purge Saved Data Logic
  const resetBtn = document.getElementById('reset-btn');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      if (confirm("Are you sure you want to purge all saved data? This will delete your profile and score forever.")) {
        localStorage.clear();
        sessionStorage.clear();
        navigate('index.html');
      }
    });
  }
});
