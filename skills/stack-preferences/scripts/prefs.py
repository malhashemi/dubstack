#!/usr/bin/env python3
"""Read and write stack preferences across the base, global, and project layers."""

import argparse
import copy
import datetime
import json
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
BASE_FILE = SKILL_DIR / "data" / "preferences.json"
GLOBAL_DIR = Path.home() / ".agents" / "stack-preferences"
GLOBAL_FILE = GLOBAL_DIR / "preferences.json"
OVERRIDES_LOG = GLOBAL_DIR / "overrides.jsonl"
PROJECT_RELATIVE = Path(".agents") / "stack-preferences" / "preferences.json"
STALE_DAYS = 90
LAYERS = ("base", "global", "project")

ENTRY_FIELDS = {
    "layer": str,
    "title": str,
    "decides": str,
    "choices": list,
    "per_project": bool,
    "decided_by": str,
    "avoid": list,
    "why": str,
    "override_when": str,
    "over": list,
    "revisit_when": list,
    "decided": str,
    "checked": str,
    "history": list,
}
REQUIRED_FOR_NEW = ("layer", "title", "choices", "why", "decided", "checked")
DECISION_FIELDS = ("choices", "per_project", "decided_by", "avoid")


def today():
    return datetime.date.today().isoformat()


def fail(message):
    print(f"prefs: {message}", file=sys.stderr)
    sys.exit(2)


def load(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as error:
        fail(f"{path} is not valid JSON: {error}")


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def project_root(explicit):
    if explicit:
        return Path(explicit).resolve()
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    )
    return Path(result.stdout.strip()) if result.returncode == 0 else Path.cwd()


def base_is_checkout():
    result = subprocess.run(
        ["git", "-C", str(SKILL_DIR), "ls-files", "--error-unmatch", "data/preferences.json"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def layer_paths(args):
    return [
        ("base", BASE_FILE),
        ("global", GLOBAL_FILE),
        ("project", project_root(args.project_root) / PROJECT_RELATIVE),
    ]


def merged(args, through="project"):
    base = load(BASE_FILE)
    if base is None:
        fail(f"base data missing at {BASE_FILE}")
    result = {key: value for key, value in base.items() if key != "categories"}
    categories = {cid: dict(entry, sources=["base"]) for cid, entry in base["categories"].items()}
    for name, path in layer_paths(args)[1 : LAYERS.index(through) + 1]:
        layer = load(path)
        if not layer:
            continue
        for cid, patch in layer.get("categories", {}).items():
            entry = categories.setdefault(cid, {"sources": []})
            owns_review = "choices" in patch or patch.get("checked", "") >= entry.get("checked", "")
            for field, value in patch.items():
                if field == "checked" and not owns_review:
                    continue
                entry[field] = copy.deepcopy(value)
            entry["sources"].append(name)
    result["categories"] = categories
    return result


def known_ids(args, through):
    return set(merged(args, through)["categories"]) if through else set()


def layer_below(layer):
    index = LAYERS.index(layer)
    return LAYERS[index - 1] if index else None


def default_write_layer():
    return "base" if base_is_checkout() else "global"


def staleness(entry, days):
    age = (datetime.date.today() - datetime.date.fromisoformat(entry["checked"])).days
    reasons = []
    if age > days:
        reasons.append(f"checked {age} days ago")
    for trigger in entry.get("revisit_when", []):
        reasons.append(f"revisit when: {trigger}")
    return age, reasons


def first_choice(entry):
    choices = entry.get("choices", [])
    if entry.get("per_project"):
        names = ", ".join(choice["option"] for choice in choices) or "none"
        return f"per project ({entry.get('decided_by', '')}); candidates: {names}"
    if not choices:
        return "no choice"
    first = choices[0]
    text = first["option"]
    if first.get("when"):
        text += f" (when {first['when']})"
    if len(choices) > 1:
        text += f" +{len(choices) - 1}"
    return text


def with_status(cid, entry, days):
    age, reasons = staleness(entry, days)
    shown = dict(entry, id=cid)
    shown["stale"] = age > days
    if reasons:
        shown["check"] = reasons
    return shown


def validate_entry(cid, entry, known, layers):
    problems = []
    for field, value in entry.items():
        if field not in ENTRY_FIELDS:
            problems.append(f"{cid}: unknown field '{field}'")
        elif not isinstance(value, ENTRY_FIELDS[field]):
            problems.append(f"{cid}: '{field}' must be {ENTRY_FIELDS[field].__name__}")
    if cid not in known:
        missing = [field for field in REQUIRED_FOR_NEW if field not in entry]
        if missing:
            problems.append(f"{cid}: a new category needs {', '.join(missing)}")
    if "layer" in entry and entry["layer"] not in layers:
        problems.append(f"{cid}: layer must be one of {', '.join(layers)}")
    for choice in entry.get("choices", []):
        if not isinstance(choice, dict) or not isinstance(choice.get("option"), str):
            problems.append(f"{cid}: each choice needs an 'option' string")
        elif set(choice) - {"option", "when"}:
            problems.append(f"{cid}: a choice holds only 'option' and 'when'")
    for field in ("decided", "checked"):
        if field in entry:
            try:
                datetime.date.fromisoformat(entry[field])
            except ValueError:
                problems.append(f"{cid}: '{field}' must be YYYY-MM-DD")
    return problems


def cmd_paths(args):
    rows = {name: {"path": str(path), "exists": path.exists()} for name, path in layer_paths(args)}
    rows["base"]["maintainer_checkout"] = base_is_checkout()
    rows["overrides_log"] = {"path": str(OVERRIDES_LOG), "exists": OVERRIDES_LOG.exists()}
    rows["default_write_layer"] = default_write_layer()
    print(json.dumps(rows, indent=2))


def cmd_index(args):
    data = merged(args)
    for cid, entry in data["categories"].items():
        if args.layer and entry.get("layer") != args.layer:
            continue
        age, _ = staleness(entry, args.days)
        mark = "  [stale]" if age > args.days else ""
        print(f"{cid}\t{entry.get('layer')}\t{entry.get('title')}\t{first_choice(entry)}{mark}")


def cmd_get(args):
    data = merged(args)
    missing = [cid for cid in args.ids if cid not in data["categories"]]
    if missing:
        fail(f"no category {', '.join(missing)}; run 'index' or 'search' to find it")
    print(json.dumps([with_status(cid, data["categories"][cid], args.days) for cid in args.ids], indent=2, ensure_ascii=False))


def cmd_list(args):
    data = merged(args)
    if args.layer not in data["layers"]:
        fail(f"layer must be one of {', '.join(data['layers'])}")
    entries = [with_status(cid, entry, args.days) for cid, entry in data["categories"].items() if entry.get("layer") == args.layer]
    print(json.dumps(entries, indent=2, ensure_ascii=False))


def cmd_search(args):
    term = args.term.lower()
    for cid, entry in merged(args)["categories"].items():
        text = json.dumps(entry, ensure_ascii=False).lower()
        if term in text or term in cid:
            print(f"{cid}\t{entry.get('title')}\t{first_choice(entry)}")


def cmd_scope(args):
    data = merged(args)
    print(json.dumps({key: data[key] for key in ("scope", "layers", "out_of_scope")}, indent=2, ensure_ascii=False))


def cmd_stale(args):
    for cid, entry in merged(args)["categories"].items():
        age, reasons = staleness(entry, args.days)
        if age > args.days or (args.triggers and entry.get("revisit_when")):
            print(f"{cid}\t{entry.get('title')}\t" + "; ".join(reasons))


def cmd_validate(args):
    layer_files = {path.resolve(): name for name, path in layer_paths(args)}
    if not args.file:
        targets = [(path, known_ids(args, layer_below(name))) for name, path in layer_paths(args)]
    elif Path(args.file).resolve() in layer_files:
        # A layer file's entries extend only the layers below it.
        targets = [(Path(args.file), known_ids(args, layer_below(layer_files[Path(args.file).resolve()])))]
    else:
        # Any other file is a patch, extending the layer it would be applied to.
        targets = [(Path(args.file), known_ids(args, args.layer or default_write_layer()))]
    layers = list(load(BASE_FILE)["layers"])
    problems = []
    for path, known in targets:
        content = load(path)
        if content is None:
            continue
        for cid, entry in content.get("categories", {}).items():
            problems += [f"{path}: {p}" for p in validate_entry(cid, entry, known, layers)]
    for problem in problems:
        print(problem)
    if problems:
        sys.exit(1)
    print("valid")


def cmd_apply(args):
    patch = load(Path(args.file))
    if not patch or not isinstance(patch.get("categories"), dict):
        fail("the patch file needs a 'categories' object keyed by category ID")
    layer = args.layer or default_write_layer()
    target = dict(layer_paths(args))[layer]
    # Compare against the entry as it stands through the target layer, so a higher layer's
    # override neither hides nor fakes a change to this layer's decision.
    current = merged(args, layer)
    layers = list(current["layers"])
    known = set(current["categories"])
    problems = []
    for cid, entry in patch["categories"].items():
        problems += validate_entry(cid, entry, known, layers)
    if problems:
        fail("; ".join(problems))
    content = load(target) or {"schema": 1, "categories": {}}
    stamp = today()
    for cid, change in patch["categories"].items():
        before = current["categories"].get(cid, {})
        entry = content["categories"].setdefault(cid, {})
        decision_changed = any(field in change and change[field] != before.get(field) for field in DECISION_FIELDS)
        if decision_changed and before.get("choices") is not None:
            history = entry.get("history", copy.deepcopy(before.get("history", [])))
            history.append({
                "choices": before.get("choices"),
                "avoid": before.get("avoid", []),
                "why": before.get("why", ""),
                "decided": before.get("decided", ""),
                "replaced": stamp,
            })
            entry["history"] = history
        entry.update(copy.deepcopy(change))
        if "choices" in change and "checked" not in entry and "checked" in before:
            # Owning choices also owns their review date; later reviews of a lower
            # layer's different choice must not make this override look current.
            entry["checked"] = before["checked"]
        if decision_changed and "decided" not in change:
            entry["decided"] = stamp
    content["updated"] = stamp
    save(target, content)
    print(f"wrote {len(patch['categories'])} categories to the {layer} layer: {target}")


def cmd_override(args):
    if args.id not in merged(args)["categories"]:
        fail(f"no category {args.id}")
    record = {"date": today(), "category": args.id, "project": args.project, "reason": args.reason}
    OVERRIDES_LOG.parent.mkdir(parents=True, exist_ok=True)
    with OVERRIDES_LOG.open("a") as log:
        log.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"logged: {args.id} set aside in {args.project}")


def cmd_overrides(args):
    if not OVERRIDES_LOG.exists():
        print("no overrides logged")
        return
    records = [json.loads(line) for line in OVERRIDES_LOG.read_text().splitlines() if line.strip()]
    counts = {}
    for record in records:
        if args.id and record["category"] != args.id:
            continue
        counts.setdefault(record["category"], []).append(record)
    for cid, items in sorted(counts.items(), key=lambda kv: -len(kv[1])):
        projects = sorted({item["project"] for item in items})
        print(f"{cid}\t{len(items)} overrides in {len(projects)} projects: {', '.join(projects)}")
        if args.id:
            for item in items:
                print(f"  {item['date']}\t{item['project']}\t{item['reason']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", help="project whose .agents/stack-preferences layer applies (default: the git root of the current directory)")
    parser.add_argument("--days", type=int, default=STALE_DAYS, help=f"age after which an entry is stale (default {STALE_DAYS})")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("paths", help="show each layer's file and the default write layer").set_defaults(run=cmd_paths)
    p = sub.add_parser("index", help="one line per category with its first choice")
    p.add_argument("--layer")
    p.set_defaults(run=cmd_index)
    p = sub.add_parser("get", help="full entries for categories, as JSON")
    p.add_argument("ids", nargs="+")
    p.set_defaults(run=cmd_get)
    p = sub.add_parser("list", help="full entries for one layer, as JSON")
    p.add_argument("--layer", required=True)
    p.set_defaults(run=cmd_list)
    p = sub.add_parser("search", help="categories that mention a term")
    p.add_argument("term")
    p.set_defaults(run=cmd_search)
    sub.add_parser("scope", help="languages covered, layers, and what is out of scope").set_defaults(run=cmd_scope)
    p = sub.add_parser("stale", help="entries due for a check")
    p.add_argument("--triggers", action="store_true", help="also list entries with revisit triggers")
    p.set_defaults(run=cmd_stale)
    p = sub.add_parser("validate", help="check a layer file or patch file, or every layer")
    p.add_argument("file", nargs="?")
    p.add_argument("--layer", choices=LAYERS, help="the layer a patch file is for (default: the layer apply writes to)")
    p.set_defaults(run=cmd_validate)
    p = sub.add_parser("apply", help="write changed entries from a patch file to a layer")
    p.add_argument("file")
    p.add_argument("--layer", choices=LAYERS)
    p.set_defaults(run=cmd_apply)
    p = sub.add_parser("override", help="log a project setting a preference aside")
    p.add_argument("id")
    p.add_argument("--project", required=True)
    p.add_argument("--reason", required=True)
    p.set_defaults(run=cmd_override)
    p = sub.add_parser("overrides", help="logged overrides, most frequent first")
    p.add_argument("id", nargs="?")
    p.set_defaults(run=cmd_overrides)

    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
