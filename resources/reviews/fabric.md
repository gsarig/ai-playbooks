---
title: "Fabric"
url: https://github.com/danielmiessler/Fabric
author: "Daniel Miessler"
date_evaluated: 2026-04-10
verdict: catalog
tags: [ai-framework, cli, prompt-patterns, go, multi-provider]
---

## What it proposes

Fabric is a Go-based CLI framework that organizes AI prompts into reusable "Patterns," each a markdown system prompt targeting a specific real-world task (summarizing articles, extracting wisdom from videos, rating content quality, generating essays, etc.). The user pipes content through a pattern via the command line (`echo "text" | fabric -p extract_wisdom`), and the framework handles model routing, provider selection, and output formatting. It ships with 200+ community-contributed patterns and supports custom ones. Patterns can be mapped to specific models, so a cheap summarization task can route to a local Ollama model while a nuanced analysis routes to a frontier API. It also offers a REST API server mode and helper utilities for tasks like converting codebases to context or transcribing speech.

The core mechanism is standardization of prompt structure and invocation. Rather than maintaining ad-hoc prompts across tools, Fabric centralizes them as named, versioned, shareable units that compose with Unix pipes.

## Best used when

- The primary workflow is **terminal-centric text processing** where content flows through pipes: logs, transcripts, scraped web pages, CLI output. Fabric excels as glue in shell pipelines.
- The user needs to run the **same prompt against many inputs** in batch (e.g., summarizing 50 articles, extracting action items from a folder of meeting notes). The CLI-first design makes scripting trivial.
- Multiple AI providers or local models are in play and the user wants a **single interface** to route tasks to the right model without switching tools.
- A team wants to **share and version-control prompt patterns** as a library, benefiting from Fabric's large community catalog as a starting point.
- The workflow does not require deep integration with a specific editor, vault, or IDE; Fabric operates at the shell layer and is tool-agnostic.

## Poor fit when

- The workflow already uses an AI-native CLI tool (such as Claude Code) that supports custom skills, slash commands, and project-level prompt management. In that setup, Fabric's pattern system is a redundant abstraction layer that duplicates capability without adding meaningful leverage. The overhead of maintaining patterns in two systems outweighs the benefit.
- The work centers on **structured vault content** (Obsidian notes, frontmatter, wikilinks, canvas files) where the AI tool needs filesystem awareness, file-editing capabilities, and vault-specific conventions. Fabric's stdin/stdout model treats content as flat text; it cannot read a vault, resolve links, or write edits back into specific files.
- Prompt iteration is tightly coupled with code or file changes in the same session. Tools that combine code editing, shell access, and AI reasoning in one loop are a better fit than a separate CLI that only handles the prompt layer.
- The pattern library's breadth is a drawback rather than a benefit. Most of the 200+ patterns are generic and require significant pruning or rewriting to match a specific domain's quality bar. For users who maintain a small, curated set of prompts, the community catalog adds noise.

## Verdict

**Catalog.** Fabric is a well-engineered, actively maintained tool that solves a real problem: organizing and invoking AI prompts from the command line in a composable, provider-agnostic way. Its pattern library and Unix-pipe philosophy make it genuinely useful for shell-heavy batch-processing workflows. However, for projects built around an AI-native coding tool with its own skill/prompt system and deep filesystem integration, Fabric occupies the same conceptual space (reusable prompt patterns, CLI invocation, model routing) while lacking the tight editor and vault awareness that those workflows depend on. It is not a poor tool; it is a parallel tool aimed at a different integration layer. Worth knowing about for contexts where the primary interface is a shell pipeline rather than an integrated agent, but adopting it alongside an existing agent-based setup would create redundancy without clear payoff.
