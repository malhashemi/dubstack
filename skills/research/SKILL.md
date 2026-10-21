---
name: research
description: Find out how things are, in the code, other repositories, documentation, or a running system, with the investigation scaled to the questions and every finding sourced and dated. Only use when the user invokes this skill by name or an earlier stage's handoff names it.
---

# Research

Find out what the decisions ahead need to know about how things are, and leave a written account that later stages can build on. Research informs; it does not decide. It describes the code, the documentation, and the systems as they are, and leaves what to build to the stages after it.

Research is dated evidence, not a ruling. Each finding says where it came from and when, so whoever uses it can judge how far to trust it: reuse what cannot have changed, such as a library's docs at the pinned version, and look again at what may have, such as a file edited since, when something important rests on it. Where a finding and its source disagree, the source is right.

## Inputs

Sync the project's local copy using its `AGENTS.md` commands before reading existing artifacts or starting the research.

With a goal, the handoff gives the path of its record. Read the record: the goal, its scope, its context, and its Open list. The decisions still ahead of the goal, including which route it takes next, decide what is worth finding out. Work in `research/` in the goal's directory.

Without a goal, use the user's question as the input. Work in `research/<slug>/` at the root of the local copy, choosing a short slug that names the question.

## Plan the questions

Look at the terrain enough to ask well: where the relevant code lives, which libraries and services are involved, and what the goal's context points to. Read `glossary/glossary.json` in the local copy and use its current terms. When working within a goal, include its proposed terms, which take precedence over current entries with the same `id`.

Write the plan in `plan.md`:

- **Questions** about how things are: what exists and where, how it works end to end, how the parts connect, what a library or service actually does, and how each area is tested. A good question says where to look, such as "in `packages/billing`, how does …", and never what to build, so the answer describes the system rather than arguing for a design.
- **Pointers**: the links, repositories, packages, and paths the goal or the user named, verbatim.
- **The decision each question serves.** A question that serves no decision ahead is not worth its cost.
- **Who investigates what.**

When the goal could change what users see, include the product's design language among the questions (its components, tokens, and theming), since the design stages draw their mockups in it.

## Investigate

How to investigate is yours to choose, following your standing guidance on models and delegation. Match the effort to the questions: a handful in one area can go to a single investigator, several independent areas to one investigator each in parallel, and when you do not know where to look, or the codebase is large, a quick pass that locates the relevant areas first lets you plan from a map rather than a guess.

Start each investigator in a fresh context with `references/investigator-brief.md`, its questions and pointers, and the path of its report in `reports/`, and nothing of the goal or the plan, so what it finds is not steered by what the goal hopes to be true.

Where the facts live changes the tools, not the approach: read the code, read official documentation and source at the version the project pins, and observe a running system without changing it. When only a person knows the answer, draft a short questionnaire for the user to pass on and leave the question open.

## Write the account

Read the reports and write `research.md` from `references/research-document.md`. Tell it as an account of how things work, organized by what its reader needs rather than by question, with each finding one step from the report it came from. Check it against the plan and the reports: every question is answered with its sources or listed as open with what could answer it, and every claim traces to a report or a source. Give the open questions one follow-up round of investigation; what remains after that stays open.

<important if="the goal already has research">
Add to it rather than starting over: extend the plan, add reports, and revise `research.md` in place, folding in any findings later stages appended, so it still reads as one account. A finding the new investigation changed is rewritten with its new date, not left beside the old one.
</important>

When the account spans several areas, or its structure is easier to see than to read, have a subagent render `research.html` beside `research.md`. Give it `references/page-brief.md` and choose its model using your guidance for visual design work. The renderer publishes the local copy and returns the page's link and coverage report. Check that every finding, report, and open question appears and every link opens. Resolve reported merge conflicts using the `AGENTS.md` instructions, then have the renderer refresh and publish the resolved version.

Publish the final research using the project's `AGENTS.md` commands, whether or not it has an HTML page.

## Completion

The research is complete when:

- Every question in the plan is answered in `research.md` with its sources, or listed as open with what could answer it, after one follow-up round.
- Every finding says where it came from and when.
- The plan and the reports are on disk beside the account.
- When the research has a page, it shows the current account and its coverage matches.
- The account, plan, reports, and any page are published with the local copy. If Dossier cannot be reached, keep them locally and report them as unpublished.

A stack of reports is not research until the account connects them, and an answer without its source is not a finding.

Summarize what the research established, which questions remain open, and what only a person can answer. For work within a goal, identify which of its facts to find are now answered. Give the account's local path and the page's link when published. State which artifacts remain unpublished.
