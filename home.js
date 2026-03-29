initModal();
const state = sharedState.load();
if (!state.username) window.location.href = 'index.html';

document.getElementById('home-username').textContent = state.username;

document.getElementById('play-friend-btn').addEventListener('click', () => {
  AudioManager.play('click');
  showModal('Under Construction', 'The Live Multiplayer servers are currently in development and will be deployed soon. Please hone your skills in Solo Play!');
});

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
