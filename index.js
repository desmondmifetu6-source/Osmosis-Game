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

function continueAs(user) {
  localStorage.setItem('osmosis_user', user);
  state.username = user;
  sharedState.save(state);
  
  // Show Akwaaba transition screen
  loginContent.style.display = 'none';
  welcomeBackContent.style.display = 'none';
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
  continueAs('Guest');
});

document.getElementById('switch-user-link')?.addEventListener('click', (e) => {
  e.preventDefault();
  welcomeBackContent.style.display = 'none';
  loginContent.style.display = 'block';
});

function handleLogin() {
  const user = document.getElementById('username-input').value.trim();
  if (user) {
    continueAs(user);
  } else {
    showModal('Notice', 'Please enter your scholarly name to proceed.');
  }
}

document.getElementById('login-btn').addEventListener('click', handleLogin);
document.getElementById('username-input').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') handleLogin();
});
