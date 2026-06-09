---
title: "Loop Engineering"
url: https://x.com/addyosmani/status/2064127981161959567
author: "Addy Osmani"
date_evaluated: 2026-06-09
verdict: adapt
tags: [loop-engineering, automations, worktrees, skills, mcp, sub-agents, memory, orchestration, claude-code, codex, methodology]
---

## What it proposes

A framing for working with coding agents in which you stop being the person who prompts each turn and instead design a recurring, self-firing system that prompts the agents for you. The unit of work is a loop: a recursive goal where you state a purpose once and the system iterates until a written done-condition is true. The author decomposes it into five building blocks plus a sixth, all of which now ship inside both Claude Code and Codex (so the loop is meant to be tool-agnostic):

1. **Automations**: the heartbeat that turns one run into a loop. A scheduled or interval-triggered run does discovery and triage on its own; findings go to an inbox, empty runs archive themselves. In Claude Code this is reached via scheduling, `/loop` (re-run on a cadence) and `/goal` (run until a condition holds), cron, lifecycle hooks, or GitHub Actions.
2. **Worktrees**: separate per-branch checkouts so parallel agents don't collide on the same files.
3. **Skills**: project knowledge written down (a `SKILL.md` folder) so the loop doesn't re-derive context every cycle and instead compounds it.
4. **Plugins and connectors**: MCP-based hooks into the tools you already use (issue tracker, DB, staging API, chat), so the loop can act beyond the filesystem; plugins bundle connectors plus skills for one-step install.
5. **Sub-agents**: split the writer from the checker so the agent grading the work isn't the one that produced it; the maker/checker split is also what `/goal` applies to the stop condition.
6. **Memory**: durable state on disk (a markdown file, a board, anything outside the single conversation) holding what's done and what's next, because the model forgets between runs. "The agent forgets, the repo doesn't."

A worked loop: a morning automation calls a triage skill that reads CI failures, open issues, and recent commits, writes findings to a state file, opens an isolated worktree per finding, sends one sub-agent to draft a fix and a second to review it, uses connectors to open the PR and update the ticket, and parks anything it can't handle in an inbox; the state file is the spine that lets the next run resume. The author is explicit that this sits "one floor above the harness" and is a synthesis of pieces, not a new tool, and that three problems get sharper rather than easier: verification stays on you ("done is a claim, not a proof"), comprehension debt grows the faster the loop ships code you didn't read, and cognitive surrender turns loop design from accelerant into liability.

## Best used when

There is genuinely recurring, self-generating work that arrives on a cadence rather than as a one-off ask: a project where triage, status checks, drift-detection, or routine fix-and-verify cycles repeat often enough that hand-prompting each pass is the bottleneck. It rewards projects that already have the substrate the loop runs on, such as checked-in skills, hooks, persistent memory files, and slash commands, so the pieces compose instead of being built from scratch. The maker/checker sub-agent split and the external state file are valuable on their own even without the full loop, anywhere a second-opinion pass or a resume-across-sessions spine would help. It suits work the operator understands deeply, because the loop amplifies whatever judgment (or lack of it) the designer brings.

## Poor fit when

The work is mostly one-off, exploratory, or irreversible-on-output: anything published, financial, medical, or otherwise unforgiving, where a loop running unattended is a loop making mistakes unattended and the human-in-the-loop gate is the whole point. It adds friction without payoff on small-to-medium projects that don't generate a steady stream of self-discoverable tasks, because there is no recurring backlog for the heartbeat to find, so the automation idles. The full multi-agent shape is token-hungry: automations fire on a schedule whether or not there's work, and sub-agents each run their own model and tool calls, so on metered usage the cost compounds quietly; the leverage only justifies the spend where a second opinion or unattended cadence is genuinely worth paying for. Single-file or tightly-sequential tasks gain nothing from worktrees or parallel agents. And the author's own warning is decisive for anyone who would let the loop substitute for understanding: the same loop design that accelerates a deep operator becomes a comprehension-debt machine for one avoiding the work.

## Verdict

Adapt. The core frame is sound and durable: the leverage point has moved from writing a good prompt to designing the system that prompts, and the six pieces are an accurate inventory of what now ships in mainstream coding agents. The pieces worth lifting directly are the cheap, scale-independent ones: external memory as the spine that survives the model's forgetting, the maker/checker sub-agent split, skills as compounding written context, and `/goal`-style written done-conditions. What needs adjustment for a solo, cost-sensitive, human-in-the-loop context is the always-on automation heartbeat and dense multi-agent fan-out: run those selectively, on work that genuinely recurs and is reversible, rather than as a default, and keep the verification and review gates the author himself insists on. This is distinct from the two adjacent reviews and complements both: harness-engineering describes the static environment a single agent runs inside, dynamic-workflows describes runtime fan-out of one large task within a single session, and Loop Engineering is the floor above, the recurring, self-firing loop that ties scheduling, worktrees, skills, connectors, sub-agents, and external memory into something that runs on a timer and feeds itself. Adopt the parts that are free and compounding; gate the parts that spend tokens or run unattended behind your own judgment, exactly as the author warns.
