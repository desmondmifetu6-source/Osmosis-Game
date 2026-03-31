const fs = require('fs');
const path = require('path');

const dir = __dirname;
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') || f.endsWith('.js'));

const replacements = [
  // CSS Variables
  [/--wood-bg/g, '--bg-light'],
  [/--wood-dark/g, '--bg-dark'],
  [/--parchment-dark/g, '--surface-dim'],
  [/--parchment/g, '--surface-white'],
  [/--ink-light/g, '--text-secondary'],
  [/--ink/g, '--text-main'],
  [/--gold/g, '--accent-primary'],
  [/--font-serif/g, '--font-main'],
  [/--font-body/g, '--font-main'],
  
  // HTML Class names with archaic words
  [/parchment-large/g, 'card-surface'],

  // Hardcoded Hex Colors (Reds)
  [/#c62828/ig, 'var(--accent-red)'],
  [/#ff5252/ig, 'var(--accent-red)'],
  [/#ef5350/ig, 'var(--accent-red)'],
  [/#ffebee/ig, '#F8D7DA'],
  [/#3e0b0b/ig, '#2C0B0E'],
  
  // Greens
  [/#2e7d32/ig, 'var(--accent-green)'],
  [/#4caf50/ig, 'var(--accent-green)'],
  [/#305e19/ig, 'var(--accent-green)'],
  [/#e8f5e9/ig, '#D1E7DD'],

  // Gold/Old Accent variants
  [/#D4AF37/ig, 'var(--accent-primary)'],
  [/rgba\(\s*212\s*,\s*175\s*,\s*55/g, 'rgba(79, 70, 229'], // gold rgb -> indigo rgb

  // Archaic backgrounds/borders
  [/#fdfbf7/ig, 'var(--bg-light)'],
  [/#f4ecd8/ig, 'var(--surface-dim)'],
  [/#d3cbb8/ig, 'var(--surface-dim)'],
  [/#3b2f2f/ig, 'var(--text-main)'],
  [/rgba\(\s*139\s*,\s*115\s*,\s*85/g, 'rgba(108, 117, 125'], // brown rgb -> grey rgb Wait, old theme had 139,115,85.
  
  // Replace old fonts in links
  [/https:\/\/fonts\.googleapis\.com\/css2\?family=Playfair\+Display[^"']*/g, 'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap']
];

files.forEach(file => {
  // skip self and previous replace files
  if (file === 'apply_modern_theme.js' || file === 'replace_colors.js' || file === 'replace_colors_v2.js') return;

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

console.log('Sweep complete.');
