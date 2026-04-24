# Watchlog — Vault Rules

Personal vault for tracking movies and TV shows, enriched with IMDB, TVmaze, and OMDB data.

## import-watchlog skill

**Natural language trigger:** when the user asks to import, sync, or run the import script, invoke the `/import-watchlog` skill automatically.

## Do not commit

- `.env` — contains your OMDB API key
- `imports/*.csv` — your personal IMDB export files
- `.import-state.json` — local run history
- `Movies/` and `TV Shows/` notes — personal viewing data (if this is your live vault, not the playbook template)
