---
title: "DESIGN.md specification"
url: https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/
author: "Google Labs"
date_evaluated: 2026-04-22
verdict: catalog
tags: [design-systems, design-tokens, ai-agents, specification, ui-design]
---

## What it proposes

A file format for expressing a visual design system in a single document that both humans and AI agents can read. YAML front matter holds machine-readable tokens (colors, typography, spacing, rounded corners, components with `{token.reference}` syntax); the markdown body holds prose rationale under a fixed set of `##` sections (Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts). Two CLI tools ship with the spec: `lint` validates structure, token references, and WCAG contrast ratios, emitting structured JSON; `diff` compares two versions for token-level and prose regressions. Consumers tolerate unknown sections and unknown tokens but reject duplicate section headings. The point is to stop regenerating design systems per project and to give AI agents explicit intent rather than leaving them to guess from screenshots or ad hoc prompts.

## Best used when

A project produces UI artifacts (web apps, mobile apps, marketing pages, design-heavy documents) and uses AI agents to generate or modify visual output. It also fits teams maintaining multiple products that should share a visual language but currently rely on implicit conventions, and any setup where a designer wants to constrain agent output to a defined palette, type scale, and component vocabulary instead of negotiating it prompt by prompt.

## Poor fit when

The work is text-first with no meaningful visual surface — fiction drafting, note-taking vaults, knowledge management, research archives, data pipelines. For those, the design system is either "whatever the reader app renders" or entirely irrelevant, and a DESIGN.md file would sit unused. The spec is also tightly coupled to the Stitch tooling for generation; contributing to the format without Stitch means hand-authoring YAML, which removes much of the ergonomic appeal. It is alpha, so the schema may shift; projects needing stability today should wait.

## Verdict

Catalog. The idea of a single file that merges machine-readable tokens with human-readable rationale, validated by a linter and diffable across versions, is a clean answer to a real problem — AI agents need explicit design intent, not guesses. For any project with a UI surface and agent-assisted design workflow, it is worth knowing about and likely worth trying once past alpha. For text-and-knowledge workflows with no visual system to express, it has no application: there is no design vocabulary to codify, and the overhead of maintaining a spec file would not pay back. The CLI tools are standard `npx` invocations and run fine in a WSL2/Ubuntu + Claude Code setup, so adoption is not blocked by tooling constraints; scope is the only reason to pass. Revisit if a project ever grows a designed UI layer.
