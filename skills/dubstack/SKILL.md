---
name: dubstack
description: Guide the user through the Dubstack skills, explaining what a skill does, where a project stands in its lifecycle, and which skill to use next and why, based on the project's actual state. Use when the user asks what to do next, which skill fits, where the project stands, or how the Dubstack workflow goes.
---

# Dubstack

Find where the project stands, recommend the next step with its reason, and explain any skill the user asks about. Read [the flow](references/flow.md) for the map: what comes before the first project, the on-ramps for new and existing projects, the goal loop, recurring work, and what needs Dossier. Its summaries orient you. Before saying what a skill does, what it needs, or that a step can be skipped, read that skill's own instructions.

## Find where the project stands

Read the project's state rather than asking the user for it, and inspect what bears on their question:

- **The repository:** whether product code exists yet, its checks and CI, the reference sources under `repos/`, a brand skill, branches, and uncommitted work.
- **The project's Dossier tree,** found through its `AGENTS.md` entry, after following the entry's synchronization instructions: the home, the brand, requirements, the architecture, the architecture review's candidates, the goals list, and each open goal's record, including the stage it is in, its next step, and what waits on the user.
- **GitHub:** open pull requests and issues, and the goals they belong to.
- **The user's setup:** whether Dossier is installed and signed in with permission to publish the project's tree or create one, when the next step needs it; and whether their global instructions have an orchestration layer and they keep stack preferences, when the question touches the start of a project.

Outside a project, explain the flow and where to begin.

## Recommend the next step

Place the project on the map: new or existing, the context it has, and the goals in flight.

Work in flight comes first. A goal waiting on the user, an unfinished stage, or a pull request awaiting review usually beats starting something new; say what it waits on.

Then name one next step: the skill, why it fits now, what it needs, and what it leaves for the step after. When several fit, or the user's intent decides between them, give the choice with your recommendation. New work goes to `basecamp`, which records the goal and chooses its route; an open goal's next stage is in its record.

When the recommended skill is not available in this session, say so and how to add it: the Dubstack plugin for the user's agent, or `npx skills add malhashemi/dubstack --skill <name>`. When the next step needs Dossier and it is not set up, guide the user through setting it up before starting that step, as [Dossier setup](references/dossier-setup.md) describes.

When the user wants to go ahead, start the skill here, or give them the message that starts it in a new session when the work deserves a fresh context. The recommended skill does the work and writes the records; the guide only reads them.

## Explain

Answer what a skill does, how stages connect, or why the library is shaped as it is from the skills' own instructions and the flow, at the depth the user asked for.

## Completion

A recommendation is complete when it rests on the project's state as inspected, accounts for work in flight, and names the next step with its reason and prerequisites, checked against that skill's instructions. A step that needs Dossier starts only once `dossier ls` shows write access to the project's tree or membership in a workspace where it can be created. An explanation is complete when it answers the question from the skills' instructions rather than the flow's summaries alone.
