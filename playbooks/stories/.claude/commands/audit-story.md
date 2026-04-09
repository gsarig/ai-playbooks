Read the following files in full:
- `_Index.md`
- `CLAUDE.md`
- `Timeline.md` (if it exists)
- All files in `_Characters/` (if the folder exists)
- All files in `_Locations/` (if the folder exists)
- All chapter files in `Chapters/` if the folder exists; otherwise read the single story file in the story root (short story structure)

Then produce a **full consistency audit** across the entire story. This is a read-only operation — present findings only, apply nothing.

---

## Story Audit Report

### Timeline Consistency
- Identify any events in the chapters that contradict the timeline order in `Timeline.md`.
- Identify any events in `Timeline.md` that are not supported by chapter text.
- Flag any time jumps that are established in the timeline but not explained in the chapters.

### Character Consistency
For each character in `_Characters/`:
- Verify `first_appearance` matches the actual chapter where they are introduced.
- Verify `last_seen` is up to date.
- Verify `status` (alive/dead/missing) is consistent with the most recent chapter they appear in.
- Flag any chapter where the character behaves in a way that contradicts their established voice or arc.

### Location Consistency
For each location in `_Locations/`:
- Verify `first_appearance` is accurate.
- Flag any chapter where a location is described in a way that contradicts its established description.
- Flag locations mentioned in chapters but missing from `_Locations/`.

### World Rule Violations
Check all chapters against the world rules in `_Index.md` and `CLAUDE.md`. List any violation, quoting the offending text.

### Orphaned Notes
- Characters mentioned in chapters but with no Character file.
- Locations mentioned in chapters but with no Location file.
- Timeline entries that reference chapters that don't exist yet.

### Chapter Frontmatter Gaps
List any chapters with incomplete frontmatter (missing characters, locations, or timeline_events fields).

### Summary
A short prioritised list of the most significant issues found.
