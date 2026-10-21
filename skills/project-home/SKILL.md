---
name: project-home
description: Create, publish, and maintain a project's home and shared pages on Dossier. Use to establish a project overview, reflect changes in understanding, decisions, or progress, or maintain project navigation, goal listings, and the glossary page.
---

# Project Home

Make the root page of the project's Dossier tree a dependable entry point for newcomers and returning participants. It should explain the project's purpose, current state, settled decisions, open questions, next steps, and where to find more detail. Let the available knowledge and the project's stage determine how to present that information.

Maintain the project overview and the context needed for future updates. This skill owns the home, the shared layout, theme, and components (the kit), the goals page, and the glossary page; basecamp adds goals to the goal list, and this skill removes them on cleanup. Domain workflows own goals, glossary terms, decisions, requirements, and evidence; bring their contributions into a coherent project view. Use `visualize-html` for presentation and interaction, and the `dossier` CLI for retrieval and publication.

## Establish the project

Identify the project and any existing home from the request, working context, and Dossier. Continue the existing home when one exists. Read [identity and continuity](references/continuity.md) to locate, create, or recover it, maintain its source associations, and keep its local copy in step and publish it. When creating a tree, also read [the project tree](references/tree.md): the initial home includes the kit, goals page, and glossary page.

Start with the material available: a conversation can establish a project just as a brief, investigation, tracker, or codebase can. Derive its purpose and current understanding without requiring a particular document or lifecycle. Ask when ambiguity would change which project or commitments the page represents; use judgment for presentation choices.

Preserve the distinction between intended outcomes, observed reality, proposals, and agreed decisions. A codebase can establish implemented behavior without establishing the business intent behind it. A brainstorming report can establish possibilities without committing anyone to execute them. Missing owners, dates, success criteria, and progress measures remain unknown until supported.

Link to authoritative material and summarize enough to make its relevance clear. Where a decision or piece of project knowledge has no other durable home, retain it here with its basis. Keep detailed material in linked pages when it would overwhelm the entry point; the home should remain sufficient to understand the project and find the next useful detail.

## Continue faithfully

Before editing, bring the local copy recorded in `AGENTS.md` up to date as the continuity reference describes, then read the home's `index.html` in it. It contains the existing content, maintenance context, and latest change summary. Recover a missing copy using the continuity reference. Read answers and comments separately with `dossier read`. If a read fails, report the error and recover access before revising the home; memory is not a substitute for its current contents.

Reconcile new material with that context. Refresh the sources needed to substantiate affected claims, and distinguish what was checked from what is carried forward. An unavailable source leaves a visible gap in freshness, not permission to invent its current state.

Follow the consequences of a change: an outcome may resolve a question, invalidate a plan, expose another dependency, or alter what should happen next. Preserve unaffected knowledge and unresolved obligations, including information that exists only on the page. Keep settled decisions and their reasons discoverable when plans change; distinguish superseded decisions from current ones.

<important if="establishing or updating a software project home">
Read [software context and updates](references/software-updates.md) to gather repository-hosted plans, reflect goal status from basecamp's records, and connect changes to project outcomes.
</important>

<important if="a planning or decision workflow uses the home as its map">
Carry its destination, resolved decisions, open questions, dependencies, and still-unclear areas as supplied by that workflow. Keep stable links to detailed investigations or decision records. Publishing an update does not itself resolve a question or authorize the work. This remains usable without an issue tracker or a particular planning skill.
</important>

## Shape and review the page

Give `visualize-html` the project's purpose, audience, evidence, existing page, design context, and Dossier destination. Explain the relationships the page should communicate and let it choose the layout, diagrams, controls, typography, and color. This workflow owns review and publication; `visualize-html` owns presentation, interaction, and feedback persistence.

Maintain recognizable navigation, item identities, and useful links across updates. Adapt the structure when the project changes enough to warrant it. A refresh should preserve a successful design while making room for new knowledge. No particular tabs, dashboard metrics, or workstream structure are required.

Keep the latest change summary in a visible section of the home HTML with `id="project-home-changes"`. Date it and summarize meaningful changes since the preceding published page, linking supporting evidence where relevant. Earlier summaries remain in Dossier's version history; use [the history convention](references/continuity.md#change-history) when consulting them. Show freshness where it affects interpretation, and choose interactions that support the project's next action.

Before preparing a draft, read [the project tree](references/tree.md) for file placement and preview requirements. Write the home to `drafts/home/index.html` in the local copy and place other changed pages or kit files under `drafts/` as described there. Publish the local copy as the continuity reference describes, so the user can review the drafts with the tree's layouts applied. Draft answers and comments are review feedback attached to the draft; read the published home's input separately.

Inspect every changed page in the rendered draft, including relevant links and changed interactions, before presenting the draft links to the user. Follow this review process for both creation and updates. Incorporate feedback and present revisions until the user accepts the current result. Keep the preview available while awaiting a response; silence is not acceptance.

<important if="the user excludes publication">
Prepare a complete HTML document in the OS temporary directory and use it for local review. Completion is the accepted local page.
</important>

## Publish and finish

Publication is part of the workflow unless the user explicitly excludes it. Once the user accepts the current result, publish without a separate confirmation:

1. Move accepted draft files to the destinations listed in the tree reference and remove local `drafts/`.
2. Publish the local copy as the continuity reference describes.
3. Run `dossier rm <workspace>/<tree>/drafts/` to remove the remaining draft data on Dossier; a push preserves comments and answers.
4. Verify that every changed page matches the accepted result at its published location and that its links and interactions work. Preserve the existing audience and sharing settings unless instructed otherwise.

After successful publication, record the project in the invocation directory's `AGENTS.md`, using the fields in the continuity reference. Create the file if needed, or update the project entry while preserving other projects and unrelated instructions. This entry lets future agents and other workflows find the tree and its local copy.

Completion requires the accepted page at the tree's root, the draft removed, and the project recorded in `AGENTS.md`. The home must reflect current supported understanding, account for the requested changes, and preserve the context needed to continue. A published draft or user acceptance alone does not establish completion. If publication or registration fails, retain the accepted work and report the outstanding step.

Return the home's link, summarize meaningful changes, and identify any unresolved source limitations. Report when the project facts are unchanged.

## Maintain shared pages and data

<important if="the user removes finished goals, the project's brand needs to be applied or updated, or shared pages or the kit need changes">
Read [the project tree](references/tree.md) for the relevant update. Removing finished goals updates `goals/goals.json` and publishes the local copy without a home-page review. Changes to the kit, goals page, or glossary page use the same draft review as the home because they affect the shared project experience. Report the completed change and its link.
</important>
