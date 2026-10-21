---
name: design-interview
description: Settle a PRD, TDD, combined design discussion, system architecture, or project glossary with the user, gather a customer's requirements, or brainstorm a problem or opportunity, through an interactive page revised in rounds. Only use when the user invokes this skill by name or an earlier stage's handoff names it.
---

# Design Interview

Reach a shared understanding with the user by interviewing them relentlessly, and leave behind what the target establishes: a design they can build from, a customer's requirements in their own terms, or a map of possibilities. One interactive HTML page does both jobs: it shows the understanding so far and the questions still open. As answers land, revise it into one coherent account of the work.

Bring judgment to the interview: discover implications, develop alternatives, recommend an approach, and make difficult choices concrete. The user supplies intent and decides the tradeoffs. The target says which of these its questions call for: a design decision takes alternatives and a recommendation, a discovery question asks for what only the user knows, and a brainstorming prompt opens possibilities without settling them. This skill supplies continuity and coverage; the exploration, explanation, and visual composition belong to the agents doing the work.

The user is the person interviewed: usually the owner, and for requirements gathering a customer interviewed on the owner's behalf, as that target describes.

Upstream documents, such as a goal, research, or a product specification, may arrive with much already settled. Later work consumes what the interview leaves behind. Its profile defines what it can decide and whether it belongs to a goal or precedes one.

## Choose the target

A **target profile** defines what the interview is for, its inputs, its phases and review gates, how options are compared, the coverage it must reach, when it is done, and what it hands off. Use the profile the user or the upstream route names; when neither names one, recommend one and confirm it with the user. Read the profile before planning the interview:

- [Product Requirements Document](references/prd-target.md): what changes for users and why, with technical design to follow.
- [Technical Design Document](references/tdd-target.md): how to deliver established product requirements.
- [Design Discussion](references/design-discussion-target.md): what, why, and how together, for one piece of work whose product and technical decisions are entangled.
- [Solution Architecture](references/architecture-target.md): what drives a whole system's design, how it is structured, what it is built with, and where it runs.
- [Glossary](references/glossary-target.md): the project's vocabulary, drawn from business sources and settled independently of a goal.
- [Requirements gathering](references/requirements-target.md): a customer's business and needs, in a form they recognise, correct, and approve.
- [Brainstorming](references/brainstorming-target.md): a problem or opportunity explored, with promising ideas made concrete and directions found; it may stay open.

To interview for a different artifact, write another profile with the same parts. The profile governs the kinds of questions, the role of recommendations, how far the interview converges, and what completes it; the rest of this file applies to every profile except where the profile says otherwise.

Requirements gathering and brainstorming also run in `conversational-interview`, as a continuous conversation by voice or chat; an interview can move between the two, as described under Changing how the interview runs.

## Two artifacts, two readers

Keep both artifacts in a directory named for the profile, such as `prd-interview/`, inside the goal's directory unless the profile or the user names another location. Without a goal, use the root of the project's local copy: `architecture/` for Solution Architecture, which describes the whole project, `requirements/<slug>/` for requirements gathering, which sits above goals, and `<slug>-interview/` for other profiles.

- **The ledger**, `ledger.md`, is the artifact for agents, and you own it. It holds every settled entry with its source and rationale, every open question, the glossary, what was ruled out, and the questions deferred to later stages, all under stable IDs. It is a set of lists, never a document. Read [ledger format](references/ledger-format.md) before creating or updating it.
- **The page**, `index.html` unless the profile places it elsewhere, is the artifact for the user. A delegated builder following `visualize-html` owns it, and every change to the page goes through the builder.

Use the project's `AGENTS.md` entry to sync the local copy before work and publish it with the tree. Keep material excluded from team sharing by the ledger's confidentiality line in the interview's `private/` folder, outside the published ledger and page.

When the project has no Dossier entry or its local copy needs recovering, read [Dossier setup](references/dossier-setup.md) before publishing. This skill can start the tree; `project-home` adopts it later and builds the home.

## Settle what is known before asking anything

Read the upstream documents and the repository they point to, including any glossary it keeps. Sort what you find:

- **Settled:** decided by an upstream document, by the codebase as it stands, or by an earlier round. Shown as the current design and never asked again.
- **Frontier:** open, with its prerequisites met. Asked this round.
- **Not yet on the frontier:** open, and waiting on a frontier answer, held for a more focused round, or both. Shown hanging off the decisions it depends on, with the reason for any hold, so the shape of the design tree is visible.

A profile may hold prior context to a different standard: in requirements gathering, what others say about the customer's business is our understanding, shown for the customer to confirm, not settled. Nobody should repeat what they already gave just because the interview has not asked it yet.

Keep what is decided apart from what is implemented: a decided stack over an empty scaffold is a design, not a product. Where an upstream document and the code disagree, the document may settle intent, but the code settles current behaviour; show the discrepancy and resolve the intended change with the user.

Every settled entry and every glossary term on the page is open to the user's comment, in every round: they can correct it, question it, or ask to reopen it, and their comments arrive in the same handoff as their answers. In the first round this is how they correct what you treated as settled; in later rounds it is how they check how you understood their answers. A settled item the user reopens becomes a frontier question.

## Work the design tree in rounds

The **frontier** holds the questions you can ask now: their prerequisites are settled and no gate or hold keeps them back. Answers can open further questions. Number each round's questions and frame them as the profile requires: alternatives and recommendations for design decisions, context for discovery, or prompts that open possibilities. Wait for the user's answers before the next round.

**Size rounds for an asynchronous user.** The user answers on the page and may be away for hours, so every round costs them a return trip. By default, ask the whole frontier at once. Hold a ready question back only when a focused round would give a hard choice the attention it needs, or the profile's pacing rules call for it. Record under Not yet why it waits.

**Keep questions in scope.** Every question stays inside the scope the profile defines. A question whose answer would not change the artifact does not belong on the frontier. The profile's phases and gates decide which decisions may enter the frontier now; a decision from a later phase waits even when its prerequisites are settled.

**Facts are your job; decisions and first-hand knowledge are the user's.** Look up anything the inputs, the repository, or other sources can answer rather than asking the user; ask only for intent, for decisions, and for what only the user knows, such as how their own work happens. When a question needs a fact, find it or dispatch a subagent to find it, without blocking: only the questions that depend on that fact wait, and the rest of the frontier goes out now. A fact found this way becomes a settled entry marked with the round it was found in, as the ledger format describes.

**Develop alternatives with a point of view** for every question that is a decision between alternatives. Offer options that differ in what they make true, including a different framing when it could improve the result. For each option, say what becomes true if it is chosen, what it costs or risks, and what it genuinely rules out: the user judges the consequence, and the label only names it. Recommend one when the context supports it, name the criterion that decides it, and give its strength. Read [comparing options](references/comparing-options.md) before writing the first option question: it supplies the criteria, how to produce interface options that genuinely differ, and how to show each kind of question.

**Use the freedom you are given.** Work out detail that follows from agreed decisions without asking; a choice that would change the artifact goes to the user. When the user explicitly hands you a decision or a class of decisions, make them and record the delegation as their source. A strong recommendation, an untouched control, or a plausible inference is not the user's agreement. Profiles that develop the shared glossary use the term-confirmation rule below.

## Keep the language sharp

For profiles that develop the shared glossary, the ledger's Language list is the project glossary in progress. Build it as you go:

- When a term arrives fuzzy or overloaded, or the work needs a term the project lacks, propose one canonical term with the words to avoid and record it in the Language list at once. The page shows it as new, open to comment; a new term the user leaves without a comment is agreed, and a comment makes it a fix or a question.
- When the user, a document, or the code uses a term in conflict with the glossary, say so and ask whether the concept is changing or only its name.
- When a relationship between terms is being decided, invent a concrete scenario that probes the edge and put it in the question.
- When the user states how something works, check the code. If it disagrees, say so and ask which is right.

Read [glossary guidance](references/glossary.md) before seeding the Language list from the project's glossary and before writing the glossary changes at handoff; it says what belongs and the file's shape.

## Write the ledger before the brief

The page can only be as good as what the ledger gives the builder. The builder owns composition, visual reasoning, wording, and interaction. You own scope, decision status, and the substance of every tradeoff, so the builder never has to work out content.

- **Pre-digested facts.** Every settled entry the page renders, with its phase, group, source, and rationale, phrased so it can be paraphrased, with any confidentiality limit its source imposes. Attached artifacts and backticked identifiers are exact. Never point the builder at a specification to work out what is settled.
- **Consequences, not labels.** For each option, what becomes true if it is chosen, what it costs or risks, and what it genuinely rules out. Where the question calls for a recommendation, include its strength and reason or what it waits on.
- **A visual idea per question.** Suggest what to draw so the user can compare alternatives, see a gap in what is known, or explore an idea. The builder may find something better; a decision question with no visual idea tends to come back as a list of labels.
- **Stable IDs.** Every entry in every list, including the lists the profile declares, carries an ID that later rounds and the handoff reuse.

## Build the page through a delegated builder

Compose the brief from [artifact brief](references/artifact-brief.md): fill its placeholders from the ledger and the profile's Page section, including its feedback rules, and resolve any bundled reference links to full paths for the builder. Hand the rest over as written, with the full ledger. The brief is the page contract, the ledger is the content, and `visualize-html` owns presentation. Put direction specific to this round in the brief's round notes rather than rewriting its sections.

Choose the builder's model by following the guidance you have been given for visual design work. Run it in the foreground, with a tool budget large enough to verify the page in a real browser.

The builder reports a coverage map, the region layout, the answers form's target and `id`, and the page link. Record the layout and form details in the ledger. Account for every ledger ID: where it appears, where its resolution appears, or the profile, confidentiality, or lifecycle rule that excludes it. Check that every required entry, term, and frontier question is present, with the context, options, and controls its kind needs. Nothing in the page's current account may contradict the ledger or remain after the ledger no longer holds it. Keep the coverage report agent-facing so exclusions reveal no private content on the page. Then read the questions as the user will; send back missing context, missing consequences for decision questions, or misleading comparisons. Share the page link after checking its coverage.

## Fold answers in, then revise the page

The page is the main loop: the user answers there and returns its copyable handoff block. Answers or corrections given in conversation count too; fold them into the same ledger. When the user asks you to read responses from the page, use `dossier read` on its answers and comments. Preserve who supplied each response: other people's input informs the user's choices without settling them. When answers arrive:

- Verify any factual claim an answer rests on before accepting it; read the files it mentions.
- A note is input, not a decision. Decide whether it is a decision, a fact to look up, or a reopened question, and handle it as that.
- A comment on a settled entry or a term is input in the same way. Make the fix it asks for, check the fact it raises, or move the entry back to the frontier as a question, and say in the delta which you did.
- When a note says someone else holds the answer, draft a short questionnaire for that person: who they are, what we need back, and the questions, most important first. Hand it to the user with the revised page, keep the question on the frontier, and move the rest of the frontier on.
- A question the user left untouched stays on the frontier; its recommendation is not a decision.
- Move each resolved question off the frontier and record what it settled as settled entries, or in the lists the profile declares, with rationale and any alternatives it beat. Rewrite every settled entry the decision changes, and retire what it makes false. Record an idea it leaves out under Out of scope, and a question for a later stage under Deferred questions.
- When a decision changes what an open question or one of its options means, supersede it as the ledger format describes rather than editing it in place, so a saved answer never lands on a choice the user did not make.
- When a look or behaviour question resolves, give the settled entry a file artifact for the chosen mockup or state demo; the revision saves the drawing there.
- Promote to the next frontier the topics an answer opens and the held topics whose round has come. Frame each as its question kind requires, with a visual idea. Demote nothing silently.
- Rewrite the delta so it lists exactly what changed since the previous round. It is not a running log.

Then delegate the revision with the brief's revision section. The handed-back block ends the round, and no comment outlives it: resolve every open comment thread with `dossier comment --resolve`, using their paths from `dossier read --json` on the page's `index.comments/`, so the revised page starts without open comments.

A round is complete when the answers are folded into the ledger, the page is revised, and its coverage map matches the ledger. Answers received but not yet folded in are progress, not completion.

<important if="revising an existing interview page">
Give the builder the full current ledger, the delta, the existing page, and the previous region layout. The persistence contract must survive: the same answers form target and `id`, and every question ID and option letter unchanged while its meaning holds, so earlier answers stay attached to the choices they made. A question or option superseded because its meaning changed passes any saved answer to its replacement as needing a new answer, never matched to something else; resolved and dropped questions leave the page. Everything else about the page may change. The result reads as one design with no trace of which round decided what; an option that lost appears only where the profile's page rules place it.
</important>

## Changing how the interview runs

A requirements or brainstorming interview can move to `conversational-interview` whenever that serves the people in it, such as a customer who would rather talk a round through, and can come back. The interview keeps its folder and its ledger; only the interaction changes.

Before handing over, fold every received answer and comment into the ledger and resolve every open comment thread to close the round. Hand over the folder's path, the profile, the latest folded round, the existing page and its feedback locations, and what is outstanding: the frontier, held topics, and anything awaiting confirmation. Keep the page path, form target and `id`, saved fields, and item identities across the switch. `conversational-interview` keeps the profile's lists and adds its session entries; a change of medium does not invalidate confirmations.

<important if="the interview continues from conversational-interview's sessions">
Read the ledger and the notes and live logs of sessions not yet reconciled. Reconcile their transcripts or messages before building a round: account for every contribution and correction in the profile's lists, preserving the speaker, source, original words, authority, and what was confirmed. Check the transcripts for anything the logs missed; record open threads and supersede changed claims as the profile requires. Leave session records in place. Collect any pending page feedback too, applying the profile's evidence rules. Build the first round from what remains outstanding, retaining earlier confirmations for unchanged content.
</important>

## Completion

The profile defines completion. An empty frontier is necessary, unless the profile lets the interview end with questions open, but never sufficient: it can also mean questions were never asked. Check the profile's coverage list against the ledger, obtain the confirmations the profile names, and make sure every received answer is folded in and the page agrees with the ledger.

Then hand off:

- Freeze the ledger where it is, with its artifact files beside it, and name it to the user as the input for the stage the profile names.
- Write the glossary changes into the project's `glossary/glossary.json`, following [glossary guidance](references/glossary.md), unless the profile leaves the glossary unchanged. Later stages read them there.
- Append every entry marked `found` to the research artifact named in the ledger's `inputs`, under one heading for findings made during design, each with its source. When the inputs name no research artifact, the frozen ledger alone carries them.
- Publish the local copy, then report where everything is, with links to the published pages, and any check you could not run. If Dossier cannot be reached, finish with the local files and report that they are unpublished.
