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

  // 5. Inspection Modal Handler
  let currentActiveItem = null;

  function openInspectionModal(item) {
    currentActiveItem = item;
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');

    modalTitle.textContent = item.primaryTerm.toUpperCase();
    modalImg.src = item.image;
    modalImg.alt = item.primaryTerm;

    // Fetch definition from STEMDictionary
    let defText = "A curriculum-endorsed scientific schematic illustrating key concepts, structures, and systems in STEM.";
    if (typeof window.STEMDictionary !== 'undefined' && typeof window.STEMDictionary.getEntry === 'function') {
      const entry = window.STEMDictionary.getEntry(item.primaryTerm);
      if (entry && entry.definition) {
        defText = entry.definition;
      }
    }

    modalDef.textContent = defText;
    if (typeof window.renderScienceText === 'function') {
      window.renderScienceText(modalDef);
    }

    modalOverlay.classList.add('active');
  }

  function closeModal() {
    modalOverlay.classList.remove('active');
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
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(currentActiveItem.primaryTerm);
      u.rate = 0.9;
      window.speechSynthesis.speak(u);
    }
  });

  readDefBtn.addEventListener('click', () => {
    if (!modalDef) return;
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const textToRead = `${currentActiveItem ? currentActiveItem.primaryTerm : ''}. ${modalDef.innerText || modalDef.textContent}`;
      const u = new SpeechSynthesisUtterance(textToRead);
      u.rate = 0.95;
      window.speechSynthesis.speak(u);
    }
  });

  // Initial render
  applyFilters();
});
