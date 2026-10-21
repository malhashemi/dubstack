---
name: describe-pr
description: Create or update the pull request for finished work, with a concise description, demos of user-facing changes attached to the pull request itself, and an HTML walkthrough for larger changes. Only use when the user invokes this skill by name or an earlier stage's handoff names it.
---

# Describe PR

Create or update the pull request for one piece of finished work so a reviewer understands why it exists, what changes for the people who use it, and the shape of the code before reading the diff. Show user-facing changes on the pull request itself, as images, video, or a terminal transcript, rather than describing them. For a larger change, also produce a walkthrough page the owner reads to follow the change from end to end.

## Inputs

The handoff names the branch, its worktree, the goal's directory, and any issue or approved outline. Without a goal, take the branch from the user and use `pr-<slug>/` at the root of the local copy as the artifact directory, with a short slug naming the change. Work in that worktree. Sync the project's local copy using its `AGENTS.md` commands before reading the artifacts.

The goal's directory in the local copy holds the design and outline, when present, and the `demos/` recorded during verification. Write this skill's artifacts there. Read the outline and every input listed under `design` in its front matter in full. Without an outline, use the branch, issue, demos, and diff. In either case, read the repository's instructions and the complete diff against the base branch, with enough surrounding code to understand the change.

Read `glossary/glossary.json` in the local copy. Use the current terms and this goal's proposals; a proposal takes precedence over the current entry with the same `id`.

Resolve this skill's bundled files against the directory containing this `SKILL.md`, wherever it is installed.

## The pull request

Find the pull request for the branch with `gh pr view`. Uncommitted changes that belong to the work are unfinished implementation: report them rather than publish them, and leave unrelated changes alone. Push the branch when it has commits the remote lacks, and never force-push. When no pull request exists, create one against the repository's default branch unless the handoff names another base, as a draft only when the user or the repository asks for drafts. When one exists, update it: commits since the last description, such as a fix for a failed owner check, are part of what it describes.

Give the pull request a title that says what lands, following the repository's conventions. Open the body with one line of available links: the issue, the goal and stage pages listed at the top of the issue, and the walkthrough when present. Use a closing keyword for the issue only when merging completes it. List each link once and omit the pull request's own URL.

Save the body as `pr-description.md` in the artifact directory, without front matter, and publish it with `--body-file`. Keep these four sections, using "None." for an empty section:

```markdown
<the issue> · [Goal page](<link>) · [<each stage's page, such as PRD or Outline>](<link>) · [Walkthrough](<link>)

## Why

<One sentence: the problem this solves and what becomes possible once it ships.>

## What changes for users

<Each user-facing change, shown with its demo.>

## Worth knowing

- <The things a reviewer must not miss, usually one to three: a migration, a compatibility limit, a deliberate omission, a surprising decision, a consequential departure from the approved plan, or an owner check still open.>

## Change outline

<Code sketches of the change, in the order easiest to follow, with a sentence between them on why the next one matters.>
```

Write as one person to another, in plain words and the project glossary's terms. Draw the change outline from the diff, as the code landed, choosing the smallest set of sketches that shows its shape; read [code sketches](references/code-sketches.md) before drawing one. Verification lists, the full story of the implementation, and the plan's local decisions stay out of the body.

## Show what changes for users

A reviewer judges a change to what users see or do fastest by seeing it. Demos are recorded while the change is verified and saved in `demos/`; `implement-outline` also lists each in the outline's Progress blocks with what it shows. Put each one where it explains its change:

- **Before and after images** side by side in a two-column table, for a change visible in one state, such as a layout, a label, or a new control.
- **A video** for a change in behaviour over time, such as a flow, an interaction, or a transition. Put its reference alone in its own paragraph; anywhere else, GitHub shows a link instead of a player.
- **A terminal transcript, or a request and its response,** in a code block for a command-line or API change. Text shows these better than a recording.

Attach files with `--attach` on `gh pr create` or `gh pr edit` (gh 2.99 or later). Write each reference in the body with exactly the path you pass to `--attach`; `gh` uploads the file and rewrites the reference to the uploaded URL. GitHub accepts PNG, JPEG, GIF, WebP, and SVG images up to 10 MB, and MP4, MOV, and WebM videos up to 100 MB. When updating a pull request, start from its published body and keep the uploaded URLs of demos that have not changed; attach only new or changed files.

When a user-facing change has no demo, show what text can, and name the missing demo in your report.

## Walkthrough for a larger change

A larger change gets a walkthrough at `pr-walkthrough.html` in the artifact directory, published with the tree. It guides the reader through the change before they read the diff. As a guide, a pull request changing about 300 lines or more across five files or more benefits from one; a smaller one reads faster from its description and diff. Judge by how hard the change is to follow as well as its size, and make one whenever the user asks.

Delegate the page. Give a subagent [walkthrough brief](references/walkthrough-brief.md) with its placeholders filled, and instruct it to follow `visualize-html`. Choose its model by the guidance you have for visual design work, and give it enough budget to verify the published page in a browser. You own what the page must communicate; the builder owns presentation and publishes the local copy.

Check the builder's coverage report: every changed file, every phase of the outline, every demo, and every point under Worth knowing must appear. Resolve reported merge conflicts using the `AGENTS.md` instructions, then have the builder refresh and publish the resolved version. Add the walkthrough's link to the body's opening line. Revise an existing walkthrough with the same brief when the pull request changes.

The page is also where the owner reviews the change: they comment on lines, ranges, files, and sections, and copy the comments into a new session that corrects the pull request.

## Publish the artifacts

After finalizing the pull request's body, including attachments and any walkthrough link, save the published body back to `pr-description.md`. Publish the local copy using the project's `AGENTS.md` commands so Dossier holds the same description as the pull request. This applies whether or not the change has a walkthrough.

## Completion

The work is complete when all of these hold:

- The pull request exists for the branch, and its head is the branch's latest commit.
- Its body has the four sections, and every user-facing change is shown by a demo, a transcript, or a sketch, or is named in your report as lacking one.
- Every attachment uploaded: the published body (`gh pr view --json body`) contains no local path, and each video stands alone in its paragraph. A partial upload still updates the pull request, and only the command's exit status shows the failure, so a returned URL is not proof.
- For a larger change, the walkthrough accounts for every changed file, renders in a browser, and is linked from the body.
- The final `pr-description.md` and any walkthrough are published with the local copy. If Dossier cannot be reached, keep the artifacts locally and report them as unpublished, with any verification you could not complete.

## Report

Report whether the pull request was created or updated, its URL, the attached demos, and any user-facing change lacking a demo. Give the saved description's path and, when there is a walkthrough, its link or publication status. Open a published walkthrough for the user. When this run pushed commits to an existing pull request, say that the new revision needs `babysit-pr`.
