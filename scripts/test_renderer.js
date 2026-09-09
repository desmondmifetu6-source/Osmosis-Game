const fs = require('fs');

// Mock browser globals for Node.js test
global.window = global;
global.document = {
  readyState: 'complete',
  createElement: () => ({ style: {}, classList: { add: () => {} } }),
  head: { appendChild: () => {} },
  querySelector: () => null
};
global.HTMLElement = class {};

require('../core_formula_renderer.js');

const testText = "Eddington limit formula: $$L_{\\text{Edd}} = \\frac{4\\pi G M m_p c}{\\sigma_T}$$ where $G$ is constant.";
console.log("Original text:\n", testText);

const formatted = window.formatScienceText(testText);
console.log("\nAfter formatScienceText:\n", formatted);
