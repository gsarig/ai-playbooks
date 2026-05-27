---
title: "grill-with-docs: Align Before You Build"
url: https://www.aihero.dev/grill-with-docs
author: "Matt Pocock"
date_evaluated: 2026-05-18
verdict: adapt
tags: [planning, documentation, ddd, skills, grilling, ubiquitous-language, adr]
---

## What it proposes

A successor to `/grill-me` that keeps the same branch-by-branch interview core but adds two documentation layers. At session start, the skill looks for a `CONTEXT.md` file holding the project's ubiquitous-language glossary (terms shared between code, developer, and domain expert) and uses it to ground the conversation. During the interview, it actively refines language: challenges fuzzy terms against the glossary, sharpens imprecise wording, runs concrete scenarios to test edge cases, cross-references the code, and writes back updated entries as decisions land. For decisions that are hard to reverse, surprising without context, or involved a real trade-off, it produces an Architectural Decision Record as a small markdown file. A monorepo can carry multiple contexts; a single-language repo gets one `CONTEXT.md`.

## Best used when

Projects with a non-trivial domain vocabulary that recurs across planning sessions, where the same terms keep getting re-explained to the AI. Strongest fit for codebases that will see repeated feature work over months, where decisions about cardinality, naming, lifecycle, and deletion semantics compound. Also valuable early in a project, before fuzzy terms calcify into inconsistent code. The glossary-plus-ADR layer pays off any time the cost of re-establishing shared language exceeds the cost of writing it down, which is most ongoing work and almost no one-shots.

The pattern generalises beyond code. Long-running creative or knowledge vaults (fiction with recurring characters and settings, domain trackers with specialised terminology, knowledge bases with stable taxonomies) benefit from the same glossary discipline, even if ADRs are less relevant there.

## Poor fit when

Throwaway scripts, one-off explorations, and tasks small enough that the whole context fits in a single prompt. Projects where the vocabulary genuinely is the standard one for the stack (a plain CRUD app over a well-known schema) gain little from formalising terms everyone already knows. Solo work with no domain expert and no collaborators risks turning the glossary into theatre, a document written for an audience of one that drifts out of sync with the code. If `CONTEXT.md` is not actively maintained as code changes, it becomes a lying artifact and is worse than no glossary at all.

ADRs specifically are wasted on reversible decisions or interchangeable choices; reserve them for the cases the article names (hard to reverse, surprising, real trade-off).

## Verdict

Adapt. The grilling core is already proven, and the glossary layer is a real improvement for any project where the same domain terms get re-explained across sessions. Adopt the skill itself from the upstream repo, but use it selectively: codebases and long-running vaults with stable vocabulary, not every project. Keep `/grill-me` available for greenfield design conversations and quick one-offs where no glossary exists yet, exactly as the author recommends. Treat `CONTEXT.md` as a living file with the same maintenance discipline as `CLAUDE.md`; if a project will not get that discipline, skip the glossary layer and stay with `/grill-me`. ADRs are worth the small ceremony only for decisions that meet the three criteria; do not let them proliferate.
