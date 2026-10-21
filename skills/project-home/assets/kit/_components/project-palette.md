# project-palette

A command palette for project navigation and glossary search. It provides keyboard interaction and accessibility, with colours, fonts, and radii drawn from the theme's variables.

## Use

Place it once in the root `_layout.html`:

```html
<project-palette></project-palette>
```

It renders its own trigger button. To supply your own trigger, put a child with `data-part="trigger"` inside it.

Optional attributes:

- `label`: the trigger's text, `Search` by default;
- `placeholder`: the input's text in page search;
- `glossary-placeholder`: the input's text in glossary search;
- `dialog-label`: the dialog's accessible name.

## Behaviour

- **Opening.** Cmd+K or Ctrl+K toggles it, except on embedded pages. The trigger opens it too.
- **Page search.** It searches the home, the goals page, the glossary page, every goal in `/goals/goals.json` with its stage from `GOAL.md`, and the pages each goal's record lists under `pages`. Enter opens the result; Cmd or Ctrl with Enter opens it in a new tab.
- **Glossary search.** Typing `gs` then a space switches to glossary search and shows the Glossary chip. It searches terms, avoided words, and definitions from `/glossary/glossary.json`. Enter copies the term. Backspace on an empty input returns to page search.
- **Navigation.** Arrow keys move through the results, and Escape closes it.
- **Screen readers.** The input is a combobox over a listbox. Result counts and copies are announced through a polite live region.
- **Loading.** Data is read each time the palette opens, so newly listed goals appear at once.

## Styling hooks

These are attributes on elements inside `<project-palette>`, all in the page's own DOM:

| Hook | Element |
|---|---|
| `[data-part="trigger"]` | the trigger button, which holds a `<kbd>` |
| `[data-part="dialog"]` | the native `<dialog>`; style its `::backdrop` too |
| `[data-part="field"]` | the row holding the chip and the input |
| `[data-part="chip"]` | the Glossary chip, hidden in page search |
| `[data-part="input"]` | the search input |
| `[data-part="list"]` | the listbox |
| `[data-part="item"]` | each result, with `[data-active]` on the active one, `data-kind` (`page`, `goal`, `goal-page`, `term`), and `data-status` |
| `[data-part="title"]`, `[data-part="detail"]` | each result's text, with matches in `<mark>` |
| `[data-part="badge"]` | the context when the project has several, and the originating goal for a proposal |
| `[data-part="empty"]` | the no-results or loading message |

The element itself carries `data-mode` (`pages` or `glossary`) and `data-state` (`loading`, `ready`, or `error`).

Styles use the `project-kit` cascade layer and theme variables: `--popover`, `--popover-foreground`, `--foreground`, `--background`, `--border`, `--radius`, `--accent`, `--accent-foreground`, `--muted-foreground`, `--primary`, `--ring`, `--font-body`, and `--font-mono`. The kit can customize them through the hooks above.

## Shared modules

The palette imports three unstyled helpers beside it, which pages can use too. A page imports them from its own folder, and Dossier serves the closest kit copy:

```js
import { loadGoals, loadGlossary, loadRecord, linkTo } from './_components/projectdata.js'
import { rank, highlight } from './_components/fuzzy.js'
import { parseFrontMatter } from './_components/frontmatter.js'
```

- `projectdata.js` reads the goal list with each record's front matter, the glossary, or any record, by paths from the tree's root. `linkTo` builds a relative link to a tree path from the current page.
- `fuzzy.js` ranks items by a query across weighted fields, and highlights the matches.
- `frontmatter.js` parses a Markdown record's YAML front matter.

## Versions

Each file starts with its name and version. When changing the kit, compare these with the copies bundled with the `project-home` skill.
