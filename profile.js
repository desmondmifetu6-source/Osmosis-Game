const state = sharedState.load();
if (!state.username) window.location.href = 'index.html';

const history = JSON.parse(localStorage.getItem('osmosis_history')) || [];
const list = document.getElementById('history-list');

if (history.length === 0) {
  list.innerHTML = "<p style='text-align:center;font-style:italic;color:var(--ink-light);'>No archival records found.</p>";
} else {
  // Show most recent first
  history.slice().reverse().forEach(record => {
    const item = document.createElement('div');
    item.className = 'history-item';
    item.innerHTML = `
      <div class="history-header">
        <span>${record.date}</span>
        <span class="history-stats">Score: ${record.score} | Acc: ${record.accuracy}%</span>
      </div>
      <div class="history-words">
        Studied: ${record.words.join(', ')}
      </div>
    `;
    list.appendChild(item);
  });
}

document.getElementById('go-home-btn').addEventListener('click', () => {
  window.location.href = 'home.html';
});
