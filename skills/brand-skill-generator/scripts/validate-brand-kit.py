# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Check a brand kit's structural integrity, not its design quality or approval.

Usage: uv run validate-brand-kit.py [--draft] KIT
Checks metadata, shared operating blocks, required files, authoring placeholders,
local links and resources, CSS import closure, and SVG structure. The human overview (index.html) is required,
but its layout and content quality are evaluated through visual review.
--draft reports unfinished content as warnings; broken references remain errors.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

import yaml

FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.S)
IMPORT = re.compile(r'''@import\s+(?:url\(\s*)?(?:"([^"]+)"|'([^']+)'|([^\s;)]+))\s*\)?[^;]*;''', re.I)
URL = re.compile(r'''url\(\s*(?:"([^"]+)"|'([^']+)'|([^)]*?))\s*\)''', re.I)
PLACEHOLDER = re.compile(r"\bREPLACE(?:\s*[:.\u2014-]|\s+with\b)|\{\{(?:brand|slug)\}\}|SLOT — replace|RULE — replace")
SHARED_BLOCKS = ("apply", "verify", "evolve")
SKILL_TEMPLATE = Path(__file__).resolve().parents[1] / "assets/brand-kit-template/SKILL.template.md"


def without_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


class ResourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.resources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag in {"img", "script", "source", "video", "audio", "iframe"} and data.get("src"):
            self.resources.append(data["src"])
        if tag == "link" and data.get("href"):
            self.resources.append(data["href"])
        if tag == "video" and data.get("poster"):
            self.resources.append(data["poster"])
        if tag in {"use", "image"}:
            for key in ("href", "xlink:href"):
                if data.get(key):
                    self.resources.append(data[key])


def validate(kit: Path, draft: bool = False) -> tuple[list[str], list[str]]:
    kit = kit.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    unfinished = warnings if draft else errors
    if not kit.is_dir():
        return [f"not a directory: {kit}"], warnings

    def label(path: Path) -> str:
        return str(path.relative_to(kit)) if path.is_relative_to(kit) else str(path)

    def local_target(source: Path, ref: str, allow_directory: bool = False) -> Path | None:
        parts = urlsplit(ref.strip())
        if parts.scheme == "file":
            if parts.netloc not in {"", "localhost"}:
                warnings.append(f"{label(source)}: cannot check file URL on another host: {ref}")
                return None
        elif parts.scheme or parts.netloc:
            return None
        if not parts.path:
            return None
        path = Path(unquote(parts.path))
        target = (source.parent / path).resolve()
        if not (target.exists() if allow_directory else target.is_file()):
            findings = unfinished if target == kit / "index.html" else errors
            findings.append(f"{label(source)}: missing local resource {ref}")
            return None
        return target

    for name in ("SKILL.md", "readme.md", "brand-card.md", "styles.css"):
        if not (kit / name).is_file():
            errors.append(f"{name}: required file missing")
    index = kit / "index.html"
    if not index.is_file() or not index.read_text().strip():
        unfinished.append("index.html: brand overview missing or empty; author it with visualize-html")
    skill = kit / "SKILL.md"
    if skill.is_file():
        skill_text = skill.read_text()
        match = FRONTMATTER.match(skill_text)
        if not match:
            errors.append("SKILL.md: YAML frontmatter missing")
        else:
            try:
                metadata = yaml.safe_load(match.group(1))
            except yaml.YAMLError as exc:
                errors.append(f"SKILL.md: invalid YAML: {exc}")
                metadata = None
            if not isinstance(metadata, dict):
                errors.append("SKILL.md: frontmatter must be a mapping")
            else:
                for field in ("name", "description"):
                    value = metadata.get(field)
                    if not isinstance(value, str) or not value.strip():
                        errors.append(f"SKILL.md: {field} must be a nonempty string")
                name = metadata.get("name")
                if isinstance(name, str) and name:
                    if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                        errors.append("SKILL.md: name must be hyphenated lowercase letters/digits, at most 64 characters")
                    if not name.endswith("-brand"):
                        warnings.append("SKILL.md: new kits conventionally use the -brand suffix; preserve deliberate legacy names")
                    if kit.name != name:
                        warnings.append(f"directory name {kit.name!r} differs from skill name {name!r}")

        # These blocks are an output contract: every generated skill carries the
        # same operating guidance. Brand-specific content surrounds them.
        try:
            template_text = SKILL_TEMPLATE.read_text()
        except OSError as exc:
            errors.append(f"validator cannot read its shared operating template: {exc}")
        else:
            for block in SHARED_BLOCKS:
                begin = f"<!-- brand-skill:{block}:begin -->"
                end = f"<!-- brand-skill:{block}:end -->"
                pattern = re.compile(re.escape(begin) + r"(.*?)" + re.escape(end), re.S)
                expected = pattern.findall(template_text)
                if len(expected) != 1:
                    errors.append(f"validator template: expected one shared {block} block")
                    continue
                actual = pattern.findall(skill_text)
                if skill_text.count(begin) != 1 or skill_text.count(end) != 1 or len(actual) != 1:
                    unfinished.append(f"SKILL.md: include exactly one shared {block} block with its markers from the template")
                elif actual[0].strip() != expected[0].strip():
                    unfinished.append(f"SKILL.md: shared {block} block changed; preserve its template text and specialize the surrounding guidance")

    for path in kit.rglob("*"):
        if path.is_symlink() and not path.exists():
            errors.append(f"{label(path)}: broken symlink")

    token_files = set((kit / "tokens").rglob("*.css"))
    if not token_files:
        errors.append("tokens/: no CSS token files")
    visited: set[Path] = set()

    def walk_css(path: Path, active: set[Path]) -> None:
        if path in active:
            errors.append(f"{label(path)}: circular CSS import")
            return
        if path in visited:
            return
        visited.add(path)
        css = without_comments(path.read_text())
        imports = list(IMPORT.finditer(css))
        if path == kit / "styles.css":
            residue = IMPORT.sub("", css)
            residue = re.sub(r"@charset\s+[^;]+;", "", residue, flags=re.I).strip()
            if residue:
                errors.append("styles.css: keep the entrypoint import-only; put declarations in token files")
        for match in imports:
            ref = next(value for value in match.groups() if value is not None)
            target = local_target(path, ref)
            if target and target.suffix == ".css":
                walk_css(target, active | {path})
        for match in URL.finditer(IMPORT.sub("", css)):
            ref = next(value for value in match.groups() if value is not None)
            local_target(path, ref)

    if (kit / "styles.css").is_file():
        walk_css(kit / "styles.css", set())
    for path in sorted(token_files - visited):
        errors.append(f"{label(path)}: unreachable from styles.css")

    text_files = [p for p in kit.rglob("*") if p.is_file() and p.suffix in {".md", ".css", ".html", ".svg"}]
    for path in sorted(text_files):
        text = path.read_text()
        if PLACEHOLDER.search(text):
            unfinished.append(f"{label(path)}: unfinished authoring placeholder")
        if path.suffix == ".md":
            prose = re.sub(r"```.*?```", "", text, flags=re.S)
            for ref in re.findall(r"\[[^\]]*\]\(([^)]+)\)", prose):
                local_target(path, ref.strip("<>"), allow_directory=True)
        if path.suffix == ".html":
            parser = ResourceParser()
            parser.feed(text)
            for ref in parser.resources:
                local_target(path, ref)
            for match in URL.finditer(without_comments(text)):
                ref = next(value for value in match.groups() if value is not None)
                local_target(path, ref)
        if path.suffix == ".svg":
            try:
                root = ET.fromstring(text)
            except ET.ParseError as exc:
                errors.append(f"{label(path)}: invalid SVG XML: {exc}")
                continue
            if root.tag != "{http://www.w3.org/2000/svg}svg":
                errors.append(f"{label(path)}: standalone SVG root must use the SVG namespace")
            try:
                bounds = [float(v) for v in re.split(r"[\s,]+", root.attrib.get("viewBox", "").strip())]
                valid_bounds = len(bounds) == 4 and all(math.isfinite(v) for v in bounds) and bounds[2] > 0 and bounds[3] > 0
            except ValueError:
                valid_bounds = False
            if not valid_bounds:
                errors.append(f"{label(path)}: viewBox must have four finite values and positive width/height")
            ids = {element.attrib["id"] for element in root.iter() if "id" in element.attrib}
            for element in root.iter():
                if element.tag == "{http://www.w3.org/2000/svg}image":
                    warnings.append(f"{label(path)}: image content needs a separate vector-portability review")
                for key, value in element.attrib.items():
                    if key in {"href", "{http://www.w3.org/1999/xlink}href"}:
                        if value.startswith("#") and value[1:] not in ids:
                            errors.append(f"{label(path)}: unresolved SVG ID {value}")
                        else:
                            local_target(path, value)
                    for ref in re.findall(r"url\(['\"]?#([^)'\"]+)['\"]?\)", value):
                        if ref not in ids:
                            errors.append(f"{label(path)}: unresolved SVG ID #{ref}")

    pantone = kit / "pantone.json"
    if not pantone.is_file():
        warnings.append("pantone.json: match evidence missing; run the Pantone CLI pass or document why matching remains incomplete")
    else:
        try:
            data = json.loads(pantone.read_text())
            if not isinstance(data, dict) or not data:
                errors.append("pantone.json: expected a nonempty match record")
            elif "scales" in data:
                scales = data["scales"]
                if not isinstance(scales, dict) or not scales:
                    errors.append("pantone.json: no mapped scales")
                else:
                    for name, scale in scales.items():
                        levels = scale.get("levels", {}) if isinstance(scale, dict) else {}
                        if not isinstance(levels, dict) or not levels or any(not isinstance(level, dict) or not level.get("matches") for level in levels.values()):
                            warnings.append(f"pantone.json: incomplete matches for {name}")
        except (ValueError, OSError) as exc:
            errors.append(f"pantone.json: invalid match record: {exc}")
    return list(dict.fromkeys(errors)), list(dict.fromkeys(warnings))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kit", type=Path)
    parser.add_argument("--draft", action="store_true")
    args = parser.parse_args()
    errors, warnings = validate(args.kit, args.draft)
    for warning in warnings:
        print(f"[!] {warning}")
    for error in errors:
        print(f"[X] {error}")
    print(f"{'FAILED' if errors else 'PASSED'} ({'draft' if args.draft else 'strict'}): {len(errors)} errors, {len(warnings)} warnings")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
