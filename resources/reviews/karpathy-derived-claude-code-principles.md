---
title: "Karpathy-Derived Claude Code Principles"
url: https://github.com/forrestchang/andrej-karpathy-skills
author: "Forrest Chang (derived from Andrej Karpathy)"
date_evaluated: 2026-04-14
verdict: skip
tags: [claude-code, prompt-engineering, claude-md, coding-discipline]
---

## What it proposes

A single CLAUDE.md file (installable as a Claude Code plugin or copied into a project) that encodes four behavioral principles for LLM-assisted coding: (1) Think Before Coding, which tells the model to surface assumptions, present alternatives, and ask when confused; (2) Simplicity First, which forbids speculative abstractions, unnecessary features, and bloated code; (3) Surgical Changes, which constrains edits to the task at hand and distinguishes between orphans created by the current change versus pre-existing dead code; (4) Goal-Driven Execution, which reframes imperative instructions as verifiable success criteria (write a failing test, then make it pass).

The resource packages Andrej Karpathy's observations about common LLM coding failures into actionable CLAUDE.md rules. The mechanism is straightforward: place behavioral constraints in the model's instruction context so it self-corrects against known failure modes.

## Best used when

Starting a new Claude Code setup from scratch with no existing behavioral rules. The file serves as a reasonable baseline for teams or individuals who have not yet written their own CLAUDE.md and want a curated starting point that addresses the most common LLM coding pitfalls. It is also useful as a checklist when auditing an existing ruleset for gaps.

## Poor fit when

The user already maintains a mature CLAUDE.md with rules covering the same territory. The four principles map almost entirely onto rules that experienced Claude Code users tend to arrive at independently: plan before implementing complex tasks, avoid speculative abstractions, do not make drive-by edits, and surface uncertainty rather than guessing. Layering this file on top of an existing ruleset creates duplication without adding new behavioral constraints. The "Goal-Driven Execution" principle (reframe tasks as testable goals) is the one idea with slightly less overlap, but it is a single paragraph of advice, not a mechanism that justifies adopting the whole file.

Additionally, the resource is a static snapshot of fairly generic advice. It does not evolve, does not address domain-specific concerns (vault workflows, cross-project consistency, CI integration), and offers no tooling beyond the rules themselves.

## Alternatives

Any well-maintained personal or team CLAUDE.md that has been iteratively refined through real usage will supersede this resource. The value of CLAUDE.md rules comes from specificity and iteration; generic principles lose their edge once a user has encountered the same failure modes firsthand and written tighter, context-aware rules. For users who lack a starting point, Anthropic's own Claude Code documentation and the community-maintained awesome-claude-code lists provide broader and more frequently updated baselines.

## Verdict

Skip. The four principles are sound but generic, and anyone who has used Claude Code seriously for more than a few weeks will have already encoded equivalent (or more specific) rules in their own CLAUDE.md. The resource solves a real onboarding problem for new Claude Code users, but as a candidate for a resource library aimed at practitioners with established workflows, it offers no incremental value. The "Goal-Driven Execution" reframing is the most distinctive idea, but it amounts to a single paragraph of advice that can be absorbed in a sentence: tell the model what success looks like, not what steps to take. There is nothing here worth maintaining a reference to when the underlying insight is already well-known.
