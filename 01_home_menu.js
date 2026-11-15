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
    
    // Close when clicking outside the popup
    soloOverlay.addEventListener('click', (e) => {
      if (e.target === soloOverlay) {
        soloOverlay.classList.remove('active');
      }
    });
  }

  if (soloContinueBtn) {
    soloContinueBtn.addEventListener('click', () => {
      // Wipe session data for a fresh run
      if (typeof sharedState.clearGameSession === 'function') {
        sharedState.clearGameSession(true);
      }
      navigate('02_campaign_setup.html');
    });
  }

  // 5b. Personal Study Logic — show popup first
  const personalStudyBtn = document.getElementById('personal-study-btn');
  const studyOverlay = document.getElementById('study-popup-overlay');
  const studyContinueBtn = document.getElementById('study-popup-continue');

  if (personalStudyBtn && studyOverlay) {
    personalStudyBtn.addEventListener('click', () => {
      studyOverlay.classList.add('active');
    });

    studyOverlay.addEventListener('click', (e) => {
      if (e.target === studyOverlay) {
        studyOverlay.classList.remove('active');
      }
    });
  }

  if (studyContinueBtn) {
    studyContinueBtn.addEventListener('click', () => {
      if (typeof sharedState.clearGameSession === 'function') {
        sharedState.clearGameSession(true);
      }
      navigate('02b_personal_study_setup.html');
    });
  }

  // 5c. STEM Hunt Logic — show popup first
  const wordhuntBtn = document.getElementById('wordhunt-btn');
  const huntOverlay = document.getElementById('hunt-popup-overlay');
  const huntContinueBtn = document.getElementById('hunt-popup-continue');

  if (wordhuntBtn && huntOverlay) {
    wordhuntBtn.addEventListener('click', () => {
      huntOverlay.classList.add('active');
    });

    huntOverlay.addEventListener('click', (e) => {
      if (e.target === huntOverlay) {
        huntOverlay.classList.remove('active');
      }
    });
  }

  if (huntContinueBtn) {
    huntContinueBtn.addEventListener('click', () => {
      navigate('module_word_hunt.html?v=2.0');
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
    
    // Close when clicking outside the popup
    friendsOverlay.addEventListener('click', (e) => {
      if (e.target === friendsOverlay) {
        friendsOverlay.classList.remove('active');
      }
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

  // 8. Check for Latest Update Button
  const checkUpdateBtn = document.getElementById('check-update-btn');
  if (checkUpdateBtn) {
    checkUpdateBtn.addEventListener('click', async () => {
      const origHtml = checkUpdateBtn.innerHTML;
      checkUpdateBtn.innerHTML = '<span>⏳ Checking for updates...</span>';
      checkUpdateBtn.style.pointerEvents = 'none';

      if (typeof window.OsmosisUpdater !== 'undefined' && typeof window.OsmosisUpdater.checkUpdateManual === 'function') {
        await window.OsmosisUpdater.checkUpdateManual(checkUpdateBtn, origHtml);
      } else {
        setTimeout(() => {
          checkUpdateBtn.innerHTML = '<span>✅ Osmosis is Up to Date!</span>';
          setTimeout(() => {
            checkUpdateBtn.innerHTML = origHtml;
            checkUpdateBtn.style.pointerEvents = 'auto';
          }, 2000);
        }, 800);
      }
    });
  }
});
