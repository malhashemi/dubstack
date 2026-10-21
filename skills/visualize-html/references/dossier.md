# Pages on Dossier

Dossier publishes trees of plain HTML. Pages inherit layouts, themes, and components from their parent folders. Form responses and comments are stored on the server with their authors' identities.

Before authoring, read `dossier --agent-info`, the authority for page rules and commands. Then run `dossier read <destination folder>/` to inspect the available layouts, theme variables, and components with their usage notes. This reference explains how to apply the visualization skill on Dossier and highlights constraints that are easy to miss.

If Dossier cannot support a required interaction, identify the missing capability and preserve the intended experience. Extending Dossier is an option to propose only when the user runs their own deployment; otherwise report the gap with the closest alternative it supports.

## Fit the tree

- **Inherit layouts with a body page.** Put the page's `<title>`, `<meta>`, `<link>`, and `<style>` before its content. The tree's layout and navigation wrap the page.
- **Use a complete document for standalone rendering.** A doctype or an `<html>` element bypasses inherited layouts. Use this form when no layout exists or when a page needs to render independently, such as an embedded mockup or state demo. To omit the outer layout for a folder of body pages, give the folder a complete-document `_layout.html` whose body contains only `<slot></slot>`.
- **Scope page styles.** Use one wrapper class to keep page CSS from affecting the layout's header and footer. Reset inherited element styles where the page relies on different styling.
- **Extend the existing theme.** Use the tree's theme variables and `_fonts/` so the page and Dossier components share a visual language. Variables can include `--background`, `--foreground`, `--primary`, `--muted`, `--border`, `--radius`, `--font-display`, `--font-body`, and `--font-mono`; `dossier read` lists those available. Extend the theme as needed for the page.
- **Use relative links and lowercase filenames.** Give pages a `.html` extension and use `index.html` for a folder's page. Omit the extension in links, such as `href="plan"` or `href="../outline/"`. Do not use `<base>`. When sharing a page alone, a file referenced only by its CSS or JavaScript must be a `_` file to accompany it; otherwise, share the containing folder.
- **Scope browser storage to the page.** Pages in a tree share one browser origin. Include the page path (`dossier.page.path`) as well as the artifact identity in `localStorage` keys.

## Use built-in rendering

Dossier renders these without a script tag:

- Mermaid, from `<pre class="mermaid">`;
- highlighted code, from `<pre><code class="language-…">`;
- math, in Pandoc's markup;
- diffs, with `<dossier-diff>`;
- a "Copy for agent" button, with `<dossier-copy>`.

Built-in Mermaid rendering switches to Mermaid's dark theme when the page shows dark, and uses the tree's body font. When a diagram needs custom colours, render Mermaid yourself under a class of your own rather than `mermaid`. Dossier renders every `<pre class="mermaid">` that is still unrendered when it scans the page, so it can reach a diagram before the page's own Mermaid does. CDN libraries and external embeds work as they do in a local file.

## Keep answers on Dossier

Use Dossier forms to persist decisions and annotations without custom persistence scripts. Reserve `localStorage` for viewing state, such as collapsed sections, filters, and reading position.

**Saving and restoration.** A `<form action="answers/">` stores one file per person. Without a submit button, it saves as the person types, retains unsent drafts in the browser, and restores their last submission on any device. Dossier validates responses against the available options and reports save status through an `<output data-dossier-status>` styled by the page.

Let Dossier manage restoration: current input and unsent drafts take precedence, and saved answers fill the remaining fields. This replaces the skill's saved-data-first rule for `localStorage`. When values arrive, update the model, visual, and handoff together. Preserve meaningful empty, false, and zero values.

**Field identity and validation.** Use stable item IDs as field names and retain them across revisions so answers remain attached to the original choices. Dossier validates each submission against the form the respondent saw. Removed fields retain their values in the data file but no longer appear on the page.

Forms must appear in the pushed markup, either directly or in a `<template>` that page code clones. Dossier does not manage forms built entirely by script and rejects their fields.

**Custom visual state.** Store structured state, such as notes on multiple items, in a JSON form field: `<input type="hidden" name="notes" data-type="json" value="{}">`. Write changes with `dossier.write('answers/~.json', { notes: { [id]: … } })`. Writes use JSON merge patches: objects should be keyed by item ID, arrays are replaced in full, and `null` removes a key. Each data file is limited to 1 MiB, and writes are limited per minute, so debounce updates while the user types.

**Shared state and visibility.** Use `action="<name>.json"` for state a group edits together; submissions merge into one file, field by field. Respondents can see only their own individual answers, while people with write access to the page can see everyone's. Use comments or a shared `.json` target for input everyone should see.

**Signed-out visitors and exported copies.** Any page that takes input can be opened by a signed-out visitor or exported to a file, so tell readers where their input goes and whether they must sign in:

- When `dossier.me` is null, submitting a form prompts sign-in and then completes the submission. Direct `dossier.write` calls fail with `sign_in_required`, so require sign-in before visitors enter custom notes that depend on those calls.
- When `dossier.page.exported` is true, forms and writes save only in the current browser. Make this local storage clear in the page's status.

## Comments beside items

Place `<dossier-comments for="<id>"></dossier-comments>` below each commentable item and give the item the matching `id="<id>"`. Use this component wherever it can anchor a comment. Use a custom control only for targets it cannot anchor to, such as a single diff line, and persist those notes in a JSON field.

The component collapses to a Comment button with an open-thread count. Threads support replies, resolution and reopening, @mentions, and page-defined stances such as `stances="reopen"`. A whole-page `<dossier-comments>` lists all threads.

Keep item IDs stable across revisions. Threads remain attached while the ID exists; removing it moves the thread to "On an earlier version".

<important if="comments must stay tied to a particular version of their subject">
Include the version, such as a diff's head commit, in the comment anchor's element ID. Give new versions new anchors so earlier threads remain associated with the content they reviewed and appear under "On an earlier version". Read each comment's version from its `anchor` when composing the handoff. Use separate, stable IDs for navigation links.
</important>

Threads are stored beside the page in `<page>.comments/`, such as `index.comments/` for `index.html`. Subscribe with `dossier.watch('index.comments/', …)`. Each comment includes `by`, `name`, `text`, `anchor`, `stance`, `mentions`, `agent`, and the thread's `resolved` status.

## Return the response

Use a copyable handoff as the primary route back to the LLM, so the reader can inspect and control the response.

Build the handoff from form values and open threads, excluding resolved threads. Identify the page with `dossier.page.link`. Include retrieval instructions: use `dossier read` on the page link and its `answers/` and `<page>.comments/` folders. The `answers/` folder exists only after the first submission; before then, `dossier read` exits with code 3, which also indicates missing access. Interpret choices by item ID and preserve undecided items as undecided.

Comments written through `dossier comment` carry `agent: true`, allowing the handoff to distinguish agent comments from human feedback.

Saving answers or comments does not notify or invoke the LLM. Report saved and copied states accurately; a response is sent only when the reader returns the copied text or an integration delivers it.

## Provide an agent-readable version

Dossier selects the agent-readable version in this order:

1. The Markdown, plain text, or JSON file named by `<link rel="alternate" href="…">`.
2. A sibling `.md` file with the same name as the page.
3. Markdown generated from the page.

When the page is drawn from a source document, such as a record, a ledger, an outline, or a data file, name that document as the page's agent version with `<link rel="alternate" type="…" href="…">`: it is what agents should read, exact and complete. The owning workflow names the document. Only a page with no source document relies on generated Markdown.

Generated Markdown preserves headings, prose, tables, Mermaid source, code, and form questions. For visuals drawn by script, it preserves only the `title` or `aria-label` on a drawing element such as `<svg>` or `<canvas>`, a custom element, or an element with `role="img"`. A label on an empty `<div>` later filled by script is lost, so give each such visual a supported element and a descriptive label.

The agent needs access to the companion file. Keep it in the folder shared with the page.

## Publish and verify

The owning workflow usually publishes the page with its containing folder. When it owns publication, write the page and supporting files into the local folder it specifies and leave publication to that workflow.

When the user names a Dossier destination directly, publish with `dossier push <folder> <workspace>/<tree>/<path>`. A push makes the destination match the local folder and removes files absent from it. Include the page and everything it links; never push a partial copy of a larger destination folder. Resolve push errors and warnings. Errors stop the push and identify the file, line, and required fix; warnings can identify issues such as a component with no definition in an ancestor folder.

Verify the page with Dossier's layouts and assets applied; a body page cannot render directly from disk. Use test input you own and preserve other people's answers and comments.

- **With a signed-in browser:** open the published link, enter an answer, wait for saved status, and reload to confirm restoration. Check that `dossier read` on the `answers/` folder returns the same intent.
- **Without a signed-in browser:** run `dossier export <link> -o <file>`, choosing an output path in the OS temporary directory. The export bundles layouts, theme, components, base libraries, and a snapshot of answers and comments. Check rendering and interactions in that file. Saves remain in the current browser, runtime reads of files outside the snapshot return empty results, and embedded pages or dynamically constructed URLs still need the network.

<important if="verification added test input to a published page">
Remove the test input after checking persistence: set only the test entries you created to `null` with a merge patch, withdraw a submission only if it consists entirely of test input, and resolve your test comment threads. Reload and confirm that none of your test input remains in the handoff.
</important>

Report the verification method and any unverified behavior, such as whether an answer reached Dossier. A successful push or local rendering alone does not establish persistence.
