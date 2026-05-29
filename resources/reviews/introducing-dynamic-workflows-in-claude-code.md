---
title: "Introducing dynamic workflows in Claude Code"
url: https://claude.com/blog/introducing-dynamic-workflows-in-claude-code
author: "Anthropic"
date_evaluated: 2026-05-29
verdict: catalog
tags: [claude-code, subagents, orchestration, parallelism, large-codebases, migration, paid-tier, research-preview]
---

## What it proposes

A Claude Code feature in which Claude, given a large end-to-end task, dynamically writes its own orchestration script: it plans the task, breaks it into subtasks, and fans the work out across tens to hundreds of subagents running in parallel within a single session. The differentiator over plain subagent delegation is the coordination and verification layer. Coordination state lives outside the conversation, so the plan survives no matter how large the task grows; progress is checkpointed, so an interrupted run resumes rather than restarting. Critically, results are independently verified before being folded in: agents attack the problem from multiple angles, separate adversarial agents try to refute each finding, and the run iterates until answers converge. The cited proof point is a Zig-to-Rust port of Bun (~750k lines of Rust, 99.8% of the test suite passing, eleven days), where one workflow mapped Rust lifetimes per struct field, another wrote every `.rs` file with two reviewers each, and a fix loop drove build and tests to green.

Activation is via "create a workflow" prompts or an `ultracode` setting that pins effort to xhigh and lets Claude decide when to spin up a workflow. It is a research-preview feature limited to Max, Team, Enterprise, and API/cloud-provider access, and it explicitly consumes substantially more tokens than a normal session.

## Best used when

The task is genuinely too large for one agent in one pass and decomposes into many near-independent units of work: codebase-wide bug or security audits, profiler-guided optimization sweeps, framework or API-deprecation migrations touching hundreds to thousands of files, language ports, or a plan you want stress-tested adversarially before committing. The verification loop earns its cost when correctness matters more than the token bill and when findings would otherwise need a second human pass to weed out false positives. It also suits long-running jobs you want to leave unattended for hours, where checkpoint-and-resume and out-of-conversation coordination prevent a single interruption from wasting the whole run.

## Poor fit when

The work is small-to-medium, mostly sequential, or dominated by a single file or a tight cluster of files: the parallel fan-out has nothing to fan out to, and the orchestration overhead plus the multiplied token cost buys nothing. Content-style projects (markdown vaults, prose pipelines, small tracker apps, shell scripts) almost never present a problem with hundreds of independent verifiable subtasks, so the feature's core mechanism idles. For a token- and cost-sensitive solo operator, the "substantially more usage" warning is decisive on routine work. It is also gated behind specific paid tiers with no self-hosted equivalent, and it is research-preview, so it is neither reliably available nor stable to build a recurring workflow around. On a normal task, ordinary planning plus a handful of explicitly delegated subagents already covers the need at a fraction of the cost.

## Verdict

Catalog. The design is sound and the adversarial-verification-until-convergence loop is the interesting idea: it addresses the real failure mode of large agent runs, which is confidently wrong output that no one checks. But the feature is built for a problem class (thousand-file migrations, codebase-wide audits, language ports) that a solo operator working mostly on markdown and shell with small-to-medium code projects rarely faces, and it carries a token cost and paid-tier/research-preview gate that make casual use unwise. Worth knowing exists, so that if a genuinely large, decomposable, correctness-critical task ever lands, the right tool is on the radar; not worth adopting as a default. If the same coordination and verification machinery later becomes available at lower cost or for smaller tasks, or surfaces in a tier already in use, it would be worth re-evaluating toward adapt. It stands apart from the existing large-codebases review, which covers static harness configuration; this is a runtime orchestration feature, related but distinct.
