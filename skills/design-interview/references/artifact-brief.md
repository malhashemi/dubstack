# Artifact brief for the interview page

Hand this brief to a delegated builder, together with the full ledger, and instruct it to follow `visualize-html`. Fill the `{placeholders}` from the ledger and the profile's Page section, putting its page and feedback rules in `{PAGE_RULES}` and resolving bundled reference links to full paths. Keep the rest as written: it is the page contract. Stable question and option identities keep answers attributable. `{DESIGN_DIRECTION}` comes from the product's design system when it has one; otherwise name a direction suited to the artifact and its readers, and the default styles to leave out. For design and glossary profiles, choose a direction that suits a design document rather than a dashboard. Put direction specific to this round in `{ROUND_NOTES}`, or leave it empty. For a later round, send the revision section at the end in place of the first-round delivery section.

---

You are building one HTML page at `{PAGE_PATH}`, published in the project's Dossier tree. It has two jobs at once:

1. It is the living `{ARTIFACT_TYPE}` for `{SUBJECT}`. Over several interview rounds it is revised as answers land.
2. It is the interview surface. The user reads each open question, understands it visually, answers it, adds notes, comments on anything settled they want changed, and hands the result back to the orchestrating agent through a copyable handoff.

Read the `visualize-html` skill in full and follow it. Then read the ledger at `{LEDGER_PATH}` in full. It supplies the page's content: the understanding so far, its sources and rationale, and the questions still open. The page rules below define how its lists appear and any exclusions. It has no document shape on purpose. You decide sections, order, grouping, wording, and visuals; the ledger and page rules decide what must be present. Be creative in how you show it. Where the ledger leaves a gap or contradicts itself, report it rather than filling it in. {CONFIDENTIALITY_RULE}

{ROUND_NOTES}

## The page is the living document

- It reads as one cohesive account of what is known, as if someone designed it on purpose: never a log, a changelog, or a record of which round decided what.
- The page opens with a short overview. Main section headings state their takeaway, like a good slide title ("Capsules run on their own origin, never under the dashboard"), not a topic label ("Origins"). Navigation, supporting sections, and question titles use plain labels. A reader who scans the overview and headings can explain the current understanding without the interview history.
- Lead with the point, then support it. Use a diagram, signature, tree, mockup, or sketch where it explains more than prose, and keep prose short and beside the visual it explains. Aim for the smallest set of visuals that reveals the decisions and tradeoffs. For requirements gathering and brainstorming, apply the same economy to showing the business, ideas, and open questions.
- Use the glossary's terms exactly, and put the glossary where a reader can reach it. When a term needs introducing, use its glossary definition rather than a new one.
- Write in plain, direct language. Paraphrase ledger phrasing freely, keeping every fact; attached artifacts and backticked identifiers are exact and appear as written.
- Structure the file so a later round can rewrite the settled design and replace the open questions cleanly, rather than append: clearly delimited regions, or one data object that drives the render.

## The understanding so far: {SETTLED_TITLE}

Render the ledger's Settled list, or the profile's replacement lists, as the current account, visually rather than as bullet lists. Visuals that often fit: {SETTLED_VISUALS}. Mark the state honestly: {HONEST_STATE}

Group values are hints, not required sections: merge, split, and reorder entries however the document reads best. Every entry required by the page rules, with any artifact attached to it, is visible somewhere on the page.

Render the Out of scope list small and clearly marked as left out, with deferred and rejected ideas apart, so a reader does not take an omission for an oversight. Show the Deferred questions as questions a named later stage takes up, apart from this round's questions. Follow the profile's rules for replacement lists, audience, lifecycle, and feedback:

{PAGE_RULES}

## Round {N}: the open questions

The ledger's Frontier list holds this round's {COUNT} questions. For each question with options, show them so the user sees the consequence of each choice rather than only reading it. A question without options asks for what only the user knows, or for their ideas: give it the context that prompts it, drawn where that helps, and room to answer in their own words. Visuals that often fit: {QUESTION_VISUALS}. Pick the medium per question. A question's `draw-as` is a starting point you may better. A compact side-by-side comparison is fine when it shows consequences; a list of option labels is not. Where the ledger names `compare-on` criteria, compare the options on them visibly.

When a question carries a recommendation, mark its strength (strong, worth exploring, speculative) and reason, visually distinct from a choice the user has made. Show any reason the ledger gives for a missing recommendation; do not add one to a question whose kind takes none.

Render the Not yet list small and clearly marked as not yet on the frontier, each topic hanging off the decisions its `depends-on` names and, when it has a `held` field, marked with the reason it is held for a later round. The shape of the design tree stays visible.

## Answering and handing back

- Each question keeps its ledger ID (`r1-q1` and so on), shows whether it is untouched or answered, lets the user choose an option or write their own answer, and has a note field. Fit the controls to the question; typing a custom answer selects it.
- Use one answers form for the page. Persist every answer and note by question ID, with a chosen option recorded by its letter, following `visualize-html`'s Dossier guidance for saving and restoring form state. Preserve the profile's item-feedback fields alongside round answers, including when the page began in another medium.
- A question with `replaces=` shows any saved answer to the question it replaces as needing a new answer, alongside what the user chose before; so does a saved answer naming an option letter its question no longer has. Such an answer counts as unanswered in the handoff and is never matched to a different option. At page load, read the person's own answers file in the form's target and preserve answers to removed options in a hidden JSON field before autosave can overwrite them. Keep that history across reloads until the user answers again.
- Every displayed settled entry, glossary term, Behaviours and Constraints entry, Out of scope entry, deferred question, and entry of a profile list takes a comment, keyed by its ledger ID, with a way to ask for it to be reopened. Use Dossier comments beside the item, with a reopen stance. Where the profile requires revision tracking, include the reviewed revision in the anchor and handoff while keeping navigation IDs stable.
- Mark the entries and terms the delta lists as added or rewritten, so the user can find and check them first: they are how the agent understood the user's last answers, and the new glossary terms it proposes. The marks belong to the interview, not to the design; each round's page carries only that round's.
- Comments belong to the round. The handed-back block ends it, and the orchestrating agent then resolves every open thread, so the revised page starts without open comments.
- One handoff panel produces a copyable natural-language block that is understandable without the page: the subject and round, then for each question its ID and title, the answer (or "unanswered", with any recommendation), and the note; then each open comment with its ledger ID, the entry as the page shows it, the comment, and whether its author asked to reopen it. Include any additional feedback, authorship, and revision details the profile requires. Preserve authorship so the user's choices remain distinguishable from other people's feedback.
- Show whether the handoff is ready to copy, copied, or changed since it was copied. Saving or copying does not deliver the response to the agent, so nothing on the page suggests it did.

The user may leave for hours and return. Losing an answer, or attaching it to a different question, is a defect however good the page looks.

## Delivery (first round)

- One HTML page, usable without a project setup, which the tree's layouts wrap, as the `visualize-html` Dossier guidance describes, unless the page rules say it stands alone.
- The ledger is the page's agent version: name it with `<link rel="alternate" type="text/markdown" href="ledger.md">`, or the ledger's path relative to the page when the page sits in a subfolder, so an agent reading the page's link gets the ledger.
- Readable and answerable on a phone as well as a laptop: every question, option, note field, and the handoff work at a narrow width, and sketches reflow or scale rather than clip.
- Design direction: {DESIGN_DIRECTION}. Make the settled, recommended, and chosen states unmistakable.
- Publish the local copy with the commands in the project's `AGENTS.md` entry before verifying. If publishing stops on a merge conflict outside this page, stop and report it to the orchestrator. If Dossier cannot be reached, report that, with the checks that remain.
- Verify in a real browser before returning: every question renders, a click selects, typing a custom answer selects it, notes and comments on a settled entry and on a term reach the handoff, state survives reload, and the copy path works. Report any check you could not run.
- Open the page's link for the user, unless the orchestrator named another destination.
- Report back: the page path and link, the region layout, the answers form's target and `id`, and a coverage map for every ledger ID: where it appears, where its resolution appears, or the profile, confidentiality, or lifecycle rule that excludes it. This report is for the orchestrator; private IDs and exclusion reasons stay off the page. An unaccounted-for ID or an omission without a governing rule is a defect.

## Revision (later rounds)

Send this section in place of "Delivery (first round)". The builder receives the full current ledger, not a patch.

> The page at `{PAGE_PATH}` already exists. Read it first to learn its design language, its engine, and its region layout, which the ledger's `regions` line also records. Then read the ledger in full: it supplies the current content, subject to the page rules. Compare it with the page; the latest delta may not include changes from intervening conversations or reviews.
>
> Redraw every changed block in the form that now conveys it best, restructuring neighbouring blocks where needed. Replace the round questions with the ledger's current Frontier list and the not-yet tree with its Not yet list. Remove controls for questions that left the frontier, while keeping any open content questions the profile requires. The page's settled account shows no trace that a decision was once a question. Keep the existing style and engine by default; coverage governs the result.
>
> A settled entry whose `artifact=` file does not exist yet came from an option the user chose: save that option's drawing from the current page to that path as a self-contained file before replacing the options. An artifact file stays a complete document, so the tree's layouts never wrap it. Embed every artifact file unchanged wherever its entry appears; never redraw one. A proposed change to an approved design arrives as a new question with its own drawing.
>
> Keep the answers form's target and `id`, `{ANSWERS_FORM}`, every question ID and option letter the ledger still holds, and the profile's feedback fields and revision identities. Saved responses remain attached to what the user saw. Carry answers to superseded questions and options onto their replacements as needing a new answer, as described under answering.
>
> Publish and verify in a real browser as for the first round, including that earlier round answers and any profile-specific feedback still restore. Report the page link, region layout, answers form's target and `id`, and the complete coverage map, accounting for exclusions as for the first round. The result reads as one coherent document.
