---
title: "goose: open-source general-purpose AI agent runtime"
url: https://github.com/aaif-goose/goose
author: "Agentic AI Foundation (Linux Foundation)"
date_evaluated: 2026-06-09
verdict: catalog
tags: [agent-runtime, open-source, mcp, cli, local-first, multi-provider, desktop-app]
---

## What it proposes

goose is a general-purpose AI agent that runs locally on your own machine rather than in a hosted environment. It is built in Rust and ships three surfaces over the same core: a native desktop app (macOS, Linux, Windows), a full command-line interface, and an API for embedding the agent into other software. The scope is deliberately broad; beyond writing and editing code, it targets research, writing, automation, and data analysis.

The provider model is open and pluggable. goose works with 15+ LLM backends (Anthropic, OpenAI, Google, Ollama, OpenRouter, Azure, Bedrock, and others), so you can point it at hosted APIs via keys, at fully local models through Ollama, or at existing chat subscriptions (Claude, ChatGPT, Gemini) through ACP (Agent Client Protocol) providers. Capabilities are extended through the Model Context Protocol (MCP): goose connects to 70+ MCP extensions, the same open standard a growing set of agent tools now share, so tool integrations are portable rather than locked to one vendor.

It also supports custom distributions: you can build a branded goose "distro" with providers, extensions, and configuration preset, which is aimed at teams shipping a tailored agent to their users. The project recently moved from its original corporate home (block/goose) to the Agentic AI Foundation under the Linux Foundation, putting governance under a neutral body. License is Apache-2.0, and the repo is large (~48k stars) and actively maintained.

## Best used when

- You want a local-first, vendor-neutral agent runtime and are not already committed to a different one. Running on your own machine with an open license and Linux Foundation governance is a strong fit for anyone wary of lock-in or hosted-only tools.
- You need provider flexibility: switching between hosted APIs, fully local models via Ollama, or reusing an existing chat subscription, without rewriting your workflow each time.
- The work spans more than coding (research, writing, data tasks, general automation) and you want one agent surface rather than a code-specific tool.
- You are shipping an agent to others and want to brand and preconfigure it (the custom-distro path), or you want to embed agent behavior into your own software through the API.
- You value the MCP ecosystem and want extensions that are portable across compatible tools rather than tied to a single product.

## Poor fit when

- You already run your entire workflow on a different agent runtime that has equivalent local-first, multi-provider, and MCP support. goose is a peer to such a runtime, not a complement: adopting it would mean duplicating or replacing existing memory, custom commands, hooks, and rule scaffolding rather than adding a missing capability. The switching cost dominates any marginal gain.
- Your accumulated customization (skills, hooks, slash commands, persistent project memory) is the core value of your setup. That investment is specific to the runtime it was built on and does not transfer to goose, so migrating means rebuilding it.
- You need a single hosted, zero-install experience for non-technical users and do not want to manage a local app or CLI. goose's local-first design is a strength elsewhere but friction here.

## Alternatives

For the specific case of someone already standing on a mature, customized agent runtime with comparable local-first and MCP support, the incumbent runtime is the better option purely on switching cost: the existing customization, memory, and tooling already deliver the capability goose would provide, and none of it transfers. goose is not inferior in the abstract; it is simply redundant once an equivalent runtime is in place.

## Verdict

Catalog. goose is a serious, well-governed, genuinely open-source general-purpose agent runtime, and for anyone choosing an agent platform from scratch (especially someone who prizes local-first operation, provider neutrality, and the MCP ecosystem) it belongs on the shortlist. The reason it lands at "catalog" rather than "adopt" is positional, not qualitative: it is a direct alternative to an agent runtime, so it is only worth adopting by someone who does not already have one they have invested in. For a workflow already built deeply on a comparable runtime, there is nothing to fold in; the value is in knowing the tool exists, what it does well, and when it would be the right call for a fresh setup or a recommendation to others. Worth revisiting only if a future need (a branded distro to ship, or a provider/governance constraint the incumbent cannot meet) changes that calculus.
