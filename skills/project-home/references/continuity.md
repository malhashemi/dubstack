# Identity and continuity

The project's Dossier tree is its durable home. Treat the local copy as recoverable working files so losing it does not lose project knowledge or create a duplicate tree.

## Find and retain identity

Identify the home by its tree address, `<workspace>/<tree>`. The home page is the root `index.html`. Resolve the tree in this order:

1. an explicit link or tree address;
2. the project's entry in `AGENTS.md`, in the directory where this skill was invoked;
3. existing project context, accessible trees from `dossier ls`, and `dossier search`.

Match the project through its sources and context as well as its name. Adopt its existing tree, including one created by `conversational-interview` or another workflow. Ask if several candidates remain plausible.

After a successful publication, the project's entry in `AGENTS.md` records:

- the project name;
- the tree address;
- the home's link, taken from the push output;
- the path of the local copy;
- the glossary's link, with an instruction for agents working in the repository to read `glossary/glossary.json` in the local copy and use its terms;
- how to publish, with this project's tree and local copy filled in, so every skill and agent working in the repository publishes the same way:
  1. before starting work, `dossier pull --merge <workspace>/<tree> <local copy>`;
  2. on a new or recovered local copy, write the root `.dossierignore` excluding dot files (`.*`) and `private/` folders at any depth before publishing; it is never uploaded;
  3. to publish, run `node glossary/_check.mjs` from the local copy if `glossary/glossary.json` changed since its last successful check; once it passes, run `dossier push <local copy> <workspace>/<tree>/ -m "<what changed>"`;
  4. if the push exits 5, merge again and repeat the publish step, checking any glossary changes brought in by the merge;
  5. if the merge exits 7, resolve the conflicts it lists, asking the user about any in work the session did not write;
  6. never `--force`, and never a plain `dossier pull` into the local copy.

## Create the tree

Run `dossier ls` and recommend:

- a workspace where the user can create trees;
- a tree name derived from the repository name, using lowercase letters, digits, and hyphens;
- sharing the tree's root with `workspace` at `write`, so teammates can publish through the same workflows as well as read and comment.

The user can override these choices. Share with `anyone` only when asked.

Keep the local copy in `.dossier/` inside the repository's main checkout, identified by the first entry in `git worktree list`, so all worktrees use the same copy. Add `.dossier/` to the repository's `.gitignore` if absent. Without a repository, use the user's chosen folder or the OS temporary directory, and record the path.

Create the root `.dossierignore` described in [the project tree](tree.md) before the first publication. The first publication creates the tree, usually with the first draft. Share its root using the selected target and access level: `--share <target>:<role>` on that push, or `dossier share <workspace>/<tree>/ <target> <role>` afterwards.

## Set up a local copy on another machine, or recover a lost one

1. Run `dossier pull --merge <workspace>/<tree> <empty folder>` at the recorded location. Into an empty folder it fills the copy with the tree's files and none of people's data. Never run a plain `dossier pull` into a working copy: it replaces local changes.
2. Write the root `.dossierignore` before publishing anything. It is never uploaded, so a pull cannot bring it back, and without it the next push would publish private files and dot files.

If this fails, report the actual error; do not reconstruct the home from memory.

## Carry maintenance context with the page

Keep a small machine-readable record in a `<meta name="project-home-context">` element, with JSON encoded in its `content` attribute. Its contract is:

- `schema_version`: `1` for this record format.
- `project_refs`: durable identifiers that distinguish this project, where available.
- `sources`: entries with a stable `id`, a retrievable `ref` when available, a `role` explaining what it establishes, and `checked_at` when actually checked.
- `continuity_notes`: project-specific associations or unresolved ambiguities that a future update would otherwise lose.

Use references appropriate for the team sharing the tree. Keep machine-local lookup details in local project context. For material that exists only in the current conversation, preserve the necessary knowledge visibly on the page and record its origin; do not invent a retrievable document.

The record supports maintenance. Project facts, decisions, and their reasons belong in the readable page or linked authoritative records. Avoid duplicating the entire page into a second hidden project model. Escape JSON for an HTML attribute; treat its contents as data. When adopting a page without this record, recover what the evidence supports without fabricating prior history.

## Change history

The latest summary is the home's `#project-home-changes` section. Read it from the local copy before preparing the next update. Compare against the published home, consolidating draft iterations into one summary of the accepted changes. On first creation, describe the starting point. When adopting an existing home without a summary, establish one from the available evidence without inventing earlier entries.

Earlier versions and their summaries live in the tree's history; no separate local changelog is needed.

- `dossier log <workspace>/<tree>/index.html` lists the home's pushes, newest first.
- `dossier diff <workspace>/<tree>/index.html` shows the latest change.
- `dossier diff <workspace>/<tree>/index.html <from> <to>` compares two pushes.

## Preserve concurrent contributions

Keep section and item IDs stable so comments and answers remain attached across updates. Pushes preserve this input, which is stored separately from the page's HTML. Before revising the page, retrieve it with `dossier read` on the page's `index.comments/` and answer folders, and reconcile it with the relevant items.

## Keep the local copy in step

The tree is worked on from more than one machine, and by several sessions at once. Every publication pushes the whole local copy to the tree's root, which then holds exactly the copy's files; people's answers and comments are never touched. Keep the copy in step this way:

1. Before starting work, bring the copy up to date: `dossier pull --merge <workspace>/<tree> <local copy>`.
2. Publish with `dossier push <local copy> <workspace>/<tree>/ -m "<what changed>"`.
3. If the push exits 5 because someone published since this copy last synced, run the merging pull again, then push.
4. If the merging pull exits 7, resolve each conflict it lists before continuing: keep the right lines and remove the markers, or keep one of a binary file and its `.theirs` copy. When a conflict is in work this session did not write, such as another goal's pages, ask the user how to resolve it.

Never use `--force`: it replaces what was published from elsewhere. When the merge brings changes to the home itself, reconcile them with your update, and return the revised result to the user's review.
