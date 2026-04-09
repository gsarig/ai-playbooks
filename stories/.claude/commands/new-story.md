Begin by checking whether a title was passed as an argument ("$ARGUMENTS").

---

## Step 0 — Choose a path

If no argument was given, present the following options to the author and wait for their choice before doing anything else:

> **Starting a new story. How would you like to proceed?**
>
> 1. **From an idea** — scaffold from a specific idea in `_Ideas.md`
> 2. **Empty novel / novella** — create the full structure with blank files, ready to fill in
> 3. **Short story** — create a lean structure with a single prose file

If a title argument was given, go directly to **Option 1** and skip the menu.

---

## Option 1 — Scaffold from `_Ideas.md`

### 1a — Find the idea

Read `_Ideas.md` from the vault root.

Ideas are separated by `---` (horizontal rule). Each idea has a `##` heading as its title. Parse the file into individual idea blocks using `---` as the boundary.

- If a title argument was given: find the block whose `##` heading matches (case-insensitive, partial match acceptable). If no match, tell the author and list available titles.
- If no title argument was given: list all idea titles found and ask the author which one to use. Wait for their answer before continuing.

### 1b — Extract and remove

Once the target idea is identified:

1. Copy its full content (heading + body) — this becomes the story's `Quicknotes.md`.
2. Remove the idea block from `_Ideas.md`, including its surrounding `---` separators (but do not leave a double `---` gap or a dangling separator). Write the cleaned file back.

### 1c — Understand the premise

Read the extracted content carefully. The notes may be in any language (including Greek — translate internally, the story will be in English). Extract:

- Story title (use the `##` heading, or propose a refinement if the heading is vague)
- **Approximate form: short story / novella / novel** — ask if unclear
- Genre
- Core premise (1–3 sentences)
- Known characters and any details
- Known locations
- Known world rules or lore
- Structural ideas (ending, key scenes, themes, narrative structure)
- Open questions (things still undecided)

Present your understanding to the author. Confirm the story title and form before building anything.

### 1d — Build the structure

**For novels and novellas**, create inside `{Story Title}/`:

```
{Story Title}/
├── _Index.md          (populated from the idea notes)
├── CLAUDE.md          (populated from world rules and tone notes)
├── Timeline.md        (format chosen based on story structure — see Timeline rules below)
├── Quicknotes.md      (the extracted idea content, preserved verbatim)
├── Chapters/
│   └── ch-01.md       (empty chapter file with frontmatter, no prose)
├── _Characters/
│   └── _Index.md      (Bases setup + any characters mentioned in the notes)
├── _Locations/
│   └── _Index.md      (Bases setup + any locations mentioned in the notes)
├── _Research/
└── _Assets/
```

**For short stories**, create inside `{Story Title}/`:

```
{Story Title}/
├── {Story Title}.md   (the story itself — blank, ready to write)
├── _Index.md          (premise, themes, lore, open questions)
├── CLAUDE.md          (world rules and tone — may be minimal)
├── Quicknotes.md      (the extracted idea content, preserved verbatim)
├── _Characters/
│   └── _Index.md      (only if characters were mentioned in the notes)
└── _Assets/
```

No `Chapters/`, no `Timeline.md`, no `_Locations/` for short stories unless the notes suggest they're needed.

---

## Option 2 — Empty novel / novella

Ask for the story title if not already provided. Wait for the answer.

Create the following inside `{Story Title}/`. All files are minimal — frontmatter and section headers only. Do not invent any content.

```
{Story Title}/
├── _Index.md
├── CLAUDE.md
├── Timeline.md
├── Quicknotes.md      (empty — just a heading)
├── Chapters/
│   └── ch-01.md       (empty chapter file with frontmatter, no prose)
├── _Characters/
│   └── _Index.md
├── _Locations/
│   └── _Index.md
├── _Research/
└── _Assets/
```

**`_Index.md`** — include the title and status in frontmatter, placeholder sections for premise, themes, world rules, and open questions. Nothing filled in.

**`CLAUDE.md`** — include the standard section headers (Story Identity, World Rules, Character Voice Guidelines, Developmental Focus, Open Rules) with everything blank.

**`Timeline.md`** — include a note that the format should be decided when the story's structure is clearer, and a placeholder for the first strand.

**`_Characters/_Index.md`** and **`_Locations/_Index.md`** — Bases setup instructions only (see Option 1 for the format).

---

## Option 3 — Empty short story

Ask for the story title if not already provided. Wait for the answer.

Create a lean structure. No `Chapters/`, no `Timeline.md`, no `_Locations/`.

```
{Story Title}/
├── {Story Title}.md   (blank prose file — just a title heading)
├── _Index.md          (frontmatter + placeholder sections, nothing filled in)
├── CLAUDE.md          (minimal — section headers only)
├── Quicknotes.md      (empty — just a heading)
└── _Assets/
```

No `_Characters/` unless the author mentions the story has notable characters. Ask if unsure.

---

## Timeline format rules (Option 1 novels only)

Choose the format based on the story's structure:

- **Linear narrative:** standard table — `Story Date | Chapter | Event | Characters | Location | Notes`
- **Non-linear, parallel timelines, or flashback-heavy:** grouped list — events grouped by strand or character, with notes on temporal position and how strands connect
- **Circular or paradoxical structure:** minimal reference list only — note explicitly that timeline order is the story's central conceit

---

## Chapter file format (ch-01.md)

All chapter files use this frontmatter:

```yaml
---
chapter: 1
title: ""
status: draft
edit_pass: 0
wordcount:
pov:
timeline_events: []
locations: []
characters: []
tags:
  - chapter
cssclasses:
  - chapter
---
```

Leave the title field empty — the author fills it in when they have one.

---

## Step — Report

When everything is created, present a brief summary:
- What was built
- What is empty and needs filling in
- Any open questions that should be resolved before writing begins
