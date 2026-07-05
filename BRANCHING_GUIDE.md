# Git Branching Guide: Switching Between Web and App Versions

This document explains how your project is structured to safely manage both the **Web Version** and the **App Version** (Mobile/Desktop) without duplicating folders or risking your code.

## The Concept: "Time Travel"
Instead of having two separate folders on your Desktop (e.g., `osmosis_web` and `osmosis_app`), we use **Git Branches**. Think of a branch as an alternate timeline or a "save slot" for your entire folder. 

When you switch between branches, the files in this folder will literally vanish and reappear to match whichever timeline you select. It feels like magic, but it keeps your workspace clean!

## The Two Branches
1. **`main`**: This is your pristine **Web Version**.
2. **`app-version`**: This is your **App Version**. Any heavy mobile configurations (like Electron or Capacitor) will be installed here.

---

## The Commands (How to Switch)

To switch to the **Web Version**, open your terminal in this folder and run:
```powershell
git checkout main
```

To switch back to the **App Version**, run:
```powershell
git checkout app-version
```

### Checking where you are:
If you ever forget which version you are currently looking at, run:
```powershell
git branch
```
*The branch with the asterisk (`*`) next to it is your current active branch.*

---

## Why did we do this? (The "Fix it Twice" Nightmare)
If we had used two separate folders on your Desktop and found a typo in the game dictionary, you would have to fix it in the Web folder, and then manually remember to open the App folder and fix it again. If you forgot, your versions would fall out of sync.

Because we used branches, everything stays in one place. If you fix a bug on the `main` branch, we can easily "merge" that fix into the `app-version` branch with a single command, keeping everything perfectly synced.
