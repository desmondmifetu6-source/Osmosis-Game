initModal();
const state = sharedState.load();
if (!state.username) window.location.href = 'index.html';

document.getElementById('home-username').textContent = state.username;

document.getElementById('play-solo-btn').addEventListener('click', () => {
  window.location.href = 'setup.html';
});

document.getElementById('profile-btn').addEventListener('click', () => {
  window.location.href = 'profile.html';
});

document.getElementById('library-btn').addEventListener('click', () => {
  window.location.href = 'library.html';
});

document.getElementById('about-btn').addEventListener('click', () => {
  window.location.href = 'about.html';
});
