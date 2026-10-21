# Color Craft

Separate **choosing the color direction** from **generating the palette**. Use brand evidence and human feedback for the former; the bundled engine owns reproducible ramps. Better hue judgment should improve the seed, not replace deterministic generation with improvised swatches.

## Preserve established color

Identify exact brand colors, their intended roles, and any production constraints before exploring. A supplied approved palette is an identity contract. Codify its values rather than regenerating them merely to fit this kit. When it needs new ramps, generate them deterministically and preserve locked anchors: the engine may map the seed to a ramp level and adjust tones for contrast, so an input seed is not a guarantee that `primary-500` equals it.

## Choose hue through comparison

Start with the work the color must do. Consider the audience and cultural context, the category's useful recognition cues, the brand's desired personality, the physical or digital materials, and the proportion of a surface the color will occupy. “Trustworthy therefore blue” is too little evidence; an unconventional hue is not automatically more distinctive.

Build a small set of plausible directions when the choice is open. Vary the underlying rationale, not just adjacent hex values: a color grounded in the brand's material world, one that supports its intended emotional register, or one that creates a useful distinction from its category. These are possible sources of a direction, not a required set of categories.

For each direction:

- Describe the intended effect and why it fits the brief. Tie associations to the relevant context rather than claiming universal color psychology.
- Choose a seed in hue, chroma, and lightness together. Compare chroma and tone as well as hue; a quiet blue-gray and electric blue do different work.
- Generate the candidate palette with the same engine and record the seed and harmony. Keep each candidate under `<work-dir>/candidates/` in its own directory so exploration does not overwrite the accepted palette.
- Show the color in comparable real applications with the actual typography and assets. Hold composition and copy steady for a focused hue comparison. If an option needs a different area of color to work, show that use deliberately and explain the distinction.
- Inspect backgrounds, text, interactive roles where relevant, imagery, and the mark. Evaluate recognition, readability, visual temperature, distinctiveness, and reproduction limits. A pleasing swatch can still fail as a surface or text color.

Use `visualize-html` through [Visual review](visual-review.md) for the comparison. Include the rationale and practical tradeoff of each direction, then recommend the strongest fit. Honor an existing authorization to choose; otherwise resolve the material direction with the user before promoting it into the final kit. Record the chosen seed, harmony, role usage, and rationale.

## Generate the palette deterministically

Run the bundled helper for new ramps:

```sh
uv run <skill-dir>/scripts/build-palette.py --seed "#315C4C" --harmony mono --brand "Example" --out <candidate-or-kit>/tokens/colors.css --card <candidate-or-kit>/brand-card.md
```

The engine generates OKLCH tonal ramps, tinted neutrals, semantic tones, and light/dark role mappings, with its APCA adjustment pass. Given the same seed, options, and engine version, it supplies the same calculation process. Keep the seed and options with the accepted palette as provenance; consumers use its final values directly without running the generator.

- `mono`: signature hue plus tinted neutrals.
- `complement`: adds a complementary direction.
- `chord`: adds neighboring hues.

Choose harmony from the brand's needs. The engine's full output is a candidate system; it does not require every surface to use every hue or support every theme. Keep exact established anchors and intentional role overrides clearly named, and reapply them deliberately after regeneration. Do not hand-tune a long ramp into an undocumented second palette.

## Assign roles and verify

Define where the brand color appears and how much visual emphasis it carries. Marketing, product UI, packaging, and print may use different emphasis while sharing the identity. Decide light, dark, or user-controlled themes from the applications; do not manufacture a scene that forces an arbitrary theme preference.

Review the engine's adjustment warnings and the actual foreground/background combinations used by the final roles. APCA diagnostics are useful design evidence, not a substitute for an applicable accessibility standard or for checking final components. For web content targeting WCAG 2.2 AA, evaluate text against the [contrast requirements](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) and relevant non-text criteria. A logo's exception does not extend to surrounding UI or body text.

For compatibility, sRGB custom-property values must remain available outside the `@supports` block that enables OKLCH. Repeating a hex variable followed by an unsupported color function does not supply a computed-value fallback; see [CSS custom-property invalid values](https://www.w3.org/TR/css-variables-1/#invalid-variables). The helper handles the palette's guarded output. Check any hand-authored additions too.

## Pantone mapping and print decisions

Use print requirements early in hue selection when packaging, signage, or merchandise matters. An online-first identity and a print-critical identity may make different compromises. A separate approved print anchor can be more appropriate than changing the digital color.

Run `uv run <skill-dir>/scripts/build-pantone.py --kit <kit-dir>` after generating the selected palette. Keep `pantone-cli` and its color index as the print-matching dependency; the helper compares the generated ramp values through that CLI. When print fidelity may decide between finalists, run the mapping before choosing as well. The helper writes `pantone.json` and the marked print block in the brand card; keep the print decision outside that generated block. For codified colors outside the helper's ramp format, use the same CLI directly and retain its evidence in `pantone.json`, with corresponding production notes in the card. Use `--help` for books and anchors. Exit 2 means the dependency or index is unavailable; continue independent work and record that matching remains incomplete.

The pass informs both digital-first and print-critical brands: a distant match can be an acceptable documented tradeoff rather than a reason to discard the hue. Treat computed matches as approximations tied to the specified book and substrate, not verified ink recipes. Record the chosen production treatment and use physical proofs or the appropriate production reference when fidelity is critical. Do not invent Pantone codes. If matching is unavailable, mark the mapping incomplete rather than claiming a match or silently dropping the dependency.

The helper replaces the mapping only when every scanned ramp level has a match in each requested book. If matching fails, retained output files are previous evidence, not proof for a changed palette; resolve or report the incomplete pass before using its results as current.
