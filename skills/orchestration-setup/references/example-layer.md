# An example orchestration layer

This is one person's orchestration layer: sessions run inside an agentic development environment that can start a child task on any of their harnesses, with models from three providers. Angle-bracketed placeholders stand where their models, environment, and tools are named. Read it for the decisions such a layer makes and how it words them, not as a form to fill: a setup with one harness, a different fleet, or no environment on top makes different decisions.

---

## Models for delegated work

Every session runs inside <development environment>, which can start a child task on any harness and model. Use the main thread, subagents, delegated tasks, or workflows as the task warrants; each delegated seat goes to the model that owns that role below.

### Roles

- **<Implementer>** (`<model id>`) is the main worker for delegated work: implementation, UI, backend, writing, and final synthesis. It owns the result. Run it at effort `<effort>`, including for ordinary UI work; use `<higher effort>` only when prototyping a new UI from scratch.
- **Fallback:** if <Implementer> is actually unavailable (for example, its quota is exhausted or its API is unreachable), <Reviewer> at `<effort>` may serve as the implementer and main worker. Don't choose <Reviewer> for this when <Implementer> is available.
- **<Reviewer>** (`<model id>`, always `<effort>` for review, research, and computer use) is the primary independent reviewer when review is warranted: the change is substantial or risky, or the user asks for review. It is also the researcher: deep codebase investigation, and locating and understanding code and tasks. It also handles computer use: driving a running app, browser, simulator, or device, and capturing screenshots or recordings, when a check needs real interaction or an independent look at runtime behaviour; don't use it for what the main thread can check itself, such as reading code or running tests. In these roles it reports findings and does not edit files unless the brief allows it.
- **<Lookup model>** (`<model id>`, effort `<effort>`) is optional and narrow: simple file location and straightforward lookups, or a supplementary adversarial review alongside <Reviewer>. It is never the primary reviewer or an implementer. Don't invent a task just to use it.
- The user chooses the model for design work. Don't route design work to a different model automatically; unless the user picks one, design work follows the roles above.
- Never use <excluded models>, at any effort, including wrappers and background workers.
- That exclusion covers simple tasks too. Delegate a simple file-location or straightforward lookup task only to <Lookup model>; otherwise do it in the main thread.

### When to delegate

Delegation pays for itself in three ways; use it when one applies:

- **Time:** independent work runs concurrently instead of in sequence.
- **Context:** a long task keeps its judgement when the main thread delegates the building and keeps its own context for integration and decisions.
- **Independence:** a reviewer or test author who did not build the code checks what was required rather than what was built.

Small, tightly coupled work is usually faster in the main thread. Always orchestrate when the user explicitly asks for it. Orchestration decides how work is split, not who does it: however many agents are involved, implementation seats go to <Implementer> (or <Reviewer> only under the fallback), and the other models keep their roles.

### Reaching each model

Use your harness's native subagent tool when it can run the role's model at the role's effort. Otherwise delegate through <development environment>'s `<delegation tool>`, whose own instructions cover review rounds, retries, and isolation.

| Role | <development environment> provider instance | Model | Option |
|---|---|---|---|
| <Implementer> | `<instance>` | `<model id>` | `effort: <effort>` |
| <Reviewer> | `<instance>` | `<model id>` | `reasoningEffort: <effort>` |
| <Lookup model> | `<instance>` | `<model id>` | `reasoningEffort: <effort>` |

- Set the model and effort explicitly on every seat, so none runs on a default.
- Give each seat a self-contained brief: the task, its role, its constraints, and whether it may edit files. Seats don't see this conversation.
- Parallel editing seats work in separate files or isolated worktrees, so their changes don't collide.
- When a role's model can't be reached, give its work to an <Implementer> seat or the main thread and tell the user; a review by <Implementer> does not cross providers.

### Computer use

Brief a computer-use seat with what to verify and on which platform, how to launch the app, any credentials, seed data, or fixtures it needs, and where to save screenshots and logs. Ask for pass, fail, or blocked, with the steps taken, what was observed, and the screenshot paths.

Launching apps, simulators, or browsers to verify work is fine without asking. Ask the user first only when a run could disrupt their environment beyond that, such as closing their apps, changing system settings, or acting on real accounts or data.

---

## Notes for one harness

The same person keeps what is particular to one harness in that harness's own instructions file, beside the layer above:

- Native <Implementer> seats: `subagent_type: "<subagent name>"` with `effort` set per role. Don't pass `model`; it replaces the pinned model.
- Workflows run <harness provider> workers only. Use them to coordinate several <Implementer> seats, passing `{model: "<model id>", effort: "<effort>"}` to each worker; reach other providers' models from the main thread through <development environment>.
- Check a workflow's progress with `<status command> <session directory> <workflow id>`, passing the session directory that contains `subagents/`. A quiet parent or a `needs inspection` status alone is not a reason to stop a workflow.
- If a built-in, plugin, or helper agent would run on <excluded models>, set its model explicitly or don't use it.
