# Logo Craft

Use `svg-design` when a new mark or a conceptual change is part of the assignment. Preserve supplied marks during codification; missing logos need not block strategy or other identity work when the user has deferred them.

## Supply the brief once

Pass the specialist the established brand name, audience, offering, positioning, personality, visual direction, domain imagery, references, and constraints. Include palette values, existing typography and font files, or an explicit statement that typography is still open. Describe the applications, required sizes and backgrounds, output paths, and which choices remain provisional.

Keep candidate SVGs under `<work-dir>/candidates/` during exploration. Specify canonical output paths in the final kit for selected assets; `assets/logo.svg` is a useful default. Request monochrome, reversed, compact, or lockup variants when their applications require them.

`svg-design` owns concept development, direct SVG construction, refinement, and SVG-specific verification. This generator owns coherence with the identity and the status of the choice. Use [Visual review](visual-review.md) to present the options through `visualize-html`; tell the specialist that this is the comparison surface so it need not build a second preview page.

If the specialist is unavailable, explain the missing capability and continue independent work. Do not represent a placeholder or an unselected candidate as the final mark.

## Integrate the selected mark

- Inspect the actual SVGs at the relevant sizes and backgrounds. A full wordmark and a favicon have different requirements; use a compact treatment where needed.
- Check the intended reproduction, including single-color use when part of the brief. Add a separate background variant only when the existing file cannot serve it.
- Preserve standalone SVG namespaces, coordinate bounds, and required resource references. Fixed dimensions are acceptable when the consumer needs them; they do not replace the viewBox.
- For font-independent distribution, outline accepted wordmark text and retain editable source and font provenance. Preserve accessible naming at its use sites.
- Record the asset paths, clear space, limits, variants, concept rationale, and any provisional choices in the guidelines and brand card.

After changes, refresh affected applications as well as isolated logo previews. A logo can pass its own checks while fitting poorly with the typography or surrounding composition.
