# SVG Animation Reference

Non-obvious patterns and gotchas for animating SVG elements, especially in React/JSX projects with bundlers like Vite.

## Choose the animation mechanism

Use the project's CSS, SVG animation, or JavaScript conventions according to the properties and control needed. In component projects, shared styles can live in the existing stylesheet system. Diagnose bundler failures against the actual configuration rather than treating an isolated error as a ban on SVG `<style>`.

Rendering performance depends on the animated property, artwork, and browser; choosing CSS alone does not guarantee GPU compositing. Provide a stable reduced-motion state that preserves the graphic's meaning.

## Splitting Opacity and Transform

When opacity and transform need different easing (common for assembly-line effects), split into separate `@keyframes` and stack them on one element:

```css
.element {
  animation:
    fade 14s linear infinite,        /* opacity: clean boundaries */
    move 14s cubic-bezier(0.12, 0, 1, 1) infinite;  /* transform: accelerating */
}
```

This gives opacity and movement independent timing. The durations and easing above are illustrative; choose them for the intended effect.

## Hidden Phase Math

If a layer is active for 20% of its cycle, 80% is invisible. This ratio controls density:

- **Average visible layers in steady state** ≈ `(active% / 100) * (cycle_duration / stagger_interval)`, for evenly staggered layers filling the cycle
- For example, a 20-second cycle with a 20% visible phase and a 2-second stagger averages two visible layers
- Inspect overlap separately: timing, trajectory, and paint order all affect which layers remain visible

## Negative Delays for Instant Start

For a repeating effect that should begin in steady state, use negative delays to start each element partway through its cycle. Positive delays remain appropriate for an intentional entrance sequence:

```
negative-delay = -(cycle-duration) + positive-delay
```

## Organic Stagger and Burst Pairs

Even spacing feels mechanical. Vary gaps for organic feel: `0, 1.6, 3.5, 5.0, 6.8` instead of `0, 2, 4, 6, 8`.

**Burst pairs:** Group elements in pairs (200-500ms apart) with larger gaps (~3-3.5s) between pairs. Creates an assembly-line pulse.

For rising pairs where the leading element should occlude the trailing one, place the trailing element first in DOM order. Later SVG elements paint on top; choose order from the intended overlap rather than delay alone.

## Easing + Keyframe Interaction

Use `linear` timing when the desired motion curve is already encoded in keyframe positions. Additional easing changes the interpolation between stops and may introduce unwanted acceleration.

With only a few position keyframes, a bezier can supply the desired acceleration. Inspect the rendered movement instead of inferring an exact physical motion from the curve parameters.

## SVG-Specific Techniques

### ViewBox clipping

Check the effective viewport and `overflow` behavior throughout motion. If clipping is enabled, an element beginning at `y=13` reaches the top boundary at a translation of −13 user units. Budget for its full painted bounds and fade before clipping when a hard cut is unwanted.

### Box occlusion (emerge-from-container)

Make layers appear to rise from inside a container using SVG paint order instead of clipPath/mask:

1. Render container lid *before* animated layers (behind)
2. Render animated layers (start at positive Y, inside the box)
3. Render container walls *after* layers (on top, occluding layers while inside)

The walls naturally hide layers until they rise above the top edge. Add a subtle opacity fade-in (~200-400ms) during the emerge for a cleaner reveal. No mask/clip elements needed.

### Stagger spacing to prevent overlap

When layers share a spawn position and should appear separately, use a stagger longer than the linger duration or change the trajectory. Paint order determines occlusion, but cannot create spatial separation between coincident layers.

## SVG vs HTML Animation Differences

These are critical differences that will silently break your animations if you assume SVG elements behave like HTML elements.

### Group clipping

For a clipping region defined in SVG coordinates, use `<clipPath>` with explicit geometry and units. When using CSS basic shapes, verify the reference box and percentage resolution on the target elements and browsers.

### CSS `transform` conflicts with SVG `transform` attribute

An SVG element with `<g transform="translate(100,50)">` cannot have an independent CSS `transform: scale(0.5)` animation. CSS `transform` and SVG `transform` occupy the same property slot. The CSS value replaces the SVG attribute, displacing the element entirely.

Keep static placement on an outer group and animate a child or inner group, or compose placement and motion into a single transform. Set `transform-box` and `transform-origin` deliberately for CSS rotation or scaling. See the [transform presentation-attribute rules](https://www.w3.org/TR/css-transforms-1/#svg-transform).

### SVG elements have no consistent DOM wrapper structure

Different SVG mark types may render as:

- `<g class="mark-type"><rect>` (wrapped in a group)
- `<circle class="mark-type">` (bare element, no wrapper)
- `<text class="mark-type">` (bare element)

A CSS selector like `.mark-type circle` fails when the circle IS the `.mark-type` element. Always inspect the actual DOM structure before writing selectors. Use `circle.mark-type` (element selector) vs `.mark-type circle` (descendant selector) accordingly.

### Continuous motion across chained segments

When motion passes between segments, match position and velocity at the handoff. A decelerating segment followed by a fast-starting segment can stutter.

Linear timing is a useful baseline, but segment distance and duration must also agree. Use other easing when a pause or speed change is intentional.
