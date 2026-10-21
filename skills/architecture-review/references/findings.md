# Findings and the register

Each pass leaves an account for agents, `findings.md`, and updates the project's register, `candidates.json`. The account holds each candidate's substance; the register lists the passes and holds candidate identities, current status, and decision history. Earlier accounts retain their dated evidence; both pages read current decisions from the register.

## The pass's account

`findings.md` sits in the pass folder beside `reports/`. It is the pass page's agent version, so it stands on its own.

```yaml
---
kind: architecture-review
title: <what was reviewed>
date: YYYY-MM-DD
commit: <the commit inspected>
scope: <the area, in a phrase>
---
```

Cover:

- **Scope:** what was reviewed and why: the area the user named, or the hot spots and the history that pointed to them. Identify the repository and any relevant uncommitted changes inspected, so evidence from the working tree is distinguishable from the recorded commit.
- **Candidates:** one section per candidate, strongest first.
- **Recommendation:** the candidate to take up first and why, or why none is ready to recommend. If the pass found no candidates, say so without inventing one.
- **Earlier candidates:** each earlier candidate in scope and what this pass found: carried forward into the candidates above, gone, still rejected, or unresolved because evidence was unavailable, with its reason. Link to its last substantive account when this pass only records a disposition.
- **Not established:** what the explorers could not settle, and what could settle it.

Head each candidate's section with its ID and a title that names the deepening, in the glossary's terms where it has them, such as "AC-04 Deepen order intake into one module". Then:

- **Revision:** a positive integer, starting at 1 and increasing when the direction or its justification changes materially. Keep it for editorial changes and unchanged carry-forwards; the same ID and revision always mean the same proposal.
- **Modules and files:** what is involved, with paths.
- **Problem:** the friction, with its evidence as paths and line ranges.
- **Direction:** what would change, in plain words. Shaping the interface is the design stage's work, so the direction names none.
- **Left open:** the decisions the direction leaves to the user: always the deepened module's interface, where the seam goes when that is a real choice, and any conflict with a recorded decision.
- **Gains:** in depth, locality, leverage, and testing: what concentrates, what callers no longer need to know, and how tests would cross the new seam.
- **Dependencies:** the applicable lens categories and the testing implications, including checks that stand-ins cannot establish.
- **Strength:** Strong, Worth exploring, or Speculative, with the reason.
- **Deletion test:** its result for each module the candidate calls shallow.
- **Recorded decisions:** any decision in `architecture/` the direction goes against, with that decision's reason as recorded. Omit when there is none.
- **Terms:** any term the direction needs that the glossary lacks, proposed for the goal's design stage to settle. Omit when there is none.
- **Drawing:** what a before and after should show, for the page's builder.

A candidate carried forward from an earlier pass keeps its ID and is rewritten from this pass's evidence. Once a page has collected feedback, preserve the reviewed account before changing a candidate's revision, for example in `revisions/<ID>-r<N>.md`. Include its evidence and inspection basis so an earlier choice can still be understood. A new pass already preserves the preceding pass's account.

## The register

`architecture-review/candidates.json` lists every pass and every candidate. Later passes read it first, so it keeps earlier decisions and the user's reasons even when a candidate is reopened or its friction goes away.

```json
{
  "version": 1,
  "passes": [
    { "id": "2026-10-18-orders", "title": "Order intake", "date": "2026-10-18" }
  ],
  "candidates": [
    {
      "id": "AC-04",
      "title": "Deepen order intake into one module",
      "revision": 1,
      "status": "taken-up",
      "strength": "Strong",
      "raised": "2026-10-18",
      "passes": ["2026-10-18-orders"],
      "decided": "2026-10-19",
      "decisions": [
        { "status": "taken-up", "date": "2026-10-19", "pass": "2026-10-18-orders", "revision": 1 }
      ],
      "work": [{ "goal": "order-intake" }]
    }
  ]
}
```

The top-level `passes` list records each pass's folder name as `id`, its `title`, and `date`, including passes with no candidates. A new register starts with empty `passes` and `candidates` lists.

Each candidate has:

- `id`: `AC-` and the next free number, never reused. A candidate raised again keeps its ID.
- `title`: as in its latest account.
- `revision`: the current proposal revision, as defined above.
- `status`, one of:
  - `open`: raised and not yet decided;
  - `taken-up`: the user chose to pursue it; this does not establish that basecamp has created a goal;
  - `deferred`: worth doing, not now;
  - `rejected`: not to be suggested again while its reason holds;
  - `gone`: the friction no longer exists in the code.
- `strength`: from the latest pass that raised it.
- `raised`: the date of the pass that first raised it.
- `passes`: every pass folder it appeared in, oldest first. The last holds its latest account or disposition, with an anchor for its ID.
- `reason`: any reason the user supplied for the current decision, or the evidence that established `gone`. Omit an unstated reason; never supply one on the user's behalf.
- `decided`: the date of the current status, for every status but `open`.
- `decisions`: the user's choices in order, each with `status`, `date`, the reviewed `pass` and `revision`, and `reason` when supplied. Append new choices rather than overwriting earlier ones; rereading the same feedback adds no decision and does not override a later choice.
- `work`: links established by records that cite this candidate's ID. Each entry names a `goal` slug, or a `url` for an issue or pull request on basecamp's route without a goal record. Keep every link when work is split. Omit or leave empty until such records exist. A link establishes an association; the linked work's scope determines whether it covers the current revision.

Untouched candidates keep their status and decisions. Reopening a rejected or gone candidate sets it to `open`, clears the current `reason` and `decided`, and preserves earlier decisions and work links. Explain the reopening in the new account. If a taken-up candidate changes materially, preserve its earlier choice but return the current proposal to `open` until the user chooses that revision. Never treat a saved choice on an older revision as approval of the new one.
