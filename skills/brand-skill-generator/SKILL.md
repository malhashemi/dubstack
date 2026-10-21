---
name: brand-skill-generator
description: Create a brand-specific design system skill when one is missing. Interpret briefs, brand materials, and codebases to codify an established identity or develop and refine an intended one with the user. Package the identity, reusable kit, application guidance, and a full-brand HTML overview for future on-brand work across media.
---

# Brand Skill Generator

Create a brand system that agents can apply without the authoring conversation and humans can understand through `index.html`. It should guide writing, imagery, motion, products, documents, and other intended applications through a clear identity, usable materials, and judgment about how to adapt them.

This skill owns creation of that reusable skill. Once it exists, its own instructions govern application and continued development. First look for an existing brand skill in the relevant project and supplied materials; use that skill for ordinary application or maintenance. An explicitly requested replacement or migration can use this generator, preserving accepted identity and accounting for existing consumers.

## Establish the assignment from the evidence

Read [Brand context](references/brand-context.md) when interpreting the inputs. A brief, conversation, codebase, website, document, asset collection, or reference image can each contribute different kinds of evidence. Establish which material reflects the intended brand. User direction can make a codebase the source to preserve, something to audit, or only a partial starting point; frequency of use does not establish authority.

Assess what is known and what needs developing across strategy, verbal identity, visual identity, and practical applications. Extract settled decisions faithfully, investigate conflicts, and develop missing or unsatisfactory areas within the requested scope. These approaches can coexist in the same project. Creating a brand skill does not itself require changing the source application.

Develop the brand with the user through [the brand interview](references/interview.md), which defines its folder, its record, its phases, and its rounds. Use available evidence to answer questions before asking the human. Distinguish factual gaps from creative choices and implementation work. Ask about what materially affects the result, and continue independent work while answers are pending.

## Develop the system with the user

Read [Verbal identity](references/verbal-identity-checklist.md) and [Visual foundations](references/visual-foundations-checklist.md) to identify established guidance, missing development, and justified exclusions. They are the interview's coverage, and their gaps choose the next design work rather than being filled with rules during documentation. They are not forms for the human to complete. A deferral that prevents an intended application keeps that part of the result unfinished.

The interview page is authored with `visualize-html` and serves understanding the brief, filling material gaps, comparing directions, and reviewing applications. Read [Visual review](references/visual-review.md) before preparing it. Supply the known context and the decisions that would move the work forward; let the presentation suit them. The generator owns brand content, completeness, recommendations, and interpretation of feedback. `visualize-html` owns composition, interaction, feedback mechanics, and delivery.

When direction is open, develop coherent alternatives through realistic uses so the user can judge how language and visual choices work together. Recommend a direction with reasons and tradeoffs. Isolate an individual variable when that helps resolve a focused question. Preserve settled choices and carry feedback into the next round instead of restarting discovery.

Provisional copy, marks, tokens, and applications are part of finding the identity. Keep them separate from established resources until their authority is resolved. Review how positioning, audience priorities, personality, and desired perception translate into language and visual expression together. Applied examples should expose whether that connection works; a selection among visual treatments does not establish the rest of the identity.

- For seeds, ramps, role mappings, and print tradeoffs, read [Color craft](references/color-craft.md). Hue selection is comparative judgment; new ramps use the bundled deterministic engine and a Pantone CLI matching pass.
- For type selection and hierarchy, read [Type craft](references/type-craft.md). Evaluate faces using actual brand language and reading conditions.
- For a new or conceptually revised mark, read [Logo craft](references/logo-craft.md) and use `svg-design`. Supply the accumulated context and coordinate its artwork with the interview page.

<important if="a material identity decision remains open">
Use the user's existing direction and delegated creative authority. Where a human choice is needed, put it in the next round as reviewable options or a concrete proposal with the consequences of the decision. Untouched defaults, a shortlist, and a successful rendering do not establish acceptance. Record what feedback accepts, changes, or leaves open; continue independent work while waiting. Without a needed answer, deliver an accurately labeled draft rather than promote an assumption into the identity.
</important>

## Establish readiness to codify

Before final packaging, reconcile the existing `working.md` with the identity coverage. For each consequential choice, identify its basis in authoritative source material, a scoped user decision, or actual delegated judgment; why it fits the intended brand; and the relevant application work demonstrating its consequences. Group related choices with the same basis rather than seeking approval for every token. Reuse established source examples where sufficient. Writing a rule, labeling it a practical default, or completing a checklist supplies none of that authority by itself.

The identity is ready when its strategic premises explain the verbal and visual direction, consequential choices have that support, and no unresolved decision prevents an intended application. Existing identity and delegated authority can establish choices without another approval round. Where a needed choice remains with the user, continue development through concrete proposals in the interview. Account for scoped feedback and open obligations across the whole system before concluding that the latest selection closes the work.

## Turn the agreed identity into an independent skill

Read [Brand kit contract](references/brand-kit-spec.md) before packaging. Use the project's established skill location or the user's destination, and `{slug}-brand` for a new kit. The template is a starting structure to specialize; its values and headings are not brand decisions.

Packaging codifies established decisions and their derived implementation details. If authoring reveals a new consequential choice, return it to development and preserve its provisional status. A draft bundle can support that work; its existence does not make the identity ready.

The resulting skill is a self-contained brand reference: identity, reusable materials, and principles for applying, assessing, and evolving them. Its consumer's workflow determines the specific task, tools, artifact production, presentation, and delivery. Keep those mechanics outside the emitted skill. Carry the template's shared application, brand-consistency, and evolution blocks into every emitted skill as directed by the kit contract, then add the brand's own grounding and resource pointers. No external skill or the authoring conversation should be needed to interpret the brand.

Create `<kit-dir>/index.html` with `visualize-html` as the human interface to the full brand. Before authoring it, read [the permanent brand interface brief](references/visual-review.md#the-permanent-brand-interface) and pass its mission and requirements explicitly to `visualize-html`: show the brand through the page's own design, voice, and applied examples, so a human can understand and apply the brand without leaving the page. Supply the current guidelines, practical guidance, and actual assets and values. The generator verifies coverage; the presentation skill chooses the narrative and layout. Hosting is separate from this local deliverable.

Teach the emitted skill to reuse existing resources, capture worthwhile patterns discovered during real work, and keep its knowledge and human interface current. Distinguish ordinary extensions from changes to identity. The kit should support useful growth without making every application a discovery session or a maintenance project.

## Establish completion

Confirm [readiness to codify](#establish-readiness-to-codify), including any choices introduced during packaging. Review the finished kit against the brief and the work developed with the user:

- Foundational choices are established by evidence, user decisions, or delegated authority. Facts, assumptions, proposals, and deferrals remain distinguishable; no unresolved blocker is disguised as a finished rule.
- The identity coverage is accounted for with usable guidance and examples. Its fixed constraints, flexible areas, and reasons help an agent make unfamiliar decisions.
- The examples developed during exploration and review show how the identity applies to the intended work, using actual assets, values, and voice. Inspect their readability and relevant accessibility and production constraints; correct gaps they reveal.
- `index.html` demonstrates the identity while communicating its full practical use to a person unfamiliar with the project, including verbal guidance and material limitations. The reader can reach the needed explanations and examples within the page.
- Guidelines, tokens, portable values, assets, resource links, and the overview agree. A future agent can interpret and extend the brand from the kit alone, without depending on the generator's tools or being instructed how to run its own task.

Run `uv run <skill-dir>/scripts/validate-brand-kit.py <kit-dir>` and resolve structural errors. Passing this check establishes mechanical integrity only; it cannot settle identity decisions or support a completion claim while development remains open.

Choose examples from the brief and reuse those developed during the review. A polished visual example alone does not establish that the system guides writing or other intended media. Resolve unfinished scaffolding and broken resource links before handoff.

Before final handoff, [finish and remove the interview folder](references/brand-kit-spec.md#finish-and-remove-the-interview-folder): preserve lasting decisions and selected resources in the kit, resolve dependencies on temporary files, and delete the interview folder. Cleanup is part of completed generation. Keep unfinished work available when pausing or awaiting a required decision.

Deliver the overview as the human entrypoint, the skill location and a usage example, and any material limitations or unresolved work. The finished kit must stand on its own after cleanup.

<important if="resuming an unfinished creation or explicitly migrating a kit">
For unfinished creation, resume from its interview folder: the record, the page and its saved answers, and the candidates. For a completed kit being migrated, use its guidelines and recorded decisions. Carry forward accepted work, unresolved feedback, and verification that still applies; recheck affected applications after changes. Preserve names, paths, invocation settings, and consumer contracts unless their change is part of the assignment. Explain migration consequences and avoid overwriting unrelated customizations.
</important>
