Parse "$ARGUMENTS" to extract the chapter reference and pass number (e.g. "ch-01 2" = chapter ch-01, pass 2). If no pass number is given, ask: "Which pass? 1 (errors), 2 (refinement), or 3 (final sweep)."

**If the pass number is 2:** This pass benefits from Opus. If you are currently on Sonnet, let the author know and suggest switching with `/model opus` before proceeding. Wait for their response.

Locate the file from the chapter reference:
- If a `Chapters/` folder exists, find the file whose name starts with the chapter reference.
- If no `Chapters/` folder exists (short story), look for the file in the story root.

Also read this story's `CLAUDE.md` and the vault-level `CLAUDE.md`. Use them to distinguish intentional stylistic choices from genuine errors — never flag or correct deliberate form.

Read the writing-style skill at `../.claude/skills/writing-style/SKILL.md`. This is the single source of truth for the author's aesthetic. Any pattern described there is intentional and must not be flagged as an error.

**Standard across all passes:** American English, Chicago Manual of Style (CMOS), Oxford comma.

**Output format (all passes):**
- For each paragraph, show inline edits using ~~strikethrough~~ for deletions and **bold** for additions.
- If a paragraph needs no changes, return it unchanged with a Polish Note stating "No substantive corrections needed."
- Follow each paragraph with a **Polish Note** labeled sequentially (PN1, PN2, PN3…) across the full chapter.
- Process the entire chapter. Do not summarise or add commentary outside the Polish Notes.

---

## Pass 1 — Errors

**Job:** Fix what is broken. Grammar, syntax, CMOS punctuation, clear non-native constructions that impede comprehension. Do not chase subtlety — that is Pass 2's job.

**Correct:**
- Grammar and syntax errors.
- CMOS punctuation (American quotation conventions, Oxford comma, capitalisation, numbers).
- Non-native constructions that cause misreading or genuine confusion.
- Dummy pronouns and unclear pronoun references where fixing yields a clear improvement.
- Maintain past-tense narration except inside dialogue.

**Do not:**
- Fix phrasing that is grammatically correct but sounds slightly non-native — flag it in the Polish Note, leave it for Pass 2.
- Rephrase for style, rhythm, or flow.
- Add, remove, or invent content.

**Polish Note format:** One line. State what was corrected and why. If flagging something for Pass 2, quote the phrase and note: "Pass 2: [brief reason]."

---

## Pass 2 — Refinement

**Job:** Assume errors are fixed. Now focus on what is technically correct but still sounds non-native to a fluent English ear.

**Target:**
- Non-native constructions specific to the author's first language (see vault-level `CLAUDE.md` for language background). Look for: unnatural article use, literal preposition choices, calqued idioms, word order that reflects the source language, constructions that are grammatically acceptable but mark non-native usage.
- Phrasing that is idiomatically weak in American English even though it is not wrong.
- Distracting word repetitions — list up to three alternatives in the Polish Note; do not force replacements.

**Be more assertive than Pass 1** on idiomatic fixes, but preserve voice. If a construction is intentional or fits the author's register, leave it.

**Polish Note format:** Two parts on one line separated by `|`:
- **Part A:** What was done (one line).
- **Part B:** Rationale — why the change preserves meaning and voice; quote flagged phrases; list alternatives separated by semicolons.

Example: `PN4: Changed "he was feeling" to **he felt** | Non-native construction: source language uses progressive where English prefers simple past in narration; preserves tense and voice.`

---

## Pass 3 — Final Sweep

**Job:** Read as if seeing the text fresh. Flag only what genuinely sticks out. Minimal by design — do not manufacture changes.

**Correct only:**
- Genuine grammatical or consistency errors that slipped through.
- CMOS issues not caught earlier.
- Anything that would make a native reader pause involuntarily.

**Do not:**
- Re-examine idiomaticity already addressed.
- Rephrase for preference.
- Add commentary on structure, pacing, or style.

**Polish Note format:** One line. If nothing sticks out in a paragraph, return it unchanged and write "No substantive corrections needed." Keep the entire pass light — if you find yourself making many changes, stop and flag that the text may need another Pass 2 instead.
