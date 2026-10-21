# Visual Review and the Human Interface

Use `visualize-html` for the interview page and the permanent `index.html`. The generator supplies brand knowledge, required coverage, recommendations, and decision status. The presentation skill owns layout, interactions, persistence, feedback transport, and delivery.

## The interview page

Author the page at `<work-dir>/index.html`, in the folder [the brand interview](interview.md#where-it-lives) defines. Supply that output path to `visualize-html`, and say when the page is published to a Dossier tree; its default temporary destination does not govern this workflow.

Prepare the first round from the evidence already available. Let the user recognize what the agent understands, correct consequential assumptions, supply missing facts, and judge creative directions in context. Combine these activities when their relationship helps the user decide. The interview's phases set what a round may ask; within one, no fixed color–type–logo sequence is needed.

Show what matters for the next decisions, with deeper context available when helpful. An established identity may need an applied audit and a few corrections; an open brief may need alternative expressions of the whole brand. A sparse brief can begin with a visual understanding of the context and a few well-grounded provisional directions, with dependencies made clear.

Give the user a way to explain preferences, reject all options, or introduce another direction. Do not make selecting one of the agent's proposals the only way forward. Support item-specific reactions and broader comments without requiring the human to diagnose technical design details.

Revise the page each round as evidence and decisions change. Carry accepted work forward, highlight consequential changes, and focus later rounds on unresolved issues. One page carries the whole interview; split a review only when the content or delivery context makes it more useful.

## Choose what to show together

- **Intake and audit:** show the working understanding, influential evidence, gaps, and any mismatch between the existing expression and stated intent. Pair a question with the example it affects.
- **Open identity direction:** show coherent alternatives combining language and visual expression in comparable applications. Explain the idea, rationale, tradeoffs, and recommendation.
- **Focused choice:** hold established decisions steady and isolate the variable where practical. For hue, compare actual generated palettes in the same composition; for a mark, use comparable size and background tests.
- **Developed system:** show how the parts hold together across the expected range of use, including restrained or functional work as well as expressive applications.
- **Refinement during creation:** demonstrate the effect of feedback on the affected use cases without reopening unrelated decisions.

Select examples from the brief. A packaging brand may need a label and service notice; a software brand may need a product state and documentation excerpt. These are possible tests, not a universal specimen inventory. If a choice depends on another unresolved choice, expose that dependency rather than imply that every combination will work.

## Supply the presentation brief

Provide the purpose, audience, working understanding, relevant source evidence, settled constraints, candidate identities and assets, actual palette values or CSS, available fonts, example copy, application conditions, and the information or decisions needed. Identify facts, assumptions, proposals, and accepted choices. Supply enough explanation for the user to judge the recommendation without reading the agent's notes.

Coordinate logo artwork from `svg-design` with this review. Use its SVG files directly and tell it that `visualize-html` handles the comparison surface. Similarly, use provisional copy, type specimens, and generated palettes to discover the system before final packaging.

Let the presentation adapt to the brand and the decision. Do not prescribe a universal card grid, fixed section order, or number of alternatives.

## Turn feedback into decisions

Give options and questions stable identities. Preserve the subject and revision of feedback so an old reaction is not silently applied to changed work. Let `visualize-html` implement local persistence and the route back to the agent; local interaction alone is not evidence the agent received the feedback.

Interpret returned responses against the brief and record their meaning in `<work-dir>/working.md`. A user can accept a concept while requesting different typography or rejecting its wording. A shortlist can express interest without settling a choice. Separate those obligations, resolve ambiguity where it would change the outcome, and retain earlier accepted decisions unless the user revises them.

Apply decisions to the working assets, values, and guidelines, then refresh affected examples and questions. Do not rely on browser storage as the only record of the established identity. If feedback requires a human response, keep dependent work provisional while progressing elsewhere.

## The permanent brand interface

Every completed kit includes `<kit-dir>/index.html`, authored with `visualize-html`. Pass the following mission and requirements explicitly in the final-page handoff, alongside the brand material; supplying files alone does not convey the intended experience.

**Mission: show the brand through an experience of the brand.** Make its identity recognizable at a glance and its full guidance understandable through one self-contained page. The page itself is a considered brand application: its writing, typography, color relationships, composition, imagery, and relevant interactions embody the accepted identity. A person should be able to understand and apply the brand without the authoring conversation or opening another document.

Demonstrate principles through actual language, assets, and applied examples, with concise explanations beside what they clarify. Let readers experience the voice through copy and see visual rules at work in compositions suited to the brand's intended uses. Choose examples that reveal the identity and its range; neither a list of attributes nor swatches and font names alone communicate how it works. Preserve exact rules, rationale, and limitations as accessible detail where demonstration alone would leave ambiguity.

Supply the full current guidelines, actual tokens and assets, portable values and production decisions, application examples, and material limitations. The page should let a human understand the brand's purpose and promise, recognize its voice and visual expression, find usable language and materials, understand fixed constraints and flexible areas, and see how the identity adapts to its intended uses. Important caveats and decision status must remain visible where they affect use.

These are information responsibilities, not required page sections. Let `visualize-html` choose the narrative, hierarchy, composition, examples, navigation, and interactions. Use progressive disclosure within the page to reconcile quick recognition with depth. A visual showcase that omits the verbal identity or practical usage guidance is incomplete.

**Self-contained describes the reader's experience.** Keep explanations, demonstrations, and deeper guidance accessible within the page, so understanding and applying the brand never requires opening a Markdown file, stylesheet, or separate document. Styles, fonts, scripts, and assets can load from separate files or services; embedding everything and offline operation are not requirements. Optional asset downloads can support reuse, while the guidance for choosing and using those assets stays on the page.

The generator remains responsible for coverage. Compare the page against the full guidelines: each human-relevant principle, rule, example, and production decision needs an intelligible representation or accessible detail. Integrate coverage into demonstrations and focused in-page details; do not append a wholesale Markdown rendering to satisfy coverage. Summarization may remove repetition but must preserve what changes a user's choices. Implementation-only detail can stay in the kit. An existing page can illustrate successful communication without becoming a layout template.

Applications developed in the interview can carry into this overview; the interview page itself is removed with its folder. Keep rejected alternatives and temporary comments from being mistaken for established guidance. Pass `<kit-dir>/index.html` explicitly as the final destination. It opens without a project build workflow or an installed presentation skill; `visualize-html` is the generator's authoring tool, not a dependency of the result.

## Render and verify

Inspect the actual document in a browser, including font loading, SVG sizing and colors, narrow layouts, relevant backgrounds, and access to deeper content. For a feedback surface, follow the presentation skill's checks for persistence, reopening, and usable feedback retrieval. Confirm that comments and choices return with the correct subjects and statuses.

Use the real assets and values, refreshing any copies after source changes. Check that the page demonstrates the identity faithfully, that practical guidance and its supporting examples are accessible without leaving the page, and that source files, examples, and decision status agree.

Hosting mechanics belong to the chosen destination's skill or CLI; no specific hosting service is required. If `visualize-html` is unavailable, continue independent brand work and identify the overview or review as outstanding. An interim surface can help with decisions but does not fulfill the requested `visualize-html` deliverable.
