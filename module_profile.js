const state = sharedState.load();
if (!state.username) window.location.href = 'index.html';

const statsEl = document.getElementById('profile-stats');
if (statsEl && typeof sharedState.getMasteryStats === 'function') {
  const m = sharedState.getMasteryStats();
  const totalXP = parseInt(localStorage.getItem('osmosis_total_score'), 10) || 0;
  statsEl.innerHTML = `
    <div class="profile-stat-box">
      <div class="profile-stat-val">${totalXP.toLocaleString()}</div>
      <div class="profile-stat-lbl">Total XP</div>
    </div>
    <div class="profile-stat-box">
      <div class="profile-stat-val">${m.masteredCount} / ${m.totalTerms}</div>
      <div class="profile-stat-lbl">Terms Mastered</div>
    </div>
    <div class="profile-stat-box">
      <div class="profile-stat-val">${m.accuracyPct}%</div>
      <div class="profile-stat-lbl">Recall Accuracy</div>
    </div>
    <div class="profile-stat-box">
      <div class="profile-stat-val">${m.dueCount}</div>
      <div class="profile-stat-lbl">Due for Review</div>
    </div>
  `;
}

const history = JSON.parse(localStorage.getItem('osmosis_history')) || [];
const list = document.getElementById('history-list');

if (history.length === 0) {
  list.innerHTML = "<p style='text-align:center;font-style:italic;color:var(--text-secondary);'>No archival records found.</p>";
} else {
  // Show most recent first
  history.slice().reverse().forEach(record => {
    const item = document.createElement('div');
    item.className = 'history-item';
    const safeDate = sharedState.escapeHTML(record.date || '');
    const safeWords = (record.words || []).map(w => sharedState.escapeHTML(w)).join(', ');
    item.innerHTML = `
      <div class="history-header">
        <span>${safeDate}</span>
        <span class="history-stats">Score: ${Number(record.score) || 0}</span>
      </div>
      <div class="history-words">
        Studied: ${safeWords}
      </div>
    `;
    list.appendChild(item);
  });
}

document.getElementById('go-home-btn').addEventListener('click', () => {
  window.location.href = '01_home_menu.html';
});
