// =====================================================================
// FILE: module_diagram_hub.js (Comprehensive Diagram Laboratory)
// =====================================================================

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('diagram-search-input');
  const letterBar = document.getElementById('letter-bar');
  const countIndicator = document.getElementById('count-indicator');
  const diagramGrid = document.getElementById('diagram-grid');
  const loadMoreBtn = document.getElementById('load-more-btn');
  const goHomeBtn = document.getElementById('go-home-btn');

  // Modal elements
  const modalOverlay = document.getElementById('diag-modal-overlay');
  const modalTitle = document.getElementById('diag-modal-title');
  const modalImg = document.getElementById('diag-modal-img');
  const modalDef = document.getElementById('diag-modal-def');
  const modalClose = document.getElementById('diag-modal-close');
  const pronounceBtn = document.getElementById('diag-pronounce-btn');
  const pauseBtn = document.getElementById('diag-pause-btn');
  const readDefBtn = document.getElementById('diag-read-def-btn');

  if (goHomeBtn) {
    goHomeBtn.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      window.location.href = '01_home_menu.html';
    });
  }

  // 1. Build Unique Diagram List from DictionaryDiagrams
  const rawMap = (typeof DictionaryDiagrams !== 'undefined') ? DictionaryDiagrams : {};
  const uniqueItemsMap = new Map();

  for (const [term, path] of Object.entries(rawMap)) {
    const normPath = path.startsWith('diagrams/') ? path : 'diagrams/' + path;
    if (!uniqueItemsMap.has(normPath)) {
      uniqueItemsMap.set(normPath, {
        primaryTerm: term,
        terms: [term],
        image: normPath
      });
    } else {
      uniqueItemsMap.get(normPath).terms.push(term);
    }
  }

  const allDiagrams = Array.from(uniqueItemsMap.values());
  // Sort alphabetically by primary term
  allDiagrams.sort((a, b) => a.primaryTerm.localeCompare(b.primaryTerm));

  let filteredDiagrams = [...allDiagrams];
  let currentRenderCount = 0;
  const PAGE_SIZE = 36;
  let activeLetter = 'ALL';

  // 2. Build Letter Filter Bar
  const letters = ['ALL', ...'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')];
  letterBar.innerHTML = '';

  letters.forEach(letter => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = `letter-pill ${letter === 'ALL' ? 'active' : ''}`;
    btn.textContent = letter;
    btn.addEventListener('click', () => {
      if (typeof AudioManager !== 'undefined') AudioManager.play('click');
      document.querySelectorAll('.letter-pill').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      activeLetter = letter;
      searchInput.value = '';
      applyFilters();
    });
    letterBar.appendChild(btn);
  });

  // 3. Filter and Search Engine
  function applyFilters() {
    const query = searchInput.value.trim().toLowerCase();

    filteredDiagrams = allDiagrams.filter(item => {
      const matchesLetter = (activeLetter === 'ALL') || 
        item.primaryTerm.toUpperCase().startsWith(activeLetter) ||
        item.terms.some(t => t.toUpperCase().startsWith(activeLetter));

      if (!matchesLetter) return false;

      if (!query) return true;

      return item.primaryTerm.toLowerCase().includes(query) ||
        item.terms.some(t => t.toLowerCase().includes(query));
    });

    currentRenderCount = 0;
    diagramGrid.innerHTML = '';
    renderNextBatch();
  }

  let searchDebounce = null;
  searchInput.addEventListener('input', () => {
    clearTimeout(searchDebounce);
    searchDebounce = setTimeout(() => {
      // Reset letter to ALL when typing a search query
      if (searchInput.value.trim().length > 0 && activeLetter !== 'ALL') {
        activeLetter = 'ALL';
        document.querySelectorAll('.letter-pill').forEach(p => {
          p.classList.toggle('active', p.textContent === 'ALL');
        });
      }
      applyFilters();
    }, 200);
  });

  // 4. Render Batch of Diagram Cards
  function renderNextBatch() {
    const nextSlice = filteredDiagrams.slice(currentRenderCount, currentRenderCount + PAGE_SIZE);
    
    nextSlice.forEach(item => {
      const card = document.createElement('div');
      card.className = 'diagram-card';

      const cleanTitle = item.primaryTerm.replace(/^[0-9]+,\s*/, '');
      const secondaryCount = item.terms.length > 1 ? `+${item.terms.length - 1} terms` : 'Curriculum Schematic';

      card.innerHTML = `
        <div class="diagram-thumb-wrap">
          <img src="${item.image}" alt="${item.primaryTerm}" class="diagram-thumb" loading="lazy" onerror="this.src='assets/stem_dictionary_cover.png'">
        </div>
        <div class="diagram-info">
          <div class="diagram-title">${cleanTitle}</div>
          <div class="diagram-meta">
            <span>🔬 Diagram</span>
            <span class="badge">${secondaryCount}</span>
          </div>
        </div>
      `;

      card.addEventListener('click', () => {
        openInspectionModal(item);
      });

      diagramGrid.appendChild(card);
    });

    currentRenderCount += nextSlice.length;

    // Update count indicator
    countIndicator.textContent = `Showing ${Math.min(currentRenderCount, filteredDiagrams.length)} of ${filteredDiagrams.length} Diagrams (Total: ${allDiagrams.length})`;

    // Toggle Load More button
    if (currentRenderCount < filteredDiagrams.length) {
      loadMoreBtn.style.display = 'block';
    } else {
      loadMoreBtn.style.display = 'none';
    }
  }

  loadMoreBtn.addEventListener('click', () => {
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');
    renderNextBatch();
  });

  // 5. Inspection Modal Handler & Smart Definition Resolver
  let currentActiveItem = null;

  function resolveDiagramDefinition(item) {
    if (typeof window.STEMDictionary === 'undefined') {
      return `Scientific schematic illustrating the structural details, properties, and core components of ${item.primaryTerm}.`;
    }

    const candidateTerms = [];
    if (item.primaryTerm) candidateTerms.push(item.primaryTerm);
    if (Array.isArray(item.terms)) {
      item.terms.forEach(t => { if (!candidateTerms.includes(t)) candidateTerms.push(t); });
    }
    if (item.image) {
      const filename = item.image.split('/').pop().replace(/\.[^/.]+$/, '').replace(/[_-]/g, ' ');
      if (filename && !candidateTerms.includes(filename)) candidateTerms.push(filename);
    }

    const allWords = (typeof window.STEMDictionary.getAllWords === 'function')
      ? window.STEMDictionary.getAllWords()
      : [];

    function findEntry(query) {
      if (!query) return null;
      const q = query.trim().toLowerCase();
      if (!q) return null;

      // 1. Direct getEntry
      let e = window.STEMDictionary.getEntry(q);
      if (e && e.definition) return e;

      // 2. Clean numeric/chemical prefixes (e.g. "1-butene" -> "butene", "2,4,6-trinitrophenol" -> "trinitrophenol" / "picric acid")
      const cleaned = q.replace(/^(\d+([,\-]\d+)*\-?|[a-z]\-|\([a-z0-9,\-]+\)\-?)/i, '').trim();
      if (cleaned && cleaned !== q) {
        e = window.STEMDictionary.getEntry(cleaned);
        if (e && e.definition) return e;
      }

      // 3. Strip parenthetical content (e.g. "quartz (mineral)" -> "quartz")
      const noParens = q.replace(/\(.*?\)/g, '').trim();
      if (noParens && noParens !== q) {
        e = window.STEMDictionary.getEntry(noParens);
        if (e && e.definition) return e;
      }

      // 4. Singularize (e.g. "canines" -> "canine", "leaves" -> "leaf")
      if (q.endsWith('s') && q.length > 3) {
        const sing = q.endsWith('es') ? q.slice(0, -2) : q.slice(0, -1);
        e = window.STEMDictionary.getEntry(sing);
        if (e && e.definition) return e;
      }

      // 5. Exact match in allWords array by word or raw_headword
      const exact = allWords.find(item => {
        const w = (item.word || '').toLowerCase();
        const r = (item.raw_headword || item.raw || '').toLowerCase();
        return w === q || r === q || w === cleaned || w === noParens;
      });
      if (exact && exact.definition) return exact;

      // 6. Check synonyms and headwords
      const inSyn = allWords.find(item => {
        if (item.synonyms && item.synonyms.some(s => s.toLowerCase() === q || s.toLowerCase() === cleaned)) {
          return true;
        }
        const r = (item.raw_headword || item.raw || '').toLowerCase();
        return r.includes(`(${q})`) || r.startsWith(`${q} `) || r.includes(`; ${q}`);
      });
      if (inSyn && inSyn.definition) return inSyn;

      // 7. Sub-phrase matching for compound terms (e.g. "cashew nut" -> "cashew", "awn of a spikelet" -> "awn")
      const tokens = q.split(/[\s\-]+/).filter(t => t.length >= 3 && !['and','the','for','with','from','into','type'].includes(t));
      for (const t of tokens) {
        e = window.STEMDictionary.getEntry(t);
        if (e && e.definition) return e;
        if (t.endsWith('s') && t.length > 3) {
          const tSing = t.endsWith('es') ? t.slice(0, -2) : t.slice(0, -1);
          e = window.STEMDictionary.getEntry(tSing);
          if (e && e.definition) return e;
        }
      }

      return null;
    }

    // Try finding definition across all candidates
    for (const term of candidateTerms) {
      const match = findEntry(term);
      if (match && match.definition && match.definition.trim()) {
        return match.definition;
      }
    }

    return `Scientific schematic illustrating the structural details, properties, and core components of ${item.primaryTerm} in the national STEM curriculum.`;
  }

  function openInspectionModal(item) {
    currentActiveItem = item;
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');

    modalTitle.textContent = item.primaryTerm.toUpperCase();
    modalImg.src = item.image;
    modalImg.alt = item.primaryTerm;

    // Fetch authentic definition using our multi-tier resolver
    const defText = resolveDiagramDefinition(item);

    modalDef.textContent = defText;
    if (typeof window.renderScienceText === 'function') {
      modalDef.removeAttribute('data-raw-content');
      modalDef.setAttribute('data-raw-content', defText);
      window.renderScienceText(modalDef);
    }

    modalOverlay.classList.add('active');
  }

  function closeModal() {
    modalOverlay.classList.remove('active');
    if (pauseBtn) pauseBtn.innerHTML = '⏸️ Pause';
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  }

  modalClose.addEventListener('click', closeModal);
  modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
      closeModal();
    }
  });

  // Audio actions inside Modal
  pronounceBtn.addEventListener('click', () => {
    if (!currentActiveItem) return;
    if (pauseBtn) pauseBtn.innerHTML = '⏸️ Pause';
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(currentActiveItem.primaryTerm);
      u.rate = 0.9;
      u.onend = () => { if (pauseBtn) pauseBtn.innerHTML = '⏸️ Pause'; };
      window.speechSynthesis.speak(u);
    }
  });

  if (pauseBtn) {
    pauseBtn.addEventListener('click', () => {
      if ('speechSynthesis' in window) {
        if (window.speechSynthesis.paused) {
          window.speechSynthesis.resume();
          pauseBtn.innerHTML = '⏸️ Pause';
        } else if (window.speechSynthesis.speaking) {
          window.speechSynthesis.pause();
          pauseBtn.innerHTML = '▶️ Resume';
        }
      }
    });
  }

  readDefBtn.addEventListener('click', () => {
    if (!modalDef) return;
    if (pauseBtn) pauseBtn.innerHTML = '⏸️ Pause';
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const textToRead = `${currentActiveItem ? currentActiveItem.primaryTerm : ''}. ${modalDef.innerText || modalDef.textContent}`;
      const u = new SpeechSynthesisUtterance(textToRead);
      u.rate = 0.95;
      u.onend = () => { if (pauseBtn) pauseBtn.innerHTML = '⏸️ Pause'; };
      window.speechSynthesis.speak(u);
    }
  });

  // Initial render
  applyFilters();
});
