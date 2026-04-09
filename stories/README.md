# Stories Playbook

A fiction writing workflow for Obsidian and Claude Code. Works for novels, novellas, and short stories.

Claude Code acts as a writing collaborator: scaffolding story structure, tracking characters and locations, running developmental and language editing passes, flagging continuity errors, and managing the state of your story as it evolves.

---

## What you get

- Slash commands for every stage of the writing process (`/new-story`, `/dev-edit`, `/language-edit`, and more)
- Automatic story scaffolding from rough notes or ideas
- Per-chapter state tracking (characters, locations, timeline, word count)
- Three-pass language editing calibrated to your voice
- Consistency audits across all chapters
- Publication prep when you're ready to ship

---

## Requirements

- [Obsidian](https://obsidian.md) — free, available on Windows, macOS, Linux, iOS, Android
- [Claude Code](https://claude.ai/code) — Anthropic's AI assistant for the command line

---

## Setup

### Step 1 — Open this folder in Obsidian

Download or clone this repository. Open the `stories/` folder as an Obsidian vault:

- Launch Obsidian
- Click **Open folder as vault**
- Select the `stories/` folder

### Step 2 — Install community plugins

In Obsidian, go to **Settings → Community plugins → Browse** and install the following:

| Plugin | Purpose | Required |
|--------|---------|----------|
| [Templater](https://obsidian.md/plugins?id=templater-obsidian) | Auto-applies chapter template when you create a new file in `Chapters/` | Required |
| [LanguageTool Integration](https://obsidian.md/plugins?id=obsidian-languagetool-plugin) | Grammar and style checking as you write | Required |
| [Editing Toolbar](https://obsidian.md/plugins?id=editing-toolbar) | Formatting toolbar in the editor | Required |
| [Smart Typography](https://obsidian.md/plugins?id=obsidian-smart-typography) | Curly quotes, em dashes, ellipsis — auto-converted as you type | Required |
| [Typing Transformer](https://obsidian.md/plugins?id=typing-transformer-obsidian) | Custom text conversion rules | Required |

After installing each plugin, enable it. The settings for each plugin are already pre-configured in this vault — no manual setup needed.

> **LanguageTool:** If you write in English as a second language, go to **Settings → LanguageTool Integration** and set your native language in the **Mother tongue** field. This helps the plugin distinguish errors from stylistic choices.

### Step 3 — Configure Claude Code

Open a terminal in the `stories/` folder and run:

```
claude
```

Claude Code will read the `CLAUDE.md` in this vault and be ready to use the slash commands.

### Step 4 — Personalise

Two files are designed for you to customise before writing:

**`CLAUDE.md`** — Edit the **Author** section to describe your language background (if writing in a second language). This calibrates the language editing passes.

**`.claude/skills/writing-style/SKILL.md`** — Your personal aesthetic profile. Leave it blank for now and fill it in after your first story, or ask Claude to build it from writing samples you share.

---

## First steps

Once everything is set up, open Claude Code in the vault folder and try:

```
/new-story
```

Claude will ask whether you want to scaffold from an idea in `_Ideas.md`, start an empty novel structure, or start a short story.

---

## Commands

| Command | Purpose |
|---------|---------|
| `/new-story` | Build a story blueprint from an idea or from scratch |
| `/continue-story` | Re-entry brief for returning to a story after time away |
| `/update-chapter ch-XX` | Post-chapter state sync — updates Timeline, Characters, Locations |
| `/dev-edit ch-XX` | Developmental editing pass on a chapter |
| `/language-edit ch-XX 1\|2\|3` | Language and grammar pass (three passes) |
| `/audit-story` | Full consistency audit across all chapters |
| `/publish-prep` | Create promo files and publication record |
| `/archive-story` | Move a completed or abandoned story to the archive |

---

## Folder structure

```
stories/
├── CLAUDE.md               Global writing rules for Claude
├── _Ideas.md               Idea scratchpad — source for /new-story
├── _Templates/             Obsidian templates (auto-applied by Templater)
├── _Archive/               Completed and abandoned stories
│   ├── Completed/
│   └── Abandoned/
└── {Story Title}/          Created by /new-story
    ├── _Index.md           Story premise, themes, open questions
    ├── CLAUDE.md           Story-specific rules (overrides vault CLAUDE.md)
    ├── Timeline.md         Event tracking
    ├── Quicknotes.md       Working notes and fragments
    ├── Chapters/           One file per chapter (ch-01.md, ch-02.md, …)
    ├── _Characters/        One file per character
    ├── _Locations/         One file per location
    ├── _Research/          Reference material
    └── _Assets/            Cover images and design files
```

---

## Notes on the writing-style skill

The `.claude/skills/writing-style/SKILL.md` file is the most powerful customisation available. Once populated, it tells Claude exactly how your prose works — your sentence rhythm, how you handle interiority, what your characteristic moves are, what should never be suggested. Without it, Claude gives generic feedback calibrated to competent fiction writing. With it, Claude gives feedback calibrated to *your* fiction writing.

To build it, share finished writing with Claude and say: *"Read this and build my writing-style skill from it."*
