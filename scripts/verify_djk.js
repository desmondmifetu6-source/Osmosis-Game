const d = require('../dictionary.json');
const checks = [
  ['D', "dini's theorem"],
  ['D', 'deduction theorem'],
  ['J', 'jordan normal form'],
  ['J', 'jeans length'],
  ['K', 'koch curve'],
  ['K', 'kinetic theory of gases'],
];
checks.forEach(([s, w]) => {
  const e = d[s].find(x => x.word.toLowerCase() === w);
  console.log(s, w, e && e.definition.includes('$') ? 'OK' : 'MISSING');
});
