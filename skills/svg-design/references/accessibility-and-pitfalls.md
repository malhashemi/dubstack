# Accessibility and Embedding

## Accessible treatment

Choose semantics from the asset's role in its host, not its appearance alone.

| Role | Treatment |
|---|---|
| Decorative inline SVG | `aria-hidden="true"`; keep it out of keyboard focus |
| Informative inline SVG | `role="img"` with an accessible name, such as a `<title>` referenced by `aria-labelledby` |
| Complex informative graphic | Add a useful description, linked with `aria-describedby`, or an adjacent text explanation |
| Icon inside a control | Name the button or link; hide a redundant decorative SVG from assistive technology |
| SVG loaded through `<img>` | Supply meaningful `alt` on the image, or `alt=""` when decorative |

Place `<title>` first for compatibility, and give referenced titles and descriptions unique IDs when multiple SVGs share a document. Outlined lettering no longer supplies text semantics; preserve the accessible name through the host or SVG labeling.

## Paint inheritance

`fill` and `stroke` inherit through SVG groups. A group with `fill="none"` is valid: children without an override have no fill, while a child with its own fill can still be painted. Inspect inherited values and CSS before diagnosing missing shapes. See the [SVG paint specification](https://www.w3.org/TR/SVG2/painting.html#FillProperty).

Inline `currentColor` assets can follow host text color. External SVG images have a separate document context, so verify their own colors and dependencies rather than relying on host CSS. Image embedding also restricts scripts and external resources; see [SVG as an image](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image).

## Sizing and bounds

A `viewBox` defines the coordinate mapping and aspect ratio, not the complete host layout. Give the SVG or its container a deliberate rendered size. For `<img>`, dimensions help reserve layout space; CSS may make the result responsive. Inspect computed dimensions when an asset disappears in flex, grid, or positioned layouts.

A stroke is normally centered on its path. A width of 2 extends one user unit on either side, with additional reach possible at caps and joins. Allow for these extents and any filter region. Check actual clipping and `overflow` behavior; expanding the canvas or adjusting geometry is usually more predictable than relying on overflow outside the allocated space.

Use `vector-effect="non-scaling-stroke"` when fixed screen-space stroke weight is intended, such as in a zoomable technical drawing. It changes how the asset behaves when scaled, so verify it in the target layout.

## Integration pitfalls

- Prefix definition IDs when inlining multiple assets, and update paint, clip, mask, and `<use>` references together.
- Prefer same-origin external sprites or inline definitions; verify the target browser and embedding mode before depending on external `<use>` resources.
- Check that fonts actually load in the delivery context. For font-independent wordmarks, follow [Logo design](logo-techniques.md#typography).
- Check required background treatments using [Logo design](logo-techniques.md#background-variants). The preview's white-silhouette fallback is not evidence that a multicolor asset works in production.
