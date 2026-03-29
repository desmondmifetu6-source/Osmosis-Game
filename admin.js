async function fetchScores() {
  try {
    const res = await fetch('http://localhost:3000/api/scores');
    const data = await res.json();
    
    document.getElementById('total-users').textContent = data.length;
    
    let highest = 0;
    const tbody = document.getElementById('leaderboard-body');
    tbody.innerHTML = '';
    
    if (data.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No records found in the database.</td></tr>';
      return;
    }
    
    // Sort by score descending
    data.sort((a, b) => b.score - a.score);
    
    data.forEach(entry => {
      if (entry.score > highest) highest = entry.score;
      
      let rankClass = 'rank-novice';
      if (entry.rank.includes('Omniscient')) rankClass = 'rank-omni';
      if (entry.rank.includes('Advanced')) rankClass = 'rank-adv';
      if (entry.rank.includes('Adept')) rankClass = 'rank-adept';
      
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${new Date(entry.timestamp).toLocaleString()}</td>
        <td style="font-weight:bold;">${entry.username}</td>
        <td style="font-family:monospace; font-weight:bold; font-size:1.5rem;">${entry.score}</td>
        <td>${entry.accuracy}%</td>
        <td class="rank-badge ${rankClass}">${entry.rank}</td>
      `;
      tbody.appendChild(tr);
    });
    
    document.getElementById('highest-score').textContent = highest;
    
  } catch (error) {
    document.getElementById('leaderboard-body').innerHTML = '<tr><td colspan="5" style="text-align:center; color:red;">Database offline. Ensure Node server is running on port 3000.</td></tr>';
  }
}

fetchScores();
// Refresh every 10 seconds
setInterval(fetchScores, 10000);
