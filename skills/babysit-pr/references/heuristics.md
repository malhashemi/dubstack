# CI and Review Heuristics

Use these as diagnostic aids alongside the [skill's goal and boundaries](../SKILL.md).

## Fix, retry, or escalate

**Branch-related:** logs connect the failure to changes in the PR, such as a compile/type error, deterministic test regression, changed snapshot, lint violation, or broken build configuration. Fix the cause and verify it before pushing.

**Transient or unrelated:** evidence points to network/registry timeouts, runner provisioning, a service outage, rate limiting, or a known intermittent failure outside the changed code. Retry failed jobs when the current CI round is terminal and a retry is warranted. The default budget is three rerun cycles per head SHA.

**Unclear:** inspect the failed job, relevant code, and available baseline evidence before deciding. A failure in a touched file alone does not prove the PR caused it. Escalate a persistent external failure rather than changing unrelated tests or infrastructure merely to turn CI green.

If a job has failed while the workflow is still running, diagnose from that job's logs immediately. If a review or CI fix will produce a new commit, push it before spending retries on the old SHA.

## Review judgment

Apply the same technical standard to feedback from any human or bot:

- Is the finding correct for the current code?
- Is it actionable within the PR's scope and the user's intent?
- Has it already been addressed, duplicated, or superseded?
- Can the change be verified, or does it require a decision from the user?

Read full threads before acting. Bot summaries may be edited in place, and one comment can contain multiple findings. A resolved thread normally needs no further action unless there is new unresolved follow-up. An outdated line location does not mean the underlying finding is fixed.

Ignore pending unpublished reviews and routine automation chatter. Track valid unresolved findings even after they disappear from `new_review_items`; that field records delivery, not completion. Follow the skill's communication permissions when replying or resolving.

## When user help is needed

Typical blockers include missing repository permissions, a branch that cannot be safely updated, local changes that conflict with the needed fix, exhausted retries on a persistent external failure, or a reviewer request requiring a product decision. Report the evidence and the specific decision or action needed.

Pending CI or missing reviewer clearance calls for the script to wait. Green CI alone, a quiet review, or resolving findings yourself does not establish approval. Once the current revision has both green CI and explicit reviewer clearance with no remaining merge blockers, report readiness and finish.
