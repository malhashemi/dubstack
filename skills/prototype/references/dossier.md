# Dossier publishing for prototypes

Before authoring, read `dossier --agent-info` as the authority on page rules and commands, and run `dossier read` on the prototype's destination folder (or its parent if it does not exist yet) to see the theme variables, fonts, and components the tree already provides, since they carry the project's brand. This reference covers the constraints that are easy to miss when publishing, sharing, commenting on, or exporting a prototype in a project's Dossier tree.

## Stand outside the tree's layout

A project's Dossier tree wraps body pages in its own site layout and navigation. A prototype must render as the product, not inside the documentation shell:

- Write complete HTML documents (with `<!doctype html>` or `<html>`), which bypass every layout above them, or
- Place a complete-document `_layout.html` in the prototype folder whose `<body>` holds only `<slot></slot>`, opting every body page in that folder out of outer layouts.

## Paths, links, and files

- Use lowercase filenames and relative links (such as `href="checkout"` or `href="billing/"`, omitting `.html` on page links).
- Never include `<base>`: Dossier refuses pushes containing `<base>`.
- When a page is shared on its own, Dossier includes files its markup loads (`<img>`, `<link>`, `<script>`, `<iframe>`) and ancestor `_` files, but not files referenced only from inside a stylesheet or script (such as CSS background images, imported JS modules, or URLs built at run time). Those travel with a shared page only when they are `_` files or when the folder itself is shared. Always share the prototype's folder rather than a single page.

## Scope browser storage

Every page in a Dossier tree runs on that tree's single browser origin, sharing `localStorage`, `sessionStorage`, and IndexedDB. Prefix every storage key with the prototype's folder path (not `dossier.page.path`, which is one page's path) so a multi-page prototype's pages share state with each other and with nothing else in the tree. Include a visible way to reset simulated state back to the starting scenario.

## Comments on screens and mockups

- Add `<dossier-comments></dossier-comments>` so anyone with `respond` can comment, reply, @mention, and resolve or reopen threads, while anyone with `read` can read them.
- Use `<dossier-comments for="<id>"></dossier-comments>` beside an element with matching `id="<id>"` to anchor threads to a screen or region, and `pins="…"` on a whole-page `<dossier-comments>` when viewers should pin comments directly onto visual regions or mockups.
- Keep element `id` values stable across pushes: threads stay attached while the `id` exists and move under "On an earlier version" if it disappears.
- Comments live beside the page in `<page>.comments/` (such as `index.comments/` for `index.html`). Pass `--json` to `dossier read <page>.comments/` to get each thread's root comment path for `dossier comment <page> --resolve <path>`.

## Sharing and history

- Apply shares to the prototype folder with `dossier share`. Roles add up across shares, and a share on a folder covers everything inside it and cannot be narrowed on a child node.
- Commenting requires the viewer to be signed in and to hold `respond`. A public `anyone` share with `read` opens without sign-in, letting viewers read comments but not write them, so the role to ask the user for depends on whether the viewer should be able to comment.
- Every push is recorded as a version in the tree's history, inspectable with `dossier log` and `dossier diff` and restorable with `dossier restore`.

## Offline export

`dossier export <link> -o <file>` saves one page as a single offline HTML file with its assets and a snapshot of readable comments inlined (files over 50 MiB keep their largest media as links to the deployment, and URLs built dynamically by script are not inlined). Because export packages a single page, a prototype that must reach someone who cannot open Dossier needs to be built as one page (switching screens inside it rather than linking across separate `.html` files). An exported copy keeps what a person enters in that browser only, so comments do not come back from it.
