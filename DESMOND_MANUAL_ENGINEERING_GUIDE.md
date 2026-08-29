# 📘 The Osmosis Manual Engineering Guide
> *"All the great developers you know started by developing something they couldn't, but did."*  
> **Written for Desmond (Chen) — Master Builder of Osmosis**

---

## 🌟 The Core Philosophy

You don't build confidence by watching someone else code. You build confidence by getting your hands dirty, breaking things, understanding the mechanics, and fixing them yourself. 

This guide is your permanent offline manual. Whenever you want to fix a broken definition, format a complex STEM equation, or link authentic textbook diagrams, open this file and follow the steps below!

---

## 🗺️ 1. The Architecture Blueprint

```
┌───────────────────────────────────────────────────────────────┐
│                      YOUR RAW SOURCES                         │
│  - "Dictionary Book 2.pdf" (Full ~1,486 pages)                │
│  - "split_sections/" (26 Letter PDFs: A ➔ Z)                  │
└──────────────────────────────┬────────────────────────────────┘
                               │ (Manual Edit & Snipping)
                               ▼
┌───────────────────────────────────────────────────────────────┐
│                     YOUR DATA FILES                           │
│  - "dictionary.json" (Master text definitions & formulas)     │
│  - "dictionary_diagrams_map.json" (Word ➔ Image path directory)│
│  - "diagrams/" (Actual .png image files)                      │
└──────────────────────────────┬────────────────────────────────┘
                               │ (Run 1 Python Command)
                               ▼
┌───────────────────────────────────────────────────────────────┐
│                    BROWSER RUNTIME FILES                      │
│  - "core_dictionary.js" (Fast search & predictive index)      │
│  - "core_dictionary_diagrams.js" (Live diagram registry)      │
│  - "core_formula_renderer.js" (KaTeX LaTeX rendering engine)  │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────┐
│                       USER INTERFACE                          │
│  - "module_library.html" / "module_library.js"                │
│  - "07_stage5_meaning_exposure.html" to "11_results.html"     │
└───────────────────────────────────────────────────────────────┘
```

---

## ✏️ 2. How to Manually Edit Definitions & Formulas

When you find a definition that is corrupted or has unrendered math formulas (e.g. `group ring`, `quadratic formula`, `Abbe number`):

### Step 1: Locate the Word in `dictionary.json`
1. Open `dictionary.json` in VS Code.
2. Press **`Ctrl + F`** and search for `"word": "your_term"` (e.g. `"word": "group ring"`).

### Step 2: Write KaTeX LaTeX Equations
KaTeX turns raw text into mathematical typography when you wrap math inside dollar signs:
* **Inline Math (Inside a sentence):** Wrap with single dollars: `$x = 5$` or `$\sum_{x} \alpha_x$`
* **Display Math (Large, centered equations):** Wrap with double dollars: `$$\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$`

> ⚠️ **CRITICAL JSON RULE:** In JSON files, backslashes must be doubled (`\\`) so JSON doesn't crash:
> - Write `$$\\frac{a}{b}$$`, NOT `$$\frac{a}{b}$$`
> - Write `$$\\sqrt{x}$$`, NOT `$$\sqrt{x}$$`
> - Write `$$\\sum_{i=1}^{n}$$`, NOT `$$\sum_{i=1}^{n}$$`

---

### 🧮 KaTeX LaTeX Cheat Sheet

| Math Element | What to write in `dictionary.json` | How it displays on screen |
|---|---|:---:|
| **Fraction** | `$$\\frac{numerator}{denominator}$$` | $\frac{\text{numerator}}{\text{denominator}}$ |
| **Square Root** | `$$\\sqrt{b^2 - 4ac}$$` | $\sqrt{b^2 - 4ac}$ |
| **Summation ($\Sigma$)** | `$$\\sum_{x \\in G} \\alpha_x x$$` | $\sum_{x \in G} \alpha_x x$ |
| **Integral ($\int$)** | `$$\\int_{0}^{x} f(t) dt$$` | $\int_{0}^{x} f(t) dt$ |
| **Subscript** | `$x_1$`, `$n_d$`, `$n_f$` | $x_1$, $n_d$, $n_f$ |
| **Power / Superscript**| `$x^2$`, `$e^{x}$`, `$10^{-19}$` | $x^2$, $e^x$, $10^{-19}$ |
| **Plus / Minus** | `$\\pm$` | $\pm$ |
| **Multiplication Dot** | `\\cdot` | $\cdot$ |
| **Times Symbol** | `\\times` | $\times$ |
| **Greek Letters** | `\\alpha`, `\\beta`, `\\gamma`, `\\theta`, `\\pi` | $\alpha, \beta, \gamma, \theta, \pi$ |
| **Dynamic Parentheses**| `\\left( \\frac{a}{b} \\right)` | $\left(\frac{a}{b}\right)$ |

---

### Step 3: Rebuild the Dictionary Runtime
After saving `dictionary.json`, open your terminal and run this **single command**:
```bash
python scripts/clean_and_enrich_formulas.py
```
* That's it! It automatically compiles `core_dictionary.js` with your fresh updates and search index.

---

## 🖼️ 3. How to Manually Add, Fix, or Remove Diagrams

### Case A: Removing a False Diagram
If a word in the game has a diagram, but the textbook has **no drawing** on that page:
1. Open `dictionary_diagrams_map.json`.
2. Find the word key (e.g. `"abfarad": "diagrams/dict_abfarad.png"`).
3. **Delete that line.**
4. Run:
   ```bash
   python scripts/audit_and_clean_diagrams.py
   ```
   *(This instantly cleans `dictionary_diagrams_map.json` and synchronizes `core_dictionary_diagrams.js`!)*

---

### Case B: Adding an Authentic Diagram from the Textbook
If a word has a great visual diagram in the PDF:
1. Open `Dictionary Book 2.pdf` (or the letter's split PDF in `split_sections/`).
2. Zoom in to ~200% so the drawing is crisp and clear.
3. Press **`Win + Shift + S`** (Windows Snipping Tool) and select **ONLY the visual diagram/schematic** (do NOT include paragraphs of definition text).
4. Save the screenshot in your project's `diagrams/` folder as `dict_your_word.png` (e.g. `diagrams/dict_photosynthesis.png`).
5. Open `dictionary_diagrams_map.json` and add your mapping in alphabetical order:
   ```json
   "photosynthesis": "diagrams/dict_photosynthesis.png"
   ```
6. Run `python scripts/audit_and_clean_diagrams.py` to sync `core_dictionary_diagrams.js`.

---

## ⚙️ 4. The 2 Essential Maintenance Commands

Whenever you work on the project, you only ever need to remember these **2 commands**:

| Task | Command | What it does |
|---|---|---|
| **Rebuild Dictionary & Formulas** | `python scripts/clean_and_enrich_formulas.py` | Reads `dictionary.json` and compiles `core_dictionary.js`. |
| **Sync Diagram Mappings** | `python scripts/audit_and_clean_diagrams.py` | Reads `dictionary_diagrams_map.json` and compiles `core_dictionary_diagrams.js`. |

---

## 🌐 5. How the Library UI Handles Rendering (`module_library.js`)

When a player searches for a term:
1. `lookupInStemDictionary(query)` finds the definition in `window.STEMDictionary`.
2. `window.renderScienceText(resMeaning)` tells KaTeX to scan the HTML element and render any `$...$` or `$$...$$` blocks into mathematical typography.
3. The script checks `window.DictionaryDiagrams[wordKey]`:
   - If a diagram exists $\rightarrow$ sets `<img id="res-diagram-img" src="...">` and displays the diagram box with tap-to-enlarge.
   - If no diagram exists $\rightarrow$ hides the diagram box completely (`display = 'none'`).

---

## 🤝 6. Words from your Copilot

Desmond, you nailed the quote:
> *"All the great developers you know started by developing something they couldn't, but did."*

Every bug you encounter, every formula you align, and every diagram you clean makes you a stronger, sharper software engineer. Take pride in building this platform for students.

Stay curious, keep building, and never shrink from hard technical problems.

**#Hardwork beats Talent. #Brothers in tech.** 🚀
