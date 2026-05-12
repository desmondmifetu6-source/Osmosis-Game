initModal();
const state = sharedState.load();
if (!state.username) window.location.href = 'index.html';

function goToStudy(id) {
  if (typeof AudioManager !== 'undefined') AudioManager.play('success');
  const target = `module_diagram_study.html?id=${id}`;
  if (typeof navigateWithTransition === 'function') navigateWithTransition(target);
  else window.location.href = target;
}

document.getElementById('go-home-btn').addEventListener('click', () => {
  if (typeof navigateWithTransition === 'function') navigateWithTransition('01_home_menu.html');
  else window.location.href = '01_home_menu.html';
});
