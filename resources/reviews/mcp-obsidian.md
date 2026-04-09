---
title: "mcp-obsidian"
url: https://github.com/MarkusPfundstein/mcp-obsidian
author: "Markus Pfundstein"
date_evaluated: 2026-04-10
verdict: skip
tags: [obsidian, mcp, vault-access, llm-tooling]
---

## What it proposes

An MCP server that gives LLMs access to an Obsidian vault through a network API layer. It wraps the Obsidian Local REST API community plugin, exposing vault operations (list files, read contents, search, patch content relative to headings or frontmatter, append, delete) as MCP tools. The server runs as a Python process (installed via `uvx`), connects to the REST API plugin inside Obsidian over HTTP (default `127.0.0.1:27124`), and authenticates with an API key. Designed primarily for Claude Desktop's MCP integration.

## Best used when

- The LLM client lacks direct filesystem access and MCP is the only way to reach vault contents (e.g., Claude Desktop on macOS/Windows without shell access).
- Obsidian must be running during LLM interactions anyway, and the REST API plugin is already installed for other automation purposes.
- The workflow benefits from Obsidian-aware operations like patching content relative to a heading or block reference, rather than raw file edits.

## Poor fit when

- The LLM tool already has native filesystem access (Read, Write, Edit, Glob, Grep or equivalent). In that case, the MCP server adds a mandatory runtime dependency (Obsidian must be open), an HTTP intermediary, an API key to manage, and a Python process to keep running — all to replicate capabilities the tool already has with lower latency and fewer failure modes.
- The vault lives on the local filesystem and the workflow prioritizes offline, self-contained tooling. The REST API plugin requires Obsidian's Electron process to be running, a heavy prerequisite for CLI-driven automation.
- Vault operations need to work in CI, on a server, or in any context where Obsidian cannot run as a GUI application.

## Alternatives

For CLI-based LLM tools with direct filesystem access, vault `.md` files can be read, searched, and edited natively without any intermediary. Heading-aware patching can be handled by the LLM itself when it reads the file content. Native file operations are the alternative — no dedicated tool needed.

## Verdict

mcp-obsidian solves a real problem for LLM clients sandboxed from the filesystem, but becomes pure overhead when the tool already has direct access to the vault's markdown files. It introduces three runtime dependencies (Obsidian running, the REST API plugin enabled, the MCP server process) to approximate what filesystem access provides natively. It is well-maintained and the right choice for Claude Desktop users. For CLI-based workflows where the vault is on the local filesystem, skip it.
