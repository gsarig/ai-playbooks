---
title: "How Claude Code works in large codebases: Best practices and where to start"
url: https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
author: "Anthropic Applied AI team"
date_evaluated: 2026-05-16
verdict: adapt
tags: [claude-code, harness, codebase-navigation, agentic-search, skills, hooks, mcp, plugins, enterprise]
---

## What it proposes

A reference model for configuring Claude Code in large, established codebases, framed around two ideas. First, agentic search: Claude navigates the live filesystem with reads, greps, and reference-following rather than querying a prebuilt embedding index, which sidesteps the staleness problems that RAG-style coding tools hit at scale. Second, the harness as the dominant performance lever: the model is one input, but the surrounding configuration determines what Claude can actually do.

The harness is decomposed into seven extension points, layered in a deliberate order: CLAUDE.md files (broad-scope context, layered by directory), hooks (deterministic checks plus self-improving stop/start hooks that propose context updates), skills (progressive-disclosure expertise scoped to paths), plugins (bundled skills/hooks/MCP for organizational distribution), LSP integrations (symbol-level navigation instead of text matching), MCP servers (structured access to internal tools and data), and subagents (isolated context windows for exploration that return only results).

It also prescribes three operational patterns: keep the codebase navigable (lean layered CLAUDE.md, subdirectory init, per-folder test/lint commands, ignore files and permission denies, codebase maps, LSP); actively maintain CLAUDE.md every three to six months because instructions written for one model can constrain a future one; and assign a single owner ("agent manager" or DRI) for configuration, permissions, marketplace, and conventions.

## Best used when

Working in repositories where Claude Code's defaults underperform: deep directory trees, mixed languages, per-subdirectory build and test commands, or code that lacks a single coherent root. The CLAUDE.md layering and per-directory init guidance apply equally to solo vault setups with multiple distinct sub-domains. The harness decomposition is useful any time the question "where should this rule live: context, hook, skill, or plugin?" comes up, regardless of team size. The agentic-search framing is also a clean argument to point at when comparing Claude Code to index-based alternatives.

## Poor fit when

The enterprise-rollout half of the article (agent managers, managed marketplaces, regulated-industry phased access, bottoms-up adoption fragmentation) assumes an organization with multiple engineers and a central platform team. Solo operators can skip that material entirely. The plugin-marketplace pattern is overkill when there is no second consumer of the bundles. The "review configuration every three to six months" cadence is sound but the trigger should be model upgrades and observed friction, not a calendar. LSP integration recommendations matter for compiled languages and large polyglot repos; for vault-style projects that are mostly markdown and shell scripts, the payoff is small.

## Verdict

Adapt. The harness taxonomy is the most useful contribution: seven extension points with a clear ordering and a one-line job description for each is a better mental model than the usual flat list, and it generalizes well beyond enterprise contexts. The agentic-search-vs-RAG framing is durable and worth internalizing because it explains why investments in CLAUDE.md hygiene, codebase maps, and ignore files pay off, while investments in external indices do not. Lift the layered-context and per-subdirectory-init patterns, the stop-hook-as-self-improvement idea, and the periodic configuration review. Drop the agent-manager role, the managed marketplace, and the regulated-rollout playbook unless and until there is a team to roll out to. The article pairs cleanly with the existing Codex "harness engineering" review: that one supplies the legibility-and-enforcement frame (plans as artifacts, lints as invariants, per-worktree app stacks), this one supplies the Claude-Code-specific extension surfaces and how they compose.
