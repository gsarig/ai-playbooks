---
title: "Obsidian Mind"
url: https://github.com/breferrari/obsidian-mind
author: "Brenno Ferrari"
date_evaluated: 2026-04-11
verdict: catalog
tags: [memory, obsidian, claude-code, vault-template, career-tracking, performance-reviews, session-lifecycle, hooks]
---

## What it proposes

A complete, opinionated Obsidian vault template that gives AI coding agents persistent memory across sessions, with a heavy focus on workplace career management. The vault ships with a predefined folder structure (work projects, org charts, performance tracking, 1:1 notes, brag docs, competency frameworks), 18 slash commands, 9 subagents, and 5 lifecycle hooks that automatically inject context at session start, classify user input on every message, validate note formatting after writes, back up transcripts before compaction, and run cleanup at session end.

The core mechanism is vault-first memory: all durable knowledge lives in human-readable, git-tracked markdown files organized by purpose (brain, work, org, perf), while the agent's own memory file serves only as an index pointing into the vault. Sessions follow a designed lifecycle where startup loads goals, active projects, recent changes, and open tasks; every message gets classified and routed to the appropriate note type (decision, incident, win, 1:1, architecture); and wrap-up verifies link integrity and updates indexes. Token efficiency comes from tiered loading, where only a small context payload is injected at startup and heavier reads happen on demand via QMD semantic search.

The system also supports Codex CLI and Gemini CLI through shared hook scripts mapped to each agent's configuration format.

## Best used when

The vault operator works in a corporate or team environment with regular 1:1 meetings, formal performance review cycles, competency frameworks, incident tracking, and cross-team collaboration. The system is purpose-built for someone who needs to accumulate evidence for self-reviews and peer reviews, track decisions across projects, maintain relationship context for colleagues and managers, and synthesize weekly patterns from daily work. It thrives when the user's primary pain point is losing institutional context between sessions and wants a turnkey system rather than building one from scratch.

It also suits users who want multi-agent support across Claude Code, Codex CLI, and Gemini CLI with a single vault and shared hook infrastructure.

## Poor fit when

The vault's domain is narrowly scoped to workplace career management. Projects that involve creative writing, personal knowledge management, research, hobby tracking, or any non-corporate workflow would inherit a large amount of unused structure (performance competencies, brag docs, org charts, 1:1 templates, incident docs) that adds cognitive overhead without payoff. The 18 commands and 9 subagents are almost entirely career-focused; adapting them to a different domain would mean rewriting most of the system rather than trimming edges.

The opinionated folder structure also resists customization. Because the hooks, commands, and subagents all assume specific paths and note schemas (frontmatter fields, section headings, linking conventions), changing the structure means updating the entire automation layer. For users who already have an established vault with its own conventions, migration would be high-friction, and the vault-upgrade command is designed for importing content into this system's schema rather than adapting the system to an existing one.

Finally, the session lifecycle hooks inject context on every startup and classify every message, which adds latency and token cost that only pays off if the career-tracking features are actually being used.

## Verdict

**Catalog.** Obsidian Mind is a well-engineered, comprehensive system for its specific domain: giving AI agents persistent memory in the context of corporate career management. The hook-driven session lifecycle, tiered token loading, and multi-agent support are genuinely thoughtful design choices. However, the vault is so thoroughly specialized for workplace performance tracking, 1:1s, incident management, and review-season preparation that it functions more as a domain-specific product than a generalizable pattern. The underlying ideas (vault-first memory, session lifecycle hooks, tiered context injection, content classification routing) are worth studying, but they are inseparable from the career-management scaffolding without significant rework. For users whose vaults serve different purposes, this is a good reference implementation to learn from but not a practical starting point. It earns a place in the catalog as a strong example of agent-augmented vault design in its niche.
