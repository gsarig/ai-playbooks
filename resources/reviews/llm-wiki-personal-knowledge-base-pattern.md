---
title: "LLM Wiki: Personal Knowledge Base Pattern"
url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
author: "Andrej Karpathy"
date_evaluated: 2026-04-10
verdict: adapt
tags: [knowledge-management, wiki, llm-maintenance, obsidian, markdown, rag-alternative]
---

## What it proposes

Instead of retrieving raw documents on every query (the standard RAG pattern), an LLM incrementally builds and maintains a persistent wiki of interlinked markdown files. The architecture has three layers: immutable raw sources (articles, papers, data files), an LLM-owned wiki layer (entity pages, concept pages, summaries, syntheses), and a schema document that codifies structure and workflows for the LLM to follow.

Three operations drive the system. Ingest processes a new source by reading it, writing a summary page, and updating 10-15 related wiki pages (entity pages, cross-references, contradiction flags). Query answers questions by searching an index file, synthesizing across wiki pages, and optionally filing valuable answers back into the wiki so exploration compounds. Lint periodically health-checks for orphan pages, stale claims, missing cross-references, and contradictions.

The key insight is that knowledge is compiled once and kept current, not re-derived on every query. The LLM absorbs the entire maintenance burden that causes humans to abandon wikis, while humans retain control over curation, direction, and judgment.

## Best used when

- The project accumulates knowledge over time from many sources and needs that knowledge organized rather than scattered. Research deep-dives, competitive analysis, course notes, and long-running reference collections are natural fits.
- The vault is primarily a knowledge base where the LLM is the authoritative writer of most content, and the human role is curation and inquiry rather than authorship.
- Sources arrive incrementally and each source should update a web of related pages, not just sit in a folder.
- The wiki is small to moderate in scale (up to a few hundred pages) where an index file can substitute for embedding-based search.
- The workflow benefits from a persistent, browsable artifact rather than ephemeral chat-based Q&A.

## Poor fit when

- The vault contains human-authored creative or editorial content where the LLM plays a supporting role. The pattern assumes the LLM owns the wiki layer entirely — in vaults where human prose is the core artifact and LLM-generated files are derived (e.g., continuity tracking maintained from a manuscript), the ownership model conflicts with the workflow.
- Sources are not primarily text documents. The pattern handles images only awkwardly, and non-textual sources require significant adaptation.
- The knowledge domain is fast-moving enough that the wiki becomes a liability. If sources are superseded frequently and the lint pass cannot keep up, the compiled wiki risks projecting stale confidence.
- There is no tolerance for LLM inaccuracies compounding silently. Because pages reference other LLM-written pages, an error in an early ingest can propagate through cross-references.

## Verdict

Adapt. The core mechanism is genuinely sound and solves a real problem: the maintenance burden that kills personal knowledge bases. For vault types where human-authored content is primary and LLM-generated files are derived artifacts under editorial constraints, the ownership model needs inverting. The three operations (ingest, query, lint) are portable and worth adopting individually. The indexing strategy (flat index.md plus append-only log.md) is practical and worth borrowing directly. The most transferable idea is filing query results back into the wiki — applicable even in vaults the LLM does not own.

## Related

- [@defileo on X](https://x.com/defileo/status/2042241063612502162) — a concrete implementation of this pattern using `claude -p --allowedTools Bash,Write,Read` per operation, making ingest/query/lint scriptable as shell aliases or cron jobs. No new methodology, but a useful confirmation that the pattern runs cleanly on the Claude Code CLI.
