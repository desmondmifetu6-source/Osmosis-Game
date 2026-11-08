# 🧭 Osmosis STEM Platform: Easy-to-Identify Architecture Guide

> **Quick Reference Map for Desmond Mifetu & Engineering Team**  
> Everything you need to find, understand, debug, or extend any stage or core file in the Osmosis ecosystem in 10 seconds or less.

---

## 🎯 1. The 8-Stage Core Learning Journey

Osmosis follows a scientifically structured **cognitive reinforcement ladder**—moving from passive exposure to active recall, context insertion, and holistic mastery.

| Stage # | Stage Name | HTML Entrypoint | JS Controller | Key Mechanic | Auto-Advance? |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Stage 1** | **Word Selection** | [`03_stage1_word_selection.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/03_stage1_word_selection.html) | `03_stage1_word_selection.js` | Pick topic & target study vocabulary | Manual |
| **Stage 2** | **Word Fill-in** | [`04_stage2_word_fillin.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/04_stage2_word_fillin.html) | [`04_stage2_word_fillin.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/04_stage2_word_fillin.js) | Fill in masked letters with time pressure | **Yes (750ms)** |
| **Stage 3** | **Flash Recall** | [`05_stage3_flash_recall.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/05_stage3_flash_recall.html) | [`05_stage3_flash_recall.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/05_stage3_flash_recall.js) | Rapid visual flashing to build visual retention | **Yes (750ms / On Input)** |
| **Stage 4** | **Self Recall** | [`06_stage4_self_recall.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/06_stage4_self_recall.html) | `06_stage4_self_recall.js` | Mental recall check with self-rating | Manual |
| **Stage 5** | **Meaning Exposure** | [`07_stage5_meaning_exposure.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/07_stage5_meaning_exposure.html) | [`07_stage5_meaning_exposure.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/07_stage5_meaning_exposure.js) | Deep study of NaCCA definitions with audio voiceover | Manual |
| **Stage 6** | **Definition Selection** | [`08_stage6_definition_selection.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/08_stage6_definition_selection.html) | [`08_stage6_definition_selection.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/08_stage6_definition_selection.js) | 2×2 Pill Matrix: Match definition to term | **Yes (750ms)** |
| **Stage 6b**| **Context Dropdowns** | [`08b_stage6b_meaning_dropdown.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/08b_stage6b_meaning_dropdown.html) | [`08b_stage6b_meaning_dropdown.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/08b_stage6b_meaning_dropdown.js) | Sentence cloze test with custom interactive dropdowns | **Yes (750ms)** |
| **Stage 7** | **Segmented Fill-in** | [`09_stage7_meaning_fillin.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/09_stage7_meaning_fillin.html) | [`09_stage7_meaning_fillin.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/09_stage7_meaning_fillin.js) | Inline puzzle slot + 2×2 deceptive distractor grid | **Yes (850ms)** |
| **Stage 8** | **Recall Test** | [`10_stage8_recall_test.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/10_stage8_recall_test.html) | [`10_stage8_recall_test.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/10_stage8_recall_test.js) | Active memory retrieval (Word + Definition typing) | **Yes (Perfect)** |
| **Summary** | **Results & Fame** | [`11_results.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/11_results.html) | `11_results.js` | Performance breakdown, grade certification & XP | N/A |

---

## ⚙️ 2. Core Engines & Shared Infrastructure

These are the foundational services powering all stages:

### 1. Distractor Engine ([`core_distractor_engine.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/core_distractor_engine.js))
* **Purpose**: Generates deceptive multiple-choice options that match the target word's part of speech, grammatical suffix (`-ion`, `-ive`, `-ic`, `-al`), and length.
* **Usage**:
  ```javascript
  const options = window.DistractorEngine.getOptionsWithAnswer(targetWord, 4, {
    exclude: [otherWords],
    preserveCase: false
  });
  ```

### 2. Shared State Engine ([`core_shared_state.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/core_shared_state.js))
* **Purpose**: Manages `localStorage` game persistence, global timer tracking, score aggregation, and cross-page animated transitions.
* **Key Methods**:
  * `sharedState.load()`: Loads active user campaign data.
  * `sharedState.save(data)`: Persists progress.
  * `sharedState.startTimer()`: Starts the campaign clock.
  * `sharedState.updateTimerUI('timer-display')`: Formats elapsed time (`MM:SS`) into `<span id="timer-display">`.
  * `window.navigateWithTransition(url)`: Smooth page transition helper.

### 3. Dictionaries & Content ([`core_dictionary.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/core_dictionary.js) & [`core_stem_dictionary.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/core_stem_dictionary.js))
* **Purpose**: Holds digitized NaCCA 1,400-page curriculum definitions, scientific terms, and letter-indexed lookup tables.

### 4. Audio Engine ([`core_audio.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/core_audio.js))
* **Purpose**: Triggers tactical audio feedback:
  * `AudioManager.play('success')` / `'ok'`: Correct deduction.
  * `AudioManager.play('error')`: Incorrect pick.
  * `AudioManager.play('chip')`: Partial match.

---

## 🎨 3. Design System & Modern UI Standard

All freed stages adhere to the unified **Osmosis Hero Design Language**:

### Visual Tokens
* **Page Background**: `linear-gradient(145deg, #dde3f8 0%, #ede5f8 45%, #d6eaf8 100%)`
* **Card Elevation**: Clean white card, `border-radius: 24px-28px`, `box-shadow: 0 20px 45px rgba(79, 70, 229, 0.08)`
* **Pill Buttons**: `border-radius: 999px`, clean typography, hover elevation.
* **Success Glow**: `#dcfce7` background, `#16a34a` border, `#14532d` deep green text.
* **Wrong Pick**: `#fee2e2` background, `#dc2626` border, `#7f1d1d` text with shake animation.

### Topbar & Mobile Rules
```html
<header class="s*-topbar">
  <!-- Left Badge -->
  <div class="s*-badge">Score : <span id="current-score">0</span></div>
  <!-- Center Title -->
  <div class="s*-topbar-center">⚡ Stage Name</div>
  <!-- Right Badge (Clean, No Fixed ID) -->
  <div class="s*-badge">Time : <span id="timer-display">00:00</span></div>
</header>
```
* **Mobile Breakpoint (`max-width: 640px`)**:
  * `flex-wrap: wrap` on header.
  * Left badge `order: 1`, Right badge `order: 2`.
  * Center title takes `order: 3; width: 100%;` to drop cleanly to row 2 without colliding.
* **Legacy Timer Suppression**: Always include this in `<style>`:
  ```css
  #global-game-timer { display: none !important; }
  ```

---

## ⚡ 4. Developer Pro Keys & Cheats

Built-in accelerator keys to test flows at lightning speed:

* **`Alt + P`**: Auto-selects the correct answer and immediately advances to the next question.
* **Manual URL Jump**: Jump directly to any stage by opening `http://localhost:3000/08_stage6_definition_selection.html` (as long as `localStorage.getItem('osmosis_game_state')` contains sample words).

---

## 🏛️ 5. Extended Modules Map

Aside from the core 8-stage campaign, Osmosis includes these standalone modules:

* [`01_home_menu.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/01_home_menu.html): Main hub, launchpad for campaigns, multiplayer, and libraries.
* [`02_campaign_setup.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/02_campaign_setup.html): Campaign configuration & curriculum level selection.
* [`module_diagram_hub.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/module_diagram_hub.html): Visual STEM anatomy & biological diagrams.
* [`module_library.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/module_library.html): 6-in-1 STEM dictionary lookup engine.
* [`module_word_hunt.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/module_word_hunt.html): Interactive term finder & pattern mini-game.
* [`multiplayer_lobby.html`](file:///c:/Users/Desmond/Desktop/final_osmosis/multiplayer_lobby.html): Real-time classroom competition via Socket.io.

