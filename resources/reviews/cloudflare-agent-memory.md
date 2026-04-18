---
title: "Cloudflare Agent Memory"
url: https://blog.cloudflare.com/introducing-agent-memory/
author: "Cloudflare"
date_evaluated: 2026-04-18
verdict: catalog
tags: [memory, agents, cloudflare, managed-service, rrf, hyde, compaction]
---

## What it proposes

Agent Memory is a managed Cloudflare service (private beta) that hooks into an agent's compaction moment to extract, classify, and store knowledge from conversations so it does not get discarded when context is shortened. Ingestion runs a two-pass extractor (full + detail) followed by an 8-check verifier and a classifier that sorts memories into facts (atomic, topic-keyed, superseded via forward-pointer version chains), events, instructions, and tasks. Deterministic SHA-256 IDs make re-ingestion idempotent, and embedding text is augmented with 3-5 auto-generated search queries to bridge the write/read vocabulary gap.

Retrieval fans out across five parallel channels (full-text with Porter stemming, exact fact-key lookup, raw message search, direct vector, HyDE vector) and fuses them with Reciprocal Rank Fusion before a synthesis model produces a natural-language answer. Temporal reasoning is handled deterministically rather than by the LLM. Each profile lives in its own SQLite-backed Durable Object plus a Vectorize index, uses Workers AI for extraction and synthesis, and is accessed via a Worker binding or REST API. Cloudflare commits to full memory exportability.

## Best used when

- The agent already runs on Cloudflare Workers or the Cloudflare Agents SDK, and adding a managed binding is a natural fit.
- The project needs a production-grade, multi-session, multi-user memory layer without building the extraction/classification/retrieval stack from scratch.
- Cross-session or cross-team shared memory is a requirement (coding agents, code review bots, support chat) and a cloud dependency is acceptable.
- Benchmarked retrieval quality across LongMemEval/LoCoMo/BEAM matters more than architectural control.

## Poor fit when

- The workflow is local-first and memory should live on disk under user control.
- Agents run outside Cloudflare's edge and adding a vendor dependency for memory is disproportionate to the value.
- The project cannot accept a private-beta, waitlisted, non-self-hostable service with pricing yet to be disclosed.
- Memory contents are sensitive and sending them through Workers AI for extraction is undesirable.

## Alternatives

- **MemPalace** (`mempalace.md`) — local ChromaDB + MCP tool surface, usable today from Claude Code, at the cost of a less polished extraction/classification pipeline.
- Rolling your own on top of an embedding store plus a small extractor remains viable; the useful ideas from this post (HyDE channel, query-prepended embeddings, fact version chains, deterministic temporal handling, RRF fusion) are transferable patterns, not Cloudflare-specific.

## Verdict

A well-engineered managed memory layer whose design choices (compaction-time ingestion, typed memory taxonomy with superseded fact chains, multi-channel retrieval fused by RRF, HyDE for vocabulary bridging, deterministic temporal arithmetic) are worth studying even if the service itself is not adopted. For a local-first setup with no Cloudflare footprint, the product is out of scope; the architectural patterns, however, are reusable reference material when designing or evaluating any agent memory system. Cataloged for the ideas, not the binding.
