# Resource Library Playbook

[![View live site](https://img.shields.io/badge/Live_site-ai--resources.gsarigiannidis.gr-green?style=for-the-badge)](https://ai-resources.gsarigiannidis.gr/)

A scaffold for building a personal curated library of evaluated methodologies, workflows, and patterns — powered by Claude Code and browsable in Obsidian.

## Requirements

- [Obsidian](https://obsidian.md) — free, available on Windows, macOS, Linux, iOS, Android
- [Claude Code](https://claude.ai/code) — Anthropic's AI CLI
- [Obsidian Web Clipper](https://obsidian.md/clipper) — browser extension for clipping resources into your inbox (optional, but the intended way to feed the workflow)

## What you get

- An `/evaluate-resource` skill that fetches any URL, drafts a structured evaluation via an Opus subagent, and writes the result to `resources/reviews/` after your approval
- A verdict taxonomy (`adopt`, `adapt`, `watch`, `catalog`, `skip`) with documented reasoning
- An Obsidian vault in `resources/` with a Bases view that automatically groups entries by verdict — no plugins required

## Setup

1. **Copy this folder to your project root** — the `.claude/` and `resources/` folders need to live at the root of wherever you run Claude Code

2. **Configure personal context** (optional but recommended):
   - Copy `.claude/skills/evaluate-resource/context.example.md` to `.claude/skills/evaluate-resource/context.md` (gitignored)
   - Fill in your vault setup, tools, and preferences — or point to a file in your dotfiles
   - The skill uses this to calibrate its judgment about conditions for fit

3. **Open `resources/` as an Obsidian vault** — the `_index.md` home note embeds a Bases view that groups entries by verdict automatically

4. **Trigger an evaluation** — either clip a resource to the inbox with Web Clipper and then ask Claude Code to evaluate it, or drop a URL directly in the chat with any evaluative phrase ("what do you think", "evaluate this", "is this worth adopting") — the skill triggers automatically either way

## Structure

```
.claude/skills/evaluate-resource/   — the evaluation skill
resources/                          — vault root
resources/_index.md                 — home note, embeds the Bases view
resources/library.base              — Bases view grouped by verdict
resources/reviews/                  — evaluation files (one per resource)
resources/README.md                 — evaluation perspective and verdict definitions
CLAUDE.md                           — auto-trigger rule for evaluative intent
```

## Setting up Obsidian Web Clipper

Web Clipper is the browser extension that feeds the workflow. When you find something worth evaluating, you clip it from the browser and it lands in your vault's inbox — ready for the cron job or Claude Code to pick up.

1. **Install the extension** — go to [obsidian.md/clipper](https://obsidian.md/clipper) and install it for your browser (Chrome, Firefox, Safari, or Edge)

2. **Connect it to your vault** — open the extension settings and select your vault from the list. Obsidian must be running at least once beforehand for the vault to appear.

3. **Set the destination folder** — in the extension settings, set the default save location to your inbox folder (e.g. `resources/tmp`). This is the folder Claude Code watches for new clips.

4. **Set the note format** — the default template works fine. You can optionally add a `url` property to the frontmatter template so the evaluation skill can pick it up automatically:
   ```
   url: {{url}}
   ```

5. **Clip something** — navigate to any page you want to evaluate, click the extension icon, and hit save. The page content lands in your inbox as a markdown file.

From there, open Claude Code and say `evaluate this` — it will find the clipped file and run the evaluation.

## Customising the evaluation lens

The evaluations produced by the skill are intentionally generic — conditions for fit described in terms of problem types and workflow characteristics, not your specific project. The personal context file calibrates the Opus subagent's judgment without appearing in the output, so the resulting library is useful to others with similar setups.

To adapt the verdict taxonomy or evaluation template, edit `.claude/skills/evaluate-resource/SKILL.md` directly — it is plain text.
