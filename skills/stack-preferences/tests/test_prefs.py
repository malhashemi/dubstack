"""Regression tests for prefs.py, run against temporary layers rather than the real preference stores."""

import datetime
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

SKILL = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("prefs", SKILL / "scripts" / "prefs.py")
prefs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prefs)

TODAY = datetime.date.today().isoformat()
OLD = (datetime.date.today() - datetime.timedelta(days=200)).isoformat()


def entry(option, **fields):
    return {
        "layer": "shared",
        "title": "CI runners",
        "choices": [{"option": option}],
        "why": "user choice, no reason given",
        "decided": OLD,
        "checked": OLD,
        **fields,
    }


@pytest.fixture
def store(tmp_path, monkeypatch):
    base = tmp_path / "skill" / "data" / "preferences.json"
    global_dir = tmp_path / "home" / ".agents" / "stack-preferences"
    project = tmp_path / "project"
    monkeypatch.setattr(prefs, "BASE_FILE", base)
    monkeypatch.setattr(prefs, "GLOBAL_DIR", global_dir)
    monkeypatch.setattr(prefs, "GLOBAL_FILE", global_dir / "preferences.json")
    monkeypatch.setattr(prefs, "OVERRIDES_LOG", global_dir / "overrides.jsonl")
    monkeypatch.setattr(prefs, "base_is_checkout", lambda: False)
    files = {"base": base, "global": global_dir / "preferences.json", "project": project / prefs.PROJECT_RELATIVE}

    def write(layer, categories, **top):
        data = {"schema": 1, **top, "categories": categories}
        files[layer].parent.mkdir(parents=True, exist_ok=True)
        files[layer].write_text(json.dumps(data))

    def read(layer):
        return json.loads(files[layer].read_text())["categories"]

    def run(*argv):
        patch = tmp_path / "patch.json"
        argv = list(argv)
        if argv[0] in ("apply", "validate") and len(argv) > 1 and isinstance(argv[1], dict):
            patch.write_text(json.dumps({"categories": argv[1]}))
            argv[1] = str(patch)
        monkeypatch.setattr(sys, "argv", ["prefs.py", "--project-root", str(project), *argv])
        try:
            prefs.main()
        except SystemExit as exit:
            return exit.code or 0
        return 0

    write("base", {"runners": entry("Blacksmith")}, layers={"shared": "Shared tooling"})
    return SimpleNamespace(write=write, read=read, run=run)


def test_decision_only_edit_keeps_the_review_date(store, capsys):
    assert store.run("apply", {"runners": {"avoid": ["Depot"]}}, "--layer", "base") == 0
    runner = store.read("base")["runners"]
    assert runner["checked"] == OLD
    assert runner["decided"] == TODAY
    capsys.readouterr()
    store.run("stale")
    assert "runners" in capsys.readouterr().out


def test_a_review_writes_its_date_explicitly(store, capsys):
    assert store.run("apply", {"runners": {"checked": TODAY}}, "--layer", "base") == 0
    assert store.read("base")["runners"]["checked"] == TODAY
    assert store.read("base")["runners"]["decided"] == OLD
    capsys.readouterr()
    store.run("stale")
    assert "runners" not in capsys.readouterr().out


@pytest.mark.parametrize("layer,lower", [("global", "base"), ("project", "global")])
def test_new_choice_override_keeps_its_date_when_a_lower_choice_is_reviewed(store, capsys, layer, lower):
    assert store.run("apply", {"runners": {"choices": [{"option": "Depot"}]}}, "--layer", layer) == 0
    assert store.read(layer)["runners"]["checked"] == OLD
    assert store.run("apply", {"runners": {"checked": TODAY}}, "--layer", lower) == 0
    capsys.readouterr()
    assert store.run("get", "runners") == 0
    runner = json.loads(capsys.readouterr().out)[0]
    assert runner["choices"] == [{"option": "Depot"}]
    assert runner["checked"] == OLD
    assert runner["stale"] is True


def test_base_edit_compares_with_the_base_not_a_higher_layer(store):
    store.write("global", {"runners": {"choices": [{"option": "Depot"}]}})
    # Matching the global choice is still a change to the base's own decision.
    assert store.run("apply", {"runners": {"choices": [{"option": "Depot"}]}}, "--layer", "base") == 0
    runner = store.read("base")["runners"]
    assert [item["choices"] for item in runner["history"]] == [[{"option": "Blacksmith"}]]
    assert runner["decided"] == TODAY


def test_base_edit_that_restates_the_base_records_no_change(store):
    store.write("global", {"runners": {"choices": [{"option": "Depot"}]}})
    assert store.run("apply", {"runners": {"choices": [{"option": "Blacksmith"}]}}, "--layer", "base") == 0
    runner = store.read("base")["runners"]
    assert "history" not in runner
    assert runner["decided"] == OLD


def test_global_edit_ignores_the_project_layer(store):
    store.write("global", {"runners": {"choices": [{"option": "Depot"}], "decided": OLD}})
    store.write("project", {"runners": {"choices": [{"option": "self-hosted"}]}})
    assert store.run("apply", {"runners": {"choices": [{"option": "self-hosted"}]}}, "--layer", "global") == 0
    runner = store.read("global")["runners"]
    assert [item["choices"] for item in runner["history"]] == [[{"option": "Depot"}]]
    assert runner["decided"] == TODAY


def test_validate_knows_categories_from_lower_layers(store, capsys):
    store.write("global", {"editor": entry("Zed", title="Editor")})
    store.write("project", {"editor": {"title": "Team editor"}})
    assert store.run("validate") == 0
    assert capsys.readouterr().out.strip() == "valid"


def test_validate_rejects_a_partial_entry_no_lower_layer_defines(store, capsys):
    store.write("global", {"editor": {"title": "Editor"}})
    assert store.run("validate") == 1
    assert "editor: a new category needs" in capsys.readouterr().out


def test_apply_to_a_lower_layer_ignores_categories_only_above_it(store):
    store.write("global", {"editor": entry("Zed", title="Editor")})
    assert store.run("apply", {"editor": {"title": "Team editor"}}, "--layer", "base") == 2
    assert "editor" not in store.read("base")
    assert store.run("apply", {"editor": {"title": "Team editor"}}, "--layer", "project") == 0
    assert store.read("project")["editor"] == {"title": "Team editor"}


def test_validate_reads_a_patch_file_for_its_target_layer(store):
    store.write("global", {"editor": entry("Zed", title="Editor")})
    assert store.run("validate", {"editor": {"title": "Team editor"}}, "--layer", "project") == 0
    assert store.run("validate", {"editor": {"title": "Team editor"}}, "--layer", "base") == 1
    assert store.run("validate", {"runners": {"title": "Runners"}}, "--layer", "base") == 0


def test_shipped_preferences_hold_decisions_not_research():
    categories = json.loads((SKILL / "data" / "preferences.json").read_text())["categories"]
    assert [cid for cid, item in categories.items() if "facts" in item] == []
