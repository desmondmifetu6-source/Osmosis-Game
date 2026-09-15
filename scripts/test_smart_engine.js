global.window = global;
const fs = require('fs');
const code = fs.readFileSync('core_dictionary.js', 'utf8');
eval(code);

function normalizeQuery(str) {
  if (!str) return '';
  return str.toLowerCase()
    .replace(/['’`]/g, '')            // remove apostrophes (gauss's -> gausss, boyle's -> boyles)
    .replace(/[,\.;:!\?]/g, ' ')      // remove punctuation
    .replace(/[-_]/g, ' ')            // convert hyphens to space
    .replace(/\s+/g, ' ')             // collapse whitespace
    .trim();
}

function getCandidateSingulars(word) {
  const forms = [];
  if (word.endsWith('ies') && word.length > 4) {
    forms.push(word.slice(0, -3) + 'y');
  }
  if (word.endsWith('es') && word.length > 3) {
    forms.push(word.slice(0, -2));
    forms.push(word.slice(0, -1)); // e.g. gases -> gas
  }
  if (word.endsWith('s') && !word.endsWith('ss') && word.length > 2) {
    forms.push(word.slice(0, -1));
  }
  return forms;
}

// Build a normalized search index from all entries
const allEntries = window.STEMDictionary.getAllWords();
const normalizedMap = new Map();

for (let i = 0; i < allEntries.length; i++) {
  const e = allEntries[i];
  const normWord = normalizeQuery(e.word);
  if (!normalizedMap.has(normWord)) normalizedMap.set(normWord, e);
  
  // Clean 's: e.g. "boyles law" -> also index "boyle law"
  const noS = normWord.replace(/(\w+)s\b/g, '$1');
  if (!normalizedMap.has(noS)) normalizedMap.set(noS, e);

  // Synonyms
  if (e.synonyms && Array.isArray(e.synonyms)) {
    for (const syn of e.synonyms) {
      const normSyn = normalizeQuery(syn);
      if (!normalizedMap.has(normSyn)) normalizedMap.set(normSyn, e);
      const noSynS = normSyn.replace(/(\w+)s\b/g, '$1');
      if (!normalizedMap.has(noSynS)) normalizedMap.set(noSynS, e);
    }
  }
}

function smartLookup(query) {
  if (!query) return null;
  const rawNorm = normalizeQuery(query);
  
  // 1. Direct normalized lookup
  if (normalizedMap.has(rawNorm)) return normalizedMap.get(rawNorm);

  // 2. Try stripping 's (e.g. boyles law -> boyle law, gauss law)
  const noS = rawNorm.replace(/(\w+)s\b/g, '$1');
  if (normalizedMap.has(noS)) return normalizedMap.get(noS);

  // 3. Plural to singular (cells -> cell, acids -> acid)
  const singulars = getCandidateSingulars(rawNorm);
  for (const s of singulars) {
    if (normalizedMap.has(s)) return normalizedMap.get(s);
  }

  // 4. Substring / phrase match in all entries
  // e.g. "newton first law" -> "newton's first law of motion"
  const tokens = rawNorm.split(' ').filter(t => t.length > 1);
  if (tokens.length > 0) {
    let best = null;
    let bestScore = 0;

    for (let i = 0; i < allEntries.length; i++) {
      const e = allEntries[i];
      const eNorm = normalizeQuery(e.word);
      const eRaw = normalizeQuery(e.raw || '');

      // Check if all tokens are present
      const allInWord = tokens.every(t => eNorm.includes(t) || eRaw.includes(t));
      if (allInWord) {
        // Shorter word that contains all tokens is a better match
        const score = 1000 - e.word.length;
        if (score > bestScore) {
          bestScore = score;
          best = e;
        }
      }
    }
    if (best) return best;
  }

  return null;
}

const testQueries = [
  'boyle law', 'boyles law', "boyle's law",
  'charles law', 'charles laws', "charles's law",
  'gauss law', "gauss's law", "gauss' law",
  'newton law', 'newton laws', "newton's first law",
  'gas', 'gases',
  'atom', 'atoms',
  'cell', 'cells',
  'acid', 'acids',
  'enzyme', 'enzymes',
  'photosynthesis',
  'respiration',
  'mitosis',
  'meiosis',
  'osmosis'
];

console.log("=== Testing Smart Lookup Engine ===");
for (const q of testQueries) {
  const e = smartLookup(q);
  console.log(q.padEnd(25) + ' => ' + (e ? 'FOUND: ' + e.word : 'NOT FOUND'));
}
