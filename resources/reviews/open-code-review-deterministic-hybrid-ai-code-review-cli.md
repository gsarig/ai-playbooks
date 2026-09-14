---
title: "Open Code Review: deterministic-hybrid AI code review CLI"
url: https://github.com/alibaba/open-code-review
author: "Alibaba Group"
date_evaluated: 2026-09-14
verdict: catalog
tags: [code-review, cli, ci-cd, agent-architecture, security-rules, token-efficiency, open-source]
---

## What it proposes

A standalone CLI (`ocr`) that reviews code with an LLM, built on the premise that a purely language-driven review agent is the wrong architecture for the job. The pitch names three failure modes of prompt-driven review: incomplete coverage on large changesets, where the agent quietly skips files; position drift, where a reported issue points at the wrong file or line; and unstable quality, where output swings with prompt wording and is hard to debug. Its answer is to pull the parts that must not go wrong out of the model's hands entirely. Deterministic code decides which changed files are in scope, groups related files into bundles (co-changing i18n message files, for example) so each bundle runs as an isolated sub-agent context, and matches review rules to each file through a template engine rather than asking the model to select them. Two further modules run after generation: one verifies and corrects comment positions against the real diff, another checks comment content. The LLM is left with the parts that genuinely need judgment, working from scenario-tuned prompts and a deliberately pruned toolset derived from analysis of production tool-call traces rather than a generic agent toolkit.

Practically, it ships `ocr review` for workspace, branch-range, or commit diffs and `ocr scan` for whole-file review where no meaningful diff exists, plus a built-in multi-language ruleset (null dereference, thread safety, XSS, SQL injection), JSON output, session resume and replay, CI integrations for GitHub Actions, GitLab CI and Gerrit, and OpenTelemetry traces. Model choice is yours through OpenAI- or Anthropic-compatible endpoints. A delegation mode inverts the arrangement: your own coding agent performs the review while the tool supplies only its file-selection and rule-resolution logic, with plugins for several popular agents. Apache-2.0, and by the project's account a two-year internal deployment before release. Its published benchmark, self-run on a purpose-built evaluation set, claims higher precision and F1 than a general-purpose coding agent on the same model at roughly a ninth of the tokens, with lower recall as an explicit trade against noise.

## Best used when

Review has to happen where no interactive agent session exists. A CI pipeline gate, a merge-request hook, or a nightly sweep across repositories needs a reviewer that runs headless, exits with a status, and emits machine-readable output; a skill invoked inside a coding session cannot fill that slot. This is the clearest case for the tool and the one its CI integrations and JSON output are built for.

Teams standardising review across mixed toolchains. When different developers use different coding assistants, a reviewer that lives outside all of them gives one ruleset and one output format regardless of what anyone has installed locally, and the delegation plugins let holdouts keep their own agent while still following the shared file-selection and rule logic.

Large or sprawling changesets where coverage is the actual risk. The bundling and sub-agent fan-out exist specifically for diffs big enough that a single-context agent starts cutting corners, and the token accounting matters at that size in a way it does not on a twenty-line change.

Auditing unfamiliar code with no diff to anchor on. `ocr scan` covers inherited repositories, vendor drops, and directories nobody has read in years, which most diff-oriented review tooling simply cannot address.

## Poor fit when

Review already happens conversationally inside a coding session. Many Claude Code and similar workflows already run diff and PR review through natural-language skills or slash commands that triage by change type and size, apply checklists, prioritise security on sensitive paths, and run the project's own linters. Those already have the diff, the surrounding code, the session history, and the requirements discussion in context. Bolting on a separate CLI duplicates the function through a second mechanism, with its own configuration surface, its own model credentials, and its own billing line, to reach roughly the same place. The token-efficiency argument also weakens here: a review you were going to run inside a session you are already paying for is not obviously cheaper when moved to a separately metered API call.

Solo work on small, frequent diffs. The deterministic machinery earns its keep by preventing skipped files and drifted line numbers, problems that barely exist on a fifty-line change a single person already understands. The setup cost lands immediately; the payoff arrives only at scale.

Review depends on requirements the tool cannot see. Whether a change actually does what a ticket asked, whether it matches a decision made in conversation last week, whether an intentional deviation was agreed: a CLI reading a diff and a ruleset has none of that, and its precision-over-recall tuning means it will not flag what it cannot evaluate. It checks defect classes, not intent.

The benchmark is load-bearing in your decision. The comparison, the evaluation set, and the annotation process all come from the project itself, and "precision at a ninth of the tokens" is measured against whatever prompt they gave the comparison agent. That is not disqualifying, but it is not independent evidence either, and a tuned workflow of your own is not the same baseline they tested.

## Verdict

Catalog. This is a serious, production-hardened tool, and its central architectural claim is the interesting part: the steps where failure is silent, such as file selection, rule matching, and comment positioning, should be deterministic code rather than instructions to a model, leaving the LLM only the judgment call in between. That idea is worth internalising whether or not you install anything, and it applies to any workflow that currently asks a model to both pick its own scope and self-report where its findings live. The tool itself, though, targets a context most individual Claude Code setups are not in: a CI gate or shared pipeline that reviews code with no agent session attached, standardised across a team on mixed toolchains. If review already runs interactively through skills that know the requirements and the project's own conventions, adding this means maintaining a second review system, separately configured and separately billed, to cover ground the first one already covers with more context. Worth knowing about, and worth reaching for the moment review needs to happen headless or across a team; the delegation mode is the cheapest way to try the file-selection and rule-resolution logic without taking on a second model bill.
