const fs = require('fs');
global.window = global;
const dictCode = fs.readFileSync('core_dictionary.js', 'utf-8');
eval(dictCode);

const allWords = window.STEMDictionary.getAllWords();

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
  const escaped = normalized.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
  const wordRegex = new RegExp(`\\b${escaped}\\b`, 'i');

  const wordBoundaryMatches = [];
  const startsWithMatches = [];

  for (let i = 0; i < all.length; i++) {
    const item = all[i];
    const w = item.word.toLowerCase();
    const raw = (item.raw || '').toLowerCase();

    if (wordRegex.test(w) || wordRegex.test(raw)) {
      wordBoundaryMatches.push(item);
    } else if (w.startsWith(normalized)) {
      startsWithMatches.push(item);
    }
  }

  if (wordBoundaryMatches.length > 0) {
    wordBoundaryMatches.sort((a, b) => a.word.length - b.word.length);
    const best = wordBoundaryMatches[0];
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

  return null;
}

const testCases = [
  'photosynthesis',
  'photosynthes',
  'phone',
  'cell',
  'acid',
  'asdfghjk',
  'xyz123',
  'randomgibberish'
];

console.log('=== TEST SMART LOOKUP RESULTS ===');
testCases.forEach(q => {
  const res = lookupInStemDictionary(q);
  if (!res) {
    console.log(`Query "${q}" -> NULL [Show clean sketch empty state]`);
  } else if (res.isExact) {
    console.log(`Query "${q}" -> Exact match: "${res.word}"`);
  } else {
    console.log(`Query "${q}" -> Close match: Showing "${res.word}" instead of "${res.replacedQuery}"`);
  }
});
