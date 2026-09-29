const fs = require('fs');
const path = require('path');

const baseDir = path.join(__dirname, '..');
const dictPath = path.join(baseDir, 'dictionary.json');
const outputPath = path.join(baseDir, 'core_dictionary.js');
const pyScriptPath = path.join(__dirname, 'rebuild_core_dictionary.py');

console.log('Loading dictionary.json...');
const dictData = JSON.parse(fs.readFileSync(dictPath, 'utf8'));

console.log('Reading engine template from rebuild_core_dictionary.py...');
const pyContent = fs.readFileSync(pyScriptPath, 'utf8');
const startToken = 'IIFE_ENGINE = r"""';
const endToken = '"""\n\ndef rebuild():';
const startIndex = pyContent.indexOf(startToken) + startToken.length;
const endIndex = pyContent.indexOf(endToken);

if (startIndex === -1 || endIndex === -1) {
  console.error('Could not extract IIFE_ENGINE from Python script!');
  process.exit(1);
}

const iifeEngine = pyContent.substring(startIndex, endIndex);

console.log('Serializing wordBank...');
const wordBankJson = JSON.stringify(dictData);

console.log('Writing core_dictionary.js...');
const header = '// STEM Core Dictionary Data Auto-Generated with Full Search & Autocomplete Engine\n';
const wordBankLine = `const wordBank = ${wordBankJson};\n\n`;
const finalOutput = header + wordBankLine + iifeEngine;

fs.writeFileSync(outputPath, finalOutput, 'utf8');
console.log(`Done! Written ${finalOutput.length.toLocaleString()} characters to core_dictionary.js`);
