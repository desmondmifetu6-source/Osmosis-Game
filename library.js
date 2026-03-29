initModal();

const inputEl = document.getElementById('dict-input');
const searchBtn = document.getElementById('dict-search-btn');
const loadingEl = document.getElementById('dict-loading');
const resultEl = document.getElementById('dict-result');
const errorEl = document.getElementById('dict-error');

const resWord = document.getElementById('res-word');
const resPhonetic = document.getElementById('res-phonetic');
const resMeaning = document.getElementById('res-meaning');

searchBtn.addEventListener('click', performSearch);
inputEl.addEventListener('keypress', (e) => {
  if(e.key === 'Enter') performSearch();
});

async function performSearch() {
  const query = inputEl.value.trim().toLowerCase();
  if(!query) return;
  
  resultEl.style.display = 'none';
  errorEl.style.display = 'none';
  loadingEl.classList.remove('hidden');
  AudioManager.play('click');
  
  try {
    const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${query}`);
    if(!res.ok) throw new Error("Not found");
    const data = await res.json();
    
    // Pick the first entry
    const entry = data[0];
    resWord.textContent = entry.word;
    
    // Extract phonetic if available
    let phonetic = entry.phonetic || "";
    if(!phonetic && entry.phonetics) {
       const p = entry.phonetics.find(ph => ph.text);
       if(p) phonetic = p.text;
    }
    resPhonetic.textContent = phonetic;
    
    // Stitch all meanings together cleanly
    let meaningsHTML = '';
    entry.meanings.forEach(m => {
      // For each speech part, get the first most relevant definition
      const def = m.definitions[0].definition;
      meaningsHTML += `<strong>${m.partOfSpeech}</strong>: ${def}<br><br>`;
    });
    resMeaning.innerHTML = meaningsHTML;
    
    loadingEl.classList.add('hidden');
    resultEl.style.display = 'block';
    
    // Success Ping
    AudioManager.play('chip');
  } catch (err) {
    loadingEl.classList.add('hidden');
    errorEl.style.display = 'block';
    AudioManager.play('error');
  }
}

document.getElementById('go-home-btn').addEventListener('click', () => {
  window.location.href = 'home.html';
});
