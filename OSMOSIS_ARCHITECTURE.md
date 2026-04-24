# Osmosis Application Architecture & Technical Guide

This document provides a comprehensive overview of the Osmosis front-end architecture. It details how the application runs, the logic behind the individual game cycles, and how the scientific dictionary serves as the backbone of the entire gameplay experience.

***

## 1. The Dictionary Logic: How Words Are Loaded

The most critical component of Osmosis is its vocabulary. The system needs to retrieve, randomize, and utilize scientific terms on-the-fly depending on what letter the user is currently playing. 

**How we get the dictionary in the code:**
All words are sourced from the `core_dictionary.js` file. Instead of querying a costly external API or relying on complex backend calls, the dictionary is baked directly into the application state using a native JavaScript object.

### The `core_dictionary.js` Mechanics
1. **The Core Object:** Inside `core_dictionary.js`, we define a massive object named `wordBank`. In this object, every letter of the z (A-Z) acts as a key. The value of that key is an array of objects containing a scientifically related `word` and its structural `definition`.
2. **Helper Functions:** Several helper functions (like `getRandomLetter`, `getWordsByLetter`, and `getRoundWords`) are written directly beneath the bank object. These handle traversing arrays and performing Fisher-Yates shuffles to ensure words are randomized without repeating in a batch.
3. **Global Registration:** At the bottom of `core_dictionary.js`, the bank and its helper functions are bound to the `window.STEMDictionary` property. Because `core_dictionary.js` is imported locally into every HTML file via a `<script>` tag, `window.STEMDictionary.getRoundWords('A', 12)` can be called globally across any other javascript file (like `03_stage1_word_selection.js` or `04_stage2_context_match.js`). 

***

## 2. Shared State Management

Because the user repeatedly traverses between different HTML pages (moving from Round 1 to Setup, to Round 2, etc.), Osmosis requires an external entity to "remember" variables like current score, loop progression, selected variables, and cooldowns.

### `core_shared_state.js`
This file introduces `window.sharedState`, a set of functions configured to manipulate `localStorage`. 
- **Persisting Data:** Variables such as `state.letter`, `state.length`, `state.word` and `state.usedLetters` are continually updated. `sharedState.save(state)` pushes the current phase's data to the browser's persistent cache.
- **Loading Data:** When jumping to a new HTML page, `const state = sharedState.load()` restores the prior data contexts into the new JavaScript scope.
- **Cooldown Logic:** To maintain challenge variety, `core_shared_state.js` implements a global timestamp-based memory that forbids words selected today from showing up in subsequent letters for a strict cooldown period!

***

## 3. The Sequence Loop Breakdown

The overarching campaign navigates sequentially through letters A-Z representing continuous rounds of play. Below is the file flow logic for obtaining words.

### The Setup (`02_campaign_setup.html` & `02_campaign_setup.js`)
If the user's progress dictates they are ready for a new letter, they are routed to `02_campaign_setup.html`.
- **Logic:** `02_campaign_setup.js` surveys what letters (A-Z) the user hasn't completed yet and generates a falling plank selection game (re-implemented as `l1_stage5` style mechanics in a prior update).
- **Execution:** Once the user clicks a falling plank depicting a designated `letter` and target `length` (e.g. `C - 8`), that metadata is locked into `sharedState` and they are navigated to Round 2.

### Selection Stage (`03_stage1_word_selection.html` & `03_stage1_word_selection.js`)
The user's objective is to extract one word from an arbitrary pool.
- **Obtaining Words:** `03_stage1_word_selection.js` queries `window.STEMDictionary.getWordsByLetter(currentLetter)`. It filters through the result to find words exactly matching `state.length`. 
- **Decoys:** It ensures at least 20 words drop into the view pool `finalPool`. If there aren't enough exactly-sized words, it pads the rest of the pool with decoy words of varying lengths starting with the same letter.
- **Progression:** Only one correct length word gets flagged internally as the "target". Once clicked, we store that word into `state.selectedWords`, animate it to the board, and navigate to Round 3.

### Contextual Matching Stage (`04_stage2_context_match.html` & `04_stage2_context_match.js`)
The user's objective is to categorize their captured word. It serves as an interactive mini-quiz.
- **Obtaining Words:** A sentence puzzle based on the vocabulary's definition is dynamically created.
- **Progression:** The player confirms the association. If correct, their overarching score is credited.

### The Finale: Review Stage (`06_stage4_review.html` & `06_stage4_review.js`)
The session culminates in an architectural summary.
- **Logic:** `06_stage4_review.js` lists out all terms the user has successfully accrued throughout their 26-letter campaign mode. It's built for rapid feedback.
- **Termination:** Once submitted, `window.sharedState` validates progress. If `state.usedLetters.length` is 26, the game completely zeroes out `localStorage` (or logs the metrics to a history archive) and displays a massive completion overlay.

***

## 4. Peripheral Pages and Tools

There are various supportive files constructed to round out the platform's professional appeal.

* `core_styles.css`: Contains CSS variables, primary typography bounds, animations (shaking error boxes, glowing buttons), and mobile flex queries.
* `01_home_menu.html / index.html / module_about.html`: Serves as static entry points that introduce the application's premise and transition the user cleanly into the first `02_campaign_setup.html` loop.
* `module_library.html / module_diagram_study.html / module_archives.html`: Supportive features functioning semi-independently of the A-Z campaign. `diagram_study` renders graphical canvases mapped to biology visuals, whereas archives show long-term metrics for historical accuracy.
