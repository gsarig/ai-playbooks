---
title: "Graphify"
url: https://github.com/safishamsi/graphify
author: "Safi Shamsi"
date_evaluated: 2026-04-10
verdict: watch
tags: [knowledge-graph, claude-code, code-navigation, markdown, multimodal]
---

## What it proposes

Graphify is a Claude Code skill that builds a queryable knowledge graph from any folder of code, documents, markdown, images, or papers. It works in two passes: a deterministic AST pass (tree-sitter, 20 languages) extracts structural relationships from code without an LLM, then parallel LLM subagents extract concepts, relationships, and design rationale from non-code files, including images via multimodal vision. Results merge into a NetworkX graph clustered with Leiden community detection (topology-based, no embeddings). Outputs include an interactive HTML graph, a report identifying hub nodes and surprising connections, a persistent JSON graph file, and a SHA256-based cache so re-runs only process changed files. Relationships are tagged as extracted, inferred (with confidence scores), or ambiguous (flagged for review).

A notable integration feature: it installs a PreToolUse hook in Claude Code that fires before every Glob/Grep call, reminding the agent to consult the graph report and navigate by structure rather than keyword search. The project claims a 71.5x token reduction per query compared to reading raw files.

## Best used when

- A project contains a large, interconnected codebase where understanding call graphs, module boundaries, and cross-cutting concerns matters more than reading individual files.
- A folder accumulates heterogeneous research material (papers, screenshots, notes, code snippets) and the primary goal is surfacing structural relationships between them for an LLM agent to navigate.
- The workflow is code-heavy and the knowledge graph's AST pass (its strongest, deterministic layer) has material to work with.
- Session continuity matters: the persistent graph and cache make repeated queries across sessions cheaper.

## Poor fit when

- The corpus is primarily long-form prose (fiction, essays, narrative documentation) where relationships are semantic and sequential rather than structural. AST parsing contributes nothing, and the LLM-inferred relationship layer is the only one operating — reducing the tool to an expensive summarization step with graph dressing.
- The vault is small enough (under a few dozen files) that an LLM agent can already navigate it efficiently with direct file reads. The overhead of graph generation, hook installation, and an additional dependency outweighs the benefit.
- Content is organized by a human-maintained taxonomy (folders, tags, links) that already encodes the relationships Graphify would infer. Adding a parallel auto-generated graph risks conflicting with or duplicating that structure.
- The workflow prioritizes human authorship and uses LLMs only for derived reference files. A persistent hook that intercepts every search call inserts an opinionated navigation layer that may interfere with simpler, intentional file access patterns.
- Privacy or resource constraints make running parallel LLM subagent calls over every document in a vault undesirable.

## Verdict

Graphify solves a real problem well for large, code-heavy projects where structural navigation saves significant tokens and time. Its deterministic AST layer is genuinely valuable, and the persistent graph with caching is a sound design. For markdown-first vaults centered on long-form prose, reference material, and human-maintained linking, the tool's strongest features have little to work with, and what remains is an LLM-inferred relationship layer that adds cost and complexity without a clear advantage over native vault organization. The always-on PreToolUse hook is also a concern for simpler workflows where direct file access is preferred. Worth revisiting if the project adds more granular hook control (opt-in per session rather than always-on) or if a vault grows to include substantial code or mixed-media research material where structural discovery becomes the bottleneck.
