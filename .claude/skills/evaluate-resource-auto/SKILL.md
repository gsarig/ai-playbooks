---
name: evaluate-resource-auto
description: "Approval-free variant of evaluate-resource for automated/batch use: reads a queued file from resources/tmp/, evaluates the URL, writes the review, and cleans up."
when_to_use: "Use when invoked by the cron job to process a queued file from resources/tmp/. Not for interactive use — use evaluate-resource for manual evaluation instead. Follow all steps in order; do not shortcut based on this description."
argument-hint: "[path to queued .md file in resources/tmp/]"
model: opus
effort: high
allowed-tools: WebFetch Read Write Bash(gh *) Bash(rm *) Bash(mv *) Agent
---

# evaluate-resource-auto

Approval-free variant of `evaluate-resource`. Follow all steps from that skill with two differences:

1. **Before step 1** — read the queued file at the path provided and extract the URL from the `source` or `url` frontmatter field. If neither is present or both are empty, append an `## Error` section with the message "No URL found in frontmatter", move the file to `resources/tmp/failed/`, and stop.

2. **Replace steps 5 and 6** — instead of presenting for approval, act on the agent's output directly:
   - **`DUPLICATE`**: insert a row at the top of the `resources/log.md` table (newest-first ordering, directly below the header), delete the source file, and stop.
   - **`EXTEND`**: append the `## Related` entry to the existing review, insert a row at the top of `resources/log.md`, then delete the source file.
   - **Full draft**: write to `resources/reviews/<slugified-title>.md`, insert a row at the top of `resources/log.md`, then delete the source file.

   If anything fails after the fetch, append an `## Error` section describing what failed and move the source file to `resources/tmp/failed/`. Do not delete it.
