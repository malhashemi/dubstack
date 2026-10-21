# SVG Editing Workflow

## Mirroring

Reflect around the canvas center, accounting for a nonzero viewBox origin. For `viewBox="minX minY width height"`, a horizontal reflection maps `x` to `2 * minX + width - x`; the vertical equivalent maps `y` to `2 * minY + height - y`.

```xml
<!-- Horizontal flip for viewBox="0 0 24 24" -->
<g transform="translate(24 0) scale(-1 1)">...</g>

<!-- Vertical flip for the same viewBox -->
<g transform="translate(0 24) scale(1 -1)">...</g>
```

Keep text or other directional content outside the reflected group unless it should also be mirrored.

## Combining assets

Map each source canvas into the destination coordinate system. Preserve needed definitions and inherited styles; prefix colliding IDs and update all their references. Check CSS selectors as well as `href` and `url(#...)` references. Combining files can change paint inheritance even when path data stays identical.

```xml
<!-- Place a 24×24 symbol in a 32×32 area beside a wordmark -->
<svg viewBox="0 0 200 40" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(4 4) scale(1.333333)">
    <!-- source symbol geometry and its required paint attributes -->
  </g>
  <!-- Iteration text; outline for font-independent logo delivery -->
  <text x="44" y="28" font-family="Inter" font-size="20"
        font-weight="700" fill="currentColor">BrandName</text>
</svg>
```

## Boolean geometry

Compound paths can reproduce some filled appearances without calculating new contours. They are not a general substitute for boolean geometry, especially for stroked outlines.

| Desired result | Construction | Caveat |
|---|---|---|
| Filled union | Same-winding subpaths with `fill-rule="nonzero"` | Strokes still trace each subpath; calculate a union for a single outer contour |
| Contained hole | Nested subpaths with `fill-rule="evenodd"`, or opposite winding with `nonzero` | `evenodd` behaves as XOR when the cutter extends outside the outer shape |
| General subtraction | A luminance mask that reveals the base and conceals the cutter, or a calculated path difference | Choose actual geometry when the consumer requires paths |
| Intersection | Clip one shape with the other | This changes visible paint, not the underlying path data |
| Exclusion / XOR | Subpaths with `fill-rule="evenodd"` | Regions covered an even number of times become unfilled |

For an intersection:

```xml
<defs>
  <clipPath id="intersection-circle">
    <circle cx="14" cy="12" r="8" />
  </clipPath>
</defs>
<circle cx="10" cy="12" r="8" clip-path="url(#intersection-circle)" />
```

When baking transforms, preserve the visible stroke weight as well as coordinates. Nonuniform scaling, strokes, masks, and filters can make flattening more than a path-data conversion. Verify the rendered result before discarding the original structure.
