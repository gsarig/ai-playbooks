---
title: "How I made my skills update themselves"
url: https://joost.blog/self-updating-agent-skills/
author: "Joost de Valk"
date_evaluated: 2026-04-21
verdict: catalog
tags: [agent-skills, claude-code, versioning, session-hooks, distribution]
---

## What it proposes

A pattern for keeping installed Claude Code agent skills in sync with their upstream source without burning tokens or interrupting sessions. The mechanism has two parts. First, distribution and updates are delegated to `skills.sh` via `npx skills add` and `npx skills update`, with a `--skill` flag for targeting individual skills inside a monorepo. Second, a `SessionStart` hook in `~/.claude/settings.json` runs a shell command (`npx skills update -g -y`) before any context loads, so skill files on disk are refreshed before the session reads them. Because the hook executes outside the context window, the freshness check costs zero tokens per invocation, which is the specific failure mode of the author's earlier pattern (a version manifest plus in-skill check paragraph that ran on every invocation and could trigger mid-task re-invokes). The `source` field in the hook input can scope execution to startup only, avoiding latency on `/clear` and compaction if desired.

## Best used when

Skills are authored in one canonical repo and consumed on multiple machines or by multiple users who install from that upstream. The stale-skill problem is real whenever there is a gap between "source of truth" and "what the agent actually reads from disk" — typical of skill libraries published for others to install, or personal skills synced across several workstations without shared storage. The `SessionStart` hook idea generalises beyond `skills.sh`: any pre-session refresh operation (git pull of a skills directory, rsync from a network share, validation of on-disk state) benefits from running outside the context window rather than inside a SKILL.md preamble.

## Poor fit when

Skills live in a single directory that is already the source of truth — for example, a dotfiles repo symlinked into `~/.claude/skills/`. In that setup there is no "installed copy" to drift from the upstream; edits land in the canonical location directly, and `npx skills update` has nothing to reconcile. The hook pattern still applies in principle (one could run `git pull` on the dotfiles repo at session start), but that is a general dotfiles-sync concern, not a skill-specific one, and most users manage it separately. The resource is also tied to the `skills.sh` distribution model; teams that ship skills through private registries, internal package managers, or direct git submodules would need to rebuild the update command themselves, at which point only the hook idea transfers.

## Verdict

Catalog. The `SessionStart` hook insight is genuinely useful and worth knowing — moving a freshness check out of the context window and into a pre-session shell command is the correct architectural move for any skill-distribution workflow, and the post articulates clearly why the in-SKILL.md version check it replaces was wrong (token cost on every invocation, mid-task re-invokes). The concrete implementation, however, is coupled to `skills.sh` as the distribution layer, which only pays off when skills are installed from an upstream repo rather than authored in place. For maintainers publishing skill libraries to other users, adopt directly. For setups where the skills directory is itself the source of truth, the mechanism does not apply, but the `SessionStart` hook pattern is worth filing away for any future case where on-disk state needs to be refreshed before a session reads it.
