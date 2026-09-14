---
title: "ECC: Agent Harness Performance Optimization System"
url: https://github.com/affaan-m/ECC
author: "affaan-m"
date_evaluated: 2026-09-05
verdict: adapt
tags: [agent-harness, skills, subagents, hooks, memory, security-scanning, multi-harness, plugin-distribution]
---

## What it proposes

ECC argues that the engineering loop most people re-explain in every prompt (plan, test, implement, review, verify, remember, improve) should live in the harness itself rather than in prompts. Install once and it becomes the agent's default behaviour. The delivery mechanism is a very large bundle: 68 subagents, roughly 286 skills, 94 legacy slash-command shims being phased out in favour of skills, opt-in per-language rule packs, and a hook runtime wired into the harness lifecycle events.

Four parts are architecturally distinct from other skill frameworks in this space, and are the reason the project is worth reading even if the bundle is not worth installing.

First, **multi-harness distribution via an adapter layer**. One set of underlying hook scripts is translated per harness rather than forked, so a harness with a different lifecycle event model reuses the same logic through a mapping shim. Support tiers are published honestly: one primary stable target, one further native plugin, several beta and experimental adapters, and one instruction-file-only target with no hooks or agents at all. Parity is explicitly not claimed, and harness-specific defects are tracked in the open.

Second, **the harness config itself as an attack surface**. A separate scanner audits agent instruction files, settings, MCP server configs, hooks, and agent/skill definitions for secrets, over-broad permissions, hook injection, and risky MCP servers. It ships as its own package and CI action, usable with none of the rest installed, and has an opt-in adversarial mode that runs red-team, blue-team, and auditor passes instead of static pattern matching alone.

Third, **a portable memory format with a stated trust boundary**. Durable context is written as versioned Markdown, scoped as project (gitignored, fail-closed), team (committed, human-reviewed), or user (opt-in), and readable across harnesses. Crucially, recalled memory is documented as unreviewed context rather than executable policy: agents are told to verify it against authoritative sources rather than obey it. That distinction is the single most transferable idea in the project, and most memory systems get it wrong.

Fourth, **confidence-scored behavioural learning**. Patterns are extracted from real sessions, scored, injected into later sessions only above a configurable threshold, and can be clustered into new skills. Import/export makes the extracted patterns portable rather than trapped in one machine's state.

Around this sits an unusually heavy commercial and marketing layer: a paid tier for private-repo automation, named corporate sponsors surfaced in the README, a brokered GPU-compute bridge for self-hosting open-weight models, trending badges, a dozen README translations, and a release cadence fast enough that major version history is documented inline. The code is MIT licensed and the open-source half is genuinely free, but the surrounding presentation is doing sales work.

## Best used when

Adopting the whole bundle makes sense for a team doing sustained multi-language software delivery across more than one agent harness, where the per-language reviewers, build-error resolvers, and framework skills each get used often enough to earn their context cost, and where a shared committed team memory scope has real readers.

Borrowing narrow pieces is the far more common fit, and holds for almost any agent-assisted workflow:

- **Run the config scanner standalone.** Auditing your own agent instruction files, settings, hooks, and MCP configs for leaked secrets and over-broad permissions is valuable independent of any framework, and this is one of the few purpose-built tools for it. Any setup with more than a handful of hooks or MCP servers benefits.
- **Steal the hook strictness profile pattern.** Environment-variable-selected profiles (permissive, standard, strict) plus per-hook disable lists is the right shape for hook configuration generally. It lets you run guardrails aggressively during risky work and loosen them during exploratory work without editing config.
- **Steal the memory trust boundary.** Recalled context as unreviewed input requiring verification, with explicit scope separation between machine-local, committed-and-reviewed, and cross-project, is worth copying verbatim into any memory setup regardless of format.
- **Steal the confidence threshold on learned behaviour.** Auto-extracted patterns gated by a score before injection is the difference between a learning system and an accumulating pile of noise.

The selective or manual install profile is also the honest recommendation for anyone who wants some of the catalogue: the project documents a low-context path with no hook runtime, and says so in its own README.

## Poor fit when

The full install is wrong for most single-operator setups and for any workflow whose centre of gravity is not code.

**Context footprint is the binding constraint.** The plugin variant advertises the installed catalogue to the model, which the maintainers acknowledge. A catalogue of this size is a standing tax on every session, paid in exchange for skills that a given workflow may never invoke. Per-framework skills for a dozen server-side ecosystems are dead weight in a workflow that touches none of them, and the always-loaded rule packs compound this.

**The transferable core is code-shaped.** Test-driven loops, build-error resolution, e2e runners, and per-language reviewers assume verifiable deliverables and a compile-test-fix cycle. Creative writing, research, and knowledge-vault work have no equivalent oracle, so the verification machinery degrades into ceremony. The business and content skills bundled alongside (article writing, market research, investor materials) are the thinnest part of the catalogue and do not compensate.

**Install-path complexity is a real maintenance cost.** Native plugin, manual file copy, and a universal guided installer are three routes to the same place, and the docs repeatedly warn against stacking them because layering duplicates skills, commands, and hooks. A setup that is easy to corrupt by following two valid sets of instructions is a setup that will eventually be corrupted, and untangling a duplicated install is worse than never installing.

**Platform maturity is uneven.** Known defects in the session-observer daemon and memory writes on one major desktop platform, plus a shell-compatibility bug on another, mean the continuous-learning and memory subsystems are not uniformly reliable yet. These are openly tracked rather than hidden, which is to the project's credit, but they still gate the two subsystems that are most interesting.

**The commercial layer does not serve solo operators.** Paid per-seat private-repo automation and brokered compute rental for self-hosting open-weight models solve organisational problems. For one person working locally, neither tier has anything to sell, and their prominence means the README optimises for a reader who is not you. The compute bridge is gated and non-executable by default, which is the correct design, but a dependency on a specific commercial marketplace with no self-hosted equivalent is worth noticing before it becomes load-bearing.

**Velocity cuts both ways.** A project shipping major versions this quickly is being actively improved, and is also a moving target. Anything built on top of its internals should expect churn.

## Verdict

**Adapt, selectively and without installing the bundle.** ECC's premise is correct, and its scope is the problem: encoding the engineering loop into the harness once beats re-prompting it, but 286 skills and 68 agents is a bet that most of a large catalogue will pay for its context cost, and for anything other than sustained multi-language team software work that bet loses. The skill-architecture lessons here are less crisply articulated than in narrower, more opinionated skill frameworks, so this is not where to learn skill design. What is genuinely novel and not available elsewhere in as usable a form is the standalone security scanner for agent configuration, which is worth running against any setup regardless of what else you use, and three design patterns worth copying into your own setup by hand: environment-variable hook strictness profiles, memory as scoped unreviewed context rather than policy, and confidence thresholds gating auto-learned behaviour before injection. Take those four things. Leave the catalogue, the marketplace install paths, and the commercial layer.
