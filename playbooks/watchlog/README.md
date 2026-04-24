# Watchlog

[![View live site](https://img.shields.io/badge/Live_site-watch.gsarigiannidis.gr-green?style=for-the-badge)](https://watch.gsarigiannidis.gr/)

A personal movie and TV show tracking vault for Obsidian and Claude Code. Import your IMDB ratings and watchlist, enrich each entry with TVmaze and OMDB metadata, then browse everything through live Bases views and DataviewJS dashboards. Add new entries any time via a queue note and a Web Clipper template without touching a CSV.

---

## Requirements

- [Obsidian](https://obsidian.md) — free, available on Windows, macOS, Linux
- [Claude Code](https://claude.ai/code) — Anthropic's AI CLI
- Python 3.12+ with the `requests` library (`pip install requests`)
- A free [OMDB API key](https://www.omdbapi.com/apikey.aspx) — for movie metadata (1,000 requests/day on the free tier)
- An [IMDB account](https://www.imdb.com) — to export your ratings and watchlist as CSV

TVmaze is free and requires no key.

---

## What you get

- **`Movies/` and `TV Shows/`** — one note per title, frontmatter-driven, enriched with IMDB rating, genres, runtime, cast, poster, and OMDB/TVmaze metadata
- **Bases views** — pre-configured views for All, Watched, To Watch, By Rating, and (for TV) Following and Upcoming seasons
- **Dashboards** — DataviewJS charts for ratings distribution, watch activity by year, top genres, top directors, runtime distribution, and series status
- **Queue workflow** — drop an IMDB URL (optionally with a rating) into `_Queue.md` and the cron job creates or updates the note automatically
- **Web Clipper template** — one-click add from any IMDB title page; reads your existing star rating automatically
- **`/import-watchlog` skill** — Claude Code slash command to run a full bulk import with a summary and commit prompt

---

## Setup

### Step 1 — Open this folder in Obsidian

Open the `watchlog/` folder as an Obsidian vault:

- Launch Obsidian
- Click **Open folder as vault**
- Select the `watchlog/` folder

### Step 2 — Install community plugins

In Obsidian, go to **Settings → Community plugins → Browse** and install:

| Plugin | What it enables | Required |
|--------|----------------|----------|
| [Dataview](https://obsidian.md/plugins?id=dataview) | Powers the DataviewJS dashboard charts | Required |
| [Charts](https://obsidian.md/plugins?id=obsidian-charts) | Renders charts via `window.renderChart` | Required |

After installing each plugin, enable it. Dataview settings are pre-configured in this vault.

In Obsidian's file explorer you may want to hide `scripts/` and `imports/`. Go to **Settings → Files & Links → Excluded files** and add them there.

### Step 3 — Add your OMDB API key

```bash
cp .env.example .env
```

Edit `.env`:

```
OMDB_API_KEY=your_key_here
```

Get a free key at [omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx).

### Step 4 — Run a bulk import from IMDB (first time)

Export your data from IMDB:

- **Ratings**: Your Ratings → Export (downloads `ratings.csv`)
- **Watchlist**: Your Watchlist → Export (downloads `watchlist.csv`)

Rename the files to `ratings.csv` and `watchlist.csv` and drop them in `imports/`. Then run:

```bash
python3 scripts/import.py --tvmaze --omdb
```

Or use the Claude Code skill — open Claude Code in this vault and say:

```
import my ratings
```

The script is incremental; re-running after a fresh export is safe and fast.

### Step 5 — Set up the queue cron job (optional)

The queue processor runs `_Queue.md` automatically. To set it up:

1. Edit `scripts/watchlog_queue.sh` — the script auto-detects the vault root, or you can set `WATCHLOG_VAULT=/absolute/path/to/watchlog` at the top
2. Make it executable: `chmod +x scripts/watchlog_queue.sh`
3. Add to crontab (`crontab -e`):
   ```
   */15 * * * * /absolute/path/to/watchlog/scripts/watchlog_queue.sh
   ```

### Step 6 — Set up Obsidian Web Clipper (optional)

Import the pre-made template to add entries from IMDB with one click:

1. Install [Obsidian Web Clipper](https://obsidian.md/clipper) for your browser
2. Open the extension → **Templates** → **Import template**
3. Select `scripts/clipper/queue.json`

The template detects your IMDB star rating and appends `URL :: score` (or just `URL` if unrated) to `_Queue.md`. The cron job picks it up within 15 minutes.

---

## Vault structure

```
watchlog/
  Movies/                       one note per film
  TV Shows/                     one note per series
  Views/
    Movies.base                 Bases view: All, Watched, To Watch, By Rating
    TV Shows.base               Bases view: All, Watched, To Watch, Following, By Rating
    Upcoming.base               Bases view: Coming Soon, Ready to Watch
    _Dashboard.md               Combined stats and charts (movies + TV)
    _Movies Dashboard.md        Movies-only stats and charts
    _TV Shows Dashboard.md      TV-only stats and charts
  imports/                      drop IMDB CSV exports here (gitignored)
  scripts/
    import.py                   bulk import and sync from IMDB CSV exports
    process_queues.py           queue processor
    watchlog_queue.sh           cron wrapper for the queue processor
    clipper/queue.json          Obsidian Web Clipper template
  .claude/skills/import-watchlog/   Claude Code import skill
  _Queue.md                     add IMDB URLs here to queue entries
  .env.example                  API key template
```

---

## Usage

**Day-to-day:** navigate to an IMDB title page, click the Web Clipper extension. The entry appears in `_Queue.md` and the cron job processes it within 15 minutes, creating the note and populating all metadata.

**Rating after watching:** click the Web Clipper after rating on IMDB (the template reads your star score), or edit `_Queue.md` directly by appending `URL :: score`.

**Bulk sync:** re-export from IMDB and run `python3 scripts/import.py --tvmaze --omdb`, or ask Claude Code to import.

**Browsing:** open `Views/Movies.base` or `Views/TV Shows.base` for the filterable Bases views. Open `Views/_Dashboard.md` for the charts.

---

## Note frontmatter

**Movies** — `title`, `original_title`, `imdb_id`, `imdb_url`, `imdb_rating`, `my_rating`, `year`, `type`, `genres`, `directors`, `runtime`, `status`, `date_watched`, `language`, `country`, `rated`, `metascore`, `awards`, `writer`, `actors`, `poster`, `omdb_last_checked`, `worth_it`

**TV shows** — all of the above (minus movie-only fields) plus `tvmaze_id`, `total_seasons`, `series_status`, `following`, `current_season`, `last_season_watched`, `next_season_start`, `next_season_date`, `tvmaze_last_checked`, `network`, `show_type`, `premiered`, `ended`

**Status values** — `watched`, `watching`, `to-watch`, `to-rewatch`
