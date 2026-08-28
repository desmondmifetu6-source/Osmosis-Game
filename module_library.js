initModal();

const inputEl = document.getElementById('dict-input');
const searchBtn = document.getElementById('dict-search-btn');
const resultEl = document.getElementById('dict-result');
const errorEl = document.getElementById('dict-error');
const emptyStateEl = document.getElementById('dict-empty-state');
const emptyQueryTerm = document.getElementById('empty-query-term');
const resInsteadOf = document.getElementById('res-instead-of');

const resWord = document.getElementById('res-word');
const resPhonetic = document.getElementById('res-phonetic');
const resMeaning = document.getElementById('res-meaning');

searchBtn.addEventListener('click', performSearch);
inputEl.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') performSearch();
});

function lookupInStemDictionary(query) {
  if (typeof window.STEMDictionary === 'undefined') return null;

  const rawQuery = query.trim();
  const normalized = rawQuery.toLowerCase();
  if (!normalized) return null;

  // 1. Direct exact match via STEMDictionary engine (handles exact word, synonyms, hyphens/spaces)
  if (typeof window.STEMDictionary.getEntry === 'function') {
    const entry = window.STEMDictionary.getEntry(normalized);
    if (entry) {
      return {
        word: entry.word,
        raw: entry.raw,
        definition: entry.definition,
        isExact: true
      };
    }
  }

  // 2. Exact match in all words bank
  const all = window.STEMDictionary.getAllWords ? window.STEMDictionary.getAllWords() : [];
  const exactEntry = all.find(
    (e) => e.word.toLowerCase() === normalized || (e.raw && e.raw.toLowerCase() === normalized)
  );
  if (exactEntry) {
    return {
      word: exactEntry.word,
      raw: exactEntry.raw,
      definition: exactEntry.definition,
      isExact: true
    };
  }

  // 3. Smart Word-Boundary / Phrase matching (e.g. user typed "phone" -> match "mobile phone")
  // Check if the query is a complete standalone word within multi-word STEM entries
  const escaped = normalized.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
  const wordRegex = new RegExp(`\\b${escaped}\\b`, 'i');

  const wordInTitleMatches = [];
  const wordInRawMatches = [];
  const startsWithMatches = [];

  for (let i = 0; i < all.length; i++) {
    const item = all[i];
    const w = item.word.toLowerCase();
    const raw = (item.raw || '').toLowerCase();

    if (wordRegex.test(w)) {
      wordInTitleMatches.push(item);
    } else if (wordRegex.test(raw)) {
      wordInRawMatches.push(item);
    } else if (w.startsWith(normalized)) {
      startsWithMatches.push(item);
    }
  }

  if (wordInTitleMatches.length > 0) {
    wordInTitleMatches.sort((a, b) => a.word.length - b.word.length);
    const best = wordInTitleMatches[0];
    return {
      word: best.word,
      raw: best.raw,
      definition: best.definition,
      isExact: false,
      replacedQuery: rawQuery
    };
  }

  if (wordInRawMatches.length > 0) {
    wordInRawMatches.sort((a, b) => a.word.length - b.word.length);
    const best = wordInRawMatches[0];
    return {
      word: best.word,
      raw: best.raw,
      definition: best.definition,
      isExact: false,
      replacedQuery: rawQuery
    };
  }

  // 4. Close prefix / typo match (e.g. "photosynthes" -> "photosynthesis")
  if (normalized.length >= 4 && startsWithMatches.length > 0) {
    startsWithMatches.sort((a, b) => a.word.length - b.word.length);
    const best = startsWithMatches[0];
    if (best.word.length <= normalized.length + 4) {
      return {
        word: best.word,
        raw: best.raw,
        definition: best.definition,
        isExact: false,
        replacedQuery: rawQuery
      };
    }
  }

  // 5. Gibberish / unmatched inputs return null -> shows minimal sketch empty state
  return null;
}

function showEmptyState(query) {
  if (resultEl) resultEl.style.display = 'none';
  if (errorEl) errorEl.style.display = 'none';

  if (emptyStateEl) {
    if (emptyQueryTerm) {
      emptyQueryTerm.textContent = `"${query}"`;
    }
    emptyStateEl.style.display = 'block';
  }

  if (typeof AudioManager !== 'undefined') AudioManager.play('error');
}

function performSearch() {
  const query = inputEl.value.trim();
  if (!query) return;

  // Dismiss autocomplete dropdown if visible
  const dropdown = document.getElementById('autocomplete-dropdown');
  if (dropdown) dropdown.style.display = 'none';

  if (resultEl) resultEl.style.display = 'none';
  if (errorEl) errorEl.style.display = 'none';
  if (emptyStateEl) emptyStateEl.style.display = 'none';

  if (typeof AudioManager !== 'undefined') AudioManager.play('click');

  const entry = lookupInStemDictionary(query);

  if (!entry) {
    showEmptyState(query);
    return;
  }

  // Handle "Showing X instead of Y" message
  if (resInsteadOf) {
    if (!entry.isExact && entry.replacedQuery) {
      resInsteadOf.innerHTML = `Showing definition for <strong>"${entry.word}"</strong> instead of <em>"${entry.replacedQuery}"</em>`;
      resInsteadOf.style.display = 'block';
    } else {
      resInsteadOf.style.display = 'none';
      resInsteadOf.innerHTML = '';
    }
  }

  resWord.textContent = entry.word;
  resPhonetic.textContent = 'Osmosis STEM Dictionary';
  resMeaning.textContent = entry.definition;

  // Check for Diagram
  const diagramBox = document.getElementById('res-diagram-box');
  const diagramContent = document.getElementById('res-diagram-content');
  const diagramImg = document.getElementById('res-diagram-img');
  
  let diagramSrc = null;
  if (typeof window.DictionaryDiagrams !== 'undefined') {
    const wordKey = entry.word.toLowerCase().trim();
    const queryKey = query.toLowerCase().trim();
    diagramSrc = window.DictionaryDiagrams[wordKey] || window.DictionaryDiagrams[queryKey];
    
    if (!diagramSrc) {
      const diagKeys = Object.keys(window.DictionaryDiagrams);
      const matchedKey = diagKeys.find(k => k.includes(wordKey) || wordKey.includes(k) || k.includes(queryKey));
      if (matchedKey) {
        diagramSrc = window.DictionaryDiagrams[matchedKey];
      }
    }
  }

  if (diagramBox) {
    if (diagramSrc && diagramImg && diagramContent) {
      diagramImg.src = diagramSrc;
      diagramImg.alt = `${entry.word} diagram`;
      diagramContent.style.display = 'block';
      diagramBox.style.display = 'block';
    } else {
      diagramBox.style.display = 'none';
      if (diagramContent) diagramContent.style.display = 'none';
      if (diagramImg) diagramImg.src = '';
    }
  }

  resultEl.style.display = 'block';
  if (typeof AudioManager !== 'undefined') AudioManager.play('chip');
}

document.getElementById('go-home-btn').addEventListener('click', () => {
  window.location.href = '01_home_menu.html';
});


