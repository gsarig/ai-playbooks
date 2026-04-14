# Plant Health Tracker — Claude Code Rules

## In-session scan

When the user says "please scan", "scan my plants", "scan plants", or similar, perform the full scan directly using tools — no script invocation needed:

1. Read `config.json` (at vault root) for `stagingPath`, `vaultPath`, and `reportLanguage`
2. List image files (jpg, jpeg, png, webp, gif) in the staging folder
3. Read each photo with the Read tool (vision-capable)
4. Load `_registry.json` and `_history/<plantId>.json` for all known plants
5. Analyze all photos as one session — same batching logic as the script:
   - Identify every distinct plant visible across all photos
   - Match against known plants using reference photos (stored as `referencePhoto` in the registry) and health history
   - For each plant, note which photo indices show it
6. Write vault files:
   - Move photos to `_attachments/` renamed to `plants-YYYYMMDDHHMMSS.jpg`
   - Update `_registry.json`
   - Append entry to `_history/<plantId>.json`
   - Update or create `<plantId>/report.md` (frontmatter + health chart + reverse-chronological timeline)
   - Regenerate `Dashboard.md`

Output is identical to running `node src/scan.js` from the project directory.

Works well for typical sessions (3–8 photos). For large batches or unattended/automated runs, use `npm start` or `npm run watch` instead.

## Report format

- Reports are written with structural labels in English
- AI-generated text (summaries, observations, care advice) is written in the language set in `config.json` → `reportLanguage` (default: English)
- Frontmatter fields: `species`, `common_name`, `plant_id`, `health_status`, `urgency`, `location`, `vessel`, `first_seen`, `last_seen`, `tags`
- `## Health History` — DataviewJS health trend chart (reads `_history/<plantId>.json`)
- `## History` — reverse-chronological timeline; each entry has embedded photos, health status, summary, and care advice

## Vault structure

```
_attachments/          all photos, renamed to plants-YYYYMMDDHHMMSS.jpg
_registry.json         plant registry — do not edit manually
_history/              per-plant structured history JSON — do not edit manually
Dashboard.md           auto-generated; regenerated on every scan
<plant-id>/
  report.md            frontmatter + health chart + reverse-chronological timeline
```

## Obsidian plugins required

- **Dataview** — powers live tables in Dashboard.md and the health chart
- **Charts** — renders the health trend chart via `window.renderChart`
