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

  // 5. Play Solo Logic — show popup first
  const playSoloBtn = document.getElementById('play-solo-btn');
  const soloOverlay = document.getElementById('solo-popup-overlay');
  const soloContinueBtn = document.getElementById('solo-popup-continue');

  if (playSoloBtn && soloOverlay) {
    playSoloBtn.addEventListener('click', () => {
      soloOverlay.classList.add('active');
    });
  }

  if (soloContinueBtn) {
    soloContinueBtn.addEventListener('click', () => {
      // Wipe session data for a fresh run
      Object.assign(gameData, {
        score: 0, usedLetters: [], selectedWords: [], stageScores: {},
        meanings: {}, lastLength: null, totalTime: 0, sessionStartedAt: null
      });
      sharedState.save(gameData);
      navigate('02_campaign_setup.html');
    });
  }

  // 6. Play Friends Logic (Local or Online)
  const playFriendsBtn = document.getElementById('play-friends-btn');
  const multiplayerBtn = document.getElementById('multiplayer-btn');
  const friendsOverlay = document.getElementById('friends-popup-overlay');
  const friendsContinueBtn = document.getElementById('friends-popup-continue');
  
  if (playFriendsBtn && friendsOverlay) {
    playFriendsBtn.addEventListener('click', () => {
      friendsOverlay.classList.add('active');
    });
  }

  if (friendsContinueBtn) {
    friendsContinueBtn.addEventListener('click', () => {
      // Close the popup and remain on the home page
      friendsOverlay.classList.remove('active');
    });
  }

  if (multiplayerBtn) {
    multiplayerBtn.addEventListener('click', () => {
      navigate('multiplayer_lobby.html');
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
