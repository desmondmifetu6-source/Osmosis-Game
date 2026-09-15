global.window = global;
const fs = require('fs');
const code = fs.readFileSync('core_dictionary.js', 'utf8');
eval(code);

const queries = [
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

console.log("=== Testing STEMDictionary.getEntry ===");
for (const q of queries) {
  const e = window.STEMDictionary.getEntry(q);
  console.log(q.padEnd(25) + ' => ' + (e ? 'FOUND: ' + e.word : 'NOT FOUND'));
}
