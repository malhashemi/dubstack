# Brand Kit Contract

The result is a self-contained brand reference: identity, usable materials, and principles for applying and evolving them. Agents use the underlying resources; humans primarily use the full-brand `index.html`. Neither audience should need the authoring conversation or the generator's environment. The consuming workflow determines the specific use, tools, artifact production, review process, and delivery; the generated skill supplies the brand knowledge that informs those choices.

## Location and resource responsibilities

Use the user's destination or the project's established skill directory. New kits use `{slug}-brand`. Ordinary maintenance belongs to that skill once it exists. During an explicitly requested migration, preserve names, discovery settings, and consumer contracts unless changing them is part of the assignment.

| Resource | Responsibility |
|---|---|
| `SKILL.md` | Brand grounding, relevant resource pointers, and shared principles for application, brand consistency, and evolution |
| `readme.md` | Identity, rationale, application guidance, decision status, coverage, resource inventory, and consequential changes |
| `index.html` | The human interface to the full brand, authored with `visualize-html` |
| `styles.css` | Import-only entrypoint for shipped CSS token files |
| `tokens/*.css` | Canonical visual values and semantic roles |
| `brand-card.md` | Corresponding portable values, asset references, units, and production decisions for non-CSS consumers |
| `assets/` | Usable marks, distributable fonts, imagery, and signature treatments |
| `pantone.json` | Print match evidence, including book identifiers and distances |
| `components/`, as needed | Self-contained specimens that explain useful brand patterns, states, and variations |

The file responsibilities are a stable starting contract, not a required prose outline. Substantial application-specific knowledge can move into linked references when selective loading helps. Keep the entrypoint's reading triggers precise and the inventory current. Do not scatter a single rule across several competing sources.

## Start and specialize the bundle

The scaffold provides a starting bundle with authoring prompts and provisional token values. It deliberately leaves the human page for `visualize-html`:

```sh
uv run <skill-dir>/scripts/scaffold-brand-skill.py --brand "Brand Name" --slug brand-name --out <project-skill-dir>/brand-name-brand
```

Use it once the destination and brand name or authorized working name are known. Prototypes and draft bundles can precede identity readiness. Finalize the authoritative kit only when [readiness to codify](../SKILL.md#establish-readiness-to-codify) is established; filling the scaffold does not resolve identity choices.

The helper's `--update` option only adds missing files; it does not migrate content or constitute a brand refinement. Preserve existing authored work when resuming. Remove scaffolding and resolve template defaults before delivery.

## Carry the operating principles into every skill

The template's `SKILL.template.md`, which becomes the kit's `SKILL.md`, is the canonical source for three shared text blocks, delimited by `brand-skill:apply`, `brand-skill:verify`, and `brand-skill:evolve` comments. **Include those blocks and their markers verbatim in every emitted skill.** They carry the common principles for contextual judgment, brand consistency, and useful growth. The structural validator checks their presence and contents. Keep them intact during later brand-specific maintenance as well.

Specialize the surrounding content: description, brand essentials, resource pointers, contextual adaptations, and usage constraints. The fixed blocks establish how to interpret and maintain the identity; they do not prescribe a specific artifact, tool, or creative workflow. Avoid adding brand-specific instructions that contradict them. Explicit user direction still governs the task.

Write the brand-specific content using the same principles:

- State the outcome and the few constraints that govern decisions. Preserve reasons where they help a future agent interpret a rule.
- Distinguish fixed identity from flexible expression, and examples or defaults from requirements. State exact brand rules where consistency depends on them, such as protected wording, color values, or mark proportions.
- Keep universally relevant grounding in the entrypoint. Put detailed knowledge where the relevant task will find it, with clear reading conditions.
- Preserve concrete examples, useful depth, and real constraints. Remove duplication or incidental prescription rather than shortening for its own sake.
- Define what correct brand application looks like and how to interpret an uncovered case. Treat missing evidence, provisional choices, and limitations honestly.

The emitted skill must contain this guidance itself. Keep references to `skill-writing`, `visualize-html`, `svg-design`, this generator, and other production tools out of its operating instructions. Those are dependencies of the generation or consuming workflow, not of the brand. Contextual examples can explain how the identity changes in expression; they must not turn into instructions for planning, producing, presenting, or delivering a particular type of artifact.

## Identity, application, and coverage

Use the [verbal](verbal-identity-checklist.md) and [visual](visual-foundations-checklist.md) coverage references during creation. Preserve their substance in the resulting guidance without shipping a generic unanswered questionnaire.

The guidelines need to establish strategy and evidence, usable messaging, recognizable voice across relevant registers, concrete visual decisions, actual asset use, and how those choices adapt to intended media. Include reasons and contrasting examples where they clarify a boundary. Define what remains constant across applications, what can change, and how a new use can be derived from the identity.

Account for every checklist dimension as resolved, inapplicable with a reason, or explicitly deferred. Group related exclusions rather than cluttering the guide with repetitive entries. A deferred capability that an intended application depends on remains unfinished; an acknowledged limitation is not proof that the capability exists. Keep accepted constraints, assumptions, proposals, and open decisions distinguishable.

Retain the meaningful sources and authority behind consequential decisions. For an audited codebase, record what was preserved or changed and why. Include the consequences for application consumers without implying that the source project was already migrated.

## Values and production knowledge

Use base values and semantic aliases where useful, preserving accepted naming contracts. `styles.css` imports all shipped token files; declarations and font loading belong in that import chain. Resolve font URLs from their stylesheet's directory.

Keep exact established colors when codifying them. During generation, new ramps use the deterministic palette helper and Pantone CLI pass described in [Color craft](color-craft.md). Record inputs, engine and dependency versions, and commands in `working.md` while developing the palette. The kit receives the accepted values, roles, anchors, intentional overrides, print references, and meaningful provenance. The engine's proposed aliases do not automatically establish the brand's final usage rules.

Keep generation scripts, their installation requirements, and executable regeneration procedures in the generator. Do not copy them into the emitted kit. The brand's values and print evidence must be usable directly. The workflow undertaking a future identity change owns the tools for producing replacement values; the brand skill owns their meaning, status, and consistency with the identity. For exact codified palettes, use the Pantone CLI directly during generation and retain its evidence without forcing regeneration through a different color model.

Document the print treatment and relevant book/substrate; computed matches are approximations. Missing CLI access or index data leaves matching incomplete. Record that limitation explicitly and do not claim full completion when it blocks the intended production use.

Typography, spacing, shape, effects, and motion need usable roles and values for actual applications. Package font files only when redistribution permits; otherwise record acquisition requirements and intentional fallbacks. Theme variants and extra font families should serve a use rather than fill a template.

Tokens govern values and guidelines govern intent and usage. The brand card provides corresponding portable values with units and color-space assumptions. The palette and Pantone helpers update only their marked blocks; keep authored decisions outside those blocks. Reconcile portable values after intentional role overrides instead of assuming regeneration covers them.

## Useful growth and resource ownership

The shared evolution block establishes how future work can improve the kit. Specialize its resource pointers and examples so an agent can act on it.

A captured pattern should fit the identity, work in its actual context, and provide reusable value. Record whether a resource is established, experimental, or only illustrative. Capture enough brand rationale, behavior, states, provenance, and use conditions for a future consumer to understand it. Match the form of the example to the knowledge it preserves.

Keep essential brand guidance and examples inside the kit. A maintained project component can be linked as supplementary implementation context, but the brand pattern must remain understandable without that project or its framework. Use a self-contained specimen where useful instead of creating a competing implementation or copying a complete one-off page into the library. The same reasoning applies to language patterns, imagery treatments, motion character, and composition.

Updates within the task's authority can proceed naturally. Identity changes outside it need a concrete proposal. Keep affected guidelines, values, assets, portable equivalents, examples, links, and the human interface aligned; explain any migration of existing consumers.

## Human interface and handoff

Author `index.html` with the mission, content coverage, and in-page experience described in [Visual review](visual-review.md#the-permanent-brand-interface), and pass that brief explicitly to `visualize-html`. Keep provisional concepts and temporary feedback from being mistaken for the established identity.

Run `uv run <skill-dir>/scripts/validate-brand-kit.py <kit-dir>`. During construction, `--draft` reports unfinished content as warnings; broken references remain errors. The validator checks required resources, shared operating blocks, metadata, scaffolding, links, CSS imports, and SVG structure. Resolve mechanical errors and keep the guidance and assets consistent. These checks establish bundle integrity, not brand quality or acceptance.

Review the kit against the brief and the examples developed with the user. Reuse exploratory applications when they still reflect the final system; refresh those affected by later choices. Address missing brand guidance revealed by that work, including relevant written and non-web uses. Confirm that the emitted instructions describe the identity and its interpretation without depending on other skills or directing an artifact-production workflow. Deliver a draft when material decisions or necessary capabilities remain unresolved.

## Finish and remove the interview folder

Begin this cleanup only after [identity readiness](../SKILL.md#establish-readiness-to-codify) and the finished-kit review are satisfied. Passing the structural validator alone does not authorize deleting the working record. Complete cleanup before handing off a finished skill:

1. Carry lasting knowledge from `working.md` into the guidelines: established identity, consequential decisions and reasons, meaningful source provenance, constraints, and any accepted limitations. Preserve the substance needed for future use without shipping the scratch note or a session transcript.
2. Move or copy selected assets, editable sources, useful examples, and necessary generation inputs into their durable kit locations. Put any separately requested deliverables at their intended destinations. Update the final overview and resource references so no shipped file, symlink, stylesheet import, or resource URL depends on the interview folder.
3. Confirm that the finished kit contains the required knowledge and usable resources. Delete the interview folder that [the brand interview](interview.md#where-it-lives) defines, including its record, page, saved answers, and unneeded candidates. When it lives in a Dossier tree, remove it from the local copy and publish the removal with the tree's commands; a push leaves saved answers and comments in place, so then delete the folder on Dossier with `dossier rm <workspace>/<tree>/brand-interview/`. Preserve unrelated work and original user inputs.
4. Confirm the interview folder is gone, on Dossier as well when it lived there, and run the structural validator on the final kit to catch any remaining dependency on removed files. Report a cleanup failure as unfinished work rather than claiming complete generation.

When generation is paused, interrupted, or still awaiting a required decision, retain the interview folder and identify its path for resumption. Resume this cleanup once the result is complete; retaining an unfinished session does not make the interview folder part of the emitted skill.
