global.window = global;
global.document = {
  readyState: 'complete',
  createElement: (tag) => {
    return {
      tagName: tag.toUpperCase(),
      style: {},
      classList: {
        contains: () => false,
        add: () => {}
      },
      querySelectorAll: () => [],
      parentNode: { insertBefore: () => {} },
      appendChild: () => {}
    };
  },
  head: { appendChild: () => {} },
  querySelector: () => null
};
global.HTMLElement = class {
  constructor() {
    this.attributes = {};
    this.innerHTML = '';
  }
  getAttribute(name) { return this.attributes[name]; }
  setAttribute(name, val) { this.attributes[name] = val; }
  hasAttribute(name) { return name in this.attributes; }
  querySelectorAll() { return []; }
};

global.renderMathInElement = (target, options) => {
  target.innerHTML = target.innerHTML.replace(/\$\$([\s\S]+?)\$\$/g, '<span class="katex-display">$1</span>')
                                     .replace(/\$([^\$\n]+?)\$/g, '<span class="katex">$1</span>');
};

require('../core_formula_renderer.js');

const el = new global.HTMLElement();
el.setAttribute('data-raw-content', 'Formula: $$E = mc^2$$ where $m$ is mass.');
window.renderScienceText(el);
console.log("Rendered innerHTML:\n", el.innerHTML);
