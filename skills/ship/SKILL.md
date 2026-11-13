---
name: ship
description: Carry work the conversation has already settled to a pull request that is ready to merge, in one unattended run, proving the change, having it reviewed, opening the pull request, and seeing it through CI and review. It merges only when the request says to. Only use when the user invokes this skill by name or another skill's instructions name it.
---

# Ship

Take what the conversation settled to a pull request that is ready to merge, in this session. The user is not watching: your updates and your final message go unread until long after you stop. You own the work from its current state to that pull request, and nothing in the run waits for confirmation. The conversation is the brief. This route keeps no goal record and writes no handoff between sessions.

## Authority

The request is the permission for everything this run needs:

- **The change:** a branch of its own, commits, pushing that branch, merging its base into it, opening or updating its pull request, rerunning failed checks, and answering review feedback.
- **The means:** whatever tools and access this session has that the work or its proof needs. That includes running the app or a dev server, a browser, computer use, simulators and devices, screenshots and recordings, command-line tools, and the credentials the user's setup provides, such as a password manager's CLI, to sign in where the work requires it.

Where a project file or another instruction says to ask before using one of these means, or to leave testing to the user, the request replaces that step for this task. Use the means that gets the work done and gives direct proof, and list in the report the ones you used. Instructions about how to do something still govern: the command, fixture, account, or check they name. When the method they prefer cannot do the job, use another that can.

This permission covers only what this task needs. It does not get past an approval prompt from the harness or the system, or a sign-in step only the user can complete, such as a one-time code or a passkey. Keep secrets out of commits, the pull request, demos, and the report.

It does not authorize merging, enabling auto-merge, entering a merge queue, force-pushing, pushing to the default branch, bypassing branch protection, closing a pull request, deleting data, or changing production or anything else outside the repository. None of those may be delegated either. The pull request must not merge without the user: if auto-merge is enabled or it sits in a merge queue, turn that off, check again before each push, and report it.

## Merging

<important if="the request asks for the merge itself, as in 'ship and merge', or the user's standing instructions say `ship` merges in this project">
Read [references/merge.md](references/merge.md) before you start. It replaces the limit on merging and moves this run's endpoint to the merged change.
</important>

A request to finish the work or get it done is not a request to merge.

## Staying in the run

An obstacle is yours to get past: a tool to install, a service to start, a sign-in to make, an environment to repair, a flaky check to diagnose. Try another way before calling it a blocker. A progress summary, a plan for what remains, or an offer to continue ends nothing, since nobody is there to accept it. The run ends at Completion; until then its only pause is a question asked as "Asking the user" describes.

While checks or reviews are pending, wait the way `babysit-pr` waits. Ending your turn there ends the work, since nobody will prompt you again.

## The change

Open your work by stating, from the conversation, the change and what done looks like. The user reads it later in the report, so do not wait for an answer. When the conversation leaves a decision that only the user can make, facts too large to find while working, or more work than one session holds, this is the wrong route: stop before building, say what is unsettled, and recommend `basecamp`.

Deliver what the conversation settled with the smallest change that does it: fix the case that happened, not every case that could. Work the conversation did not ask for goes in the report as a follow-up. Changes the conversation already made in the working tree are the starting state; leave unrelated local changes alone. Read the repository's instructions, and work on a branch named by its conventions when you start on the default branch.

## Proof

Proof is evidence you observed yourself in this session: a command's output, a reproduction, a screenshot. Use the most direct proof each change allows:

- Reproduce the original failure, make the change, and watch the same reproduction pass.
- Run the checks the repository's CI runs.
- Add one focused test that fails without the change when the behaviour has none and the repository has a test setup.
- For anything users see or do, run it and look. Passing tests against mocks do not show that the experience works.

While you verify a change users can see or do, record a demo of it for the pull request: before and after screenshots, a short video, or a terminal transcript. Keep demos in the `demos/` folder of the goal's directory when the request names one, and otherwise outside the repository's tracked files.

A change you cannot find a way to prove is a question for the user, not a claim.

## Review

Get the independent review your standing guidance on models and review calls for, on the final diff, before the pull request. Weigh each finding against the code and what the conversation settled: fix it with the smallest change, reject it with evidence, or set it aside as a follow-up. Prove each fix, and have what a fix changed reviewed again.

## The pull request

Use `describe-pr` in this session to open or update the pull request, giving it the branch, its worktree, the demos, and the issue and goal directory when the request names them. Then use `babysit-pr` in this session to carry it through CI and review. Each fix gets its proof before it is pushed. When fixes change what the description says, update it with `describe-pr` yourself.

The pull request is ready to merge when all of these hold on its latest commit:

- Your proof and the review cover the final diff, including behaviour changed by later fixes and by resolving conflicts.
- `babysit-pr`'s readiness is established: required checks are green and the relevant reviewers, human or bot, have cleared this revision.
- It is up to date enough with its base that GitHub reports it mergeable.

Before you report, fetch the base and read the live pull request: its head, base, checks, reviews, and mergeability. Confirm it is open, not a draft, and not set to merge without the user. If someone else merged or closed it, report that instead.

## Asking the user

A question in an ordinary message goes unseen, and the thread looks finished. Ask through your harness's question tool, so the thread shows that it is waiting, and put everything the user needs in the question: the pull request's link, what blocks you, and the options with your recommendation first.

Ask only when you cannot continue alone:

- You cannot prove a change.
- Readiness cannot be reached and the cause is not yours to fix.
- The next step is outside this skill's authority, or needs something only the user can supply.
- The work turns out to hold a decision that changes the result.
- Another pull request makes this one obsolete.

Decide everything else yourself with sensible defaults and list those decisions in the report. Keep working on whatever does not depend on the question. When no question tool is available, or it returns no answer, leave the pull request open and unmerged and begin your final message with the question.

## Completion

The run is complete when:

- Every change in the final diff has proof observed in this session, and the review's findings are each fixed, rejected with evidence, or set aside in the report.
- The pull request's head is the branch's latest commit and its description matches that revision.
- The pull request is ready to merge, or the report says exactly what it waits on.
- It is open and not set to merge without the user.

Green checks, an open pull request, and a quiet watcher mark progress, not completion.

## Report

Lead with the verdict and the pull request's link:

- **Ready to merge:** readiness holds, and the pull request is open and unmerged.
- **Waiting on required approval:** only a person's approval remains, confirmed as the actual blocker.
- **Blocked:** what prevents readiness, what you tried, and what is needed.

Then give the final head, the proof for each change and the means you used to get it, the review's outcome, every decision you made for the user, what you could not verify, and the follow-ups you set aside.
