---
title: "prompt-master"
url: https://github.com/nidhinjs/prompt-master
author: "nidhinjs"
date_evaluated: 2026-04-26
verdict: skip
tags: [claude-skill, prompt-engineering, meta-prompting, prompt-templates]
---

## What it proposes

A Claude skill (SKILL.md-based, installable via Claude.ai sidebar or by cloning into `~/.claude/skills/`) that acts as a meta-prompter: you describe what you want from some target AI tool, and the skill produces a finished prompt aimed at that tool. The pipeline is fixed: detect the target tool from 30+ profiles (Claude, ChatGPT, Cursor, Midjourney, ComfyUI, Bolt, v0, Devin, ElevenLabs, Zapier, etc.), extract nine intent dimensions (task, input, output, constraints, context, audience, memory, success criteria, examples), ask up to three clarifying questions if critical info is missing, route to one of twelve prompt templates (RTF, CO-STAR, RISEN, CRISPE, Chain of Thought, Few-Shot, File-Scope, ReAct + Stop Conditions, Visual Descriptor, Reference Image Editing, ComfyUI, Prompt Decompiler), apply five techniques as needed (role assignment, few-shot, XML tags, grounding anchors, CoT), audit against 35 catalogued anti-patterns ("credit-killers" across task, context, format, scope, reasoning, agentic categories), and emit a single copyable prompt block plus a one-line strategy note. A Memory Block prepends prior decisions from the conversation so the generated prompt does not contradict earlier work.

## Best used when

Operators who hand-write prompts for many heterogeneous downstream tools (image generators, video AI, voice AI, no-code automators, agentic IDEs they do not normally use) and want a consistent intake template that forces them to specify task, output format, constraints, and success criteria before firing. Also reasonable for users who are new to prompt engineering and want a structured catalogue of templates and anti-patterns surfaced inside their main chat tool rather than read from a blog post.

## Poor fit when

The user already drives one or two AI tools daily and has internalised what a good prompt for those tools looks like; the meta-prompting layer then adds a turn of friction (describe the prompt, answer clarifying questions, copy the output, paste it elsewhere) for prompts they could have written directly. Particularly weak inside Claude Code itself, where the natural unit of reuse is a domain-specific skill or CLAUDE.md rule that fires automatically on the real task, not a generic prompt-writing skill that produces text the user must then manually route. The 12-template / 5-technique / 35-pattern taxonomy is presented as authoritative without sourcing or evaluation, and the version history (removing "fabrication-prone techniques" in 1.2.0, rebuilding around an unexplained "PAC2026 positional structure" in 1.3.0) suggests the framework is still churning. There is no evidence (benchmarks, examples, before/after comparisons) that the generated prompts outperform a competent hand-written one for the tools the user actually knows.

## Alternatives

For Claude Code specifically, writing a focused SKILL.md per recurring task gives the same structuring benefit with no meta layer: the skill fires on the real task and bakes the constraints into its own instructions. For a curated prompt library invoked across tools, Fabric (already reviewed) covers the centralised-pattern use case via CLI. For internalising prompt-quality heuristics, reading the underlying frameworks (CO-STAR, RISEN, etc.) directly is faster than routing through a generator.

## Verdict

Skip. The skill packages a reasonable amount of prompt-engineering folklore behind a clean pipeline, but it solves a problem (prompt-writing as a discrete artifact to be generated and then copied elsewhere) that mostly exists for users who have not yet built per-task skills or per-tool muscle memory. For anyone already operating a SKILL.md ecosystem, the right unit of reuse is a skill that does the work, not a skill that writes the prompt that does the work; the meta-prompting layer adds turns and credits rather than saving them. The taxonomy is presented without evidence, the framework has changed shape across recent versions, and the named "PAC2026 positional structure" is not explained in the README. Worth a skim for the 35-pattern checklist as a self-review prompt, but not worth installing.
