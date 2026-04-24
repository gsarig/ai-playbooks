---
name: import-watchlog
description: "Imports IMDB ratings and watchlist exports from imports/ into the Watchlog vault (incremental, TVmaze-aware), reports the summary, and offers to commit."
when_to_use: "Use when the user invokes /import-watchlog, asks to import their IMDB exports, sync Watchlog, or run the Watchlog import script. Follow all steps in order; do not shortcut based on this description."
allowed-tools: Bash(python3 *) Bash(git *) Read
---

## Steps

### 1. Verify the CSV files are in place

Check that both `imports/ratings.csv` and `imports/watchlist.csv` exist at the vault root. If either is missing, stop and tell the user exactly what to do:
- Export Your Ratings and Your Watchlist from IMDB (both as CSV)
- Rename them to `ratings.csv` and `watchlist.csv`
- Drop them in the `imports/` folder

Do not proceed until both are present.

### 2. Run the import

From the vault root, run:

```bash
python3 scripts/import.py --tvmaze
```

The `--tvmaze` flag is always safe: the TTL (default 30 days) means ongoing shows are re-queried only when stale, and Ended shows are never re-queried.

### 3. Report the summary

When the script finishes, surface the summary block it prints (Added, Updated, Skipped, TVmaze calls). If errors were reported, surface them explicitly.

### 4. Offer to commit

Run `git status --short` from the vault root.

- If nothing changed, say so and stop.
- If there are changes, propose a commit message in this form:
  ```
  feat: IMDB re-import — <N> added, <M> updated
  ```
  Wait for the user to approve before running `git commit`. Do not push.

## What to avoid

- Do not run the import without `--tvmaze`. The TTL handles rate limiting already; running without it skips season date tracking.
- Do not commit automatically. Always show the summary and wait for approval.
- Do not touch files in `imports/` — they are gitignored and user-managed.
