# Design Discussion

artifact-type: Design Discussion

A design discussion settles, for one piece of work and in one interview, **what** changes for the people who use the product, **why**, and **how** the code changes to deliver it. It is the combined route: work whose product and technical decisions are small and entangled takes it instead of a PRD followed by a TDD, and hands off directly to the structure outline.

## Inputs and readers

Inputs are the goal record and the research, cited as settled sources. The research-questions document shaped the research and stays out; the design reads the findings. When the product context is thin, surface the gap as a frontier question; a requirement nobody stated is a question, never a settled entry.

Every design question is the user's to decide, or to hand to you explicitly. When the research makes a choice look obvious, put it on the frontier with a strong recommendation; only the inputs, the codebase as it stands, the user, or the user's explicit delegation settle an entry.

Write today's experience and the desired end state from the user's side, in what they see and do. File paths, functions, and code belong to the code sketches, contracts, and patterns. The names on a **surface** (commands, flags, fields, messages) are product decisions, so the design settles them exactly. Keep evidence, inference, and proposal apart: today's state cites the research that found it, and a proposal reads as a decision, never as a fact about the code.

A design discussion has three readers: the user deciding now, the outline and implementation that build from it, and the PR reviewer who later checks the diff against it. Write so that each finds what the change must do, what it leaves out, and where it joins the existing code.

## One phase, one review

Product and technical questions share rounds, and the design tree alone sets their order: a technical question waits for the product decision it hangs off, and a product question that needs a technical fact waits for that fact. The design opens with the overall approach; its losing options become the paths not taken, and detail questions follow from the approach chosen. When later exploration shows the approach no longer fits, reopen it as a question rather than working around it.

When the frontier is empty and the coverage below is met, ask the user to read the whole settled design and confirm it, as a round of its own with no other questions. Fold in the fixes they raise before completing.

**When the work outgrows the route.** If the problem framing is contested, or the change reaches several components, put a route question on the frontier with your recommendation. If the user moves to the separate route, freeze the ledger with its artifacts and open questions. It becomes an input to a PRD interview and then a TDD interview, each taking the entries in its own scope as settled context.

## The product side

- **Summary.** One statement of the change and why, settled from the goal and open to correction.
- **Actors.** Everyone the product serves or acts for, such as Owner and Guest. Each actor is a Language term, and every behaviour names its actor.
- **Today's experience.** What the actors go through now, as a short flow or a before-view, citing the research.
- **Desired end state.** What the actors can do once the change ships.
- **Success signal.** What the team reads after shipping to see whether the work helped the people it was for: a number, an adoption sign, a benchmark, an error-rate or latency target, or a qualitative read, fitted to the work. For a small change the user may agree to an explicit "no sensible success signal"; record that agreement in its place.

## The design

- **Flows and surfaces.** For every flow the change adds or changes, settle each surface an actor meets, drawn as a mockup.
- **Behaviours.** A behaviour is one observable outcome with an ID that the outline, the implementation checks, and the PR review cite. For every flow and actor, cover four situations: the main path, nothing there yet, something fails, and the actor is not allowed. One shared behaviour may cover a situation for every flow, such as "every failure keeps the text the actor typed", or record that a situation does not apply; only exceptions get their own. Where the wording matters, quote the exact message.
- **Constraints.** Rules that hold everywhere and that no single behaviour shows: privacy and compliance, supported platforms, accessibility level, and limits the business sets, each with its source. An expectation an actor can observe is a behaviour.
- **Rollout.** When the product has existing users or data, settle who gets the change first, what happens to what users already have, and how the success signal is read during the rollout.
- **Code sketches.** Attach a code sketch, as an exact artifact, for every shape the change touches in the code: a call tree, file tree, component tree, schema, contract, or state. Read [code sketches](code-sketches.md) before drawing one.
- **Contracts and test seams.** At every seam the change crosses, settle the contract as an exact artifact: its interface, meaning everything a caller must know (types, invariants, ordering, error modes, and required configuration). Settle where tests cross it: existing seams first, the highest seam that exercises the behaviour, and as few seams as possible.
- **Patterns to follow.** Each pattern pairs a short snippet of the existing code, with its file location, and a short snippet of how the new code applies it, both as exact artifacts. The outline reads the design discussion within the same goal, so this precision stays current long enough to be worth it.

## Comparing and showing options

Compare product options on the product criteria in [comparing options](comparing-options.md), with the summary as the measure of fit, and seam and interface options on its seam and interface criteria, designing it twice when a seam has real design freedom. Show look, behaviour, and code questions as it describes.

## Coverage

Every item below ends as a settled entry, a Behaviours or Constraints entry, or an Out of scope entry; the success signal may end as an agreed explicit none. Only local questions leave as deferred questions for the outline, using the split `structure-outline` applies: where code lives, an internal helper, or the order of work inside a phase. A decision that changes observable behaviour, scope, a public or cross-component contract, data compatibility, security or privacy, or what the owner must pay for or provide is settled here; a missing product or design decision is not outline work. One entry may cover every instance of an item by stating the shared rule; only exceptions need their own. An item that does not apply is recorded as not applying. An item the interview never reached is not done.

Product:
- A one-statement summary of the change and why.
- Every actor, each a Language term.
- Today's experience from the user's side, citing the research.
- The desired end state from the user's side.
- The success signal, or an agreed "no sensible success signal".

Design:
- The overall approach, with its paths not taken.
- Every flow the change adds or changes, with a mockup of each surface an actor meets.
- For every flow and actor, behaviours for the main path, nothing there yet, a failure, and not allowed.
- Every rule that holds everywhere, as a constraint with its source.
- A rollout, when the product has existing users or data.
- A code sketch for every shape the change touches.
- Every seam the change crosses: its contract, and the test seam that checks it.
- Every pattern to follow: the existing code with its location, and how the new code applies it.
- Every idea left out, marked deferred or rejected, each rejection with a durable reason.
- Every question for the outline, as a deferred question.
- Every term specific to the work, in the Language list.

## Completion

The interview is complete when all of these hold:

- The frontier and not-yet lists are empty.
- Every coverage item is accounted for in the ledger.
- The user confirmed the whole design in the final review round.
- A reader who scans the page's overview and main section headings can explain what changes for users and in the code, without the interview history, and a PR reviewer can check a diff against the page.

A frontier that emptied because few questions were asked does not meet this. The coverage list, not the question count, sets the bar.

## Ledger

Settled entries carry `phase=design` and one of these groups: `product` (cited context), `summary`, `today`, `end-state`, `signal`, `approach`, `flows`, `rollout`, `sketches`, `contracts`, `tests`, `patterns`. Actors are Language terms. Product option questions and seam questions carry `compare-on`. Use the Behaviours and Constraints lists from [ledger format](ledger-format.md). Attach the exact artifact to entries whose substance is a shape: an approved mockup or state demo file, an exact message, a code sketch, a contract, or a pattern's snippets with their file location.

## Page

These fill the brief's page placeholders. The visuals are starting points the builder may better; the page rules hold.

- **Settled title:** the change as agreed, the product side first and then the design.
- **Settled visuals that fit:** today's experience beside the desired end state; each flow with its mockups and behaviours beside them; code sketches as diffs; each seam's contract with the test seam that checks it.
- **Question visuals that fit:** one mockup per option for a look question; a state demo for a behaviour question; one code sketch per option for a code question.
- **Page rules:** each behaviour sits beside the flow or mockup it belongs to, not in a separate list, and the constraints form one short part of the design. One small "paths not taken" block for the overall approach, drawn from the `over` of the entries that settle it, is the only place the page shows an option that lost. Evidence, inference, and proposal are marked apart. Mockups use the product's design system; when the product has none, the mockup direction names the default styles to leave out, not only the style wanted.

## Handoff to the structure outline

The frozen ledger, with its mockup and state demo files beside it, is the input for the structure outline. Its settled entries, behaviours, and constraints stay citable by ID through the outline, implementation, and review, and the outline takes up its deferred questions first.
