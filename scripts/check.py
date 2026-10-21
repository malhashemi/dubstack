# /// script
# requires-python = ">=3.14"
# dependencies = ["pytest==9.1.1", "pyyaml==6.0.3", "coloraide==8.13.1"]
# ///
"""Check the skill library: skill metadata, links, plugin manifests, and every test suite.

Usage: mise run check (or uv run scripts/check.py)
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
PORTABLE_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^(\s*)(```|~~~)")
# These assets are copied into other places, where their links resolve: the brand kit template into
# each emitted kit, and upstream-source's instructions into a project's repos/ folder.
LINKS_RESOLVED_ELSEWHERE = [
    SKILLS / "brand-skill-generator" / "assets" / "brand-kit-template",
    SKILLS / "upstream-source" / "assets" / "repos-agents.md",
]

problems = []


def problem(path, message):
    problems.append(f"{path.relative_to(ROOT)}: {message}")


def frontmatter(path):
    text = path.read_text()
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    return yaml.safe_load(text[4:end]) if end != -1 else None


def check_skill(skill):
    entry = skill / "SKILL.md"
    if not entry.is_file():
        problem(skill, "missing SKILL.md")
        return
    meta = frontmatter(entry)
    if not isinstance(meta, dict):
        problem(entry, "frontmatter missing or not a mapping")
        return
    if meta.get("name") != skill.name or not NAME.match(skill.name) or len(skill.name) > 64:
        problem(entry, f"name must be '{skill.name}', lowercase and hyphenated, at most 64 characters")
    description = meta.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        problem(entry, "description must be a nonempty string of at most 1024 characters")
    agent = skill / "agents" / "openai.yaml"
    if not agent.is_file():
        problem(skill, "missing agents/openai.yaml")
    else:
        interface = (yaml.safe_load(agent.read_text()) or {}).get("interface", {})
        for field in ("display_name", "short_description", "default_prompt"):
            if not isinstance(interface.get(field), str) or not interface[field].strip():
                problem(agent, f"interface.{field} must be a nonempty string")
    for nested in skill.rglob("SKILL.md"):
        if nested != entry:
            problem(nested, "a nested SKILL.md is discovered as a separate skill; rename it")
    for path in skill.rglob("*"):
        if path.is_symlink():
            problem(path, "plugin directories reject symlinked components")


def check_links(path):
    if any(path.is_relative_to(base) for base in LINKS_RESOLVED_ELSEWHERE):
        return
    fence = None
    for number, line in enumerate(path.read_text().splitlines(), 1):
        opened = FENCE.match(line)
        if opened:
            fence = None if fence == opened.group(2) else fence or opened.group(2)
            continue
        if fence:
            continue
        for target in LINK.findall(re.sub(r"`[^`]*`", "", line)):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            resolved = (path.parent / target.split("#")[0]).resolve()
            if not resolved.exists():
                problem(path, f"line {number}: link target '{target}' does not exist")


def check_manifests():
    def load(relative):
        path = ROOT / relative
        try:
            return json.loads(path.read_text())
        except (OSError, json.JSONDecodeError) as error:
            problem(path, f"unreadable JSON: {error}")
            return {}

    portable = load("plugin.json")
    claude = load(".claude-plugin/plugin.json")
    marketplace = load(".claude-plugin/marketplace.json")
    release = load(".release-please-manifest.json")
    if portable.get("$schema") != PORTABLE_SCHEMA:
        problem(ROOT / "plugin.json", f"$schema must be {PORTABLE_SCHEMA}")
    name = portable.get("name")
    if not isinstance(name, str) or not NAME.match(name):
        problem(ROOT / "plugin.json", "name must be lowercase and hyphenated")
    version = portable.get("version")
    if not isinstance(version, str) or not SEMVER.match(version):
        problem(ROOT / "plugin.json", "version must be MAJOR.MINOR.PATCH")
    for label, value in (
        ("Claude manifest name", claude.get("name")),
        ("marketplace plugin name", (marketplace.get("plugins") or [{}])[0].get("name")),
    ):
        if value != name:
            problem(ROOT / ".claude-plugin", f"{label} '{value}' differs from plugin.json '{name}'")
    for label, value in (
        ("Claude manifest version", claude.get("version")),
        ("release-please version", release.get(".")),
        ("version.txt", (ROOT / "version.txt").read_text().strip() if (ROOT / "version.txt").exists() else None),
    ):
        if value != version:
            problem(ROOT, f"{label} '{value}' differs from plugin.json version '{version}'")


def main():
    skills = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    for skill in skills:
        check_skill(skill)
    for path in sorted(SKILLS.rglob("*.md")):
        check_links(path)
    for path in sorted(ROOT.glob("*.md")):
        check_links(path)
    check_manifests()
    for path in sorted(SKILLS.rglob("*.json")):
        try:
            json.loads(path.read_text())
        except json.JSONDecodeError as error:
            problem(path, f"invalid JSON: {error}")
    preferences = subprocess.run(
        [sys.executable, str(SKILLS / "stack-preferences" / "scripts" / "prefs.py"), "validate", str(SKILLS / "stack-preferences" / "data" / "preferences.json")],
        capture_output=True,
        text=True,
    )
    if preferences.returncode != 0:
        problems.append(f"stack-preferences base data: {preferences.stdout.strip() or preferences.stderr.strip()}")

    for line in problems:
        print(line)
    print(f"{len(skills)} skills checked; {len(problems)} problems")
    tests = pytest.main(["-q", str(SKILLS / "babysit-pr" / "scripts"), str(SKILLS / "brand-skill-generator" / "tests"), str(SKILLS / "stack-preferences" / "tests")])
    sys.exit(1 if problems or tests != 0 else 0)


if __name__ == "__main__":
    main()
