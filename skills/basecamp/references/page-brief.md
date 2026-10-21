# Goal page brief

Render a page that shows the goal's status and gives its owner access to the work produced along the way. Use the goal record and its linked artifacts as the source of truth. Preserve those sources; your responsibility is the page and its layout. Read `visualize-html` for presentation and verification, including its Dossier guidance for pages published to the project tree.

Write to the record's `page` path, normally `index.html` in the goal directory. Use the supplied change summary to update an existing page while preserving its design language and layout. Reorganize only when the goal has changed enough that the existing structure no longer fits.

For Dossier pages, use the tree's shared layout and theme, and maintain the goal's `_layout.html`. That layout gives the goal's pages, including stage pages that inherit it, the goal title, stage navigation with links, and an indication of the current stage. Declare the record as the page's agent-readable version with `<link rel="alternate" type="text/markdown" href="GOAL.md">`.

<important if="the goal is maintained outside the project's local copy">
Keep the page at its recorded local path. Verify it locally and return its path to the coordinating agent for opening; do not publish it to Dossier.
</important>

## What the page shows

The first screen answers three questions: what the goal is, where it stands, and what it needs from the owner now.

- The goal, and what done looks like.
- Where it stands: the stages taken, each with its date and what it produced, the current stage, and the next step with its reason. Later stages appear only as the expected route, visibly tentative, because the route can change after research or when a stage finds something new.
- What the goal is waiting on from the owner, first on the page whenever there is anything.
- Artifacts grouped by stage with descriptive names. Link tree files relative to the page and repository files through GitHub; show other locations as plain paths. Give interview pages, outline views, walkthroughs, and the pull request prominence, and make demos and videos playable in the page.
- Scope, with what was set aside, and the open items, keeping facts still to find, decisions for the owner, and what is not yet clear visibly apart.
- The request, available without getting in the way of the rest.
- What changed in this update, dated.

Preserve the record's distinctions between user intent, established facts, proposals, and decisions. The page supports reading and navigation. Keep decisions and feedback in the stages' own pages and in conversation; the goal page needs no feedback controls.

## Deliver

Publish through the commands in the project's `AGENTS.md` entry. Resolve merge conflicts in the goal's page and layout. If conflicts remain elsewhere, stop before verification and report them to the coordinating agent, which owns their resolution and will request publication again. Also report any merge that changed the goal record so the coordinator can reconcile it and request a fresh render.

After publication, verify the hosted page as `visualize-html` describes and check every link. Leave opening the page to the coordinating agent. Return the page link and a coverage report mapping every stage, artifact, open item, and item waiting on the owner to its location on the page. Identify any broken links.

<important if="Dossier is unreachable">
Retain the page locally and report its path, the publication failure, and any verification that remains unavailable. The coordinating agent carries the outstanding publication into the next handoff.
</important>
