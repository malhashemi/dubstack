# Goal record

`GOAL.md` is the entry point for agents working on a goal. Every stage reads it; only `basecamp` writes it. Keep the record as an index: summarize each stage's output in one line and link to its artifacts, where the detailed decisions and findings belong. Describe the goal in its own terms and let each stage structure its documents.

Retain every section below. Write "None." in empty sections so readers can distinguish an empty section from an omission.

The goals page, project home, and command palette read the YAML front matter at runtime. Use values, lists, and one level of nesting so the shared parser can read it. Keep these fields synchronized with their corresponding sections:

- `waiting`: one short line for each item in Waiting on the user. Double-quote each line so colons are treated as text. Use `[]` when there are no items.
- `pages`: every page linked from Stages, with a descriptive title and a path relative to the goal directory. Use `[]` when there are no pages.

````markdown
---
stage: <the stage the goal is in or waiting for>
next: <the step after it>
waiting:
  - "<one short line for each item under Waiting on the user>"
pages:
  - title: <what the page is, such as PRD interview>
    path: <its path relative to the goal's directory>
repository: <absolute path of the repository>
issue: <URL of the GitHub issue, or none, with the reason>
directory: <absolute path of the goal's directory>
page: <absolute path of the page, index.html in the goal's directory>
link: <the goal page's Dossier link>
related: <paths of the records of goals this one was split from or into, or none>
---

# <What the goal achieves, in a few words>

## Goal

<What is true when the goal is done, for whom, and why, in two or three sentences.>

## The request

<Everything the user asked for, as they meant it, in the glossary's terms.>

## Scope

- In: <what the goal covers>
- Out: <what was set aside, and why>
- Must hold: <what the user requires, such as a platform, a library, or a limit>

## Context

References for later stages to consult, not decisions: a stage that relies on one decides what it establishes.

- <What it is> · <its link, its path, or its copy in context/> · <what the user said it is for>

## Open

- Fact to find: <a precise question about how things are, for research or the stage that needs it>
- Decision for the user: <a precise question only the user can settle, for the design stage>
- Not yet clear: <an area that will need decisions but cannot yet be put as a precise question>

## Waiting on the user

- <What the goal needs from the user now.>

## Stages

- <YYYY-MM-DD> · <stage> · <path of each artifact, and of its page when it has one> · <what the stage produced, in one sentence> · next: <step>, because <reason>
````

## Keeping the record true

- **The request** stays complete and current, changing as the user adds to or changes what they want.
- **Out** stays out. Something set aside returns only when the user redraws the goal, and then Goal and Scope change with it.
- **Open** holds a question under Fact to find or Decision for the user only once it can be put precisely; until then it sits under Not yet clear. When a stage settles an item, remove it: the stage's artifact holds the answer. When one becomes precise, move it.
- **Stages** is history. Add an entry when a stage finishes, and leave earlier entries as they were written.
