---
title: "MarkItDown"
url: https://github.com/microsoft/markitdown
author: "Microsoft"
date_evaluated: 2026-04-11
verdict: catalog
tags: [file-conversion, markdown, pdf, document-processing, python, cli]
---

## What it proposes

MarkItDown is a Python utility that converts a wide range of file formats (PDF, Word, Excel, PowerPoint, HTML, images, audio, EPub, and more) into Markdown. The mechanism is straightforward: feed it a file path or URL, and it outputs structured Markdown that preserves headings, lists, tables, and links. It works as both a CLI tool (`markitdown file.pdf > output.md`) and a Python library, with optional dependency groups so you only install what you need. It also offers an MCP server for direct integration with LLM tool-use workflows, a plugin system for third-party format support, and optional LLM-powered image descriptions via any OpenAI-compatible client. No temporary files are created during conversion, and it runs entirely locally with no mandatory cloud dependencies.

The core value proposition is preparing non-Markdown documents for LLM consumption. Markdown is token-efficient, preserves document structure, and is natively understood by language models, making it a better intermediate format than raw text extraction.

## Best used when

- A workflow requires ingesting external documents (research PDFs, spreadsheets, slide decks) into a Markdown-native environment like an Obsidian vault, and doing so programmatically or in batch.
- Building automation pipelines where non-Markdown source material needs to be converted before LLM processing, summarization, or analysis.
- The source material lives in heterogeneous formats and a single tool that handles all of them is preferable to maintaining format-specific converters.
- Local-only operation matters; the core conversion pipeline has no cloud requirement, which suits privacy-sensitive or offline workflows.
- An MCP-based toolchain is in use and would benefit from letting an LLM agent request file conversions directly.

## Poor fit when

- The primary workflow is authoring and organizing Markdown natively (as in most Obsidian vault work). MarkItDown solves an ingestion problem, not a writing or knowledge-management problem. If the vault content is already Markdown, there is nothing for this tool to do.
- High-fidelity PDF conversion is critical. Lightweight converters tend to struggle with complex layouts, scanned documents, or PDFs with heavy use of columns and figures. The Azure Document Intelligence integration can help, but that reintroduces a cloud dependency.
- The workflow is purely note-taking, fiction writing, or journal-based. These vault types rarely need to ingest Word documents or spreadsheets.
- Obsidian-specific Markdown features (wikilinks, callouts, properties/frontmatter) are needed in the output. MarkItDown produces standard Markdown; any Obsidian-flavored formatting would require a post-processing step.

## Verdict

Catalog. MarkItDown is a well-maintained, practical tool for converting documents into LLM-friendly Markdown, and its local-first design, broad format support, and MCP server make it a strong choice in its domain. However, that domain is document ingestion, which is tangential to workflows centered on authoring, organizing, and processing content that already lives in Markdown. For vault-based creative or personal knowledge work, there is rarely a need to bulk-convert PDFs or slide decks into notes. The tool is worth knowing about for projects that do involve heavy document ingestion (research pipelines, corporate knowledge bases, archival workflows), but it does not address a recurring need in the type of vault work this library serves.
