# Technical Design Document

artifact-type: Technical Design Document (TDD)

A TDD establishes **how** to build what the product context describes, not what or why. It settles the shape of the system and the shape of its code down to seams and depth. It leaves exhaustive signatures and file-by-file structure to the structure outline that follows, which works them out from the seams this document decides.

## Inputs

A TDD normally arrives after a goal record, research, and a PRD interview. Cite them as settled sources, and do not re-decide them. When a PRD interview ran, its frozen ledger is an input: its settled entries arrive as settled product context citing their IDs, its behaviours and constraints stay citable by ID, and its deferred questions for the TDD join the first frontier, or wait on their prerequisites. When a design discussion moved to the separate route, its technical entries arrive as settled context the same way.

Research supplies what exists today; the PRD supplies what must be true for users. When a technical decision would change product scope or behaviour, put it on the frontier as a product question and say so.

## System Design first, then Program Design

Each question belongs to exactly one phase.

1. **System Design** settles behaviour *between* components, the parts that run or deploy separately: services, endpoints, schemas, stores, queues, external systems, and how the arrangement changes from what exists today. It settles the contracts at the seams: type signatures, endpoint and message shapes, data schemas.
2. **Program Design** settles the shape inside those components: which modules are deep, where each in-code seam goes, what sits behind it, how dependencies are injected, and where tests cross the interface. A module is anything with an interface and an implementation, at any scale; System Design treats each component as a module at its seams.

**The gate.** No Program Design question enters the frontier until the System Design coverage below is met and the user has read the settled System Design top to bottom and confirmed it hangs together. Ask for that confirmation as a round of its own, with no other questions. Fold in the fixes they raise before Program Design opens. An explicit confirmation carried in from an earlier stage counts for the entries it covered, as long as they have not changed since; record which entries it covered, and put anything added or changed after it in front of the user in the gate round. Answers to individual questions are not a confirmation. Investigating code-level detail earlier is fine when it is evidence for a System Design question.

Decisions that shape the implementation loop rather than the design (branching, review cadence, dependency policy, who may add what) form a third group, **Delivery process**. They may be asked in either phase, and the page keeps them apart so the TDD stays a design.

## Comparing seam and interface options

When a question in either phase is about where a seam goes or what an interface holds, compare its options on the seam and interface criteria in [comparing options](comparing-options.md), and produce them by designing it twice when the seam has real design freedom.

## Coverage

Every item below ends as a settled entry, an Out of scope entry, or a deferred question naming the later stage that decides it. One settled entry may cover every instance of an item by stating the shared rule, such as how all contracts report failure; only exceptions need their own. An item that does not apply is recorded as not applying. An item the interview never reached is not done, and a missing architectural decision is not routine outline work.

System Design:
- Every component in scope and what it owns.
- Every contract across a seam: its interface, what varies across it, and how it is tested through that interface.
- Every data schema that persists, who owns writes to it, and any migration it needs.
- Every external system touched, and what the design assumes about it.
- The delta from today: what exists, what is new, what changes.
- Identity and authorization at every seam a request crosses.
- Failure paths for each contract: what a caller sees when the other side is down, slow, or wrong.
- The local verification substrate: how the system runs in a check without its real dependencies.

Program Design:
- Which modules are deep and what each hides.
- Where each seam goes and which adapters justify it.
- Call trees or sequence sketches for the main paths.
- Dependency injection: what each module accepts rather than creates.
- Test placement and what each test establishes through which interface, preferring existing seams and the highest seam that exercises the behaviour, with as few seams as possible.
- Existing codebase patterns to follow, or to depart from deliberately, with file locations.
- What is out of scope, when a decision leaves something out.

## Completion

The interview is complete when all of these hold:

- The frontier and not-yet lists are empty.
- Every coverage item is accounted for in the ledger.
- The user confirmed System Design at the gate, and confirmed Program Design in a final review round of its own.
- A reader who scans the page's overview and main section headings can explain how the system fits together and what the code looks like, without the interview history.

A frontier that emptied because few questions were asked does not meet this. The coverage list, not the question count, sets the bar.

## Ledger

Settled entries carry `phase=system|program|process` and one of these groups: `product` (cited context), `components`, `contracts`, `schemas`, `external`, `delta`, `access`, `failure`, `verification`, `seams`, `calls`, `injection`, `tests`, `patterns`. Frontier questions carry the same `phase`, and seam and interface questions carry `compare-on` in either phase. Attach the exact artifact to entries whose substance is a shape: seam contracts (signatures, endpoint and message shapes), persisted schemas, call trees and sequences, dependency-injection maps, and pattern snippets with their file location. Draw each as a code sketch; read [code sketches](code-sketches.md) before drawing one. Other entries stay one line.

## Page

These fill the brief's page placeholders. The visuals are starting points the builder may better; the page rules hold.

- **Settled title:** the current System Design, joined by Program Design once the gate opens.
- **Settled visuals that fit:** a deployment or topology diagram, a module map with dependency direction, a short "who can do what" matrix.
- **Question visuals that fit:** for a scope decision, a slice diagram across the components showing what each option lights up; for a bootstrap or handshake, a small sequence sketch per option; for where a secret lives, a flow of its path; for an execution substrate, a diagram of what runs where.
- **Page rules:** entries and questions tagged `phase=process` appear apart from the design, in their own clearly labelled area.

## Handoff to the structure outline

The frozen ledger is the input for the structure outline. Its settled entries, rationale, Language list, Out of scope list, and requirement IDs are what the outline reads, and it takes up the deferred questions for the outline first.
