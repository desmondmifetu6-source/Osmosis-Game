initModal();

const inputEl = document.getElementById('dict-input');
const searchBtn = document.getElementById('dict-search-btn');
const resultEl = document.getElementById('dict-result');
const errorEl = document.getElementById('dict-error');

const resWord = document.getElementById('res-word');
const resPhonetic = document.getElementById('res-phonetic');
const resMeaning = document.getElementById('res-meaning');

searchBtn.addEventListener('click', performSearch);
inputEl.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') performSearch();
});

function lookupInStemDictionary(query) {
  if (typeof window.STEMDictionary === 'undefined') return null;

  const normalized = query.trim().toLowerCase();
  if (!normalized) return null;

  const exactDefinition = window.STEMDictionary.getDefinition(normalized);
  if (exactDefinition) {
    const entry = window.STEMDictionary.getAllWords().find(
      (e) => e.word.toLowerCase() === normalized
    );
    return {
      word: entry ? entry.word : query.trim(),
      definition: exactDefinition
    };
  }

  const matches = window.STEMDictionary.getAllWords().filter((entry) => {
    const word = entry.word.toLowerCase();
    return word.startsWith(normalized) || word.includes(normalized);
  });

  if (matches.length === 0) return null;

  const best = matches.find((entry) => entry.word.toLowerCase().startsWith(normalized)) || matches[0];
  return {
    word: best.word,
    definition: best.definition,
    suggestions: matches.length > 1 ? matches.slice(0, 5).map((m) => m.word) : null
  };
}

function performSearch() {
  const query = inputEl.value.trim();
  if (!query) return;

  resultEl.style.display = 'none';
  errorEl.style.display = 'none';
  if (typeof AudioManager !== 'undefined') AudioManager.play('click');

  const entry = lookupInStemDictionary(query);

  if (!entry) {
    errorEl.style.display = 'block';
    if (typeof AudioManager !== 'undefined') AudioManager.play('error');
    return;
  }

  resWord.textContent = entry.word;
  resPhonetic.textContent = 'Osmosis STEM Dictionary';
  resMeaning.textContent = entry.definition;

  // Check for Diagram
  const diagramBox = document.getElementById('res-diagram-box');
  const diagramContent = document.getElementById('res-diagram-content');
  const diagramImg = document.getElementById('res-diagram-img');
  const noDiagramMsg = document.getElementById('res-no-diagram-msg');
  
  let diagramSrc = null;
  if (typeof window.DictionaryDiagrams !== 'undefined') {
    const wordKey = entry.word.toLowerCase().trim();
    const queryKey = query.toLowerCase().trim();
    diagramSrc = window.DictionaryDiagrams[wordKey] || window.DictionaryDiagrams[queryKey];
    
    if (!diagramSrc) {
      // Partial match search in DictionaryDiagrams
      const diagKeys = Object.keys(window.DictionaryDiagrams);
      const matchedKey = diagKeys.find(k => k.includes(wordKey) || wordKey.includes(k) || k.includes(queryKey));
      if (matchedKey) {
        diagramSrc = window.DictionaryDiagrams[matchedKey];
      }
    }
  }

  if (diagramBox) {
    diagramBox.style.display = 'block';
    if (diagramSrc && diagramImg && diagramContent) {
      diagramImg.src = diagramSrc;
      diagramImg.alt = `${entry.word} diagram`;
      diagramContent.style.display = 'block';
      if (noDiagramMsg) noDiagramMsg.style.display = 'none';
    } else {
      if (diagramContent) diagramContent.style.display = 'none';
      if (noDiagramMsg) noDiagramMsg.style.display = 'block';
    }
  }

  if (entry.suggestions && entry.suggestions.length > 1) {
    const note = document.createElement('p');
    note.style.marginTop = '1rem';
    note.style.fontSize = '0.95rem';
    note.style.color = 'var(--text-secondary)';
    note.textContent = `Related entries: ${entry.suggestions.join(', ')}`;
    resMeaning.appendChild(note);
  }

  resultEl.style.display = 'block';
  if (typeof AudioManager !== 'undefined') AudioManager.play('chip');
}

document.getElementById('go-home-btn').addEventListener('click', () => {
  window.location.href = '01_home_menu.html';
});
