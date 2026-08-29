const fs = require('fs');

// Mock window for Node testing
global.window = global;

require('../core_dictionary.js');

console.log('Testing STEMDictionary.predictWords():\n');

['pho', 'abb', 'dna', 'chem', 'grav'].forEach(query => {
  console.log(`=== Query: "${query}" ===`);
  const predictions = window.STEMDictionary.predictWords(query, 5);
  predictions.forEach((p, idx) => {
    console.log(`  ${idx + 1}. [${p.matchType}] ${p.word} (${p.display}) -> ${p.definition.substring(0, 60)}...`);
  });
  console.log('');
});
