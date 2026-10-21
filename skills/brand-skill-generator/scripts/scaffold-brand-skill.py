# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Create a brand-skill draft at an explicit destination.

Usage:
  uv run scaffold-brand-skill.py --brand "Acme" --out PATH [--slug acme] [--update]

--update adds missing files only. It does not migrate or overwrite an existing kit.
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


# The template's skill file is not named SKILL.md, so skill installers do not mistake it for an installable skill.
TEMPLATE_SKILL = "SKILL.template.md"


def destination(out: Path, template: Path, source: Path) -> Path:
    relative = source.relative_to(template)
    return out / relative.with_name("SKILL.md") if relative == Path(TEMPLATE_SKILL) else out / relative


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brand", required=True, help="single-line brand display name")
    parser.add_argument("--slug", help="lowercase hyphenated name; derived from --brand")
    parser.add_argument("--out", required=True, help="destination in the target project's skill directory")
    parser.add_argument("--template", help="custom template directory")
    parser.add_argument("--update", action="store_true", help="add missing files without overwriting")
    args = parser.parse_args()
    brand = args.brand.strip()
    if not brand or any(c in brand for c in "\r\n\x00"):
        parser.error("--brand must be a nonempty single-line name")
    slug = args.slug if args.slug is not None else slugify(brand)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or len(slug) > 57:
        parser.error("--slug must be lowercase letters/digits separated by hyphens, at most 57 characters")

    out = Path(args.out).resolve()
    template = Path(args.template).resolve() if args.template else Path(__file__).resolve().parents[1] / "assets/brand-kit-template"
    entry_names = (TEMPLATE_SKILL, "SKILL.md") if args.template else (TEMPLATE_SKILL,)
    entries = [name for name in entry_names if (template / name).is_file()]
    if len(entries) != 1:
        parser.error(f"template needs exactly one of {', '.join(entry_names)}: {template}")
    if out == template or out.is_relative_to(template) or template.is_relative_to(out):
        parser.error("output and template directories must not contain one another")
    if out.exists() and not out.is_dir():
        parser.error(f"output is not a directory: {out}")
    if out.exists() and any(out.iterdir()) and not args.update:
        parser.error(f"output is nonempty: {out}; --update adds missing files only")

    sources = [p for p in sorted(template.rglob("*")) if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]
    # Check collisions before adding anything in update mode.
    for source in sources:
        dest = destination(out, template, source)
        if dest.exists() and not dest.is_file():
            parser.error(f"expected a file at {dest}")
        for parent in dest.parents:
            if parent == out.parent:
                break
            if parent.exists() and not parent.is_dir():
                parser.error(f"expected a directory at {parent}")

    out.mkdir(parents=True, exist_ok=True)
    added = skipped = 0
    for source in sources:
        dest = destination(out, template, source)
        if dest.exists():
            skipped += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            content = source.read_text()
        except UnicodeDecodeError:
            shutil.copy2(source, dest)
        else:
            dest.write_text(content.replace("{{brand}}", brand).replace("{{slug}}", slug))
        added += 1
    (out / "assets").mkdir(exist_ok=True)
    print(f"Draft {slug}-brand: {out}\nAdded {added} files; preserved {skipped} existing files.")
    print("Complete the identity files and use visualize-html to author index.html as the human brand overview; then validate the kit.")


if __name__ == "__main__":
    main()
