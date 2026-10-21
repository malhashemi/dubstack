# Requirements gathering

A customer-facing business interview. Its outcome is an understanding of the customer's business and needs that they recognise as theirs, can correct, and eventually approve, and that others can design and build from, with every statement traceable to something a person said or showed.

It sits above goals: it can start a new system, or show what an existing one must change, and what it produces is what kicks off the work.

## Where it lives

The interview's folder is `requirements/<slug>/` at the root of the project's local copy, with a short name for the subject as its slug, made unique when it exists. Beside the shared layout it holds:

- `owner-report.md`: readiness, considerations, and the recommended next step, for the owner and their team, never the interviewee;
- `feedback/`: feedback on the document as collected, before it is folded in;
- `customer/`: the only folder the interviewee can open, holding the requirements document as `index.html` and any other view of it.

Share only `customer/`, only with the people the owner names, at `respond`. Never share the interview's folder itself: its ledger holds material marked for the owner only.

## Who decides

An interviewee confirms what they need; only someone with authority decides for their organisation; only the owner decides what the owner's company will do; a decision the customer leaves to the delivery team is recorded as delegated, with who delegated it. Record which each statement is.

## Start from what is known

The interview often begins with a lot already supplied: the owner's notes, earlier conversations, documents the customer sent, the project itself. Read it first and use it: ask about what is thin, ambiguous, contradictory, or needs the person's judgment, never about what they already gave just to cover a topic.

Context guides the interview without becoming the customer's word. Record prior context with its source and the status it has earned. A customer statement is stated; the owner's interpretation is inferred until the customer confirms it. Preserve earlier confirmations and decisions for unchanged content, with who gave them, when, and what they covered. Changing the interview's medium does not require the customer to confirm the same content again.

## What to understand

These areas describe any business need. They tell you what is still missing; they are never an agenda, and the person's own threads come first.

| Area | What it captures |
|---|---|
| Purpose | What they want to be different, and why now |
| Business | Their situation, organisation, domain, customers, market |
| People | Who uses it, is affected, operates, pays, decides, can block |
| Today | How the work happens now, end to end, and where it fails |
| Outcomes | What good looks like, and how they would know |
| Scenarios | What they picture happening: triggers, steps, variations, exceptions, failures |
| Needs | What each person must be able to do or have |
| Responsibilities | Who or what does each part, where work is handed over, and what must never happen without a person |
| Rules | Policies, calculations, approvals, regulations they work under |
| Constraints | Money, dates, volumes, platforms, existing systems and data, languages |
| Product and technical detail | Whatever they hold, as deep as they hold it |
| Priorities | What is essential, what can wait, what is out |
| Risks and unknowns | What they are unsure of or worried about |

Each area reaches the depth the idea needs: mentioned, described, specified (real cases, numbers, exceptions), or decided (with who decided and why), or it ends as not applicable, not known to this person (with who knows), or declined. What is central to what they want needs specifics; what is peripheral can rest at a description.

## Reaching checkable detail

Rigour comes from specifics, asked for in the customer's terms:

- **Today first, end to end.** Follow the work from the moment it starts to the moment it is done, across every person and channel it touches, then follow it under pressure: a busy day, a peak season, two things at once. What breaks under load shows what matters.
- **A real recent case** beats a general account: "Tell me about the last order that went wrong."
- **For each scenario:** what starts it, who is involved, the steps, what varies, what goes wrong and what happens then, how often and how many, what information is used or produced, which rules apply, and how it ends.
- **Responsibilities and handoffs.** When something passes from one person or system to another, ask what is passed, who acknowledges it, how fast, and what happens when nobody picks it up. Ask what must never happen without a person's say.
- **For each need:** "How would you know this works?" The answer becomes its check.
- **Numbers** where they matter: volumes on a normal day and at peak, deadlines, amounts, response times. Repeat them back.
- **How binding.** Volunteered product or technical detail is kept whole and classified by asking: is it required, and by whose authority; a preference; an example of what they mean; or something they leave to the delivery team?
- **Where statements meet.** When two answers pull against each other, such as "customers pick a delivery time" and "nothing is promised until we confirm it", ask how they fit rather than choosing for them.

## During the session

Nothing is organised into the ledger during the session: research, reconciling, and composing wait until it ends. Show something only when the interviewee asks to see it; a visual they ask for can be made while the conversation continues and is kept in `visuals/`. Never promise what the system will do or when; the owner's team answers that.

Draw out the need behind a solution the customer volunteers, and keep the solution attributed to them. Do not pitch, sell, or steer them toward a solution they did not bring.

## The record

Read [the requirements record](requirements-record.md) before creating or reconciling the ledger. It defines evidence, status, review flags, authorship, audience, and feedback that carries across media. Keep this file's areas in view while you talk, since the document can only show what the ledger holds.

## Readiness

The requirements reach their states by evidence, not by time spent or sessions held.

| State | Holds when |
|---|---|
| **Sketch** | The idea is captured; core content is thin or open. |
| **Draft** | Every core area is backed by evidence or names what is missing and who holds it; the document can be composed. |
| **Customer-confirmed** | The customer has reviewed the document and confirmed its sections, in conversation or on the document, each confirmation recorded with who, when, and the `rev` it was given on. |
| **Baselined** | Someone with authority for the customer's side has approved what the document treats as decided, and the owner has adopted it. |

The core areas decide readiness: purpose and business context, people, outcomes and how they are measured, today's work, scenarios, and needs. The rest may stay partly open. Keep three readings apart, and report each:

- **Exhaustion:** the interviewee has nothing more to give. Recent questions return only restatements, a closing "What did I miss?" adds nothing, and every remaining gap is held by someone else, unknown to them, or declined.
- **Coverage:** every area has reached the depth the idea needs, or ends as not applicable, not known (with who knows), or declined.
- **Detail sufficiency:** every requirement is checkable, and a later stage could design from the document without inventing the customer's intent or needs. Design decisions the customer did not make are left to the stages after this one.

An open question marked as blocking holds the requirements below the state it blocks. A conversation ends on exhaustion or on the person's time; the requirements move on only on readiness. An interview can be complete for this person and still wait on others; say so and name them.

## Writing requirements

A requirement states what a person must be able to do or have, in their terms, so that it is necessary (it traces to an outcome, scenario, or rule they stated), unambiguous (one reading, in their glossary's terms), checkable (its check says how they would know it is met), and consistent (it contradicts nothing else, or the conflict is recorded). Avoid vague qualities such as "fast" or "easy" unless a number or a check makes them testable; ask for one. Setting targets nobody stated belongs to the design that follows.

## After each session

Reconcile the session into the ledger, update `owner-report.md`, publish, and give the owner the report's gist with its link. The owner report is for the owner and their team, never the interviewee. Write it for them to read in a couple of minutes, in plain words and the subject's own terms, the point first, with these sections, writing "None." where empty:

1. **In brief:** what the customer has in mind, in two sentences, and the recommended next step with its reason.
2. **Readiness:** the state, the three readings, and what would move it to the next state.
3. **Who we spoke to:** each person, their role and authority as stated, and how confident we are in that.
4. **Considerations:** commercial, feasibility, and risk observations, marked as your reading.
5. **Interviewee questions:** what they asked that the owner must answer.
6. **Conflicts and gaps held by others:** with who can close each.
7. **Next step:** another session with this person, a session with someone named, a human conversation, composing or recomposing the document, handoff, or no further work, with the reason.

## The requirements document

The customer-facing artifact establishes, in the customer's own terms: their business and what they want to change; the people and roles involved; how the work happens today and where it fails; the outcomes they want and how they would know; the scenarios, with their exceptions; the requirements, each with its priority, its check, and whether it is required, a preference, an example, or delegated; the rules and constraints; what is in, what is out, and what comes later; the open questions, with who can answer each; their terms; and who confirmed or approved what, on which version. When the owner or customer asks for a standard layout, such as a Stakeholder Requirements Specification or a business requirements document, compose it as another view of the same ledger.

Compose it once exhaustion and coverage hold for the people consulted so far. The owner may ask for an earlier draft; it still waits until the session has ended and been reconciled. Detail that still needs the customer goes into the document as something to confirm. Give the composer [the document brief](requirements-document-brief.md) with its placeholders filled. Check that its coverage report accounts for every ledger ID under the brief's audience, lifecycle, and view rules, that nothing owner-only appears, and that feedback survives a reload. Record the page and form details under `documents`. Then read it as the customer would. Where it reads as a conversation log, buries the idea under IDs, or leaves the reader to reconstruct from prose what a picture would show, send it back with what to change.

Share the document's link with the people the owner names and tell them how to respond: on the document, through feedback anchored to its items, or in conversation, walking through it by its spoken pointers. When a response opens a gap, interview again on that gap.

## Folding in feedback

After each session or review, and before the next, fold every piece of feedback, spoken or on the document, into the ledger:

- Fold only feedback the ledger's evidence does not already hold, since answers on the document stay there after they are folded. Feedback given on an earlier `rev` is evidence about that version, not a reaction to the current one.
- Check any factual claim you can check before relying on it.
- A comment is input, not a change. Decide whether it is a fix you make, a fact to look up, or a question to raise, and record which.
- A reaction of "not quite" or "reopen" adds `disputed=Q-nn` to the item's review flags, with that question carrying the objection. Set its status to what the remaining evidence supports.
- Feedback from someone you cannot identify is evidence, not confirmation, until the customer confirms it.
- A change to an item that was confirmed or approved marks it for reconfirmation; the earlier confirmation no longer counts for the new content.
- When an item's meaning changes, supersede it rather than editing it in place, so feedback never attaches to something the customer did not see.
- Untouched items stay as they were. A proposal nobody reacted to is still a proposal.
- Rewrite everything a change reaches, retire what it makes false, and record what changed in the delta.

Then update the owner report, and have the document recomposed with the brief's revision section.

## Completion

The interview is complete when the requirements are baselined and:

- exhaustion and coverage hold for every person consulted, and detail sufficiency holds for the document;
- every core area is substantiated, and no blocking question remains open;
- every requirement has its evidence, rationale, priority, check, and status;
- no unresolved conflict touches a core area;
- every item treated as decided names who decided it, with their authority;
- nothing inferred, proposed, disputed, or awaiting reconfirmation reads as confirmed;
- the customer has reviewed and confirmed the document's sections, on the page or in conversation, covering the current `rev` of every item;
- the document shows the baselined ledger.

The owner may instead accept the requirements at an earlier state and hand them on with their gaps. That is an accepted handoff, not a completed interview: record it as such in the owner report, with every reading that does not hold and every blocking question still open.

## Handoff

Freeze the ledger and the document as they stand. Leave the project's glossary unchanged: the customer's terms stay in the record, for a later Glossary or Solution Architecture interview to seed from. Report the paths and links of the document, the ledger, and the owner report, with the readiness state. End with a ready-to-use message for what the requirements start, shown in a Markdown code block so it can be copied whole:

- **A new system:** "Use the `design-interview` skill with the Solution Architecture profile to design the architecture of <subject>. The requirements document is at <document path>, with its ledger at <ledger path>, and the owner report at <owner report path>. Its requirements, rules, constraints, and terms are citable by their IDs, and <who owns them> owns them, so requirements questions go to them. Seed the Language list from its terms. <What is still open or inconsistent, and the readiness state.> <Where the system it replaces lives, and what carries over, when there is one.> Work in `architecture/` at the root of the project's local copy."
- **Changes to an existing system:** "Use the `basecamp` skill to take in the work described by the requirements document at <document path>, with its ledger at <ledger path> and the owner report at <owner report path>. <Who owns the requirements.> <What is still open, and the readiness state.>" basecamp decides how many goals it becomes and routes each.
