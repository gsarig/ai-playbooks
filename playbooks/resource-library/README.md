# Resource Library Playbook

A scaffold for building a personal curated library of evaluated methodologies, workflows, and patterns — powered by Claude Code and browsable in Obsidian.

## What you get

- An `/evaluate-resource` skill that fetches any URL, drafts a structured evaluation via an Opus subagent, and writes the result to `resources/` after your approval
- A verdict taxonomy (`adopt`, `adapt`, `watch`, `catalog`, `skip`) with documented reasoning
- An Obsidian vault in `resources/` with a Dataview dashboard that automatically groups entries by verdict

## Setup

1. **Copy this folder to your project root** — the `.claude/` and `resources/` folders need to live at the root of wherever you run Claude Code

2. **Configure personal context** (optional but recommended):
   - Copy `.claude/skills/evaluate-resource/context.example.md` to `.claude/skills/evaluate-resource/context.md` (gitignored)
   - Fill in your vault setup, tools, and preferences — or point to a file in your dotfiles
   - The skill uses this to calibrate its judgment about conditions for fit

3. **Open `resources/` as an Obsidian vault** and install the Dataview community plugin — the `_index.md` dashboard uses it to build verdict-grouped tables from file frontmatter automatically

4. **Drop a URL in the chat** with any evaluative phrase ("what do you think", "evaluate this", "is this worth adopting") — the skill triggers automatically

## Structure

```
.claude/skills/evaluate-resource/   — the evaluation skill
resources/                          — evaluated entries (one file each)
resources/_index.md                 — Dataview dashboard (auto-maintained)
resources/README.md                 — evaluation perspective and verdict definitions
CLAUDE.md                           — auto-trigger rule for evaluative intent
```

## Customising the evaluation lens

The evaluations produced by the skill are intentionally generic — conditions for fit described in terms of problem types and workflow characteristics, not your specific project. The personal context file calibrates the Opus subagent's judgment without appearing in the output, so the resulting library is useful to others with similar setups.

To adapt the verdict taxonomy or evaluation template, edit `.claude/skills/evaluate-resource/SKILL.md` directly — it is plain text.
