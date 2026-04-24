---
title: "Basic Memory"
url: https://github.com/basicmachines-co/basic-memory
author: "Basic Machines"
date_evaluated: 2026-04-23
verdict: adapt
tags: [memory, mcp, markdown, obsidian, knowledge-graph, local-first, semantic-search, sqlite]
---

## What it proposes

A local-first persistent memory layer for LLMs, exposed via the Model Context Protocol. Knowledge lives in plain Markdown files on disk; a SQLite index plus optional vector embeddings make those files searchable and traversable. Each file is treated as an Entity. Inside a file, bullet lines following semantic patterns become structured data: `- [category] content #tag` entries become Observations, and `- relation_type [[WikiLink]]` entries become Relations, together forming a knowledge graph across the vault.

The MCP server exposes note CRUD (`write_note`, `read_note`, `edit_note`, `move_note`, `delete_note`), graph traversal via `memory://` URLs (`build_context`), hybrid full-text plus vector `search_notes`, `list_directory`, `recent_activity`, multi-project management, and a canvas visualization tool. Both the user and the LLM read and write the same files, so edits made manually in Obsidian and edits made by Claude stay in the same substrate. Installation is a single `uv tool install` plus an MCP config entry. Cloud sync is optional and paid; nothing in the local workflow depends on it. License is AGPL-3.0.

## Best used when

- A vault is already Markdown-based and edited manually, and the goal is to let an LLM read, append, and cross-link notes without a separate storage layer.
- The workflow benefits from a queryable knowledge graph across entries (people, projects, recurring topics) rather than flat note retrieval.
- Multiple MCP-compatible clients (desktop chat, editor, IDE) need to share the same memory source of truth.
- Semantic structure (categories, tags, typed relations) is worth the small authoring overhead because retrieval precision matters.
- Knowledge must remain fully on local disk with no mandatory cloud dependency.

## Poor fit when

- The agent in use already has its own persistent memory at the tool level and the goal is session-to-session continuity inside that tool; adding an MCP memory layer duplicates responsibility and splits the record.
- The vault is purely narrative or long-form prose where the Observation/Relation bullet syntax would pollute the text.
- The workflow is single-shot task execution with no accumulated state worth querying later.
- AGPL-3.0 conflicts with downstream licensing requirements (relevant only if redistributing or embedding the server itself, not for personal use).
- The intended retrieval pattern is token-reduction for large codebases rather than cross-session knowledge recall; other tools target that problem more directly.

## Verdict

Adapt. This is the most coherent local-first, MCP-native memory system currently available: Markdown as the primary substrate, Obsidian-compatible, a real knowledge graph rather than an opaque vector store, and no security blockers of the kind that sink comparable projects. The friction is the semantic bullet syntax, which pays off for structured domains (tracking, reference, project logs) but is noise in prose vaults. The right adoption pattern is per-vault rather than universal: wire it into vaults where typed observations and cross-entity relations are genuinely useful, and leave narrative or single-purpose vaults alone. Treat its memory as complementary to, not a replacement for, any agent-native persistent memory already in play — pick one as the source of truth per workflow to avoid drift.
