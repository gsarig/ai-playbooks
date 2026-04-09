# ai-playbooks — Project Rules

## Repo structure

```
playbooks/   — Standalone Obsidian + Claude Code workflow blueprints
resources/   — Evaluated external methodologies and patterns
.claude/     — Repo-level skills
```

Each playbook has its own `CLAUDE.md` with rules specific to that vault. Rules in this file apply repo-wide.

## evaluate-resource skill

The `.claude/skills/evaluate-resource/SKILL.md` skill evaluates external methodologies and patterns for relevance to this project and stores the result in `resources/`.

**Natural language trigger:** when the user shares a URL accompanied by evaluative intent — "what do you think", "evaluate this", "is this worth adopting", "should we use this", "thoughts on this" — invoke the evaluate-resource skill automatically. Do not wait for an explicit `/evaluate-resource` command.
