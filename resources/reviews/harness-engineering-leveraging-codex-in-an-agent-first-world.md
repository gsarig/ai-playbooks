---
title: "Harness engineering: leveraging Codex in an agent-first world"
url: https://openai.com/index/harness-engineering/
author: "Ryan Lopopolo"
date_evaluated: 2026-05-07
verdict: adapt
tags: [agent-engineering, harness, repo-structure, agents-md, feedback-loops, codex, methodology]
---

## What it proposes

A methodology for building software where agents write all the code and humans design the environment the agents work in. The core mechanism is "harness engineering": treating the repository, tooling, and feedback loops as the primary artifact, not the code itself. Concrete components:

- **Repo as system of record.** A short `AGENTS.md` (~100 lines) functions as a table of contents pointing into a structured `docs/` tree (architecture, design docs, execution plans, product specs, references, quality/reliability/security policies). Plans are first-class, checked-in artifacts. Doc freshness is enforced mechanically via linters, CI jobs, and a recurring "doc-gardening" agent.
- **Application legibility for agents.** UI, logs, metrics, and traces are exposed to the agent through local stacks per worktree (browser DevTools protocol for UI; an observability stack for telemetry). The app is bootable per worktree so the agent can drive its own instance, reproduce bugs, and validate fixes.
- **Architectural invariants over style policing.** A rigid layered model (Types → Config → Repo → Service → Runtime → UI, with cross-cutting concerns entering through Providers) is enforced via custom lints and structural tests. Lint messages embed remediation instructions consumed by the agent. Boundaries are validated; implementations are not micromanaged.
- **Agent-to-agent review loops.** Code is reviewed primarily by other agent runs iterating until reviewers are satisfied. Human review is optional. Merge gates are minimal; flakes are handled with retries rather than blocking.
- **Continuous garbage collection.** Background agent tasks scan for pattern drift, grade quality, and open small refactor PRs that auto-merge. When recurring human feedback appears, the rule is promoted from documentation into code or tooling.

The throughline: when something fails, the question is never "try harder" but "what capability is missing, and how do we make it legible and enforceable for the agent?"

## Best used when

- A codebase is large enough or moves fast enough that documentation drift, pattern inconsistency, or onboarding cost is a real bottleneck — agent or human.
- Multiple agents (or multiple sessions) operate on the same repo and need a shared, mechanically enforced ground truth rather than tribal knowledge.
- The work involves a long-running application where the agent benefits from driving the running system: reproducing bugs, validating fixes against logs/metrics, exercising the UI.
- The team or solo operator has already invested in slash commands, skills, hooks, and custom linters and is looking for the next layer of leverage.
- A workflow has hit the ceiling of "one big AGENTS.md / CLAUDE.md" and needs to migrate to a progressive-disclosure structure.

## Poor fit when

- The project is small enough that a single `CLAUDE.md` or `AGENTS.md` plus a handful of skills covers it. The structured `docs/` tree, doc-gardening agent, and quality-grading background runs only pay back at scale; on a repo-sized single-domain project they add maintenance overhead without proportional return.
- Agent-to-agent review without human gating is the default. For a solo operator on production-affecting code (publishing, financial data, medical data, anything irreversible), the human-in-the-loop gate is the value, not the friction.
- Throughput is not the bottleneck. The "minimal merge gates, retry flakes, corrections are cheap" stance assumes 1,500 PRs over five months. At lower volume the calculus inverts: a flaky test caught now is cheaper than a bug caught in production tomorrow.
- Background agent loops would run on paid API calls without a budget ceiling. Continuous doc-gardening, quality grading, and refactor PRs are economical at OpenAI's cost basis; they are not free for an independent operator on metered tokens.
- The stack leans on hosted observability or browser-driving infrastructure that conflicts with a self-hosted, locally-run preference. The pattern still applies, but the specific tooling choices need substitution.

## Verdict

Adapt. The high-level frame — humans design the harness, agents execute inside it; the repo is the system of record; legibility is the constraint that matters — is durable and applies at any scale. Several specific patterns are worth lifting directly: short `AGENTS.md`/`CLAUDE.md` as a table of contents pointing into a structured `docs/` tree; plans as first-class checked-in artifacts; lint messages that embed remediation instructions for the agent; promoting recurring feedback from documentation into enforced code rules. Other parts do not transfer to small-repo, solo, or low-throughput contexts without modification: agent-to-agent review as the default merge path, minimal blocking gates, continuous background refactor agents, and per-worktree observability stacks all assume team scale and a cost basis that an independent operator does not share. The right move is to treat this as a reference architecture for the harness layer — borrow the legibility-and-enforcement patterns, keep human review and stricter merge gates, and skip the always-on background agent loops until throughput justifies them.
