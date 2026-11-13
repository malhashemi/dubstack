# Merging

The request asked for the merge, so this run ends with the change merged rather than with a pull request waiting for the user. You own the work from its current state to the merge commit.

## What changes

- Merging this run's pull request is authorized once the merge gate passes. So is the repository's auto-merge or merge queue for that pull request, where that is how the repository merges.
- The instruction to turn off auto-merge or leave a merge queue no longer applies to it.

Every other limit holds: no force-push, no push to the default branch, no closing the pull request, and no merging any other pull request. Merge through branch protection as it is configured. `--admin`, dismissing a review, and changing a protection or a required check are bypasses, and stay outside this permission.

## The merge gate

Merge only with full confidence, which means all of these are true on the latest commit, read from the live pull request just before merging:

- The pull request is ready to merge as the skill defines it.
- No person's review requests changes, and every approval the repository requires has been given.
- Review bots have finished, and each finding is fixed or answered with a written reason. A bot that only asks for a person to look, with no finding behind it, does not hold the merge when your proof covers the diff; name it in the report.
- The pull request is open, not a draft, and its head is the commit you proved and had reviewed.

A check still running, a reviewer who has not answered, and a watcher gone quiet are not a pass.

## Merging

Use the method the repository uses: look at the methods it allows and at recently merged pull requests, and follow its conventions for the merge commit's title and message. Where auto-merge or a merge queue does the merging, stay until GitHub reports the pull request merged. A merge that fails, or a pull request the queue removes, is a failure to diagnose like any failed check.

Confirm the merge from GitHub and record the merge commit. What the merge sets off afterwards, such as a release or a deploy, is not part of this run; report what you can see it started.

## When the gate cannot pass

Leave the pull request open and unmerged and ask as the skill's "Asking the user" describes. A required approval that has not come is the user's to obtain, never yours to work around.

## Completion and report

The run is complete when GitHub reports the pull request merged and the rest of the skill's completion holds for the merged revision. Lead the report with **Merged**, the pull request's link, and the merge commit, then give what the skill's report asks for.
