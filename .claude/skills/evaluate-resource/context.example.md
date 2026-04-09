# evaluate-resource — personal context

This file gives the evaluate-resource skill additional context about your setup, so the "How it maps to our setup" and "Where we'd diverge" sections reflect your actual situation rather than the project in isolation.

Create a copy of this file named `context.md` (gitignored) and fill it in. Two options:

---

## Option A — Inline context

List your vaults, their purpose, and any relevant details directly here.

Example:

```
## My vaults

- **stories** (`/path/to/stories`) — fiction writing, novels and short stories
- **plants** (`/path/to/plants`) — plant care tracking and notes
- **personal** (`/path/to/personal`) — journal, tasks, general notes

## My setup

- Claude Code with memory system at ~/.claude/projects/
- Obsidian for all vaults
- Running on [OS]
```

---

## Option B — Pointer to dotfiles (recommended if you maintain a dotfiles repo)

Instead of duplicating information here, point to a file in your dotfiles:

```
See /path/to/your/dotfiles/claude/evaluate-resource-context.md
```

The skill will follow the pointer and read that file. This way you maintain one source of truth and this file stays minimal.
