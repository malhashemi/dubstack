# Software context and updates

Use the repository and its existing planning or review workflow as evidence. Resolve the relevant change and its relationship to this project; a repository may contain several projects, and a project may span several repositories.

During information gathering, check the repository hosting service for relevant issues, open pull requests, and milestones; these can reveal planned work and unresolved decisions. Prefer the `gh` CLI for GitHub.

`basecamp` owns goal status and declares when a goal is done. Reflect that status from `goals/goals.json` and its `GOAL.md` front matter. If repository evidence conflicts with the recorded status, surface the discrepancy for basecamp to reconcile.

Connect the change to the project: what capability or constraint changed, which decision or requirement it addresses, what was verified, and what remains. Update affected next steps, risks, dependencies, and supporting links. Keep PR-level detail linked unless it is necessary to understand the project. The project's structure need not mirror its branches or PR sequence.

When only a codebase exists, describe demonstrated capabilities and structure. Separate inferred purpose and possible next steps from recorded project commitments. Do not reconstruct an imaginary planning history.

A PR-closing workflow can invoke this skill with the home's link or project context, the change reference, and the outcome evidence. Maintaining the home does not itself merge PRs, close issues, or modify implementation.
