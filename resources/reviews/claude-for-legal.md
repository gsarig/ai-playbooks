---
title: "Claude for Legal"
url: https://github.com/anthropics/claude-for-legal
author: "Anthropic"
date_evaluated: 2026-05-17
verdict: catalog
tags: [legal, plugin-suite, managed-agents, mcp-connectors, practice-profile, cold-start-interview, trust-layer, scheduled-agents]
---

## What it proposes

A reference suite of Claude Code plugins and Managed Agents for legal work, organised by practice area (commercial, privacy, product, corporate, employment, litigation, regulatory, AI governance, IP, plus clinics and law students). Each plugin bundles named agents (Vendor Agreement Reviewer, NDA Triager, DSAR Responder, Docket Watcher, Claim Chart Builder, and dozens more) exposed as slash commands or scheduled-agent triggers. The same system prompt and skill set run either locally as a Claude Code plugin or remotely via the Managed Agents API.

Three mechanisms are worth naming separately from the legal payload, because they generalise:

1. A `cold-start-interview` skill per plugin that asks structured questions on first use and writes a practice profile to `CLAUDE.md`; every other skill in the plugin reads from that profile, so configuration is captured once and reused.
2. A `legal-builder-hub` trust layer for community-contributed skills: security review, allowlist, license gate, freshness gate, re-scan at update, install log. This is a working pattern for shipping a plugin marketplace without trusting every contributor.
3. Managed-agent cookbooks for scheduled, recurring workflows (renewal watcher, docket watcher, reg-change monitor, diligence grid, launch radar) that combine cron-style triggers with MCP connectors and produce drafts gated behind explicit human approval.

Strong domain discipline runs through the suite: every output is framed as a draft for attorney review, source attribution is required, privilege defaults are conservative, and filing or sending is gated.

## Best used when

The user practises law, supervises legal work, or runs a legal-adjacent operation (in-house counsel, paralegal team, law clinic, compliance function) that touches contracts, privacy requests, dockets, or regulatory monitoring. The MCP connector list (Ironclad, DocuSign, iManage, Everlaw, CourtListener, Westlaw CoCounsel) is the tell: the suite assumes a working seat in a legal SaaS stack.

The non-legal patterns inside it (cold-start interview writing a `CLAUDE.md` profile, builder-hub trust layer for community skills, scheduled-agent cookbooks with human-gated outputs) are reusable in any plugin suite that needs persistent per-user configuration, a community contribution pipeline, or recurring monitoring workflows with conservative defaults.

## Poor fit when

The workflow is creative, personal, or hobbyist with no legal surface. Fiction drafting, plant care logs, personal journals, household tracking, none of the practice-area plugins map onto these. Installing the suite would add ~12 plugins and 80+ agents that never fire, plus connector configuration to SaaS the user does not subscribe to.

The connector dependency is also a hard gate: most of the highest-leverage agents assume a live MCP connection to a paid legal-tech platform. Without those subscriptions the suite degrades to a generic document-review wrapper, which is not where its value sits.

## Verdict

Catalog. This is a high-quality, domain-specific suite from Anthropic itself, with reference patterns (per-plugin practice profile written by a cold-start interview, builder-hub trust layer, scheduled-agent cookbooks, conservative drafting defaults) that are worth knowing about. None of the legal payload applies to fiction, personal, or household vaults, and the connector dependency means even adapting an individual agent for non-legal use would strip out most of what makes it work. The three reusable patterns above are the durable takeaway; the rest sits in the catalogue for anyone evaluating a legal-adjacent project later.
