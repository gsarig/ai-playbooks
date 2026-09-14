---
title: "pi-claude-bridge: Claude Code as a provider inside another agent harness"
url: https://github.com/elidickinson/pi-claude-bridge
author: "elidickinson"
date_evaluated: 2026-08-07
verdict: catalog
tags: [agent-harness, interop, delegation, subagents, claude-code, agent-sdk, tooling]
---

## What it proposes

An extension for a third-party agent toolkit that mounts Claude Code inside it through the Claude Agent SDK, so a subscription-billed coding agent becomes usable in a harness that is not its own CLI. It does this two ways.

The first is a **provider**. Installing the extension registers the Claude model family in the host toolkit's model picker; selecting one routes the host's requests through the Agent SDK, which spawns a real Claude Code process while the host's TUI renders streaming output and tool calls as if they were native. Bridging runs both directions: the host's own tools are exposed to Claude Code so edits, shell commands, and MCP servers still execute under the host's display and permission layer, and the host's project context files and skills block are appended to the system prompt so instructions carry across. Sessions persist and resume between turns, mid-turn steering lands at tool boundaries rather than after the turn completes, and shell calls get a default timeout to match the vendor CLI's own. Configuration is a global JSON file with a project-level file merged over it, covering subscription plan (which gates long-context model access), context forwarding, filesystem settings, and MCP trust. MCP servers declared in the machine's vendor config are blocked by default, cloud MCP via account OAuth is blocked unconditionally, and auto-memory is off by default.

The second is an **AskClaude tool**, available whenever a non-Claude provider is driving. It turns Claude Code into a bounded, callable specialist: the host's model passes a prompt and receives an answer or a completed task. Four parameters define each call's contract: permission mode (none, read-only, or full write and shell, disableable in config), model, thinking effort, and whether the delegate inherits conversation history or starts clean. That last one is what makes "implement, then have an isolated instance review the implementation" expressible in a single instruction. The README suggests wiring the tool into project instruction files so delegation happens by policy rather than ad hoc.

Two operational details matter. The README documents that the vendor announced and then unannounced a billing change for Agent SDK tools, and that such tools currently draw on subscription quota exactly as the first-party CLI does. And the maintenance section states plainly that after each upstream CLI release, a hardcoded per-mode disallowed-tools list in the source must be reviewed so newly added agentic tools do not leak into delegate sessions.

## Best used when

- Your daily driver is an agent harness other than the vendor's own CLI, and you want that vendor's strongest models without moving to per-token API billing. This is a real gap: subscription pricing and a preferred TUI are otherwise mutually exclusive.
- You run a multi-provider workflow where a cheaper or faster model drives the session and hands off selectively. The parameters make the handoff a governed contract rather than a free hand: a read-only research call that cannot touch the filesystem, a high-effort planning call, an isolated review call that cannot be anchored by the reasoning that produced the thing it reviews.
- You already cross-check one model's output against another's, and want the second opinion to come from a different runtime with independent tooling rather than the same one twice.
- A single interface matters more to you than a single backend: one TUI, one keybinding set, one set of project instructions, with model choice as a per-turn decision.

## Poor fit when

- The vendor's CLI is already your primary and only harness. The provider half is then a round trip back to the starting point, and not a free one: a process boundary, a second config file with its own merge semantics, a separate debug log, a maintenance obligation tied to someone else's release cadence, and a hardcoded model list that must be edited in source because the host toolkit's model-override mechanism does not reach extension-registered providers. The delegation half fares no better, since permission-scoped subagents, per-call model selection, effort control, and clean-context isolation are first-party features there already.
- The work is not software. Everything the bridge adds concerns tool surface, permission gating, and runtime interop. When the bottleneck is judgement over prose, records, or structured notes, a second engineering-grade agent runtime adds no capability and the extra moving parts are pure cost.
- You need the billing basis to be stable. By the README's own account this policy was announced, reversed, and now sits in a favourable position; economics that have moved once can move again, and if they do, the provider half becomes a metered API bill with no code change required to trigger it. That is a structural caveat about wrapping a first-party SDK, not a criticism of this implementation.
- You run agents under tight filesystem confinement. The bridge spawns real subprocesses and writes to the vendor's session-state directory; a sandbox that blocks that directory makes session resume fail outright.
- You would be building a critical workflow on it without a fallback. Maturity signals argue for patience: a repo a few months old, roughly thirty commits, no tagged releases, a single maintainer, derived from an earlier project, with correctness of the tool-gating lists explicitly dependent on a human reviewing them after each upstream release.

## Verdict

Catalog. This is a well-built extension solving a real problem for a specific population: people whose primary harness is not the vendor's CLI and who want its models on subscription terms, plus anyone deliberately running a multi-runtime setup where one agent calls another as a bounded specialist. For a workflow already committed to that CLI as its single harness, both halves are redundant, the provider by definition and the delegation tool because the same controls exist natively; and non-software domains gain nothing from a second coding-agent runtime. Worth knowing about rather than installing. The part that transfers regardless of implementation is the shape of the delegation contract: treating another agent runtime as a tool whose call declares permission mode, model, reasoning effort, and whether it inherits or is denied conversation history. That is a good way to specify any agent-to-agent handoff, in-harness or across harnesses.
