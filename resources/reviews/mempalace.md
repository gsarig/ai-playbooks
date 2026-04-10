---
title: "MemPalace"
url: https://github.com/milla-jovovich/mempalace
author: "milla-jovovich"
date_evaluated: 2026-04-10
verdict: watch
tags: [memory, mcp, chromadb, claude-code, local-first]
---

## What it proposes

MemPalace is a local AI memory system that stores conversation and project data verbatim in ChromaDB, organized into a hierarchical namespace (wings, halls, rooms, closets, drawers). It exposes 19 MCP tools so that Claude Code, Cursor, or ChatGPT can read and write memories during a session. Auto-save hooks capture context at session boundaries (Stop and PreCompact events in Claude Code). A SQLite-backed temporal knowledge graph tracks entity-relationship triples with validity windows, enabling queries like "what was true about X between date A and date B."

The core design choice is raw verbatim storage with no LLM summarization at ingest. Retrieval relies on ChromaDB's vector similarity search, filtered by the hierarchical metadata (wing, hall, room). This achieves 96.6% R@5 on the LongMemEval benchmark in raw mode, a score that has been independently reproduced without any API calls. An experimental lossy compression dialect called AAAK exists but currently regresses retrieval accuracy to 84.2%, making it counterproductive at present.

## Best used when

- A project accumulates enough conversational context that Claude Code's built-in memory (`~/.claude/projects/`) becomes insufficient; for example, long-running multi-month efforts where facts, decisions, and rationale need to survive across hundreds of sessions.
- Cross-project memory sharing matters. The wing/room hierarchy allows one memory store to serve multiple workstreams while keeping them logically separated.
- Temporal queries are valuable. If a workflow requires knowing what was believed or decided at a specific point in time (not just the latest state), the temporal knowledge graph is a differentiating feature that built-in memory does not offer.
- The environment is local-only. MemPalace requires no cloud services or API keys for its core storage and retrieval loop.

## Poor fit when

- The built-in Claude Code memory system already covers the project's needs. For most single-vault or single-project workflows, the native `CLAUDE.md` and project memory files are simpler, require no extra dependencies, and integrate without configuration. Adding MemPalace in these cases introduces operational overhead (ChromaDB process, SQLite database, MCP server) with no clear retrieval benefit.
- The project runs on macOS ARM64, where a known segfault (#74) remains unresolved.
- Security matters. A shell injection vulnerability in the auto-save hooks (#110) is documented but unfixed. Any workflow that runs hooks automatically in an environment with untrusted input is exposed until this is patched.
- ChromaDB version pinning (#100) is absent, meaning a dependency update could silently break storage or retrieval without warning.
- The AAAK compression feature is needed for token savings. It currently performs worse than raw mode and its earlier savings claims were overstated. The "+34% palace boost" metric reflects standard ChromaDB metadata filtering, not a novel mechanism.

## Verdict

MemPalace demonstrates a strong core idea: verbatim local storage with hierarchical namespacing and temporal awareness, backed by a genuine 96.6% benchmark score. However, several factors prevent recommending it for production use today. The unpatched shell injection bug (#110) is a real security risk in any automated hook workflow. The unpinned ChromaDB dependency makes reproducible installs unreliable. The contradiction detection module exists in the codebase but is not wired into knowledge graph operations, leaving a gap in data integrity. Claude Code's built-in memory system handles the common case (single-project, session-to-session continuity) well enough that MemPalace's added complexity needs a clear justification, which only emerges for long-running, multi-project, or temporally complex workflows. The project is worth revisiting once the security issue is resolved, dependencies are pinned, and the knowledge graph integration is complete. Until then, the verdict is **watch**.
