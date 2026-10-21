# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Scan source(s) for brand style candidates -> JSON inventory (the codify path).

Walks files and extracts colors, CSS custom properties, font families, @font-face
sources, border-radius and box-shadow values, plus font/image asset paths, with
frequency counts. Emits JSON the agent curates into the token layer. Deterministic,
stdlib-only.

Usage:
  uv run extract-style-candidates.py PATH [PATH ...] [--out candidates.json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

TEXT_EXT = {".css", ".scss", ".sass", ".less", ".html", ".htm", ".js", ".jsx",
            ".ts", ".tsx", ".vue", ".svelte", ".md", ".json"}
FONT_EXT = {".woff2", ".woff", ".ttf", ".otf", ".eot"}
ASSET_EXT = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "out",
             "coverage", ".vera", ".extern", ".cache"}

HEX = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
FUNCCOL = re.compile(r"\b(?:rgb|rgba|hsl|hsla|oklch|oklab|lab|lch)\([^)]*\)")
VAR = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]+)")
FONTFAM = re.compile(r"font-family\s*:\s*([^;{}]+)")
FONTFACE_SRC = re.compile(r"@font-face[^}]*?src\s*:\s*([^;}]+)", re.IGNORECASE | re.DOTALL)
RADIUS = re.compile(r"border-radius\s*:\s*([^;{}]+)")
SHADOW = re.compile(r"box-shadow\s*:\s*([^;{}]+)")


def iter_files(root: Path):
    if root.is_file():
        yield root
        return
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        # Skip only on components BELOW the scan root (so a scan root that itself
        # sits under e.g. .vera/ is not wrongly excluded by its own ancestors).
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        yield p


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out")
    ap.add_argument("--max-bytes", type=int, default=2_000_000)
    args = ap.parse_args()

    colors: Counter = Counter()
    props: dict[str, Counter] = {}
    fams: Counter = Counter()
    faces: Counter = Counter()
    radii: Counter = Counter()
    shadows: Counter = Counter()
    font_files: set[str] = set()
    assets: set[str] = set()

    for raw in args.paths:
        root = Path(raw).resolve()
        if not root.exists():
            print(f"warning: path not found: {root}", file=sys.stderr)
            continue
        for p in iter_files(root):
            ext = p.suffix.lower()
            if ext in FONT_EXT:
                font_files.add(str(p))
                continue
            if ext in ASSET_EXT:
                assets.add(str(p))
                continue
            if ext not in TEXT_EXT:
                continue
            try:
                if p.stat().st_size > args.max_bytes:
                    continue
                t = p.read_text(errors="ignore")
            except Exception:
                continue
            for m in HEX.findall(t):
                colors[m.lower()] += 1
            for m in FUNCCOL.findall(t):
                colors[re.sub(r"\s+", "", m.lower())] += 1
            for name, val in VAR.findall(t):
                props.setdefault(name, Counter())[val.strip()] += 1
            for m in FONTFAM.findall(t):
                fams[m.strip().strip("\"'")] += 1
            for m in FONTFACE_SRC.findall(t):
                faces[m.strip()[:200]] += 1
            for m in RADIUS.findall(t):
                radii[m.strip()] += 1
            for m in SHADOW.findall(t):
                shadows[m.strip()[:200]] += 1

    def top(c: Counter, n: int = 40):
        return [{"value": k, "count": v} for k, v in c.most_common(n)]

    out = {
        "colors": top(colors),
        "custom_properties": [
            {"name": k, "values": [{"value": vv, "count": cc} for vv, cc in v.most_common(3)]}
            for k, v in sorted(props.items())
        ],
        "font_families": top(fams),
        "font_face_src": top(faces, 20),
        "radii": top(radii, 20),
        "shadows": top(shadows, 20),
        "font_files": sorted(font_files),
        "image_assets": sorted(assets)[:200],
    }

    s = json.dumps(out, indent=2)
    if args.out:
        Path(args.out).write_text(s)
        print(f"wrote {args.out}")
    else:
        print(s)


if __name__ == "__main__":
    main()
