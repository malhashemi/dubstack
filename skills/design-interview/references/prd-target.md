# Product Requirements Document

artifact-type: Product Requirements Document (PRD)

A PRD establishes **what** to build and **why**, for the people who will use it: what they go through today, what changes for them, and how the team will know it helped. It stays in product space, in what users experience and how the product behaves. How it is built belongs to the TDD that follows.

## Inputs and product space

Inputs are whatever exists: a goal record, research, or a few sentences from the user. Cite them as settled sources. When a design discussion moved to this route, its frozen ledger is an input too, and its product entries arrive as settled context with their IDs. When the product context is thin, surface the gap as a question and let the user fill it; a requirement nobody stated is a question, never a settled entry. Research the product as it stands when a question needs that fact.

Write the problem and the solution from the user's side, in what they see and do. File paths and function names belong to the TDD. The names on a **surface** (commands, flags, fields, messages) are product decisions, so the PRD settles them exactly. When a technical question comes up, record it as a deferred question for the TDD with the context that raised it, and keep the round in product space.

## Foundation first, then the solution

The interview has two phases. **Foundation** settles the framing, the actors, today's experience, the success signal, and the riskiest assumptions. **Solution** settles the overall approach, then the flows, behaviours, constraints, and rollout that follow from it.

**The gate.** No solution question enters the frontier until the foundation coverage below is met and the user has read the settled foundation and confirmed it. Ask for that confirmation as a round of its own, with no other questions, so the framing gets the user's full attention before anything is built on it. Fold in the fixes they raise before the solution phase opens. An explicit confirmation carried in from an earlier stage counts for the entries it covered, as long as they have not changed since; record which entries it covered, and put anything added or changed after it in front of the user in the gate round. Answers to individual foundation questions are not a confirmation.

## Settling the foundation

- **Framing.** The framing is the first product decision, because framings differ in the solutions they allow. State it in exact words, naming whose pain it is and at which moment it hurts. When the inputs already state one, show it for confirmation; otherwise draft two or three that would lead to different solutions. The user picks one or writes their own.
- **Actors.** Name everyone the product serves or acts for, such as Owner and Guest. Each actor is a Language term, and every behaviour names its actor.
- **Today's experience.** Show what the actors go through now as a short flow or a before-view. Cite the evidence the inputs hold (numbers, quotes, tickets), so every piece of evidence on the page has a source.
- **Success signal.** What the team reads after shipping to see whether the work helped the people it was for: a number, an adoption sign, a benchmark, an error-rate or latency target, or a qualitative read, fitted to the work. For a small change the user may agree to an explicit "no sensible success signal"; record that agreement in its place.
- **Riskiest assumptions.** Name the one to three beliefs about users that the solution bets on and that nobody can check before shipping. Choose the success signal so that its reading would show them wrong.

## Settling the solution

The solution opens with the overall approach. Its losing options become the paths not taken, and the detail questions follow from the approach chosen.

- **Flows and surfaces.** For every flow the approach adds or changes, settle each surface an actor meets, drawn as a mockup.
- **Behaviours.** A behaviour is one observable outcome with an ID that the outline, the implementation checks, and review cite. For every flow and actor, cover four situations: the main path, nothing there yet, something fails, and the actor is not allowed. One shared behaviour may cover a situation for every flow, such as "every failure keeps the text the actor typed", or record that a situation does not apply; only exceptions get their own. Where the wording matters, quote the exact message.
- **Constraints.** Rules that hold everywhere and that no single behaviour shows: privacy and compliance, supported platforms, accessibility level, and limits the business sets, each with its source. An expectation an actor can observe, such as "a comment appears to others within two seconds", is a behaviour.
- **Rollout.** When the product has existing users or data, settle who gets the change first, what happens to what users already have, and how the success signal is read during the rollout.

## Comparing and showing options

Compare product options on the product criteria in [comparing options](comparing-options.md), with the framing as the measure of fit, and show look and behaviour questions as mockups and state demos as it describes.

## Coverage

Every item below ends as a settled entry, a Behaviours or Constraints entry, or an Out of scope entry; the success signal may end as an agreed explicit none. Only technical questions leave as deferred questions for the TDD: a product decision the solution needs is settled here, not passed on. One entry may cover every instance of an item by stating the shared rule; only exceptions need their own. An item that does not apply is recorded as not applying. An item the interview never reached is not done.

Foundation:
- The chosen framing: whose pain, at which moment, in its exact words.
- Every actor, each a Language term.
- Today's experience as a short flow or before-view, citing evidence when the inputs hold it.
- The success signal, or an agreed "no sensible success signal".
- One to three riskiest assumptions, each tied to the success signal reading that would show it wrong.

Solution:
- The overall approach, with its paths not taken.
- Every flow the approach adds or changes, with a mockup of each surface an actor meets.
- For every flow and actor, behaviours for the main path, nothing there yet, a failure, and not allowed.
- Every rule that holds everywhere, as a constraint with its source.
- A rollout, when the product has existing users or data.
- Every idea left out, marked deferred or rejected, each rejection with a durable reason.
- Every technical question raised, as a deferred question for the TDD.
- Every term specific to the product, in the Language list.

## Completion

The interview is complete when all of these hold:

- The frontier and not-yet lists are empty.
- Every coverage item is accounted for in the ledger.
- The user confirmed the foundation at the gate, and confirmed the solution in a final review round of its own.
- A reader who scans the page's overview and main section headings can explain whose problem this is, what changes for them, and how the team will know it helped, without the interview history.

A frontier that emptied because few questions were asked does not meet this. The coverage list, not the question count, sets the bar.

## Ledger

Settled entries carry `phase=foundation|solution` and one of these groups: `product` (cited context), `framing`, `today`, `signal`, `assumptions`, `approach`, `flows`, `rollout`. Frontier questions carry the same `phase`, and product option questions carry `compare-on`. Actors are Language terms. Use the Behaviours and Constraints lists from [ledger format](ledger-format.md). Attach the exact artifact to entries whose substance is a shape: an approved mockup or state demo file, an exact message, or a command's or API's exact form.

## Page

These fill the brief's page placeholders. The visuals are starting points the builder may better; the page rules hold.

- **Settled title:** the product as agreed, foundation first, then solution.
- **Settled visuals that fit:** today's experience as a flow; each flow with its mockups and behaviours beside them; the success signal next to the assumptions it would show wrong; the rollout as a timeline.
- **Question visuals that fit:** one mockup per option for a look question; a state demo for a behaviour question; each option's effect drawn on a running example for a scope question.
- **Page rules:** each behaviour sits beside the flow or mockup it belongs to, not in a separate list, and the constraints form one short part of the solution. One small "paths not taken" block for the overall approach, drawn from the `over` of the entries that settle it, is the only place the page shows an option that lost. Mockups use the product's design system; when the product has none, the mockup direction names the default styles to leave out, not only the style wanted.

## Handoff to the TDD

The frozen ledger, with its mockup and state demo files beside it, is the input for a TDD interview in a fresh session. There its settled entries arrive as settled product context, its behaviours and constraints stay citable by ID through the outline, implementation, and review, and its deferred questions for the TDD join the TDD's first frontier.
