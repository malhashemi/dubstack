# project-term-hints

Underlines the first mention of each glossary term and shows its definition in a popover on hover or tap. CSS highlights mark the text without wrapping or replacing page nodes, preserving the elements used by page scripts. Colours, fonts, and radii come from the theme's variables.

## Use

Place it once in the root `_layout.html`, beside `<project-palette>`:

```html
<project-term-hints></project-term-hints>
```

- `scope`: a selector for the area to mark. By default, it uses `main` when present, otherwise the body. Content outside that area is left alone.
- `data-term-hints="off"` on any element keeps its contents unmarked, such as a mockup or a quoted transcript.

## Behaviour

- It reads `/glossary/glossary.json` through `projectdata.js`, matching current and proposed names. Plurals ending in "s" or "es" count. Word boundaries include letters, digits, and combining marks, so matches stay outside longer words, including Arabic words with diacritics.
- It skips links, buttons, headings, code, form fields, and Dossier's own components, and marks again when page code changes the text.
- The popover shows the term's definition, any example, words to avoid, related-term links, and its context when the project has several. A name shared across contexts shows each meaning. Proposals name their originating goals; changes to current terms show the proposed name and definition beside the current entry. A link opens the term on the glossary page.
- Moving the pointer into the popover keeps it open. A tap elsewhere, Escape, scrolling, or resizing closes it.
- It is a pointer aid. Keyboard and screen reader users reach the same terms through the palette's glossary search (`gs` then a space) and the glossary page.
- A browser without CSS highlights shows no hints; the page is otherwise unchanged.

## Styling hooks

| Hook | Element |
|---|---|
| `::highlight(project-term)` | the underline on each marked mention |
| `html[data-project-term-hover]` | set while the pointer is over a marked mention |
| `[data-part="term-popover"]` | the popover |
| `[data-part="term-meaning"]` | one meaning of the term, one per context |
| `[data-part="term-name"]`, `[data-part="term-definition"]`, `[data-part="term-example"]`, `[data-part="term-avoid"]`, `[data-part="term-related"]`, `[data-part="term-context"]`, `[data-part="term-status"]`, `[data-part="term-proposal"]`, `[data-part="term-link"]` | the popover's contents |

Styles use the `project-kit` cascade layer and theme variables: `--popover`, `--popover-foreground`, `--foreground`, `--border`, `--radius`, `--muted-foreground`, `--primary`, and `--font-body`. The kit can customize them through the hooks above.
