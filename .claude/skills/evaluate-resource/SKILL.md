# evaluate-resource

Evaluate an external resource — a methodology, workflow, or pattern — for relevance to this project. Draft a structured evaluation, present it for approval, then write it to `resources/`.

---

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

### 3. Draft the evaluation using an Opus subagent

Spawn an Agent with `model: "opus"` and pass it:
- The full URL
- The contents of the context file (if loaded in step 1)
- The evaluation template below
- Instruction to return the completed draft as its only output — the agent must NOT write any files

**Important framing for the agent:** the evaluation lives in a public repo and must be durable across projects. Write entirely in generic terms — problem types, vault categories, workflow patterns. Do not reference specific project names, file paths, or personal setups. Use the personal context only to calibrate judgment (e.g. deciding what "Best used when" conditions are realistic), never to cite it directly.

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

[What is the methodology, workflow, or pattern? What problem does it solve? Be concrete — describe the mechanism, not just the goal.]

## Best used when

[Conditions under which this methodology thrives. Describe in terms of problem types, vault categories, or workflow characteristics — not specific projects.]

## Poor fit when

[Conditions under which it breaks down or adds friction without payoff. Be specific about why, not just where.]

## Verdict

[One paragraph. State the verdict and justify it in plain terms. Must be durable — useful to anyone evaluating this resource for a similar type of project, not just the original author.]
```

**Verdict definitions:**
- `adopt` — use this as-is
- `adapt` — the core idea is sound but needs adjustment for the use case
- `skip` — not relevant or not worth the cost; document why so the decision isn't revisited
- `watch` — promising but not yet ready, mature, or relevant; state what would need to change

**Filename convention:** slugify the title — lowercase, hyphens for spaces, no special characters. Example: `karpathy-llm-wiki-pattern.md`

### 4. Present for approval

Show the full draft to the user. Ask for corrections or confirmation before writing anything.

### 5. Write on confirmation

Once the user approves (or after incorporating corrections):

1. Write the file to `resources/<filename>.md`
2. Append a row to `resources/index.md` with the title, verdict, tags, and filename

Confirm the file path after writing.
