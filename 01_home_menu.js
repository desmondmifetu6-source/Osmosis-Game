// =====================================================================
// FILE: 01_home_menu.js (The Crossroad)
// =====================================================================
// This is the Main Menu lobby. From here, you pick which hallway to walk down.
// We use the "HomeMenuController" to keep all the buttons and logic neatly packaged.

const HomeMenuController = {
  // Encapsulated state mapping
  state: {
    gameData: null,
    domCache: {}
  },

  init() {
    if (typeof initModal === 'function') initModal();
    this.state.gameData = sharedState.load();

    // Security Check: If they snuck in here without logging in, kick them back to the login screen!
    if (!this.state.gameData.username) {
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('00_login.html');
      else window.location.href = '00_login.html';
      return;
    }

    this.cacheDOM(); // Gather all our buttons
    this.render(); // Put their name on screen
    this.attachListeners(); // Make the buttons listen for clicks

  },

  cacheDOM() {
    this.state.domCache = {
      homeUsername: document.getElementById('home-username'),
      playSoloBtn: document.getElementById('play-solo-btn'),
      playFriendsBtn: document.getElementById('play-friends-btn'),
      diagramBtn: document.getElementById('diagram-btn'),
      profileBtn: document.getElementById('profile-btn'),
      libraryBtn: document.getElementById('library-btn'),
      aboutBtn: document.getElementById('about-btn'),
      modalCloseBtn: document.getElementById('modal-close-btn')
    };
  },

  render() {
    if (this.state.domCache.homeUsername) {
      this.state.domCache.homeUsername.textContent = this.state.gameData.username;
    }
  },

  attachListeners() {
    const { domCache } = this.state;

    if (domCache.playSoloBtn) {
      domCache.playSoloBtn.addEventListener('click', () => this.handlePlaySolo());
    }
    if (domCache.playFriendsBtn) {
      domCache.playFriendsBtn.addEventListener('click', () => this.handlePlayFriends());
    }

    // Abstract basic navigation
    const navMap = {
      'diagramBtn': 'module_diagram_hub.html',
      'profileBtn': 'module_profile.html',
      'libraryBtn': 'module_library.html',
      'aboutBtn': 'module_about.html'
    };

    // We loop through the map above and make sure each button sends you to the right place smoothly.
    for (const [btnKey, destUrl] of Object.entries(navMap)) {
      if (domCache[btnKey]) {
        domCache[btnKey].addEventListener('click', () => { 
          if (typeof window.navigateWithTransition === 'function') navigateWithTransition(destUrl);
          else window.location.href = destUrl; 
        });
      }
    }
  },

  // Function: handlePlaySolo
  // What happens when you hit the big "Play Solo" button? We wipe out any old game data
  // so you start with a totally fresh slate, perfectly ready to hunt!
  handlePlaySolo() {
    const { gameData } = this.state;

    // Wipe slate clean conceptually
    gameData.score = 0;
    gameData.usedLetters = [];
    gameData.selectedWords = [];
    gameData.stageScores = {};
    gameData.meanings = {};
    gameData.lastLength = null;
    gameData.totalTime = 0;
    gameData.sessionStartedAt = null;

    sharedState.save(gameData);

    // Give them a quick reminder on how the game works
    if (typeof showModal === 'function') {
      showModal('Instructions', 'Play Solo means play alone or with one or two people supporting you. Begin Now by selecting your words.');
    }

    // Wait for them to click 'Close' on the instruction pop-up, then zoom them off to Campaign Setup!
    const closeBtn = document.getElementById('modal-close-btn');
    if (closeBtn) {
      const navigate = () => {
        if (typeof window.navigateWithTransition === 'function') navigateWithTransition('02_campaign_setup.html');
        else window.location.href = '02_campaign_setup.html';
        closeBtn.removeEventListener('click', navigate);
      };
      closeBtn.addEventListener('click', navigate);
    } else {
      if (typeof window.navigateWithTransition === 'function') navigateWithTransition('02_campaign_setup.html');
      else window.location.href = '02_campaign_setup.html';
    }
  },

  // Function: handlePlayFriends
  // Eventually this will be multiplayer, but for now we give a tip!
  handlePlayFriends() {
    if (typeof showModal === 'function') {
      showModal('Tip', 'This mode can be played manually in groups by each player acquiring the dictionary. In this case the hard-copy  is the tool for playing the game not the compuer or phone ');
    }
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => HomeMenuController.init());
} else {
  HomeMenuController.init();
}
