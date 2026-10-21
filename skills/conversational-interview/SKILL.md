---
name: conversational-interview
description: Gather a customer's requirements or brainstorm a problem or opportunity through live voice, relayed speech, or turn-by-turn chat. Only use when invoked by name, when a caller connects through a channel set up to run it, when an earlier stage's handoff names it, or to resume, compose, or review such an interview.
---

# Conversational Interview

Hold a real conversation with the people who hold the knowledge or the ideas, and leave behind a record that later work can build on. The **target** defines what the interview is for: what it must discover or establish, whom it serves, who decides, and what completes it. This skill defines how the exchange works: a continuous conversation, contributions captured as they arrive, understanding checked in the flow of talk, and the target's record and artifacts reconciled and composed after each session.

## Targets

- [Requirements gathering](references/requirements-target.md): a customer-facing business interview that understands the customer's business and needs in a form they can recognise, correct, and approve.
- [Brainstorming](references/brainstorming-target.md): exploring a problem or opportunity, developing possibilities, making promising ones concrete, and finding useful directions and open questions.

Use the target the user or the handoff names; when neither names one, recommend one and confirm it. Read the target before the first session: it governs what you pursue, how prior context counts, what the record holds, and when the interview is done.

The same targets run in `design-interview` as visual rounds. An interview can start in conversation and continue there, or the reverse, as described under Changing how the interview runs.

## Who is who

- **The interviewee** is whoever is in the conversation: one person or several, a stranger, a customer, a colleague. Who they are and what they can decide are findings, not premises.
- **The owner** is the person you work for. The owner's standing instructions govern what you may share or promise, what may be recorded, and how far you go on your own. Where they are silent, say you are an AI working for the owner, promise nothing on the owner's behalf, and keep the owner's own considerations out of anything the interviewee sees.

The target says who decides what. Whatever it says, your reading of what someone meant stays a proposal until they confirm it.

## Channels

The conversation runs over whatever the harness provides: live voice, speech relayed as text, or turn-by-turn chat. In voice, keep spoken turns short and never make the person wait on slow work. Research, reconciling the record, and composing artifacts wait until the session ends, unless the target allows otherwise; a visual the interviewee asks to see can be made while the conversation goes on, and the target says whether you may offer one.

## Where the interview lives

The interview keeps one folder in the project's Dossier tree, in its local copy: the folder the target names, unless the owner names another. The project's `AGENTS.md` entry names the tree, the local copy, and the publish commands: bring the copy up to date with them before each session, and publish after each session and each composition.

| Path | What it is |
|---|---|
| `ledger.md` | The target's record: the reconciled, current account of what the interview has established |
| `sessions/<n>/` | Each session's transcript or messages, its live log, and its notes |
| `materials/` | What the interviewee showed or sent, each with an ID |
| `visuals/` | What was drawn during a session, because someone asked or the target allowed it |

Everything in the folder is published for the owner's team unless the target says otherwise; keep what the ledger's confidentiality line holds back from the team in a `private/` folder, which is never published. The target adds what its own work needs, such as a folder for what the interviewee may see.

When the project has no Dossier entry or its local copy needs recovering, read [Dossier setup](references/dossier-setup.md) before publishing. This skill can start the tree; `project-home` adopts it later and builds the home.

## Before the first question

Read what is already known before asking anything: what the owner told you, what the interviewee sent, earlier sessions and rounds, documents, and the project itself. Use it. Nobody should repeat what they have already given just because the conversation has not covered it yet; build on it, and ask where it is thin, ambiguous, contradictory, or needs that person's judgment. Prior context guides the conversation without speaking for the person in it: the target says how it counts until they confirm it.

## During the session

Read [conversation guidance](references/conversation.md) before a session to guide the exchange at the person's pace.

Capture as you go, lightly. Keep the transcript or messages, and append to the session's live log as things arrive: one short line for each contribution, correction, idea, question to come back to, and thread opened or left, in the person's words, with the time and who said it. Appending is cheap, so it never holds up the conversation. Read the log, not the formal record, for the current understanding while you talk. Leave the ledger alone until the session ends: organising, linking evidence, superseding, and checking consistency are reconciliation work, and doing them mid-conversation pulls the talk toward the record's shape.

## After the session

Reconcile the session into the ledger, as the target's record describes: every contribution and correction from the transcript and the log lands as evidence and in the entries it supports, superseding what it changes. The log is a guide to the transcript, not a replacement for it: check the transcript for anything the log missed. Note in the session's notes the threads still open, so the next session can return to them. Then do the target's after-session work, publish the local copy, and tell the owner where things stand, with links.

## Composing and review

The target says what to compose, when, and for whom. Delegate composition to a subagent following `visualize-html`, with the target's brief when it has one, and pick its model by the guidance you have for visual design work. You own what the artifact must say, through the ledger; the composer owns how it reads and looks, and publishes the local copy. Check its coverage report against the ledger. Resolve any merge conflict it reports as the `AGENTS.md` entry describes, then request a fresh composition and publication.

For a revision, give the composer the existing page and its feedback locations, including when the page came from visual rounds. Require it to preserve the form target and `id`, saved field identities and meanings, and comments attached to existing items. Check that earlier responses still restore after the revision.

People can respond to a composed artifact on it, through its feedback, or in conversation. Collect feedback on the page with `dossier read` on its answers and comments, or from a copied handoff block; fold it in as the target describes, then resolve the comment threads you folded in with `dossier comment --resolve`, using their paths from `dossier read --json` on the page's comments, so the next handoff does not repeat them. Who supplied each response stays recorded.

## Changing how the interview runs

An interview can move between conversation and `design-interview`'s visual rounds whenever that serves the people in it, such as a customer who would rather read and answer on a page, or a round of answers that is better talked through. The interview keeps its folder and its ledger; only the interaction changes.

Before handing over, reconcile every session and received page response into the ledger. Hand over the folder's path, the target, the latest reconciled session, the existing page and its feedback locations, and what is outstanding: open questions, threads still open, and anything awaiting confirmation. Keep the page path, form target and `id`, saved fields, and item identities across the switch. `design-interview` keeps the target's record and adds its round entries; a change of medium does not invalidate confirmations.

<important if="the interview continues from design-interview's rounds">
Read the ledger and any page feedback not yet folded in. Apply the target's authority and evidence rules, preserving each response's author, question and option IDs, and any item revisions it names. Record corrections and confirmations in the target's lists, resolve answered frontier questions, and retain unanswered questions and held topics. A recommendation or an untouched control is not an answer.

Ending the visual round also ends its comments: fold every open thread into the ledger, then resolve every thread with `dossier comment --resolve`, using the paths from `dossier read --json` on the page's comments. Preserve the round entries and saved answers when composing the next artifact. Start the conversation from what remains outstanding.
</important>

## Completion

A session is complete when:

- its transcript or messages and its live log are saved, and everything in them is reconciled into the ledger;
- the target's after-session work is done;
- the local copy is published, or the owner knows Dossier could not be reached;
- the interviewee knows what happens next and how to continue.

The interview is complete when the target says so. A long transcript is not a record, and a rendered page is not a confirmed one.

<important if="resuming an interview">
Bring the local copy up to date, then read the ledger, the latest session's notes and log, and any composed artifact. Collect and fold in feedback that arrived since the last session before it starts. Open with what changed since the person last spoke with you, what they flagged, and the threads they left open.
</important>
