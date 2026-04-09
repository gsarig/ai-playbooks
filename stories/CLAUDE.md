# Fiction Writing Rules — Global

These rules apply to all stories in this vault. Story-specific rules in each story's own `CLAUDE.md` override these where they conflict.

## Author

<!-- Describe your language background here if relevant to your writing. Example: -->
<!-- "Non-native English speaker (Spanish). Flag constructions that sound like direct translations." -->
<!-- Leave blank if writing in your native language. -->

## Language Rules

Applied during all `/language-edit` passes.

- Flag non-native constructions: unnatural article use, verb tense confusion, over-formal register, and idioms that read as direct translations from another language.
- Prefer simple, direct sentence structure. Flag run-on sentences or complex subordinate clause structures that impede clarity.
- Watch for: excessive passive voice, adjective order errors, misplaced adverbs, and plural/singular agreement errors.
- The target is natural, idiomatic English prose — not formal or translated-sounding.
- Do not auto-apply corrections. Present findings with the original text, the issue, and a suggested fix. Let the author decide.

> **Customise this section:** If you write in English as a second language, describe your native language in the Author section above and update the language rules to reflect the patterns most common in your writing. The `/language-edit` command uses these rules to calibrate its Pass 2 refinement.

## Developmental Editing Defaults

Applied during all `/dev-edit` passes unless the story's `CLAUDE.md` overrides them.

- Flag telling instead of showing in emotional beats.
- Flag pacing issues: scenes that stall without narrative purpose, and transitions that rush significant moments.
- Flag on-the-nose dialogue or dialogue that exists only to deliver exposition.
- Flag repetition of words, phrases, or ideas within a chapter.

## Editing Rules

Never modify the content of a chapter or story file unless explicitly instructed to do so. When reviewing a chapter, present suggestions only — the author applies changes manually. The only exception is batch operations (e.g. renaming a character across all files) when explicitly requested.

`/update-chapter` may only modify frontmatter and tracking files (Timeline.md, Character files, Location files). It must never alter chapter prose.

## Consistency Rules

- Use character names exactly as they appear in their Character file. Flag any variation.
- Use location names exactly as they appear in their Location file. Flag any variation.
- Flag any contradiction with the story's `Timeline.md`.
- When uncertain about a world detail, check `_Index.md` before suggesting.
- If a Character file says a character is dead, do not write them as alive.

## Session Start

If the author's first message in a new session is a greeting, vague, or does not specify a task, respond with a brief welcome and present the available commands as options. Do not do this if the first message is already specific about what they want to work on.

## Commands

| Command | Purpose |
|---------|---------|
| `/new-story` | Build a story blueprint from an idea or from scratch |
| `/continue-story` | Re-entry brief for returning to a story after time away |
| `/update-chapter ch-XX` | Post-chapter state sync — updates Timeline, Characters, Locations, checks Quicknotes |
| `/dev-edit ch-XX` | Developmental editing pass on a chapter |
| `/language-edit ch-XX 1\|2\|3` | Language and grammar pass on a chapter (three passes) |
| `/audit-story` | Full consistency audit across all chapters |
| `/publish-prep` | Create promo files and publication record when ready to publish |
| `/archive-story` | Move a completed or abandoned story to the archive |
