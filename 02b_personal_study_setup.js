// =====================================================================
// FILE: 02b_personal_study_setup.js
// Personal Study — uses the exact same STEMDictionary.predictWords()
// autocomplete engine as the Dictionary Library, now with interactive
// diagram preview and full modal display with back navigation.
// =====================================================================

document.addEventListener('DOMContentLoaded', function () {

  // 1. Security check
  var gameData = sharedState.load();
  if (!gameData.username) {
    window.location.href = 'index.html';
    return;
  }

  var MAX_WORDS = 5;
  var selectedWords = [];   // array of { word, definition }

  // DOM refs
  var input       = document.getElementById('ps-search-input');
  var dropdown    = document.getElementById('ps-autocomplete-dropdown');
  var chipsEl     = document.getElementById('ps-chips');
  var emptyHint   = document.getElementById('ps-empty-hint');
  var counterEl   = document.getElementById('ps-counter');
  var beginBtn    = document.getElementById('ps-begin-btn');
  var backBtn     = document.getElementById('ps-back-btn');

  // Modal DOM refs
  var modalEl     = document.getElementById('ps-diagram-modal');
  var modalWordEl = document.getElementById('ps-modal-word');
  var modalImgEl  = document.getElementById('ps-modal-img');
  var modalDefEl  = document.getElementById('ps-modal-def');
  var modalBackBtn= document.getElementById('ps-modal-back-btn');

  function navigate(url) {
    if (typeof window.navigateWithTransition === 'function') navigateWithTransition(url);
    else window.location.href = url;
  }

  // ── Diagram Lookup Helper ──────────────────────────────────────────
  function getWordDiagram(word, raw) {
    if (typeof window.DictionaryDiagrams === 'undefined' || !word) return null;
    var wKey = word.toLowerCase().trim();
    var rawKey = (raw || '').toLowerCase().trim();
    var baseWordKey = wKey.replace(/\(.*?\)/g, '').trim();

    return window.DictionaryDiagrams[wKey] ||
           (rawKey && window.DictionaryDiagrams[rawKey]) ||
           window.DictionaryDiagrams[baseWordKey] ||
           null;
  }

  // ── Diagram Modal Display ──────────────────────────────────────────
  var currentModalWord = '';
  var currentModalDef = '';
  var modalPronounceBtn = document.getElementById('ps-modal-pronounce-btn');
  var modalReadDefBtn = document.getElementById('ps-modal-read-def-btn');

  function showDiagram(word, diagramSrc, definition) {
    if (!modalEl) return;
    currentModalWord = word || '';
    currentModalDef = definition || '';
    if (modalWordEl) modalWordEl.textContent = (word || 'DEFINITION').toUpperCase();

    var subtitleEl = modalEl.querySelector('.ps-diagram-subtitle');
    var imgWrapperEl = modalEl.querySelector('.ps-diagram-img-wrapper');

    if (diagramSrc) {
      if (modalImgEl) {
        modalImgEl.src = diagramSrc;
        modalImgEl.alt = (word || 'STEM') + ' diagram';
      }
      if (imgWrapperEl) imgWrapperEl.style.display = 'flex';
      if (subtitleEl) subtitleEl.textContent = 'Osmosis STEM Diagram & Definition';
    } else {
      if (modalImgEl) modalImgEl.removeAttribute('src');
      if (imgWrapperEl) imgWrapperEl.style.display = 'none';
      if (subtitleEl) subtitleEl.textContent = 'Osmosis STEM Dictionary Definition';
    }

    if (modalDefEl) {
      modalDefEl.textContent = definition || 'Scientific definition from the 6-In-1 STEM Dictionary.';
    }
    modalEl.classList.add('active');
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');
  }

  function closeDiagramModal() {
    if (!modalEl) return;
    if (typeof VoiceManager !== 'undefined') VoiceManager.stop();
    modalEl.classList.remove('active');
    if (modalImgEl) modalImgEl.removeAttribute('src');
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');
  }

  if (modalPronounceBtn) {
    modalPronounceBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (currentModalWord && typeof VoiceManager !== 'undefined') {
        VoiceManager.speak(currentModalWord, { force: true });
      }
    });
  }

  if (modalReadDefBtn) {
    modalReadDefBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (currentModalDef && typeof VoiceManager !== 'undefined') {
        VoiceManager.speak(currentModalDef, { force: true, rate: 0.95 });
      }
    });
  }

  if (modalBackBtn) {
    modalBackBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      closeDiagramModal();
    });
  }

  if (modalEl) {
    modalEl.addEventListener('click', function (e) {
      if (e.target === modalEl) {
        closeDiagramModal();
      }
    });
  }

  // ── Autocomplete (identical logic to module_library.html) ──────────

  var debounceTimer = null;

  function renderDropdown(predictions) {
    dropdown.innerHTML = '';
    if (!predictions || predictions.length === 0) {
      dropdown.style.display = 'none';
      return;
    }
    dropdown.style.display = 'block';

    predictions.forEach(function (p) {
      var item = document.createElement('div');
      item.className = 'ps-ac-item';

      var displayWord = (p.display || p.word).toUpperCase();
      var snippet = p.definition.length > 80
        ? p.definition.substring(0, 80) + '...'
        : p.definition;

      var diagSrc = getWordDiagram(p.word, p.raw || p.display);

      var actionBtnHtml = diagSrc
        ? '<button type="button" class="ps-diagram-btn" title="View diagram schematic & definition">🖼️ Diagram ▾</button>'
        : '<button type="button" class="ps-def-btn" title="View definition">📖 Meaning ▾</button>';

      var headerHtml = '<div class="ps-ac-header">' +
        '<div style="display: flex; align-items: center; gap: 6px;">' +
        '<span class="ac-word">' + displayWord + '</span>' +
        '<button type="button" class="ps-pronounce-mini-btn" title="Pronounce word">🔊</button>' +
        '</div>' +
        actionBtnHtml +
        '</div>';

      item.innerHTML =
        headerHtml +
        '<div class="ac-snippet">' + snippet + '</div>';

      // Wire pronounce button
      var voiceBtn = item.querySelector('.ps-pronounce-mini-btn');
      if (voiceBtn) {
        voiceBtn.addEventListener('click', function (e) {
          e.stopPropagation(); // Do not add word when clicking voice button
          if (typeof VoiceManager !== 'undefined') {
            VoiceManager.speak(p.word, { force: true });
          }
        });
      }

      // Wire view detail (diagram or definition) button
      var viewDetailBtn = item.querySelector('.ps-diagram-btn, .ps-def-btn');
      if (viewDetailBtn) {
        viewDetailBtn.addEventListener('click', function (e) {
          e.stopPropagation(); // Do not add word when clicking details button
          showDiagram(p.word, diagSrc, p.definition);
        });
      }

      item.addEventListener('click', function () {
        dropdown.style.display = 'none';
        input.value = '';
        // Add the word to the deck
        addWord(p.word, p.definition);
      });

      dropdown.appendChild(item);
    });
  }

  input.addEventListener('input', function (e) {
    clearTimeout(debounceTimer);
    var query = e.target.value.trim();
    if (query.length < 2) {
      dropdown.style.display = 'none';
      return;
    }
    debounceTimer = setTimeout(function () {
      if (typeof STEMDictionary === 'undefined') return;
      var preds = STEMDictionary.predictWords(query, 8);
      renderDropdown(preds);
    }, 120);
  });

  document.addEventListener('click', function (e) {
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.style.display = 'none';
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (modalEl && modalEl.classList.contains('active')) {
        closeDiagramModal();
      } else {
        dropdown.style.display = 'none';
      }
    }
  });

  // ── Deck management ────────────────────────────────────────────────

  function addWord(word, definition) {
    // Already selected?
    if (selectedWords.some(function (w) { return w.word.toLowerCase() === word.toLowerCase(); })) {
      return;
    }
    // Full deck?
    if (selectedWords.length >= MAX_WORDS) {
      if (typeof showModal === 'function') {
        showModal('Deck Full', 'You have already selected 5 words. Remove a word first to add another.');
      } else {
        alert('Maximum 5 words reached. Remove a word first.');
      }
      return;
    }
    selectedWords.push({ word: word, definition: definition || '' });
    if (typeof AudioManager !== 'undefined') AudioManager.play('success');
    renderDeck();
  }

  function removeWord(word) {
    selectedWords = selectedWords.filter(function (w) {
      return w.word.toLowerCase() !== word.toLowerCase();
    });
    if (typeof AudioManager !== 'undefined') AudioManager.play('click');
    renderDeck();
  }

  function renderDeck() {
    var count = selectedWords.length;

    // Counter badge
    counterEl.textContent = count + ' / ' + MAX_WORDS;
    if (count >= MAX_WORDS) {
      counterEl.classList.add('full');
    } else {
      counterEl.classList.remove('full');
    }

    // Begin button
    beginBtn.disabled = count === 0;

    // Chips
    if (count === 0) {
      chipsEl.innerHTML = '';
      chipsEl.appendChild(emptyHint);
      emptyHint.style.display = 'block';
    } else {
      chipsEl.innerHTML = '';
      selectedWords.forEach(function (item) {
        var chip = document.createElement('div');
        chip.className = 'ps-chip';

        var diagSrc = getWordDiagram(item.word);
        var chipActionBtn = diagSrc
          ? '<button type="button" class="ps-chip-diagram-btn" title="View diagram schematic & definition">🖼️ ▾</button>'
          : '<button type="button" class="ps-chip-def-btn" title="View definition">📖 ▾</button>';

        chip.innerHTML =
          '<span>' + sharedState.escapeHTML(item.word) + '</span>' +
          chipActionBtn +
          '<button type="button" class="ps-chip-remove" title="Remove">✕</button>';

        var chipViewBtn = chip.querySelector('.ps-chip-diagram-btn, .ps-chip-def-btn');
        if (chipViewBtn) {
          chipViewBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            showDiagram(item.word, diagSrc, item.definition);
          });
        }

        chip.querySelector('.ps-chip-remove').addEventListener('click', function (e) {
          e.stopPropagation();
          removeWord(item.word);
        });
        chipsEl.appendChild(chip);
      });
    }
  }

  // ── Launch game ────────────────────────────────────────────────────

  beginBtn.addEventListener('click', function () {
    if (selectedWords.length === 0) return;

    var session = sharedState.load();
    session.selectedWords = selectedWords.map(function (w) { return w.word; });
    session.meanings = {};
    selectedWords.forEach(function (w) {
      session.meanings[w.word] = w.definition;
    });
    session.personalStudyMode = true;
    session.score = 0;
    session.usedLetters = [];
    session.letters = [];
    session.stageScores = {};
    sharedState.save(session);

    if (typeof AudioManager !== 'undefined') AudioManager.play('success');
    navigate('04_stage2_word_fillin.html');
  });

  // ── Back button ────────────────────────────────────────────────────

  backBtn.addEventListener('click', function () {
    navigate('01_home_menu.html');
  });

});
