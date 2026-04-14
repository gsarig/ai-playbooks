# ai-playbooks

A collection of standalone workflow blueprints for AI-assisted creative and knowledge work. Each playbook is a self-contained folder you can use as an Obsidian vault, pre-configured with Claude Code commands, Obsidian settings, and plugin configurations.

## Playbooks

| Playbook | Description |
|----------|-------------|
| [playbooks/stories/](playbooks/stories/) | Fiction writing workflow — novels, novellas, and short stories |
| [playbooks/resource-library/](playbooks/resource-library/) | Scaffold for a personal evaluated resource library, powered by the evaluate-resource skill |
| [playbooks/plant-health-tracker/](playbooks/plant-health-tracker/) | AI-powered plant health monitor — drop photos into a staging folder, get per-plant reports and a live dashboard in Obsidian |

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

Optional, for the resource library workflow:
- [Obsidian Web Clipper](https://obsidian.md/clipper) — browser extension to clip web pages directly into your vault

Each playbook's `README.md` lists any additional plugins required.

## evaluate-resource skill

The repo ships with an `/evaluate-resource` skill. Drop a URL into the chat with any evaluative phrase ("what do you think", "evaluate this") and it will spawn an Opus subagent, draft a structured evaluation, present it for your approval, then write the file to `resources/reviews/`.

The skill is designed to be portable — you can use it in any project with your own context:

1. Copy `.claude/skills/evaluate-resource/context.example.md` to `context.md` in the same folder (it is gitignored)
2. Fill in your own vault or project context, or point to a file in your dotfiles
3. Drop a URL in the chat with any evaluative phrase and the skill triggers automatically

The evaluations in this repo reflect a specific setup (see [resources/README.md](resources/README.md)), but the skill itself works for any project. The verdict taxonomy and conditions-for-fit framing are general enough to apply to any domain.
