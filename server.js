const express = require('express');
const cors = require('cors');
const fs = require('fs');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// --- DATABASE LOGIC ---
// This acts as a lightweight persistent layer for keeping score records
// saving the data to local 'database.json', intended for future leaderboard expansions.
const DB_FILE = 'database.json';
if (!fs.existsSync(DB_FILE)) {
  fs.writeFileSync(DB_FILE, JSON.stringify([]));
}

app.post('/api/score', (req, res) => {
  try {
    const newEntry = req.body;
    newEntry.timestamp = new Date().toISOString();
    
    const data = JSON.parse(fs.readFileSync(DB_FILE));
    data.push(newEntry);
    fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: 'Database Write Error' });
  }
});

app.get('/api/scores', (req, res) => {
  try {
    const data = JSON.parse(fs.readFileSync(DB_FILE));
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: 'Database Read Error' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Osmosis Live Server running on port ${PORT}`));
