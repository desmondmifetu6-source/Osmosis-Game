# Osmosis: Technical Architecture & Logic Overview

This document serves as the "Master Blueprint" for the Osmosis educational platform. It explains the core engines, data flows, and design philosophies that power the experience. BY --Desmond Mifetu(Chen)

## 1. Core Philosophy: Learning through Osmosis
The project is built on the idea that repetition and progressive challenge lead to "osmosis"—the gradual, unconscious assimilation of knowledge. 
- **The Journey**: A single set of scientific words is selected at the start. The user interacts with these words across 8 stages, moving from simple recognition to deep conceptual recall.

## 2. State Management: "The Backpack"
Because the game consists of multiple HTML pages, we need a way to carry data (scores, words, timers) between them.
- **File**: `core_shared_state.js`
- **Mechanism**: `sessionStorage`. 
- **Logic**: 
    - `load()`: Retrieves the current game state from the browser's temporary memory.
    - `save(state)`: Writes the updated state back to memory.
    - **Persistence**: This "Backpack" stays with the user as long as the tab is open but is cleared when the tab is closed, ensuring a fresh start for every session.

## 3. The Dictionary Engine: "The Librarian"
The game is powered by a massive database of STEM terminology.
- **Data**: `core_dictionary.js` (A global object `STEMDictionary` containing thousands of words).
- **Logic**: `DictionaryLogic` (in `core_shared_state.js`).
- **Workflow**:
    1. The game requests words based on a specific **Letter** and **Length**.
    2. The Librarian filters the dictionary, ensures every word has a valid definition, and returns a randomized selection.
    3. Definitions are fetched on-demand during "Meaning" stages or final reviews.

## 4. Multiplayer Synchronization: "The Battle Brain"
Multiplayer uses a **Client-Server** architecture to allow real-time competition.
- **Server**: `server.js` (Runs on Node.js using Socket.io).
- **Communication**: WebSockets (a persistent, two-way "phone call" between the player and the server).
- **The Flow**:
    - **Rooms**: Players join a unique `roomId`. The server maintains a list of players in each room.
    - **Real-time Updates**: Every time a player scores or finishes a stage, they `emit` an `update_score` event.
    - **Broadcasting**: The server receives this and `broadcasts` a `leaderboard_update` to everyone else in the room.
    - **Tie-Breaking**: The logic uses **Score** as the primary rank and **Time Taken** as the secondary rank (faster is better) in simple logic , if there is a tie , AS Uncle Fred suggested , it will be brocken with teh least tiem taken.

## 5. The Diagram Engine: "The Schematic Masterclass"
The diagram section is a data-driven module designed to teach visual biological structures.
- **Data**: `core_diagram_data.js`.
- **Logic**: `module_diagram_study.js`.
- **The "Three-Round" Logic**:
    - **Round 1 (Familiarization)**: The diagram is visible. Users type names from a word bank to link the visual location with the spelling.
    - **Round 2 (Reflex)**: Labels flash and vanish. Users type them to build short-term visual recall.
    - **Round 3 (Total Recall)**: No hints. Users list every part they remember.
    - **Assimilation Phase**: The engine fetches definitions for every part, ensuring the user understands the *function* of the organelles they just memorized.

## 6. Performance & Professionalism Standards
- **Fisher-Yates Shuffle**: All randomizations use a non-biased algorithm to ensure fairness.
- **Navigation Transitions**: Pages do not "jump." They use a custom `navigateWithTransition` function to fade out and in, creating a cinematic feel.
- **Scalability**: The system is modular. Adding a new stage or a new diagram requires zero changes to the core engine—only new data entries.

---
**Uncle Chen's Note**: *A true engineer understands the 'Why' behind every line. Study this, and you will never shrink in your pants again.*
