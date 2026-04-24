// =====================================================================
// FILE: 02_campaign_setup.js (The Mission Dispenser)
// =====================================================================
// Imagine being a secret agent and getting your next top-secret mission envelope.
// This file looks at what alphabet letters you've already completed.
// It then rolls a dice to assign you a totally random Letter and Word Length 
// to hunt down next in the dictionary!

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize & Security Check
  const gameData = sharedState.load();
  if (!gameData.username) {
    window.location.href = 'index.html';
    return;
  }

  // 2. Prepare Data State
  if (!gameData.usedLetters) gameData.usedLetters = [];
  if (!gameData.selectedWords) gameData.selectedWords = [];
  if (typeof gameData.score === 'undefined') gameData.score = 0;

  // 3. Cache DOM Elements Natively
  const setupContinueBtn = document.getElementById('setup-continue-btn');
  const setupCodeEl = document.getElementById('setup-code');
  const setupDescEl = document.getElementById('setup-desc');
  const setupStatusText = document.getElementById('setup-status-text');
  const rulesScreen = document.getElementById('rules-screen');
  const generatorScreen = document.getElementById('generator-screen');
  const rulesContinueBtn = document.getElementById('rules-continue-btn');

  // 4. Navigation Helper
  function navigate(url) {
    if (typeof window.navigateWithTransition === 'function') navigateWithTransition(url);
    else window.location.href = url;
  }

  // 5. Route Flow Control
  // If they have played before, skip rules and go straight to generator
  if (gameData.usedLetters && gameData.usedLetters.length > 0) {
    if (rulesScreen) rulesScreen.style.display = 'none';
    if (generatorScreen) generatorScreen.style.display = 'block';
    runSelectionAlgorithm();
  } else {
    // Wait for them to read rules and click Proceed
    if (rulesContinueBtn) {
      rulesContinueBtn.addEventListener('click', () => {
        if (rulesScreen) rulesScreen.style.display = 'none';
        if (generatorScreen) generatorScreen.style.display = 'block';
        runSelectionAlgorithm();
      });
    } else {
      runSelectionAlgorithm(); // Fallback if button missing
    }
  }

  // Setup continue button routes to stage 1
  if (setupContinueBtn) {
    setupContinueBtn.addEventListener('click', () => navigate('03_stage1_word_selection.html'));
  }

  // 6. Core Selection Algorithm
  function runSelectionAlgorithm() {
    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const availableLetters = alphabet.split('').filter(l => !gameData.usedLetters.includes(l));

    // If we ran out of alphabet letters, they beat all sections! Move to Stage 2.
    if (availableLetters.length === 0) {
      if (typeof showModal === 'function') {
        showModal('Mission Complete', 'Every letter done — continuing to the next stage.');
        setTimeout(() => navigate('04_stage2_primary_recall.html'), 1700);
      } else {
        navigate('04_stage2_primary_recall.html');
      }
      return;
    }

    if (setupStatusText) setupStatusText.textContent = "Shuffling ...";

    // Start a rapid shuffle animation to build suspense
    let counter = 0;
    const cipherInterval = setInterval(() => {
      const randChar = availableLetters[Math.floor(Math.random() * availableLetters.length)];
      const randLength = Math.floor(Math.random() * 8) + 4; // Between 4 and 11

      if (setupCodeEl) setupCodeEl.textContent = `${randLength},${randChar}`;
      counter++;

      // After 30 shuffles (about 1.5 seconds), finalize the assignment
      if (counter > 30) {
        clearInterval(cipherInterval);
        finalizeAssignment(availableLetters);
      }
    }, 50);
  }

  // 7. Finalize The Word Length & Letter
  function finalizeAssignment(availableLetters) {
    // Pick the letter
    gameData.letter = availableLetters[Math.floor(Math.random() * availableLetters.length)];
    gameData.usedLetters.push(gameData.letter);
    gameData.letters = [gameData.letter]; // Keeping for backwards compatibility

    // Fetch words for this letter to determine an appropriate length
    if (typeof window.STEMDictionary === 'undefined') {
      if (typeof showModal === 'function') {
        showModal('System Error', 'The Dictionary Archives are currently offline. Please refresh the page.');
      } else {
        alert("CRITICAL ERROR: Dictionary failed to load.");
      }
      return; // Stop the game from breaking further!
    }

    let possibleWords = window.STEMDictionary.getWordsByLetter(gameData.letter).map(w => w.word);

    // Cooldown Logic: Don't repeat words played globally in the last 3 days
    const globalUsedRaw = JSON.parse(localStorage.getItem('osmosis_global_used_words')) || [];
    const now = Date.now();
    const cooldownMs = 3 * 24 * 60 * 60 * 1000;

    const onCooldown = globalUsedRaw
      .map(item => typeof item === 'string' ? { word: item.toLowerCase(), time: now } : item)
      .filter(item => (now - item.time) < cooldownMs)
      .map(i => i.word);

    let freshWords = possibleWords.filter(w => !onCooldown.includes(w.toLowerCase()));
    
    // If somehow all words are on cooldown, ignore cooldown and use all words
    if (freshWords.length === 0) freshWords = possibleWords;
    possibleWords = freshWords;

    // Pick a random word from the pool just to establish our target length
    if (possibleWords.length > 0) {
      const chosenWord = possibleWords[Math.floor(Math.random() * possibleWords.length)];
      gameData.length = chosenWord.length;
    } else {
      gameData.length = 7; // Fallback
    }

    gameData.wordsPool = possibleWords;

    // Play Success Sound & Save State
    if (typeof AudioManager !== 'undefined') AudioManager.play('success');
    sharedState.save(gameData);

    // Update UI with final assignment
    if (setupStatusText) setupStatusText.textContent = "ASSIGNMENT GENERATOR";
    if (setupCodeEl) setupCodeEl.innerHTML = `<span style="animation: pulse 1s ease-in-out;">${gameData.length},${gameData.letter}</span>`;
    if (setupDescEl) setupDescEl.innerHTML = `implies.<br>Select one word starting with '<strong>${gameData.letter}</strong>' and exactly <strong>${gameData.length}</strong> letters long.`;

    if (setupContinueBtn) {
      setupContinueBtn.style.display = 'block';
      setupContinueBtn.textContent = 'Go Pick Word';
    }
  }
});
