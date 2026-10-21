# /// script
# requires-python = ">=3.11"
# dependencies = ["coloraide"]
# ///
"""Build tokens/colors.css from a seed color, using the vendored palette engine.

Generates OKLCH tonal ramps (50-950) with ColorBox-tinted neutrals and APCA
auto-contrast, then layers our semantic aliases (light + dark) and a conventional
semantic-tone set on top. This is the generation-time color tool: it writes the
candidate palette into tokens/colors.css for visual evaluation and role assignment.

The seed comes from comparative hue selection or an existing color. The engine
may adjust ramp tones, so preserve exact established anchors separately when
required. The helper proposes semantic aliases; inspect their final pairings.

Engine (vendored, our own): brandcolor.py + palette.py + color_utils.py (coloraide).

Usage:
  uv run build-palette.py --seed "#7C5CFF" --out tokens/colors.css [--harmony mono|complement|chord] [--brand NAME] [--card brand-card.md]
  uv run build-palette.py --seed "0.65 0.18 290" --out tokens/colors.css --harmony complement

--card regenerates the marked Colors block in brand-card.md (portable sRGB hex
for print/decks/docs) while preserving every hand-authored section.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from coloraide import Color

sys.path.insert(0, str(Path(__file__).resolve().parent))  # import the vendored siblings
from brandcolor import brand_color_from_hex  # noqa: E402
from palette import (  # noqa: E402
    LEVELS,
    auto_adjust_palette_contrast,
    format_css,
    generate_palette_from_brand_color,
    print_adjustment_report,
)
from color_utils import hex_from_rgb01, oklch_to_srgb  # noqa: E402

CARD_BEGIN = "<!-- colors:begin -->"
CARD_END = "<!-- colors:end -->"

# Semantic aliases → ramp levels. "ACCENT" resolves to complement (if present) else primary.
SEMANTIC_LIGHT = {
    "background": "neutral-50", "foreground": "neutral-900",
    "card": "neutral-100", "card-foreground": "neutral-900",
    "popover": "neutral-50", "popover-foreground": "neutral-900",
    "muted": "neutral-100", "muted-foreground": "neutral-500",
    "primary": "primary-500", "primary-foreground": "neutral-50",
    "accent": "ACCENT-500", "accent-foreground": "neutral-50",
    "border": "neutral-200", "input": "neutral-200", "ring": "primary-500",
}
SEMANTIC_DARK = {
    "background": "neutral-950", "foreground": "neutral-100",
    "card": "neutral-900", "card-foreground": "neutral-100",
    "popover": "neutral-900", "popover-foreground": "neutral-100",
    "muted": "neutral-900", "muted-foreground": "neutral-400",
    "primary": "primary-400", "primary-foreground": "neutral-950",
    "accent": "ACCENT-400", "accent-foreground": "neutral-950",
    "border": "neutral-800", "input": "neutral-800", "ring": "primary-400",
}
# Conventional semantic tones (OKLCH), brand-agnostic sensible defaults.
SEMANTIC_TONES = {
    "success": "oklch(62% 0.15 150)",
    "warning": "oklch(75% 0.15 80)",
    "danger": "oklch(58% 0.20 27)",
    "info": "oklch(62% 0.14 250)",
}


def seed_to_hex(seed: str) -> str:
    s = seed.strip()
    if s.startswith("#"):
        return s
    if re.fullmatch(r"[0-9a-fA-F]{6}", s):
        return "#" + s
    nums = re.findall(r"[-+]?\d*\.?\d+%?", s)  # oklch: "oklch(L C H)" or "L C H"
    if len(nums) >= 3:
        L = float(nums[0].rstrip("%")) / (100 if "%" in nums[0] else 1)
        C, H = float(nums[1]), float(nums[2])
        r, g, b, _ = oklch_to_srgb(L, C, H)
        return hex_from_rgb01(r, g, b)
    raise SystemExit(f"Error: could not parse --seed '{seed}' (use #hex or 'L C H' oklch)")


def render_aliases(mapping: dict, accent_scale: str, indent: str) -> str:
    out = []
    for name, ref in mapping.items():
        ref = ref.replace("ACCENT", accent_scale)
        out.append(f"{indent}--{name}: var(--color-{ref});")
    return "\n".join(out)


def resolve_hex(palette, ref: str) -> str:
    """'neutral-50' / 'analogous-warm-500' -> sRGB hex from the palette."""
    scale, _, level = ref.rpartition("-")
    color = palette.scales[scale].colors[int(level)]
    return color.hex_srgb


def render_card_block(palette, accent_scale: str, hexc: str, harmony: str) -> str:
    """Portable sRGB values; print production still needs its own mapping/proof."""
    lines = [
        f"Seed `{hexc}` · harmony `{harmony}` · sRGB hex for non-web use; the CSS",
        "tokens in `tokens/colors.css` carry the P3/OKLCH originals.",
        "",
        "### Ramps",
        "",
        "| Scale | " + " | ".join(str(l) for l in LEVELS) + " |",
        "|---" * (len(LEVELS) + 1) + "|",
    ]
    for name, scale in palette.scales.items():
        cells = " | ".join(
            f"`{scale.colors[l].hex_srgb}`" if l in scale.colors else "—" for l in LEVELS
        )
        lines.append(f"| **{name}** | {cells} |")
    lines += ["", "### Roles", "", "| Role | Light | Dark |", "|---|---|---|"]
    for role in SEMANTIC_LIGHT:
        lref = SEMANTIC_LIGHT[role].replace("ACCENT", accent_scale)
        dref = SEMANTIC_DARK[role].replace("ACCENT", accent_scale)
        lines.append(f"| {role} | `{resolve_hex(palette, lref)}` | `{resolve_hex(palette, dref)}` |")
    return "\n".join(lines)


def update_card(card_path: Path, block: str) -> None:
    """Replace ONLY the marked Colors block; hand-authored sections are preserved."""
    if card_path.exists():
        text = card_path.read_text()
    else:
        text = (
            "# Brand Card\n\nPortable brand values for surfaces where CSS doesn't"
            " reach. Complete the\nnon-color sections by hand (see the brand-kit"
            " template).\n\n## Colors\n\n" + CARD_BEGIN + "\n" + CARD_END + "\n"
        )
    if CARD_BEGIN in text and CARD_END in text:
        pre, _, rest = text.partition(CARD_BEGIN)
        _, _, post = rest.partition(CARD_END)
        text = pre + CARD_BEGIN + "\n" + block.strip("\n") + "\n" + CARD_END + post
    else:
        text = text.rstrip() + "\n\n## Colors\n\n" + CARD_BEGIN + "\n" + block.strip("\n") + "\n" + CARD_END + "\n"
    card_path.parent.mkdir(parents=True, exist_ok=True)
    card_path.write_text(text)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", required=True, help="#hex or OKLCH 'L C H'")
    ap.add_argument("--out", required=True, help="output path, e.g. tokens/colors.css")
    ap.add_argument("--harmony", choices=["mono", "complement", "chord"], default="mono")
    ap.add_argument("--brand", default="", help="brand name for the header comment")
    ap.add_argument("--card", help="brand-card.md path — regenerate its marked Colors "
                                   "block (portable sRGB hex for non-web surfaces)")
    args = ap.parse_args()

    hexc = seed_to_hex(args.seed)
    palette_set = "adjacent" if args.harmony == "chord" else "base"
    include_comp = args.harmony == "complement"

    result = brand_color_from_hex(hexc, palette_set=palette_set, include_complementary=include_comp)
    palette = generate_palette_from_brand_color(result)
    adjustments = auto_adjust_palette_contrast(palette)  # APCA, mutates in place
    # Guard modern color syntax: custom properties alone accept unknown functions.
    base_css = format_css(palette, use_oklch=True, srgb_fallback=True).rstrip()

    accent_scale = "complement" if "complement" in palette.scales else "primary"

    parts = []
    if args.brand:
        parts.append(
            f"/* {args.brand} — brand palette. Seed {hexc} ({args.harmony}). "
            f"OKLCH ramps + ColorBox tinted neutrals + APCA. Generated by build-palette.py. */\n"
        )
    parts.append(base_css)
    parts.append("\n:root {\n  /* semantic tones */")
    for name, val in SEMANTIC_TONES.items():
        fallback = Color(val).convert("srgb", fit=True).to_string(hex=True)
        parts.append(f"  --color-{name}: {fallback};")
    parts.append("}")
    parts.append("\n@supports (color: oklch(50% 0 0)) {\n  :root {")
    for name, val in SEMANTIC_TONES.items():
        parts.append(f"    --color-{name}: {val};")
    parts.append("  }\n}")
    parts.append("\n:root {\n  /* semantic aliases — light */")
    parts.append(render_aliases(SEMANTIC_LIGHT, accent_scale, "  "))
    parts.append("}")
    parts.append("\n@media (prefers-color-scheme: dark) {\n  :root {\n    /* semantic aliases — dark */")
    parts.append(render_aliases(SEMANTIC_DARK, accent_scale, "    "))
    parts.append("  }\n}")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(parts) + "\n")
    print(f"Wrote {args.out}  ({len(palette.scales)} scales, "
          f"{len(adjustments)} APCA adjustment(s), accent={accent_scale})")

    # Report unresolved engine diagnostics; they do not validate every final role.
    failed = [a for a in adjustments if not a.success]
    if failed:
        print_adjustment_report(failed, file=sys.stderr)
        pairs = ", ".join(f"{a.scale_name}-{a.level} on {a.background}" for a in failed)
        print(f"WARNING: {len(failed)} pairing(s) could not reach target "
              f"contrast — review these pairings: {pairs}")

    print("Check final semantic pairings against the application's accessibility requirements; "
          "the engine's APCA pass is not a compliance verdict.")

    if args.card:
        update_card(Path(args.card), render_card_block(palette, accent_scale, hexc, args.harmony))
        print(f"Updated {args.card} (Colors block — portable sRGB hex; complete the "
              f"non-color sections by hand)")


if __name__ == "__main__":
    main()
