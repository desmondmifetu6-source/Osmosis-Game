initModal();
const state = sharedState.load();
const savedUser = localStorage.getItem('osmosis_user');

if (savedUser && !state.username) {
  state.username = savedUser;
  sharedState.save(state);
  window.location.href = 'home.html';
}

function handleLogin() {
  const user = document.getElementById('username-input').value.trim();
  if (user) {
    localStorage.setItem('osmosis_user', user);
    state.username = user;
    sharedState.save(state);
    
    // Show Akwaaba transition screen
    document.getElementById('login-content').classList.add('hidden');
    const akwaabaScreen = document.getElementById('akwaaba-screen');
    akwaabaScreen.textContent = `Akwaaba, ${user}`;
    akwaabaScreen.classList.add('visible');
    
    setTimeout(() => {
      window.location.href = 'home.html';
    }, 2000);
  } else {
    showModal('Notice', 'Please enter your scholarly name to proceed.');
  }
}

document.getElementById('login-btn').addEventListener('click', handleLogin);
document.getElementById('username-input').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') handleLogin();
});
