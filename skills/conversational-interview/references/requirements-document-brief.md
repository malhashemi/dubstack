# Requirements document brief

Hand this brief to the composer with its `{placeholders}` filled, and have it use the `visualize-html` skill. Keep the rest as written: it is the document's contract. Set `{RECORD_FORMAT_PATH}` to the full path of the bundled [requirements record](requirements-record.md). Set `{DOC_PATH}` to `customer/index.html` within the interview's folder, or another file in `customer/` for a separately requested view. If the page exists, including one used for visual rounds, include the "Revision" section and set `{ANSWERS_FORM}` to its recorded answers form target and `id`.

Set `{LANGUAGE}` to the readers' language, with any second language they requested. Take `{DESIGN_DIRECTION}` from the owner's brand or design system when one exists; otherwise leave it to the composer. Put direction specific to this composition in `{NOTES}`, such as the sections a standard layout requires, or leave it empty.

---

You are composing `{DOC_PATH}`: the requirements document for `{SUBJECT}`, as one HTML page published in the project's Dossier tree, in a folder shared only with its readers. Its first readers are the people who described their business and needs. They read it to see whether they were understood, to correct what was not, and to approve it. The owner, who will build it, reads it next, and later the people designing it.

Read the `visualize-html` skill and follow it, including its Dossier guidance. Read the requirements record format at `{RECORD_FORMAT_PATH}`, including its feedback contract, then the ledger at `{LEDGER_PATH}` in full. It supplies the document's content: every person, outcome, scenario, requirement, rule, constraint, assumption, open question, and term, with its status and evidence. You decide the structure, order, wording, and visuals. Show every current item whose `audience` is `all`, including scenario steps, unless the notes narrow the view. Evidence entries and owner-only items stay out. Retired entries are history, and a closed question or choice shows through what settled it. Apply the audience rules to any round questions or delta carried in the ledger too. Where the ledger leaves a gap or contradicts itself, report it rather than filling it in. `{WORK_DIR}/visuals/` and `{WORK_DIR}/materials/` hold what was drawn at the readers' request and what they showed; keep faith with what they confirmed. Readers can open only the page's own folder, so copy into it anything the page shows from elsewhere. {CONFIDENTIALITY_RULE}

{NOTES}

## A document they enjoy reading

- It tells the business and its needs back to the people who own them, as one coherent account: never a record of the conversation, or of how it was collected. Write in {LANGUAGE}, in the readers' own terms. The ledger's machinery stays out of it: evidence IDs, status vocabulary, person codes, and words like "interviewee" or "ledger". Name the document, and each part of it, in words the readers would use.
- Readers should recognise their business at a glance and come away feeling understood. Open with what they want to change, and let headings state their takeaway.
- Their own words, quoted in the language they spoke, can bring a point home.
- How the work happens today and where it fails, the scenarios they picture, and the people involved carry most of this document's meaning. Bring them to life: a process view, a journey, a scenario walked step by step.

## What every reader can find

- **Requirements** are easy to connect to the scenario or outcome they serve. Each shows its ID, since readers and later stages cite `R-nn`, a plain statement, its priority, and how the readers would know it is met.
- **Status, where it matters.** Everything reads as what the readers told us, for their review to confirm, unless it is marked otherwise. Mark in the readers' terms what came from someone else's reading (inferred or proposed), what is disputed, and what is awaiting reconfirmation; when a whole class is pending, such as checks that are only proposed, say so once rather than on every item. A suggestion from the interviewer reads as a suggestion, never as something the readers said. A decision names who made it where that matters to the reader.
- **How binding** each constraint and each piece of volunteered product or technical detail is: required, a preference, an example, or left to the delivery team.
- **What is out,** and what comes later, apart from what is in.
- **Open questions,** phrased as questions to the readers, with who can answer each.
- **Their terms,** within reach.
- **Approval:** what approving this version means, who approves it, and the confirmations and approvals already given, with who gave them and when.

Every section, item, and scenario step shows a short spoken pointer: an item's ID, a step's number within its scenario, or a section's number. The interviewer walks readers through the document by these, and readers point aloud with them.

## Feedback

Readers never edit the document. Offer only bounded feedback, anchored to ledger IDs:

- **Comment** on any section, item, step, open question, or term. Device dictation must work in the field.
- **React** to any item or step: right, not quite, or reopen, each optionally with a comment.
- **Choose** an option where the ledger holds a choice, or "neither" with a comment.
- **Approve** a section, or the whole document.
- **Flag** a section as unclear or missing something.

Follow the requirements record's contract for page feedback across sessions and rounds: versioned comments, item feedback in a JSON form field, approvals tied to the items reviewed, and existing round answers preserved alongside them. Use `visualize-html` for Dossier storage and restoration. The feedback panel produces the contract's copyable handoff, with the subject and composition date, so each response remains attributable without the page. Show whether feedback is saved, ready to copy, copied, or changed since copied.

## Delivery

- A complete HTML document that bypasses the tree's shared navigation, with everything it shows inside its own folder.
- Name the ledger as its agent version with `<link rel="alternate" type="text/markdown" href="../ledger.md">`. Dossier gives the ledger only to readers who can open it; the document's readers get the page's own Markdown instead.
- Readable on a phone as well as a laptop.
- Design direction: {DESIGN_DIRECTION}
- Publish the local copy with the commands in the project's `AGENTS.md` entry. If publishing stops on a merge conflict outside the page's folder, stop before verifying and report it. If Dossier cannot be reached, report that, with the checks that remain.
- Verify the published page as `visualize-html` describes: every item renders with its spoken pointer, visuals and animations play as intended, every feedback control works and reaches the handoff, and feedback survives a reload.
- Report the document's path and link, the answers form's target and `id` and its JSON feedback field name, any ledger gaps or contradictions, and any checks you could not run. Account for every ledger ID in a coverage map: where it appears, where its resolution appears, or the audience, lifecycle, or narrowed-view rule that excludes it. Keep the report agent-facing; private IDs and exclusion reasons stay off the page.

## Revision

> The document at `{DOC_PATH}` already exists. Read it first, then the ledger in full, applying the audience and lifecycle rules above. Compare the two: every item added or retired since, or whose `rev`, status, or review flags differ, has changed, whether or not the latest delta lists it. Recompose what changed, restructuring neighbouring parts where needed, and mark changed items so readers can check how their words were understood; the marks belong to this revision only. Keep the design language unless the notes ask otherwise. Keep the answers form's target and `id`, `{ANSWERS_FORM}`, and follow the record's feedback contract to preserve fields, item and option identities, and revision history. When continuing from visual rounds, round controls can leave the page while their saved answers remain. The result reads as one document. Verify and report as under Delivery, including that both item feedback and earlier round answers still restore.
