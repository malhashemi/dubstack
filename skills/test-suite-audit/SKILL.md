---
name: test-suite-audit
description: Audit a repository's tests and CI for cost that buys no protection, then remove, merge, move, or fix what the evidence supports and open a pull request carrying that evidence. Use when the user asks to audit, prune, or speed up a test suite, cut its CI time, cost, or flakiness, or find tests that are not worth keeping.
---

# Test Suite Audit

Make the suite catch meaningful regressions at the lowest cost, and deliver the justified changes as an open pull request with the evidence a reviewer needs. The aim is protection per minute and per dollar, never a test count or a coverage target.

A test earns its place when it guards behavior someone relies on, fails when that behavior breaks, survives refactors that preserve the behavior, and no cheaper test already catches the same break. Each of those is a judgment backed by evidence; the signals below inform it, and none decides it alone.

## Scope and authority

Infer the context from the conversation, the repository, its CI configuration and history, and what the user has said. Ask only for what you cannot find and that would change what you do, such as an area the user wants protected or excluded.

Invocation authorizes the justified, in-scope changes to tests and their CI, commits on a working branch, pushing it, and opening or updating the pull request. There is no selection or approval round before acting. It does not authorize merging, enabling auto-merge, publishing releases, changing product behavior, or changing permissions, branch protection, or which checks a merge requires; bring any of those to the user. Explicit constraints govern: a read-only request ends with the findings in chat, and an excluded area stays untouched.

Work on a branch of its own from the repository's base, unless the user names one, and leave the user's uncommitted work as it was.

**Protected areas** come from the user, plus whichever of these the repository has: authentication and permissions, tenant isolation, money, migrations and data integrity, security boundaries, and data loss or leaks. Each protected candidate gets its own reason and its own breakage result. A slow test that is the sole essential protection for such an area stays on the required path.

## Map the suite

Build a lean map: languages and frameworks; unit, integration, end-to-end, contract, and snapshot tests by module; the CI jobs with their matrix, runner sizes, triggers, caches, and retries; and how much Git and CI history is available. Measure at the finest practical grain, a test case before a file and a file before a job.

## Gather the evidence

Scale the effort to the suite and the access you have. Disclose every run, history window, or permission you lacked. Missing evidence lowers confidence in a removal; it never justifies one, and a safeguard is not discarded because proving its worth would be costly.

**Cost.** Take runtimes from machine-readable reporters. Look back over CI history, normally 30 to 90 days as available. Separate setup, install, build, and download time from test execution. Aggregate billed cost from the provider's actual prices and plan rules, weighted by runner size, and keep runner minutes, wall-clock time, and money actually saved distinct. Label every number measured, estimated with its basis, or unavailable. Never invent a rate or present local timings as CI timings. A sum of baseline durations is not a saving when parallelism, fixed setup, per-minute rounding, or included allowances decide what is paid or waited for.

**Flakiness.** In CI, find commits where the same test failed and then passed, including manual reruns and retries that the reporter hides. Locally, run the suite at least three times before changing anything, in random order where the runner supports it, with extra runs for suspects. Classify each flake's cause: timing, order, shared state, network, an external service, or a driver. Tell infrastructure noise apart from real regressions. Three passes do not prove a test is stable.

**History.** Trace each retained CI failure to what fixed it. A product fix with the test unchanged supports a real catch. A test-only change suggests noise, but it may be a changed specification or the repair of an assertion that passed when it should have failed, so read the context. A pass on rerun with nothing changed suggests a flake. Missing or unresolved history is unknown. Co-changes with bug fixes support a test's value; repeated edits during refactors that changed no behavior suggest coupling to implementation. Short history weakens any "never failed" claim.

**Overlap.** Use per-test coverage contexts when the tooling supports them or they are practical to enable; otherwise sample and state the limits. A test whose lines are a subset of another's is a hint, not proof: distinct assertions, inputs, boundaries, and failure modes matter. Look for duplicates across levels, such as a unit test and an end-to-end test on the same path, and parametrized cases that exercise the same path.

**Static hints.** Tests that restate types or schemas, check mock interactions rather than outcomes, import private internals, assert snapshots or exact text, or assert nothing beyond not throwing are worth a closer look. Some of these are legitimate contracts.

## Prove it before removing

Deliberate breakage is the gate for every deletion or merge. Introduce focused faults in the behavior the candidate is meant to guard, then record whether the candidate catches each fault and whether the remaining cheaper tests catch it. Count a surviving test as overlap only when it runs in the same required lane, on the same triggers and required checks. Break a sample of the ordinary candidates and every candidate in a protected area, and make sure each test you actually delete has a demonstrated absence of any relevant gap.

- Only the candidate catches a meaningful fault: keep it.
- Neither catches it: close the high-signal gap first, or keep the candidate.
- The survivors catch what the candidate catches: the candidate can go, on this evidence.

Interpret the results honestly. A surviving mutant may be a real gap or an equivalent mutant; an invalid mutant proves nothing. Sampling never proves full equivalence.

Apply faults in isolation so the user's edits are never at risk, revert every one, and confirm none remains in the final diff.

## Decide

Give each candidate a verdict: delete, merge, move, fix, or keep. Rank the changes by the CI money, minutes, and reruns they are expected to avoid, weighted by confidence in the evidence. Do not count overlapping savings twice or credit a whole job's cost to one test; unknown data is unknown, not zero. High confidence needs several independent signals.

Cost outside test bodies, such as caching, triggers, the matrix, runner size, and duplicated setup, is often larger. Judge it on the same basis. Make the CI changes directly tied to the audit within the authority above, and bring to the user any that carry product risk or need permissions.

## Change

- Remove or merge only candidates the evidence supports.
- Move a valuable but expensive test to a nightly or pre-release lane only when that feedback delay is acceptable, the lane really runs, and required critical protection stays on the required path.
- Fix flaky tests whose cause you established; leave undiagnosed ones reported, not guessed at.
- Clean up fixtures, helpers, mocks, and configuration left dead by the changes, keeping whatever remaining tests use.
- Get green honestly: no skips, commented-out tests, weakened assertions, added retries, or lowered thresholds.
- Add a test only where breakage revealed a meaningful uncovered gap, and list each addition with its reason.
- Leave product behavior as it is.

Commit in coherent groups by area rather than as one mixed change.

## Verify

Run the full suite and checks the repository expects. Repeat the local runs in a way comparable to the baseline, with the same run count and ordering. Confirm no deliberate fault remains. Report before-and-after measurements apart from projections.

## The pull request

Open or update the pull request with the repository's usual tooling and conventions, with the latest commits pushed. Keep the description concise and reviewable: what changed, why each change is safe, the protection that remains, the breakage results, before-and-after figures, the history window and its limits, the data that was unavailable, and the CI and setup savings with their basis. The evidence belongs in the description; no report file, Dossier page, or goal stage is required.

## Completion

The audit is complete when its justified changes are in an open pull request with the latest commits pushed, every deliberate fault is gone from the diff, and the description carries the evidence above. Report the pull request's URL and the current state of its checks and reviews as they are.

An open pull request is not a mergeable one. Call it ready only when the repository's merge process is satisfied for the current revision: required checks green and required reviews cleared. When checks or reviews are pending, or a failure stems from the change, either carry it through the platform's workflow, which `babysit-pr` does, or report it as not yet ready with what remains. Leave merging and releasing to the user.

When the evidence supports no change, open no pull request. Report what was measured, the verdicts, and why nothing earned a change. A read-only audit ends the same way, with the findings and the changes they would support.
