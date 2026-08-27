const fs = require('fs');

global.window = global;
const code = fs.readFileSync('core_dictionary.js', 'utf-8');
eval(code);

const testQueries = [
  'amorphous carbon',
  'amino acid',
  'axis of symmetry',
  'circle graph',
  'pie chart',
  'bar chart',
  'base-pairing rule',
  'flower',
  'cell',
  'photosynthesis',
  'dynamic programming'
];

console.log("=== TESTING SEARCH LOOKUP IN STEMDictionary ===");
for (const q of testQueries) {
  const def = window.STEMDictionary.getDefinition(q);
  console.log(`\nQuery: "${q}"`);
  if (def) {
    console.log(`FOUND: ${def.substring(0, 120)}...`);
  } else {
    console.log("NOT FOUND!");
  }
}
