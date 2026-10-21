---
name: upstream-source
description: Choose, install, pin, or update open-source repositories as local references for coding agents and configure project guidance. Use for a named upstream repository or to select sources from a project's architecture and dependencies.
---

# Upstream Source

Install or update an upstream repository, record its revision, and configure the host project to use it as reference material. Default to a Git subtree under `repos/<name>/`. Follow an existing reference-directory convention when present.

This skill performs setup and maintenance. Inspect metadata and file locations needed for that work; leave API research, source searches for coding questions, and pattern extraction to later tasks following the installed `repos/AGENTS.md`. Do not upgrade the application's dependency as part of a reference update.

<important if="the user asks which upstream sources the project should have, rather than naming a repository">
Read [choosing sources](references/choosing-sources.md) and agree the list with the user before installing anything. It covers what to read, which libraries earn a local reference, and how each chosen one goes through the steps below.
</important>

## 1. Identify the repository and revision

Read the host project's agent instructions, existing reference index, and dependency metadata. Resolve:

- The canonical upstream Git URL and a short local name.
- The reference root and destination, normally `repos/` and `repos/<name>/`.
- An explicit release tag, branch, or commit to import.
- The corresponding package or tool version, if applicable.

Use the requested revision. Otherwise match the resolved dependency version in the lockfile or equivalent metadata. For a repository with no associated dependency, use a suitable stable release unless the task calls for development-branch source. Verify package-specific monorepo tags; do not assume a repository's default branch matches the installed package.

Reuse an existing reference instead of creating a duplicate. If it uses a submodule or separate checkout, preserve that acquisition method unless conversion was requested. Record a known version mismatch; ask only if the repository or revision cannot be chosen responsibly.

For a subtree, continue through steps 2–4. For another acquisition method, use the corresponding instructions in [operational exceptions](references/subtrees.md), verify its checked-out revision, and resume at step 5.

## 2. Prepare the host repository

Run from the host repository root:

```sh
git rev-parse --show-toplevel
git rev-parse --verify HEAD
git status --short
git subtree -h
```

The subtree help command may exit nonzero after printing usage. Require an existing host commit, no operation already in progress, and a clean index and tracked working tree before importing. Check for untracked or ignored files at the destination too. Perform the subtree operation before editing the integration files in step 5.

Subtree operations create commits. Use existing task authorization and the host's commit policy. Do not stash, commit, reset, or discard unrelated user work to clear the way. Read [operational exceptions](references/subtrees.md) if the worktree is dirty, the destination already exists unexpectedly, commits are disallowed, or the existing reference uses another acquisition method.

## 3. Fetch and add or update

Set these values for the actual repository. The URL and tag below are placeholders to replace, not defaults to run:

```sh
upstream_url='https://host.example/owner/project.git'
upstream_ref='refs/tags/v1.2.3'
reference_root='repos'
upstream_name='project'
reference_prefix="$reference_root/$upstream_name"
```

For both initial setup and every update, fetch the selected ref and resolve it to a commit. Stop if either command fails:

```sh
git fetch --no-tags "$upstream_url" "$upstream_ref"
upstream_commit=$(git rev-parse --verify 'FETCH_HEAD^{commit}')
```

For a **new subtree**, require that the destination does not exist, then run:

```sh
git subtree add --prefix="$reference_prefix" "$upstream_commit" --squash
```

For an **existing subtree**, confirm its URL and prefix against the reference index and its subtree history, then run:

```sh
git subtree merge --prefix="$reference_prefix" "$upstream_commit" --squash
```

If both the recorded commit and imported tree already match, skip the merge and repair only missing integration. Fetching first makes the exact revision available for inspection and records a commit even when following a moving branch. For commit-only inputs, annotated-tag compatibility, or conflicts, use the operational exceptions reference.

## 4. Verify the imported tree

Run:

```sh
git rev-parse "HEAD:$reference_prefix"
git rev-parse "$upstream_commit^{tree}"
git status --short -- "$reference_prefix"
git ls-files --stage -- "$reference_prefix"
```

For an unmodified whole-repository subtree, the two tree IDs must match and the prefix must have no working-tree changes. Verify that actual source files are tracked rather than only a `160000` gitlink. Preserve upstream license and attribution files. Account for upstream submodules or large-file pointers using the operational exceptions reference when present.

## 5. Write the project integration

Update these files after the Git operation succeeds. Substitute the actual reference root in all paths and preserve unrelated entries and instructions.

| File | Required change |
| --- | --- |
| `repos/README.md` | Add or update this repository's source record, using the fields below. |
| `repos/AGENTS.md` | Install or merge the bundled source-use and pattern-writing instructions. |
| Root `AGENTS.md` | Add a task-specific pointer that makes agents working on application code read `repos/AGENTS.md`. |
| Existing editor and tool configuration | Exclude reference source from application discovery where needed, following step 6. |

In `repos/README.md`, record the local path, canonical URL, selected ref, full resolved commit, related dependency version, and reason for the revision choice. Include any mismatch or missing source, verified locations of upstream guidance such as `LLMS.md`, and links to existing pattern notes. Locate guidance files without investigating library APIs.

Include a runnable refresh block for this repository: the `git fetch`, commit-resolution, and `git subtree merge` commands from step 3 with its actual URL, ref, and prefix. State that the commands run from the host root with a clean tree, and that provenance must be updated afterward. Use portable project-relative paths rather than machine-specific paths.

Use [the bundled repos/AGENTS.md content](assets/repos-agents.md) when creating `repos/AGENTS.md`. When the file exists, merge the relevant sections without deleting other repositories' guidance. Adapt its reference and pattern paths to the project; default pattern storage is `repos/patterns/<repo>-<topic>.md`, outside imported trees. Keep the installed instructions self-contained: future coding agents must not need access to this skill's files.

In the root `AGENTS.md`, add or update a concise pointer like this, replacing the library and paths:

```md
When working with <library>, read [repos/AGENTS.md](repos/AGENTS.md) before
consulting its source or writing code that depends on it. See
[repos/README.md](repos/README.md) for the local source revision, upstream
guidance, and saved patterns.
```

The root pointer is required because tasks that edit application files may not automatically load instructions scoped to `repos/`. Maintain the list of covered libraries as references are added.

When a revision changes, mark existing notes for that repository as needing revalidation in its source record. Preserve their contents and inspected commits. The next coding task revalidates the relevant patterns under `repos/AGENTS.md`; setup does not perform that research or generate placeholder notes.

## 6. Configure host tooling

Inspect existing workspace, compiler, formatter, linter, test, package, and watcher discovery rules. Exclude the reference tree where their globs would otherwise treat it as application code. Do not add it to package workspaces or resolve application imports from it.

For editor settings and access checks, follow [project tooling integration](references/subtrees.md#project-tooling-integration). Merge into configuration already used by the project. Keep source tracked and directly readable by agent tools even when hidden from interactive editor search.

## 7. Finish

Verify source identity, provenance, the root pointer, the installed `repos/AGENTS.md`, and the concrete refresh commands. Check that referenced files exist; an instruction describing where future pattern notes belong does not require creating them now. Run relevant host checks when tooling configuration changes.

Report the source path, selected ref and resolved commit, integration files changed, and verification performed. If work was isolated in another worktree, integrate it through the project's normal workflow when safe and authorized; otherwise identify the branch and outstanding integration explicitly. Completion means the requested source and its project instructions are installed, not that the library has been researched.
