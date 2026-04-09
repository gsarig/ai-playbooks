---
title: "Superpowers"
url: https://github.com/obra/superpowers
author: "Jesse Vincent / Prime Radiant"
date_evaluated: 2026-04-10
verdict: adapt
tags: [claude-code, workflow-framework, skill-architecture, planning, agent-orchestration]
---

## What it proposes

Superpowers is a composable skills framework for AI coding agents (Claude Code, Cursor, Gemini CLI, Codex). It ships as a zero-dependency plugin that injects workflow discipline through auto-triggering skills: the agent checks for relevant skills before every action and is instructed to follow them without exception.

The framework enforces a rigid pipeline: Socratic brainstorming to refine intent before any work begins, a detailed planning phase that decomposes work into small tasks with exact file paths and verification steps, subagent-driven execution where a fresh agent handles each task under two-stage review (spec compliance, then quality), and a structured branch-finishing step.

Two things matter more than the specific skills it ships:

**The skill architecture pattern.** Skills are SKILL.md files in a flat namespace. Triggering descriptions specify only *when* to trigger, never *what* the skill does internally — summarising the workflow in the description causes agents to shortcut-follow the summary instead of reading the full skill. Skills are categorised as rigid (follow exactly) or flexible (adapt principles). Cross-references use named markers rather than file-path links, avoiding premature context loading.

**The meta-skill for writing skills.** The `writing-skills` skill applies TDD to process documentation itself. Write a pressure scenario, run a subagent without the skill to see how it fails (baseline), write the minimal skill that addresses those specific failures, then iteratively close rationalisation loopholes. This produces skills calibrated against observed agent behaviour rather than invented from first principles — including "Red Flags" tables and "Common Rationalisations" sections.

## Best used when

- Building a composable skill system for any AI agent and looking for proven patterns around skill discovery, triggering, description design, and anti-shortcutting techniques.
- Wanting a structured methodology for writing durable process documentation that agents actually follow under pressure, rather than ignore when convenient.
- Coordinating multi-step work where tasks are independent and can be dispatched to subagents with isolated context.
- Needing a Socratic brainstorming protocol that forces intent clarification before any execution begins.

## Poor fit when

- The work does not involve software development. Roughly 60% of the shipped skills (TDD, code review, git worktrees, branch finishing) are software-specific with no meaningful transfer.
- Workflow needs are lightweight or exploratory. The mandatory seven-stage pipeline adds significant ceremony. For creative or knowledge work where iteration is the process, rigid gate structure creates friction without proportional payoff.
- The domain involves a single human working with a single agent session. The subagent orchestration pattern assumes tool-call-level agent spawning and makes sense at scale but is overhead for simpler interactions.

## Alternatives

No single alternative covers the same scope. For structured planning methodologies, chain-of-thought and task decomposition patterns are well-documented in the prompt engineering literature without requiring a framework. The anti-rationalisation and pressure-testing methodology for writing skills appears to be unique to this project.

## Verdict

The transferable core is the skill architecture pattern and the meta-methodology for writing skills that resist agent rationalisation: triggering-only descriptions (summarising the workflow in the description causes agents to skip the actual skill content), the distinction between rigid and flexible skills, and the TDD-for-documentation approach (baseline failure, minimal skill, loophole closing). These apply to any domain where an AI agent needs to follow structured processes. The specific pipeline (brainstorm, worktree, plan, subagent execution, two-stage review, branch finish) is a software engineering workflow and does not transfer to creative or knowledge work without substantial rearchitecting. Adapt the skill design patterns and the meta-skill methodology; leave the development pipeline behind.
