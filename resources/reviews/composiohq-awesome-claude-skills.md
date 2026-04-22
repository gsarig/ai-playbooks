---
title: "ComposioHQ/awesome-claude-skills"
url: https://github.com/ComposioHQ/awesome-claude-skills
author: "ComposioHQ (community-curated)"
date_evaluated: 2026-04-22
verdict: catalog
tags: [claude-skills, directory, awesome-list, discovery, composio]
---

## What it proposes

An "awesome list" style directory of Claude Skills, grouped by category (document processing, dev tools, data, business, writing, creative, productivity, security, and a large Composio-powered SaaS automation section covering 78+ apps). Each entry is a pointer to an external skill repository or plugin; the list itself contains no implementation. It also bundles a short "Getting Started" and "Creating Skills" primer (SKILL.md structure, YAML frontmatter, best practices) and promotes Composio's `connect-apps` plugin for binding Claude to 500+ SaaS apps via API key. The mechanism is discovery: a flat index you scan when looking for a skill that already exists before writing one from scratch.

## Best used when

Scouting for an existing skill before building one, particularly in well-trodden categories (docx/pdf/pptx/xlsx processing, Playwright, postgres read-only SQL, youtube-transcript, article-extractor, git worktrees, MCP builder, Skill Creator). Useful as a periodic survey to see what patterns the community is converging on, and as a jumping-off point when an unfamiliar skill name appears in discussions. The SaaS automation index is handy if evaluating whether a specific app already has a Composio integration rather than writing a bespoke MCP.

## Poor fit when

Looking for curation or quality signals: entries are listed, not vetted, so the index flattens serious skill libraries (Anthropic's document skills, obra/superpowers, addyosmani, WordPress) and one-off experiments into the same bullet list. Anything under "App Automation via Composio" requires a Composio API key and routes actions through their cloud, which is a poor fit for local-first, self-hosted, or privacy-sensitive workflows. The "Creating Skills" section is a shallow primer compared to dedicated skill-authoring references and should not be treated as authoritative. The list also goes stale quickly; entries linked today may be abandoned or renamed tomorrow.

## Verdict

Catalog. This is a discovery index, not a methodology or a skill library with its own architectural stance, so it does not compete with the superpowers/addyosmani/WordPress reviews already on file; those evaluate specific implementations, this points at many. Keep it bookmarked as a scouting tool before writing a new skill in a common category, and mine it occasionally for pointers to review individually, but do not treat inclusion as endorsement and do not rely on the Composio automations (cloud-only, API-key-gated) for workflows that should run locally. The evaluation targets here are the linked projects, not this page.

## Related

- `superpowers.md` — a specific composable skills framework; this list points at it among many others.
- `addyosmani-agent-skills.md` — a specific SDLC skill library; listed here without the architectural context the dedicated review provides.
- `wordpress-agent-skills.md` — WordPress-specific skill library; similarly flattened to a single bullet in this index.
