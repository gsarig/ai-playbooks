Locate the file to update from "$ARGUMENTS":
- If the story uses a `Chapters/` folder, find the file whose name starts with or matches the argument (e.g. "ch-05" → `Chapters/ch-05*.md`).
- If the story is a single-file short story, the argument will be the story filename itself (e.g. "Full Circle" → `Full Circle.md` in the story root).
- If the argument is ambiguous, list matching files and ask which one to use.

Then read the following files in full:
- `Timeline.md` (if it exists)
- `_Characters/_Index.md` and any individual Character files for characters mentioned in the chapter
- `_Locations/_Index.md` and any individual Location files for locations mentioned in the chapter
- `Quicknotes.md`
- `_Index.md` (for world/lore context)
- `CLAUDE.md` in this story folder (for continuity anchors and world rules)

Based on everything you have read, prepare the following updates. **Present them to the author as a structured summary before applying anything. Wait for confirmation.**

---

### 1. Timeline updates

Before proposing timeline entries, consider the story's temporal structure:
- **Linear:** propose entries in story-chronological order with story date, chapter reference, event description, characters, location.
- **Non-linear or multi-strand:** group entries by timeline strand or character arc; note temporal position relative to other events rather than asserting a single sequence. Flag where chronological order is uncertain or deliberately ambiguous.
- **Circular or paradoxical:** note the temporal position of events relative to the story's own logic, not an external timeline. Do not flatten paradoxical or simultaneous events into a sequence that implies a linearity the story rejects.

If Timeline.md does not exist (common for short stories), propose whether one is worth creating given what the story contains. If the story is short and self-contained, it may not be needed.

### 2. Character updates

For each character appearing in this file:
- **New characters:** create a Character file using the template. Set `first_appearance` to this chapter or file. Add this chapter to `appearances`.
- **Existing characters:**
  - Add this chapter to the `appearances` array in frontmatter (if not already present).
  - Update `last_seen` to this chapter.
  - Note any changes to `status` (alive/dead/missing) or Relationships.
  - Add or update a `Key Moments` entry for this chapter. Use a short list of bullets under the chapter heading, one per significant beat involving this character:
    ```
    - **Ch-XX:**
      - What the character does or discovers.
      - How they respond or what changes for them.
      - Any significant interaction, decision, or revelation.
    ```
    Include only beats that are narratively significant — not every action. One bullet is fine if the chapter is light on this character. If `/update-chapter` is run again on the same chapter (e.g. after a revision), replace the existing entry for that chapter rather than appending a duplicate.

For the character's name in the file: use whatever the story uses. Descriptive labels — "The Boy", "The Mother", "The Man" — are valid character names if that is how the story refers to them. Do not invent or infer a real name that the story deliberately withholds.

### 3. Location updates

For each location appearing in this file:
- **New locations:** create a Location file using the template. Set `first_appearance` to this chapter or file. Add this chapter to `appearances`.
- **Existing locations:**
  - Add this chapter to the `appearances` array in frontmatter (if not already present).
  - Add or update a `Key Events` entry for this chapter. Use a short list of bullets under the chapter heading, one per significant event at this location:
    ```
    - **Ch-XX:**
      - What happens here in this chapter.
      - Any change to the location's significance or atmosphere.
    ```
    Include only events that are narratively significant. One bullet is fine for minor appearances. If `/update-chapter` is run again on the same chapter, replace the existing entry rather than appending a duplicate.

### 4. Frontmatter update

Proposed values for:
- `timeline_events` — list of story-time anchors for key events. For non-linear stories, include a brief note on temporal position where relevant.
- `locations` — all locations appearing
- `characters` — all characters appearing, using whatever names or labels the story uses
- `status` — keep existing value unless you have a reason to change it
- `wordcount` — count the words in the chapter and update this field
- `edit_pass` — do not change this field; it is updated manually by the author to track language editing progress (0 = no pass, 1/2/3 = last completed pass)

Note: `appearances` and `last_seen` are maintained in the individual Character and Location files (updated in steps 2 and 3 above), not in the chapter frontmatter.

### 5. Quicknotes check

List any items in `Quicknotes.md` that appear to have been addressed or placed in this chapter or file. Flag them for the author — do not remove them until confirmed.

### 6. Inconsistencies

List any contradictions found between this file and the existing notes (Timeline, Character files, Location files, `_Index.md`). Be specific: quote the conflicting text. Do not flag deliberate ambiguity or unexplained elements as inconsistencies — only flag things that appear to contradict an established fact.

---

After the author confirms (all, partial, or with modifications), apply the approved changes.
