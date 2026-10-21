# Icon Design Principles

## Library conventions

Match the target library's source assets and contribution rules: viewBox, live area, fill or stroke treatment, weight, caps, joins, corner treatment, and supported sizes. Variants within a library can use different geometry. Source conventions from the actual target rather than a generic library comparison.

## Pixel-Perfect Alignment

Icons at small sizes (16-24px) render on actual device pixels. Misalignment causes blurry edges.

### Rules for sharp rendering

At a scale of one user unit per device pixel, align the edges of horizontal and vertical strokes to pixel boundaries. Even integer stroke widths usually need integer centers; odd widths usually need half-pixel centers. Curves, diagonals, fractional strokes, display scaling, and device pixel ratio still require visual inspection. Do not snap every path coordinate indiscriminately.

### Stroke alignment cheat sheet

| Stroke width | Position line center at | Why |
|-------------|------------------------|-----|
| 1 | x.5 (half pixel) | 0.5 + 0.5 = fills exactly 1 pixel |
| 1.5 | Inspect at target scale | Both edges cannot align to whole pixels at 1× |
| 2 | integer | 1 + 1 = fills exactly 2 pixels |
| 3 | x.5 (half pixel) | 1.5 + 1.5 = fills exactly 3 pixels |

## Consistent Stroke Weights

Keep stroke weight consistent within each weight and size variant of a set. Introduce contrast deliberately, and compare apparent weight as well as numeric width. For filled icons, inspect the thickness of stems and gaps; their contours carry the weight that a stroke attribute would otherwise control.

## Optical Balance and Visual Weight

Not all shapes have equal visual weight at the same physical size. Compensate:

| Shape | Adjustment needed |
|-------|------------------|
| Circle | Slightly larger than a square to look the same size |
| Triangle | Needs to be taller than a square to match visual weight |
| Horizontal line | Looks lighter than vertical line of same dimensions |
| Detailed icon | Looks heavier than simple icon at same size |

### The blur test

Squint at your icon or apply a gaussian blur. If it looks significantly darker/lighter than neighboring icons, adjust the visual weight. A set of icons should look roughly equally "dense" when blurred.

### Optical centering

Mathematical center can differ from visual center. Compare the icon with its container and neighboring icons, then adjust for perceived balance. Directional forms may need an offset, but its direction and amount depend on the geometry; avoid a fixed shift for every arrow or triangle.

## Icon Grid System

Use the existing set's keylines and padding. For a new set, the following 24×24 grid is one possible starting point:

### The 24x24 grid zones

```
+------------------------+
|  2px padding (all sides)|
|  +------------------+  |
|  |   20x20 live     |  |
|  |    area          |  |
|  |                  |  |
|  |   Content goes   |  |
|  |   here           |  |
|  +------------------+  |
+------------------------+
```

- **Trim area:** Full 24x24 canvas. Nothing should extend beyond this.
- **Live area:** 20x20 (2px padding on each side). All icon content should fit within this zone.
- **Padding:** 2px minimum on all sides. Some icons (circles, squares) may use the full live area; others should have more breathing room.

### Example keyline shapes

These are reference shapes that define the "bounding box" of different icon types:

| Shape | Dimensions (within 20x20 live area) | Use for |
|-------|-------------------------------------|---------|
| Circle | 20px diameter | Round icons (globe, user avatar) |
| Square | 18x18 | Square icons (file, card) |
| Vertical rectangle | 16x20 | Tall icons (document, phone) |
| Horizontal rectangle | 20x16 | Wide icons (landscape, video) |

Use keylines to help different-shaped icons occupy similar visual space, then check optical balance.

### Corner radius

| Element size | Corner radius |
|-------------|---------------|
| >= 8px | 2px |
| < 8px | 1px |
| Interior corners | 0px (square) |

## Lucide Element Constraints

When contributing to Lucide, check its current element restrictions and prefer bare shape/path elements with shared root styling. Apply library-specific restrictions only to assets targeting that library; other icon systems may use groups, definitions, transforms, or text.

## Naming Conventions

Follow project naming first. For a new reusable library, these conventions are useful defaults:

| Convention | Example |
|-----------|---------|
| Lowercase kebab-case | `arrow-up-right.svg` |
| Describe appearance, not function | `arrow-up` not `scroll-to-top` |
| Group variants | `chevron-left`, `chevron-right`, `chevron-up` |
| Size elements largest-to-smallest | `circle-dot` (circle is bigger than dot) |
| No numerals (unless the icon shows a number) | `calendar` not `calendar1` |
