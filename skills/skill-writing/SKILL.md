---
name: skill-writing
description: Write or revise agent skills. Use when turning intent into a skill, refining its instructions, or reviewing whether it guides the desired behavior without unnecessary prescription.
---

# Skill Writing

Write skills that improve an agent's work while leaving room for judgment. Choose the skill's structure around what it needs to contribute: knowledge, judgment, procedure, conventions, or some combination. Preserve the context and detail needed to apply that contribution reliably.

## Establish the intent

Derive the skill's purpose, inputs, and responsibilities from the request and supplied material. Distinguish reusable requirements from examples, preferences, and choices specific to one task.

Identify what the agent needs from the skill: specialized facts, guidance for choosing between approaches, a necessary sequence, or consistent standards. Let those needs determine the organization and supporting resources.

Give the skill a coherent responsibility. Separate what an owning workflow requires from how a specialist realizes it. Domain content, visual presentation, and hosting mechanics, for example, can have different owners without each repeating the others' instructions.

Write for an agent that has not seen the authoring conversation. Preserve the decisions and reasons it needs. Resolve variable choices—such as design language, terminology, and tools—from relevant context at invocation time. Define fallbacks only where the task needs them.

## Guide judgment

**Outcomes over recipes.** For skills that own a task, describe the result and the evidence needed to establish it. Give ordered steps where order affects correctness, and exact mechanics where a fragile operation requires them. Otherwise let the agent choose its approach. Consistency should come from reliable decisions, not identical outputs.

**Purposeful prescription.** A specific mechanism, convention, or limit can be part of the intended behavior. State it explicitly when the skill's purpose depends on it—for example, one watcher per state file, a retry budget, or a shared format. Keep the requirement scoped to the situation it serves.

**Freedom within constraints.** Preserve essential contracts, scope, and authorization boundaries. Treat defaults as defaults and examples as examples. A catalogue should help the agent recognize possibilities; a complete template earns its place when the task requires that structure. Keep incidental choices from becoming universal rules.

**Positive, concrete language.** State the behavior wanted. A familiar leading word, such as “progressive disclosure” or “source of truth,” can carry a useful body of knowledge without a lengthy definition. Reuse the term consistently, rather than repeating its explanation or inventing new jargon. Explain a constraint's reason when it changes judgment. Retain prohibitions when they define a real boundary, and pair them with the intended action.

## Make completion meaningful

For skills that own a task, define what establishes completion. For skills that supply expertise within another task, define when the guidance applies, which decisions it informs, and what correct application looks like.

A completion criterion needs both **clarity** and **demand**: the agent can tell whether it is satisfied, and satisfying it covers the required work. “Produce a change list” is checkable but weaker than “account for every modified interface and its affected callers.” State coverage through the outcome rather than prescribing every search the agent must perform.

Distinguish evidence of progress from evidence of completion. “Checks pass and relevant reviewers clear the current revision” establishes more than “checks pass.” A tool reporting no new findings does not establish that earlier findings were resolved. Name a misleading proxy when it is a plausible stopping point for this particular skill.

When a workflow rushes an early stage, sharpen that stage's completion criterion first. If premature progression persists, consider a handoff that controls which instructions the next stage receives. Merely splitting headings or files does not isolate context already loaded.

## Put detail where it belongs

Choose between steps and reference deliberately. Steps express necessary order; reference supplies principles and facts consulted when relevant. A skill can be either or both. Keep the shared purpose, essential constraints, and any applicable completion criteria in `SKILL.md`, with universally relevant context in ordinary Markdown.

Use `<important if="condition">...</important>` for consequential instructions that apply only under a recognizable condition. Name the actual situation, such as resuming unfinished work. The condition should help the agent decide when to apply the instruction; routine guidance needs no wrapper.

**Progressive disclosure.** Move substantial branch-specific detail into a bundled reference. Split where a task takes a distinct branch, not just because a document is long. Keep an idea, its rules, and its caveats together so reading one brings the others into view.

**Context pointers.** A pointer names out-of-context material and the condition for reading it. Its wording determines whether the agent reaches the knowledge. “When changing persisted fields, read the migration reference before editing” gives a usable trigger; “see references” does not. Give each distinct branch one trigger, rather than several synonyms. If required material is being missed, strengthen the pointer before moving everything into the main file.

**Context load and cognitive load.** Descriptions and routing instructions spend context wherever they are loaded. More documents also mean more places to remember and navigate. Keep pointers cheap, but split only when selective loading or independent discovery earns that navigation cost. Spend human attention where the user's judgment matters, rather than making them remember implementation details.

Add supporting resources only when they improve execution: examples that clarify a difficult choice, assets that belong in the output, or scripts for repeated deterministic work. Leave easily discoverable commands and configuration with their source of truth; preserve non-obvious constraints and gotchas that discovery would miss.

<important if="the skill coordinates ongoing, delegated, or stateful work">
Define who owns mechanics and who owns judgment. A watcher may own waiting and event detection while the agent owns diagnosis and resolution. When inputs can conflict, establish which source governs requirements. Tool outputs and review comments are evidence to assess against those requirements, not automatic instructions to act.

State what establishes the current result, what remains outstanding, and when to continue, stop, or seek the user's help. Preserve completed work, unresolved obligations, and the evidence they depend on across retries and handoffs. Reuse verification while it remains applicable; recheck what changed. A worker finishing or a process exiting does not establish that the user's goal is complete.

Keep recovery bounded and tied to the problem. Continue independent work when one part is blocked, change strategy when retries add no progress, and keep optional cleanup from expanding the completion criteria. Give handoffs the context needed to continue rather than the entire execution history.
</important>

## Prune for effect

For each instruction, ask: **What would the agent do differently because this is here?** Retain knowledge, examples, and conventions that materially improve selection, accuracy, or consistent application. Remove generic advice, repeated meanings, and explanations that do not improve expected behavior. If removing a sentence loses no useful direction, remove it rather than merely shortening it.

Keep each meaning in one authoritative place. Repeated instructions increase apparent importance as well as maintenance cost. Prune stale or irrelevant rules, but keep the constraints that prevent an attractive yet incorrect result. Brevity serves effectiveness; a word limit is not the goal.

<important if="you are revising an existing skill">
Preserve its intended behavior and real operational constraints while changing the guidance. Address feedback or an observed failure at the narrowest useful scope. Reconsider the existing wording, placement, and trigger before adding another rule. Distinguish user preferences from demonstrated improvements; one example does not establish a universal requirement.
</important>

## Deliver and validate

Deliver in the requested form: skill files, draft text, or review findings. For file changes, use the requested location and the target environment's format. The name and description must make the capability and its distinct triggers discoverable before the body is loaded. Keep execution details in the body. Preserve invocation settings unless a change is requested.

Check the finished skill for clear scope, reachable references, consistent instructions, valid metadata, and unfinished scaffolding. Confirm that a future agent can understand when to apply the skill and distinguish requirements from optional approaches without this conversation. Check executable resources when included.

A review is complete when material mismatches with the intended behavior are accounted for and each proposed change identifies the affected guidance and the decision it should improve. A review may conclude that no change is warranted.

<important if="behavioral evaluation is part of the task">
Use realistic inputs and judge the resulting work, not whether the agent repeats the instructions. When comparing revisions, establish expected outcomes before evaluating them. Include cases beyond those that prompted the change, and check that previously correct behavior is preserved. Hold the inputs and execution conditions comparable when comparing approaches. Record limitations and make changes supported by the observed behavior. Structural validation alone does not establish effectiveness.
</important>
