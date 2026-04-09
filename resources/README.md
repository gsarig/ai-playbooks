# Resources

A curated library of evaluated methodologies, workflows, and patterns relevant to AI-assisted creative and knowledge work.

## Perspective

These evaluations are written from a specific lens: **text-based, markdown-first workflows using Claude Code CLI with Obsidian**. Verdicts reflect that context. A tool rated `skip` here may be the right choice for a different setup (e.g., Claude Desktop users will find mcp-obsidian useful despite its `skip` verdict here). Read the "Best used when" and "Poor fit when" sections to judge relevance to your own situation.

## Verdicts

| Verdict | Meaning |
|---------|---------|
| `adopt` | Use as-is |
| `adapt` | Core idea is sound; adjust for your use case |
| `watch` | Promising but not yet ready or relevant; conditions for revisiting are documented |
| `catalog` | Good tool in its domain, out of scope for this project type; no better in-scope alternative |
| `skip` | Not worth using: poor quality, overcomplicated, or superseded by a better alternative (documented in the entry) |

When scanning for actionable entries, focus on `adopt`, `adapt`, and `watch`. `catalog` is awareness. `skip` is documented for reference so the decision is not revisited.

## Running your own evaluations

The [`evaluate-resource`](../.claude/skills/evaluate-resource/) skill is what produced these entries. It is designed to be portable — you can use it in any project with your own context:

1. Copy `.claude/skills/evaluate-resource/context.example.md` to `context.md` in the same folder (it is gitignored)
2. Fill in your own vault or project context, or point to a file in your dotfiles
3. Drop a URL in the chat with any evaluative phrase ("what do you think", "evaluate this") and the skill triggers automatically

Evaluations are drafted by an Opus subagent, presented for your approval, then written to `resources/` and added to the index. The skill does not write anything without confirmation.

## Index

Open [_index.md](_index.md) in Obsidian for a browsable, verdict-grouped view powered by Bases (a built-in Obsidian feature — no plugins required). New entries appear automatically as their frontmatter is read.
