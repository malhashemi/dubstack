# Operational exceptions

Use the add/update commands in `SKILL.md` for ordinary subtree setup. This reference covers acquisition exceptions and host tooling integration.

## Working tree and acquisition

- **Unrelated uncommitted changes:** use a clean isolated worktree when appropriate. Do not move or commit the user's changes. Finish integration through the project's normal workflow when possible and report where the work actually resides.
- **Commits disallowed or no initialized host history:** a subtree import cannot satisfy an uncommitted-only request. Prepare a pinned reference clone outside the host working tree and the proposed integration files instead; report that a tracked subtree remains outstanding. Do not initialize or commit an unrelated repository just to make the command work.
- **Existing destination:** inspect its acquisition method and provenance. Do not replace a directory or submodule with a subtree merely because its name matches. Preserve deliberate local changes. For a clone or submodule, use its recorded remote and pinned revision, check local modifications before updating, and record the reproduction or initialization command alongside it.
- **Repository too large to vendor:** use a pinned external checkout when project constraints require it. Record its location and acquisition commands, and make its availability limits explicit in project guidance.

For a separate reference clone, choose a new destination and verified ref, then run:

```sh
git clone --no-checkout "$upstream_url" "$reference_checkout"
git -C "$reference_checkout" fetch --no-tags origin "$upstream_ref"
upstream_commit=$(git -C "$reference_checkout" rev-parse --verify 'FETCH_HEAD^{commit}')
git -C "$reference_checkout" checkout --detach "$upstream_commit"
```

To update that clone, reuse the fetch, resolution, and detached checkout commands after confirming its working tree is clean. Never use forced checkout to discard changes. For an existing submodule, preserve its host gitlink and `.gitmodules` configuration and update through the host's established submodule workflow.

## Revisions and import failures

- **Commit-only input:** fetch a containing branch or tag, verify the requested commit is available, and import that commit rather than the fetched branch tip. Servers need not allow fetching arbitrary object IDs. Record both the acquisition ref and pinned commit; a refresh command must preserve an explicitly pinned commit until a new target is requested.
- **Prior annotated-tag import:** older subtrees can require a previous tag object to be fetched before merging. Fetch the specific missing upstream tag identified by the subtree history, then retry. The main workflow peels refs to commits before importing.
- **Conflicts or modified subtree:** inspect unexpected differences and preserve intentional changes. Do not blindly choose an entire side. Recover or abort only the operation started for this task, and leave provenance at the last verified revision until the import succeeds.
- **Upstream submodules or Git LFS:** a subtree records gitlinks or pointer files, not necessarily the referenced contents. Record these omissions and acquire required content separately within scope. Do not claim the complete upstream is available offline when it is not.

`--squash` summarizes imported history; the operation can still create a squash commit and a host merge commit. It does not shrink the source tree or guarantee a small fetch. Command details are in the [upstream Git subtree manual](https://github.com/git/git/blob/master/contrib/subtree/git-subtree.adoc).

## Project tooling integration

Editor hiding does not prevent compilers or package managers from discovering a nested project. Apply exclusions only where existing host rules would include the new source. Preserve useful policy checks and unrelated configuration.

For VS Code projects, merge relevant entries into `.vscode/settings.json`, retaining existing JSONC comments, keys, and array entries. Use the actual prefix, or the shared reference root if the whole directory serves this purpose:

```json
{
  "typescript.preferences.autoImportFileExcludePatterns": ["repos/**"],
  "javascript.preferences.autoImportFileExcludePatterns": ["repos/**"],
  "files.exclude": { "repos/**": true },
  "files.watcherExclude": { "repos/**": true },
  "search.exclude": { "repos/**": true }
}
```

Apply the TypeScript and JavaScript settings only where those languages are used. Configure the editor already used by the project; do not add editor-specific files solely because this example exists. Explorer hiding can follow user preference. VS Code documents the workspace format in [User and workspace settings](https://code.visualstudio.com/docs/configure/settings).

Do not use `.gitignore` as a substitute for these settings: it can hide reference files from agent discovery and does not control every tool. Confirm that the agent can open a known file by its explicit local path. If its file-discovery tool inherits editor exclusions, use a direct file tool or a targeted override.

Ordinary clones of a host with a subtree should contain its tracked source without submodule initialization. When diagnosing availability problems, clone the host into a temporary directory and verify this directly; account separately for submodules inside the upstream itself.
