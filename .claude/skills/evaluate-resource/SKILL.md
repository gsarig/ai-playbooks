# evaluate-resource

Evaluate an external resource — a methodology, workflow, or pattern — for relevance to this project. Draft a structured evaluation, present it for approval, then write it to `resources/`.

---

## Steps

### 1. Load personal context (if available)

Check whether `.claude/skills/evaluate-resource/context.md` exists.

- If it does, read it.
- If it contains a pointer to an external file (e.g. "See /path/to/file"), read that file too.
- Use any context found to inform the "How it maps to our setup" and "Where we'd diverge" sections.
- If no `context.md` exists, proceed using only what is known from the current project's CLAUDE.md and structure.

### 2. Fetch the resource

Use the appropriate tool to retrieve the content at the URL:

- For GitHub gists or repos: prefer `gh api` via Bash
- For all other URLs: use WebFetch

Read enough to understand the core methodology or proposal — not just the summary.

### 3. Draft the evaluation

Use this exact structure:

```markdown
---
title: ""
url: 
author: ""
date_evaluated: YYYY-MM-DD
verdict: adopt | adapt | skip | watch
tags: []
---

## What it proposes

[What is the methodology, workflow, or pattern? What problem does it solve? Be concrete.]

## How it maps to our setup

[Where does this align with how this project already works? What would slot in without friction?]

## Where we'd adopt it

[Specific things worth taking directly.]

## Where we'd diverge

[What doesn't fit, and why. This is the most important section for `skip` verdicts — document the reasoning so the decision doesn't get revisited unnecessarily.]

## Verdict

[One paragraph. Restate the verdict and justify it in plain terms. For `watch`: explain what would need to change before it becomes relevant.]
```

**Verdict definitions:**
- `adopt` — use this as-is
- `adapt` — the core idea is sound but needs adjustment for this context
- `skip` — not relevant or not worth the cost; the reasoning must be documented
- `watch` — promising but not yet ready, mature, or relevant; revisit when conditions change

**Filename convention:** slugify the title — lowercase, hyphens for spaces, no special characters. Example: `karpathy-llm-wiki-pattern.md`

### 4. Present for approval

Show the full draft to the user. Ask for corrections or confirmation before writing anything.

### 5. Write on confirmation

Once the user approves (or after incorporating corrections), write the file to `resources/<filename>.md`.

Confirm the file path after writing.
