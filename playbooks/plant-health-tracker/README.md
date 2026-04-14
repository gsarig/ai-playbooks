# Plant Health Tracker

An AI-powered plant health monitor for Obsidian and Claude Code. Drop photos of your plants into a staging folder, and Claude analyzes them — identifying each plant, assessing its health, and writing structured reports to your vault. Every scan updates a live Dashboard and per-plant timelines with embedded photos, health scores, and care advice.

---

## How it works

Once set up, using it is two steps:

1. **Drop your photos** into the staging folder (a local folder, OneDrive, Dropbox — anything that syncs from your phone works)
2. **Trigger a scan** — pick whichever mode suits you:
   - Open Claude Code in the vault folder and say `please scan` — Claude reads the photos directly and writes everything in the conversation, no API key needed
   - Or run `npm start` from the terminal for a one-shot script scan
   - Or run `npm run watch` once and leave it running — it fires automatically 2 minutes after your last photo lands

That's it. Claude identifies every plant, matches returning plants against their history, writes a new timeline entry with embedded photos, updates the health trend chart, and regenerates the Dashboard. If a result is uncertain, a warning appears in the Dashboard and the photos are queued for a higher-quality rescan with `npm run rescan`.

---

## What you get

- **Photo inbox workflow** — drop photos into any folder; the tracker picks them up automatically
- **Vision-based analysis** — Claude identifies every plant in a session, matches it against known plants, and produces a health report
- **Per-plant reports** — frontmatter-driven notes with an embedded health trend chart and reverse-chronological timeline
- **Live Dashboard** — Dataview table of all plants, attention filters, watering tracker, and recent activity
- **Confidence-aware rescanning** — low-confidence identifications are flagged and queued for a more thorough Opus rescan
- **Two run modes** — a Node.js script (automated/batch, requires Anthropic API key) or in-session via Claude Code (no key needed, works for typical sessions)

---

## Requirements

- [Obsidian](https://obsidian.md) — free, available on Windows, macOS, Linux
- [Claude Code](https://claude.ai/code) — Anthropic's AI CLI
- [Node.js](https://nodejs.org) 18+ — for the script mode
- An [Anthropic API key](https://console.anthropic.com) — for script mode only; Claude Code mode needs no key

---

## Setup

### Step 1 — Open this folder in Obsidian

Open the `plant-health-tracker/` folder as an Obsidian vault:

- Launch Obsidian
- Click **Open folder as vault**
- Select the `plant-health-tracker/` folder

### Step 2 — Install community plugins

In Obsidian, go to **Settings → Community plugins → Browse** and install:

| Plugin | What it enables | Required |
|--------|----------------|----------|
| [Dataview](https://obsidian.md/plugins?id=dataview) | Powers the live tables in Dashboard.md and the health trend chart | Required |
| [Charts](https://obsidian.md/plugins?id=obsidian-charts) | Renders the health trend chart via `window.renderChart` | Required |

After installing each plugin, enable it. Plugin settings are pre-configured in this vault — no manual setup needed.

In Obsidian's file explorer you may want to hide the `src/` and `node_modules/` folders. Go to **Settings → Files & Links → Excluded files** and add them there.

### Step 3 — Configure paths

```bash
cp config.example.json config.json
```

Edit `config.json`:

```json
{
  "stagingPath": "/path/to/your/photo/inbox",
  "vaultPath": "/path/to/plant-health-tracker",
  "pollIntervalMs": 10000,
  "reportLanguage": "English"
}
```

- **stagingPath** — the folder where you drop photos before a scan (can be a OneDrive or Dropbox folder for mobile uploads)
- **vaultPath** — absolute path to this vault folder
- **reportLanguage** — the language for AI-generated report text (summaries, observations, care advice); structural labels stay in English

Windows paths work fine — they are converted to POSIX automatically when running under WSL.

### Step 4 — Set your API key (script mode only)

```bash
cp .env.example .env
```

Edit `.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
```

The API key is only needed for `npm start` / `npm run watch` / `npm run rescan`. If you only use Claude Code's in-session scan, skip this step.

### Step 5 — Install dependencies (script mode only)

```bash
npm install
```

---

## Usage

### In-session scan (Claude Code — recommended for most sessions)

Open Claude Code in this vault folder and say:

```
please scan
```

Claude reads the photos directly with vision, identifies every plant, and writes all vault files in the conversation. No API key required. Works well for typical sessions (3–8 photos).

### Scan once (script)

Processes all photos currently in the staging folder as a single session:

```bash
npm start
```

### Watch for new photos (script)

Watches the staging folder and fires automatically 2 minutes after the last photo arrives — giving a full mobile sync session time to land:

```bash
npm run watch
```

### Rescan with Opus (script)

When a scan produces uncertain identifications, the Dashboard warns you and photos are queued for rescan. Run this to re-analyze them using the more powerful `claude-opus-4-6` model:

```bash
npm run rescan
```

You will be shown what is queued and asked to confirm before any Opus call is made.

---

## How to take good photos

All photos dropped in one session are analyzed together as a single Claude call. Claude uses all angles to produce a richer analysis. There is no limit on how many photos you drop per session.

A suggested checklist per plant:

1. **Full plant shot** — far enough to see the entire shape. Drooping, leaning, or uneven growth reveals water stress, light direction, and overall vigour.
2. **Soil surface close-up** — from 10–15 cm away. Dry soil is lighter and cracked; moist soil is darker and compact. This is the most reliable way to assess watering needs.
3. **Underside of a leaf** — pests (spider mites, mealybugs, scale) appear there first and are invisible from above.
4. **Any problem close-ups** — if you notice a yellow leaf, brown tips, or a suspicious spot, a dedicated close-up is more useful than a general shot.

Things that hurt more than they help:

- Multiple shots from the same angle (redundant)
- Very wide shots where the plant is small in the frame (too little detail)
- Flash photography (distorts colour, which matters for health assessment)

### Using OneDrive or Dropbox as your staging folder

Set `stagingPath` to a synced folder on your phone. Take photos on your phone, save them to that folder, and they sync automatically. Run `npm run watch` on your desktop to process them as soon as they land, or trigger a manual scan from Claude Code.

---

## Plant identification

On first encounter Claude identifies the species and registers the plant automatically (e.g. `monstera-deliciosa-01`). On subsequent scans it matches against reference photos of known plants. If you have two plants of the same species they get separate numbered entries (`monstera-deliciosa-01`, `monstera-deliciosa-02`).

If identification confidence is low, a warning appears in the Dashboard and the photos are queued for `npm run rescan`.

---

## Vault structure

```
plant-health-tracker/
  CLAUDE.md                    Claude Code rules for in-session scan
  config.example.json          Configuration template
  package.json
  src/                         Node.js scanner source
  _attachments/                All photos land here after scanning
  _registry.json               Internal plant registry — do not edit manually
  _history/                    Per-plant structured history JSON — do not edit manually
  Dashboard.md                 Auto-generated overview
  monstera-deliciosa-01/
    report.md                  Frontmatter + health chart + timeline
  pothos-01/
    report.md
```

---

## Reports

Each `report.md` contains:

- **Frontmatter** — `species`, `health_status`, `urgency`, `location`, `vessel`, `first_seen`, `last_seen` (queryable via Dataview)
- **Summary table**
- **Health History** — a DataviewJS line chart showing health score over time (requires Charts plugin)
- **History** — reverse-chronological timeline; each entry has embedded photos, health status, summary, observations, problems, and care advice

---

## Models

| Mode | Model | When |
|------|-------|------|
| Normal scan | `claude-sonnet-4-6` | Every scan |
| Rescan | `claude-opus-4-6` | Explicit `npm run rescan` only |

---

## Customising the report language

Set `reportLanguage` in `config.json` to any language (e.g. `"French"`, `"Spanish"`, `"Greek"`). AI-generated text — summaries, observations, problems, and care advice — will be written in that language. Structural labels (section headers, table headers, frontmatter keys) stay in English.
