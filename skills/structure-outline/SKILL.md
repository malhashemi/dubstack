---
name: structure-outline
description: Turn an approved design, or a researched goal with nothing left for the user to decide, into a phased structure outline of outcomes, contracts, dependencies, and checks that an implementing agent delivers and records its progress in, with a visual view for review. Only use when the user invokes this skill by name or an earlier stage's handoff names it.
---

# Structure Outline

Turn the approved design for one piece of work into an implementation outline: the outcomes to deliver, exact contracts to preserve, dependencies to respect, and checks that establish completion. Group the work into phases, each landing one shippable result, and recommend an order with reasons. Give an agent that never saw the design conversation enough context to choose how to carry out the work from the outline and the design.

Once the user approves it, the outline is the most recent plan: where it differs from the design, the outline governs, and it records the difference. During implementation the same document becomes the progress record, with the approved plan and the progress kept apart. Read `references/outline-template.md` before drafting; it holds the document's shape and says which parts are plan and which are progress.

## Inputs and authority

Before reading the goal's artifacts, sync the project's local copy using its `AGENTS.md` commands. Read in full the frozen design ledger (a design discussion's, or a TDD's with the PRD ledger behind it), the approved mockups and state demos beside it, the goal record, the research, and the code the design touches. The research-questions document stays out. Take up the design's deferred questions for the outline first. A phase that builds a surface the design approved as a mockup or state demo names that file as the target it must match.

Read `glossary/glossary.json` in the local copy. Use the current terms and this goal's proposals; a proposal takes precedence over the current entry with the same `id`.

Finding facts is your job: investigate the code and any system you can reach read-only, such as a server's logs or which settings it holds, and delegate research where that is faster. While outlining, change nothing outside the outline and its view. Changing the design is the user's decision. When the design and the code disagree, or a deferred question needs an answer, sort it:

- **Consequential:** it changes observable behaviour, scope, a public or cross-component contract, data compatibility, security or privacy, or what the owner must pay for or provide. Ask the user, with your recommendation, and keep drafting whatever does not depend on the answer.
- **Local:** everything within those bounds, such as where code lives, an internal helper, or execution order within the stated dependencies. Decide it and record it under Decisions Made While Outlining, with the design entry it touches and the reason.

Record each consequential point the user decided in the same list, so the outline shows every place it departs from the design.

Design IDs, such as behaviour and constraint IDs, belong in the outline, which is archived with the design once the feature ships. Wherever the outline names tests, code, or messages, describe behaviour in the glossary's domain words, so nothing permanent depends on an archived document.

<important if="no design stage preceded the outline">
The goal record and the research stand in for the design: the goal's statement of what done looks like and its scope take the place of the design's behaviours and constraints, and its Open items the place of the deferred questions. List what done looks like and what must hold as numbered items in Desired End State, and cite those numbers wherever the template asks for design IDs. A decision a design would have settled is consequential and goes to the user. When such decisions turn out to be more than a handful, recommend a design stage rather than outlining around them.
</important>

## What makes a good outline

- **Phases.** Each phase lands one independently shippable result: a vertical slice through every layer it needs. Recommend the riskiest or least known result first among the phases its prerequisites allow, prefactoring before the change that needs it, and a wide refactor as expand, migrate, contract. State each phase's real prerequisites and why they matter, including any ordering the user requires. A phase builds on those results, not automatically on every earlier phase. Transition code that keeps the system working during a migration, such as a compatibility adapter the contract phase removes, belongs in the plan together with the phase that removes it. Scaffolding that exists only to let a phase stand alone, such as stubs or fake data a later phase replaces, means the phases are split in the wrong place.
- **Contracts.** The outline works at the level of C header files. Every exported symbol the change adds or changes gets its full signature, in the codebase's language. Each shared type is declared once, in the phase that introduces it, and referenced by name after that; a contract the design already settled keeps its exact form. Concise applies to prose, never to signatures: the implementer builds against these exact shapes. Function bodies are the implementer's.
- **Connections.** Each phase says where its new code is called from and what it calls, in the existing code and in earlier phases.
- **Verification an agent can run.** Each check names an observable result and a runnable way to establish it, through a command, the browser, computer use, a CLI, or an API. Phase Verification covers that phase's result. Put repository-wide checks and journeys across phases once under Plan Verification. Name an earlier checkpoint only when the design, repository instructions, or a concrete risk requires it, and say why; a shippable phase does not by itself require a full-suite run. A check only a person can make goes to Owner Checks at the end, never into a phase.
- **Owner setup, only what the agent cannot do.** Owner Setup lists what a person must provide because the implementing agent cannot: a secret it has no way to obtain, a paid service or account only the owner can open, or consent only the owner can give. Before listing an item, check whether the agent can do it with the access it has, such as SSH to a server, a CLI already signed in, or an admin account, trying it read-only where you can; a document naming the owner or an operator as the one who usually does it is not a reason. Work the agent can do, even outside the repository, such as creating test accounts or changing a server's settings, goes into the phase that needs it, so approving the outline approves it. List each remaining item with the phase that needs it, where it goes, and why the agent cannot do it, so the run never stops halfway to ask.
- **Releases are the user's call.** Plan a release or deployment to a shared environment only where the design or the user places one; when the work seems to need one elsewhere, ask. Keep each phase's verification to what runs without a release, and put a check that needs a released environment in Owner Checks, after the release.

## Write, check, and present

1. Draft the outline from the template and save it beside the design artifacts in the goal's directory, or at the user's chosen location. Keep it uncommitted; it is archived with the design once the feature ships.
2. Check it against the design and the code for what is inconsistent or missing, and fix what you find. After each fix, recheck what changed and everything that refers to it, such as later phases that use a changed shared type or connect to a changed phase. The check is done when every behaviour, constraint, and deferred question is accounted for as the completion list requires, and every finding is fixed or put to the user; a pass that finds nothing new is not enough on its own. For substantial or risky work, also have an independent reviewer check it.
3. Delegate the view. Give a subagent `references/view-brief.md` and the outline's path, and pick its model by the guidance you have for visual design work. You own the substance; the renderer owns presentation and publishes the local copy. Check its coverage report: every phase, Plan Verification item, owner setup item, owner check, decision, and revision must appear. Resolve reported merge conflicts using the `AGENTS.md` instructions, then have the renderer refresh and publish the resolved version. Record the returned URL in the outline's `link` field.
4. Share the view's link and the outline's path. If Dossier could not be reached, report that the view is unpublished. Treat the user's feedback as a request to revise the outline, never to start implementing, and check factual claims against the code first. Bring other people's comments to the user for consideration. When the user asks you to read comments directly, use `dossier read` on the view's comments folder.

   The copied feedback message ends the round. After updating the outline, resolve every open thread with `dossier comment --resolve`, using the paths returned by `dossier read --json` on the view's comments folder. The revised view starts with no open comments.

   When the user approves, set `status` to `approved <YYYY-MM-DD>`. Have the updated outline and view published before handing off.

## Completion

The outline is complete when the user has approved it and all of these hold:

- Every behaviour and constraint in the design is mapped to the phase that delivers it and to a check that proves it, in phase Verification, Plan Verification, or Owner Checks when only a person can check it.
- Every deferred question for the outline is answered in the outline or decided by the user, and every mismatch found is a recorded local decision or decided by the user.
- Every phase has one shippable result, its connections, full contracts, and verification an agent can run.
- Owner Setup names only what a person must provide because the agent cannot, each with the reason and checked against the agent's access, or says there is nothing.
- The view shows the current outline.

An outline that reads well but leaves a behaviour unmapped is not complete, and a rendered view is not an approval.

## Handoff to implementation

Give the user the approved outline's absolute path and the view's link as the inputs for implementation in a fresh session.

<important if="the approved outline must change">
Change the plan only when the user asks, or when they decide a consequential mismatch. Edit the phases the change reaches, keeping phase numbers as the template describes, add a line to Revisions with the date, what changed, and why, and have the view re-rendered.

This holds until implementation starts. From then until implementation's final handoff, the implementation session owns the plan and the view and revises them between progress reports, so take the change there rather than editing the outline from here. The `status` field cannot tell you whether implementation has started: the progress reporter sets `implementing` only after the first phase, and `implemented` after the last, before final verification and review. The user's latest statement about whether the run has started settles it, unless something since shows otherwise, such as new commits or Progress entries. Without such a statement, check the branch and the Progress blocks, and when neither shows that the run has started, confirm with the user before revising.

After implementation's final handoff the plan is not revised. A defect against its approved requirements, such as a failed owner check, is unfinished work for the implementation session; a request that changes the agreed scope is new work.
</important>
