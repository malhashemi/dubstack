---
name: implement-outline
description: Implement an approved structure outline end to end in one continuous run, verified and reviewed, and stop before the pull request. Only use when the user invokes this skill by name or an earlier stage's handoff names it.
---

# Implement Outline

Deliver the approved outline's outcomes in one continuous run and hand back a branch that is verified, reviewed, and ready for a pull request. Preserve its scope, exact contracts, and required dependencies; choose the execution order and division of work within those bounds. Phases organise acceptance and progress, while work within and across them can overlap where dependencies allow. Carry the work through without pausing for routine confirmation, so the user comes back to finished work rather than a run waiting on them.

## Inputs and authority

The handoff gives the outline's absolute path. Sync the project's local copy using its `AGENTS.md` commands, then read the outline, every input listed under `design` in its front matter, and the repository's instructions in full.

Read `glossary/glossary.json` in the local copy. Use the current terms and this goal's proposals; a proposal takes precedence over the current entry with the same `id`. Leave repository glossary files unchanged. When the goal completes, basecamp makes its terms current.

Implement an outline whose status is approved, or implementing when you resume one. An implemented outline comes back when the user brings unfinished work against its approved requirements, such as a failed owner check; fix it against the plan as it stands. A draft goes back to the user for approval, and a change to the agreed scope is new work rather than part of this run.

The approved outline is the most recent plan. Where documents conflict, the outline governs, then the TDD, the PRD, the design discussion, the research, and the goal record. The code may have moved since the outline was written, so reconcile the two before building on the plan. Finding facts is your job. When the plan and the code disagree, sort the mismatch:

- **Consequential:** it changes observable behaviour, scope, a public or cross-component contract, data compatibility, security or privacy, or what the owner must pay for or provide. The user decides it.
- **Local:** everything within those bounds. Decide it and report it with the phase.

Keep design IDs, such as behaviour and constraint IDs, and links to the outline or the design out of code, tests, and comments: those documents are archived once the feature ships. Name behaviour in the glossary's domain words.

## Doing the work

How you carry out the plan is yours to decide, following your standing guidance on models, delegation, and review. This skill is your opt-in to the multi-agent tools your harness provides, such as subagents, delegated tasks, and workflows.

Before building, read the outline's dependencies as the run's dependency graph and decide from it what can proceed at once. The user is away while you work, so the time to a finished branch matters: run independent work concurrently, and keep work serial only where a dependency or a shared file requires it. A long run keeps its judgement when building is delegated and your own context stays on integration, verification, and the plan as a whole.

Choose verification from the changed behaviour, affected callers, and the risks of building further on it. Run focused checks when their seams are usable. Run Plan Verification and the repository's required full checks on the final integrated state; bring a broad check forward when an explicit checkpoint or the risk calls for it. Reuse results while the code, requirements, and environment they depend on still hold, and recheck what later changes could invalidate. Verify with your own tools: commands, the browser, computer use, a CLI, or an API.

The outcomes in the outline's Delivers, phase Verification, and Plan Verification are the acceptance contract. Check methods may adapt without weakening coverage or bypassing a required gate. Turn the contract into acceptance tests before the code that satisfies them: the outline's contracts give their exact shapes, so the tests can be written, and seen to fail, before any body exists. Tests written by whoever builds the code tend to confirm what was built rather than what was required, so acceptance tests are worth writing apart from the build. Exercise the real components the behaviour depends on; a mock of the behaviour under examination, a skip, a setup failure, or a fake success response proves nothing. Implementation tests evolve with the code, but weakening what an acceptance test or Verification item proves is a consequential change.

Record a demo of every change users can see or do, while you verify it, so the pull request can show the change rather than describe it. Choose whatever makes the change quickest to review: before and after screenshots when it shows in one state, a short video when it lies in behaviour over time, such as a flow or an interaction, and a terminal transcript or a request and its response for a command-line or API change. Capture the before view before the phase changes it.

Save finished demos in `demos/` beside the outline, named for what they show. Use formats GitHub displays: PNG, JPEG, GIF, or WebP images; MP4, MOV, or WebM video; and text transcripts. Keep each file under Dossier's 50 MiB limit, compressing videos as needed. Record and compress in the goal's `private/` folder, then move finished files into `demos/` so progress reports publish only complete demos. `describe-pr` attaches them to the pull request. A change with nothing user-facing needs no demo.

Make every check yourself where your tools allow. A check becomes an owner check only when only a person can make it, or when a real attempt with your tools failed; report it with the reason, and never count it as passed.

Check Owner Setup at the start. Name any missing item to the user straight away, and begin with the phases that do not need it.

Integrate each phase as one unbroken commit range on the branch so the progress reporter can read what it landed. Work may be built in parallel and integrated in dependency order; the range is a reporting boundary, not a requirement to do the work serially. Acceptance tests land in the range of the phase whose outcomes they check. A fix to a phase already reported, such as one for a failed owner check, is its own range, attributed to the phase or phases that deliver the requirement that failed. Leave unrelated local changes alone.

Weigh review findings and failed checks on their merits against the outline and the code: a finding may need a fix, a supported rejection, or the user's decision. Keep repair bounded and change strategy when an attempt makes no progress. Re-review what a repair changed, widening only on evidence of a regression or a missed requirement; optional cleanup is not part of completion. When verification exposes a defect in an earlier phase, fix it and include the fix in verification and review.

## When to ask the user

Keep working on whatever does not depend on an open consequential mismatch, a missing Owner Setup item, or a blocker you cannot clear, such as an environment you cannot repair or attempts that make no progress. When nothing independent remains, stop and put every open question to the user in one message, each with your recommendation.

## Recording progress

As each phase is integrated, in whatever order phases finish, launch a background subagent with the absolute path of `references/progress-report.md`, the progress reporter's brief. Give it the outline's path, the phase number, the phase's commit range, and your account of the phase: the checks you ran, with their results and where the evidence is, the demos you recorded and what each shows, the local decisions you made, and anything you raised. Include evidence you gathered for an earlier phase's checks. After a fix to a reported phase, launch the same reporter with the fix's range, the phase or phases it fixes, the requirement that failed, and fresh evidence for the checks the fix touched.

Keep evidence and demos beside the outline, uncommitted and available to the reporter and `describe-pr`. These files publish with the tree. Store evidence that must stay on the machine in the goal's `private/` folder.

The reporter is the only writer of the outline's progress and its view. Run one report at a time, starting the next after the previous one finishes. Each report publishes the local copy so the team can follow progress. Treat consequential differences it identifies as you would your own findings, and handle reported merge conflicts using the project's `AGENTS.md` instructions.

After final verification and review, launch the same reporter with the final commit, the whole-plan check results, the review outcome, and any outstanding owner checks. It records Plan Verification and refreshes the view even when no new phase landed.

<important if="the user's decision changes the approved plan">
Revise the outline while no report is running: edit the phases the decision reaches, and add a line to its Revisions with the date, what changed, and why. Every existing phase keeps its number. A new phase takes a number never used in this outline, such as `2a`, so a removed phase's number is never reused; place its section in the recommended order and update dependencies the decision changes. Progress already recorded stays, since it describes work done against the earlier plan. The next report shows the revision in the view.
</important>

<important if="you are resuming a partially implemented outline">
Establish where the work stands from the outline's Progress blocks and the branch history, and reconcile both with the files. A committed phase without a Progress entry lost its report; launch that report again. Use the verification guidance above to decide which recorded results still apply.
</important>

<important if="you create worktrees or branches during implementation">
Keep the goal's original worktree and branch as the integration point and the PR branch, and bring side work back to it. Before the handoff, remove the worktrees and branches you created once their work is integrated, keeping uncommitted work and leaving other tasks' worktrees alone.
</important>

## Completion

The implementation is complete when all of these hold:

- Every phase has landed on the branch, and each phase Verification and Plan Verification item has passed with supporting results or is an owner check after a real attempt, with the reason.
- The repository's full checks pass on the final state, and journeys that cross phases work end to end.
- The final state has had the independent review your standing guidance calls for, and every finding is fixed, rejected with support, or decided by the user.
- The last report has finished: the outline is marked implemented and its view shows the final state.
- The worktrees and branches you created are cleaned up.

A green suite, every phase committed, or a finished report marks progress, not completion.

## Handoff

Close with the owner checks and open decisions that need the user's attention, followed by what landed and the verification and review results. Give the outline's path and the view's link, or report that the view is unpublished if Dossier could not be reached. Identify the branch, its worktree, and the outline as the inputs for the pull request stage in a fresh session. Leave the pull request to that session.
