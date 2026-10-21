import argparse
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).with_name("gh_pr_watch.py")
MODULE_SPEC = importlib.util.spec_from_file_location("gh_pr_watch", MODULE_PATH)
gh_pr_watch = importlib.util.module_from_spec(MODULE_SPEC)
assert MODULE_SPEC.loader is not None
MODULE_SPEC.loader.exec_module(gh_pr_watch)


def sample_pr():
    return {
        "number": 123,
        "url": "https://github.com/example/project/pull/123",
        "repo": "example/project",
        "head_sha": "abc123",
        "head_branch": "feature",
        "state": "OPEN",
        "merged": False,
        "closed": False,
        "mergeable": "MERGEABLE",
        "merge_state_status": "CLEAN",
        "review_decision": "",
    }


def sample_checks(**overrides):
    checks = {
        "pending_count": 0,
        "failed_count": 0,
        "passed_count": 12,
        "all_terminal": True,
    }
    checks.update(overrides)
    return checks


def sample_snapshot(**overrides):
    snapshot = {
        "pr": sample_pr(),
        "checks": sample_checks(),
        "failed_runs": [],
        "failed_jobs": [],
        "new_review_items": [],
        "retry_state": {
            "current_sha_retries_used": 0,
            "max_flaky_retries": 3,
        },
    }
    snapshot.update(overrides)
    snapshot["actions"] = gh_pr_watch.recommend_actions(
        snapshot["pr"],
        snapshot["checks"],
        snapshot["failed_runs"],
        snapshot["failed_jobs"],
        snapshot["new_review_items"],
        snapshot["retry_state"]["current_sha_retries_used"],
        snapshot["retry_state"]["max_flaky_retries"],
    )
    return snapshot


@pytest.mark.parametrize(
    "exit_code,bucket,state",
    [(0, "pass", "SUCCESS"), (1, "fail", "FAILURE"), (8, "pending", "PENDING")],
)
def test_pr_checks_accepts_status_exit_codes(monkeypatch, exit_code, bucket, state):
    checks = [{"name": "CI", "bucket": bucket, "state": state}]

    def fake_run(cmd, **kwargs):
        output = json.dumps(checks)
        if exit_code:
            raise subprocess.CalledProcessError(exit_code, cmd, output=output)
        return subprocess.CompletedProcess(cmd, 0, stdout=output)

    monkeypatch.setattr(gh_pr_watch.subprocess, "run", fake_run)

    assert gh_pr_watch.get_pr_checks("123", "example/project") == checks


def test_pr_checks_still_reports_command_errors(monkeypatch):
    def fake_run(cmd, **kwargs):
        raise subprocess.CalledProcessError(1, cmd, stderr="authentication failed")

    monkeypatch.setattr(gh_pr_watch.subprocess, "run", fake_run)

    with pytest.raises(gh_pr_watch.GhCommandError, match="authentication failed"):
        gh_pr_watch.get_pr_checks("123", "example/project")


def test_collect_snapshot_fetches_review_items_before_ci(monkeypatch, tmp_path):
    call_order = []
    pr = sample_pr()

    monkeypatch.setattr(gh_pr_watch, "resolve_pr", lambda *args, **kwargs: pr)
    monkeypatch.setattr(gh_pr_watch, "load_state", lambda path: ({}, True))
    monkeypatch.setattr(
        gh_pr_watch,
        "fetch_new_review_items",
        lambda *args, **kwargs: call_order.append("review") or [],
    )
    monkeypatch.setattr(
        gh_pr_watch,
        "get_pr_checks",
        lambda *args, **kwargs: call_order.append("checks") or [],
    )
    monkeypatch.setattr(
        gh_pr_watch,
        "summarize_checks",
        lambda checks: call_order.append("summarize") or sample_checks(),
    )
    monkeypatch.setattr(
        gh_pr_watch,
        "get_workflow_runs_for_sha",
        lambda *args, **kwargs: call_order.append("workflow") or [],
    )
    monkeypatch.setattr(
        gh_pr_watch,
        "failed_runs_from_workflow_runs",
        lambda *args, **kwargs: call_order.append("failed_runs") or [],
    )
    monkeypatch.setattr(
        gh_pr_watch,
        "failed_jobs_from_workflow_runs",
        lambda *args, **kwargs: call_order.append("failed_jobs") or [],
    )
    monkeypatch.setattr(
        gh_pr_watch,
        "recommend_actions",
        lambda *args, **kwargs: call_order.append("recommend") or ["idle"],
    )
    monkeypatch.setattr(gh_pr_watch, "save_state", lambda *args, **kwargs: None)

    args = argparse.Namespace(
        pr="123",
        repo=None,
        state_file=str(tmp_path / "watcher-state.json"),
        max_flaky_retries=3,
    )

    gh_pr_watch.collect_snapshot(args)

    assert call_order.index("review") < call_order.index("checks")
    assert call_order.index("review") < call_order.index("workflow")


def test_recommend_actions_prioritizes_review_comments():
    actions = gh_pr_watch.recommend_actions(
        sample_pr(),
        sample_checks(failed_count=1),
        [{"run_id": 99}],
        [],
        [{"kind": "review_comment", "id": "1"}],
        0,
        3,
    )

    assert actions == [
        "process_review_comment",
        "diagnose_ci_failure",
        "retry_failed_checks",
    ]


@pytest.mark.parametrize("kind", ["issue_comment", "review_comment", "review"])
@pytest.mark.parametrize(
    "login,author_type,association",
    [
        ("review-assistant[bot]", "Bot", "NONE"),
        ("custom-review-service", "Bot", "NONE"),
        ("external-contributor", "User", "NONE"),
        ("maintainer", "User", "MEMBER"),
    ],
)
def test_review_activity_surfaces_without_author_allowlists(
    monkeypatch, kind, login, author_type, association
):
    item = {
        "id": 10,
        "user": {"login": login, "type": author_type},
        "author_association": association,
        "state": "COMMENTED",
        "body": "This can return the wrong result.",
    }
    endpoint = gh_pr_watch.comment_endpoints(sample_pr()["repo"], 123)[kind]
    monkeypatch.setattr(
        gh_pr_watch,
        "gh_api_list_paginated",
        lambda requested, **kwargs: [item] if requested == endpoint else [],
    )
    state = {}

    items = gh_pr_watch.fetch_new_review_items(sample_pr(), state, fresh_state=True)

    assert len(items) == 1
    assert items[0]["kind"] == kind
    assert items[0]["author"] == login
    assert items[0]["author_type"] == author_type
    assert items[0]["author_association"] == association
    assert gh_pr_watch.fetch_new_review_items(sample_pr(), state, fresh_state=False) == []


@pytest.mark.parametrize("kind", ["issue_comment", "review_comment", "review"])
def test_edited_review_activity_resurfaces_once(monkeypatch, kind):
    item = {
        "id": 10,
        "user": {"login": "maintainer", "type": "User"},
        "author_association": "MEMBER",
        "state": "COMMENTED",
        "body": "Initial feedback",
    }
    endpoint = gh_pr_watch.comment_endpoints(sample_pr()["repo"], 123)[kind]
    monkeypatch.setattr(
        gh_pr_watch,
        "gh_api_list_paginated",
        lambda requested, **kwargs: [item] if requested == endpoint else [],
    )
    state = {}
    assert len(gh_pr_watch.fetch_new_review_items(sample_pr(), state, fresh_state=True)) == 1
    assert gh_pr_watch.fetch_new_review_items(sample_pr(), state, fresh_state=False) == []

    # Submitted reviews do not always expose updated_at; content changes count.
    item["body"] = "Updated feedback with another finding"
    items = gh_pr_watch.fetch_new_review_items(sample_pr(), state, fresh_state=False)

    assert len(items) == 1
    assert items[0]["body"] == item["body"]
    assert gh_pr_watch.fetch_new_review_items(sample_pr(), state, fresh_state=False) == []


def test_submitted_review_state_change_resurfaces(monkeypatch):
    review = {
        "id": 10,
        "user": {"login": "maintainer", "type": "User"},
        "author_association": "MEMBER",
        "state": "CHANGES_REQUESTED",
        "body": "",
    }
    monkeypatch.setattr(
        gh_pr_watch,
        "gh_api_list_paginated",
        lambda endpoint, **kwargs: [review] if endpoint.endswith("/reviews") else [],
    )
    state = {}
    gh_pr_watch.fetch_new_review_items(sample_pr(), state, fresh_state=True)
    review["state"] = "DISMISSED"

    items = gh_pr_watch.fetch_new_review_items(sample_pr(), state, fresh_state=False)

    assert len(items) == 1
    assert items[0]["review_state"] == "DISMISSED"


def test_pending_review_feedback_surfaces_only_after_publication(monkeypatch):
    state = {
        "seen_review_comment_ids": ["20"],
        "seen_review_ids": ["10"],
    }
    review = {
        "id": 10,
        "user": {"login": "octocat"},
        "author_association": "MEMBER",
        "state": "PENDING",
        "body": "Please rename this.",
        "created_at": "2026-06-08T10:00:00Z",
        "submitted_at": None,
        "html_url": "https://github.com/example/project/pull/123#pullrequestreview-10",
    }
    review_comment = {
        "id": 20,
        "pull_request_review_id": 10,
        "user": {"login": "octocat"},
        "author_association": "MEMBER",
        "body": "Please rename this.",
        "created_at": "2026-06-08T10:00:00Z",
        "path": "src/example.rs",
        "line": 7,
        "html_url": "https://github.com/example/project/pull/123#discussion_r20",
    }

    def fake_list(endpoint, **kwargs):
        if endpoint.endswith("/issues/123/comments"):
            return []
        if endpoint.endswith("/pulls/123/comments"):
            return [review_comment]
        if endpoint.endswith("/pulls/123/reviews"):
            return [review]
        raise AssertionError(f"unexpected endpoint: {endpoint}")

    monkeypatch.setattr(gh_pr_watch, "gh_api_list_paginated", fake_list)

    assert (
        gh_pr_watch.fetch_new_review_items(
            sample_pr(),
            state,
            fresh_state=True,
        )
        == []
    )
    assert state["seen_review_comment_ids"] == []
    assert state["seen_review_ids"] == []

    review["state"] = "COMMENTED"
    review["submitted_at"] = "2026-06-08T10:05:00Z"

    published_items = gh_pr_watch.fetch_new_review_items(
        sample_pr(),
        state,
        fresh_state=False,
    )

    assert {(item["kind"], item["id"]) for item in published_items} == {
        ("review", "10"),
        ("review_comment", "20"),
    }
    assert state["seen_review_comment_ids"] == ["20"]
    assert state["seen_review_ids"] == ["10"]


def test_run_watch_waits_silently_through_pending_checks_and_approval(monkeypatch, tmp_path, capsys):
    sleeps = []
    snapshots = iter(
        sample_snapshot(
            pr={**sample_pr(), "review_decision": "REVIEW_REQUIRED"},
            checks=sample_checks(pending_count=n, all_terminal=n == 0),
        )
        for n in (3, 2, 1, 0)
    )

    monkeypatch.setattr(
        gh_pr_watch,
        "collect_snapshot",
        lambda args: (next(snapshots), tmp_path / "state.json"),
    )

    class StopWatch(Exception):
        pass

    def fake_sleep(seconds):
        sleeps.append(seconds)
        if len(sleeps) >= 4:
            raise StopWatch

    monkeypatch.setattr(gh_pr_watch.time, "sleep", fake_sleep)

    with pytest.raises(StopWatch):
        gh_pr_watch.run_watch(argparse.Namespace(poll_seconds=30))

    assert sleeps == [30, 30, 30, 30]
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    "snapshot,expected_action",
    [
        (sample_snapshot(), "ready_to_merge"),
        (
            sample_snapshot(checks=sample_checks(failed_count=1)),
            "diagnose_ci_failure",
        ),
        (
            sample_snapshot(pr={**sample_pr(), "mergeable": "CONFLICTING"}),
            "resolve_merge_conflict",
        ),
    ],
)
def test_run_watch_hands_off_once_then_waits_on_restart(
    monkeypatch, tmp_path, capsys, snapshot, expected_action
):
    monkeypatch.setattr(
        gh_pr_watch,
        "collect_snapshot",
        lambda args: (snapshot, tmp_path / "state.json"),
    )

    class Waiting(Exception):
        pass

    def stop_when_waiting(seconds):
        raise Waiting

    monkeypatch.setattr(gh_pr_watch.time, "sleep", stop_when_waiting)

    assert gh_pr_watch.run_watch(argparse.Namespace(poll_seconds=30)) == 0
    event = json.loads(capsys.readouterr().out)
    assert event["event"] == "attention"
    assert expected_action in event["payload"]["snapshot"]["actions"]

    with pytest.raises(Waiting):
        gh_pr_watch.run_watch(argparse.Namespace(poll_seconds=30))
    assert capsys.readouterr().out == ""


def test_run_watch_returns_new_feedback_without_waiting(monkeypatch, tmp_path, capsys):
    snapshots = iter(
        sample_snapshot(new_review_items=[{"id": "1", "body": body}])
        for body in ("Initial feedback", "Edited feedback")
    )
    monkeypatch.setattr(
        gh_pr_watch,
        "collect_snapshot",
        lambda args: (next(snapshots), tmp_path / "state.json"),
    )
    monkeypatch.setattr(
        gh_pr_watch.time, "sleep", lambda seconds: pytest.fail("Feedback should hand off immediately")
    )

    for expected_body in ("Initial feedback", "Edited feedback"):
        assert gh_pr_watch.run_watch(argparse.Namespace(poll_seconds=30)) == 0
        event = json.loads(capsys.readouterr().out)
        assert event["event"] == "attention"
        assert event["payload"]["snapshot"]["new_review_items"][0]["body"] == expected_body


def test_run_watch_does_not_reannounce_readiness_after_feedback(monkeypatch, tmp_path, capsys):
    snapshots = iter([
        sample_snapshot(new_review_items=[{"id": "1", "body": "Feedback"}]),
        sample_snapshot(),
    ])
    monkeypatch.setattr(
        gh_pr_watch,
        "collect_snapshot",
        lambda args: (next(snapshots), tmp_path / "state.json"),
    )

    class Waiting(Exception):
        pass

    def stop_when_waiting(seconds):
        raise Waiting

    monkeypatch.setattr(gh_pr_watch.time, "sleep", stop_when_waiting)

    assert gh_pr_watch.run_watch(argparse.Namespace(poll_seconds=30)) == 0
    capsys.readouterr()
    with pytest.raises(Waiting):
        gh_pr_watch.run_watch(argparse.Namespace(poll_seconds=30))
    assert capsys.readouterr().out == ""


def test_run_watch_reports_new_failed_attempt_even_if_pending_was_not_observed(
    monkeypatch, tmp_path, capsys
):
    snapshots = iter(
        sample_snapshot(
            checks=sample_checks(failed_count=1),
            failed_runs=gh_pr_watch.failed_runs_from_workflow_runs(
                [{
                    "id": 99,
                    "head_sha": "abc123",
                    "status": "completed",
                    "conclusion": "failure",
                    "run_attempt": attempt,
                }],
                "abc123",
            ),
        )
        for attempt in (1, 2)
    )
    monkeypatch.setattr(
        gh_pr_watch,
        "collect_snapshot",
        lambda args: (next(snapshots), tmp_path / "state.json"),
    )
    monkeypatch.setattr(
        gh_pr_watch.time, "sleep", lambda seconds: pytest.fail("New failure should hand off immediately")
    )

    for _ in range(2):
        assert gh_pr_watch.run_watch(argparse.Namespace(poll_seconds=30)) == 0
        event = json.loads(capsys.readouterr().out)
        assert event["event"] == "attention"
        assert "diagnose_ci_failure" in event["payload"]["snapshot"]["actions"]


def test_run_watch_waits_for_retry_eligibility_after_diagnosis(monkeypatch, tmp_path, capsys):
    pending_failure = sample_snapshot(
        checks=sample_checks(pending_count=1, failed_count=1, all_terminal=False),
        failed_runs=[{"run_id": 99}],
    )
    terminal_failure = sample_snapshot(
        checks=sample_checks(failed_count=1),
        failed_runs=[{"run_id": 99}],
    )
    snapshots = iter([pending_failure, pending_failure, terminal_failure])
    sleeps = []
    monkeypatch.setattr(
        gh_pr_watch,
        "collect_snapshot",
        lambda args: (next(snapshots), tmp_path / "state.json"),
    )
    monkeypatch.setattr(gh_pr_watch.time, "sleep", sleeps.append)

    assert gh_pr_watch.run_watch(argparse.Namespace(poll_seconds=30)) == 0
    first = json.loads(capsys.readouterr().out)
    assert first["payload"]["snapshot"]["actions"] == ["diagnose_ci_failure"]
    assert gh_pr_watch.run_watch(argparse.Namespace(poll_seconds=30)) == 0
    second = json.loads(capsys.readouterr().out)
    assert "retry_failed_checks" in second["payload"]["snapshot"]["actions"]
    assert sleeps == [30]


@pytest.mark.parametrize("merged", [False, True])
def test_run_watch_reports_closed_pr_and_exits(monkeypatch, tmp_path, capsys, merged):
    snapshot = sample_snapshot(
        pr={**sample_pr(), "closed": True, "merged": merged, "state": "MERGED" if merged else "CLOSED"}
    )
    monkeypatch.setattr(
        gh_pr_watch,
        "collect_snapshot",
        lambda args: (snapshot, tmp_path / "state.json"),
    )
    monkeypatch.setattr(
        gh_pr_watch.time, "sleep", lambda seconds: pytest.fail("Closed PR should stop immediately")
    )

    assert gh_pr_watch.run_watch(argparse.Namespace(poll_seconds=30)) == 0
    event = json.loads(capsys.readouterr().out)
    assert event["event"] == "stop"
    assert "stop_pr_closed" in event["payload"]["snapshot"]["actions"]


def test_failed_jobs_include_direct_logs_endpoint(monkeypatch):
    jobs_by_run = {
        99: [
            {
                "id": 555,
                "name": "unit tests",
                "status": "completed",
                "conclusion": "failure",
                "html_url": "https://github.com/example/project/actions/runs/99/job/555",
            },
            {
                "id": 556,
                "name": "lint",
                "status": "completed",
                "conclusion": "success",
            },
        ]
    }

    monkeypatch.setattr(
        gh_pr_watch,
        "get_jobs_for_run",
        lambda repo, run_id: jobs_by_run[run_id],
    )

    failed_jobs = gh_pr_watch.failed_jobs_from_workflow_runs(
        "example/project",
        [
            {
                "id": 99,
                "name": "CI",
                "status": "in_progress",
                "conclusion": "",
                "head_sha": "abc123",
                "run_attempt": 2,
            }
        ],
        "abc123",
    )

    assert failed_jobs == [
        {
            "run_id": 99,
            "run_attempt": 2,
            "workflow_name": "CI",
            "run_status": "in_progress",
            "run_conclusion": "",
            "job_id": 555,
            "job_name": "unit tests",
            "status": "completed",
            "conclusion": "failure",
            "html_url": "https://github.com/example/project/actions/runs/99/job/555",
            "logs_endpoint": "repos/example/project/actions/jobs/555/logs",
        }
    ]
