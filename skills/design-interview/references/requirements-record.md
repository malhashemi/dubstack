# The requirements record

The record is the requirements interview's source of truth, kept in the interview folder's `ledger.md`. The requirements document, any other view of it, and the owner report are composed from it, and later sessions, rounds, and stages read it. Keep it a set of lists, not a document: no narrative beyond the lists below.

The record is the same whether the interview runs in conversation or in visual rounds, so it can move between them. Each way of running adds its own working entries to the ledger, such as session notes or a round's open questions, and leaves the lists below in this shape.

Keep it current, not cumulative. After each reconciliation it describes the present state; only the delta speaks of what changed. Rewrite every entry a change reaches and leave the rest as they are, so what was quoted exactly stays exact.

## Header

- `target`: requirements gathering
- `subject`: the subject, in the customer's words
- `state`: sketch, draft, customer-confirmed, or baselined
- `readings`: exhaustion, coverage, and detail sufficiency, one line each
- `areas`: one line per area of the target, with its current depth, its target depth, and any terminal state (not applicable, not known with who knows, or declined) with the reason, so a resumed interview does not reopen what was exhausted or declined
- `documents`: for the requirements document and each other view, its path and link, its answers form's target and `id`, and the name of its JSON feedback field
- `owner-instructions`: what the owner allowed, or "defaults"
- `consent`: per session, who consented to what, and when
- `confidentiality`: what may not be shown to the customer, and what may not reach the owner's team, which stays in `private/`

## Lists

| List | ID | Content |
|---|---|---|
| Evidence | `E-01` | What was said, shown, written, or given as feedback, exactly, with its source |
| Language | `T-01` | The customer's terms and their definitions |
| People | `P-01` | People and groups, their stake, and their authority |
| Context | `CX-01` | Purpose, business background, facts about today |
| Outcomes | `G-01` | Outcomes and how they are measured |
| Scenarios | `SC-01` | What happens, step by step, with variations, exceptions, and failures |
| Requirements | `R-01` | What a person must be able to do or have |
| Rules | `BR-01` | Policies, calculations, approvals, regulations |
| Constraints | `K-01` | Required conditions, preferences, examples, and delegated decisions |
| Assumptions and risks | `A-01` | Beliefs the need rests on, risks, dependencies |
| Out of scope | `X-01` | What is left out, deferred or rejected, with why |
| Open questions | `Q-01` | What is not yet known or decided, with who can close it |
| Conflicts | `CF-01` | Where people disagree |
| Owner considerations | `OC-01` | Owner only: commercial, feasibility, and risk observations |
| Interviewee questions | `IQ-01` | Owner only: questions the interviewee asked that the owner must answer |
| Choices | `CH-01` | Alternatives the customer is asked to pick among |
| Delta | existing IDs | What changed since the previous reconciliation |

IDs are stable for the life of the interview: retire and add, never renumber, never reuse an ID for another meaning. Choice options keep their letters for as long as the choice lives.

## Evidence entries

```markdown
- [E-14] s2 00:12:31 | speaker=P-02 Layla, operations lead (as stated) | channel=voice | kind=said | "كل طلب لازم يوافق عليه المدير قبل الشحن" | gloss: every order needs the manager's approval before shipping
- [E-15] r1 page | speaker=P-02 | channel=document | kind=reaction:not-quite | on=SC-03.4 rev=2 | at=2026-10-16T09:12 | comment: "Only orders over 500"
- [E-16] s1 00:31:02 | speaker=P-01 | channel=material | kind=shown | materials/M-03-order-sheet.png | what it shows: the paper order form, five fields
- [E-17] context | speaker=owner | channel=document | kind=written | notes from the owner's first call | "They take orders by phone, Instagram, and walk-in"
```

The first field says where it came from: a session (`s2`), a round (`r1`), or prior context. `channel` is voice, chat, document, or material. `kind` is said, written, shown, drawn (a visual made during a session, saved in `visuals/`), comment, reaction (right, not-quite, reopen), choice, approval, flag (unclear, missing), or answer. Quotes stay in the language used. Feedback on a page records the reader as Dossier names them, or `speaker=unidentified` for pasted feedback nobody can attribute, its time, and the `rev` of the item it was given on; unidentified feedback cannot confirm or approve anything until the customer confirms it.

## Items

Every entry in the lists from Language to Choices carries the fields below. Its ID is also what people say aloud to point at it.

- `lifecycle`: current, or retired, naming what replaced it or why it went. Open questions and choices are open or closed, naming what closed them.
- `status`: what the evidence supports.
  - **stated:** the person it concerns said, wrote, or showed it.
  - **inferred:** a reading of yours or someone else's, not yet confirmed by the person it concerns, such as the owner's summary of what the customer wants.
  - **proposed:** you suggested it; it stays proposed until confirmed, and silence is not confirmation.
  - **confirmed:** the person agreed to a playback, a drawing, or the document's account of it.
  - **decided:** someone with authority decided it; name them.
- `review`: `none`, or one or both of `disputed=Q-nn` and `reconfirm`. A dispute names the open question carrying the objection; resolve that question before clearing the flag. A content change after confirmation or approval requires reconfirmation of the new revision; clear that flag when the new content is confirmed. The status records what the evidence still supports. While either flag remains, the item must not read as confirmed or approved.
- `rev`: a number raised whenever its content changes; confirmations and approvals record the `rev` they were given on.
- `origin`: interviewee, owner, document, or agent.
- `evidence`: the evidence IDs it rests on.
- `audience`: all, or owner (never shown to the customer). Owner considerations and interviewee questions are always owner.
- `since`: the session or round it arrived or last changed in.

List-specific fields:

- **People:** role, stake, `authority` (what they can decide, as stated or confirmed), whether they took part.
- **Scenarios:** trigger, actors, steps (each with an ID made of the scenario's ID and its number, such as `SC-02.4`, and its own `rev` and status), variations, exceptions and failures, frequency and volume, information used, rules applied, and outcome.
- **Requirements:** statement, `kind` (capability, information, quality, compliance, operational), `holder` (the person or group it belongs to), rationale, `priority` (must, should, could, later), `check` (how they would know it is met), and the scenarios it serves.
- **Constraints:** `force` (required, by whose authority; preferred; example; or delegated to the delivery team, by whom), and the statement in full, however technical.
- **Open questions:** `holder` (this interviewee, a named person, a lookup, or a decision by someone named), `blocks` (the items or areas it holds back), and whether it blocks readiness.
- **Out of scope:** deferred or rejected, and a durable `why`.

## Superseding

A change that keeps an item's meaning raises its `rev`. When a change alters what an item or a choice means, add a new entry that records `replaces=<old ID>` and set the old one's lifecycle to retired. Feedback given on the old entry shows on the new one as needing a fresh answer; it is never matched to something the customer did not see. A choice option whose meaning changes gets a new letter; old letters are never reused.

## Page feedback across sessions and rounds

The requirements page keeps the same path and individual answers form across changes of medium. Reuse its target, `id`, field names, and saved data shape. A separately requested view has its own target, recorded under `documents`.

- Use one JSON field keyed by item ID for reactions (right, not-quite, reopen), choices (including neither), approvals, and flags (unclear, missing). A scenario step uses its own ID. Section feedback uses a stable section key with the IDs and revisions it covers. Record the field's name under `documents`.
- Save each response with its author, time, and the item's ID and `rev` as seen. A section or document approval carries every covered ID and `rev`; it approves only those versions. Retain feedback on earlier revisions, replaced items, and removed option letters, showing it as needing a fresh answer rather than applying it to new content.
- Round answers and notes stay in the same form, keyed by their question IDs, with option letters unchanged while their meanings hold. A question's `about=<ID>` links it to the item; its saved answer also identifies the item revision reviewed, or every covered ID and revision for an approval question. Keep these fields alongside the JSON feedback field, including when conversation resumes and round controls leave the page. Neither medium clears the other's saved answers.
- Use Dossier comments beside each item, with the item ID and `rev` in the anchor, as `visualize-html` describes; keep navigation IDs stable. Section anchors identify the covered item revisions. Existing anchors keep their meanings, so older threads remain attributable to the content reviewed.
- The copyable handoff includes each response's author, time, question or item ID, reviewed revision or section coverage, the content as shown, and the response. Keep round answers, item feedback, and open comments distinguishable. Saving or copying does not deliver feedback to the interviewer.

Read the existing page before revising it, and restore its saved fields before autosave can replace them. A change of medium alone neither changes item revisions nor invalidates confirmations. Verify that both kinds of saved feedback survive a revision and reload.

## Visuals

A visual made during a session is evidence of kind `drawn`, saved in `visuals/`. What the customer confirms in it moves the items it shows to confirmed, like a confirmed playback. The document may redraw it in its own style, keeping what was confirmed.

## Delta

List only IDs with one-line reasons: `+` added, `~` rewritten, `-` retired or superseded, `=` carried over open. Rewrite it at each reconciliation; never append. The document marks the items the delta lists so the customer can check how their words were understood.
