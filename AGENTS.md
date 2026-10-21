# Dubstack

Agent skills for the whole development lifecycle. Each skill lives in `skills/<name>/`: a `SKILL.md`, an `agents/openai.yaml` for Codex's interface, and any `references/`, `scripts/`, and `assets/` it needs. The repository is also a plugin: `plugin.json` is the portable Agent Plugins manifest, and `.claude-plugin/` holds Claude Code's manifest and marketplace. Both discover every folder in `skills/`.

## Working on skills

Write or revise a skill with the `skill-writing` skill. Each skill is self-contained: it may name another skill and ask the agent to use it, but it never links to another skill's files or relies on where they are installed. Changes to existing skills keep their intended behaviour unless the change is the point.

A file named `SKILL.md` anywhere below a skill's folder is installed as a separate skill, so templates use another name, as the brand kit's `SKILL.template.md` does.

## Checks

Tools are pinned in `mise.toml`; run `mise install` once. `mise run check` is the full check, and CI runs exactly that. It validates each skill's metadata, links, and Codex interface, the plugin manifests and their shared version, and the stack preferences data, then runs the Python test suites.

## Releases

Pull requests are squash-merged with a conventional title, such as `feat: add a guide skill` or `fix(basecamp): keep the issue label current`. release-please turns those titles into a release pull request that bumps `version.txt`, both plugin manifests, and `CHANGELOG.md`; merging it publishes the release. Claude Code updates an installed plugin only when its version changes.

## Dossier

The maintainer publishes this project's pages to the Dossier tree `personal/dubstack` (project name: Dubstack). Its local copy is `.dossier/` at the repository root, ignored by Git. Run these from the repository root:

1. Before starting work, run `dossier pull --merge personal/dubstack .dossier`.
2. On a new or recovered local copy, write the root `.dossierignore` excluding dot files (`.*`) and `private/` folders at any depth before publishing; it is never uploaded.
3. Publish with `dossier push .dossier personal/dubstack/ -m "<what changed>"`.
4. If the push exits 5, merge again and push. If the merge exits 7, resolve the conflicts it lists, asking the user about any in work the session did not write.
5. Never use `--force` or a plain `dossier pull` into the working copy: both can replace work from another session.
