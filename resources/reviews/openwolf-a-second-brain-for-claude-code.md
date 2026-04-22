---
title: "OpenWolf: A Second Brain for Claude Code"
url: https://github.com/cytostack/openwolf
author: "cytostack"
date_evaluated: 2026-04-22
verdict: watch
tags: [claude-code, hooks, token-tracking, project-intelligence, memory, node]
---

## What it proposes

OpenWolf is a Node.js CLI that installs a `.wolf/` directory and six Claude Code lifecycle hooks into a project. The hooks intercept Claude's actions and feed it project context it would otherwise lack: a generated file map with per-file token estimates (`anatomy.md`), a learning memory that accumulates corrections and preferences (`cerebrum.md`), a bug-fix ledger searchable before attempting repairs (`buglog.json`), and a chronological action log with token accounting (`memory.md`, `token-ledger.json`). Before a read, hooks surface the file's summary so Claude can skip opening it when the summary suffices; if a file was already read in the session, hooks flag the duplicate. Before a write, hooks check the learned-mistake list. After writes, the project map and token ledger auto-update. The project also ships optional extras: a web dashboard, a design-QC screenshot pipeline via `puppeteer-core`, and a curated UI-framework migration knowledge base. The author reports ~65.8% average token reduction across 132+ sessions and 71% of repeated reads caught.

## Best used when

Large codebases where Claude burns tokens re-reading files it has already seen, or opening modules whose contents could have been conveyed by a one-line description. Projects with recurring bug patterns where a searchable fix log genuinely saves rediscovery. Workflows where the user wants token accounting without instrumenting it by hand. Environments that already run Node.js 20+ and are comfortable with a local-only tool that writes plain files into the repo. Teams or solo operators who accept that some context discipline must be automated rather than enforced by prompt.

## Poor fit when

Small projects or content vaults (fiction, notes, single-directory workflows) where the file count is low enough that a project map adds overhead without payoff. Workflows that do not revisit the same files repeatedly within a session, which neutralises the largest claimed saving. Setups where hook reliability matters more than token savings, since the author states hooks are a young Claude Code feature and OpenWolf falls back to CLAUDE.md instructions when hooks do not fire. Projects where adding a `.wolf/` directory, committing or gitignoring nine generated artefacts, and trusting an ~85-90% compliance rate on memory updates introduces more maintenance than the saved tokens justify. Cases where the user already maintains a deliberate CLAUDE.md and per-session context strategy; OpenWolf's value proposition assumes the baseline is undisciplined context use.

## Verdict

Watch. The mechanism is coherent and addresses real gaps in Claude Code's default behaviour: no file index, no session-level read deduplication, no persistent correction memory. The claimed savings are plausible for the scenario described (large active codebase, many repeat reads). What keeps this from an adopt or adapt rating is maturity and scope fit. It is v1.0.4 with the author's own "things may break" caveat; token accounting is estimated, not measured; cerebrum.md compliance is self-reported at 85-90%; and the whole apparatus is optimised for code projects with dozens to hundreds of files, not for note vaults or short-lived fiction workflows. The dashboard, design-QC, and framework-migration features expand surface area in directions most evaluators will not use. Revisit once the hook model is stable, the tool reaches a later version with external validation of the token-savings numbers, and a clearer separation exists between the core `.wolf/` intelligence layer and the optional extras. For any evaluator whose main pain is Claude re-reading large files in long coding sessions, it is worth a sandbox trial before then.
