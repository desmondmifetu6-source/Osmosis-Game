const fs = require('fs');
const path = require('path');

// 1. Load core_dictionary.js and core_dictionary_diagrams.js
const dictCode = fs.readFileSync(path.join(__dirname, '..', 'core_dictionary.js'), 'utf-8');
const diagCode = fs.readFileSync(path.join(__dirname, '..', 'core_dictionary_diagrams.js'), 'utf-8');

// Mock window environment
const window = {};
eval(dictCode);
eval(diagCode);

console.log(`STEMDictionary words loaded: ${window.STEMDictionary ? window.STEMDictionary.getAllWords().length : 0}`);
console.log(`DictionaryDiagrams entries loaded: ${Object.keys(window.DictionaryDiagrams || {}).length}`);

function resolveDiagramForWord(entry, query) {
  if (typeof window.DictionaryDiagrams === 'undefined') return null;
  const wordKey = entry.word.toLowerCase().trim();
  const queryKey = (query || '').toLowerCase().trim();
  const baseWordKey = wordKey.replace(/\(.*?\)/g, '').trim();
  const rawKey = (entry.raw || '').toLowerCase().trim();

  return window.DictionaryDiagrams[wordKey] ||
         window.DictionaryDiagrams[rawKey] ||
         window.DictionaryDiagrams[baseWordKey] ||
         window.DictionaryDiagrams[queryKey] ||
         null;
}

// Previously problematic words due to substring matches:
const testWordsNoFalseDiagrams = [
  "work",
  "force",
  "gravity",
  "momentum",
  "hormone",
  "action",
  "radiation",
  "convection",
  "sheath",
  "knot",
  "bone",
  "base",
  "plasma",
  "current",
  "voltage"
];

// Verified diagram words:
const testWordsWithVerifiedDiagrams = [
  "abacus",
  "abbe prism",
  "abbe refractometer",
  "aberration",
  "abscissa",
  "absorption spectrum",
  "leaf",
  "heart",
  "neuron",
  "osmosis",
  "photosynthesis",
  "atom",
  "mitochondrion",
  "electric circuit",
  "cell membrane",
  "solar eclipse",
  "lunar eclipse",
  "covalent bond",
  "ionic bond",
  "meiosis",
  "synapse",
  "magnetic field",
  "respiratory system",
  "skeletal system",
  "rock cycle",
  "plate tectonics"
];

let failed = 0;

console.log("\n--- Testing words for absence of false diagrams ---");
for (const word of testWordsNoFalseDiagrams) {
  const entry = window.STEMDictionary.getEntry(word);
  if (!entry) continue;
  const diag = resolveDiagramForWord(entry, word);
  if (diag !== null) {
    console.error(`❌ FALSE DIAGRAM for '${word}': ${diag}`);
    failed++;
  } else {
    console.log(`✅ '${word}' -> Pure Definition (Diagram: None)`);
  }
}

console.log("\n--- Testing verified diagram words ---");
for (const word of testWordsWithVerifiedDiagrams) {
  const entry = window.STEMDictionary.getEntry(word);
  if (!entry) {
    console.error(`❌ Word '${word}' not found in dictionary bank.`);
    failed++;
    continue;
  }
  const diag = resolveDiagramForWord(entry, word);
  if (!diag) {
    console.error(`❌ Missing verified diagram for '${word}'`);
    failed++;
  } else {
    console.log(`✅ '${word}' -> Diagram: ${diag}`);
  }
}

if (failed === 0) {
  console.log("\n🎉 ALL TESTS PASSED! Strict resolution validated with zero false diagrams.");
  process.exit(0);
} else {
  console.error(`\n💥 ${failed} test(s) failed.`);
  process.exit(1);
}
