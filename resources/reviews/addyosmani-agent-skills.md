---
title: "addyosmani/agent-skills: Production-grade engineering skills for AI coding agents"
url: https://github.com/addyosmani/agent-skills
author: "Addy Osmani"
date_evaluated: 2026-04-19
verdict: catalog
tags: [claude-code, skills, software-engineering, workflow, sdlc, spec-driven]
---

## What it proposes

A library of 20 SKILL.md files organised around a six-phase software development lifecycle (DEFINE, PLAN, BUILD, VERIFY, REVIEW, SHIP), activated by seven slash commands. Each skill is a structured process, not prose: it defines steps, checkpoints, and exit criteria. Three mechanisms distinguish it from a typical prompt collection:

- **Anti-rationalization tables.** Each skill enumerates the common excuses an agent would use to skip the step ("I'll test it all at the end", "it's faster to do it all at once") paired with documented counter-arguments. The table exists specifically to pre-empt agent shortcutting.
- **Non-negotiable verification gates.** Every skill terminates with an evidence requirement — passing tests, build output, runtime traces — and explicitly forbids "seems right" as a completion signal.
- **Progressive disclosure.** SKILL.md is the entry point; supporting references are loaded only when the workflow reaches them, keeping the context budget manageable.

Individual skills bake in established engineering practices (test pyramid 80/15/5, Hyrum's Law, Chesterton's Fence, trunk-based development, feature flags, Shift Left). Spec-driven-development enforces a gated SPECIFY → PLAN → TASKS → IMPLEMENT pipeline with human validation between phases; incremental-implementation enforces thin vertical slices with a compile-test-verify-commit loop. The library supports Claude Code, Cursor, Gemini CLI, Windsurf, OpenCode, Copilot, and Kiro.

## Best used when

- The project is a working software codebase where the agent routinely writes, tests, reviews, and ships production code across the full SDLC.
- The team wants a uniform skill vocabulary across multiple IDEs or CLIs and benefits from a single authoritative source.
- Agents have a track record of skipping verification or compressing multi-step workflows into one shot, and explicit anti-rationalization framing is needed to counter that.
- The codebase is large enough that spec-first and incremental-slice discipline pay back the ceremony cost.
- A team is building its own skill library and wants a reference implementation of the SKILL.md anatomy, gate pattern, and progressive-disclosure layering.

## Poor fit when

- The primary workload is non-engineering: research evaluation, long-form writing, content curation, or vault-based knowledge work. The full SDLC scaffolding adds ceremony with no matching payoff because there is no build, test, or ship phase to gate.
- A mature, personalised skill system already exists. Dropping in 20 opinionated skills risks colliding with established conventions on naming, routing, and verification; selective borrowing of patterns is lower-cost than wholesale adoption.
- The agent already reliably follows simplicity-first and verification-first norms through existing rules. The anti-rationalization tables then duplicate what is already enforced upstream.
- Projects where spec-driven gating would stall exploratory or prototype work that is explicitly meant to be cheap and disposable.

## Verdict

Catalog. This is a high-quality, well-structured reference for anyone running a full software engineering workflow through an AI coding agent, and the three mechanisms — anti-rationalization tables, non-negotiable evidence gates, and progressive disclosure — are genuinely worth studying even if the skills themselves are not adopted. For projects whose centre of gravity is software delivery, `adopt` is defensible. For projects whose centre of gravity is evaluation, writing, or knowledge work, the package as a whole is out of scope, but the structural patterns are instructive and worth mining when designing skills for any domain. The anti-rationalization table in particular is a transferable idea: it generalises to any skill where an agent is likely to cut corners, not just engineering ones. Keep for reference; do not install wholesale outside an engineering context.
