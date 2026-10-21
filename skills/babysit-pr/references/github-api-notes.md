# GitHub CLI / API Notes

The bundled [watcher](../scripts/gh_pr_watch.py) owns monitoring. Use the commands below for the initial PR assessment and for diagnosis and action after it returns an event, not as an agent-side polling loop. Run repository commands from the target worktree. The placeholders below refer to the PR's base repository unless noted otherwise.

## PR state and checks

```bash
gh pr view <pr> --repo <owner/repo> --json number,url,state,mergedAt,closedAt,headRefName,headRefOid,headRepository,headRepositoryOwner,mergeable,mergeStateStatus,reviewDecision
gh pr checks <pr> --repo <owner/repo> --json name,state,bucket,link,workflow,event,startedAt,completedAt
gh api 'repos/<owner>/<repo>/actions/runs' -X GET -f head_sha=<sha> -f per_page=100
```

Check the current head SHA after a push. The PR's base repository owns its reviews and checks; a fork's head repository is the push target. Read the latest state before a mutation.

`gh pr checks` can return JSON with exit code 1 for failed checks or 8 for pending checks. The watcher accepts those status responses while still reporting command errors and invalid JSON.

The watcher summarizes pending, failed, and passed checks and inspects Actions runs/jobs for the head SHA. It retrieves up to 100 runs per SHA and 100 jobs per run. Use additional pages or linked check-provider reports when that is insufficient. External CI and review providers may publish details through check annotations or report links rather than PR comments.

## Failed jobs and retries

```bash
gh run view <run-id> --repo <owner/repo> --json jobs,name,workflowName,conclusion,status,url,headSha
gh api 'repos/<owner>/<repo>/actions/runs/<run-id>/jobs' -X GET -f per_page=100
gh api 'repos/<owner>/<repo>/actions/jobs/<job-id>/logs'
gh run view <run-id> --repo <owner/repo> --log-failed
gh run rerun <run-id> --repo <owner/repo> --failed
```

Prefer the individual job's logs as soon as it fails. `gh run view --log-failed` may not expose logs until the overall workflow finishes. Fetching logs is read-only; rerunning jobs is a write.

The watcher's `--retry-failed-now` command refreshes state, requires failed PR checks and failed Actions runs, waits for checks to be terminal, and enforces the per-SHA retry budget. It reruns all discovered failed Actions runs, so inspect their failures first. It cannot classify flakiness or retry an external provider's jobs. Its response includes a fresh snapshot; inspect that for review feedback too.

## Published review activity

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/<pr>/comments?per_page=100'
gh api --paginate 'repos/<owner>/<repo>/pulls/<pr>/comments?per_page=100'
gh api --paginate 'repos/<owner>/<repo>/pulls/<pr>/reviews?per_page=100'
```

The watcher paginates all three collections and surfaces all authors without bot-name or repository-membership allowlists. Items include their kind, ID, author login/type/association, timestamps, body, URL, and available file/line context. Submitted reviews also include `review_state`. Use this context to judge relevance; delivery is not an endorsement of the content.

An inline comment's `pull_request_review_id` identifies its parent review. Reviews in `PENDING` state and their inline comments are excluded without marking them seen, so they can surface when published.

Thread resolution is not available from these REST comment collections. Use GitHub's review-thread data when deciding whether feedback is still open. For example:

```graphql
query($owner: String!, $repo: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $cursor) {
        nodes {
          id
          isResolved
          isOutdated
          comments(first: 100) {
            nodes { databaseId body url author { login } }
            pageInfo { hasNextPage endCursor }
          }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}
```

Follow `pageInfo` for both threads and their comments. Match REST comment IDs to `databaseId` to find the thread. Inspect all participants before replying or resolving under the [skill's communication rules](../SKILL.md). Review requests and retriggers depend on the repository and reviewer integration; infer them from its instructions or documented behavior.

## Watcher output and state

- `--watch` polls silently and exits after emitting one JSON event. `event` is `attention` for new feedback, new or changed failures/conflicts, or candidate readiness; `stop` indicates a closed/merged PR or exhausted retries. `payload` contains `snapshot` and `state_file`. The snapshot includes `pr`, `checks`, `failed_runs`, `failed_jobs`, `new_review_items`, `actions`, and `retry_state`.
- Restart `--watch` only when further progress depends on checks or reviewers. Once the agent verifies green CI and explicit reviewer clearance for the current revision with no remaining merge blockers, babysitting is complete. Persisted observations suppress repeat notifications for unchanged conditions if watching resumes. Poll timing is controlled by the script's `--poll-seconds` option.
- `--once` emits a single snapshot plus `state_file` for the initial assessment or diagnosis. It is not the monitoring loop.
- `--retry-failed-now` emits its snapshot, state-file path, rerun outcome, run IDs, and reason. It performs a write only when its eligibility checks pass.

By default, state lives in the system temporary directory as `babysit-pr-<owner>-<repo>-pr<number>.json`. Use `--state-file` for a durable location or to distinguish sessions with otherwise identical repository names on different GitHub hosts. Use the same file across snapshots and retries, with only one writer at a time.

The first poll surfaces existing published activity. Later polls deduplicate by item kind, ID, and a fingerprint of content, update timestamp, and review state. This catches edited bot summaries and changed review submissions. Older state files without fingerprints replay published items once; pass their path explicitly to resume them.

Execution failures return an error for the agent to resolve. Address dependencies and access without modifying the watcher; request user authentication or credentials when needed, then resume with the same state file.

Seen items have been delivered, not resolved. Preserve your own outstanding-findings record and re-read unresolved threads on resumption. Likewise, `ready_to_merge` is a candidate signal based on checks, mergeability, review decision, and absence of newly delivered items; it cannot prove all findings are resolved or establish explicit reviewer clearance. The agent interprets the reviewers' actual conclusions against the current revision. Readiness can be established from any handoff, including a review comment, without waiting for a separate `ready_to_merge` event.
