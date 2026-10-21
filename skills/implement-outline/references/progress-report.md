# Implementation progress report

Record phase or whole-plan results in the outline's progress, refresh its HTML view, and publish the local copy. The implementing agent continues working in the same checkout. Read the code, history, and supplied evidence; edit only the outline's progress and its view. Sync the local copy using the project's `AGENTS.md` commands before reading the outline.

You receive the outline's path, the phase number, the phase's commit range (`base..head`), and the implementing agent's account of the phase: which checks it ran, for this phase or an earlier one, with their results and evidence (command output, screenshots, logs), what it decided locally, and anything it raised. For a fix to a phase already recorded, the range is the fix's own, and the account names the phase or phases it fixes and the requirement that failed; record it as described under Record a fix.

## Record the phase

The outline is an approved plan with progress recorded against it. The progress is the checkbox state, `status` in the front matter, each phase's `### Progress` block, the Plan Verification `### Progress` block, and entries appended to Owner Checks; everything else is the plan, and you write only the progress.

1. Inspect `git log` and `git diff` for the commit range and compare them with the phase's plan: its result, Change Outline, Contracts, Delivers, and Verification.
2. Replace the phase's `### Progress` block:

   ```markdown
   ### Progress

   status: landed | verified | blocked · commits: <base>..<head>

   - Landed: <what the commits contain, against the plan>
   - Verified: <each check with its result and where its evidence is>
   - Demos: <each demo's file in demos/ and what it shows, or None>
   - Differs from plan: <each difference, marked local or consequential, with the reason given>
   - For later phases: <anything they need to know>
   ```

   `landed` means the commits are in and some check still lacks evidence, `verified` that every check in the phase has passed (whole-plan checks are recorded separately), and `blocked` that the phase could not land.

3. Tick a checkbox only when the evidence you were given shows it passed, or, for Owner Setup, that it was provided. Evidence for an earlier phase's check counts the same: tick it, add it to that phase's Verified line, and set that phase to `verified` once all its checks have passed. Tick a phase's line in Implementation Overview when every check in the phase has passed. A check without evidence stays unticked and is named under Verified.
4. Append to Owner Checks any check the account says only a person can make, or that the agent's tools could not complete after a real attempt, with the design IDs it proves, its phase, and the reason.
5. Set the front matter's `status` from the whole outline, whichever phase you recorded: `implemented` once every phase's Progress shows `landed` or `verified`, and `implementing` before that.
6. Update the view at the front matter's `view` path to show the new progress and any plan revision. Follow `visualize-html`, including its Dossier guidance. Preserve the design language and the visual distinction between plan and progress. Keep the layout for ordinary progress updates; when a plan revision changes the outline's structure, reorganize as far as the change needs.
7. Publish the local copy using the project's `AGENTS.md` commands, then verify the published view as `visualize-html` describes. If publishing stops on a merge conflict outside the progress and view you own, stop before verifying and report it to the implementing agent. If Dossier cannot be reached, report that the view is unpublished and identify any checks you could not run.

## Record a fix

A fix adds to a phase's record rather than replacing it:

1. Inspect the fix's range with `git log` and `git diff`, and compare it with the requirement that failed and the plan of each phase it fixes.
2. In each fixed phase's Progress block, keep the original commits and Landed lines, and add `- Fix <base>..<head>: <what failed and what the fix changed>`. Add any demo the fix recorded to the Demos line.
3. Update the checks the fix touched from the fresh evidence: tick a check it re-ran and passed, and untick one it broke, naming the reason under Verified. An owner check is ticked only on evidence that establishes its outcome: the owner's confirmation for a check only a person can make, or a successful run of the check itself for one the tools failed at before. A fix alone never ticks one; note beside it what was fixed. Then set each fixed phase's status, and its line in Implementation Overview, from its checks as in the steps above.
4. Set `status`, update the view, and publish as in steps 5 to 7 above.

## Record final verification

For a final report, you receive the final commit, whole-plan check results, the review outcome, and outstanding owner checks. Compare the reported results with Plan Verification. Tick only checks whose results apply to the final state; leave other checks open with the reason. Update its `### Progress` block with the commit, check results and their locations, the review outcome, and outstanding work. If an older outline has no Plan Verification section, append this final account to the last phase's Progress instead of adding a new plan section. Update affected phase checks and Owner Checks under the same rules as a phase report, then set `status`, update the view, and publish as in steps 5 to 7. A final report does not establish completion by itself; the implementing agent checks the full completion criteria.

## Keep to your part

The plan belongs to the user and the implementing agent. Leave its wording as it is, and change another phase's progress only to record evidence for its checks. When what landed differs from the plan, record the difference in this phase's progress; a later reader compares plan and progress side by side.

Judgment about a difference belongs to the implementing agent. Name every consequential difference you find in your final message, so it can take it to the user, and continue recording the rest.

Your work is done when the relevant progress blocks, checkboxes, Owner Checks, and status match the supplied results, and the view reflects them and any plan revision. Publish and verify the view as described above; report an unreachable Dossier and any unfinished checks explicitly. In your final message, summarize what you recorded, checks lacking evidence, consequential differences, and the view's link or the reason publication stopped.
