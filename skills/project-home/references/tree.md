# The project tree

The project tree contains the home, goals and their stage outputs, and the glossary. This skill maintains the root, shared pages, and kit. Use `visualize-html` to build those pages and kit files in the project's design language. The requirements below define their behavior while leaving visual choices to that skill.

## What lives where

```text
<workspace>/<tree>/
  index.html           project home
  _layout.html         shared layout
  _theme.css           shared theme
  _fonts/              font files
  _components/         shared components
  .dossierignore       excludes dot files and private/ folders
  goals/
    index.html         goals page
    goals.json         goal list
    <slug>/            goal and its stage outputs
  glossary/
    index.html         glossary page
    glossary.json      terms
    _check.mjs         the glossary check
  requirements/<slug>/ a requirements interview: ledger and owner report for the team,
                       and customer/, the only part shared with the customer
  architecture/        the project's architecture: interview, ARCHITECTURE.md, adr/
  architecture-review/ architecture review passes and the register of their candidates
  research/<slug>/     research without a goal
  pr-<slug>/           a pull request's description and walkthrough, without a goal
  <slug>-interview/    other interviews without a goal, such as a brainstorm
  brand/               the brand's overview page, once the project has a brand
  brand-interview/     the brand interview, while a brand is being developed
  notes/<username>/    each person's notes, visible to the team
  drafts/              this skill's drafts under review
```

Draft pages mirror their published counterparts. After acceptance, move them to these destinations:

| Draft | Published destination |
|---|---|
| `drafts/home/index.html` | `index.html` |
| `drafts/goals/index.html` | `goals/index.html` |
| `drafts/glossary/index.html` | `glossary/index.html` |
| `drafts/brand/` | `brand/`, including the overview's dependencies |
| Other restyled pages under `drafts/`, mirroring their tree paths | Corresponding published paths |
| Changed kit files under `drafts/` | Corresponding paths at the root |

A new tree's first draft includes all three pages and the kit, plus the brand overview when a brand exists. Keep the goal list and glossary terms at their permanent data paths throughout review.

To support both draft and published locations:

- read data with paths relative to the tree root, such as `dossier.read('/goals/goals.json')` and `dossier.read('/glossary/glossary.json')`;
- construct links to tree pages using the current page's depth from `dossier.page.path`.

Links written directly in page markup resolve from that page's folder. Recheck them after moving the page to its published location.

An exported copy holds only its page's folder, so a draft that reads the goal list or glossary shows them empty there. Verify those drafts on the published tree; an export alone leaves that check outstanding.

Each part has one writer, but every writer publishes the same way: it brings the whole local copy up to date with `dossier pull --merge`, writes its part, and pushes the whole copy to the tree's root, as the continuity reference describes.

| Part | Written by |
|---|---|
| The home, kit, goals page, glossary page | project-home |
| `brand/` | project-home publishes a copy; the brand skill owns the identity and canonical resources |
| `brand-interview/` | brand-skill-generator, which removes it once the brand skill exists |
| `goals/goals.json` | basecamp adds each goal and marks it done; project-home removes goals on cleanup |
| `goals/<slug>/` | basecamp and that goal's stages |
| `glossary/glossary.json` | the stage that settles terms, and basecamp |
| `requirements/<slug>/` | requirements gathering, in `conversational-interview` or `design-interview` |
| `architecture/` | design-interview, Solution Architecture profile |
| `architecture-review/` | architecture-review |
| `research/<slug>/` | research |
| `pr-<slug>/` | describe-pr |
| `<slug>-interview/` | design-interview profiles other than Solution Architecture and requirements gathering, and brainstorming in `conversational-interview` |

Link the project home to `architecture/` and `architecture-review/` when each is present.

Dossier automatically excludes only `.git`, `node_modules`, and `.DS_Store`. The root `.dossierignore` excludes at least dot files (`.*`) and `private/` folders at any depth. A `private/` folder is never published or synced, so it stays on the machine where it was written; any skill or agent may use one for material that must not leave that machine. Everything else is published and visible to the team, including each person's notes in `notes/<username>/`. The ignore file is never uploaded, so write it again on every new or recovered local copy.

A push may hold at most 2,000 files and 500 MiB in total, counted over the whole copy even though only changed files upload. Demo videos use most of that budget; removing finished goals keeps the tree within it. A push over the limit fails and names it.

## The kit

The kit supplies shared navigation and a consistent visual foundation. Individual pages can develop their own design within it.

**Root layout.** `_layout.html` includes the project name linked to the home, breadcrumbs derived from `dossier.page.path`, `<dossier-notifications>` for mentions and replies, the command palette, and the term hints. Hide this shared navigation when a page is embedded, using an `html[data-dossier-embedded]` rule. Goal layouts nest inside the root layout and are owned by basecamp.

**Theme.** `_theme.css` defines variables for Dossier components and project pages: shadcn roles such as `--background`, `--primary`, `--border`, and `--radius`, plus `--font-display`, `--font-body`, and `--font-mono`. Store font files in `_fonts/`. Keep bare element selectors out of the shared theme so pages control their own styling.

Shared components and kit CSS use the theme's variables for colours, radii, and fonts, so changes to `_theme.css` carry the brand across the kit.

**Components.** Keep the command palette, front matter reader, and other shared components in `_components/`. Give each a sibling `.md` usage note for authors to discover through `dossier read`.

**Bundled kit code.** Copy the dependency-free modules from [`assets/kit/_components/`](../assets/kit/_components/) into the tree's `_components/` when creating the kit:

- `project-palette.js`, with its `project-palette.md`: the command palette element.
- `project-term-hints.js`, with its `project-term-hints.md`: marks each glossary term's first mention on a page and shows its definition in a popover.
- `projectdata.js`: reads the goal list, goal records, and glossary by tree-root paths, and builds relative links.
- `frontmatter.js`: the front matter reader.
- `fuzzy.js`: ranking and match highlighting, for the palette and the glossary page.

The components' styles use the `project-kit` cascade layer. Customize them through the hooks in their usage notes when the design needs it. Only hyphenated file names in `_components/` are component tags, so the three helpers load only when imported. Pages import them from their own folder, such as `./_components/projectdata.js`, and Dossier serves the closest copy. Each file begins with its version. When changing the kit of an existing tree, compare those versions with the bundled files and offer the newer ones.

<important if="a draft changes the shared kit">
Place changed kit files under `drafts/`. Dossier uses the nearest `_` file, and a complete-document `drafts/_layout.html` replaces the root layout for draft pages. This lets the user review the new kit before it affects published pages.

Components resolve module imports relative to their own location. When changing a shared module, copy every component that imports it into `drafts/` too. Otherwise, the published component continues loading the published module and the draft shows the previous behavior.
</important>

## Apply the project's brand

The project's brand skill, created with `brand-skill-generator`, governs its identity and stays independent of Dossier. Its kit holds `index.html`, the brand overview, with `styles.css`, `tokens/`, and `assets/`. The tree publishes a copy of that overview and applies the brand to its presentation.

<important if="creating a tree for a branded project, applying a brand to an existing tree, or updating its brand">
Read the project's brand skill and its relevant application guidance before preparing changes. Use `visualize-html` to apply the established identity through the usual draft review:

1. Copy the overview and its dependencies into `drafts/brand/`, preserving their relative paths, with the kit's `brand-card.md` beside it, named as the overview's agent version (`<link rel="alternate" type="text/markdown" href="brand-card.md">`). Keep it a complete document with its own design, so the tree's layouts do not wrap it.
2. Prepare the theme and font changes under `drafts/`, mapping the brand's roles onto the kit's theme variables using its canonical tokens and fonts.
3. Restyle the home, goals page, and glossary page. Identify other pages that should adopt the brand and prepare their drafts at the paths listed above. Restyle pages owned by other workflows yourself, keeping their content, interactions, and deliberate visual exceptions, such as a mockup demonstrating another design.

Review the overview, shared kit, and all restyled pages together. After acceptance, promote their files using the draft mapping. Verify every changed page at its published location, including loaded styles, fonts, assets, links, and interactions. Report which pages were updated and any deliberate exceptions.
</important>

## Front matter

Markdown records, including each goal's `GOAL.md`, store data in YAML front matter using values, lists, and one level of nesting. Read it with the kit's `frontmatter.js` wherever a page or component reads these records.

From a goal's front matter, the goals page and the palette read `stage`, `next`, `waiting`, and `pages`. `pages` lists the goal's stage pages, each as a `title` and a `path` relative to the goal's folder.

## The goals page

`goals/index.html` shows every goal at a glance:

- its title;
- its current stage and next step;
- any action needed from the owner;
- a link to its page.

Name `goals.json` as the goals page's agent version with `<link rel="alternate" type="application/json" href="goals.json">`, so an agent reading the page's link gets the goal list.

Read `goals/goals.json` and each listed goal's `GOAL.md` front matter at runtime with the kit's `projectdata.js`. This keeps progress current when basecamp publishes a goal, without rebuilding the page. The home can use the same data.

`goals/goals.json` holds `{ "goals": [ … ] }`. For each goal it records the `slug`, `title`, `link`, `opened` date, and `status` (`open` or `done`). basecamp adds a goal when it opens and marks it done when it finishes. This skill removes goals the user cleans up, and creates the file, empty, with the tree. Goal-list changes need no home-page review and no change to the home's summary.

<important if="the user deletes completed goal folders from the local copy">
Remove those goals from the list, and any terms they still propose from `glossary/glossary.json`, then publish; the push removes them from Dossier. Report which goals were removed and how to recover them: `dossier restore <workspace>/<tree>/goals/<slug>/ --to <time before the push>`. Restoration is available within the retention period, which defaults to 30 days unless the deployment configures another duration.
</important>

## The glossary page

**Terms.** `glossary/glossary.json` is the source of truth for project vocabulary. Declare it as the page's agent-readable version with `<link rel="alternate" type="application/json" href="glossary.json">` so `dossier read <workspace>/<tree>/glossary/` returns it unchanged.

```json
{
  "version": 1,
  "contexts": [
    { "id": "ordering", "name": "Ordering", "about": "Receives and tracks customer orders." },
    { "id": "billing", "name": "Billing", "about": "Invoices customers for their orders." }
  ],
  "terms": [
    { "id": "ordering.order", "term": "Order", "definition": "A customer's request to buy items.",
      "example": "Order 104 contains two Line Items.",
      "avoid": ["purchase"],
      "related": [{ "to": "ordering.line-item", "how": "has many" }, { "to": "billing.invoice", "how": "leads to" }],
      "context": "ordering", "status": "current", "since": "2026-10-01" },
    { "id": "ordering.order", "term": "Order", "definition": "A confirmed request to buy items.",
      "example": "Order 104 contains two Line Items.", "avoid": ["purchase", "basket"],
      "related": [{ "to": "ordering.line-item", "how": "has many" }, { "to": "billing.invoice", "how": "leads to" }],
      "context": "ordering", "status": "proposed", "goal": "checkout-redesign", "since": "2026-10-15" },
    { "id": "ordering.line-item", "term": "Line Item", "definition": "One product and its quantity within an Order.",
      "avoid": [], "context": "ordering", "status": "current", "since": "2026-10-01" },
    { "id": "billing.invoice", "term": "Invoice", "definition": "A request for payment for an Order.",
      "avoid": [], "context": "billing", "status": "current", "since": "2026-10-01" }
  ]
}
```

- **Stable identity.** Set `id` to `<context id>.<slug>` when adding a term and keep it across revisions. A rename adds the previous name to `avoid`.
- **One concept, one name.** Within a context, each concept has one preferred name, and each name identifies one `id`. A project with one context still has an entry in `contexts`.
- **Examples.** The optional `example` is one sentence using the term in context to distinguish it from similar terms.
- **Relations.** The optional `related` list records relationships within or across contexts. Each `{ "to": "<term id>", "how": "<short verb phrase>" }` reads as a sentence, such as "Order *leads to* Invoice". Record relationships here; a relation change follows the same proposal rules as any other term change.
- **Current and proposed entries.** An `id` has at most one `current` entry and one `proposed` entry. A proposal names its `goal`; a current entry omits that field. A proposal without a current entry introduces a new term. If another goal already proposes a change to the same `id`, raise the conflict with the user and wait for the goals' owners to agree before changing it.
- **Validation.** Copy [`assets/glossary/_check.mjs`](../assets/glossary/_check.mjs) into the tree as `glossary/_check.mjs`. Follow the `AGENTS.md` publish commands to check changes and correct reported problems before publishing. The script checks fields, duplicate names and entries, relation targets, and conflict markers. For a rename proposal, it checks the old name against the current entry's name. Authors remain responsible for preserving identity across published revisions and distinguishing concepts. When updating an existing tree's glossary, compare the check script's version with the bundled version and offer the newer one.

**Page.** `glossary/index.html` reads terms at runtime so vocabulary changes require no page rebuild. Group current and proposed entries under one element per term `id`, using that value as its HTML `id` for direct links. Show each definition with its example and related-term links, and label proposals with their goals. Choose a presentation that explains the relations, such as a small map. Provide fuzzy search across terms, definitions, and avoided words, a quick way to copy a term, and each term's context. Place `<dossier-comments for="<term id>">` beneath each term so the team can discuss its meaning and proposed changes.

**Ownership.** This skill creates the version 1 file and imports any existing glossary as described below. A new glossary starts with one project context and no terms. `design-interview` settles terms and folds in comments on its proposals; at handoff it writes proposed entries for a goal or current entries for an interview without a goal. `basecamp` promotes a goal's proposals when the goal completes. Cleanup removes proposals belonging to deleted goals. Each writer uses the project's publish commands, including checking the glossary after resolving a merge conflict.

<important if="the repository has a glossary">
Import every term and context from `GLOSSARY.md`, or the glossaries listed in `GLOSSARY-MAP.md`, into `glossary.json` as `current`, giving each term its `id`. Preserve definitions exactly. Then replace those files' contents with a link to the glossary page, so the project keeps one source of terms.
</important>

<important if="creating the glossary in a tree that already holds completed interviews">
An interview that finished before the glossary existed kept its agreed terms in its frozen ledger's Language list. Scan the tree's ledgers and include those terms in the new `glossary.json` as `current`, from interviews whose profile writes the glossary at handoff, preserving each definition exactly. Requirements gathering and brainstorming leave the glossary unchanged, so their terms stay out.
</important>

## The command palette

Provide navigation across the tree through a command palette in the root layout: place the bundled `<project-palette>` there and style it, modelled on [shadcn's Command](https://ui.shadcn.com/docs/components/base/command), in the project's design language. The behaviour below is what the bundled element does; it stays the definition of correct behaviour if a project changes or replaces it.

- **Navigation search.** Open with Cmd+K, or Ctrl+K on other systems. Search the home, goals page, glossary page, every goal in `goals/goals.json` with its stage from `GOAL.md`, and the stage pages linked by each goal's record. Use fuzzy matching. Enter opens the selected page.
- **Glossary search.** Typing `gs` followed by a space switches to glossary mode and replaces the prefix with a **Glossary** chip. Search terms, definitions, and avoided words from `glossary/glossary.json`. Enter copies the selected term. Backspace on an empty query removes the chip.
- **Fresh data.** Load sources when the palette opens so newly listed goals are available immediately.
- **Accessibility.** Support all actions from the keyboard and announce results to screen readers.
