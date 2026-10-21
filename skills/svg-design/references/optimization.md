# SVG Optimization

Optimize for the actual delivery context: compact output, maintainable source, and preserved rendering and behavior. Element count or file size alone does not establish improvement.

## Safe simplification

Consolidate repeated paint attributes on the root or a suitable group when inheritance preserves the result. Keep groups used for transforms, shared effects, animation, events, or caller selectors. Flatten geometry when the target library requires it or the simpler structure is worth the loss of editability.

Remove unused editor data and hidden construction geometry from delivery files only after checking their purpose. Preserve required metadata, accessible names, licensing information, and content that CSS or animation reveals later. Reduce numeric precision only as far as the target sizes permit.

## SVGO

Use the project's installed version and configuration. Consult its version-matched plugin documentation rather than copying a preset blindly; defaults and plugin membership change. The [current default preset](https://svgo.dev/docs/preset-default/) is a reference, not a reason to upgrade the project.

| Area | What to preserve or check |
|---|---|
| Canvas | Retain the `viewBox` needed for scaling and aspect ratio |
| Namespace | Keep `xmlns` for standalone SVG files; inline HTML has different requirements |
| IDs | Preserve externally referenced IDs; avoid collisions when optimized files share a document |
| Groups and hidden elements | Retain animation targets, selectors, and dynamically revealed content |
| Path conversion and precision | Compare contours, strokes, small gaps, and alignment at target sizes |
| Accessibility | Retain labels and referenced title/description elements |

`cleanupIds` handles references it can see inside an asset, but cannot infer every caller's dependency. Disable it or preserve specific IDs when they form an external contract. When combining separately optimized assets, use a deliberate prefixing strategy. See [SVGO's ID guidance](https://svgo.dev/docs/plugins/cleanupIds/).

## Sprites

A sprite can share and cache symbols used together, but may send icons the page does not need. Compare it with the project's existing component or asset delivery model.

Give each symbol its intended coordinate system, preserve unique definition IDs, and verify sizing, styling, and accessible naming at the use site. Prefer same-origin external sprites and check target-browser behavior. Use `href` for modern consumers; preserve legacy compatibility only where the target requires it.
