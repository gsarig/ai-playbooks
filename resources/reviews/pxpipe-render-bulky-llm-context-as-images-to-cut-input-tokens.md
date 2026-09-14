---
title: "pxpipe: render bulky LLM context as images to cut input tokens"
url: https://github.com/teamchong/pxpipe
author: "teamchong"
date_evaluated: 2026-07-05
verdict: catalog
tags: [token-efficiency, context-compression, claude-code, proxy, vision-tokens, local-first]
---

## What it proposes

A local proxy sits between the agent harness and the model API on `127.0.0.1`, intercepts each `/v1/messages` request, and rewrites the bulky, token-dense parts (the static system prompt and tool docs, large tool-result bodies, older collapsed history) into compact PNG image blocks before the request leaves the machine. The premise is that an image's token cost is fixed by its pixel dimensions, not its text content, so dense content packs roughly 3x more characters per token as an image than as text. A per-request profitability estimator, calibrated on production traffic, images a block only when the character-per-token math beats leaving it as text; sparse prose stays text. Recent turns stay text, prompt caching is preserved, and every conversion is measured against a free `count_tokens` counterfactual logged to `~/.pxpipe/events.jsonl`. It ships as both a drop-in proxy and a library. Reported end-to-end savings run 59 to 70 percent on token-dense, API-billed workloads.

## Best used when

The workload is genuinely token-dense (code, JSON, tool output at roughly 1 to 2 characters per token) and sessions carry large, mostly static context: a big system prompt, extensive tool definitions, and long histories that would otherwise be re-sent each turn. It pays off most when billing is per-token (API usage), where the input-token cut maps directly to a lower bill, and when the reader model is on the supported allowlist (the tool's own benchmarks show its default reader handling dense renders at high fidelity while flagging misreads rather than fabricating). It also suits anyone who wants context-window headroom on long-running tasks, since imaged bulk occupies far fewer tokens in the window regardless of billing model.

## Poor fit when

Sessions are modest-context and correctness-sensitive: short repo edits or note/vault workflows where the total context is small enough that the profitability gate rarely fires, so the savings never compound, while the residual risk remains. That risk is the core hazard: the compression is lossy and its failures are silent confabulations, not errors. Exact strings read out of imaged content (identifiers, hashes, file paths, dates, proper names, frontmatter values) are unreliable, and the model returns a plausible wrong value with no signal that it misread. Workflows whose correctness hinges on byte-exact recall of such strings are exactly where a silent wrong answer does the most damage. It is also a poor fit when the preferred reader model sits outside the supported set (some strong models misread a meaningful fraction of renders and are opt-in for that reason), and it delivers no dollar savings to users on flat subscription plans rather than per-token billing, though the context-window headroom still applies. Non-Latin scripts are handled conservatively, and PNG encoding adds latency to large requests.

## Verdict

Catalog. This is a well-engineered, honestly documented, actively maintained, local-first tool that does what it claims on the workloads it targets, and its author is unusually candid about the failure mode: lossy image rendering produces silent confabulations of exact strings, which the README states plainly and mitigates by keeping recent turns and byte-exact content as text. The reason it lands as catalog rather than adopt is scope, not quality. The savings compound only when sessions carry large, token-dense, mostly static context, which is the enterprise or heavy-repo profile, not the modest-context sessions typical of note-based or small-repo work, where the profitability gate would leave most content as text and the net benefit is marginal. Against that thin upside sits a real downside for correctness-sensitive work: silent misreads of paths, IDs, dates, and names are the failure mode most likely to corrupt a structured record without anyone noticing. For per-token-billed users running genuinely large, dense contexts it is worth a serious look, and its measurement discipline (a free counterfactual logged per request) makes it easy to prove the savings on your own traffic before trusting it. For everyone else the conditions that make it pay off rarely arise, and no in-scope alternative is strictly better at the same job, so it belongs in the catalog rather than the toolkit.
