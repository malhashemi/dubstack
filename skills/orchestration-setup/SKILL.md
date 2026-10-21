---
name: orchestration-setup
description: Set up or revise the orchestration layer of a user's global agent instructions, covering which model owns each kind of work, when delegation pays, and how each model is reached from their harness or development environment. Use when configuring multi-model delegation, or when a new model, harness, or environment changes the user's setup.
---

# Orchestration Setup

The orchestration layer is the part of a user's global instructions that tells every session which model owns which kind of work, when delegating is worth it, and how to reach each model from where the session runs. Write it for the user's actual setup. Sessions read it on every task, so it states durable decisions in few words and leaves unsaid what a capable agent already knows.

## What to work from

- **The user's current instructions.** Before deciding anything, read the global instructions file of each harness they use, such as `AGENTS.md`, `CLAUDE.md`, or the harness's equivalent, including any orchestration layer already there. Changes build on what exists.
- **The user's setup.** Establish the harnesses they run, the models each can reach and at what effort, how they pay for them, and whether anything sits above the harnesses: a development environment that runs several harnesses, a terminal multiplexer, MCP servers, or scripts that start sessions elsewhere. Inspect what you can, such as configuration folders, installed CLIs, and the subagents and tools available in this session. Ask only what the user alone knows: which models they trust for which work, what they want to avoid, and what they are willing to spend.
- **What the user tells you,** such as a new model to place, a role to change, or a constraint.
- **[The example layer](references/example-layer.md):** one person's layer for a setup with several providers under a development environment. It shows the decisions a layer makes and one way to word them. Take what serves this user and leave the rest; their setup decides the content.

## Shape the layer to the setup

Decide what the user's work needs:

- roles such as implementation, review, research, quick lookups, and driving a running app;
- the model and effort that owns each role, fallbacks for when a model is unavailable, and models to avoid;
- when delegation pays for itself;
- how a delegated task is briefed.

Prefer a reviewer that did not build the work, from a different provider when the setup reaches one.

Say how each model is reached from where the session runs:

- **Within one harness:** its own subagents, when they can run the role's model at the role's effort. A harness that already reaches every model the user wants needs nothing more.
- **Across harnesses:** the route the setup actually has, such as a development environment's delegation tool, a multiplexer's sessions, or an MCP server. Name the tool and what a session must select when it uses it.
- **When nothing reaches a model:** the role falls back to what can be reached, and the layer says so.

Recommend no tool the user does not already use. When the setup cannot fill a gap, tell the user what would fill it; adopting anything new is their decision.

When a new model arrives, place it within the existing layer: the role it should own, a fallback it could serve as, or no role, and what changes for the models around it. Find out what you need about it, such as its strengths, cost, and how the user can reach it.

## Write it

Write to the global instructions of the harnesses the user chooses, in each file's own format. Give each file the full text it needs rather than a pointer to another file, and keep what is particular to one harness, such as how its subagents select a model, in that harness's file only. The orchestration layer is all this skill changes; leave the rest of each file as it is. Show the user the change before writing it.

## Completion

The layer is complete when:

- Every role the user's work needs has a model and effort, with its fallback and any exclusions stated.
- Each role has a reachable model at its assigned effort, or a stated fallback that can run it. Confirm the routes through the subagents and tools actually available. Excluded models need no route.
- Each target file holds the layer in full, the rest of each file is unchanged, and the user approved the change.
