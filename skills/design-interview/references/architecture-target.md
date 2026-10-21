# Solution Architecture

artifact-type: Solution Architecture Document (arc42)

A solution architecture establishes, for a whole system, **what drives** its design, **how** it is structured, **what** it is built with, and **where** it runs. It stays at the altitude of the system: the parts that run or deploy separately, the contracts between them, the data each owns, the technology and vendors they rest on, and the concerns that cut across them. How each part is built inside belongs to the detailed design that follows, and what users see and do belongs to the product requirements.

The page reads as an arc42 document, so readers who know arc42 find each decision where they expect it; the coverage below follows its sections.

## Inputs

There is no required input: a requirements document from a requirements interview, a stakeholder or software requirements specification, a product brief, a few sentences from the user, or an existing system. Cite what exists as settled sources, and keep the requirement IDs of those documents citable. When the drivers are thin, surface the gap as a question; a quality goal or constraint nobody stated is a question, never a settled entry.

The user's standing preferences, such as a usual stack or hosting, are their stated intent. Once the drivers are confirmed, retrieve them with the `stack-preferences` skill for the categories the solution touches. Settle an applicable preference with that source, open to comment like any settled entry. A `per_project` entry supplies candidates for a question, with `decided_by` as its deciding criterion. A preference whose `override_when` the drivers meet also becomes a question, with the preference as one option. Where choices have conditions, settle only the choice the drivers support; otherwise ask what would decide it.

The requirements belong to whoever owns them. When a technical decision would change what the system's users or stakeholders get, such as a cut in scope or a quality they would notice, put it on the frontier as a requirements question and say who must answer it.

When the work replaces or restructures an existing system, establish its current architecture from the code first: it is settled as today, and the code settles current behaviour. Show today inside each part of the design as the delta to the target, rather than as a separate account. The solution also settles the way from one to the other: what coexists, how data moves, and how the switch happens.

## Drivers first, then the solution

**Drivers** settle what the architecture must achieve and respect: purpose and scope, the stakeholders whose concerns shape it, the quality goals, the constraints, and the system's context. **Solution** settles the strategy and everything that follows from it: technology and vendors, building blocks, data, repository layout, runtime, deployment, cross-cutting concerns, and risks.

**The gate.** No solution question enters the frontier until the drivers coverage below is met and the user has read the settled drivers and confirmed them, as a round of its own with no other questions. A stack chosen before anyone has said what "fast" means is the failure this gate prevents. Fold in the fixes the user raises before the solution opens. An explicit confirmation carried in from an earlier stage counts for the entries it covered, as long as they have not changed since; put anything added or changed after it in front of the user in the gate round.

The solution opens with the strategy: the architectural style and overall shape. Its losing options become the paths not taken, and the detail questions follow from the shape chosen. When later exploration shows the shape no longer fits, reopen it as a question rather than working around it.

Decisions that shape how the system is built and shipped rather than what it is, such as branching, release cadence, review, and dependency policy, form a third group, **Delivery process**. They may be asked in either phase, and the page keeps them apart so the architecture stays an architecture.

The user is usually present and iterating: keep each round quick to read and answer in one sitting, and fold in what a conversation settles between rounds without waiting for the page.

## Comparing options

Compare technology and structural options on how well each meets the quality goals, what it costs to build and to run, what it takes to operate, how hard it would be to leave, how mature and well supported it is, and how familiar it is to the people who will build it, and name the criterion that decides it. When the overall shape has real design freedom, design it twice as [comparing options](comparing-options.md) describes, with constraints that make the shape telling, such as the fewest moving parts, parts that scale and fail independently, or the lowest running cost. For a contract between building blocks with real design freedom, use its seam and interface criteria. A decision that rests on facts that age, such as pricing, limits, or a library's upkeep, records each fact's source and the date it was checked.

## Coverage

Every item below ends as a settled entry, a Quality goals or Constraints entry, an Out of scope entry, or a deferred question naming the later stage that decides it. One entry may cover every instance of an item by stating the shared rule; only exceptions need their own. An item that does not apply is recorded as not applying. An item the interview never reached is not done.

Drivers:
- What the system is for, its scope, and what it leaves out.
- The stakeholders whose concerns shape the architecture, and those concerns.
- The top quality goals, a handful, each as a scenario with a measurable target and its source.
- Every constraint the architecture must respect, organisational, technical, regulatory, budget, or time, each with its source.
- The context: every person and external system the system deals with, and what passes between them.

Solution:
- The strategy: the architectural style and overall shape, with its paths not taken, and the approach that reaches each quality goal.
- The technology of each building block, and every dependency or vendor that would take real work to replace, with what it was chosen over.
- The toolchain the system is built with: language and runtime, package and build tooling, and test and quality tooling.
- Build or buy, for each capability that could be either.
- Every building block that runs or deploys separately, what it owns, and the contract across each boundary between them.
- Every persistent store, what it holds, and who owns writes to it.
- The repository layout: how many repositories, the packages in them, and which may depend on which.
- The domain contexts, when the language differs between parts of the system, and which building blocks or packages each lives in. The Language list follows them, as [glossary guidance](glossary.md) describes for several contexts.
- The key runtime scenarios across the building blocks, including what callers see when a part is down, slow, or wrong.
- Deployment: where each building block runs, the environments, how a change reaches production, and the rough running cost.
- The cross-cutting concerns the system needs, such as identity and access, secrets, observability, data protection and retention, languages, and how it is verified without its real dependencies.
- The riskiest technical assumptions, such as a vendor handling the load or a language well enough, each with how it will be tested before much is built on it.
- The risks and technical debt accepted, each with what would reduce it.
- Every idea left out, marked deferred or rejected, each rejection with a durable reason.
- Every question about the inside of a building block, as a deferred question for its detailed design.
- Every term specific to the system, in the Language list.

## Completion

The interview is complete when all of these hold:

- The frontier and not-yet lists are empty.
- Every coverage item is accounted for in the ledger.
- The user confirmed the drivers at the gate, and confirmed the solution in a final review round of its own.
- A reader who scans the page's overview and main section headings can explain what the system must achieve, how it is structured, what it is built with, and where it runs, without the interview history.

A frontier that emptied because few questions were asked does not meet this. The coverage list, not the question count, sets the bar, and a chosen stack is not yet an architecture.

## Ledger

Settled entries carry `phase=drivers|solution|process` and one of these groups: `inputs` (cited context), `purpose`, `stakeholders`, `context`, `strategy`, `technology`, `toolchain`, `blocks`, `contracts`, `data`, `repository`, `domains`, `runtime`, `deployment`, `crosscutting`, `assumptions`, `risks`. Frontier questions carry the same `phase`, and technology, structure, and seam questions carry `compare-on`.

Declare two lists after Settled:

- **Quality goals** (`QG-01`): the quality, the scenario, the measurable target, its priority among the goals, and its source. Page rule: they lead the settled design, each beside the approach that reaches it.
- **Constraints** (`C-01`), in the shape [ledger format](ledger-format.md) gives, with kinds such as `organisational`, `technical`, `regulatory`, `budget`, and `time`. Page rule: they form one short part of the drivers.

Attach the exact artifact to entries whose substance is a shape: a contract between building blocks, a store's ownership, the repository layout, a deployment topology, a key sequence. Draw each as a code sketch; read [code sketches](code-sketches.md) before drawing one.

## Page

These fill the brief's page placeholders. The visuals are starting points the builder may better; the page rules hold.

- **Settled title:** the architecture as agreed, in arc42's order.
- **Settled visuals that fit:** the C4 context, container, and deployment views; key runtime scenarios as sequences or animated flows; the repository layout as a tree; a risk map.
- **Question visuals that fit:** for a technology choice, each option's container view with what it pulls in and what it costs to run; for a structural choice, the building blocks each option produces; for deployment, a topology per option.
- **Page rules:** the settled design reads as an arc42 document, in its sections' order, showing only sections with content. Each section marks what in it is still open, pointing to the question that would settle it. The C4 views name every element exactly as the ledger does, and the views agree with one another. One small "paths not taken" block for the strategy, drawn from the `over` of the entries that settle it, is the only place the page shows an option that lost. Entries and questions tagged `phase=process` appear apart from the architecture, in their own clearly labelled area.

## Handoff

Beside the frozen ledger, write:

- `ARCHITECTURE.md`: the settled architecture for readers who will not open the page, in arc42's order with only the sections that have content. Draw the C4 views and key scenarios in Mermaid, naming elements as the ledger does. Its decisions section lists the ADRs in a line each and links to them rather than repeating them.
- `adr/NNNN-<slug>.md`: one ADR for each settled decision that is hard to reverse, would surprise a reader without its context, and came from a real trade-off. Most decisions are not all three and get no ADR. An ADR is short: the context, the decision, and why, in a few sentences. Add the alternatives considered, the consequences, or the dated facts it relied on only when a reader needs them.

The frozen ledger, `ARCHITECTURE.md`, and the ADRs are the input for whatever designs or builds from this architecture, such as the detailed design of one building block or the work that sets up the system.
