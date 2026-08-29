/**
 * =====================================================================
 * CORE FORMULA & SCIENTIFIC NOTATION RENDERER (Osmosis STEM Engine)
 * =====================================================================
 * Transforms raw text, scientific notation, chemical formulas, and 
 * mathematical expressions into crisp, beautiful, accessible typography.
 * 
 * Features:
 * - Seamless KaTeX LaTeX math rendering (with dynamic auto-loader)
 * - Protected LaTeX delimiters ($...$ and $$...$$) to prevent HTML corruption
 * - Automatic chemical compound parsing (H2O -> H₂O) in plain text
 * - Physics units and power normalization (m/s^2, kg m^-3, x 10^8)
 * - Standalone formula callout cards with copy actions
 * - Resilient fallback rendering when offline or without CDN
 */

(function () {
  'use strict';

  // Configuration & KaTeX CDN sources
  const KATEX_VERSION = '0.16.9';
  const KATEX_CSS_URL = `https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist/katex.min.css`;
  const KATEX_JS_URL = `https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist/katex.min.js`;
  const KATEX_AUTO_RENDER_URL = `https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist/contrib/auto-render.min.js`;

  let katexLoaded = false;
  let katexLoadingPromise = null;

  // Load KaTeX dynamically if not already present in the DOM
  function loadKaTeX() {
    if (window.katex && window.renderMathInElement) {
      katexLoaded = true;
      return Promise.resolve(window.katex);
    }

    if (katexLoadingPromise) {
      return katexLoadingPromise;
    }

    katexLoadingPromise = new Promise((resolve) => {
      // 1. Inject KaTeX CSS
      if (!document.querySelector(`link[href*="katex"]`)) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = KATEX_CSS_URL;
        link.crossOrigin = 'anonymous';
        document.head.appendChild(link);
      }

      // 2. Inject KaTeX JS
      if (!window.katex) {
        const script = document.createElement('script');
        script.src = KATEX_JS_URL;
        script.crossOrigin = 'anonymous';
        script.onload = () => {
          // 3. Inject KaTeX Auto-Render contrib
          const autoScript = document.createElement('script');
          autoScript.src = KATEX_AUTO_RENDER_URL;
          autoScript.crossOrigin = 'anonymous';
          autoScript.onload = () => {
            katexLoaded = true;
            resolve(window.katex);
          };
          autoScript.onerror = () => {
            katexLoaded = true;
            resolve(window.katex);
          };
          document.head.appendChild(autoScript);
        };
        script.onerror = () => {
          console.warn('[FormulaRenderer] KaTeX CDN unreachable. Using semantic typography fallback.');
          katexLoaded = false;
          resolve(null);
        };
        document.head.appendChild(script);
      } else if (!window.renderMathInElement) {
        const autoScript = document.createElement('script');
        autoScript.src = KATEX_AUTO_RENDER_URL;
        autoScript.crossOrigin = 'anonymous';
        autoScript.onload = () => {
          katexLoaded = true;
          resolve(window.katex);
        };
        document.head.appendChild(autoScript);
      } else {
        katexLoaded = true;
        resolve(window.katex);
      }
    });

    return katexLoadingPromise;
  }

  // Preload KaTeX early
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', loadKaTeX);
    } else {
      loadKaTeX();
    }
  }

  // Common Chemical Formulas Lookup
  const COMMON_CHEMICALS = [
    'H2O', 'CO2', 'CO', 'CH4', 'NH3', 'O2', 'N2', 'H2', 'Cl2', 'NaCl',
    'CaCO3', 'H2SO4', 'HCl', 'HNO3', 'NaOH', 'KOH', 'C6H12O6', 'C2H5OH',
    'CH3COOH', 'SO2', 'SO3', 'NO2', 'N2O', 'KMnO4', 'Fe2O3', 'CuSO4',
    'Al2O3', 'MgO', 'CaO', 'Ca(OH)2', 'BaSO4', 'AgNO3', 'NH4Cl', 'NaHCO3',
    'Na2CO3', 'H3PO4', 'ATP', 'ADP', 'DNA', 'RNA', 'Fe2+', 'Fe3+', 'Cu2+',
    'Ca2+', 'Mg2+', 'Na+', 'K+', 'Cl-', 'OH-', 'SO4^2-', 'NO3-', 'CO3^2-',
    'NH4+', 'PO4^3-'
  ];

  /**
   * Transforms raw chemical compound strings into clean HTML subscript notation
   */
  function formatChemicalFormula(chem) {
    let formatted = chem
      .replace(/([A-Z][a-z]?|\))(\d+)/g, '$1<sub>$2</sub>')
      .replace(/\^(\d*[+-])/g, '<sup>$1</sup>')
      .replace(/(\d+)([+-])$/g, '<sup>$1$2</sup>')
      .replace(/([+-])$/g, '<sup>$1</sup>');
    return `<span class="stem-chem-badge" title="Chemical Formula">${formatted}</span>`;
  }

  /**
   * Formats scientific units and exponential notation in plain text
   */
  function formatScientificUnits(text) {
    if (!text) return '';

    // Scientific notation: e.g., 3.00 x 10^8 or 3.00 × 10^8 or 6.022 x 10^23
    text = text.replace(/(\d+(?:\.\d+)?)\s*(?:x|×|\*)\s*10\s*\^\s*(-?\d+)/gi, (m, num, exp) => {
      return `<span class="stem-sci-notation">${num} &times; 10<sup>${exp}</sup></span>`;
    });

    // Spaced scientific notation: e.g. 10^-19 J or 10^8 m/s
    text = text.replace(/\b10\s*\^\s*(-?\d+)\b/g, '10<sup>$1</sup>');

    // Unicode superscripts to HTML superscripts if present
    text = text.replace(/([a-zA-Z\)])([⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+)/g, (m, base, sup) => {
      const charMap = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁺': '+', '⁻': '-' };
      const norm = Array.from(sup).map(c => charMap[c] || c).join('');
      return `${base}<sup>${norm}</sup>`;
    });

    // Common STEM power units: e.g., m/s^2 -> m/s², kg m^-3, mol dm^-3, m s^-1
    text = text.replace(/\b(mol|kg|m|g|s|cm|dm|rad|cd|A|K|N|J|W|Pa|Hz|V|C|T)\s*(?:dm|m|s|kg|cm)?\s*\^\s*(-?\d+)\b/gi, (m) => {
      return m.replace(/\^\s*(-?\d+)/g, '<sup>$1</sup>');
    });

    // Standard metric compound units: e.g., mol dm-3 -> mol dm<sup>-3</sup>
    text = text.replace(/\b(mol\s*dm|kg\s*m|m\s*s|g\s*cm)\s*-\s*(\d+)\b/gi, '$1<sup>-$2</sup>');

    return text;
  }

  /**
   * Pre-processes raw dictionary definition text to beautify chemistry, math symbols, and arrows
   * IMPORTANT: Protects all LaTeX math blocks ($$...$$ and $...$) from plain text regex tampering.
   */
  function preprocessScienceText(text) {
    if (!text) return '';

    // Step 1: Protect LaTeX blocks with unique safe tokens
    const mathTokens = [];
    let tokenizedText = text;

    // First protect display math $$ ... $$
    tokenizedText = tokenizedText.replace(/\$\$([\s\S]+?)\$\$/g, (match) => {
      const id = `___STEM_DISPLAY_MATH_${mathTokens.length}___`;
      mathTokens.push({ id, content: match });
      return id;
    });

    // Then protect inline math $ ... $
    tokenizedText = tokenizedText.replace(/\$([^\$\n]+?)\$/g, (match) => {
      const id = `___STEM_INLINE_MATH_${mathTokens.length}___`;
      mathTokens.push({ id, content: match });
      return id;
    });

    // Step 2: Apply plain-text transformations ONLY to non-math text
    let res = tokenizedText;

    // Normalize arrows in chemical reactions and processes
    res = res.replace(/\s*(?:->|-->|→)\s*/g, ' &rarr; ');
    res = res.replace(/\s*(?:<->|<-->|⇄|⇌)\s*/g, ' &#8652; ');

    // Normalize Greek characters and plain-text superscripts
    res = res.replace(/\b([a-zA-Z0-9_]+)\s*(\^|²|³)\s*(\d+)?/g, (match, base, op, exp) => {
      if (op === '²') return `${base}<sup>2</sup>`;
      if (op === '³') return `${base}<sup>3</sup>`;
      if (op === '^' && exp) return `${base}<sup>${exp}</sup>`;
      return match;
    });

    // Format recognized standalone chemical compounds
    COMMON_CHEMICALS.forEach(chem => {
      const escaped = chem.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
      const regex = new RegExp(`(?<=[\\s(,]|^)${escaped}(?=[\\s).,;:]|$)`, 'g');
      res = res.replace(regex, formatChemicalFormula(chem));
    });

    // Format scientific units & powers
    res = formatScientificUnits(res);

    // Step 3: Restore protected LaTeX math blocks exactly as original
    mathTokens.forEach(t => {
      res = res.replace(t.id, t.content);
    });

    return res;
  }

  /**
   * Copies text to clipboard with feedback
   */
  function copyToClipboard(text, btnElement) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => {
        if (btnElement) {
          const orig = btnElement.innerHTML;
          btnElement.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> Copied!`;
          btnElement.classList.add('copied');
          setTimeout(() => {
            btnElement.innerHTML = orig;
            btnElement.classList.remove('copied');
          }, 1800);
        }
      });
    }
  }

  /**
   * Main Public API: Formats string or renders into DOM container
   */
  function renderScienceText(target, options = {}) {
    if (typeof target === 'string') {
      return preprocessScienceText(target);
    }

    if (!target || !(target instanceof HTMLElement)) {
      return '';
    }

    const rawText = target.getAttribute('data-raw-content') || target.textContent || '';
    if (!target.hasAttribute('data-raw-content')) {
      target.setAttribute('data-raw-content', rawText);
    }

    // Step 1: Preprocess plain-text while protecting LaTeX blocks
    let processedHtml = preprocessScienceText(rawText);
    target.innerHTML = processedHtml;

    // Step 2: Render LaTeX math in element using KaTeX
    function applyKaTeX() {
      if (typeof window.renderMathInElement === 'function') {
        try {
          window.renderMathInElement(target, {
            delimiters: [
              { left: '$$', right: '$$', display: true },
              { left: '$', right: '$', display: false },
              { left: '\\(', right: '\\)', display: false },
              { left: '\\[', right: '\\]', display: true }
            ],
            ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"],
            throwOnError: false
          });

          // Enhance block math with interactive formula cards
          const blockMathElements = target.querySelectorAll('.katex-display');
          blockMathElements.forEach((mathEl) => {
            if (!mathEl.parentElement.classList.contains('stem-formula-card')) {
              const card = document.createElement('div');
              card.className = 'stem-formula-card';
              
              const header = document.createElement('div');
              header.className = 'stem-formula-header';
              header.innerHTML = `
                <span class="stem-formula-badge"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg> Equation</span>
                <button type="button" class="stem-formula-copy-btn" title="Copy Formula">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg> Copy
                </button>
              `;

              const copyBtn = header.querySelector('.stem-formula-copy-btn');
              copyBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                const mathText = mathEl.innerText || '';
                copyToClipboard(mathText.trim(), copyBtn);
              });

              mathEl.parentNode.insertBefore(card, mathEl);
              card.appendChild(header);
              card.appendChild(mathEl);
            }
          });
        } catch (e) {
          console.warn('[FormulaRenderer] Math rendering error:', e);
        }
      }
    }

    if (processedHtml.includes('$')) {
      if (window.renderMathInElement) {
        applyKaTeX();
      } else {
        loadKaTeX().then(() => {
          if (target.isConnected) {
            applyKaTeX();
          }
        });
      }
    }

    return target.innerHTML;
  }

  // Export global helpers
  window.FormulaRenderer = {
    render: renderScienceText,
    format: preprocessScienceText,
    loadKaTeX: loadKaTeX,
    formatChemical: formatChemicalFormula,
    formatUnits: formatScientificUnits
  };

  window.renderScienceText = renderScienceText;
  window.formatScienceText = preprocessScienceText;

})();
