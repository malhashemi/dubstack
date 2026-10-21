# Architecture review page brief

Build an architecture review's pages for the project's owner and team, and publish them in the project's Dossier tree. Use `findings.md` and the reports beside it as the source for the pass page, and `candidates.json` for the register; leave those files unchanged. Read [findings and the register](findings.md) for the data and revision contract. Follow `visualize-html` for presentation and verification, including its Dossier guidance.

## The pass page

Write `index.html` in the pass folder, a body page wrapped by the tree's layouts. Declare `findings.md` as its agent version with `<link rel="alternate" type="text/markdown" href="findings.md">`. If a page already exists there, change what the account changed, and keep its design language and layout.

The first screen says what was reviewed, when, at which commit, and whether relevant uncommitted changes were included. Show the recommendation linked to its candidate, or the account's explanation that none is ready. A pass with no candidates still has a page showing its scope, result, and limitations.

Each candidate is one item, with its ID as the element's `id`:

- **The before and after drawing carries the weight.** Draw what the account's drawing idea describes, in the form that best shows its friction and proposed deepening. A dependency graph, a call graph collapsing into one module, a cross-section of the layers a call passes through, or an interface drawn against the implementation it hides are starting points, not a menu. Make the relationship understandable from the drawing and concise labels; choose variety only where it helps. Draw modules, seams, leaks, and deep modules the same way in every drawing, with a small legend on the page, so each drawing reads like the last. Label the after as proposed and keep it at the account's level of detail, leaving interface design to the goal.
- **Prose stays sparse:** the problem and the direction in a sentence each, and the gains as short lines.
- Strength and dependency categories read at a glance; limitations and deletion-test results stay accessible with the evidence.
- The modules, files, and evidence are within reach without crowding the drawing. Link repository files through their remote host at the inspected commit and lines when available; identify uncommitted evidence without presenting a commit link as its exact source. Use relative links for tree files and plain text for machine-local paths.
- A conflict with a recorded decision stands out, with that decision's reason.
- Proposed terms are marked as proposals.
- The decisions a candidate leaves open are visible beside its direction, so the owner sees what the design stage will settle before taking it up.

Earlier candidates the pass rechecked appear in a short section of their own, with each disposition and reason from the account. Each candidate has exactly one stable ID anchor: link carried-forward entries to their full candidate section, and put the anchor on the disposition for those not proposed in this pass. Preserve links to earlier accounts and reviewed revisions. Show any inspection gaps from the account.

## The choices

The owner decides on each candidate proposed on this page. Use one form, `<form id="architecture-review-choices" action="answers/">`, with a field per candidate named `<ID>-r<revision>`, offering take up, defer, or reject, and an optional reason field named `<ID>-r<revision>-reason`. Leave new choices unanswered. Keep the form identity and each revision's field names across page updates so saved input stays with the proposal reviewed.

Place `<dossier-comments for="<ID>-r<revision>">` beside a matching revision anchor within each candidate's stable navigation anchor. Build the copyable handoff from choices, reasons, and open threads, as visualize-html's Dossier guidance describes. Include the pass, candidate IDs and revisions, and authorship so the owner’s choices remain distinguishable from teammates' input. Saving or copying does not send the handoff to the reviewing agent.

Show each candidate's current recorded status and reason beside its choices, read live from the register with `dossier.read('/architecture-review/candidates.json')`, and keep earlier decisions accessible. Do not prefill personal answers from the shared status. When this page's revision is older than the register's, show that it was superseded and link to the latest account; its saved answers and comments remain feedback on the older proposal. A failed live read shows status as unavailable, not open.

## The register page

When `architecture-review/index.html` does not exist, build it as well, as a body page wrapped by the tree's layouts. It draws `candidates.json` live with `dossier.read('/architecture-review/candidates.json')`, so it stays current without rebuilding, and declares `candidates.json` as its agent version with `<link rel="alternate" type="application/json" href="candidates.json">`.

It shows every candidate grouped by status, open candidates first. Each shows its title, strength, and latest pass, linked to that pass's candidate or disposition anchor. Show recorded reasons and access to decision history. Link any work recorded for a candidate: a goal links to its page with status read live from `/goals/goals.json`, and an issue or pull request links to its URL. A taken-up candidate without work links is awaiting a recorded handoff result. Keep work links visible when the candidate becomes gone; a missing goal entry means its status is unavailable, not complete. List all passes from the register's top-level `passes` list, newest first, including those with no candidates. Decisions are made on the pass pages, so this page needs no form.

## Deliver

Publish the local copy using the project's `AGENTS.md` commands. If publishing stops on a merge conflict outside these pages, stop before verifying, report it to the agent that launched you, and leave its resolution to that agent. If Dossier cannot be reached, report the pages as unpublished and identify the checks you could not run.

Verify the published pages as `visualize-html` describes, including form restoration and handoff, live reads, and links. On updates, check that saved input remains tied to its revision. Leave opening the pages for the user to the agent that launched you. Return each page's local path and published link, a coverage list showing where every candidate, earlier candidate, and inspection gap appears, and any links or checks that failed.
