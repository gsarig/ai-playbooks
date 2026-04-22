---
title: "video-use — edit videos with Claude Code"
url: https://github.com/browser-use/video-use
author: "browser-use"
date_evaluated: 2026-04-21
verdict: catalog
tags: [video-editing, claude-code, skill, multimodal, ffmpeg, transcription]
---

## What it proposes

A Claude Code skill that turns a folder of raw video takes into a finished cut through conversational direction. The core mechanism is a two-layer representation that lets the model edit without ever watching frames. Layer one is an always-loaded word-level transcript produced by ElevenLabs Scribe, packed across all takes into a single ~12KB markdown file with timestamps, speaker diarization, and audio events. Layer two is an on-demand `timeline_view` tool that renders a filmstrip plus waveform plus word-label PNG for any requested time range, called only at decision points. The pipeline is transcribe → pack → LLM reasons → produce an EDL (edit decision list) → render via ffmpeg → self-eval the render at each cut boundary, with up to three auto-fix retries before the user sees a preview. Filler-word removal, 30ms audio fades on cuts, color grading, subtitle burn-in, and parallel sub-agent generation of Manim/Remotion/PIL animation overlays are all built in. Session state persists in a `project.md` so subsequent edits resume context. The stated design analogy is browser-use's structured-DOM approach, applied to video instead of web pages.

## Best used when

Editing longer-form spoken-word footage where the cut is driven by speech boundaries: talking-head videos, interviews, tutorials, podcast video, launch or explainer content. It thrives when there are many takes to sift through, filler words and dead space dominate the cleanup cost, and the editor wants conversational direction rather than timeline scrubbing. The text-first representation is genuinely clever for content where the audio track carries the edit logic. Works well when the user already pays for ElevenLabs or is willing to, and when ffmpeg workflows are acceptable.

## Poor fit when

Content is primarily visual rather than spoken: B-roll montages, music videos, silent tutorials, screen recordings without narration, or anything where cut points are dictated by visual rhythm rather than word boundaries. The transcript-first abstraction loses its leverage there. Also a poor fit when the user has no ElevenLabs API key and no appetite for adding a paid transcription dependency, since Scribe is the ingestion layer the whole design rests on. Not relevant for workflows that do not involve video production at all; most knowledge-work, writing, and tracking vaults have no surface where this applies. Installation assumes macOS-style Homebrew; Linux or WSL users need to translate the ffmpeg/yt-dlp install steps themselves, though the skill itself should run fine once the binaries are present.

## Verdict

Catalog. The two-layer "read the video, do not watch it" representation is a legitimately interesting idea and the self-eval-before-preview loop is a sound production pattern worth remembering. The tooling is well-scoped, open source, and lives as a Claude Code skill, which matches how personal skill libraries are typically organized. It does not warrant adoption right now because video editing is not a recurring workflow in most text, tracking, or fiction-writing contexts, and the ElevenLabs dependency is a non-trivial ongoing cost for a capability that sits idle most of the time. Worth knowing about the moment a spoken-word video project appears: launch video, course material, interview cleanup. Until then, the architectural lesson — give the model a compact structured view of the medium plus a zoom-in tool for decision points, rather than dumping raw frames — is the more portable takeaway and transfers to any domain where an LLM needs to reason over bulky media.
