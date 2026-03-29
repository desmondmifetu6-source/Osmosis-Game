const fs = require('fs');
const path = require('path');

const directory = __dirname;

const replacements = {
  '#190f09': '#0a1710',
  '#1f1109': '#0f2115',
  '#2b1d14': '#162e1c',
  '#3e2723': '#1e3b26',
  '#4e342e': '#2b4f35',
  '#5c4b3a': '#426b52',
  'rgba(139, 69, 19': 'rgba(46, 139, 87',
  'rgba(58, 46, 36': 'rgba(30, 59, 38'
};

function processFile(filePath) {
  if (filePath.endsWith('.html') || filePath.endsWith('.css')) {
    let content = fs.readFileSync(filePath, 'utf8');
    let original = content;
    
    for (const [brown, green] of Object.entries(replacements)) {
      // Use global regex, case insensitive just in case
      const regex = new RegExp(brown.replace(/\(/g, '\\('), 'gi');
      content = content.replace(regex, green);
    }
    
    if (content !== original) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`Updated ${path.basename(filePath)}`);
    }
  }
}

function walkDir(dir) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const fullPath = path.join(dir, file);
    if (fs.statSync(fullPath).isDirectory()) {
      if (!fullPath.includes('.git') && !fullPath.includes('node_modules')) {
        walkDir(fullPath);
      }
    } else {
      processFile(fullPath);
    }
  }
}

walkDir(directory);
console.log('Color replacement complete.');
