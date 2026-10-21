---
name: svg-design
description: Create, edit, and refine SVG logos, icons, and vector graphics as maintainable SVG code. Use for SVG design, path construction, icon systems, SVG animation, or SVG optimization, including visual comparison of design alternatives.
---

# SVG Design

Author and edit SVG markup directly so the result remains editable and renders correctly where it will be used. Let the brief and existing visual system govern the artwork; use this skill for SVG construction, refinement, and verification.

## Establish the design context

Inspect the current thread, supplied artifacts, and relevant project conventions before asking for context. Establish what the asset should communicate, its intended applications, applicable style and typography, target sizes and backgrounds, and requested deliverables. Resolve only the decisions relevant to the task.

Ask when a missing decision materially changes the design. For visual direction, offer a few concrete, domain-specific choices that the user can compare. Reuse settled decisions and proceed with reasonable defaults for incidental choices.

<important if="editing an existing SVG or extending an icon system">
Preserve its visual language and integration contracts: canvas, stroke or fill conventions, public IDs, CSS hooks, animation targets, and accessibility. Inspect how the asset is consumed before changing those contracts. A geometry or color correction does not require reopening the brand direction.
</important>

## Construct the SVG

- **Canvas and sizing.** Include a `viewBox` and, for standalone files, `xmlns="http://www.w3.org/2000/svg"`. Match the established canvas or natural aspect ratio. A 24×24 canvas is a useful fallback for a new UI icon, not a constraint on logos or illustrations. Set dimensions on the SVG or its host as the embedding context requires.
- **Geometry.** Use primitives for recognizable geometric shapes and paths for custom contours or compound shapes. Keep groups and transforms when they express useful structure; flatten or combine geometry when the consumer requires it or the result is meaningfully simpler.
- **Paint.** Choose filled or stroked construction from the visual system. Put shared paint attributes on the root or a suitable group, with deliberate child overrides. Use `currentColor` for inline assets that should inherit text color; an SVG loaded through `<img>` does not inherit the host page's `color`.
- **Bounds and weight.** Stroke widths are in user units and normally scale with the artwork. Budget space for strokes, caps, joins, filters, and intentional clear space. Judge weight and alignment at the rendered size, not just from coordinates.
- **Maintainability.** Retain IDs and structure used by callers. Use distinct IDs for definitions that may share a document. Remove unused editor data from delivery files while retaining meaningful metadata. Choose numeric precision by visible error at the required sizes, rather than a universal decimal limit.

## Read the relevant reference

Load a reference when the task reaches its branch; ordinary edits need only the guidance that applies.

| When working on… | Read |
|---|---|
| Logo concepts, wordmarks, or brand variants | [Logo design](references/logo-techniques.md) |
| Icon families, grid alignment, or optical balance | [Icon design](references/icon-design.md) |
| Arc flags or reusable path geometry | [Path patterns](references/path-patterns.md) |
| Mirroring, combining assets, or boolean geometry | [Editing workflow](references/editing-workflow.md) |
| Gradients, masks, clipping, filters, or transform choices | [Advanced techniques](references/advanced-techniques.md) |
| Motion, timing, or animated SVG integration | [Animation](references/animation.md) |
| File optimization or sprite delivery | [Optimization](references/optimization.md) |
| Embedding, accessible naming, or browser rendering issues | [Accessibility and pitfalls](references/accessibility-and-pitfalls.md) |

## Present work and collect feedback

Use `visualize-html` for visual presentations, comparisons, and user feedback. Supply the actual SVG files, stable option identifiers, concept descriptions, intended applications, relevant sizes and backgrounds, and the decision the user needs to make. This skill owns the artwork and comparison criteria; `visualize-html` owns the presentation, interaction, and feedback path. Coordinate with an existing review document when the owning workflow already provides one.

Let the presentation suit the artwork and the decision. Show symbols and wordmarks at their natural proportions and relevant sizes, using the actual background variants. Apply feedback to the SVG source files, then refresh the presentation so the user sees the current work. Distinguish tentative preferences and the agent's inspection from a user's accepted selection.

## Verify and deliver

Render the actual delivery files in the intended embedding context, or the closest available equivalent. Valid XML and a successful optimizer run do not establish visual correctness.

- Inspect the smallest required size and a larger view for legibility, optical balance, clipping, stroke quality, and typography. Check the requested backgrounds and variants; compare related icons together.
- Confirm that definitions, IDs, fonts, and external resources resolve, and that the asset has the appropriate accessible treatment. For animated assets, inspect the cycle and reduced-motion behavior.
- After optimization or structural changes, compare the rendered result and relevant behavior with the prior version. Preserve intentional differences while checking for regressions.
- Deliver the requested files or code, with links or a preview where useful. Identify material assumptions and any validation that could not be performed. Distinguish the agent's inspection from the user's design selection; presenting options does not establish approval.

Completion means the requested assets and variants are delivered, their applicable visual and integration requirements have been checked, and any remaining limitation is explicit.
