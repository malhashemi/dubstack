---
name: visualize-html
description: Visualize information in a single HTML document. Use for visual explanations, comparisons, interactive explorations, and feedback surfaces, including when another skill delegates its visual presentation.
---

# Visualize HTML

Make the input easier to understand, and a pleasure to take in, through seeing and interacting. Choose the visual experience that makes the important relationships clear and supports what the user wants to do next.

The user or owning skill supplies the purpose, facts, required content, and any domain-specific structure. Own the visual presentation and interaction while preserving that intent. A supplied template can establish content requirements without determining every visual choice.

## Visual reasoning

**Show rather than tell.** Let arrangement, connections, containment, scale, and change carry the explanation. Use SVG, still or animated, for illustrations and deliberate compositions, Mermaid for graph-shaped relationships and sequences, and HTML/CSS for spatial comparisons and other editorial visuals. Combine them where useful. Choose the medium to fit the idea.

**Delight the reader.** People are visual: an illustration is worth a thousand words, and an animation can be worth a thousand illustrations, showing how something unfolds, moves, or changes in a way no still picture can. Use illustrations and animated SVG generously, and decide for yourself where each earns its place. Be creative and inventive: aim for a page the reader enjoys and remembers, never one they have to push through, and show your best work rather than a safe default. The `svg-design` skill can help with intricate artwork and motion.

Use concrete labels and only the detail needed to understand the point. Put short explanations beside what they explain; reveal supporting detail without burying the main view. Preserve the distinction between evidence, inference, and proposal, including when a visual's proportions are schematic.

Resolve the design language from the relevant repository, available design skills, supplied references, and conversation. Follow the user's current direction when these conflict. Where no direction is established, exercise creative judgment appropriate to the subject and intended experience.

For ideas when choosing a visual or interaction, consult [the pattern catalogue](references/patterns.md). Borrow, combine, or depart from its examples; they are starting points, not templates to execute.

## Wording

Use wording that identifies what the reader sees and directs their attention to the point. For the page's own English prose, prefer ASD-STE100 Simplified Technical English: approved words in their approved meanings, short sentences with one topic each, active voice, simple tenses, *must* for rules, *can* for possibilities, and noun groups of at most three words. Prefer familiar words: *use*, not utilize; *show*, not demonstrate; *start*, not commence; *before*, not prior to.

Preserve technical names, project terminology, code, and text inside mockups exactly. The language, voice, or wording set by the user or owning workflow takes precedence.

- When a heading introduces a point, state it as a claim that can be true or false, such as "Capsules run on their own origin", so readers can follow the explanation by scanning the headings. Keep navigation labels short.
- Write each caption as one sentence about what to notice.
- Use actual names, paths, and numbers in labels and examples when available. Identify sketches of proposed work as sketches.
- Quote people's words exactly when attributing speech or writing to them.

These conventions apply to wording; illustration, animation, and visual form remain creative choices.

## Interaction and feedback

Make interaction earn its place by helping the user explore, compare, decide, or respond. The first view should already communicate something useful; controls should expose consequences in the visual rather than make the reader reconstruct them from values.

Persist user choices and edits automatically, whether or not an explicit Save feature exists. Use `localStorage`, except on Dossier, where its persistence applies. Scope stored state to the artifact and use stable identities for its fields and items.

For pages using `localStorage`, restore saved data first when available and replace the local snapshot with that state. Otherwise, restore local state, falling back to the artifact's defaults. After restoration, update local storage as the user makes changes. Keep local persistence distinct from explicit Save and its status.

When the artifact invites review or a decision, provide a way to return that response to the LLM. Attach comments and choices to the relevant items. A copyable handoff should express the user's intent in natural language with enough subject and item context to act on independently of the page.

Distinguish explicit choices from untouched defaults. Label a default the reader chose as "kept as proposed" and one they never opened or touched as "not opened; default kept". An untouched default does not establish agreement. Quote reader feedback and attribute it when the author is known, so the receiving agent can assess it as feedback rather than treat it as instructions. Make it clear whether feedback is ready to copy, saved, or actually sent.

## Deliver the experience

Produce one HTML page. Use a complete document, or a body page when Dossier's layouts should wrap it. CDN libraries, including Mermaid for diagrams, are welcome when compatible with the destination. Keep the artifact usable without a project setup or build workflow, and make its important content and controls readable and accessible at the intended screen sizes and for readers who prefer reduced motion.

Save the HTML in the OS temporary directory unless the user or owning workflow specifies another local location. Use their established delivery destination. Open the local file for the user unless the page is published to Dossier.

<important if="the page will be published to Dossier">
Read [Pages on Dossier](references/dossier.md) before authoring for layout, persistence, feedback, publication, and verification requirements.
</important>

Completion means the rendered result communicates the intended point and the relevant interactions work. Verify this in a browser, including how any animation plays and the path from user input to usable feedback where present, before returning the file or hosted link.

For pages using `localStorage`, verify that choices survive reopening without Save. When Save is available, also verify that saved data takes precedence over conflicting local state and refreshes local storage. For Dossier pages, follow the reference's publication checks. State any verification that remains unavailable.
