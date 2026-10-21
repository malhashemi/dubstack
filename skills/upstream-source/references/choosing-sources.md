# Choosing sources

Propose a list, agree it with the user, then install the chosen sources through the main workflow, batching its steps as described below. Judge each library from what the project builds on and from its metadata, release history, and documentation; leave API research to later coding tasks.

## What the project builds on

Read both, each for what it establishes:

- **The code:** dependency manifests and lockfiles, and how widely the code uses or configures each dependency. They establish what the project uses now, and at which version.
- **The architecture,** when the project's Dossier tree has one: the technology and toolchain decisions in `architecture/ARCHITECTURE.md`, and the `technology` and `toolchain` entries of `architecture/ledger.md`, which name every dependency or vendor that would take real work to replace. Find the local copy through the project's `AGENTS.md` entry and follow its synchronization instructions before reading it. The architecture establishes what the project will build on before code uses it.

The architecture was frozen when it was delivered, so where it and the code disagree, the code settles what the project uses now. Distinguish a replaced choice from a dependency the settled architecture calls for but the project has not installed yet.

Read the existing reference index and its "Considered, not added" list, if present. Use the host's reference-root convention throughout; paths below use the default `repos/`.

## What earns a local reference

Recommend adding a library only when all of these hold:

- **The project depends on it in depth.** Its code uses the library's API or configuration extensively, or the settled architecture calls for that depth of use before implementation. Frameworks, the data layer, authentication, UI kits, and central SDKs are candidates; a library reached through one thin wrapper or used for a single call does not qualify on that use alone.
- **Agents are likely to get it wrong without the source.** Look for evidence such as fast-moving APIs, a recent major version that changed familiar patterns, thin documentation, a large surface, or reliance on less-documented parts.
- **Its source is public and reasonable to vendor.** For a very large repository, recommend the pinned external checkout from [operational exceptions](subtrees.md) or skipping it, and say which and why.

Skip small stable utilities and straightforward uses that documentation already supports, and reuse anything already referenced. A monorepo that publishes several packages the project uses is one candidate.

A library on the "Considered, not added" list comes back only when something changed since, such as a new major version or the project now depending on it in depth; say what changed.

## Propose the list

Show one table: each candidate, why it qualifies or not, the revision it would pin, its rough size, and the recommendation, add or skip. Include the candidates you recommend skipping where the user might expect them, so the decision is visible.

For the revision, follow step 1 when the dependency is installed. When it is not yet, as in a new project whose stack is decided but not installed, use the version the architecture names, otherwise the latest stable release, and say so.

Below the table, list existing references whose library the project no longer uses. Removing them is the user's decision.

Every subtree import needs a commit in the host repository. When the proposal includes a subtree and the host has no commit, ask in the same message for the user to make the first commit or authorize an initial commit with its scope stated.

The user confirms or edits the list. Their confirmation authorizes the commits the imports create.

## Install and record

Use the agreed revision as the requested revision. For multiple subtrees, complete steps 1–4 for each source serially before writing any integration files in steps 5–6. Those edits would otherwise make the host dirty and block the next import. Then write the combined integration and run step 7 for every chosen source. Keep the clean-tree safeguards and follow the operational exceptions for other acquisition methods; do not let their host edits interrupt pending subtree imports.

For a source chosen before its dependency was installed, say so in its source record, so the next update matches the installed version. If a source is blocked, retain the verified imports, continue independent work where possible, and report which chosen sources or integration steps remain outstanding. On resumption, reuse verified imports whose revision and tree still match.

After the imports, add each candidate the user declined or deferred to the "Considered, not added" list in `repos/README.md`, with the reason and date. Distinguish a reason supplied by the user from the proposal's rationale. Already-installed sources and approved sources still awaiting installation are not declined candidates.

The choice is complete when every source approved for installation is installed and verified as step 7 describes, and every declined or deferred candidate is recorded with its reason. A confirmed list or a partially installed batch is not completion. Report each installed source as step 7 describes, the candidates left out, and any unused references found.
