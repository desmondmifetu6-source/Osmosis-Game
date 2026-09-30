const fs = require('fs');
const path = require('path');

const map = JSON.parse(fs.readFileSync('dictionary_diagrams_map.json', 'utf8'));
const mappedValues = new Set(Object.values(map));

const folders = [
  'c-d didagrams',
  'cropped diagrams',
  'e-d diagrams',
  'f-j diagrams',
  'k_diagrams',
  'l-m diagrams',
  'n-o diagrams',
  'p_diagrams',
  'section a-b images'
];

folders.forEach(folder => {
  if (!fs.existsSync(folder)) return;
  const files = fs.readdirSync(folder).filter(f => f.match(/\.(png|jpe?g|webp|gif)$/i));
  let inDiagrams = 0;
  let inMap = 0;
  
  files.forEach(f => {
    // Check if copied to diagrams/ with same name or dict_ prefix
    const directPath = `diagrams/${f}`;
    const dictPath = `diagrams/dict_${f}`;
    const mappedDirect = mappedValues.has(directPath);
    const mappedDict = mappedValues.has(dictPath);
    if (fs.existsSync(path.join('diagrams', f)) || fs.existsSync(path.join('diagrams', `dict_${f}`))) {
      inDiagrams++;
    }
    if (mappedDirect || mappedDict) {
      inMap++;
    }
  });
  console.log(`Folder [${folder}]: ${files.length} images. ${inDiagrams} found in diagrams/, ${inMap} mapped directly.`);
});
