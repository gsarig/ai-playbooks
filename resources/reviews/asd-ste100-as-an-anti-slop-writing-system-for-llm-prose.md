---
title: "ASD-STE100 as an anti-slop writing system for LLM prose"
url: https://github.com/woosal1337/blog/tree/main/videos/ep01-the-cure-for-ai-slop
author: "woosal1337"
date_evaluated: 2026-07-30
verdict: adapt
tags: [writing, prose-quality, agent-skills, linting, documentation, evaluation-methodology]
---

## What it proposes

Take ASD-STE100, the controlled-English standard written for aircraft maintenance manuals, distil it into an agent skill, and use it as the system that stops LLM prose from reading like LLM prose. The kit has three parts.

The skill file is a one-page rule set in five groups: words (one name per thing, short common word over Latinate synonym, no marketing adjectives), verbs (active voice, verb instead of nominalization, no stacked auxiliaries), sentences (one instruction each, 20-word cap for instructions and 25 for description, no contractions, keep articles), punctuation (no semicolons), and structure (one topic per paragraph, six sentences max, numbered lists for steps, condition before command). It ships two modes: strict, for procedures, runbooks, and error messages, where every rule and both caps apply; and STE-flavored, for READMEs and PR text, which keeps the sentence and voice discipline but drops the roughly 900-word dictionary lockdown so the text still reads. It closes with a six-item self-lint the model runs on its own output before returning it.

The linter is about 90 lines of dependency-free Python. It strips code fences, splits sentences, and counts regex-matched violations in eleven categories: long sentence, semicolon, contraction, passive voice, "-ing" main verb, nominalization, phrasal verb, banned word (roughly 45 entries), marketing adjective (roughly 28), modal hedge, long paragraph. The score is violations per 100 words. The author is explicit that the delta between two scores, not the absolute number, is the signal, and that this is not a certified STE checker; the judgment half of the standard needs a human.

The experiment is the argument for the skill over the alternatives. Six engineer-writing tasks (README, PR description, API docs, error message, getting-started, deprecation notice) crossed with four conditions (plain baseline, a banned-words list, Orwell's six rules, the STE skill), run on two models. Headline: STE cut the linter score 74% on one model and 50% on the other; Orwell landed in the same low band; the banned-words list was the least reliable, cutting 3% on one model and 40% on the other.

## Best used when

The output is documentation, procedure, or interface text where clarity is the whole point and voice is a liability: READMEs, runbooks, error messages, release notes, deprecation notices, API reference, PR descriptions. STE was designed for readers who must not misparse a sentence, and that constraint maps cleanly onto text a person reads while something is broken. The before/after sample shows the mechanism plainly: a 191-word README paragraph built from stacked clauses and "seamless/robust" filler becomes 169 words of short declaratives that say the same thing and are easier to check for truth.

It also fits as a machine-checked layer under rules that already exist informally. The linter is deterministic and has no dependencies, so it drops into a pre-commit hook, a CI step on docs directories, or an ad-hoc pass over a folder of markdown. For anyone already enforcing one or two slop markers at write time, this is the same idea generalised to eleven, with the difference that it scores rather than blocks, which suits categories like passive voice where a hard block would be wrong.

Least obviously, the experiment design is reusable independently of STE. Six tasks, four prompt conditions, one scoring script, two models is a cheap template for answering "does this instruction file actually change the output?" about any writing rule. Most style rules in agent configs have never been tested at all.

## Poor fit when

The text needs a voice. The skill says so in its own first paragraph, and it is the sharpest limit: STE strips voice deliberately, because in an aircraft manual voice is noise. Fiction, essays, blog posts, and any reader-facing copy with a personality are the opposite case. No contractions makes conversational prose stilted; the 20-word cap flattens rhythm, and varied sentence length is one of the few reliable signals of a human writer; one topic per paragraph forbids the long paragraph that builds an argument. Running this over voice-driven artifacts produces lower scores and worse writing, and the score cannot show it. Where a dedicated voice definition already governs the prose, that definition wins.

The evidence needs the same caution. The linter scoring the experiment is the same rule set the STE condition was instructed to follow, which is close to grading an exam against its own answer key. The number that survives the objection is Orwell's, which was not told the rules and still landed in the same band; that points at "any coherent writing system helps" more than at "STE specifically". n is six tasks on two models, scored by regex with no parser, so passive-voice and nominalization counts carry known false positives, and per-100-words is unstable on short outputs where one violation in a 17-word notice reads as 8 to 12. On one of six tasks STE scored worse than baseline because of the linter's own paragraph heuristic penalising short sentences. The author states all of this himself, which is why the kit is worth reading; it does not make the numbers stronger.

One asymmetry inverts the usual priority: em-dash count is reported but excluded from the score, and the em-dash is the marker most readers actually use to spot machine prose. The baseline README sample had four, the STE version zero. A project that cares mainly about that marker gets more from a three-line write-time guard than from adopting the full standard.

Finally, the fix is model-specific. One model's default output was flashy, with em-dashes, marketing adjectives, and run-ons; the other produced zero em-dashes, zero semicolons, and zero marketing adjectives by default, and slopped subtly instead through long sentences, passive voice, and empty closers. Banned-word lists were near-useless on the first and cut 40% on the second, so "banning words does nothing" is a claim about a model, not about writing. A rule set tuned against a different model's failure mode spends rules on problems you do not have.

## Verdict

Adapt. The core claim is sound and the honest reading of the data supports it: giving a model a coherent writing system, with structure and a self-check, beats giving it a list of forbidden words, and that holds across models even though the margin does not. The right adoption is scoped. Take the skill for procedure and documentation text, where the 20-word cap and the no-voice premise are features, and keep it away from anything with a voice, where a dedicated voice definition should govern instead. Take the linter as a scoring tool rather than a gate: deterministic, dependency-free, useful as a delta, but regex all the way down, and silent on the marker most people care about. The most transferable piece may be neither. The six-tasks-by-four-conditions design is a cheap template for testing whether any standing style rule changes model output at all, and most such rules have never been checked. Treat the headline percentages as directional and the method as the deliverable.
