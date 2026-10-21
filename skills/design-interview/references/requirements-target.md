# Requirements gathering

artifact-type: Requirements document

A customer-facing business interview. Its outcome is an understanding of the customer's business and needs that they recognise as theirs, can correct, and eventually approve, and that others can design and build from, with every statement traceable to something a person said or showed.

It sits above goals: it can start a new system, or show what an existing one must change, and what it produces is what kicks off the work.

Here the user who answers the page is the customer, interviewed on the owner's behalf. The owner directs the interview: whom to ask, what may be shared or promised, and what happens with the result.

## Where it lives

The interview's folder is `requirements/<slug>/` at the root of the project's local copy, with a short name for the subject as its slug, made unique when it exists. The ledger stays at the folder's root. The page is the requirements document itself, `customer/index.html`: `customer/` is the only folder the customer can open. Beside them, `owner-report.md` holds readiness, considerations, and the recommended next step, for the owner and their team, never the customer.

Share only `customer/`, only with the people the owner names, at `respond`. Never share the interview's folder itself: its ledger holds material marked for the owner only.

## Who decides

A customer confirms what they need; only someone with authority decides for their organisation; only the owner decides what the owner's company will do; a decision the customer leaves to the delivery team is recorded as delegated, with who delegated it. Record which each statement is.

## Start from what is known

The interview often begins with a lot already supplied: the owner's notes, earlier conversations, documents the customer sent, the project itself. Read it first and use it: ask about what is thin, ambiguous, contradictory, or needs the customer's judgment, never about what they already gave just to cover a topic.

Context guides the interview without becoming the customer's word. Record prior context with its source and the status it has earned. A customer statement is stated; the owner's interpretation is inferred until the customer confirms it. Preserve earlier confirmations and decisions for unchanged content, with who gave them, when, and what they covered. Changing the interview's medium does not require the customer to confirm the same content again.

## What to understand

These areas describe any business need. They tell you what is still missing; they are never an agenda.

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

Each area reaches the depth the idea needs: mentioned, described, specified (real cases, numbers, exceptions), or decided (with who decided and why), or it ends as not applicable, not known to this person (with who knows), or declined. What is central to what they want needs specifics; what is peripheral can rest at a description. Do not assume the customer is nontechnical: follow their knowledge as deep as it is useful.

## Kinds of questions

Most questions in this interview ask for what only the customer knows, and you cannot answer them on their behalf.

- **Discovery questions** ask how their work happens, what goes wrong, and what they need. Give each the context that prompts it, such as the process drawn so far with the gap marked, or an example to react to, and room to answer in their own words. They carry no options and no recommendation.
- **A proposed reading** shows what the context or an earlier answer suggests, as our understanding, and asks whether it is right. It stays proposed until the customer confirms it.
- **Choices** appear only where the customer genuinely picks among alternatives, such as which of two scenarios they mean or what comes first. Show what each choice makes true without steering. Recommend nothing about what they need or how their business works.
- **Approval questions** ask the customer to confirm a section of the document, recording the `rev` of every item it covers.

Rigour comes from specifics, asked for in the customer's terms:

- **Today first, end to end.** Follow the work from the moment it starts to the moment it is done, across every person and channel it touches, then under pressure: a busy day, a peak season, two things at once. What breaks under load shows what matters.
- **A real recent case** beats a general account.
- **For each scenario:** what starts it, who is involved, the steps, what varies, what goes wrong and what happens then, how often and how many, what information is used or produced, which rules apply, and how it ends.
- **Responsibilities and handoffs.** When something passes from one person or system to another, ask what is passed, who acknowledges it, how fast, and what happens when nobody picks it up. Ask what must never happen without a person's say.
- **For each need:** how they would know it works. The answer becomes its check.
- **Numbers** where they matter: volumes on a normal day and at peak, deadlines, amounts, response times.
- **How binding.** Volunteered product or technical detail is kept whole and classified: required, and by whose authority; a preference; an example; or left to the delivery team.
- **Where statements meet.** When two answers pull against each other, ask how they fit rather than choosing for the customer.

## Rounds

The customer answers on the page, often between other work and over days. Keep each round answerable in one sitting and readable in their business terms: today's process with where it fails, scenarios walked step by step, examples to react to, and the open questions that follow from them. A round is never a questionnaire pasted into a page. When a round would go better talked through, the interview can continue in `conversational-interview`.

Never promise on the page what the system will do or when; the owner's team answers that.

Draw out the need behind a solution the customer volunteers, and keep the solution attributed to them. Do not pitch, sell, or steer them toward a solution they did not bring.

## Readiness

The requirements reach their states by evidence, not by rounds held.

| State | Holds when |
|---|---|
| **Sketch** | The idea is captured; core content is thin or open. |
| **Draft** | Every core area is backed by evidence or names what is missing and who holds it. |
| **Customer-confirmed** | The customer has reviewed the document and confirmed its sections, on the page or in conversation, each confirmation recorded with who, when, and the `rev` it was given on. |
| **Baselined** | Someone with authority for the customer's side has approved what the document treats as decided, and the owner has adopted it. |

The core areas decide readiness: purpose and business context, people, outcomes and how they are measured, today's work, scenarios, and needs. The rest may stay partly open. Keep three readings apart, and report each:

- **Exhaustion:** the customer has nothing more to give. Recent rounds return only restatements, a closing "What did we miss?" adds nothing, and every remaining gap is held by someone else, unknown to them, or declined.
- **Coverage:** every area has reached the depth the idea needs, or ends as not applicable, not known (with who knows), or declined.
- **Detail sufficiency:** every requirement is checkable, and a later stage could design from the document without inventing the customer's intent or needs. Design decisions the customer did not make are left to the stages after this one.

An open question marked as blocking holds the requirements below the state it blocks. An interview can be complete for this customer and still wait on others; say so and name them.

## Writing requirements

A requirement states what a person must be able to do or have, in their terms, so that it is necessary (it traces to an outcome, scenario, or rule they stated), unambiguous (one reading, in their terms), checkable (its check says how they would know it is met), and consistent (it contradicts nothing else, or the conflict is recorded). Avoid vague qualities such as "fast" or "easy" unless a number or a check makes them testable; ask for one. Setting targets nobody stated belongs to the design that follows.

## Folding in answers

Fold answers as the skill describes, with these additions:

- Answers on the page stay there after they are folded, so fold only what the ledger's evidence does not already hold. Feedback given on an earlier `rev` is evidence about that version, not a reaction to the current one.
- A reaction of "not quite" or "reopen" adds `disputed=Q-nn` to the item's review flags, with that question carrying the objection. Set its status to what the remaining evidence supports.
- An answer from someone you cannot identify is evidence, not confirmation, until the customer confirms it.
- A change to an item that was confirmed or approved marks it for reconfirmation; the earlier confirmation no longer counts for the new content.
- A term you propose for the Language list stays proposed until the customer confirms it. Here, unlike the skill's default for new terms, leaving it uncommented is not agreement.

After each round, update `owner-report.md` for the owner and their team, in plain words and the subject's own terms, the point first, with these sections, writing "None." where empty: **In brief** (what the customer has in mind, in two sentences, and the recommended next step); **Readiness** (the state, the three readings, and what would move it on); **Who we heard from** (each person, their role and authority as stated, and how confident we are); **Considerations** (commercial, feasibility, and risk observations, marked as your reading); **Customer questions** (what they asked that the owner must answer); **Conflicts and gaps held by others** (with who can close each); **Next step** (another round, a conversation, someone else to ask, handoff, or no further work, with the reason).

## Coverage and completion

The interview is complete when the requirements are baselined and:

- exhaustion and coverage hold for every person consulted, and detail sufficiency holds for the document;
- every core area is substantiated, and no blocking question remains open;
- every requirement has its evidence, rationale, priority, check, and status;
- no unresolved conflict touches a core area;
- every item treated as decided names who decided it, with their authority;
- nothing inferred, proposed, disputed, or awaiting reconfirmation reads as confirmed;
- the customer has reviewed and confirmed the document's sections, on the page or in conversation, covering the current `rev` of every item;
- the page shows the baselined ledger.

The owner may instead accept the requirements at an earlier state and hand them on with their gaps. That is an accepted handoff, not a completed interview: record it as such in the owner report, with every reading that does not hold and every blocking question still open.

## Ledger

The ledger is the requirements record: read [the requirements record](requirements-record.md) before creating or folding into it. Its lists take the place of Settled. The skill's round header fields, Frontier, Not yet, and Delta sit beside them. The round header and `documents` entry refer to the same page and form. A frontier question about an item names it with `about=<ID>`. An open question the customer can answer enters the frontier linked to its `Q` entry; one held by someone else stays a `Q` entry, with its holder.

## Page

These fill the brief's page placeholders. The visuals are starting points the builder may better; the page rules hold.

- **Settled title:** their business and needs, as we understand them.
- **Settled visuals that fit:** today's process with where it fails; the people and who does what, with the handoffs between them; scenarios walked step by step, exceptions beside the step they break; outcomes beside the needs that serve them.
- **Question visuals that fit:** the process or scenario drawn so far with the open step marked; an example to react to; for a choice, each alternative played through a real case.
- **Page rules:** the page stands alone, a complete document that bypasses the tree's shared navigation, with everything it shows inside `customer/`, and names the ledger as its agent version with `href="../ledger.md"`; Dossier gives the ledger only to readers who can open it. Show every current item with audience `all`, including scenario steps. Evidence entries and owner-only items stay out; retired entries are history, and closed questions and choices appear through what settled them. Apply the same audience rules to frontier questions, held topics, and the delta so they disclose no owner-only material. It reads in the customer's terms: evidence IDs, status vocabulary, and words like "ledger" stay out, while each item shows its ID as a short pointer people can cite and say aloud. Mark in the customer's terms what is our reading, what is disputed, and what awaits reconfirmation.
- **Feedback rules:** read [the requirements record](requirements-record.md), including its contract for page feedback across sessions and rounds. Offer item reactions, choices, section approvals, and flags alongside round answers, using the same form. Comments and handoffs identify the revisions reviewed; approvals cover every item ID and revision in the section. Preserve existing form fields, saved feedback, and anchors when revising a page or changing medium. Report the JSON feedback field's name with the form details for the ledger's `documents` entry.

## Handoff

Leave the project's glossary unchanged: the customer's terms stay in the record, for a later Glossary or Solution Architecture interview to seed from. Report the paths and links of the document, the ledger, and the owner report, with the readiness state, and end with a ready-to-use message for what the requirements start, shown in a Markdown code block so it can be copied whole:

- **A new system:** "Use the `design-interview` skill with the Solution Architecture profile to design the architecture of <subject>. The requirements document is at <document path>, with its ledger at <ledger path>, and the owner report at <owner report path>. Its requirements, rules, constraints, and terms are citable by their IDs, and <who owns them> owns them, so requirements questions go to them. Seed the Language list from its terms. <What is still open or inconsistent, and the readiness state.> <Where the system it replaces lives, and what carries over, when there is one.> Work in `architecture/` at the root of the project's local copy."
- **Changes to an existing system:** "Use the `basecamp` skill to take in the work described by the requirements document at <document path>, with its ledger at <ledger path> and the owner report at <owner report path>. <Who owns the requirements.> <What is still open, and the readiness state.>" basecamp decides how many goals it becomes and routes each.
