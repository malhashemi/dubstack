# /// script
# requires-python = ">=3.11"
# dependencies = ["coloraide"]
# ///
"""Map the brand palette to Pantone equivalents for print — via pantone-cli.

Scans ramp levels in tokens/colors.css against Pantone books. The report
includes the digital anchor and closest matches at other levels so the user
can choose a print treatment without automatically changing the digital hue.

Outputs:
  - {kit}/pantone.json          match evidence for review and future applications
  - {kit}/brand-card.md         regenerated <!-- pantone:begin/end --> block
  - stdout                      the posture-framed report with dE00 flags

Requires pantone-cli (npm) + its offline index. Degrades gracefully: if the
CLI or index is missing, prints the one-time setup instruction and exits 2 —
the workflow proceeds without print mapping, flagged as a caveat.

Matching uses CIEDE2000 against offline Lab values — an approximation, NOT a
substitute for Pantone Connect or physical guides. Verify production-critical
color against a physical guide.

Usage:
  uv run build-pantone.py --kit DIR [--books id,id] [--anchors primary-500,neutral-900]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from color_utils import hex_from_rgb01, oklch_to_srgb  # noqa: E402

DEFAULT_BOOKS = "pantoneSolidCoated,pantoneSolidUncoated"
RAMP_RE = re.compile(r"--color-([a-z][a-z-]*?)-(\d{2,3})\s*:\s*([^;]+);")
OKLCH_RE = re.compile(r"oklch\(\s*([\d.]+)(%?)\s+([\d.]+)\s+([\d.]+)")
HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b")
SKIP_SCALES = {"success", "warning", "danger", "info"}
CARD_BEGIN = "<!-- pantone:begin -->"
CARD_END = "<!-- pantone:end -->"
DISCLAIMER = (
    "Matched with CIEDE2000 against an offline index (pantone-cli) — an "
    "approximation, not Pantone Connect or a physical guide. Verify "
    "production-critical color against a physical guide."
)


def classify(de: float) -> str:
    if de < 1:
        return "imperceptible"
    if de < 2:
        return "close (visible on inspection)"
    if de < 4:
        return "noticeable"
    if de < 10:
        return "clearly different"
    return "no good match"


def css_value_to_hex(value: str) -> str | None:
    m = OKLCH_RE.search(value)
    if m:
        L = float(m.group(1)) / (100 if m.group(2) else 1)
        r, g, b, _ = oklch_to_srgb(L, float(m.group(3)), float(m.group(4)))
        return hex_from_rgb01(r, g, b)
    m = HEX_RE.search(value)
    return m.group(0) if m else None


def cli_cmd() -> list[str]:
    if shutil.which("pantone-cli"):
        return ["pantone-cli"]
    if shutil.which("npx"):
        return ["npx", "-y", "pantone-cli"]
    return []


def run_match(cmd: list[str], hexc: str, books: str, relationships: bool) -> dict | None:
    args = cmd + ["match", hexc, "--books", books, "--json"]
    if not relationships:
        args.append("--no-relationships")
    proc = subprocess.run(args, capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout).strip()
        if "index" in err.lower():
            print("Pantone index not installed. One-time setup:\n"
                  "  npx -y pantone-cli fetch-index\n"
                  "Then re-run build-pantone.py. Proceeding WITHOUT print mapping "
                  "(flag this as a caveat).", file=sys.stderr)
            sys.exit(2)
        print(f"pantone-cli failed for {hexc}: {err[:200]}", file=sys.stderr)
        return None
    return json.loads(proc.stdout)


def collect_ramps(css: str) -> dict[str, dict[int, str]]:
    ramps: dict[str, dict[int, str]] = {}
    for scale, level, value in RAMP_RE.findall(css):
        if scale in SKIP_SCALES:
            continue
        hexc = css_value_to_hex(value)
        if hexc:
            ramps.setdefault(scale, {})[int(level)] = hexc.upper()
    return ramps


def render_card_block(data: dict) -> str:
    lines = [
        "Print equivalents per ramp level (CIEDE2000; lower is closer). **Bold** =",
        "the digital anchor; ✦ = best print match in that book. Record print",
        "decisions outside this generated block so regeneration preserves them.",
        "",
    ]
    for scale, sd in data["scales"].items():
        lines.append(f"### {scale}")
        lines.append("")
        book_ids = data["book_ids"]
        header = "| Level | Hex | " + " | ".join(data["book_titles"][b] for b in book_ids) + " |"
        lines.append(header)
        lines.append("|---|---|" + "---|" * len(book_ids))
        for level in sorted(sd["levels"]):
            e = sd["levels"][level]
            cells = []
            for b in book_ids:
                m = e["matches"].get(b)
                if not m:
                    cells.append("—")
                    continue
                star = " ✦" if sd["best"].get(b, {}).get("level") == level else ""
                cells.append(f"{m['code']} `{m['hex']}` ΔE {m['deltaE']:.1f}{star}")
            lvl = f"**{level}**" if level == sd.get("anchor") else str(level)
            lines.append(f"| {lvl} | `{e['hex']}` | " + " | ".join(cells) + " |")
        anchor = sd["levels"].get(sd.get("anchor"), {})
        for b, m in anchor.get("matches", {}).items():
            shades = m.get("shades")
            if shades:
                strip = " · ".join(f"{s['code']} `{s['hex']}`" for s in shades)
                lines.append(f"\nAnchor shade strip ({data['book_titles'][b]}): {strip}")
        lines.append("")
    lines += [f"*{DISCLAIMER}*"]
    return "\n".join(lines)


def update_card(card_path: Path, block: str) -> None:
    if card_path.exists():
        text = card_path.read_text()
    else:
        text = "# Brand Card\n\n## Pantone (print)\n\n" + CARD_BEGIN + "\n" + CARD_END + "\n"
    if CARD_BEGIN in text and CARD_END in text:
        pre, _, rest = text.partition(CARD_BEGIN)
        _, _, post = rest.partition(CARD_END)
        text = pre + CARD_BEGIN + "\n" + block.strip("\n") + "\n" + CARD_END + post
    else:
        text = text.rstrip() + "\n\n## Pantone (print)\n\n" + CARD_BEGIN + "\n" + block.strip("\n") + "\n" + CARD_END + "\n"
    card_path.write_text(text)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kit", required=True, help="brand kit directory")
    ap.add_argument("--books", default=DEFAULT_BOOKS,
                    help="comma-separated pantone-cli book ids (default: coated+uncoated; "
                         "add textile/CMYK books when the brand does merch/product)")
    ap.add_argument("--anchors", default="",
                    help="comma-separated scale-level anchors to highlight "
                         "(default: <scale>-500 per chromatic scale + neutral-900)")
    args = ap.parse_args()
    requested_books = {book.strip() for book in args.books.split(",") if book.strip()}
    if not requested_books:
        ap.error("--books must name at least one Pantone book")

    kit = Path(args.kit).resolve()
    css_path = kit / "tokens" / "colors.css"
    if not css_path.exists():
        print(f"Error: {css_path} not found — run build-palette.py first", file=sys.stderr)
        sys.exit(1)

    cmd = cli_cmd()
    if not cmd:
        print("pantone-cli not available (need the npm package or npx). One-time setup:\n"
              "  npm i -g pantone-cli && pantone-cli fetch-index\n"
              "Proceeding WITHOUT print mapping (flag this as a caveat).", file=sys.stderr)
        sys.exit(2)

    ramps = collect_ramps(css_path.read_text())
    if not ramps:
        print("Error: no --color-{scale}-{level} ramps found in tokens/colors.css", file=sys.stderr)
        sys.exit(1)

    anchors: dict[str, int] = {}
    if args.anchors:
        for a in args.anchors.split(","):
            scale, _, level = a.strip().rpartition("-")
            anchors[scale] = int(level)
    for scale, levels in ramps.items():
        if scale not in anchors:
            want = 900 if scale == "neutral" else 500
            anchors[scale] = want if want in levels else sorted(levels)[len(levels) // 2]

    book_titles: dict[str, str] = {}
    incomplete: list[str] = []
    data: dict = {"generated": date.today().isoformat(),
                  "method": "CIEDE2000 via pantone-cli (offline index)",
                  "books": args.books, "scales": {}, "disclaimer": DISCLAIMER}

    for scale, levels in ramps.items():
        sd: dict = {"anchor": anchors[scale], "levels": {}, "best": {}}
        for level in sorted(levels):
            hexc = levels[level]
            want_shades = level == anchors[scale]
            res = run_match(cmd, hexc, args.books, relationships=want_shades)
            if res is None:
                incomplete.append(f"{scale}-{level}: no response")
                continue
            entry: dict = {"hex": hexc, "matches": {}}
            for r in res.get("results", []):
                bid = r["book"]["id"]
                book_titles.setdefault(bid, r["book"].get("title", bid))
                m = {"code": r["color"]["code"], "name": r["color"].get("name", ""),
                     "hex": "#" + r["color"]["hex"].lstrip("#").upper(),
                     "deltaE": round(r["deltaE"], 2),
                     "cmyk": r["color"].get("cmyk")}
                if want_shades:
                    sh = (r.get("relationships") or {}).get("shades") or {}
                    light = sh.get("lightness") or []
                    m["shades"] = [{"code": s["code"], "hex": "#" + s["hex"].lstrip("#").upper()}
                                   for s in light[:7]]
                entry["matches"][bid] = m
                best = sd["best"].get(bid)
                if best is None or m["deltaE"] < best["deltaE"]:
                    sd["best"][bid] = {"level": level, "deltaE": m["deltaE"], "code": m["code"]}
            missing_books = requested_books - entry["matches"].keys()
            if missing_books:
                incomplete.append(f"{scale}-{level}: missing books {', '.join(sorted(missing_books))}")
            sd["levels"][level] = entry
            print(f"  {scale}-{level} {hexc}  " + "  ".join(
                f"{m['code']} ΔE {m['deltaE']:.1f}" for m in entry["matches"].values()))
        data["scales"][scale] = sd

    if incomplete:
        print("Error: incomplete Pantone mapping; existing mapping and brand card were left unchanged.\n"
              + "\n".join(incomplete), file=sys.stderr)
        sys.exit(1)

    if not book_titles:
        print("Error: no Pantone matches returned; existing mapping was left unchanged.", file=sys.stderr)
        sys.exit(1)

    data["book_ids"] = sorted(book_titles)
    data["book_titles"] = book_titles

    (kit / "pantone.json").write_text(json.dumps(data, indent=2) + "\n")
    update_card(kit / "brand-card.md", render_card_block(data))

    print(f"\nWrote {kit / 'pantone.json'} and brand-card.md's Pantone block.")
    print("\nPrint match review — choose production anchors for the intended use:")
    for scale, sd in data["scales"].items():
        a = sd["levels"].get(sd["anchor"])
        if not a:
            continue
        for bid, m in a["matches"].items():
            note = classify(m["deltaE"])
            flag = "  <-- FLAG: discuss print posture" if m["deltaE"] >= 4 else ""
            print(f"  {scale}-{sd['anchor']} anchor -> {m['code']} ΔE {m['deltaE']:.1f} "
                  f"({note}) [{book_titles[bid]}]{flag}")
        for bid, b in sd["best"].items():
            if b["level"] != sd["anchor"]:
                print(f"    best in {book_titles[bid]}: {scale}-{b['level']} -> "
                      f"{b['code']} ΔE {b['deltaE']:.1f} (a different level may be the print anchor)")
    print(f"\n{DISCLAIMER}")


if __name__ == "__main__":
    main()
