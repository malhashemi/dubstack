# Advanced SVG Techniques

## Gradients

Use gradients when they contribute to the design, and inspect them at the smallest target size. A few purposeful stops are often easier to control than a complex ramp. Provide a flat or monochrome treatment when the intended reproduction requires it.

`gradientUnits="userSpaceOnUse"` can give shapes sharing a coordinate system a continuous gradient. The default object-bounding-box mapping instead adapts the gradient to each shape's bounds. Account for transforms when deciding which behavior is intended.

## Clipping and masking

| Need | Mechanism | Decision to check |
|---|---|---|
| Geometric boundary | `<clipPath>` | Coordinate units and `clip-rule` on compound clipping geometry |
| Graded visibility or soft edges | `<mask>` | Alpha versus luminance interpretation, units, and mask region |

In a luminance mask, white reveals and black conceals; in an alpha mask, opacity controls visibility. Choose the type explicitly when the design depends on the distinction. See [Logo design](logo-techniques.md#negative-space) for contained cutouts and the limits of `evenodd` subtraction.

## Filters

Shadows and glows can support illustrations or display treatments, but they may lose clarity at small sizes and increase rendering cost. Check the filtered output at the required sizes and ensure the filter region includes the effect. For a core logo, consider whether the silhouette still communicates without the effect.

A vector duplicate may provide a simple offset shadow; a host CSS effect may suit decoration that belongs to a page rather than the asset. Choose according to the deliverable and rendering context.

## Transforms

Use SVG transforms for geometric placement and repetition when that structure remains useful. Flatten them when required by the consumer or when it materially simplifies a static asset; preserve the visible effect on strokes and definitions.

CSS `transform` takes precedence over the SVG presentation attribute on the same element. Keep independent placement and animation on separate nested elements when both are needed. For CSS transforms, set `transform-box` and `transform-origin` to the reference box and pivot the design requires; do not assume HTML defaults apply to SVG elements. See [CSS Transforms for SVG](https://www.w3.org/TR/css-transforms-1/#svg-transform).
