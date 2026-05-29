---
title: "How to code with AI agents"
url: https://humanmade.com/engineering/how-to-code-with-ai-agents/
author: "Ivan Kristianto"
date_evaluated: 2026-05-27
verdict: adapt
tags: [agent-workflow, methodology, tool-agnosticism, quality-gates, spec-first, fire-and-forget, throwaway-code, practitioner]
---

## What it proposes

A first-person account of an everyday AI-augmented engineering workflow, presented as a set of patterns rather than a tool recommendation. It is built on top of the obra/superpowers framework but does not follow it mechanically; the author keeps the core sequence (brainstorm, spec, plan, build, review) and discards the rest. The concrete mechanisms:

- **Tool-agnosticism as a stance.** The author commits to no single model or CLI, moving between several agents per task on the premise that the landscape shifts daily and locking in leaves capability unused. Output is treated as non-deterministic by design.
- **Spec-first, multi-pass review before building.** A nine-step loop: a worktree per feature; agent-led brainstorming that interviews the human; a design spec the human refines, then hands to a *fresh* second agent to check against intent and find gaps; an implementation plan broken into 2-5 minute tasks with exact paths and verification steps, refined until each step is "something you'd hand a junior dev with no further explanation"; a cross-review of plan against spec by another fresh agent; automated execution that dispatches subagents and stops on failure.
- **Review as a user, not an engineer.** After execution the human exercises the feature rather than reading code. If it falls materially short: discard and return to the plan. A separate three-agent parallel review (maintainability, performance, security) runs independently and triages findings before shipping.
- **Throw-away code mindset.** Generated code is disposable by default. "Code is cheap now. The expensive part is reading, deciding, and knowing when to stop." The discipline is to resist patching a mostly-right result and instead reset with a different model or refined plan.
- **Quality gates as the primary quality lever.** The author's central claim: the biggest quality improvement is not a better prompt or smarter model but strict gates (lint, format, design-system compliance, typecheck, tests) that run before every commit. They let the agent catch and fix its own hallucinations dozens of times before the human ever sees output.
- **Build-once-reuse skills.** Search existing skill libraries first, read before adopting (a skill can encode conflicting assumptions), build a custom skill for anything done more than twice, delete what doesn't work with no sunk cost.
- **Fire-and-forget and parallelism.** Independent work runs in parallel worktrees and parallel agents; before starting, ask which parts depend on each other. Much of the away-from-keyboard usage is research and sense-making (mobile agents, source-grounded tools), following "define the question, send the agent, move on, come back to the answer."
- **The "vibe user" and emotional discipline.** Ask an agent with browser access to use the app as a naive user and report friction, because the builder knows too much. And: stop putting emotion into prompts; frustration produces worse output; when stuck, open a fresh session with a precise question.

## Best used when

- Running a software workflow with reversible artifacts (feature branches, PRs) where regenerating from a refined spec is genuinely cheaper than debugging a flawed output.
- A project already has, or can cheaply add, automated quality gates (lint, typecheck, tests, structural checks) that an agent can run in a loop and self-correct against. This is the load-bearing prerequisite; without it the throw-away mindset has nothing to catch errors.
- Tasks decompose into independent units that benefit from parallel agents and per-feature isolation.
- The operator wants concrete, battle-tested practices to layer on top of an existing spec-first framework rather than a framework itself.
- Cross-domain pickups: the spec-first / fresh-agent-review pattern, the "define the question, send the agent, come back" research loop, the source-grounded note synthesis, and the emotional-discipline rules all transfer cleanly to knowledge and creative work.

## Poor fit when

- The output is irreversible or published and the throw-away/fire-and-forget defaults remove the human gate. "I start it and leave" and disposable code assume cheap regeneration and a safety net of gates; on prose meant for publication, financial or medical data, or any one-way action, the human-in-the-loop checkpoint is the value, not the friction.
- No automated quality gates exist and none can be built. Most of the quality claim rests on gates doing the self-correction; on domains with no objective pass/fail check (most creative and a lot of knowledge work), the agent cannot catch its own mistakes and the workflow degrades to unsupervised generation.
- The operating mode is a single human with a single agent session. The parallel-worktree, multi-agent-review, subagent-dispatch machinery assumes running three or four streams at once; for one focused session most of the orchestration is overhead.
- Tool-hopping across many paid clouds is not affordable or practical. The premise of moving freely between several frontier agents per task has a cost and setup basis that a locally-runnable, single-tool operator does not share; the *stance* (don't over-commit) transfers, the literal practice does not.

## Verdict

Adapt. This is a practitioner narrative, not a framework, and it earns standalone treatment because it adds patterns its underlying framework's review does not cover: tool-agnosticism, throw-away code, quality-gates-as-self-correction, the "vibe user," away-from-keyboard fire-and-forget, and explicit emotional discipline. The most durable and generally useful claim is that strict automated gates, not prompt-craft or model choice, are the dominant quality lever; that reframes "how do I get better output" into "what can the agent mechanically check itself against," and it generalises to any domain that can define a pass/fail signal. The spec-first loop with fresh-agent cross-review, the source-grounded research pattern, and the no-emotion-just-precision rules transfer to knowledge and creative work as-is. What needs adjustment is the throw-away and fire-and-forget posture: it is calibrated for reversible code under a gate safety net and a high-throughput multi-agent setup, so for solo single-session work, for output without objective checks, and for anything irreversible or published, keep the human review gate and treat regeneration as a deliberate choice rather than a default. Borrow the gates and the disciplines; leave the leave-it-running defaults.
