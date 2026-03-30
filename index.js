initModal();
const state = sharedState.load();
const savedUser = localStorage.getItem('osmosis_user');

const loginContent = document.getElementById('login-content');
const welcomeBackContent = document.getElementById('welcome-back-content');

if (savedUser) {
  loginContent.style.display = 'none';
  welcomeBackContent.style.display = 'block';
  document.getElementById('welcome-back-title').textContent = `Welcome back, ${savedUser}`;
  document.getElementById('continue-saved-btn').textContent = `Continue as ${savedUser}`;
} else {
  loginContent.style.display = 'block';
  welcomeBackContent.style.display = 'none';
}

let pendingUser = '';

function showLevelSelection(user) {
  pendingUser = user;
  loginContent.style.display = 'none';
  welcomeBackContent.style.display = 'none';
  document.getElementById('level-selection-content').style.display = 'block';
}

function continueAs(user, startingScore = null) {
  if (startingScore !== null) {
    localStorage.setItem('osmosis_total_score', startingScore);
  }
  localStorage.setItem('osmosis_user', user);
  state.username = user;
  sharedState.save(state);
  
  // Show Akwaaba transition screen
  loginContent.style.display = 'none';
  welcomeBackContent.style.display = 'none';
  document.getElementById('level-selection-content').style.display = 'none';
  const akwaabaScreen = document.getElementById('akwaaba-screen');
  akwaabaScreen.textContent = `Akwaaba, ${user}`;
  akwaabaScreen.classList.add('visible');
  
  setTimeout(() => {
    window.location.href = 'home.html';
  }, 2000);
}

document.getElementById('continue-saved-btn')?.addEventListener('click', () => {
  continueAs(savedUser);
});

document.getElementById('continue-guest-btn')?.addEventListener('click', () => {
  showLevelSelection('Guest');
});

document.getElementById('switch-user-link')?.addEventListener('click', (e) => {
  e.preventDefault();
  welcomeBackContent.style.display = 'none';
  loginContent.style.display = 'block';
  document.getElementById('level-selection-content').style.display = 'none';
});

function handleLogin() {
  const user = document.getElementById('username-input').value.trim();
  if (user) {
    showLevelSelection(user);
  } else {
    showModal('Notice', 'Please enter your scholarly name to proceed.');
  }
}

document.querySelectorAll('.level-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    const score = e.target.getAttribute('data-score');
    continueAs(pendingUser, score);
  });
});

document.getElementById('login-btn').addEventListener('click', handleLogin);
document.getElementById('username-input').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') handleLogin();
});
