const fs = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const data = JSON.parse(fs.readFileSync(dictPath, 'utf8'));

let embeddedCount = 0;

for (const letter of Object.keys(data)) {
  const list = data[letter];
  if (!Array.isArray(list)) continue;

  for (const entry of list) {
    if (entry.formula && typeof entry.formula === 'string') {
      const trimmedFormula = entry.formula.trim();
      if (!entry.definition.includes(trimmedFormula)) {
        let formulaBlock = `\n\n${trimmedFormula}`;
        if (entry.formula_description && !entry.definition.includes(entry.formula_description.trim())) {
          formulaBlock += `\n\n${entry.formula_description.trim()}`;
        }
        entry.definition = entry.definition.trim() + formulaBlock;
        embeddedCount++;
      }
    }
  }
}

fs.writeFileSync(dictPath, JSON.stringify(data, null, 2), 'utf8');
console.log(`Successfully embedded formulas into definitions for ${embeddedCount} entries.`);
