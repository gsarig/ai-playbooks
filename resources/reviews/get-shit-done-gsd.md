---
title: "Get Shit Done (GSD)"
url: https://github.com/gsd-build/get-shit-done
author: "TÂCHES"
date_evaluated: 2026-04-22
verdict: skip
tags: [claude-code, spec-driven-development, workflow-framework, multi-agent, context-engineering, software-only]
---

## What it proposes

GSD is a spec-driven development framework for Claude Code (with ports to other coding CLIs) that solves context rot by externalising state into a fixed set of markdown artifacts and orchestrating subagents against them. The workflow is a strict loop: initialise a project (questions → optional parallel research agents → requirements → roadmap), then for each phase run discuss (capture implementation preferences as CONTEXT.md) → plan (researcher + planner + checker loop producing atomic XML-structured task plans) → execute (wave-based parallel executors, each with a fresh 200k context window, atomic commit per task) → verify (user acceptance testing with automated debug agents). Milestones group phases; shipping creates a PR; completion archives and starts fresh.

The mechanism rests on four pillars: a canonical artifact set with size caps (PROJECT, REQUIREMENTS, ROADMAP, STATE, CONTEXT, RESEARCH, PLAN, SUMMARY, VERIFICATION, plus todos/threads/seeds sidecars); XML task formatting with explicit name/files/action/verify/done fields; an orchestrator-agent split where the main context only coordinates while spawned agents do heavy lifting; and a hardened security layer (prompt injection scanning, path traversal prevention, PreToolUse guard hook). Configurable model profiles route planning to Opus and execution to Sonnet by default. Quick mode exists for ad-hoc tasks that bypass the full pipeline.

## Best used when

Greenfield or phased software projects where requirements can be captured upfront and decomposed into atomic tasks with objective verification criteria (curl returns 200, test passes, endpoint exists). Solo developers or small teams building product-shaped software — web apps, APIs, CLIs — who want enterprise-style rigour without enterprise ceremony. Situations where context rot across long builds is the actual blocker and where the codebase is large enough that keeping the main window at 30-40% matters. Works best when the work naturally partitions into independent parallel tasks within a phase.

## Poor fit when

Non-code creative or knowledge work. The entire framework assumes objective deliverables verifiable by shell commands or UAT questions, atomic git commits per task, and an executor that writes files in a repo. Fiction writing, research note synthesis, content pipelines, and vault-based workflows have no natural mapping to phases/plans/verifies — the artifacts would be theatre. Poor fit also for small scripts or one-off tasks where the setup cost (new-project → discuss → plan → execute) dwarfs the work; quick mode helps but the framework's value proposition collapses at that scale. Finally, poor fit for exploratory or research-driven work where requirements genuinely cannot be fixed upfront — the discuss-phase step locks decisions before investigation, which is the opposite of what emergent work needs.

## Alternatives

For the transferable ideas — context engineering via structured artifacts, subagent orchestration with fresh contexts, skill-based workflow patterns — Superpowers (already reviewed, adapt verdict) offers the same architectural lessons in a more composable form that travels beyond code. Superpowers' skill-architecture and meta-methodology for writing agent-resistant skills generalise to creative and knowledge work; GSD's pipeline does not. For pure spec-driven coding, SpecKit, BMAD, and OpenSpec are named competitors in GSD's own README and cover similar ground.

## Verdict

Skip. GSD is a competent, clearly-built software development framework that solves a real problem (context rot in long Claude Code builds) with sensible mechanisms (artifact discipline, XML task structure, wave orchestration, fresh-context executors). The XML task format and the orchestrator-never-does-heavy-lifting pattern are genuinely good ideas worth noting. But it is a code-only framework whose abstractions — phases, plans, atomic commits, curl-verifiable deliverables — do not survive contact with non-code work, and for the code work it does fit, the transferable architectural lessons are already available in a more portable form via Superpowers. Adopting GSD wholesale would import a software-engineering workflow into contexts where it is inert; adapting it piecemeal produces a worse version of what Superpowers already offers. Note the XML task-structure pattern and the wave-execution model as references, but do not install or adopt.
