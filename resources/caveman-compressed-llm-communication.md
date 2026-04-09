---
title: "Caveman: compressed LLM communication via telegraphic prose"
url: https://github.com/JuliusBrussee/caveman
author: "Julius Brussee"
date_evaluated: 2026-04-10
verdict: adapt
tags: [token-efficiency, prompt-engineering, context-window, llm-output]
---

## What it proposes

Caveman is a Claude Code skill that instructs the LLM to respond in compressed, filler-free language by dropping articles, hedging, pleasantries, and connective fluff. It claims roughly 65% output token reduction (the README headline says 75%; the project's own honest three-arm eval, which controls for a simple "be terse" baseline, shows the skill-specific contribution is narrower). A companion sub-tool, caveman-compress, rewrites instruction files (CLAUDE.md, memory files, preferences) into compressed prose so the LLM reads fewer input tokens on every session load, with measured savings around 35-60% on prose-heavy files while leaving code blocks, URLs, and technical terms untouched.

The underlying principle is more durable than the tool itself: natural-language instructions and LLM output both contain enormous amounts of filler that consumes tokens without improving accuracy or comprehension. The project cites a March 2026 arxiv paper (2604.00025) showing that brevity constraints can actually improve model accuracy on certain benchmarks, not just reduce cost. The insight is that verbosity is not a proxy for quality in LLM communication in either direction, and that systematically compressing the prose layer of human-to-model and model-to-human text is a legitimate optimization axis.

A second, quieter insight lives in the compress sub-tool: instruction files that load on every session represent a recurring token tax. Compressing them is a form of amortized optimization — you pay the compression cost once and save on every subsequent session.

## Best used when

- Workflows involve long coding sessions where output verbosity slows reading and inflates cost, and the content is primarily technical (debugging, code review, architecture decisions).
- Instruction files (project rules, preferences, memory) have grown large and load on every session, making input token reduction worthwhile.
- The LLM's audience is an experienced practitioner who does not need pedagogical scaffolding, hedging, or step-by-step narration of obvious actions.
- Output is consumed ephemerally (chat, terminal) rather than published or stored as prose artifacts.

## Poor fit when

- The output is itself a prose deliverable: creative writing, documentation, blog posts, reader-facing copy. Compressed telegraphic style would degrade the artifact, not just the medium.
- The workflow depends on nuanced tone, voice, or register. Caveman's compression rules are blunt instruments that strip connective tissue indiscriminately; they cannot distinguish between filler and intentional rhetorical structure.
- Instruction files contain carefully worded conditional rules where articles and conjunctions carry semantic load. The compress tool's "preserve technical terms" heuristic does not cover logical nuance in rule prose.
- Multiple contributors maintain shared instruction files. The backup-file workflow (FILE.original.md as human-readable, FILE.md as compressed) adds drift risk if the original is edited without re-compressing.

## Verdict

The tool itself is not the right fit for workflows that include creative writing or prose-quality output, because its compression rules are context-blind and conflict with any style or voice requirements. The principle it demonstrates is directly applicable, however: instruction files that load on every session should be written in dense, imperative, filler-free prose from the start, as a matter of authoring discipline rather than automated post-processing. This avoids the drift risk of maintaining two copies while capturing most of the input token savings. For output, a lighter version of the same idea — instructing the model to be concise for technical exchanges and explicit about when to switch to full prose — achieves the core benefit without an external dependency. The adapt verdict reflects this: the lesson is "write your instruction files tight and tell the model to skip filler in technical exchanges," not "install this skill."
