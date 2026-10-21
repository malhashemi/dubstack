---
name: stack-preferences
description: Look up, refresh, and change the user's preferred technologies for each category of a project's stack, from tooling and frameworks to hosting, native apps, and games. Use when choosing or recommending technology for a project, or when the user states or changes a stack preference.
---

# Stack Preferences

The user's stack preferences are data. For each category of technology decision they hold the choices the user prefers in order, the condition each applies under, options to avoid, the reason, what would set the preference aside, and when it was last decided and last reviewed. They are preferences, not decisions: a project starts from them as the user's stated intent, and its own requirements can set any of them aside. They name tools, not versions; a project resolves and pins versions when it is set up.

Work with the data only through `scripts/prefs.py` (Python 3, standard library), run as `python3 <skill-dir>/scripts/prefs.py <command>`. It merges three layers, each a `preferences.json` of categories keyed by ID:

- **base**: shipped with this skill in `data/`, replaced whenever the skill updates;
- **global**: the user's own overrides, in `~/.agents/stack-preferences/`;
- **project**: a repository's overrides for its team, in `.agents/stack-preferences/` at its root.

A project's field wins over a global one, which wins over the base. A layer that sets a category's choices brings its own review date; otherwise the most recent review wins. Overrides belong to whoever wrote them, and a skill update never touches them.

## Look up

Read only what the decision at hand needs:

- `index` lists every category with its first choice; `--layer` narrows it to one layer.
- `get <id>...` returns full entries.
- `list --layer <layer>` returns every entry in a layer.
- `search <term>` finds the categories that mention a tool.
- `scope` gives the languages the preferences cover and what is left to each project.

Present a preference with its choices in order, their conditions, and its reason. Check its `override_when` against the project's requirements: when a requirement meets it, the choice is open, with the preference as one option and the requirement as the reason it may not fit.

When a project sets a preference aside, log it with `override <id> --project <name> --reason "<why>"`. When `overrides` shows a category set aside across several projects, suggest reviewing that entry with the user.

## Keep it current

An entry is stale when it was last reviewed more than 90 days ago; `get` and `index` mark it, and `stale` lists every one. `stale --triggers` adds entries whose `revisit_when` names something that may have happened since. Changing a decision does not review it, so an entry stays stale until a refresh.

Refresh a stale entry before relying on it. Start a researcher, chosen by your guidance on models and delegation, with [the refresh brief](references/refresh-brief.md) and the entries from `get`. Group related entries into one researcher and run independent groups in parallel. It checks from primary sources whether each preference still suits, and reports:

- **Findings:** what bears on the preference, such as a deprecation, a licence or ownership change, or a `revisit_when` event that has happened. Tell the user the material ones, with their sources. They inform the user's decisions and are not written into the entry.
- **Proposals:** a change to the choices, their order or conditions, the avoid list, or a new option worth ranking is the user's decision. Show each with its reason, the deciding criterion, and the evidence behind it, and write only what the user accepts, with their reason.

Write an entry's `checked` date once the checks needed to assess it are complete, whether or not anything changed. If missing evidence prevents a conclusion, report the gap and leave its date unchanged.

A preference the user states in conversation, such as "from now on, Biome over oxfmt", is written the same way, with their reason.

## Write

Write with `apply <patch-file>`: a JSON file holding `categories` keyed by ID, with only the fields that change. Read [the entry fields](references/entry.md) before writing one. The script validates the patch, dates changed decisions, and keeps replaced choices in the entry's history; `checked` changes only when the patch sets it.

`apply` writes to the layer `paths` reports as `default_write_layer`: the base when this skill's data is tracked in a Git checkout, which is its maintainer's working copy, and otherwise the user's global layer. Pass `--layer project` when a change is for one repository and its team. `validate <patch-file>` takes the same `--layer` and checks a patch without writing it.

## Completion

A lookup is complete when every category the decision touches has been retrieved, no stale entry was relied on without a refresh, and each preference's `override_when` was checked against the project.

A refresh is complete when the requested entries have been reviewed, their `checked` dates are written, and material findings and proposals have been reported. Pending proposals leave the user's choices unchanged.

A change is complete when the user has accepted every change to a choice, `apply` has written it to the intended layer, and `validate` passes.
