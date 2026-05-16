---
name: evaluate-resource
description: "Evaluates an external resource and writes a structured review with a verdict to resources/reviews/."
when_to_use: "Use when the user shares a URL with evaluative intent ('what do you think', 'evaluate this', 'is this worth adopting', 'thoughts on this'), or explicitly invokes /evaluate-resource. Follow all steps in order; do not shortcut based on this description."
argument-hint: "[URL to evaluate]"
model: opus
effort: high
allowed-tools: WebFetch Read Write Bash(gh *) Agent
---

# evaluate-resource

## Steps

### 1. Load personal context (if available)

Check whether `.claude/skills/evaluate-resource/context.md` exists.

- If it does, read it.
- If it contains a pointer to an external file (e.g. "See /path/to/file"), read that file too.
- Use any context found to calibrate judgment about conditions for fit — not to write project-specific content.
- If no `context.md` exists, proceed using only what is known from the current project's CLAUDE.md and structure.

### 2. Fetch the resource

Use the appropriate tool to retrieve the content at the URL:

- For GitHub gists or repos: prefer `gh api` via Bash
- For all other URLs: use WebFetch

Read enough to understand the core methodology or proposal — not just the summary.

### 3. Check for overlap

**First**, read `resources/log.md` and check whether the URL appears in it.

- If the URL is already in the log: stop. The resource has been processed before. Report the existing outcome to the user (interactive mode) or log and exit cleanly (auto mode). Do not re-evaluate.

**Then**, glob `resources/reviews/*.md` and read the `title`, `url`, and `tags` frontmatter fields from each file to build a lightweight index.

- If the title or topic looks **substantially similar** to one or more existing entries: read those reviews in full and carry them into step 4. The Opus subagent will assess overlap as part of its work.
- If nothing looks related: proceed to step 4 with no existing reviews attached.

### 4. Draft the evaluation using an Opus subagent

Spawn an Agent with `model: "opus"` and pass it:
- The full URL and fetched content
- The contents of the context file (if loaded in step 1)
- Any existing reviews identified as potentially overlapping in step 3
- The evaluation template below
- Instruction to return the completed draft as its only output — the agent must NOT write any files

**If overlapping reviews were provided**, the agent must first assess the degree of overlap:
- **Same core idea, nothing new**: return `DUPLICATE: <existing-filename>` as its entire output. No draft needed.
- **Same core idea, but adds something worth preserving**: produce a short `## Related` entry (URL + one sentence on what it adds) to be appended to the existing review, prefixed with `EXTEND: <existing-filename>`. Do not produce a full new draft.
- **Distinct enough to stand alone**: proceed with a full draft as normal.

**Important framing for the agent:** the evaluation lives in a public repo and must be durable across projects. Write entirely in generic terms — problem types, vault categories, workflow patterns. Do not reference specific project names, file paths, or personal setups. Use the personal context only to calibrate judgment (e.g. deciding what "Best used when" conditions are realistic), never to cite it directly.

Use this exact structure:

```markdown
---
title: ""
url: 
author: ""
date_evaluated: YYYY-MM-DD
verdict: adopt | adapt | skip | catalog | watch
tags: []
---

## What it proposes

[What is the methodology, workflow, or pattern? What problem does it solve? Be concrete — describe the mechanism, not just the goal.]

## Best used when

[Conditions under which this thrives. Describe in terms of problem types, vault categories, or workflow characteristics — not specific projects.]

## Poor fit when

[Conditions under which it breaks down or adds friction without payoff. Be specific about why, not just where.]

## Alternatives

[Only include this section if a better or equivalent option exists. Name the alternative and explain why it is preferable. If this section is present, the verdict should be `skip`.]

## Verdict

[One paragraph. State the verdict and justify it in plain terms. Must be durable — useful to anyone evaluating this resource for a similar type of project, not just the original author.]
```

**Verdict definitions:**
- `adopt` — use this as-is
- `adapt` — the core idea is sound but needs adjustment for the use case
- `skip` — not worth using: poor quality, overcomplicated, or superseded by a better alternative. Name the alternative in the `## Alternatives` section.
- `catalog` — good tool in its domain, but out of scope for this project type; no better in-scope alternative identified. Worth knowing about for other contexts.
- `watch` — promising but not yet ready, mature, or relevant; state what would need to change

**Filename convention:** slugify the title — lowercase, hyphens for spaces, no special characters. Example: `karpathy-llm-wiki-pattern.md`

### 5. Present for approval

Handle the three possible outcomes from step 4:

- **`DUPLICATE`**: tell the user the resource is already covered by the named review. No further action needed.
- **`EXTEND`**: show the proposed `## Related` entry and the name of the existing review it would be appended to. Ask for confirmation before writing.
- **Full draft**: show the complete draft. Ask for corrections or confirmation before writing anything.

### 6. Write on confirmation

Once the user approves (or after incorporating corrections):

- **`EXTEND`**: append the `## Related` entry to the existing review at `resources/reviews/<existing-filename>.md`. If a `## Related` section already exists, add the new bullet to it; otherwise add the section at the end of the file.
- **Full draft**: write the file to `resources/reviews/<filename>.md`.

In both cases, also insert a row into `resources/log.md`. For `DUPLICATE`, insert the log row but write nothing else.

In all cases (including `DUPLICATE`), insert a row into `resources/log.md` immediately below the table header (so the newest entry sits at the top, since the log is sorted newest-first):

```
| YYYY-MM-DD | <url> | <outcome> | <notes> |
```

Where outcome is `reviewed`, `extended`, or `duplicate`, and notes is a wikilink to the relevant review file (e.g. `[[review-slug]]`) or a short explanation of why it was skipped.

The `resources/_index.md` is maintained automatically by Bases — no manual update needed.

Confirm the file path after writing.
