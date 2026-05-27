---
title: "Modern Web Guidance: on-demand web platform expertise for coding agents"
url: https://developer.chrome.com/docs/modern-web-guidance
author: "Google Chrome team"
date_evaluated: 2026-05-25
verdict: catalog
tags: [claude-code, skills, web-platform, css, frontend, agent-context, preview]
---

## What it proposes

An agent skill (a `SKILL.md` plus a CLI) that injects curated modern web-platform knowledge into a coding agent's context window on demand, rather than relying on whatever the model absorbed from training data. The premise: LLM training corpora are dominated by legacy code, so agents default to bloated, dated patterns even for tasks that now have native platform solutions, and even when a model knows an API exists it lacks the density of production-ready implementation patterns.

The mechanism is a retrieval CLI with three commands: `install` (an interactive wizard that places the SKILL.md), `search "<query>"` (find relevant guides by natural-language description), and `retrieve "<guide-id>"` (pull a specific guide into context). It ships roughly 102 feature guides across CSS and layout (container queries, subgrid, oklch, text-wrap, line-height trimming), HTML and DOM, UX (View Transitions, entry/exit animations), performance (instant preloading, INP diagnostics, scheduler.yield), forms and UI (Anchor Positioning, Popover API, `<dialog>`, `:user-invalid`, field-sizing), accessibility (error announcements, focus management), and built-in browser AI APIs. The guides are deliberately token-efficient: evals prune content the models already know reliably, so only the high-value, hard-to-recall patterns are loaded. It installs via its own CLI, via Vercel's Agent Skills, or as a plugin/marketplace entry for Claude Code, Copilot CLI, and Antigravity CLI, and integrates with Chrome DevTools for agents for real-time auditing. Supported by the Chrome and Edge teams; currently a preview release.

## Best used when

- The agent regularly builds or maintains interactive web UI: components (accordions, tab bars, dashboard cards), dialogs and tooltips, forms, animations, or anything touching layout and styling.
- A codebase is migrating off legacy patterns (jQuery modals to `<dialog>`, custom tooltip positioning to Popover API plus Anchor Positioning) and you want the agent to reach for native platform features instead of reinventing them in JavaScript.
- Performance and accessibility of a real front end matter (INP/LCP work, focus management, accessible error announcements) and you want expert-curated, current guidance loaded just-in-time rather than trusting the model's stale defaults.
- You want the knowledge available across multiple agent CLIs from one source, loaded only when a task actually needs it, keeping the context budget lean.

## Poor fit when

- The project's centre of gravity is knowledge work, writing, or content curation rather than building feature-rich web applications. The guidance targets dialogs, popovers, anchor positioning, view transitions, and similar interactive primitives that such projects rarely implement, so the skill sits idle.
- The only web surface is a static content site (a blog, a documentation site, an Astro site rendering markdown). These benefit marginally at most: they style and lay out content but seldom build the interactive, stateful UI the bulk of the guides address, and a static-site generator's own conventions usually dictate the limited CSS involved. Installing it adds an agent skill that almost never fires.
- The team has no recurring front-end UI workload at all. The payoff scales with how much interactive web code the agent writes; near zero such work means near zero return, even though the tool itself is free and local.

## Verdict

Catalog. This is a genuinely high-quality, well-targeted tool: free, local (npx/CLI), backed by the browser vendors who define the platform, and built on a sound insight that agents default to dated patterns and benefit from token-efficient, eval-pruned, just-in-time guidance. For any project whose agent routinely builds modern web UIs, `adopt` is the obvious call. The reason it lands at catalog rather than adopt here is scope, not quality or cost: a workflow centred on vault/knowledge work, writing, and static content sites rarely produces the interactive web features the guides specialise in, so the skill would seldom activate. The preview-release status is a minor secondary caveat (surface area and guide IDs may shift), but it does not drive the verdict; even at 1.0 the applicability gap would remain. Worth knowing about and worth adopting immediately should a front-end-heavy project enter the picture; not worth installing into a project that doesn't build interactive web UI. The transferable idea, independent of web development, is the retrieval pattern itself: an eval-pruned, search-and-retrieve knowledge skill that loads only what the model demonstrably doesn't already know, which generalises to any domain where an agent's training-data defaults are stale.
