# Claude Code Commands

Run these from inside a story folder.

| Command | Purpose |
|---------|---------|
| `/new-story` | Build a story blueprint from an idea or from scratch |
| `/continue-story` | Re-entry brief for returning to a story after time away |
| `/update-chapter ch-XX` | Post-chapter state sync — updates Timeline, Characters, Locations |
| `/dev-edit ch-XX` | Developmental editing pass on a chapter |
| `/language-edit ch-XX 1\|2\|3` | Language and grammar pass (three passes) |
| `/audit-story` | Full consistency audit across all chapters |
| `/publish-prep` | Create promo files and publication record when ready to publish |
| `/archive-story` | Move a completed or abandoned story to the archive |

---

## `/new-story`

Reads `Quicknotes.md` and builds the full story blueprint. Asks about form (short story / novella / novel) before creating structure.

- **Novel / novella:** creates `_Index.md`, `CLAUDE.md`, `Timeline.md`, `_Lore.md`, `_Lines.md`, `Quicknotes.md`, `Chapters/`, `_Characters/`, `_Locations/`, `_Research/`, `_Assets/`.
- **Short story:** leaner structure — single story file, `_Index.md`, `CLAUDE.md`, `Quicknotes.md`, optional `_Characters/`.

Timeline format is chosen based on narrative structure (linear table / grouped list / minimal reference points).

---

## `/continue-story`

Re-entry brief for returning to a story after time away.

Reads the last two chapters, `_Index.md`, `CLAUDE.md`, `Timeline.md`, and `Quicknotes.md`, then presents: where the story stands, last chapter recap, open threads, Quicknotes to action, and what to write next.

---

## `/update-chapter ch-XX`

Post-chapter sync. Run after finishing or revising a chapter.

Reads the chapter, then proposes (before applying):
- New timeline entries
- New or updated character files
- New or updated location files
- Updated chapter frontmatter (`timeline_events`, `locations`, `characters`, `status`, `wordcount`)
- Quicknotes items that appear to have been addressed
- Any inconsistencies found against existing notes

Works on single-file short stories too — pass the story filename instead of a chapter reference.

---

## `/dev-edit ch-XX`

Developmental editing pass on a chapter or story file. Prompts to switch to Opus before starting.

Covers: structure and pacing, showing vs. telling, dialogue, POV consistency, repetition, continuity, story-specific focus areas (from `CLAUDE.md`), and strengths. Calibrated to the author's writing-style skill.

Read-only — presents findings only, applies nothing.

---

## `/language-edit ch-XX 1|2|3`

Language and grammar pass. Pass number is required.

- **Pass 1** — Errors only: grammar, syntax, punctuation, clear non-native constructions
- **Pass 2** — Refinement: subtle idiomaticity issues, rationale explained for every change. Prompts to switch to Opus.
- **Pass 3** — Final sweep: minimal, genuine errors only, fresh read

Returns inline markup (~~strikethrough~~ old / **bold** new) with sequential Polish Notes. Applies nothing — author selects changes.

---

## `/audit-story`

Full consistency audit across all chapters, timeline, characters, and locations.

Checks: timeline consistency, character consistency (status, traits, names), location consistency, world rule violations, orphaned notes, frontmatter gaps.

Read-only — presents findings only.

---

## `/publish-prep`

Creates the `_Promo/` folder (Blurb, Tags, Campaign) and `_Publication.md` when a story is ready for publication. Pre-fills what it can from `_Index.md`; leaves the rest as placeholders.

---

## `/archive-story`

Moves a completed or abandoned story to `_Archive/Completed/` or `_Archive/Abandoned/`. Updates `_Index.md` status. Asks before applying. Suggests running `/publish-prep` first if the story is complete and has no publication file.
