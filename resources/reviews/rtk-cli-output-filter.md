---
title: "rtk: CLI proxy that filters command output before the LLM sees it"
url: https://github.com/rtk-ai/rtk
author: "rtk-ai"
date_evaluated: 2026-05-16
verdict: watch
tags: [tooling, context-compression, cli, claude-code, token-savings]
---

## What it proposes

A single Rust binary that sits between an AI coding agent and the shell. A `PreToolUse` hook rewrites Bash invocations (`git status` becomes `rtk git status`) before they run, and four strategies (smart filtering, grouping, truncation, deduplication) trim the output the model ingests. Coverage spans roughly 100 commands across git/gh, test runners, linters, build tools, package managers, AWS/Docker/kubectl, and generic file ops. When a filtered command fails, "tee mode" writes the full unfiltered output to a local file and tells the agent where to read it, preserving an escape hatch. Analytics (`rtk gain`, `rtk discover`) report per-command savings. Telemetry is opt-in, aggregate-only. The README claims 60-90% token savings on common dev commands, backed by an estimated per-command table the project explicitly labels as estimates from medium-sized TS/Rust projects.

## Best used when

- The agent runs many shell commands per session and the host AI tool routes them through a Bash-style tool the hook can intercept.
- Sessions are long-lived and verbose-by-default commands (`cargo test`, `git status` in a busy worktree, `kubectl` listings) dominate the transcript.
- The shell environment supports the auto-rewrite hook properly (macOS, Linux, or WSL under Linux) so adoption does not depend on a `CLAUDE.md` injection workaround.
- The workflow already leans on shell wrappers like `cat`, `rg`, `grep`, `find` rather than the agent's native structured file tools, because only Bash-routed commands get rewritten.
- A team or solo dev is willing to spot-check filtered output against raw output for the handful of commands they rely on most, and to disable filtering per-command when it strips something useful.

## Poor fit when

- The agent leans heavily on built-in structured tools (Read, Grep, Glob, or equivalents) rather than shell commands. Those calls bypass the Bash hook entirely, so realized savings drop far below the headline number unless the user actively rewires their workflow toward shell calls or explicit `rtk` invocations, which is friction in the opposite direction from what the tool advertises.
- The work is correctness-sensitive in ways that depend on full command output: build warnings, deprecation notices, partial test failures, log lines around an error, or any signal that lives in the "noise" a filter might remove. An opaque filter between the model and the truth is a liability when the model needs the truth.
- Native Windows without WSL, where the hook degrades to a `CLAUDE.md` instruction injection that is weaker and easier for the model to ignore.
- Short sessions, small repos, or workflows where context window pressure is not the binding constraint. The setup cost and the small ongoing risk of filtered-away signal outweigh modest savings.
- Projects that resist adding a binary dependency in the critical path between agent and shell, or that want reproducible behaviour across machines without an extra install step.

## Alternatives

- Tighter prompting: instruct the agent to prefer compact flags (`git status --porcelain`, `ls -1`, `grep -c`, `--quiet` test runners) and structured output where available. Costs nothing, no dependency, no filter to audit.
- Prefer the agent's native file and search tools where they exist; their output is already structured and usually tighter than raw shell.
- Per-command shell aliases or wrapper scripts for the two or three commands that actually dominate a given project's transcript, kept under the project's own version control.

These are partial substitutes rather than full replacements; none of them deliver rtk's breadth or its `gain`/`discover` analytics.

## Verdict

Watch. The mechanism is well-designed: transparent rewriting via a PreToolUse hook, tee-on-failure as an escape hatch, opt-in telemetry, single-binary install. The headline savings are plausible for shell-heavy sessions, and the tee fallback meaningfully reduces the worst-case downside of an over-aggressive filter. Two things hold it back from an adopt today. First, the scope limitation: the hook only rewrites Bash calls, so agents that route most file and search operations through native structured tools will see a fraction of the advertised savings without restructuring their workflow toward shell commands, which cuts against the tool's "transparent" pitch. Second, the maturity profile: version 0.28.x, a small contributor base, and 100+ command-specific filters whose quality is necessarily uneven mean the project is taking on a non-trivial maintenance surface. A filter that silently drops a deprecation warning or a flaky-test hint is a class of bug that is hard to notice until it costs you. Revisit once the project hits a 1.0, the filter set has been stress-tested by a wider user base, and there is either first-class support for non-Bash agent tools or a clear statement that shell-routed workflows are the intended target. In the meantime it is worth trying in a sandboxed project to measure realized (not headline) savings against the specific commands that dominate one's own transcripts.
