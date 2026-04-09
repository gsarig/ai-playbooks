# ai-playbooks

A collection of standalone workflow blueprints for AI-assisted creative and knowledge work. Each playbook is a self-contained folder you can use as an Obsidian vault, pre-configured with Claude Code commands, Obsidian settings, and plugin configurations.

## Playbooks

| Playbook | Description |
|----------|-------------|
| [playbooks/stories/](playbooks/stories/) | Fiction writing workflow — novels, novellas, and short stories |

## Resources

The [`resources/`](resources/) folder contains evaluated external methodologies and patterns — things worth knowing about, with documented reasoning on whether and how to adopt them. Each entry includes a verdict (`adopt`, `adapt`, `skip`, or `watch`) and the reasoning behind it.

These are not a link dump. The evaluation is the artifact.

## Philosophy

These playbooks are not templates in the traditional sense. They are structured workflows where Claude Code acts as a collaborator: tracking story state, running editing passes, flagging inconsistencies, and managing file scaffolding through slash commands.

Each playbook is designed to be:
- **Standalone** — everything needed is in the folder, no external dependencies
- **Cross-platform** — works on Windows, macOS, and Linux
- **Customisable** — the AI instructions are plain text files you can read and edit

## Requirements

All playbooks require:
- [Obsidian](https://obsidian.md) — free note-taking app
- [Claude Code](https://claude.ai/code) — Anthropic's AI coding assistant (also works for writing)

Each playbook's `README.md` lists any additional plugins required.

## evaluate-resource skill

The repo ships with an `/evaluate-resource` skill. Point it at any methodology or workflow URL and it will draft a structured evaluation for your review, then store it in `resources/`.

See `.claude/skills/evaluate-resource/context.example.md` for how to configure it with your personal vault context.
