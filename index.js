// =====================================================================
// FILE: index.js (The Bouncer)
// =====================================================================
// Imagine this file as a friendly bouncer at the front door of a club.
// It checks if you've been here before. If you have, it warmly welcomes you back.
// If you are new, it gives you a nametag and lets you inside!

const LoginController = {
  // Encapsulated state to prevent bleeding variables
  state: {
    gameData: null,
    savedUser: null,
    selectedAvatar: "🤓",
    domCache: {}
  },

  init() {
    const splash = document.getElementById('intro-splash');
    if (splash) {
      if (!sessionStorage.getItem('osmosis_splash_seen')) {
        sessionStorage.setItem('osmosis_splash_seen', 'true');
        setTimeout(() => {
          splash.classList.add('hidden');
        }, 2000);
      } else {
        splash.style.transition = 'none';
        splash.classList.add('hidden');
      }
    }

    if (typeof initModal === 'function') initModal();
    this.state.gameData = sharedState.load();
    this.state.savedUser = localStorage.getItem('osmosis_user');

    this.cacheDOM();
    this.render();
    this.attachListeners();
  },

  cacheDOM() {
    this.state.domCache = {
      loginContent: document.getElementById('login-content'),
      welcomeBackContent: document.getElementById('welcome-back-content'),
      welcomeBackTitle: document.getElementById('welcome-back-title'),
      continueSavedBtn: document.getElementById('continue-saved-btn'),
      continueGuestBtn: document.getElementById('continue-guest-btn'),
      switchUserLink: document.getElementById('switch-user-link'),
      loginBtn: document.getElementById('login-btn'),
      usernameInput: document.getElementById('username-input'),
      avatarOptions: document.querySelectorAll('.avatar-option'),
      akwaabaScreen: document.getElementById('akwaaba-screen')
    };
  },

  render() {
    const { domCache, savedUser } = this.state;

    if (savedUser) {
      if (domCache.loginContent) domCache.loginContent.style.display = 'none';
      if (domCache.welcomeBackContent) domCache.welcomeBackContent.style.display = 'block';
      
      if (domCache.welcomeBackTitle) domCache.welcomeBackTitle.textContent = `Welcome back, ${savedUser}`;
      if (domCache.continueSavedBtn) domCache.continueSavedBtn.textContent = `Continue as ${savedUser}`;
    } else {
      if (domCache.loginContent) domCache.loginContent.style.display = 'block';
      if (domCache.welcomeBackContent) domCache.welcomeBackContent.style.display = 'none';
    }
  },

  attachListeners() {
    const { domCache, savedUser } = this.state;

    if (domCache.continueSavedBtn) {
      domCache.continueSavedBtn.addEventListener('click', () => this.continueAs(savedUser));
    }

    if (domCache.continueGuestBtn) {
      domCache.continueGuestBtn.addEventListener('click', () => this.continueAs('Guest', 0));
    }

    if (domCache.switchUserLink) {
      domCache.switchUserLink.addEventListener('click', (e) => {
        e.preventDefault();
        if (domCache.welcomeBackContent) domCache.welcomeBackContent.style.display = 'none';
        if (domCache.loginContent) domCache.loginContent.style.display = 'block';
      });
    }

    if (domCache.loginBtn) {
      domCache.loginBtn.addEventListener('click', () => this.handleLogin());
    }

    if (domCache.avatarOptions) {
      domCache.avatarOptions.forEach(opt => {
        opt.addEventListener('click', () => {
          domCache.avatarOptions.forEach(o => o.classList.remove('selected'));
          opt.classList.add('selected');
          this.state.selectedAvatar = opt.getAttribute('data-avatar');
          if (typeof AudioManager !== 'undefined') AudioManager.play('chip');
        });
      });
    }

    if (domCache.usernameInput) {
      domCache.usernameInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') this.handleLogin();
      });
    }
  },

  handleLogin() {
    const { domCache } = this.state;
    const user = domCache.usernameInput ? domCache.usernameInput.value.trim() : '';

    if (user) {
      this.continueAs(user, 0);
    } else {
      if (typeof showModal === 'function') showModal('Notice', 'Please type your name first.');
    }
  },

  continueAs(user, startingScore = null) {
    const { domCache, gameData } = this.state;

    if (startingScore !== null) {
      localStorage.setItem('osmosis_total_score', startingScore);
    }
    localStorage.setItem('osmosis_user', user);

    gameData.username = user;
    gameData.avatar = this.state.selectedAvatar;
    gameData.totalTime = 0;
    gameData.startTime = null;
    sharedState.save(gameData);

    if (domCache.loginContent) domCache.loginContent.style.display = 'none';
    if (domCache.welcomeBackContent) domCache.welcomeBackContent.style.display = 'none';

    if (domCache.akwaabaScreen) {
      domCache.akwaabaScreen.textContent = `Welcome, ${user}`;
      domCache.akwaabaScreen.classList.add('visible');
    }

    setTimeout(() => {
      window.location.href = '01_home_menu.html';
    }, 2000);
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => LoginController.init());
} else {
  LoginController.init();
}
