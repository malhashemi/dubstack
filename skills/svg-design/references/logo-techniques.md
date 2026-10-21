# Logo Design

## Direction and ideation

Use the brand, audience, intended applications, imagery, palette, and existing typography to constrain exploration. When a directional choice is missing, offer concrete alternatives grounded in the brand's domain. Reference brands can clarify an aesthetic preference; their marks are not templates to copy.

<important if="creating a set of logo concepts">
Explore distinct meanings and structures before refining layouts. A useful set gives the user materially different directions to choose from; recolors and rearrangements of one symbol are refinements of that concept. Honor the requested number and kind of options.

Start from objects, tools, actions, or forms specific to the product's world. For a bakery, dough scoring, oven arches, and braided loaves offer more specific material than a generic badge. Push promising imagery from literal depiction toward abstraction or a second meaning when that improves distinctiveness.

Use the following categories to broaden an open brief, not as a quota that overrides an agreed direction:

| Approach | Design opportunity |
|---|---|
| Wordmark | Character through lettering, rhythm, ligatures, or spacing |
| Symbolic mark | A recognizable domain object reduced to its essential form |
| Abstract geometry | Meaning through proportion, movement, or spatial relationships |
| Letterform and metaphor | A brand initial that also depicts an idea |
| Negative space | A second reading created by the relationship between forms |

Recognizable industry motifs can communicate quickly but may be generic. Assess whether the treatment makes the mark specific to this brand. To develop a promising concept, try changing proportion, combining meanings, removing detail, or reversing figure and ground.

Present concepts through `visualize-html` as described in [Present work and collect feedback](../SKILL.md#present-work-and-collect-feedback). Make viable concepts visible as they develop when the review surface supports updates. Explain what each concept communicates so feedback can distinguish meaning from execution.
</important>

## Typography

Inspect supplied typefaces, font files, weights, casing, tracking, and display roles before proposing a wordmark or letterform concept.

- Use established brand typography or derive custom letterforms from it deliberately. Identify a proposed departure explicitly.
- When no typography exists, explore type as part of the logo direction and identify the chosen typeface or custom construction.
- During iteration, `<text>` can use an available font. For a distributed wordmark that must render without that font, convert the accepted lettering to paths and retain editable source and font provenance, including relevant licensing information.
- Keep text as text when it is dynamic, searchable, or supported by a guaranteed font environment. Outlining trades editability, text semantics, and file size for rendering portability.

## Scalability and composition

Judge complexity against the intended applications. A symbol used as a favicon needs a recognizable silhouette at that size; a full wordmark need not fit a square favicon. Provide a simplified mark or alternate lockup when the brief calls for both.

Use consistent visual weight, deliberate spacing, and a palette that supports recognition. Check a monochrome treatment when single-color reproduction is required or when it helps expose dependence on decorative effects. Fine gaps, thin strokes, and intricate overlaps need particular attention at the smallest target size.

For stacked or layered compositions, budget the occupied height, gaps, and padding before drawing. Include stroke extents and retain the brand's clear space. Coordinates inside the canvas alone do not prove the rendered artwork fits.

### Negative space

For a contained hole, `fill-rule="evenodd"` avoids dependence on subpath winding direction:

```xml
<!-- Circle with a contained square cutout -->
<path fill-rule="evenodd" fill="currentColor" d="
  M 12 2 A 10 10 0 1 1 12 22 A 10 10 0 1 1 12 2 Z
  M 8 8 h 8 v 8 h -8 Z
" />
```

With the default `nonzero` fill rule, the inner contour must wind opposite the outer contour to form a hole. `evenodd` is parity-based: a cutting shape that extends outside the outer contour can add filled regions there. Use a mask or a calculated boolean difference for general subtraction.

In a clipping path, set `clip-rule` on the geometry inside `<clipPath>`:

```xml
<defs>
  <clipPath id="badge-cutout">
    <path clip-rule="evenodd"
      d="M 0 0 h 24 v 24 h -24 Z M 8 8 h 8 v 8 h -8 Z" />
  </clipPath>
</defs>
<circle cx="12" cy="12" r="10" clip-path="url(#badge-cutout)" />
```

This distinction follows the [SVG clipping rule](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/clip-rule).

For luminance masks, white reveals and black conceals. Set the mask type explicitly when the construction relies on luminance:

```xml
<defs>
  <mask id="badge-knockout" mask-type="luminance">
    <rect width="24" height="24" fill="white" />
    <rect x="8" y="8" width="8" height="8" fill="black" />
  </mask>
</defs>
<circle cx="12" cy="12" r="10" mask="url(#badge-knockout)" />
```

### Symmetry and depth

Mirroring and rotation can keep repeated geometry consistent. Use transforms during construction where useful, then retain or flatten them according to the delivery requirements.

Isometric forms can suggest depth through three faces with distinct lightness. For example:

```xml
<!-- Example on a 32×32 canvas; palette is illustrative -->
<path d="M 16 4 L 28 11 L 16 18 L 4 11 Z" fill="#38BDF8" />
<path d="M 4 11 L 16 18 L 16 28 L 4 21 Z" fill="#2563EB" />
<path d="M 16 18 L 28 11 L 28 21 L 16 28 Z" fill="#1E3A5F" />
```

Choose lighting and color from the design direction. Check that faces remain distinguishable at the target size and background.

## Background variants

Check the mark against each required background. Reuse the same file when it already works; create an alternate palette or reversed version when contrast or brand rules require it. Dark outlines can disappear on dark backgrounds even when colored fills remain visible. Adapt the affected colors within the brand palette, then inspect the whole mark again.

An inline monochrome mark can follow the host's `color` through `currentColor`. External SVG images need their own paint values. A filter that turns all artwork white can preview a reversed silhouette, but it discards a multicolor palette.

Name separate files consistently with the project, such as `logo.svg` and `logo-dark.svg`. When supplying assets to `visualize-html`, identify which file belongs on each background so the presentation uses the intended artwork.
