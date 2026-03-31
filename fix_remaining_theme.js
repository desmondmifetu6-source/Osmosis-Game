const fs = require('fs');
const path = require('path');

const dir = __dirname;
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') || f.endsWith('.js') || f.endsWith('.css'));

const replacements = [
  // Fonts
  [/Playfair\+Display[^"']*/g, 'Inter:wght@400;500;600;700&display=swap'],
  [/Lora[^"']*/g, 'Roboto:wght@400;500;700&display=swap'],

  // Colors
  [/#254515/ig, 'var(--bg-dark)'],
  [/#305e19/ig, 'var(--accent-primary)'],
  [/#1b2e10/ig, 'var(--bg-dark)'],
  [/#15220c/ig, 'var(--text-main)'],
  [/#D4AF37/ig, 'var(--accent-primary)'],
  [/#e0d4b8/ig, 'var(--surface-white)'],
  [/#2a2118/ig, 'var(--bg-dark)'],
  [/#4a3c2b/ig, 'var(--surface-dim)'],
  [/#fdfbf7/ig, 'var(--bg-light)'],

  // Hardcode backgrounds that were archaic
  [/background: linear-gradient\([^)]+\)/g, 'background: var(--bg-light)']
];

files.forEach(file => {
  if (file === 'apply_modern_theme.js' || file === 'fix_remaining_theme.js') return;

  const filePath = path.join(dir, file);
  let content = fs.readFileSync(filePath, 'utf8');
  let original = content;

  replacements.forEach(([regex, replacement]) => {
    content = content.replace(regex, replacement);
  });

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Updated ${file}`);
  }
});

console.log('Final sweep complete.');
