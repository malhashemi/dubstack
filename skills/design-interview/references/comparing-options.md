# Comparing options

This file supplies the criteria for comparing product and interface options, how to produce interface options that genuinely differ, and how to show each kind of question. The profile says which criteria apply to its questions.

A comparison ends in a recommendation that names the criterion that decides it, when the context supports one; otherwise it says what is missing. When the work has a criterion that matters more than these, such as a regulatory limit, add it and say why.

## Product options

- **Success signal:** how far the option moves it.
- **Fit:** how directly it serves the named actors at the moment the work is for, as the PRD's framing or the design discussion's summary states them.
- **What the user must learn:** the new concepts, steps, and surfaces it adds.

Existing product patterns break ties.

## Seam and interface options

- **Depth:** how much behaviour a caller gets per unit of interface they must learn. The interface is everything a caller must know: types, invariants, ordering, error modes, and required configuration.
- **Locality:** where change, bugs, and verification concentrate. Fix once, fixed everywhere.
- **Seam placement:** whether something real varies across the seam. One adapter is a hypothetical seam; two adapters (production and test) make a real one.

Two checks a question may cite: the **deletion test** (delete the module; if complexity vanishes it was a pass-through, if it reappears across callers it earned its keep), and **the interface is the test surface** (tests that must reach past the interface mean the module is the wrong shape).

## Design it twice

For a seam or interface question with real design freedom, the options come from independent attempts: separate subagents, each in its own context and under a different constraint. Independence reduces a real risk: one agent drafting several designs in a single context tends to anchor on its first idea and produce variations of it. Give every attempt the same requirements and inputs, and keep sibling proposals and any favoured solution out of its context until the attempts are compared. Separate contexts make distinct designs likely, not certain; when attempts converge anyway, present the convergence as evidence rather than inventing a difference.

By default, run three attempts in parallel, constrained to minimize the interface, to maximize flexibility, and to make the common caller trivial. Swap a constraint for one the seam makes more telling, such as supporting a variation the design already knows about, and add or drop an attempt when the seam calls for it, keeping at least two. Each attempt returns the interface with a usage example, what it hides, its dependency strategy, and where its leverage is thin. The attempts become the drawn options of one frontier question, each with its interface attached; add a hybrid when parts of two designs combine well. The page shows them as a comparison, never as prose.

## Showing options

- A look question shows one **mockup** per option: a drawing of the surface before it exists. That is a screen for a person, a terminal transcript for a command-line user, a request and its response from the caller's side for an API, or a message for a notification. Mockups differ in structure (layout, information hierarchy, primary action), not only in styling, and use the product's own design system with realistic labels and data.
- A behaviour question is shown as a **state demo**: a small clickable model that lets the user push the behaviour through hard cases.
- A code or interface question shows one code sketch per option; read [code sketches](code-sketches.md) before drawing one.

Beyond these, use whatever makes the difference between options visible. Build a prototype in the product's real code only when the user asks for one on a specific question.
