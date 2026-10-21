# Walkthrough brief

Hand this brief to a delegated builder and instruct it to follow `visualize-html`. Fill the `{placeholders}` and keep the rest as written; it is the page contract. Put direction specific to this pull request in `{NOTES}`, or leave it empty. When the work has no outline, drop the outline line and say so in `{NOTES}`: the builder then orders the change by concern and describes verification from what the description and the commits show. Use absolute paths throughout.

---

Build an HTML walkthrough of pull request {PR_URL} at `{PAGE_PATH}` and publish it in the project's Dossier tree. Help readers understand the change before reading the diff and comment as they review it.

Read `visualize-html` in full and follow it, including its Dossier guidance. Use a body page wrapped by the tree's layouts. Declare the pull request description as the agent-readable version with `<link rel="alternate" type="text/markdown" href="pr-description.md">`, so an agent reading the page's link receives the description. Then read:

- the pull request description at `{DESCRIPTION_PATH}`: why the change exists, what changes for users, and what a reviewer must not miss;
- the approved outline at `{OUTLINE_PATH}` and the design it names: the intent, the phases, the checks and their results, and every departure from the plan;
- the complete diff, `git -C {REPO_DIR} diff {BASE}...{HEAD}`, and the surrounding code you need to explain it.

You decide the structure, order, visuals, and wording. Where these sources leave a gap or contradict each other, report it rather than filling it in.

{NOTES}

## What the page must communicate

- **Why, first.** A short opening that a reader who stops there still understands: the problem, what becomes possible, and the size of the change (files, lines added and removed, the head commit).
- **What changes for users,** with the demos in `{DEMOS_DIR}` shown where they explain their change. Embed images and videos by their path relative to the page, so they load on the published page.
- **The ideas the implementation rests on,** before the details they explain.
- **The change itself,** told in groups of files that change together for one reason, such as a new sign-in flow or a storage migration, rather than by folder or alphabet. Order the groups the way the story is easiest to follow: by phase when the outline's phases tell it, by concern when they do not. For each group, explain what changed and why, and show it as a picture wherever one explains more than prose: a flow or sequence diagram, a before and after of the structure, a component or call tree, or an SVG of how the pieces connect. Put the lines that matter beside the explanation, and keep each file's full diff one step away, with a link to the file in the pull request's Files changed view. Every changed file belongs to a group. Where a code shape explains more than the diff, draw a code sketch following `{CODE_SKETCHES_PATH}`.
- **What was deliberately left unchanged,** and why, where a reviewer might otherwise ask.
- **How it was verified:** the outline's checks and their results, and the owner checks still open.
- **Every consequential departure from the approved plan,** with the decision behind it.

Scale the page to the pull request: a mid-sized change needs a handful of sections, not a node for every function. Headers state their point. Write in plain, direct language, and use the project's terms as the glossary defines them.

## Diffs come from the script

Generate the diff data with the bundled script, which preserves file and line addresses and handles escaping:

```
python3 {EMBED_SCRIPT} {PAGE_PATH} --repo {REPO_DIR} --base {BASE} --head {HEAD} --pr-url {PR_URL}
```

For `pr-walkthrough.html`, the script writes `pr-walkthrough-diffs.json` beside the page. It contains `{"base", "head", "pr", "files": [{"path", "oldPath", "status", "additions", "deletions", "url", "diff", "hunks"}]}`. Each file's `status` is added, deleted, renamed, or modified; `url` opens it in Files changed; and `diff` is its unified diff.

`hunks` holds the same diff as `{"header", "lines": [{"kind", "old", "new", "id", "text"}]}`. A line's `kind` is added, removed, or context. Its `id` follows GitHub's addressing: `R12` for line 12 of the new version, or `L7` for a removed line 7 of the old version.

Load the JSON relative to the page with `await (await fetch('pr-walkthrough-diffs.json')).json()`. Use `fetch` because `dossier.read` returns at most 1 MiB of a file and diffs can be larger. The data leaves presentation to you: show files, hunks, or line ranges wherever they help explain the change.

Rerun the script when revising the page. It replaces the data file and lists every changed file; use that list to check page coverage. `--max-lines N` shortens each file's diff, which helps with large generated files such as lockfiles. If the payload exceeds Dossier's 50 MiB limit, the script exits with an error and leaves the previous file unchanged. Rerun successfully before publishing the revised walkthrough.

## The reader's review

The owner reviews the pull request on this page. Let them comment on any line of a diff, on a range of lines, on a file, and on a section of the walkthrough, and leave an overall note. Follow `visualize-html` for how comments attach, persist, and come back; the addresses they carry are fixed here, because the owner copies them into a new session that works from the repository, not from this page:

- Store line and range comments by comment ID in one JSON field of a `<form action="review/">`. This keeps each person's comments in their own response file. Use Dossier comments for files, sections, and the overall review.
- A line comment is addressed by its file's path and the line's `id`; a range, by the ids of its first and last lines. Show the quoted line beside the comment.
- Preserve the reviewed `head` commit with every comment. Store it in each line or range comment's entry and encode it in the anchor for Dossier comments, following `visualize-html`'s guidance for comments tied to a version. Earlier comments remain in the handoff with their original head and address; a reused line number does not move them to new code.
- Make the handoff understandable without the page. Start with the pull request URL and current head. Include each line or range comment's author, original head, file, line or range address, quoted code, and text. Follow with file, section, and overall comments, retaining their authors, subjects, and original heads.

## Deliver

- Publish the local copy using the project's `AGENTS.md` commands. If publishing stops on a merge conflict outside the page and its diff data, stop before verifying and report it to the agent that launched you. If Dossier cannot be reached, report the page as unpublished and identify the checks you could not run.
- Verify the published page as `visualize-html` describes. Check diffs on that page because an export omits the diff data file. Confirm that every section and diff renders, every demo displays or plays, and every Files changed link reaches its file. Add comments to a line, range, file, and section, then reload and confirm they reach the handoff with their original addresses and heads. Follow the skill's test-input cleanup guidance.
- Leave opening the page to the agent that launched you.
- Report the page's path and link, and a coverage list: every changed file and the group it belongs to, every phase of the outline, every demo, and every point under Worth knowing in the description, with where each appears. A changed file missing from the list is a defect.

## Revising an existing page

Read the existing page before revising it. Reflect the new commits, preserve its design language and layout by default, regenerate the diff data, and publish and verify as above. Keep the review form's target and `id` unchanged. Preserve saved comments' original heads and addresses, and use versioned anchors for the new content as described above. Present the pull request's current state as one coherent walkthrough.
