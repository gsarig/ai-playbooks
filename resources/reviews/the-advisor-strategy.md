---
title: "The Advisor Strategy"
url: https://claude.com/blog/the-advisor-strategy
author: "Anthropic"
date_evaluated: 2026-04-22
verdict: catalog
tags: [anthropic-api, agent-architecture, cost-optimization, claude-platform, multi-model]
---

## What it proposes

A pattern and accompanying server-side tool (`advisor_20260301`) that inverts the usual orchestrator-worker hierarchy for agentic pipelines. Instead of a large model decomposing work and delegating to smaller workers, a cheaper executor (Sonnet or Haiku) drives the task end-to-end — calling tools, reading results, iterating — and escalates to Opus as an advisor only when it hits a decision it cannot reasonably resolve. The advisor sees the shared context and returns a plan, correction, or stop signal; it never calls tools or produces user-facing output. The executor resumes with that guidance. Declared as a single entry in the `tools` array of a `/v1/messages` call, with `max_uses` capping advisor invocations per request and advisor tokens billed separately at Opus rates. Anthropic reports ~2.7pp gain on SWE-bench Multilingual over Sonnet-solo at ~12% lower cost, and roughly doubling of Haiku's BrowseComp score when paired with an Opus advisor.

## Best used when

Building agentic pipelines directly against the Anthropic Messages API where the executor loops autonomously for many turns and occasionally hits reasoning cliffs (ambiguous plans, tricky refactors, tool-selection decisions). Especially valuable when cost-per-task matters at volume and you already run evals, so you can measure whether the advisor actually lifts scores on your workload. Fits cleanly when the existing architecture is single-agent with tools rather than a multi-agent orchestration graph, since it avoids having to build a worker pool or routing layer.

## Poor fit when

Running through Claude Code or any client that abstracts over the Messages API and does not expose the `tools` array or beta headers — there is no user-facing knob for this. Also a poor fit for workflows that are not agentic loops (single-shot generation, short chat turns, simple RAG), where there is no executor to escalate from. Not applicable to local-only or self-hosted model setups, since it depends on Anthropic's server-side tool dispatch. And if your pipeline is already Opus-solo for quality reasons, the advisor pattern is orthogonal — you would be moving down-tier to gain the cost savings the strategy advertises.

## Verdict

Catalog. This is a genuinely clever inversion of the orchestrator-worker pattern and the numbers are credible, but it only surfaces as a one-line change if you are writing against the Messages API directly. The agentic pipelines in this repo's ecosystem run primarily through Claude Code rather than raw SDK calls, and the advisor tool is not something a Claude Code user opts into — it is a server-side tool declared in request JSON. For the SDK-based projects in adjacent repos (translation pipelines, PDF processors, tracker backends), it is worth remembering when a Sonnet-driven loop underperforms and the next instinct would be to upgrade the whole run to Opus; swapping in an advisor tool with `max_uses: 2-3` is cheaper to try than a full model bump and easy to A/B against solo baselines. Keep it in the toolbox, reach for it when an SDK-based agent loop needs a quality lift without a cost blowup, but no action to take on the Claude Code side of the ecosystem.
