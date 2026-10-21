# The lens

What the review looks for and the words it uses. Use the same structural terms when exploring and judging candidates, so the findings can inform design-interview's comparison of interface options.

## Words

Use these terms the same way throughout the reports, the findings, and the page. The project's glossary names the domain; these name the structure.

- **Module:** anything with an interface and an implementation, at any scale: a function, a class, a package, a slice across tiers, or a separately deployed service. The review applies at every scale, so friction between services is found the same way as friction between functions.
- **Implementation:** what is inside a module.
- **Depth:** how much behaviour a caller gets per unit of interface they must learn. The interface is everything a caller must know: types, invariants, ordering, error modes, and required configuration. A module is deep when much behaviour sits behind a small interface, and shallow when its interface is nearly as complex as its implementation.
- **Seam:** the place where a module's interface lives, where behaviour can change without editing there. Where a seam goes is its own decision, apart from what sits behind it.
- **Adapter:** what fills the slot at a seam, such as a production client or an in-memory fake used by tests.
- **Leverage:** what callers get from depth: one implementation pays back across every call site and every test.
- **Locality:** where change, bugs, and verification concentrate. Fix once, fixed everywhere.
- **Seam placement:** whether something real varies across the seam. One adapter is a hypothetical seam; two adapters (production and test) make a real one.

Two checks:

- **The deletion test** (delete the module; if complexity vanishes it was a pass-through, if it reappears across callers it earned its keep). Reason through the deletion without changing code. Apply it to every module a candidate calls shallow, and record the result with the candidate.
- **The interface is the test surface** (tests that must reach past the interface mean the module is the wrong shape).

Depth belongs to the interface, not the implementation. A deep module may be built from small parts with their own private seams and tests; those parts do not make it shallow, and a direction keeps them out of the interface even when tests use them.

## Friction to look for

Follow the code rather than a checklist. These are the signs worth noting:

- Understanding one concept means bouncing between many small modules.
- An interface nearly as complex as its implementation.
- Pure functions extracted to be testable, while the bugs hide in how they are called: no locality.
- Tightly coupled modules leaking across their seams: callers rely on internals, or a change in one forces a change in another.
- Code that is untested, or hard to test through its current interface, often because it creates its own dependencies instead of accepting them, or acts through side effects instead of returning results.
- A seam with a single adapter, adding indirection where nothing varies.

Deepening pays off by making future changes easier, so friction in code that changes often counts for more than friction in code nobody touches.

## Dependencies decide how a deepened module is tested

Classify the dependencies involved; a candidate may span several categories. Use these testing directions to assess the likely gain, leaving the choice of interfaces and adapters to the design stage:

- **In-process:** pure computation or in-memory state. Absorbing shallow modules can let tests exercise their behaviour through one interface without an adapter.
- **Locally substitutable:** a dependency with a local stand-in, such as an in-memory database or filesystem. Tests can use the stand-in behind an internal seam.
- **Remote but owned:** the project's own services across a network. A port with production and in-memory adapters can make the logic testable independently of transport.
- **True external:** a third-party service the project does not control. An injected port can let tests use a fake adapter.

A stand-in tests only the behaviour it reproduces. Identify which transport, storage, or provider behaviours still need integration or contract checks; deepening does not remove those obligations.

A direction says how testing would change: tests through the deepened interface, asserting what callers can observe, in place of the tests on the shallow modules it absorbs.

## Strength

Every candidate carries one:

- **Strong:** real friction in code that changes, supported by the deletion test where it applies, with a clear direction.
- **Worth exploring:** real friction, but the gain or the direction needs the design stage to judge.
- **Speculative:** a plausible improvement that the evidence only partly supports, or friction in code that rarely changes.
