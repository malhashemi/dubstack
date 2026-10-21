# Research page brief

Render the research account as one HTML page for its owner and team, and publish it in the project's Dossier tree. Use `research.md` as the source and the reports beside it for detail; leave those files unchanged. Follow `visualize-html` for presentation and verification, including its Dossier guidance.

Use a body page wrapped by the tree's layouts. Declare `research.md` as the agent-readable version with `<link rel="alternate" type="text/markdown" href="research.md">`, so an agent reading the page's link receives the source account.

Write the page to `research.html` beside `research.md`. If a page already exists there, update it: change what the account and the reports changed, and keep its design language and layout.

## What the page shows

The first screen says what was researched, when, and the summary's main points.

- The findings in the account's order, each under the takeaway its header states, with its diagrams, trees, signatures, and code rendered exactly as written.
- Each finding's sources within reach without crowding the reading: the paths, links, versions, and dates. Use relative links for tree files, GitHub links for repository files, and source URLs for external references. Show machine-local paths as text.
- The reports, rendered as part of the page: each one opens from the findings that rest on it and from the list of reports, so a reader drills into an area without leaving the page for a raw Markdown file. Keep them out of the way of the account until a reader asks for one.
- The open questions, each with what or who could answer it, easy to find.
- The as-of date and commit, visible wherever a reader judges how fresh a finding is.

Keep what was observed apart from what was inferred, as the account does. The page is for reading, so it needs no feedback controls.

## Deliver

Publish the local copy using the project's `AGENTS.md` commands. If publishing stops on a merge conflict outside the page, stop before verifying, report it to the agent that launched you, and leave its resolution to that agent. If Dossier cannot be reached, report the page as unpublished and identify any checks you could not run.

Verify the published page as `visualize-html` describes, including its links. Leave opening the page to the agent that launched you. Return its local path and published link, a coverage list showing where every finding, report, and open question appears, and any links that failed verification.
