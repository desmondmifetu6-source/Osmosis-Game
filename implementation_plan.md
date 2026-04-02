# Refactoring and Cleanup Plan

This plan focuses on making the Osmoisis codebase more understandable and removing unused files, while retaining the Multi-Page Architecture (MPA) which is crucial for the current stage-by-stage progression.

## Proposed Changes

### Deletions
#### [DELETE] `Team_Documentation/` (Empty directory)

### Code Understandability Improvements
We will go through the core game logic files and add clear, descriptive comments explaining the flow and state management. This won't change functionality but will drastically improve how easy it is to change the code later.

#### [MODIFY] [shared.js](file:///c:/Users/Desmond/Desktop/osmosisi_retry/shared.js)
- Document the `sharedState` object and how `localStorage` is used to persist data across the 6 different HTML pages.
- Add comments explaining the modal system (`initModal`, `showModal`).

#### [MODIFY] [wordBank.js](file:///c:/Users/Desmond/Desktop/osmosisi_retry/wordBank.js)
- Clarify the dictionary structures (`STEMDictionary`) and how random letters/words are generated.

#### [MODIFY] [server.js](file:///c:/Users/Desmond/Desktop/osmosisi_retry/server.js) & [package.json](file:///c:/Users/Desmond/Desktop/osmosisi_retry/package.json)
- Add comments explaining that the Express server ([server.js](file:///c:/Users/Desmond/Desktop/osmosisi_retry/server.js)) currently handles saving scores to [database.json](file:///c:/Users/Desmond/Desktop/osmosisi_retry/database.json) via `/api/score`, which is likely for future multiplayer/leaderboard features. 

#### [MODIFY] Game Logic Files ([round1.js](file:///c:/Users/Desmond/Desktop/osmosisi_retry/round1.js) ... [round6.js](file:///c:/Users/Desmond/Desktop/osmosisi_retry/round6.js))
- Add clear block comments at the top of each file explaining the objective of that specific round.
- Comment complex logic (like falling word logic in [round2.js](file:///c:/Users/Desmond/Desktop/osmosisi_retry/round2.js)).

## Verification Plan

### Automated Tests
- N/A. No test framework is currently setup.

### Manual Verification
- We will start the [server.js](file:///c:/Users/Desmond/Desktop/osmosisi_retry/server.js) process via `npm start`.
- Play through from [index.html](file:///c:/Users/Desmond/Desktop/osmosisi_retry/index.html) to [setup.html](file:///c:/Users/Desmond/Desktop/osmosisi_retry/setup.html) and the first few rounds to ensure that functionality remains exactly as before and no errors are thrown due to regressions from commenting/cleanup operations.
