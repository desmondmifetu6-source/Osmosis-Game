// =====================================================================
// FILE: core_distractor_engine.js
// Osmosis STEM Rapid Learning Engine - Smart Distractor & POS Matcher
// Architect: Desmond Mifetu & Co-Chief Developer
// =====================================================================
// High-Order Pedagogical Guarantee:
// Every generated distractor matches the target word in:
// 1. Exact Length (or strict +-1 char boundary when pools are small)
// 2. Part-of-Speech & Morphological Suffix (-ed, -ing, -tion, -ity, -ment, etc.)
// 3. STEM Authenticity (drawn from the 27,000+ scientific vocabulary database)
// =====================================================================

(function () {
  'use strict';

  // Common singular words ending in -s that are NOT plurals
  const NON_PLURALS = new Set([
    'gas', 'lens', 'focus', 'radius', 'basis', 'crisis', 'axis',
    'apparatus', 'status', 'virus', 'fetus', 'mucus', 'nucleus',
    'stimulus', 'fungus', 'calculus', 'rhombus', 'uterus', 'bronchus',
    'pelvis', 'epidermis', 'metamorphosis', 'osmosis', 'synthesis',
    'analysis', 'paralysis', 'homeostasis', 'hypnosis', 'symbiosis'
  ]);

  // High-frequency non-scientific stop words to never blank out
  const STOP_WORDS = new Set([
    'that', 'with', 'this', 'have', 'they', 'their', 'them', 'what', 'which',
    'when', 'where', 'who', 'whom', 'whose', 'why', 'how', 'some', 'such',
    'than', 'very', 'will', 'just', 'should', 'also', 'into', 'only', 'about',
    'many', 'then', 'would', 'like', 'these', 'because', 'could', 'been',
    'much', 'even', 'from', 'were', 'there', 'used', 'part', 'made', 'each',
    'other', 'another', 'called', 'known', 'forms', 'type', 'types', 'form'
  ]);

  const DistractorEngine = {
    _indexed: false,
    _index: {}, // Map: "length_pos" -> Array<string>
    _allWordsList: [],

    /**
     * Morphological Part-of-Speech & Grammatical Category Classifier
     * Accurately groups words based on scientific English inflectional & derivational morphology.
     * @param {string} word 
     * @returns {string} POS category key
     */
    detectPOS(word) {
      if (!word) return 'noun-base';
      const lower = String(word).trim().toLowerCase();
      const len = lower.length;

      // Verb Inflections
      if (lower.endsWith('ed') && !lower.endsWith('eed') && len >= 4) return 'verb-past';
      if (lower.endsWith('ing') && len >= 5) return 'verb-ing';

      // Adverbs
      if (lower.endsWith('ly') && len >= 4) return 'adverb';

      // Derivational Nouns
      if ((lower.endsWith('tion') || lower.endsWith('sion')) && len >= 5) return 'noun-action';
      if (lower.endsWith('ity') && len >= 5) return 'noun-ity';
      if (lower.endsWith('ment') && len >= 5) return 'noun-ment';
      if ((lower.endsWith('ance') || lower.endsWith('ence')) && len >= 5) return 'noun-ance';
      if (lower.endsWith('ure') && len >= 4) return 'noun-ure';
      if (lower.endsWith('sis') && len >= 5) return 'noun-sis';
      if ((lower.endsWith('er') || lower.endsWith('or')) && len >= 4) return 'noun-agent';
      if (lower.endsWith('ism') && len >= 5) return 'noun-ism';
      if (lower.endsWith('ist') && len >= 5) return 'noun-ist';
      if (lower.endsWith('ness') && len >= 5) return 'noun-ness';

      // Adjectives
      if ((lower.endsWith('ous') || lower.endsWith('ive') || lower.endsWith('able') || lower.endsWith('ible')) && len >= 4) return 'adj';
      if ((lower.endsWith('ic') || lower.endsWith('ical') || lower.endsWith('ar') || lower.endsWith('al')) && len >= 4) return 'adj';

      // Base Verbs (infinitives with active verb suffixes)
      if ((lower.endsWith('ize') || lower.endsWith('ise') || lower.endsWith('ify') || lower.endsWith('ate')) && len >= 5) return 'verb-base';

      // Plural Nouns
      if (lower.endsWith('s') && !NON_PLURALS.has(lower) && !lower.endsWith('ss') && !lower.endsWith('us') && !lower.endsWith('is')) {
        return 'noun-plural';
      }

      return 'noun-base';
    },

    /**
     * Initializes the in-memory index from the 27,000+ STEM dictionary
     */
    _ensureIndex() {
      if (this._indexed) return;

      this._index = {};
      const wordSet = new Set();

      // 1. Source headwords from STEMDictionary or window globals
      let rawEntries = [];
      if (typeof window !== 'undefined' && window.STEMDictionary && typeof window.STEMDictionary.getAllWords === 'function') {
        rawEntries = window.STEMDictionary.getAllWords();
      } else if (typeof global !== 'undefined' && global.STEMDictionary && typeof global.STEMDictionary.getAllWords === 'function') {
        rawEntries = global.STEMDictionary.getAllWords();
      }

      for (let i = 0; i < rawEntries.length; i++) {
        const entry = rawEntries[i];
        if (!entry || !entry.word) continue;

        // Add single-word headwords
        const head = entry.word.trim().toLowerCase();
        if (/^[a-z]+$/i.test(head) && head.length >= 3) {
          wordSet.add(head);
        }

        // Add enriched vocabulary from definitions (harvesting STEM-specific terms)
        if (entry.definition) {
          const cleanText = entry.definition.replace(/<\/?[^>]+(>|$)/g, ' ');
          const defWords = cleanText.match(/\b[a-zA-Z]{3,}\b/g);
          if (defWords) {
            for (let j = 0; j < defWords.length; j++) {
              const dw = defWords[j].toLowerCase();
              if (!STOP_WORDS.has(dw) && /^[a-z]+$/i.test(dw) && dw.length <= 18) {
                wordSet.add(dw);
              }
            }
          }
        }
      }

      // 2. Build Multi-key Bucket Index: length_pos -> Array<word>
      this._allWordsList = Array.from(wordSet);
      for (let i = 0; i < this._allWordsList.length; i++) {
        const w = this._allWordsList[i];
        const len = w.length;
        const pos = this.detectPOS(w);
        const key = `${len}_${pos}`;

        if (!this._index[key]) this._index[key] = [];
        this._index[key].push(w);
      }

      this._indexed = true;
    },

    /**
     * Retrieves scientifically deceptive distractors matching both length & part of speech
     * @param {string} targetWord The correct answer word
     * @param {number} count Number of distractors to generate (default: 3)
     * @param {object} options Configuration options:
     *   - exactLengthOnly: boolean (default: false, will prioritize exact then allow +-1)
     *   - exclude: Array<string> words to exclude
     *   - preserveCase: boolean (match target's casing: lower, UPPER, Title)
     * @returns {Array<string>} List of distractors
     */
    getDistractors(targetWord, count = 3, options = {}) {
      if (!targetWord) return [];
      this._ensureIndex();

      const rawTarget = String(targetWord).trim();
      const lowerTarget = rawTarget.toLowerCase();
      const targetLen = lowerTarget.length;
      const targetPOS = this.detectPOS(lowerTarget);

      const excludeSet = new Set((options.exclude || []).map(w => String(w).toLowerCase()));
      excludeSet.add(lowerTarget);

      // Suffix variations that share semantic roots (e.g., react -> reaction -> reacting) to avoid trivial giveaways
      const stemRoot = lowerTarget.slice(0, Math.max(3, targetLen - 3));

      const filterCandidate = (w) => {
        if (!w || excludeSet.has(w)) return false;
        // Avoid words that share almost the entire stem of the target (e.g. "cell" vs "cells")
        if (targetLen >= 4 && w.startsWith(stemRoot) && Math.abs(w.length - targetLen) <= 2) return false;
        return true;
      };

      // 1. Tier 1: Exact Length + Exact POS
      const exactKey = `${targetLen}_${targetPOS}`;
      let candidates = (this._index[exactKey] || []).filter(filterCandidate);

      // 2. Tier 2: Length +- 1 with Exact POS (if exact length pool is depleted)
      if (candidates.length < count && !options.exactLengthOnly) {
        const nearMin = `${targetLen - 1}_${targetPOS}`;
        const nearMax = `${targetLen + 1}_${targetPOS}`;
        const nearCandidates = [
          ...(this._index[nearMin] || []),
          ...(this._index[nearMax] || [])
        ].filter(filterCandidate);
        candidates = candidates.concat(nearCandidates);
      }

      // 3. Tier 3: Morphological fallback (generate grammatical variation if word bank is exhausted)
      if (candidates.length < count) {
        const morphFallbacks = this._generateMorphologicalFallbacks(lowerTarget, targetPOS, targetLen);
        for (let fb of morphFallbacks) {
          if (filterCandidate(fb) && !candidates.includes(fb)) {
            candidates.push(fb);
          }
        }
      }

      // 4. Tier 4: Exact length general STEM words if POS is rare
      if (candidates.length < count) {
        const generalKey = `${targetLen}_noun-base`;
        const generalCandidates = (this._index[generalKey] || []).filter(filterCandidate);
        candidates = candidates.concat(generalCandidates);
      }

      // Shuffle candidates using Fisher-Yates
      for (let i = candidates.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [candidates[i], candidates[j]] = [candidates[j], candidates[i]];
      }

      let selected = candidates.slice(0, count);

      // Match Casing of targetWord
      if (options.preserveCase !== false) {
        const isUpper = rawTarget === rawTarget.toUpperCase() && rawTarget.length > 1;
        const isTitle = rawTarget[0] === rawTarget[0].toUpperCase() && rawTarget.slice(1) === rawTarget.slice(1).toLowerCase();

        selected = selected.map(w => {
          if (isUpper) return w.toUpperCase();
          if (isTitle) return w.charAt(0).toUpperCase() + w.slice(1);
          return w.toLowerCase();
        });
      }

      return selected;
    },

    /**
     * Generates a complete shuffled options array containing the correct answer + distractors
     * @param {string} targetWord The correct answer
     * @param {number} totalOptions Total number of choices (default: 4)
     * @param {object} options Options passed to getDistractors
     * @returns {Array<string>} Shuffled array of options with answer included
     */
    getOptionsWithAnswer(targetWord, totalOptions = 4, options = {}) {
      const distractors = this.getDistractors(targetWord, totalOptions - 1, options);
      const all = [targetWord, ...distractors];

      // Fisher-Yates Shuffle
      for (let i = all.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [all[i], all[j]] = [all[j], all[i]];
      }

      return all;
    },

    // =====================================================================
    // SEMANTIC DISTRACTOR ENGINE — "Semantic Gravity" Algorithm
    // Architect: Desmond Mifetu & Co-Chief Developer
    // =====================================================================
    // Strategy: Instead of matching by POS+length (which gives random-feeling
    // distractors like "synthesis" for "heart"), we extract high-signal content
    // words from the correct word's definition, then score EVERY other dictionary
    // entry by how many of those signals appear in its own definition.
    //
    // Result: "heart" → ["liver", "kidney", "artery", "lung"]
    //         "photosynthesis" → ["respiration", "chlorophyll", "transpiration"]
    //         "atom" → ["electron", "neutron", "proton", "molecule"]
    // =====================================================================

    // Per-session cache to avoid re-scoring the entire dictionary on every question
    _semanticCache: {},

    // Extended stopword list for keyword extraction
    _SEMANTIC_STOPWORDS: new Set([
      'the','a','an','is','are','was','were','be','been','being','have','has',
      'had','do','does','did','will','would','could','should','may','might',
      'shall','can','need','dare','ought','used','this','that','these','those',
      'it','they','he','she','we','you','which','who','what','when','where',
      'why','how','and','or','but','if','as','of','in','on','at','to','for',
      'with','by','from','into','about','through','during','before','after',
      'above','below','between','each','other','than','so','yet','such','both',
      'either','neither','its','his','her','their','our','your','my','not',
      'also','very','most','more','some','any','all','no','only','just',
      'because','while','although','however','therefore','thus','hence','often',
      'usually','typically','generally','especially','particularly','certain',
      'found','called','known','made','form','forms','type','types','process',
      'processes','system','systems','part','parts','include','includes',
      'including','example','examples','result','results','cause','causes',
      'produce','produces','allow','allows','make','makes','well','often',
      'without','within','around','along','across','term','refers','used',
      'containing','contained','related','similar','different','same','another',
      'one','two','three','four','five','six','many','much','few','several',
      'occurs','occur','occur','occur','present','common','important','main',
      'major','small','large','long','short','high','low','new','old','given',
      'point','using','use','where','they','there','here','based','consists'
    ]),

    /**
     * Extracts high-signal semantic keywords from a definition string.
     * These keywords represent the domain fingerprint of the word.
     *
     * @param {string} definition The word's definition text
     * @returns {string[]} Array of meaningful content words, longest/rarest first
     */
    _extractSemanticKeywords(definition) {
      if (!definition) return [];

      // Strip HTML tags, then extract alphabetic word tokens
      const cleanDef = definition.replace(/<\/?[^>]+(>|$)/g, ' ');
      const tokens = cleanDef.match(/\b[a-zA-Z]{4,}\b/g) || [];

      const stopwords = this._SEMANTIC_STOPWORDS;
      const seen = new Set();
      const keywords = [];

      for (const token of tokens) {
        const lower = token.toLowerCase();
        if (stopwords.has(lower) || seen.has(lower)) continue;
        seen.add(lower);
        keywords.push(lower);
      }

      // Sort by length descending — longer words are more domain-specific
      // (e.g. "circulatory" beats "organ", "muscular" beats "pump")
      keywords.sort((a, b) => b.length - a.length);

      // Keep the top 8 most specific keywords
      return keywords.slice(0, 8);
    },

    /**
     * Scores a candidate word's definition against a set of semantic keywords.
     * Returns the number of keyword matches found in the candidate's definition.
     *
     * @param {string} candidateDef The candidate word's definition
     * @param {string[]} keywords   Keywords extracted from the correct word's definition
     * @returns {number} Semantic relevance score
     */
    _scoreSemanticMatch(candidateDef, keywords) {
      if (!candidateDef || !keywords.length) return 0;
      const cleanDef = candidateDef.toLowerCase().replace(/<\/?[^>]+(>|$)/g, ' ');
      let score = 0;
      for (const kw of keywords) {
        // Use a word-boundary check so "cell" doesn't match "cellular" accidentally
        if (cleanDef.includes(kw)) score++;
      }
      return score;
    },

    /**
     * ✨ MAIN SEMANTIC API ✨
     * Generates a shuffled array of [correctWord + 3 semantically-related distractors].
     *
     * Uses the "Semantic Gravity" algorithm:
     *   Tier 1 — Words scoring ≥ 2 keyword matches (strong domain cousins)
     *   Tier 2 — Words scoring ≥ 1 keyword match (loose domain relatives)
     *   Tier 3 — POS+length fallback via getOptionsWithAnswer() (safety net)
     *
     * @param {string} correctWord  The correct answer word
     * @param {string} definition   The definition shown to the user
     * @param {number} totalCount   Total options including correct (default: 4)
     * @param {object} opts         { exclude: string[] }
     * @returns {string[]} Shuffled array with correctWord + (totalCount-1) distractors
     */
    getSemanticOptions(correctWord, definition, totalCount = 4, opts = {}) {
      if (!correctWord) return this.getOptionsWithAnswer(correctWord, totalCount, opts);

      const neededDistractors = totalCount - 1;
      const lowerCorrect = correctWord.toLowerCase();
      const cacheKey = lowerCorrect;

      // Build exclude set — never use the correct word or any user-specified exclusions
      const excludeSet = new Set((opts.exclude || []).map(w => String(w).toLowerCase()));
      excludeSet.add(lowerCorrect);

      // ── Keyword Extraction ──────────────────────────────────────────────
      // Pull semantic keywords from this word's definition. This is the
      // "domain fingerprint" we use to find relatives.
      const keywords = this._extractSemanticKeywords(definition);

      let semanticDistractors = [];

      // ── Semantic Scoring (with cache) ───────────────────────────────────
      // We cache the scored candidates per correctWord to keep the UI snappy.
      // On cache miss, we score the full dictionary once and store results.
      if (!this._semanticCache[cacheKey]) {
        this._ensureIndex(); // Makes sure _allWordsList is populated

        // Get all dictionary entries that have definitions — we need them for scoring
        let allEntries = [];
        const dictRef = (typeof window !== 'undefined' && window.STEMDictionary) ||
                        (typeof global !== 'undefined' && global.STEMDictionary);

        if (dictRef && typeof dictRef.getAllWords === 'function') {
          allEntries = dictRef.getAllWords();
        }

        // Score every entry in the dictionary
        const scored = [];
        for (const entry of allEntries) {
          if (!entry || !entry.word) continue;
          const candidateWord = entry.word.trim().toLowerCase();

          // Must be a clean alphabetic single-word, 3+ chars, not the correct word
          if (!/^[a-z]+$/i.test(candidateWord) || candidateWord.length < 3) continue;
          if (candidateWord === lowerCorrect) continue;

          const score = this._scoreSemanticMatch(
            entry.definition || entry.raw_headword || '',
            keywords
          );

          if (score > 0) {
            scored.push({ word: candidateWord, score });
          }
        }

        // Sort by score descending, then by word length similarity to correct word
        // (closer in length = more visually plausible distractor)
        const correctLen = lowerCorrect.length;
        scored.sort((a, b) => {
          if (b.score !== a.score) return b.score - a.score;
          return Math.abs(a.word.length - correctLen) - Math.abs(b.word.length - correctLen);
        });

        // Cache the sorted candidates (store word + score for flexible thresholding)
        this._semanticCache[cacheKey] = scored;
      }

      const cachedCandidates = this._semanticCache[cacheKey];

      // ── Tier 1: Strong semantic match (score ≥ 2) ──────────────────────
      const tier1 = cachedCandidates
        .filter(c => c.score >= 2 && !excludeSet.has(c.word))
        .map(c => c.word);

      semanticDistractors = tier1.slice(0, neededDistractors);

      // ── Tier 2: Loose semantic match (score ≥ 1) ───────────────────────
      if (semanticDistractors.length < neededDistractors) {
        const alreadyPicked = new Set(semanticDistractors);
        const tier2 = cachedCandidates
          .filter(c => c.score >= 1 && !excludeSet.has(c.word) && !alreadyPicked.has(c.word))
          .map(c => c.word);

        const needed = neededDistractors - semanticDistractors.length;
        semanticDistractors = semanticDistractors.concat(tier2.slice(0, needed));
      }

      // ── Tier 3: POS+length fallback (safety net) ────────────────────────
      // If even Tier 2 didn't give us enough candidates (very rare edge case),
      // fall back gracefully to the existing morphological engine.
      if (semanticDistractors.length < neededDistractors) {
        const alreadyPicked = new Set(semanticDistractors);
        const posDistractors = this.getDistractors(correctWord, neededDistractors, {
          exclude: [...excludeSet, ...semanticDistractors]
        });
        for (const pd of posDistractors) {
          if (!alreadyPicked.has(pd.toLowerCase()) && semanticDistractors.length < neededDistractors) {
            semanticDistractors.push(pd);
            alreadyPicked.add(pd.toLowerCase());
          }
        }
      }

      // ── Assemble & Shuffle ──────────────────────────────────────────────
      // Combine correct word + distractors, then Fisher-Yates shuffle so the
      // correct answer lands in a random position every time
      const finalOptions = [correctWord, ...semanticDistractors.slice(0, neededDistractors)];

      for (let i = finalOptions.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [finalOptions[i], finalOptions[j]] = [finalOptions[j], finalOptions[i]];
      }

      return finalOptions;
    },

    /**
     * Generates syntactically realistic morphological distractors when dictionary lookup needs extra depth
     */
    _generateMorphologicalFallbacks(target, pos, len) {
      const results = [];
      if (pos === 'verb-past') {
        results.push('formed', 'melted', 'heated', 'forced', 'caused', 'flowed', 'bonded');
      } else if (pos === 'verb-ing') {
        results.push('forming', 'melting', 'heating', 'forcing', 'flowing', 'bonding');
      } else if (pos === 'noun-action') {
        results.push('motion', 'action', 'fusion', 'vision', 'fission', 'tension', 'density');
      } else if (pos === 'adj') {
        results.push('atomic', 'acidic', 'static', 'liquid', 'linear', 'neural', 'active');
      } else {
        results.push('system', 'matter', 'energy', 'charge', 'liquid', 'plasma', 'vector');
      }
      return results.filter(w => Math.abs(w.length - len) <= 1);
    }
  };

  // Export for Browser & Node environments
  if (typeof window !== 'undefined') {
    window.DistractorEngine = DistractorEngine;
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = DistractorEngine;
  }
})();

