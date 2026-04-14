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
- Select the `stories/` folder inside `playbooks/`

### Step 2 — Install community plugins

In Obsidian, go to **Settings → Community plugins → Browse** and install the following:

| Plugin | What it enables | Required |
|--------|----------------|----------|
| [Templater](https://obsidian.md/plugins?id=templater-obsidian) | Auto-applies the chapter template (with auto-numbered filename) whenever you create a new file in `Chapters/` | Required |
| [LanguageTool Integration](https://obsidian.md/plugins?id=obsidian-languagetool-plugin) | Live grammar and style checking as you write; set your native language for second-language support | Recommended |
| [Editing Toolbar](https://obsidian.md/plugins?id=editing-toolbar) | Floating formatting toolbar; pre-configured with text, list, alignment, and insert commands | Recommended |
| [Smart Typography](https://obsidian.md/plugins?id=obsidian-smart-typography) | Converts straight quotes to curly, double-dash to em dash, and triple-dot to ellipsis as you type | Recommended |
| [Typing Transformer](https://obsidian.md/plugins?id=typing-transformer-obsidian) | Custom keystroke shortcuts; pre-configured with `***` → scene-break divider (`✽✽✽`) and other writing shortcuts | Recommended |
| [Better Word Count](https://obsidian.md/plugins?id=better-word-count) | Status bar showing word count and page count (at 300 words/page); replaces Obsidian's built-in word count | Recommended |
| [Iconize](https://obsidian.md/plugins?id=obsidian-icon-folder) | Adds icons to folders and files in the sidebar; pre-configured for `_Archive`, `_Templates`, `_Ideas`, `_Commands`, and `_Dashboard` | Recommended |
| [Outliner](https://obsidian.md/plugins?id=obsidian-outliner) | Improves list behaviour: better Tab/Enter handling, drag-and-drop reordering, cursor stays on bullet | Recommended |
| [Advanced Cursors](https://obsidian.md/plugins?id=advanced-cursors) | Multi-cursor support; adds Cmd/Ctrl+D to select and edit the next matching word — useful for renaming within a chapter | Recommended |
| [Pandoc Plugin](https://obsidian.md/plugins?id=obsidian-pandoc) | Export your story to DOCX, PDF, EPUB, and other formats directly from Obsidian | Recommended |

After installing each plugin, enable it. The settings for each plugin are already pre-configured in this vault — no manual setup needed.

> **LanguageTool:** If you write in English as a second language, go to **Settings → LanguageTool Integration** and set your native language in the **Mother tongue** field. This helps the plugin distinguish errors from stylistic choices.

> **Pandoc Plugin:** This plugin requires [Pandoc](https://pandoc.org/installing.html) to be installed on your system separately. Install Pandoc first, then install the Obsidian plugin. Once set up, use it to export finished chapters or full manuscripts to DOCX (for editors), EPUB (for ebook distribution), or PDF.

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
| `/update-chapter ch-XX` | Post-chapter state sync — updates Timeline, Characters, Locations (also works on single-file short stories) |
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
├── _Commands.md            Quick reference for all slash commands
├── _Dashboard.base         Story tracker — Active, In Revision, Completed, Abandoned
├── _Ideas.md               Idea scratchpad — source for /new-story
├── _Templates/             Obsidian templates (auto-applied by Templater)
├── _Archive/               Completed and abandoned stories
│   ├── Completed/
│   └── Abandoned/
│
├── My Novel/               Novel or novella — created by /new-story
│   ├── _Index.md           Story premise, themes, open questions
│   ├── _Lore.md            Detailed worldbuilding — rules, cosmology, factions
│   ├── _Lines.md           Reserved lines to place later in the draft
│   ├── CLAUDE.md           Story-specific rules (overrides vault CLAUDE.md)
│   ├── Timeline.md         Event tracking
│   ├── Quicknotes.md       Working notes and fragments
│   ├── Chapters/           One file per chapter (ch-01.md, ch-02.md, …)
│   ├── _Characters/        One file per character
│   │   └── _Index.md       Character roster and Bases view guidance
│   ├── _Locations/         One file per location
│   │   └── _Index.md       Location roster and Bases view guidance
│   ├── _Research/          Reference material
│   └── _Assets/            Cover images and design files
│
└── My Short Story/         Short story — leaner structure
    ├── _Index.md           Story premise and open questions
    ├── CLAUDE.md           Story-specific rules
    ├── Quicknotes.md       Working notes and fragments
    ├── my-short-story.md   The story itself (single file)
    └── _Characters/        Optional — only if the cast needs tracking
        └── _Index.md
```

---

## Notes on the writing-style skill

The `.claude/skills/writing-style/SKILL.md` file is the most powerful customisation available. Once populated, it tells Claude exactly how your prose works — your sentence rhythm, how you handle interiority, what your characteristic moves are, what should never be suggested. Without it, Claude gives generic feedback calibrated to competent fiction writing. With it, Claude gives feedback calibrated to *your* fiction writing.

To build it, share finished writing with Claude and say: *"Read this and build my writing-style skill from it."*
