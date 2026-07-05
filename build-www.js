const fs = require('fs');
const path = require('path');

const src = __dirname;
const dest = path.join(__dirname, 'www');

if (fs.existsSync(dest)) {
  fs.rmSync(dest, { recursive: true, force: true });
}
fs.mkdirSync(dest);

const ignore = ['node_modules', 'dist', 'android', 'ios', 'www', '.git', 'package.json', 'package-lock.json', 'build-www.js'];

function copyFolderSync(from, to) {
  if (!fs.existsSync(to)) fs.mkdirSync(to);
  fs.readdirSync(from).forEach(element => {
    if (ignore.includes(element) || element.startsWith('.')) return;
    const stat = fs.lstatSync(path.join(from, element));
    if (stat.isFile()) {
      fs.copyFileSync(path.join(from, element), path.join(to, element));
    } else if (stat.isDirectory()) {
      copyFolderSync(path.join(from, element), path.join(to, element));
    }
  });
}

copyFolderSync(src, dest);
console.log('Copied files to www');
