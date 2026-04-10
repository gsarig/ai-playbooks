---
title: "WordPress Agent Skills"
url: https://github.com/WordPress/agent-skills
author: "WordPress (official organization)"
date_evaluated: 2026-04-10
verdict: catalog
tags: [ai-skills, wordpress, claude-code, portable-skills]
---

## What it proposes

A collection of portable, composable skill bundles that teach AI coding assistants (Claude Code, Cursor, Codex, and others) how to work effectively with the WordPress ecosystem. Each skill follows a consistent structure: a `SKILL.md` with structured instructions (trigger conditions, step-by-step procedures, verification checks, failure modes), a `references/` directory containing deep-dive documentation, and a `scripts/` directory with deterministic Node.js helpers for detection and validation. The skills cover the full breadth of WordPress development, from block and theme development to REST APIs, WP-CLI operations, performance profiling, and static analysis with PHPStan.

The design philosophy is worth noting independently of the WordPress domain. Skills are kept small and composable, with short top-level instruction files that delegate depth to reference documents. Deterministic scripts handle detection and validation rather than relying on the LLM to guess. A router skill classifies repositories and dispatches to the appropriate workflow skill. This layered architecture (router, triage, domain skills) is a well-considered pattern for organizing AI assistant knowledge.

## Best used when

The primary use case is WordPress plugin, theme, or block development assisted by an AI coding agent. The skills are most valuable when a developer works across multiple WordPress projects with different configurations (classic themes vs. block themes, custom plugins vs. full-site editing) and needs the AI assistant to reliably detect context and apply the right patterns. Teams maintaining several WordPress properties would benefit from installing these globally so that every project gets correct WordPress-aware assistance without per-repo configuration.

The structural patterns (composable skill directories, router-based dispatching, deterministic validation scripts, canonical upstream docs as the source of truth) are independently valuable as a reference for anyone designing their own skill libraries for AI assistants, regardless of domain.

## Poor fit when

The skills are narrowly scoped to WordPress development. Projects that do not involve WordPress (fiction writing workflows, knowledge management vaults, personal organization systems, non-WordPress web development) will get no direct benefit from installing them. The skills also require a Node.js build step, which adds friction for environments where Node.js tooling is not already part of the workflow. The skills target WordPress 6.9+ and were generated using GPT-5.2 Codex, so they carry assumptions about both the WordPress version and the AI model capabilities that may not transfer cleanly to other contexts.

For non-developers or users whose AI-assisted workflows center on content creation, note-taking, or vault management rather than software engineering, these skills solve a problem that simply does not exist in their workflow.

## Verdict

Catalog. This is a well-designed, officially maintained skill library for WordPress development, and the structural patterns it uses (small composable skills, router-based dispatching, deterministic scripts for validation, depth pushed into reference documents) are genuinely instructive for anyone building AI assistant skill systems. However, the content is entirely WordPress-specific. For projects outside the WordPress ecosystem, there is nothing to adopt or adapt; the skills simply do not apply. Worth knowing about as a reference for skill architecture, and worth revisiting if WordPress development ever enters scope.
