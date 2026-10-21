# Set up the project's Dossier tree

An interview can be the project's first published work. Keep one tree for the project; `project-home` can adopt it later and build the home.

## Find or create the tree

Use the tree named in project context or `AGENTS.md`. If none is recorded, check `dossier ls` for an existing project tree before creating one; ask when several candidates fit.

For a new tree, recommend a workspace where the user can create trees, a tree name derived from the repository using lowercase letters, digits, and hyphens, and root sharing with `workspace` at `write`. Honour the user's choices; share with `anyone` only when asked.

Keep the local copy in `.dossier/` in the repository's main checkout, the first entry in `git worktree list`, and add `.dossier/` to `.gitignore`. Before the first publication, write a root `.dossierignore` that excludes dot files (`.*`) and `private/` folders at any depth. The ignore file is never uploaded, so write it again on every new or recovered copy.

The first publication creates the tree and applies the chosen sharing: `dossier push <local copy> <workspace>/<tree>/ -m "<what changed>" --share <target>:<role>`.

## Recover a local copy

Pull the existing tree into an empty folder at its recorded location with `dossier pull --merge <workspace>/<tree> <local copy>`, then recreate the root `.dossierignore` before publishing. A pull cannot restore that file.

## Record how to continue

After the initial push, record the project name, tree address, and local copy's path in the project's `AGENTS.md` before delegating further publication to a builder. For an existing tree, record them before starting work. Include these commands with the project's paths filled in:

1. Before starting work, run `dossier pull --merge <workspace>/<tree> <local copy>`.
2. On a new or recovered local copy, write the root `.dossierignore` excluding dot files and `private/` folders at any depth before publishing; it is never uploaded.
3. Publish with `dossier push <local copy> <workspace>/<tree>/ -m "<what changed>"`.
4. If the push exits 5, merge again and push. If the merge exits 7, resolve the conflicts it lists, asking the user about any in work the session did not write.
5. Never use `--force` or a plain `dossier pull` into the working copy: both can replace work from another session.

Keep any existing project checks in its publish commands. `project-home` adds its own page and glossary guidance when it adopts the tree.
