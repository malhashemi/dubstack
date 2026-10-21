# View brief

Render the structure outline as one HTML view for the owner to review, approve, and follow, and publish it in the project's Dossier tree. The outline's Markdown file supplies all content; leave that file unchanged. Follow `visualize-html` for presentation, interaction, and verification, including its Dossier guidance.

Use a body page wrapped by the tree's layouts. Declare the outline as the view's agent-readable version with `<link rel="alternate" type="text/markdown" href="<the outline's path relative to the view>">`, so an agent reading the view's link receives the source outline.

Write to the path in the outline's `view` front matter field. If a view already exists there, change what the outline changed, preserving its design language and layout unless the outline's structure has changed enough that the old layout no longer fits.

## What the view shows

The first screen answers four questions: what lands, which results depend on others and why, what the owner must set up before work starts, and where the work stands.

- The phases in the recommended order, each with its result, stated dependencies and reasons, and progress status. Make independent work recognisable; document order alone is not a dependency.
- Owner Setup before the phases, prominent enough that nothing is discovered mid-run; Plan Verification and its progress after the phases, then Owner Checks. Keep whole-plan results distinct from phase results: verified phases alone do not mean final verification and review have passed.
- For each phase: what it delivers, its connections, its change outline, its contracts, and its verification. Code sketches and contracts render exactly as written, in code blocks.
- Decisions Made While Outlining and Revisions, where a reviewer can find why the plan differs from the design.
- The plan and the progress in visibly different treatments, so a reader never mistakes what happened for what was approved. Before implementation the progress parts say "Not started".

While the outline is a draft, attach Dossier comments to each phase and item using stable IDs based on the phase number and item. Let the reader copy open threads into one feedback message, preserving each author's identity. Keep the IDs across revisions so threads stay attached to their subjects.

## Deliver

Publish the local copy using the project's `AGENTS.md` commands, then verify the published view as `visualize-html` describes. If publishing stops on a merge conflict outside the view, stop before verifying, report it to the agent that launched you, and leave its resolution to that agent. If Dossier cannot be reached, report that the view is unpublished and identify any checks you could not run.

Leave opening the view to the agent that launched you. Return its local path and published link, plus a coverage list showing where every phase, Plan Verification item, Owner Setup item, Owner Check, decision, and revision appears.
