---
name: evaluate-resource-auto
description: Approval-free variant of evaluate-resource for automated/batch use. Reads a queued file from resources/tmp/, evaluates the URL, writes the review directly, then deletes the source file. On failure, moves the file to resources/tmp/failed/ for manual retry. Invoked by the cron job.
---

# evaluate-resource-auto

Approval-free variant of `evaluate-resource`. Follow all steps from that skill with two differences:

1. **Before step 1** — read the queued file at the path provided and extract the URL from the `source` or `url` frontmatter field. If neither is present or both are empty, append an `## Error` section with the message "No URL found in frontmatter", move the file to `resources/tmp/failed/`, and stop.

2. **Replace steps 5 and 6** — instead of presenting for approval, act on the agent's output directly:
   - **`DUPLICATE`**: append to `resources/log.md`, delete the source file, and stop.
   - **`EXTEND`**: append the `## Related` entry to the existing review, append to `resources/log.md`, then delete the source file.
   - **Full draft**: write to `resources/reviews/<slugified-title>.md`, append to `resources/log.md`, then delete the source file.

   If anything fails after the fetch, append an `## Error` section describing what failed and move the source file to `resources/tmp/failed/`. Do not delete it.
