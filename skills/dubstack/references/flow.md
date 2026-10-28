# The Dubstack flow

The skills carry a project from its first context to merged work and keep it healthy between features. Every project starts as a folder with Git. Most stages keep their records and pages in the project's Dossier tree; whichever stage runs first creates it, and the others adopt it.

The summaries below orient. Each skill's own instructions govern what it does, what it needs, and when it applies.

## Before the first project

- **`orchestration-setup`** writes the part of the user's global instructions that says which model owns which kind of work and how sessions reach it. Once per setup, and again when a model, harness, or development environment changes.
- **`stack-preferences`** holds the user's preferred technologies per category. The architecture interview and scaffolding read it; the user can review or change it at any time.

## Project context, in any order

- **`project-home`** creates the project's home and shared pages, for a new project or an existing codebase that never had one. Every goal expects a home; basecamp creates one through project-home first when there is none.
- **Requirements:** `design-interview`, requirements gathering profile, or `conversational-interview` when the customer would rather talk it through. Either medium can hand over to the other.
- **Brand:** `brand-skill-generator`, before the requirements when the brand is already known, or after them when what is being built shapes it. When the brand arrives, project-home restyles the tree.
- **Glossary:** `design-interview`, glossary profile, when the business language needs settling before any goal.
- **Brainstorming:** `design-interview` or `conversational-interview`, when a problem or opportunity needs exploring before anyone commits to work.

## A new project

1. **Context,** as above.
2. **Architecture:** `design-interview`, Solution Architecture profile, usually once the context exists. It starts from the user's stack preferences.
3. **Reference sources:** `upstream-source` chooses the open-source repositories the architecture and dependencies call for and installs them as local references.
4. **Scaffolding:** `project-scaffolding` opens a goal that sets up the whole stack the architecture chose, connected end to end, ready for the first feature.
5. **The first major goal,** through `basecamp`: the scope the requirements and architecture describe.
6. **Follow-up goals** for the gaps the first one leaves.

## An existing codebase

1. **Context:** `project-home`, and the brand when there is one.
2. **Safeguards:** `project-scaffolding` opens a goal that brings the checks and CI up to standard and fixes the code until it passes them. Changing the stack itself is design work for `design-interview` first, then a goal of its own.
3. **Architecture:** `architecture-review` finds where the structure makes change harder and proposes deepening; each candidate taken up becomes a goal.
4. **Features,** as goals.

## The goal loop

`basecamp` is the front door for any goal, from a one-line fix to a loose set of ideas. Skills that act on demand, such as a test-suite audit, run without one. Basecamp records the goal and chooses the route by what remains unresolved:

| The goal still lacks | Next stage | Then |
|---|---|---|
| Nothing: the intent is clear and the work fits one session | Do it now | Pull request |
| Facts too large to find along the way | `research` | Choose again |
| Decisions where product and technical choices are entangled | `design-interview`, design discussion | Structure outline |
| An open product framing, or product and technical design large enough to settle separately | `design-interview`, PRD, then TDD | Structure outline |
| Only a plan: nothing left to decide, but several phases | `structure-outline` | Implementation |
| An approved outline | `implement-outline` | Pull request |
| A committed change | `describe-pr`, then `babysit-pr` | Done once merged |

Each stage ends by naming its output for the next stage, and the user returns to basecamp, which records the stage, refreshes the goal's page, and writes the next handoff.

## Between features

- **Architecture:** `architecture-review` over the areas that keep changing; candidates the user takes up go to basecamp.
- **Reference sources:** `upstream-source`, update mode, when a dependency's version moves.
- **Dependencies:** a bot such as Renovate opens the update pull requests and `babysit-pr` carries each to merge readiness. It merges only when requested. A major upgrade that needs code changes becomes a goal.
- **Issues:** each one worth doing becomes a goal through basecamp.
- **Test suite:** `test-suite-audit`, on demand, when the tests or CI cost more than the protection they give. It runs without a goal or Dossier and ends at a pull request of its own, which `babysit-pr` can carry to merge readiness.

## Anywhere

- **`research`** answers questions without a goal.
- **`babysit-pr`** carries any pull request through CI and review, including a bot's.
- **`visualize-html`** makes any visual explanation, comparison, or feedback page.
- **`svg-design`** makes logos, icons, and other vector graphics.
- **`skill-writing`** writes or revises agent skills.

## What needs Dossier

The stages that keep records and pages in the project's tree need Dossier: `project-home`, `basecamp`, `research`, `design-interview`, `conversational-interview`, `structure-outline`, `implement-outline`, `describe-pr`, `architecture-review`, and `project-scaffolding`, which runs as a goal. [Dossier setup](dossier-setup.md) walks through access to an existing deployment or hosting one.

These work without it: `orchestration-setup`, `stack-preferences`, `upstream-source`, `test-suite-audit`, `babysit-pr`, `brand-skill-generator` (its interview runs from a temporary folder), `visualize-html` (local pages), `svg-design`, and `skill-writing`.
