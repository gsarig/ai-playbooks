---
title: "Claude Code's creator keeps sharing tips, and they all made my experience better"
url: https://www.xda-developers.com/claude-codes-creator-keeps-sharing-tips-and-they-all-made-my-experience-better/
author: "Mahnoor Faisal (covering tips from Boris Cherny)"
date_evaluated: 2026-04-21
verdict: adapt
tags: [claude-code, commands, workflow, productivity, slash-commands, mobile]
---

## What it proposes

A roundup of five native Claude Code features surfaced by its creator:

1. `/btw` — inline side-question overlay that inherits full conversation context without polluting the main transcript, distinct from spawning a parallel session with a blank slate.
2. Claude in Chrome — a paid-tier browser extension that gives Claude Code direct visual and interactive access to a running browser, replacing the "user as Claude's eyes" loop with a build-test-verify cycle.
3. `/loop` and `/schedule` — `/loop` reruns a prompt at a fixed or self-paced interval during an active session; `/schedule` creates persistent tasks in two flavors: Desktop (runs while the app is open) and Cloud (runs on Anthropic's servers regardless of device state). Positioned for recurring automation like periodic review, queue-triggered PRs, and stale-PR cleanup.
4. `--add-dir` — launch-time flag granting access to additional folders outside the current working directory, with `settings.json` as the persistent equivalent for frequently used paths.
5. Mobile and multi-device — iOS/Android app plus `/teleport` (move a cloud session to a local machine), `/remote-control` (drive a local session from phone or browser), and Dispatch (phone as a remote for Claude Desktop).

The underlying pattern is situational command awareness: small features that only help if you know they exist and remember to reach for them.

## Best used when

- A workflow already runs in Claude Code daily and small friction reductions compound over time.
- Work spans multiple directories or vaults that do not share a common parent, where `--add-dir` or a `settings.json` entry removes repeated context-switching.
- A task benefits from a sustained cadence of the same prompt (periodic continuity checks, scheduled sweeps of a folder, draft-status audits) where `/loop` or `/schedule` Desktop tasks replace manual reruns.
- A side question would otherwise derail a long-running agent turn; `/btw` preserves the main thread's focus.
- A user genuinely works across devices and wants a started-on-desktop session reachable from a phone.

## Poor fit when

- The feature requires paid-tier access with no self-hosted or local substitute. Claude in Chrome is the clearest example: the build-test-verify loop is valuable, but gating it behind a subscription extension makes it a poor default for anyone optimizing for local-first tooling. Playwright driven by Claude Code through a local MCP or script achieves a comparable loop without the paywall.
- Cloud-only scheduling (`/schedule` Cloud tasks) touches private vaults or repositories whose contents should not leave the local machine. Desktop tasks are the acceptable variant in that case, at the cost of requiring the app to stay open.
- The workflow is single-directory and single-device; `--add-dir`, `/teleport`, `/remote-control`, and Dispatch solve problems that do not exist in that setup.
- `/loop` is reached for as a substitute for a proper cron or file-watcher when persistence across session close matters. The session-bound lifetime is a real constraint, not a detail.

## Verdict

Adapt. The article is a catalog of native features rather than a methodology, so the useful output is a selective pick list, not wholesale adoption. `/btw`, `--add-dir`, and `/loop` are low-cost additions to any Claude Code workflow and worth internalizing immediately. `/schedule` Desktop tasks are worth trying for recurring vault or repo sweeps, with the caveat that anything surviving session close via the cloud variant needs a privacy check first. The Chrome extension is the weakest item for a local-first setup and should be treated as skippable until a comparable local story exists or a specific project justifies the subscription. Mobile and multi-device features are situational; relevant only when cross-device work is already a real pattern, not aspirational. The durable lesson for any Claude Code user is that the tool ships more built-in commands than the default UI surfaces, and periodically auditing the command list against current workflow pain points pays off.
